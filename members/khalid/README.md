# Khalid
    **Program:** Artificial Intelligence
    **Main focus:** Polynomial sigmoid approximation + validation, evaluation

    This is your own space. Put your research notes, drafts and logbook notes here.
    Only edit files inside your own folder (and the shared files in `meetings/` and `research/`).

    ## My tasks (from the Team Work Plan)
    | Week | Dates | Task | Due | Done |
    |---|---|---|---|---|
    | Wk 6 | 27 Sep–1 Oct | Find papers on polynomial approximation of sigmoid for encrypted logistic regression. | Logbook Sun 4 Oct | ⬜ |
| Wk 7 | 4–8 Oct | Run the Scopus search check (3 known papers), then the Scopus search; fill the Scopus row of the Search Log tab; Abdullah re-runs both to confirm. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Write the PR1 'Expected results' section. | PR1 + logbook Sun 11 Oct | ⬜ |
| Wk 8 | 11–15 Oct | Screen titles/abstracts for all of Set 3 with Abdullah (SLR v3, Pair 3). Draft the polynomial-sigmoid method as your section of `reports/progress-report-2/methodology-v1.md`. | Thu 15 Oct (no logbook, mid-term – keep notes) | ⬜ |
| Wk 10 | 25–29 Oct | Pilot: fit a polynomial approximation of sigmoid over the expected score range and plot vs real sigmoid. Full-text screening of your half of Pair 3's papers, with extraction + quality rows. | Logbook Sun 1 Nov | ⬜ |
| Wk 11 | 1–5 Nov | Rerun test-set predictions with the polynomial instead of real sigmoid; compare with Sarim's metrics; pass/fail. Backward snowballing on your included papers (Screening Log, Source = Snowballing). | PR2 + logbook Sun 8 Nov | ⬜ |
| Wk 12 | 8–12 Nov | Draft final report: sigmoid approximation methodology/results and expected outcomes. Co-write SLR synthesis RQ2 with Abdullah. | Logbook Sun 15 Nov | ⬜ |
| Wk 13 | 15–19 Nov | Close every Shikfa comment on your sections (done when none are open in `reports/final-report/feedback.md`). Build slides: sigmoid approximation + expected results. | Logbook Sun 22 Nov | ⬜ |

    Tick a task by changing ⬜ to ✅. If something is blocked, write it in `logbook-notes.md` and tell Naif.

    ## Files in this folder
    - `logbook-notes.md` – what you did each day + times (copy into the official logbook template)
    - `research-notes.md` – papers you read and what you learned
    - `slr/` – your SLR checklist (`TASKS.md`) and working files

## Status after Progress Report 2 (11 Nov 2026)
Taken from PR2 Table 4 and your Week 10–11 logbook. Correct anything that is wrong.

**Done (Weeks 10–11)**
- Team planning 25 Oct; supervisor meeting 29 Oct; checked PRISMA exclusion labels and outlined the RQ3 cost-evidence table (31 Oct)
- Screened own records 3–5 Nov: GuardML, Nguyen (DASC), Sayyad & Kulkarni, Naresh & Varma (retracted), Yadkar, Sravani & Kumar

**Next (Weeks 12–13)** – the SLR now uses the refined set in [`research/slr/refined-2026-10-29/`](../../research/slr/refined-2026-10-29/); the old Set 1–3 screening tasks in `slr/TASKS.md` are superseded.
- [ ] Run `python code/pilots/sigmoid/fit_sigmoid.py` on both datasets; check the plot `code/results/<ds>/sigmoid_vs_poly.png`; pass at ≥90% decision match (RQ-A), and say whether the 95% expected result is reached (decision #16)
- [ ] Verify seeded extraction rows P034 (GuardML) and P005 (Nguyen) against the papers
- [ ] Get full texts: Sayyad & Kulkarni, Yadkar et al., Sravani & Kumar
- [ ] Draft final report: sigmoid approximation methodology/results; RQ2 with Abdullah
