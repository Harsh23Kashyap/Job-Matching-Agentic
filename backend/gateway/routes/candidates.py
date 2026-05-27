from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from auth.deps import get_optional_user, require_role
from auth.store import ProfileAlreadyLinkedError, User
from contracts.profiles import CandidateProfile
from core.resume_text import extract_text_from_upload
from hooks.llm_parser import LlmParseError, LlmParser, LlmUnavailableError
from hooks.parser_factory import create_llm_parser, make_candidate_id

router = APIRouter(prefix="/candidates", tags=["candidates"])


def _public_profile(profile: CandidateProfile) -> dict:
    data = profile.model_dump()
    data.pop("embedding", None)
    return data


def _get_llm_parser(request: Request) -> LlmParser:
    return create_llm_parser(request.app.state.container.settings)


@router.get("")
def list_candidates(request: Request):
    return {"names": request.app.state.container.candidate.list_names()}


@router.get("/full")
def list_candidates_full(request: Request):
    return [_public_profile(p) for p in request.app.state.container.candidate.list_profiles()]


@router.get("/me")
def get_my_candidate(
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    profile = request.app.state.container.candidate.get_by_id(candidate_id)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Profile not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


@router.post("/upload-resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    user: User = Depends(require_role("candidate")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    text = extract_text_from_upload(file)
    try:
        extracted = llm.parse_candidate_from_text(text)
    except LlmUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail={"error": str(exc), "code": "LLM_UNAVAILABLE"},
        ) from exc
    except LlmParseError as exc:
        raise HTTPException(
            status_code=422,
            detail={"error": f"Could not parse resume: {exc}", "code": "PARSE_FAILED"},
        ) from exc
    preview = text[:500] + ("…" if len(text) > 500 else "")
    return {"extracted_fields": extracted, "raw_text_preview": preview}


@router.get("/{name}")
def get_candidate(name: str, request: Request):
    profile = request.app.state.container.candidate.get_by_name(name)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Candidate not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


@router.post("", status_code=201)
def register_candidate(
    raw: dict,
    request: Request,
    user: User | None = Depends(get_optional_user),
):
    store = request.app.state.auth_store
    if user is not None and user.role == "candidate":
        existing_id = store.get_candidate_id(user.id)
        if existing_id is not None:
            if raw.get("id") != existing_id:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Profile already exists", "code": "PROFILE_EXISTS"},
                )
        elif "id" not in raw:
            name = raw.get("name", "Unknown Candidate")
            raw = {**raw, "id": make_candidate_id(name)}
    profile = request.app.state.container.candidate.register(raw)
    if user is not None and user.role == "candidate" and store.get_candidate_id(user.id) is None:
        try:
            store.link_candidate(user.id, profile.id)
        except ProfileAlreadyLinkedError:
            raise HTTPException(
                status_code=400,
                detail={"error": "Profile already linked", "code": "PROFILE_EXISTS"},
            ) from None
    return _public_profile(profile)
