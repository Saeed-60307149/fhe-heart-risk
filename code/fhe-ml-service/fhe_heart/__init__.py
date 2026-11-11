"""Shared code for the FHE heart-risk project.

Modules
-------
data         load + clean + split + scale the UCI Cleveland and Edinburgh MI datasets
model        train the plaintext logistic regression, export/load model_weights.json
metrics      accuracy, precision, recall, F1, ROC-AUC, decision match
sigmoid      least-squares polynomial approximation of the sigmoid
params       the CKKS parameter sets used by the project (single source of truth)
ckks_packed  TenSEAL high-level API, packed layout (13 features in 1 ciphertext)
seal_server  raw SEAL API, per-feature layout (node-seal compatible). SERVER SIDE:
             never decrypts, never sees a secret key.
seal_client  raw SEAL API helpers that hold the secret key. Used ONLY by tests,
             pilots and the Python fallback client (Plan B). Never import this
             from app.py.
"""

__all__ = ["data", "model", "metrics", "sigmoid", "params", "ckks_packed",
           "seal_server", "seal_client"]
