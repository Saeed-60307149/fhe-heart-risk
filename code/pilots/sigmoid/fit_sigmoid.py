#!/usr/bin/env python3
"""Polynomial sigmoid: fit and validate in plaintext (runbook steps 8-9; PR2 objective 3).

Fits a least-squares cubic over an interval chosen from the TRAINING logits, then on
the TEST split compares real sigmoid vs polynomial: MAE, accuracy/F1/AUC, and the
decision match (share of patients with the same low/high-risk decision).
Pass/fail (decision #16): pass when decision match >= 90% (RQ-A, objective 3);
whether the 95% expected result (PR2 section D) is reached is reported next to it.

Also scores the two published cubics for comparison. Writes the chosen polynomial
into model_weights_<dataset>.json so the FHE service can use it.

Usage (from code/, after train_baseline.py):
    python pilots/sigmoid/fit_sigmoid.py
    python pilots/sigmoid/fit_sigmoid.py --dataset cleveland --interval -8 8
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import pilot_paths as PP  # noqa: E402

from fhe_heart import data as D  # noqa: E402
from fhe_heart import metrics as M  # noqa: E402
from fhe_heart import model as ML  # noqa: E402
from fhe_heart import sigmoid as S  # noqa: E402


def evaluate(name, coeffs, interval, z_te, y_te, thr):
    p_true = M.sigmoid(z_te)
    p_poly = S.poly_eval(coeffs, z_te)
    met = M.classification_metrics(y_te, S.clipped(p_poly), thr)
    return {
        "name": name, "coeffs_ascending": [float(c) for c in coeffs],
        "interval": [float(interval[0]), float(interval[1])] if interval else None,
        "mae_vs_sigmoid_test": M.mae(p_true, p_poly),
        "max_abs_err_test": float(np.max(np.abs(p_true - p_poly))),
        "decision_match_vs_sigmoid": M.decision_match(p_true, p_poly, thr),
        "test_logits_outside_interval": (int(np.sum((z_te < interval[0]) | (z_te > interval[1])))
                                         if interval else None),
        "metrics": met,
    }


def plot(path, candidates, z_lo, z_hi, z_te):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    z = np.linspace(z_lo, z_hi, 800)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(z, M.sigmoid(z), color="#222222", lw=2.4, label="sigmoid")
    styles = ["-", "--", ":"]
    for c, st in zip(candidates, styles):
        ax.plot(z, S.poly_eval(c["coeffs_ascending"], z), st, lw=1.6, label=c["name"])
    ax.plot(z_te, np.full_like(z_te, -0.08), "|", color="#888888", ms=8, label="test logits")
    ax.axhline(0.5, color="#bbbbbb", lw=0.8)
    ax.set_ylim(-0.15, 1.15)
    ax.set_xlabel("logit z = w·x + b")
    ax.set_ylabel("output")
    ax.set_title("Sigmoid vs degree-3 polynomial approximations")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def run(dataset, interval, target):
    wpath = PP.model_path(dataset)
    doc = ML.load_weights(wpath)
    split = D.split_and_scale(D.load_dataset(dataset, PP.RAW_DIR))
    w, b, thr = np.array(doc["weights"]), doc["bias"], doc["threshold"]
    z_tr, z_te = split.X_train @ w + b, split.X_test @ w + b
    if interval is None:
        interval = S.interval_from_logits(z_tr)
    fitted = S.fit_least_squares(interval, degree=3, odd_only=True)
    cands = [
        evaluate(f"least-squares cubic on [{interval[0]:.1f}, {interval[1]:.1f}]",
                 fitted, interval, z_te, split.y_test, thr),
        evaluate("Kim et al. 2018 cubic [-8, 8]", S.KIM_2018_DEG3, (-8, 8), z_te, split.y_test, thr),
        evaluate("runbook cubic [-5, 5]", S.RUNBOOK_DEG3, (-5, 5), z_te, split.y_test, thr),
    ]
    baseline = M.classification_metrics(split.y_test, M.sigmoid(z_te), thr)
    chosen = cands[0]
    chosen["pass"] = chosen["decision_match_vs_sigmoid"] >= target
    chosen["pass_rq_a_90"] = chosen["decision_match_vs_sigmoid"] >= 0.90
    chosen["meets_expected_95"] = chosen["decision_match_vs_sigmoid"] >= 0.95
    out = {"dataset": dataset, "target_decision_match": target, "baseline_test": baseline,
           "chosen": chosen["name"], "candidates": cands}
    rdir = PP.results_dir(dataset)
    out["plot"] = plot(os.path.join(rdir, "sigmoid_vs_poly.png"), cands,
                       min(interval[0], z_te.min()) - 1, max(interval[1], z_te.max()) + 1, z_te)
    if out["plot"]:
        out["plot"] = os.path.relpath(out["plot"], PP.CODE_DIR)
    with open(os.path.join(rdir, "sigmoid_validation.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    doc["sigmoid_poly"] = {"coeffs_ascending": chosen["coeffs_ascending"],
                           "interval": chosen["interval"], "method": "least squares, odd cubic"}
    with open(wpath, "w") as fh:
        json.dump(doc, fh, indent=2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(D.LOADERS), action="append")
    ap.add_argument("--interval", nargs=2, type=float, metavar=("LO", "HI"))
    ap.add_argument("--target", type=float, default=0.90,
                    help="pass threshold for decision match (RQ-A: 0.90)")
    args = ap.parse_args()
    for name in args.dataset or sorted(D.LOADERS):
        r = run(name, tuple(args.interval) if args.interval else None, args.target)
        for c in r["candidates"]:
            print(f"{name}: {c['name']}: MAE={c['mae_vs_sigmoid_test']:.4f} "
                  f"match={c['decision_match_vs_sigmoid']:.3f} acc={c['metrics']['accuracy']:.3f}"
                  + (f"  PASS(90%)={c['pass_rq_a_90']} expected95={c['meets_expected_95']}" if "pass" in c else ""))


if __name__ == "__main__":
    main()
