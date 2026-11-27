"""Runbook steps 13-16: encrypt -> compute -> decrypt with the final parameters."""
import numpy as np
import pytest

from fhe_heart import sigmoid as S
from fhe_heart.seal_server import FheInputError, SealServer

TOL = 1e-3


def test_weighted_sum_matches_plaintext(client_keys, toy_model, patients):
    client, _ = client_keys
    server = SealServer(client.parms_bytes())
    w, b = toy_model["weights"], toy_model["bias"]
    for x in patients:
        res = server.infer(client.encrypt_features(x), w, b)
        assert res.output == "logit"
        assert abs(client.decrypt_scalar(res.ciphertext) - (x @ np.array(w) + b)) < TOL


def test_cubic_sigmoid_matches_plaintext_poly(client_keys, toy_model, patients):
    client, rk = client_keys
    server = SealServer(client.parms_bytes())
    w, b = toy_model["weights"], toy_model["bias"]
    poly = toy_model["sigmoid_poly"]["coeffs_ascending"]
    for x in patients:
        res = server.infer(client.encrypt_features(x), w, b, poly, rk)
        assert res.output == "probability_poly"
        expected = S.poly_eval(poly, x @ np.array(w) + b)
        assert abs(client.decrypt_scalar(res.ciphertext) - expected) < TOL


def test_general_cubic_with_square_term(client_keys):
    client, rk = client_keys
    server = SealServer(client.parms_bytes())
    poly = [0.1, -0.3, 0.05, 0.002]
    x = np.array([1.5, -0.5] + [0.0] * 11)
    w = [1.0, 2.0] + [0.0] * 11
    res = server.infer(client.encrypt_features(x), w, 0.2, poly, rk)
    z = 1.5 - 1.0 + 0.2
    assert abs(client.decrypt_scalar(res.ciphertext) - S.poly_eval(poly, z)) < TOL


def test_wrong_number_of_ciphertexts(client_keys, toy_model):
    client, _ = client_keys
    server = SealServer(client.parms_bytes())
    with pytest.raises(FheInputError) as e:
        server.infer(client.encrypt_features([0.1, 0.2]), toy_model["weights"], 0.0)
    assert e.value.code == "BAD_REQUEST"


def test_garbage_ciphertext_rejected(client_keys):
    client, _ = client_keys
    server = SealServer(client.parms_bytes())
    with pytest.raises(FheInputError) as e:
        server.load_ciphertext(b"\x00" * 128)
    assert e.value.code == "INVALID_CIPHERTEXT"


def test_ciphertext_from_other_parameters_rejected(client_keys):
    from fhe_heart.seal_client import SealClient
    client, _ = client_keys
    other = SealClient.create("n8192_depth2")
    server = SealServer(client.parms_bytes())
    with pytest.raises(FheInputError):
        server.load_ciphertext(other.encrypt_features([1.0])[0])


def test_garbage_parameters_rejected():
    with pytest.raises(FheInputError):
        SealServer(b"not seal parameters")


def test_oversized_ciphertext_rejected(client_keys):
    client, _ = client_keys
    server = SealServer(client.parms_bytes())
    with pytest.raises(FheInputError) as e:
        server.load_ciphertext(b"\x00" * 3_000_000)
    assert e.value.code == "PAYLOAD_TOO_LARGE"


@pytest.mark.parametrize("layout", ["per_feature", "packed"])
def test_web_sized_settings_both_layouts(toy_model, patients, layout):
    """Small settings: the encrypted score matches the plain score in both layouts."""
    from tenseal import sealapi as seal
    from fhe_heart import params as P
    from fhe_heart.seal_client import SealClient
    from fhe_heart.seal_server import _save
    client = SealClient.create("web_logit")
    server = SealServer(client.parms_bytes())
    w, b = toy_model["weights"], toy_model["bias"]
    galois = None
    if layout == "packed":
        degree = P.PARAM_SETS["web_logit"]["poly_modulus_degree"]
        keys = seal.GaloisKeys()
        client._keygen.create_galois_keys([pow(3, s, 2 * degree) for s in P.rotation_steps(len(w))], keys)
        galois = _save(keys)
    for x in patients:
        if layout == "packed":
            pt, ct = seal.Plaintext(), seal.Ciphertext()
            client.encoder.encode([float(v) for v in x], client.scale, pt)
            seal.Encryptor(client.ctx, client.public_key).encrypt(pt, ct)
            blobs = [_save(ct)]
        else:
            blobs = client.encrypt_features(x)
        res = server.infer(blobs, w, b, layout=layout, galois_bytes=galois)
        tolerance = 0.1 if layout == "packed" else 1e-2   # packed adds rotation noise
        assert abs(client.decrypt_scalar(res.ciphertext) - (x @ np.array(w) + b)) < tolerance
