from fastapi import APIRouter, Depends, HTTPException, Query, Request

from auth.deps import require_role
from auth.store import User
from core.similar_entities import find_similar_candidates, find_similar_jobs

router = APIRouter(prefix="/similar", tags=["similar"])


@router.get("/jobs/{job_id}")
def similar_jobs(
    job_id: str,
    request: Request,
    _user: User = Depends(require_role("candidate")),
    limit: int = Query(default=3, ge=1, le=10),
):
    employer = request.app.state.container.employer
    job = employer.get_by_id(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})

    items = find_similar_jobs(employer, job_id, limit=limit)
    return {
        "anchor_id": job_id,
        "anchor_label": job.title,
        "items": items,
    }


@router.get("/candidates/{candidate_id}")
def similar_candidates(
    candidate_id: str,
    request: Request,
    _user: User = Depends(require_role("employer")),
    limit: int = Query(default=3, ge=1, le=10),
):
    candidate_agent = request.app.state.container.candidate
    profile = candidate_agent.get_by_id(candidate_id)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Candidate not found", "code": "NOT_FOUND"})

    items = find_similar_candidates(candidate_agent, candidate_id, limit=limit)
    return {
        "anchor_id": candidate_id,
        "anchor_label": profile.name,
        "items": items,
    }
