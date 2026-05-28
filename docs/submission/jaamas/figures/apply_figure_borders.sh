#!/usr/bin/env bash
# Bake #94a3b8 frames into screenshot PNGs and diagram PNG previews.
# Manuscript PDF figures also get a LaTeX frame via \JFigFramed in jaamas-macros.tex.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"
if [[ -x "$ROOT/../../../../backend/.venv/bin/python" ]]; then
  PYTHON="$ROOT/../../../../backend/.venv/bin/python"
fi

"$PYTHON" "$ROOT/crop_figures.py" "$ROOT" --borders-only --border-screenshots-only --border-px 3
"$PYTHON" "$ROOT/crop_figures.py" "$ROOT" --borders-only --border-figure-png-only --border-px 2

echo "Done: borders applied to screenshots/ and Fig*.png previews"
