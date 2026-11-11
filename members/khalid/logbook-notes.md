# Logbook notes – Khalid
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
SLR (v3, Pair 3, screener 1): Scopus search check first, then the Scopus search; fill the Search Log tab of the live PRISMA sheet; Abdullah confirms. Reply 'changes' or 'no changes' on Protocol v3 to Abdullah by Sat 10 Oct. Checklist: [slr/TASKS.md](slr/TASKS.md)
*Draft – check every line, fill in the [ ] parts, delete anything you didn't do, then commit from your own account.*
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| [fill in: Sun 4–Wed 7 Oct] | [fill in] | Reviewed research papers with Sarim and found 5 more datasets used in previous work | [fill in] |
| Thu 8 Oct | 11:00–13:00 | Weekly supervisor/team meeting [confirm attendance] | 2 |
| [fill in: Fri 9 or Sat 10 Oct] | [fill in] | Read SLR Protocol v3 and replied to Abdullah | [fill in] |
| Sat 10 Oct | [start: fill in]–19:53 | Scopus search check (2 of 3 known papers found), then the Scopus search (1,017 results). Tested narrowing the search and exported the results | [fill in] |
| [fill in: Fri 9–Sun 11 Oct] | [fill in] | Progress Report 1: "Expected results" section | [fill in] |
| Sun 11 Oct | 16:00–18:00 | Team work session on Progress Report 1 [confirm after the session] | 2 |
| **Total** | | | **4 h** |

*Short by 2 h: add real work you did this week (date, time, task).*

## Week 8 (11 – 15 Oct)
No logbook (mid-term) – keep notes.
SLR: screen all of Set 3 (Screening Log, column G) independently of Abdullah; compare and settle differences (Naif breaks ties).
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | | |
| **Total** | | | |

## Week 9 (18 – 22 Oct)
Semester break – no logbook.

## Week 10 (25 – 29 Oct) – as submitted

Copied word for word from the submitted logbook PDF (Logbook_3_60306117.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 25 Oct | 4:00–6:00 PM | I took part in a team planning session focused on the systematic literature review (SLR) and project responsibilities. I reviewed the current search pool of 1,044 unique records from IEEE Xplore, PubMed and Scopus after deduplication. We discussed how the review should use a documented protocol and reproducible selection decisions rather than AI-based paper ranking. I considered the three-pair allocation, the four research questions (FHE schemes/libraries, model accuracy and sigmoid approximations, computational cost, and key management/client encryption), and the need to maintain PRISMA screening records. Topics I referenced in the discussion: confirming inclusion/exclusion criteria, independent title/abstract screening and disagreement resolution, and preparing for full-text review. | 2 |
| Thu 29 Oct | 11:00 AM–1:00 PM | I attended a supervisory meeting with Dr. Abdulatif Shikfa, as recorded in the reference logbook. During the meeting, our team raised concerns about having over 1,000 SLR records remaining after the initial filtering process. The supervisor clarified our questions and discussed techniques that could help narrow down the pool of research papers. Following the meeting, I discussed the key points with my team and helped divide the follow-up tasks.<br><br>My key SLR follow-up responsibilities included tightening and consistently applying the eligibility criteria, documenting every exclusion in the PRISMA record, independently screening records and resolving disagreements with the team, prioritizing relevant FHE-on-healthcare ML papers for full-text review, extracting comparable benchmark and accuracy data, and maintaining a reproducible research protocol. These follow-up actions reflect the guidance and tasks established through our team discussion rather than a verbatim account of the meeting. | 2 |
| Sat 31 Oct | 6:00–8:00 PM | I dedicated a two-hour weekend work block to reviewing the SLR references and organizing the research evidence. I revisited the written screening criteria, checked the consistency of the PRISMA exclusion labels, and outlined the RQ3 evidence table focusing on FHE performance costs.<br><br>I also reviewed how different studies report encryption, encrypted inference, and decryption times, identifying missing hardware specifications and parameter details. Additionally, I considered why performance measurements obtained using different machines and hardware configurations should not be directly compared.<br><br>This entry describes the suggested activities for the two-hour work block; individual task completion has not been independently verified. | 2 |
| **Total** | | | **6 h** |

## Week 11 (1 – 5 Nov) – as submitted

Copied word for word from the submitted logbook PDF (Logbook_Week11_603036117.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Tue 3 Nov | 6:00–8:00 PM | Reviewed GuardML (Frimpong et al., 2024), which uses Hybrid HE (PASTA + BFV) with Microsoft SEAL on MIT-BIH ECG data (13,245 train/test samples). Models use a 4-bit integer quantized fully connected layer achieving 87.55% encrypted accuracy (~0.65% accuracy gap). Encrypted outputs are sent to the analyst, indicating sigmoid activation occurs post-decryption. BFV requires integer quantization, unlike our CKKS floating-point approach.<br>Reference: Frimpong, E., et al. (2024). GuardML: Efficient Privacy-Preserving Machine Learning Services Through Hybrid Homomorphic Encryption. ACM SAC. https://doi.org/10.1145/3605098.3635983 | 2 |
| Wed 4 Nov | 3:00–5:00 PM | Analyzed Nguyen et al. (2024) from IEEE DASC. Shares the same author team, PASTA + BFV scheme, and MIT-BIH dataset as GuardML, representing overlapping project evidence. For RQ4, it introduces a trusted-hardware variant for key generation alongside analyst generation. Exact accuracy numbers and execution timings were not reported in the accessible text, requiring careful screening to avoid duplicate counting.<br>Reference: Nguyen, K., et al. (2024). A Pervasive, Efficient and Private Future: Realizing Privacy-Preserving Machine Learning Through Hybrid Homomorphic Encryption. IEEE DASC. https://doi.org/10.1109/DASC64200.2024.00013 | 2 |
| Thu 5 Nov | 1:00–3:00 PM | Extracted findings for Sayyad & Kulkarni (2022), which uses HElib on our exact target dataset (UCI Heart Disease); accuracy figures and model specs were not reported. Naresh & Varma (2025) uses CKKS with Federated Learning on stroke data (5,111 samples) achieving ~96% accuracy with ~17% overhead. Yadkar et al. (2025) and Sravani & Kumar (2025) were cataloged for full retrieval.<br>References: Sayyad, S., & Kulkarni, D. (2022). IJISAE, 10(3), 129–134. Naresh, V. S., & Varma, G. T. (2025). Smart Health, 37, 100594. https://doi.org/10.1016/j.smhl.2025.100594 Yadkar, M. S., et al. (2025). IEEE ICBATS. https://doi.org/10.1109/ICBATS66542.2025.11258322 Sravani, K. V., & Kumar, A. P. S. (2025). CRC Press. https://doi.org/10.1201/9781003685364-11 | 2 |
| **Total** | | | **6 h** |

## Week 12 (8 – 12 Nov)
Logbook due Sun 15 Nov. **Write these rows yourself, the same day you work** – the course treats AI-written logbook entries as academic dishonesty. The prompts below are only reminders of what to record (from your README's next steps); delete them as you fill in real entries.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | fit_sigmoid.py on both datasets – MAE and decision match you got | |
| | | Target agreed: 90% or 95%? pass/fail | |
| | | Extraction rows verified (P034, P005) | |
| | | Full texts requested: Sayyad & Kulkarni, Yadkar, Sravani & Kumar – result | |
| | | Final report sigmoid section; RQ2 with Abdullah | |
| **Total** | | | |
