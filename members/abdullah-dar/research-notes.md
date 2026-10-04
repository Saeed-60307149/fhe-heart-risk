# Research notes – Abdullah Dar (Software Eng.)

## Week 6 – what the software side needs

### 1. Architecture
- Three parts: **client** (form), **backend API** (Node/Express), **FHE-ML service** (Python + TenSEAL).
- Main rule: **encrypt on the client, compute on the server, decrypt on the client.**
- The server only gets the ciphertext + a **public context** (public key + evaluation keys). Never the **secret key**.
- In TenSEAL you can make a copy of the context without the secret key (`make_context_public()`) and serialize it to send.

### 2. Key management
| Item | Where | Leaves the client? |
|---|---|---|
| Secret key | Patient's device | Never |
| Public + evaluation keys | Sent to server | Yes |
| Encrypted input / result | Client ↔ server | Yes |
| Model weights | Server | – |

### 3. Risk: client language vs server language
- TenSEAL is Python only, so a browser can't run it.
- Browser option: **node-seal** (Microsoft SEAL compiled to WebAssembly).
- Both use Microsoft SEAL underneath, but TenSEAL wraps ciphertexts in its own format, so a node-seal ciphertext might **not** load in TenSEAL.
- Plan A: node-seal browser + TenSEAL server (needs Saif's Wk 11 test). Plan B: Python client, TenSEAL on both sides.
- API design waits for this result.

### 4. API notes
- Ciphertexts are binary and big → send as base64 in JSON, raise Express body limit.
- Draft: `POST /api/predict`, `GET /api/health` (see `design/api-contract.md`).
- Don't log request bodies.

### 5. Repo + workflow
- One repo: research now (Sem 1), code later (Sem 2).
- `.gitignore` blocks dataset, keys, venv, node_modules.
- Branch protection on a **private** repo needs a paid plan (free with GitHub Student Developer Pack), or make the repo public, or follow the PR rule by agreement.
- Task board: GitHub Projects (tasks link to files/PRs).

## Papers / sources
| # | Title | Year | Where found | Link | Why it matters |
|---|---|---|---|---|---|
| 1 | TenSEAL: A Library for Encrypted Tensor Operations Using HE | 2021 | arXiv | https://arxiv.org/abs/2104.03152 | Our main library |
| 2 | node-seal | – | npm | https://www.npmjs.com/package/node-seal | Browser-side encryption option |
| 3 | Homomorphic encryption for web apps | – | Medium | https://medium.com/@s0l0ist/homomorphic-encryption-for-web-apps-b615fb64d2a2 | How node-seal is used in web apps |
| 4 | CKKS in OpenFHE vs TenSEAL (forum) | – | OpenFHE Discourse | https://openfhe.discourse.group/t/comparison-of-ckks-scheme-between-openfhe-and-tenseal/1466 | Library differences |
| 5 | GitHub Docs – protected branches | – | GitHub | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches | Repo workflow rules |

## Open questions (for meeting)
1. Repo public or private?
2. Web client (node-seal) or Python client – can it stay open until the pilot?
3. Can the dataset go in the repo? (Sarim checking licence)
