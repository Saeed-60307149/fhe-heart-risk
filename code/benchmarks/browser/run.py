"""Runs the browser benchmark: serves bench.html, runs the production server code for each request,
launches a headless Chromium browser (Edge or Chrome) and saves the results.

    python benchmarks/browser/run.py --configs benchmarks/browser/configs.json \
        --out results/benchmarks/browser.json
"""
import argparse
import base64
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C  # noqa: E402

from fhe_heart import params as P  # noqa: E402
from fhe_heart.seal_server import SealServer  # noqa: E402

P.PARAM_SETS["_bench4096"] = {"poly_modulus_degree": 4096, "coeff_mod_bit_sizes": [36, 36, 37]}
P.MAX_GALOIS_KEY_BYTES = 600_000_000
P.MAX_RELIN_KEY_BYTES = 100_000_000
DIST = os.path.join(C.CODE_DIR, "backend", "node_modules", "node-seal", "dist")
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    configs = json.load(open(args.configs))
    problems = {d: C.load_problem(d) for d in C.DATASETS}
    job = {"configs": configs, "datasets": {
        d: {"X": p["X"].tolist(), "y": p["y"].tolist(), "p": p["p"].tolist()} for d, p in problems.items()}}
    by_id = {c["id"]: c for c in configs}
    keys, lock, done = {}, threading.Lock(), threading.Event()
    final = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, ctype="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path in ("/", "/bench.html"):
                return self.send(200, open(os.path.join(HERE, "bench.html"), "rb").read(), "text/html")
            if path == "/bench.js":
                return self.send(200, open(os.path.join(HERE, "bench.js"), "rb").read(), "text/javascript")
            if path == "/job":
                return self.send(200, json.dumps(job).encode())
            if path.startswith("/vendor/"):
                f = os.path.join(DIST, os.path.basename(path))
                if os.path.isfile(f):
                    ctype = "application/wasm" if f.endswith(".wasm") else "text/javascript"
                    return self.send(200, open(f, "rb").read(), ctype)
            self.send(404, b"{}")

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            try:
                if self.path == "/keys":
                    keys[(body["cfg"], body["dataset"])] = {
                        k: (base64.b64decode(body[k]) if body[k] else None) for k in ("parms", "galois", "relin")}
                    return self.send(200, b"{}")
                if self.path == "/infer":
                    cfg, pr = by_id[body["cfg"]], problems[body["dataset"]]
                    k = keys[(body["cfg"], body["dataset"])]
                    with lock:
                        res = SealServer(k["parms"]).infer(
                            [base64.b64decode(c) for c in body["ciphertexts"]], list(pr["w"]), pr["b"],
                            pr["poly"] if cfg["sigmoid"] == "server_cubic" else None, k["relin"],
                            layout=cfg["layout"], galois_bytes=k["galois"], trim=cfg["trim"])
                    return self.send(200, json.dumps({
                        "encrypted_result": base64.b64encode(res.ciphertext).decode(),
                        "compute_ms": res.timings_ms["compute_ms"],
                        "total_ms": sum(res.timings_ms.values())}).encode())
                if self.path == "/progress":
                    print(body["text"], flush=True)
                    if body["text"].startswith("FATAL"):
                        done.set()
                    return self.send(200, b"{}")
                if self.path == "/done":
                    final.update(body)
                    self.send(200, b"{}")
                    done.set()
                    return
            except Exception as exc:  # report to the page
                return self.send(500, json.dumps({"error": f"{type(exc).__name__}: {exc}"}).encode())
            self.send(404, b"{}")

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    exe = next(b for b in BROWSERS if os.path.exists(b))
    profile = tempfile.mkdtemp(prefix="bench-browser-")
    proc = subprocess.Popen([exe, "--headless=new", "--disable-gpu", "--no-first-run",
                             "--disable-background-timer-throttling", f"--user-data-dir={profile}",
                             "--remote-debugging-port=0", f"http://127.0.0.1:{args.port}/"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        done.wait(timeout=7200)
    finally:
        proc.terminate()
        server.shutdown()
        time.sleep(1)
        shutil.rmtree(profile, ignore_errors=True)
    if not final:
        sys.exit("benchmark did not finish")
    final["environment"] = {"browser": final.pop("userAgent"), "python": platform.python_version(),
                            "platform": platform.platform(), "processor": platform.processor(),
                            "note": "client and server on the same computer; no network delay"}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(final, fh, indent=1)
    print("saved", args.out)


if __name__ == "__main__":
    main()
