# Architecture (draft)
Owner: Abdullah Dar

## Parts
1. **Client** – collects patient features, encrypts them, later decrypts the result. Holds the **secret key**.
2. **Backend API** (Node/Express) – receives ciphertext, passes it to the FHE service. Never sees plaintext.
3. **FHE-ML service** (Python + TenSEAL) – runs the model (dot product + polynomial sigmoid) on encrypted data.

## Who holds what
| Item | Where | Leaves the client? |
|---|---|---|
| Secret key | Client only | Never |
| Public + evaluation keys | Sent with the request | Yes |
| Encrypted input / result | Client ↔ server | Yes |
| Model weights | Server | – |

## Open decision
Plan A: browser client with node-seal · Plan B: Python client with TenSEAL. Depends on Saif's compatibility test (Wk 11).
