# Logbook notes – Naif
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
SLR (v3, Pair 1, screener 2): re-run Saif's IEEE Xplore search to confirm the count; add the protocol + search counts to PR1. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Checklist: [slr/TASKS.md](slr/TASKS.md)
*Draft – check every line, fill in the [ ] parts, delete anything you didn't do, then commit from your own account.*
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| [fill in: Sun 4–Wed 7 Oct] | [fill in] | Researched Microsoft SEAL, node-seal and TenSEAL with Saif and checked whether they are compatible (encryption in the website front end, encrypted model on the server) | [fill in] |
| Thu 8 Oct | 11:00–13:00 | Weekly supervisor/team meeting [confirm attendance] | 2 |
| [fill in: Fri 9 or Sat 10 Oct] | [fill in] | Read SLR Protocol v3 and replied to Abdullah | [fill in] |
| Sat 10 Oct | [time: fill in] | Re-ran the IEEE Xplore search and confirmed Saif's count (337) | [fill in] |
| [fill in: Fri 9–Sun 11 Oct] | [fill in] | Progress Report 1: SLR section and compiling the report | [fill in] |
| Sun 11 Oct | 16:00–18:00 | Team work session on Progress Report 1 [confirm after the session] | 2 |
| **Total** | | | **4 h** |

*Short by 2 h: add real work you did this week (date, time, task).*

## Week 8 (11 – 15 Oct)
No logbook (mid-term) – keep notes.
SLR: screen all of Set 1 (Screening Log, column H) independently of Saif; tie-breaker for Pairs 2 and 3.
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | | |
| **Total** | | | |

## Week 9 (18 – 22 Oct)
Semester break – no logbook.

## Week 10 (25 – 29 Oct) – as submitted

Copied word for word from the submitted logbook PDF (naif_week_10_COMP4101_Practicum_Logbook_Template_Fall2026_v2.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 25 Oct | 4:00–6:00 PM | Participated in the weekly team meeting to plan Week 10, partnering with Saif for our assigned tasks. Our responsibilities included running the encrypted round-trip pilot using node-seal 7.0.0 and TenSEAL 0.3.16 while documenting errors, measuring ciphertext and key sizes for the cost tables, validating the IEEE search string against my IEEE Xplore history, and compiling technical facts for the threat model. | 2 |
| Mon 26 Oct | 6:00–8:00 PM | I worked on the SLR, but it didn’t go well. My search string was too vague, so what I found wasn’t very useful and I’m not going into detail on it. I needed Dr. Shikfa’s help with it, so I waited for our meeting on Thursday to ask him. I asked Saif to take the encrypted pilot. He set up the environment, tested the toy examples and looked into the node-seal and TenSEAL compatibility issue. I only looked over what he did, because I was busy with the SLR. | 2 |
| Thu 29 Oct | 9:00 AM–1:00 PM | We met Dr. Shikfa. He told us to focus on finishing the SLR and to make our search strings more exact. After the meeting I re-ran my searches.<br><br>IEEE Xplore: `("Abstract":"homomorphic encryption" OR "Abstract":"fully homomorphic" OR "Abstract":FHE) AND "Abstract":"machine learning" AND "Abstract":"heart disease"` But I couldn’t really login for some reasons and for<br><br>Scopus: I made an account and ran `TITLE-ABS-KEY(("homomorphic encryption" OR "fully homomorphic" OR FHE) AND "machine learning" AND "heart disease")`<br><br>From now on we will use these new, more exact strings unless we feel like they not enough. Next week I will divide these papers between the team and we will start screening them. | 4 |
| **Total** | | | **8 h** |

## Week 11 (1 – 5 Nov) – as submitted

Copied word for word from the submitted logbook PDF (naif_week_11_COMP4101_Practicum_Logbook.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 1 Nov | 4:00–6:00 PM | Team meeting: We met with the team and divided the reading work. I was given the papers below. I’ll read them one by one and write up each one.<br><br>My papers: 1. ANN Activation Function Estimators for Homomorphic Encrypted Inference (IEEE Access, 2025) 2. Convergence of Blockchain, k-medoids and homomorphic encryption for privacy preserving biomedical data classification (Internet of Things and Cyber-Physical Systems, 2022) 3. Secure No… (Lecture Notes in Computer Science, vol. 16176, 2026 4. Outsourced privacy-preserving decision tree classification service over encrypted data (Journal of Information Security and Applications, 2020) 5. IEEE International Conference on Data Science and Information System, ICDSIS 2022<br><br>I read Paper 1 after discussing the workload<br><br>**Paper 1** Title: ANN Activation Function Estimators for Homomorphic Encrypted Inference. By: Mhd Raja Abou Harb and Baris Celiktas / Where: IEEE Access, 2025<br>What they did: Homomorphic encryption (HE) lets a cloud do math on locked data. But it only does adding and multiplying, and neural networks need harder functions (sigmoid, tanh). The authors train a small neural network to copy those functions, then use it on locked data. They compare it to two old tricks: a simple curve formula (polynomial) and many small straight lines (piecewise).<br>What they found: On MNIST (handwritten digits), their method gets 87.1% (sigmoid) and 85.6% (tanh). The polynomial gets 85.4% and 49.5%. Their method is also slower (5.7s vs 1.9s).<br>What I liked: It’s easy to read. They test two functions, they honestly show the slowdown, and they add a heart disease example.<br>Problems I found: • Their “estimator” is just one layer with no non-linear part. That means it can only do straight-line math, so it can’t really copy a curve. That goes against their own main argument. • The straight-lines method scores 10%, which is random guessing. I think it was coded wrong, so the comparison isn’t fair. • The tests are small: 1,000 images, and about 61 patients in the heart test. • They say it’s secure, but they never tried any real attack.<br>My verdict: Nice idea, but the proof doesn’t match the claims. | 2 |
| Mon 2 Nov | 7:00–8:00 PM | Progress today: I read Paper 2.<br><br>**Paper 2** Title: Convergence of Blockchain, k-medoids and homomorphic encryption for privacy preserving biomedical data classification. By: Shamima Akter, Farhana Reza, Manik Ahmed / Where: Internet of Things and Cyber-Physical Systems, Vol. 2, 2022<br>What they did: Several data owners (like hospitals) want one analyst to train a k-medoids model (a way to sort data into groups) without the analyst seeing the raw data. They lock the data with Paillier encryption, a type of homomorphic encryption that can only add. They also use a blockchain (Hyperledger) to keep tamper-proof records of who shared what.<br>What they found: On breast cancer data, it gets 97.8% accuracy. On heart disease it gets 82.5%. On diabetes data it does badly (65.2%, while other methods get about 78%). Training takes about 17 to 30 minutes, which they say is faster than other secure methods.<br>What I liked: They admit the diabetes result was bad instead of hiding it. They test 3 different datasets, and they also test how it scales with 1 to 5 data owners.<br>Problems I found: • k-medoids doesn’t use labels, but they report accuracy and recall without clearly explaining how. • Locking the data doesn’t change the math, so the scores are the same as normal k-medoids. The real questions are cost and safety, not accuracy. • Their reason for the diabetes failure (low R²) doesn’t hold up, because the heart disease data also has a low R² and works fine. • The scores of the other methods are copied from other papers, not tested side by side. On breast cancer, secure kNN ties them at 97.80%, so “better than others” is too strong. • The blockchain was never really tested. Everything ran on one laptop with pretend owners. • Paillier can only add, so calling it “polynomial operations” is a stretch. The privacy trick (adding a random number before comparing) is not fully explained. • Training is still slow for such small datasets.<br>My verdict: Good topic, but it is a small step from earlier secure kNN and k-means work, and the claims are bigger than the proof. | 1 |
| Wed 4 Nov | 3:00–6:00 PM | Progress today: I read Paper 3. The other two papers on my list I could not read, and the reasons are at the bottom.<br><br>**Paper 3** Title: Outsourced privacy-preserving decision tree classification service over encrypted data. By: Chen Wang, Andi Wang, Jian Xu, Qiang Wang, Fucai Zhou / Where: Journal of Information Security and Applications, Vol. 53, 2020<br>What they did: A hospital has a trained decision tree (a flowchart of yes/no questions). It wants a cloud server to run it for patients, so the hospital doesn’t have to stay online. Three things must stay secret: the hospital’s model, the patient’s data, and the result. The authors turn the tree into simple math formulas (one per path), lock them, and give them to the cloud. They also build two small locked-math tools: a secure XOR and a secure “is A smaller than B” check.<br>What they found: One classification takes under 1 second and under 500 kB of data. For example, the heart disease tree takes about 84 ms for the user and 66 ms for the cloud. It is also faster than two older schemes (Bost and Wu), and it handles up to 8 users at once.<br>What I liked: It hides all three secrets, the owner can go offline after setup, and the timing results are clear.<br>Problems I found: • It needs a trusted “Key Center”, and the user and cloud must not team up. If they do, the secrets leak. • It only protects against parties that are nosy but follow the rules, not against cheaters. • The timings leave out network time, even though the protocol sends many messages back and forth. That hides a real cost. • The user does most of the work, and the authors admit this. • Only small trees were tested, and the security “proofs” are written as arguments, not strict math proofs. One part even mentions Paillier, which they don’t use.<br>My verdict: Solid and practical, but the trust assumptions are strong.<br><br>Papers I did not read: • Sun Y. et al., Lecture Notes in Computer Science, vol. 16176, 2026 (Springer chapter). I couldn’t read this one because it is behind a paywall. The page asks for an institution login or a payment. I only saw the abstract: it is about a secure decision tree evaluation protocol using fully homomorphic encryption. • IEEE International Conference on Data Science and Information System (ICDSIS 2022). This one is a conference review. It is a summary page for a whole conference (134 papers), not one paper, so there was nothing to read. | 3 |
| **Total** | | | **6 h** |

## Week 12 (8 – 12 Nov)
Logbook due Sun 15 Nov. **Write these rows yourself, the same day you work** – the course treats AI-written logbook entries as academic dishonesty. The prompts below are only reminders of what to record (from your README's next steps); delete them as you fill in real entries.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | Assigned the 4 unscreened records (P002, P011, P023, P029)? To whom? | |
| | | Team decision on partial HE (MediVault, Akter) – what was decided? | |
| | | Final report sections drafted (Introduction, Scope, Feasibility) – pages | |
| | | Threat model review – rows changed/added | |
| | | SLR synthesis RQ1 + RQ4 with Saif – progress | |
| **Total** | | | |
