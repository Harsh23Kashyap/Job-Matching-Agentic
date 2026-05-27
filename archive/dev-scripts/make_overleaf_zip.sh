#!/usr/bin/env bash
# Package JAAMAS manuscript sources for Overleaf / Springer upload.
# Output: docs/submission/jaamas/build/jaamas-overleaf-upload.zip
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/docs/submission/jaamas"
BUILD="${ROOT}/build"
STAGING="${BUILD}/overleaf-staging"
ZIP="${BUILD}/jaamas-overleaf-upload.zip"

rm -rf "${STAGING}"
mkdir -p "${STAGING}/manuscript/sections" "${STAGING}/manuscript/tables" "${STAGING}/figures" "${BUILD}"

# --- Manuscript core ---
cp "${ROOT}/manuscript/main.tex" \
   "${ROOT}/manuscript/sn-jnl.cls" \
   "${ROOT}/manuscript/sn-mathphys-num.bst" \
   "${ROOT}/manuscript/references.bib" \
   "${ROOT}/manuscript/jaamas-macros.tex" \
   "${ROOT}/manuscript/jaamas-style.tex" \
   "${STAGING}/manuscript/"

# Vendored LaTeX deps (BasicTeX / minimal Overleaf compatibility)
for sty in cuted.sty threeparttable.sty wrapfig.sty appendix.sty enumitem.sty; do
  if [[ -f "${ROOT}/manuscript/${sty}" ]]; then
    cp "${ROOT}/manuscript/${sty}" "${STAGING}/manuscript/"
  fi
done

cp "${ROOT}/manuscript/sections/"*.tex "${STAGING}/manuscript/sections/"
cp "${ROOT}/manuscript/tables/"*.tex "${STAGING}/manuscript/tables/"

# --- Figures (submission PDFs only) ---
cp "${ROOT}/figures"/Fig*.pdf "${STAGING}/figures/"

# --- README for Overleaf ---
cat > "${STAGING}/README-OVERLEAF.txt" <<'EOF'
JAAMAS Overleaf upload package
==============================

Compile: manuscript/main.tex with pdfLaTeX + BibTeX (sn-mathphys-num.bst).

Directory layout:
  manuscript/main.tex
  manuscript/sections/*.tex
  manuscript/tables/*.tex
  figures/Fig1.pdf ... Fig5.pdf

Do NOT add main-preprint.tex or archive/ contents to this project.
EOF

# --- Build zip (exclude build artifacts and forbidden paths) ---
rm -f "${ZIP}"
(
  cd "${STAGING}"
  zip -r "${ZIP}" . \
    -x "*.log" -x "*.aux" -x "*.out" -x "*.blg" -x "*.bbl" -x "*.fdb_latexmk" -x "*.fls" \
    -x "*main-preprint*" -x "*/archive/*" -x "*/docs/latex/*"
)

rm -rf "${STAGING}"

echo "Wrote ${ZIP}"
echo ""
echo "Contents:"
unzip -l "${ZIP}" | sed 's|^|  |'
