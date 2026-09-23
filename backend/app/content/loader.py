"""Loads the content layer from disk into a ContentBundle."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

from .schema import ContentBundle, ContextModule, Module, Parameters, Phrasings

DEFAULT_CONTENT_DIR = Path(__file__).resolve().parents[3] / "content"


def content_dir() -> Path:
    return Path(os.getenv("CONTENT_DIR", str(DEFAULT_CONTENT_DIR)))


def _read(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def content_mode() -> str:
    """simulation (default) loads grounded content; clinical refuses anything below reviewed (A9, C3, HAZ-8)."""
    if os.getenv("REQUIRE_REVIEWED_CONTENT", "false").lower() == "true":
        return "clinical"
    return os.getenv("CONTENT_MODE", "simulation").lower()


def load_bundle(root: Path | None = None, deployment: str | None = None) -> ContentBundle:
    root = root or content_dir()
    deployment = deployment or os.getenv("PARAMETERS_DEPLOYMENT", "sa_health_regional")
    modules: dict[str, Module] = {}
    disabled: dict[str, str] = {}
    mode = content_mode()
    paths = sorted((root / "modules").glob("*.yaml")) + sorted((root / "shared").glob("*_section*.yaml")) + sorted((root / "shared").glob("gating.yaml"))
    for path in paths:
        m = Module.model_validate(_read(path))
        rs = m.effective_review_status
        if rs in ("first_draft", "blocked"):
            disabled[m.module] = f"{m.version} ({rs})"       # A9: never loads
            continue
        if mode == "clinical" and rs != "reviewed":
            raise RuntimeError(f"HAZ-8 (C3): module {m.module} v{m.version} is {rs}, below reviewed; refusing to start in clinical mode")
        modules[m.module] = m
    content_version = (root / "CONTENT_VERSION").read_text().strip() if (root / "CONTENT_VERSION").exists() else "0.0.0"
    prohibited = _read(root / "shared" / "prohibited_phrases.yaml").get("phrases", []) if (root / "shared" / "prohibited_phrases.yaml").exists() else []
    context = ContextModule.model_validate(_read(root / "context.yaml"))
    parameters = Parameters.model_validate(_read(root / "parameters" / f"{deployment}.yaml"))
    phrasings = Phrasings.model_validate(_read(root / "phrasings" / "invitations.yaml"))
    lexicon = [t.lower() for t in _read(root / "lexicon" / "symptoms.yaml").get("terms", [])]
    scripts = _read(root / "scripts" / "fixed.yaml")
    versions = {
        "content_version": content_version,
        "content_mode": mode,
        "content": {name: m.version for name, m in modules.items()},
        "review_status": {name: m.effective_review_status for name, m in modules.items()},
        "context": context.version,
        "parameters": f"{parameters.deployment}@{parameters.version}",
        "disabled_modules": disabled,
    }
    return ContentBundle(
        modules=modules, context=context, parameters=parameters, phrasings=phrasings,
        lexicon=lexicon, scripts=scripts, versions=versions, prohibited=prohibited,
    )


@lru_cache(maxsize=1)
def get_bundle() -> ContentBundle:
    return load_bundle()


def reload_bundle() -> ContentBundle:
    """D-51: content is reloadable at runtime; a failed load leaves the previous bundle active."""
    fresh = load_bundle()
    get_bundle.cache_clear()
    get_bundle()  # warm
    return fresh
