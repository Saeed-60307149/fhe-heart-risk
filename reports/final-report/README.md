# Final report (due Thu 26 Nov 2026)

Owner: Naif (compiles) · each section owner drafts in Week 12 (work plan). This page only maps
each section to its owner and to the files in this repo that hold the evidence – the text is
written by the owners.

| Section | Owner (work plan Wk 12) | Evidence in the repo |
|---|---|---|
| Introduction, scope, feasibility | Naif | PR2 §A; `planning/decision-log.md` |
| Background: FHE schemes (CKKS vs BFV/BGV/TFHE) | Saif | `research/reading-list.md`; extraction form RQ1 |
| SLR method (protocol v3 → v5) | Naif, Abdullah | `research/slr/protocol.md`, `SLR_Protocol_v4_changes.md`, `SLR_Protocol_v5_changes.md` |
| SLR results: PRISMA + synthesis RQ1–RQ4 | Hassan (PRISMA); pairs for RQs | `research/slr/refined-2026-10-29/prisma-flow.md`, `screening-decisions.csv`, extraction form |
| Data + baseline | Sarim | `code/data/DATA_DICTIONARY.md`; `code/results/<ds>/baseline_metrics.json` |
| Sigmoid approximation | Khalid | `code/results/<ds>/sigmoid_validation.json`, `sigmoid_vs_poly.png` |
| Cryptographic method + pilot results | Saif | `code/results/README.md`; `design/pilot-workflow.md`; `design/benchmark-plan.md` |
| Architecture, API, threat model | Abdullah, Naif | `design/architecture.md`, `design/api-contract.md`, `design/threat-model.md`, `design/diagrams/` |
| Gantt (Practicum → Capstone 2), challenges | Abdullah | `planning/gantt.md`, PR2 §C |
| Data/code availability, references, formatting | Hassan | this repo; `research/ethics-data-note.md` |

Before submitting: apply the PR2 errata ([../progress-report-2/README.md](../progress-report-2/README.md)),
re-run `python research/slr/scripts/prisma_counts.py --write` and `bash code/scripts/run_pilot.sh`,
and quote the commit hash of the run in the report.

## Defense report files

> **The two PDFs below are not in this repository.** It is publicly visible and they carry student ID numbers. The team
> keeps them locally and on D2L; add them with `git add -f` only after the repository is made private.

| File | What |
|---|---|
| `Defense_Report_corrected_reference.pdf` | **The repo's reference (decision #26).** Corrected report; five student IDs are still blank in this copy |
| `Abdullatif_Shikfa_2026_495_Practicum_ProposalDefenseReport.pdf` | The submitted report, kept unchanged as a record |

### How the submitted PDF differs from the reference (tell the supervisor)

| Topic | Submitted PDF | Reference |
|---|---|---|
| Literature review (C.4) | IEEE, PubMed, Scopus; 1,526 / 1,044; 36 included | Refined search: 43 records, 34 after de-duplication + 1 by hand; 31 screened, 14 included, 4 unscreened. **The records support the reference figures; no record of 36 was found** |
| Haq in the search (F.4) | Did not appear | Not in the refined search; it **is** in the superseded 10 Oct broad Scopus export (the reference should say this too) |
| RQ-A pass mark | 100% | At least 90% |
| Layout | Both compared, delivered layout chosen from results | One ciphertext per feature; packed for comparison only |

### After the reports

The benchmarks planned in the reports were run on 27 Nov 2026, **after** both report versions, so neither report
contains these results: [`code/results/benchmarks/`](../../code/results/benchmarks/README.md).
The corrected reference also still says, in F.4 and C.4, that the search missed Haq et al.; that is true of the refined
search only (it is in the superseded 10 Oct broad Scopus export).
