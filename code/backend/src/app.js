import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';

import { ApiError, sendError } from './errors.js';
import { fheClient } from './fheClient.js';
import { rateLimit } from './rateLimit.js';
import { validateDataset, validatePredict } from './validate.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND_DIR = path.resolve(HERE, '..', '..', 'frontend');

function nodeSealDist() {
  try {
    // node-seal's "exports" hides package.json, so resolve the ESM entry (dist/index_throws.js)
    return path.dirname(fileURLToPath(import.meta.resolve('node-seal')));
  } catch {
    return null;
  }
}

export function createApp({
  fheUrl = 'http://127.0.0.1:8001',
  fheToken = '',
  apiTokens = [],
  authDisabled = false,
  perMinute = 20,
  tls = false,
  logger = console,
  fetchImpl = fetch,
  serveFrontend = true,
} = {}) {
  const app = express();
  const fhe = fheClient({ baseUrl: fheUrl, token: fheToken, fetchImpl });
  const tokens = new Set(apiTokens.filter(Boolean));

  app.disable('x-powered-by');
  app.set('trust proxy', 'loopback');

  // request id + metadata-only access log (never the body: threat model T6)
  app.use((req, res, next) => {
    res.locals.requestId = crypto.randomUUID();
    res.set('X-Request-Id', res.locals.requestId);
    const t0 = process.hrtime.bigint();
    res.on('finish', () => {
      const ms = Number(process.hrtime.bigint() - t0) / 1e6;
      logger.info(JSON.stringify({ t: new Date().toISOString(), id: res.locals.requestId, method: req.method,
        path: req.path, status: res.statusCode, bytes_in: Number(req.get('content-length') ?? 0), ms: Math.round(ms) }));
    });
    next();
  });

  // security headers
  app.use((req, res, next) => {
    res.set({
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'no-referrer',
      'X-Frame-Options': 'DENY',
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Content-Security-Policy': "default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
      'Cache-Control': req.path.startsWith('/api/') ? 'no-store' : 'no-cache',
    });
    if (tls) res.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    next();
  });

  function requireAuth(req, res, next) {
    if (authDisabled) return next();
    const h = req.get('authorization') ?? '';
    const token = h.startsWith('Bearer ') ? h.slice(7) : '';
    const ok = token && [...tokens].some((t) => t.length === token.length
      && crypto.timingSafeEqual(Buffer.from(t), Buffer.from(token)));
    return ok ? next() : sendError(res, new ApiError('UNAUTHORIZED', 'missing or invalid bearer token'));
  }

  const json = express.json({ limit: '48mb', strict: true });
  const api = express.Router();

  api.get('/health', async (req, res) => {
    let service = 'ok';
    try { await fhe.health(); } catch { service = 'unavailable'; }
    res.json({ status: 'ok', fhe_service: service, version: '2.0.0' });
  });

  api.get('/model/:dataset', async (req, res) => {
    try {
      validateDataset(req.params.dataset);
      res.json(await fhe.model(req.params.dataset));
    } catch (err) { sendError(res, err); }
  });

  api.post('/predict', rateLimit({ perMinute }), requireAuth, json, async (req, res) => {
    try {
      const payload = validatePredict(req.body);
      const out = await fhe.infer(payload);
      res.json({ encrypted_result: out.encrypted_result, output: out.output, threshold: out.threshold,
        timings_ms: out.timings_ms, request_id: res.locals.requestId });
    } catch (err) { sendError(res, err); }
  });

  app.use('/api', api);

  if (serveFrontend) {
    const dist = nodeSealDist();
    if (dist) {
      app.use('/vendor/node-seal', express.static(dist, {
        setHeaders: (res, file) => { if (file.endsWith('.wasm')) res.set('Content-Type', 'application/wasm'); },
      }));
    }
    app.use(express.static(FRONTEND_DIR));
  }

  app.use((req, res) => sendError(res, new ApiError('NOT_FOUND', 'no such route')));
  // body-parser errors (too large, bad JSON) arrive here
  // eslint-disable-next-line no-unused-vars
  app.use((err, req, res, next) => {
    if (err?.type === 'entity.too.large') return sendError(res, new ApiError('PAYLOAD_TOO_LARGE', 'request body too large'));
    if (err?.type === 'entity.parse.failed') return sendError(res, new ApiError('BAD_REQUEST', 'body is not valid JSON'));
    logger.error(JSON.stringify({ id: res.locals.requestId, error: 'unhandled', name: err?.name }));
    return sendError(res, new ApiError('INTERNAL_ERROR', 'internal error'));
  });

  return app;
}
