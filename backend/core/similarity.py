import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def euclidean_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dist = float(np.linalg.norm(a - b))
    return 1.0 / (1.0 + dist)


def compute_similarity(a: np.ndarray, b: np.ndarray, metric: str) -> float:
    if metric == "euclidean":
        return euclidean_similarity(a, b)
    return cosine_similarity(a, b)
