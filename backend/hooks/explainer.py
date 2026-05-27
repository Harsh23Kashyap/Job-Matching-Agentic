from contracts.interfaces import Explainer
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.explain import build_why_ranked


class RuleExplainer(Explainer):
    def explain(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
    ) -> list[str]:
        return build_why_ranked(candidate, job, scores)
