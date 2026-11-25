# Finalized design decisions (Architecture v1.0, 15 Nov 2026)

One-page summary of what is closed, why, and which paper backs it. Source of truth for each row is
[`architecture.md`](architecture.md) and [`planning/decision-log.md`](../planning/decision-log.md).
Papers other than PR2 were added from memory: **verify details before citing.**

"Open to ablation" means the value is final as the *reference setting* but Capstone 2 will test cheaper
alternatives ([`planning/project-direction.md`](../planning/project-direction.md), lever in brackets).
It stays the reference row 0 in the ablation table until a measured row beats it with ≥ 90% decision match.

| Finalized | What it is | Reason | Reference paper | Open to ablation? |
|---|---|---|---|---|
| Browser-to-server encrypted inference; secret key and plain data only in the browser | Patient encrypts in the browser, server computes on ciphertext only, only the patient decrypts | Server never sees the health data or the result | Acar et al., A Survey on Homomorphic Encryption Schemes, ACM Computing Surveys, 2018 | No |
| CKKS | Approximate arithmetic on encrypted real numbers | Handles real-valued features such as blood pressure | Cheon, Kim, Kim, Song, ASIACRYPT 2017 | No (#1) |
| Polynomial modulus degree 16,384 | Polynomial size: bigger = more room, bigger and slower ciphertexts | Pilot setting (supports weighted sum plus the server cubic); the browser sigmoid needs far less | Albrecht et al., Homomorphic Encryption Security Standard, 2018; Microsoft SEAL 4.1 | **Yes** (L1–L3: 8192, 4096 logit-only) |
| Scale 2^40 | Fixes decimal precision of encoded numbers | Encrypted accuracy matched plain (0.853) | PR2 Table 5 | **Yes** (L1) |
| **Sigmoid in the browser (main, #24)**; least-squares cubic on the server is an add-on | The server returns the encrypted score and the browser applies the sigmoid after decrypting. The degree-3 least-squares cubic (ciphertexts allow only + and ×) stays as a measured extra | Same privacy, fewer levels, no relinearisation keys; the cubic error (0.031 in PR2, 0.0356 on the 11 Nov re-run, still to settle, Khalid) only matters for the add-on | Haq et al. (sigmoid after decryption); Kim et al., BMC Med Genomics, 2018 (cubic) | Add-on measured in row 7 |
| Logistic regression (scikit-learn); weights, bias, scaler stored in repo | Weighted sum plus bias, sigmoid for risk | Cheap on ciphertext; model files hold no patient data | Pedregosa et al., Scikit-learn, JMLR 2011 | No |
| Browser client: node-seal 7.0.0 (SEAL 4.1.2) | JavaScript/WebAssembly port of SEAL | Keygen, encryption, decryption in the browser | Microsoft SEAL; node-seal (github.com/morfix-io/node-seal) | No (#13) |
| FHE service: FastAPI + TenSEAL 0.3.16 | Python wrapper of SEAL behind a web framework | Computes with public context, evaluation keys and model weights only | Benaissa et al., TenSEAL, 2021 | No |
| Pinned versions | Exact library versions | TenSEAL 0.3.17+ rejects node-seal ciphertexts | Project pilot finding; no paper | No (#13) |
| Gateway: Node.js (Express) | Front layer for access control and validation | TLS, authentication, rate limiting, request checks; sees ciphertext only | Engineering choice; no paper | No |
| One ciphertext per feature (13) | Each feature in its own ciphertext | Packed needs 163.9 MB Galois keys; per-feature needs none and matched plain (0.877) | PR2 Table 5 | Layout fixed (#15); its cost is what L1–L7 reduce |
| Dataset: UCI Cleveland (13 features) | Cleveland Clinic heart disease data | Pilot dataset; accuracy 0.853, ROC-AUC 0.947 (plain and encrypted) | Detrano et al., Am. J. Cardiology 64(5), 1989; UCI repository | No |
| Dataset: Edinburgh MI (9 features) | Myocardial infarction data from Edinburgh | Second dataset; request about 11 MB; Edinburgh benchmarks scripted (11 Nov run), reviewed in Week 13 | Kennedy et al., Eur. Heart J. 17(8), 1996 (PR2 ref. [8]) | No |
| Plan B: node-seal on a Node.js server, or local Python client | Fallback design | Used only if browser encryption fails the Capstone 2 tests; weakens the browser-encryption claim | Project design decision; no paper | No |

## Corrections made while filing this table
- Detrano 1989 is the *American* Journal of Cardiology (as in PR2 ref. [7]), not "Int. J. Cardiology / Am. J.".
- The Edinburgh reference was blank; it is Kennedy et al. 1996 (PR2 ref. [8]).
- "Benchmarks not yet run" for Edinburgh was out of date: the 11 Nov official run has Edinburgh results
  (`code/results/README.md`); the Week 13 plan has Sarim re-checking them.
- Added the "Open to ablation" column so nothing here reads as contradicting the improvement plan.
