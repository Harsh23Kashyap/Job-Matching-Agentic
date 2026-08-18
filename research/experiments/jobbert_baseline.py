"""EXP-014b: recruitment-domain encoder (JobBERT) dense-retrieval baseline (RQ1; RD-007).

Zero-shot domain encoder baseline: embed the SAME resume/job document texts the MiniLM semantic
channel uses (resume_document_text / job_document_text), but with jjzha/jobbert-base-cased
(mean-pooled), rank jobs per resume by cosine, compute nDCG@5. Only the ENCODER differs from the
semantic bi-encoder baseline -> a fair comparison. No training (zero-shot).

Run: cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/jobbert_baseline.py
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

from config import Settings
from core.document_text import job_document_text, resume_document_text
from benchmarks.eval_data import load_eval_labels
from benchmarks.extended_evaluation import load_settings_data, bootstrap_ci
from benchmarks.metrics import ndcg_at_k, precision_at_k, recall_at_k

REPO = Path(__file__).resolve().parents[2]
MODEL = "jjzha/jobbert-base-cased"
TOP_K = 5


def main() -> None:
    torch.manual_seed(42)
    settings = Settings()
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")
    cvs, jobs = load_settings_data(settings)

    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModel.from_pretrained(MODEL).eval()

    @torch.no_grad()
    def embed(texts):
        enc = tok(texts, padding=True, truncation=True, max_length=256, return_tensors="pt")
        out = model(**enc).last_hidden_state
        mask = enc["attention_mask"].unsqueeze(-1).float()
        vecs = (out * mask).sum(1) / mask.sum(1).clamp(min=1)
        vecs = torch.nn.functional.normalize(vecs, dim=-1)
        return vecs.cpu().numpy()

    cv_vecs = embed([resume_document_text(c) for c in cvs])
    job_vecs = embed([job_document_text(j) for j in jobs])
    job_ids = [j["id"] for j in jobs]

    ndcgs, ps, rs = [], [], []
    for i, cv in enumerate(cvs):
        relmap = eval_map.get(cv["id"], {})
        if not any(r > 0 for r in relmap.values()):
            continue
        sims = job_vecs @ cv_vecs[i]
        ranking = [job_ids[j] for j in np.argsort(-sims)]
        ndcgs.append(ndcg_at_k(ranking, relmap, TOP_K))
        pos = {d: r for d, r in relmap.items() if r > 0}
        ps.append(precision_at_k(ranking, pos, TOP_K))
        rs.append(recall_at_k(ranking, pos, TOP_K))

    out = {
        "experiment": "EXP-014b JobBERT (jjzha/jobbert-base-cased) domain-encoder dense baseline (RQ1)",
        "model": MODEL, "hidden": 768, "protocol": "zero-shot mean-pooled embeddings of the SAME doc texts as the semantic channel; cosine rank; graded nDCG@5",
        "n_resumes_scored": len(ndcgs), "n_jobs": len(jobs),
        "jobbert_ndcg_at_5_mean": round(float(np.mean(ndcgs)), 6),
        "jobbert_ndcg_at_5_ci": bootstrap_ci(ndcgs, n_boot=2000),
        "jobbert_p_at_5_mean": round(float(np.mean(ps)), 6),
        "jobbert_r_at_5_mean": round(float(np.mean(rs)), 6),
        "reference": {"semantic_MiniLM_bi_encoder": 0.878, "fixed_composite": 0.949, "lambdamart": 0.963},
        "interpretation": (
            "Domain encoder (JobBERT) as a zero-shot dense baseline vs the general MiniLM bi-encoder. "
            "Report honestly whether the domain encoder beats MiniLM/composite; if it wins on raw nDCG, "
            "that is a valid negative result and the paper's contribution rests on decomposition/calibration."
        ),
    }
    outdir = REPO / "research" / "results"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "jobbert_baseline.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
