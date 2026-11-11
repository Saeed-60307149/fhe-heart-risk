"""Server-side encrypted inference on node-seal ciphertexts (per-feature layout).

Layout: one CKKS ciphertext per feature (the Report 1 design, used in the PR2
cross-library round-trip). The weighted sum needs no rotation (Galois) keys; the
cubic sigmoid needs only relinearization keys, which the client creates and sends.

SECURITY RULES for this module (checked by tests/test_no_secret_on_server.py):
  * it never imports or creates a SecretKey or a Decryptor;
  * it never calls decrypt;
  * it never logs ciphertext or key bytes.
"""
from __future__ import annotations

import os
import tempfile
import time
from dataclasses import dataclass, field

from tenseal import sealapi as seal

from . import params as P


class FheInputError(ValueError):
    """The client sent something we cannot use. `code` maps to an API error code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _load(obj, data: bytes, ctx=None) -> None:
    """sealapi only loads from a file path, so write to a private temp file."""
    with tempfile.TemporaryDirectory(prefix="fhe-") as tmp:
        path = os.path.join(tmp, "blob")
        with open(path, "wb") as fh:
            fh.write(data)
        if ctx is None:
            obj.load(path)
        else:
            obj.load(ctx, path)


def _save(obj) -> bytes:
    with tempfile.TemporaryDirectory(prefix="fhe-") as tmp:
        path = os.path.join(tmp, "blob")
        obj.save(path)
        with open(path, "rb") as fh:
            return fh.read()


@dataclass
class InferenceResult:
    ciphertext: bytes
    output: str                       # "logit" or "probability_poly"
    timings_ms: dict = field(default_factory=dict)


class SealServer:
    def __init__(self, parms_bytes: bytes):
        parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
        try:
            _load(parms, parms_bytes)
        except Exception as exc:  # malformed header, wrong scheme, ...
            raise FheInputError("INVALID_CIPHERTEXT", f"cannot read encryption parameters: {exc}")
        if parms.scheme() != seal.SCHEME_TYPE.CKKS:
            raise FheInputError("UNSUPPORTED_PARAMETERS", "scheme must be CKKS")
        degree = parms.poly_modulus_degree()
        if degree not in P.allowed_degrees():
            raise FheInputError("UNSUPPORTED_PARAMETERS",
                                f"poly_modulus_degree {degree} not in {sorted(P.allowed_degrees())}")
        self.ctx = seal.SEALContext(parms, True, seal.SEC_LEVEL_TYPE.TC128)
        if not self.ctx.parameters_set():
            raise FheInputError("UNSUPPORTED_PARAMETERS",
                                f"parameters rejected by SEAL: {self.ctx.parameters_error_message()}")
        self.degree = degree
        self.levels = len(parms.coeff_modulus()) - 2      # rescales available
        self.encoder = seal.CKKSEncoder(self.ctx)
        self.evaluator = seal.Evaluator(self.ctx)

    # ---------- loading ----------
    def load_ciphertext(self, data: bytes) -> "seal.Ciphertext":
        if len(data) > P.MAX_CIPHERTEXT_BYTES:
            raise FheInputError("PAYLOAD_TOO_LARGE", "ciphertext larger than allowed")
        ct = seal.Ciphertext()
        try:
            _load(ct, data, self.ctx)          # SEAL validates it against the context
        except Exception as exc:
            raise FheInputError("INVALID_CIPHERTEXT", f"ciphertext rejected: {exc}")
        if ct.size() != 2:
            raise FheInputError("INVALID_CIPHERTEXT", "expected a fresh size-2 ciphertext")
        if ct.parms_id() != self.ctx.first_parms_id():
            raise FheInputError("INVALID_CIPHERTEXT", "ciphertext is not at the first level")
        if ct.is_transparent():
            raise FheInputError("INVALID_CIPHERTEXT", "transparent ciphertext")
        return ct

    def load_relin_keys(self, data: bytes) -> "seal.RelinKeys":
        if len(data) > P.MAX_RELIN_KEY_BYTES:
            raise FheInputError("PAYLOAD_TOO_LARGE", "relinearization keys larger than allowed")
        rk = seal.RelinKeys()
        try:
            _load(rk, data, self.ctx)
        except Exception as exc:
            raise FheInputError("INVALID_CIPHERTEXT", f"relinearization keys rejected: {exc}")
        return rk

    # ---------- arithmetic ----------
    def _normalise(self, ct) -> None:
        # After a rescale the scale is 2^40 * (2^40 / q_i), close to but not exactly
        # 2^40. Re-labelling it as exactly 2^40 lets terms be added; the relative error
        # is about |q_i / 2^40 - 1| (< 1e-6 for 40-bit primes), far below the sigmoid
        # approximation error.
        ct.scale = P.SCALE

    def _mul_plain(self, ct, value: float):
        pt = seal.Plaintext()
        self.encoder.encode([float(value)], ct.parms_id(), ct.scale, pt)
        out = seal.Ciphertext()
        self.evaluator.multiply_plain(ct, pt, out)
        self.evaluator.rescale_to_next_inplace(out)
        self._normalise(out)
        return out

    def _add_plain(self, ct, value: float) -> None:
        pt = seal.Plaintext()
        self.encoder.encode([float(value)], ct.parms_id(), ct.scale, pt)
        self.evaluator.add_plain_inplace(ct, pt)

    def weighted_sum(self, cts: list, weights: list[float], bias: float):
        """z = sum_j w_j * x_j + b. Uses 1 level. Zero weights are skipped (a
        multiply by 0 gives a transparent ciphertext, which SEAL refuses)."""
        acc = None
        for ct, w in zip(cts, weights):
            if abs(w) < 1e-12:
                continue
            term = self._mul_plain(ct, w)
            if acc is None:
                acc = term
            else:
                self.evaluator.add_inplace(acc, term)
        if acc is None:
            raise FheInputError("BAD_REQUEST", "model has no non-zero weights")
        self._add_plain(acc, bias)
        return acc

    def cubic(self, z, coeffs_ascending: list[float], relin_keys):
        """p(z) = c0 + c1 z + c2 z^2 + c3 z^3 using 2 more levels:
        level+1: z2 = z*z, a = c3*z ; level+2: z2*a, c2*z2, c1*z (mod-switched)."""
        c = list(coeffs_ascending) + [0.0] * (4 - len(coeffs_ascending))
        if self.levels < 3:
            raise FheInputError("UNSUPPORTED_PARAMETERS",
                                "parameter set has too few levels for the cubic sigmoid")
        ev = self.evaluator
        z2 = seal.Ciphertext()
        ev.square(z, z2)
        ev.relinearize_inplace(z2, relin_keys)
        ev.rescale_to_next_inplace(z2)
        self._normalise(z2)

        terms = []
        if abs(c[3]) > 1e-12:
            a = self._mul_plain(z, c[3])
            z3 = seal.Ciphertext()
            ev.multiply(z2, a, z3)
            ev.relinearize_inplace(z3, relin_keys)
            ev.rescale_to_next_inplace(z3)
            self._normalise(z3)
            terms.append(z3)
        if abs(c[2]) > 1e-12:
            terms.append(self._mul_plain(z2, c[2]))
        if abs(c[1]) > 1e-12:
            terms.append(self._mul_plain(z, c[1]))
        if not terms:
            raise FheInputError("BAD_REQUEST", "sigmoid polynomial has no non-constant term")
        target = min(terms, key=lambda t: t.coeff_modulus_size()).parms_id()
        for t in terms:
            if t.parms_id() != target:
                ev.mod_switch_to_inplace(t, target)
        res = terms[0]
        for t in terms[1:]:
            ev.add_inplace(res, t)
        self._add_plain(res, c[0])
        return res

    def infer(self, ct_bytes: list[bytes], weights: list[float], bias: float,
              poly: list[float] | None = None, relin_bytes: bytes | None = None) -> InferenceResult:
        if len(ct_bytes) != len(weights):
            raise FheInputError("BAD_REQUEST",
                                f"expected {len(weights)} ciphertexts, got {len(ct_bytes)}")
        t0 = time.perf_counter()
        cts = [self.load_ciphertext(b) for b in ct_bytes]
        rk = self.load_relin_keys(relin_bytes) if (poly and relin_bytes) else None
        t1 = time.perf_counter()
        z = self.weighted_sum(cts, weights, bias)
        output = "logit"
        if rk is not None:
            z = self.cubic(z, poly, rk)
            output = "probability_poly"
        t2 = time.perf_counter()
        out = _save(z)
        t3 = time.perf_counter()
        return InferenceResult(out, output, {
            "load_ms": round((t1 - t0) * 1000, 2),
            "compute_ms": round((t2 - t1) * 1000, 2),
            "serialize_ms": round((t3 - t2) * 1000, 2),
        })
