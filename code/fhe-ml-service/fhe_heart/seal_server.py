"""Server-side encrypted inference on node-seal ciphertexts (both layouts).

per_feature: one CKKS ciphertext per feature. The weighted sum needs no rotation (Galois) keys.
packed:      all features of one patient in the first slots of ONE ciphertext. The sum uses
             rotations by 1, 2, 4, ... only, so the client creates just those Galois keys.
The main output is the encrypted score (the client applies the sigmoid). The optional cubic
sigmoid needs relinearization keys, which the client creates and sends.

SECURITY RULES for this module (checked by tests/test_no_secret_on_server.py):
  * it never imports or creates a SecretKey or a Decryptor;
  * it never calls decrypt;
  * it never logs ciphertext or key bytes.
"""
from __future__ import annotations

import math
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
    def __init__(self, parms_bytes: bytes, approved_only: bool = False):
        parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
        try:
            _load(parms, parms_bytes)
        except Exception as exc:  # malformed header, wrong scheme, ...
            raise FheInputError("INVALID_CIPHERTEXT", f"cannot read encryption parameters: {exc}")
        if parms.scheme() != seal.SCHEME_TYPE.CKKS:
            raise FheInputError("UNSUPPORTED_PARAMETERS", "scheme must be CKKS")
        degree = parms.poly_modulus_degree()
        if approved_only:
            chain = tuple(m.bit_count() for m in parms.coeff_modulus())
            if (degree, chain) not in P.approved_parameters():
                raise FheInputError("UNSUPPORTED_PARAMETERS",
                                    "encryption parameters are not one of the approved sets")
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

    def load_galois_keys(self, data: bytes) -> "seal.GaloisKeys":
        if len(data) > P.MAX_GALOIS_KEY_BYTES:
            raise FheInputError("PAYLOAD_TOO_LARGE", "rotation keys larger than allowed")
        gk = seal.GaloisKeys()
        try:
            _load(gk, data, self.ctx)
        except Exception as exc:
            raise FheInputError("INVALID_CIPHERTEXT", f"rotation keys rejected: {exc}")
        return gk

    # ---------- arithmetic ----------
    def _normalise(self, ct) -> None:
        # Used inside the cubic only. After a rescale the scale is s0 * (s0 / q_i), close to
        # s0 when the middle primes are about s0. Re-labelling lets terms be added; the
        # relative error is about |q_i / s0 - 1|.
        ct.scale = self.s0

    def _dropped_prime(self, ct) -> float:
        """Value of the last prime at this level (the one the next rescale removes)."""
        return float(self.ctx.get_context_data(ct.parms_id()).parms().coeff_modulus()[-1].value())

    def _linear_weight_scale(self, ct) -> float:
        if self.levels >= 1:
            # Encoding the weights at exactly the dropped prime makes the rescaled result
            # come back to the input scale with no approximation.
            return self._dropped_prime(ct)
        # Only one data prime: no rescale is possible; the result keeps scale s0 * weight scale.
        q0_bits = math.log2(self._dropped_prime(ct))
        bits = min(math.log2(ct.scale), q0_bits - math.log2(ct.scale) - 7)
        if bits < 6:
            raise FheInputError("UNSUPPORTED_PARAMETERS", "modulus too small for a weighted sum")
        return 2.0 ** int(bits)

    def _finish_linear(self, ct) -> None:
        if self.levels >= 1:
            self.evaluator.rescale_to_next_inplace(ct)
            ct.scale = self.s0

    def _mul_plain(self, ct, value: float):
        pt = seal.Plaintext()
        self.encoder.encode(float(value), ct.parms_id(), ct.scale, pt)
        out = seal.Ciphertext()
        self.evaluator.multiply_plain(ct, pt, out)
        self.evaluator.rescale_to_next_inplace(out)
        self._normalise(out)
        return out

    def _add_plain(self, ct, value: float) -> None:
        pt = seal.Plaintext()
        self.encoder.encode(float(value), ct.parms_id(), ct.scale, pt)
        self.evaluator.add_plain_inplace(ct, pt)

    def weighted_sum(self, cts: list, weights: list[float], bias: float):
        """Per-feature layout: z = sum_j w_j * x_j + b. Uses 1 level. Zero weights are skipped
        (a multiply by 0 gives a transparent ciphertext, which SEAL refuses)."""
        acc = None
        weight_scale = None
        for ct, w in zip(cts, weights):
            if abs(w) < 1e-12:
                continue
            weight_scale = weight_scale or self._linear_weight_scale(ct)
            pt = seal.Plaintext()
            self.encoder.encode(float(w), ct.parms_id(), weight_scale, pt)
            term = seal.Ciphertext()
            self.evaluator.multiply_plain(ct, pt, term)
            if acc is None:
                acc = term
            else:
                self.evaluator.add_inplace(acc, term)
        if acc is None:
            raise FheInputError("BAD_REQUEST", "model has no non-zero weights")
        self._finish_linear(acc)
        self._add_plain(acc, bias)
        return acc

    def packed_sum(self, ct, weights: list[float], bias: float, galois_keys):
        """Packed layout: slot j holds feature j. Multiply by the weight vector, then
        rotate-and-add so slot 0 holds the full sum. Only slot 0 is the result; the other
        slots hold partial sums (threat model: model-weight leakage, public-data model)."""
        weight_scale = self._linear_weight_scale(ct)
        vec = [float(w) for w in weights] + [0.0] * (self.encoder.slot_count() - len(weights))
        pt = seal.Plaintext()
        self.encoder.encode(vec, ct.parms_id(), weight_scale, pt)
        acc = seal.Ciphertext()
        self.evaluator.multiply_plain(ct, pt, acc)
        self._finish_linear(acc)
        for step in P.rotation_steps(len(weights)):
            rot = seal.Ciphertext()
            try:
                self.evaluator.rotate_vector(acc, step, galois_keys, rot)
            except Exception as exc:
                raise FheInputError("INVALID_CIPHERTEXT", f"rotation by {step} failed: {exc}")
            self.evaluator.add_inplace(acc, rot)
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
              poly: list[float] | None = None, relin_bytes: bytes | None = None,
              layout: str = "per_feature", galois_bytes: bytes | None = None,
              trim: bool = True) -> InferenceResult:
        expected = 1 if layout == "packed" else len(weights)
        if len(ct_bytes) != expected:
            raise FheInputError("BAD_REQUEST",
                                f"expected {expected} ciphertexts, got {len(ct_bytes)}")
        if layout == "packed" and not galois_bytes:
            raise FheInputError("BAD_REQUEST", "layout=packed needs galois_keys")
        t0 = time.perf_counter()
        cts = [self.load_ciphertext(b) for b in ct_bytes]
        scales = {round(math.log2(c.scale), 6) for c in cts}
        if len(scales) != 1 or not 10 <= next(iter(scales)) <= 60:
            raise FheInputError("INVALID_CIPHERTEXT", "ciphertexts must share one sensible scale")
        self.s0 = cts[0].scale
        rk = self.load_relin_keys(relin_bytes) if (poly and relin_bytes) else None
        gk = self.load_galois_keys(galois_bytes) if layout == "packed" else None
        t1 = time.perf_counter()
        if layout == "packed":
            z = self.packed_sum(cts[0], weights, bias, gk)
        else:
            z = self.weighted_sum(cts, weights, bias)
        output = "logit"
        if rk is not None:
            z = self.cubic(z, poly, rk)
            output = "probability_poly"
        if trim and z.parms_id() != self.ctx.last_parms_id():
            self.evaluator.mod_switch_to_inplace(z, self.ctx.last_parms_id())
        t2 = time.perf_counter()
        out = _save(z)
        t3 = time.perf_counter()
        return InferenceResult(out, output, {
            "load_ms": round((t1 - t0) * 1000, 2),
            "compute_ms": round((t2 - t1) * 1000, 2),
            "serialize_ms": round((t3 - t2) * 1000, 2),
        })
