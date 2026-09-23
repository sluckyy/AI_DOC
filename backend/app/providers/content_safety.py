"""Screens every spoken turn. `fake` passes everything; `azure` calls the Azure AI
Content Safety text endpoint and blocks on any severity >= the configured level.
Blocked turns are replaced by a deflection and logged."""
from __future__ import annotations

import os
from typing import Protocol


class ContentSafetyProvider(Protocol):
    def screen(self, text: str) -> tuple[bool, str]: ...


class FakeContentSafety:
    name = "fake"

    def screen(self, text: str) -> tuple[bool, str]:
        return True, "fake:pass"


class AzureContentSafety:
    name = "azure"

    def __init__(self) -> None:
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
        self.key = os.getenv("CONTENT_SAFETY_KEY", "")
        self.threshold = int(os.getenv("CONTENT_SAFETY_BLOCK_SEVERITY", "4"))

    def screen(self, text: str) -> tuple[bool, str]:
        if not (self.endpoint and self.key):
            return True, "azure:unconfigured"
        import httpx

        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
        try:
            r = httpx.post(url, headers={"Ocp-Apim-Subscription-Key": self.key}, json={"text": text}, timeout=10)
            r.raise_for_status()
            cats = r.json().get("categoriesAnalysis", [])
        except Exception as exc:
            return True, f"azure:error:{exc.__class__.__name__}"
        worst = max((c.get("severity", 0) for c in cats), default=0)
        return worst < self.threshold, f"azure:severity={worst}"


def get_content_safety_provider() -> ContentSafetyProvider:
    if os.getenv("CONTENT_SAFETY_PROVIDER", "fake").lower() == "azure":
        return AzureContentSafety()
    return FakeContentSafety()
