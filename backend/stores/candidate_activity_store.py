"""SQLite store for saved jobs and job applications."""
from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class SavedJob:
    id: str
    candidate_id: str
    job_id: str
    job_title: str
    created_at: str


@dataclass
class JobApplication:
    id: str
    candidate_id: str
    candidate_name: str
    job_id: str
    job_title: str
    match_score: float | None
    status: str
    created_at: str


class CandidateActivityStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS saved_jobs (
                    id TEXT PRIMARY KEY,
                    candidate_id TEXT NOT NULL,
                    job_id TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(candidate_id, job_id)
                );
                CREATE INDEX IF NOT EXISTS idx_saved_jobs_candidate
                    ON saved_jobs(candidate_id);

                CREATE TABLE IF NOT EXISTS job_applications (
                    id TEXT PRIMARY KEY,
                    candidate_id TEXT NOT NULL,
                    candidate_name TEXT NOT NULL,
                    job_id TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    match_score REAL,
                    status TEXT NOT NULL DEFAULT 'applied',
                    created_at TEXT NOT NULL,
                    UNIQUE(candidate_id, job_id)
                );
                CREATE INDEX IF NOT EXISTS idx_applications_job
                    ON job_applications(job_id);
                CREATE INDEX IF NOT EXISTS idx_applications_candidate
                    ON job_applications(candidate_id);
                """
            )

    def list_saved_jobs(self, candidate_id: str) -> list[SavedJob]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, candidate_id, job_id, job_title, created_at FROM saved_jobs WHERE candidate_id = ? ORDER BY created_at DESC",
                (candidate_id,),
            ).fetchall()
        return [SavedJob(**dict(row)) for row in rows]

    def save_job(self, candidate_id: str, job_id: str, job_title: str) -> SavedJob:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id, candidate_id, job_id, job_title, created_at FROM saved_jobs WHERE candidate_id = ? AND job_id = ?",
                (candidate_id, job_id),
            ).fetchone()
            if existing:
                return SavedJob(**dict(existing))
            row_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO saved_jobs (id, candidate_id, job_id, job_title, created_at) VALUES (?, ?, ?, ?, ?)",
                (row_id, candidate_id, job_id, job_title, now),
            )
        return SavedJob(id=row_id, candidate_id=candidate_id, job_id=job_id, job_title=job_title, created_at=now)

    def unsave_job(self, candidate_id: str, job_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM saved_jobs WHERE candidate_id = ? AND job_id = ?",
                (candidate_id, job_id),
            )
        return cur.rowcount > 0

    def is_saved(self, candidate_id: str, job_id: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM saved_jobs WHERE candidate_id = ? AND job_id = ?",
                (candidate_id, job_id),
            ).fetchone()
        return row is not None

    def apply(
        self,
        *,
        candidate_id: str,
        candidate_name: str,
        job_id: str,
        job_title: str,
        match_score: float | None = None,
    ) -> JobApplication:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id, candidate_id, candidate_name, job_id, job_title, match_score, status, created_at FROM job_applications WHERE candidate_id = ? AND job_id = ?",
                (candidate_id, job_id),
            ).fetchone()
            if existing:
                return JobApplication(**dict(existing))
            row_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO job_applications (id, candidate_id, candidate_name, job_id, job_title, match_score, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'applied', ?)",
                (row_id, candidate_id, candidate_name, job_id, job_title, match_score, now),
            )
        return JobApplication(
            id=row_id,
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            job_id=job_id,
            job_title=job_title,
            match_score=match_score,
            status="applied",
            created_at=now,
        )

    def list_applications_for_candidate(self, candidate_id: str) -> list[JobApplication]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, candidate_id, candidate_name, job_id, job_title, match_score, status, created_at FROM job_applications WHERE candidate_id = ? ORDER BY created_at DESC",
                (candidate_id,),
            ).fetchall()
        return [JobApplication(**dict(row)) for row in rows]

    def list_applications_for_jobs(self, job_ids: list[str]) -> list[JobApplication]:
        if not job_ids:
            return []
        placeholders = ",".join("?" * len(job_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT id, candidate_id, candidate_name, job_id, job_title, match_score, status, created_at FROM job_applications WHERE job_id IN ({placeholders}) ORDER BY created_at DESC",
                job_ids,
            ).fetchall()
        return [JobApplication(**dict(row)) for row in rows]
