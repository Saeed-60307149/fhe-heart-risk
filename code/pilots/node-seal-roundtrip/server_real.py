#!/usr/bin/env python3
"""TenSEAL server: encrypted weighted sum on the real node-seal ciphertexts."""
from tenseal import sealapi
import base64, json, os, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def b64_to_file(name):
    raw = base64.b64decode(open(name).read().strip())
    os.makedirs("out", exist_ok=True)
    path = os.path.join("out", name.replace(".b64", ".seal"))
    open(path, "wb").write(raw)
    return path

M = json.load(open("model_patient.json"))
W, BIAS = M["w"], M["b"]

parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.CKKS)
parms.load(b64_to_file("real_parms.b64"))
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)

enc = sealapi.CKKSEncoder(ctx)
ev = sealapi.Evaluator(ctx)

t0 = time.perf_counter()
acc = None
for j in range(len(W)):
    ct = sealapi.Ciphertext()
    ct.load(ctx, b64_to_file(f"real_ct_{j}.b64"))
    wplain = sealapi.Plaintext()
    enc.encode([W[j]], ct.scale, wplain)
    tmp = sealapi.Ciphertext()
    ev.multiply_plain(ct, wplain, tmp)
    ev.rescale_to_next_inplace(tmp)
    if acc is None:
        acc = tmp
    else:
        ev.add_inplace(acc, tmp)
bplain = sealapi.Plaintext()
enc.encode([BIAS], acc.parms_id(), acc.scale, bplain)
ev.add_plain_inplace(acc, bplain)
inf_ms = (time.perf_counter() - t0) * 1000

acc.save(os.path.join("out", "real_z.seal"))
print(f"TenSEAL encrypted inference: {inf_ms:.0f} ms; saved out/real_z.seal")
