#!/usr/bin/env bash
# Build JAAMAS portal information sheet PDF.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEX="${SCRIPT_DIR}/information-sheet.tex"
COMPILE="${HOME}/latex-document-skill/scripts/compile_latex.sh"

if [[ -x "${COMPILE}" ]]; then
  bash "${COMPILE}" "${TEX}" --quiet
else
  pdflatex -interaction=nonstopmode -output-directory="${SCRIPT_DIR}" "${TEX}" >/dev/null
  pdflatex -interaction=nonstopmode -output-directory="${SCRIPT_DIR}" "${TEX}" >/dev/null
fi

echo "Wrote ${SCRIPT_DIR}/information-sheet.pdf"
