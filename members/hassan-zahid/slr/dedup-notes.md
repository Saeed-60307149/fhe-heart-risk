# De-duplication notes – Hassan

Tool used: de-duplication script (not RefWorks) · Date: 10 Oct 2026 · Results: [SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx](../../../research/slr/dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx) in [research/slr/dedup/](../../../research/slr/dedup/)

Export files are in [research/slr/exports/](../../../research/slr/exports/); search counts are in [search-log.md](../../../research/slr/search-log.md).

## Records imported

| Database | Export file | Records imported | Matches Search Log tab count? |
|---|---|---|---|
| IEEE Xplore | `IEEE_2026-10-10_p1.ris` – `p4.ris` | 337 | Yes |
| PubMed | `PubMed_2026-10-10.nbib` | 172 | Yes |
| Scopus | `Scopus_2026-10-10.ris` | 1,017 | Yes |
| **Total identified** | | **1,526** | Yes |

## Duplicates

| Item | Value |
|---|---|
| Method (auto-detect, manual check, both) | Both: script matched same DOI (474), same title after removing case/punctuation (6), near-identical title with year within 1 (2); 4 similar-title pairs checked by hand and kept apart |
| Duplicates removed | 482 (listed in the workbook's *Duplicates Removed* tab) |
| Records left to screen | 1,044 |
| Set 1 (Pair 1: Saif, Naif) – count | 348 |
| Set 2 (Pair 2: Sarim, Hassan) – count | 348 |
| Set 3 (Pair 3: Khalid, Abdullah) – count | 348 |

## Notes / problems

- Kept the copy with an abstract (Scopus > PubMed > IEEE). Random split with fixed seed 20261010, so it can be repeated.
- Search check: Kim JMIR 2018 was not found by any database; it is added as 1 record identified from other sources (approved by Abdullah, 10 Oct 2026). See [search-log.md](../../../research/slr/search-log.md#search-check-10-oct-2026-all-databases).

**Next (before Mon 12 Oct):** enter 482 in "Duplicate records removed" on the **PRISMA Counts** tab and paste the 1,044 records into the **Screening Log** of a new `PRISMA_Tracking_Sheet_2026-10-11.xlsx` in [research/slr/](../../../research/slr/). The column order differs from the dedup workbook – follow the steps in [search-log.md](../../../research/slr/search-log.md).
