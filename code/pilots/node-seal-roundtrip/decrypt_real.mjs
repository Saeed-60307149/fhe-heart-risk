// node-seal client: decrypt the encrypted score and compute the risk locally
import initialize from 'node-seal';
import fs from 'fs';

const seal = await initialize();

const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
parms.loadFromBase64(fs.readFileSync('real_parms.b64', 'utf8').trim());
const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);

const secretKey = new seal.SecretKey();
secretKey.loadFromBase64(context, fs.readFileSync('real_sk.b64', 'utf8').trim());

const cipher = new seal.Ciphertext();
cipher.loadFromArray(context, new Uint8Array(fs.readFileSync('out/real_z.seal')));

const encoder = new seal.CKKSEncoder(context);
const decryptor = new seal.Decryptor(context, secretKey);
const plain = new seal.Plaintext();

const t0 = performance.now();
decryptor.decrypt(cipher, plain);
const decMs = performance.now() - t0;

const z = encoder.decodeFloat64(plain)[0];
const { z_true, label } = JSON.parse(fs.readFileSync('model_patient.json', 'utf8'));
const prob = 1 / (1 + Math.exp(-z));
console.log(`node-seal decrypted z = ${z.toFixed(4)} (plain model: ${z_true.toFixed(4)})`);
console.log(`risk probability = ${prob.toFixed(4)} -> prediction ${prob > 0.5 ? 1 : 0} (true label ${label})`);
console.log(`decrypt ${decMs.toFixed(1)} ms`);
if (Math.abs(z - z_true) > 1e-3) { console.error('ROUND TRIP FAILED: z differs from the plain model'); process.exit(1); }
console.log('ROUND TRIP OK: node-seal encrypt -> TenSEAL compute -> node-seal decrypt');
