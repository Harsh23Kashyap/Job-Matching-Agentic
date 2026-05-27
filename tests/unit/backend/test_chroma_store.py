import numpy as np

from stores.chroma_store import ChromaVectorStore


def test_chroma_upsert_and_search(tmp_path):
    store = ChromaVectorStore(str(tmp_path / "chroma"), "test_collection")
    vec = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    store.upsert("entity_1", vec, {"id": "entity_1", "name": "Test", "skills": ["Python"]})
    hits = store.search(vec, k=1)
    assert len(hits) == 1
    assert hits[0].entity_id == "entity_1"


def test_chroma_empty_search():
    store = ChromaVectorStore("/tmp/chroma_empty_test_unused", "empty_col_test")
    # fresh collection with no upserts - count may be 0
    if store.count() == 0:
        hits = store.search(np.array([1.0, 0.0]), k=5)
        assert hits == []
