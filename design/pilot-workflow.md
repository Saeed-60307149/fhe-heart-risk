# Pilot workflow notes

Owner: Abdullah Dar (work plan Week 11, Gantt 4.9a) · 11 Nov 2026 · how the practicum pilot runs,
step by step, and where each PR2 number comes from. Diagram: [diagrams/architecture.md](diagrams/architecture.md#practicum-pilot-workflow).

| # | Step | Who (PR2) | Code | Output | PR2 reference |
|---|---|---|---|---|---|
| 1 | Environment with pinned versions (Python 3.12, Node 22, TenSEAL 0.3.16, node-seal 7.0.0) | Saif (Wk 8–10) | `code/requirements.txt`, `pilots/compat/check_versions.py` | "Toolchain OK" | §A.4, §C |
| 2 | Toy examples: encrypt, add, multiply by plaintext, multiply ciphertexts, decrypt | Saif (26 Oct) | `pilots/node-seal-roundtrip/encrypt_demo.mjs`, `server_demo.py`, `decrypt_demo.mjs` | z = 11.5 exactly | Saif logbook Wk 10 |
| 3 | node-seal encrypt/decrypt check; sizes at N = 8192 (ct 0.39 MB, pk 0.52 MB, relin 1.57 MB, sk 0.26 MB; max error ≈ 3.3 × 10⁻⁷) | Saif (29 Oct) | same | logbook table | Saif logbook Wk 10 |
| 4 | Load data, clean, split 75/25 (seed 42), scale | Sarim / Saif | `pilots/baseline/train_baseline.py` | `baseline_metrics.json` | Table 5 accuracy 0.853, AUC 0.947 |
| 5 | Fit cubic sigmoid (least squares) | Khalid / Saif | `pilots/sigmoid/fit_sigmoid.py` | MAE, decision match | Table 5 MAE 0.031 |
| 6 | Packed encrypted inference over the test set | Saif, Naif (Wk 10–11) | `pilots/tenseal-pilot/pilot.py --layout packed` | times, sizes, encrypted accuracy | Table 5 rows 1–7 |
| 7 | Cross-library round trip on one real patient | Saif, Naif (Wk 11) | `pilots/node-seal-roundtrip/` (`npm run real`) | z = z_true (0.877) | §B, Table 5 rows 8–10 |
| 8 | Per-feature inference with encrypted sigmoid (server path of the prototype) | new, 11 Nov | `pilot.py --layout per_feature` | relin-key size, times | answers §C "large evaluation keys" |
| 9 | Tables for the report | Hassan | `scripts/summarise_results.py` | `code/results/README.md` | Table 5 (final) |

## Changes to the plan since PR1

- PR1 planned browser encryption (Plan A). Measurements were first taken with a Python client
  (Plan B) and the full node-seal ↔ TenSEAL round trip followed in Week 11 – **Plan A is feasible**.
- Ciphertext layout closed (decision #15): **one ciphertext per feature** (no Galois keys); the
  packed layout is kept in the benchmark as the comparison.
- Edinburgh MI pilot (PR2 "Week 12") is now scripted: the same commands with `--dataset edinburgh`.
