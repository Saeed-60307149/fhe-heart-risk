#!/usr/bin/env python3
"""Collect code/results/<dataset>/*.json into code/results/README.md (tables for the
final report: baseline metrics, sigmoid validation, pilot cost per layout)."""
import json
import os
from datetime import date

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results"))


def load(ds, name):
    p = os.path.join(RES, ds, name)
    return json.load(open(p)) if os.path.exists(p) else None


def f(x, d=3):
    return "–" if x is None else f"{x:.{d}f}"


lines = [f"# Results (generated {date.today().isoformat()} by `code/scripts/summarise_results.py`)", "",
         "Do not edit by hand: re-run `bash code/scripts/run_pilot.sh`. Raw JSON is next to this file.", ""]
datasets = sorted(d for d in os.listdir(RES) if os.path.isdir(os.path.join(RES, d))) if os.path.isdir(RES) else []

lines += ["## Plaintext baseline (logistic regression, fixed stratified split, seed 42)", "",
          "| Dataset | Rows | Test rows | Accuracy | Precision | Recall | F1 | ROC-AUC |", "|---|---|---|---|---|---|---|---|"]
for ds in datasets:
    b = load(ds, "baseline_metrics.json")
    if b:
        t = b["test"]
        lines.append(f"| {ds} | {b['rows_after_cleaning']} | {b['test_rows']} | {f(t['accuracy'])} | "
                     f"{f(t['precision'])} | {f(t['recall'])} | {f(t['f1'])} | {f(t['roc_auc'])} |")

lines += ["", "## Polynomial sigmoid (test split)", "",
          "| Dataset | Polynomial | MAE vs sigmoid | Decision match | Accuracy | Pass (≥90%, RQ-A) | ≥95% (expected) |", "|---|---|---|---|---|---|---|"]
for ds in datasets:
    s = load(ds, "sigmoid_validation.json")
    if s:
        for c in s["candidates"]:
            lines.append(f"| {ds} | {c['name']} | {f(c['mae_vs_sigmoid_test'], 4)} | "
                         f"{f(c['decision_match_vs_sigmoid'])} | {f(c['metrics']['accuracy'])} | {c.get('pass_rq_a_90', '')} | {c.get('meets_expected_95', '')} |")

lines += ["", "## Encrypted inference pilot (CKKS N=16384, scale 2^40, 128-bit)", "",
          "| Dataset | Layout | Patients | Enc ms | Inference ms | Dec ms | Ciphertext MB / patient | Eval keys MB | Plain acc | Enc acc | Decision match |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
for ds in datasets:
    for layout in ("packed", "per_feature"):
        p = load(ds, f"pilot_{layout}.json")
        if not p:
            continue
        c = p["cost"]
        ct = c.get("ciphertext_per_patient_MB", c.get("ciphertexts_per_patient_MB"))
        keys = c["galois_keys_MB"] if layout == "packed" else c["relin_keys_MB"]
        lines.append(f"| {ds} | {layout} | {p['patients']} | {f(c['encrypt_ms']['mean'], 1)} | "
                     f"{f(c['inference_ms']['mean'], 1)} | {f(c['decrypt_ms']['mean'], 1)} | {f(ct, 2)} | "
                     f"{f(keys, 1)} ({'Galois' if layout == 'packed' else 'relin'}) | "
                     f"{f(p['accuracy']['plain_sigmoid']['accuracy'])} | {f(p['accuracy']['encrypted_poly']['accuracy'])} | "
                     f"{f(p['decision_match_encrypted_vs_plain_sigmoid'])} |")
lines += ["", "Times are means over the test patients on the machine recorded in each JSON file (`environment`).", ""]
os.makedirs(RES, exist_ok=True)
open(os.path.join(RES, "README.md"), "w").write("\n".join(lines))
print("wrote", os.path.join(RES, "README.md"))
