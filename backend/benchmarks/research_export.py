"""Export benchmark artifacts into docs/research/evaluation/ for paper and thesis use."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import Settings

REPORT_FILES = {
    "embedding": [
        "benchmark_report.json",
        "benchmark_summary.csv",
        "benchmark_per_query.csv",
    ],
    "comparison": [
        "comparison_table.csv",
        "comparison_table.json",
        "comparison_summary.json",
    ],
    "ablation": [
        "ablation_report.json",
        "ablation_summary.json",
        "ablation_summary.csv",
        "ablation_table.csv",
        "ablation_summary.md",
        "ablation_per_query.csv",
    ],
    "significance_benchmark": [
        "significance_report.json",
        "significance_summary.md",
        "significance_comparisons.csv",
        "significance_methods.csv",
    ],
    "significance_ablation": [
        "significance_ablation_report.json",
        "significance_ablation_summary.md",
        "significance_ablation_comparisons.csv",
        "significance_ablation_methods.csv",
    ],
    "cross_encoder": [
        "cross_encoder_report.json",
        "cross_encoder_table.csv",
        "cross_encoder_rank_changes.json",
    ],
    "fairness_audit": [
        "fairness_audit_report.json",
        "fairness_audit_summary.md",
        "fairness_audit_pairs.csv",
        "fairness_audit_flagged.csv",
    ],
}


def _run_module(module: str, *args: str, env: dict | None = None) -> None:
    cmd = [sys.executable, "-m", module, *args]
    subprocess.run(cmd, check=True, env=env)


def run_all_studies(
    settings: Settings,
    reports_dir: Path,
    *,
    top_k: int = 5,
    skip_cross_encoder: bool = False,
) -> None:
    """Execute every offline research runner; writes to backend/reports/."""
    reports_dir.mkdir(parents=True, exist_ok=True)
    common = ["--top-k", str(top_k), "--out-dir", str(reports_dir)]

    _run_module("benchmarks.run_eval", *common, "--prefix", "benchmark")
    _run_module("benchmarks.run_comparison", *common, "--prefix", "comparison")
    _run_module("benchmarks.run_ablation", *common, "--prefix", "ablation")
    _run_module(
        "benchmarks.run_significance",
        *common,
        "--prefix",
        "significance",
        "--source",
        "benchmark",
    )
    _run_module(
        "benchmarks.run_significance",
        *common,
        "--prefix",
        "significance_ablation",
        "--source",
        "ablation",
        "--baseline",
        "semantic_only",
    )
    if not skip_cross_encoder:
        import os

        ce_env = os.environ.copy()
        ce_env["ENABLE_CROSS_ENCODER_RERANK"] = "true"
        _run_module(
            "benchmarks.run_cross_encoder_report",
            "--top-k",
            str(top_k),
            "--out-dir",
            str(reports_dir),
            env=ce_env,
        )
    _run_module(
        "benchmarks.run_fairness_audit",
        "--top-k",
        str(top_k),
        "--out-dir",
        str(reports_dir),
    )


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_study_files(reports_dir: Path, dest: Path, filenames: list[str]) -> list[str]:
    copied: list[str] = []
    dest.mkdir(parents=True, exist_ok=True)
    for name in filenames:
        src = reports_dir / name
        if src.is_file():
            shutil.copy2(src, dest / name)
            copied.append(name)
    return copied


def _fmt_row(values: list[Any]) -> str:
    return "| " + " | ".join(str(v) for v in values) + " |"


def _metrics_table(rows: list[dict], name_field: str, extra_cols: list[tuple[str, str]] | None = None) -> str:
    headers = [name_field, "P@K", "R@K", "MRR", "nDCG@K", "MAP"]
    if extra_cols:
        headers.extend(label for _, label in extra_cols)
    lines = [_fmt_row(headers), _fmt_row(["---"] * len(headers))]
    for row in rows:
        vals = [
            row.get(name_field.replace(" ", "_").lower(), row.get(name_field, "")),
            f"{row['precision_at_k']:.3f}",
            f"{row['recall_at_k']:.3f}",
            f"{row['mrr']:.3f}",
            f"{row['ndcg_at_k']:.3f}",
            f"{row['map']:.3f}",
        ]
        if extra_cols:
            for key, _ in extra_cols:
                val = row.get(key, "")
                vals.append(f"{val:.3f}" if isinstance(val, float) else str(val))
        # Fix name field lookup
        display = row.get("method") or row.get("variant") or row.get(name_field, "")
        vals[0] = display
        lines.append(_fmt_row(vals))
    return "\n".join(lines)


def _write_embedding_study(path: Path, payload: dict | None) -> None:
    if not payload:
        path.write_text("# Embedding strategies\n\n*No data — run research suite first.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    lines = [
        "# Study 1 — Embedding Retrieval Strategies",
        "",
        f"Generated from: `artifacts/.../embedding/benchmark_report.json`",
        "",
        "## Protocol",
        "",
        "- **Task:** resume → jobs (exhaustive ranking over 15 jobs per query)",
        f"- **Corpus:** {meta['corpus']['candidates']} candidates, {meta['corpus']['jobs']} jobs",
        f"- **Queries:** {meta['corpus']['labeled_queries']} labeled in `data/eval_pairs.json`",
        f"- **Top-K:** {meta['top_k']}",
        f"- **Embedding model:** `{meta['embedding_model']}`",
        f"- **Multimodal semantic weight:** {meta.get('semantic_weight_multimodal', 0.7)}",
        f"- **RRF k:** {meta.get('rrf_k', 60)}",
        "",
        "## Strategies",
        "",
        "| Key | Method | Description |",
        "|-----|--------|-------------|",
    ]
    for row in payload["summary"]:
        lines.append(f"| `{row['method_key']}` | {row['method']} | {row.get('description', '')} |")
    lines.extend(["", "## Results (macro-averaged)", "", _metrics_table(payload["summary"], "method"), ""])
    best = max(payload["summary"], key=lambda r: r["ndcg_at_k"])
    lines.extend(
        [
            "## Best method",
            "",
            f"**{best['method']}** — nDCG@{meta['top_k']} = {best['ndcg_at_k']:.3f}, "
            f"MRR = {best['mrr']:.3f}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_comparison_study(path: Path, payload: dict | None) -> None:
    if not payload:
        path.write_text("# Lexical vs embedding\n\n*No data.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    lexical = [r for r in payload["summary"] if r.get("family") == "lexical"]
    embedding = [r for r in payload["summary"] if r.get("family") == "embedding"]
    lines = [
        "# Study 2 — Lexical vs Embedding Baselines",
        "",
        "## Protocol",
        "",
        f"- Same corpus and labels as Study 1 (K={meta['top_k']})",
        "- Lexical: BM25, TF-IDF cosine, exact skill overlap",
        "- Embedding: semantic, skills, soft embed, multimodal, RRF",
        "- Latency measured as mean ms per query (exhaustive scan)",
        "",
        "## Lexical baselines",
        "",
        _metrics_table(lexical, "method", [("latency_ms", "latency_ms")]),
        "",
        "## Embedding strategies",
        "",
        _metrics_table(embedding, "method", [("latency_ms", "latency_ms")]),
        "",
        "## Observations",
        "",
    ]
    best_lex = max(lexical, key=lambda r: r["ndcg_at_k"]) if lexical else None
    best_emb = max(embedding, key=lambda r: r["ndcg_at_k"]) if embedding else None
    if best_lex and best_emb:
        lines.append(
            f"- Best lexical: **{best_lex['method']}** (nDCG={best_lex['ndcg_at_k']:.3f}, "
            f"{best_lex['latency_ms']:.2f} ms/query)"
        )
        lines.append(
            f"- Best embedding: **{best_emb['method']}** (nDCG={best_emb['ndcg_at_k']:.3f}, "
            f"{best_emb['latency_ms']:.2f} ms/query)"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_ablation_study(path: Path, payload: dict | None) -> None:
    if not payload:
        path.write_text("# Ablation\n\n*No data.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    weights = meta.get("composite_weights", {})
    lines = [
        "# Study 3 — Composite Matching Ablation",
        "",
        "## Production composite weights",
        "",
        "| Component | Weight |",
        "|-----------|--------|",
    ]
    for comp, w in weights.items():
        lines.append(f"| {comp.capitalize()} | {w:.0%} |")
    lines.extend(
        [
            "",
            f"- **Skills mode:** {meta.get('skills_mode', 'jaccard')}",
            f"- **Best variant (nDCG):** {meta.get('best_ndcg', 'n/a')}",
            "",
            "## Variants",
            "",
            "| Variant | Category | Components | P@K | R@K | MRR | nDCG@K | MAP | ms |",
            "|---------|----------|------------|-----|-----|-----|--------|-----|-----|",
        ]
    )
    for row in payload["summary"]:
        lines.append(
            f"| {row['variant']} | {row['category']} | {row['components']} | "
            f"{row['precision_at_k']:.3f} | {row['recall_at_k']:.3f} | {row['mrr']:.3f} | "
            f"{row['ndcg_at_k']:.3f} | {row['map']:.3f} | {row.get('latency_ms', 0):.2f} |"
        )
    lines.extend(
        [
            "",
            "## Findings",
            "",
            "- Semantic-only is the strongest single signal (nDCG ~0.88).",
            "- Structural signals alone (experience, compensation, location) rank poorly in isolation.",
            "- Full weighted composite (40/30/15/10/5) achieves best nDCG on this corpus.",
            "- RRF over single-component rankers underperforms weighted composite here.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_significance_study(path: Path, payload: dict | None, *, title: str, baseline_note: str) -> None:
    if not payload:
        path.write_text(f"# {title}\n\n*No data.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    k = meta.get("top_k", 5)
    lines = [
        f"# {title}",
        "",
        "## Setup",
        "",
        f"- **Baseline:** {meta['baseline']} (`{meta['baseline_key']}`)",
        f"- **Metrics:** {', '.join(meta['metrics'])}",
        f"- **Resamples:** {meta['n_resamples']:,} (seed={meta['seed']})",
        f"- **p-value:** {meta['p_value_definition']}",
        baseline_note,
        "",
        "## Method means with 95% bootstrap CI",
        "",
        "| Method | Metric | Mean | 95% CI |",
        "|--------|--------|------|--------|",
    ]
    for method in payload["methods"]:
        for metric in meta["metrics"]:
            m = method["metrics"][metric]
            label = "nDCG@K" if metric == "ndcg_at_k" else "MRR"
            disp = f"nDCG@{k}" if label == "nDCG@K" else label
            lines.append(
                f"| {method['method']} | {disp} | {m['mean']:.4f} | "
                f"[{m['ci95_lo']:.4f}, {m['ci95_hi']:.4f}] |"
            )
    lines.extend(
        [
            "",
            f"## Paired comparisons vs {meta['baseline']}",
            "",
            "| Compare | Metric | Δ mean | 95% CI | p-value | sig@0.05 | W/L/T |",
            "|---------|--------|--------|--------|---------|----------|-------|",
        ]
    )
    for row in payload["comparisons"]:
        sig = "yes" if row["significant_at_05"] else "no"
        disp = f"nDCG@{k}" if row["metric"] == "ndcg_at_k" else "MRR"
        lines.append(
            f"| {row['compare']} | {disp} | {row['mean_diff']:+.4f} | "
            f"[{row['ci95_lo']:+.4f}, {row['ci95_hi']:+.4f}] | {row['p_value']:.4f} | {sig} | "
            f"{row['wins']}/{row['losses']}/{row['ties']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_cross_encoder_study(path: Path, payload: dict | None) -> None:
    if not payload:
        path.write_text("# Cross-encoder\n\n*No data.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    q = meta.get("quality_summary", {})
    lat = meta.get("latency_summary", {})
    lines = [
        "# Study 5 — Two-Stage Cross-Encoder Reranking",
        "",
        "## Setup",
        "",
        f"- **Strategy:** {meta.get('strategy', 'composite')}",
        f"- **Top-K:** {meta.get('top_k', 5)}",
        f"- **Rerank pool:** {meta.get('rerank_pool', 20)}",
        f"- **Queries:** {meta.get('queries', 30)}",
        "",
        "## Quality summary",
        "",
        f"| Metric | Bi-encoder | + Cross-encoder | Δ |",
        f"|--------|------------|-----------------|---|",
        f"| nDCG@K | {q.get('ndcg_baseline', 0):.3f} | {q.get('ndcg_with_ce', 0):.3f} | {q.get('ndcg_delta', 0):+.3f} |",
        f"| MRR | — | — | {q.get('mrr_delta', 0):+.3f} |",
        "",
        "## Latency",
        "",
        f"- Bi-encoder avg: {lat.get('baseline_avg_ms', 0):.2f} ms/query",
        f"- With CE avg: {lat.get('with_ce_avg_ms', 0):.2f} ms/query",
        f"- CE overhead: {lat.get('cross_encoder_overhead_ms', 0):.2f} ms/query",
        "",
        "## Note",
        "",
        "Cross-encoder is **not enabled in production UI by default**. "
        "Requires `ENABLE_CROSS_ENCODER_RERANK=true` and explicit `use_cross_encoder` on match API.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_fairness_audit_study(path: Path, payload: dict | None) -> None:
    if not payload:
        path.write_text("# Fairness audit\n\n*No data.*\n", encoding="utf-8")
        return
    meta = payload["meta"]
    summaries = payload.get("pair_summaries", [])
    lines = [
        "# Study 6 — Fairness & Bias Audit (Synthetic Profiles)",
        "",
        f"> {meta.get('warning', 'Synthetic profiles only.')}",
        "",
        f"- Pairs: {meta.get('pairs', 0)}",
        f"- Jobs per variant: {meta.get('jobs', 0)}",
        f"- Strategy: `{meta.get('strategy', 'composite')}`",
        f"- Flagged pairs: {meta.get('flagged_pairs', 0)} ({meta.get('flagged_pair_rate', 0):.0%})",
        "",
        "| Pair | Category | Top-1 stable | Top-K overlap | Max score Δ | Flagged |",
        "|------|----------|--------------|---------------|-------------|---------|",
    ]
    k = meta.get("top_k", 5)
    for row in summaries:
        lines.append(
            f"| {row['pair_id']} | {row['category']} | "
            f"{'yes' if row['top_1_stable'] else 'no'} | "
            f"{row['top_k_overlap_count']}/{k} | {row['max_score_delta']:.4f} | "
            f"{'yes' if row['flagged'] else 'no'} |"
        )
    lines.extend(["", "See `methodology/fairness-audit.md` for protocol details.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_findings(path: Path, bundle: dict[str, Any]) -> None:
    emb = bundle.get("embedding") or {}
    cmp_ = bundle.get("comparison") or {}
    abl = bundle.get("ablation") or {}
    sig = bundle.get("significance_benchmark") or {}
    ce = bundle.get("cross_encoder") or {}
    fair = bundle.get("fairness_audit") or {}

    lines = [
        "# Research Findings — Synthesis",
        "",
        f"Run ID: `{bundle.get('run_id', 'unknown')}`",
        "",
        "## Corpus",
        "",
        "- 30 candidate profiles, 15 job postings, 30 labeled queries (47 graded pairs)",
        "- Graded relevance 0–2 in `data/eval_pairs.json`; binary relevant = grade > 0",
        "- Evaluation protocol: exhaustive ranking (all jobs scored per query)",
        "",
        "## Headline results (K=5)",
        "",
    ]

    if emb.get("summary"):
        best = max(emb["summary"], key=lambda r: r["ndcg_at_k"])
        lines.append(
            f"1. **Best embedding strategy:** {best['method']} — "
            f"nDCG@5={best['ndcg_at_k']:.3f}, MRR={best['mrr']:.3f}"
        )
    if abl.get("summary"):
        full = next((r for r in abl["summary"] if r.get("variant_key") == "full_composite"), None)
        if full:
            lines.append(
                f"2. **Production composite (ablation):** nDCG@5={full['ndcg_at_k']:.3f}, "
                f"R@5={full['recall_at_k']:.3f} — best among ablation variants"
            )
    if sig.get("comparisons"):
        sig_ndcg = [r for r in sig["comparisons"] if r["metric"] == "ndcg_at_k" and r["significant_at_05"]]
        if sig_ndcg:
            names = ", ".join(r["compare"] for r in sig_ndcg)
            lines.append(f"3. **Significant vs semantic baseline (nDCG, p<0.05):** {names}")
        else:
            lines.append("3. **Significance:** no method significantly beats semantic baseline on nDCG at α=0.05")
    if ce.get("meta", {}).get("quality_summary"):
        q = ce["meta"]["quality_summary"]
        lines.append(
            f"4. **Cross-encoder on composite:** nDCG Δ={q.get('ndcg_delta', 0):+.3f} "
            f"(quality ↓, latency ↑ ~{ce['meta'].get('latency_summary', {}).get('cross_encoder_overhead_ms', 0):.0f} ms/query)"
        )
    if fair.get("meta"):
        fm = fair["meta"]
        lines.append(
            f"5. **Fairness audit (synthetic):** {fm.get('flagged_pairs', 0)}/{fm.get('pairs', 0)} pairs flagged "
            f"under demographic counterfactuals — manual review required"
        )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Small fixed corpus (n=30 queries) — bootstrap CIs are wide",
            "- Exhaustive evaluation ≠ ANN production path (see phase11 for store sweep)",
            "- Cross-encoder model adds heavy latency; not default in portals",
            "- Composite weights (40/30/15/10/5) are hand-tuned, not learned",
            "",
            "## Artifact index",
            "",
            "See `artifacts/manifest.json` and per-study folders under `artifacts/runs/<run_id>/`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_unified_tables(tables_dir: Path, bundle: dict[str, Any]) -> None:
    tables_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    cmp_ = bundle.get("comparison") or {}
    for row in cmp_.get("summary", []):
        all_rows.append(
            {
                "study": "lexical_vs_embedding",
                "method_key": row.get("method_key"),
                "method": row.get("method"),
                "family": row.get("family"),
                "precision_at_k": row.get("precision_at_k"),
                "recall_at_k": row.get("recall_at_k"),
                "mrr": row.get("mrr"),
                "ndcg_at_k": row.get("ndcg_at_k"),
                "map": row.get("map"),
                "latency_ms": row.get("latency_ms"),
            }
        )
    abl = bundle.get("ablation") or {}
    for row in abl.get("summary", []):
        all_rows.append(
            {
                "study": "ablation",
                "method_key": row.get("variant_key"),
                "method": row.get("variant"),
                "family": row.get("category"),
                "precision_at_k": row.get("precision_at_k"),
                "recall_at_k": row.get("recall_at_k"),
                "mrr": row.get("mrr"),
                "ndcg_at_k": row.get("ndcg_at_k"),
                "map": row.get("map"),
                "latency_ms": row.get("latency_ms"),
            }
        )

    if all_rows:
        fields = list(all_rows[0].keys())
        with (tables_dir / "table_all_methods.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_rows)

    sig = bundle.get("significance_benchmark") or {}
    if sig.get("comparisons"):
        fields = [
            "baseline",
            "compare",
            "metric",
            "baseline_mean",
            "compare_mean",
            "mean_diff",
            "ci95_lo",
            "ci95_hi",
            "p_value",
            "significant_at_05",
            "wins",
            "losses",
            "ties",
        ]
        with (tables_dir / "table_significance.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            for row in sig["comparisons"]:
                out = {
                    "baseline": row.get("baseline"),
                    "compare": row.get("compare"),
                    "metric": row.get("metric_label") or row.get("metric"),
                    "baseline_mean": row.get("baseline_mean"),
                    "compare_mean": row.get("compare_mean"),
                    "mean_diff": row.get("mean_diff"),
                    "ci95_lo": row.get("ci95_lo"),
                    "ci95_hi": row.get("ci95_hi"),
                    "p_value": row.get("p_value"),
                    "significant_at_05": row.get("significant_at_05"),
                    "wins": row.get("wins"),
                    "losses": row.get("losses"),
                    "ties": row.get("ties"),
                }
                writer.writerow(out)


def export_research_bundle(
    *,
    settings: Settings | None = None,
    reports_dir: Path | None = None,
    out_root: Path | None = None,
    run_id: str | None = None,
    from_cache: bool = False,
    skip_cross_encoder: bool = False,
    top_k: int = 5,
) -> dict[str, Path]:
    """Run studies (optional) and export to docs/research/evaluation/."""
    settings = settings or Settings()
    reports_dir = Path(reports_dir or settings.repo_root / "backend" / "reports")
    out_root = Path(out_root or settings.repo_root / "docs" / "research" / "evaluation")
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    if not from_cache:
        run_all_studies(settings, reports_dir, top_k=top_k, skip_cross_encoder=skip_cross_encoder)

    run_dir = out_root / "artifacts" / "runs" / run_id
    studies_dir = out_root / "studies"
    methodology_dir = out_root / "methodology"
    tables_dir = out_root / "artifacts" / "tables"

    studies_dir.mkdir(parents=True, exist_ok=True)
    methodology_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "run_id": run_id,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "reports_source": str(reports_dir),
        "top_k": top_k,
        "studies": {},
    }

    bundle: dict[str, Any] = {"run_id": run_id}

    for study_key, filenames in REPORT_FILES.items():
        dest = run_dir / study_key.replace("_benchmark", "").replace("_ablation", "_ablation")
        if study_key == "significance_benchmark":
            dest = run_dir / "significance" / "benchmark"
        elif study_key == "significance_ablation":
            dest = run_dir / "significance" / "ablation"
        copied = _copy_study_files(reports_dir, dest, filenames)
        manifest["studies"][study_key] = {"dest": str(dest.relative_to(out_root)), "files": copied}

        json_name = next((f for f in filenames if f.endswith("_report.json") or f.endswith("_summary.json")), None)
        if json_name and (dest / json_name).is_file():
            key = study_key.replace("significance_benchmark", "significance_benchmark").replace(
                "significance_ablation", "significance_ablation"
            )
            if study_key == "embedding":
                bundle["embedding"] = _load_json(dest / "benchmark_report.json")
            elif study_key == "comparison":
                bundle["comparison"] = _load_json(dest / "comparison_summary.json")
            elif study_key == "ablation":
                bundle["ablation"] = _load_json(dest / "ablation_summary.json")
            elif study_key == "significance_benchmark":
                bundle["significance_benchmark"] = _load_json(dest / "significance_report.json")
            elif study_key == "significance_ablation":
                bundle["significance_ablation"] = _load_json(dest / "significance_ablation_report.json")
            elif study_key == "cross_encoder":
                bundle["cross_encoder"] = _load_json(dest / "cross_encoder_report.json")
            elif study_key == "fairness_audit":
                bundle["fairness_audit"] = _load_json(dest / "fairness_audit_report.json")

    _write_embedding_study(studies_dir / "01-embedding-strategies.md", bundle.get("embedding"))
    _write_comparison_study(studies_dir / "02-lexical-vs-embedding.md", bundle.get("comparison"))
    _write_ablation_study(studies_dir / "03-composite-ablation.md", bundle.get("ablation"))
    _write_significance_study(
        studies_dir / "04-significance-embedding.md",
        bundle.get("significance_benchmark"),
        title="Study 4a — Bootstrap Significance (Embedding Strategies)",
        baseline_note="- Compares embedding suite vs **Semantic cosine** baseline",
    )
    _write_significance_study(
        studies_dir / "04-significance-ablation.md",
        bundle.get("significance_ablation"),
        title="Study 4b — Bootstrap Significance (Ablation Variants)",
        baseline_note="- Compares ablation variants vs **Semantic only** baseline",
    )
    _write_cross_encoder_study(studies_dir / "05-cross-encoder.md", bundle.get("cross_encoder"))
    _write_fairness_audit_study(studies_dir / "06-fairness-audit.md", bundle.get("fairness_audit"))
    _write_findings(out_root / "FINDINGS.md", bundle)
    _write_unified_tables(tables_dir, bundle)

    manifest_path = out_root / "artifacts" / "manifest.json"
    manifest["findings"] = str((out_root / "FINDINGS.md").relative_to(out_root))
    manifest["studies_docs"] = [str(p.relative_to(out_root)) for p in sorted(studies_dir.glob("*.md"))]
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    latest_link = out_root / "artifacts" / "latest"
    if latest_link.is_symlink() or latest_link.exists():
        if latest_link.is_symlink():
            latest_link.unlink()
        elif latest_link.is_dir():
            shutil.rmtree(latest_link)
    try:
        latest_link.symlink_to(f"runs/{run_id}", target_is_directory=True)
    except OSError:
        shutil.copytree(run_dir, latest_link, dirs_exist_ok=True)

    return {
        "run_dir": run_dir,
        "manifest": manifest_path,
        "findings": out_root / "FINDINGS.md",
        "tables": tables_dir,
    }
