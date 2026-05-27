"""SQLite store for match interaction feedback."""
from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

USER_FEEDBACK_ACTIONS = frozenset(
    {"save", "not_interested", "apply", "reject", "contact", "dismiss"}
)
MATCH_FEEDBACK_ACTIONS = frozenset({"save", "dismiss", "apply"})


@dataclass
class FeedbackCounts:
    save_count: int = 0
    dismiss_count: int = 0
    apply_count: int = 0


@dataclass
class UserFeedbackRow:
    id: str
    user_id: str
    target_id: str
    action: str
    context_id: str | None
    role: str
    created_at: str


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

                CREATE TABLE IF NOT EXISTS user_feedback (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    context_id TEXT,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_user_feedback_user
                    ON user_feedback(user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_user_feedback_target
                    ON user_feedback(user_id, target_id, context_id);
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
        if action not in MATCH_FEEDBACK_ACTIONS:
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

    def record_user_action(
        self,
        *,
        user_id: str,
        target_id: str,
        action: str,
        role: str,
        context_id: str | None = None,
    ) -> UserFeedbackRow:
        if action not in USER_FEEDBACK_ACTIONS:
            raise ValueError(f"Invalid action: {action}")
        row_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_feedback (id, user_id, target_id, action, context_id, role, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (row_id, user_id, target_id, action, context_id, role, created_at),
            )
        return UserFeedbackRow(
            id=row_id,
            user_id=user_id,
            target_id=target_id,
            action=action,
            context_id=context_id,
            role=role,
            created_at=created_at,
        )

    def list_latest_for_user(
        self,
        user_id: str,
        *,
        context_id: str | None = None,
    ) -> list[UserFeedbackRow]:
        query = """
            SELECT id, user_id, target_id, action, context_id, role, created_at
            FROM user_feedback
            WHERE user_id = ?
        """
        params: list[str] = [user_id]
        if context_id is not None:
            query += " AND context_id = ?"
            params.append(context_id)
        query += " ORDER BY created_at DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        latest: dict[tuple[str, str | None], UserFeedbackRow] = {}
        for row in rows:
            key = (row["target_id"], row["context_id"])
            if key in latest:
                continue
            latest[key] = UserFeedbackRow(
                id=row["id"],
                user_id=row["user_id"],
                target_id=row["target_id"],
                action=row["action"],
                context_id=row["context_id"],
                role=row["role"],
                created_at=row["created_at"],
            )
        return list(latest.values())

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
