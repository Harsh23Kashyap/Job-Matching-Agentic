from fastapi import APIRouter, HTTPException, Request

from contracts.profiles import CandidateProfile

router = APIRouter(prefix="/candidates", tags=["candidates"])


def _public_profile(profile: CandidateProfile) -> dict:
    data = profile.model_dump()
    data.pop("embedding", None)
    return data


@router.get("")
def list_candidates(request: Request):
    return {"names": request.app.state.container.candidate.list_names()}


@router.get("/full")
def list_candidates_full(request: Request):
    return [_public_profile(p) for p in request.app.state.container.candidate.list_profiles()]


@router.get("/{name}")
def get_candidate(name: str, request: Request):
    profile = request.app.state.container.candidate.get_by_name(name)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Candidate not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


@router.post("", status_code=201)
def register_candidate(raw: dict, request: Request):
    profile = request.app.state.container.candidate.register(raw)
    return _public_profile(profile)
