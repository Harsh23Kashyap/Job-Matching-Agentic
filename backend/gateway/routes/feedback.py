from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

from auth.deps import get_current_user, get_optional_user
from auth.store import User
from gateway.errors import (
    forbidden,
    job_not_found,
    no_profile_linked,
    profile_stale,
    validation_error,
)

router = APIRouter(prefix="/feedback", tags=["feedback"])

CANDIDATE_ACTIONS = frozenset({"save", "not_interested", "apply", "unsave"})
EMPLOYER_ACTIONS = frozenset({"save", "reject", "contact", "unsave"})


class FeedbackRequest(BaseModel):
    candidate_id: str
    job_id: str
    action: str = Field(pattern="^(save|dismiss|apply)$")


class FeedbackActionRequest(BaseModel):
    target_id: str
    action: str
    context_id: str | None = None
    target_label: str = ""
    match_score: float | None = None


def _pair_action(action: str) -> str | None:
    if action in {"save", "apply"}:
        return action
    if action in {"not_interested", "reject"}:
        return "dismiss"
    return None


def _record_match_pair(feedback_store, *, candidate_id: str, job_id: str, action: str, user_id: str) -> None:
    pair_action = _pair_action(action)
    if pair_action:
        feedback_store.record(
            candidate_id=candidate_id,
            job_id=job_id,
            action=pair_action,
            user_id=user_id,
        )


def _require_employer_job(request: Request, user: User, job_id: str) -> None:
    owned = request.app.state.auth_store.list_job_ids(user.id)
    if job_id not in owned:
        raise job_not_found()


@router.get("/me")
def my_feedback(
    request: Request,
    user: User = Depends(get_current_user),
    context_id: str | None = Query(default=None),
):
    rows = request.app.state.feedback_store.list_latest_for_user(user.id, context_id=context_id)
    return {"feedback": [row.__dict__ for row in rows]}


@router.post("/actions")
def record_feedback_action(body: FeedbackActionRequest, request: Request, user: User = Depends(get_current_user)):
    feedback_store = request.app.state.feedback_store
    auth_store = request.app.state.auth_store
    activity_store = request.app.state.activity_store

    if user.role == "candidate":
        allowed = CANDIDATE_ACTIONS
    elif user.role == "employer":
        allowed = EMPLOYER_ACTIONS
    else:
        raise forbidden("Role cannot record feedback.")

    if body.action not in allowed:
        raise validation_error(f"Invalid action '{body.action}' for role '{user.role}'.")

    if user.role == "employer":
        if not body.context_id:
            raise validation_error("context_id (job_id) is required for employer feedback.")
        _require_employer_job(request, user, body.context_id)

    if body.action == "unsave":
        if user.role == "candidate":
            candidate_id = auth_store.get_candidate_id(user.id)
            if candidate_id is None:
                raise no_profile_linked()
            activity_store.unsave_job(candidate_id, body.target_id)
        row = feedback_store.record_user_action(
            user_id=user.id,
            target_id=body.target_id,
            action="unsave",
            role=user.role,
            context_id=body.context_id,
        )
        return {"ok": True, "feedback": row.__dict__}

    if user.role == "candidate":
        candidate_id = auth_store.get_candidate_id(user.id)
        if candidate_id is None:
            raise no_profile_linked()
        profile = request.app.state.container.candidate.get_by_id(candidate_id)
        if profile is None:
            raise profile_stale()
        job_id = body.target_id
        if request.app.state.container.employer.get_by_id(job_id) is None:
            raise job_not_found()
        if body.action == "apply":
            activity_store.apply(
                candidate_id=candidate_id,
                candidate_name=profile.name,
                job_id=job_id,
                job_title=body.target_label or job_id,
                match_score=body.match_score,
            )

    row = feedback_store.record_user_action(
        user_id=user.id,
        target_id=body.target_id,
        action=body.action,
        role=user.role,
        context_id=body.context_id,
    )

    if user.role == "candidate":
        candidate_id = auth_store.get_candidate_id(user.id)
        job_id = body.target_id
        _record_match_pair(
            feedback_store,
            candidate_id=candidate_id,
            job_id=job_id,
            action=body.action,
            user_id=user.id,
        )
        if body.action == "save":
            activity_store.save_job(candidate_id, job_id, body.target_label or job_id)
    else:
        candidate_id = body.target_id
        job_id = body.context_id or ""
        _record_match_pair(
            feedback_store,
            candidate_id=candidate_id,
            job_id=job_id,
            action=body.action,
            user_id=user.id,
        )

    return {"ok": True, "feedback": row.__dict__}


@router.post("")
def record_feedback(body: FeedbackRequest, request: Request, user=Depends(get_optional_user)):
    store = request.app.state.feedback_store
    user_id = user.id if user is not None else None
    try:
        store.record(
            candidate_id=body.candidate_id,
            job_id=body.job_id,
            action=body.action,
            user_id=user_id,
        )
    except ValueError as exc:
        raise validation_error(str(exc)) from exc
    return {"ok": True}


@router.get("/counts")
def feedback_counts(candidate_id: str, job_id: str, request: Request):
    counts = request.app.state.feedback_store.counts_for_pair(candidate_id, job_id)
    return counts.__dict__
