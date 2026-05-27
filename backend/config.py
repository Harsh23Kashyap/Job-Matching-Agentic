from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent
_ENV_FILE = _BACKEND_DIR / ".env"

# Local .env must win over stale shell exports (common when OPENAI_API_KEY was set in the terminal).
if _ENV_FILE.is_file():
    load_dotenv(_ENV_FILE, override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    repo_root: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = repo_root / "data"
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_persist_dir: Path = Path(__file__).resolve().parent / "chroma_db"
    vector_store: str = "chroma"
    qdrant_persist_dir: Path = Path(__file__).resolve().parent / "qdrant_db"
    sqlite_path: Path = Path(__file__).resolve().parent / "app.db"
    session_secret: str = "dev-change-me"
    parser_backend: str = "json"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    rrf_k: int = 60
    host: str = "0.0.0.0"
    port: int = 8001
    read_only: bool = False
    seed_demo: bool = True
    demo_mode: bool = True
    enable_cross_encoder_rerank: bool = False
    cross_encoder_rerank_pool: int = 20

    @property
    def cvs_path(self) -> Path:
        return self.data_dir / "cvs.json"

    @property
    def jobs_path(self) -> Path:
        return self.data_dir / "jobs.json"

    @property
    def models_dir(self) -> Path:
        return self.data_dir / "models"

    @property
    def fusion_model_path(self) -> Path:
        return self.models_dir / "fusion.json"

    @property
    def calibration_model_path(self) -> Path:
        return self.models_dir / "calibration.json"
