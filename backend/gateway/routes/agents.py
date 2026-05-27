from fastapi import APIRouter, Request

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/status")
def get_agent_status(request: Request):
    container = request.app.state.container
    return {
        "candidates": container.candidate.status().model_dump(),
        "employer": container.employer.status().model_dump(),
        "matchmaking": container.matchmaker.status().model_dump(),
    }
