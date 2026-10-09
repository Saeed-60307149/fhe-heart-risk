# Search strings

Source: SLR Protocol v3 ([protocol.md](protocol.md)), 9 Oct 2026. Copy these **exactly** – do not reformat. If a string changes, record the new string and the reason in the **Search Log** tab of the live PRISMA sheet (see [README.md](README.md)).

Master string: **A (encryption) AND B (machine learning) AND C (health)**.

The first person in each pair runs the logged search and fills the Search Log tab; the partner re-runs it the same day to confirm the count.

## IEEE Xplore (Command Search, Abstract field) – Pair 1: Saif runs, Naif confirms

```
("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE OR "Abstract":CKKS OR "Abstract":BFV OR "Abstract":BGV OR "Abstract":TenSEAL OR "Abstract":"Microsoft SEAL") AND ("Abstract":"machine learning" OR "Abstract":"logistic regression" OR "Abstract":"neural network" OR "Abstract":"deep learning" OR "Abstract":classif* OR "Abstract":predict* OR "Abstract":inference) AND ("Abstract":health* OR "Abstract":medical OR "Abstract":clinical OR "Abstract":patient* OR "Abstract":disease* OR "Abstract":biomedical OR "Abstract":diagnos* OR "Abstract":genom* OR "Abstract":cancer OR "Abstract":diabet* OR "Abstract":"heart disease" OR "Abstract":cardiovascular)
```

- **Filters:** Publication Year 2016 to 2026; Conferences and Journals.
- This string uses **8 wildcards**; IEEE Xplore allows at most 10 per search, so do not add more.

## ACM Digital Library (Advanced Search, Edit Query) – Pair 2: Sarim runs, Hassan confirms

```
Abstract:("homomorphic encryption" OR "fully homomorphic" OR FHE OR CKKS OR BFV OR BGV OR TenSEAL OR "Microsoft SEAL") AND Abstract:("machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference) AND Abstract:(health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular)
```

- **Filters:** Publication date 2016 to 2026; content type Research Article.

## Scopus (Advanced document search) – Pair 3: Khalid runs, Abdullah confirms

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```

- **Filters:** in the string (PUBYEAR 2016–2026, English, DOCTYPE article + conference paper).
- Run the **search check** below first.

## Rules

1. IEEE Xplore and ACM search the abstract only, while Scopus searches title, abstract, and keywords. Abstracts almost always repeat the title's key terms, so this difference is small, but it is reported as a limitation.
2. Test each string before the logged run, and record the exact string actually used, the date, and the result count.
3. If any database returns more than about 400 results, narrow concept B to its first four terms (`"machine learning"`, `"logistic regression"`, `"neural network"`, `"deep learning"`) in **all three** databases, not just that one, so the search stays the same everywhere. Record the change in the search log.

## Search check (Scopus, before the logged run – Khalid, confirmed by Abdullah)

Check that Scopus finds these known on-topic papers. If any is missing, find out which concept failed to match its title, abstract, or keywords, fix the string, and note the change.

1. Kim, M., Song, Y., Wang, S., Xia, Y., and Jiang, X. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. *JMIR Medical Informatics, 6*(2), e19.
2. Kim, A., Song, Y., Kim, M., Lee, K., and Cheon, J. H. (2018). Logistic regression model training based on the approximate homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 83.
3. Chen, H., Gilad-Bachrach, R., Han, K., Huang, Z., Jalali, A., Laine, K., and Lauter, K. (2018). Logistic regression over encrypted data from fully homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 81.
