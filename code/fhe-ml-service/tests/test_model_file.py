import json

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from fhe_heart import model as ML


def test_export_load_roundtrip(tmp_path):
    X = np.random.default_rng(0).normal(size=(60, 3))
    y = (X[:, 0] > 0).astype(int)
    sc = StandardScaler().fit(X)
    m = LogisticRegression().fit(sc.transform(X), y)
    p = tmp_path / "model_weights_t.json"
    ML.export_weights(str(p), m, sc, ["a", "b", "c"], "t", poly_coeffs=[0.5, 0.2, 0.0, -0.004])
    doc = ML.load_weights(str(p))
    assert doc["n_features"] == 3 and len(doc["weights"]) == 3
    np.testing.assert_allclose(ML.scale_raw(doc, X[0]), sc.transform(X[:1])[0])


def test_validate_rejects_mismatched_lengths(tmp_path):
    doc = {"schema_version": 1, "dataset": "x", "feature_names": ["a"], "weights": [1, 2],
           "bias": 0, "scaler_mean": [0], "scaler_scale": [1], "threshold": 0.5}
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(doc))
    with pytest.raises(ValueError):
        ML.load_weights(str(p))
