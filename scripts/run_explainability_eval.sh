#!/usr/bin/env bash
# Explainability evaluation → backend/reports/explainability_*
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
python -m benchmarks.run_explainability_eval "$@"
