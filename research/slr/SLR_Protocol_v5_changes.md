# SLR Protocol v5 – changes from v4 (refined search)

29 Oct – 11 Nov 2026 · Protocol owner: Abdullah Dar · decided with the supervisor (Dr. Abdullatif
Shikfa) at the meeting of Thu 29 Oct 2026 · reported in Progress Report 2 (section A.3).

**Unchanged:** review questions RQ1–RQ4, PICOC, Kitchenham and Charters method, PRISMA 2020
reporting, 2016–2026, English, journal and conference papers.

## 1. Search strings replaced (29 Oct 2026)

**Why:** the v3/v4 strings (A AND B AND C with broad synonym lists) returned 1,526 records
(1,044 after de-duplication). Screening in Weeks 8–10 showed most were irrelevant: the strings did
not require all three concepts *encryption*, *machine learning* and *heart disease* to appear
together. Screening 1,044 mostly irrelevant records would have used the rest of the term for little
gain. After the supervisor meeting the team adopted exact strings that require all three.

| Database | v5 string (exact) | Field |
|---|---|---|
| IEEE Xplore | `("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE) AND "Abstract":"machine learning" AND "Abstract":"heart disease"` | Abstract; filters 2016–2026, Conferences and Journals |
| Scopus | `TITLE-ABS-KEY(("homomorphic encryption" OR "fully homomorphic" OR FHE) AND "machine learning" AND "heart disease")` | Title, abstract, keywords; 2016–2026, English |

## 2. PubMed dropped

PubMed replaced ACM in v4 only because UDST has no ACM subscription. With the refined strategy the
team searches the two databases that index the computing literature where FHE-based ML is
published. Scopus covers about 6,700 of the roughly 7,000 MEDLINE journal titles (Elsevier, Scopus
Content Coverage Guide), so the biomedical literature PubMed would return is largely inside the
Scopus search. **Reported as a limitation.**

## 3. Results and de-duplication (29 Oct – 6 Nov 2026)

| | Records | Run / confirmed by |
|---|---|---|
| IEEE Xplore | 8 | Naif; re-run and confirmed by Saif |
| Scopus | 35 rows (34 unique) | Naif; re-run and confirmed by Abdullah |
| Total identified | 43 | |
| Duplicates removed | 9 (8 same DOI across databases + 1 listed twice in Scopus: ICSCSP 2018) | Naif; checked by Saif |
| Records to screen | 34 | |

Export: [refined-2026-10-29/exports/Scopus_refined_2026-10-29.csv](refined-2026-10-29/exports/Scopus_refined_2026-10-29.csv).
The 8 IEEE records all appear in Scopus (same DOI); **the IEEE export file is not in the repo yet –
Naif to add it** (`refined-2026-10-29/exports/IEEE_refined_2026-10-29.csv`).

## 4. Screening procedure changed

| v3/v4 | v5 (1–5 Nov 2026) |
|---|---|
| Three fixed pairs; every record screened independently by both pair members; tie-breakers | Leader divides the records across all six members (5–6 each); **one reviewer per record**; the whole team discusses borderline records; a **second member re-checks every excluded record** (still to do) |
| Exclusion codes E1–E6 (Protocol v3) | Codes **E1–E5** from the refined PRISMA sheet's Criteria tab: E1 no FHE · E2 not health or no ML · E3 review only · E4 no full text · E5 too little to extract. Abdullah found the mismatch on 29 Oct (protocol E1–E5 vs sheet E1–E6); v5 adopts E1–E5. |
| – | **Retracted** papers: excluded with reason "retracted" (no E-code fits). |
| – | Conference-proceedings entries ("Conference review" in Scopus) are excluded as **E3** (not a study). |
| – | Review papers are excluded (E3) but kept for **snowballing** their reference lists. |
| – | Records whose full text cannot be obtained stay undecided until access is arranged, then E4. |

Why single screening: with 34 records and the PR2 deadline (Sun 8 Nov), one reviewer per record plus
a second check of every exclusion was judged enough. **Limitation:** inter-rater agreement cannot
be reported for the refined set.

## 5. Outcome so far (PR2 Table 2, reconciled 11 Nov)

See [refined-2026-10-29/prisma-flow.md](refined-2026-10-29/prisma-flow.md) (generated from
[screening-decisions.csv](refined-2026-10-29/screening-decisions.csv)).

- 31 records screened: 11 excluded, 12 included, 2 borderline (Paillier only: MediVault, Akter),
  6 awaiting full text (as reported in PR2). On 11 Nov the 2 borderline records were included as a
  partial-HE subgroup (decision #17) → 14 included.
- **Correction found on 11 Nov:** 4 records of the 34 were never assigned (P002 Dziri 2025,
  P011 Janagama 2026, P023 ICIC 2019 proceedings, P029 Dakhare 2024). PR2 explained the 34 → 31
  gap by the 3 records read twice; that was not the reason. These 4 must be screened (Week 12).
- **Kim A. et al. 2018** (BMC Med Genomics, included by Saif) is not in the refined results – it is
  one of the protocol's search-check papers. It is now counted as **1 record from other sources**
  (sheet ID P035).

## 6. Decisions (closed 11 Nov 2026)

1. **Partial HE (Paillier, additive only) is included** as a separate *partial HE* subgroup
   (decision #17): criterion 1 accepts "homomorphic encryption", and both papers compute on
   encrypted health data. This is the same rule that included TrustFedHealth (HE-protected federated
   updates). They are synthesised apart from the FHE papers. Gogoi & Valan stays excluded for E5.
2. **Search check for v5:** Kim A. 2018 is not found by the refined strings (its record has no
   "heart disease"), so it is counted as 1 record from other sources (decision #14) and the miss is a
   limitation: papers on heart data that do not say "heart disease" in title/abstract/keywords can be missed.
3. **The 4 unassigned records** are screened in Week 12: P002 → Naif, P011 → Saif, P023 → Abdullah,
   P029 → Hassan (decision #14).
4. **Backward snowballing** of the 3 excluded reviews (P015, P016, P003) – Week 12.
