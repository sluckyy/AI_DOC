"""Group 5 of the case pack: interview conduct and equity. C-16 needs live speech (endpointing, ASR
confidence per cohort) and is run with actors; the parts a scripted run can check are here."""
import pytest

from tests.simulation.runner import ActorScript, run_case


def test_c16_slow_second_language_speaker_scripted_parts(bundle):
    # Six symptoms produced one per prompt across the open phase (F-8 saturation must not be premature).
    opening = [
        "I have had a cough.", "And my chest feels tight.", "I feel tired all the time.",
        "My ankles are swollen.", "I have a headache most days.", "And I have been dizzy when I stand.",
    ]
    script = ActorScript(opening=opening, capability={"cap.hearing": "Yes.", "cap.language": "Maybe Vietnamese would be easier.", "cap.present": "No."}, default="No.")
    r = run_case(bundle, script, setting="gp_booking")
    # dialogue pack 2.2: the language offer is made and honoured (major)
    assert "cap.language" in [a.get("slot_id") for _, a in r.log]
    assert r.state["language"] == "vi" and r.state["capability"]["language_switched_to"] == "vi"
    # F-8 / P13: the open phase kept prompting until three empty invitations, so all six symptoms were named
    named = [p["term"] for p in r.state["problems"]]
    assert len(named) >= 6, named
    assert len(set(r.state["invitations_used"])) >= 3
    # F-9: every symptom carries the prompt id that pulled it
    assert all("pulled_by" in p for p in r.state["problems"])
    # F-33: the handover states the interview language
    assert "Interview language: vi" in r.narrative
    # N-3 endpointing is a deployment parameter, adjustable per site
    assert bundle.parameters.silence_end_of_turn_ms >= 1200


@pytest.mark.xfail(reason="N-3/N-5/N-8 (no premature endpointing, no truncation, per-cohort ASR accuracy) need the live speech path and actors; the plumbing for N-9 confidence is covered in tests/test_recognition.py", strict=True)
def test_c16_speech_layer_criteria():
    raise AssertionError("run with actors on the speech path")
