# Joint Meeting Notes
All team and supervisor meetings in one place. **Newest at the top.**
Scribe fills this in during the meeting; anyone can fix or add after.
Copy the template from `meetings/TEMPLATE.md` for each new meeting.

---

## Week 11 · Sun 1 Nov 2026 · Team meeting
**Time:** 4:00 – 6:00 PM · **With:** team only
**Attended (from logbooks):** Naif, Saeed Abdullah Dar *(others: confirm)*
**Scribe:**

### Discussed / decided
- Naif divided the 34 refined-search records: each member reads and screens 5–6 (assignment in
  `research/slr/refined-2026-10-29/README.md`).
- Screening 1–5 Nov; every decision logged in the PRISMA sheet; borderline records discussed by all.

### Action items
| Who | What | By |
|---|---|---|
| All | Screen assigned records, log decision + reason | Thu 5 Nov |
| Naif | Compile Progress Report 2 | Sun 8 Nov |

---

## Week 10 · Thu 29 Oct 2026 · Supervisor meeting
**Time:** about 9:00/11:00 AM – 1:00 PM (logbooks differ) · **With:** Dr. Abdullatif Shikfa
**Attended (from logbooks):** Naif, Owais Khalid *(others: confirm)*. **Absent:** Saif and Saeed Abdullah Dar
(worked together that evening instead – their logbooks).
**Scribe:**

### Discussed
- More than 1,000 SLR records were left after de-duplication and most were off-topic.
- Techniques to narrow the pool.

### Decisions
- Focus on finishing the SLR first.
- Make the search strings more exact (all three concepts required) → Protocol v5, decision #9.

### Action items
| Who | What | By |
|---|---|---|
| Naif | Re-run IEEE Xplore and Scopus with the new strings | 6 Nov |
| Saif / Abdullah | Re-run IEEE / Scopus to confirm counts | 6 Nov |
| Naif | Divide the new records across the team | Sun 1 Nov |

---

## Week 10 · Sun 25 Oct 2026 · Team meeting
**Time:** 4:00 – 6:00 PM · **With:** team only
**Attended (from logbooks):** Naif, Saif, Saeed Abdullah Dar, Owais Khalid *(others: confirm)*
**Scribe:**

### Discussed / decided
- Week 10 plan. Pair 1 (Naif, Saif): encrypted round-trip pilot (node-seal 7.0.0 + TenSEAL 0.3.16),
  ciphertext/key sizes for the cost tables, IEEE string check, technical facts for the threat model.
- Abdullah: architecture diagram, API contract, protocol document, repository.
- SLR: 1,044 records to screen; selection must follow the documented protocol (not AI ranking);
  four review questions; PRISMA record keeping.

---

## Week 6 · Thu 1 Oct 2026 · Supervisor meeting #1
**Time:** 11:00 AM – 1:00 PM · **With:** Shikfa (supervisor)
**Attended:** Naif, Saif, Sarim, Khalid, Abdullah Dar, Hassan Zahid *(fix if anyone was absent)*
**Scribe:**

### Discussed
- Went over the project with the supervisor: client-side encryption, prediction on encrypted data, patient keeps the key.
- Cleared doubts about the tech (FHE, CKKS, TenSEAL) and how to plan the full project.
- IRB / ethics approval: do we need it if we only use the public UCI dataset and no real patients?
- Which databases to use for the literature review.

### Decisions
- IRB: *(write what was decided)*
- Databases: *(e.g. IEEE Xplore, ACM DL, Scopus – confirm)*
-

### Action items (until next meeting)
| Who | What | By |
|---|---|---|
| All | Week 7 tasks from the work plan | Thu 8 Oct |
| | | |

---

## Week 6 · Sun 27 Sep 2026 · Team meeting #1
**Time:** 4:00 – 6:00 PM · **With:** team only
**Attended:** Naif, Saif, Sarim, Khalid, Abdullah Dar, Hassan Zahid *(fix if anyone was absent)*
**Scribe:**

### Discussed
- What the project is about and what problem it solves (server sees no plaintext patient data).
- Our doubts and confusions about FHE, CKKS, TenSEAL and the overall tech.
- How to plan the whole project from start to finish.

### Decisions
- Naif assigned Week 6 tasks and research topics to each member (see `planning/` and each `members/` folder).
-

### Action items
| Who | What | By |
|---|---|---|
| Naif | Team agreement + scope lists to Shikfa; 1 review + 2 review questions | Thu 1 Oct |
| Saif | 2–3 FHE / PPML surveys | Thu 1 Oct |
| Sarim | Heart disease ML studies + UCI licence | Thu 1 Oct |
| Khalid | Papers on polynomial sigmoid approximation | Thu 1 Oct |
| Abdullah Dar | GitHub repo + task board, invite everyone | Thu 1 Oct |
| Hassan Zahid | Library/RefWorks access, shared folder, TenSEAL install test | Thu 1 Oct |
