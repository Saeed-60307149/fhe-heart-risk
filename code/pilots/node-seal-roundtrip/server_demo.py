#!/usr/bin/env python3
"""TenSEAL server side: encrypted weighted sum on node-seal ciphertexts.

Loads the ciphertexts produced by encrypt_demo.mjs (node-seal), computes
z = sum_j (ct_j * w_j) + bias with the raw SEAL API, saves the result.
"""
from tenseal import sealapi
import base64, os, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def b64_to_file(name):
    raw = base64.b64decode(open(name).read().strip())
    os.makedirs("out", exist_ok=True)
    path = os.path.join("out", name.replace(".b64", ".seal"))
    open(path, "wb").write(raw)
    return path

parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.CKKS)
parms.load(b64_to_file("demo_parms.b64"))
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)

sk = sealapi.SecretKey()  # loaded only for the demo sanity check
sk.load(ctx, b64_to_file("demo_sk.b64"))

W = [0.5, -1.0, 2.0, 0.25]
BIAS = 0.0

enc = sealapi.CKKSEncoder(ctx)
ev = sealapi.Evaluator(ctx)
dec = sealapi.Decryptor(ctx, sk)

cts = []
for j in range(len(W)):
    ct = sealapi.Ciphertext()
    ct.load(ctx, b64_to_file(f"demo_ct_{j}.b64"))
    cts.append(ct)

t0 = time.perf_counter()
acc = None
for j, ct in enumerate(cts):
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

# sanity check on server (demo only - in production the client decrypts)
pt = sealapi.Plaintext()
dec.decrypt(acc, pt)
z = enc.decode_double(pt)[0]
expected = sum(v * w for v, w in zip([1.5, -2.25, 3.75, 4.0], W)) + BIAS
print(f"encrypted inference: {inf_ms:.1f} ms, server-side check z = {z:.4f} (expected {expected})")

acc.save(os.path.join("out", "demo_z.seal"))
print("saved out/demo_z.seal")
