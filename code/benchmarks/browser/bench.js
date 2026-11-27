// Browser side of the benchmark: keys, encryption and decryption with node-seal 7.0.0 (WASM),
// exactly like the web client. The server side is the production module fhe_heart.seal_server.
import initialize from '/vendor/index_throws.js';

const log = (t) => { document.getElementById('log').textContent += `${t}\n`; };
const bytesOf = (b64) => Math.floor(b64.length * 3 / 4) - (b64.endsWith('==') ? 2 : b64.endsWith('=') ? 1 : 0);
const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
const median = (a) => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];

async function post(url, body) {
  const text = JSON.stringify(body);
  let r;
  for (let attempt = 1; ; attempt++) {
    try { r = await fetch(url, { method: 'POST', body: text }); break; } catch (err) {
      // a dropped local connection; computation times are measured separately, so retrying is safe
      if (attempt >= 4) throw err;
      await new Promise((ok) => setTimeout(ok, 500 * attempt));
    }
  }
  const j = await r.json();
  if (!r.ok) throw new Error(j.error ?? r.status);
  return j;
}

function steps(n) { const s = []; for (let k = 1; k < n; k *= 2) s.push(k); return s; }

async function runOne(seal, cfg, name, data) {
  const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
  parms.setPolyModulusDegree(cfg.N);
  parms.setCoeffModulus(seal.CoeffModulus.Create(cfg.N, Int32Array.from(cfg.chain)));
  const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
  if (!context.parametersSet()) throw new Error('parameters rejected');
  const compr = seal.ComprModeType[cfg.compr];
  const nFeatures = data.X[0].length;

  let t = performance.now();
  const keyGen = new seal.KeyGenerator(context);
  const secretKey = keyGen.secretKey();
  const publicKey = keyGen.createPublicKey();
  let galois = null;
  let relin = null;
  if (cfg.layout === 'packed') {
    galois = cfg.full_galois ? keyGen.createGaloisKeysSerializable()
      : keyGen.createGaloisKeysSerializableWithSteps(Int32Array.from(steps(nFeatures)));
  }
  if (cfg.sigmoid === 'server_cubic') relin = keyGen.createRelinKeysSerializable();
  const galoisB64 = galois ? galois.saveToBase64(compr) : null;
  const relinB64 = relin ? relin.saveToBase64(compr) : null;
  const keygenMs = performance.now() - t;

  const encryptor = new seal.Encryptor(context, publicKey, secretKey);
  const decryptor = new seal.Decryptor(context, secretKey);
  const encoder = new seal.CKKSEncoder(context);
  const scale = 2 ** cfg.scale_bits;
  await post('/keys', { cfg: cfg.id, dataset: name, parms: parms.saveToBase64(seal.ComprModeType.none), galois: galoisB64, relin: relinB64 });

  const encryptOne = (values) => {
    const pt = new seal.Plaintext();
    encoder.encode(Float64Array.from(values), scale, pt);
    let out;
    if (cfg.encryption === 'seeded') {
      const s = encryptor.encryptSymmetricSerializable(pt);
      out = s.saveToBase64(compr);
      s.delete();
    } else {
      const ct = new seal.Ciphertext();
      encryptor.encrypt(pt, ct);
      out = ct.saveToBase64(compr);
      ct.delete();
    }
    pt.delete();
    return out;
  };

  const enc = []; const total = []; const srv = []; const dec = []; const trip = []; const outputs = [];
  let upload = 0; let result = 0;
  const count = Math.min(cfg.max_patients, data.X.length);
  for (let i = 0; i < count; i++) {
    const x = data.X[i];
    const t0 = performance.now();
    const cts = cfg.layout === 'packed' ? [encryptOne(x)] : x.map((v) => encryptOne([v]));
    const t1 = performance.now();
    const res = await post('/infer', { cfg: cfg.id, dataset: name, ciphertexts: cts });
    const t2 = performance.now();
    const ct = new seal.Ciphertext();
    ct.loadFromBase64(context, res.encrypted_result);
    const pt = new seal.Plaintext();
    decryptor.decrypt(ct, pt);
    let value = encoder.decodeFloat64(pt)[0];
    if (cfg.sigmoid === 'browser') value = 1 / (1 + Math.exp(-value));
    const t3 = performance.now();
    ct.delete(); pt.delete();
    enc.push(t1 - t0); trip.push(t2 - t1); dec.push(t3 - t2); srv.push(res.compute_ms); total.push(res.total_ms);
    outputs.push(value);
    if (i % 5 === 4) await post('/progress', { text: `  ${cfg.id} ${name} patient ${i + 1}/${count} heap=${Math.round((performance.memory?.usedJSHeapSize ?? 0) / 1e6)}MB` });
    upload = cts.reduce((s, c) => s + bytesOf(c), 0);
    result = bytesOf(res.encrypted_result);
  }
  const match = outputs.filter((v, i) => (v >= 0.5) === (data.p[i] >= 0.5)).length / count;
  const accuracy = outputs.filter((v, i) => Number(v >= 0.5) === data.y[i]).length / count;
  parms.delete();
  return {
    patients: count, decision_match: match, accuracy, keygen_ms: keygenMs,
    upload_bytes: upload, result_bytes: result,
    galois_key_bytes: galoisB64 ? bytesOf(galoisB64) : 0,
    relin_key_bytes: relinB64 ? bytesOf(relinB64) : 0,
    encrypt_ms: mean(enc), encrypt_ms_median: median(enc),
    server_ms: mean(srv), server_ms_median: median(srv), server_total_ms: mean(total),
    decrypt_ms: mean(dec), decrypt_ms_median: median(dec),
    local_roundtrip_ms: mean(trip),
  };
}

async function main() {
  const seal = await initialize();
  const job = await (await fetch('/job')).json();
  const results = [];
  for (const cfg of job.configs) {
    const entry = { ...cfg, datasets: {} };
    for (const [name, data] of Object.entries(job.datasets)) {
      try {
        entry.datasets[name] = await runOne(seal, cfg, name, data);
      } catch (err) {
        entry.datasets[name] = { error: String(err.message ?? err).slice(0, 200) };
      }
      log(`${cfg.id} ${name} done`);
      await post('/progress', { text: `${cfg.id} ${name} ${JSON.stringify(entry.datasets[name]).slice(0, 260)}` });
    }
    results.push(entry);
  }
  await post('/done', { results, userAgent: navigator.userAgent });
  log('finished');
}

window.addEventListener('error', (e) => post('/progress', { text: `FATAL window error ${e.message}` }));
main().catch((e) => post('/progress', { text: `FATAL ${e.stack ?? e}` }));
