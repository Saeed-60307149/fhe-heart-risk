"""FHE-ML service (Python, FastAPI, TenSEAL 0.3.16 raw SEAL API).

Internal service: only the Node.js API (code/backend) calls it. It computes the
encrypted risk score on the patient's ciphertexts and returns a ciphertext. It never
holds a secret key and never decrypts (enforced by tests/test_no_secret_on_server.py).

Run:  uvicorn app:app --host 127.0.0.1 --port 8001
Env:  MODEL_DIR (default ./model), FHE_SERVICE_TOKEN (shared secret with the Node API;
      if set, requests must send header X-Internal-Token)
Contract: design/api-contract.md and design/openapi.yaml (internal /infer section).
"""
from __future__ import annotations

import base64
import binascii
import glob
import hmac
import logging
import os
from typing import Literal, Optional

from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from fhe_heart import params as P
from fhe_heart.model import load_weights
from fhe_heart.seal_server import FheInputError, SealServer

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.environ.get("MODEL_DIR", os.path.join(HERE, "model"))
SERVICE_TOKEN = os.environ.get("FHE_SERVICE_TOKEN", "")
MAX_FEATURES = 64

# Metadata-only logging: never log bodies, ciphertexts or keys (threat model T6).
log = logging.getLogger("fhe-ml-service")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

STATUS = {"BAD_REQUEST": 400, "UNAUTHORIZED": 401, "PAYLOAD_TOO_LARGE": 413,
          "INVALID_CIPHERTEXT": 422, "UNSUPPORTED_PARAMETERS": 422,
          "MODEL_NOT_FOUND": 404, "INTERNAL_ERROR": 500}


def load_models(model_dir: str) -> dict:
    models = {}
    for path in sorted(glob.glob(os.path.join(model_dir, "model_weights_*.json"))):
        doc = load_weights(path)
        models[doc["dataset"]] = doc
    return models


MODELS = load_models(MODEL_DIR)
app = FastAPI(title="fhe-heart FHE-ML service", version="2.0.0",
              docs_url=None, redoc_url=None)


def error(code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=STATUS.get(code, 500),
                        content={"error": {"code": code, "message": message}})


@app.exception_handler(RequestValidationError)
async def _validation(_: Request, exc: RequestValidationError):
    # Do not echo the input back (it may contain ciphertext).
    fields = sorted({".".join(str(p) for p in e.get("loc", [])[1:]) for e in exc.errors()})
    return error("BAD_REQUEST", f"invalid request fields: {fields}")


class InferRequest(BaseModel):
    dataset: str = Field(..., pattern=r"^[a-z0-9_-]{1,32}$")
    layout: Literal["per_feature"] = "per_feature"
    parms: str = Field(..., description="base64 SEAL EncryptionParameters (CKKS)")
    ciphertexts: list[str] = Field(..., min_length=1, max_length=MAX_FEATURES)
    relin_keys: Optional[str] = None
    output: Literal["logit", "probability_poly"] = "logit"


def b64(value: str, what: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        raise FheInputError("INVALID_CIPHERTEXT", f"{what} is not valid base64")


def check_token(token: Optional[str]) -> bool:
    return not SERVICE_TOKEN or (token is not None and hmac.compare_digest(token, SERVICE_TOKEN))


@app.get("/health")
def health():
    return {"status": "ok", "models": sorted(MODELS), "tenseal_seal_api": True}


@app.get("/model/{dataset}")
def model_info(dataset: str, x_internal_token: Optional[str] = Header(default=None)):
    if not check_token(x_internal_token):
        return error("UNAUTHORIZED", "missing or wrong internal token")
    doc = MODELS.get(dataset)
    if doc is None:
        return error("MODEL_NOT_FOUND", f"no model for dataset {dataset!r}")
    # Public metadata only: the weights are the server's asset and are NOT returned.
    return {"dataset": doc["dataset"], "feature_names": doc["feature_names"],
            "n_features": len(doc["weights"]), "scaler_mean": doc["scaler_mean"],
            "scaler_scale": doc["scaler_scale"], "threshold": doc["threshold"],
            "param_set": doc.get("param_set", P.DEFAULT_PARAM_SET),
            "params": P.PARAM_SETS[doc.get("param_set", P.DEFAULT_PARAM_SET)],
            "scale_bits": P.SCALE_BITS,
            "supports_probability_poly": bool(doc.get("sigmoid_poly"))}


@app.post("/infer")
def infer(req: InferRequest, x_internal_token: Optional[str] = Header(default=None)):
    if not check_token(x_internal_token):
        return error("UNAUTHORIZED", "missing or wrong internal token")
    doc = MODELS.get(req.dataset)
    if doc is None:
        return error("MODEL_NOT_FOUND", f"no model for dataset {req.dataset!r}")
    try:
        if req.output == "probability_poly":
            if not doc.get("sigmoid_poly"):
                raise FheInputError("BAD_REQUEST", "this model has no sigmoid polynomial")
            if not req.relin_keys:
                raise FheInputError("BAD_REQUEST", "output=probability_poly needs relin_keys")
        server = SealServer(b64(req.parms, "parms"))
        cts = [b64(c, f"ciphertexts[{i}]") for i, c in enumerate(req.ciphertexts)]
        poly = doc["sigmoid_poly"]["coeffs_ascending"] if req.output == "probability_poly" else None
        rk = b64(req.relin_keys, "relin_keys") if poly else None
        res = server.infer(cts, doc["weights"], doc["bias"], poly, rk)
    except FheInputError as exc:
        log.info("infer rejected dataset=%s code=%s n_ct=%d", req.dataset, exc.code,
                 len(req.ciphertexts))
        return error(exc.code, str(exc))
    except Exception:  # never leak internals
        log.exception("infer failed dataset=%s", req.dataset)
        return error("INTERNAL_ERROR", "encrypted inference failed")
    log.info("infer ok dataset=%s n_ct=%d output=%s compute_ms=%s", req.dataset,
             len(req.ciphertexts), res.output, res.timings_ms["compute_ms"])
    return {"encrypted_result": base64.b64encode(res.ciphertext).decode("ascii"),
            "output": res.output, "threshold": doc["threshold"],
            "timings_ms": res.timings_ms}
