#!/usr/bin/env python3
"""Plan B client: encrypt on the patient's own machine with Python (TenSEAL raw SEAL API).

Same privacy guarantee as the browser client (Plan A): the secret key is created here
and never sent. Use it when a browser cannot load node-seal (it needs WebAssembly GC +
exception handling: a current Chrome/Edge/Firefox/Safari, or Node.js 22+).

Usage:
    python fhe_client.py --api http://127.0.0.1:3000 --dataset cleveland \
        --token <bearer> --values 57 1 4 140 241 0 1 123 1 0.2 2 0 7
    python fhe_client.py ... --output logit        # sigmoid applied locally
Values are RAW (unscaled) and in the model's feature order (see GET /api/model/<dataset>).
"""
import argparse
import base64
import json
import math
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "..", "fhe-ml-service")))
from fhe_heart import params as P  # noqa: E402
from fhe_heart.seal_client import SealClient  # noqa: E402


def request(url, token=None, body=None):
    headers = {"content-type": "application/json"}
    if token:
        headers["authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read() or b"{}").get("error", {})
        sys.exit(f"API error {e.code} {err.get('code')}: {err.get('message')}")
    except urllib.error.URLError as e:
        # The API answers 401/429 before reading a large body, which can close the
        # connection while we are still uploading.
        sys.exit(f"connection closed by the API ({e.reason}). Usual causes: wrong or missing "
                 f"--token (401) or rate limit (429). Is the API running at the --api URL?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:3000")
    ap.add_argument("--dataset", default="cleveland")
    ap.add_argument("--token", default=os.environ.get("API_TOKEN"))
    ap.add_argument("--values", nargs="+", type=float, required=True)
    ap.add_argument("--output", choices=["probability_poly", "logit"], default="probability_poly")
    a = ap.parse_args()

    meta = request(f"{a.api}/api/model/{a.dataset}")
    n = meta["n_features"]
    if len(a.values) != n:
        sys.exit(f"expected {n} values in this order: {', '.join(meta['feature_names'])}")
    scaled = [(v - m) / s for v, m, s in zip(a.values, meta["scaler_mean"], meta["scaler_scale"])]
    param_set = next(k for k, v in P.PARAM_SETS.items() if v == meta["params"])

    t0 = time.perf_counter()
    client = SealClient.create(param_set)
    cts = client.encrypt_features(scaled)
    output = a.output if meta.get("supports_probability_poly") else "logit"
    rk = client.relin_keys_bytes() if output == "probability_poly" else None
    t1 = time.perf_counter()
    body = {"dataset": a.dataset, "parms": base64.b64encode(client.parms_bytes()).decode(),
            "ciphertexts": [base64.b64encode(c).decode() for c in cts],
            "relin_keys": base64.b64encode(rk).decode() if rk else None, "output": output}
    res = request(f"{a.api}/api/predict", a.token, body)
    t2 = time.perf_counter()
    v = client.decrypt_scalar(base64.b64decode(res["encrypted_result"]))
    prob = 1 / (1 + math.exp(-v)) if res["output"] == "logit" else min(1.0, max(0.0, v))
    risk = "HIGHER RISK" if prob >= res.get("threshold", 0.5) else "LOWER RISK"
    print(f"{risk}  (probability {prob:.3f}; output={res['output']})")
    print(f"encrypt {1000 * (t1 - t0):.0f} ms, request {1000 * (t2 - t1):.0f} ms, "
          f"server compute {res['timings_ms'].get('compute_ms')} ms")


if __name__ == "__main__":
    main()
