"""API contract tests for the internal FHE service (design/api-contract.md, section 3)."""
import base64
import importlib

import numpy as np
import pytest
from fastapi.testclient import TestClient

from fhe_heart import sigmoid as S


def b64(x: bytes) -> str:
    return base64.b64encode(x).decode()


@pytest.fixture(scope="module")
def api(model_dir):
    mp = pytest.MonkeyPatch()
    mp.setenv("MODEL_DIR", model_dir)
    mp.setenv("FHE_SERVICE_TOKEN", "test-token")
    import app as app_module
    importlib.reload(app_module)
    yield TestClient(app_module.app)
    mp.undo()


H = {"X-Internal-Token": "test-token"}


@pytest.fixture(scope="module")
def web_clients():
    from fhe_heart.seal_client import SealClient
    logit, poly = SealClient.create("web_logit"), SealClient.create("web_poly")
    return logit, poly, poly.relin_keys_bytes()


def body(client, x, output="logit", rk=None):
    return {"dataset": "toy", "parms": b64(client.parms_bytes()),
            "ciphertexts": [b64(c) for c in client.encrypt_features(x)],
            "relin_keys": b64(rk) if rk else None, "output": output}


def test_health(api):
    r = api.get("/health")
    assert r.status_code == 200 and r.json()["models"] == ["toy"]


def test_model_info_hides_weights(api):
    r = api.get("/model/toy", headers=H)
    assert r.status_code == 200
    j = r.json()
    assert "weights" not in j and "bias" not in j and j["n_features"] == 13
    assert j["params"]["poly_modulus_degree"] == 4096 and j["poly_params"]["poly_modulus_degree"] == 8192


def test_token_required(api, web_clients, patients):
    client = web_clients[0]
    r = api.post("/infer", json=body(client, patients[0]))
    assert r.status_code == 401 and r.json()["error"]["code"] == "UNAUTHORIZED"


def test_infer_logit(api, web_clients, toy_model, patients):
    client = web_clients[0]
    x = patients[0]
    r = api.post("/infer", json=body(client, x), headers=H)
    assert r.status_code == 200, r.text
    j = r.json()
    z = client.decrypt_scalar(base64.b64decode(j["encrypted_result"]))
    assert j["output"] == "logit"
    assert abs(z - (x @ np.array(toy_model["weights"]) + toy_model["bias"])) < 1e-2


def test_infer_probability_poly(api, web_clients, toy_model, patients):
    _, client, rk = web_clients
    x = patients[1]
    r = api.post("/infer", json=body(client, x, "probability_poly", rk), headers=H)
    assert r.status_code == 200, r.text
    p = client.decrypt_scalar(base64.b64decode(r.json()["encrypted_result"]))
    z = x @ np.array(toy_model["weights"]) + toy_model["bias"]
    assert abs(p - S.poly_eval(toy_model["sigmoid_poly"]["coeffs_ascending"], z)) < 1e-2


def test_unapproved_parameters_rejected(api, client_keys, patients):
    """A valid, secure parameter set that is not on the approved list is refused (T7)."""
    client, _ = client_keys          # the pilot set: valid for SEAL, not approved for the web service
    r = api.post("/infer", json=body(client, patients[0]), headers=H)
    assert r.status_code == 422 and r.json()["error"]["code"] == "UNSUPPORTED_PARAMETERS"


def test_poly_without_relin_keys(api, web_clients, patients):
    client = web_clients[0]
    r = api.post("/infer", json=body(client, patients[0], "probability_poly"), headers=H)
    assert r.status_code == 400 and r.json()["error"]["code"] == "BAD_REQUEST"


def test_bad_base64(api, web_clients, patients):
    client = web_clients[0]
    b = body(client, patients[0])
    b["ciphertexts"][0] = "@@not-base64@@"
    r = api.post("/infer", json=b, headers=H)
    assert r.status_code == 422 and r.json()["error"]["code"] == "INVALID_CIPHERTEXT"


def test_unknown_dataset(api, web_clients, patients):
    client = web_clients[0]
    b = body(client, patients[0])
    b["dataset"] = "nope"
    r = api.post("/infer", json=b, headers=H)
    assert r.status_code == 404 and r.json()["error"]["code"] == "MODEL_NOT_FOUND"


def test_validation_error_does_not_echo_input(api):
    r = api.post("/infer", json={"dataset": "toy", "ciphertexts": "SECRETBLOB"}, headers=H)
    assert r.status_code == 400 and "SECRETBLOB" not in r.text
