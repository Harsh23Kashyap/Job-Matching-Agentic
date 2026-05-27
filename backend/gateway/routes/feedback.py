from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from auth.deps import get_optional_user

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackRequest(BaseModel):
    candidate_id: str
    job_id: str
    action: str = Field(pattern="^(save|dismiss|apply)$")


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
