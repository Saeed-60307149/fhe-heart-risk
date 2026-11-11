import numpy as np
import pytest

from fhe_heart import ckks_packed as CP
from fhe_heart import sigmoid as S


@pytest.mark.slow
def test_packed_dot_and_poly(toy_model, patients):
    ctx = CP.make_context()
    w, b = toy_model["weights"], toy_model["bias"]
    poly = toy_model["sigmoid_poly"]["coeffs_ascending"]
    for x in patients[:2]:
        out = CP.infer(CP.encrypt(ctx, x), w, b, poly).decrypt()[0]
        assert abs(out - S.poly_eval(poly, x @ np.array(w) + b)) < 1e-3
