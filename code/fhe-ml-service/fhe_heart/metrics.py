"""Evaluation metrics used everywhere in the project (baseline, sigmoid, FHE)."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score,
                             roc_auc_score)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, dtype=float)))


def classification_metrics(y_true, scores, threshold: float = 0.5) -> dict:
    """scores are probabilities (or probability-like outputs of a polynomial)."""
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, dtype=float)
    y_pred = (scores >= threshold).astype(int)
    out = {
        "n": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
    out["roc_auc"] = float(roc_auc_score(y_true, scores)) if len(set(y_true)) == 2 else None
    return out


def decision_match(scores_a, scores_b, threshold: float = 0.5) -> float:
    """Share of patients whose low/high-risk decision is the same (RQ-A)."""
    a = np.asarray(scores_a) >= threshold
    b = np.asarray(scores_b) >= threshold
    return float(np.mean(a == b))


def mae(a, b) -> float:
    return float(np.mean(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))
