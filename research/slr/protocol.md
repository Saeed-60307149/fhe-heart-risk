# SLR Protocol

Privacy-Preserving Heart Disease Risk Prediction Using FHE · COMP4101 Practicum · UDST
Oct 9, 2026 · v2 · Abdullah Dar

> Markdown copy of [SLR_Protocol_v2.docx](SLR_Protocol_v2.docx). Keep the two in sync – if you change one, change the other and bump the version.

## Review questions

This review asks how fully homomorphic encryption (FHE) has been used to run machine learning inference on health data, and at what cost. Each question maps to a project objective.

| RQ | Question | Project objective |
|---|---|---|
| RQ1 | Which FHE schemes and libraries have been used for ML inference on healthcare data, and why were they chosen? | Encrypted computation |
| RQ2 | Which ML models and approximations of non-linear functions (such as sigmoid) are used, and how does encrypted accuracy compare with plaintext? | Encrypted computation |
| RQ3 | What computational costs are reported, such as latency, ciphertext size, and memory? | Evaluate trade-offs |
| RQ4 | How do studies handle key management, client-side encryption, and fit with clinical workflows? | Key management; practical feasibility |

## PICOC

The search combines three concepts: encryption, machine learning, and health data. Comparison and outcome terms are used for screening, not in the search string, so that relevant papers are not missed.

| Element | Definition for this review | Used in search string? |
|---|---|---|
| Population | Healthcare, medical, biomedical, or patient data, such as clinical records, genomic data, or disease prediction datasets | Yes |
| Intervention | Homomorphic encryption (FHE, CKKS, BFV, BGV) applied to ML inference or training | Yes |
| Comparison | Plaintext ML, or other privacy techniques such as federated learning or secure multi-party computation | No, used in screening |
| Outcome | Accuracy, latency, ciphertext size, memory, security guarantees | No, used in extraction |
| Context | ML-as-a-service, cloud or client-server inference | No, used in screening |

## Search strategy

Three databases are searched: IEEE Xplore (Saif), ACM Digital Library (Sarim), and Scopus (Khalid). Each search covers papers published 2016 to 2026, in the fields noted under each database below.

| Concept | Synonyms (joined with OR) |
|---|---|
| A. Encryption | "homomorphic encryption", "fully homomorphic", FHE, CKKS, BFV, BGV, TenSEAL, "Microsoft SEAL" |
| B. Machine learning | "machine learning", "logistic regression", "neural network", "deep learning", classif\*, predict\*, inference |
| C. Health | health\*, medical, biomedical, clinical, patient\*, disease\*, diagnos\*, genom\*, cancer, diabet\*, "heart disease", cardiovascular |

Master string: A AND B AND C. Concept C names common diseases (cancer, diabetes) and genomic data because many encrypted-ML papers describe their dataset that way rather than as "health" data, and "biomedical" is not matched by "medical".

### IEEE Xplore (Command Search, Abstract field)

```
("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE OR "Abstract":CKKS OR "Abstract":BFV OR "Abstract":BGV OR "Abstract":TenSEAL OR "Abstract":"Microsoft SEAL") AND ("Abstract":"machine learning" OR "Abstract":"logistic regression" OR "Abstract":"neural network" OR "Abstract":"deep learning" OR "Abstract":classif* OR "Abstract":predict* OR "Abstract":inference) AND ("Abstract":health* OR "Abstract":medical OR "Abstract":clinical OR "Abstract":patient* OR "Abstract":disease* OR "Abstract":biomedical OR "Abstract":diagnos* OR "Abstract":genom* OR "Abstract":cancer OR "Abstract":diabet* OR "Abstract":"heart disease" OR "Abstract":cardiovascular)
```

Filter: Publication Year 2016 to 2026; Conferences and Journals. This string uses 8 wildcards; IEEE Xplore allows at most 10 per search, so do not add more.

### ACM Digital Library (Advanced Search, Edit Query)

```
Abstract:("homomorphic encryption" OR "fully homomorphic" OR FHE OR CKKS OR BFV OR BGV OR TenSEAL OR "Microsoft SEAL") AND Abstract:("machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference) AND Abstract:(health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular)
```

Filter: Publication date 2016 to 2026; content type Research Article.

### Scopus (Advanced document search)

```
TITLE-ABS-KEY ( "homomorphic encryption" OR "fully homomorphic" OR fhe OR ckks OR bfv OR bgv OR tenseal OR "Microsoft SEAL" ) AND TITLE-ABS-KEY ( "machine learning" OR "logistic regression" OR "neural network" OR "deep learning" OR classif* OR predict* OR inference ) AND TITLE-ABS-KEY ( health* OR medical OR biomedical OR clinical OR patient* OR disease* OR diagnos* OR genom* OR cancer OR diabet* OR "heart disease" OR cardiovascular ) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```

IEEE Xplore and ACM search the abstract only, while Scopus searches title, abstract, and keywords. Abstracts almost always repeat the title's key terms, so this difference is small, but it is reported as a limitation.

Test each string before the logged run, and record the exact string actually used, the date, and the result count.

If any database returns more than about 400 results, narrow concept B to its first four terms ("machine learning", "logistic regression", "neural network", "deep learning") in all three databases, not just that one, so the search stays the same everywhere. Record the change in the search log.

### Search check

Before the logged run, check that Scopus finds these known on-topic papers. If any is missing, find out which concept failed to match its title, abstract, or keywords, fix the string, and note the change.

- Kim, M., Song, Y., Wang, S., Xia, Y., and Jiang, X. (2018). Secure logistic regression based on homomorphic encryption: design and evaluation. JMIR Medical Informatics, 6(2), e19.
- Kim, A., Song, Y., Kim, M., Lee, K., and Cheon, J. H. (2018). Logistic regression model training based on the approximate homomorphic encryption. BMC Medical Genomics, 11(Suppl 4), 83.
- Chen, H., Gilad-Bachrach, R., Han, K., Huang, Z., Jalali, A., Laine, K., and Lauter, K. (2018). Logistic regression over encrypted data from fully homomorphic encryption. BMC Medical Genomics, 11(Suppl 4), 81.

## Inclusion and exclusion criteria

A paper is included only if it meets every inclusion criterion and no exclusion criterion. Each exclusion is recorded with its code, which feeds the PRISMA diagram.

| Code | Inclusion criteria |
|---|---|
| I1 | Applies homomorphic encryption to ML training or inference |
| I2 | Uses healthcare, medical, or patient data, or a health dataset |
| I3 | Reports experimental results, such as accuracy or runtime |
| I4 | Peer-reviewed journal article or conference paper |
| I5 | Published 2016 to 2026, in English |

| Code | Exclusion criteria |
|---|---|
| E1 | Uses another privacy technique only (federated learning, differential privacy, MPC) without homomorphic encryption. Hybrid papers that combine homomorphic encryption with another technique are kept. |
| E2 | Not applied to health data |
| E3 | Purely theoretical, with no implementation or results |
| E4 | Survey, review, editorial, poster abstract, or thesis (reviews are kept separately as background reading) |
| E5 | Full text not available through UDST library access |
| E6 | Duplicate or earlier version of an included study (keep the most complete version) |

## Screening and selection process

Screening runs in two stages, with a second screener checking a sample at each stage to reduce bias.

1. Export all records from each database into RefWorks (or Rayyan) and remove duplicates. Hassan logs the count.
2. Title and abstract screening: split records into Set A (Saif) and Set B (Sarim). Mark each as include, exclude, or maybe; keep it when unsure.
3. Second screener: Khalid independently re-screens a random 20% of Set A. Record how many decisions differ, and resolve differences by discussion, with Naif deciding if needed.
4. Full-text screening: read the remaining papers in full and apply criteria I1 to I5 and E1 to E6, recording an exclusion code for each paper removed.
5. Backward snowballing: check the reference lists of included papers for relevant studies the search missed, and log these separately.
6. Hassan updates the PRISMA tracking sheet after each stage.

## Quality assessment checklist

Each included paper is scored on five questions: Yes = 1, Partly = 0.5, No = 0. Papers scoring below 2.5 out of 5 are kept but flagged as low quality in the synthesis.

| # | Question |
|---|---|
| Q1 | Are the aims and research question clearly stated? |
| Q2 | Are the FHE scheme, library, and encryption parameters reported? |
| Q3 | Is the dataset described and publicly available or clearly sourced? |
| Q4 | Are both accuracy and performance (time or size) measured? |
| Q5 | Is the encrypted result compared against a plaintext baseline? |

## Data extraction form

For every included paper, record one row in the shared synthesis sheet with these fields. Each field answers one of the review questions.

| Field | What to record | Answers |
|---|---|---|
| Reference | Authors, year, title, venue, DOI | — |
| Scheme | CKKS, BFV, BGV, TFHE, or other | RQ1 |
| Library | TenSEAL, SEAL, OpenFHE, HElib, Concrete, or other | RQ1 |
| Parameters | Polynomial modulus degree, scale, security level | RQ1 |
| Model | Logistic regression, neural network, or other | RQ2 |
| Activation approximation | Polynomial degree and input range used for sigmoid or ReLU | RQ2 |
| Dataset | Name and size | RQ2 |
| Accuracy | Encrypted vs plaintext accuracy, F1, or AUC | RQ2 |
| Performance | Encryption, inference, and decryption time; ciphertext size; hardware used | RQ3 |
| Key management | Where keys are generated and stored; client-side encryption | RQ4 |
| Deployment and workflow | Architecture, clinical setting, stated barriers | RQ4 |
| Limitations | As stated by the authors | All |
| Quality score | From the checklist above, out of 5 | — |

## Search log

Fill one row per search as it is run. These numbers become the Identification stage of the PRISMA diagram, so record them exactly and never estimate. *(The working copy is [search-log.csv](search-log.csv).)*

| Database | Run by | Date run | Exact string used | Filters applied | Results |
|---|---|---|---|---|---|
| IEEE Xplore | Saif | | | | |
| ACM Digital Library | Sarim | | | | |
| Scopus | Khalid | | | | |
| Total before de-duplication | | | | | |
| Duplicates removed | Hassan | | | | |
| Records to screen | | | | | |

## To do before Progress Report 1 (Sun 11 Oct)

This draft still needs the team's review and the real database searches before it goes into Progress Report 1.

- [ ] Naif and Saif: review the review questions, PICOC, and criteria; change anything the team disagrees with
- [ ] Saif: run the IEEE Xplore string and fill the search log
- [ ] Sarim: run the ACM string and fill the search log
- [ ] Khalid: run the Scopus string and fill the search log
- [ ] Hassan: export all records to RefWorks, remove duplicates, and start the PRISMA tracking sheet
- [ ] Naif: add the protocol and search counts to Progress Report 1
