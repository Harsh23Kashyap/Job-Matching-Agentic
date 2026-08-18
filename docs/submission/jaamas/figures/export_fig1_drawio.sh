#!/usr/bin/env bash
# Regenerate Fig 1 from draw.io source (canonical HLD).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  if [[ -x "$ROOT/../../../../backend/.venv/bin/python" ]]; then
    PYTHON="$ROOT/../../../../backend/.venv/bin/python"
  else
    PYTHON="python3"
  fi
fi

"$PYTHON" "$ROOT/scripts/gen_fig1_drawio.py"

DRAWIO="${DRAWIO:-$(command -v drawio || true)}"
if [[ -z "$DRAWIO" && -x /opt/homebrew/bin/drawio ]]; then
  DRAWIO=/opt/homebrew/bin/drawio
fi
if [[ -z "$DRAWIO" ]]; then
  echo "draw.io CLI not found; install from https://www.drawio.com/" >&2
  exit 1
fi

SRC="$ROOT/source/Fig1.drawio"
for fmt in pdf png; do
  extra=(--crop -b 20)
  if [[ "$fmt" == "png" ]]; then
    extra=(-s 2 --crop -b 20)
  fi
  echo "Export Fig1.$fmt"
  "$DRAWIO" -x -f "$fmt" -o "$ROOT/Fig1.$fmt" "$SRC" "${extra[@]}"
done

"$PYTHON" "$ROOT/crop_figures.py" "$ROOT" --margin 12 --tolerance 20 --fig-margins "1:32"

echo "Done: $ROOT/Fig1.pdf and Fig1.png"
