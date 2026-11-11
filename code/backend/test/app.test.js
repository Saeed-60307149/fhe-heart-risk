import assert from 'node:assert/strict';
import { after, before, describe, test } from 'node:test';

import { auth, B64, fakeFhe, goodBody, start } from './helpers.js';

describe('API contract (design/api-contract.md)', () => {
  let srv; let fhe;
  before(async () => {
    fhe = fakeFhe(async (url, init) => {
      if (url.endsWith('/health')) return { body: { status: 'ok' } };
      if (url.includes('/model/cleveland')) return { body: { dataset: 'cleveland', n_features: 13 } };
      if (url.includes('/model/')) return { status: 404, body: { error: { code: 'MODEL_NOT_FOUND', message: 'no model' } } };
      const b = JSON.parse(init.body);
      if (b.ciphertexts[0] === 'QUFBQQ==') return { status: 422, body: { error: { code: 'UNSUPPORTED_PARAMETERS', message: 'bad degree' } } };
      return { body: { encrypted_result: B64(20), output: b.output, threshold: 0.5, timings_ms: { compute_ms: 1 } } };
    });
    srv = await start({ fetchImpl: fhe.impl, fheToken: 'internal', perMinute: 1000 });
  });
  after(() => srv.close());

  test('GET /api/health reports the FHE service', async () => {
    const r = await fetch(`${srv.base}/api/health`);
    assert.equal(r.status, 200);
    assert.deepEqual((await r.json()).fhe_service, 'ok');
  });

  test('security headers are set and x-powered-by is hidden', async () => {
    const r = await fetch(`${srv.base}/api/health`);
    assert.equal(r.headers.get('x-content-type-options'), 'nosniff');
    assert.match(r.headers.get('content-security-policy'), /wasm-unsafe-eval/);
    assert.equal(r.headers.get('x-powered-by'), null);
    assert.ok(r.headers.get('x-request-id'));
  });

  test('GET /api/model/:dataset proxies metadata; unknown -> NOT_FOUND', async () => {
    assert.equal((await fetch(`${srv.base}/api/model/cleveland`)).status, 200);
    const r = await fetch(`${srv.base}/api/model/unknown`);
    assert.equal(r.status, 404);
    assert.equal((await r.json()).error.code, 'NOT_FOUND');
  });

  test('POST /api/predict without token -> 401 UNAUTHORIZED', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(goodBody()) });
    assert.equal(r.status, 401);
    assert.equal((await r.json()).error.code, 'UNAUTHORIZED');
  });

  test('POST /api/predict with wrong token -> 401', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: { ...auth, authorization: 'Bearer nope' }, body: JSON.stringify(goodBody()) });
    assert.equal(r.status, 401);
  });

  test('happy path forwards only whitelisted fields with the internal token', async () => {
    const body = { ...goodBody(), extra: 'should not be forwarded' };
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify(body) });
    assert.equal(r.status, 200);
    const j = await r.json();
    assert.ok(j.encrypted_result && j.request_id);
    const call = fhe.calls.at(-1);
    assert.equal(call.init.headers['x-internal-token'], 'internal');
    const sent = JSON.parse(call.init.body);
    assert.equal(sent.extra, undefined);
    assert.equal(sent.layout, 'per_feature');
  });

  test('missing fields -> 400 BAD_REQUEST', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ dataset: 'cleveland' }) });
    assert.equal(r.status, 400);
    assert.equal((await r.json()).error.code, 'BAD_REQUEST');
  });

  test('invalid JSON -> 400', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: '{not json' });
    assert.equal(r.status, 400);
  });

  test('non-base64 ciphertext -> 422 INVALID_CIPHERTEXT', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), ciphertexts: ['@@@@'] }) });
    assert.equal(r.status, 422);
    assert.equal((await r.json()).error.code, 'INVALID_CIPHERTEXT');
  });

  test('probability_poly without relin_keys -> 400', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), output: 'probability_poly' }) });
    assert.equal(r.status, 400);
  });

  test('too many ciphertexts -> 400; oversize ciphertext -> 413', async () => {
    let r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), ciphertexts: Array(65).fill(B64()) }) });
    assert.equal(r.status, 400);
    r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), ciphertexts: ['A'.repeat(2_700_000)] }) });
    assert.equal(r.status, 413);
    assert.equal((await r.json()).error.code, 'PAYLOAD_TOO_LARGE');
  });

  test('FHE service error codes are mapped to public codes', async () => {
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), ciphertexts: ['QUFBQQ=='] }) });
    assert.equal(r.status, 422);
    assert.equal((await r.json()).error.code, 'INVALID_CIPHERTEXT');
  });

  test('access log holds metadata only, never ciphertext', async () => {
    const marker = Buffer.from('VERY-SECRET-CIPHERTEXT-MARKER').toString('base64');
    await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify({ ...goodBody(), ciphertexts: [marker] }) });
    const log = srv.logger.lines.join('\n');
    assert.ok(log.includes('/api/predict'));
    assert.ok(!log.includes(marker));
  });

  test('unknown route -> 404 NOT_FOUND', async () => {
    const r = await fetch(`${srv.base}/api/nope`);
    assert.equal(r.status, 404);
  });
});

describe('failure modes', () => {
  test('FHE service down -> 503 FHE_SERVICE_UNAVAILABLE', async () => {
    const srv = await start({ fetchImpl: async () => { throw new Error('ECONNREFUSED'); } });
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify(goodBody()) });
    assert.equal(r.status, 503);
    assert.equal((await r.json()).error.code, 'FHE_SERVICE_UNAVAILABLE');
    const h = await (await fetch(`${srv.base}/api/health`)).json();
    assert.equal(h.fhe_service, 'unavailable');
    await srv.close();
  });

  test('rate limit -> 429 RATE_LIMITED with Retry-After', async () => {
    const fhe = fakeFhe(async () => ({ body: { encrypted_result: B64(), output: 'logit' } }));
    const srv = await start({ fetchImpl: fhe.impl, perMinute: 2 });
    const send = () => fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: JSON.stringify(goodBody()) });
    assert.equal((await send()).status, 200);
    assert.equal((await send()).status, 200);
    const r = await send();
    assert.equal(r.status, 429);
    assert.ok(Number(r.headers.get('retry-after')) > 0);
    await srv.close();
  });

  test('body over 48 MB -> 413', async () => {
    const fhe = fakeFhe(async () => ({ body: {} }));
    const srv = await start({ fetchImpl: fhe.impl, perMinute: 100 });
    const big = JSON.stringify({ ...goodBody(), pad: 'x'.repeat(49 * 1024 * 1024) });
    const r = await fetch(`${srv.base}/api/predict`, { method: 'POST', headers: auth, body: big });
    assert.equal(r.status, 413);
    await srv.close();
  });
});
