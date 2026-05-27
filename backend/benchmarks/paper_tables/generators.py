"""Generate paper-ready tables from benchmark report artifacts."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from benchmarks.paper_tables.formatters import (
    _fmt_float,
    bold_best_markdown,
    write_table_bundle,
)


REPORT_FILES = {
    "comparison": "comparison_summary.json",
    "ablation": "ablation_summary.csv",
    "cross_encoder": "cross_encoder_report.json",
    "fairness": "fairness_audit_pairs.csv",
    "explainability": "explainability_report.json",
    "explainability_flagged": "explainability_flagged.csv",
}


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _short_method(name: str) -> str:
    mapping = {
        "BM25 (lexical)": "BM25",
        "TF-IDF cosine (lexical)": "TF-IDF",
        "Exact skill overlap": "Exact overlap",
        "Semantic cosine": "Semantic (cosine)",
        "Semantic euclidean-derived": "Semantic (L2)",
        "Skills Jaccard": "Skills Jaccard",
        "Soft skill embedding": "Soft skill embed",
        "Multimodal weighted blend": "Multimodal",
        "RRF ensemble": "RRF",
    }
    return mapping.get(name, name)


def generate_method_comparison(reports_dir: Path, out_dir: Path, *, top_k: int = 5) -> dict[str, Any]:
    payload = _load_json(reports_dir / REPORT_FILES["comparison"])
    if not payload:
        return {"error": "missing comparison_summary.json"}

    headers = ["Method", "Family", f"P@{top_k}", f"R@{top_k}", "MRR", f"nDCG@{top_k}", "MAP"]
    rows: list[list[str]] = []
    md_rows: list[list[str]] = []

    sorted_summary = sorted(payload["summary"], key=lambda r: r["ndcg_at_k"], reverse=True)
    for row in sorted_summary:
        data_row = [
            _short_method(row["method"]),
            row.get("family", "").capitalize(),
            _fmt_float(row["precision_at_k"]),
            _fmt_float(row["recall_at_k"]),
            _fmt_float(row["mrr"]),
            _fmt_float(row["ndcg_at_k"]),
            _fmt_float(row["map"]),
        ]
        rows.append(data_row)
        md_rows.append(list(data_row))

    md_rows = bold_best_markdown(md_rows, col_idx=5)
    meta = payload.get("meta", {})
    note = (
        f"Exhaustive ranking over {meta.get('corpus', {}).get('jobs', 15)} jobs, "
        f"{meta.get('corpus', {}).get('labeled_queries', 30)} queries, K={top_k}. "
        f"Embedding model: {meta.get('embedding_model', 'all-MiniLM-L6-v2')}."
    )
    return write_table_bundle(
        out_dir,
        "table1_method_comparison",
        headers,
        rows,
        markdown_rows=md_rows,
        caption=f"Retrieval method comparison (macro-averaged, K={top_k}).",
        label="tab:method-comparison",
        note=note,
        col_align="llrrrrr",
    )


def generate_ablation_table(reports_dir: Path, out_dir: Path, *, top_k: int = 5) -> dict[str, Any]:
    rows_csv = _load_csv_rows(reports_dir / REPORT_FILES["ablation"])
    if not rows_csv:
        return {"error": "missing ablation_summary.csv"}

    headers = ["Variant", "Category", f"P@{top_k}", f"R@{top_k}", "MRR", f"nDCG@{top_k}", "MAP"]
    rows: list[list[str]] = []
    md_rows: list[list[str]] = []

    ordered = sorted(rows_csv, key=lambda r: float(r["ndcg_at_k"]), reverse=True)
    for row in ordered:
        data_row = [
            row["variant"],
            row["category"].capitalize(),
            _fmt_float(row["precision_at_k"]),
            _fmt_float(row["recall_at_k"]),
            _fmt_float(row["mrr"]),
            _fmt_float(row["ndcg_at_k"]),
            _fmt_float(row["map"]),
        ]
        rows.append(data_row)
        md_rows.append(list(data_row))

    md_rows = bold_best_markdown(md_rows, col_idx=5)
    note = (
        "Composite weights: semantic 40\\%, skills 30\\%, experience 15\\%, "
        "compensation 10\\%, location 5\\%. Partial variants use renormalized weights."
    )
    return write_table_bundle(
        out_dir,
        "table2_ablation",
        headers,
        rows,
        markdown_rows=md_rows,
        caption=f"Ablation over composite matching components (K={top_k}).",
        label="tab:ablation",
        note=note.replace("\\%", "%"),
        col_align="llrrrrr",
    )


def generate_latency_table(reports_dir: Path, out_dir: Path, *, top_k: int = 5) -> dict[str, Any]:
    comparison = _load_json(reports_dir / REPORT_FILES["comparison"])
    ce = _load_json(reports_dir / REPORT_FILES["cross_encoder"])
    if not comparison:
        return {"error": "missing comparison_summary.json"}

    headers = ["Method", f"nDCG@{top_k}", "Latency (ms/query)", "Notes"]
    rows: list[list[str]] = []

    for row in sorted(comparison["summary"], key=lambda r: r["latency_ms"]):
        note = "Lexical baseline" if row.get("family") == "lexical" else "Embedding"
        rows.append(
            [
                _short_method(row["method"]),
                _fmt_float(row["ndcg_at_k"]),
                _fmt_float(row["latency_ms"], 2),
                note,
            ]
        )

    if ce:
        lat = ce["meta"].get("latency_summary", {})
        qual = ce["meta"].get("quality_summary", {})
        rows.append(
            [
                "Composite + cross-encoder",
                _fmt_float(qual.get("ndcg_with_ce")),
                _fmt_float(lat.get("with_ce_avg_ms"), 1),
                f"Pool={ce['meta'].get('rerank_pool', 20)}; ΔnDCG={_fmt_float(qual.get('ndcg_delta'), 3)}",
            ]
        )
        rows.append(
            [
                "Composite (bi-encoder only)",
                _fmt_float(qual.get("ndcg_baseline")),
                _fmt_float(lat.get("baseline_avg_ms"), 2),
                "Production composite baseline",
            ]
        )

    note = "Latency is mean wall-clock ms per query on exhaustive evaluation (single machine)."
    return write_table_bundle(
        out_dir,
        "table3_latency",
        headers,
        rows,
        caption="Quality–latency trade-off across retrieval methods.",
        label="tab:latency",
        note=note,
        col_align="lrrl",
    )


def generate_fairness_table(reports_dir: Path, out_dir: Path, *, top_k: int = 5) -> dict[str, Any]:
    rows_csv = _load_csv_rows(reports_dir / REPORT_FILES["fairness"])
    if not rows_csv:
        return {"error": "missing fairness_audit_pairs.csv"}

    headers = [
        "Pair",
        "Field changed",
        "Top-1 stable",
        f"Top-{top_k} overlap",
        "Max rank Δ",
        "Max score Δ",
        "Flagged",
    ]
    rows: list[list[str]] = []
    for row in rows_csv:
        overlap = float(row["top_k_overlap"]) * top_k
        rows.append(
            [
                row["pair_id"],
                row["field_changed"],
                "Yes" if row["top_1_stable"] == "True" else "No",
                f"{int(round(overlap))}/{top_k}",
                str(row["max_rank_change"]),
                _fmt_float(row["max_score_delta"], 4),
                "Yes" if row["flagged"] == "True" else "No",
            ]
        )

    flagged = sum(1 for r in rows_csv if r["flagged"] == "True")
    note = (
        f"Synthetic counterfactual pairs only ({len(rows_csv)} pairs). "
        f"{flagged} flagged under score-delta and rank-stability thresholds. "
        "No protected attributes inferred from real users."
    )
    return write_table_bundle(
        out_dir,
        "table4_fairness",
        headers,
        rows,
        caption="Fairness audit under synthetic demographic counterfactuals.",
        label="tab:fairness",
        note=note,
        col_align="lllrrrl",
    )


def generate_explanation_quality_table(reports_dir: Path, out_dir: Path) -> dict[str, Any]:
    payload = _load_json(reports_dir / REPORT_FILES["explainability"])
    if not payload:
        return {"error": "missing explainability_report.json"}

    headers = [
        "Explainer",
        "Faithfulness",
        "Specificity",
        "Skill mention (%)",
        "No hallucination (%)",
        "Component align (%)",
        "Flagged (%)",
        "Consistency (Jaccard)",
    ]
    rows: list[list[str]] = []
    cons = payload["meta"].get("consistency_by_mode", {})
    for mode, stats in payload["meta"].get("by_mode", {}).items():
        jaccard = cons.get(mode, {}).get("avg_jaccard")
        rows.append(
            [
                mode.capitalize(),
                _fmt_float(stats["avg_faithfulness"]),
                _fmt_float(stats["avg_specificity"]),
                _fmt_float(stats["pass_mentions_skill"] * 100, 1),
                _fmt_float(stats["pass_no_hallucination"] * 100, 1),
                _fmt_float(stats["pass_component_alignment"] * 100, 1),
                _fmt_float(stats["flagged_rate"] * 100, 1),
                _fmt_float(jaccard) if jaccard is not None else "---",
            ]
        )

    note = (
        "Automated checks on top-5 composite matches. "
        "Faithfulness = pass rate on skill mention, hallucination, and component alignment checks. "
        "Consistency = bullet Jaccard on synthetic similar-profile pairs."
    )
    return write_table_bundle(
        out_dir,
        "table5_explanation_quality",
        headers,
        rows,
        caption="Explainability evaluation summary (rules vs. grounded template).",
        label="tab:explanation-quality",
        note=note,
        col_align="lrrrrrrr",
    )


def generate_qualitative_examples(
    reports_dir: Path,
    out_dir: Path,
    data_dir: Path,
    *,
    max_examples: int = 6,
) -> dict[str, Any]:
    flagged = _load_csv_rows(reports_dir / REPORT_FILES["explainability_flagged"])
    fairness = _load_csv_rows(reports_dir / REPORT_FILES["fairness"])

    cvs = {}
    jobs = {}
    cvs_path = data_dir / "cvs.json"
    jobs_path = data_dir / "jobs.json"
    if cvs_path.is_file():
        cvs = {c["id"]: c for c in json.loads(cvs_path.read_text(encoding="utf-8"))}
    if jobs_path.is_file():
        jobs = {j["id"]: j for j in json.loads(jobs_path.read_text(encoding="utf-8"))}

    examples: list[dict[str, Any]] = []

    def add_example(category: str, title: str, detail: str, bullets: str, issue: str) -> None:
        if len(examples) >= max_examples:
            return
        examples.append(
            {"category": category, "title": title, "detail": detail, "bullets": bullets, "issue": issue}
        )

    # Hallucination case
    for row in flagged:
        if "hallucinated_skills" in row.get("violations", "") and row.get("hallucinated_skills"):
            cv = cvs.get(row["candidate_id"], {})
            job = jobs.get(row["job_id"], {})
            add_example(
                "Hallucination",
                f"{cv.get('name', row['candidate_id'])} → {job.get('title', row['job_id'])}",
                f"Rank {row['rank']}; explainer={row['explain_mode']}",
                row.get("bullets", "").replace(" || ", "; "),
                f"Phantom skill: {row['hallucinated_skills']}",
            )
            break

    # Generic / missing skill reference
    for row in flagged:
        if "missing_skill_reference" in row.get("violations", "") and row.get("missing_skills"):
            cv = cvs.get(row["candidate_id"], {})
            job = jobs.get(row["job_id"], {})
            add_example(
                "Low specificity",
                f"{cv.get('name', row['candidate_id'])} → {job.get('title', row['job_id'])}",
                f"Missing skills: {row.get('missing_skills', '')}",
                row.get("bullets", "").replace(" || ", "; "),
                "Explanation omits matched/missing skills; generic component bullets only.",
            )
            break

    # Fairness top-1 change
    for row in fairness:
        if row.get("top_1_stable") == "False":
            add_example(
                "Fairness (rank shift)",
                f"Synthetic pair `{row['pair_id']}`",
                f"Field changed: {row['field_changed']}; max score Δ={row['max_score_delta']}",
                "Ranking order changed for top-1 job when only demographic-like metadata differed.",
                row.get("flag_reasons", "top_1_changed"),
            )
            break

    # Template success (non-flagged from report if available)
    payload = _load_json(reports_dir / REPORT_FILES["explainability"])
    if payload:
        for inst in payload.get("flagged_instances", []):
            pass
    # Pick a rules case with good skill mention from instances - load from flagged inverse via report
    inst_path = reports_dir / "explainability_instances.csv"
    if inst_path.is_file():
        for row in _load_csv_rows(inst_path):
            if (
                row.get("explain_mode") == "template"
                and row.get("flagged") == "False"
                and row.get("rank") == "1"
            ):
                cv = cvs.get(row["candidate_id"], {})
                job = jobs.get(row["job_id"], {})
                add_example(
                    "Grounded template (pass)",
                    f"{cv.get('name', row['candidate_id'])} → {job.get('title', row['job_id'])}",
                    f"Faithfulness={row.get('faithfulness_score')}, specificity={row.get('specificity_score')}",
                    row.get("bullets", "").replace(" || ", "; "),
                    "Passes skill mention and component alignment checks.",
                )
                break
        for row in _load_csv_rows(inst_path):
            if row.get("explain_mode") == "rules" and "component_mismatch" in row.get("violations", ""):
                cv = cvs.get(row["candidate_id"], {})
                job = jobs.get(row["job_id"], {})
                add_example(
                    "Component mismatch",
                    f"{cv.get('name', row['candidate_id'])} → {job.get('title', row['job_id'])}",
                    f"Violations: {row.get('violations', '')}",
                    row.get("bullets", "").replace(" || ", "; "),
                    "Textual claim inconsistent with score breakdown.",
                )
                break

    headers = ["Category", "Case", "Context", "Explanation excerpt", "Issue / outcome"]
    rows = [
        [ex["category"], ex["title"], ex["detail"], ex["bullets"][:200], ex["issue"]]
        for ex in examples[:max_examples]
    ]

    md_lines = [
        "**Table 6 · Qualitative explanation and fairness examples**",
        "",
        "*Label: `tab:qualitative`*",
        "",
    ]
    for i, ex in enumerate(examples[:max_examples], start=1):
        md_lines.extend(
            [
                f"### Example {i}: {ex['category']}",
                "",
                f"**Case:** {ex['title']}",
                "",
                f"**Context:** {ex['detail']}",
                "",
                f"**Explanation:** {ex['bullets']}",
                "",
                f"**Issue / outcome:** {ex['issue']}",
                "",
            ]
        )

    note = "Selected instances illustrate failure modes and grounded template successes from automated audit."
    from benchmarks.paper_tables.formatters import _escape_latex, to_csv

    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "markdown": out_dir / "table6_qualitative_examples.md",
        "csv": out_dir / "table6_qualitative_examples.csv",
        "latex": out_dir / "table6_qualitative_examples.tex",
    }
    paths["markdown"].write_text("\n".join(md_lines), encoding="utf-8")
    paths["csv"].write_text(to_csv(headers, rows), encoding="utf-8")
    # Qualitative table uses p{...} for long text in LaTeX
    tex_rows = rows
    tex = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Qualitative examples of explanation quality and fairness audit findings.}",
        r"\label{tab:qualitative}",
        r"\small",
        r"\begin{tabular}{p{1.6cm}p{2.2cm}p{2.5cm}p{4.5cm}p{3cm}}",
        r"\toprule",
        " & ".join(headers) + r" \\",
        r"\midrule",
    ]
    from benchmarks.paper_tables.formatters import _escape_latex

    for row in tex_rows:
        tex.append(" & ".join(_escape_latex(c) for c in row) + r" \\")
    tex.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\footnotesize{" + _escape_latex(note) + "}",
            r"\end{table}",
            "",
        ]
    )
    paths["latex"].write_text("\n".join(tex), encoding="utf-8")

    return {"stem": "table6_qualitative_examples", "label": "tab:qualitative", "paths": paths, "rows": len(rows)}


def generate_all_paper_tables(
    *,
    reports_dir: Path,
    out_dir: Path,
    data_dir: Path,
    top_k: int = 5,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    generators = [
        ("method_comparison", lambda: generate_method_comparison(reports_dir, out_dir, top_k=top_k)),
        ("ablation", lambda: generate_ablation_table(reports_dir, out_dir, top_k=top_k)),
        ("latency", lambda: generate_latency_table(reports_dir, out_dir, top_k=top_k)),
        ("fairness", lambda: generate_fairness_table(reports_dir, out_dir, top_k=top_k)),
        ("explanation_quality", lambda: generate_explanation_quality_table(reports_dir, out_dir)),
        (
            "qualitative_examples",
            lambda: generate_qualitative_examples(reports_dir, out_dir, data_dir),
        ),
    ]

    results: dict[str, Any] = {}
    index_lines = [
        "# Paper Tables · Copy-Paste Artifacts",
        "",
        f"Generated from `backend/reports/` benchmark outputs.",
        "",
        "| # | Table | Label | Markdown | CSV | LaTeX |",
        "|---|-------|-------|----------|-----|-------|",
    ]

    for i, (key, fn) in enumerate(generators, start=1):
        result = fn()
        results[key] = result
        if "error" in result:
            index_lines.append(f"| {i} | {key} | · | *missing data* | | |")
            continue
        p = result["paths"]
        index_lines.append(
            f"| {i} | {result['stem']} | `{result['label']}` | "
            f"[md]({p['markdown'].name}) | [csv]({p['csv'].name}) | [tex]({p['latex'].name}) |"
        )

    index_lines.extend(
        [
            "",
            "## Usage in manuscript",
            "",
            "- **Markdown:** paste into Google Docs / Notion or convert via Pandoc.",
            "- **CSV:** import to Excel or `csv_to_latex.py` from latex-document skill.",
            "- **LaTeX:** copy into `assets/templates/academic-paper.tex` or thesis chapter; requires booktabs.",
            "",
            "```bash",
            "cd ~/latex-document-skill",
            "python3 scripts/csv_to_latex.py path/to/table1_method_comparison.csv --style booktabs \\",
            '  --caption "Method comparison" --label tab:method-comparison',
            "```",
            "",
        ]
    )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reports_dir": str(reports_dir),
        "out_dir": str(out_dir),
        "top_k": top_k,
        "tables": {
            k: {
                "label": v.get("label"),
                "stem": v.get("stem"),
                "rows": v.get("rows"),
                "error": v.get("error"),
            }
            for k, v in results.items()
        },
    }

    (out_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {"manifest": manifest, "results": results, "out_dir": out_dir}
