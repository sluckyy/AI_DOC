"""Scripted conversations through the controller on the rules extractor.

Answers are keyed by the slot the agent actually asks for, because the controller
skips slots it already filled from the patient's narrative (P12: capture at
elicitation), so a fixed answer order would misalign.
"""
from app.control.controller import Controller, new_state

CONSENT = {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True}


def run(bundle, open_lines, answers=None, setting="ed", consent=None, summary_reply="Yes, that's right.",
        final_reply="No, that's it.", read_back_reply="Yes that's right.", max_turns=80):
    ctrl = Controller(bundle)
    state = new_state(setting, "en", consent or CONSENT)
    log = [("agent", t.as_dict()) for t in ctrl.start(state)]
    answers = answers or {}
    open_lines = list(open_lines)
    n = 0
    while state["phase"] != "ended" and n < max_turns:
        n += 1
        last = next((a for r, a in reversed(log) if r == "agent"), None)
        move = last["move"] if last else "disclose"
        if move == "disclose":
            line = "Yes, that's fine."
        elif move in ("open", "facilitate"):
            line = open_lines.pop(0) if open_lines else "That's all really."
        elif move == "invite":
            line = open_lines.pop(0) if open_lines else "No, nothing else."
        elif move == "summarise":
            line = summary_reply
        elif move in ("ask", "reask"):
            line = answers.get(last["slot_id"], "I'm not sure.")
        elif move == "final_invite":
            line = final_reply
        elif move == "read_back":
            line = read_back_reply
        elif move in ("deflect", "explain_why"):
            line = "Ok."
        else:
            break
        tid, turns = ctrl.person_turn(state, line)
        log.append(("person", {"text": line, "turn_id": tid, "slot_id": last.get("slot_id") if last else None}))
        log.extend(("agent", t.as_dict()) for t in turns)
    return state, log


SETTLED_OPEN = [
    "I've had this pain in my chest since this morning. It's like a pressure, and I felt a bit sick with it.",
    "It's settled now, it's gone. I was worried because my dad had heart problems.",
]
SETTLED_ANSWERS = {
    "cp.current": "No, it's gone now.",
    "cp.onset_clock_time": "About 7am this morning.",
    "cp.onset": "It came on suddenly.",
    "cp.quality": "Like a pressure, a heavy weight.",
    "cp.radiation": "It went into both arms.",
    "cp.duration_pattern": "Maybe twenty minutes.",
    "cp.pleuritic": "No, breathing didn't change it.",
    "cp.positional": "No, moving made no difference.",
    "cp.exertional": "I was walking up the stairs.",
    "cp.sweating": "Yes I was sweating.",
    "cp.breathlessness": "No, my breathing was fine.",
    "cp.prior_cardiac_workup": "No, never had anything like that.",
}


def test_settled_chest_pain_full_history(bundle):
    state, log = run(bundle, SETTLED_OPEN, SETTLED_ANSWERS)
    assert state["phase"] == "ended"
    assert state["problem_list_closed"]
    assert len(set(state["invitations_used"])) >= 3, "P13: three distinct invitations before closing the problem list"
    assert "chest_pain" in state["module_queue"]
    sv = state["slot_values"]
    assert sv["cp.current"]["value"] == "no"
    assert sv["cp.onset"]["value"] == "abrupt"
    assert sv["cp.quality"]["value"] == "pressure"
    assert "both_arms" in sv["cp.radiation"]["value"]
    assert sv["cp.duration_pattern"]["value"] == "minutes"
    assert sv["cp.pleuritic"]["value"] == "no"
    assert sv["cp.exertional"]["value"] == "exertion"
    assert sv["cp.sweating"]["value"] == "yes"
    assert sv["cp.prior_cardiac_workup"]["value"] == ["none"]
    assert all(v["turn_id"] for v in sv.values() if v["state"] == "filled"), "P12: every filled slot carries a turn id"
    assert not [k for k, v in sv.items() if v["state"] == "not_asked"]
    assert state["fired_rules"] == []
    assert state["closing_delivered"]["uncertainty"]
    agent_text = " ".join(a["text"] for role, a in log if role == "agent").lower()
    assert "anything else" not in agent_text
    assert "heart attack" not in agent_text and "angina" not in agent_text
    assert any(a["move"] == "summarise" for role, a in log if role == "agent")
    assert any(a["move"] == "read_back" for role, a in log if role == "agent")


def test_narrative_fills_slots_with_originating_turn(bundle):
    state, log = run(bundle, SETTLED_OPEN, SETTLED_ANSWERS)
    # "since this morning" and "pressure" were in the opening statement, so those slots
    # carry the opening turn's id, not the id of a later question
    presenting_tid = state["presenting_turn_id"]
    assert state["slot_values"]["cp.quality"]["turn_id"] == presenting_tid
    assert state["slot_values"]["cp.quality"]["source"] == "person_open_phase"


def test_current_chest_pain_fires_immediate_alert_and_stops(bundle):
    open_lines = ["I've got a tight pain in my chest right now, it's there at the moment and it's going through to my back."]
    state, log = run(bundle, open_lines, SETTLED_ANSWERS)
    assert "rf.chest_pain_current" in state["fired_rules"]
    a = state["alerts"][0]
    assert a["tier"] == "immediate" and a["route"] == "alert_triage"
    assert a["verbatim"], "alert carries the patient's words"
    assert state["closed_by_alert"] and state["phase"] == "ended"
    not_asked = [k for k, v in state["slot_values"].items() if v["state"] == "not_asked"]
    assert not_asked, "everything after the alert is not asked, never negative"
    agent_moves = [a["move"] for role, a in log if role == "agent"]
    assert "alert" in agent_moves
    assert "ask" not in agent_moves, "the interview did not continue after an immediate alert"


def test_gp_booking_immediate_routes_to_duty_gp(bundle):
    state, _ = run(bundle, ["I have chest pain now, right now, it's tight."], SETTLED_ANSWERS, setting="gp_booking")
    assert state["alerts"][0]["route"] == "live_transfer"
    assert "put you through" in state["alerts"][0]["patient_message"]


def test_dissection_pattern_rule(bundle):
    open_lines = ["I had a tearing pain in my chest that came on suddenly and went through to my back. It's gone now."]
    state, _ = run(bundle, open_lines, SETTLED_ANSWERS)
    sv = state["slot_values"]
    assert sv["cp.onset"]["value"] == "abrupt"
    assert sv["cp.quality"]["value"] == "tearing"
    assert "back" in sv["cp.radiation"]["value"]
    assert "rf.aortic_dissection_pattern" in state["fired_rules"]
    assert "rf.chest_pain_current" not in state["fired_rules"]


def test_unanswerable_slot_becomes_unknown_not_negative(bundle):
    answers = dict(SETTLED_ANSWERS)
    answers["cp.duration_pattern"] = "I really couldn't tell you, it's all a blur."
    state, _ = run(bundle, SETTLED_OPEN, answers)
    v = state["slot_values"]["cp.duration_pattern"]
    assert v["state"] in ("unknown", "filled")
    if v["state"] == "unknown":
        assert v["value"] is None


def test_declined_consent_bails_out(bundle):
    ctrl = Controller(bundle)
    state = new_state("ed", "en", CONSENT)
    ctrl.start(state)
    ctrl.person_turn(state, "No, I'd rather talk to a person.")
    assert state["phase"] == "ended" and state["bail_out_reason"] == "declined_consent"


def test_serious_question_is_deflected_not_answered(bundle):
    state, log = run(bundle, ["I've got chest pain, it's gone now. Is it serious?"], SETTLED_ANSWERS)
    texts = [a["text"] for role, a in log if role == "agent"]
    assert any("I don't make that call" in t for t in texts)
    assert not any("nothing to worry" in t.lower() for t in texts)


def test_tone_is_stored_only_with_consent(bundle):
    lines = ["I'm really worried, is it serious? I've got chest pain but it's gone."]
    state, _ = run(bundle, lines, SETTLED_ANSWERS, consent={"ai_disclosure": True, "tone_adaptation": False, "summary_to_clinician": True})
    assert state["tone_log"] == []
    state, _ = run(bundle, lines, SETTLED_ANSWERS)
    assert any(t["label"] == "anxious" for t in state["tone_log"])


def test_generic_module_used_for_ungrounded_presentation(bundle):
    answers = {"gen.onset": "Three days ago.", "gen.progression": "Getting worse.", "gen.triggers": "Bright light.",
               "gen.relief": "Lying down in the dark.", "gen.functional_impact": "I can't work.", "gen.associated": "Feeling sick."}
    state, log = run(bundle, ["I've had hiccups for three days."], answers)
    assert state["module_queue"] == ["generic_symptom"]
    assert state["generic_problem"] == "hiccups"
    asked = [a["text"] for r, a in log if r == "agent" and a["move"] == "ask"]
    assert any("hiccups" in t for t in asked), "the generic module names the patient's own problem"
    assert state["slot_values"]["gen.progression"]["value"] == "worse"
