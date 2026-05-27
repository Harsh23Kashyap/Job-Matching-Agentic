from fastapi import APIRouter, Depends, HTTPException, Request

from auth.deps import get_optional_user, require_role
from auth.store import User
from contracts.profiles import JobProfile
from hooks.parser_factory import make_candidate_id, make_entity_id

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _public_profile(profile: JobProfile) -> dict:
    data = profile.model_dump()
    data.pop("embedding", None)
    return data


def _slug_job_id(title: str) -> str:
    return make_entity_id(title)


@router.get("")
def list_jobs(request: Request):
    return {"titles": request.app.state.container.employer.list_titles()}


@router.get("/full")
def list_jobs_full(request: Request):
    return [_public_profile(p) for p in request.app.state.container.employer.list_jobs()]


@router.get("/mine")
def list_my_jobs(
    request: Request,
    user: User = Depends(require_role("employer")),
):
    job_ids = request.app.state.auth_store.list_job_ids(user.id)
    profiles = []
    for job_id in job_ids:
        profile = request.app.state.container.employer.get_by_id(job_id)
        if profile is not None:
            profiles.append(_public_profile(profile))
    return profiles


@router.get("/{title}")
def get_job(title: str, request: Request):
    profile = request.app.state.container.employer.get_by_title(title)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


@router.post("", status_code=201)
def register_job(
    raw: dict,
    request: Request,
    user: User | None = Depends(get_optional_user),
):
    if user is not None and user.role == "employer":
        if "id" not in raw:
            title = raw.get("title", "Untitled Job")
            raw = {**raw, "id": _slug_job_id(title)}
    profile = request.app.state.container.employer.register(raw)
    if user is not None and user.role == "employer":
        request.app.state.auth_store.link_job(user.id, profile.id)
    return _public_profile(profile)
