"""CKKS parameter sets - the single source of truth for Python and JavaScript.

The browser does not hard-code these: it reads them from GET /api/model/{dataset}
(field "params"), so a change here reaches the client automatically. The node-seal
pilot scripts in code/pilots/node-seal-roundtrip/ use the same numbers by hand.

Two kinds of set: the pilot sets (N = 16384 at scale 2^40, used by the pilot scripts) and the
web sets, chosen by benchmarks/sweep.py. The weighted sum needs 1 level (or none with a
two-prime chain); the cubic sigmoid needs 3, which fits N = 8192 only with scales smaller than 2^40.
"""
from __future__ import annotations

SCALE_BITS = 40
SCALE = 2.0 ** SCALE_BITS

PARAM_SETS = {
    # Full pipeline: weighted sum + cubic sigmoid (PR2 Table 5 parameters).
    "n16384_depth4": {"poly_modulus_degree": 16384,
                      "coeff_mod_bit_sizes": [60, 40, 40, 40, 40, 60]},
    # Weighted sum only (logit returned, sigmoid applied by the client after decrypting).
    "n8192_depth2": {"poly_modulus_degree": 8192,
                     "coeff_mod_bit_sizes": [60, 40, 40, 60]},
    # ---- sets used by the web system, chosen by benchmarks/sweep.py (smallest passing per layout:
    # 100% decision match on both datasets and score error <= 0.01) ----
    # Main method (browser sigmoid), one ciphertext per feature.
    "web_logit": {"poly_modulus_degree": 4096, "coeff_mod_bit_sizes": [46, 46]},
    # Add-on mode (server cubic).
    "web_poly": {"poly_modulus_degree": 8192, "coeff_mod_bit_sizes": [31, 26, 26, 26, 31]},
}
DEFAULT_PARAM_SET = "n16384_depth4"      # pilot setting (used by the pilot scripts)
WEB_SCALE_BITS = {"web_logit": 26, "web_poly": 26}
WEB_SETS = tuple(WEB_SCALE_BITS)


def scale_bits_for(param_set: str) -> int:
    return WEB_SCALE_BITS.get(param_set, SCALE_BITS)


def approved_parameters() -> set[tuple[int, tuple[int, ...]]]:
    """The exact (N, modulus chain bit sizes) pairs the web service accepts (threat model T7)."""
    return {(PARAM_SETS[k]["poly_modulus_degree"], tuple(PARAM_SETS[k]["coeff_mod_bit_sizes"]))
            for k in WEB_SETS}

# Upper bound on the rotation keys for the packed layout (only the needed steps).
MAX_GALOIS_KEY_BYTES = 16_000_000


def rotation_steps(n_features: int) -> list[int]:
    """Slot rotations needed to add n_features packed values: 1, 2, 4, ... < n_features."""
    steps, k = [], 1
    while k < n_features:
        steps.append(k)
        k *= 2
    return steps


# Upper bound on one serialized ciphertext (bytes) accepted by the service. A fresh
# N=16384, 5-prime ciphertext saved without compression is about 1.3 MB.
MAX_CIPHERTEXT_BYTES = 2_000_000
MAX_RELIN_KEY_BYTES = 12_000_000


def allowed_degrees() -> set[int]:
    return {p["poly_modulus_degree"] for p in PARAM_SETS.values()}
