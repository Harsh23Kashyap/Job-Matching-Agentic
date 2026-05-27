from fastapi import APIRouter, HTTPException, Request

from contracts.profiles import JobProfile

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _public_profile(profile: JobProfile) -> dict:
    data = profile.model_dump()
    data.pop("embedding", None)
    return data


@router.get("")
def list_jobs(request: Request):
    return {"titles": request.app.state.container.employer.list_titles()}


@router.get("/full")
def list_jobs_full(request: Request):
    return [_public_profile(p) for p in request.app.state.container.employer.list_jobs()]


@router.get("/{title}")
def get_job(title: str, request: Request):
    profile = request.app.state.container.employer.get_by_title(title)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


@router.post("", status_code=201)
def register_job(raw: dict, request: Request):
    profile = request.app.state.container.employer.register(raw)
    return _public_profile(profile)
