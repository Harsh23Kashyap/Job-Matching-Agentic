"""Format paper-ready tables as Markdown, CSV, and LaTeX (booktabs)."""
from __future__ import annotations

import csv
import io
import re
from typing import Any


def _fmt_float(value: Any, digits: int = 3) -> str:
    if value is None or value == "":
        return "---"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def _escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = str(text)
    for char, repl in replacements.items():
        out = out.replace(char, repl)
    return out


def bold_best_markdown(rows: list[list[str]], col_idx: int, *, higher_is_better: bool = True) -> list[list[str]]:
    """Bold the best numeric value in a column (for markdown)."""
    numeric: list[tuple[int, float]] = []
    for i, row in enumerate(rows):
        try:
            val = float(row[col_idx])
            numeric.append((i, val))
        except (ValueError, IndexError):
            continue
    if not numeric:
        return rows
    best = max(numeric, key=lambda x: x[1]) if higher_is_better else min(numeric, key=lambda x: x[1])
    out = [list(r) for r in rows]
    idx = best[0]
    out[idx][col_idx] = f"**{out[idx][col_idx]}**"
    return out


def to_markdown_table(
    headers: list[str],
    rows: list[list[str]],
    *,
    caption: str = "",
    label: str = "",
    note: str = "",
) -> str:
    lines: list[str] = []
    if caption:
        lines.extend([f"**{caption}**", ""])
    if label:
        lines.append(f"*Label: `{label}`*")
        lines.append("")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    if note:
        lines.extend(["", f"*Note: {note}*"])
    lines.append("")
    return "\n".join(lines)


def to_csv(headers: list[str], rows: list[list[str]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def to_latex_table(
    headers: list[str],
    rows: list[list[str]],
    *,
    caption: str,
    label: str,
    note: str = "",
    col_align: str | None = None,
) -> str:
    n = len(headers)
    align = col_align or ("l" + "r" * (n - 1))
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{_escape_latex(caption)}}}",
        rf"\label{{{label}}}",
        rf"\begin{{tabular}}{{{align}}}",
        r"\toprule",
        " & ".join(_escape_latex(h) for h in headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(_escape_latex(c) for c in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    if note:
        lines.append(rf"\footnotesize{{{_escape_latex(note)}}}")
    lines.extend([r"\end{table}", ""])
    return "\n".join(lines)


def write_table_bundle(
    out_dir,
    stem: str,
    headers: list[str],
    rows: list[list[str]],
    *,
    caption: str,
    label: str,
    note: str = "",
    markdown_rows: list[list[str]] | None = None,
    col_align: str | None = None,
) -> dict[str, Any]:
    from pathlib import Path

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_rows = markdown_rows if markdown_rows is not None else rows
    md = to_markdown_table(headers, md_rows, caption=caption, label=label, note=note)
    csv_text = to_csv(headers, rows)
    tex = to_latex_table(headers, rows, caption=caption, label=label, note=note, col_align=col_align)

    paths = {
        "markdown": out_dir / f"{stem}.md",
        "csv": out_dir / f"{stem}.csv",
        "latex": out_dir / f"{stem}.tex",
    }
    paths["markdown"].write_text(md, encoding="utf-8")
    paths["csv"].write_text(csv_text, encoding="utf-8")
    paths["latex"].write_text(tex, encoding="utf-8")
    return {"stem": stem, "label": label, "paths": paths, "rows": len(rows)}
