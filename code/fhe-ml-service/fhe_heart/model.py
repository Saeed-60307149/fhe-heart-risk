"""Plaintext logistic regression and the model_weights.json bridge file.

model_weights.json is what the FHE service loads. It holds the weights, the bias,
the scaler (so a raw patient form can be scaled exactly as in training), the
sigmoid polynomial and the decision threshold.
"""
from __future__ import annotations

import json
from typing import Any

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold

SCHEMA_VERSION = 1


def train_logreg(X: np.ndarray, y: np.ndarray, tune: bool = False,
                 random_state: int = 42) -> LogisticRegression:
    """Default C=1.0 reproduces the PR2 pilot. tune=True picks C by 5-fold CV
    on the training rows only (runbook step 6)."""
    if not tune:
        return LogisticRegression(max_iter=1000).fit(X, y)
    grid = GridSearchCV(
        LogisticRegression(max_iter=1000),
        {"C": [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]},
        cv=StratifiedKFold(5, shuffle=True, random_state=random_state),
        scoring="roc_auc")
    grid.fit(X, y)
    return grid.best_estimator_


def logits(model_or_w, X: np.ndarray, b: float | None = None) -> np.ndarray:
    if b is None:
        w = model_or_w.coef_[0]
        b = float(model_or_w.intercept_[0])
    else:
        w = np.asarray(model_or_w, dtype=float)
    return X @ w + b


def export_weights(path: str, model: LogisticRegression, scaler, feature_names: list[str],
                   dataset: str, poly_coeffs: list[float] | None = None,
                   poly_interval: tuple[float, float] | None = None,
                   threshold: float = 0.5, extra: dict[str, Any] | None = None) -> dict:
    doc = {
        "schema_version": SCHEMA_VERSION,
        "dataset": dataset,
        "feature_names": list(feature_names),
        "n_features": len(feature_names),
        "weights": [float(v) for v in model.coef_[0]],
        "bias": float(model.intercept_[0]),
        "scaler_mean": [float(v) for v in scaler.mean_],
        "scaler_scale": [float(v) for v in scaler.scale_],
        "threshold": float(threshold),
        "sigmoid_poly": None if poly_coeffs is None else {
            "coeffs_ascending": [float(c) for c in poly_coeffs],
            "interval": list(poly_interval) if poly_interval else None,
        },
    }
    if extra:
        doc.update(extra)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
    return doc


def load_weights(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    validate_weights(doc)
    return doc


def validate_weights(doc: dict) -> None:
    required = ["schema_version", "dataset", "feature_names", "weights", "bias",
                "scaler_mean", "scaler_scale", "threshold"]
    missing = [k for k in required if k not in doc]
    if missing:
        raise ValueError(f"model_weights.json missing keys: {missing}")
    n = len(doc["weights"])
    if not (len(doc["feature_names"]) == len(doc["scaler_mean"]) == len(doc["scaler_scale"]) == n):
        raise ValueError("weights, feature_names and scaler lengths differ")


def scale_raw(doc: dict, raw: list[float]) -> np.ndarray:
    """Apply the training scaler to one raw patient row (client side, before encryption)."""
    raw = np.asarray(raw, dtype=float)
    return (raw - np.asarray(doc["scaler_mean"])) / np.asarray(doc["scaler_scale"])
