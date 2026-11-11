# Progress Report 2 (submitted Sun 8 Nov 2026)

| File | What |
|---|---|
| `Practicum_Progress_Report_2_submitted.pdf` | The submitted PDF (Weeks 8–11) |
| `Progress_Report_2_draft.docx` | Editable draft (earlier version: some table numbers differ from the PDF) |

Reporting period Week 8 – Week 11 (up to Sat 7 Nov). Compiled by Naif.

## Errata – fix these in the final report

Found on 11 Nov while turning PR2 into the repo record. None changes the conclusions.

| # | Where | Issue | Fix (status 11 Nov) |
|---|---|---|---|
| 1 | §A.2 objective 3, RQ-A vs §B.1, §D | Decision-match target is **90%** in RQ-A and objective 3 but **95%** in the ongoing tasks and expected results | **Resolved (#16):** pass = 90% (RQ-A); 95% reported as the expected result. Word it that way in the final report |
| 2 | §B Table 2, Table 3 | "3 records listed twice explain 34 → 31 screened". In fact 4 sheet records were never assigned (P002 Dziri 2025, P011 Janagama 2026, P023 ICIC 2019, P029 Dakhare 2024) and Kim et al. 2018 (Table 3 #7) is not in the refined results | **Resolved (#14):** Kim = 1 other source; the 4 records assigned for Week 12. Use `prisma-flow.md` numbers |
| 3 | Figure 1 / Table 2 | All 11 exclusions shown at the screening stage; 5 of them were made after reading the full text | PRISMA 2020: put those 5 in "Reports excluded" with reasons |
| 4 | Table 3 #2 | TrustFedHealth counted as included but only the abstract was checked | Read the full text before counting it as included |
| 5 | §A.4 Tools | "private repository" – GitHub serves the repo publicly | Make it private, or change the wording |
| 6 | §A.4 Part 3 vs §A.3 | Part 3 says all 13 features are packed into one ciphertext; the round trip and the prototype use one ciphertext per feature | **Resolved (#15):** one ciphertext per feature; describe packed only as the measured comparison |
| 7 | Table 5 | "Public context 7.7 MB" is larger than "with secret key 1.9 MB", which reads like a typo. Checked 11 Nov: when the secret key is saved TenSEAL leaves out the relinearization keys (it regenerates them from the secret key), so 1.9 MB = secret key 0.63 + public key 1.26 MB, while the public context = public key 1.26 + relin keys 6.28 MB | Say what each size contains |
| 8 | Header/footer | "Version 2, 4 October 2026" is the template version, not the report date | Leave, or note it is the template version |
