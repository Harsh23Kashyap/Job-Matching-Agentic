"""Run fairness baseline on eval corpus."""
from __future__ import annotations

import json

from config import Settings
from core.calibration import PlattCalibrator
from core.fairness import evaluate_fairness_report
from core.fusion import LearnedFusionModel
from core.matchmaking_scoring import resolve_routing, score_pair_advanced
from contracts.matching import MatchRequest

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels


def run_fairness_eval(
    settings: Settings | None = None,
    *,
    top_k: int = 5,
    fusion_model: LearnedFusionModel | None = None,
    calibrator: PlattCalibrator | None = None,
) -> dict:
    settings = settings or Settings()
    resumes = json.loads(settings.cvs_path.read_text(encoding="utf-8"))
    jobs_raw = json.loads(settings.jobs_path.read_text(encoding="utf-8"))
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    model_name = settings.embedding_model

    if fusion_model is None:
        fusion_model = LearnedFusionModel.load(settings.fusion_model_path)
    if calibrator is None:
        calibrator = PlattCalibrator.load(settings.calibration_model_path)

    job_snaps = [job_to_snapshot(j, model_name) for j in jobs_raw]
    cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    base_req = MatchRequest(
        query_key="",
        top_k=top_k,
        fusion_mode="learned",
        apply_constraints=True,
        auto_strategy=True,
        use_calibration=True,
        strategy="multimodal",
    )

    ranked_by_query: dict[str, list[tuple[str, float]]] = {}
    query_metadata: dict[str, dict] = {}

    for cv in resumes:
        qid = cv["id"]
        if qid not in cv_snaps:
            continue
        cand = cv_snaps[qid]
        req, _ = resolve_routing(cand, base_req)
        scored: list[tuple[str, float]] = []
        for job in job_snaps:
            breakdown, _, _ = score_pair_advanced(
                cand,
                job,
                req,
                model_name=model_name,
                fusion_model=fusion_model,
                calibrator=calibrator,
                feedback_store=None,
            )
            scored.append((job.id, breakdown.final_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        ranked_by_query[qid] = scored
        query_metadata[qid] = {
            "experience_years": cv.get("experience_years", 0),
            "remote_preference": cv.get("remote_preference", False),
            "name": cv.get("name", ""),
        }

    report = evaluate_fairness_report(ranked_by_query, query_metadata)
    report["queries_evaluated"] = len(ranked_by_query)
    report["eval_pairs_in_labels"] = sum(len(v) for v in eval_map.values())
    return report
