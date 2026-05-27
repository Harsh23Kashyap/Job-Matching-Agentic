from fastapi import APIRouter, Request

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/config")
def get_system_config(request: Request):
    settings = request.app.state.container.settings
    return {
        "vector_store": "chroma",
        "embedding_model": settings.embedding_model,
        "strategies": ["semantic", "multimodal"],
        "metrics": ["cosine", "euclidean"],
        "skills_modes": ["jaccard", "embedding"],
        "rrf_k": settings.rrf_k,
    }
