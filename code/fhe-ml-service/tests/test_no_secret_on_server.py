"""Threat model T1 / runbook step 22: the server code never decrypts and never holds
a secret key. Checked on the syntax tree (comments and docstrings do not count)."""
import ast
import os

import pytest

SERVICE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SERVER_FILES = ["app.py", os.path.join("fhe_heart", "seal_server.py")]
FORBIDDEN_NAMES = {"Decryptor", "SecretKey", "secret_key", "decrypt", "decrypt_scalar",
                   "make_context_public"}
FORBIDDEN_MODULES = {"fhe_heart.seal_client", "seal_client", "fhe_heart.ckks_packed"}


@pytest.mark.parametrize("rel", SERVER_FILES)
def test_server_code_has_no_secret_key_use(rel):
    tree = ast.parse(open(os.path.join(SERVICE_DIR, rel), encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            assert node.attr not in FORBIDDEN_NAMES, f"{rel}: uses .{node.attr}"
        if isinstance(node, ast.Name):
            assert node.id not in FORBIDDEN_NAMES, f"{rel}: uses {node.id}"
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            names = [a.name for a in node.names]
            for m in mods + names:
                assert m not in FORBIDDEN_MODULES, f"{rel}: imports {m}"
