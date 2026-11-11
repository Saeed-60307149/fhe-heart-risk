import fs from 'node:fs';
import http from 'node:http';
import https from 'node:https';

import { createApp } from './app.js';

const env = process.env;
const tls = Boolean(env.TLS_CERT && env.TLS_KEY);
const app = createApp({
  fheUrl: env.FHE_URL ?? 'http://127.0.0.1:8001',
  fheToken: env.FHE_SERVICE_TOKEN ?? '',
  apiTokens: (env.API_TOKENS ?? '').split(',').map((s) => s.trim()),
  authDisabled: env.AUTH_DISABLED === '1',
  perMinute: Number(env.RATE_LIMIT_PER_MIN ?? 20),
  tls,
});

if (env.AUTH_DISABLED === '1') console.warn('WARNING: AUTH_DISABLED=1 - bearer-token auth is off (development only)');
if (!tls && (env.HOST ?? '127.0.0.1') !== '127.0.0.1') console.warn('WARNING: no TLS - run behind an HTTPS reverse proxy');

const server = tls
  ? https.createServer({ cert: fs.readFileSync(env.TLS_CERT), key: fs.readFileSync(env.TLS_KEY) }, app)
  : http.createServer(app);
const port = Number(env.PORT ?? 3000);
server.listen(port, env.HOST ?? '127.0.0.1', () => {
  console.log(`fhe-heart API on ${tls ? 'https' : 'http'}://${env.HOST ?? '127.0.0.1'}:${port}`);
});
