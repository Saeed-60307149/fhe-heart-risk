import { ApiError, sendError } from './errors.js';

// Fixed-window limiter in memory (one process). For several instances use a shared store.
export function rateLimit({ perMinute = 20, now = () => Date.now() } = {}) {
  const hits = new Map();
  return (req, res, next) => {
    const key = `${req.ip}|${req.get('authorization') ?? ''}`;
    const t = now();
    let entry = hits.get(key);
    if (!entry || t - entry.start >= 60_000) {
      entry = { start: t, count: 0 };
      hits.set(key, entry);
    }
    entry.count += 1;
    res.set('RateLimit-Limit', String(perMinute));
    res.set('RateLimit-Remaining', String(Math.max(0, perMinute - entry.count)));
    if (entry.count > perMinute) {
      res.set('Retry-After', String(Math.ceil((entry.start + 60_000 - t) / 1000)));
      return sendError(res, new ApiError('RATE_LIMITED', 'too many requests, try again later'));
    }
    if (hits.size > 10_000) { // drop stale windows
      for (const [k, v] of hits) if (t - v.start >= 60_000) hits.delete(k);
    }
    return next();
  };
}
