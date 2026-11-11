# Sarim
    **Program:** Artificial Intelligence
    **Main focus:** UCI dataset, preprocessing, baseline logistic regression + metrics

    This is your own space. Put your research notes, drafts and logbook notes here.
    Only edit files inside your own folder (and the shared files in `meetings/` and `research/`).

    ## My tasks (from the Team Work Plan)
    | Week | Dates | Task | Due | Done |
    |---|---|---|---|---|
    | Wk 6 | 27 Sep–1 Oct | Find existing studies on heart-disease prediction with ML (ideally privacy-aware). Check the UCI Heart Disease page and licence. | Logbook Sun 4 Oct | ⬜ |
| Wk 7 | 4–8 Oct | Run the PubMed search (replaced ACM Digital Library) and fill the PubMed row of the Search Log tab; Hassan re-runs it to confirm. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Write the PR1 data statement and the ethics/data note with Hassan. | PR1 + logbook Sun 11 Oct | ⬜ |
| Wk 8 | 11–15 Oct | Screen titles/abstracts for all of Set 2 with Hassan (SLR v3, Pair 2). Draft the plaintext baseline method as your section of `reports/progress-report-2/methodology-v1.md`. | Thu 15 Oct (no logbook, mid-term – keep notes) | ⬜ |
| Wk 10 | 25–29 Oct | Pilot: download UCI Heart Disease, clean, scale, split, train baseline logistic regression. Save weights to JSON. Full-text screening of your half of Pair 2's papers, with extraction + quality rows. | Logbook Sun 1 Nov | ⬜ |
| Wk 11 | 1–5 Nov | Evaluate the baseline: accuracy, precision, recall, F1, ROC-AUC on the test set. Backward snowballing on your included papers (Screening Log, Source = Snowballing). | PR2 + logbook Sun 8 Nov | ⬜ |
| Wk 12 | 8–12 Nov | Draft final report: data and baseline model methodology/results. Co-write SLR synthesis RQ3 with Hassan. | Logbook Sun 15 Nov | ⬜ |
| Wk 13 | 15–19 Nov | Close every Shikfa comment on your sections (done when none are open in `reports/final-report/feedback.md`). Build slides: data + baseline. | Logbook Sun 22 Nov | ⬜ |

    Tick a task by changing ⬜ to ✅. If something is blocked, write it in `logbook-notes.md` and tell Naif.

    ## Files in this folder
    - `logbook-notes.md` – what you did each day + times (copy into the official logbook template)
    - `research-notes.md` – papers you read and what you learned
    - `slr/` – your SLR checklist (`TASKS.md`) and working files

## Status after Progress Report 2 (11 Nov 2026)
Taken from PR2 Table 4 and your Week 10–11 logbook. Correct anything that is wrong.

**Done (Weeks 10–11)**
- Screened own records 1–5 Nov (PR2 Table 3): Behera, Kapila, Shruthi & Naidu, Gogoi & Valan; second reader for Sayyad & Kulkarni and ICSCSP 2018
- (Your Week 10–11 logbook was not in the 11 Nov update – add anything else you did)

**Next (Weeks 12–13)** – the SLR now uses the refined set in [`research/slr/refined-2026-10-29/`](../../research/slr/refined-2026-10-29/); the old Set 1–3 screening tasks in `slr/TASKS.md` are superseded.
- [ ] Finalise the plaintext baselines on both datasets: `python code/pilots/baseline/train_baseline.py` (decide default C vs `--tune`); record the numbers
- [ ] Get the full texts of Behera et al. and Kapila et al. through UDST (ask the librarian before E4)
- [ ] Draft final report: data + baseline methodology/results (use `code/data/DATA_DICTIONARY.md`); RQ3 with Hassan
