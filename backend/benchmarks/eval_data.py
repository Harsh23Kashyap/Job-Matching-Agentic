"""Load eval corpus and build benchmark snapshots."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.embedding import embed_text


def load_eval_labels(eval_path: str | Path) -> dict[str, dict[str, int]]:
    with open(eval_path, encoding="utf-8") as f:
        payload = json.load(f)
    labels = payload.get("labels", payload)
    query_to_relevance: dict[str, dict[str, int]] = defaultdict(dict)
    for item in labels:
        qid = item["query_id"]
        doc_id = item["doc_id"]
        rel = int(item["relevance"])
        if rel < 0:
            continue
        existing = query_to_relevance[qid].get(doc_id, 0)
        query_to_relevance[qid][doc_id] = max(existing, rel)
    return dict(query_to_relevance)


def cv_to_snapshot(cv: dict, model_name: str) -> CandidateSnapshot:
    doc = resume_document_text(cv)
    doc_hash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
    emb = embed_text(doc, model_name=model_name).tolist()
    return CandidateSnapshot(
        id=cv["id"],
        name=cv.get("name", ""),
        skills=list(cv.get("skills", [])),
        experience_years=float(cv.get("experience_years", 0)),
        remote_preference=bool(cv.get("remote_preference", False)),
        preferred_salary=cv.get("preferred_salary"),
        summary=str(cv.get("summary", "")),
        version=1,
        document_text_hash=doc_hash,
        embedding=emb,
    )


def job_to_snapshot(job: dict, model_name: str) -> JobSnapshot:
    doc = job_document_text(job)
    doc_hash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
    emb = embed_text(doc, model_name=model_name).tolist()
    return JobSnapshot(
        id=job["id"],
        title=job.get("title", ""),
        required_skills=list(job.get("required_skills", [])),
        preferred_skills=list(job.get("preferred_skills", [])),
        required_experience=int(job.get("required_experience", 0)),
        remote_policy=bool(job.get("remote_policy", False)),
        budget=job.get("budget"),
        description=str(job.get("description", "")),
        version=1,
        document_text_hash=doc_hash,
        embedding=emb,
    )
