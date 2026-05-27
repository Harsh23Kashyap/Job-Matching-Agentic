import uuid
from typing import Any

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from stores.base import SearchHit

_POINT_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
_DEFAULT_VECTOR_SIZE = 384

# Embedded Qdrant (path=...) allows only one client per storage directory.
# Bootstrap opens separate candidate/job collections on the same path, so reuse one client.
_CLIENTS: dict[str, QdrantClient] = {}


def get_qdrant_client(*, persist_dir: str | None = None, url: str | None = None) -> QdrantClient:
    if url:
        key = f"url:{url.rstrip('/')}"
        if key not in _CLIENTS:
            _CLIENTS[key] = QdrantClient(url=url)
        return _CLIENTS[key]
    if not persist_dir:
        raise ValueError("persist_dir or url is required")
    key = f"path:{persist_dir}"
    if key not in _CLIENTS:
        _CLIENTS[key] = QdrantClient(path=persist_dir)
    return _CLIENTS[key]


def reset_qdrant_clients_for_tests() -> None:
    """Close cached clients (tests only)."""
    for client in _CLIENTS.values():
        close = getattr(client, "close", None)
        if callable(close):
            close()
    _CLIENTS.clear()


def _flatten_metadata(metadata: dict) -> dict:
    flat: dict[str, Any] = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            flat[key] = ", ".join(str(v) for v in value)
        elif value is None:
            flat[key] = ""
        else:
            flat[key] = value
    return flat


def _point_id(entity_id: str) -> str:
    return str(uuid.uuid5(_POINT_NAMESPACE, entity_id))


class QdrantVectorStore:
    def __init__(
        self,
        persist_dir: str,
        collection_name: str,
        *,
        url: str | None = None,
    ) -> None:
        self.collection_name = collection_name
        self._client = get_qdrant_client(persist_dir=persist_dir, url=url)
        self._vector_size = _DEFAULT_VECTOR_SIZE
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        if self._client.collection_exists(self.collection_name):
            info = self._client.get_collection(self.collection_name)
            params = info.config.params.vectors
            if isinstance(params, dict):
                self._vector_size = next(iter(params.values())).size
            else:
                self._vector_size = params.size
            return
        self._client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self._vector_size, distance=Distance.COSINE),
        )

    def upsert(self, entity_id: str, vector: np.ndarray, metadata: dict) -> None:
        dim = int(vector.shape[0])
        if dim != self._vector_size:
            if self.count() == 0 and not self._client.collection_exists(self.collection_name):
                self._vector_size = dim
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
                )
            elif dim != self._vector_size:
                raise ValueError(f"Vector dimension {dim} does not match collection size {self._vector_size}")

        payload = _flatten_metadata({**metadata, "entity_id": entity_id})
        point = PointStruct(
            id=_point_id(entity_id),
            vector=vector.tolist(),
            payload=payload,
        )
        self._client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, query_vector: np.ndarray, k: int) -> list[SearchHit]:
        if self.count() == 0:
            return []
        k = min(k, self.count())
        results = self._client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=k,
            with_payload=True,
        )
        hits: list[SearchHit] = []
        for point in results.points:
            payload = dict(point.payload or {})
            entity_id = str(payload.pop("entity_id", point.id))
            score = float(point.score or 0.0)
            distance = max(0.0, 1.0 - score)
            hits.append(SearchHit(entity_id=entity_id, distance=distance, metadata=payload))
        return hits

    def delete(self, entity_id: str) -> None:
        self._client.delete(
            collection_name=self.collection_name,
            points_selector=[_point_id(entity_id)],
        )

    def count(self) -> int:
        if not self._client.collection_exists(self.collection_name):
            return 0
        return int(self._client.count(collection_name=self.collection_name, exact=True).count)
