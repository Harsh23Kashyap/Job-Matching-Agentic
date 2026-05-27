# Tests

**208 pytest** + **20 node** tests (as of 2026-05-27).

## Run all

```bash
cd backend && source .venv/bin/activate
pytest ../tests -q

node --test tests/unit/test_*.mjs
```

## Folders

| Folder | README | Scope |
|--------|--------|-------|
| [unit/](unit/README.md) | Isolated logic | Agents, scoring, parsers, stores, frontend utils |
| [integration/](integration/README.md) | HTTP + flows | Auth, match, profile upsert, feature checklist |
| `benchmarks/` | Regression | Table 9 / eval pair gates |

## Shared fixtures

`conftest.py` · test client, in-memory or temp DB, bootstrapped system container.

## Feature checklist

```bash
pytest tests/integration/test_feature_reverification.py -q
```

Covers: composite scoring, JD parse, feedback, CID cleanup, profile upsert.

## Frontend build

```bash
cd frontend && npm run build
```
