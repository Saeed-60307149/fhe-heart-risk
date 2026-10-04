# fhe-heart-risk
**Privacy-Preserving Machine Learning for Healthcare Risk Prediction**
Heart disease risk prediction on encrypted patient data using Fully Homomorphic Encryption (CKKS / TenSEAL).

COMP4101 Practicum, Fall 2026 → Capstone 2 · Supervisor: **Shikfa** · Team leader: **Naif**

## The idea in one line
Patient data is encrypted on the client, the server runs the model on the encrypted data, and only the patient can decrypt the result. The server never sees the data or holds the secret key.

```
[Patient client] --encrypt--> [Backend API] --> [FHE-ML service] --encrypted score--> [Patient client] --decrypt--> risk
```

## Two phases, one repo
| Phase | When | What lives here |
|---|---|---|
| **1. Research** (now) | Practicum, Fall 2026 | `meetings/`, `members/`, `research/`, `design/`, `planning/`, `reports/` |
| **2. Build** (later) | Capstone 2 | `code/` – frontend, backend, FHE-ML service, data scripts |

## Where things go
| Folder | What it is | Who edits |
|---|---|---|
| [`meetings/`](meetings/) | **Joint meeting notes** – every team + supervisor meeting | Scribe / anyone |
| [`members/`](members/) | **One folder per person** – your tasks, research notes, logbook notes | Only the owner |
| [`research/`](research/) | Shared research: reading list, SLR protocol, search log, PRISMA | Everyone |
| [`design/`](design/) | Architecture, API contract, diagrams | Abdullah (+ review) |
| [`planning/`](planning/) | Work plan, Gantt, decision log, task board link | Naif, Abdullah |
| [`reports/`](reports/) | Progress reports, final report, slides | Everyone, Naif compiles |
| [`code/`](code/) | Semester 2 implementation (empty for now) | Later |

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
