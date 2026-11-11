"""Make code/fhe-ml-service importable from the pilot scripts."""
import os
import sys

CODE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SERVICE_DIR = os.path.join(CODE_DIR, "fhe-ml-service")
MODEL_DIR = os.path.join(SERVICE_DIR, "model")
RESULTS_DIR = os.path.join(CODE_DIR, "results")
RAW_DIR = os.path.join(CODE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(CODE_DIR, "data", "processed")
if SERVICE_DIR not in sys.path:
    sys.path.insert(0, SERVICE_DIR)


def results_dir(dataset: str) -> str:
    path = os.path.join(RESULTS_DIR, dataset)
    os.makedirs(path, exist_ok=True)
    return path


def model_path(dataset: str) -> str:
    os.makedirs(MODEL_DIR, exist_ok=True)
    return os.path.join(MODEL_DIR, f"model_weights_{dataset}.json")
