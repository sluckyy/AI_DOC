import os

import pytest

os.environ.setdefault("CONTENT_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "..", "content"))

from app.content.loader import load_bundle  # noqa: E402


@pytest.fixture(scope="session")
def bundle():
    return load_bundle()
