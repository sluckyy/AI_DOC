"""Wording: how Dr Sam says what the controller has decided to say.

`template` uses the stored phrasing verbatim (auditable, offline). `azure_openai`
may re-word for register and language but the output is checked against P5, P7
and the stand-down and diagnosis lists, and falls back to the template on any hit.
"""
from __future__ import annotations

import os
import re
from typing import Protocol

from app.content.checks import ANYTHING_ELSE, polarity_ok
from app.process.rules import DIAGNOSIS_WORDS, STAND_DOWN

REGISTERS = {
    "patient": "plain language, second person, one question per turn, no jargon, no reassurance, no exclamation marks",
    "older": "slower, shorter sentences, more repetition, patient with tangents, no reassurance",
    "clinician": "concise, structured, no reassurance talk",
}


class WordingProvider(Protocol):
    def word(self, template_text: str, *, register: str, language: str, intent: str) -> str: ...


def passes_guardrails(text: str) -> bool:
    if ANYTHING_ELSE.search(text):
        return False
    if "?" in text and not polarity_ok(text):
        return False
    return not any(re.search(p, text, re.I) for p in STAND_DOWN + DIAGNOSIS_WORDS)


class TemplateWording:
    name = "template"

    def word(self, template_text: str, *, register: str = "patient", language: str = "en", intent: str = "") -> str:
        return template_text


class AzureOpenAIWording:
    name = "azure_openai"

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        self.key = os.getenv("AZURE_OPENAI_KEY", "")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_PERSONA", "")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

    def word(self, template_text: str, *, register: str = "patient", language: str = "en", intent: str = "") -> str:
        # N-30: stored wording is delivered verbatim. Generation is permitted only to render a
        # stored line in another language while authored phrasings do not yet exist, and the
        # turn is then marked as a machine translation, not validated (F-32, N-13).
        if not (self.endpoint and self.key and self.deployment) or language == "en":
            return template_text
        if os.getenv("ALLOW_MACHINE_TRANSLATION", "false").lower() != "true":
            return template_text
        import httpx

        system = (
            "You are a translator for Dr Sam, an AI history-taking assistant (they/them). Translate the given line into "
            f"{language} keeping exactly the same meaning and asking exactly the same thing; register: {REGISTERS.get(register, register)}. "
            "Rules: say 'something else' never 'anything else'; never phrase a question toward the negative; never reassure; "
            "never suggest a diagnosis or that the person can wait; one question at most. Return the line only."
        )
        body = {"messages": [{"role": "system", "content": system}, {"role": "user", "content": template_text}], "temperature": 0.2}
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        try:
            r = httpx.post(url, headers={"api-key": self.key}, json=body, timeout=20)
            r.raise_for_status()
            out = r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return template_text
        return out if (language != "en" or passes_guardrails(out)) else template_text


def get_wording_provider() -> WordingProvider:
    if os.getenv("MODEL_PROVIDER", "fake").lower() == "azure_openai":
        return AzureOpenAIWording()
    return TemplateWording()
