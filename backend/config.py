from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    repo_root: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = repo_root / "data"
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_persist_dir: Path = Path(__file__).resolve().parent / "chroma_db"
    rrf_k: int = 60
    host: str = "0.0.0.0"
    port: int = 8000
    read_only: bool = False

    @property
    def cvs_path(self) -> Path:
        return self.data_dir / "cvs.json"

    @property
    def jobs_path(self) -> Path:
        return self.data_dir / "jobs.json"
