# Search strings

Source: [protocol.md](protocol.md) (SLR Protocol v2, 9 Oct 2026). Copy these **exactly** – do not reformat. If you change a string, record the new string and the reason in [search-log.csv](search-log.csv) and in your own `members/<you>/slr/*-search-notes.md`.

Master string: **A (encryption) AND B (machine learning) AND C (health)**.

## IEEE Xplore (Command Search, Abstract field) – Saif

```
("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE OR "Abstract":CKKS OR "Abstract":BFV OR "Abstract":BGV OR "Abstract":TenSEAL OR "Abstract":"Microsoft SEAL") AND ("Abstract":"machine learning" OR "Abstract":"logistic regression" OR "Abstract":"neural network" OR "Abstract":"deep learning" OR "Abstract":classif* OR "Abstract":predict* OR "Abstract":inference) AND ("Abstract":health* OR "Abstract":medical OR "Abstract":clinical OR "Abstract":patient* OR "Abstract":disease* OR "Abstract":biomedical OR "Abstract":diagnos* OR "Abstract":genom* OR "Abstract":cancer OR "Abstract":diabet* OR "Abstract":"heart disease" OR "Abstract":cardiovascular)
```

- **Filters:** Publication Year 2016–2026; Conferences and Journals.
- Uses **8 wildcards**; IEEE Xplore allows at most 10 per search, so do not add more.

## ACM Digital Library (Advanced Search → Edit Query) – Sarim

```
Abstract:("homomorphic encryption" OR "fully homomorphic" OR FHE OR CKKS OR BFV OR BGV OR TenSEAL OR "Microsoft SEAL") AND Abstract:("machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference) AND Abstract:(health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular)
```

- **Filters:** Publication date 2016–2026; content type Research Article.

## Scopus (Advanced document search) – Khalid

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```

- **Filters:** built into the string (years 2016–2026, English, journal articles + conference papers).

## Rules

1. **Test each string before the logged run.** Record the exact string actually used, the date, and the result count.
2. **More than ~400 results in any database?** Narrow concept B to its first four terms – `"machine learning"`, `"logistic regression"`, `"neural network"`, `"deep learning"` – in **all three** databases (not just that one), so the search stays the same everywhere. Record the change in the search log.
3. IEEE Xplore and ACM search the abstract only; Scopus searches title, abstract, and keywords. The difference is small, but it is reported as a limitation.

## Scopus search check (Khalid – do this BEFORE the logged Scopus run)

Scopus must find all three of these known on-topic papers. If one is missing, find out which concept (A, B or C) failed to match its title, abstract or keywords, fix the string, and note the change.

1. Kim, M., Song, Y., Wang, S., Xia, Y., & Jiang, X. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. *JMIR Medical Informatics, 6*(2), e19.
2. Kim, A., Song, Y., Kim, M., Lee, K., & Cheon, J. H. (2018). Logistic regression model training based on the approximate homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 83.
3. Chen, H., Gilad-Bachrach, R., Han, K., Huang, Z., Jalali, A., Laine, K., & Lauter, K. (2018). Logistic regression over encrypted data from fully homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 81.
