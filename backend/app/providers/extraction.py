"""Slot extraction: turns the person's words into a slot value.

The controller decides which slots are outstanding and writes the values (P12);
the provider only proposes values with the supporting span. `rules` is
deterministic (synonym matching from the module YAML) and runs offline and in
tests. `azure_openai` asks the model for JSON and is validated against the slot's
option set before anything is written.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Protocol

from app.content.schema import Slot

CLOCK_RE = re.compile(
    r"\b(\d{1,2}(:\d{2})?\s*(am|pm|a\.m\.|p\.m\.|o'clock)|midnight|midday|noon|lunchtime|breakfast|dinner|tea time|dawn|first thing"
    r"|(this|in the|yesterday) (morning|afternoon|evening)|last night|bedtime"
    r"|\d{1,2}(:\d{2})?(?=\b[^\d]{0,30}\b(yesterday|this morning|last night|today|tonight|ago)))",
    re.I,
)
NUMBER_RE = re.compile(r"\b(\d{1,3})\b")
NEGATION_BEFORE = re.compile(r"\b(no|not|never|without|haven't|hasn't|didn't|don't|doesn't|isn't|wasn't|nor|any)\b(?:\s+\w+){0,3}\s*$", re.I)


@dataclass
class Proposal:
    slot_id: str
    value: object
    verbatim: str
    confidence: float


class ExtractionProvider(Protocol):
    def propose(self, slot: Slot, text: str, language: str, opportunistic: bool = False) -> Proposal | None: ...


def _contains(text: str, term: str) -> bool:
    return re.search(r"(?<![a-z])" + re.escape(term.lower()) + r"(?![a-z])", text) is not None


class RulesExtraction:
    name = "rules"

    BARE = {"yes", "no", "yeah", "yep", "nope", "nah", "none", "now"}

    def propose(self, slot: Slot, text: str, language: str = "en", opportunistic: bool = False) -> Proposal | None:
        """opportunistic=True is used when mining narrative the person gave before the slot was
        asked: bare yes/no tokens and one-word negatives are then ignored, because they
        answer whatever was asked at the time, not this slot."""
        t = " " + text.lower().strip() + " "
        vt = slot.value.type
        if vt == "yes_no":
            ex = slot.extraction
            if ex is None:
                return None
            no_terms = [x for x in ex.no_terms if not (opportunistic and x.lower() in self.BARE)]
            yes_terms = [x for x in ex.yes_terms if x.lower() not in self.BARE]
            no_hit = any(_contains(t, term) for term in no_terms)
            yes_hit = any(_contains(t, term) for term in yes_terms)
            if opportunistic and yes_hit and not no_hit:
                # narrative mining: "I haven't had any fever at all" names the feature to deny it
                for term in yes_terms:
                    m_ = re.search(r"(?<![a-z])" + re.escape(term.lower()) + r"(?![a-z])", t)
                    if m_ and NEGATION_BEFORE.search(t[max(0, m_.start() - 40):m_.start()]):
                        return Proposal(slot.id, "no", text.strip(), 0.7)
            bare_yes = (not opportunistic) and (_contains(t, "yes") or _contains(t, "yeah") or _contains(t, "yep"))
            bare_no = (not opportunistic) and (_contains(t, "no") or _contains(t, "nope") or _contains(t, "nah"))
            if no_hit or (bare_no and not yes_hit):
                return Proposal(slot.id, "no", text.strip(), 0.7)
            if yes_hit or bare_yes:
                return Proposal(slot.id, "yes", text.strip(), 0.7)
            return None
        if vt in ("enum", "set"):
            hits: list[str] = []
            for opt in slot.value.options:
                syns = [x for x in opt.synonyms if not (opportunistic and x.lower() in self.BARE)]
                if any(_contains(t, syn) for syn in syns) or (not opportunistic and _contains(t, opt.id.replace("_", " "))) or (opportunistic and opt.id not in ("none", "unsure") and _contains(t, opt.id.replace("_", " "))):
                    hits.append(opt.id)
            if not hits:
                return None
            if vt == "enum":
                # first option listed wins on ties, except 'unsure'/'none' which lose to a real value
                real = [h for h in hits if h not in ("unsure",)]
                return Proposal(slot.id, (real or hits)[0], text.strip(), 0.6 if len(hits) == 1 else 0.5)
            if "none" in hits and len(hits) > 1:
                hits = [h for h in hits if h != "none"]
            return Proposal(slot.id, sorted(set(hits)), text.strip(), 0.6)
        if vt == "clock_time":
            m = CLOCK_RE.search(text)
            if m:
                return Proposal(slot.id, m.group(0).strip(), text.strip(), 0.6)
            return None
        if vt == "number":
            m = NUMBER_RE.search(text)
            return Proposal(slot.id, int(m.group(1)), text.strip(), 0.6) if m else None
        if vt == "text":
            if len(text.strip()) < 2:
                return None
            return Proposal(slot.id, text.strip(), text.strip(), 0.5)
        return None


class AzureOpenAIExtraction:
    """JSON extraction through Azure OpenAI chat completions. Validated before use."""

    name = "azure_openai"

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        self.key = os.getenv("AZURE_OPENAI_KEY", "")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_PERSONA", "")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
        self.fallback = RulesExtraction()

    def propose(self, slot: Slot, text: str, language: str = "en", opportunistic: bool = False) -> Proposal | None:
        if not (self.endpoint and self.key and self.deployment):
            return self.fallback.propose(slot, text, language, opportunistic)
        import httpx

        options = [o.id for o in slot.value.options]
        system = (
            "You extract one structured value from a patient's words for a clinical history. "
            "Return JSON only: {\"value\": <value or null>, \"span\": <the patient's exact words that support it or null>}. "
            "Never infer beyond what was said. If the words do not answer the question, return null. "
            f"Slot intent: {slot.intent}. Value type: {slot.value.type}. "
            + (f"Allowed values: {options}. " if options else "")
            + ("For type set return a list of allowed values. " if slot.value.type == "set" else "")
            + ("For yes_no return 'yes' or 'no'. " if slot.value.type == "yes_no" else "")
            + f"The patient may speak {language}; the value must be in the allowed vocabulary, the span in the original language."
        )
        body = {
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": text}],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        try:
            r = httpx.post(url, headers={"api-key": self.key}, json=body, timeout=20)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            data = json.loads(content)
        except Exception:
            return self.fallback.propose(slot, text, language, opportunistic)
        value = data.get("value")
        if value in (None, "", []):
            return None
        if options:
            if slot.value.type == "set":
                value = [v for v in value if v in options] if isinstance(value, list) else []
                if not value:
                    return None
            elif value not in options:
                return None
        if slot.value.type == "yes_no" and value not in ("yes", "no"):
            return None
        return Proposal(slot.id, value, data.get("span") or text.strip(), 0.8)


def get_extraction_provider() -> ExtractionProvider:
    provider = os.getenv("MODEL_PROVIDER", "fake").lower()
    if provider == "azure_openai":
        return AzureOpenAIExtraction()
    return RulesExtraction()
