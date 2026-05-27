"""Hard negative mining report for contrastive / rerank analysis."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from config import Settings
from core.scoring import compute_multimodal_weighted

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels


def mine_hard_negatives(top_k: int = 5, pool: int = 10):
    settings = Settings()
    resumes = json.loads(settings.cvs_path.read_text(encoding="utf-8"))
    jobs = json.loads(settings.jobs_path.read_text(encoding="utf-8"))
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    model_name = settings.embedding_model

    job_snaps = {j["id"]: job_to_snapshot(j, model_name) for j in jobs}
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    report: list[dict] = []
    for qid, rel_map in eval_map.items():
        if qid not in cv_snaps:
            continue
        cand = cv_snaps[qid]
        relevant = {jid for jid, r in rel_map.items() if r > 0}
        scored = []
        for jid, job in job_snaps.items():
            b = compute_multimodal_weighted(cand, job, model_name=model_name)
            scored.append((jid, b.final_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        hard_negs = [jid for jid, _ in scored[:pool] if jid not in relevant][:top_k]
        report.append({"query_id": qid, "hard_negatives": hard_negs, "relevant": sorted(relevant)})

    out = settings.repo_root / "backend" / "benchmark_outputs" / "hard_negatives.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Mined {len(report)} queries → {out}")


if __name__ == "__main__":
    mine_hard_negatives()
