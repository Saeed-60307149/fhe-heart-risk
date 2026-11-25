# SLR synthesis: answers to RQ1–RQ4 (draft, 25 Nov 2026)

Built from [`data-extraction.csv`](data-extraction.csv) (14 included records: 12 FHE/hybrid-HE and 2 partial-HE).
**Read this first – how solid each statement is.** Publisher sites blocked automated access on 25 Nov, so
only part of the evidence was read:

| Level | Meaning | Records |
|---|---|---|
| **V** | Open text read (some tables came through a summary and need a hand check) | P024 AutoPro-RHC, P034 GuardML, P005 Nguyen |
| **A** | Abstract only | P026 Cenitta, P013 Amer, P035 Kim, P008 Harb |
| **S** | Seeded from the reviewers' own notes, not re-checked | P006, P028, P001, P014, P019, P009, P018 |

Every figure below carries its level. **Nothing here has been verified by a second team member**, and the
quality scores (Q1–Q5) are left blank on purpose: scoring needs the full text and the team has not yet
agreed the checklist (the protocol and the extraction form use different Q lists – decide which one first).
A person with UDST access should upgrade the A and S rows; the CSV column `evidence_note` says what to check.

## What the review covers

34 records from IEEE Xplore and Scopus (2016–2026) after de-duplication, plus Kim 2018 by hand. 14 included.
4 records were never screened (Dziri, Janagama, ICIC 2019, Dakhare) and 6 await full text (see
[`refined-2026-10-29/prisma-flow.md`](refined-2026-10-29/prisma-flow.md)); the review is therefore **incomplete by
those 10 records**. The search also missed our baseline paper (Haq et al. 2025), whose abstract says
"medical tabular data", not "heart disease" – a search-strategy limitation.

## RQ1 – Which FHE schemes and libraries?

| Scheme | Records | Level |
|---|---|---|
| CKKS | Kim 2018 (HEAAN library), Naresh & Reddi (TenSEAL), Cenitta (scheme not named in the abstract), Harb (not verified) | A / S |
| TFHE | AutoPro-RHC (Concrete-ML), Gaddam (Concrete ML) | V / S |
| BFV (hybrid HE with the PASTA cipher) | GuardML, Nguyen (SEAL + IAIK PASTA library) | V |
| Partial HE (Paillier, additive only) | MediVault, Akter | S |

**Finding:** CKKS is the common choice for real-valued clinical features and is the scheme used by the two
logistic-regression studies closest to ours. BFV/TFHE papers need integer quantisation (GuardML uses 4-bit
inputs). No included record reports TenSEAL with node-seal.

## RQ2 – Models, sigmoid approximation, encrypted vs plain accuracy

| Record | Model | Non-linearity | Plain vs encrypted | Level |
|---|---|---|---|---|
| AutoPro-RHC | SVC, LR, XGBoost, tree | none stated | Tables report identical metrics; abstract: SVC 88%, LR 86% | V-partial |
| GuardML | one linear layer + sigmoid | training only; inference handling not reported | 88.2% float, 87.4% integer, 87.55% encrypted (2,000 inputs) | V-partial |
| Naresh & Reddi | logistic regression | not read | 85% vs 84% (seeded) | S |
| Cenitta | CNN | not read | abstract gives 94.2% only; **the 93.4% encrypted figure is not in the abstract** | A |
| Harb | NN with learned activation estimator | learned estimator vs polynomial | claims +2% (sigmoid), up to +73% (tanh) vs conventional | A |
| Kim 2018 | LR training | least-squares polynomial (team note) | not read | A |

**Finding:** where numbers were read, encrypted accuracy is equal to or within about 1 point of plaintext.
Few records say how the sigmoid is handled; two avoid it under encryption. This supports our design
(least-squares cubic, plus logit-only as the comparison). The "no loss" claim rests on **small test sets**
and, for Cenitta, on a number we could not confirm.

## RQ3 – Reported computing costs

| Record | Reported cost | Level |
|---|---|---|
| AutoPro-RHC (TFHE) | FHE inference 61–521 s depending on model and server (unit unclear); enc/dec milliseconds; ciphertext and key sizes **not reported** | V-partial |
| GuardML / Nguyen (BFV hybrid) | about 12 s per sample on the server; HE ciphertext about 1.8 MB, public key 2.06 MB; up to 5.5 GB analyst–server traffic at 2,000 inputs | V-partial |
| Cenitta (CKKS CNN) | 420 ms average encrypted inference | A |
| Wang (trees) | about 84 ms user, 66 ms cloud | S |
| Kim 2018 (training) | 3.6 min and 0.02 GB vs 114 min and 0.69 GB for the prior method on 1,253 × 9 data | A |

**Finding:** costs are reported inconsistently: parameters (polynomial degree, scale) are often missing
(AutoPro none; GuardML none; Nguyen only N), ciphertext and key sizes are rare, and hardware differs. TFHE and
hybrid-BFV approaches take seconds per sample; CKKS logistic regression is in the millisecond range. This is
the gap RQ-B fills: one dataset pair, all costs, reported side by side.

## RQ4 – Keys, client-side encryption, workflow

| Record | Who generates keys / where the secret key lives | Real client device? | Level |
|---|---|---|---|
| AutoPro-RHC | patient encrypts with PK1, decrypts with SK1; generation not stated | **No** – listed as future work; experiments on a workstation and AWS | V-partial |
| GuardML / Nguyen | analyst (or trusted hardware) generates keys and sends the evaluation key to the server; secret-key storage not reported | **No** – everything on one desktop | V-partial |
| Wang | trusted key centre (seeded) | not read | S |
| Others | not read | not read | A / S |

**Finding:** none of the records we could read runs encryption in a browser or on a real client device or
reports the size of the keys a client must upload. That is the clearest gap our project addresses (RQ-C).

## What this means for the project

1. **Gap confirmed (V-partial):** read papers omit parameters, key sizes and real-client evidence.
2. **Design supported:** CKKS for real-valued features; polynomial sigmoid or none under encryption; equal
   accuracy at the bottom of the reported range.
3. **Cost improvement is plausible but unproven:** the only parameter-sweep evidence is Haq et al. (not part of
   the SLR); see [`planning/project-direction.md`](../../planning/project-direction.md) §5.
4. **Weakest links:** Cenitta's encrypted accuracy; the Cloud-IoT paper's HE is generic; the Paillier papers
   cannot answer the sigmoid question.

## What the SLR gives the project (benefits, and what it does not give)

| Benefit | What it supports | Solidity |
|---|---|---|
| The gap exists | No record we could read reports key sizes or runs encryption on a real client or browser (AutoPro-RHC lists a real client as future work) | Partly verified (3 read, 4 abstracts) |
| Why CKKS | CKKS logistic regression is in the millisecond range; TFHE (AutoPro-RHC) takes 61-521 s and hybrid BFV (GuardML) about 12 s per sample; CKKS suits real-valued features | Partly verified |
| Sigmoid handling | Papers use a polynomial sigmoid or avoid it under encryption (Kim 2018, Haq, GuardML, Harb): backs the cubic plus logit-only choice | Mostly abstract level |
| Dataset choice | Kim 2018 uses the same Edinburgh MI data as our project | Abstract |
| Closest prior work | Naresh and Reddi (TenSEAL logistic regression on heart data; Haq cite it). Its seeded note says it compares polynomial degrees 4096 and 8192: **if verified, that is SLR evidence for the lower-N change. Read it next.** | Not read |
| A required deliverable | PRISMA diagram, study table, RQ1-RQ4 answers | In progress |

**What it does not give:** the cost evidence for Track 1 and the model evidence for Track 2 come from Haq et al.
2025, which the SLR search **missed** (their abstract says "medical tabular data", not "heart disease"). Naif
supplied it by hand. About half of the SLR rows are still unverified.

## Limitations (for the report)

- Two databases only (IEEE Xplore, Scopus); PubMed dropped (Scopus covers most MEDLINE titles).
- Search strings missed Haq et al. (abstract wording); added by hand.
- Single reviewer per record, no inter-rater agreement; a second reader for exclusions is still pending.
- 4 records unscreened, 6 awaiting full text, 7 included records not re-read.
- Quality assessment not done.
- Tables from AutoPro-RHC, GuardML and Nguyen were read through automated page summaries.

## To finish the SLR (needs a person with UDST access)

1. Screen the 4 unscreened records; get the 6 full texts (or exclude as E5 and say so).
2. Upgrade the A/S rows in `data-extraction.csv` by reading the full texts. Priority: Naresh & Reddi,
   Cenitta (plain vs encrypted accuracy), Kim 2018 (open on PMC), Harb.
3. Agree one quality checklist, score Q1–Q5, second reader checks.
4. Re-run `scripts/prisma_counts.py --write` and update the numbers here.
