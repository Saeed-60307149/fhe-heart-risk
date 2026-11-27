"""Track 2 cost: encrypted inference of the square-activation MLP (candidate M4), next to LR.

Same fixed split as the pilot. Depth 3 (hidden sum, square, output sum), browser-style output
(encrypted score; the sign gives the decision). Smallest working setting is searched from a short
list; per_feature and packed layouts. Output: results/benchmarks/mlp_cost.json
"""
import json
import os
import sys
import time

import numpy as np
from sklearn.model_selection import GridSearchCV, StratifiedKFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
from mlp import SquareMLP  # noqa: E402

from tenseal import sealapi as seal  # noqa: E402
from fhe_heart import params as P  # noqa: E402
from fhe_heart.seal_server import _load, _save  # noqa: E402

# smallest first
SETTINGS = [(8192, [34, 25, 25, 25, 34], 25), (8192, [36, 28, 28, 28, 36], 28),
            (8192, [40, 30, 30, 30, 40], 30), (8192, [50, 38, 38, 38, 50], 38),
            (16384, [60, 40, 40, 40, 60], 40)]


def evaluate(problem, m, N, chain, bits, layout):
    parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
    parms.set_poly_modulus_degree(N)
    parms.set_coeff_modulus(seal.CoeffModulus.Create(N, chain))
    ctx = seal.SEALContext(parms, True, seal.SEC_LEVEL_TYPE.TC128)
    kg = seal.KeyGenerator(ctx)
    pk = seal.PublicKey()
    kg.create_public_key(pk)
    enc, encoder, ev = seal.Encryptor(ctx, pk), seal.CKKSEncoder(ctx), seal.Evaluator(ctx)
    dec = seal.Decryptor(ctx, kg.secret_key())
    rk = seal.RelinKeys()
    kg.create_relin_keys(rk)
    d = problem["X"].shape[1]
    gk = None
    gk_bytes = 0
    if layout == "packed":
        gk = seal.GaloisKeys()
        kg.create_galois_keys([pow(3, s, 2 * N) for s in P.rotation_steps(d)], gk)
        gk_bytes = len(_save(gk))
    scale = 2.0 ** bits

    def prime(ct):
        return float(ctx.get_context_data(ct.parms_id()).parms().coeff_modulus()[-1].value())

    def encode(value, ct, s):
        pt = seal.Plaintext()
        encoder.encode(value, ct.parms_id(), s, pt)
        return pt

    def accumulate(acc, term):
        if acc is None:
            return term
        ev.add_inplace(acc, term)
        return acc

    outs, server_ms, upload = [], [], 0
    for x in problem["X"]:
        groups = [[float(v) for v in x]] if layout == "packed" else [[float(v)] * 1 for v in x]
        cts = []
        for g in groups:
            pt, ct = seal.Plaintext(), seal.Ciphertext()
            encoder.encode(g if layout == "packed" else g[0], scale, pt)
            enc.encrypt(pt, ct)
            cts.append(ct)
        upload = sum(len(_save(c)) for c in cts)
        t0 = time.perf_counter()
        total = None
        for j in range(m.hidden):
            if layout == "packed":
                col = [float(v) for v in m.W1_[:, j]] + [0.0] * (encoder.slot_count() - d)
                h = seal.Ciphertext()
                ev.multiply_plain(cts[0], encode(col, cts[0], prime(cts[0])), h)
                ev.rescale_to_next_inplace(h)
                h.scale = scale
                for step in P.rotation_steps(d):
                    rot = seal.Ciphertext()
                    ev.rotate_vector(h, step, gk, rot)
                    ev.add_inplace(h, rot)
            else:
                h = None
                for i, ct in enumerate(cts):
                    term = seal.Ciphertext()
                    ev.multiply_plain(ct, encode(float(m.W1_[i, j]), ct, prime(ct)), term)
                    h = accumulate(h, term)
                ev.rescale_to_next_inplace(h)
                h.scale = scale
            ev.add_plain_inplace(h, encode(float(m.b1_[j]), h, h.scale))
            sq = seal.Ciphertext()
            ev.square(h, sq)
            ev.relinearize_inplace(sq, rk)
            ev.rescale_to_next_inplace(sq)
            sq_scale = sq.scale
            term = seal.Ciphertext()
            q = prime(sq)
            ev.multiply_plain(sq, encode(float(m.w2_[j]), sq, scale * q / sq_scale), term)
            ev.rescale_to_next_inplace(term)
            term.scale = scale
            total = accumulate(total, term)
        ev.add_plain_inplace(total, encode(float(m.b2_), total, total.scale))
        if total.parms_id() != ctx.last_parms_id():
            ev.mod_switch_to_inplace(total, ctx.last_parms_id())
        server_ms.append((time.perf_counter() - t0) * 1000)
        pt = seal.Plaintext()
        dec.decrypt(total, pt)
        outs.append(float(encoder.decode_double(pt)[0]))
    outs = np.array(outs)
    z = m.decision_function(problem["X"])
    return {"decision_match": float(np.mean((outs >= 0) == (z >= 0))),
            "max_abs_error": float(np.max(np.abs(outs - z))), "server_ms_mean": float(np.mean(server_ms)),
            "upload_bytes": upload, "result_bytes": len(_save(total)),
            "relin_key_bytes": len(_save(rk)), "rotation_key_bytes": gk_bytes}


def main():
    out = {"datasets": {}}
    for name in C.DATASETS:
        pr = C.load_problem(name)
        search = GridSearchCV(SquareMLP(hidden=12), {"epochs": [30, 100, 300], "l2": [0.1, 1.0, 3.0]},
                              cv=StratifiedKFold(3, shuffle=True, random_state=42), scoring="accuracy")
        m = search.fit(pr["split"].X_train, pr["split"].y_train).best_estimator_
        entry = {"plain_accuracy_fixed_split": float(np.mean(m.predict(pr["X"]) == pr["y"])),
                 "best_params": search.best_params_, "layouts": {}}
        for layout in ("per_feature", "packed"):
            for N, chain, bits in SETTINGS:
                try:
                    r = evaluate(pr, m, N, chain, bits, layout)
                except Exception as exc:
                    print(name, layout, N, chain, "rejected:", str(exc)[:80], flush=True)
                    continue
                print(name, layout, N, chain, bits, r["decision_match"], f"{r['max_abs_error']:.1e}",
                      f"{r['server_ms_mean']:.0f}ms", f"{r['upload_bytes'] / 1024:.0f}KB", flush=True)
                if r["decision_match"] == 1.0 and r["max_abs_error"] <= C.MAX_SCORE_ERROR:
                    entry["layouts"][layout] = {"N": N, "chain": chain, "scale_bits": bits, **r}
                    break
        out["datasets"][name] = entry
    os.makedirs(C.OUT_DIR, exist_ok=True)
    with open(os.path.join(C.OUT_DIR, "mlp_cost.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
