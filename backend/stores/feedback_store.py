"""SQLite store for match interaction feedback."""
from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class FeedbackCounts:
    save_count: int = 0
    dismiss_count: int = 0
    apply_count: int = 0


class FeedbackStore:
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
                CREATE TABLE IF NOT EXISTS match_feedback (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    candidate_id TEXT NOT NULL,
                    job_id TEXT NOT NULL,
                    action TEXT NOT NULL CHECK (action IN ('save', 'dismiss', 'apply')),
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_feedback_pair
                    ON match_feedback(candidate_id, job_id);
                """
            )

    def record(
        self,
        *,
        candidate_id: str,
        job_id: str,
        action: str,
        user_id: str | None = None,
    ) -> None:
        if action not in {"save", "dismiss", "apply"}:
            raise ValueError(f"Invalid action: {action}")
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO match_feedback (id, user_id, candidate_id, job_id, action, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    user_id,
                    candidate_id,
                    job_id,
                    action,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

    def counts_for_pair(self, candidate_id: str, job_id: str) -> FeedbackCounts:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT action, COUNT(*) AS c FROM match_feedback WHERE candidate_id = ? AND job_id = ? GROUP BY action",
                (candidate_id, job_id),
            ).fetchall()
        out = FeedbackCounts()
        for row in rows:
            if row["action"] == "save":
                out.save_count = int(row["c"])
            elif row["action"] == "dismiss":
                out.dismiss_count = int(row["c"])
            elif row["action"] == "apply":
                out.apply_count = int(row["c"])
        return out
