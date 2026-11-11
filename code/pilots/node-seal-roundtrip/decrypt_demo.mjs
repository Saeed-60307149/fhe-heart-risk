// node-seal client: decrypt the toy-demo result written by server_demo.py
import initialize from 'node-seal';
import fs from 'fs';

const seal = await initialize();
const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
parms.loadFromBase64(fs.readFileSync('demo_parms.b64', 'utf8').trim());
const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
const secretKey = new seal.SecretKey();
secretKey.loadFromBase64(context, fs.readFileSync('demo_sk.b64', 'utf8').trim());

const cipher = new seal.Ciphertext();
cipher.loadFromArray(context, new Uint8Array(fs.readFileSync('out/demo_z.seal')));
const plain = new seal.Plaintext();
new seal.Decryptor(context, secretKey).decrypt(cipher, plain);
const z = new seal.CKKSEncoder(context).decodeFloat64(plain)[0];

const values = [1.5, -2.25, 3.75, 4.0];
const W = [0.5, -1.0, 2.0, 0.25];
const expected = values.reduce((s, v, i) => s + v * W[i], 0);
console.log(`node-seal decrypted z = ${z.toFixed(4)} (expected ${expected})`);
if (Math.abs(z - expected) > 1e-3) { console.error('DEMO FAILED'); process.exit(1); }
console.log('DEMO ROUND TRIP OK');
