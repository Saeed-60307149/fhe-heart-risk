# Search log

Database searches for the SLR, run on **10 Oct 2026**. These numbers are the Identification stage of the PRISMA diagram: record them exactly and never estimate.

> The same numbers are in the **Search Log** tab of `PRISMA_Tracking_Sheet_2026-10-11.xlsx`: IEEE Xplore **337**, PubMed **172**, Scopus **1,017**. Its **PRISMA Counts** tab adds them up (1,526).

| Database | Pair | Run by | Confirmed by | Date run | Exact string used | Filters applied | Results | Notes / changes |
|---|---|---|---|---|---|---|---|---|
| IEEE Xplore | Pair 1 | Saif | Naif | 10 Oct 2026 | [IEEE Xplore string](#ieee-xplore) (unchanged from v3) | Publication Year 2016–2026; Conferences and Journals | **337** | Exported in 4 RIS files (100 + 100 + 100 + 37) |
| PubMed | Pair 2 | Sarim | Hassan | 10 Oct 2026 | [PubMed string](#pubmed) (new; replaces ACM) | In the string: 2016:2026[dp], english[la] | **172** | Replaces ACM Digital Library (no UDST subscription; filters and export locked). A [tw] variant (176 results) was tested and not used. |
| Scopus | Pair 3 | Khalid | Abdullah | 10 Oct 2026 | [Scopus string](#scopus) (unchanged from v3) | In the string: PUBYEAR 2016–2026, English, DOCTYPE ar + cp | **1,017** | Over the 400 limit. Narrowing was tested (766 and 855 results, still over), so the full 1,017 was kept by team decision. |
| **Total before de-duplication** | | | | | | | **1,526** | 337 + 172 + 1,017 |
| Duplicates removed | | Hassan | | 10 Oct 2026 | | | **482** | Removed by script (see [De-duplication](#de-duplication-10-oct-2026)); every removed copy is listed in the *Duplicates Removed* tab of the [dedup workbook](dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx) |
| Records to screen | | Hassan | | 10 Oct 2026 | | | **1,044** | 1,526 − 482. Split at random into 3 sets of 348 (see below) |

Export files: [exports/](exports/) · De-duplication and screening sets: [SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx](dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx) · Change details: [SLR_Protocol_v4_changes.md](SLR_Protocol_v4_changes.md)

> **Done (11 Oct sheet):** the 1,044 records are in the Screening Log of [`PRISMA_Tracking_Sheet_2026-10-11.xlsx`](PRISMA_Tracking_Sheet_2026-10-11.xlsx), ready for screening from Mon 12 Oct. Mapping from the dedup workbook: Record ID → A, Title → B, Authors → C, Year → D, first database listed → E *Source* (IEEE → IEEE Xplore), Set 1/2/3 → F *Pair 1/2/3*, databases + DOI + PMID → P *Notes*, abstract → new column Q. The sheet now runs to row 1046; *Duplicate records removed* = 482. Kim JMIR is row R1045 with Source = *Other sources* (Pair 3) and goes straight to full text.

## De-duplication (10 Oct 2026)

Done by script instead of RefWorks (see [v4 change 3](SLR_Protocol_v4_changes.md#3-de-duplication-by-script-instead-of-refworks)). Full lists are in the [dedup workbook](dedup/SLR_Dedup_and_Screening_Sets_2026-10-10.xlsx).

| Step | Records |
|---|---|
| Total before de-duplication | 1,526 |
| Duplicates removed – same DOI (case-insensitive) | 474 |
| Duplicates removed – same title after removing case and punctuation | 6 |
| Duplicates removed – near-identical title (97%+ similar) with year within 1 | 2 |
| **Duplicates removed – total** | **482** |
| **Records to screen** | **1,044** |

- When copies matched, the one with an abstract was kept, in the order **Scopus > PubMed > IEEE**. The workbook's *Databases* column lists every database that returned each record.
- 4 pairs with 90–96% similar titles were checked by hand: they are different papers and were **not** merged.
- **Screening sets:** random shuffle with fixed seed **20261010** (so the split can be repeated), then dealt into sets in turn.

| Set | Pair | Screeners | Records |
|---|---|---|---|
| Set 1 | Pair 1 | Saif + Naif | 348 |
| Set 2 | Pair 2 | Sarim + Hassan | 348 |
| Set 3 | Pair 3 | Khalid + Abdullah | 348 |

## Search check (10 Oct 2026, all databases)

The protocol's three known on-topic papers, checked against every database's results:

| Known paper | IEEE Xplore | PubMed | Scopus | Result |
|---|---|---|---|---|
| Kim, A. et al. (2018). Logistic regression model training based on the approximate homomorphic encryption. *BMC Medical Genomics* | – | – | Found | Found in Scopus |
| Chen, H. et al. (2018). Logistic regression over encrypted data from fully homomorphic encryption. *BMC Medical Genomics* | – | Found | Found | Found in PubMed and Scopus |
| Kim, M. et al. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. *JMIR Medical Informatics* | – | – | – | **Not found by any database** |

- IEEE Xplore is not expected to hold these: all three were published in medical journals.
- **Kim JMIR:** indexed in PubMed (PMID 29666041), but its record has no health terms, so concept C (health) misses it. **Fix:** add it to PRISMA as 1 record *identified from other sources* and list it as a limitation. Approved by Abdullah (protocol owner), 10 Oct 2026. Details: [v4 change 4](SLR_Protocol_v4_changes.md#4-search-check-kim-jmir-2018-not-found-by-any-database).

## Exact strings used

### IEEE Xplore

```
("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE OR "Abstract":CKKS OR "Abstract":BFV OR "Abstract":BGV OR "Abstract":TenSEAL OR "Abstract":"Microsoft SEAL") AND ("Abstract":"machine learning" OR "Abstract":"logistic regression" OR "Abstract":"neural network" OR "Abstract":"deep learning" OR "Abstract":classif* OR "Abstract":predict* OR "Abstract":inference) AND ("Abstract":health* OR "Abstract":medical OR "Abstract":clinical OR "Abstract":patient* OR "Abstract":disease* OR "Abstract":biomedical OR "Abstract":diagnos* OR "Abstract":genom* OR "Abstract":cancer OR "Abstract":diabet* OR "Abstract":"heart disease" OR "Abstract":cardiovascular)
```

### PubMed

```
("homomorphic encryption"[tiab] OR "fully homomorphic"[tiab] OR FHE[tiab] OR CKKS[tiab] OR BFV[tiab] OR BGV[tiab] OR TenSEAL[tiab] OR "Microsoft SEAL"[tiab]) AND ("machine learning"[tiab] OR "logistic regression"[tiab] OR "neural network"[tiab] OR "deep learning"[tiab] OR classif*[tiab] OR predict*[tiab] OR inference[tiab]) AND (health*[tiab] OR medical[tiab] OR biomedical[tiab] OR clinical[tiab] OR patient*[tiab] OR disease*[tiab] OR diagnos*[tiab] OR genom*[tiab] OR cancer[tiab] OR diabet*[tiab] OR "heart disease"[tiab] OR cardiovascular[tiab]) AND 2016:2026[dp] AND english[la]
```

### Scopus

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```
