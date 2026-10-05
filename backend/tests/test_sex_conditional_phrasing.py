"""D-66: a review-of-systems item that would otherwise read out an anatomically irrelevant
option (testicular pain to someone who has said they're a woman, early-pregnancy bleeding to
someone who has said they're a man) picks the matching wording instead, once the patient has
said which they are - from ctx.sex_recorded, or their own words anywhere in the conversation.
Nothing is ever removed for someone whose sex isn't yet known; the combined wording (today's
behaviour) is the fallback, never a sex-specific one.
"""
from app.control.controller import Controller
from tests.simulation.runner import ActorScript, run_case

SAFE = {"cw.sentences": "Yes, easily.", "cw.haemoptysis_screen": "No blood, never.", "hd.thunderclap": "No, it built up slowly.",
        "hd.worst_ever": "No.", "cp.current": "No, it's gone now."}


def _genitourinary_question(r):
    return next(a["text"] for role, a in r.log if role == "agent" and a.get("slot_id") == "ros.genitourinary")


def test_combined_wording_when_sex_is_not_known(bundle):
    script = ActorScript(opening=["I've had a cough for three weeks."], answers=SAFE, default="No.")
    r = run_case(bundle, script, setting="gp_booking")
    text = _genitourinary_question(r)
    assert "testicle" in text and "pregnant" in text


def test_male_self_description_drops_the_pregnancy_option(bundle):
    script = ActorScript(opening=["I'm a man and I've had a cough for three weeks."], answers=SAFE, default="No.")
    r = run_case(bundle, script, setting="gp_booking")
    text = _genitourinary_question(r)
    assert "testicle" in text
    assert "pregnant" not in text and "vaginal" not in text


def test_female_self_description_drops_the_testicular_option(bundle):
    script = ActorScript(opening=["I'm a woman and I've had a cough for three weeks."], answers=SAFE, default="No.")
    r = run_case(bundle, script, setting="gp_booking")
    text = _genitourinary_question(r)
    assert "pregnant" in text
    assert "testicle" not in text


def test_ctx_sex_recorded_also_selects_the_wording(bundle):
    ctrl = Controller(bundle)
    from app.control.controller import new_state
    state = new_state("gp_booking", "en", {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True})
    state["slot_values"]["ctx.sex_recorded"] = {"slot_id": "ctx.sex_recorded", "module": "context", "value": "male", "verbatim": None, "state": "filled", "turn_id": "t0", "source": "record", "confidence": None, "written_at": "", "epistemic_status": None}
    slot = ctrl._module("review_of_systems").slot("ros.genitourinary")
    active = ctrl._active_phrasings(state, slot)
    assert [p.id for p in active] == ["ros-gu-male-v1"]


def test_sex_self_description_is_never_a_red_flag_rule_input(bundle):
    """The mechanism only ever selects a Phrasing; it has no path into rule evaluation, so a
    red-flag rule can never fire or fail to fire because of it (check 8's boundary)."""
    for m in bundle.modules.values():
        for rf in m.red_flags:
            assert "self_described_sex" not in rf.fires_when
