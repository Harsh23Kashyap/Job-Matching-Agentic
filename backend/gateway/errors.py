"""Shared API error helpers, consistent {error, code} envelope via HTTPException."""

from __future__ import annotations

from fastapi import HTTPException
from pydantic import ValidationError


def api_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"error": message, "code": code})


def validation_error(message: str) -> HTTPException:
    return api_error(422, "VALIDATION", message)


def not_found(message: str, *, code: str = "NOT_FOUND") -> HTTPException:
    return api_error(404, code, message)


def forbidden(message: str, *, code: str = "FORBIDDEN") -> HTTPException:
    return api_error(403, code, message)


def storage_error(message: str = "Database temporarily unavailable. Try again shortly.") -> HTTPException:
    return api_error(503, "STORAGE_ERROR", message)


# --- Auth ---

def unauthorized() -> HTTPException:
    return api_error(401, "UNAUTHORIZED", "Authentication required.")


def invalid_credentials() -> HTTPException:
    return api_error(401, "INVALID_CREDENTIALS", "Invalid email or password.")


# --- Candidate profile ---

PROFILE_NOT_FOUND_MSG = "Profile not found. Save your profile again from the Profile page."


def no_profile_linked() -> HTTPException:
    return not_found("No profile linked to this account.", code="NOT_FOUND")


def profile_stale() -> HTTPException:
    return not_found(PROFILE_NOT_FOUND_MSG, code="PROFILE_NOT_FOUND")


def candidate_not_owned() -> HTTPException:
    return forbidden("This profile id belongs to another account.", code="CANDIDATE_NOT_OWNED")


def profile_already_linked() -> HTTPException:
    return api_error(409, "PROFILE_ALREADY_LINKED", "A profile is already linked to this account.")


# --- Jobs ---

def job_not_found() -> HTTPException:
    return not_found("Job not found.")


def job_not_owned() -> HTTPException:
    return forbidden("This role id belongs to another account.", code="JOB_NOT_OWNED")


# --- Matching ---

def match_candidate_not_found(query_key: str) -> HTTPException:
    return not_found(f"No candidate profile matches '{query_key}'.")


def match_job_not_found(query_key: str) -> HTTPException:
    return not_found(f"No job posting matches '{query_key}'.")


def lookup_not_found(exc: LookupError) -> HTTPException:
    message = str(exc)
    if message.startswith("Candidate not found:"):
        query_key = message.split(":", 1)[1].strip()
        return match_candidate_not_found(query_key)
    if message.startswith("Job not found:"):
        query_key = message.split(":", 1)[1].strip()
        return match_job_not_found(query_key)
    return not_found(message)


# --- File parsing ---

def empty_file() -> HTTPException:
    return api_error(400, "EMPTY_FILE", "Empty file.")


def file_too_large() -> HTTPException:
    return api_error(400, "FILE_TOO_LARGE", "File too large (max 5MB).")


def unsupported_file_type() -> HTTPException:
    return api_error(
        400,
        "UNSUPPORTED_TYPE",
        "Unsupported file type. Use PDF, DOCX, or TXT.",
    )


def no_extractable_text(kind: str = "file") -> HTTPException:
    if kind == "pdf":
        return api_error(
            400,
            "NO_TEXT",
            "Could not extract text from PDF. Use a text-based PDF or enter details manually.",
        )
    return api_error(400, "NO_TEXT", f"Could not extract text from {kind.upper()}.")


def invalid_docx() -> HTTPException:
    return api_error(400, "INVALID_DOCX", "Invalid DOCX file.")


def corrupt_pdf() -> HTTPException:
    return api_error(400, "INVALID_PDF", "Could not read PDF file. It may be corrupt or password-protected.")


def payload_validation_error(exc: ValidationError) -> HTTPException:
    first = exc.errors()[0]
    field = ".".join(str(part) for part in first.get("loc", ()))
    msg = first.get("msg", "Invalid request body.")
    if field:
        return validation_error(f"{field}: {msg}")
    return validation_error(msg)


def missing_field(field: str) -> HTTPException:
    return validation_error(f"{field} is required.")
