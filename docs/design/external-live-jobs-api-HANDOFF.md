# Handoff — External Live Jobs API Contract
> Written: 2026-05-27 | Branch: main | Dir: `/Users/harshkashyap/Projects/JobMatcher-v1/Agentic-Job-Matching`

## Goal

Document the **complete contract** for the external live jobs feed used by Agentic Job Matching, so a **new application** can implement the same upstream integration (fetch, paginate, normalize, snapshot, ingest) without re-reading the legacy codebase. This handoff covers: upstream provider API, field mapping, pagination rules, snapshot format, env configuration, and how the current FastAPI service exposes sync/status to clients.

---

## Current state

- **Done:** External jobs sync fully implemented in `backend/real_jobs_sync.py`; wired into `backend/app.py` (`/real-jobs/*`), frontend sync button, daily agent pre-sync, and CLI `backend/scripts/sync_real_jobs_once.py`.
- **In progress:** None for this API — documentation handoff only.
- **Blocked:** No committed `data/jobs_live.json` sample (gitignored). `REAL_JOBS_BASE_URL` is not checked into the repo — must be supplied per deployment.

---

## Architecture overview

```
┌─────────────────────┐     GET ?limit&skip      ┌──────────────────────────┐
│ External Jobs API   │ ◄─────────────────────── │ real_jobs_sync.py        │
│ (provider)          │     JSON paginated       │ fetch_all_jobs()         │
└─────────────────────┘                          └───────────┬──────────────┘
                                                               │ normalize + dedupe
                                                               ▼
                                                   ┌──────────────────────────┐
                                                   │ data/jobs_live.json      │
                                                   │ (snapshot on disk)       │
                                                   └───────────┬──────────────┘
                                                               │ load on startup / after sync
                                                               ▼
┌─────────────────────┐     POST /real-jobs/sync ┌──────────────────────────┐
│ Frontend / new app  │ ───────────────────────► │ backend/app.py           │
│                     │     GET /real-jobs/status│ in-memory jobs[] + ANN   │
└─────────────────────┘                          └──────────────────────────┘
```

**Default corpus when sync is disabled:** `data/jobs.json` (15 static jobs). Live sync **replaces** in-memory jobs entirely — resumes stay on `data/cvs.json`.

---

## Contract 1 — Upstream external provider API

This is what **your new application must call** (or what your new backend must expose if you become the provider).

### Request

| Property | Value |
|----------|-------|
| **Method** | `GET` |
| **URL pattern** | `{REAL_JOBS_BASE_URL}{REAL_JOBS_PATH}?limit={limit}&skip={skip}` |
| **Default path** | `/jobs` |
| **Default base** | Set via env — **not hardcoded in repo** |
| **Example** | `https://api.example.com/jobs?limit=50&skip=0` |

**URL construction** (from `fetch_all_jobs`):

```python
endpoint = urljoin(base_url.rstrip("/") + "/", jobs_path.lstrip("/"))
url = f"{endpoint}?limit={limit}&skip={skip}"
```

### Request headers (required by current client)

| Header | Value |
|--------|-------|
| `Accept` | `application/json` |
| `User-Agent` | `JobMatchingSync/1.0 (+https://aiforjob.ai)` |

No auth headers are implemented in the current client. If the provider requires API keys, the new app must add them (not present in legacy code).

### Query parameters

| Param | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| `limit` | int | Clamped to **1–50** client-side (`max(1, min(config.limit, 50))`) | Page size |
| `skip` | int | Starts at 0, increments by `limit` each page | Offset pagination |

### Pagination termination rules

Client stops fetching when **any** of:

1. `total <= 0`
2. `skip + limit >= total` (primary contract — comment in code: *"Contract from provider: stop when skip+limit >= total"*)
3. Current page returns **zero jobs**

First response sets `total` from payload; if absent, defaults to `len(current_page_jobs)`.

### Response envelope — accepted shapes

The client accepts **either** a bare array **or** a JSON object. Job list is extracted by `_extract_jobs_and_total`:

**Shape A — bare array**

```json
[
  { "id": "abc123", "title": "ML Engineer", ... },
  { "id": "def456", "title": "Backend Engineer", ... }
]
```

- `total` = `len(array)` (no further pages unless array length equals limit and you implement provider-specific logic — current code treats total as array length, so **single page only** for bare arrays).

**Shape B — paginated object (preferred)**

```json
{
  "total": 237,
  "jobs": [ ... ]
}
```

Also accepts list keys (first match wins): `jobs`, `data`, `results`, `items`.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `total` | int | Recommended | Total job count across all pages; used for pagination stop |
| `jobs` / `data` / `results` / `items` | array | Required (one of) | Page of raw job objects |

**Example paginated response:**

```json
{
  "total": 120,
  "jobs": [
    {
      "id": "64f1a2b3c4d5e6f7a8b9c0d1",
      "title": "Machine Learning Engineer",
      "company": "Acme Corp",
      "description": "Build ML pipelines...",
      "required_skills": ["Python", "TensorFlow"],
      "required_experience": 2,
      "budget": 130000,
      "remote_policy": true,
      "location": "Remote",
      "link": "https://example.com/apply/123",
      "posted_at": "2026-05-15T10:00:00Z",
      "source": "aiforjob"
    }
  ]
}
```

### Upstream HTTP error handling (current client)

| Condition | Behavior |
|-----------|----------|
| HTTP 4xx/5xx | `RuntimeError: HTTP {code} while fetching jobs: {url}` |
| Network / DNS / timeout | `RuntimeError: Network error while fetching jobs: {url}` |
| Invalid JSON body | `RuntimeError: Invalid JSON from jobs API: {url}` |
| Empty job list after all pages | Sync fails: `RuntimeError: No jobs returned from external API` |
| Missing `REAL_JOBS_BASE_URL` | `ValueError: REAL_JOBS_BASE_URL is not configured` |

Timeout: `REAL_JOBS_TIMEOUT_SEC` (default **30** seconds per request).

---

## Contract 2 — Raw job field mapping (provider → canonical)

Each raw job object is passed through `normalize_external_job()`. Your new app should implement the same mapping for compatibility with existing snapshots and ingestion.

### ID

| Raw fields tried (first non-empty) | Fallback |
|-----------------------------------|----------|
| `id`, `_id`, `job_id` | `ext_{index}` (1-based page index) |

Output: `id` as **string**.

### Core fields

| Canonical field | Raw aliases | Default if missing |
|-----------------|-------------|-------------------|
| `title` | `title`, `job_title` | `"Untitled Role"` |
| `company` | `company`, `company_name` | `"Unknown Company"` |
| `link` | `link`, `url`, `apply_url`, `redirect_url` | `""` |
| `description` | `description`, `job_description` | `""` |
| `required_skills` | `required_skills`, `skills` | `[]` |
| `required_experience` | `required_experience`, `experience_years`, `min_experience` | `0` |
| `budget` | `budget`, `salary_min`, `stipend_min` | `0` |
| `remote_policy` | `remote_policy`, `remote` | `false` |
| `location` | `location` | `""` |
| `job_type` | `job_type` | `""` |
| `posted_at` | `posted_at`, `created_at` | `""` |
| `source` | `source` | `"external_api"` |
| `score_hint` | `score` (float) | `0.0` |

### Skills list coercion (`_as_list`)

| Input type | Behavior |
|------------|----------|
| `null` / missing | `[]` |
| `array` | stringified, trimmed, empty strings dropped |
| `string` with commas | split on `,`, trim each part |
| plain `string` | single-element list if non-empty |

### Boolean coercion for `remote_policy` (`_to_bool`)

Truthy strings: `1`, `true`, `yes`, `y`, **`remote`** (note: `"remote"` alone → true).

### Numeric coercion

Non-parseable ints/floats → default (`0` / `0.0`).

### Canonical job object (after normalization)

```json
{
  "id": "64f1a2b3c4d5e6f7a8b9c0d1",
  "title": "Machine Learning Engineer",
  "company": "Acme Corp",
  "link": "https://example.com/apply/123",
  "description": "Build ML pipelines with Python and TensorFlow.",
  "required_skills": ["Python", "TensorFlow", "Machine Learning"],
  "required_experience": 2,
  "budget": 130000,
  "remote_policy": true,
  "source": "external_api",
  "location": "Remote",
  "job_type": "full-time",
  "posted_at": "2026-05-15T10:00:00Z",
  "score_hint": 0.0
}
```

### Deduplication

After normalization, jobs are deduped by **`id`**, preserving **first-seen order** (latest page order from provider).

---

## Contract 3 — Snapshot file (`jobs_live.json`)

Written after every successful fetch. Default path: `data/jobs_live.json` (`REAL_JOBS_OUTPUT_PATH`).

### Snapshot schema

```json
{
  "fetched_at_utc": "2026-05-27T14:30:00.123456+00:00",
  "expected_refresh_utc": "02:00",
  "raw_count": 125,
  "normalized_count": 125,
  "deduped_count": 120,
  "jobs": [ /* array of canonical job objects */ ]
}
```

| Field | Meaning |
|-------|---------|
| `fetched_at_utc` | ISO8601 UTC timestamp when fetch completed |
| `expected_refresh_utc` | Hardcoded `"02:00"` — provider hint, not enforced |
| `raw_count` | Jobs collected before dedupe |
| `normalized_count` | Same as raw_count (normalize is 1:1) |
| `deduped_count` | Unique jobs after ID dedupe |
| `jobs` | Canonical job array used by matching pipeline |

### Startup behavior

On `app.py` import:

1. Load `data/cvs.json` + `data/jobs.json` (default jobs).
2. If `jobs_live.json` exists and has non-empty `jobs[]`, **replace** in-memory jobs with snapshot jobs; set `real_jobs_state.source = "snapshot"`.

---

## Contract 4 — Environment variables

| Variable | Default | Required for live sync | Effect |
|----------|---------|------------------------|--------|
| `REAL_JOBS_ENABLE` | `false` | Yes (`true`) | Gate for sync endpoints and agent pre-sync |
| `REAL_JOBS_BASE_URL` | `""` | Yes | Provider base URL (no trailing slash required) |
| `REAL_JOBS_PATH` | `/jobs` | No | List endpoint path |
| `REAL_JOBS_PAGE_LIMIT` | `50` | No | Page size (clamped to 50 max) |
| `REAL_JOBS_TIMEOUT_SEC` | `30` | No | Per-request timeout (seconds) |
| `REAL_JOBS_OUTPUT_PATH` | `data/jobs_live.json` | No | Snapshot write path |

**Truthy values for `REAL_JOBS_ENABLE`:** `1`, `true`, `yes`, `y`, `on` (case-insensitive).

**Example `.env` for new deployment:**

```bash
REAL_JOBS_ENABLE=true
REAL_JOBS_BASE_URL=https://your-provider.example.com
REAL_JOBS_PATH=/jobs
REAL_JOBS_PAGE_LIMIT=50
REAL_JOBS_TIMEOUT_SEC=30
REAL_JOBS_OUTPUT_PATH=data/jobs_live.json
```

---

## Contract 5 — Current backend proxy API (wraps upstream)

If the new app talks to **this** FastAPI service instead of the provider directly:

### `GET /real-jobs/status`

**Response 200:**

```json
{
  "enabled": true,
  "base_url_configured": true,
  "jobs_path": "/jobs",
  "page_limit": 50,
  "snapshot_path": "/abs/path/to/data/jobs_live.json",
  "state": {
    "enabled": true,
    "source": "external_api",
    "last_sync": "2026-05-27T14:30:00.123456+00:00",
    "last_error": null,
    "job_count": 120
  }
}
```

**`state.source` values:** `"local_seed"` | `"snapshot"` | `"external_api"`

### `POST /real-jobs/sync`

**Request:**

```json
{
  "reindex": true
}
```

| Field | Type | Default | Effect |
|-------|------|---------|--------|
| `reindex` | bool | `true` | Re-embed all jobs + resumes into active vector store after sync |

**Response 200 (success):**

```json
{
  "message": "Real jobs synced successfully",
  "job_count": 120,
  "raw_count": 125,
  "deduped_count": 120,
  "fetched_at_utc": "2026-05-27T14:30:00.123456+00:00",
  "expected_refresh_utc": "02:00",
  "reindexed": true
}
```

**Response 400 (disabled):**

```json
{
  "detail": "Real jobs sync is disabled. Set REAL_JOBS_ENABLE=true and REAL_JOBS_BASE_URL."
}
```

**Response 502 (fetch/normalize failure):**

```json
{
  "detail": "Real jobs sync failed: {error message}"
}
```

### Post-sync job catalog (for UI)

After sync, clients typically refresh:

- `GET /jobs` — title strings only
- `GET /jobs/full` — full canonical job objects (includes `company`, `link`, `location`, etc.)

### Daily agent integration

`POST /agent/run-daily-recommendations` with `"sync_before_run": true` (default) calls `_sync_real_jobs(reindex=True)` **only if** `REAL_JOBS_ENABLE=true`.

---

## Contract 6 — Ingestion & matching (downstream of sync)

After jobs land in memory, `ingestion.ingest_data()`:

1. Builds embedding text via `job_document_text(job)` (includes title, company, skills, description, etc.).
2. Upserts to vector store with metadata:

| Metadata key | Source field |
|--------------|--------------|
| `id` | `job.id` |
| `title` | `job.title` |
| `company` | `job.company` |
| `link` | `job.link` |
| `budget` | `job.budget` |
| `remote_policy` | `job.remote_policy` |
| `required_experience` | `job.required_experience` |
| `required_skills` | comma-joined string (Chroma constraint) |
| `location` | `job.location` |
| `job_type` | `job.job_type` |
| `posted_at` | `job.posted_at` |
| `source` | `job.source` |

**Pydantic `Job` schema** (`schemas.py`) validates only: `id`, `title`, `required_skills`, `required_experience`, `budget`, `remote_policy`, `description`. Extended fields (`company`, `link`, …) are **not** in the strict schema but are preserved in dicts from live sync and used in ingestion/daily recommendations.

Daily recommendation results expose per job:

```json
{
  "job_id": "...",
  "job_title": "...",
  "company": "...",
  "apply_link": "...",
  "location": "...",
  "posted_at": "...",
  "source": "...",
  "similarity": 0.85,
  "why_ranked": ["Matching skills: python, ..."]
}
```

Note: API field is `apply_link` in daily output but canonical job uses `link`.

---

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Offset pagination (`limit`/`skip`) | Matches provider contract comment in code | Cursor-based (not implemented) |
| Max page size 50 | Hard cap in client regardless of env | Larger pages (provider may not support) |
| Snapshot to disk | Survive restarts; boot from last good fetch | In-memory only (lost on restart) |
| Replace entire job corpus on sync | Live feed is source of truth | Merge with static `jobs.json` (not done) |
| Field alias mapping in normalize | Tolerate heterogeneous provider schemas | Strict schema validation at fetch (too brittle) |
| No auth in fetch client | Provider was open at build time | API key header (add in new app if needed) |
| Dedupe by `id` only | Prevent duplicate ANN points | Dedupe by title+company (not implemented) |

---

## Open questions

- [ ] **Unknown:** Exact production `REAL_JOBS_BASE_URL` — not in repo; confirm with deployment/env owner.
- [ ] **Unknown:** Whether provider requires auth (Bearer/API key) — legacy client sends none.
- [ ] **Hypothesis:** Provider is `aiforjob.ai` (User-Agent references it) — verify URL and OpenAPI if migrating.
- [ ] **Hunch:** Bare-array responses only return one page — if provider uses arrays without `total`, pagination may be incomplete.

---

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Production `REAL_JOBS_BASE_URL` | Deployment env / team | Not in repo |
| Provider API documentation | External team | Not in repo — this handoff derives contract from client code |
| Sample `jobs_live.json` | Runtime artifact | Gitignored — generate via sync |

---

## Environment

- **Branch:** `main`
- **Uncommitted changes:** JAAMAS manuscript/portal edits (unrelated to jobs API)
- **Recent commits:** 2026-05-17 submission polish
- **Build status:** Not run this session
- **Test status:** `test_real_jobs_sync_disabled` expects 400 when sync disabled; no live integration test in CI
- **Active processes:** None

---

## What worked

- Paginated fetch with `limit`/`skip` + `total` field
- Flexible response envelope (`jobs`/`data`/`results`/`items`/bare array)
- Normalization layer decouples provider schema from matching pipeline
- Snapshot boot on startup avoids empty state after restart
- Frontend sync → refresh `/jobs/full` pattern

---

## What didn't work

- Calling sync with `REAL_JOBS_ENABLE=false` → 400 (by design; must enable first)
- Strict Pydantic `Job` model strips extra fields if you run `Job(**dict)` on normalized live jobs — ingestion uses `.dict()` only on seed JSON; live jobs bypass strict validation
- Bare JSON array responses without `total` → single-page fetch only

---

## Commands

```bash
# One-shot sync + reindex (from backend/)
cd backend
export REAL_JOBS_ENABLE=true
export REAL_JOBS_BASE_URL=https://your-provider.example.com
python scripts/sync_real_jobs_once.py

# Via running API
curl -s http://localhost:8000/real-jobs/status | jq
curl -s -X POST http://localhost:8000/real-jobs/sync \
  -H 'Content-Type: application/json' \
  -d '{"reindex": true}' | jq

# Start API with live jobs enabled
cd backend
REAL_JOBS_ENABLE=true REAL_JOBS_BASE_URL=https://your-provider.example.com \
  uvicorn app:app --reload --port 8000

# Test sync disabled behavior
pytest backend/tests/test_api.py::test_real_jobs_sync_disabled -v
pytest backend/tests/test_api.py::test_get_real_jobs_status -v
```

---

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/real_jobs_sync.py` | **Source of truth** for upstream contract, normalization, pagination, snapshot |
| `backend/app.py` | `/real-jobs/status`, `/real-jobs/sync`, startup snapshot boot, agent pre-sync |
| `backend/ingestion.py` | How normalized jobs become embeddings + vector metadata |
| `backend/schemas.py` | Strict seed job schema (subset of canonical live job) |
| `backend/scripts/sync_real_jobs_once.py` | CLI sync without HTTP |
| `frontend/src/App.jsx` | `handleSyncRealJobs`, `fetchRealJobsStatus` — client integration reference |
| `backend/tests/test_api.py` | Status + disabled-sync tests |
| `data/jobs.json` | Static fallback corpus (15 jobs) |
| `.claude/knowledge_graph.md` | Broader system encyclopedia including API matrix |

---

## External links

None documented in repo for provider OpenAPI. User-Agent references: `https://aiforjob.ai`

---

## Memory snapshot

- `.claude/knowledge_graph.md` — full backend/frontend encyclopedia, paper↔code gaps, eval corpus
- `.claude/knowledge_graph.json` — machine-readable metrics + code_reference

---

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`, `.claude/knowledge_graph.json`
- Technical docs: `README.md` (env vars), `docs/report/DOCUMENTATION.md` (API table)
- Manuscript API table: `docs/submission/jaamas/manuscript/sections/section-5.tex`

---

## Next steps (for new application)

1. **Confirm provider URL + auth** — verify: manual `curl` to `{BASE}/jobs?limit=1&skip=0` returns expected JSON envelope.
2. **Port `normalize_external_job` logic** — verify: output matches canonical schema above for 3 sample raw jobs.
3. **Implement pagination loop** — verify: fetch all pages until `skip + limit >= total`; compare `deduped_count` with provider total.
4. **Decide snapshot strategy** — keep `jobs_live.json` pattern or replace with DB; verify: restart loads last sync without re-fetch.
5. **Wire ingestion** — embed `job_document_text` equivalent and upsert to your vector store; verify: ANN search returns synced job IDs.
6. **Expose sync/status endpoints** — mirror `GET /real-jobs/status` + `POST /real-jobs/sync` or call provider directly from new app.
7. **Add integration test** — mock provider paginated JSON; verify: normalize + dedupe + empty-response error handling.

---

## Quick reference — endpoint cheat sheet

| Layer | Endpoint | Purpose |
|-------|----------|---------|
| **Provider (upstream)** | `GET {BASE}{PATH}?limit=&skip=` | Paginated job feed |
| **This backend** | `GET /real-jobs/status` | Config + sync state |
| **This backend** | `POST /real-jobs/sync` | Fetch upstream → snapshot → memory → reindex |
| **This backend** | `GET /jobs/full` | Current job catalog after sync |
| **This backend** | `POST /agent/run-daily-recommendations` | Optional pre-sync + batch recommendations |
