"""Parameter sweep (Track 1, rows 1, 2, 4, 7): which CKKS settings keep every decision?

Python client + the real server code (fhe_heart.seal_server), every test patient of both
datasets. Pass = 100% decision match AND max |encrypted - plain| score error <= 0.01.
Output: results/benchmarks/sweep.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

from tenseal import sealapi as seal  # noqa: E402
from fhe_heart import metrics as M  # noqa: E402
from fhe_heart import params as P  # noqa: E402
from fhe_heart import sigmoid as S  # noqa: E402
from fhe_heart.seal_server import SealServer, _load, _save  # noqa: E402

P.PARAM_SETS["_bench4096"] = {"poly_modulus_degree": 4096, "coeff_mod_bit_sizes": [36, 36, 37]}
P.MAX_GALOIS_KEY_BYTES = 400_000_000
P.MAX_RELIN_KEY_BYTES = 100_000_000

LINEAR = [
    (16384, [60, 40, 40, 40, 40, 60], 40), (16384, [60, 40, 60], 40), (16384, [40, 30, 40], 30),
    (8192, [60, 40, 60], 40), (8192, [50, 30, 50], 30), (8192, [40, 30, 40], 30),
    (8192, [40, 26, 40], 26), (8192, [36, 24, 36], 24), (8192, [31, 26, 31], 26),
    (8192, [30, 22, 30], 22), (8192, [60, 60], 40), (8192, [50, 50], 30), (8192, [40, 40], 25),
    (8192, [31, 26, 26, 26, 26, 26, 26, 31], 26),
    (4096, [40, 26, 40], 26), (4096, [36, 30, 36], 30), (4096, [36, 25, 36], 25),
    (4096, [30, 20, 30], 20), (4096, [54, 54], 35), (4096, [54, 54], 30), (4096, [50, 50], 30),
    (4096, [46, 46], 26), (4096, [40, 40], 24),
]
CUBIC = [
    (16384, [60, 40, 40, 40, 40, 60], 40), (8192, [50, 38, 38, 38, 50], 38),
    (8192, [40, 30, 30, 30, 40], 30), (8192, [31, 26, 26, 26, 31], 26),
]


def run(problem, N, chain, bits, layout, cubic):
    parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
    parms.set_poly_modulus_degree(N)
    parms.set_coeff_modulus(seal.CoeffModulus.Create(N, chain))
    ctx = seal.SEALContext(parms, True, seal.SEC_LEVEL_TYPE.TC128)
    if not ctx.parameters_set():
        raise ValueError(ctx.parameters_error_message())
    kg = seal.KeyGenerator(ctx)
    pk = seal.PublicKey()
    kg.create_public_key(pk)
    enc, encoder = seal.Encryptor(ctx, pk), seal.CKKSEncoder(ctx)
    dec = seal.Decryptor(ctx, kg.secret_key())
    gk_bytes = rk_bytes = None
    if layout == "packed":
        gk = seal.GaloisKeys()
        steps = P.rotation_steps(len(problem["w"]))
        galois_tool_elts = [pow(3, s, 2 * N) for s in steps]  # Galois element for a left rotation
        kg.create_galois_keys(galois_tool_elts, gk)
        gk_bytes = _save(gk)
    if cubic:
        rk = seal.RelinKeys()
        kg.create_relin_keys(rk)
        rk_bytes = _save(rk)
    server = SealServer(_save(parms))
    scale = 2.0 ** bits
    outs, ct_size, res_size = [], 0, 0
    for x in problem["X"]:
        groups = [[float(v) for v in x]] if layout == "packed" else [[float(v)] for v in x]
        blobs = []
        for g in groups:
            pt, ct = seal.Plaintext(), seal.Ciphertext()
            encoder.encode(g, scale, pt)
            enc.encrypt(pt, ct)
            blobs.append(_save(ct))
        res = server.infer(blobs, list(problem["w"]), problem["b"], problem["poly"] if cubic else None,
                           rk_bytes, layout=layout, galois_bytes=gk_bytes)
        ct, pt = seal.Ciphertext(), seal.Plaintext()
        _load(ct, res.ciphertext, ctx)
        dec.decrypt(ct, pt)
        outs.append(float(encoder.decode_double(pt)[0]))
        ct_size, res_size = sum(map(len, blobs)), len(res.ciphertext)
    outs = np.array(outs)
    if cubic:
        expected = S.poly_eval(problem["poly"], problem["z"])
        match = M.decision_match(outs, problem["p"])
    else:
        expected = problem["z"]
        match = float(np.mean((outs >= 0) == (problem["z"] >= 0)))
    return {"decision_match": match, "max_abs_error": float(np.max(np.abs(outs - expected))),
            "upload_bytes_zstd": ct_size, "result_bytes": res_size,
            "rotation_key_bytes": len(gk_bytes) if gk_bytes else 0,
            "relin_key_bytes": len(rk_bytes) if rk_bytes else 0}


def main():
    problems = [C.load_problem(d) for d in C.DATASETS]
    rows = []
    for cubic, table in ((False, LINEAR), (True, CUBIC)):
        for N, chain, bits in table:
            for layout in ("per_feature", "packed"):
                if layout == "packed" and len(chain) == 2 and N == 4096 and bits > 33:
                    pass
                row = {"N": N, "chain": chain, "scale_bits": bits, "layout": layout,
                       "sigmoid": "server_cubic" if cubic else "browser", "datasets": {}}
                try:
                    for pr in problems:
                        row["datasets"][pr["name"]] = run(pr, N, chain, bits, layout, cubic)
                    d = row["datasets"].values()
                    row["pass"] = all(r["decision_match"] == 1.0 and r["max_abs_error"] <= C.MAX_SCORE_ERROR for r in d)
                except Exception as exc:  # setting rejected by SEAL or cannot compute
                    row["pass"] = False
                    row["error"] = str(exc)[:200]
                rows.append(row)
                c = row["datasets"].get("cleveland", {})
                e = row["datasets"].get("edinburgh", {})
                print(f"{'cubic ' if cubic else 'linear'} N={N:5d} {str(chain):34s} s={bits} {layout:11s} "
                      f"pass={row['pass']!s:5s} match={c.get('decision_match', '-')}/{e.get('decision_match', '-')} "
                      f"err={c.get('max_abs_error', float('nan')):.1e}/{e.get('max_abs_error', float('nan')):.1e} "
                      f"up={c.get('upload_bytes_zstd', 0) / 1024:.0f}KB gk={c.get('rotation_key_bytes', 0) / 1024:.0f}KB "
                      f"{row.get('error', '')}", flush=True)
    os.makedirs(C.OUT_DIR, exist_ok=True)
    with open(os.path.join(C.OUT_DIR, "sweep.json"), "w") as fh:
        json.dump({"criterion": {"decision_match": 1.0, "max_abs_error": C.MAX_SCORE_ERROR}, "rows": rows}, fh, indent=1)


if __name__ == "__main__":
    main()
