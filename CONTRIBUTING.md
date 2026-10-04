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

## Semester 2 (code)
Branch per task (`name/task`) → Pull Request → 1 review → merge. No direct pushes to `main` for code.
