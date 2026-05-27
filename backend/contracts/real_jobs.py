from pydantic import BaseModel, Field


class RealJobsSyncRequest(BaseModel):
    reindex: bool = True


class RealJobsState(BaseModel):
    enabled: bool = False
    source: str = "local_seed"
    last_sync: str | None = None
    last_error: str | None = None
    job_count: int = 0


class RealJobsStatusResponse(BaseModel):
    enabled: bool
    base_url_configured: bool
    jobs_path: str
    page_limit: int
    snapshot_path: str
    state: RealJobsState


class RealJobsSyncResponse(BaseModel):
    message: str
    job_count: int
    raw_count: int
    deduped_count: int
    fetched_at_utc: str
    expected_refresh_utc: str
    reindexed: bool
