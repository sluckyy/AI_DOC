"""D-43/D-65: the wellbeing gate. A dedicated capability-check question (asked directly, never
inferred from the open-phase narrative - see the module docstring on WELLBEING_SEVERE/BARRIER in
controller.py for why). A severe answer (intoxication, significant cognitive impairment, acute
distress) always ends the interview. A communication-barrier answer (confusion, speech disturbance)
switches to the person with the patient if one is available, and ends the interview if not.
"""
from app.control.controller import Controller, new_state
from app.handover.generate import generate

CONSENT = {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True}


def _through_capability(ctrl, state, hearing="Yes, I can hear you.", language="English is fine.", present="No, it's just me.", wellbeing="No, I'm fine."):
    ctrl.start(state)
    ctrl.person_turn(state, "Yes, that's fine.")   # consent
    ctrl.person_turn(state, hearing)
    ctrl.person_turn(state, language)
    ctrl.person_turn(state, present)
    return ctrl.person_turn(state, wellbeing)


def test_normal_answer_proceeds_to_the_open_phase(bundle):
    ctrl = Controller(bundle)
    state = new_state("ed", "en", CONSENT)
    _, turns = _through_capability(ctrl, state)
    assert state["phase"] == "open"
    assert state["informant"] == "self"
    assert state["bail_out_reason"] is None
    assert turns[0].move == "open"


def test_severe_answer_ends_the_interview_regardless_of_collateral(bundle):
    ctrl = Controller(bundle)
    state = new_state("ed", "en", CONSENT)
    _, turns = _through_capability(ctrl, state, present="Yes, my daughter's with me.", wellbeing="I've had a couple of drinks.")
    assert state["phase"] == "ended"
    assert state["bail_out_reason"] == "distress_or_impairment"
    assert state["capability"]["wellbeing_flag"] == "severe"
    assert turns[-1].move == "bail_out"
    doc = generate(state, bundle)
    assert doc["partial"] == "interview did not run: distress or impairment"


def test_barrier_with_collateral_switches_informant_and_continues(bundle):
    ctrl = Controller(bundle)
    state = new_state("gp_booking", "en", CONSENT)
    _, turns = _through_capability(ctrl, state, present="My daughter's with me.", wellbeing="He's quite confused and not really making sense.")
    assert state["phase"] == "open"
    assert state["informant"] == "collateral"
    assert state["capability"]["wellbeing_flag"] == "barrier"
    assert any(t.move == "capability" for t in turns)   # the collateral_handoff line
    assert turns[-1].move == "open"
    # every direct answer from here on is relabelled, not read as the patient's own account
    slot = next(s for s in ctrl._module("chest_pain").slots if s.id == "cp.quality")
    state["module_queue"] = ["chest_pain"]
    ctrl._write(state, "chest_pain", slot, "pressure", "a pressure", "t9")   # default source="person"
    assert state["slot_values"]["cp.quality"]["source"] == "collateral"
    doc = generate(state, bundle)
    assert any(e["slot_id"] == "cp.quality" and e["provenance"] == "collateral_reported" for e in doc["structured_record"])
    assert any(line.startswith("COLLATERAL HISTORY") for line in doc["narrative"])
    assert doc["metadata"]["informant"] == "collateral"


def test_barrier_without_collateral_ends_the_interview(bundle):
    ctrl = Controller(bundle)
    state = new_state("ed", "en", CONSENT)
    _, turns = _through_capability(ctrl, state, present="No, just me.", wellbeing="Sorry, I keep losing track, it's hard to follow.")
    assert state["phase"] == "ended"
    assert state["bail_out_reason"] == "communication_barrier_no_collateral"
    assert state["informant"] == "self"
    assert turns[-1].move == "bail_out"


def test_wellbeing_gate_never_fires_on_the_open_phase_narrative(bundle):
    """The exact wording of the C-02 wake-up-stroke case: a caller describing someone else's
    speech as slurred is a symptom, not a barrier to *this* conversation, and must never be
    mistaken for one - which is why the gate only ever looks at a direct answer to its own
    question, never at the narrative."""
    ctrl = Controller(bundle)
    state = new_state("gp_booking", "en", CONSENT)
    _, turns = _through_capability(ctrl, state, present="It's me, his wife, I'm calling for him.")
    assert state["phase"] == "open"
    assert state["informant"] == "self"
    ctrl.person_turn(state, "When he woke up this morning his face was drooping and his speech was slurred, I couldn't understand him.")
    assert state["phase"] not in ("ended",)
    assert state["bail_out_reason"] is None
