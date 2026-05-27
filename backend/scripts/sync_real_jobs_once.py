#!/usr/bin/env python3
"""One-shot external jobs sync + reindex (no HTTP server required)."""

from bootstrap import create_system
from config import Settings


def main() -> None:
    settings = Settings()
    if not settings.real_jobs_enable:
        raise RuntimeError("REAL_JOBS_ENABLE is false. Set REAL_JOBS_ENABLE=true to run sync.")
    if not settings.real_jobs_base_url.strip():
        raise RuntimeError("REAL_JOBS_BASE_URL is missing.")

    container = create_system(settings)
    result = container.real_jobs.sync(reindex=True)
    print(
        f"[real-jobs-sync] jobs={result.job_count} "
        f"deduped={result.deduped_count} fetched_at={result.fetched_at_utc}"
    )


if __name__ == "__main__":
    main()
