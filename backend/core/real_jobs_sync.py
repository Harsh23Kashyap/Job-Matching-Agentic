"""Fetch, normalize, and snapshot external live job feeds."""

from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from config import Settings


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "remote"}
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        if "," in value:
            return [part.strip() for part in value.split(",") if part.strip()]
        value = value.strip()
        return [value] if value else []
    return []


def normalize_external_job(raw: dict, fallback_idx: int = 0) -> dict:
    raw_id = raw.get("id") or raw.get("_id") or raw.get("job_id") or f"ext_{fallback_idx}"
    title = (raw.get("title") or raw.get("job_title") or "Untitled Role").strip()
    company = (raw.get("company") or raw.get("company_name") or "Unknown Company").strip()
    link = raw.get("link") or raw.get("url") or raw.get("apply_url") or raw.get("redirect_url") or ""

    description = raw.get("description") or raw.get("job_description") or ""
    required_skills = _as_list(raw.get("required_skills") or raw.get("skills"))
    required_experience = _safe_int(
        raw.get("required_experience") or raw.get("experience_years") or raw.get("min_experience"),
        default=0,
    )
    budget = _safe_int(raw.get("budget") or raw.get("salary_min") or raw.get("stipend_min"), default=0)
    remote_policy = _to_bool(raw.get("remote_policy") or raw.get("remote"), default=False)

    return {
        "id": str(raw_id),
        "title": title,
        "company": company,
        "link": str(link),
        "description": str(description),
        "required_skills": required_skills,
        "required_experience": required_experience,
        "budget": budget,
        "remote_policy": remote_policy,
        "source": raw.get("source") or "external_api",
        "location": raw.get("location") or "",
        "job_type": raw.get("job_type") or "",
        "posted_at": raw.get("posted_at") or raw.get("created_at") or "",
        "score_hint": _safe_float(raw.get("score"), default=0.0),
    }


@dataclass
class RealJobsConfig:
    base_url: str
    jobs_path: str = "/jobs"
    limit: int = 50
    timeout_sec: int = 30
    enabled: bool = False
    output_path: str = ""

    @classmethod
    def from_settings(cls, settings: Settings) -> RealJobsConfig:
        return cls(
            base_url=settings.real_jobs_base_url.strip(),
            jobs_path=settings.real_jobs_path.strip() or "/jobs",
            limit=settings.real_jobs_page_limit,
            timeout_sec=settings.real_jobs_timeout_sec,
            enabled=settings.real_jobs_enable,
            output_path=str(settings.real_jobs_output_path_resolved),
        )


def _request_json(url: str, timeout_sec: int) -> Any:
    headers = {
        "Accept": "application/json",
        "User-Agent": "JobMatchingSync/1.0 (+https://aiforjob.ai)",
    }
    req = Request(url, headers=headers)
    ssl_context = None
    try:
        import certifi

        ssl_context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_context = ssl.create_default_context()

    with urlopen(req, timeout=timeout_sec, context=ssl_context) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw)


def _extract_jobs_and_total(payload: Any) -> tuple[list[dict], int]:
    if isinstance(payload, list):
        return payload, len(payload)

    if not isinstance(payload, dict):
        return [], 0

    for key in ("jobs", "data", "results", "items"):
        if isinstance(payload.get(key), list):
            total = _safe_int(payload.get("total"), default=len(payload[key]))
            return payload[key], total

    return [], 0


def fetch_all_jobs(config: RealJobsConfig) -> dict:
    if not config.base_url:
        raise ValueError("REAL_JOBS_BASE_URL is not configured")

    all_jobs: list[dict] = []
    limit = max(1, min(config.limit, 50))
    skip = 0
    total: int | None = None

    while True:
        query = urlencode({"limit": limit, "skip": skip})
        endpoint = urljoin(config.base_url.rstrip("/") + "/", config.jobs_path.lstrip("/"))
        url = f"{endpoint}?{query}"

        try:
            payload = _request_json(url, timeout_sec=config.timeout_sec)
        except HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.code} while fetching jobs: {url}") from exc
        except URLError as exc:
            reason = getattr(exc, "reason", None)
            raise RuntimeError(f"Network error while fetching jobs: {url} (reason={reason})") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON from jobs API: {url}") from exc

        page_jobs, page_total = _extract_jobs_and_total(payload)
        if total is None:
            total = page_total
        all_jobs.extend(page_jobs)

        if total <= 0 or (skip + limit) >= total:
            break
        if not page_jobs:
            break
        skip += limit

    normalized = [normalize_external_job(job, idx + 1) for idx, job in enumerate(all_jobs)]

    seen: set[str] = set()
    deduped: list[dict] = []
    for job in normalized:
        job_id = job["id"]
        if job_id in seen:
            continue
        seen.add(job_id)
        deduped.append(job)

    return {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "expected_refresh_utc": "02:00",
        "raw_count": len(all_jobs),
        "normalized_count": len(normalized),
        "deduped_count": len(deduped),
        "jobs": deduped,
    }


def write_snapshot(snapshot: dict, path: str) -> None:
    from pathlib import Path

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")


def load_snapshot(path: str) -> dict | None:
    from pathlib import Path

    out = Path(path)
    if not out.is_file():
        return None
    return json.loads(out.read_text(encoding="utf-8"))
