"""Apply interaction feedback boosts to match scores."""
from __future__ import annotations

from contracts.matching import ScoreBreakdown

SAVE_BOOST = 0.04
DISMISS_PENALTY = 0.06
APPLY_BOOST = 0.06


def apply_feedback_adjustment(
    breakdown: ScoreBreakdown,
    *,
    save_count: int = 0,
    dismiss_count: int = 0,
    apply_count: int = 0,
) -> ScoreBreakdown:
    delta = save_count * SAVE_BOOST + apply_count * APPLY_BOOST - dismiss_count * DISMISS_PENALTY
    if delta == 0:
        return breakdown
    adjusted = max(0.0, min(1.0, breakdown.final_score + delta))
    return breakdown.model_copy(update={"final_score": adjusted, "feedback_delta": delta})
