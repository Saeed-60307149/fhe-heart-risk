# Architecture – v1.0 (final, submitted 15 Nov 2026)

> **Aligned with the corrected Defense Report (reference, decision #26).** Updated from Architecture v1.0 (15 Nov): **the user is now the hospital**; the browser sigmoid is the main output; the layout is one ciphertext per feature.

Owner: Abdullah Dar · Practicum (Capstone 1) · Supervisor: Dr. Abdulatif Shikfa · history: v1 draft
Week 10 (26 Oct) → v2 repo draft 11 Nov → **v1.0 final document 15 Nov** (the submitted PDF is numbered
from 1.0). Diagram source: [diagrams/architecture.md](diagrams/architecture.md) (Mermaid, renders on
GitHub); the Week 10 PNG is in `members/abdullah-dar/images/architecture.png` (the submitted Figure 1 is in the PDF only). Security
analysis: [threat-model.md](threat-model.md).

## Purpose and design rule

A hospital gets a heart disease risk prediction without the server ever seeing the patient's health data. The
hospital encrypts 13 clinical features in the browser and keeps the secret key. The server computes the
risk score on the ciphertext with CKKS and returns an encrypted score that only the hospital can decrypt.

**Design rule: plain data and the secret key exist only in the hospital's browser. Every server-side
component handles ciphertext, public keys and model weights only.** Trust boundary: the browser is trusted;
gateway, FHE service, logs and disk are untrusted for patient data.

## Parts

| # | Part | Runs where | Stack | Responsibilities | Holds |
|---|---|---|---|---|---|
| 1 | **Hospital client** (Plan A: browser page; Plan B: local Python CLI) | Hospital's device | HTML/JS + node-seal 7.0.0 (SEAL 4.1.2, WASM; Node.js 22+ or a current browser) · or Python + TenSEAL 0.3.16 | Generate CKKS keys; scale and encrypt the 13 features; send ciphertexts and public keys; decrypt the encrypted score; apply the low/high-risk threshold | **Secret key** (memory only), plain features, plain score |
| 2 | **Gateway** (Node.js API) | Server, public (behind TLS) | Express 4, Node 22 | Serve the front end; TLS; authentication; rate limiting; check request size, format and encryption parameters; route requests (no cryptography) | Ciphertext in transit only; API tokens |
| 3 | **FHE-ML service** | Server, localhost/private only | FastAPI + TenSEAL 0.3.16 (`sealapi`) | Load the public context; compute weighted sum, bias and cubic polynomial sigmoid on ciphertext; return the encrypted score | Plain model weights, public context, evaluation keys. **Never the secret key** |
| 4 | **Model files** | In the repository | scikit-learn logistic regression | Weights, bias and scaler per dataset (UCI Cleveland: 13 features; Edinburgh MI: 9 features) | Model parameters only. No patient data |

```
[1 Hospital client] --HTTPS: parms + n ciphertexts (+ relin keys)--> [2 Node API] --localhost--> [3 FHE-ML service]
       ^                                                                                    |
       +--------------------- encrypted score (ciphertext) <-------------------------------+
   decrypt locally -> threshold 0.5 -> "Lower / Higher risk"
```

## Request flow (`POST /api/predict`)

1. Client calls `GET /api/model/{dataset}`: feature order, scaler, CKKS parameters, threshold.
2. Client creates CKKS keys **in the browser** (N = 16384, moduli [60,40,40,40,40,60], scale 2^40, 128-bit).
3. Client scales each raw answer `(x − mean) / scale` and encrypts it into its own ciphertext.
4. Client sends `parms`, the `n` ciphertexts and (for server-side sigmoid) the relinearization keys.
5. Node API: token check → rate limit → size and base64 checks → drops unknown fields → forwards.
6. FHE service: SEAL validates parameters and ciphertexts → `z = Σ wⱼ·ctⱼ + b` (1 level) →
   optional cubic `p(z) = c₀ + c₁z + c₃z³` (2 levels, relinearized) → returns the ciphertext.
7. Client decrypts with its secret key and shows the risk. The server never sees `x`, `z` or `p(z)`.

## Who holds what

| Item | Where | Leaves the client? | Notes |
|---|---|---|---|
| Secret key | Client memory only | **Never** | New keys per page load / per CLI run |
| Encryption parameters | Client → server | Yes (≈100 bytes) | Public |
| Relinearization keys | Client → server | Add-on mode only (about 685 KB) | Public evaluation keys; cannot decrypt |
| Galois (rotation) keys | – | Not used | Needed only by the packed layout (comparison only) |
| Encrypted features / score | Client ↔ server | Yes | Ciphertext only |
| Model weights, polynomial | FHE service | No | Server asset; not returned by `/api/model` |
| Scaler mean/scale | Server → client | Yes | Public; needed to scale before encrypting |

## Cryptographic parameters (web system, updated 27 Nov from the benchmarks)

| Mode | N | Modulus chain (bits) | Scale | Why |
|---|---|---|---|---|
| **Main: browser sigmoid** | 4096 | 46 / 46 | 2^26 | Smallest passing per-feature setting: 100% decision match, score error ≤ 0.01, 128-bit security |
| Add-on: server cubic | 8192 | 31 / 26 / 26 / 26 / 31 | 2^26 | Smallest passing per-feature setting for the cubic |
| Pilot (PR2 history) | 16384 | 60 / 40 / 40 / 40 / 40 / 60 | 2^40 | Used by the pilot scripts only |

CKKS; node-seal 7.0.0 and TenSEAL 0.3.16 (pinned). The browser uses **seeded secret-key encryption** and **zstd
compression**. The web service accepts **only these two exact parameter sets**. The cubic is a least-squares fit
(mean absolute error 0.0356 on the Cleveland test set in the 11 Nov and later runs; PR2 reported 0.031).
Source: [`code/fhe-ml-service/fhe_heart/params.py`](../code/fhe-ml-service/fhe_heart/params.py).

## Ciphertext layout: one ciphertext per feature

| (Cleveland, N=4096, seeded + zstd) | Per-feature (**delivered**) | Packed (comparison only) |
|---|---|---|
| Upload per patient | 354 KB | 30 KB |
| Rotation keys (sent once) | none | 241 KB (only steps 1, 2, 4, 8) |
| Other slots of the result | nothing useful | partial sums that reveal model weights unless masked |

The server module supports both layouts; the web page and API use per-feature (#15, #26). The benchmarks show packed
is lighter; see FINAL-PLAN section 11 for the open team decision. In the PR2 pilot, packed looked heavy because it used
the full default set of rotation keys (164 MB).

## Plan B (fallbacks only)

Run node-seal on a Node.js server instead of the browser, or encrypt in a local Python client
(`code/client-python/`). The server-side design stays the same, but the "encrypt in the browser" claim is
weakened.

## Pilot evidence behind the design (UCI Cleveland, 75-patient test split; PR2 Table 5)

| Measurement | Value |
|---|---|
| Key generation (one-off) | 1.18 s |
| Encrypt / infer / decrypt per patient (TenSEAL, packed) | 13.3 / 87.5 / 3.5 ms |
| node-seal encryption in the client (Node.js 22) | 33.4 ms per feature (434 ms per patient) |
| Plain vs encrypted accuracy | 0.853 vs 0.853 (ROC-AUC 0.947) |
| Public context / Galois keys | 7.7 MB / 163.9 MB |

Edinburgh MI and per-feature end-to-end timing are the first benchmarks of the next phase
([benchmark-plan.md](benchmark-plan.md)). The 11 Nov official run (`code/results/`) reproduced the
accuracy, AUC and sizes; timings depend on the machine; the public context is 7.54 MiB (7.9 MB decimal).

## Interfaces

The submitted PDF lists two endpoints in short form: `POST /predict` (public context, 13 ciphertexts,
dataset id → one encrypted score) and `GET /health` (status only, no patient or model data). In the
implemented contract v2 these are `POST /api/predict` and `GET /api/health`, plus `GET /api/model/{dataset}`
(feature order, scaler, CKKS parameters, threshold; weights are never returned). The contract in
[api-contract.md](api-contract.md) and [openapi.yaml](openapi.yaml) is authoritative.

## Build order for Capstone 2

1. Front end, gateway and a plaintext baseline app.
2. Real FHE pipeline: node-seal encryption in the browser, TenSEAL on the server, per-feature layout.
3. Security hardening and testing against the [threat model](threat-model.md).
4. Benchmark plaintext against FHE on both datasets, then polish and demo.

The skeleton in `code/` already covers steps 1 and 2 (11 Nov); step 3 has the open items in the threat
model's "Status in `code/`" column.

## Decisions recorded (see `planning/decision-log.md`)

| Decision | Status | Evidence |
|---|---|---|
| Scheme: CKKS | Final (#1) | Real-valued features |
| Client: **Plan A (node-seal in the browser) works**; Plan B (Python CLI) kept as fallback | Final (#12) | PR2 cross-library round trip; `code/frontend` tested in headless Chrome 11 Nov |
| Versions pinned: node-seal 7.0.0, TenSEAL 0.3.16, Node.js ≥ 22 | Final (#13) | PR2 compatibility test |
| Ciphertext layout: one ciphertext per feature | Final (#15, #26) | Packed is measured for comparison only. Pilot: packed about 1 MB per patient but 164 MB of full-set Galois keys; per-feature about 13 MB per Cleveland patient (Python client) |
| Sigmoid on server (encrypted cubic) vs on client (after decrypt) | **Browser sigmoid is the main output (#24)**; the server cubic stays as a measured add-on (`output` field) | Client-side reveals the score only to the patient and needs 1 level and no relin keys; server-side needs relin keys + 2 more levels |

## Capstone 2 backlog (engineering items, not open decisions)

- **Upload size**: done (27 Nov): seeded + zstd at the approved small settings (about 354 KB per Cleveland patient per-feature in browser-sigmoid mode, from 16.3 MB). Open: the team decision on packed (FINAL-PLAN section 11).
  SEAL `zstd` compression (test on both libraries), N = 8192 with `output = "logit"` (smaller
  ciphertexts, no relin keys; sigmoid on the client), or packing several features per ciphertext
  with a few targeted Galois keys only.
- **Key reuse**: today keys are regenerated per page load. Keeping them in IndexedDB would cut the
  per-request upload of relin keys, but stores a secret key at rest; decide with the threat model (T3).
- **Result integrity**: the client cannot verify the server used the real model; CKKS gives no integrity
  (threat model T6). Add the client-side range check.
