# Project direction – what we are improving, and how we will prove it

Written 25 Nov 2026 from the team discussion, Progress Report 2 (submitted 8 Nov) and the baseline paper
(Haq, Chen and Chen, *Algorithms* 18, 731, 2025 – notes in [`research/baseline-paper/`](../research/baseline-paper/README.md)).
Status: **proposed, team to confirm** (decision #20 in [`decision-log.md`](decision-log.md)).

## 1. The goal in three sentences

1. Haq et al. (2025) show that logistic regression, SVM and a small MLP can run on CKKS-encrypted heart
   and breast-cancer data with the same accuracy as plaintext. They use **one fixed, heavy encryption
   setting for every model** (N = 8192, eight primes, six of them "to provide redundancy", chosen by
   trial and error) and compute the sigmoid after decryption.
2. We take that result as our reference point and **make the same kind of service lighter**: choose the
   smallest secure settings for our one model, and shrink the request, the response, the keys and the
   computation time. We also add what they do not cover: the patient encrypts in the browser and keeps the
   secret key, and the server computes the sigmoid on ciphertext.
3. **Accuracy is not what we improve.** Encryption can at best match the plaintext model (Haq got
   identical numbers with and without encryption). Our claim is *"same decisions as the plaintext model,
   at a lower measured cost"* – which is exactly RQ-A and RQ-B.

Every improvement below is an **expectation until we measure it**. Nothing here goes into a report as a
result before it is in `code/results/`.

## 2. Where this fits (nothing in the existing plan changes)

| Existing commitment | How the direction relates |
|---|---|
| RQ-A: ≥ 90% decision match (#16) | Every lever below must keep this (and ideally 100%, as in the pilot) |
| RQ-B: cost of privacy (time, ciphertext, keys, accuracy) | The levers *are* the RQ-B experiments; the benchmark plan gets an ablation table |
| One ciphertext per feature (#15) | Kept. The levers are chosen to make that layout cheaper |
| Encrypted cubic sigmoid on the server (PR2 objective 3, architecture) | Kept as the main design; logit-only output is measured as the comparison |
| Pinned versions node-seal 7.0.0 / TenSEAL 0.3.16 (#13) | Kept. Any lever that needs a different version is out |

## 3. Ways to improve (the levers)

"Box" = the CKKS parameter set (N, primes, scale). Bigger box = more room for maths, more bytes, more time.

| # | Lever | What changes | Expected effect | Honest caveat | How we prove it | Owner / when |
|---|---|---|---|---|---|---|
| L1 | **Smaller modulus chain** | Today `[60,40,40,40,40,60]`, scale 2^40. Find the shortest chain and smallest scale that keep 100% decision match | Fewer primes ⇒ smaller ciphertexts, keys and faster operations (cost scales with N × number of primes) | Too small a scale breaks accuracy: Haq's own Table 10 shows 2^24 and 2^22 collapsing | Sweep chains/scales on Cleveland + Edinburgh; table of size, time, decision match | Hassan, Khalid – Wk 13/14 |
| L2 | **Lower N: 16384 → 8192** (cubic) | Halves the polynomial size | About half the ciphertext bytes and less compute | The 128-bit limit at N = 8192 is a total of 218 modulus bits; the cubic needs enough levels to fit | Already in the Week 13 plan: N = 8192 with and without compression | Hassan – Wk 13 |
| L3 | **N = 4096, logit-only output** | Server returns the encrypted weighted sum; browser applies the sigmoid after decryption | Smallest box: no relinearisation keys, fewer levels | Limit at N = 4096 is 109 bits, so scale and precision are tight; **may not hold 100% match – test, do not assume**. Does not work with the encrypted cubic | Same sweep as L1 with `output = "logit"` | Khalid – Wk 13/14 |
| L4 | **Seeded (symmetric-key) encryption in the browser** | The browser owns the secret key, so it can encrypt with the secret key; a fresh ciphertext then stores a seed instead of its second polynomial | Roughly halves the upload | Must be confirmed in node-seal 7.0.0 and readable by TenSEAL 0.3.16 (the pinned pair) | Round trip test, then size comparison | Saif – Wk 14 |
| L5 | **Compression (zstd)** | SEAL can compress when saving | Smaller upload | **Probably already on by default** in both libraries: our 1.0 MB per feature and Haq's 477 KB per sample are both smaller than the raw size for their parameters. First task is to check what is currently on, otherwise we double-count | Measure raw vs compressed serialisation | Hassan – Wk 13 |
| L6 | **Shrink the response** | Before returning, the server switches the result ciphertext down to the last prime | Smaller download (Haq's result is almost as large as their input, which suggests no trimming) | Cheap to try; benefit is on the response only | Size of the result before/after | Saif – Wk 14 |
| L7 | **Only the keys we need** | Relinearisation keys only (no Galois keys, per #15); seeded key serialisation; decide key reuse vs per-load keys (T3) | Keys are uploaded from the browser, so they matter more for us than for Haq, whose keys never leave the hospital | Reusing keys means storing a secret key at rest (threat model T3) | Key-size table; T3 decision | Abdullah, Naif |
| L8 | **Sigmoid location (A vs B)** | A: encrypted cubic on the server (main). B: logit only, sigmoid in the browser | B gives the smallest box and the largest savings. In both options only the patient can decrypt; A returns an encrypted risk probability, B an encrypted score (logit) | A is what PR2 objective 3 promises. Haq also does B, so "faster than Haq" is only meaningful against B | Measure both, report which is lighter | Capstone 2 |
| L9 | **Packed layout with targeted rotations** | All 13 features in one ciphertext, summed with rotations by 1, 2, 4, 8 only | About 1 MB per patient | Rotation keys are only generated for those four steps, not the 164 MB default set; this is a *backlog* option because #15 chose per-feature | Measure the four-key size | Capstone 2 backlog |
| L10 | **Hardware** | GPU, faster CPU | **GPU: no effect** – TenSEAL/SEAL run on the CPU only (Haq's A100 is not used by CKKS). A faster CPU helps all variants equally | Timings are only comparable on one machine | Record the CPU in every results file (already in the JSON `environment`) | Everyone |
| L11 | **Accuracy-side work (not encryption)** | Nested/k-fold cross-validation, feature scaling, regularisation, hybrids like Haq's LR-MLP | Makes the *accuracy figure* more trustworthy or higher | Out of the RQ-A scope (RQ-A is logistic regression); a hybrid MLP needs depth 3, which makes the box bigger again | Optional: report 10-fold CV next to the fixed split so we can compare with Haq | Sarim – optional |

### Do the fairest comparison with Haq

Reproduce **their** setting (N = 8192, chain `31,26×6,31`, scale 2^26) on **our machine and our data** and put
it in the ablation table as "Haq-style configuration". That is the only comparison that is not distorted by
different hardware, data split or sigmoid placement.

## 4. What we can and cannot claim

| Claim | Allowed? |
|---|---|
| Same decisions as the plaintext model (≥ 90%, measured 100% in the pilot) | Yes – measured |
| Smaller request / keys / faster than the fixed-setting approach of Haq et al. | Only after the ablation shows it, on our machine, against the Haq-style row |
| More accurate than Haq et al. | **No.** Different data splits (our test sets are 75 and 314 patients, theirs 60 and 114); and see the table inconsistency in the paper notes |
| Faster than Haq et al. in absolute terms | **No** – different hardware, model and sigmoid placement |
| A GPU makes it faster | **No** |
| Hybrid models improve our results | Not tested; out of scope |

## 5. Where the proof comes from

Two kinds of evidence, and we need both:

**A. Papers (why we expect it to work).** Read these for the specific lever, then add a row to
`research/reading-list.md`. Items marked ✔ are already in our list; the rest are named so the team knows
what to look for – *check each exists and says what we think before citing it*.

| Lever | Read |
|---|---|
| L1–L3 (chain, N, scale) | ✔ Haq et al. §4.4, §5.5 (their own sweep, Table 8–10); ✔ TenSEAL tutorials (their refs 36, 37); Cheon et al. CKKS (rescaling and levels); the HomomorphicEncryption.org security standard (maximum modulus bits per N for 128-bit security) |
| L3, L8 (logit-only, sigmoid) | ✔ Naresh and Reddi 2025 (CKKS LR, TenSEAL); ✔ Kim et al. 2018 (cubic sigmoid); ✔ ANN activation estimators for HE (reading list #11) |
| L4–L7 (seeded encryption, compression, keys) | Microsoft SEAL documentation and examples (serialisation, compression modes, seeded/symmetric encryption); ✔ TenSEAL paper |
| L7, L9 (client-side cost, who holds keys) | ✔ GuardML (hybrid HE, reading list #13); ✔ Haq et al. §6 future work |
| General cost numbers | ✔ Cenitta 2025 (≈ 420 ms/prediction CKKS); ✔ Wang 2020 (tree timings); ✔ Wood and Najarian 2020 survey (cited by Haq) |

**B. Our own measurements (that it did work).** The papers only justify trying a lever; the result is the
benchmark. See the ablation section of [`design/benchmark-plan.md`](../design/benchmark-plan.md).

## 6. Order of work

1. **Wk 13 (now, already assigned):** N = 8192 with/without compression (Hassan); N = 8192 and logit-only accuracy (Khalid); sigmoid error figure settled.
2. **Check first:** is compression already on (L5)? One run, ten minutes, avoids wrong claims.
3. **Wk 14:** modulus/scale sweep (L1, L3); seeded encryption and response trimming (L4, L6) if node-seal supports them with the pinned versions.
4. **Capstone 2:** full ablation on both datasets, A-versus-B sigmoid, key-reuse decision, then the reported RQ-B table.
5. **Final report (Thu 26 Nov):** present this as the Capstone 2 plan and the evidence we will collect. No improvement is reported as a result.

## 7. Inconsistencies found while writing this, and how they are settled

| Where | Conflict | Resolution |
|---|---|---|
| PR2 §A.4 Part 3 says all 13 features are packed into one ciphertext | PR2 §A.3, the round trip and the prototype use one ciphertext per feature | Per-feature (#15; PR2 errata #6). Packed appears only as the measured comparison (L9) |
| An earlier suggestion in the team chat: "N = 4096" for our model | The encrypted cubic needs more levels than 4096 allows | 4096 only for logit-only output (L3), and only if it passes. Main target is 8192 |
| Chat: "pack features and add with rotations 1, 2, 4, 8" | Only applies to the packed layout; the chosen per-feature layout needs no rotations | Backlog L9 |
| Chat: "Haq et al. don't use compression" | Their sizes suggest default compression is on | Unknown; check L5 first and do not claim it |
| 90% vs 95% decision match | PR2 mentions both | 90% is pass, 95% expected (#16) |
| Sigmoid error 0.031 (PR2) vs 0.0356 (11 Nov re-run) | Two numbers | Still open for Khalid: one number plus one method sentence |
| Haq et al. Table 3 (Cleveland) | With 60 test patients the specificity of 0.7768 cannot follow from the other columns | Do not use their CHD numbers as a hard benchmark; see paper notes |
