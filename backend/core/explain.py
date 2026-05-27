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

    if scores.title_score is not None and scores.title_score >= 0.65:
        reasons.append(f"Role title aligns with your profile ({scores.title_score:.0%} title fit)")
    elif scores.title_score is not None and scores.title_score < 0.35:
        reasons.append("Role title differs from your stated background")

    sem = scores.semantic_score
    if sem >= 0.65:
        reasons.append("High semantic similarity")
    elif sem >= 0.5:
        reasons.append("Moderate semantic similarity")

    if scores.strategy_used == "composite":
        if scores.experience_score is not None and scores.experience_score >= 0.8:
            reasons.append("Experience aligns with role requirement")
        elif scores.experience_score is not None and scores.experience_score <= 0.4:
            reasons.append("Experience gap vs role requirement")
        if scores.compensation_score is not None and scores.compensation_score >= 0.85:
            reasons.append("Compensation expectations align")
        elif scores.compensation_score is not None and scores.compensation_score <= 0.5:
            reasons.append("Compensation expectations may exceed budget")
        remote = scores.remote_score if scores.remote_score is not None else scores.location_score
        if remote is not None and remote >= 0.9:
            reasons.append("Remote/work setup aligns")
        elif remote is not None and remote <= 0.5:
            reasons.append("Remote preference may not match role setup")
        if scores.score_components:
            top = max(scores.score_components, key=lambda item: item.contribution)
            weak = min(scores.score_components, key=lambda item: item.score)
            reasons.append(
                f"Top driver: {top.label} ({top.score:.0%}); weakest signal: {weak.label} ({weak.score:.0%})"
            )
        else:
            reasons.append(
                "Composite score blends semantic fit, skills, title, experience, compensation, and remote preference"
            )
    elif scores.strategy_used == "multimodal" and scores.skills_score is not None:
        reasons.append(
            f"Multimodal blend (semantic {scores.semantic_score:.2f}, skills {scores.skills_score:.2f})"
        )

    return reasons[:5]
