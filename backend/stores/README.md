# Stores

Persistence adapters — vector stores for semantic search, SQLite for auth-adjacent activity.

## Vector stores

| File | Backend |
|------|---------|
| `chroma_store.py` | Chroma persistent (`backend/chroma_db/`) — default |
| `qdrant_store.py` | Qdrant — switch via `POST /system/vector-store` |
| `factory.py` | `create_store(settings, collection_name)` |
| `base.py` | Shared vector store interface |

Collections: `candidates_collection`, `jobs_collection`.

## SQLite (same DB as auth, path from `Settings.sqlite_path`)

| File | Tables |
|------|--------|
| `feedback_store.py` | `user_feedback` (portal UI), `match_feedback` (research) |
| `candidate_activity_store.py` | Saved jobs, in-app applications |

Feedback actions do **not** change match rankings — UI state only.
