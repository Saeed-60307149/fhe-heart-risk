#!/usr/bin/env python3
"""Train the model (same split and model as the pilot) and export ONE test patient
for the cross-library round-trip (node-seal encrypt -> TenSEAL compute -> node-seal
decrypt).

Uses the shared loader in code/fhe-ml-service/fhe_heart (UCI Cleveland by default,
stratified test_size=0.25, seed 42), so the patient and weights are identical to the
ones used by pilots/tenseal-pilot/pilot.py.

Usage:  python train_export.py [--dataset cleveland|edinburgh] [--index 0]
Output: model_patient.json (git-ignored)
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "fhe-ml-service")))

from fhe_heart import data as D  # noqa: E402
from fhe_heart import model as ML  # noqa: E402

RAW_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "data", "raw"))

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", default="cleveland", choices=sorted(D.LOADERS))
ap.add_argument("--index", type=int, default=0, help="which test patient to export")
args = ap.parse_args()

split = D.split_and_scale(D.load_dataset(args.dataset, RAW_DIR))
model = ML.train_logreg(split.X_train, split.y_train)
w = model.coef_[0]
b = float(model.intercept_[0])
x = split.X_test[args.index]
z_true = float(x @ w + b)

with open(os.path.join(HERE, "model_patient.json"), "w") as fh:
    json.dump({"dataset": args.dataset, "w": w.tolist(), "b": b, "patient": x.tolist(),
               "z_true": z_true, "label": int(split.y_test[args.index])}, fh)
print(f"exported model_patient.json ({args.dataset}, test patient {args.index}); "
      f"z_true = {z_true:.4f} label = {int(split.y_test[args.index])}")
