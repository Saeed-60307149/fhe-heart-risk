#!/usr/bin/env python3
"""Encrypted inference pilot: cost and accuracy of both ciphertext layouts
(PR2 objective 4, Table 5; Capstone 2 first design decision).

Layouts
  packed       TenSEAL CKKSVector, all features in 1 ciphertext, dot product.
               Needs Galois (rotation) keys.                          [PR2 Table 5]
  per_feature  raw SEAL API, 1 ciphertext per feature, the same server code as the
               web prototype (fhe_heart.seal_server). Needs only relinearization keys
               for the cubic sigmoid; none at all if only the logit is returned.

For every test patient: encrypt -> encrypted weighted sum + cubic sigmoid -> decrypt,
then compare with the plaintext model (accuracy, decision match, max error).

Usage (from code/, after train_baseline.py and fit_sigmoid.py):
    python pilots/tenseal-pilot/pilot.py --dataset cleveland
    python pilots/tenseal-pilot/pilot.py --dataset edinburgh --layout packed --limit 100
Output: results/<dataset>/pilot_<layout>.json
"""
import argparse
import json
import os
import platform
import statistics
import sys
import time

import numpy as np

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import pilot_paths as PP  # noqa: E402

from fhe_heart import ckks_packed as CP  # noqa: E402
from fhe_heart import data as D  # noqa: E402
from fhe_heart import metrics as M  # noqa: E402
from fhe_heart import model as ML  # noqa: E402
from fhe_heart import params as P  # noqa: E402
from fhe_heart import sigmoid as S  # noqa: E402
from fhe_heart.seal_client import SealClient  # noqa: E402
from fhe_heart.seal_server import SealServer  # noqa: E402

MB = 1024 * 1024


def summarise(xs):
    return {"mean": statistics.fmean(xs), "median": statistics.median(xs),
            "min": min(xs), "max": max(xs)}


def run_packed(X, w, b, poly):
    t0 = time.perf_counter()
    ctx = CP.make_context(galois=True)
    keygen_s = time.perf_counter() - t0
    sizes = CP.key_sizes_bytes(ctx)
    enc_ms, inf_ms, dec_ms, outs, ct_bytes = [], [], [], [], None
    for x in X:
        t0 = time.perf_counter(); ex = CP.encrypt(ctx, x); t1 = time.perf_counter()
        er = CP.infer(ex, w, b, poly); t2 = time.perf_counter()
        outs.append(er.decrypt()[0]); t3 = time.perf_counter()
        enc_ms.append((t1 - t0) * 1000); inf_ms.append((t2 - t1) * 1000); dec_ms.append((t3 - t2) * 1000)
        if ct_bytes is None:
            ct_bytes = len(ex.serialize())
    return np.array(outs), {
        "keygen_s": keygen_s,
        "encrypt_ms": summarise(enc_ms), "inference_ms": summarise(inf_ms), "decrypt_ms": summarise(dec_ms),
        "ciphertext_per_patient_MB": ct_bytes / MB,
        "public_context_MB": sizes["public_context"] / MB,
        "context_with_secret_key_MB": sizes["context_with_secret_key"] / MB,
        "galois_keys_MB": sizes["galois_keys"] / MB,
    }


def run_per_feature(X, w, b, poly):
    t0 = time.perf_counter()
    client = SealClient.create()
    rk = client.relin_keys_bytes()
    keygen_s = time.perf_counter() - t0
    server = SealServer(client.parms_bytes())
    enc_ms, inf_ms, dec_ms, outs, ct_total = [], [], [], [], None
    for x in X:
        t0 = time.perf_counter(); cts = client.encrypt_features(x); t1 = time.perf_counter()
        res = server.infer(cts, list(w), b, poly, rk); t2 = time.perf_counter()
        outs.append(client.decrypt_scalar(res.ciphertext)); t3 = time.perf_counter()
        enc_ms.append((t1 - t0) * 1000); inf_ms.append((t2 - t1) * 1000); dec_ms.append((t3 - t2) * 1000)
        if ct_total is None:
            ct_total = sum(len(c) for c in cts)
            result_bytes = len(res.ciphertext)
    return np.array(outs), {
        "keygen_s": keygen_s,
        "encrypt_ms": summarise(enc_ms), "inference_ms": summarise(inf_ms), "decrypt_ms": summarise(dec_ms),
        "ciphertexts_per_patient_MB": ct_total / MB,
        "result_ciphertext_MB": result_bytes / MB,
        "parms_KB": len(client.parms_bytes()) / 1024,
        "relin_keys_MB": len(rk) / MB,
        "galois_keys_MB": 0.0,
        "note": "inference_ms includes loading the ciphertexts from bytes (server path)",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(D.LOADERS), default="cleveland")
    ap.add_argument("--layout", choices=["packed", "per_feature", "both"], default="both")
    ap.add_argument("--limit", type=int, default=0, help="only the first N test patients")
    args = ap.parse_args()

    doc = ML.load_weights(PP.model_path(args.dataset))
    if not doc.get("sigmoid_poly"):
        sys.exit("run pilots/sigmoid/fit_sigmoid.py first (no sigmoid_poly in model file)")
    split = D.split_and_scale(D.load_dataset(args.dataset, PP.RAW_DIR))
    X, y = split.X_test, split.y_test
    if args.limit:
        X, y = X[:args.limit], y[:args.limit]
    w, b = np.array(doc["weights"]), float(doc["bias"])
    poly, thr = doc["sigmoid_poly"]["coeffs_ascending"], doc["threshold"]
    z = X @ w + b
    p_sig, p_poly = M.sigmoid(z), S.poly_eval(poly, z)

    layouts = ["packed", "per_feature"] if args.layout == "both" else [args.layout]
    for layout in layouts:
        fn = run_packed if layout == "packed" else run_per_feature
        enc_out, cost = fn(X, w, b, poly)
        out = {
            "dataset": args.dataset, "layout": layout, "patients": int(len(y)),
            "params": {**P.PARAM_SETS[P.DEFAULT_PARAM_SET], "scale_bits": P.SCALE_BITS,
                       "security": "128-bit (SEAL tc128)"},
            "sigmoid_poly": poly,
            "accuracy": {
                "plain_sigmoid": M.classification_metrics(y, p_sig, thr),
                "plain_poly": M.classification_metrics(y, S.clipped(p_poly), thr),
                "encrypted_poly": M.classification_metrics(y, S.clipped(enc_out), thr),
            },
            "decision_match_encrypted_vs_plain_sigmoid": M.decision_match(enc_out, p_sig, thr),
            "decision_match_encrypted_vs_plain_poly": M.decision_match(enc_out, p_poly, thr),
            "max_abs_error_encrypted_vs_plain_poly": float(np.max(np.abs(enc_out - p_poly))),
            "pass_rq_a_90": M.decision_match(enc_out, p_sig, thr) >= 0.90,
            "meets_expected_95": M.decision_match(enc_out, p_sig, thr) >= 0.95,
            "sigmoid_approx_mae": M.mae(p_sig, p_poly),
            "cost": cost,
            "environment": {"python": platform.python_version(), "machine": platform.machine(),
                            "processor": platform.processor() or "unknown",
                            "platform": platform.platform()},
        }
        path = os.path.join(PP.results_dir(args.dataset), f"pilot_{layout}.json")
        with open(path, "w") as fh:
            json.dump(out, fh, indent=2)
        c = out["cost"]
        print(f"[{layout}] n={len(y)} enc={c['encrypt_ms']['mean']:.1f}ms "
              f"inf={c['inference_ms']['mean']:.1f}ms dec={c['decrypt_ms']['mean']:.1f}ms "
              f"acc_plain={out['accuracy']['plain_sigmoid']['accuracy']:.3f} "
              f"acc_enc={out['accuracy']['encrypted_poly']['accuracy']:.3f} "
              f"match={out['decision_match_encrypted_vs_plain_sigmoid']:.3f} -> {path}")


if __name__ == "__main__":
    main()
