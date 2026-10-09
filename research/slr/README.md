# Systematic Literature Review (SLR)

A **systematic literature review** answers fixed research questions by searching set databases with a written, repeatable search string, then screening every result against criteria agreed in advance. Every decision (search string, date, counts, why each paper was excluded) is logged, so anyone can repeat the review and get the same papers. The numbers feed a **PRISMA** flow diagram showing how many records were found, removed and finally included. Our review asks how FHE has been used for ML inference on health data, and at what cost. The full rules are in [protocol.md](protocol.md) (Word original: [SLR_Protocol_v2.docx](SLR_Protocol_v2.docx)).

## The 10 steps and which file each one uses

| # | Step | File(s) |
|---|---|---|
| 1 | Research questions + PICOC | [protocol.md](protocol.md) |
| 2 | Inclusion / exclusion criteria (I1–I5, E1–E6) | [protocol.md](protocol.md) |
| 3 | Search string | [search-strings.md](search-strings.md) |
| 4 | Search IEEE Xplore / ACM DL / Scopus | [search-log.csv](search-log.csv) · `members/{saif,sarim,khalid}/slr/*-search-notes.md` |
| 5 | Remove duplicates | [prisma-tracking.csv](prisma-tracking.csv) · `members/hassan-zahid/slr/dedup-notes.md` |
| 6 | Title / abstract screening | `members/saif/slr/screening-set-A.csv` · `members/sarim/slr/screening-set-B.csv` · `members/khalid/slr/second-screening-sample.csv` |
| 7 | Full-text screening | [prisma-tracking.csv](prisma-tracking.csv) (exclusion codes E1–E6) · [quality-assessment.csv](quality-assessment.csv) |
| 8 | Data extraction | [data-extraction.csv](data-extraction.csv) |
| 9 | Synthesis + PRISMA diagram | [data-extraction.csv](data-extraction.csv) · [prisma-tracking.csv](prisma-tracking.csv) |
| 10 | Write-up | `reports/progress-report-1/` → `reports/final-report/` |

## Files in this folder

| File | What it is | Owner |
|---|---|---|
| `SLR_Protocol_v2.docx` | Protocol, Word original | Abdullah |
| `protocol.md` | Same protocol, readable on GitHub | Abdullah |
| `search-strings.md` | The three exact search strings, filters and rules | Everyone (read-only unless the team agrees a change) |
| `search-log.csv` | One row per database search: string, date, filters, result count | Saif, Sarim, Khalid |
| `prisma-tracking.csv` | Counts at every PRISMA stage | Hassan |
| `quality-assessment.csv` | Q1–Q5 score per included paper | Whoever extracts the paper |
| `data-extraction.csv` | One row per included paper (answers RQ1–RQ4) | Whoever extracts the paper |

**Quality scoring (quality-assessment.csv):** Yes = 1, Partly = 0.5, No = 0 for each of Q1–Q5. `total` = sum out of 5. Set `low_quality_flag` = `yes` if total < 2.5. Low-quality papers are kept but flagged in the synthesis.

**Never estimate a count.** If a number isn't known yet, leave the cell empty.

> Note: the repo's `.gitignore` ignores `*.csv` (to keep datasets out). An exception has been added for `research/slr/*.csv` and `members/*/slr/*.csv` so these tracking sheets are committed.

## Task table

| Person | Task | File | Due |
|---|---|---|---|
| Naif, Saif | Review research questions, PICOC and criteria with the team | [protocol.md](protocol.md) | Sun 11 Oct |
| Saif | Run IEEE Xplore search, fill search log | [search-log.csv](search-log.csv), `members/saif/slr/ieee-search-notes.md` | Sun 11 Oct |
| Sarim | Run ACM DL search, fill search log | [search-log.csv](search-log.csv), `members/sarim/slr/acm-search-notes.md` | Sun 11 Oct |
| Khalid | Scopus search check, then Scopus search, fill search log | [search-log.csv](search-log.csv), `members/khalid/slr/scopus-search-notes.md` | Sun 11 Oct |
| Hassan | Export to RefWorks, remove duplicates, start PRISMA sheet | [prisma-tracking.csv](prisma-tracking.csv), `members/hassan-zahid/slr/dedup-notes.md` | Sun 11 Oct |
| Naif | Add protocol + search counts to Progress Report 1 | `members/naif/slr/progress-report-1-checklist.md` | Sun 11 Oct |
| Saif | Title/abstract screening, Set A | `members/saif/slr/screening-set-A.csv` | Wk 8 (Thu 15 Oct) |
| Sarim | Title/abstract screening, Set B | `members/sarim/slr/screening-set-B.csv` | Wk 8 (Thu 15 Oct) |
| Khalid | Second screener, random 20% of Set A | `members/khalid/slr/second-screening-sample.csv` | Wk 8 (Thu 15 Oct) |
| Naif | Settle screening disagreements | `members/khalid/slr/second-screening-sample.csv` | Wk 8 (Thu 15 Oct) |
| Hassan | Update PRISMA counts after every stage | [prisma-tracking.csv](prisma-tracking.csv) | Ongoing |
| Abdullah | Keep protocol.md and the docx in sync; track progress against this table | [protocol.md](protocol.md), this README | Ongoing |
