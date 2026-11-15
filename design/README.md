# Design
Owner: Abdullah Dar · reviewed by the team · Semester 1 = paper design + pilots; Capstone 2 builds on it.

| File | What | Week | Owner |
|---|---|---|---|
| [`architecture.md`](architecture.md) | Parts, request flow, parameters, layout, who holds which key, decisions, open items (**v1.0 final, 15 Nov**) | Wk 10 → 15 Nov | Abdullah |
| [`api-contract.md`](api-contract.md) | Endpoints, request/response, 8 error codes (v2) | Wk 10 → 11 Nov | Abdullah |
| [`openapi.yaml`](openapi.yaml) | Same contract, machine-readable (OpenAPI 3.1) | 11 Nov | Abdullah |
| [`threat-model.md`](threat-model.md) | Assets S1–S6, adversaries A1–A5, threats T1–T15, residual risks, security test plan, status in `code/` (**v1.0 final, 15 Nov**) | Wk 10 → 15 Nov | Naif |
| [`benchmark-plan.md`](benchmark-plan.md) | What is measured for RQ-A/RQ-B and how | Wk 10–11 | Hassan |
| [`pilot-workflow.md`](pilot-workflow.md) | Pilot steps and where each PR2 number comes from | Wk 11 | Abdullah |
| [`diagrams/architecture.md`](diagrams/architecture.md) | Mermaid: architecture, request sequence, pilot workflow | 11 Nov | Abdullah |

Contract tests: `code/backend/test/app.test.js`, `code/fhe-ml-service/tests/test_api.py`.
