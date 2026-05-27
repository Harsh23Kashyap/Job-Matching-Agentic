"""Baseline fairness metrics on ranked match lists."""
from __future__ import annotations

from collections import defaultdict


def experience_group(years: float) -> str:
    if years < 2:
        return "junior"
    if years < 5:
        return "mid"
    return "senior"


def remote_group(prefers_remote: bool) -> str:
    return "remote_seeker" if prefers_remote else "onsite_flexible"


def top_k_selection_rate(
    ranked_by_query: dict[str, list[tuple[str, float]]],
    query_groups: dict[str, str],
    *,
    top_k: int = 1,
) -> dict[str, float | None]:
    """Fraction of queries in each group where top-k average score exceeds corpus median."""
    group_scores: dict[str, list[float]] = defaultdict(list)
    for qid, ranked in ranked_by_query.items():
        group = query_groups.get(qid, "unknown")
        if not ranked:
            continue
        top_scores = [score for _, score in ranked[:top_k]]
        group_scores[group].append(sum(top_scores) / len(top_scores))

    all_scores = [s for scores in group_scores.values() for s in scores]
    if not all_scores:
        return {}
    median = sorted(all_scores)[len(all_scores) // 2]

    rates: dict[str, float | None] = {}
    for group, scores in group_scores.items():
        if not scores:
            rates[group] = None
            continue
        above = sum(1 for s in scores if s >= median)
        rates[group] = above / len(scores)
    return rates


def disparate_impact_ratio(rates: dict[str, float | None]) -> float | None:
    """Ratio of minimum to maximum group selection rate (1.0 = parity)."""
    valid = [v for v in rates.values() if v is not None and v > 0]
    if len(valid) < 2:
        return None
    return min(valid) / max(valid)


def evaluate_fairness_report(
    ranked_by_query: dict[str, list[tuple[str, float]]],
    query_metadata: dict[str, dict],
) -> dict:
    """Build a fairness summary using experience and remote-preference proxies."""
    exp_groups = {qid: experience_group(meta.get("experience_years", 0)) for qid, meta in query_metadata.items()}
    rem_groups = {qid: remote_group(bool(meta.get("remote_preference", False))) for qid, meta in query_metadata.items()}

    exp_rates = top_k_selection_rate(ranked_by_query, exp_groups)
    rem_rates = top_k_selection_rate(ranked_by_query, rem_groups)

    return {
        "experience_groups": exp_rates,
        "remote_groups": rem_rates,
        "experience_disparate_impact": disparate_impact_ratio(exp_rates),
        "remote_disparate_impact": disparate_impact_ratio(rem_rates),
        "note": "Proxy groups on synthetic corpus; not demographic inference.",
    }
