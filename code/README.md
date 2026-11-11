# Code

Practicum pilots (Weeks 10–12) and the Capstone 2 prototype skeleton. Everything here runs on
public, de-identified data only; raw data, ciphertexts and keys are never committed.

```
patient browser (node-seal 7.0.0)          Node.js API (Express)            FHE-ML service (FastAPI + TenSEAL 0.3.16)
  keys made here, secret key stays   --->  auth, size/format checks,  --->  weighted sum + cubic sigmoid on
  encrypt each feature (CKKS)              rate limit, metadata logs        ciphertexts; never decrypts
  decrypt the score locally          <---  forwards ciphertext only   <---  returns an encrypted score
```

| Folder | What | Stack | Owner (work plan) |
|---|---|---|---|
| [`data/`](data/) | Data dictionary; raw files download to `data/raw/` (git-ignored) | – | Sarim |
| [`fhe-ml-service/`](fhe-ml-service/) | Shared Python package `fhe_heart` + FastAPI `/infer` service + tests | Python, TenSEAL, FastAPI | Saif, Naif |
| [`backend/`](backend/) | Public API: `/api/health`, `/api/model/:dataset`, `/api/predict` | Node.js 22, Express | Abdullah |
| [`frontend/`](frontend/) | Patient form, browser-side encryption and decryption | HTML/JS, node-seal | Abdullah, Saif |
| [`client-python/`](client-python/) | Plan B client (encrypt/decrypt in local Python) | Python | Saif |
| [`pilots/baseline/`](pilots/baseline/) | Plaintext logistic regression on both datasets | scikit-learn | Sarim |
| [`pilots/sigmoid/`](pilots/sigmoid/) | Polynomial sigmoid fit + validation | numpy | Khalid |
| [`pilots/tenseal-pilot/`](pilots/tenseal-pilot/) | Cost/accuracy of both ciphertext layouts (PR2 Table 5) | TenSEAL | Saif, Hassan |
| [`pilots/node-seal-roundtrip/`](pilots/node-seal-roundtrip/) | PR2 cross-library round trip | node-seal + TenSEAL | Saif, Naif |
| [`pilots/compat/`](pilots/compat/) | Toolchain version check | – | Hassan |
| [`results/`](results/) | Generated JSON + tables for the report | – | Hassan |
| [`scripts/`](scripts/) | `run_pilot.sh` / `.ps1`, `summarise_results.py` | – | Hassan |

## Setup (once)

Needs **Python 3.10–3.13** and **Node.js 22+** (node-seal 7.0.0 does not load on Node 20).

```bash
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r code/requirements.txt                     # pins tenseal==0.3.16
(cd code/backend && npm ci)
(cd code/pilots/node-seal-roundtrip && npm ci)
python code/pilots/compat/check_versions.py              # must print "Toolchain OK"
```

Do **not** upgrade TenSEAL: 0.3.17 and 0.3.18 reject node-seal 7.0.0 ciphertexts (PR2).

## 1. Practicum measurements (both datasets)

```bash
bash code/scripts/run_pilot.sh          # Windows: powershell -File code\scripts\run_pilot.ps1
```
Runs, in order: baseline → sigmoid fit/validation → encrypted pilot (packed and per-feature) on
Cleveland and Edinburgh → `results/README.md` tables → node-seal round trip. Each step can also
be run alone (see each folder's README). Cleveland downloads from the UCI archive; Edinburgh from
the public copy published with Kim et al. (2018).

## 2. Run the prototype locally

```bash
# terminal 1 – FHE service (needs fhe-ml-service/model/model_weights_*.json from step 1)
cd code/fhe-ml-service && FHE_SERVICE_TOKEN=dev-internal uvicorn app:app --port 8001
# terminal 2 – API + web page
cd code/backend && FHE_SERVICE_TOKEN=dev-internal API_TOKENS=dev-client npm start
# open http://127.0.0.1:3000, Advanced -> API token = dev-client
```
Plan B client: `python code/client-python/fhe_client.py --dataset cleveland --token dev-client --values 57 1 4 140 241 0 1 123 1 0.2 2 0 7`

## 3. Tests

```bash
(cd code/fhe-ml-service && python -m pytest)        # 26 tests: round trip, sigmoid, API contract, no secret key on server
(cd code/backend && npm test)                        # 17 tests: auth, validation, error codes, rate limit, logging
# full chain (service running on 8001 with a model for the dataset):
(cd code/backend && E2E_FHE_URL=http://127.0.0.1:8001 E2E_DATASET=cleveland FHE_SERVICE_TOKEN=dev-internal node --test test/e2e.test.js)
```
CI (`.github/workflows/ci.yml`) runs all three on every pull request.

## Ciphertext layout

Two layouts were measured in the pilot (PR2 Table 5 and section A.3). The project uses
**one ciphertext per feature** (decision #15 in [`planning/decision-log.md`](../planning/decision-log.md)):
it needs no Galois keys, and with the cubic sigmoid computed on the server only relinearization keys
(about 6–8 MB) instead of 164 MB of Galois keys. The cost is a bigger upload (about 1.3 MB per
feature uncompressed, ≈16 MB per patient – PR2 Table 5). The packed layout stays in the benchmark
as the comparison.
