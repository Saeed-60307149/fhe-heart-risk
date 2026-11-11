// node-seal client: encrypt every feature of a real test patient (per-feature design)
import initialize from 'node-seal';
import fs from 'fs';

const seal = await initialize();

const schemeType = seal.SchemeType.ckks;
const securityLevel = seal.SecLevelType.tc128;
const polyModulusDegree = 16384;                 // same as the TenSEAL pilot
const bitSizes = [60, 40, 40, 40, 40, 60];
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

const { patient } = JSON.parse(fs.readFileSync('model_patient.json', 'utf8'));

const compr = seal.ComprModeType.none;
const t0 = performance.now();
patient.forEach((v, j) => {
  const plain = new seal.Plaintext();
  encoder.encode(Float64Array.from([v]), scale, plain);
  const cipher = new seal.Ciphertext();
  encryptor.encrypt(plain, cipher);
  fs.writeFileSync(`real_ct_${j}.b64`, cipher.saveToBase64(compr));
});
const encMs = performance.now() - t0;
fs.writeFileSync('real_parms.b64', parms.saveToBase64(compr));
fs.writeFileSync('real_sk.b64', secretKey.saveToBase64(compr));

let total = 0;
for (let j = 0; j < patient.length; j++) total += fs.statSync(`real_ct_${j}.b64`).size;
console.log(`node-seal encrypted ${patient.length} features of 1 patient in ${encMs.toFixed(0)} ms ` +
  `(${(encMs / patient.length).toFixed(1)} ms/feature), ${(total / 1024).toFixed(0)} KB of ciphertexts (base64)`);
