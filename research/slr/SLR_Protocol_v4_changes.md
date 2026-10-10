# SLR Protocol v4 – changes from v3

10 Oct 2026 · Protocol owner: Abdullah Dar

Protocol v3 ([protocol.md](protocol.md), [SLR_Protocol_v3.pdf](SLR_Protocol_v3.pdf)) stays as the record of the plan. This file lists what changed when the searches and de-duplication were done on 10 Oct 2026. **The review questions (RQ1–RQ4), PICOC, and inclusion/exclusion criteria (I1–I5, E1–E6) are unchanged.**

## 1. ACM Digital Library replaced by PubMed

| | v3 | v4 |
|---|---|---|
| Pair 2 database | ACM Digital Library | **PubMed** |
| Run by / confirmed by | Sarim / Hassan | Sarim / Hassan (unchanged) |
| Fields searched | Abstract | Title and abstract (`[tiab]`) |
| Filters | Publication date 2016–2026; Research Article | In the string: `2016:2026[dp]`, `english[la]` |

**Why:** UDST has no ACM Digital Library subscription, so the search filters and the export were locked. PubMed is free, allows a full export, and covers health and biomedical research, which fits concept C (health).

**Result:** 172 records (10 Oct 2026). The exact string is in [search-strings.md](search-strings.md#pubmed-advanced-search--pair-2-sarim-runs-hassan-confirms) and [search-log.md](search-log.md#pubmed).

## 2. Scopus kept above the 400-result limit

v3 rule: if any database returns more than about 400 results, narrow concept B to its first four terms in all three databases.

**What happened:** Scopus returned 1,017 records with the unchanged v3 string. Narrowing was tested and still gave 766 and 855 results, both well over the limit.

**Decision (team, 10 Oct 2026):** keep the full 1,017 Scopus records and do not narrow any database. The string is unchanged.

## 3. De-duplication by script instead of RefWorks

v3 step 1 of screening: export all records into RefWorks (or Rayyan) and remove duplicates.

**What was done (10 Oct 2026):** the six export files were merged and de-duplicated by an automated script, in three passes:

| Match rule | Duplicates removed |
|---|---|
| Same DOI (case-insensitive) | 474 |
| Same title after removing case and punctuation | 6 |
| Near-identical title (97%+ similar) with year within 1 | 2 |
| **Total** | **482** |

When copies matched, the copy with an abstract was kept (Scopus > PubMed > IEEE). 4 pairs with 90–96% similar titles were checked by hand and kept as different papers. The 1,044 remaining records were split at random (fixed seed 20261010) into 3 sets of 348. Everything is in [dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx](dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx): *Screening Log* (the 1,044 records and their sets), *Duplicates Removed* (the 482 removed copies and why), *PRISMA Counts* and *Search Check*.

**Why:** the matching rules are written down, every removed record is listed with its reason, and the split can be repeated from the seed, which makes it more transparent and reproducible than a manual RefWorks pass.

## 4. Search check: Kim JMIR 2018 not found by any database

v3 rule: before the logged run, Scopus must find three known on-topic papers; if one is missing, find which concept failed, fix the string, and note the change.

**Result (10 Oct 2026, checked in all three databases):**
- Kim, A. et al. (2018), *BMC Medical Genomics*: found in Scopus.
- Chen, H. et al. (2018), *BMC Medical Genomics*: found in PubMed and Scopus.
- Kim, M. et al. (2018), *JMIR Medical Informatics*: **not found by any database.** It is indexed in PubMed (PMID 29666041), but its record has no health terms, so concept C (health) misses it.

**Why the string was not fixed:** the failing concept is C, and this record contains none of its health terms. The only way to catch it would be to drop or loosen concept C, which would let in encrypted-ML papers that are not about health data and break the review's scope (health data, criterion I2). Adding more health terms cannot help, because the record has none.

**Fix:** add Kim JMIR 2018 to the PRISMA diagram as **1 record identified from other sources**, and report the miss as a **limitation** (records that describe health data without health terms in their title, abstract or keywords can be missed by the search).

**Approved by Abdullah (protocol owner), 10 Oct 2026.**

## Search totals after the changes

| Database | Results |
|---|---|
| IEEE Xplore | 337 |
| PubMed | 172 |
| Scopus | 1,017 |
| **Total before de-duplication** | **1,526** |
| Duplicates removed | 482 |
| **Records to screen** | **1,044** (3 sets of 348) |
| Identified from other sources | 1 (Kim JMIR 2018, change 4) |

Full details: [search-log.md](search-log.md) · Export files: [exports/](exports/) · De-duplication: [dedup/](dedup/)
