#!/usr/bin/env bash
# Full offline research pipeline → backend/reports/research_run_<timestamp>/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -f backend/.venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source backend/.venv/bin/activate
fi
python backend/scripts/run_research_pipeline.py "$@"
