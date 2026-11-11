"""Polynomial approximation of the sigmoid (runbook steps 8-9).

FHE only supports + and x, so sigmoid(z) is replaced by p(z) = c0 + c1 z + c2 z^2 + c3 z^3.
The PR2 pilot used a least-squares cubic (MAE 0.031 on the Cleveland test set).

Coefficients are stored lowest power first ("ascending") everywhere in this repo.
"""
from __future__ import annotations

import numpy as np

# Published degree-3 approximations, for comparison (ascending order).
# Kim et al. 2018 (BMC Med Genomics), least squares on [-8, 8].
KIM_2018_DEG3 = [0.5, 0.15012, 0.0, -0.001593]
# Common textbook choice quoted in the project runbook (step 8), range about [-5, 5].
RUNBOOK_DEG3 = [0.5, 0.197, 0.0, -0.004]


def fit_least_squares(interval: tuple[float, float], degree: int = 3,
                      n_points: int = 2001, odd_only: bool = True) -> list[float]:
    """Least-squares fit of sigmoid on a uniform grid over `interval`.

    odd_only=True forces p(z) - 0.5 to be odd (c2 = 0), which matches the symmetry
    of the sigmoid, saves one encrypted multiplication and avoids a zero-plaintext
    multiply (SEAL refuses transparent ciphertexts).
    """
    lo, hi = interval
    z = np.linspace(lo, hi, n_points)
    s = 1.0 / (1.0 + np.exp(-z))
    if odd_only:
        powers = [p for p in range(1, degree + 1) if p % 2 == 1]
        A = np.column_stack([z ** p for p in powers])
        sol, *_ = np.linalg.lstsq(A, s - 0.5, rcond=None)
        coeffs = [0.0] * (degree + 1)
        coeffs[0] = 0.5
        for p, c in zip(powers, sol):
            coeffs[p] = float(c)
        return coeffs
    desc = np.polyfit(z, s, degree)
    return [float(c) for c in desc[::-1]]


def poly_eval(coeffs_ascending, z):
    z = np.asarray(z, dtype=float)
    return np.polyval(np.asarray(coeffs_ascending, dtype=float)[::-1], z)


def interval_from_logits(z_train: np.ndarray, coverage: float = 0.99,
                         margin: float = 1.0) -> tuple[float, float]:
    """Symmetric interval that covers `coverage` of the training logits plus a margin.
    Uses training rows only, so the test set does not leak into the choice."""
    q = float(np.quantile(np.abs(z_train), coverage)) + margin
    return (-q, q)


def clipped(p):
    """Probability view of a polynomial output, for reporting only (clipping is not
    possible under FHE; the decision threshold at 0.5 does not need it)."""
    return np.clip(p, 0.0, 1.0)
