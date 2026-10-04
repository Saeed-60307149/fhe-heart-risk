# API Contract (draft – paper design)
Owner: Abdullah Dar

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/health` | – | `{ "status": "ok" }` |
| POST | `/api/predict` | `{ "context": "<base64 public context>", "encrypted_features": "<base64 ciphertext>" }` | `{ "encrypted_score": "<base64 ciphertext>" }` |

Notes
- Ciphertexts are large → raise the Express body size limit.
- Do not log request bodies.
