# Logbook notes – Abdullah Dar
Write here right after you work, so you don't forget. Copy into the COMP4101 logbook template before the deadline.
Minimum: 6 hours per week. Only log days you actually worked.

## Week 6 (27 Sep – 1 Oct)
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 27 Sep | 4:00–6:00 PM | Team meeting #1: understood the project, cleared doubts about the tech, planned the project, got my tasks (repo + board) | 2 |
| Mon 28 Sep | 4:00–5:20 PM | Software research: 3-part architecture, key management, TenSEAL vs node-seal risk, GitHub branch protection limits (see research-notes.md) | 1.33 |
| Wed 30 Sep | 4:00–5:00 PM | Work plan task: repo structure and task board | 1 |
| Thu 1 Oct | 11:00 AM–1:00 PM | Supervisor meeting #1: cleared doubts with Shikfa, IRB, which databases, plan for next week | 2 |
| **Total** | | | **6 h 20 m** |

## Week 7 (4 – 8 Oct)
Task: PR1 work-distribution section + Gantt chart. Update task board.
SLR: wrote SLR Protocol v2 → v3 and set up `research/slr/` + each member's `slr/` folder. v3 role (Pair 3, screener 2): protocol owner (collect changes by Sat 10 Oct); confirm Khalid's Scopus search check + count. Checklist: [slr/TASKS.md](slr/TASKS.md)
*Draft – check every line, fill in the [ ] parts, delete anything you didn't do, then commit from your own account.*
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 4 Oct | 03:25–03:45 (start may be earlier) | Set up the GitHub repo and task board | 0.33 |
| Sun 4 Oct | [start: fill in]–17:45 | Added the system architecture diagram to my research notes | [fill in] |
| [fill in: Sun 4–Wed 7 Oct] | [fill in] | Researched IRB requirements for the project with Hassan | [fill in] |
| Thu 8 Oct | 11:00–13:00 | Weekly supervisor/team meeting [confirm attendance] | 2 |
| Fri 9 Oct | 18:36–20:06 (start may be earlier) | Wrote SLR Protocol v3 and set up the SLR files in the repo; made and fixed the Gantt chart; checked the project plan | 1.5 |
| Sat 10 Oct | [time: fill in] | Tried the ACM search (no UDST access) and decided to use PubMed instead | [fill in] |
| Sat 10 Oct | [time: fill in] | Re-ran the Scopus search check and search and confirmed Khalid's count (1,017) | [fill in] |
| Sat 10 Oct | 20:07–20:46 (start may be earlier) | Wrote the protocol v4 changes and updated the repo with the search and de-duplication results | 0.65 |
| [fill in: Fri 9 or Sat 10 Oct] | [fill in] | Collected the team's replies on Protocol v3 | [fill in] |
| [fill in: Fri 9–Sun 11 Oct] | [fill in] | Progress Report 1: work-distribution section and Gantt chart | [fill in] |
| Sun 11 Oct | 16:00–18:00 | Team work session on Progress Report 1 [confirm after the session] | 2 |
| **Total** | | | **6 h 29 m** |

## Week 8 (11 – 15 Oct)
No logbook (mid-term) – keep notes.
SLR: screen all of Set 3 (Screening Log, column H) independently of Khalid; tie-breaker for Pair 1.
| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | | |
| **Total** | | | |

## Week 9 (18 – 22 Oct)
Semester break – no logbook.

## Week 10 (25 – 29 Oct) – as submitted

Copied word for word from the submitted logbook PDF (COMP4101_Practicum_Logbook_60307149_No.3_Week_10.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 25 Oct | 4:00–6:00 PM | Our team met to plan the week and share out the tasks. Mine were the architecture diagram, the API contract, the protocol document and the repository. | 2 |
| Mon 26 Oct | 5:00–8:00 PM | I drew the system design (browser, Node API, Python FHE service) and wrote a first draft of the API contract. | 3 |
| Thu 29 Oct | 9:00–11:00 PM | Saif and I worked together because we missed the weekly meeting with our supervisor. We each did our own tasks. I read the SLR protocol (version 1.0) and worked on the screening criteria. I checked it with the PRISMA sheet, which has 1,044 records to screen after 482 duplicates were removed. My pair’s set is 348 records. I found that the protocol has 5 exclusion codes (E1- E5) but the PRISMA sheet has 6 (E1-E6), so I need to fix this with Naif. I also updated the API contract with Saif’s details. It has 2 endpoints and 7 error codes. | 2 |
| **Total** | | | **7 h** |

## Week 11 (1 – 5 Nov) – as submitted

Copied word for word from the submitted logbook PDF (COMP4101_Practicum_Logbook_60307149_No.4_Week_11.pdf); only line breaks were changed. Do not edit – it is the record of what was handed in.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| Sun 1 Nov | 4:00–6:00 PM | Each Member was assigned to read 6 papers. So, I read the 1st paper from my assigned list: Sheu et al. (2023), AutoPro-RHC, is about a system that lets hospitals check a patient’s heart health without seeing their data. The patient’s data stays encrypted with TFHE the whole time, and the hospital servers run machine learning models (SVC, LR, XGBoost and decision tree) on it through Concrete-ML. The authors tested it on the UCI heart disease data from Cleveland, Hungary and V.A. SVC got 88% accuracy and LR got 86%. - [Include. Passes Q1–Q3] | 2 |
| Mon 2 Nov | 5:00–6:30 PM | I read the 2nd Paper: Nisha et al. (2023), Blockchain + HE + voting classifier in IIoT, is about keeping data private in Industrial IoT systems, meaning machines and sensors in factories and industry. It combines blockchain, homomorphic encryption, and a voting classifier, which is a group of machine learning models that vote on the answer. I couldn’t find the abstract anywhere, and nothing we found shows it uses health or patient data. - [Maybe, leaning Exclude E2] | 1.5 |
| Wed 4 Nov | 7:00–10:00 PM | I read the 3rd and 4th Paper: Dang et al. (2023), TrustFedHealth, is about training a heart disease prediction model across many devices without collecting the patients’ data in one place, which is called federated learning. Each device trains on its own data and sends back only model updates, and homomorphic encryption keeps those updates locked while the server combines them. Blockchain keeps a record of who sent which update, and edge computing makes communication faster. The authors tested it on the MIT-BIH ECG heart data. - [Include at stage 1]<br><br>Cenitta et al. (2025), XAI + HE for cloud ECG, is about checking a patient’s ECG for heart disease in the cloud while the signal stays encrypted the whole time. It uses CKKS encryption and a deep learning model called a CNN, and a method called SHAP shows doctors why the model made its decision. On the MIT-BIH ECG data, the model got 94.2% accuracy on normal data and 93.4% on encrypted data. Each encrypted prediction took about 420 ms, which is less than half a second. - [Include. Passes Q1–Q3] | 3 |
| Thu 5 Nov | 4:00–5:15 PM and 9:00–10:30 PM | I read the 5th and 6th Paper: IC-ICN 2020 (conference review) is not a real research paper. It is a Scopus record for the conference book itself, which collects 27 general papers on AI and networking. It has no authors, no abstract and no method of its own. - [Exclude as it is just a review]<br><br>Sinciya et al. (2025), Heartify, is about a mobile app that checks for early signs of heart disease using data from wearable devices like smartwatches. The model is trained with federated learning, so each device trains on its own data and only shares model updates. The authors used two ways of combining the updates, FedAvg and FedMA. FedMA did best with 85.32% accuracy. The paper does not use any encryption. - [Exclude E1. Federated learning only, no HE] | 2.75 |
| **Total** | | | **9 h 15 m** |

## Week 12 (8 – 12 Nov)
Logbook due Sun 15 Nov. **Write these rows yourself, the same day you work** – the course treats AI-written logbook entries as academic dishonesty. The prompts below are only reminders of what to record (from your README's next steps); delete them as you fill in real entries.

| Day / Date | Time | What I did | Hours |
|---|---|---|---|
| | | API contract v2 review – error codes kept/renamed | |
| | | Gantt PNG updated for Practicum → Capstone 2 | |
| | | Branch protection + CI turned on? | |
| | | Extraction rows verified (P024, P006, P026); TrustFedHealth full text read? | |
| | | Final report sections drafted (architecture, Gantt, challenges); RQ2 with Khalid | |
| **Total** | | | |
