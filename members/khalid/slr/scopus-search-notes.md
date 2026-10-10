# Scopus search notes – Khalid

Where: Scopus → **Advanced document search**. Copy the string exactly from [search-strings.md](../../../research/slr/search-strings.md).

## Step 1: Search check (before the logged run)

Run the string below and confirm each paper is in the results.

- [ ] Kim, M., Song, Y., Wang, S., Xia, Y., & Jiang, X. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. *JMIR Medical Informatics, 6*(2), e19. – **Not found** by any database
- [x] Kim, A., Song, Y., Kim, M., Lee, K., & Cheon, J. H. (2018). Logistic regression model training based on the approximate homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 83.
- [x] Chen, H., Gilad-Bachrach, R., Han, K., Huang, Z., Jalali, A., Laine, K., & Lauter, K. (2018). Logistic regression over encrypted data from fully homomorphic encryption. *BMC Medical Genomics, 11*(Suppl 4), 81.

If one is missing: which concept failed (A encryption / B ML / C health)? → **C health** (the Kim JMIR record has no health terms) · Fix applied: added to PRISMA as 1 record from other sources, reported as a limitation – approved by Abdullah, 10 Oct 2026 ([v4 change 4](../../../research/slr/SLR_Protocol_v4_changes.md#4-search-check-kim-jmir-2018-not-found-by-any-database))

## Exact string used

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```

## Run record

| Item | Value |
|---|---|
| Date of search check | 10 Oct 2026 |
| Search check result (3/3 found?) | No – 2/3 (Kim JMIR not found; fix approved) |
| Date run (logged) | 10 Oct 2026 |
| Filters applied | In the string: PUBYEAR 2016–2026, English, DOCTYPE ar + cp |
| Result count (logged) | 1,017 |
| Confirmed by partner (same-day re-run) + their count | Abdullah (1,017) |
| Export file / format | [`Scopus_2026-10-10.ris`](../../../research/slr/exports/Scopus_2026-10-10.ris) (RIS, 1,017 records) |

## Changes made (with reason)

| Date | Change | Reason | Agreed with |
|---|---|---|---|
| 10 Oct 2026 | Kept the full 1,017 results (over the 400 limit); string unchanged | Narrowing concept B was tested: 766 and 855, still over | Team |

If the string changes, paste the new exact string in the Search Log tab of the PRISMA sheet in research/slr/ too.
