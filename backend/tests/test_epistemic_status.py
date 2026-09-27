"""D-63: the epistemic ladder and dependency-aware repair (Mathematics of Clinical History
Taking, s.4, s.8, s.8.1). A value mined from narrative is a hypothesis; reading it back and
getting a plain confirmation grounds it; a non-confirming reply flags it, and anything that
fired on it, pending clarification, rather than silently keeping or discarding either one.
"""
from app.control.controller import Controller, new_state
from app.handover.generate import generate

CONSENT = {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True}


def _setup(bundle):
    ctrl = Controller(bundle)
    state = new_state("ed", "en", CONSENT)
    ctrl.start(state)
    state["module_queue"] = ["chest_pain"]
    return ctrl, state


def _slot(ctrl, module, slot_id):
    return next(s for s in ctrl._module(module).slots if s.id == slot_id)


def test_opportunistic_write_is_a_hypothesis(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.quality")
    ctrl._write(state, "chest_pain", slot, "pressure", "like a pressure", "t1", source="person_open_phase")
    assert state["slot_values"]["cp.quality"]["epistemic_status"] == "hypothesis"


def test_direct_answer_is_grounded_immediately(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.quality")
    ctrl._write(state, "chest_pain", slot, "pressure", "a pressure", "t1")   # default source="person"
    assert state["slot_values"]["cp.quality"]["epistemic_status"] == "grounded"


def test_confirmed_readback_grounds_a_hypothesis(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.quality")
    ctrl._write(state, "chest_pain", slot, "pressure", "like a pressure", "t1", source="person_open_phase")
    state["phase"] = "final_invite"
    ctrl._on_final_invite(state, "No, nothing else.", "t2")
    assert state["phase"] == "read_back"
    assert "cp.quality" in state["read_back_slot_ids"]
    assert state["slot_values"]["cp.quality"]["epistemic_status"] == "patient_grounded"   # exposed for confirmation, s.4.1 L4
    ctrl._on_read_back(state, "Yes, that's right.", "t3")
    assert state["read_back_done"]
    assert state["slot_values"]["cp.quality"]["epistemic_status"] == "patient_grounded"
    assert state["patient_corrections"] == []


def test_corrected_readback_flags_the_item_and_its_alert(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.current")
    ctrl._write(state, "chest_pain", slot, "yes", "still got it", "t1", source="person_open_phase")
    ctrl._evaluate_rules(state, "t1")   # rf.chest_pain_current fires_when cp.current == 'yes'
    assert state["fired_rules"] == ["rf.chest_pain_current"]
    alert_id = state["alerts"][0]["id"]
    assert state["alerts"][0].get("correction_flag") is None

    state["phase"] = "final_invite"
    ctrl._on_final_invite(state, "No, nothing else.", "t2")
    assert "cp.current" in state["read_back_slot_ids"]

    ctrl._on_read_back(state, "Actually no, it had already gone by then.", "t3")
    assert state["slot_values"]["cp.current"]["epistemic_status"] == "correction_pending"
    assert state["alerts"][0]["correction_flag"] is True
    corr = state["patient_corrections"][0]
    assert "cp.current" in corr["read_back_slot_ids"]
    assert corr["affected_alerts"] == [alert_id]


def test_not_asked_and_unknown_slots_carry_no_epistemic_status(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.quality")
    ctrl._write(state, "chest_pain", slot, None, "not sure", "t1", st="unknown")
    assert state["slot_values"]["cp.quality"]["epistemic_status"] is None


def test_handover_surfaces_epistemic_status_and_correction(bundle):
    ctrl, state = _setup(bundle)
    slot = _slot(ctrl, "chest_pain", "cp.current")
    ctrl._write(state, "chest_pain", slot, "yes", "still got it", "t1", source="person_open_phase")
    ctrl._evaluate_rules(state, "t1")
    alert_id = state["alerts"][0]["id"]
    state["phase"] = "final_invite"
    ctrl._on_final_invite(state, "No, nothing else.", "t2")
    ctrl._on_read_back(state, "Actually no, it had already gone by then.", "t3")

    doc = generate(state, bundle)
    narrative = " ".join(doc["narrative"])
    assert "Correction at read-back" in narrative
    assert "cp.current" in narrative
    assert alert_id in narrative
    assert f"affects alert(s) {alert_id}" in narrative
    assert "correction_flag" not in narrative   # code-level key names never leak into clinician text
    alert_line = next(l for l in doc["narrative"] if l.startswith("ALERT"))
    assert "the patient later queried" in alert_line
    entry = next(e for e in doc["structured_record"] if e["slot_id"] == "cp.current")
    assert entry["epistemic_status"] == "correction_pending"
