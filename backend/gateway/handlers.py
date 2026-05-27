import logging
import sqlite3

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from auth.store import CandidateIdOwnedError, DuplicateEmailError, JobIdOwnedError, ProfileAlreadyLinkedError
from gateway.errors import (
    api_error,
    payload_validation_error,
    storage_error,
)

logger = logging.getLogger(__name__)


def _error_body(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": {"error": message, "code": code}})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(_request: Request, exc: RequestValidationError):
        errors = exc.errors()
        if not errors:
            return _error_body(422, "VALIDATION", "Invalid request body.")
        first = errors[0]
        loc = [str(part) for part in first.get("loc", ()) if part != "body"]
        field = ".".join(loc) if loc else "body"
        msg = first.get("msg", "Invalid value.")
        return _error_body(422, "VALIDATION", f"{field}: {msg}")

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(_request: Request, exc: ValidationError):
        err = payload_validation_error(exc)
        return _error_body(err.status_code, err.detail["code"], err.detail["error"])

    @app.exception_handler(KeyError)
    async def key_error_handler(_request: Request, exc: KeyError):
        return _error_body(422, "VALIDATION", f"Missing required field: {exc.args[0]}")

    @app.exception_handler(sqlite3.Error)
    async def sqlite_error_handler(_request: Request, exc: sqlite3.Error):
        logger.exception("SQLite error: %s", exc)
        err = storage_error()
        return _error_body(err.status_code, err.detail["code"], err.detail["error"])

    @app.exception_handler(ProfileAlreadyLinkedError)
    async def profile_already_linked_handler(_request: Request, exc: ProfileAlreadyLinkedError):
        err = api_error(409, "PROFILE_ALREADY_LINKED", str(exc))
        return _error_body(err.status_code, err.detail["code"], err.detail["error"])

    @app.exception_handler(CandidateIdOwnedError)
    async def candidate_id_owned_handler(_request: Request, _exc: CandidateIdOwnedError):
        err = api_error(403, "CANDIDATE_NOT_OWNED", "This profile id belongs to another account.")
        return _error_body(err.status_code, err.detail["code"], err.detail["error"])

    @app.exception_handler(JobIdOwnedError)
    async def job_id_owned_handler(_request: Request, _exc: JobIdOwnedError):
        err = api_error(403, "JOB_NOT_OWNED", "This role id belongs to another account.")
        return _error_body(err.status_code, err.detail["code"], err.detail["error"])
