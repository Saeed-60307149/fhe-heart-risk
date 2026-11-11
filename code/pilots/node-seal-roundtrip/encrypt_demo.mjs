// node-seal side: encrypt one value per ciphertext (per-feature design)
import initialize from 'node-seal';
import fs from 'fs';

const seal = await initialize();

const schemeType = seal.SchemeType.ckks;
const securityLevel = seal.SecLevelType.tc128;
const polyModulusDegree = 8192;
const bitSizes = [60, 40, 40, 60];
const scale = 2 ** 40;

const parms = new seal.EncryptionParameters(schemeType);
parms.setPolyModulusDegree(polyModulusDegree);
parms.setCoeffModulus(seal.CoeffModulus.Create(polyModulusDegree, Int32Array.from(bitSizes)));
const context = new seal.SEALContext(parms, true, securityLevel);

const encoder = new seal.CKKSEncoder(context);
const keyGen = new seal.KeyGenerator(context);
const secretKey = keyGen.secretKey();
const publicKey = keyGen.createPublicKey();
const encryptor = new seal.Encryptor(context, publicKey);

// per-feature: one ciphertext per value (Report 1 design, no rotation keys)
const values = [1.5, -2.25, 3.75, 4.0];
const compr = seal.ComprModeType.none;
const t0 = performance.now();
const cts = values.map((v) => {
  const plain = new seal.Plaintext();
  encoder.encode(Float64Array.from([v]), scale, plain);
  const cipher = new seal.Ciphertext();
  encryptor.encrypt(plain, cipher);
  return cipher;
});
const encMs = (performance.now() - t0) / values.length;

fs.writeFileSync('demo_parms.b64', parms.saveToBase64(compr));
fs.writeFileSync('demo_sk.b64', secretKey.saveToBase64(compr));
cts.forEach((c, i) => fs.writeFileSync(`demo_ct_${i}.b64`, c.saveToBase64(compr)));
console.log(`encrypted ${values.length} features, avg ${encMs.toFixed(1)} ms each`);
