# Practicum pilots

Run from `code/` in this order (or all at once with `bash scripts/run_pilot.sh`):

| Step | Script | Writes | Runbook step / PR2 objective |
|---|---|---|---|
| 0 | `python pilots/compat/check_versions.py` | – | toolchain pins (PR2 §A.4) |
| 1 | `python pilots/baseline/train_baseline.py [--dataset X] [--tune]` | `results/<ds>/baseline_metrics.json`, `fhe-ml-service/model/model_weights_<ds>.json` | 3–7 / objective 2 |
| 2 | `python pilots/sigmoid/fit_sigmoid.py [--interval LO HI] [--target 0.90]` | `results/<ds>/sigmoid_validation.json`, `sigmoid_vs_poly.png`, adds `sigmoid_poly` to the model file | 8–9 / objective 3 |
| 3 | `python pilots/tenseal-pilot/pilot.py --dataset X [--layout packed\|per_feature\|both] [--limit N]` | `results/<ds>/pilot_<layout>.json` | 13–17 / objective 4, Table 5 |
| 4 | `node-seal-roundtrip/` (`npm run real`) | console | 2, 20 / PR2 cross-library round trip |
| 5 | `python scripts/summarise_results.py` | `results/README.md` | 28 (pilot) |

Notes
- Split: stratified, `test_size=0.25`, `random_state=42`, same as the PR2 pilot (Cleveland:
  297 rows, 75 test patients).
- `--tune` picks the regularisation C by 5-fold CV on the training rows (runbook step 6). The PR2
  numbers used the default C = 1.0; report which one you use.
- The sigmoid interval defaults to the 99th percentile of |training logits| + 1, so the test set
  does not influence the choice.
- The packed layout reproduces PR2 Table 5 sizes (1.0 MB ciphertext, 163.9 MB Galois keys).
- Times depend on the machine: each JSON records `environment`. Report the machine in the paper.
