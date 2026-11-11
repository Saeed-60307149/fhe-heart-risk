import { ApiError } from './errors.js';

export const LIMITS = {
  maxFeatures: 64,
  // one serialized ciphertext <= 2,000,000 bytes -> base64 length
  maxCiphertextB64: Math.ceil(2_000_000 / 3) * 4,
  maxRelinKeysB64: Math.ceil(12_000_000 / 3) * 4,
  maxParmsB64: 4096,
};

const DATASET = /^[a-z0-9_-]{1,32}$/;
const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
const OUTPUTS = new Set(['logit', 'probability_poly']);

function b64(value, field, max) {
  if (typeof value !== 'string' || value.length === 0) throw new ApiError('BAD_REQUEST', `${field} must be a base64 string`);
  if (value.length > max) throw new ApiError('PAYLOAD_TOO_LARGE', `${field} is too large`);
  if (value.length % 4 !== 0 || !B64.test(value)) throw new ApiError('INVALID_CIPHERTEXT', `${field} is not valid base64`);
}

export function validateDataset(dataset) {
  if (typeof dataset !== 'string' || !DATASET.test(dataset)) throw new ApiError('BAD_REQUEST', 'dataset must match [a-z0-9_-]{1,32}');
}

// Returns a clean copy with only the fields we forward (no unexpected keys pass through).
export function validatePredict(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) throw new ApiError('BAD_REQUEST', 'body must be a JSON object');
  const { dataset, parms, ciphertexts, relin_keys: relinKeys = null, output = 'logit' } = body;
  validateDataset(dataset);
  if (!OUTPUTS.has(output)) throw new ApiError('BAD_REQUEST', 'output must be "logit" or "probability_poly"');
  b64(parms, 'parms', LIMITS.maxParmsB64);
  if (!Array.isArray(ciphertexts) || ciphertexts.length < 1 || ciphertexts.length > LIMITS.maxFeatures) {
    throw new ApiError('BAD_REQUEST', `ciphertexts must be an array of 1-${LIMITS.maxFeatures} base64 strings`);
  }
  ciphertexts.forEach((c, i) => b64(c, `ciphertexts[${i}]`, LIMITS.maxCiphertextB64));
  if (output === 'probability_poly') {
    if (relinKeys == null) throw new ApiError('BAD_REQUEST', 'output=probability_poly needs relin_keys');
    b64(relinKeys, 'relin_keys', LIMITS.maxRelinKeysB64);
  } else if (relinKeys != null) {
    b64(relinKeys, 'relin_keys', LIMITS.maxRelinKeysB64);
  }
  return { dataset, layout: 'per_feature', parms, ciphertexts, relin_keys: relinKeys, output };
}
