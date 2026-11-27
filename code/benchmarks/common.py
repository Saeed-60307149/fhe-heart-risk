"""Shared helpers for the benchmarks: models (fixed split) and parameter sets."""
from __future__ import annotations

import os
import sys

import numpy as np

CODE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(CODE_DIR, "fhe-ml-service"))

from fhe_heart import data as D  # noqa: E402
from fhe_heart import metrics as M  # noqa: E402
from fhe_heart import model as ML  # noqa: E402
from fhe_heart import sigmoid as S  # noqa: E402

RAW_DIR = os.path.join(CODE_DIR, "data", "raw")
OUT_DIR = os.path.join(CODE_DIR, "results", "benchmarks")
DATASETS = ("cleveland", "edinburgh")
MAX_SCORE_ERROR = 0.01  # a setting passes only with 100% decision match AND this accuracy


def load_problem(name: str) -> dict:
    """Same model and split as the pilot: stratified 75/25, seed 42, C = 1.0."""
    split = D.split_and_scale(D.load_dataset(name, RAW_DIR))
    model = ML.train_logreg(split.X_train, split.y_train)
    w, b = model.coef_[0].astype(float), float(model.intercept_[0])
    interval = S.interval_from_logits(split.X_train @ w + b)
    poly = S.fit_least_squares(interval, degree=3, odd_only=True)
    z = split.X_test @ w + b
    return {"name": name, "X": split.X_test, "y": split.y_test, "w": w, "b": b, "poly": poly,
            "z": z, "p": M.sigmoid(z), "split": split, "model": model, "interval": interval}
