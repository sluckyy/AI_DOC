"""Emotional tone classification of the person's most recent turn (D-46).

The label changes pace, wording and expression only. It never enters gating,
red-flag, escalation or handover clinical content, and is stored only with consent.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Protocol

LABELS = ["settled", "anxious", "in_pain", "frustrated", "low", "confused", "embarrassed", "distressed"]

CUES = {
    "distressed": [r"\bcan't cope\b", r"\bcan't go on\b", r"\bend it\b", r"\bkill myself\b", r"\bcrying\b", r"\bterrified\b"],
    "anxious": [r"\bis it serious\b", r"\bworried\b", r"\bscared\b", r"\bfrightened\b", r"\bpanick", r"\bsorry\b.*\bsorry\b", r"\bwhat if\b"],
    "in_pain": [r"\bagony\b", r"\bit really hurts\b", r"\bcan't stand it\b", r"\bkilling me\b", r"\bso much pain\b", r"\bouch\b"],
    "frustrated": [r"\bwaited\b", r"\bwaiting for hours\b", r"\bnobody\b", r"\bridiculous\b", r"\bfed up\b", r"\bagain\b.*\bagain\b"],
    "low": [r"\bwhat's the point\b", r"\bdon't care\b", r"\bhopeless\b", r"\bnothing helps\b", r"\btired of it all\b"],
    "confused": [r"\bwhat did you ask\b", r"\bI don't understand\b", r"\bwhat do you mean\b", r"\bsay that again\b"],
    "embarrassed": [r"\bprobably nothing\b", r"\bembarrass", r"\bawkward\b", r"\bdown there\b", r"\bsilly\b"],
}


@dataclass
class Tone:
    label: str
    confidence: float


class ToneProvider(Protocol):
    def classify(self, text: str, prosody: dict | None) -> Tone: ...


class RulesTone:
    name = "rules"

    def classify(self, text: str, prosody: dict | None = None) -> Tone:
        t = text.lower()
        for label in ("distressed", "in_pain", "anxious", "frustrated", "low", "confused", "embarrassed"):
            hits = sum(1 for p in CUES[label] if re.search(p, t))
            if hits:
                conf = min(0.95, 0.55 + 0.2 * hits)
                if prosody:
                    rate = prosody.get("words_per_minute") or 0
                    if label == "anxious" and rate > 170:
                        conf = min(0.95, conf + 0.1)
                    if label == "low" and 0 < rate < 90:
                        conf = min(0.95, conf + 0.1)
                return Tone(label, conf)
        return Tone("settled", 0.9)


def get_tone_provider() -> ToneProvider:
    # The Azure OpenAI tone classifier is a small prompt on the same deployment; the
    # rules classifier is used until that prompt has been reviewed. Both return the same shape.
    return RulesTone()
