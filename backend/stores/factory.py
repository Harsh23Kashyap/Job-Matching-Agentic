from typing import Any

from config import Settings
from stores.chroma_store import ChromaVectorStore

VectorStore = Any


def create_store(
    settings: Settings,
    collection_name: str,
    *,
    collection_suffix: str = "",
    chroma_space: str = "cosine",
) -> VectorStore:
    backend = settings.vector_store.lower()
    name = f"{collection_name}{collection_suffix}" if collection_suffix else collection_name
    if backend == "qdrant":
        from stores.qdrant_store import QdrantVectorStore

        settings.qdrant_persist_dir.mkdir(parents=True, exist_ok=True)
        return QdrantVectorStore(
            persist_dir=str(settings.qdrant_persist_dir),
            collection_name=name,
            url=settings.qdrant_url or None,
        )
    if backend != "chroma":
        raise ValueError(f"Unsupported vector_store: {settings.vector_store}")
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    return ChromaVectorStore(
        persist_dir=str(settings.chroma_persist_dir),
        collection_name=name,
        space=chroma_space,
    )
