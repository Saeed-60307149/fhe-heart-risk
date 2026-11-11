// Client-side CKKS with node-seal 7.0.0 (Plan A). The secret key is created here and
// never leaves this page (it lives only in memory; reload = new keys).
import initialize from '/vendor/node-seal/index_throws.js';

let sealPromise;
const getSeal = () => (sealPromise ??= initialize());

export async function createSession(params, scaleBits) {
  const seal = await getSeal();
  const parms = new seal.EncryptionParameters(seal.SchemeType.ckks);
  parms.setPolyModulusDegree(params.poly_modulus_degree);
  parms.setCoeffModulus(seal.CoeffModulus.Create(params.poly_modulus_degree, Int32Array.from(params.coeff_mod_bit_sizes)));
  const context = new seal.SEALContext(parms, true, seal.SecLevelType.tc128);
  if (!context.parametersSet()) throw new Error('CKKS parameters rejected by node-seal');
  const keyGen = new seal.KeyGenerator(context);
  const secretKey = keyGen.secretKey();
  const encryptor = new seal.Encryptor(context, keyGen.createPublicKey());
  const encoder = new seal.CKKSEncoder(context);
  const none = seal.ComprModeType.none;
  const scale = 2 ** scaleBits;
  let relin = null;

  return {
    parmsB64: () => parms.saveToBase64(none),
    relinKeysB64: () => (relin ??= keyGen.createRelinKeys().saveToBase64(none)),
    encryptEach(values) {
      return values.map((v) => {
        const pt = new seal.Plaintext();
        encoder.encode(Float64Array.from([v]), scale, pt);
        const ct = new seal.Ciphertext();
        encryptor.encrypt(pt, ct);
        const b64 = ct.saveToBase64(none);
        pt.delete(); ct.delete();
        return b64;
      });
    },
    decryptScalar(b64) {
      const ct = new seal.Ciphertext();
      ct.loadFromBase64(context, b64);
      const pt = new seal.Plaintext();
      new seal.Decryptor(context, secretKey).decrypt(ct, pt);
      const v = encoder.decodeFloat64(pt)[0];
      ct.delete(); pt.delete();
      return v;
    },
  };
}
