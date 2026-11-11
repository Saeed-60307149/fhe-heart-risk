# Results (generated 2026-11-11 by `code/scripts/summarise_results.py`)

Do not edit by hand: re-run `bash code/scripts/run_pilot.sh`. Raw JSON is next to this file.

## Plaintext baseline (logistic regression, fixed stratified split, seed 42)

| Dataset | Rows | Test rows | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|---|---|
| cleveland | 297 | 75 | 0.853 | 0.853 | 0.829 | 0.841 | 0.947 |
| edinburgh | 1253 | 314 | 0.927 | 0.871 | 0.783 | 0.824 | 0.963 |

## Polynomial sigmoid (test split)

| Dataset | Polynomial | MAE vs sigmoid | Decision match | Accuracy | Pass (≥90%, RQ-A) | ≥95% (expected) |
|---|---|---|---|---|---|---|
| cleveland | least-squares cubic on [-6.4, 6.4] | 0.0356 | 1.000 | 0.853 | True | True |
| cleveland | Kim et al. 2018 cubic [-8, 8] | 0.0568 | 1.000 | 0.853 |  |  |
| cleveland | runbook cubic [-5, 5] | 0.0291 | 1.000 | 0.853 |  |  |
| edinburgh | least-squares cubic on [-8.1, 8.1] | 0.0331 | 1.000 | 0.927 | True | True |
| edinburgh | Kim et al. 2018 cubic [-8, 8] | 0.0339 | 1.000 | 0.927 |  |  |
| edinburgh | runbook cubic [-5, 5] | 0.0607 | 0.981 | 0.908 |  |  |

## Encrypted inference pilot (CKKS N=16384, scale 2^40, 128-bit)

| Dataset | Layout | Patients | Enc ms | Inference ms | Dec ms | Ciphertext MB / patient | Eval keys MB | Plain acc | Enc acc | Decision match |
|---|---|---|---|---|---|---|---|---|---|---|
| cleveland | packed | 75 | 13.4 | 94.5 | 2.0 | 1.00 | 163.9 (Galois) | 0.853 | 0.853 | 1.000 |
| cleveland | per_feature | 75 | 354.1 | 212.6 | 5.0 | 13.06 | 6.3 (relin) | 0.853 | 0.853 | 1.000 |
| edinburgh | packed | 314 | 12.6 | 67.9 | 1.9 | 1.00 | 163.9 (Galois) | 0.927 | 0.927 | 1.000 |
| edinburgh | per_feature | 314 | 265.3 | 184.4 | 5.6 | 9.04 | 6.3 (relin) | 0.927 | 0.927 | 1.000 |

Times are means over the test patients on the machine recorded in each JSON file (`environment`).
