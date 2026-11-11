# Hassan Zahid
    **Program:** Information Technology
    **Main focus:** Environment/reproducibility, PRISMA tracking, data & ethics note, benchmarking, report formatting

    This is your own space. Put your research notes, drafts and logbook notes here.
    Only edit files inside your own folder (and the shared files in `meetings/` and `research/`).

    ## My tasks (from the Team Work Plan)
    | Week | Dates | Task | Due | Done |
    |---|---|---|---|---|
    | Wk 6 | 27 Sep–1 Oct | Check library database access + RefWorks. Set up the shared folder. Test the TenSEAL install on your machine. | Logbook Sun 4 Oct | ⬜ |
| Wk 7 | 4–8 Oct | Build the PRISMA tracking sheet (counts per database, duplicates). Re-run Sarim's PubMed search and confirm the count. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Write the ethics/data note with Sarim. De-duplicate (by script) and split records at random into Pairs 1–3 in the Screening Log. | PR1 + logbook Sun 11 Oct | ⬜ |
| Wk 8 | 11–15 Oct | Screen all of Set 2 (column H) with Sarim. Update PRISMA counts after screening. Write requirements.txt/setup notes for the pilot environment. | Thu 15 Oct (no logbook, mid-term – keep notes) | ⬜ |
| Wk 10 | 25–29 Oct | Plan the benchmark: encryption time, inference time, ciphertext size, and how to measure. Full-text screening of the other half of Pair 2's papers, with extraction + quality rows. | Logbook Sun 1 Nov | ⬜ |
| Wk 11 | 1–5 Nov | Time Saif's PoC: encryption/decryption time and ciphertext size vs plaintext. Backward snowballing on your included papers (Screening Log, Source = Snowballing). | PR2 + logbook Sun 8 Nov | ⬜ |
| Wk 12 | 8–12 Nov | Draw the PRISMA 2020 diagram; co-write SLR synthesis RQ3 with Sarim. Draft data/code availability, acknowledgments, references (IEEE). | Logbook Sun 15 Nov | ⬜ |
| Wk 13 | 15–19 Nov | Format the report (TNR 12, single-spaced), check references and numbering. Build slides: methodology + feasibility. | Logbook Sun 22 Nov | ⬜ |

    Tick a task by changing ⬜ to ✅. If something is blocked, write it in `logbook-notes.md` and tell Naif.

    ## Files in this folder
    - `logbook-notes.md` – what you did each day + times (copy into the official logbook template)
    - `research-notes.md` – papers you read and what you learned
    - `slr/` – your SLR checklist (`TASKS.md`) and working files

## Status after Progress Report 2 (11 Nov 2026)
Taken from PR2 Table 4 and your Week 10–11 logbook. Correct anything that is wrong.

**Done (Weeks 10–11)**
- Screened own records 1–5 Nov (PR2 Table 3): Data mining Cloud-IoT, Singh & Alphy, Concrete ML, FL-for-heart-disease review, Heartify
- (Your Week 10–11 logbook was not in the 11 Nov update – add anything else you did)

**Next (Weeks 12–13)** – the SLR now uses the refined set in [`research/slr/refined-2026-10-29/`](../../research/slr/refined-2026-10-29/); the old Set 1–3 screening tasks in `slr/TASKS.md` are superseded.
- [ ] Screen P029 (Dakhare 2024) – decision #14
- [ ] Review `design/benchmark-plan.md` (your Week 10 task, draft added 11 Nov); add machine details (CPU, RAM)
- [ ] After Saif's run: `python code/scripts/summarise_results.py` → tables in `code/results/README.md`
- [ ] PRISMA 2020 diagram for the report from `research/slr/refined-2026-10-29/prisma-flow.md` (re-run `prisma_counts.py --write` first)
- [ ] Verify seeded extraction rows P013, P028, P001; snowball the FL review (P016)
- [ ] Draft data/code availability, acknowledgements, references (IEEE); RQ3 with Sarim
