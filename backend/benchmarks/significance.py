"""Paired bootstrap significance testing for offline benchmark results."""
from __future__ import annotations

import csv
import json
import random
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIGNIFICANCE_METRICS = [
    ("ndcg_at_k", "nDCG@K"),
    ("mrr", "MRR"),
]

DEFAULT_N_RESAMPLES = 5000
DEFAULT_SEED = 42
TIE_EPS = 1e-12

COMPARISON_CSV_FIELDS = [
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
    "n_queries",
]

METHOD_CSV_FIELDS = [
    "method_key",
    "method",
    "metric",
    "mean",
    "ci95_lo",
    "ci95_hi",
    "n_queries",
]


@dataclass
class SignificanceReport:
    meta: dict[str, Any]
    methods: list[dict[str, Any]]
    comparisons: list[dict[str, Any]]


def bootstrap_mean_ci(
    values: list[float],
    *,
    n_resamples: int = DEFAULT_N_RESAMPLES,
    seed: int = DEFAULT_SEED,
) -> dict[str, float | int]:
    """Non-parametric 95% CI for the mean via bootstrap resampling."""
    if not values:
        return {"mean": 0.0, "ci95_lo": 0.0, "ci95_hi": 0.0, "n": 0}

    rng = random.Random(seed)
    n = len(values)
    boot_means = []
    for _ in range(n_resamples):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        boot_means.append(statistics.mean(sample))
    boot_means.sort()
    return {
        "mean": statistics.mean(values),
        "ci95_lo": boot_means[int(0.025 * n_resamples)],
        "ci95_hi": boot_means[int(0.975 * n_resamples)],
        "n": n,
    }


def win_loss_tie(baseline: list[float], compare: list[float], *, tie_eps: float = TIE_EPS) -> tuple[int, int, int]:
    wins = losses = ties = 0
    for b, c in zip(baseline, compare):
        diff = c - b
        if diff > tie_eps:
            wins += 1
        elif diff < -tie_eps:
            losses += 1
        else:
            ties += 1
    return wins, losses, ties


def paired_bootstrap_test(
    baseline: dict[str, float],
    compare: dict[str, float],
    *,
    n_resamples: int = DEFAULT_N_RESAMPLES,
    seed: int = DEFAULT_SEED,
    tie_eps: float = TIE_EPS,
) -> dict[str, Any]:
    """Paired bootstrap on query-level score differences (compare − baseline)."""
    keys = sorted(set(baseline) & set(compare))
    base_vals = [baseline[k] for k in keys]
    comp_vals = [compare[k] for k in keys]
    diffs = [c - b for b, c in zip(base_vals, comp_vals)]

    wins, losses, ties = win_loss_tie(base_vals, comp_vals, tie_eps=tie_eps)

    rng = random.Random(seed)
    boot_diffs: list[float] = []
    for _ in range(n_resamples):
        sample = [diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        boot_diffs.append(statistics.mean(sample))
    boot_diffs.sort()

    ci_lo = boot_diffs[int(0.025 * n_resamples)]
    ci_hi = boot_diffs[int(0.975 * n_resamples)]
    p_value = sum(1 for m in boot_diffs if m <= 0) / n_resamples

    return {
        "baseline_mean": statistics.mean(base_vals),
        "compare_mean": statistics.mean(comp_vals),
        "mean_diff": statistics.mean(diffs),
        "ci95_lo": ci_lo,
        "ci95_hi": ci_hi,
        "p_value": p_value,
        "significant_at_05": p_value < 0.05,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "n_queries": len(keys),
    }


def paired_bootstrap_ndcg(
    per_query: list[dict[str, Any]],
    baseline: str,
    compare: str,
    *,
    n_resamples: int = DEFAULT_N_RESAMPLES,
    seed: int = DEFAULT_SEED,
    method_field: str = "method",
) -> dict[str, Any]:
    """Backward-compatible wrapper used by paper_progression."""
    base = {r["query_id"]: r["ndcg_at_k"] for r in per_query if r.get(method_field) == baseline}
    comp = {r["query_id"]: r["ndcg_at_k"] for r in per_query if r.get(method_field) == compare}
    result = paired_bootstrap_test(base, comp, n_resamples=n_resamples, seed=seed)
    return {
        "baseline": baseline,
        "compare": compare,
        "metric": "ndcg_at_k",
        "mean_ndcg_diff": result["mean_diff"],
        "ci95_lo": result["ci95_lo"],
        "ci95_hi": result["ci95_hi"],
        "p_value": result["p_value"],
        "significant_at_05": result["significant_at_05"],
        "wins": result["wins"],
        "losses": result["losses"],
        "ties": result["ties"],
        "n_queries": result["n_queries"],
    }


def index_per_query_scores(
    per_query: list[dict[str, Any]],
    *,
    method_key_field: str = "method_key",
    method_label_field: str = "method",
    query_field: str = "query_id",
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, dict[str, float]]]]:
    """Return method labels and nested scores[method_key][metric][query_id]."""
    labels: dict[str, str] = {}
    scores: dict[str, dict[str, dict[str, float]]] = {}

    for row in per_query:
        key = row[method_key_field]
        labels[key] = row.get(method_label_field, key)
        bucket = scores.setdefault(key, {})
        for metric, _ in SIGNIFICANCE_METRICS:
            bucket.setdefault(metric, {})[row[query_field]] = float(row[metric])
    return labels, scores


def run_significance_analysis(
    per_query: list[dict[str, Any]],
    *,
    baseline_key: str,
    compare_keys: list[str] | None = None,
    n_resamples: int = DEFAULT_N_RESAMPLES,
    seed: int = DEFAULT_SEED,
    method_key_field: str = "method_key",
    method_label_field: str = "method",
    top_k: int | None = None,
    task: str = "resume_to_jobs",
) -> SignificanceReport:
    labels, scores = index_per_query_scores(
        per_query,
        method_key_field=method_key_field,
        method_label_field=method_label_field,
    )
    if baseline_key not in scores:
        raise ValueError(f"Baseline key not found in per-query data: {baseline_key}")

    all_keys = sorted(scores)
    targets = compare_keys or [k for k in all_keys if k != baseline_key]
    baseline_label = labels[baseline_key]

    methods_out: list[dict[str, Any]] = []
    for key in all_keys:
        method_metrics: dict[str, Any] = {}
        for metric, label in SIGNIFICANCE_METRICS:
            vals = list(scores[key][metric].values())
            ci = bootstrap_mean_ci(vals, n_resamples=n_resamples, seed=seed + hash(key + metric) % 997)
            method_metrics[metric] = {
                "label": label,
                "mean": round(ci["mean"], 6),
                "ci95_lo": round(ci["ci95_lo"], 6),
                "ci95_hi": round(ci["ci95_hi"], 6),
                "n_queries": ci["n"],
            }
        methods_out.append(
            {
                "method_key": key,
                "method": labels[key],
                "metrics": method_metrics,
            }
        )

    comparisons: list[dict[str, Any]] = []
    for compare_key in targets:
        if compare_key == baseline_key or compare_key not in scores:
            continue
        compare_label = labels[compare_key]
        for metric, metric_label in SIGNIFICANCE_METRICS:
            result = paired_bootstrap_test(
                scores[baseline_key][metric],
                scores[compare_key][metric],
                n_resamples=n_resamples,
                seed=seed + hash((baseline_key, compare_key, metric)) % 997,
            )
            comparisons.append(
                {
                    "baseline_key": baseline_key,
                    "baseline": baseline_label,
                    "compare_key": compare_key,
                    "compare": compare_label,
                    "metric": metric,
                    "metric_label": metric_label,
                    "baseline_mean": round(result["baseline_mean"], 6),
                    "compare_mean": round(result["compare_mean"], 6),
                    "mean_diff": round(result["mean_diff"], 6),
                    "ci95_lo": round(result["ci95_lo"], 6),
                    "ci95_hi": round(result["ci95_hi"], 6),
                    "p_value": round(result["p_value"], 6),
                    "significant_at_05": result["significant_at_05"],
                    "wins": result["wins"],
                    "losses": result["losses"],
                    "ties": result["ties"],
                    "n_queries": result["n_queries"],
                }
            )

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "report_type": "bootstrap_significance",
        "task": task,
        "baseline_key": baseline_key,
        "baseline": baseline_label,
        "metrics": [m for m, _ in SIGNIFICANCE_METRICS],
        "n_resamples": n_resamples,
        "seed": seed,
        "top_k": top_k,
        "methods": all_keys,
        "compare_keys": targets,
        "p_value_definition": "one-sided: fraction of bootstrap mean-diffs <= 0 (H1: compare > baseline)",
    }
    return SignificanceReport(meta=meta, methods=methods_out, comparisons=comparisons)


def write_significance_report(
    report: SignificanceReport,
    out_dir: Path,
    *,
    prefix: str = "significance",
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{prefix}_report.json",
        "markdown": out_dir / f"{prefix}_summary.md",
        "comparisons_csv": out_dir / f"{prefix}_comparisons.csv",
        "methods_csv": out_dir / f"{prefix}_methods.csv",
    }

    paths["json"].write_text(
        json.dumps(
            {"meta": report.meta, "methods": report.methods, "comparisons": report.comparisons},
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["markdown"].write_text(render_significance_markdown(report), encoding="utf-8")

    with paths["methods_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=METHOD_CSV_FIELDS)
        writer.writeheader()
        for method in report.methods:
            for metric, label in SIGNIFICANCE_METRICS:
                m = method["metrics"][metric]
                writer.writerow(
                    {
                        "method_key": method["method_key"],
                        "method": method["method"],
                        "metric": label,
                        "mean": m["mean"],
                        "ci95_lo": m["ci95_lo"],
                        "ci95_hi": m["ci95_hi"],
                        "n_queries": m["n_queries"],
                    }
                )

    with paths["comparisons_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COMPARISON_CSV_FIELDS)
        writer.writeheader()
        for row in report.comparisons:
            writer.writerow(
                {
                    "baseline": row["baseline"],
                    "compare": row["compare"],
                    "metric": row["metric_label"],
                    "baseline_mean": row["baseline_mean"],
                    "compare_mean": row["compare_mean"],
                    "mean_diff": row["mean_diff"],
                    "ci95_lo": row["ci95_lo"],
                    "ci95_hi": row["ci95_hi"],
                    "p_value": row["p_value"],
                    "significant_at_05": row["significant_at_05"],
                    "wins": row["wins"],
                    "losses": row["losses"],
                    "ties": row["ties"],
                    "n_queries": row["n_queries"],
                }
            )

    return paths


def _metric_label(label: str, top_k: int | None) -> str:
    if top_k is None:
        return label
    if label == "nDCG@K":
        return f"nDCG@{top_k}"
    return label


def render_significance_markdown(report: SignificanceReport) -> str:
    meta = report.meta
    k = meta.get("top_k")
    lines = [
        "# Bootstrap Significance · Benchmark Results",
        "",
        f"Generated: {meta['generated_at']}",
        "",
        "## Setup",
        "",
        f"- Task: {meta['task']}",
        f"- Baseline: **{meta['baseline']}** (`{meta['baseline_key']}`)",
        f"- Metrics: {', '.join(meta['metrics'])}",
        f"- Resamples: {meta['n_resamples']:,} (seed={meta['seed']})",
        f"- p-value: {meta['p_value_definition']}",
    ]
    if k is not None:
        lines.append(f"- Top-K: {k}")

    lines.extend(
        [
            "",
            "## Method means with 95% bootstrap CI",
            "",
            "| Method | Metric | Mean | 95% CI |",
            "|--------|--------|------|--------|",
        ]
    )
    for method in report.methods:
        for metric, label in SIGNIFICANCE_METRICS:
            m = method["metrics"][metric]
            disp = _metric_label(label, k)
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
    for row in report.comparisons:
        sig = "yes" if row["significant_at_05"] else "no"
        disp = _metric_label(row["metric_label"], k)
        lines.append(
            f"| {row['compare']} | {disp} | {row['mean_diff']:+.4f} | "
            f"[{row['ci95_lo']:+.4f}, {row['ci95_hi']:+.4f}] | {row['p_value']:.4f} | {sig} | "
            f"{row['wins']}/{row['losses']}/{row['ties']} |"
        )

    sig_rows = [r for r in report.comparisons if r["significant_at_05"]]
    lines.extend(["", "## Significant improvements (p < 0.05)", ""])
    if sig_rows:
        for row in sig_rows:
            disp = _metric_label(row["metric_label"], k)
            lines.append(
                f"- **{row['compare']}** vs {row['baseline']} on {disp}: "
                f"Δ={row['mean_diff']:+.4f}, p={row['p_value']:.4f}, "
                f"W/L/T={row['wins']}/{row['losses']}/{row['ties']}"
            )
    else:
        lines.append("- None at α=0.05 (one-sided).")

    lines.append("")
    return "\n".join(lines)


def print_significance_summary(report: SignificanceReport) -> None:
    meta = report.meta
    print(
        f"\nBootstrap significance · baseline: {meta['baseline']}, "
        f"{meta['n_resamples']:,} resamples\n"
    )
    print(f"{'Compare':<28} {'Metric':<10} {'Δ':>8} {'CI lo':>8} {'CI hi':>8} {'p':>7} {'W/L/T':>9}")
    print("-" * 88)
    for row in report.comparisons:
        print(
            f"{row['compare']:<28} "
            f"{row['metric_label']:<10} "
            f"{row['mean_diff']:+8.4f} "
            f"{row['ci95_lo']:+8.4f} "
            f"{row['ci95_hi']:+8.4f} "
            f"{row['p_value']:7.4f} "
            f"{row['wins']}/{row['losses']}/{row['ties']:>5}"
        )
