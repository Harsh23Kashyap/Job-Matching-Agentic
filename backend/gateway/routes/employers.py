from fastapi import APIRouter, Depends, File, Request, UploadFile

from pydantic import BaseModel

from auth.deps import get_optional_user, require_role
from auth.store import User
from contracts.profiles import JobProfile
from core.document_parse import parse_job_document
from core.job_quality import analyze_job_quality
from core.resume_text import extract_text_from_upload
from gateway.errors import (
    api_error,
    job_not_found,
    job_not_owned,
    missing_field,
    validation_error,
)
from hooks.llm_parser import LlmParser
from hooks.parser_factory import create_llm_parser, make_entity_id

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


def _parse_job_description_text(llm: LlmParser, text: str) -> dict:
    result = parse_job_document(text, llm)
    extracted = result.get("extracted_fields") or {}
    result["quality"] = analyze_job_quality(_quality_payload_from_extracted(extracted))
    return result


def _quality_payload_from_extracted(extracted: dict) -> dict:
    return {
        "title": extracted.get("title") or "",
        "company": extracted.get("company") or "",
        "location": extracted.get("location") or "",
        "job_type": extracted.get("job_type") or "",
        "required_skills": extracted.get("required_skills") or [],
        "required_experience": extracted.get("required_experience") or 0,
        "budget_currency": extracted.get("budget_currency") or "INR",
        "budget_min": extracted.get("budget_min"),
        "budget_max": extracted.get("budget_max"),
        "budget": extracted.get("budget"),
        "remote_policy": bool(extracted.get("remote_policy")),
        "description": extracted.get("description") or "",
    }


@router.post("/upload-description")
async def upload_job_description(
    file: UploadFile = File(...),
    user: User = Depends(require_role("employer")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    text = extract_text_from_upload(file)
    if len(text.strip()) < 40:
        raise validation_error("Job description text is too short to extract from.")
    if len(text.strip()) > 50000:
        raise api_error(400, "TEXT_TOO_LONG", "Job description text exceeds the 50,000 character limit.")
    return _parse_job_description_text(llm, text)


class ParseJobDescriptionBody(BaseModel):
    text: str


@router.post("/parse-description")
async def parse_job_description(
    body: ParseJobDescriptionBody,
    user: User = Depends(require_role("employer")),
    llm: LlmParser = Depends(_get_llm_parser),
):
    cleaned = body.text.strip()
    if len(cleaned) < 40:
        raise api_error(
            400,
            "TEXT_TOO_SHORT",
            "Job description text is too short to extract from.",
        )
    if len(cleaned) > 50000:
        raise api_error(
            400,
            "TEXT_TOO_LONG",
            "Job description text exceeds the 50,000 character limit.",
        )
    return _parse_job_description_text(llm, cleaned)


@router.post("/quality-check")
def check_job_quality(
    raw: dict,
    user: User = Depends(require_role("employer")),
):
    return analyze_job_quality(dict(raw))


@router.get("/{title}")
def get_job(title: str, request: Request):
    profile = request.app.state.container.employer.get_by_title(title)
    if profile is None:
        raise job_not_found()
    return _public_profile(profile)


def _employer_owns_job(request: Request, user: User, job_id: str) -> None:
    job_ids = request.app.state.auth_store.list_job_ids(user.id)
    if job_id not in job_ids:
        raise job_not_found()


class JobStatusBody(BaseModel):
    status: str


def _validate_job_payload(raw: dict) -> dict:
    payload = dict(raw)
    if not str(payload.get("title") or "").strip():
        raise missing_field("title")
    return payload


@router.put("/mine/{job_id}")
def update_my_job(
    job_id: str,
    raw: dict,
    request: Request,
    user: User = Depends(require_role("employer")),
):
    _employer_owns_job(request, user, job_id)
    payload = {**_validate_job_payload(raw), "id": job_id}
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
        raise api_error(400, "INVALID_STATUS", "Invalid status. Use open, closed, or draft.")
    employer = request.app.state.container.employer
    existing = employer.get_by_id(job_id)
    if existing is None:
        raise job_not_found()
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
    raw = _validate_job_payload(raw)
    auth_store = request.app.state.auth_store

    if user is not None and user.role == "employer":
        if "id" not in raw:
            title = raw.get("title", "Untitled Job")
            raw = {**raw, "id": _slug_job_id(title)}
        if "status" not in raw:
            raw = {**raw, "status": "open"}
        job_id = str(raw["id"])
        owner = auth_store.get_job_owner(job_id)
        if owner is not None and owner != user.id:
            raise job_not_owned()
        profile = request.app.state.container.employer.register(raw)
        if not auth_store.link_job_if_unowned(user.id, profile.id):
            raise job_not_owned()
        return _public_profile(profile)

    if "id" not in raw:
        raw = {**raw, "id": _slug_job_id(raw["title"])}
    profile = request.app.state.container.employer.register(raw)
    return _public_profile(profile)
