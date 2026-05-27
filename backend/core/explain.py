from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.skills import raw_skill_overlap


def build_why_ranked(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    scores: ScoreBreakdown,
) -> list[str]:
    reasons: list[str] = []
    overlap = raw_skill_overlap(candidate.skills, job.required_skills)
    if overlap:
        reasons.append(f"Matching skills: {', '.join(overlap[:5])}")

    title_tokens = set(job.title.lower().split())
    summary_tokens = set(candidate.summary.lower().split())
    common = title_tokens & summary_tokens
    if len(common) >= 2:
        reasons.append(f"Title/summary overlap: {', '.join(sorted(common)[:4])}")

    sem = scores.semantic_score
    if sem >= 0.65:
        reasons.append("High semantic similarity")
    elif sem >= 0.5:
        reasons.append("Moderate semantic similarity")

    if scores.strategy_used == "composite":
        if scores.experience_score is not None and scores.experience_score >= 0.8:
            reasons.append("Experience aligns with role requirement")
        if scores.compensation_score is not None and scores.compensation_score >= 0.85:
            reasons.append("Compensation expectations align")
        if scores.location_score is not None and scores.location_score >= 0.9:
            reasons.append("Remote/work setup aligns")
        reasons.append(
            "Composite score blends semantic, skills, experience, compensation, and location signals"
        )
    elif scores.strategy_used == "multimodal" and scores.skills_score is not None:
        reasons.append(
            f"Multimodal blend (semantic {scores.semantic_score:.2f}, skills {scores.skills_score:.2f})"
        )

    return reasons[:4]
