from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from auth.deps import get_current_user, get_optional_user
from auth.store import User

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
        raise HTTPException(status_code=403, detail={"error": "Role cannot record feedback", "code": "FORBIDDEN"})

    if body.action not in allowed:
        raise HTTPException(
            status_code=422,
            detail={"error": f"Invalid action '{body.action}' for role '{user.role}'", "code": "VALIDATION"},
        )

    if user.role == "employer" and not body.context_id:
        raise HTTPException(
            status_code=422,
            detail={"error": "context_id (job_id) is required for employer feedback", "code": "VALIDATION"},
        )

    if body.action == "unsave":
        if user.role == "candidate":
            candidate_id = auth_store.get_candidate_id(user.id)
            if candidate_id is None:
                raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
            activity_store.unsave_job(candidate_id, body.target_id)
            row = feedback_store.record_user_action(
                user_id=user.id,
                target_id=body.target_id,
                action="unsave",
                role=user.role,
                context_id=body.context_id,
            )
            return {"ok": True, "feedback": row.__dict__}

        row = feedback_store.record_user_action(
            user_id=user.id,
            target_id=body.target_id,
            action="unsave",
            role=user.role,
            context_id=body.context_id,
        )
        return {"ok": True, "feedback": row.__dict__}

    row = feedback_store.record_user_action(
        user_id=user.id,
        target_id=body.target_id,
        action=body.action,
        role=user.role,
        context_id=body.context_id,
    )

    if user.role == "candidate":
        candidate_id = auth_store.get_candidate_id(user.id)
        if candidate_id is None:
            raise HTTPException(status_code=404, detail={"error": "No profile linked", "code": "NOT_FOUND"})
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
        elif body.action == "apply":
            profile = request.app.state.container.candidate.get_by_id(candidate_id)
            if profile is None:
                raise HTTPException(status_code=404, detail={"error": "Profile not found", "code": "NOT_FOUND"})
            activity_store.apply(
                candidate_id=candidate_id,
                candidate_name=profile.name,
                job_id=job_id,
                job_title=body.target_label or job_id,
                match_score=body.match_score,
            )
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
        raise HTTPException(status_code=422, detail={"error": str(exc), "code": "VALIDATION"}) from exc
    return {"ok": True}


@router.get("/counts")
def feedback_counts(candidate_id: str, job_id: str, request: Request):
    counts = request.app.state.feedback_store.counts_for_pair(candidate_id, job_id)
    return counts.__dict__
