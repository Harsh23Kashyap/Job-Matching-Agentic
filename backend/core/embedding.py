import numpy as np
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None
_model_name: str | None = None
_skill_cache: dict[str, np.ndarray] = {}


def get_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    global _model, _model_name
    if _model is None or _model_name != model_name:
        _model = SentenceTransformer(model_name)
        _model_name = model_name
        _skill_cache.clear()
    return _model


def embed_text(text: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    model = get_model(model_name)
    vector = model.encode(text, normalize_embeddings=False)
    return np.asarray(vector, dtype=np.float32)


def embed_skill(skill: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    key = skill.strip().lower()
    if key not in _skill_cache:
        _skill_cache[key] = embed_text(key, model_name=model_name)
    return _skill_cache[key]


def reset_embedding_cache() -> None:
    global _model, _model_name
    _model = None
    _model_name = None
    _skill_cache.clear()
