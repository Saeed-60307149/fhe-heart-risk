"""Browser benchmark settings (Track 1 rows). Settings come from sweep.py: for each row and layout,
the smallest passing setting. Writes configs.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = (16384, [60, 40, 40, 40, 40, 60], 40)
HAQ = (8192, [31, 26, 26, 26, 26, 26, 26, 31], 26)


def cfg(i, row, setting, layout, sigmoid="browser", encryption="public", compr="zstd",
        trim=True, full_galois=False, max_patients=75, note=""):
    N, chain, bits = setting
    return {"id": i, "row": row, "N": N, "chain": chain, "scale_bits": bits, "layout": layout,
            "sigmoid": sigmoid, "encryption": encryption, "compr": compr, "trim": trim,
            "full_galois": full_galois, "max_patients": max_patients, "note": note}


def smallest(sweep, N, layout, sigmoid="browser"):
    ok = [r for r in sweep if r["pass"] and r["N"] == N and r["layout"] == layout and r["sigmoid"] == sigmoid]
    best = min(ok, key=lambda r: (r["datasets"]["cleveland"]["upload_bytes_zstd"], len(r["chain"])))
    return best["N"], best["chain"], best["scale_bits"]


def main():
    sweep = json.load(open(os.path.join(HERE, "..", "..", "results", "benchmarks", "sweep.json")))["rows"]
    out = []
    for lay, tag in (("per_feature", "pf"), ("packed", "pk")):
        s16 = (16384, [40, 30, 40], 30)
        s8, s4 = smallest(sweep, 8192, lay), smallest(sweep, 4096, lay)
        out += [
            cfg(f"row0-{tag}", "0", REF, lay, compr="none", note="reference, as the first web client (no compression)"),
            cfg(f"row1-{tag}", "1", s16, lay, note="shorter chain, smaller scale at N=16384"),
            cfg(f"row2-{tag}", "2", s8, lay, note="smallest passing at N=8192"),
            cfg(f"row3-none-{tag}", "3", s4, lay, compr="none", note="N=4096, no compression"),
            cfg(f"row3-zlib-{tag}", "3", s4, lay, compr="zlib", note="N=4096, zlib"),
            cfg(f"row4-{tag}", "4", s4, lay, note="smallest passing at N=4096, zstd"),
            cfg(f"row5-{tag}", "5", s4, lay, encryption="seeded", note="row 4 + seeded encryption"),
            cfg(f"row7-ref-{tag}", "7", REF, lay, sigmoid="server_cubic", compr="none",
                note="add-on: server cubic at the reference setting"),
        ]
        cub = [r for r in sweep if r["pass"] and r["N"] == 8192 and r["layout"] == lay and r["sigmoid"] == "server_cubic"]
        if cub:
            b = min(cub, key=lambda r: r["datasets"]["cleveland"]["upload_bytes_zstd"])
            out.append(cfg(f"row7-8192-{tag}", "7", (8192, b["chain"], b["scale_bits"]), lay,
                           sigmoid="server_cubic", note="add-on: server cubic at N=8192"))
    out += [
        cfg("row6-notrim-pk", "6", smallest(sweep, 4096, "packed"), "packed", trim=False,
            encryption="seeded", note="response NOT trimmed, to measure the effect of trimming"),
        cfg("rowH-pf", "H", HAQ, "per_feature", trim=False, note="Haq-style setting, per-feature"),
        cfg("rowH-pk", "H", HAQ, "packed", trim=False, full_galois=True, max_patients=20,
            note="Haq-style setting, packed, full default rotation keys"),
    ]
    with open(os.path.join(HERE, "configs.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    for c in out:
        print(c["id"], c["N"], c["chain"], c["scale_bits"], c["layout"], c["sigmoid"], c["encryption"], c["compr"])


if __name__ == "__main__":
    main()
