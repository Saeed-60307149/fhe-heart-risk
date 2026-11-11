# Cross-library FHE round trip (node-seal → TenSEAL → node-seal)

PR2 result (Saif, Naif, Week 11): node-seal (the browser library) encrypts a real test patient,
TenSEAL computes the encrypted score on the server, node-seal decrypts it. The decrypted score
matched the plain model exactly (z = 0.877 for Cleveland test patient 0).

Per-feature layout: one CKKS ciphertext per feature, so the server needs no rotation keys.

## Requirements
- **Node.js 22 or newer** (node-seal 7.0.0 uses WebAssembly GC + exception handling; Node 20 fails)
- Python with `pip install -r ../../requirements.txt` (pins **tenseal==0.3.16**; 0.3.17/0.3.18
  reject node-seal 7.0.0 ciphertexts)
- `npm ci` in this folder (pins node-seal 7.0.0)

## Run (in this folder)
```bash
npm run real          # = the 4 steps below
python train_export.py [--dataset cleveland|edinburgh] [--index 0]   # model + 1 test patient
node encrypt_real.mjs         # node-seal encrypts every feature
python server_real.py         # TenSEAL computes the encrypted score -> out/real_z.seal
node decrypt_real.mjs         # node-seal decrypts; exits 1 unless z equals z_true
```
Expected end: `ROUND TRIP OK` and `z = z_true`.

Quick sanity check with 4 toy values: `npm run demo` (expected `DEMO ROUND TRIP OK`, z = 11.5).

## Changes from the PR2 zip (11 Nov)
- Scratch files go to `out/` instead of `/tmp/` (works on Windows); `out/`, `*.b64` and
  `model_patient.json` are git-ignored because they hold a secret key and ciphertexts.
- Feature count is read from the data (Edinburgh has 9), not hard-coded to 13.
- `train_export.py` uses the shared loader (`fhe_heart.data`), so the split and model are
  identical to the pilot and the prototype.
- Added the missing `decrypt_demo.mjs`; both decrypt scripts now fail loudly on a mismatch.

`server_demo.py` loads the secret key only to print a sanity check. That is fine for the toy
demo; the real server (`server_real.py`, `fhe-ml-service/`) never receives a secret key.
