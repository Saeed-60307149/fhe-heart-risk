# Week 13 plan – finishing the design (15 – 21 Nov 2026)

Source: Architecture v1.0 and Threat Model v1.0 (submitted 15 Nov) and their open items in
[`design/threat-model.md`](../design/threat-model.md) (column "Status in `code/`") and
[`design/architecture.md`](../design/architecture.md). Everyone works to the same two sessions.

## Common sessions (whole team)

| Session | Date | Time | Hours |
|---|---|---|---|
| 1 | Thursday 19 Nov 2026 | 8:00 – 11:00 PM | 3 |
| 2 | Saturday 21 Nov 2026 | 7:00 – 10:00 PM | 3 |

That is 6 hours per person, the weekly logbook minimum. Each person logs only the time they actually
worked, in their own words, in `members/<name>/logbook-notes.md`. Nobody's logbook is written for them.

## Threat model – Saif and Naif

| Who | Tasks | Done when |
|---|---|---|
| **Naif** (owner, documentation + access and metadata controls) | Review T1–T15 wording against the submitted PDF. Add the data-flow diagram with trust boundaries (reuse [`design/diagrams/architecture.md`](../design/diagrams/architecture.md)). Decide whether T10 needs decision-only output (open point in section 8). **Test plan 2** (capture traffic, memory and logs: no plain features or score; T1, T2, T5, T12). **Test plan 6** (authentication; add and test the CORS allow-list; T14). Copy the final table into the final report (Security) | Test results in the status column; diagram added; T10 decision logged |
| **Saif** (crypto and input-handling controls) | **Test plan 1** (server never loads a context with a secret key) re-run, **3** (oversized, malformed, wrong-parameter ciphertexts; add fuzz cases; T7, T8, T9), **4** (rate-limit and load test; T8, T10), **7** (plain-vs-encrypted decision match ≥ 90% on both datasets; T15). Add the client-side score range check (T6). Container with limited rights for the service (T9) | Tests pass or failures are written up; range check merged; status column updated |
| **Both** | **Test plan 5** (CSP, SRI and dependency audit of the front end and lockfiles; T3, T4, T13): Saif runs the audit and lockfile hashes, Naif adds SRI/hashed bundles to the front end. Update the "Status in `code/`" column and the open list in decision #19 | Column matches the code |

## Architecture – Sarim, Khalid, Hassan, Abdullah

| Who | Tasks | Done when |
|---|---|---|
| **Abdullah** (owner) | Replace the Week 10 PNG with a figure matching v1.0 (browser / gateway / FHE service / model files, trust boundary). Make `/predict` vs `/api/predict` naming consistent across the PDF text, `api-contract.md` and `openapi.yaml`. Decide key reuse (IndexedDB vs per-load keys) with Naif's T3 view. Final read of both documents | Figure and contract consistent; key-reuse decision logged |
| **Hassan** (benchmarks) | Measure the two upload reductions the architecture promises: lower polynomial degree (N = 8192) and ciphertext compression (zstd), for size and timing, per-feature layout, Cleveland. Fill [`design/benchmark-plan.md`](../design/benchmark-plan.md) with the results | Size and timing table for N = 16384 vs 8192, with and without compression |
| **Khalid** (sigmoid / model) | Check accuracy and decision match at N = 8192 (smaller modulus chain) and with the logit-only output; settle which sigmoid error figure the report uses (0.031 PR2 vs 0.0356 from the 11 Nov run) and how the interval was chosen | One number, one method sentence, for the report |
| **Sarim** (baseline + Edinburgh) | Run and check the Edinburgh MI pilot end to end (9 features, about 11 MB request) and record the numbers next to Cleveland. Check the plaintext baseline app step of the build order (front end + gateway without FHE) against `code/` | Edinburgh row in the results table; build-order step 1 confirmed or gap listed |

## Notes

- The threat model's open items come straight from its "Status in `code/`" column; if a test fails,
  write the failure up rather than changing a number.
- Nothing here changes the pinned versions (node-seal 7.0.0, TenSEAL 0.3.16).
- The final report draft goes to Dr. Shikfa by Thu 19 Nov (see `members/naif/README.md`); the
  Thursday evening session is for the work above, not the report merge.
