# Logbook notes – Saif
Write here right after you work, so you don't forget. Copy into the COMP4101 logbook template before the deadline.
Minimum: 6 hours per week. Only log days you actually worked.

## Week 6 (27 Sep – 1 Oct)
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 27 Sep | 4:00–6:00 PM | Team meeting #1 (see meetings/MEETING_NOTES.md) | 2 |
| | | | |
| Thu 1 Oct | 11:00 AM–1:00 PM | Supervisor meeting #1 (see meetings/MEETING_NOTES.md) | 2 |
| **Total** | | | |

## Week 7 (4 – 8 Oct)
SLR (v3, Pair 1, screener 1): run the IEEE Xplore search, fill the Search Log tab of the live PRISMA sheet; Naif confirms the count. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Checklist: [slr/TASKS.md](slr/TASKS.md)
*Draft – check every line, fill in the [ ] parts, delete anything you didn't do, then commit from your own account.*
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| [fill in: Sun 4–Wed 7 Oct] | [fill in] | Researched Microsoft SEAL, node-seal and TenSEAL with Naif and checked whether they are compatible (encryption in the website front end, encrypted model on the server) | [fill in] |
| Thu 8 Oct | 11:00–13:00 | Weekly supervisor/team meeting [confirm attendance] | 2 |
| [fill in: Fri 9 or Sat 10 Oct] | [fill in] | Read SLR Protocol v3 and replied to Abdullah | [fill in] |
| Sat 10 Oct | [start: fill in]–18:56 | Ran the IEEE Xplore search (337 results), exported the results and filled the search notes | [fill in] |
| [fill in: Fri 9–Sun 11 Oct] | [fill in] | Progress Report 1: feasibility/risk paragraph | [fill in] |
| Sun 11 Oct | 16:00–18:00 | Team work session on Progress Report 1 [confirm after the session] | 2 |
| **Total** | | | **4 h** |

*Short by 2 h: add real work you did this week (date, time, task).*

## Week 8 (11 – 15 Oct)
No logbook (mid-term) – keep notes.
SLR: screen all of Set 1 (Screening Log, column G) independently of Naif; compare and settle differences (Abdullah breaks ties).
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | | |
| **Total** | | | |

## Week 9 (18 – 22 Oct)
Semester break – no logbook.

## Week 10 (25 – 29 Oct) – as submitted

Copied word for word from the submitted logbook PDF (COMP4101_Practicum_Logbook_Template_Fall2026_v2_60305560 - week10.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 25 Oct | 4:00–6:00 PM | Attended the weekly team meeting where we planned Week 10, and I was assigned to Pair 1 with Naif. My tasks were to run the encrypted round-trip pilot (node-seal 7.0.0 and TenSEAL 0.3.16) and record the errors, measure ciphertext and key sizes for the cost tables, check the IEEE search string against my IEEE Xplore search history, and give the team technical facts for the threat model. | 2 |
| Mon 26 Oct | 2:00–4:00 PM | Individual work: Worked independently on my assigned technical tasks. I set up the local testing environment (Python 3.12, Node 22.22.2) and reviewed the pilot scripts for node-seal and TenSEAL. I tested the toy examples (addition, plaintext multiplication, ciphertext multiplication) and investigated the TenSEAL protobuf wrapper layout to resolve compatibility issues with node-seal ciphertexts.. | 2 |
| Thu 29 Oct | 9:00–11:00 PM | Worked collaboratively with Saeed Abdullah as we missed our weekly supervisor meeting. I finalized the encrypted round-trip testing: I verified that node-seal encrypts and decrypts correctly, recorded the maximum error rates (approx. 3.3 × 10⁻⁷), and documented cipher/key sizes (ciphertext 0.39 MB, public key 0.52 MB, relin keys 1.57 MB, secret key 0.26 MB) for the team’s cost tables. We also reviewed our screening workflow against the PRISMA tracking sheet (covering our database search results) and coordinated our Pair 1 review tasks. Finally, we aligned our technical pilot findings with Abdullah’s API endpoint requirements. | 2 |
| **Total** | | | **6 h** |

## Week 11 (1 – 5 Nov) – as submitted

Copied word for word from the submitted logbook PDF (COMP4101_Practicum_Logbook_Fall2026_60305560 - week11.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 1 Nov | 4:00–6:00 PM | Progress: Read 2 papers on homomorphic encryption (HE) and heart disease.<br><br>**Paper 1:** Logistic Regression Model Training based on the Approximate Homomorphic Encryption. Kim, Song, Kim, Lee, Cheon (preprint; check the “Source title” column in my sheet, I think BMC Medical Genomics, 2018)<br>• What they did: Trained logistic regression on encrypted data using HEAAN (HE for real numbers). Three speed-ups: the whole table packed into one ciphertext, Nesterov training, and a polynomial replacing the sigmoid. Winner of iDASH 2017.<br>• Findings: 1,579 samples took about 6-8 min and 0.04 GB. On the Edinburgh dataset: 3.6 min and 0.02 GB, versus 114 min and 0.69 GB for the older method.<br>• Liked: Clear and step by step, open-source code, huge speed-up.<br>• Problems: o Only about 7-9 training rounds, since there is no bootstrapping. o Accuracy only about 62% on the competition data, with no unencrypted baseline for comparison. o 80-bit security, which is outdated. o Learning rate not tuned.<br>• Verdict: Strong speed improvement, but model quality and security level are limited.<br><br>**Paper 2:** A Review on Explainable, Federated Multimodal AI for Heart Disease Detection Using ECG, Cardiac Imaging, and EHRs. Murali & Meenatchi, Engineering Reports (Wiley), 2026<br>• What they did: Systematic review of heart disease prediction papers, 2015-2025 (550 checked, 72 kept), comparing ML, DL and federated learning. They propose a framework combining ECG, images and health records, with explainability (Grad-CAM, SHAP) and federated learning plus HE.<br>• Findings: Most studies use small or single datasets, don’t test on new data, and rarely measure the cost of privacy tools like HE. Many report 98-100% accuracy, but on different datasets, so they can’t be compared fairly.<br>• Liked: Wide coverage, many tables, an honest “risk” table of the field’s weak points.<br>• Problems: o Counts are inconsistent (67 vs 72 studies kept), and the exclusion numbers don’t sum. o Some off-topic papers (e.g., software effort estimation). o The framework is only described, never built or tested. o HE is only a small part of the paper.<br>• Verdict: Useful map of the field, but sloppy with numbers, and the framework is just an idea.<br>Next: Papers 3 and 4. | 2 |
| Mon 2 Nov | 12:00–2:00 PM | Progress: Read 2 papers on privacy for heart disease monitoring and federated learning.<br><br>**Paper 3:** Secure Healthcare Monitoring: Algorithms and Techniques for Heart Disease Detection and Data Privacy. Poonam & Mallapur, ICISCN 2025 (IEEE)<br>• What they did: Short survey on healthcare monitoring and data privacy, covering ML for heart disease (SVM, decision trees, neural networks) and encryption (AES, ECC, HE).<br>• Findings: FHE-based method reported highest accuracy (99.8%); Paillier had the shortest encryption time (0.09 s). Open problems: scalability, real-time speed, compliance with health data laws.<br>• Liked: Good topic, and it explains the wearable and real-time monitoring problem clearly.<br>• Problems: o Inconsistent numbers: 15 vs 25 papers, and “18 papers = 72%” becomes “15 papers = 72%”. o Empty sections (Springer and Elsevier analysis). o Claiming FHE “reached the highest accuracy” is misleading, since accuracy depends on the model and data, not the encryption. o Short, with only brief descriptions of each paper.<br>• Verdict: Easy, relevant overview, but thin and inconsistent.<br><br>**Paper 4:** MediVault: An Auditable and Secure Federated Learning System for Privacy-Preserving Healthcare Collaboration. Li, Adeel, Akram, Algorithms (MDPI), 2026<br>• What they did: Federated learning across hospitals. Each hospital encrypts its model update with Paillier and hides it with a random mask. A dashboard logs events so partners can audit later. Tested on breast cancer and heart disease data with 2 and 5 hospitals.<br>• Findings: Federated results were close to centralised (heart disease accuracy 0.853 vs 0.868). Encryption is costly: a small update took about 260 ms and grew from 0.24 KB to 9.4 KB; the neural network update took about 8.7 s.<br>• Liked: Honest about limits, measured encryption cost, tested Non-IID data, public code.<br>• Problems: o Only one random seed, and the heart test set is tiny (about 61 patients), so small differences may be luck. o Masking works only for 2 hospitals, but tests use 5. o The neural network scores better federated than centralised on heart disease (about 0.89 vs 0.82), suggesting a weak baseline. o 1024-bit Paillier key is small today, and the logs are not tamper-proof (admitted).<br>• Verdict: Nice working prototype, but too small and lightly tested to prove its claims.<br>Next: Papers 5 and 6. | 2 |
| Thu 5 Nov | 3:00–5:00 PM | Progress: Read 1 paper; the other could not be read (reason below).<br><br>**Paper 5:** Exploring the future of privacy-preserving heart disease prediction: a fully homomorphic encryption-driven logistic regression approach. Naresh & Reddi, Journal of Big Data, 2025<br>• What they did: Logistic regression on encrypted heart disease data using CKKS (TenSEAL). Compared two encryption sizes (4096 and 8192) and SVM. Argued HE protects against five kinds of attack.<br>• Findings: Accuracy 84% encrypted vs 85% normal logistic regression. Size 8192 is much slower (encrypting training data: 4.5-12 s vs 1-1.7 s).<br>• Liked: Easy to follow, clear time costs, admits scaling to large data is hard.<br>• Problems: o The gradient is decrypted and re-encrypted every round, so training is not fully encrypted and the key holder must keep participating. o Weak security claims: HE can’t stop poisoning or evasion attacks, since anyone can encrypt bad data with the public key. o One dataset shows a perfect 100%, which looks like an error or data leakage. o Wrong ROC explanation (AUC can’t be measured “at one threshold”). o Not a big step beyond Paper 1, which was faster and better described 7 years earlier.<br>• Verdict: Easy to read, but security claims are overstated and results look doubtful.<br><br>**Paper 6:** International Conference on Soft Computing and Signal Processing, ICSCSP 2018. Advances in Intelligent Systems and Computing, 2019<br>• Not readable: It is a “Conference Review” page summarizing a whole conference (156 papers), listing only topic names, with no full text.<br>• To do: Search for the exact titles of two useful papers inside it: “homomorphic encryption scheme for data security in cloud using compression technique” and “clustering algorithms with heart disease datasets using the Weka tool.” | 2 |
| **Total** | | | **6 h** |

## Week 12 (8 – 12 Nov)
Logbook due Sun 15 Nov. **Write these rows yourself, the same day you work** – the course treats AI-written logbook entries as academic dishonesty. The prompts below are only reminders of what to record (from your README's next steps); delete them as you fill in real entries.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | run_pilot.sh on your machine – did it finish? exact numbers vs PR2 Table 5 | |
| | | Machine used (CPU, RAM, OS) | |
| | | Extraction rows verified (P035, P014) – page/table found | |
| | | Final report sections drafted (Background, crypto method, pilot results) | |
| **Total** | | | |
