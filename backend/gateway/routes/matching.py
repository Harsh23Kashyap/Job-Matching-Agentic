from fastapi import APIRouter, Request

from contracts.matching import DailyBatchRequest, EnsembleRequest, MatchRequest
from gateway.errors import api_error, lookup_not_found

router = APIRouter(tags=["matching"])


@router.post("/match/candidate-to-jobs")
def match_candidate_to_jobs(body: MatchRequest, request: Request):
    try:
        return request.app.state.container.matchmaker.match_candidate_to_jobs(body)
    except LookupError as exc:
        raise lookup_not_found(exc) from exc


@router.post("/match/job-to-candidates")
def match_job_to_candidates(body: MatchRequest, request: Request):
    try:
        return request.app.state.container.matchmaker.match_job_to_candidates(body)
    except LookupError as exc:
        raise lookup_not_found(exc) from exc


@router.post("/match/ensemble")
def match_ensemble(body: EnsembleRequest, request: Request):
    if not body.searches:
        raise api_error(400, "VALIDATION", "At least one search config required.")
    try:
        return request.app.state.container.matchmaker.match_ensemble(body)
    except LookupError as exc:
        raise lookup_not_found(exc) from exc


@router.post("/match/daily-batch")
def run_daily_batch(body: DailyBatchRequest, request: Request):
    try:
        return request.app.state.container.matchmaker.run_daily_batch(body)
    except LookupError as exc:
        raise lookup_not_found(exc) from exc
    except OSError as exc:
        raise api_error(500, "BATCH_WRITE_FAILED", f"Could not write batch output: {exc}") from exc


# Legacy aliases
@router.post("/match-resume")
def legacy_match_resume(body: MatchRequest, request: Request):
    return match_candidate_to_jobs(body, request)


@router.post("/match-job")
def legacy_match_job(body: MatchRequest, request: Request):
    return match_job_to_candidates(body, request)


@router.post("/match-resume-ensemble")
def legacy_match_resume_ensemble(body: EnsembleRequest, request: Request):
    return match_ensemble(body, request)


@router.post("/agent/run-daily-recommendations")
def legacy_daily_batch(body: DailyBatchRequest, request: Request):
    return run_daily_batch(body, request)
