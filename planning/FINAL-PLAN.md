# FINAL PLAN – what we are doing (decided 25 Nov 2026; sigmoid decision flipped later the same day, #24)

> **Aligned with the corrected Defense Report (reference, decision #26).** Users are hospitals. RQ-A passes at **90% or more**. The delivered layout is **one ciphertext per feature**; packed is measured for comparison only.

This page is the single answer. If another document disagrees with it, this page wins.
Background and reasoning: [`project-direction.md`](project-direction.md). **The experiments in this plan were run on 27 Nov 2026: results are in section 11.** Sections 1–10 are the plan as decided before the results;
results come only from the Capstone 2 measurements.

## 1. The project in one paragraph

We build a heart-disease risk checker where a hospital's browser encrypts the 13 health values, the server
computes the risk on the encrypted values, and only the hospital can decrypt the answer. Others have shown
FHE machine learning works (our reference is Haq et al. 2025), but the papers we read use heavy fixed
settings, rarely report key sizes, and, among those we could read, do not encrypt on a real client. **Our contribution is a lighter,
measured version of that system.** Cost = server time, upload size, key size, response size. Accuracy must
equal the plain model's.

## 2. Research questions (unchanged from PR2, plus one)

| | Question |
|---|---|
| RQ-A | Does the encrypted logistic regression give the same low/high-risk decision as the plain model for at least 90% of test patients? |
| RQ-B | What does privacy cost in accuracy, time, and ciphertext and key size, on both datasets? |
| RQ-C | Can the hospital encrypt in the browser and keep the key, so the server only sees ciphertext, and which attacks remain? |
| RQ-D (new) | Does a stronger model raise accuracy enough to justify its extra encrypted cost? |

## 3. What is fixed (no more discussion)

- Scheme CKKS; node-seal 7.0.0 in the browser, TenSEAL 0.3.16 on the server; Node.js 22+ (#1, #13).
- One ciphertext per feature (#15, #26). A packed layout is measured for comparison only; it is not the delivered layout.
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

**Reading task, still open (Saif, Hassan):** read the SEAL documentation (serialisation, compression,
seeded encryption) and the security standard; add both to `research/reading-list.md` and update this table.
The measurements (section 11) are the proof; the sources only justified trying each row.

Dropped for good: GPU (our libraries compute on the CPU) and a packed layout as a delivered option (measured for comparison only).

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

The gap (among the studies whose text we obtained, none encrypts on a real client or in a browser, and key sizes are
rarely reported; GuardML gives a public-key size), support for CKKS and the sigmoid choice, the Edinburgh dataset
(Kim 2018), and the required practicum deliverable. It did **not** give the cost or model evidence: that is Haq et al.,
which the refined search missed. Details and limits: `research/slr/synthesis.md`.

## 11. Results (27 Nov 2026) – the experiments in this plan have been run

Full tables and how each test runs: [`code/results/benchmarks/README.md`](../code/results/benchmarks/README.md).
Sizes are exact; times are indicative (one laptop, client and server together, repeat runs differed up to about 2x).

**Track 1 (Cleveland, browser benchmark, 100% decision match in all 21 settings on both datasets)**

| Setting | Upload per patient | Keys (sent once) | Browser encrypt |
|---|---|---|---|
| Reference, first web client (N=16384, no compression), per-feature | 16.3 MB | none | 329 ms |
| **Delivered: per-feature, N=4096, 46/46, 2^26, seeded + zstd** | **354 KB** | **none** | **16 ms** |
| Haq-style setting, per-feature | 5.9 MB | none | 591 ms |
| Haq-style setting, packed, full rotation keys | 466 KB | 44.4 MB | 24 ms |
| Comparison only: packed, N=4096, 54/54, 2^30, seeded + zstd | 30 KB | 241 KB | 3 ms |

| Row | Finding |
|---|---|
| 0–2, 4 | Shorter chains and lower N work down to N = 4096 with two primes. Going lower in precision breaks the packed layout first (sweep) |
| 3 | Compression: per-feature at N=4096, none 833 KB, zlib 716 KB, zstd 706 KB (about 15% saved; zstd is much faster than zlib). The first web client had compression **off** |
| 5 | Seeded encryption halves the upload (706 → 354 KB per-feature; 60 → 30 KB packed). It works from node-seal 7.0.0 to TenSEAL 0.3.16 |
| 6 | Browser sigmoid generates **no** relinearisation keys; per-feature needs **no** rotation keys. Trimming has no effect at the two-prime setting (there is nothing to drop). Keys: made fresh when the page loads, never stored |
| 7 | Server cubic works at N = 8192 (31/26/26/26/31). Per-feature cost vs the delivered browser sigmoid: upload 354 KB → 3.4 MB, plus 685 KB relinearisation keys |
| H | The delivered setting is lighter than the Haq-style setting on our machine: per-feature upload about 17x smaller; also smaller than Haq-style packed (466 KB + 44.4 MB keys) |

**Finding to decide on:** with only the four rotation keys it needs, **packed** is lighter than per-feature even for one
patient (30 KB + 241 KB keys against 354 KB), and about 12x lighter for each further patient. Per-feature stays the
delivered layout (corrected report, #26). One reason to keep it: in the packed layout as built, the other slots of the
returned ciphertext hold partial sums, from which a client could work out model weights; masking them would need an extra
level. The model is trained on public data, so this is low sensitivity. **Changing the delivered layout is a team decision.**

**Track 2 (10-fold cross-validation, 10 repeats): logistic regression stays.**

| Model | Cleveland accuracy | Edinburgh accuracy | Passes rule (a)? |
|---|---|---|---|
| Logistic regression | 0.8339 ± 0.0660 | 0.9175 ± 0.0257 | reference |
| M1 tuned LR | 0.8382 | 0.9159 | no |
| M2 linear SVM | 0.8362 | 0.9186 | no |
| M4 square-activation MLP | 0.8359 | 0.9130 | no |

M4 also fails the cost limits: per-feature about 3.5 MB and 121 ms server calculation against 706 KB and about 1–2 ms
for logistic regression under the same (public-key) encryption. The MLP's tuning grid was widened once (stronger
regularisation, fewer epochs) because the first grid over-fitted on Cleveland (0.753); all tuning stays inside the
training folds.

### Status

| Item | Status |
|---|---|
| Track 1 rows 0–7 and H | **Done** |
| Track 2: M1, M2, M4 | **Done** |
| Web system: browser sigmoid, per-feature, tested settings, seeded + compressed, exact parameter check, result range check | **Done**, tested live in a headless browser |
| Security assessment (tests 2, 4, 5, 6), CORS allow-list, SRI, per-user quotas, container, fuzz tests | **Not done** |
| Timing on other computers, over a real network | **Not done** |
| Literature review: 4 unscreened, 6 awaiting full text, quality scoring, second reader | **Not done** (needs people with library access) |
