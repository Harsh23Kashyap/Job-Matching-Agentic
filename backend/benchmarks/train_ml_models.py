"""Train fusion + calibration models from labeled eval pairs."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from config import Settings
from core.calibration import PlattCalibrator
from core.fusion import LearnedFusionModel, extract_pair_features
from core.scoring import compute_multimodal_weighted

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels


def build_training_matrix(settings: Settings | None = None):
    settings = settings or Settings()
    resumes = json.loads(settings.cvs_path.read_text(encoding="utf-8"))
    jobs = json.loads(settings.jobs_path.read_text(encoding="utf-8"))
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    model_name = settings.embedding_model

    jobs_by_id = {j["id"]: job_to_snapshot(j, model_name) for j in jobs}
    cvs_by_id = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

    features: list[np.ndarray] = []
    labels: list[float] = []
    raw_scores: list[float] = []

    for qid, rel_map in eval_map.items():
        if qid not in cvs_by_id:
            continue
        cand = cvs_by_id[qid]
        for jid, rel in rel_map.items():
            if jid not in jobs_by_id or rel < 0:
                continue
            job = jobs_by_id[jid]
            feat = extract_pair_features(cand, job, model_name=model_name)
            features.append(feat)
            labels.append(1.0 if rel >= 1 else 0.0)
            base = compute_multimodal_weighted(cand, job, model_name=model_name)
            raw_scores.append(base.final_score)

    return np.vstack(features), np.array(labels), np.array(raw_scores)


def main():
    settings = Settings()
    out_dir = settings.data_dir / "models"
    out_dir.mkdir(parents=True, exist_ok=True)

    X, y, raw_scores = build_training_matrix(settings)
    fusion = LearnedFusionModel.train(X, y)
    fusion.save(out_dir / "fusion.json")

    calibrator = PlattCalibrator.fit(raw_scores, y)
    calibrator.save(out_dir / "calibration.json")

    print(f"Trained fusion on {len(y)} pairs → {out_dir / 'fusion.json'}")
    print(f"Trained Platt calibrator → {out_dir / 'calibration.json'}")


if __name__ == "__main__":
    main()
