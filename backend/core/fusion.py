"""Learned fusion over semantic + skills + constraint features."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.constraints import experience_factor, must_have_coverage, remote_factor, salary_factor
from core.scoring import compute_semantic
from core.skill_taxonomy import taxonomy_overlap
from core.skills import hierarchical_skills_score, skills_score

FEATURE_NAMES = [
    "semantic",
    "skills",
    "taxonomy",
    "exp_factor",
    "remote_factor",
    "salary_factor",
    "must_have_coverage",
    "bias",
]


def extract_pair_features(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> np.ndarray:
    sem = compute_semantic(candidate, job, metric).semantic_score
    sk = skills_score(candidate.skills, job.required_skills, skills_mode, model_name)
    tax = taxonomy_overlap(candidate.skills, job.required_skills)
    exp_f, _ = experience_factor(candidate, job)
    rem_f, _ = remote_factor(candidate, job)
    sal_f, _ = salary_factor(candidate, job)
    cov, _ = must_have_coverage(candidate, job)
    return np.array([sem, sk, tax, exp_f, rem_f, sal_f, cov, 1.0], dtype=np.float64)


def _sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


class LearnedFusionModel:
    def __init__(self, weights: np.ndarray | None = None) -> None:
        self.weights = weights if weights is not None else np.zeros(len(FEATURE_NAMES), dtype=np.float64)

    def predict_proba(self, features: np.ndarray) -> float:
        z = float(np.dot(features, self.weights))
        return float(_sigmoid(np.array([z]))[0])

    def score_pair(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        *,
        metric: str = "cosine",
        skills_mode: str = "jaccard",
        model_name: str = "all-MiniLM-L6-v2",
    ) -> ScoreBreakdown:
        feats = extract_pair_features(
            candidate, job, metric=metric, skills_mode=skills_mode, model_name=model_name
        )
        sem = float(feats[0])
        sk = float(feats[1])
        final = self.predict_proba(feats)
        return ScoreBreakdown(
            semantic_score=sem,
            skills_score=sk,
            final_score=final,
            strategy_used="learned_fusion",
            metric_used=metric,
            skills_mode_used=skills_mode,
            fusion_mode_used="learned",
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"feature_names": FEATURE_NAMES, "weights": self.weights.tolist()}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> LearnedFusionModel | None:
        if not path.is_file():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        weights = np.array(payload["weights"], dtype=np.float64)
        return cls(weights=weights)

    @classmethod
    def train(
        cls,
        features: np.ndarray,
        labels: np.ndarray,
        *,
        lr: float = 0.1,
        epochs: int = 800,
        l2: float = 0.01,
    ) -> LearnedFusionModel:
        w = np.zeros(features.shape[1], dtype=np.float64)
        y = labels.astype(np.float64)
        n = len(y)
        for _ in range(epochs):
            z = features @ w
            pred = _sigmoid(z)
            grad = (features.T @ (pred - y)) / n + l2 * w
            grad[-1] -= l2 * w[-1]  # don't regularize bias as strongly
            w -= lr * grad
        return cls(weights=w)


def compute_hierarchical_multimodal(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    semantic_weight: float = 0.7,
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    sem = compute_semantic(candidate, job, metric)
    skills = hierarchical_skills_score(
        candidate.skills,
        job.required_skills,
        job.preferred_skills,
        skills_mode=skills_mode,
        model_name=model_name,
    )
    alpha = semantic_weight
    final = alpha * sem.semantic_score + (1.0 - alpha) * skills
    return ScoreBreakdown(
        semantic_score=sem.semantic_score,
        skills_score=skills,
        final_score=final,
        strategy_used="multimodal",
        metric_used=metric,
        skills_mode_used=skills_mode,
        fusion_mode_used="hierarchical",
    )
