"""Track 2: is a stronger model worth it? Repeated stratified 10-fold cross-validation.

Models: LR (reference, C=1), M1 tuned LR, M2 tuned linear SVM, M4 small MLP with square
activation (12 hidden units). Every choice (scaler, C, epochs, L2) is made inside the
training folds only (nested), so the test fold is never used for tuning.
Rule (a) of the report: the gain in mean accuracy must exceed the spread (standard
deviation) of the reference model's fold accuracies.
Output: results/benchmarks/model_cv.json
"""
import json
import os
import sys
import warnings

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
from mlp import SquareMLP  # noqa: E402

warnings.filterwarnings("ignore")
N_SPLITS, N_REPEATS, SEED = 10, 10, 42
C_GRID = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]


def inner():
    return StratifiedKFold(5, shuffle=True, random_state=SEED)


def models():
    return {
        "LR": lambda: make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "M1 tuned LR": lambda: GridSearchCV(
            make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)),
            {"logisticregression__C": C_GRID}, cv=inner(), scoring="accuracy"),
        "M2 linear SVM": lambda: GridSearchCV(
            make_pipeline(StandardScaler(), LinearSVC(max_iter=20000)),
            {"linearsvc__C": C_GRID}, cv=inner(), scoring="accuracy"),
        "M4 square MLP": lambda: GridSearchCV(
            make_pipeline(StandardScaler(), SquareMLP(hidden=12, random_state=SEED)),
            {"squaremlp__epochs": [30, 100, 300], "squaremlp__l2": [0.1, 1.0, 3.0]},
            cv=StratifiedKFold(3, shuffle=True, random_state=SEED), scoring="accuracy"),
    }


def main():
    out = {"cv": {"n_splits": N_SPLITS, "n_repeats": N_REPEATS, "seed": SEED}, "datasets": {}}
    for name in C.DATASETS:
        ds = C.D.load_dataset(name, C.RAW_DIR)
        folds = list(RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS,
                                             random_state=SEED).split(ds.X, ds.y))
        res = {}
        for label, make in models().items():
            acc, auc = [], []
            for tr, te in folds:
                m = make().fit(ds.X[tr], ds.y[tr])
                score = m.decision_function(ds.X[te])
                acc.append(accuracy_score(ds.y[te], (score >= 0).astype(int)))
                auc.append(roc_auc_score(ds.y[te], score))
            res[label] = {"acc": acc, "auc": auc}
            print(f"{name:10s} {label:14s} accuracy {np.mean(acc):.4f} +/- {np.std(acc, ddof=1):.4f}  "
                  f"AUC {np.mean(auc):.4f}", flush=True)
        ref = np.array(res["LR"]["acc"])
        summary = {}
        for label, r in res.items():
            a = np.array(r["acc"])
            gain = float(a.mean() - ref.mean())
            summary[label] = {
                "accuracy_mean": float(a.mean()), "accuracy_sd": float(a.std(ddof=1)),
                "auc_mean": float(np.mean(r["auc"])), "auc_sd": float(np.std(r["auc"], ddof=1)),
                "gain_vs_lr": gain, "paired_diff_sd": float((a - ref).std(ddof=1)),
                "folds_better_than_lr": int(np.sum(a > ref)), "folds_worse_than_lr": int(np.sum(a < ref)),
                "passes_rule_a": bool(label != "LR" and gain > ref.std(ddof=1)),
            }
        out["datasets"][name] = {"rows": int(len(ds.y)), "spread_lr_sd": float(ref.std(ddof=1)), "models": summary}
    os.makedirs(C.OUT_DIR, exist_ok=True)
    with open(os.path.join(C.OUT_DIR, "model_cv.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
