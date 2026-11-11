# Threat model – draft v1

Owner: **Naif** (runbook step 11; Gantt 3.6a/3.6b) · technical facts compiled by Naif in Week 10 and
from the PR2 pilot · draft structure 11 Nov 2026 · **status: draft for Naif to review and edit
before it goes into the final report.** Capstone 2 tests every row (runbook step 27).

## 1. Scope and assumptions

- System: patient client (browser with node-seal, or Plan B Python CLI) → Node.js API → FHE-ML
  service (TenSEAL). See [architecture.md](architecture.md).
- **Server model: honest-but-curious** (follows the protocol, but may read anything it stores or
  sees, and may be breached). Malicious-server behaviour is discussed in T7 but not prevented.
- The patient's device and browser are trusted. The CKKS parameters give 128-bit security
  (HE Standard; SEAL `tc128`).
- Data: public de-identified datasets only; no real patients (PR2 data statement).

## 2. Assets

| ID | Asset | Why it matters |
|---|---|---|
| A1 | Patient's raw answers (13 clinical features) | Health data (HIPAA/GDPR-type sensitivity) |
| A2 | The prediction (logit / probability / decision) | Reveals the patient's health status |
| A3 | Model weights, bias, sigmoid polynomial | Server's intellectual property; enables model-inversion attempts |
| A4 | Client secret key | Decrypts A1 and A2 |
| A5 | API tokens, internal service token | Access control |
| A6 | Service availability | FHE is expensive; easy to exhaust |

## 3. Threats and controls (STRIDE-style)

| ID | Threat | Asset | Control in the design | Implemented / tested in `code/` | Residual risk |
|---|---|---|---|---|---|
| T1 | **Compromised or curious server** reads patient data or result | A1, A2 | Server only receives CKKS ciphertexts; secret key never leaves the client | `fhe-ml-service/tests/test_no_secret_on_server.py` (no `Decryptor`/`SecretKey`/`decrypt` in server code); browser keeps the key in memory | Metadata (time, IP, dataset, request size) is visible |
| T2 | **Network eavesdropping / MITM** | A1, A2, A5 | TLS on the public API; FHE service bound to localhost | `backend/src/server.js` (HTTPS when `TLS_CERT/TLS_KEY` set, HSTS header) | Even without TLS, payload is ciphertext; tokens would leak |
| T3 | **Unauthenticated or abusive requests** | A6, A3 | Bearer token on `/api/predict`; internal token between services | `backend/test/app.test.js` (401 cases); `test_api.py::test_token_required` | Static tokens; no per-user accounts yet |
| T4 | **Malformed / malicious ciphertext or parameters** (crash, memory exhaustion, wrong-parameter attack) | A6 | Size limits, base64 checks, SEAL validation against the context, degree whitelist, level and size checks, transparent-ciphertext check | `test_seal_roundtrip.py` (garbage, wrong parameters, oversize), `app.test.js` (413/422) | SEAL parsing bugs (dependency risk) |
| T5 | **Denial of service** (FHE compute is ≈100–200 ms + large uploads) | A6 | Rate limit per client, 48 MB body limit, auth checked before the body is read, 120 s upstream timeout | `app.test.js` rate-limit and 413 tests | Single-process in-memory limiter |
| T6 | **Leakage through logs or error messages** | A1, A2 | Metadata-only access logs; errors never echo input; stack traces only server-side | `app.test.js` "access log holds metadata only"; `test_api.py::test_validation_error_does_not_echo_input` | Reverse-proxy logs must be configured the same way |
| T7 | **Malicious server returns a wrong result** (wrong model, manipulated score) | A2 | Out of scope for FHE (no integrity); documented limitation | – | Patient could get a wrong risk; needs verifiable computation (future work) |
| T8 | **Model extraction / inversion** by a client sending chosen inputs | A3 | Rate limit; weights not exposed by `/api/model`; logit-only mode reveals less than probability | `test_api.py::test_model_info_hides_weights` | A client decrypts real scores for chosen inputs, so ≈14 queries can recover a 13-feature linear model. Accepted for this prototype; mitigations: output only the decision, add noise, per-user quotas |
| T9 | **Replay** of a captured request | A6 | TLS prevents capture; a replayed request only returns a ciphertext the attacker cannot decrypt | Request IDs logged | Costs server compute only |
| T10 | **Client-side compromise** (XSS, malicious script steals the secret key) | A1, A2, A4 | Strict CSP (`script-src 'self' 'wasm-unsafe-eval'`, no inline scripts), no third-party scripts, node-seal served from our origin | `app.test.js` checks the CSP header | A compromised device is out of scope |
| T11 | **Library/version mismatch** silently corrupts results | A2 | Versions pinned (node-seal 7.0.0, TenSEAL 0.3.16); decrypt scripts fail on mismatch | `pilots/compat/check_versions.py`; CI round trip | Upgrades must re-run the compatibility test |
| T12 | **CKKS approximation / precision attacks** (e.g. Li–Micciancio 2021 key-recovery when decrypted CKKS results are shared) | A4 | Decrypted values stay on the patient's device and are never sent back to the server | By design (no endpoint accepts decrypted values) | Must stay true in Capstone 2 (no "report result" feature) |

## 4. What the pilot tells us (facts for the report)

- Encrypted inference is fast (≈80–110 ms server compute per patient, packed; PR2 Table 5) and
  gives the same decisions as the plaintext model on the pilot test sets.
- The main practical risk is **size**, not speed: packed layout needs 164 MB Galois keys;
  per-feature (the chosen layout, decision #15) avoids them but uploads about 16 MB of uncompressed
  ciphertext for 13 features (PR2 Table 5).
- node-seal needs WebAssembly GC + exception handling (Node 22+ / current browsers); old browsers
  fall back to Plan B.

## 5. To do (Naif)

- [ ] Review each row; add anything from the Week 10 technical facts not covered.
- [ ] Decide whether T8 needs a mitigation in Capstone 2 (decision-only output?).
- [ ] Add a data-flow diagram with trust boundaries (can reuse `diagrams/architecture.md`).
- [ ] Copy the final table into the final report (Methodology / Security).
