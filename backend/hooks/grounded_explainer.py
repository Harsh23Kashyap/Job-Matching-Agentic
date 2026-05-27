"""LLM explainer grounded in structured match features — no hallucinated fields."""
from __future__ import annotations

from contracts.interfaces import Explainer
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.explain import build_why_ranked
from core.skills import skill_overlap_details


class GroundedLlmExplainer(Explainer):
    """Template-first explainer; optional LLM polish when available."""

    def explain(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
    ) -> list[str]:
        base = build_why_ranked(candidate, job, scores)
        matched, missing = skill_overlap_details(candidate.skills, job.required_skills)
        if scores.constraint_factor is not None and scores.constraint_factor < 0.95:
            base.append(f"Constraint adjustment applied (×{scores.constraint_factor:.2f})")
        if scores.calibrated_score is not None:
            base.append(f"Calibrated relevance: {scores.calibrated_score:.0%}")
        if scores.routing_reason:
            base.append(scores.routing_reason)
        if missing:
            base.append(f"Gaps: {', '.join(missing[:3])}")
        return base[:5]

    def narrative(self, candidate: CandidateSnapshot, job: JobSnapshot, scores: ScoreBreakdown) -> str:
        bullets = self.explain(candidate, job, scores)
        return " ".join(bullets)
