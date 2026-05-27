from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

import re

from pydantic import BaseModel

from auth.deps import get_optional_user, require_role
from auth.store import User
from contracts.profiles import CandidateProfile
from core.contact_extract import extract_contact_from_text, merge_contact_fields
from core.resume_clean import CID_RE, clean_resume_text, resume_preview_excerpt
from core.resume_suggestions import build_resume_suggestions
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
    auth_store = request.app.state.auth_store
    candidate_id = auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    candidate_agent = request.app.state.container.candidate
    profile = candidate_agent.get_by_id(candidate_id)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Profile not found. Save your profile again from the Profile page.",
                "code": "PROFILE_NOT_FOUND",
            },
        )
    return _public_profile(profile)


class SavedJobBody(BaseModel):
    job_id: str
    job_title: str
    saved: bool = True


class ApplicationBody(BaseModel):
    job_id: str
    job_title: str
    match_score: float | None = None


class ResumeSuggestionsBody(BaseModel):
    job_id: str


@router.post("/me/resume-suggestions")
def resume_suggestions_for_job(
    body: ResumeSuggestionsBody,
    request: Request,
    user: User = Depends(require_role("candidate")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    profile = request.app.state.container.candidate.get_by_id(candidate_id)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Profile not found. Save your profile again from the Profile page.",
                "code": "PROFILE_NOT_FOUND",
            },
        )

    job = request.app.state.container.employer.get_by_id(body.job_id.strip())
    if job is None:
        raise HTTPException(status_code=404, detail={"error": "Job not found", "code": "NOT_FOUND"})

    suggestions = build_resume_suggestions(profile, job, llm)
    return suggestions


@router.get("/me/saved-jobs")
def list_my_saved_jobs(
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    rows = request.app.state.activity_store.list_saved_jobs(candidate_id)
    return {"saved_jobs": [row.__dict__ for row in rows]}


@router.put("/me/saved-jobs")
def update_saved_job(
    body: SavedJobBody,
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    store = request.app.state.activity_store
    feedback = request.app.state.feedback_store
    if body.saved:
        row = store.save_job(candidate_id, body.job_id, body.job_title)
        feedback.record(candidate_id=candidate_id, job_id=body.job_id, action="save", user_id=user.id)
        return {"saved_job": row.__dict__}
    removed = store.unsave_job(candidate_id, body.job_id)
    if removed:
        feedback.record(candidate_id=candidate_id, job_id=body.job_id, action="dismiss", user_id=user.id)
    return {"removed": removed}


@router.get("/me/applications")
def list_my_applications(
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    rows = request.app.state.activity_store.list_applications_for_candidate(candidate_id)
    return {"applications": [row.__dict__ for row in rows]}


@router.post("/me/applications", status_code=201)
def create_application(
    body: ApplicationBody,
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    candidate_id = request.app.state.auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
    profile = request.app.state.container.candidate.get_by_id(candidate_id)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Profile not found", "code": "NOT_FOUND"})
    app_row = request.app.state.activity_store.apply(
        candidate_id=candidate_id,
        candidate_name=profile.name,
        job_id=body.job_id,
        job_title=body.job_title,
        match_score=body.match_score,
    )
    request.app.state.feedback_store.record(
        candidate_id=candidate_id,
        job_id=body.job_id,
        action="apply",
        user_id=user.id,
    )
    return app_row.__dict__


@router.post("/upload-resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    user: User = Depends(require_role("candidate")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    raw_text = extract_text_from_upload(file)
    text = clean_resume_text(raw_text)
    regex_contact = extract_contact_from_text(text)
    preview = resume_preview_excerpt(text)
    empty_fields = {
        "name": regex_contact.get("name") or "",
        "skills": [],
        "experience_years": 0,
        "preferred_salary": None,
        "remote_preference": False,
        "summary": "",
        "email": regex_contact.get("email") or "",
        "phone": regex_contact.get("phone") or "",
        "linkedin": regex_contact.get("linkedin") or "",
        "portfolio": regex_contact.get("portfolio") or "",
        "other_links": regex_contact.get("other_links") or [],
    }
    try:
        extracted = llm.parse_candidate_from_text(text)
        extracted = merge_contact_fields(extracted, regex_contact)
    except LlmUnavailableError:
        return {
            "extracted_fields": merge_contact_fields(empty_fields, regex_contact),
            "raw_text_preview": preview,
            "cleaned_text": text,
            "llm_status": "unavailable",
            "message": "Automatic extraction unavailable. Review the text preview and fill in details manually.",
        }
    except LlmParseError as exc:
        return {
            "extracted_fields": merge_contact_fields(empty_fields, regex_contact),
            "raw_text_preview": preview,
            "cleaned_text": text,
            "llm_status": "parse_failed",
            "message": f"Could not parse resume automatically ({exc}). Fill in details manually.",
        }
    return {
        "extracted_fields": extracted,
        "raw_text_preview": preview,
        "cleaned_text": text,
        "llm_status": "ok",
    }


@router.get("/{name}")
def get_candidate(name: str, request: Request):
    profile = request.app.state.container.candidate.get_by_name(name)
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": "Candidate not found", "code": "NOT_FOUND"})
    return _public_profile(profile)


def _sanitize_profile_payload(raw: dict) -> dict:
    payload = dict(raw)
    if not str(payload.get("id") or "").strip():
        payload.pop("id", None)
    for key in ("name", "email", "phone", "linkedin", "portfolio"):
        value = payload.get(key)
        if value:
            cleaned = CID_RE.sub("", str(value))
            cleaned = re.sub(r"\s*(?:,\s*)+$", "", cleaned).strip()
            payload[key] = cleaned.strip()
    summary = payload.get("summary")
    if summary:
        payload["summary"] = clean_resume_text(str(summary))
    return payload


def _upsert_my_candidate(raw: dict, request: Request, user: User) -> dict:
    """Create or update the logged-in candidate profile and ensure ownership link."""
    raw = _sanitize_profile_payload(raw)
    auth_store = request.app.state.auth_store
    candidate_agent = request.app.state.container.candidate
    candidate_id = auth_store.get_candidate_id(user.id)
    if candidate_id is None:
        payload = dict(raw)
        if "id" not in payload:
            name = payload.get("name", "Unknown Candidate")
            payload = {**payload, "id": make_candidate_id(name)}
        profile = candidate_agent.register(payload)
        auth_store.link_candidate(user.id, profile.id)
        return _public_profile(profile)
    payload = {**raw, "id": candidate_id}
    profile = candidate_agent.register(payload)
    auth_store.link_candidate(user.id, profile.id)
    return _public_profile(profile)


@router.put("/me")
def upsert_my_candidate(
    raw: dict,
    request: Request,
    user: User = Depends(require_role("candidate")),
):
    return _upsert_my_candidate(raw, request, user)


@router.post("", status_code=201)
def register_candidate(
    raw: dict,
    request: Request,
    user: User | None = Depends(get_optional_user),
):
    if user is not None and user.role == "candidate":
        return _upsert_my_candidate(raw, request, user)

    payload = _sanitize_profile_payload(raw)
    profile = request.app.state.container.candidate.register(payload)
    return _public_profile(profile)
