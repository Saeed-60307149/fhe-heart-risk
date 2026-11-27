// End-to-end: node-seal (client) -> Node API -> Python FHE service -> node-seal decrypt.
// Runs only when a real FHE service is up:  E2E_FHE_URL=http://127.0.0.1:8001 npm test
// (the service must have a model for E2E_DATASET, default "cleveland").
import assert from 'node:assert/strict';
import { test } from 'node:test';
import initialize from 'node-seal';

import { start } from './helpers.js';

const FHE = process.env.E2E_FHE_URL;
const DATASET = process.env.E2E_DATASET ?? 'cleveland';

test('browser-style round trip through the API', { skip: !FHE && 'set E2E_FHE_URL to run' }, async () => {
  const srv = await start({ fheUrl: FHE, fheToken: process.env.FHE_SERVICE_TOKEN ?? '', authDisabled: true });
  try {
    const meta = await (await fetch(`${srv.base}/api/model/${DATASET}`)).json();
    const seal = await initialize();
    const x = Array.from({ length: meta.n_features }, (_, i) => ((i % 3) - 1) * 0.5);
    const modes = meta.supports_probability_poly ? ['logit', 'probability_poly'] : ['logit'];
    for (const output of modes) {
      const poly = output === 'probability_poly';
      const params = poly ? meta.poly_params : meta.params;
      const scale = 2 ** (poly ? meta.poly_scale_bits : meta.scale_bits);
      const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
      parms.setPolyModulusDegree(params.poly_modulus_degree);
      parms.setCoeffModulus(seal.CoeffModulus.Create(params.poly_modulus_degree, Int32Array.from(params.coeff_mod_bit_sizes)));
      const ctx = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
      const kg = new seal.KeyGenerator(ctx);
      const sk = kg.secretKey();
      const enc = new seal.Encryptor(ctx, kg.createPublicKey(), sk);
      const encoder = new seal.CKKSEncoder(ctx);
      const zstd = seal.ComprModeType.zstd;
      const cts = x.map((v) => {
        const pt = new seal.Plaintext(); encoder.encode(Float64Array.from([v]), scale, pt);
        return enc.encryptSymmetricSerializable(pt).saveToBase64(zstd);
      });
      const relin = poly ? kg.createRelinKeysSerializable().saveToBase64(zstd) : null;
      const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ dataset: DATASET, parms: parms.saveToBase64(seal.ComprModeType.none), ciphertexts: cts, relin_keys: relin, output }) });
      assert.equal(r.status, 200, await r.clone().text());
      const j = await r.json();
      const ct = new seal.Ciphertext(); ct.loadFromBase64(ctx, j.encrypted_result);
      const pt = new seal.Plaintext(); new seal.Decryptor(ctx, sk).decrypt(ct, pt);
      const v = encoder.decodeFloat64(pt)[0];
      assert.ok(Number.isFinite(v));
      if (poly) assert.ok(v > -0.2 && v < 1.2, `poly output ${v} out of range`);
      else assert.ok(Math.abs(v) < 100, `score ${v} out of range`);
    }
  } finally { await srv.close(); }
});
