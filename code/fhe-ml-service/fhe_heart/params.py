"""CKKS parameter sets - the single source of truth for Python and JavaScript.

The browser does not hard-code these: it reads them from GET /api/model/{dataset}
(field "params"), so a change here reaches the client automatically. The node-seal
pilot scripts in code/pilots/node-seal-roundtrip/ use the same numbers by hand.

Why N = 16384 for the full pipeline: the weighted sum uses 1 level and the cubic
sigmoid uses 2 more (z^2 and c3*z in parallel, then their product). 3 levels plus the
60-bit first and special primes need more than the 218 bits allowed at N = 8192
(128-bit security, HE standard), so N = 16384 (max 438 bits) is required. This is the
"polynomial degree required for the cubic sigmoid (16,384)" in PR2 section C.
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
}
DEFAULT_PARAM_SET = "n16384_depth4"

# Upper bound on one serialized ciphertext (bytes) accepted by the service. A fresh
# N=16384, 5-prime ciphertext saved without compression is about 1.3 MB.
MAX_CIPHERTEXT_BYTES = 2_000_000
MAX_RELIN_KEY_BYTES = 12_000_000


def allowed_degrees() -> set[int]:
    return {p["poly_modulus_degree"] for p in PARAM_SETS.values()}
