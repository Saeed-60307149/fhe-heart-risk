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

**Timing:** searches due Sun 11 Oct · title/abstract screening Week 8 · full text + extraction Week 10 · synthesis + PRISMA Week 12.

## Due Sun 11 Oct

- [ ] Everyone: read the protocol, send changes to Abdullah by **Sat 10 Oct**
- [ ] Khalid + Abdullah: Scopus search check first, then Scopus search
- [ ] Saif + Naif: IEEE Xplore search
- [ ] Sarim + Hassan: ACM Digital Library search
- [ ] First person in each pair runs it and fills the **Search Log** tab; partner re-runs it to confirm the count
- [ ] Hassan: de-duplicate in RefWorks, enter the count, split records at random into Pair 1/2/3 in the **Screening Log**
- [ ] Naif: add protocol + counts to Progress Report 1

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
