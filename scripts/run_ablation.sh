#!/usr/bin/env bash
# Composite matching ablation study → backend/reports/ablation_*
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
python -m benchmarks.run_ablation "$@"
