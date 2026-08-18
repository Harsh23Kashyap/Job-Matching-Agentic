#!/usr/bin/env bash
# Export all JAAMAS Mermaid figures to PNG (review) and PDF (LaTeX).
# Portrait-friendly canvas + pdfFit + auto-crop to remove excess white edges.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
CFG="$ROOT/source/mermaid-config.json"
MMDC=(npx --yes @mermaid-js/mermaid-cli@11.4.0 -c "$CFG" -b white)

PORTRAIT_W=680
PORTRAIT_H=1400

for n in 1 2 3 4 5 6 7 8 9; do
  src="$ROOT/source/Fig${n}.mmd"
  if [[ ! -f "$src" ]]; then
    echo "Skip Fig${n}: missing $src" >&2
    continue
  fi
  echo "Exporting Fig${n}..."
  if [[ "$n" == "1" ]]; then
    echo "  Skip Fig1 (canonical source: source/Fig1.drawio; run export_fig1_drawio.sh)"
    continue
  elif [[ "$n" == "2" || "$n" == "3" ]]; then
    # Figs 2–3 agent internals: square grid layout
    "${MMDC[@]}" -i "$src" -o "$ROOT/Fig${n}.png" -s 4 -w 1000 -H 1000
    "${MMDC[@]}" -f -i "$src" -o "$ROOT/Fig${n}.pdf" -s 3 -w 1000 -H 1000
  else
    "${MMDC[@]}" -i "$src" -o "$ROOT/Fig${n}.png" -s 4 -w "$PORTRAIT_W" -H "$PORTRAIT_H"
    "${MMDC[@]}" -f -i "$src" -o "$ROOT/Fig${n}.pdf" -s 3 -w "$PORTRAIT_W" -H "$PORTRAIT_H"
  fi
done

echo "Cropping white margins..."
PYTHON="${PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  if [[ -x "$ROOT/../../../../backend/.venv/bin/python" ]]; then
    PYTHON="$ROOT/../../../../backend/.venv/bin/python"
  else
    PYTHON="python3"
  fi
fi
"$PYTHON" "$ROOT/crop_figures.py" "$ROOT" --margin 12 --tolerance 20 --fig-margins "1:48,2:32,3:32" --fig-square "2,3"

echo "Done. PDFs ready for \\\\JFigure in manuscript/sections/*.tex"
