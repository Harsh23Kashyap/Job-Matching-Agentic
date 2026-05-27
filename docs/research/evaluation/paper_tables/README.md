# Paper Tables — Copy-Paste Artifacts

Generated from `backend/reports/` benchmark outputs.

| # | Table | Label | Markdown | CSV | LaTeX |
|---|-------|-------|----------|-----|-------|
| 1 | table1_method_comparison | `tab:method-comparison` | [md](table1_method_comparison.md) | [csv](table1_method_comparison.csv) | [tex](table1_method_comparison.tex) |
| 2 | table2_ablation | `tab:ablation` | [md](table2_ablation.md) | [csv](table2_ablation.csv) | [tex](table2_ablation.tex) |
| 3 | table3_latency | `tab:latency` | [md](table3_latency.md) | [csv](table3_latency.csv) | [tex](table3_latency.tex) |
| 4 | table4_fairness | `tab:fairness` | [md](table4_fairness.md) | [csv](table4_fairness.csv) | [tex](table4_fairness.tex) |
| 5 | table5_explanation_quality | `tab:explanation-quality` | [md](table5_explanation_quality.md) | [csv](table5_explanation_quality.csv) | [tex](table5_explanation_quality.tex) |
| 6 | table6_qualitative_examples | `tab:qualitative` | [md](table6_qualitative_examples.md) | [csv](table6_qualitative_examples.csv) | [tex](table6_qualitative_examples.tex) |

## Usage in manuscript

- **Markdown:** paste into Google Docs / Notion or convert via Pandoc.
- **CSV:** import to Excel or `csv_to_latex.py` from latex-document skill.
- **LaTeX:** copy into `assets/templates/academic-paper.tex` or thesis chapter; requires booktabs.

```bash
cd ~/latex-document-skill
python3 scripts/csv_to_latex.py path/to/table1_method_comparison.csv --style booktabs \
  --caption "Method comparison" --label tab:method-comparison
```
