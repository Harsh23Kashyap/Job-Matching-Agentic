#!/usr/bin/env bash
# Build all JAAMAS submission artifacts.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPILE="${HOME}/latex-document-skill/scripts/compile_latex.sh"

echo "== Manuscript =="
(
  cd "${ROOT}/manuscript"
  pdflatex -interaction=nonstopmode main.tex >/dev/null
  bibtex main >/dev/null 2>&1 || true
  pdflatex -interaction=nonstopmode main.tex >/dev/null
  pdflatex -interaction=nonstopmode main.tex >/dev/null
)
echo "  ${ROOT}/manuscript/main.pdf"

echo "== Portal =="
bash "${ROOT}/portal/build_cover_letter.sh"
bash "${ROOT}/portal/build_info_sheet.sh"

echo "== Supplementary =="
if [[ -x "${COMPILE}" ]]; then
  bash "${COMPILE}" "${ROOT}/supplementary/supplementary-information.tex" --quiet
else
  pdflatex -interaction=nonstopmode -output-directory="${ROOT}/supplementary" \
    "${ROOT}/supplementary/supplementary-information.tex" >/dev/null
fi
echo "  ${ROOT}/supplementary/supplementary-information.pdf"

echo "== Overleaf zip =="
bash "${ROOT}/../../../archive/dev-scripts/make_overleaf_zip.sh"

echo "Done."
