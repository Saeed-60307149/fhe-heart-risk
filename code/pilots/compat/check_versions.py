#!/usr/bin/env python3
"""Check the pinned FHE toolchain before running anything (PR2 section A.4 / C).

Known results (PR2, Weeks 10-11):
  node-seal 7.0.0 (SEAL 4.1.2) ciphertexts load in TenSEAL 0.3.15 and 0.3.16;
  TenSEAL 0.3.17 and 0.3.18 report an incompatible version.
  node-seal 7.0.0 needs Node.js >= 22 (WebAssembly GC + exception handling);
  Node.js 20 cannot load it.
Exit code 1 if something is off.
"""
import json
import os
import shutil
import subprocess
import sys

OK_TENSEAL = {"0.3.15", "0.3.16"}
problems = []

try:
    import tenseal
    v = tenseal.__version__
    print(f"TenSEAL {v}")
    if v not in OK_TENSEAL:
        problems.append(f"TenSEAL {v} is not one of {sorted(OK_TENSEAL)}: pip install tenseal==0.3.16")
except ImportError:
    problems.append("TenSEAL not installed: pip install tenseal==0.3.16")

print(f"Python {sys.version.split()[0]}")
node = shutil.which("node")
if node:
    out = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"Node.js {out}")
    if int(out.lstrip("v").split(".")[0]) < 22:
        problems.append(f"Node.js {out} is too old for node-seal 7.0.0: install Node.js 22+")
else:
    problems.append("Node.js not found (needed for node-seal)")

here = os.path.dirname(os.path.abspath(__file__))
for pkg_dir in ["../node-seal-roundtrip", "../../backend"]:
    p = os.path.normpath(os.path.join(here, pkg_dir, "node_modules", "node-seal", "package.json"))
    if os.path.exists(p):
        ver = json.load(open(p))["version"]
        print(f"node-seal {ver} in {os.path.relpath(os.path.dirname(os.path.dirname(os.path.dirname(p))))}")
        if ver != "7.0.0":
            problems.append(f"node-seal {ver} found; pin 7.0.0")

if problems:
    print("\nPROBLEMS:\n- " + "\n- ".join(problems))
    sys.exit(1)
print("\nToolchain OK")
