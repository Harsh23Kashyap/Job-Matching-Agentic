import numpy as np
import pytest

pytest.importorskip("qdrant_client")

from stores.qdrant_store import QdrantVectorStore, reset_qdrant_clients_for_tests


@pytest.fixture(autouse=True)
def _reset_qdrant_clients():
    yield
    reset_qdrant_clients_for_tests()


def test_qdrant_upsert_and_search(tmp_path):
    store = QdrantVectorStore(str(tmp_path / "qdrant"), "test_collection")
    vec = np.array([1.0, 0.0, 0.0] + [0.0] * 381, dtype=np.float32)
    store.upsert("entity_1", vec, {"id": "entity_1", "name": "Test", "required_skills": ["Python"]})
    hits = store.search(vec, k=1)
    assert len(hits) == 1
    assert hits[0].entity_id == "entity_1"


def test_qdrant_empty_search(tmp_path):
    store = QdrantVectorStore(str(tmp_path / "qdrant_empty"), "empty_col")
    if store.count() == 0:
        vec = np.zeros(384, dtype=np.float32)
        vec[0] = 1.0
        hits = store.search(vec, k=5)
        assert hits == []


def test_qdrant_two_collections_share_one_client(tmp_path):
    """Bootstrap opens candidate + job collections on the same persist path."""
    base = str(tmp_path / "shared")
    vec = np.zeros(384, dtype=np.float32)
    vec[0] = 1.0

    candidates = QdrantVectorStore(base, "candidates_collection")
    jobs = QdrantVectorStore(base, "jobs_collection")

    candidates.upsert("resume:1", vec, {"id": "resume:1", "name": "Alice"})
    jobs.upsert("job:1", vec, {"id": "job:1", "title": "Engineer"})

    assert candidates.count() == 1
    assert jobs.count() == 1
    assert candidates.search(vec, k=1)[0].entity_id == "resume:1"
    assert jobs.search(vec, k=1)[0].entity_id == "job:1"
