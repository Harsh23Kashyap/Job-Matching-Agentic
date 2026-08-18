#!/usr/bin/env bash
# Synthetic fairness & bias audit → backend/reports/fairness_audit_*
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
python -m benchmarks.run_fairness_audit "$@"
