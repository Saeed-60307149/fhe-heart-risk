# FINAL PLAN – what we are doing (decided 25 Nov 2026)

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
- Reference setting = row 0: N = 16384, chain 60/40/40/40/40/60, scale 2^40, encrypted least-squares cubic.
- Delivered system supports both outputs: encrypted cubic sigmoid (main) and logit-only (sigmoid in the browser).
- Datasets reported separately: UCI Cleveland and Edinburgh MI.

## 4. Track 1 – make it cheaper (the main contribution)

One ablation table per dataset; each row changes one thing; every row reports upload MB, response bytes,
key MB, encrypt / infer / decrypt ms, decision match, accuracy. A row below 90% decision match is a fail and is
still reported.

| Row | Change | Owner |
|---|---|---|
| 0 | Reference setting | Hassan |
| 1 | Shortest chain and smallest scale that keep 100% match | Hassan, Khalid |
| 2 | N = 8192, encrypted cubic | Hassan |
| 3 | Check whether compression is already on; report raw vs compressed size | Hassan |
| 4 | N = 8192, logit-only | Khalid |
| 5 | N = 4096, logit-only (one attempt; report either way) | Khalid |
| 6 | Seeded (symmetric-key) encryption in the browser + trimmed response ciphertext | Saif |
| 7 | Relinearisation keys only; key reuse decision | Saif, Naif |
| H | Haq-style setting (N = 8192, chain 31/26×6/31, scale 2^26) on our data and machine | Hassan |

Dropped for good: GPU (SEAL is CPU-only), packed layout as a delivered option (measured once as a
comparison, already in the PR2 pilot), packed layout with rotation keys.

## 5. Track 2 – better model, without undoing Track 1

Candidates, and only these:

| Model | Why |
|---|---|
| M1 tuned logistic regression | free under encryption |
| M2 linear SVM | free under encryption |
| M4 small MLP, square activation, logit-only output | the one test of whether a stronger model fits the same box |

Dropped for good: extra interaction features (no source), the LR-MLP hybrid (weakest evidence), trees and
XGBoost (too costly under encryption).

**Decision rule (final):** compare with 10-fold repeated stratified cross-validation. A model replaces
logistic regression only if (a) its accuracy gain is larger than the spread between folds, (b) it fits the
optimised LR's box (same N and chain), and (c) its server time is at most 2× the LR's. Otherwise logistic
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
| Saif | Real FHE pipeline; rows 6–7; security tests 1, 3, 4, 7 |
| Hassan | Benchmark harness; rows 0–3 and H; results table |
| Khalid | Sigmoid and rows 1, 4, 5; Track 2 modelling with Sarim |
| Sarim | Baselines, Edinburgh, cross-validation, Track 2 (M1, M2, M4) |
| Naif | Threat model and security assessment; SLR upkeep; reports |

## 8. Order of work in Capstone 2 (follows the PR2 Gantt)

1. Front end, API, plaintext baseline app.
2. Real FHE pipeline with node-seal and TenSEAL; rows 0–3.
3. Security hardening and assessment against the threat model; rows 4–7 and H.
4. Performance evaluation on both datasets (Track 1 table, then Track 2).
5. Polish, final report, demo that shows the server only handles ciphertext.

## 9. What is left in the practicum (before Capstone 2)

Finish the final report (Thu 26 Nov) and the defence. State this plan as the Capstone 2 plan with no result
claimed. The SLR is reported as in progress: 4 unscreened and 6 inaccessible records, quality scoring and a
full-text re-read of the abstract-only and seeded rows still open (`research/slr/synthesis.md`).
