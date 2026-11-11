#!/usr/bin/env python3
"""Plaintext logistic regression baseline (runbook steps 3-7; PR2 objective 2).

For each dataset: load, clean, fixed stratified split (test_size=0.25, seed 42),
scale on train only, train logistic regression, report accuracy, precision, recall,
F1 and ROC-AUC on the test split, and export model_weights_<dataset>.json for the
FHE service.

Usage (from code/):
    python pilots/baseline/train_baseline.py                 # both datasets
    python pilots/baseline/train_baseline.py --dataset cleveland
    python pilots/baseline/train_baseline.py --tune          # pick C by 5-fold CV
Outputs:
    results/<dataset>/baseline_metrics.json
    fhe-ml-service/model/model_weights_<dataset>.json
    data/processed/<dataset>/{train,test}.csv   (not committed)
"""
import argparse
import json
import os
import platform
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import pilot_paths as PP  # noqa: E402

from fhe_heart import data as D  # noqa: E402
from fhe_heart import metrics as M  # noqa: E402
from fhe_heart import model as ML  # noqa: E402


def run(dataset: str, tune: bool) -> dict:
    ds = D.load_dataset(dataset, PP.RAW_DIR)
    split = D.split_and_scale(ds)
    D.save_processed(split, os.path.join(PP.PROCESSED_DIR, dataset))
    model = ML.train_logreg(split.X_train, split.y_train, tune=tune)
    z_te = ML.logits(model, split.X_test)
    z_tr = ML.logits(model, split.X_train)
    test = M.classification_metrics(split.y_test, M.sigmoid(z_te))
    train = M.classification_metrics(split.y_train, M.sigmoid(z_tr))
    out = {
        "dataset": dataset,
        "rows_after_cleaning": int(len(ds.y)),
        "n_features": int(ds.X.shape[1]),
        "positives": int(ds.y.sum()),
        "train_rows": int(len(split.y_train)),
        "test_rows": int(len(split.y_test)),
        "split": {"test_size": D.TEST_SIZE, "random_state": D.RANDOM_STATE, "stratified": True},
        "model": {"type": "LogisticRegression", "C": float(model.C), "tuned": tune},
        "test": test,
        "train": train,
        "logit_range_train": [float(z_tr.min()), float(z_tr.max())],
        "logit_range_test": [float(z_te.min()), float(z_te.max())],
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
    }
    ML.export_weights(PP.model_path(dataset), model, split.scaler, split.feature_names,
                      dataset, extra={"param_set": "n16384_depth4"})
    with open(os.path.join(PP.results_dir(dataset), "baseline_metrics.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(D.LOADERS), action="append")
    ap.add_argument("--tune", action="store_true")
    args = ap.parse_args()
    for name in args.dataset or sorted(D.LOADERS):
        r = run(name, args.tune)
        t = r["test"]
        print(f"{name}: rows={r['rows_after_cleaning']} test={r['test_rows']} "
              f"acc={t['accuracy']:.3f} prec={t['precision']:.3f} rec={t['recall']:.3f} "
              f"f1={t['f1']:.3f} auc={t['roc_auc']:.3f}")


if __name__ == "__main__":
    main()
