# Systematic Literature Review (SLR)

A **systematic literature review** answers fixed research questions by searching set databases with a written, repeatable search string, then screening every result against criteria agreed in advance. Every decision (search string, date, counts, why each paper was excluded) is logged, so anyone can repeat the review and get the same papers. The numbers feed a **PRISMA** flow diagram showing how many records were found, removed and finally included. Our review asks how FHE has been used for ML inference on health data, and at what cost. The full rules are in [protocol.md](protocol.md) (Protocol v3; PDF: [SLR_Protocol_v3.pdf](SLR_Protocol_v3.pdf)).

## Where the live files are

LIVE LINK: <add link>

- The **live** PRISMA tracking sheet and the **live** protocol are edited in our shared OneDrive/SharePoint folder (link above), **not in the repo**.
- **Nobody edits the `.xlsx` or `.docx` in the repo directly.** The copies here are snapshots.
- At each milestone (after searches, after title/abstract screening, after full text, final), **Hassan** commits a new dated snapshot `PRISMA_Tracking_Sheet_YYYY-MM-DD.xlsx` here and moves the previous one to [archive/](archive/).
- The protocol is re-committed only when its version number changes (Abdullah). The old version goes to [archive/](archive/).

## The 10 steps and which file each one uses

"Sheet" = the live PRISMA tracking sheet (snapshot: `PRISMA_Tracking_Sheet_YYYY-MM-DD.xlsx`).

| # | Step | File / tab |
|---|---|---|
| 1 | Research questions + PICOC | [protocol.md](protocol.md) |
| 2 | Inclusion / exclusion criteria (I1–I5, E1–E6) | [protocol.md](protocol.md) |
| 3 | Search string | [search-strings.md](search-strings.md) |
| 4 | Search IEEE Xplore / ACM DL / Scopus | Sheet → **Search Log** tab |
| 5 | Remove duplicates (RefWorks), split into Sets 1–3 | Sheet → **PRISMA Counts** + **Screening Log** tabs |
| 6 | Title / abstract screening (both pair members, independently) | Sheet → **Screening Log** (screener 1 = column G, screener 2 = column H) |
| 7 | Full-text screening | Sheet → **Screening Log** (full-text reader, decision, exclusion code) |
| 8 | Data extraction + quality scoring | [data-extraction.csv](data-extraction.csv), [quality-assessment.csv](quality-assessment.csv) |
| 9 | Synthesis + PRISMA diagram | Data extraction + Sheet → **PRISMA Counts** |
| 10 | Write-up | `reports/progress-report-1/` → `reports/final-report/` |

## Team

| Pair | Members | Search (runs / confirms) | Screening set | Synthesis |
|---|---|---|---|---|
| Pair 1 | Saif, Naif | IEEE Xplore (Saif runs, Naif confirms) | Set 1 | RQ1, RQ4 |
| Pair 2 | Sarim, Hassan | ACM Digital Library (Sarim runs, Hassan confirms) | Set 2 | RQ3 |
| Pair 3 | Khalid, Abdullah | Scopus + search check (Khalid runs, Abdullah confirms) | Set 3 | RQ2 |

Extra roles:
- **Hassan:** de-duplication, splitting records into sets, PRISMA sheet + diagram, and repo snapshots.
- **Naif:** tie-breaker for Pairs 2 and 3, and progress reports.
- **Abdullah:** protocol owner, and tie-breaker for Pair 1.

Each person's checklist is in `members/<name>/slr/TASKS.md`.

**Timing:** searches due Sun 11 Oct · title/abstract screening Week 8 (Mon 12–Thu 15 Oct) · full-text decisions Week 10 · extraction + quality Weeks 10–11 · snowballing Week 11 · synthesis + PRISMA Week 12.

## Due Sun 11 Oct

- [ ] Each of the six (Naif, Saif, Sarim, Khalid, Hassan, Abdullah): reply 'changes' or 'no changes' on the protocol to Abdullah by **Sat 10 Oct**. Done when all six replies are ticked in `members/abdullah-dar/slr/TASKS.md`
- [ ] Khalid + Abdullah: Scopus search check first, then Scopus search
- [ ] Saif + Naif: IEEE Xplore search
- [ ] Sarim + Hassan: ACM Digital Library search
- [ ] First person in each pair runs it and fills the **Search Log** tab; partner re-runs it to confirm the count
- [ ] Hassan: de-duplicate in RefWorks, enter the count, split records at random into Pair 1/2/3 in the **Screening Log**
- [ ] Naif: add protocol + counts to Progress Report 1

## Week 7 schedule (draft, 9 Oct)

Planned slots for the work due before Progress Report 1. Each slot is also a **Planned** row in that person's `logbook-notes.md`. Confirmations follow straight after the run they check; Hassan de-duplicates after all three counts are confirmed; Naif writes the SLR section after the counts and compiles PR1 after every section is in.

| Day | Time | Who | Task | Maps to |
|---|---|---|---|---|
| Fri 9 Oct | 20:30–21:30 | Hassan | Read SLR Protocol v3 (`research/slr/protocol.md`) and send 'changes' or 'no changes' to Abdullah | Protocol v3 to-do (Gantt 2.2 review) |
| Fri 9 Oct | 20:30–21:30 | Khalid | Read SLR Protocol v3 (`research/slr/protocol.md`) and send 'changes' or 'no changes' to Abdullah | Protocol v3 to-do (Gantt 2.2 review) |
| Fri 9 Oct | 20:30–21:30 | Naif | Read SLR Protocol v3 (`research/slr/protocol.md`) and send 'changes' or 'no changes' to Abdullah | Protocol v3 to-do (Gantt 2.2 review) |
| Fri 9 Oct | 20:30–21:30 | Saif | Read SLR Protocol v3 (`research/slr/protocol.md`) and send 'changes' or 'no changes' to Abdullah | Protocol v3 to-do (Gantt 2.2 review) |
| Fri 9 Oct | 20:30–21:30 | Sarim | Read SLR Protocol v3 (`research/slr/protocol.md`) and send 'changes' or 'no changes' to Abdullah | Protocol v3 to-do (Gantt 2.2 review) |
| Sat 10 Oct | 10:00–11:30 | Khalid | Scopus search check (3 known papers found?), then the logged Scopus run; log date, exact string and ___ results in the Search Log tab; export the records for Hassan | Gantt 2.4 / protocol search check |
| Sat 10 Oct | 10:00–11:00 | Saif | Test, then run the logged IEEE Xplore string (2016–2026, Conferences + Journals); log date, exact string, filters and ___ results in the Search Log tab; export the records for Hassan | Gantt 2.4 |
| Sat 10 Oct | 10:00–11:00 | Sarim | Test, then run the logged ACM Digital Library string (2016–2026, Research Article); log date, exact string, filters and ___ results in the Search Log tab; export the records for Hassan | Gantt 2.4 |
| Sat 10 Oct | 11:00–11:30 | Hassan | Re-run Sarim's ACM string, confirm the count (___) and tick 'Confirmed by' in the Search Log tab | Gantt 2.4 |
| Sat 10 Oct | 11:00–11:30 | Naif | Re-run Saif's IEEE Xplore string, confirm the count (___) and tick 'Confirmed by' in the Search Log tab | Gantt 2.4 |
| Sat 10 Oct | 11:30–12:30 | Abdullah | Confirm Khalid's Scopus search check (3/3 papers) and re-run the Scopus string; tick 'Confirmed by' in the Search Log tab (count: ___) | Gantt 2.4 / protocol search check |
| Sat 10 Oct | 13:00–15:00 | Hassan | Import the three exports into RefWorks, remove duplicates, type 'Duplicate records removed' on the PRISMA Counts tab, split records at random into Pair 1/2/3 in the Screening Log; commit a dated sheet snapshot | Gantt 2.5 |
| Sat 10 Oct | 13:00–14:30 | Khalid | Write the PR1 'Expected results' section (sigmoid approximation accuracy vs the plaintext baseline) | Work plan Wk 7 (no Gantt task) |
| Sat 10 Oct | 13:00–15:00 | Saif | Write the PR1 feasibility/risk paragraph (TenSEAL vs node-seal risk, key management, Plan A/B) | Work plan Wk 7 (no Gantt task) |
| Sat 10 Oct | 15:30–17:00 | Hassan | Write the PR1 data statement with Sarim: UCI Heart Disease source, licence, size, fields, personal-data check | Work plan Wk 7 (no Gantt task) |
| Sat 10 Oct | 15:30–17:00 | Naif | Write the SLR section of Progress Report 1: RQs, PICOC, databases and pairs, criteria, results per database, duplicates removed, records to screen | Gantt 5.1 / protocol to-do |
| Sat 10 Oct | 15:30–17:00 | Sarim | Write the PR1 data statement with Hassan: UCI Heart Disease source, licence, size, fields, personal-data check | Work plan Wk 7 (no Gantt task) |
| Sat 10 Oct | 18:00–18:30 | Abdullah | Collect the six 'changes / no changes' replies on Protocol v3 and update the live protocol (new version only if something changed) | Gantt 2.2 (protocol owner) |
| Sat 10 Oct | 18:30–19:30 | Abdullah | Update the task board: Week 8 cards for screening Sets 1–3, methodology outline and workflow diagram, each with an owner | Gantt 3.1 (work plan Wk 7: update the task board) |
| Sun 11 Oct | 10:00–11:30 | Hassan | Fill `research/ethics-data-note.md` with Sarim: dataset link, licence, personal data, IRB decision | Ethics/data note (owners Sarim + Hassan; no Gantt task) |
| Sun 11 Oct | 10:00–11:30 | Sarim | Fill `research/ethics-data-note.md` with Hassan: dataset link, licence, personal data, IRB decision | Ethics/data note (owners Sarim + Hassan; no Gantt task) |
| Sun 11 Oct | 12:00–14:00 | Naif | Compile Progress Report 1: merge the work distribution, feasibility/risk, data statement, expected results and SLR sections into one document | Gantt 5.1 |
| Sun 11 Oct | 15:00–16:00 | Naif | Final check of PR1 (numbers match the PRISMA sheet), save it to `reports/progress-report-1/` and submit on D2L | Gantt 5.1 / PR1 due Sun 11 Oct |

## Files in this folder

| File | What it is | Owner |
|---|---|---|
| `SLR_Protocol_v3.pdf` | Protocol v3 (snapshot of the live protocol) | Abdullah |
| `protocol.md` | Same protocol, readable on GitHub | Abdullah |
| `search-strings.md` | The three exact search strings, filters and rules | Everyone (change only if the team agrees) |
| `PRISMA_Tracking_Sheet_2026-10-09.xlsx` | Snapshot of the PRISMA sheet (tabs: How to use, PRISMA Counts, Lists, Search Log, Screening Log). Replaces the old search-log and PRISMA CSVs | Hassan |
| `data-extraction.csv` | One row per included paper (answers RQ1–RQ4); `checked_by` = partner who spot-checked | Full-text reader |
| `quality-assessment.csv` | Q1–Q5 score per included paper; `checked_by` = partner | Full-text reader |
| `archive/` | Protocol v2, old CSVs, old sheet snapshots | – |

**Quality scoring:** Yes = 1, Partly = 0.5, No = 0 for each of Q1–Q5. `total` = sum out of 5. Set `low_quality_flag` = `yes` if total < 2.5. Low-quality papers are kept but flagged in the synthesis.

**Never estimate a count.** If a number isn't known yet, leave the cell empty.

> The repo's `.gitignore` ignores `*.csv` (to keep datasets out). An exception allows `research/slr/*.csv` and `members/*/slr/*.csv`.
