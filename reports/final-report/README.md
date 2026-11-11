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
