import json
import os
import sys

import numpy as np
import pytest

SERVICE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if SERVICE_DIR not in sys.path:
    sys.path.insert(0, SERVICE_DIR)

from fhe_heart import sigmoid as S  # noqa: E402

N_FEATURES = 13


@pytest.fixture(scope="session")
def toy_model():
    """A fixed 13-feature model (no dataset download needed in tests)."""
    rng = np.random.default_rng(7)
    w = rng.normal(0, 0.5, N_FEATURES)
    w[4] = 0.0                      # a zero weight must be skipped, not multiplied
    return {
        "schema_version": 1, "dataset": "toy", "n_features": N_FEATURES,
        "feature_names": [f"f{i}" for i in range(N_FEATURES)],
        "weights": [float(v) for v in w], "bias": 0.25,
        "scaler_mean": [0.0] * N_FEATURES, "scaler_scale": [1.0] * N_FEATURES,
        "threshold": 0.5, "param_set": "n16384_depth4",
        "sigmoid_poly": {"coeffs_ascending": S.fit_least_squares((-8, 8)), "interval": [-8, 8]},
    }


@pytest.fixture(scope="session")
def model_dir(tmp_path_factory, toy_model):
    d = tmp_path_factory.mktemp("model")
    with open(d / "model_weights_toy.json", "w") as fh:
        json.dump(toy_model, fh)
    return str(d)


@pytest.fixture(scope="session")
def client_keys():
    from fhe_heart.seal_client import SealClient
    c = SealClient.create()
    return c, c.relin_keys_bytes()


@pytest.fixture
def patients():
    rng = np.random.default_rng(11)
    return rng.normal(0, 1, (4, N_FEATURES))
