# fhe-heart-risk
**Privacy-Preserving Machine Learning for Healthcare Risk Prediction**
Heart disease risk prediction on encrypted patient data using Fully Homomorphic Encryption (CKKS / TenSEAL).

COMP4101 Practicum, Fall 2026 → Capstone 2 · Supervisor: **Shikfa** · Team leader: **Naif**

## The idea in one line
Patient data is encrypted on the client, the server runs the model on the encrypted data, and only the patient can decrypt the result. The server never sees the data or holds the secret key.

```
[Patient browser: node-seal] --ciphertext--> [Node API] --> [FHE-ML service: TenSEAL] --encrypted score--> [browser] --decrypt--> risk
```

## Where we are (11 Nov 2026, after Progress Report 2)
- **SLR:** refined search of 29 Oct (Protocol v5) – 43 identified, 9 duplicates, 34 to screen + 1 other
  source; PR2: 31 screened (11 excluded, 12 included, 2 borderline, 6 awaiting full text). Since PR2 the 2
  borderline (Paillier) records are included as a partial-HE subgroup → 14 included; 4 records assigned for Week 12.
  → [`research/slr/refined-2026-10-29/`](research/slr/refined-2026-10-29/)
- **Pilot:** logistic regression on CKKS-encrypted UCI Cleveland features, same accuracy as plaintext
  (0.853, AUC 0.947), ≈13 / 88 / 4 ms encrypt / infer / decrypt; node-seal → TenSEAL → node-seal round
  trip exact. Edinburgh MI and both ciphertext layouts are scripted. → [`code/pilots/`](code/pilots/)
- **Prototype skeleton (Capstone 2 head start):** browser encryption, Node API, FHE service, Plan B
  client, 44 tests, CI. → [`code/`](code/)
- **Decisions closed 11 Nov:** one ciphertext per feature (#15), pass = 90% decision match with 95%
  reported as the expected result (#16), partial HE included as a subgroup (#17), API contract v2
  final (#18) → [`planning/decision-log.md`](planning/decision-log.md). PR2 errata →
  [`reports/progress-report-2/`](reports/progress-report-2/).

## Two phases, one repo
| Phase | When | What lives here |
|---|---|---|
| **1. Research + pilots** (now) | Practicum, Fall 2026 | `meetings/`, `members/`, `research/`, `design/`, `planning/`, `reports/`, `code/pilots/` |
| **2. Build** | Capstone 2 | `code/` – frontend, backend, FHE-ML service, Plan B client (skeleton in place) |

## Where things go
| Folder | What it is | Who edits |
|---|---|---|
| [`meetings/`](meetings/) | **Joint meeting notes** – every team + supervisor meeting | Scribe / anyone |
| [`members/`](members/) | **One folder per person** – your tasks, research notes, logbook notes | Only the owner |
| [`research/`](research/) | Shared research: reading list, SLR protocol, search log, PRISMA | Everyone |
| [`design/`](design/) | Architecture, API contract + OpenAPI, threat model, benchmark plan, diagrams | Abdullah, Naif, Hassan |
| [`planning/`](planning/) | Work plan, Gantt, decision log, task board link | Naif, Abdullah |
| [`reports/`](reports/) | Progress reports, final report, slides | Everyone, Naif compiles |
| [`code/`](code/) | Pilots, results, prototype skeleton, tests ([how to run](code/README.md)) | Saif, Sarim, Khalid, Hassan, Abdullah |

## Team
| Member | Program | Focus | Folder |
|---|---|---|---|
| Naif (Leader) | Cyber | SLR, scheme choice, methodology, threat model, reports | [naif](members/naif/) |
| Saif | Cyber | TenSEAL pilot, node-seal compatibility, key management | [saif](members/saif/) |
| Sarim | AI | Dataset, preprocessing, baseline model | [sarim](members/sarim/) |
| Khalid | AI | Polynomial sigmoid approximation, evaluation | [khalid](members/khalid/) |
| Abdullah Dar | Software Eng. | Repo/board, architecture + API, workflow diagram, Gantt | [abdullah-dar](members/abdullah-dar/) |
| Hassan Zahid | IT | Environment, PRISMA, ethics note, benchmarking, formatting | [hassan-zahid](members/hassan-zahid/) |

## Key dates
| Item | Due |
|---|---|
| Logbook Wk 6 | Sun 4 Oct, 11:59 PM |
| Progress Report 1 + logbook Wk 7 | Sun 11 Oct |
| Logbook Wk 10 | Sun 1 Nov |
| Progress Report 2 + logbook Wk 11 | Sun 8 Nov |
| Logbook Wk 12 | Sun 15 Nov |
| Logbook Wk 13 | Sun 22 Nov |
| Final report | Thu 26 Nov |
| Defence | Week 15 (date on D2L) |

Supervisor meeting: **Thursdays 11:00**. New here? Read [CONTRIBUTING.md](CONTRIBUTING.md).
