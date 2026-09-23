"""Binds captured concepts to SNOMED CT-AU. Never emits ICD-10-AM (D-24).
`fake` returns stable placeholder ids; `fhir` queries a FHIR terminology server
($lookup / ValueSet $expand with a text filter) such as the NCTS Ontoserver."""
from __future__ import annotations

import hashlib
import os
from typing import Protocol


class TerminologyProvider(Protocol):
    def bind(self, term: str) -> dict: ...


class FakeTerminology:
    name = "fake"

    def bind(self, term: str) -> dict:
        digest = hashlib.sha1(term.lower().encode()).hexdigest()[:8]
        return {"system": "http://snomed.info/sct", "edition": "SNOMED CT-AU", "code": f"pending-{digest}", "display": term, "bound_by": "fake"}


class FhirTerminology:
    name = "fhir"

    def __init__(self) -> None:
        self.base = os.getenv("TERMINOLOGY_FHIR_BASE", "").rstrip("/")
        self.token = os.getenv("TERMINOLOGY_FHIR_TOKEN", "")

    def bind(self, term: str) -> dict:
        if not self.base:
            return FakeTerminology().bind(term)
        import httpx

        params = {"url": "http://snomed.info/sct?fhir_vs", "filter": term, "count": 1}
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            r = httpx.get(f"{self.base}/ValueSet/$expand", params=params, headers=headers, timeout=10)
            r.raise_for_status()
            contains = r.json().get("expansion", {}).get("contains", [])
        except Exception:
            return FakeTerminology().bind(term)
        if not contains:
            return {"system": "http://snomed.info/sct", "edition": "SNOMED CT-AU", "code": None, "display": term, "bound_by": "fhir:no-match"}
        c = contains[0]
        return {"system": c.get("system"), "edition": "SNOMED CT-AU", "code": c.get("code"), "display": c.get("display"), "bound_by": "fhir"}


def get_terminology_provider() -> TerminologyProvider:
    if os.getenv("TERMINOLOGY_PROVIDER", "fake").lower() == "fhir":
        return FhirTerminology()
    return FakeTerminology()
