"""Cross-encoder reranking over a short candidate list."""
from __future__ import annotations

import os

from core.document_text import job_document_text, resume_document_text

_cross_encoder = None
_cross_encoder_name: str | None = None


def get_cross_encoder_model_name() -> str:
    return os.environ.get("CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2").strip()


def get_cross_encoder():
    global _cross_encoder, _cross_encoder_name
    name = get_cross_encoder_model_name()
    if _cross_encoder is None or _cross_encoder_name != name:
        from sentence_transformers import CrossEncoder

        _cross_encoder = CrossEncoder(name)
        _cross_encoder_name = name
    return _cross_encoder


def rerank_jobs(
    resume: dict,
    jobs: list[dict],
    *,
    rich: bool = False,
    blend_alpha: float = 0.4,
    prior_scores: dict[str, float] | None = None,
) -> list[tuple[str, float]]:
    if not jobs:
        return []
    pairs = [
        (resume_document_text(resume, rich=rich), job_document_text(job, rich=rich))
        for job in jobs
    ]
    ce = get_cross_encoder()
    raw = ce.predict(pairs)
    lo, hi = float(min(raw)), float(max(raw))
    span = hi - lo if hi > lo else 1.0
    ranked = []
    for job, score in zip(jobs, raw):
        ce_norm = (float(score) - lo) / span
        jid = job["id"]
        if prior_scores and jid in prior_scores:
            blended = blend_alpha * prior_scores[jid] + (1.0 - blend_alpha) * ce_norm
        else:
            blended = ce_norm
        ranked.append((jid, blended))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
