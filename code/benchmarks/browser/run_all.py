"""Runs every setting in configs.json in its own fresh browser (long single sessions can crash),
retries once, and saves the merged results after each setting.

    python benchmarks/browser/run_all.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "results", "benchmarks", "browser.json")


def keep_awake():
    """Windows: stop idle sleep while the benchmark runs (sleep freezes the browser and spoils
    timings). Ends automatically when this process exits. Closing the lid still sleeps."""
    if os.name == "nt":
        import ctypes
        es_continuous, es_system, es_display = 0x80000000, 0x00000001, 0x00000002
        ctypes.windll.kernel32.SetThreadExecutionState(es_continuous | es_system | es_display)


def main():
    keep_awake()
    configs = json.load(open(os.path.join(HERE, "configs.json")))
    merged = {"results": [], "environment": None, "failed": []}
    if os.path.exists(OUT):
        merged = json.load(open(OUT))
        merged["failed"] = []
    done = {r["id"] for r in merged["results"]}
    tmp = tempfile.mkdtemp(prefix="bench-")
    for n, cfg in enumerate(configs, 1):
        if cfg["id"] in done:
            continue
        one, res = os.path.join(tmp, "one.json"), os.path.join(tmp, f"{cfg['id']}.json")
        json.dump([cfg], open(one, "w"))
        ok = False
        for attempt in (1, 2):
            try:
                # output goes to a file: on Windows the browser's child processes can keep a pipe open
                with open(os.path.join(tmp, f"{cfg['id']}.log"), "w") as log:
                    p = subprocess.run([sys.executable, "-u", os.path.join(HERE, "run.py"), "--configs", one,
                                        "--out", res], stdout=log, stderr=log, timeout=1500)
                ok = p.returncode == 0 and os.path.exists(res)
            except subprocess.TimeoutExpired:
                ok = False
            if ok:
                break
            print(f"[{n}/{len(configs)}] {cfg['id']} attempt {attempt} failed", flush=True)
        if not ok:
            merged["failed"].append(cfg["id"])
            continue
        data = json.load(open(res))
        entry = data["results"][0]
        merged["results"].append(entry)
        merged["environment"] = data["environment"]
        with open(OUT, "w") as fh:
            json.dump(merged, fh, indent=1)
        c = entry["datasets"]["cleveland"]
        print(f"[{n}/{len(configs)}] {cfg['id']}: " + (c.get("error") or
              f"match={c['decision_match']} upload={c['upload_bytes'] / 1024:.0f}KB enc={c['encrypt_ms']:.0f}ms "
              f"server={c['server_ms']:.0f}ms server_total={c['server_total_ms']:.0f}ms dec={c['decrypt_ms']:.1f}ms"), flush=True)
    print("ALL DONE; failed:", merged["failed"], flush=True)


if __name__ == "__main__":
    main()
