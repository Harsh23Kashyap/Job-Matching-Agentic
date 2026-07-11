"""External live jobs API contract, ported from Agentic-Job-Matching HANDOFF.md.

See the six contracts: upstream provider API, field mapping, snapshot schema,
environment variables, backend proxy (`GET/POST /real-jobs/*`), and downstream
ingestion into the Employer Agent vector store.

Implementation:
- `backend/core/real_jobs_sync.py`, fetch, normalize, snapshot
- `backend/services/real_jobs_service.py`, sync orchestration + boot
- `backend/gateway/routes/real_jobs.py`, HTTP proxy
- `backend/scripts/sync_real_jobs_once.py`, CLI sync

Configure via `REAL_JOBS_*` env vars in `backend/.env.example`.
Provider URL (`REAL_JOBS_BASE_URL`) is deployment-specific and not committed.
"""
