"""Packed layout with the TenSEAL high-level API (the PR2 Table 5 pilot).

All features of one patient go in ONE ciphertext and the weighted sum is a dot
product. Small ciphertext (about 1 MB per patient) but the dot product needs Galois
(rotation) keys: about 164 MB at N = 16384 (PR2 section C).
"""
from __future__ import annotations

import tenseal as ts

from . import params as P


def make_context(param_set: str = P.DEFAULT_PARAM_SET, galois: bool = True) -> ts.Context:
    spec = P.PARAM_SETS[param_set]
    ctx = ts.context(ts.SCHEME_TYPE.CKKS,
                     poly_modulus_degree=spec["poly_modulus_degree"],
                     coeff_mod_bit_sizes=spec["coeff_mod_bit_sizes"])
    ctx.global_scale = P.SCALE
    if galois:
        ctx.generate_galois_keys()
    return ctx


def encrypt(ctx: ts.Context, x) -> ts.CKKSVector:
    return ts.ckks_vector(ctx, [float(v) for v in x])


def infer(enc_x: ts.CKKSVector, weights, bias: float, poly_coeffs=None) -> ts.CKKSVector:
    z = enc_x.dot([float(w) for w in weights]) + float(bias)
    if poly_coeffs is not None:
        z = z.polyval([float(c) for c in poly_coeffs])   # ascending order
    return z


def key_sizes_bytes(ctx: ts.Context) -> dict:
    """Serialized sizes, measured the same way as PR2 Table 5.

    Note: when the secret key is saved, TenSEAL omits the relinearization keys (they are
    regenerated from the secret key on load), so "context_with_secret_key" = secret key +
    public key only (about 0.6 + 1.3 MB at N=16384), while "public_context" = public key +
    relin keys (about 1.3 + 6.3 MB). Checked 11 Nov 2026."""
    with_sk = len(ctx.serialize(save_public_key=True, save_secret_key=True,
                                save_galois_keys=False, save_relin_keys=True))
    public = ctx.copy()
    public.make_context_public()
    public_no_galois = len(public.serialize(save_galois_keys=False, save_relin_keys=True))
    galois = len(ctx.serialize(save_public_key=False, save_secret_key=False,
                               save_galois_keys=True, save_relin_keys=False))
    return {"public_context": public_no_galois, "context_with_secret_key": with_sk,
            "galois_keys": galois}
