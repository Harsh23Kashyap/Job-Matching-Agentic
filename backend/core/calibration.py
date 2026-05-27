"""Platt scaling for relevance-calibrated match scores."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def _sigmoid(z: float) -> float:
    z = max(-500.0, min(500.0, z))
    return 1.0 / (1.0 + math.exp(-z))


class PlattCalibrator:
    def __init__(self, a: float = 1.0, b: float = 0.0) -> None:
        self.a = a
        self.b = b

    def calibrate(self, score: float) -> float:
        return _sigmoid(self.a * score + self.b)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"a": self.a, "b": self.b}, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> PlattCalibrator | None:
        if not path.is_file():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(a=float(payload["a"]), b=float(payload["b"]))

    @classmethod
    def fit(cls, scores: np.ndarray, labels: np.ndarray, *, epochs: int = 400, lr: float = 0.05) -> PlattCalibrator:
        a, b = 1.0, 0.0
        y = labels.astype(np.float64)
        for _ in range(epochs):
            z = a * scores + b
            pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
            err = pred - y
            da = float(np.mean(err * scores))
            db = float(np.mean(err))
            a -= lr * da
            b -= lr * db
        return cls(a=a, b=b)
