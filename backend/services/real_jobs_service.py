from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from contracts.real_jobs import RealJobsState, RealJobsSyncResponse
from core.real_jobs_sync import (
    RealJobsConfig,
    fetch_all_jobs,
    load_snapshot,
    write_snapshot,
)

if TYPE_CHECKING:
    from bootstrap import SystemContainer


@dataclass
class RealJobsService:
    container: SystemContainer
    state: RealJobsState = field(default_factory=RealJobsState)

    def __post_init__(self) -> None:
        config = self._config()
        self.state.enabled = config.enabled

    def _config(self) -> RealJobsConfig:
        return RealJobsConfig.from_settings(self.container.settings)

    def _set_state(self, source: str, job_count: int, last_sync: str | None = None) -> None:
        self.state.source = source
        self.state.job_count = job_count
        if last_sync is not None:
            self.state.last_sync = last_sync

    def boot_from_snapshot_if_available(self) -> bool:
        config = self._config()
        snapshot = load_snapshot(config.output_path)
        if not snapshot:
            return False
        snapshot_jobs = snapshot.get("jobs") or []
        if not snapshot_jobs:
            return False
        self.container.employer.replace_corpus(snapshot_jobs)
        self._set_state(
            source="snapshot",
            job_count=len(snapshot_jobs),
            last_sync=snapshot.get("fetched_at_utc"),
        )
        return True

    def reindex_all(self) -> None:
        settings = self.container.settings
        self.container.candidate.rebootstrap_from_file(settings.cvs_path)
        jobs = [p.model_dump() for p in self.container.employer.list_jobs()]
        if jobs:
            self.container.employer.replace_corpus(jobs)

    def status_payload(self) -> dict:
        config = self._config()
        page_limit = max(1, min(config.limit, 50))
        return {
            "enabled": config.enabled,
            "base_url_configured": bool(config.base_url),
            "jobs_path": config.jobs_path,
            "page_limit": page_limit,
            "snapshot_path": config.output_path,
            "state": self.state.model_dump(),
        }

    def sync(self, reindex: bool = True) -> RealJobsSyncResponse:
        config = self._config()
        if not config.enabled:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=400,
                detail="Real jobs sync is disabled. Set REAL_JOBS_ENABLE=true and REAL_JOBS_BASE_URL.",
            )
        try:
            snapshot = fetch_all_jobs(config)
            write_snapshot(snapshot, config.output_path)
            synced_jobs = snapshot.get("jobs", [])
            if not synced_jobs:
                raise RuntimeError("No jobs returned from external API")
            self.container.employer.replace_corpus(synced_jobs)
            self._set_state(
                source="external_api",
                job_count=len(synced_jobs),
                last_sync=snapshot.get("fetched_at_utc"),
            )
            self.state.last_error = None
            if reindex:
                self.reindex_all()
            return RealJobsSyncResponse(
                message="Real jobs synced successfully",
                job_count=len(synced_jobs),
                raw_count=int(snapshot.get("raw_count", 0)),
                deduped_count=int(snapshot.get("deduped_count", len(synced_jobs))),
                fetched_at_utc=str(snapshot.get("fetched_at_utc", "")),
                expected_refresh_utc=str(snapshot.get("expected_refresh_utc", "02:00")),
                reindexed=reindex,
            )
        except Exception as exc:
            from fastapi import HTTPException

            if isinstance(exc, HTTPException):
                raise
            self.state.last_error = str(exc)
            raise HTTPException(status_code=502, detail=f"Real jobs sync failed: {exc}") from exc
