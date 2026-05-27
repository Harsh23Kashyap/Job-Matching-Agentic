"""Tests for synthetic research dataset generation."""
from __future__ import annotations

import json

from benchmarks.synthetic_dataset.generator import SyntheticDatasetConfig, generate_dataset, write_dataset
from benchmarks.synthetic_dataset.roles import ROLES, label_pair


def test_generate_default_counts():
    config = SyntheticDatasetConfig(num_candidates=100, num_jobs=50, seed=7)
    dataset = generate_dataset(config)
    assert len(dataset["candidates"]) == 100
    assert len(dataset["jobs"]) == 50
    assert len(dataset["eval_pairs"]["labels"]) == 5000
    assert dataset["manifest"]["relevance_scale"] == "0-3"


def test_all_roles_represented():
    dataset = generate_dataset(SyntheticDatasetConfig(num_candidates=80, num_jobs=40, seed=1))
    cand_roles = {c["role"] for c in dataset["candidates"]}
    job_roles = {j["role"] for j in dataset["jobs"]}
    assert cand_roles == set(ROLES)
    assert job_roles == set(ROLES)


def test_labels_have_rationale_and_valid_relevance():
    dataset = generate_dataset(SyntheticDatasetConfig(num_candidates=16, num_jobs=8, seed=3))
    for label in dataset["eval_pairs"]["labels"]:
        assert "rationale" in label
        assert label["rationale"]
        assert 0 <= label["relevance"] <= 3


def test_label_pair_deterministic():
    candidate = {
        "role": "backend",
        "skills": ["Python", "PostgreSQL", "Microservices", "Kafka"],
        "experience_years": 5,
        "remote_preference": True,
        "preferred_salary": 130000,
    }
    job = {
        "role": "backend",
        "required_skills": ["Python", "PostgreSQL", "REST APIs"],
        "required_experience": 3,
        "remote_policy": True,
        "budget": 140000,
    }
    rel, rationale = label_pair(candidate, job)
    assert rel >= 2
    assert "Skills:" in rationale


def test_write_dataset(tmp_path):
    dataset = generate_dataset(SyntheticDatasetConfig(num_candidates=8, num_jobs=4, seed=5))
    paths = write_dataset(tmp_path, dataset)
    assert paths["candidates"].is_file()
    payload = json.loads(paths["eval_pairs"].read_text(encoding="utf-8"))
    assert payload["relevance_scale"] == "0-3"
    assert len(payload["labels"]) == 32
