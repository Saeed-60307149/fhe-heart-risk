# Refined search set (Protocol v5, from 29 Oct 2026)

This is the **current** SLR record set. The 10 Oct broad search (1,044 records) in the parent
folder is superseded and kept only as history.

| File | What | Edit? |
|---|---|---|
| [`screening-decisions.csv`](screening-decisions.csv) | **Source of truth**: one row per record – reviewer, what was checked, decision, code, reason (PR2 Table 3) + the 4 unscreened records + Kim 2018 (other sources) | Yes – after every decision |
| [`prisma-flow.md`](prisma-flow.md) | PRISMA 2020 numbers and Mermaid diagram, generated | No – run `python research/slr/scripts/prisma_counts.py --write` |
| `PRISMA_Screening_Sheet_2026-11-11.xlsx` | The team's sheet with PR2 decisions filled in; yellow rows = not yet screened; P035 = Kim 2018 | Yes (one person at a time); keep in step with the CSV |
| `PRISMA_Screening_Sheet_2026-11-06_as-built.xlsx` | Sheet exactly as rebuilt by Naif on 6–7 Nov (reference) | No |
| `FHE_Extraction_Form_v1.1_2026-11-11_seeded.xlsx` | Extraction form with rows for the 14 included records (incl. 2 partial HE), **seeded only with facts from each reviewer's logbook / PR2** – every value must be checked against the paper | Yes |
| `FHE_Extraction_Form_v1.0_2026-10-28.xlsx` | Blank form v1.0 (reference) | No |
| [`exports/`](exports/) | Raw search exports (Scopus CSV; IEEE export still to add) | No |

## Week 12 to-do (in order)

- [ ] Screen the 4 unassigned records (decision #14): P002 Dziri 2025 → Naif, P011 Janagama 2026 → Saif, P023 ICIC 2019 → Abdullah, P029 Dakhare 2024 → Hassan
- [x] Partial HE settled 11 Nov (decision #17): MediVault and Akter included as a partial-HE subgroup
- [ ] Get the 6 full texts through UDST (ask the librarian before E4): Sayyad & Kulkarni, Sun et al., Behera et al., Kapila et al., Yadkar et al., Sravani & Kumar
- [ ] Read the TrustFedHealth full text (included on abstract only)
- [ ] Second reviewer re-checks every excluded record (record who in the CSV `second_reader` column)
- [ ] Extraction + quality score (Q1–Q5) for every included record; partner fills *Checked by*
- [ ] Backward snowballing of P015, P016, P003; add finds as new rows (database = Other (by hand))
- [ ] Re-run `prisma_counts.py --write` and copy the numbers into the final report

## Reviewer assignment (PR2, 1–5 Nov 2026)

| Reviewer | Records (sheet IDs) |
|---|---|
| Naif | P008, P018, P010, P019, P020 |
| Saif | P035 (Kim), P014, P009, P015, P003, P021 |
| Saeed Abdullah Dar | P024, P006, P026, P025, P022, P027 |
| Hassan Zahid | P013, P028, P001, P016, P027 |
| Owais Khalid | P034, P005, P033, P004, P017, P012 |
| Muhammad Sarim | P007, P031, P032, P030, P033, P021 |
