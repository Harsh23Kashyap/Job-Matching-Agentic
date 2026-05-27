from config import Settings
from stores.chroma_store import ChromaVectorStore


def create_store(settings: Settings, collection_name: str) -> ChromaVectorStore:
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    return ChromaVectorStore(
        persist_dir=str(settings.chroma_persist_dir),
        collection_name=collection_name,
    )
