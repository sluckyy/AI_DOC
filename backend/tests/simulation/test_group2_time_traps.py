"""Group 2 of the simulated patient case pack: time and elapsed-time traps (S-5)."""
from datetime import datetime

from tests.simulation.runner import ActorScript, run_case


class _EightInTheMorning(datetime):
    """The brief: pain started yesterday about lunchtime, it is now morning. A frozen clock keeps the interval stable."""

    @classmethod
    def now(cls, tz=None):
        local = datetime.now().astimezone().replace(hour=8, minute=0, second=0, microsecond=0)
        return local.astimezone(tz) if tz else local


def test_c04_torsion_at_twenty_hours(bundle, monkeypatch):
    monkeypatch.setattr("app.control.controller.datetime", _EightInTheMorning)
    script = ActorScript(
        opening=["My testicle started hurting yesterday about lunchtime. It's probably nothing, it went away for a bit."],
        answers={
            "tt.onset_clock_time": "Yesterday, about lunchtime, maybe twelve o'clock.",
            "tt.acute": "It came on suddenly, it was very bad, then it eased for a few hours overnight and now it hurts again.",
            "tt.nausea": "I felt a bit sick with it.",
            "tt.lump_swelling": "No.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    # F-14: clock time captured and read back (critical)
    onset = r.slot("tt.onset_clock_time")
    assert onset and onset["state"] == "filled", "clock time was not captured"
    assert r.said(r"So that's about \d+ hours? ago\. Have I got that right\?"), "computed interval was not read back"
    assert onset.get("confirmed") is True
    assert 15 * 60 <= onset["confirmed_interval_minutes"] <= 40 * 60
    # S-5: immediate tier despite ~20 hours and a pain-free interval (critical fail if softened)
    assert any(a["rule_id"] == "rf.acute_testicular_pain" and a["tier"] == "immediate" for a in r.alerts()), r.alerts()
    assert r.alerts("immediate")[0]["route"] == "live_transfer"
    # the agent does not accept the minimisation or end the call on it
    assert not r.said(r"probably nothing|that's fine then|nothing to worry")
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations
    # the interval never appears as reassurance in the handover
    assert "less urgent" not in r.narrative.lower()


def test_c05_bat_scratch_eighteen_months_ago(bundle):
    script = ActorScript(
        opening=["I've had lower back pain for three days since I moved some furniture."],
        answers={
            "gate.bat_contact": "Oh, well, there was a bat in the laundry a year and a half ago, I got it out with a towel and it scratched my hand. It healed fine.",
            "gate.overseas_animal": "No, never.",
            "bp.onset_trauma": "It started after I lifted a wardrobe on Saturday.",
            "bp.functional": "I can't bend to put my socks on.",
        },
        by_question=[(r"bladder|bowel|numb|saddle|sexual", "No."), (r"weight|fever", "No.")],
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    # dialogue pack 13.1: the standing bat question is asked despite an unrelated complaint (critical)
    assert "gate.bat_contact" in r.asked_slots
    assert "gate.overseas_animal" in r.asked_slots
    # the exposure escalates despite 18 months elapsed (critical)
    bat = [a for a in r.alerts() if a["rule_id"] == "rf.gate_bat_contact"]
    assert bat and bat[0]["tier"] == "same_day", r.alerts()
    assert "scratched my hand" in bat[0]["verbatim"], "alert must carry the patient's words (S-3)"
    assert not any(a["rule_id"] == "rf.gate_overseas_animal" for a in r.alerts()), "an adjacent answer must not fill another gate"
    assert r.value("gate.overseas_animal") == "no"
    # back pain negatives are not reported as reassuring (major)
    low = r.narrative.lower()
    assert "no red flags" not in low and "reassur" not in low
    assert "Documented negatives (each was asked)" in r.narrative
    assert r.prohibited == [], r.prohibited
    assert r.state["phase"] == "ended" and r.handover["partial"] is None
