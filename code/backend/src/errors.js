// Public error codes of the API (design/api-contract.md section 4). Every error
// response is { "error": { "code", "message", "request_id" } } and never echoes input.
export const ERRORS = {
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  PAYLOAD_TOO_LARGE: 413,
  INVALID_CIPHERTEXT: 422,
  RATE_LIMITED: 429,
  INTERNAL_ERROR: 500,
  FHE_SERVICE_UNAVAILABLE: 503,
};

// FHE service codes -> public codes
const FROM_SERVICE = {
  BAD_REQUEST: 'BAD_REQUEST',
  UNAUTHORIZED: 'INTERNAL_ERROR', // internal token problem is our fault, not the client's
  PAYLOAD_TOO_LARGE: 'PAYLOAD_TOO_LARGE',
  INVALID_CIPHERTEXT: 'INVALID_CIPHERTEXT',
  UNSUPPORTED_PARAMETERS: 'INVALID_CIPHERTEXT',
  MODEL_NOT_FOUND: 'NOT_FOUND',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
};

export class ApiError extends Error {
  constructor(code, message) {
    super(message);
    this.code = ERRORS[code] ? code : 'INTERNAL_ERROR';
    this.status = ERRORS[this.code];
  }
}

export function fromService(code, message) {
  return new ApiError(FROM_SERVICE[code] ?? 'INTERNAL_ERROR', message ?? 'FHE service error');
}

export function sendError(res, err) {
  const e = err instanceof ApiError ? err : new ApiError('INTERNAL_ERROR', 'internal error');
  res.status(e.status).json({ error: { code: e.code, message: e.message, request_id: res.locals.requestId } });
}
