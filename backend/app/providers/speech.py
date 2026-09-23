"""Text-to-speech. `fake` returns no audio and a synthetic viseme timeline, and the
browser speaks the caption with its own synthesis. `azure_rest` synthesises MP3
through the Azure AI Speech REST endpoint; viseme events need the Speech SDK and
are estimated from text until that is wired (phase 1 follow-up).
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from html import escape
from typing import Protocol

VOWELS = set("aeiouy")


@dataclass
class Synthesis:
    audio: bytes | None
    content_type: str
    visemes: list[dict] = field(default_factory=list)
    duration_ms: int = 0
    cache_key: str = ""


def estimate_visemes(text: str, ms_per_char: int = 62) -> tuple[list[dict], int]:
    """A crude mouth-shape timeline: one event per character group, used for lip sync
    when real viseme events are unavailable. Viseme ids: 0 silence, 1 open, 2 wide, 3 round, 4 closed."""
    visemes: list[dict] = []
    t = 0
    for ch in text.lower():
        if ch.isspace() or ch in ",.;:!?":
            vis = 0
            dt = ms_per_char
        elif ch in "aeiouy":
            vis = {"a": 1, "e": 2, "i": 2, "o": 3, "u": 3, "y": 2}[ch]
            dt = ms_per_char + 20
        elif ch in "mbp":
            vis = 4
            dt = ms_per_char
        else:
            vis = 1
            dt = ms_per_char - 10
        if not visemes or visemes[-1]["viseme_id"] != vis:
            visemes.append({"offset_ms": t, "viseme_id": vis})
        t += dt
    visemes.append({"offset_ms": t, "viseme_id": 0})
    return visemes, t


class SpeechProvider(Protocol):
    def synthesise(self, text: str, *, language: str, rate: str, pitch: str) -> Synthesis: ...


class FakeSpeech:
    name = "fake"

    def synthesise(self, text: str, *, language: str = "en", rate: str = "-8%", pitch: str = "0%") -> Synthesis:
        visemes, dur = estimate_visemes(text)
        return Synthesis(audio=None, content_type="", visemes=visemes, duration_ms=dur, cache_key="")


LOCALES = {"en": "en-AU", "vi": "vi-VN", "it": "it-IT", "fr": "fr-FR", "ms": "ms-MY", "hi": "hi-IN"}


class AzureRestSpeech:
    name = "azure_rest"

    def __init__(self) -> None:
        self.key = os.getenv("AZURE_SPEECH_KEY", "")
        self.region = os.getenv("AZURE_SPEECH_REGION", "australiaeast")
        self.voice = os.getenv("AZURE_SPEECH_VOICE", "")
        self.voices_by_lang = {
            k: v for k, v in (pair.split("=") for pair in os.getenv("AZURE_SPEECH_VOICES", "").split(",") if "=" in pair)
        }
        self.cache: dict[str, Synthesis] = {}

    def synthesise(self, text: str, *, language: str = "en", rate: str = "-8%", pitch: str = "0%") -> Synthesis:
        voice = self.voices_by_lang.get(language) or self.voice
        if not (self.key and voice):
            return FakeSpeech().synthesise(text, language=language, rate=rate, pitch=pitch)
        locale = LOCALES.get(language, "en-AU")
        ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{locale}">'
            f'<voice name="{voice}"><prosody rate="{rate}" pitch="{pitch}">{escape(text)}</prosody></voice></speak>'
        )
        key = hashlib.sha256(ssml.encode()).hexdigest()
        if key in self.cache:
            return self.cache[key]
        import httpx

        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "aidoc-drsam",
        }
        try:
            r = httpx.post(url, headers=headers, content=ssml.encode("utf-8"), timeout=30)
            r.raise_for_status()
        except Exception:
            return FakeSpeech().synthesise(text, language=language, rate=rate, pitch=pitch)
        visemes, dur = estimate_visemes(text)
        syn = Synthesis(audio=r.content, content_type="audio/mpeg", visemes=visemes, duration_ms=dur, cache_key=key)
        self.cache[key] = syn
        return syn


def get_speech_provider() -> SpeechProvider:
    provider = os.getenv("TTS_PROVIDER", "fake").lower()
    if provider in ("azure", "azure_rest"):
        return AzureRestSpeech()
    return FakeSpeech()


_WORD = re.compile(r"\w+")


def word_count(text: str) -> int:
    return len(_WORD.findall(text))
