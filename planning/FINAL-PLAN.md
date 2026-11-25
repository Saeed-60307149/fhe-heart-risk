# FINAL PLAN – what we are doing (decided 25 Nov 2026; sigmoid decision flipped later the same day, #24)

This page is the single answer. If another document disagrees with it, this page wins.
Background and reasoning: [`project-direction.md`](project-direction.md). Nothing below is a result yet;
results come only from the Capstone 2 measurements.

## 1. The project in one paragraph

We build a heart-disease risk checker where the patient's browser encrypts the 13 health values, the server
computes the risk on the encrypted values, and only the patient can decrypt the answer. Others have shown
FHE machine learning works (our reference is Haq et al. 2025), but the papers we read use heavy fixed
settings, leave out key sizes, and never encrypt on a real client. **Our contribution is a lighter,
measured version of that system.** Cost = server time, upload size, key size, response size. Accuracy must
equal the plain model's.

## 2. Research questions (unchanged from PR2, plus one)

| | Question |
|---|---|
| RQ-A | Does the encrypted logistic regression give the same low/high-risk decision as the plain model for ≥ 90% of test patients? |
| RQ-B | What does privacy cost in accuracy, time, and ciphertext and key size, on both datasets? |
| RQ-C | Can the patient encrypt in the browser and keep the key, so the server only sees ciphertext, and which attacks remain? |
| RQ-D (new) | Does a stronger model raise accuracy enough to justify its extra encrypted cost? |

## 3. What is fixed (no more discussion)

- Scheme CKKS; node-seal 7.0.0 in the browser, TenSEAL 0.3.16 on the server; Node.js 22+ (#1, #13).
- One ciphertext per feature (#15).
- Reference model: logistic regression, 13 features (Cleveland) and 9 (Edinburgh).
- **Main method = BROWSER SIGMOID (#24).** The server returns the encrypted score (weighted sum + bias); the browser decrypts it and applies the sigmoid. No ciphertext-times-ciphertext multiplication, so no relinearisation keys and only 1 multiplication level. This is also how Haq et al. do it, so our gain over Haq comes from the layout, the smaller settings, the browser-side keys and the measured costs, not from where the sigmoid is.
- **Server sigmoid (encrypted cubic) is an add-on only**: still implemented (`output = "sigmoid"`) and measured once (row 7) to report its extra cost. It is not the reference and not part of the cost claims.
- Reference setting = row 0: pilot box N = 16384, chain 60/40/40/40/40/60, scale 2^40, with the browser sigmoid.
- Datasets reported separately: UCI Cleveland and Edinburgh MI.

## 4. Track 1 – make it cheaper (the main contribution)

One ablation table per dataset; each row changes one thing; every row reports upload MB, response bytes,
key MB, encrypt / infer / decrypt ms, decision match, accuracy. A row below 90% decision match is a fail and is
still reported.

| Row | Change | Owner |
|---|---|---|
All rows use the browser sigmoid unless stated.

| Row | Change | Owner |
|---|---|---|
| 0 | Reference: pilot box (N = 16384, 60/40/40/40/40/60, 2^40) | Hassan |
| 1 | Shortest chain and smallest scale that keep 100% match | Hassan, Khalid |
| 2 | N = 8192 | Hassan |
| 3 | Check whether compression is already on; report raw vs compressed size | Hassan |
| 4 | N = 4096 (one attempt; report either way) | Khalid |
| 5 | Seeded (symmetric-key) encryption in the browser + trimmed response ciphertext | Saif |
| 6 | Confirm no relinearisation or rotation keys are generated or uploaded; key reuse decision | Saif, Naif |
| 7 | **Add-on:** server sigmoid (encrypted cubic) at the reference box and at N = 8192: extra cost vs rows 0 and 2, and decision match of the polynomial | Khalid |
| H | Haq-style setting (N = 8192, chain 31/26×6/31, scale 2^26) on our data and machine | Hassan |

### Why we expect each row to help, and how solid that is

| Rows | Evidence | Status |
|---|---|---|
| 1 (chain, scale) | Haq et al. Table 9: 8 → 5 primes cut time 15.6 → 5.9 s and upload 477 → 276 KB with no accuracy change; Table 10: scale 2^24 and 2^22 collapse accuracy (`research/baseline-paper/README.md`) | **Read; the only solid evidence.** Their hardware and model |
| 2, 4 (lower N) | HomomorphicEncryption.org security standard (maximum modulus bits per N at 128-bit security) | **Not read yet**, named from memory. Haq never vary N |
| 3 (compression) | Microsoft SEAL documentation | **Not read yet.** May already be on, so it may give nothing |
| 0 (browser sigmoid is the main method) | Haq et al. and GuardML apply the sigmoid after decryption | They show it works; **none measures the benefit** |
| 5 (seeded encryption, trimmed response) | Microsoft SEAL documentation | **Not read yet**; not yet confirmed in node-seal 7.0.0 and TenSEAL 0.3.16 |
| 6, 7 (keys) | Our own pilot: relinearisation keys about 6.3 MB, needed only by the server sigmoid (`code/results/`) | Measured by us |

**Reading task before the measurements (Saif, Hassan):** read the SEAL documentation (serialisation, compression,
seeded encryption) and the security standard; add both to `research/reading-list.md` and update this table.
Only the Capstone 2 measurements prove any row; the sources only justify trying it.

Dropped for good: GPU (SEAL is CPU-only), packed layout as a delivered option (measured once as a
comparison, already in the PR2 pilot), packed layout with rotation keys.

## 5. Track 2 – better model, without undoing Track 1

Candidates, and only these:

| Model | Why |
|---|---|
| M1 tuned logistic regression | free under encryption |
| M2 linear SVM | free under encryption |
| M4 small MLP, square activation, browser sigmoid | the one test of whether a stronger model stays affordable. It needs about 3 multiplication levels against 1 for LR, so it will not fit LR's smallest box; we measure it in its own smallest box |

Dropped for good: extra interaction features (no source), the LR-MLP hybrid (weakest evidence), trees and
XGBoost (too costly under encryption).

### Why we expect each model to help, and how solid that is

| Model | Evidence | Status |
|---|---|---|
| M1 tuned LR | Standard practice; Haq tune training length by 10-fold CV | Background only; expect a small gain at most |
| M2 linear SVM | Haq: SVM beat LR on Wisconsin (0.9649 vs 0.9211) but not on Cleveland (0.7667 vs 0.7883); AutoPro-RHC abstract: SVC 88% vs LR 86% on UCI heart data | Read (Haq); mixed result |
| M4 small MLP | Haq: MLP beat LR on both datasets (0.9737 vs 0.9211; 0.8167 vs 0.7883) but ran about 18x (Wisconsin) and 14x (Cleveland) slower under encryption (`research/baseline-paper/README.md`) | Read; **one small split, inconsistent Cleveland table, so suggestive only** |

Not found: any source comparing LR and MLP on Cleveland-type data with cross-validation. That is why the rule above
uses cross-validation and a cost budget instead of trusting Haq's single split.

**Decision rule (final):** compare with 10-fold repeated stratified cross-validation. A model replaces
logistic regression only if (a) its accuracy gain is larger than the spread between folds, (b) its upload per
patient is at most 1.5× the LR's, and (c) its server time is at most 2× the LR's (each model in its own smallest
working box; M1 and M2 use the same box as LR, so they always pass b and c). Otherwise logistic
regression stays, and the result is reported as "simplest model is the best balance". Both outcomes are fine.

## 6. Claims we will make, and not make

| We say | Only if |
|---|---|
| Same decisions as plaintext | RQ-A measured ≥ 90% |
| Lighter than the fixed-setting approach | The ablation beats the Haq-style row H on our machine |
| A model is better than LR | It passes the Track 2 rule |

We do **not** say: more accurate because of encryption; faster than Haq in absolute terms (different hardware); a GPU helps.

## 7. Who does what

| Person | Capstone 2 job |
|---|---|
| Abdullah | Front end, API and plaintext baseline app; architecture and API contract kept in line |
| Saif | Real FHE pipeline; rows 5–6; security tests 1, 3, 4, 7 |
| Hassan | Benchmark harness; rows 0–3 and H; results table |
| Khalid | Sigmoid; rows 1, 4, 7; Track 2 modelling with Sarim |
| Sarim | Baselines, Edinburgh, cross-validation, Track 2 (M1, M2, M4) |
| Naif | Threat model and security assessment; SLR upkeep; reports |

## 8. Order of work in Capstone 2 (follows the PR2 Gantt)

1. Front end, API, plaintext baseline app.
2. Real FHE pipeline with the browser sigmoid, node-seal and TenSEAL; rows 0–3.
3. Security hardening and assessment against the threat model; rows 4–6 and H; then the server-sigmoid add-on (row 7).
4. Performance evaluation on both datasets (Track 1 table, then Track 2).
5. Polish, final report, demo that shows the server only handles ciphertext.

## 9. What is left in the practicum (before Capstone 2)

Finish the final report (Thu 26 Nov) and the defence. State this plan as the Capstone 2 plan with no result
claimed. The SLR is reported as in progress: 4 unscreened and 6 inaccessible records, quality scoring and a
full-text re-read of the abstract-only and seeded rows still open (`research/slr/synthesis.md`).

## 10. What the SLR gave us

The gap (no read paper reports key sizes or a real client), the reason for CKKS (milliseconds vs seconds for TFHE
and hybrid BFV), support for the sigmoid choice, the Edinburgh dataset (Kim 2018), and the required practicum
deliverable. It did **not** give the cost or model evidence: that is Haq et al., which the search missed.
Details and limits: `research/slr/synthesis.md`.

