# Benchmark plan

Owner: **Hassan Zahid** (work plan Week 10, runbook step 28 plan) · draft 11 Nov 2026, built on the
PR2 Table 5 measurements · answers **RQ-B** (cost of privacy) and feeds RQ-A (decision match).

## What is measured

| Metric | Unit | How | Script |
|---|---|---|---|
| Accuracy, precision, recall, F1, ROC-AUC | – | Fixed stratified split, seed 42, test rows only | `pilots/baseline/train_baseline.py` |
| Sigmoid approximation error | MAE, max abs error | Test logits, sigmoid vs polynomial | `pilots/sigmoid/fit_sigmoid.py` |
| **Decision match** (RQ-A) | % of test patients | Same low/high decision as plaintext sigmoid | `pilot.py`, `fit_sigmoid.py` |
| Key generation time | s | One-off per client | `pilot.py` |
| Encryption time per patient | ms | Mean, median, min, max over the test set | `pilot.py` (Python client); browser: node-seal timing in the page / `encrypt_real.mjs` |
| Encrypted inference time | ms | Server compute (+ load from bytes for per-feature) | `pilot.py`; API: `timings_ms` |
| Decryption time | ms | Client | `pilot.py`, `decrypt_real.mjs` |
| End-to-end latency | ms | Browser submit → result, through the API | Capstone 2 (step 28): Playwright or manual, 20 patients |
| Ciphertext size per patient | MB | Serialized bytes (raw, and base64 on the wire) | `pilot.py` |
| Key sizes | MB | Public context, secret-key context, Galois keys, relin keys | `pilot.py` |
| Plaintext size per patient | bytes | 13 × 8-byte floats = 104 B (reference) | – |

## Conditions

- Both datasets, reported separately (Cleveland: 75 test patients; Edinburgh: 314).
- Both layouts: packed (TenSEAL CKKSVector) and per-feature (raw SEAL, prototype path).
- CKKS N = 16384, moduli [60, 40, 40, 40, 40, 60], scale 2^40, 128-bit security.
- Same machine for all runs; the JSON `environment` block records Python, OS and CPU. Add RAM
  and the exact CPU model by hand in the report.
- Each timing = mean over all test patients; warm-up excluded is not needed for means over ≥75
  runs, but report the median too (already in the JSON).
- Re-run before every reported number: `bash code/scripts/run_pilot.sh`; commit `code/results/`.

## Reporting

`code/scripts/summarise_results.py` writes `code/results/README.md` with three tables (baseline,
sigmoid, pilot). Copy them into the final report and cite the commit hash of the run.

## Already measured (PR2 Table 5, Cleveland, packed, 7 Nov 2026, re-run by Saif)

Keygen 1.18 s · enc / inference / dec 13.3 / 87.5 / 3.5 ms · ciphertext 1,029 KB · public context
7.7 MB · with secret key 1.9 MB · Galois keys 163.9 MB · accuracy 0.853 plain = 0.853 encrypted
(ROC-AUC 0.947) · sigmoid MAE 0.031 · node-seal 33.4 ms/feature (434 ms/patient), decrypt 3.3 ms ·
per-feature ciphertexts ≈16 MB per patient.

The new scripts reproduce the packed sizes exactly (1.00 MB ciphertext, 163.9 MB Galois keys,
1.9 MB secret-key context) – checked 11 Nov.
