"""Datasets: download, clean, split, scale.

Both datasets are public and de-identified (see research/ethics-data-note.md).
Raw files are downloaded to code/data/raw/ and are NOT committed (.gitignore).

Split rule (same as the PR2 pilot and train_export.py): stratified, test_size=0.25,
random_state=42. For Cleveland that gives 297 rows after dropping missing values,
222 train / 75 test (PR2 Table 5).
"""
from __future__ import annotations

import os
import urllib.request
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RAW_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "data", "raw"))

CLEVELAND_URL = ("https://archive.ics.uci.edu/ml/machine-learning-databases/"
                 "heart-disease/processed.cleveland.data")
CLEVELAND_FILE = "processed.cleveland.data"
CLEVELAND_COLS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                  "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]

# Edinburgh MI (Kennedy et al. 1996): 1,253 patients, 9 binary features + label.
# Public copy distributed with Kim et al. (2018), iDASH 2017 Track 3 winner
# (CC BY-NC 3.0, CryptoLab). Columns are anonymised as x1..x9 in that copy.
EDINBURGH_URL = ("https://raw.githubusercontent.com/kimandrik/IDASH2017/master/"
                 "IDASH2017/data/edin.txt")
EDINBURGH_FILE = "edin.txt"

TEST_SIZE = 0.25
RANDOM_STATE = 42


@dataclass
class Dataset:
    name: str
    X: np.ndarray
    y: np.ndarray
    feature_names: list[str]


@dataclass
class Split:
    name: str
    X_train: np.ndarray      # scaled
    X_test: np.ndarray       # scaled
    y_train: np.ndarray
    y_test: np.ndarray
    scaler: StandardScaler
    feature_names: list[str]


def _download(url: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urllib.request.urlretrieve(url, path)


def load_cleveland(raw_dir: str = DEFAULT_RAW_DIR, download: bool = True) -> Dataset:
    path = os.path.join(raw_dir, CLEVELAND_FILE)
    if not os.path.exists(path):
        if not download:
            raise FileNotFoundError(path)
        _download(CLEVELAND_URL, path)
    df = pd.read_csv(path, names=CLEVELAND_COLS, na_values="?").dropna()
    X = df[CLEVELAND_COLS[:-1]].to_numpy(dtype=float)
    y = (df["num"].to_numpy() > 0).astype(int)      # 0 = no disease, 1-4 = disease
    return Dataset("cleveland", X, y, CLEVELAND_COLS[:-1])


def load_edinburgh(raw_dir: str = DEFAULT_RAW_DIR, download: bool = True) -> Dataset:
    path = os.path.join(raw_dir, EDINBURGH_FILE)
    if not os.path.exists(path):
        if not download:
            raise FileNotFoundError(path)
        _download(EDINBURGH_URL, path)
    df = pd.read_csv(path)
    X = df.iloc[:, :-1].to_numpy(dtype=float)
    y = df.iloc[:, -1].to_numpy().astype(int)
    names = [f"x{i + 1}" for i in range(X.shape[1])]
    return Dataset("edinburgh", X, y, names)


LOADERS = {"cleveland": load_cleveland, "edinburgh": load_edinburgh}


def load_dataset(name: str, raw_dir: str = DEFAULT_RAW_DIR, download: bool = True) -> Dataset:
    try:
        loader = LOADERS[name]
    except KeyError as exc:
        raise ValueError(f"unknown dataset {name!r}; use one of {sorted(LOADERS)}") from exc
    return loader(raw_dir, download)


def split_and_scale(ds: Dataset, test_size: float = TEST_SIZE,
                    random_state: int = RANDOM_STATE) -> Split:
    """Fixed stratified split, scaler fitted on the training rows only."""
    X_tr, X_te, y_tr, y_te = train_test_split(
        ds.X, ds.y, test_size=test_size, random_state=random_state, stratify=ds.y)
    scaler = StandardScaler().fit(X_tr)
    return Split(ds.name, scaler.transform(X_tr), scaler.transform(X_te),
                 y_tr, y_te, scaler, ds.feature_names)


def save_processed(split: Split, out_dir: str) -> None:
    """Write train/test CSVs (scaled) for inspection. Not committed (.gitignore)."""
    os.makedirs(out_dir, exist_ok=True)
    cols = split.feature_names + ["label"]
    for part, X, y in (("train", split.X_train, split.y_train),
                       ("test", split.X_test, split.y_test)):
        pd.DataFrame(np.column_stack([X, y]), columns=cols).to_csv(
            os.path.join(out_dir, f"{part}.csv"), index=False)
