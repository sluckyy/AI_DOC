"""Azure recognition in the browser (N-1, N-3, N-8, N-9): the API hands out configuration and a token, never the key;
endpointing comes from the parameters and lengthens for the older register; per-utterance confidence travels with the
turn into the transcript layer and the handover; a language switch during the capability check is reported so the
recogniser restarts in the new language."""
import pytest

from app.providers import recognition


def test_speech_config_falls_back_to_the_browser_without_a_key(client, monkeypatch):
    monkeypatch.delenv("AZURE_SPEECH_KEY", raising=False)
    monkeypatch.delenv("STT_PROVIDER", raising=False)
    r = client.get("/speech/config?language=vi&register=older")
    assert r.status_code == 200, r.text
    cfg = r.json()
    assert cfg["stt_provider"] == "browser" and cfg["token"] is None
    assert cfg["bcp47"] == "vi-VN"
    assert cfg["silence_end_of_turn_ms"] == 1800, "the older register waits longer before ending a turn (N-3)"
    assert cfg["low_confidence_threshold"] == 0.6
    assert set(cfg["languages"]) == {"en", "vi", "it", "fr", "ms", "hi"}
    assert client.get("/speech/token").status_code == 404


def test_speech_config_issues_a_token_and_never_the_key(client, monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", "not-a-real-key")
    monkeypatch.setenv("AZURE_SPEECH_REGION", "australiaeast")
    monkeypatch.delenv("STT_PROVIDER", raising=False)
    calls = []

    def fake_get(self, key, region):
        calls.append((key, region))
        return "tok-123", 600

    monkeypatch.setattr(recognition.TokenCache, "get", fake_get)
    r = client.get("/speech/config?language=en&register=patient")
    cfg = r.json()
    assert cfg["stt_provider"] == "azure" and cfg["token"] == "tok-123" and cfg["region"] == "australiaeast"
    assert cfg["silence_end_of_turn_ms"] == 1200 and cfg["initial_silence_timeout_ms"] == 8000
    assert "not-a-real-key" not in r.text
    assert calls == [("not-a-real-key", "australiaeast")]
    t = client.get("/speech/token").json()
    assert t["token"] == "tok-123" and t["expires_in_s"] == 600


def test_token_service_failure_degrades_to_the_browser(client, monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setenv("AZURE_SPEECH_REGION", "australiaeast")

    def boom(self, key, region):
        raise ConnectionError("down")

    monkeypatch.setattr(recognition.TokenCache, "get", boom)
    cfg = client.get("/speech/config").json()
    assert cfg["stt_provider"] == "browser" and "token unavailable" in cfg["note"]


def test_confidence_travels_with_the_turn_into_the_handover(client):
    r = client.post("/conversations", json={"setting": "ed", "language": "en"})
    cid = r.json()["conversation_id"]
    asr = {"provider": "azure", "confidence": 0.41, "language": "en-AU", "duration_ms": 2100, "segments": 1, "endpoint_silence_ms": 1200,
           "nbest": [{"text": "Yes.", "confidence": 0.41}, {"text": "Yet.", "confidence": 0.3}]}
    client.post(f"/conversations/{cid}/turns", json={"transcript": "Yes.", "asr": asr})
    for line in ["Yes I can hear you.", "English is fine.", "No, just me."]:
        client.post(f"/conversations/{cid}/turns", json={"transcript": line, "asr": {"provider": "azure", "confidence": 0.93, "language": "en-AU"}})
    client.post(f"/conversations/{cid}/turns", json={"transcript": "I've got a tight pain in my chest right now."})   # typed
    conv = client.get(f"/conversations/{cid}").json()
    person = [t for t in conv["turns"] if t["role"] == "person"]
    assert person[0]["asr"]["confidence"] == 0.41 and person[0]["asr"]["nbest"][1]["text"] == "Yet."
    assert person[-1]["asr"] == {"provider": "typed", "confidence": None}
    # drive to the end so a handover exists
    for line in ["No.", "No.", "No.", "No.", "Yes that's right."]:
        rr = client.post(f"/conversations/{cid}/turns", json={"transcript": line, "asr": {"provider": "azure", "confidence": 0.88, "language": "en-AU"}})
        if rr.status_code != 200 or rr.json()["phase"] == "ended":
            break
    h = client.get(f"/conversations/{cid}/handover")
    assert h.status_code == 200, h.text
    meta = h.json()["metadata"]["asr"]
    assert meta["spoken_turns"] >= 4 and meta["typed_turns"] == 1 and meta["min_confidence"] == 0.41
    assert meta["low_confidence_turns"][0]["confidence"] == 0.41 and meta["languages"] == ["en-AU"]
    narrative = " ".join(h.json()["narrative"])
    assert "Speech recognition (azure, typed)" in narrative and "below the 0.6 threshold" in narrative


def test_language_switch_is_reported_for_the_recogniser(client):
    r = client.post("/conversations", json={"setting": "gp_booking", "language": "en"})
    cid = r.json()["conversation_id"]
    client.post(f"/conversations/{cid}/turns", json={"transcript": "Yes."})
    client.post(f"/conversations/{cid}/turns", json={"transcript": "Yes I can hear you."})
    r = client.post(f"/conversations/{cid}/turns", json={"transcript": "Vietnamese would be easier, please."})
    assert r.json()["language_switched"] is True and r.json()["language"] == "vi"
    assert client.get(f"/conversations/{cid}").json()["language"] == "vi"
    assert client.get("/speech/config?language=vi").json()["bcp47"] == "vi-VN"


def test_stt_provider_env_overrides(monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setenv("STT_PROVIDER", "browser")
    assert recognition.stt_provider_name() == "browser"
    monkeypatch.setenv("STT_PROVIDER", "auto")
    assert recognition.stt_provider_name() == "azure"
    monkeypatch.delenv("AZURE_SPEECH_KEY")
    assert recognition.stt_provider_name() == "browser"
