#!/usr/bin/env bash
# Full research suite → docs/research/evaluation/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
python -m benchmarks.run_research_suite "$@"
