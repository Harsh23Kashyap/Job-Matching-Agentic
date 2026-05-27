"""Advanced scoring pipeline for Matchmaking Agent."""
from __future__ import annotations

from contracts.matching import MatchRequest, ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.calibration import PlattCalibrator
from core.constraints import apply_constraints
from core.feedback_boost import apply_feedback_adjustment
from core.fusion import LearnedFusionModel, compute_hierarchical_multimodal
from core.scoring import compute_multimodal_weighted, compute_semantic
from core.strategy_router import route_strategy
from stores.feedback_store import FeedbackStore


def score_pair_advanced(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    request: MatchRequest,
    *,
    model_name: str,
    fusion_model: LearnedFusionModel | None,
    calibrator: PlattCalibrator | None,
    feedback_store: FeedbackStore | None,
    routing_reason: str | None = None,
) -> tuple[ScoreBreakdown, list[str], str | None]:
    strategy = request.strategy
    skills_mode = request.skills_mode
    semantic_weight = request.semantic_weight
    reason = routing_reason

    if request.fusion_mode == "learned" and fusion_model is not None:
        breakdown = fusion_model.score_pair(
            candidate,
            job,
            metric=request.metric,
            skills_mode=skills_mode,
            model_name=model_name,
        )
    elif request.fusion_mode == "hierarchical":
        breakdown = compute_hierarchical_multimodal(
            candidate,
            job,
            metric=request.metric,
            skills_mode=skills_mode,
            semantic_weight=semantic_weight,
            model_name=model_name,
        )
    elif strategy == "semantic":
        breakdown = compute_semantic(candidate, job, request.metric)
    else:
        breakdown = compute_multimodal_weighted(
            candidate,
            job,
            metric=request.metric,
            semantic_weight=semantic_weight,
            skills_mode=skills_mode,
            model_name=model_name,
        )

    if reason:
        breakdown = breakdown.model_copy(update={"routing_reason": reason})

    constraint_notes: list[str] = []
    if request.apply_constraints:
        breakdown, constraint_notes = apply_constraints(breakdown, candidate, job)

    if request.use_feedback_boost and feedback_store is not None:
        counts = feedback_store.counts_for_pair(candidate.id, job.id)
        breakdown = apply_feedback_adjustment(
            breakdown,
            save_count=counts.save_count,
            dismiss_count=counts.dismiss_count,
            apply_count=counts.apply_count,
        )

    if request.use_calibration and calibrator is not None:
        cal = calibrator.calibrate(breakdown.final_score)
        breakdown = breakdown.model_copy(update={"calibrated_score": cal, "final_score": cal})

    return breakdown, constraint_notes, reason


def resolve_routing(
    candidate: CandidateSnapshot,
    request: MatchRequest,
) -> tuple[MatchRequest, str | None]:
    if not request.auto_strategy:
        return request, None
    strategy, skills_mode, sem_w, reason = route_strategy(
        candidate,
        default_strategy=request.strategy,
        default_skills_mode=request.skills_mode,
        default_semantic_weight=request.semantic_weight,
    )
    updated = request.model_copy(
        update={
            "strategy": strategy,
            "skills_mode": skills_mode,
            "semantic_weight": sem_w,
        }
    )
    return updated, reason
