import numpy as np
import pytest

pytest.importorskip("qdrant_client")

from stores.qdrant_store import QdrantVectorStore


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
