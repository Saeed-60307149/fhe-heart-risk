# Windows PowerShell version of run_pilot.sh. Run from the repo root:
#   powershell -ExecutionPolicy Bypass -File code\scripts\run_pilot.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
python pilots/compat/check_versions.py; if ($LASTEXITCODE) { throw "fix the toolchain first" }
python pilots/baseline/train_baseline.py
python pilots/sigmoid/fit_sigmoid.py
python pilots/tenseal-pilot/pilot.py --dataset cleveland
python pilots/tenseal-pilot/pilot.py --dataset edinburgh
python scripts/summarise_results.py
Push-Location pilots/node-seal-roundtrip
npm install --no-audit --no-fund
python train_export.py; node encrypt_real.mjs; python server_real.py; node decrypt_real.mjs
Pop-Location
Write-Host "Done. See code/results/README.md"
