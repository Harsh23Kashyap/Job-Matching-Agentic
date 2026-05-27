# Unit tests

Split by runtime:

| Folder | Runtime | Count | README |
|--------|---------|-------|--------|
| [backend/](backend/) | Python / pytest | 33 files | [backend/README.md](backend/README.md) |
| [frontend/](frontend/) | Node `node:test` | 9 files | [frontend/README.md](frontend/README.md) |

Quick run:

```bash
bash scripts/run_tests.sh          # everything
pytest tests/unit/backend -q       # backend only
node --test tests/unit/frontend/test_*.mjs   # frontend only
```
