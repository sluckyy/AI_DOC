"""Speech recognition configuration for the browser (N-1, N-3, N-8, N-9).

Recognition runs in the browser against Azure AI Speech so audio never passes
through the API. The browser needs a short-lived authorisation token, never the
key: the key stays on the server and this module trades it for a ten-minute
token. `browser` falls back to the Web Speech API when no key is configured.

Endpointing is a deployment parameter (N-3): the segmentation silence that ends
a turn is `silence_end_of_turn_ms` from the parameters register, longer for the
older register, never the vendor default that truncates slow speakers.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

LOW_CONFIDENCE_DEFAULT = 0.6


@dataclass
class RecognitionConfig:
    stt_provider: str                   # azure | browser
    region: str | None
    bcp47: str
    silence_end_of_turn_ms: int
    initial_silence_timeout_ms: int
    low_confidence_threshold: float
    token: str | None = None
    expires_in_s: int | None = None
    languages: dict[str, str] = field(default_factory=dict)
    note: str = ""

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class TokenCache:
    def __init__(self) -> None:
        self.token: str | None = None
        self.fetched_at = 0.0

    def get(self, key: str, region: str) -> tuple[str, int]:
        """Azure speech tokens live ten minutes; refresh after nine."""
        if self.token and time.time() - self.fetched_at < 9 * 60:
            return self.token, int(10 * 60 - (time.time() - self.fetched_at))
        import httpx

        r = httpx.post(f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken",
                       headers={"Ocp-Apim-Subscription-Key": key, "Content-Length": "0"}, timeout=10)
        r.raise_for_status()
        self.token = r.text
        self.fetched_at = time.time()
        return self.token, 10 * 60


_cache = TokenCache()


def stt_provider_name() -> str:
    """STT_PROVIDER=azure|browser|auto (default auto: azure when a Speech key exists)."""
    p = os.getenv("STT_PROVIDER", "auto").lower()
    if p == "auto":
        return "azure" if os.getenv("AZURE_SPEECH_KEY") else "browser"
    return p


def recognition_config(language: str, register: str, parameters, bcp47_by_language: dict[str, str]) -> RecognitionConfig:
    silence = parameters.silence_end_of_turn_ms
    by_register = getattr(parameters, "silence_end_of_turn_ms_by_register", {}) or {}
    silence = int(by_register.get(register, silence))
    cfg = RecognitionConfig(
        stt_provider=stt_provider_name(), region=os.getenv("AZURE_SPEECH_REGION") or None,
        bcp47=bcp47_by_language.get(language, "en-AU"), silence_end_of_turn_ms=silence,
        initial_silence_timeout_ms=int(getattr(parameters, "initial_silence_timeout_ms", 8000) or 8000),
        low_confidence_threshold=float(getattr(parameters, "asr_low_confidence_threshold", LOW_CONFIDENCE_DEFAULT) or LOW_CONFIDENCE_DEFAULT),
        languages=bcp47_by_language,
    )
    if cfg.stt_provider == "azure":
        key = os.getenv("AZURE_SPEECH_KEY", "")
        if not key or not cfg.region:
            cfg.stt_provider = "browser"
            cfg.note = "STT_PROVIDER is azure but AZURE_SPEECH_KEY or AZURE_SPEECH_REGION is missing; using the browser recogniser"
            return cfg
        try:
            cfg.token, cfg.expires_in_s = _cache.get(key, cfg.region)
        except Exception as exc:  # the token service is down: degrade to the browser path rather than stop the interview (N-20)
            cfg.stt_provider = "browser"
            cfg.note = f"speech token unavailable ({type(exc).__name__}); using the browser recogniser"
    return cfg
