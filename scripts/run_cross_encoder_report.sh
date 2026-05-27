#!/usr/bin/env bash
# Bi-encoder vs two-stage cross-encoder report → backend/reports/cross_encoder_table.csv
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
python -m benchmarks.run_cross_encoder_report "$@"
