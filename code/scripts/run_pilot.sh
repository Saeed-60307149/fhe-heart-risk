#!/usr/bin/env bash
# Re-run every practicum measurement from scratch (both datasets) and refresh
# code/results/. Run from the repo root:  bash code/scripts/run_pilot.sh
set -euo pipefail
cd "$(dirname "$0")/.."
python pilots/compat/check_versions.py || { echo "fix the toolchain first"; exit 1; }
python pilots/baseline/train_baseline.py
python pilots/sigmoid/fit_sigmoid.py
python pilots/tenseal-pilot/pilot.py --dataset cleveland
python pilots/tenseal-pilot/pilot.py --dataset edinburgh
python scripts/summarise_results.py
( cd pilots/node-seal-roundtrip && npm install --no-audit --no-fund && npm run real )
echo "Done. See code/results/README.md"
