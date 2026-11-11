# How to use this repo (simple version)

## Easiest way: edit on the website
1. Open the file on github.com → click the ✏️ pencil.
2. Write your changes → **Commit changes** → write a short message (e.g. `saif: add 3 survey papers`).
3. For your own folder (`members/yourname/`) you can commit straight to `main`.

## Rules
- Only edit **your own** folder in `members/`. Shared files (`meetings/`, `research/`) are fine for everyone.
- Write your logbook notes the same day you work. Times + what you did.
- Every paper you read also goes into `research/reading-list.md`.
- Big shared changes (design, reports, and all code later) → make a branch and open a **Pull Request**; one teammate reviews.
- Never commit: dataset files, `.env`, keys, `venv/`, `node_modules/`.

## With git (optional)
```
git pull                      # always first
git add .
git commit -m "name: what you did"
git push
```

## Code (from now on)
Branch per task (`name/task`) → Pull Request → 1 review → merge. No direct pushes to `main` for code.
- CI (`.github/workflows/ci.yml`) must be green: Python tests, backend tests, end-to-end round trip.
- Before a PR: `(cd code/fhe-ml-service && python -m pytest)` and `(cd code/backend && npm test)`.
- Do **not** upgrade `tenseal` (pinned 0.3.16) or `node-seal` (pinned 7.0.0) – see `code/pilots/compat/`.
- Never commit `code/data/raw/`, `*.b64`, `*.seal`, `model_patient.json` or `.env` (all git-ignored).
- Results you report go in `code/results/` (regenerate with `bash code/scripts/run_pilot.sh`).

## SLR records
- The decision record is `research/slr/refined-2026-10-29/screening-decisions.csv`. Update it after
  every decision, then `python research/slr/scripts/prisma_counts.py --write`.
- Keep the Excel sheet in step with the CSV (one person edits the sheet at a time).
