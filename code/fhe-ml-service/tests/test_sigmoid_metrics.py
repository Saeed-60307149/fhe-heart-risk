import numpy as np

from fhe_heart import metrics as M
from fhe_heart import sigmoid as S


def test_least_squares_cubic_is_odd_and_close():
    c = S.fit_least_squares((-8, 8))
    assert c[0] == 0.5 and c[2] == 0.0
    z = np.linspace(-8, 8, 501)
    assert M.mae(M.sigmoid(z), S.poly_eval(c, z)) < 0.06


def test_published_cubic_matches_kim_on_its_interval():
    z = np.linspace(-8, 8, 501)
    assert M.mae(M.sigmoid(z), S.poly_eval(S.KIM_2018_DEG3, z)) < 0.06


def test_interval_from_train_logits_covers_them():
    z = np.random.default_rng(1).normal(0, 2, 500)
    lo, hi = S.interval_from_logits(z, coverage=1.0, margin=0.0)
    assert lo <= z.min() and hi >= z.max()


def test_decision_match_and_metrics():
    assert M.decision_match([0.1, 0.6, 0.9], [0.4, 0.7, 0.2]) == 2 / 3
    m = M.classification_metrics([0, 1, 1, 0], [0.2, 0.8, 0.4, 0.1])
    assert m["accuracy"] == 0.75 and m["roc_auc"] == 1.0
