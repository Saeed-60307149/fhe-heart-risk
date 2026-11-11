import { ApiError, fromService } from './errors.js';

export function fheClient({ baseUrl, token = '', timeoutMs = 120_000, fetchImpl = fetch }) {
  const headers = { 'content-type': 'application/json', ...(token ? { 'x-internal-token': token } : {}) };

  async function call(path, init = {}) {
    let res;
    try {
      res = await fetchImpl(new URL(path, baseUrl), { ...init, headers, signal: AbortSignal.timeout(timeoutMs) });
    } catch {
      throw new ApiError('FHE_SERVICE_UNAVAILABLE', 'FHE service is not reachable');
    }
    let json = null;
    try { json = await res.json(); } catch { /* non-JSON */ }
    if (!res.ok) {
      const e = json?.error;
      throw e?.code ? fromService(e.code, e.message) : new ApiError('FHE_SERVICE_UNAVAILABLE', `FHE service returned ${res.status}`);
    }
    return json;
  }

  return {
    health: () => call('/health'),
    model: (dataset) => call(`/model/${encodeURIComponent(dataset)}`),
    infer: (payload) => call('/infer', { method: 'POST', body: JSON.stringify(payload) }),
  };
}
