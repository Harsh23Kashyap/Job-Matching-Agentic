from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from auth.deps import require_role
from auth.store import User
from bootstrap_reindex import switch_vector_store
from demo_reset import demo_snapshot, reset_demo_data

router = APIRouter(prefix="/system", tags=["system"])


class VectorStoreRequest(BaseModel):
    vector_store: Literal["chroma", "qdrant"]


@router.get("/config")
def get_system_config(request: Request):
    settings = request.app.state.container.settings
    read_only_note = (
        "Read-only demo mode is active: POST, PUT, PATCH, and DELETE are blocked "
        "except /auth/login and /auth/register."
        if settings.read_only
        else "Mutating requests are allowed."
    )
    demo_accounts = getattr(request.app.state, "demo_accounts", None)
    demo_snapshot_data = None
    if settings.demo_mode and demo_accounts:
        demo_snapshot_data = demo_snapshot(request.app.state.container, request.app.state.auth_store)
    return {
        "vector_store": settings.vector_store,
        "read_only": settings.read_only,
        "read_only_note": read_only_note,
        "demo_mode": settings.demo_mode,
        "seed_demo": settings.seed_demo,
        "demo_accounts": demo_accounts,
        "demo_snapshot": demo_snapshot_data,
        "embedding_model": settings.embedding_model,
        "strategies": ["semantic", "multimodal"],
        "metrics": ["cosine", "euclidean"],
        "skills_modes": ["jaccard", "embedding"],
        "rrf_k": settings.rrf_k,
        "cross_encoder_available": True,
        "enable_cross_encoder_rerank": settings.enable_cross_encoder_rerank,
        "cross_encoder_rerank_pool": settings.cross_encoder_rerank_pool,
        "fusion_modes": ["fixed", "learned", "hierarchical"],
        "fusion_model_loaded": request.app.state.container.matchmaker.fusion_model is not None,
        "calibration_model_loaded": request.app.state.container.matchmaker.calibrator is not None,
        "ml_features": {
            "apply_constraints": True,
            "auto_strategy": True,
            "use_calibration": request.app.state.container.matchmaker.calibrator is not None,
            "use_feedback_boost": True,
            "explain_modes": ["rules", "llm"],
        },
    }


@router.post("/vector-store")
def set_vector_store(body: VectorStoreRequest, request: Request):
    if request.app.state.container.settings.read_only:
        raise HTTPException(
            status_code=403,
            detail={"error": "Read-only mode · vector store switch disabled", "code": "READ_ONLY"},
        )
    try:
        result = switch_vector_store(request.app.state.container, body.vector_store)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"error": str(exc), "code": "VALIDATION"}) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail={"error": str(exc), "code": "UNAVAILABLE"}) from exc
    return result


@router.post("/demo/reset")
def reset_demo(
    request: Request,
    _admin: User = Depends(require_role("admin")),
):
    settings = request.app.state.container.settings
    if not settings.demo_mode:
        raise HTTPException(
            status_code=403,
            detail={"error": "Demo mode is disabled on this server.", "code": "DEMO_MODE_OFF"},
        )
    if settings.read_only:
        raise HTTPException(
            status_code=403,
            detail={"error": "Cannot reset demo data while read-only mode is active.", "code": "READ_ONLY"},
        )
    result = reset_demo_data(request.app.state.container, request.app.state.auth_store)
    request.app.state.demo_accounts = {
        "candidate_email": result["candidate_email"],
        "employer_email": result["employer_email"],
        "admin_email": result["admin_email"],
        "password": result["password"],
        "summary": result.get("summary", "demo data reset"),
    }
    return result


@router.get("/fairness")
def get_fairness_report(request: Request):
    from benchmarks.fairness_eval import run_fairness_eval

    container = request.app.state.container
    report = run_fairness_eval(
        container.settings,
        fusion_model=container.matchmaker.fusion_model,
        calibrator=container.matchmaker.calibrator,
    )
    return report
