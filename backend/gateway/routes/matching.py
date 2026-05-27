from fastapi import APIRouter, HTTPException, Request

from contracts.matching import DailyBatchRequest, EnsembleRequest, MatchRequest

router = APIRouter(tags=["matching"])


def _not_found(exc: LookupError) -> HTTPException:
    return HTTPException(status_code=404, detail={"error": str(exc), "code": "NOT_FOUND"})


@router.post("/match/candidate-to-jobs")
def match_candidate_to_jobs(body: MatchRequest, request: Request):
    try:
        return request.app.state.container.matchmaker.match_candidate_to_jobs(body)
    except LookupError as exc:
        raise _not_found(exc) from exc


@router.post("/match/job-to-candidates")
def match_job_to_candidates(body: MatchRequest, request: Request):
    try:
        return request.app.state.container.matchmaker.match_job_to_candidates(body)
    except LookupError as exc:
        raise _not_found(exc) from exc


@router.post("/match/ensemble")
def match_ensemble(body: EnsembleRequest, request: Request):
    if not body.searches:
        raise HTTPException(
            status_code=400,
            detail={"error": "At least one search config required", "code": "VALIDATION"},
        )
    try:
        return request.app.state.container.matchmaker.match_ensemble(body)
    except LookupError as exc:
        raise _not_found(exc) from exc


@router.post("/match/daily-batch")
def run_daily_batch(body: DailyBatchRequest, request: Request):
    return request.app.state.container.matchmaker.run_daily_batch(body)


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
