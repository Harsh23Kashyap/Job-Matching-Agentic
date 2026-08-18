#!/usr/bin/env bash
# Run full test suite: pytest (unit + integration + benchmarks) + Node frontend utils.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "Missing backend/.venv, create venv and install deps first." >&2
  exit 1
fi

echo "== pytest =="
pytest ../tests -q "$@"

echo ""
echo "== node (frontend utils) =="
node --test ../tests/unit/frontend/test_*.mjs

echo ""
echo "All tests passed."
