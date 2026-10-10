# Decision Log
| # | Date | Decision | Why | Decided by |
|---|---|---|---|---|
| 1 | 27 Sep 2026 | Use CKKS scheme via TenSEAL | Supports real numbers, fits logistic regression | Team |
| 2 | 27 Sep 2026 | One GitHub repo for research (Sem 1) and code (Sem 2) | One place for everything | Team |
| 3 | 1 Oct 2026 | IRB: | | Supervisor |
| 4 | 1 Oct 2026 | Databases for SLR: | | Supervisor |
| 5 | 9 Oct 2026 | SLR Protocol v2 drafted: RQ1–RQ4, PICOC, search string A AND B AND C on IEEE Xplore / ACM DL / Scopus (2016–2026), criteria I1–I5 / E1–E6, 20% second screening, Q1–Q5 quality check (see `research/slr/protocol.md`) | Repeatable search and screening for PR1 | Abdullah Dar (draft) – pending review by Naif + Saif |
| 6 | 9 Oct 2026 | SLR Protocol v3: three fixed pairs (IEEE: Saif + Naif, ACM: Sarim + Hassan, Scopus: Khalid + Abdullah); every record screened by both pair members; tie-breakers Naif (Pairs 2, 3) and Abdullah (Pair 1); PRISMA tracking sheet replaces the search-log/PRISMA CSVs | Work shared evenly; full double screening is stronger than a 20% sample | Abdullah Dar (protocol owner) – team to review by Sat 10 Oct |
| 7 | 10 Oct 2026 | SLR Protocol v4 changes: ACM Digital Library replaced by PubMed for Pair 2; Scopus kept at the full 1,017 results (narrowing tested: 766 and 855). Searches: IEEE 337, PubMed 172, Scopus 1,017, total 1,526 (see `research/slr/SLR_Protocol_v4_changes.md`) | No UDST ACM subscription (filters and export locked); narrowing Scopus still left it far over the 400 limit | Team |
| 8 | 10 Oct 2026 | De-duplication by script instead of RefWorks (same DOI 474, same title 6, near-identical title 2 = 482 removed; 1,044 to screen in 3 random sets of 348, seed 20261010). Search check: Kim JMIR 2018 not found by any database → added as 1 record from other sources and reported as a limitation (see `research/slr/SLR_Protocol_v4_changes.md`, changes 3–4) | Transparent, reproducible matching; loosening concept C to catch Kim JMIR would break the health-data scope | Hassan (de-duplication); Abdullah Dar (protocol owner) approved the Kim JMIR fix |
