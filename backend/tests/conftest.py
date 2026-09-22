import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
os.environ.setdefault("CONTENT_DIR", str(ROOT / "content"))
os.environ["DATABASE_URL"] = "sqlite:///./test_aidoc.sqlite"
os.environ["MODEL_PROVIDER"] = "fake"
os.environ["TTS_PROVIDER"] = "fake"


@pytest.fixture(scope="session")
def bundle():
    from app.content.loader import load_bundle

    return load_bundle(ROOT / "content")


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from app.db import Base, engine
    from app.main import app

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
