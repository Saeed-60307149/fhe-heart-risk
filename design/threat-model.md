# Threat model – v1.0 (final, submitted 15 Nov 2026)

> **Aligned with the corrected Defense Report (reference, decision #26).** This page records Threat Model v1.0, written with an individual user as the client; as the report says (D.6), it will be updated to the hospital scenario.

Owner: **Naif** · Practicum (Capstone 1) · Supervisor: Dr. Abdulatif Shikfa · Method: STRIDE applied to
each component and data flow, with a residual risk rating after mitigation. Covers the system in
[architecture.md](architecture.md): browser client, Express gateway, FastAPI/TenSEAL service and the data
flowing between them. This file records the submitted *Threat Model v1.0* PDF; the
"Status in `code/`" column and section 8 are added by the repo (they are not in the PDF) so that
Capstone 2 knows what is already built and tested.

## 1. Assets

| ID | Asset | Why it matters |
|---|---|---|
| S1 | Patient's plain health features | Sensitive health data (the thing the system exists to protect) |
| S2 | Plain risk score and decision | Reveals the patient's health status |
| S3 | Secret key | Decrypts every ciphertext of that patient |
| S4 | Integrity of the returned score | A wrong score could mislead the patient |
| S5 | Service availability | Large ciphertexts make the service easy to overload |
| S6 | Model weights | Low sensitivity: model is trained on public datasets |

## 2. Adversaries and trust boundary

| ID | Adversary | Capability |
|---|---|---|
| A1 | Honest-but-curious server operator | Sees all ciphertext, keys, logs, timing and memory on the server but follows the protocol |
| A2 | External attacker who breaches the server | Same view as A1 and may modify server code |
| A3 | Network attacker | Reads or alters traffic if TLS fails |
| A4 | Malicious client or user | Sends crafted, oversized or repeated requests; probes the model |
| A5 | Malicious web content or dependency | XSS, tampered script or compromised package running in the browser |

**Trust boundary:** the hospital's browser is trusted. Everything behind TLS (gateway, FHE service, logs,
disk) is untrusted for patient data.

## 3. Assumptions and out of scope

- The server is honest-but-curious. A fully malicious server is covered only where stated (T4, T6).
- CKKS security relies on the standard RLWE parameters in Microsoft SEAL (128-bit, `tc128`). Known
  attacks on CKKS decryption results (e.g. Li–Micciancio 2021) do not apply because decrypted scores are
  never shared with the server. **This must stay true in Capstone 2: no "report result" endpoint.**
- Training-data privacy is out of scope: both datasets are public and de-identified.
- Compromise of the patient's own device or operating system is out of scope.
- Differential privacy and verifiable FHE computation are future work.

## 4. Threats and mitigations

Residual risk is the rating after the listed mitigation is in place.

| ID | Threat | Adv. | Mitigation | Residual | Status in `code/` (15 Nov) |
|---|---|---|---|---|---|
| T1 | Server reads patient features | A1, A2 | Features exist only as CKKS ciphertext on the server. Test that the server context is public and holds no secret key | Low | **Tested:** `fhe-ml-service/tests/test_no_secret_on_server.py` |
| T2 | Server reads the risk result | A1, A2 | Score is returned encrypted and decrypted only in the browser | Low | **By design:** no endpoint accepts decrypted values |
| T3 | Secret key stolen from the browser (XSS, extension, key stored) | A5 | Key in memory only, never persisted or sent; strict CSP; no inline scripts | Medium | **Implemented:** CSP `script-src 'self' 'wasm-unsafe-eval'`, key in memory; `app.test.js` checks the CSP header |
| T4 | Server ships malicious JavaScript that leaks plain data before encryption | A1, A2 | Subresource integrity, hashed and pinned bundles, CSP. Cannot be fully removed in a browser design; documented as the main residual risk | High | **Partly:** CSP and own-origin scripts only. SRI and hashed bundles not yet |
| T5 | Traffic read or altered in transit | A3 | HTTPS only, HSTS, no mixed content | Low | **Implemented:** HTTPS when `TLS_CERT/TLS_KEY` set, HSTS header (`backend/src/app.js`, `server.js`) |
| T6 | Wrong score returned (CKKS gives no integrity) | A1, A2 | Client sanity check that the score is in a valid range; verifiable computation is future work | Medium | **Partly:** the web page rejects a result outside the possible range (catches gross errors only) |
| T7 | Weak or altered encryption parameters sent by the client | A4 | Server accepts only the fixed approved parameter set and rejects others | Low | **Tested:** the service accepts only the two exact approved sets (`test_unapproved_parameters_rejected`), plus SEAL 128-bit validation |
| T8 | Denial of service: large uploads (limit 48 MB per request), floods, heavy compute | A4 | Request size caps, rate limiting, authentication, timeouts, queue limits | Medium | **Mostly:** 48 MB body limit, per-client rate limit (`RATE_LIMITED`), auth before body read, 120 s upstream timeout. Queue limits not yet; limiter is in-memory, single process |
| T9 | Malformed ciphertext exploits or crashes the parser | A4 | Format and length checks, pinned library versions, container with limited rights, fuzz tests | Medium | **Partly:** format, size, level and transparent-ciphertext checks tested (`test_seal_roundtrip.py`: garbage, oversize). Container and fuzz tests not yet |
| T10 | Model extraction through repeated queries | A4 | Per-user quotas and rate limits. Accepted: the model is trained on public data | Low | **Partly:** rate limit; weights hidden by `/api/model` (`test_model_info_hides_weights`). Per-user quotas not yet (static tokens) |
| T11 | Metadata leakage (sizes, timing, IP, frequency, account linkage) | A1, A2 | Fixed-size requests, no patient identifiers, minimal logging | Medium | **Partly:** metadata-only access logs (`app.test.js`). Request sizes are fixed per dataset by design |
| T12 | Keys or ciphertexts exposed through logs or crash dumps | A1, A2 | Never log payloads; scrub error output; restrict repository and log access | Low | **Tested:** `app.test.js` "access log holds metadata only"; `test_api.py::test_validation_error_does_not_echo_input` |
| T13 | Tampered dependency (node-seal, TenSEAL, npm or pip package) | A5 | Pinned versions, lockfiles, hash checks, no runtime CDN, dependency audit | Medium | **Partly:** pinned versions and lockfile (`npm ci`), node-seal served from own origin. Hash checks and audit not yet |
| T14 | Unauthorised or spoofed API use | A4 | Authentication and authorisation, CORS allow-list | Low | **Partly:** bearer token on `/api/predict`, internal token between services (401 tests). CORS allow-list not yet |
| T15 | Library version mismatch gives silent wrong results | None | Compatibility test and plain-vs-encrypted comparison on every version change | Low | **Implemented:** `pilots/compat/check_versions.py`; CI round trip; decision match 100% on the 11 Nov run |

## 5. Residual risks to state in the report

1. **T4, malicious client code (High).** In any browser-based design the server delivers the code that
   does the encrypting, so a compromised server could replace it. Integrity controls reduce this but do
   not remove it. A signed or locally installed client would remove it and is future work.
2. **T6, no result integrity (Medium).** CKKS proves nothing about the computation. A malicious server
   could return a wrong score. The client range check catches only gross errors.
3. **T11, metadata (Medium).** Ciphertext sizes, timing and request patterns remain visible to the server.

## 6. Security test plan (run in Capstone 2 as the security assessment)

| # | Test | Covers |
|---|---|---|
| 1 | Assert the server never loads a context that contains a secret key | T1, T2 |
| 2 | Capture traffic, server memory and logs; confirm no plain features or score | T1, T2, T5, T12 |
| 3 | Send oversized, malformed and wrong-parameter ciphertexts; confirm rejection | T7, T8, T9 |
| 4 | Rate-limit, quota and load test the API | T8, T10 |
| 5 | CSP, SRI and dependency audit of the front end and lockfiles | T3, T4, T13 |
| 6 | Authentication and CORS tests | T14 |
| 7 | Plain-vs-encrypted decision match (target 90% or better, decisions #16, #26) on every library change | T15 |

Tests 1 and 3 already exist as automated tests; 7 is the pilot run. Tests 2, 4, 5 and 6 are open.

## 7. What the pilot told us (11 Nov facts; current sizes are in `code/results/benchmarks/`)

- Encrypted inference is fast (≈80–110 ms server compute per patient, packed; PR2 Table 5) and gives the
  same decisions as the plaintext model on the pilot test sets.
- The main practical risk is **size**, not speed: the packed layout needs 164 MB Galois keys; per-feature
  (the chosen layout, decisions #15 and #26) avoids them but uploads about 16 MB of uncompressed ciphertext for 13
  features (PR2 Table 5).
- node-seal needs WebAssembly GC + exception handling (Node 22+ / current browsers); old browsers fall back
  to Plan B.

## 8. Changes from the 11 Nov draft (repo)

The draft's T1–T12 were renumbered in the submitted v1.0. Mapping, so old references still resolve:

| Draft (11 Nov) | v1.0 |
|---|---|
| T1 curious server | T1, T2 |
| T2 network | T5 |
| T3 unauthenticated requests | T14 (and T8) |
| T4 malformed ciphertext / parameters | T7, T9 |
| T5 denial of service | T8 |
| T6 logs and errors | T12 |
| T7 wrong result from server | T6 |
| T8 model extraction | T10 |
| T9 replay | dropped (costs server compute only; covered by T8) |
| T10 client-side compromise | T3, T4 |
| T11 version mismatch | T15 |
| T12 CKKS precision attacks | Section 3 (assumption) |
| – | New in v1.0: T11 metadata, T13 dependencies |

Open point carried over from the draft: a client can decrypt real scores for chosen inputs, so about 14
queries can recover a 13-feature linear model. v1.0 accepts this (T10, "model is trained on public data").
Decision-only output remains an option if the team wants to reduce it.

## Note added 27 Nov: packed layout (comparison only)

If the packed layout were ever delivered, the slots other than slot 0 of the returned ciphertext hold partial sums of
weight × feature. A client knows its features, so it could work out model weights (asset S6, low sensitivity: public
training data). Masking those slots needs one more multiplication level. The delivered per-feature layout does not
have this issue.
