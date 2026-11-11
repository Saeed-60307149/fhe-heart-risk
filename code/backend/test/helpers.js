import { createApp } from '../src/app.js';

export const B64 = (n = 8) => Buffer.alloc(n, 7).toString('base64');

export function silentLogger() {
  const lines = [];
  return { lines, info: (l) => lines.push(l), error: (l) => lines.push(l) };
}

export async function start(opts = {}) {
  const logger = opts.logger ?? silentLogger();
  const app = createApp({ apiTokens: ['tok'], serveFrontend: false, logger, ...opts });
  const server = await new Promise((resolve) => { const s = app.listen(0, '127.0.0.1', () => resolve(s)); });
  const base = `http://127.0.0.1:${server.address().port}`;
  return { base, logger, close: () => new Promise((r) => server.close(r)) };
}

// fake FHE service injected through fetchImpl
export function fakeFhe(handler) {
  const calls = [];
  const impl = async (url, init = {}) => {
    calls.push({ url: String(url), init });
    const { status = 200, body } = await handler(String(url), init);
    return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
  };
  return { impl, calls };
}

export const goodBody = () => ({ dataset: 'cleveland', parms: B64(12), ciphertexts: [B64(), B64()], output: 'logit' });
export const auth = { authorization: 'Bearer tok', 'content-type': 'application/json' };
