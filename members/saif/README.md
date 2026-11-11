# Saif
    **Program:** Cyber Security
    **Main focus:** FHE/TenSEAL pilot, node-seal compatibility (Plan A/B), key-management feasibility

    This is your own space. Put your research notes, drafts and logbook notes here.
    Only edit files inside your own folder (and the shared files in `meetings/` and `research/`).

    ## My tasks (from the Team Work Plan)
    | Week | Dates | Task | Due | Done |
    |---|---|---|---|---|
    | Wk 6 | 27 Sep–1 Oct | Find 2–3 existing reviews/surveys on FHE or privacy-preserving ML. Note title, year, what each covers. | Logbook Sun 4 Oct | ⬜ |
| Wk 7 | 4–8 Oct | Draft search strings. Run IEEE Xplore and fill the IEEE row of the Search Log tab (string, date, filters, count); Naif re-runs it to confirm. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Write PR1 feasibility/risk paragraph. | PR1 + logbook Sun 11 Oct | ⬜ |
| Wk 8 | 11–15 Oct | Screen titles/abstracts for all of Set 1 with Naif (SLR v3, Pair 1). Draft the pilot method (encrypt → dot product → decrypt) as your section of `reports/progress-report-2/methodology-v1.md`. | Thu 15 Oct (no logbook, mid-term – keep notes) | ⬜ |
| Wk 10 | 25–29 Oct | Pilot: TenSEAL toy example on CKKS (encrypt, add, multiply by plaintext, decrypt). Full-text screening of your half of Pair 1's papers, with extraction + quality rows. | Logbook Sun 1 Nov | ⬜ |
| Wk 11 | 1–5 Nov | Test whether a node-seal ciphertext loads in TenSEAL. Write the Plan A/B recommendation. Backward snowballing on your included papers (Screening Log, Source = Snowballing). | PR2 + logbook Sun 8 Nov | ⬜ |
| Wk 12 | 8–12 Nov | Draft final report: Background (FHE schemes) + cryptographic methodology + pilot results. Co-write SLR synthesis RQ1 + RQ4 with Naif. | Logbook Sun 15 Nov | ⬜ |
| Wk 13 | 15–19 Nov | Close every Shikfa comment on your sections (done when none are open in `reports/final-report/feedback.md`). Build slides: background + pilot. | Logbook Sun 22 Nov | ⬜ |

    Tick a task by changing ⬜ to ✅. If something is blocked, write it in `logbook-notes.md` and tell Naif.

    ## Files in this folder
    - `logbook-notes.md` – what you did each day + times (copy into the official logbook template)
    - `research-notes.md` – papers you read and what you learned
    - `slr/` – your SLR checklist (`TASKS.md`) and working files

## Status after Progress Report 2 (11 Nov 2026)
Taken from PR2 Table 4 and your Week 10–11 logbook. Correct anything that is wrong.

**Done (Weeks 10–11)**
- Pilot environment with pinned versions (Python 3.12, Node 22, node-seal 7.0.0, TenSEAL 0.3.16)
- Toy examples; node-seal encrypt/decrypt check, sizes and max error (29 Oct)
- Encrypted pilot on UCI Cleveland (PR2 Table 5) and re-run before submission
- Cross-library round trip node-seal → TenSEAL → node-seal (z = 0.877, Wk 11)
- Re-ran and confirmed the IEEE Xplore count; screened own 6 (Kim 2018, Naresh & Reddi, Murali, Poonam, MediVault, ICSCSP)

**Next (Weeks 12–13)** – the SLR now uses the refined set in [`research/slr/refined-2026-10-29/`](../../research/slr/refined-2026-10-29/); the old Set 1–3 screening tasks in `slr/TASKS.md` are superseded.
- [ ] Run `bash code/scripts/run_pilot.sh` on your machine → official numbers for both datasets and both layouts; commit `code/results/`
- [ ] Screen P011 (Janagama 2026) – decision #14
- [ ] Report the per-feature + encrypted-sigmoid numbers (relin keys instead of 164 MB Galois keys) – the chosen layout, decision #15
- [ ] Verify the seeded extraction rows P035 (Kim) and P014 (Naresh & Reddi) against the papers
- [ ] Draft final report: Background (FHE schemes) + cryptographic methodology + pilot results; RQ1 + RQ4 with Naif
