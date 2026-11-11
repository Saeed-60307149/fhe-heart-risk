"""Client-side helpers that HOLD THE SECRET KEY (raw SEAL API).

Use only in: tests, pilots, and the Plan B local Python client. The web client
(Plan A) does the same thing in the browser with node-seal (code/frontend/js/fhe.js).
This module must never be imported by app.py or seal_server.py.
"""
from __future__ import annotations

from dataclasses import dataclass

from tenseal import sealapi as seal

from . import params as P
from .seal_server import _load, _save


def make_parms(param_set: str = P.DEFAULT_PARAM_SET):
    spec = P.PARAM_SETS[param_set]
    parms = seal.EncryptionParameters(seal.SCHEME_TYPE.CKKS)
    parms.set_poly_modulus_degree(spec["poly_modulus_degree"])
    parms.set_coeff_modulus(seal.CoeffModulus.Create(spec["poly_modulus_degree"],
                                                     spec["coeff_mod_bit_sizes"]))
    return parms


@dataclass
class SealClient:
    parms: object
    ctx: object
    secret_key: object
    public_key: object
    encoder: object

    @classmethod
    def create(cls, param_set: str = P.DEFAULT_PARAM_SET) -> "SealClient":
        parms = make_parms(param_set)
        ctx = seal.SEALContext(parms, True, seal.SEC_LEVEL_TYPE.TC128)
        kg = seal.KeyGenerator(ctx)
        pk = seal.PublicKey()
        kg.create_public_key(pk)
        client = cls(parms, ctx, kg.secret_key(), pk, seal.CKKSEncoder(ctx))
        client._keygen = kg
        return client

    def parms_bytes(self) -> bytes:
        return _save(self.parms)

    def relin_keys_bytes(self) -> bytes:
        rk = seal.RelinKeys()
        self._keygen.create_relin_keys(rk)
        return _save(rk)

    def encrypt_features(self, values) -> list[bytes]:
        enc = seal.Encryptor(self.ctx, self.public_key)
        out = []
        for v in values:
            pt = seal.Plaintext()
            self.encoder.encode([float(v)], P.SCALE, pt)
            ct = seal.Ciphertext()
            enc.encrypt(pt, ct)
            out.append(_save(ct))
        return out

    def decrypt_scalar(self, ct_bytes: bytes) -> float:
        ct = seal.Ciphertext()
        _load(ct, ct_bytes, self.ctx)
        dec = seal.Decryptor(self.ctx, self.secret_key)
        pt = seal.Plaintext()
        dec.decrypt(ct, pt)
        return float(self.encoder.decode_double(pt)[0])
