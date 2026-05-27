import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from auth.passwords import hash_password, verify_password

VALID_ROLES = frozenset({"candidate", "employer", "admin"})


@dataclass
class User:
    id: str
    email: str
    role: str
    created_at: str


class UserStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('candidate', 'employer', 'admin')),
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS candidate_ownership (
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    candidate_id TEXT NOT NULL,
                    PRIMARY KEY (user_id)
                );

                CREATE TABLE IF NOT EXISTS job_ownership (
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    job_id TEXT NOT NULL,
                    PRIMARY KEY (job_id)
                );
                """
            )

    def create_user(self, email: str, password: str, role: str) -> User:
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        normalized = email.strip().lower()
        user_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO users (id, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, normalized, hash_password(password), role, created_at),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateEmailError(normalized) from exc
        return User(id=user_id, email=normalized, role=role, created_at=created_at)

    def authenticate(self, email: str, password: str) -> User | None:
        normalized = email.strip().lower()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, email, password_hash, role, created_at FROM users WHERE email = ?",
                (normalized,),
            ).fetchone()
        if row is None or not verify_password(password, row["password_hash"]):
            return None
        return User(
            id=row["id"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"],
        )

    def get_by_id(self, user_id: str) -> User | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, email, role, created_at FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
        if row is None:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"],
        )

    def get_by_email(self, email: str) -> User | None:
        normalized = email.strip().lower()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, email, role, created_at FROM users WHERE email = ?",
                (normalized,),
            ).fetchone()
        if row is None:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"],
        )

    def link_candidate(self, user_id: str, candidate_id: str) -> None:
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT candidate_id FROM candidate_ownership WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if existing is not None:
                if existing["candidate_id"] == candidate_id:
                    return
                conn.execute(
                    "UPDATE candidate_ownership SET candidate_id = ? WHERE user_id = ?",
                    (candidate_id, user_id),
                )
                return
            conn.execute(
                "INSERT INTO candidate_ownership (user_id, candidate_id) VALUES (?, ?)",
                (user_id, candidate_id),
            )

    def get_candidate_id(self, user_id: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT candidate_id FROM candidate_ownership WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        return row["candidate_id"] if row else None

    def clear_candidate_link(self, user_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM candidate_ownership WHERE user_id = ?",
                (user_id,),
            )

    def link_job(self, user_id: str, job_id: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO job_ownership (user_id, job_id) VALUES (?, ?)",
                (user_id, job_id),
            )

    def link_job_if_unowned(self, user_id: str, job_id: str) -> bool:
        """Link job to user when no owner exists. Returns True if linked."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT user_id FROM job_ownership WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if row is not None:
                return row["user_id"] == user_id
            conn.execute(
                "INSERT INTO job_ownership (user_id, job_id) VALUES (?, ?)",
                (user_id, job_id),
            )
            return True

    def list_job_ids(self, user_id: str) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT job_id FROM job_ownership WHERE user_id = ? ORDER BY job_id",
                (user_id,),
            ).fetchall()
        return [row["job_id"] for row in rows]


class DuplicateEmailError(Exception):
    pass


class ProfileAlreadyLinkedError(Exception):
    def __init__(self, profile_type: str) -> None:
        self.profile_type = profile_type
        super().__init__(f"{profile_type} profile already linked")
