import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


@pytest.fixture(scope="session")
def repo_root():
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def settings(tmp_path, repo_root):
    from config import Settings

    return Settings(
        repo_root=repo_root,
        data_dir=repo_root / "data",
        chroma_persist_dir=tmp_path / "chroma_db",
        sqlite_path=tmp_path / "app.db",
    )


@pytest.fixture
def system(settings):
    from bootstrap import create_system

    return create_system(settings)
