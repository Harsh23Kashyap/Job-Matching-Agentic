# Tests

**302 pytest** + **Node frontend utils** (9 files) as of 2026-05-28.

## Run all

```bash
bash scripts/run_tests.sh
```

Or manually:

```bash
cd backend && source .venv/bin/activate
pytest ../tests -q

node --test tests/unit/frontend/test_*.mjs
```

## Layout

```
tests/
├── conftest.py           # shared pytest fixtures (repo root paths, system bootstrap)
├── unit/
│   ├── backend/          # Python unit tests (agents, scoring, parsers, stores)
│   └── frontend/         # Node tests for frontend/src/utils/*
├── integration/          # HTTP / TestClient flows
└── benchmarks/           # offline eval + paper regression gates
```

| Folder | README | Scope |
|--------|--------|-------|
| [unit/backend/](unit/backend/) | yes | Isolated backend logic |
| [unit/frontend/](unit/frontend/) | yes | Frontend utility modules |
| [integration/](integration/) | yes | Auth, match, profile, demo flows |
| [benchmarks/](benchmarks/) | yes | Table 9 / eval pair regression |

## External live jobs

When `REAL_JOBS_ENABLE=true`, sync external job feeds via `GET/POST /real-jobs/*`.
See [docs/design/external-live-jobs-api-HANDOFF.md](../docs/design/external-live-jobs-api-HANDOFF.md).

## Shared fixtures

`conftest.py` · test client, temp DB, bootstrapped `SystemContainer`.

## Feature checklist

```bash
pytest tests/integration/test_feature_reverification.py -q
```

## Live smoke (optional)

Requires backend on `:8001`:

```bash
python3 scripts/smoke_employer_jobs.py
```

## Frontend build

```bash
cd frontend && npm run build
```
