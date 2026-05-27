from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from bootstrap_reindex import switch_vector_store

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
    return {
        "vector_store": settings.vector_store,
        "read_only": settings.read_only,
        "read_only_note": read_only_note,
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
