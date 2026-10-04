"""D-68: a set/enum question carries the vocabulary its answer is likely to use, so the browser's
Azure Speech recogniser can bias recognition towards it (medical terms and drug names a generic
speech model was never trained to expect) instead of guessing blind.
"""
from app.control.controller import Controller


def test_set_slot_has_hints(bundle):
    ctrl = Controller(bundle)
    slot = ctrl._module("review_of_systems").slot("ros.genitourinary")
    hints = ctrl._asr_hints(slot)
    assert hints is not None
    assert "burning" in hints and "testicle pain" in hints


def test_yes_no_slot_has_no_hints(bundle):
    ctrl = Controller(bundle)
    slot = ctrl._module("chest_pain").slot("cp.current")
    assert slot.value.type == "yes_no"
    assert ctrl._asr_hints(slot) is None


def test_text_slot_has_no_hints(bundle):
    ctrl = Controller(bundle)
    slot = ctrl._module("medications").slot("md.list")
    assert slot.value.type == "text"
    assert ctrl._asr_hints(slot) is None


def test_ask_turn_carries_asr_hints(bundle):
    from app.control.controller import new_state
    ctrl = Controller(bundle)
    state = new_state("ed", "en", {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True})
    state["module_queue"] = ["review_of_systems"]
    state["active_module"] = "review_of_systems"
    state["phase"] = "module"
    turns = ctrl._ask_next(state)
    ros_turn = next(t for t in turns if t.slot_id == "ros.cardiorespiratory")
    assert ros_turn.asr_hints and "chest pain" in ros_turn.asr_hints
