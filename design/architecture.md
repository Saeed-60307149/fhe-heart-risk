# Architecture – v2

Owner: Abdullah Dar · v1 draft Week 10 (26 Oct) · **v2: 11 Nov 2026** – updated with the PR2 pilot
results and the prototype skeleton in `code/`. Diagram source: [diagrams/architecture.md](diagrams/architecture.md)
(Mermaid, renders on GitHub); the Week 10 PNG is in `members/abdullah-dar/images/architecture.png`.

## Parts

| # | Part | Runs where | Stack | Holds |
|---|---|---|---|---|
| 1 | **Patient client** (Plan A: browser page; Plan B: local Python CLI) | Patient's device | HTML/JS + node-seal 7.0.0 (WASM) · or Python + TenSEAL 0.3.16 | **Secret key** (memory only), public key, relin keys, raw answers |
| 2 | **Node.js API** | Server, public (behind TLS) | Express 4, Node 22 | API tokens; nothing about the patient in readable form |
| 3 | **FHE-ML service** | Server, localhost/private only | FastAPI + TenSEAL 0.3.16 (`sealapi`) | Model weights, bias, sigmoid polynomial |

```
[1 Patient client] --HTTPS: parms + n ciphertexts (+ relin keys)--> [2 Node API] --localhost--> [3 FHE-ML service]
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
| Relinearization keys | Client → server | Yes (≈6–8 MB raw) | Public evaluation keys; cannot decrypt |
| Galois (rotation) keys | – | Not used | Needed only by the packed layout (164 MB) |
| Encrypted features / score | Client ↔ server | Yes | Ciphertext only |
| Model weights, polynomial | FHE service | No | Server asset; not returned by `/api/model` |
| Scaler mean/scale | Server → client | Yes | Public; needed to scale before encrypting |

## Decisions recorded (see `planning/decision-log.md`)

| Decision | Status | Evidence |
|---|---|---|
| Scheme: CKKS | Final (#1) | Real-valued features |
| Client: **Plan A (node-seal in the browser) works**; Plan B (Python CLI) kept as fallback | Final (#12) | PR2 cross-library round trip; `code/frontend` tested in headless Chrome 11 Nov |
| Versions pinned: node-seal 7.0.0, TenSEAL 0.3.16, Node.js ≥ 22 | Final (#13) | PR2 compatibility test |
| Ciphertext layout: one ciphertext per feature | Final (#15) | PR2 §C mitigation + Report 1 plan. Packed = 1 MB/patient but 164 MB Galois keys; per-feature ≈ 16 MB/patient uncompressed (PR2 Table 5) but no Galois keys, ≈6–8 MB relin keys for the encrypted sigmoid |
| Sigmoid on server (encrypted cubic) vs on client (after decrypt) | Both supported (`output` field) | Server-side needs relin keys + 2 more levels; client-side reveals the logit only to the patient |

## Capstone 2 backlog (engineering items, not open decisions)

- **Upload size**: per-feature uploads ≈ 16 MB raw / ≈ 22 MB base64 for 13 features (+10 MB relin keys). Options:
  SEAL `zstd` compression (test on both libraries), N = 8192 with `output = "logit"` (smaller
  ciphertexts, no relin keys; sigmoid on the client), or packing several features per ciphertext
  with a few targeted Galois keys only.
- **Key reuse**: today keys are regenerated per page load. Keeping them in IndexedDB would cut the
  per-request upload of relin keys, but stores a secret key at rest; decide with the threat model.
- **Model integrity**: the client cannot verify the server used the real model (threat model T7).
