# Search strings

## Change log

| Date | Change | Why |
|---|---|---|
| 10 Oct 2026 | **ACM Digital Library replaced by PubMed** for Pair 2 (Sarim runs, Hassan confirms). | UDST has no ACM subscription, so filters and export were locked. PubMed is free, allows full export and covers health research. |
| 10 Oct 2026 | **Scopus kept at the full 1,017 results** (string unchanged). | Over the 400-result limit, but narrowing concept B was tested and still gave 766 and 855 results, so the team decided to keep the full set. |

Details: [SLR_Protocol_v4_changes.md](SLR_Protocol_v4_changes.md) · Results: [search-log.md](search-log.md)

Source: SLR Protocol v3 ([protocol.md](protocol.md)), 9 Oct 2026, with the v4 changes above. Copy these **exactly** – do not reformat. If a string changes, record the new string and the reason in the **Search Log** tab of the PRISMA sheet in this folder (see [README.md](README.md)).

Master string: **A (encryption) AND B (machine learning) AND C (health)**.

The first person in each pair runs the logged search and fills the Search Log tab; the partner re-runs it the same day to confirm the count.

## IEEE Xplore (Command Search, Abstract field) – Pair 1: Saif runs, Naif confirms

```
("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE OR "Abstract":CKKS OR "Abstract":BFV OR "Abstract":BGV OR "Abstract":TenSEAL OR "Abstract":"Microsoft SEAL") AND ("Abstract":"machine learning" OR "Abstract":"logistic regression" OR "Abstract":"neural network" OR "Abstract":"deep learning" OR "Abstract":classif* OR "Abstract":predict* OR "Abstract":inference) AND ("Abstract":health* OR "Abstract":medical OR "Abstract":clinical OR "Abstract":patient* OR "Abstract":disease* OR "Abstract":biomedical OR "Abstract":diagnos* OR "Abstract":genom* OR "Abstract":cancer OR "Abstract":diabet* OR "Abstract":"heart disease" OR "Abstract":cardiovascular)
```

- **Filters:** Publication Year 2016 to 2026; Conferences and Journals.
- This string uses **8 wildcards**; IEEE Xplore allows at most 10 per search, so do not add more.

## PubMed (Advanced search) – Pair 2: Sarim runs, Hassan confirms

```
("homomorphic encryption"[tiab] OR "fully homomorphic"[tiab] OR FHE[tiab] OR CKKS[tiab] OR BFV[tiab] OR BGV[tiab] OR TenSEAL[tiab] OR "Microsoft SEAL"[tiab]) AND ("machine learning"[tiab] OR "logistic regression"[tiab] OR "neural network"[tiab] OR "deep learning"[tiab] OR classif*[tiab] OR predict*[tiab] OR inference[tiab]) AND (health*[tiab] OR medical[tiab] OR biomedical[tiab] OR clinical[tiab] OR patient*[tiab] OR disease*[tiab] OR diagnos*[tiab] OR genom*[tiab] OR cancer[tiab] OR diabet*[tiab] OR "heart disease"[tiab] OR cardiovascular[tiab]) AND 2016:2026[dp] AND english[la]
```

- **Filters:** in the string – publication date 2016 to 2026 (`2016:2026[dp]`) and English (`english[la]`). `[tiab]` searches the title and abstract.
- Replaces ACM Digital Library from 10 Oct 2026 (see the change log above).

## Scopus (Advanced document search) – Pair 3: Khalid runs, Abdullah confirms

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```

- **Filters:** in the string (PUBYEAR 2016–2026, English, DOCTYPE article + conference paper).
- Run the **search check** below first.

## Rules

1. IEEE Xplore searches the abstract only, PubMed (`[tiab]`) searches title and abstract, and Scopus searches title, abstract, and keywords. Abstracts almost always repeat the title's key terms, so this difference is small, but it is reported as a limitation.
2. Test each string before the logged run, and record the exact string actually used, the date, and the result count.
3. If any database returns more than about 400 results, narrow concept B to its first four terms (`"machine learning"`, `"logistic regression"`, `"neural network"`, `"deep learning"`) in **all three** databases, not just that one, so the search stays the same everywhere. Record the change in the search log.
   - **Exception (10 Oct 2026):** Scopus returned 1,017. Narrowing was tested (766 and 855 results, still over the limit), so the team kept the full 1,017 and did not narrow any database. See the change log.

## Search check (Scopus, before the logged run – Khalid, confirmed by Abdullah)

Check that Scopus finds these known on-topic papers. If any is missing, find out which concept failed to match its title, abstract, or keywords, fix the string, and note the change.

1. Kim, M., Song, Y., Wang, S., Xia, Y., and Jiang, X. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. *JMIR Medical Informatics, 6*(2), e19.
2. Kim, A., Song, Y., Kim, M., Lee, K., and Cheon, J. H. (2018). Logistic regression model training based on the approximate homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 83.
3. Chen, H., Gilad-Bachrach, R., Han, K., Huang, Z., Jalali, A., Laine, K., and Lauter, K. (2018). Logistic regression over encrypted data from fully homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 81.
