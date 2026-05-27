from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from auth.deps import get_optional_user, require_role
from auth.store import User
from contracts.profiles import JobProfile
from core.resume_text import extract_text_from_upload
from hooks.llm_parser import LlmParseError, LlmParser, LlmUnavailableError
from hooks.parser_factory import create_llm_parser, make_candidate_id, make_entity_id

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _get_llm_parser(request: Request) -> LlmParser:
    return create_llm_parser(request.app.state.container.settings)


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


@router.post("/upload-description")
async def upload_job_description(
    file: UploadFile = File(...),
    user: User = Depends(require_role("employer")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    text = extract_text_from_upload(file)
    preview = text[:500] + ("…" if len(text) > 500 else "")
    empty_fields = {
        "title": "",
        "required_skills": [],
        "required_experience": 0,
        "description": "",
        "company": "",
        "location": "",
        "remote_policy": False,
        "link": "",
    }
    try:
        extracted = llm.parse_job_from_text(text)
    except LlmUnavailableError:
        return {
            "extracted_fields": empty_fields,
            "raw_text_preview": preview,
            "llm_status": "unavailable",
            "message": "AI extraction unavailable. Review the text preview and fill in job details manually.",
        }
    except LlmParseError as exc:
        return {
            "extracted_fields": empty_fields,
            "raw_text_preview": preview,
            "llm_status": "parse_failed",
            "message": f"Could not parse job description automatically ({exc}). Fill in details manually.",
        }
    return {
        "extracted_fields": extracted,
        "raw_text_preview": preview,
        "llm_status": "ok",
    }


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
