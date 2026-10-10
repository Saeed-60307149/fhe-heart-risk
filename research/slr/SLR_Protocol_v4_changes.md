# SLR Protocol v4 – changes from v3

10 Oct 2026 · Protocol owner: Abdullah Dar

Protocol v3 ([protocol.md](protocol.md), [SLR_Protocol_v3.pdf](SLR_Protocol_v3.pdf)) stays as the record of the plan. This file lists what changed when the searches were run on 10 Oct 2026. **The review questions (RQ1–RQ4), PICOC, and inclusion/exclusion criteria (I1–I5, E1–E6) are unchanged.**

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

## Search totals after the changes

| Database | Results |
|---|---|
| IEEE Xplore | 337 |
| PubMed | 172 |
| Scopus | 1,017 |
| **Total before de-duplication** | **1,526** |

Full details: [search-log.md](search-log.md) · Export files: [exports/](exports/)
