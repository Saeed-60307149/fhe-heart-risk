# API Contract – v2

Owner: Abdullah Dar · v1 drafted 26 Oct 2026 (2 endpoints, 7 error codes), updated with Saif's
pilot details 29 Oct · **v2: 11 Nov 2026**, aligned with the implemented prototype in `code/` and
the PR2 pilot (per-feature layout, node-seal 7.0.0 ↔ TenSEAL 0.3.16).
Machine-readable version: [openapi.yaml](openapi.yaml). Tests that enforce this contract:
`code/backend/test/app.test.js` (public API) and `code/fhe-ml-service/tests/test_api.py` (internal).

## 1. What changed from v1

| v1 (26–29 Oct) | v2 (11 Nov, final) | Why |
|---|---|---|
| `POST /api/predict` body `{ context, encrypted_features }` (one packed ciphertext + public context) | `{ dataset, parms, ciphertexts[], relin_keys?, output }` – one ciphertext per feature | Per-feature layout needs no Galois keys (PR2: 164 MB). `parms` (≈100 bytes) replaces the 7.7 MB public context. |
| 2 endpoints | 3 public endpoints (added `GET /api/model/{dataset}`) | The browser needs the feature order, scaler and CKKS parameters before encrypting. |
| 7 error codes | 8 public codes (section 4) – final (decision #18) | Added `RATE_LIMITED` (runbook step 26) |
| – | Bearer-token auth, 48 MB body limit, rate limit, metadata-only logs | Runbook step 26, threat model T3–T6. |

## 2. Public API (browser / Plan B client → Node.js API)

Base URL: `https://<host>` (TLS required outside localhost). All bodies are JSON (UTF-8).
Every response carries `X-Request-Id`.

| Method | Path | Auth | Body | Success |
|---|---|---|---|---|
| GET | `/api/health` | – | – | `200 { "status": "ok", "fhe_service": "ok" \| "unavailable", "version": "2.0.0" }` |
| GET | `/api/model/{dataset}` | – | – | `200` model metadata (2.1) |
| POST | `/api/predict` | `Authorization: Bearer <token>` | 2.2 | `200` 2.3 |

### 2.1 `GET /api/model/{dataset}` → 200
`dataset` ∈ `cleveland`, `edinburgh` (pattern `^[a-z0-9_-]{1,32}$`).
```json
{
  "dataset": "cleveland",
  "feature_names": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
  "n_features": 13,
  "scaler_mean": [54.4, 0.68, "…"],
  "scaler_scale": [9.0, 0.47, "…"],
  "threshold": 0.5,
  "param_set": "n16384_depth4",
  "params": { "poly_modulus_degree": 16384, "coeff_mod_bit_sizes": [60, 40, 40, 40, 40, 60] },
  "scale_bits": 40,
  "supports_probability_poly": true
}
```
The model **weights are not returned** (they are a server asset, threat model A3).

### 2.2 `POST /api/predict` request
```json
{
  "dataset": "cleveland",
  "parms": "<base64 SEAL EncryptionParameters, CKKS, no compression>",
  "ciphertexts": ["<base64 ciphertext of scaled feature 1>", "…", "<feature n>"],
  "relin_keys": "<base64 SEAL RelinKeys>",
  "output": "probability_poly"
}
```
| Field | Rules |
|---|---|
| `dataset` | required; must have a model on the server |
| `parms` | required; base64; ≤ 4,096 chars; CKKS; degree 8192 or 16384; accepted by SEAL at 128-bit security |
| `ciphertexts` | required; 1–64 base64 strings; count must equal `n_features`; each ≤ 2,000,000 bytes decoded; fresh size-2 ciphertexts at the first level; order = `feature_names`; each holds one **scaled** value (`(raw − mean) / scale`) in slot 0 at scale 2^40 |
| `relin_keys` | required when `output = "probability_poly"`; ≤ 12,000,000 bytes decoded |
| `output` | `"logit"` (default; server returns encrypted z = w·x + b, client applies the sigmoid after decrypting) or `"probability_poly"` (server also applies the cubic sigmoid on ciphertext) |

Unknown fields are dropped by the API and never forwarded.
Typical size: 13 features × ≈1.7 MB base64 ≈ 22 MB, plus ≈10 MB of base64 relin keys for
`probability_poly`. Body limit: 48 MB.

### 2.3 `POST /api/predict` response → 200
```json
{
  "encrypted_result": "<base64 ciphertext, decrypt with the client's secret key>",
  "output": "probability_poly",
  "threshold": 0.5,
  "timings_ms": { "load_ms": 210.4, "compute_ms": 131.8, "serialize_ms": 3.1 },
  "request_id": "6f1c…"
}
```
Client: decrypt → slot 0 → if `output = "logit"` apply `1 / (1 + e^−z)`; else clip to [0, 1].
Risk is **high** when the value ≥ `threshold`.

## 3. Internal API (Node.js API → FHE-ML service, localhost only)

| Method | Path | Header | Notes |
|---|---|---|---|
| GET | `/health` | – | `{ "status": "ok", "models": ["cleveland", "edinburgh"] }` |
| GET | `/model/{dataset}` | `X-Internal-Token` | same body as 2.1 |
| POST | `/infer` | `X-Internal-Token` | body = 2.2 plus `"layout": "per_feature"`; response = 2.3 without `request_id` |

The FHE service must bind to `127.0.0.1` (or a private network) and is never exposed publicly.
`X-Internal-Token` = env `FHE_SERVICE_TOKEN`, shared by both services.

## 4. Error codes

Every error is `{ "error": { "code": "<CODE>", "message": "<text>", "request_id": "<id>" } }`.
Messages never echo the request body.

| Code | HTTP | When |
|---|---|---|
| `BAD_REQUEST` | 400 | Not JSON; missing/invalid field; wrong ciphertext count; `probability_poly` without `relin_keys` |
| `UNAUTHORIZED` | 401 | Missing or wrong bearer token |
| `NOT_FOUND` | 404 | Unknown route or no model for `dataset` |
| `PAYLOAD_TOO_LARGE` | 413 | Body > 48 MB, or one ciphertext / key above its limit |
| `INVALID_CIPHERTEXT` | 422 | Not base64; SEAL rejects the parameters, ciphertext or keys; wrong level/size; transparent ciphertext; unsupported degree |
| `RATE_LIMITED` | 429 | More than `RATE_LIMIT_PER_MIN` (default 20) requests per minute per client; `Retry-After` header set |
| `INTERNAL_ERROR` | 500 | Unexpected failure (details only in the server log, never in the response) |
| `FHE_SERVICE_UNAVAILABLE` | 503 | FHE service not reachable or timed out (120 s) |

Internal-only codes from the FHE service are mapped: `UNSUPPORTED_PARAMETERS` → `INVALID_CIPHERTEXT`,
`MODEL_NOT_FOUND` → `NOT_FOUND`, internal `UNAUTHORIZED` → `INTERNAL_ERROR`.

## 5. Serialization decision (runbook step 10)

Ciphertexts, parameters and keys are SEAL's own binary format (`save` / `saveToBase64`, compression
`none`), base64-encoded inside JSON. Same format in node-seal 7.0.0 (SEAL 4.1.2) and TenSEAL 0.3.16
`sealapi`. Compression (`zstd`) would roughly halve the upload; not enabled until it is tested on
both libraries (open item in [architecture.md](architecture.md)).
