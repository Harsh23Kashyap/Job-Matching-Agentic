from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from pydantic import BaseModel

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


@router.get("/mine/applications")
def list_applications_for_my_jobs(
    request: Request,
    user: User = Depends(require_role("employer")),
):
    job_ids = request.app.state.auth_store.list_job_ids(user.id)
    rows = request.app.state.activity_store.list_applications_for_jobs(job_ids)
    return {"applications": [row.__dict__ for row in rows]}


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


def _employer_owns_job(request: Request, user: User, job_id: str) -> None:
    job_ids = request.app.state.auth_store.list_job_ids(user.id)
    if job_id not in job_ids:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})


class JobStatusBody(BaseModel):
    status: str


@router.put("/mine/{job_id}")
def update_my_job(
    job_id: str,
    raw: dict,
    request: Request,
    user: User = Depends(require_role("employer")),
):
    _employer_owns_job(request, user, job_id)
    payload = {**raw, "id": job_id}
    profile = request.app.state.container.employer.register(payload)
    return _public_profile(profile)


@router.patch("/mine/{job_id}/status")
def update_my_job_status(
    job_id: str,
    body: JobStatusBody,
    request: Request,
    user: User = Depends(require_role("employer")),
):
    _employer_owns_job(request, user, job_id)
    status = body.status.lower()
    if status not in {"open", "closed", "draft"}:
        raise HTTPException(status_code=400, detail={"error": "Invalid status", "code": "INVALID_STATUS"})
    employer = request.app.state.container.employer
    existing = employer.get_by_id(job_id)
    if existing is None:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})
    payload = existing.model_dump()
    payload["status"] = status
    if status == "closed":
        payload["accepts_applications"] = False
    elif status == "open":
        payload["accepts_applications"] = True
    profile = employer.register(payload)
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
        if "status" not in raw:
            raw = {**raw, "status": "open"}
    profile = request.app.state.container.employer.register(raw)
    if user is not None and user.role == "employer":
        request.app.state.auth_store.link_job(user.id, profile.id)
    return _public_profile(profile)
