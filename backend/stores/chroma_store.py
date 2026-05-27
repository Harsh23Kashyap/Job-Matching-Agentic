import chromadb
import numpy as np

from stores.base import SearchHit


def _flatten_metadata(metadata: dict) -> dict:
    flat: dict = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            flat[key] = ", ".join(str(v) for v in value)
        else:
            flat[key] = value
    return flat


class ChromaVectorStore:
    def __init__(self, persist_dir: str, collection_name: str) -> None:
        self.collection_name = collection_name
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def upsert(self, entity_id: str, vector: np.ndarray, metadata: dict) -> None:
        self._collection.upsert(
            ids=[entity_id],
            embeddings=[vector.tolist()],
            metadatas=[_flatten_metadata(metadata)],
        )

    def search(self, query_vector: np.ndarray, k: int) -> list[SearchHit]:
        if self._collection.count() == 0:
            return []
        k = min(k, self._collection.count())
        results = self._collection.query(query_embeddings=[query_vector.tolist()], n_results=k)
        hits: list[SearchHit] = []
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        for entity_id, distance, metadata in zip(ids, distances, metadatas):
            hits.append(SearchHit(entity_id=entity_id, distance=float(distance), metadata=metadata or {}))
        return hits

    def delete(self, entity_id: str) -> None:
        self._collection.delete(ids=[entity_id])

    def count(self) -> int:
        return int(self._collection.count())
