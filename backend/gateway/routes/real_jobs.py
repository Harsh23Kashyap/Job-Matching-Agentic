from fastapi import APIRouter, Request

from contracts.real_jobs import RealJobsSyncRequest

router = APIRouter(prefix="/real-jobs", tags=["real-jobs"])


@router.get("/status")
def get_real_jobs_status(request: Request):
    return request.app.state.container.real_jobs.status_payload()


@router.post("/sync")
def sync_real_jobs(body: RealJobsSyncRequest, request: Request):
    response = request.app.state.container.real_jobs.sync(reindex=body.reindex)
    return response.model_dump()
