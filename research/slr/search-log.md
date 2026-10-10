# Search log

Database searches for the SLR, run on **10 Oct 2026**. These numbers are the Identification stage of the PRISMA diagram: record them exactly and never estimate.

> **Update the live PRISMA sheet by hand.** The live sheet in OneDrive is not updated from the repo. Type the same numbers into its **Search Log** tab: IEEE Xplore **337**, PubMed **172**, Scopus **1,017**.

| Database | Pair | Run by | Confirmed by | Date run | Exact string used | Filters applied | Results | Notes / changes |
|---|---|---|---|---|---|---|---|---|
| IEEE Xplore | Pair 1 | Saif | Naif | 10 Oct 2026 | [IEEE Xplore string](#ieee-xplore) (unchanged from v3) | Publication Year 2016–2026; Conferences and Journals | **337** | Exported in 4 RIS files (100 + 100 + 100 + 37) |
| PubMed | Pair 2 | Sarim | Hassan | 10 Oct 2026 | [PubMed string](#pubmed) (new; replaces ACM) | In the string: 2016:2026[dp], english[la] | **172** | Replaces ACM Digital Library (no UDST subscription; filters and export locked). A [tw] variant (176 results) was tested and not used. |
| Scopus | Pair 3 | Khalid | Abdullah | 10 Oct 2026 | [Scopus string](#scopus) (unchanged from v3) | In the string: PUBYEAR 2016–2026, English, DOCTYPE ar + cp | **1,017** | Over the 400 limit. Narrowing was tested (766 and 855 results, still over), so the full 1,017 was kept by team decision. |
| **Total before de-duplication** | | | | | | | **1,526** | 337 + 172 + 1,017 |
| Duplicates removed | | Hassan | | | | | | *Hassan fills this in after RefWorks de-duplication* |
| Records to screen | | Hassan | | | | | | *Total minus duplicates* |

Export files: [exports/](exports/) · Change details: [SLR_Protocol_v4_changes.md](SLR_Protocol_v4_changes.md)

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
