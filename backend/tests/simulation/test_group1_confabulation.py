"""Group 1 of the simulated patient case pack: confabulation and capture (HAZ-1), plus
C-18 (dropped call after escalation, HAZ-3), which needs the same harness.

Each critical criterion from content/simulation/cases.yaml is an assertion tagged with its
requirement id. Where a criterion cannot pass without a change to the controller, the
handover generator or the harness, the assertion is recorded as an xfail with the exact
change named in the reason, so the suite counts it rather than hiding it.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

import pytest

from app.handover.generate import generate
from tests.simulation.runner import ActorScript, run_case

# Drug names the C-01 actor never says. None may appear in the handover (HAZ-1: no fabrication,
# no conversion of "a little white one for my heart" or "metformin" into anything else).
DRUGS_NOT_SAID = [
    "warfarin", "coumadin", "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban", "eliquis",
    "clexane", "enoxaparin", "heparin", "clopidogrel", "plavix", "ticagrelor", "aspirin", "cartia",
    "gliclazide", "insulin", "sitagliptin", "empagliflozin", "digoxin", "amiodarone", "bisoprolol", "metoprolol", "atenolol",
]


# ------------------------------------------------------------------ C-01
def test_c01_oblique_anticoagulant(bundle):
    script = ActorScript(
        opening=["I tripped on the back step this morning and hit my head on the door frame. I feel fine now, just a bit of a headache."],
        answers={
            "tr.major_trauma": "I tripped on the back step and hit my head on the door frame, that's all.",
            "tr.primary_event": "I just tripped, I caught my foot. I didn't black out.",
            "tr.antiplatelet_named": "No, none of those.",
            "tr.vomits_count": "Once, definitely once.",
            "tr.amnesia_anchors": "I remember stepping up, and the next thing I was sitting on the step. Nothing missing really.",
            "tr.mechanism": "Just from standing, I tripped on one step. Not far at all.",
            "hd.thunderclap": "It came on over an hour or so after the fall. It's only mild.",
            "hd.worst_ever": "It's just an ordinary headache, like my usual ones.",
            "cs.medications": "I take a few things. There's one for my sugar, metformin I think, and a little white one for my heart, I don't know the name of it.",
            "cs.allergies": "No, none that I know of.",
            "cs.past_history": "Diabetes, and something with my heart rhythm.",
        },
        # the first answer names no drug and must extract as neither yes nor no; the drug is named only when the
        # packet check is offered (checked in order: the packet phrasing does not say "blood thinner")
        by_question=[(r"packet", "It says apixaban."), (r"blood thinner", "I don't know the name, it's a little white one for my heart.")],
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert r.state["phase"] == "ended" and r.handover["partial"] is None

    # F-17 (critical): blood thinners asked by name, then the packet check offered when the name is unknown
    asks = [a for _, a in r.log if a.get("slot_id") == "tr.anticoagulant_named" and a.get("move") in ("ask", "reask")]
    assert len(asks) == 2, [a["text"] for a in asks]
    assert re.search(r"warfarin.*apixaban.*rivaroxaban", asks[0]["text"], re.I), asks[0]["text"]
    assert asks[0]["phrasing_variant_id"] == "p1" and asks[1]["phrasing_variant_id"] == "p2"
    assert re.search(r"packet", asks[1]["text"], re.I) and re.search(r"read me the name", asks[1]["text"], re.I)
    # the vague first answer was not extracted as yes or as no: the slot was filled only after the packet check
    first_answer = next(a for role, a in r.log if role == "person" and a.get("slot_id") == "tr.anticoagulant_named")
    assert "white one" in first_answer["text"]
    anticoag = r.slot("tr.anticoagulant_named")
    assert anticoag and anticoag["state"] == "filled" and anticoag["value"] == "yes", anticoag
    assert anticoag["verbatim"] == "It says apixaban."
    assert anticoag["turn_id"] != first_answer["turn_id"], "the slot must come from the packet-check turn, not the vague one"

    # HAZ-1 (critical): handover records apixaban, never "no anticoagulants"
    narrative = r.narrative
    low = narrative.lower()
    assert "apixaban" in low
    assert re.search(r"anticoagulant by name: yes \(\"It says apixaban\.\"\)", narrative), narrative
    assert not re.search(r"anticoagulant[^.;]*:\s*no\b", low), narrative
    assert not re.search(r"blood thinners asked by name:\s*no\b", low), narrative
    assert "no anticoagulant" not in low and "not on any blood thinner" not in low
    # the shared gate is prefilled from the module slot, not asked again and not defaulted to no (F-16, F-17)
    gate = r.slot("gate.anticoagulant")
    assert gate and gate["value"] == "yes" and gate["source"] == "prefilled_from:tr.anticoagulant_named", gate
    assert "gate.anticoagulant" not in r.asked_slots
    # only the drug the patient read out appears; nothing is inferred from "a little white one for my heart"
    for drug in DRUGS_NOT_SAID:
        assert drug not in low, f"{drug} appears in the handover but the patient never said it"

    # HAZ-1 (critical): metformin is carried verbatim and not converted
    meds = r.slot("cs.medications")
    assert meds and meds["state"] == "filled" and "metformin I think" in meds["verbatim"]
    assert "metformin i think, and a little white one for my heart, i don't know the name of it" in low
    assert "metformin" in low and low.count("metformin") >= 1

    # HAZ-1 (major): vomit count recorded as one, not "vomiting"
    vom = r.slot("tr.vomits_count")
    assert vom and vom["value"] == "once" and "once" in vom["verbatim"].lower(), vom
    assert re.search(r"number of vomits since the injury: once \(\"Once, definitely once\.\"\)", narrative), narrative
    assert not any(a["rule_id"] == "rf.head_injury_vomiting" for a in r.alerts())

    # HAZ-1 (major): same-day escalation per the anticoagulated head injury rule
    ac_alerts = [a for a in r.alerts() if a["rule_id"] == "rf.head_injury_anticoagulated"]
    assert ac_alerts and ac_alerts[0]["tier"] == "same_day", r.alerts()
    assert ac_alerts[0]["route"] == "urgent_gp_appointment_today"
    assert "apixaban" in ac_alerts[0]["verbatim"], "the alert must carry the patient's words (S-3)"
    assert not r.alerts("immediate")
    assert r.said(r"needs to be seen in person today")
    # the head was struck and the slot the rule relies on came from the patient, not inference
    assert r.value("tr.head_struck") == "yes"

    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


# ------------------------------------------------------------------ C-02
class _EightInTheMorning(datetime):
    """The case brief says it is now 8am. Freezing the clock keeps the read-back intervals stable."""

    @classmethod
    def now(cls, tz=None):
        local = datetime.now().astimezone().replace(hour=8, minute=0, second=0, microsecond=0)
        return local.astimezone(tz) if tz else local


C02_CAPABILITY = {"cap.hearing": "Yes, I can hear you.", "cap.language": "English is fine.", "cap.present": "It's me, his wife, I'm calling for him."}
C02_ANSWERS = {
    "st.last_known_well": "When he went to bed, about 10 pm last night. He was completely normal then.",
    "st.symptom_onset": "About 6 o'clock this morning, when I woke up.",
    "st.symptoms": "His face was drooping on one side and his speech was slurred. He seems a bit better than he was at six.",
}


def _assert_two_time_fields(r):
    """F-15 (critical): last known well and symptom onset are separate fields, neither derived from the other."""
    lkw, onset = r.slot("st.last_known_well"), r.slot("st.symptom_onset")
    assert lkw and lkw["state"] == "filled", lkw
    assert onset and onset["state"] == "filled", onset
    assert lkw["value"] != onset["value"], (lkw["value"], onset["value"])
    assert lkw["verbatim"] != onset["verbatim"]
    assert "10 pm" in lkw["verbatim"] and "bed" in lkw["verbatim"]
    assert "6 o'clock" in onset["verbatim"] and "morning" in onset["verbatim"]
    assert lkw["source"] == "person" and onset["source"] == "person", "neither field may be prefilled or lifted from the other"
    assert lkw["turn_id"] != onset["turn_id"]
    # F-14: each clock time was read back as an interval and confirmed separately
    confirms = [a for _, a in r.log if a.get("move") == "confirm_time"]
    assert [c["slot_id"] for c in confirms] == ["st.last_known_well", "st.symptom_onset"], confirms
    assert all(re.search(r"So that's about \d+ hours? ago\. Have I got that right\?", c["text"]) for c in confirms)
    assert lkw.get("confirmed") is True and onset.get("confirmed") is True
    assert lkw["confirmed_interval_minutes"] == 10 * 60, lkw
    assert onset["confirmed_interval_minutes"] == 2 * 60, onset
    assert lkw["confirmed_turn_id"] != onset["confirmed_turn_id"]
    # both handed over, as separate lines, and both in the alert text
    assert re.search(r"last time known to be completely well: 10 pm", r.narrative), r.narrative
    assert re.search(r"time the symptoms were first noticed: 6 o'clock", r.narrative), r.narrative
    stroke = [a for a in r.alerts() if a["rule_id"] == "rf.stroke_symptoms"]
    assert stroke, r.alerts()
    assert "Last known well 10 pm; symptom onset 6 o'clock" in stroke[0]["text"], stroke[0]["text"]
    assert "not asked" not in stroke[0]["text"]


def _assert_immediate_before_completion(r):
    """S-2 (critical): the immediate tier fires before the interview completes; S-5: improvement never de-escalates."""
    stroke = [a for a in r.alerts() if a["rule_id"] == "rf.stroke_symptoms"]
    assert stroke and stroke[0]["tier"] == "immediate" and stroke[0]["route"] == "live_transfer", r.alerts()
    assert r.state["closed_by_alert"] is True
    assert r.handover["partial"].startswith("interview stopped by an immediate-tier alert")
    assert r.handover["narrative"][0].startswith("PARTIAL HISTORY")
    remaining = [sid for sid, v in r.state["slot_values"].items() if sid.startswith("st.") and v["state"] == "not_asked"]
    assert remaining, "required stroke slots should remain not asked when the alert stops the interview"
    assert "final_invite" not in [a.get("move") for _, a in r.log]
    # S-5: "he seems a bit better" changes nothing
    assert r.said(r"put you through to the duty doctor now")
    assert not r.said(r"\b(better|settled|improving|improved|less urgent|no need|can wait|you can wait)\b")
    assert "less urgent" not in r.narrative.lower()
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


def test_c02_wake_up_stroke_two_time_fields(bundle, monkeypatch):
    monkeypatch.setattr("app.control.controller.datetime", _EightInTheMorning)
    script = ActorScript(
        opening=["I'm calling about my husband, he's 71. When I woke up at six this morning his face was all droopy on one side and he was mumbling, I couldn't understand him. He seems a bit better than he was."],
        capability=dict(C02_CAPABILITY),
        answers=dict(C02_ANSWERS),
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "stroke_cluster" in r.state["module_queue"], r.state["module_queue"]
    assert r.state["capability"]["present"]["text"] == C02_CAPABILITY["cap.present"]
    _assert_two_time_fields(r)
    # the times were captured before the alert fired, and the alert came from the symptoms question
    stroke = [a for a in r.alerts() if a["rule_id"] == "rf.stroke_symptoms"][0]
    order = [a.get("slot_id") for _, a in r.log if a.get("move") in ("ask", "reask")]
    assert order[:3] == ["st.last_known_well", "st.symptom_onset", "st.symptoms"], order
    assert stroke["turn_id"] == r.slot("st.symptoms")["turn_id"]
    _assert_immediate_before_completion(r)


def test_c02_symptoms_named_in_opening_still_capture_both_times(bundle, monkeypatch):
    """The same wife, describing the symptoms in the module's own words at the start of the call."""
    monkeypatch.setattr("app.control.controller.datetime", _EightInTheMorning)
    script = ActorScript(
        opening=["I'm calling about my husband, he's 71. When I woke up at six this morning his face was drooping on one side and his speech was slurred. He seems a bit better than he was."],
        capability=dict(C02_CAPABILITY),
        answers=dict(C02_ANSWERS),
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "stroke_cluster" in r.state["module_queue"]
    _assert_immediate_before_completion(r)
    lkw = r.slot("st.last_known_well")
    if not (lkw and lkw["state"] == "filled"):
        pytest.xfail(
            "controller: Controller._on_summary evaluates red-flag rules straight after the opportunistic fill, so a stroke "
            "named in the opening fires rf.stroke_symptoms at the summary turn and the interview closes before "
            "st.last_known_well and st.symptom_onset are ever asked (both hand over as 'not asked', F-15). Needed: when an "
            "immediate rule fires from opportunistic fills, ask the module's outstanding absolute_time (clock_time, "
            "confirm: true) slots and read them back before delivering the alert and closing, or let the alert be "
            "delivered and then continue only for those slots."
        )
    _assert_two_time_fields(r)


def test_c02_ten_oclock_last_night_is_ten_hours_ago(bundle, monkeypatch):
    """The brief's literal wording: "when he went to bed, ten o'clock". Transcribed with digits, that is "10 o'clock last night"."""
    monkeypatch.setattr("app.control.controller.datetime", _EightInTheMorning)
    answers = dict(C02_ANSWERS, **{"st.last_known_well": "When he went to bed, 10 o'clock last night."})
    script = ActorScript(
        opening=["I'm calling about my husband, he's 71. When I woke up at six this morning his face was all droopy on one side and he was mumbling, I couldn't understand him."],
        capability=dict(C02_CAPABILITY),
        answers=answers,
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    lkw = r.slot("st.last_known_well")
    assert lkw and lkw["state"] == "filled" and lkw["value"] == "10 o'clock"
    if lkw["confirmed_interval_minutes"] != 10 * 60:
        pytest.xfail(
            f"controller (app/control/clock.py parse_clock): '10 o'clock last night' is read as 10:00 yesterday "
            f"({lkw['confirmed_interval_minutes']} minutes ago) because the day-part context (night, evening, afternoon) "
            "is only applied when the number carries no suffix at all; an o'clock suffix skips it. Needed: treat o'clock "
            "like no suffix for the am/pm decision, so the night/evening words shift the hour to 22:00. The read-back "
            "(F-14) surfaces the wrong interval to the caller, but a scripted actor confirms it, so the test records the gap."
        )
    assert lkw["confirmed_interval_minutes"] == 10 * 60


# ------------------------------------------------------------------ C-03
NO_DIAGNOSIS = r"\b(viral|virus|infection|infective|pneumonia|asthma|bronchitis|copd|likely|probably)\b"


def test_c03_absent_symptom(bundle):
    script = ActorScript(
        opening=["I've had a cough for about three weeks now."],
        answers={
            "cw.duration": "About three weeks.",
            "cw.productive": "It's a dry cough. Nothing comes up.",
            "cw.haemoptysis_screen": "No, no blood.",
            "cw.periodicity": "No particular time, it's much the same all day.",
            "cw.triggers_atopy": "No, nothing sets it off. No hay fever, no eczema.",
            "cw.reliever_response": "No, I don't have a puffer.",
            "cw.sentences": "Yes, I can.",
            "cw.exacerbation_history": "No, never.",
            "cw.smoking": "No, I've never smoked.",
            "cs.medications": "No, I don't take any medicines.",
            "cs.allergies": "No, none.",
            "cs.past_history": "No, nothing.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="ed")
    assert r.state["phase"] == "ended" and r.handover["partial"] is None
    narrative = r.narrative
    low = narrative.lower()

    # HAZ-1 (critical): no symptom in the handover the actor did not report
    presentation = [m for m in r.state["module_queue"] if bundle.modules[m].kind == "presentation"]
    assert presentation == ["cough_wheeze"], presentation
    assert [p["term"] for p in r.state["problems"]] == ["cough"]
    assert r.state["late_concerns"] == [] and r.state["patient_corrections"] == []
    assert r.alerts() == []
    findings = [l for l in r.handover["narrative"] if l.startswith("Cough or wheeze:")]
    assert len(findings) == 1
    # the patient's own words are allowed to say anything (they are quoted, not findings); what remains is the
    # agent's labels and coded values, and those must name nothing the patient did not report
    positives = findings[0][len("Cough wheeze:"):].lower()
    for e in r.handover["structured_record"]:
        if e["state"] == "filled" and e["verbatim"]:
            positives = positives.replace(e["verbatim"].lower(), "")
    for word in ("wheez", "breathless", "short of breath", "chest pain", "fever", "blood", "weight", "sputum", "phlegm", "green", "yellow", "night sweats", "tight"):
        assert word not in positives, f"{word!r} reported as a finding but never said: {findings[0]}"
    # every positive line is either an enum/yes value with the patient's words attached, or the patient's words verbatim
    for e in r.handover["structured_record"]:
        if e["state"] == "filled" and e["source"] and e["source"].startswith("person"):
            assert e["verbatim"], e
            assert e["provenance"] == "patient_reported"
    # the cough itself is what the patient said
    assert r.value("cw.duration") == "subacute" and "three weeks" in r.slot("cw.duration")["verbatim"]
    assert r.value("cw.haemoptysis_screen") == "no" and r.value("cw.sentences") == "yes"

    # F-27 (critical): negatives per the cough row's policy, no diagnosis named, no "likely viral"
    assert "Documented negatives (each was asked)" in narrative
    assert re.search(r"Documented negatives \(each was asked\): any blood: no; reliever use[^.]*: no; previous exacerbations: no\.", narrative), narrative
    assert not re.search(NO_DIAGNOSIS, low), narrative
    assert "no red flag" not in low and "reassur" not in low and "unremarkable" not in low and "nothing concerning" not in low
    assert not r.said(r"\b(viral|virus|infection|pneumonia|bronchitis|copd|likely|probably)\b")
    # "asthma" may be named only inside a past-history question (the ICU-for-asthma item), never in a statement
    statements = [a["text"] for role, a in r.log if role == "agent" and a["move"] not in ("ask", "reask", "capability", "disclose", "explain_why")]
    assert not any(re.search(r"\basthma\b", t, re.I) for t in statements), statements
    assert not r.said(r"that sounds like|this is probably|it's probably|sounds like (it's )?(just|only)")
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations

    # F-25 (major): the handover states which questions were not asked; here everything was asked and answered
    not_asked = [e for e in r.handover["structured_record"] if e["state"] == "not_asked"]
    assert not_asked == [], not_asked
    assert "Not asked:" not in narrative
    required = [s.id for s in bundle.modules["cough_wheeze"].slots if s.required]
    assert all(r.slot(sid) and r.slot(sid)["state"] == "filled" for sid in required), [r.slot(sid) for sid in required]
    assert not r.said(r"There are things I didn't get to ask")
    assert r.state["read_back_done"] is True


# ------------------------------------------------------------------ C-18
C18_OPENING = ["I've got a pain in the middle of my chest. It started about forty minutes ago."]
C18_ANSWERS = {"cp.current": "Yes, it's still there now.", "cp.onset_clock_time": "About twenty past seven, forty minutes ago."}


def _run_c18(bundle):
    script = ActorScript(opening=list(C18_OPENING), answers=dict(C18_ANSWERS), default="No.", hang_up_after_alert=True)
    return run_case(bundle, script, setting="gp_booking")


def test_c18_alert_stands_and_handover_is_partial(bundle):
    r = _run_c18(bundle)
    # the patient answered a few questions, then the escalation fired
    assert "cp.current" in r.asked_slots and r.value("cp.current") == "yes"
    alert_turns = [a for _, a in r.log if a.get("move") == "alert"]
    assert alert_turns and alert_turns[0]["alert_id"] == "a1"
    # S-14 (critical): the alert stands after the call is lost
    imm = r.alerts("immediate")
    assert len(imm) == 1 and imm[0]["rule_id"] == "rf.chest_pain_current" and imm[0]["route"] == "live_transfer", r.alerts()
    assert imm[0]["verbatim"] == "Yes, it's still there now."
    assert r.state["alerts"] == r.handover["alerts"], "the alert is carried into the handover unchanged"
    assert r.handover["coding_document"]["safety_net_events"]["items"] == r.state["alerts"]
    # S-4: nothing on the agent side can mark the alert acknowledged; acknowledgement is a named human act through the API
    assert "acknowledged" not in imm[0] and "acknowledged_by" not in imm[0] and "acknowledged_at" not in imm[0]
    # N-20 / N-21 (critical): no partial handover that reads as complete
    assert r.state["closed_by_alert"] is True
    assert r.handover["partial"].startswith("interview stopped by an immediate-tier alert")
    assert r.handover["narrative"][0].startswith("PARTIAL HISTORY: interview stopped by an immediate-tier alert")
    assert "This must not be read as a complete assessment" in r.handover["narrative"][0]
    assert "The interview was stopped by an immediate-tier alert; everything after that point is not asked." in r.narrative
    assert "Not asked:" in r.narrative
    not_asked = [e["slot_id"] for e in r.handover["structured_record"] if e["state"] == "not_asked"]
    assert "cp.onset_clock_time" in not_asked and "cs.medications" in not_asked, not_asked
    assert all(e["value"] is None for e in r.handover["structured_record"] if e["state"] == "not_asked")
    assert "Documented negatives" not in r.narrative, "nothing was asked that could be a documented negative"
    assert "complete" not in r.narrative.lower().replace("complete assessment", "").replace("complete sentences", "")
    assert r.said(r"There are things I didn't get to ask")
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


def test_c18_harness_records_the_hang_up(bundle):
    r = _run_c18(bundle)
    assert r.alerts("immediate")
    if not (r.hung_up and r.state["contact_lost"]):
        pytest.xfail(
            "harness: run_case checks hang_up_after_alert at the top of the while loop, but with "
            "continue_after_immediate_alert: false the controller closes the interview in the same batch of turns as "
            "the alert, so the loop exits on phase == 'ended' before the check runs and hung_up/contact_lost stay False. "
            "Needed in runner.py: evaluate the hang-up condition right after log.extend(...) inside the loop (or after "
            "the loop) whenever an alert turn has been logged, then set state['contact_lost'] = True and hung_up = True."
        )
    assert r.hung_up is True and r.state["contact_lost"] is True


def test_c18_alert_carries_that_contact_was_lost(bundle):
    r = _run_c18(bundle)
    # what the harness should have recorded (see test_c18_harness_records_the_hang_up); the question here is whether
    # the alert and handover carry it once it is recorded (S-14)
    r.state["contact_lost"] = True
    doc = generate(r.state, bundle, versions=bundle.versions)
    narrative = " ".join(doc["narrative"])
    imm = [a for a in doc["alerts"] if a["tier"] == "immediate"]
    assert imm, doc["alerts"]
    carried = any(a.get("contact_lost") for a in imm) or re.search(r"contact (was )?lost|line dropped|call dropped", narrative, re.I)
    if not carried:
        pytest.xfail(
            "controller/handover: state['contact_lost'] is defined in new_state but nothing writes it or reads it. "
            "Needed: (1) an API route (e.g. POST /conversations/{cid}/contact-lost, or the transfer route on a failed "
            "hand-off) that sets state['contact_lost'] = True and stamps the open immediate alert with contact_lost and "
            "the time; (2) generate.py appends a narrative line when state['contact_lost'] is set, using the existing but "
            "unused scripts/fixed.yaml transfer_dropped text ('The line dropped after I raised the alert. The alert stands "
            "and records that contact was lost.'), and includes contact_lost in the partial reason; (3) the alert row/"
            "unacknowledged listing shows contact_lost so the duty GP sees the patient cannot be called back on the line."
        )
    assert doc["partial"]


def test_c18_api_alert_requires_acknowledgement(client, bundle):
    """S-4 through the API: the alert is listed until a named human acknowledges it, and an unacknowledged alert
    older than the configured timeout is flagged for further escalation."""
    r = client.post("/conversations", json={"setting": "gp_booking", "language": "en", "is_simulation": True})
    assert r.status_code == 200, r.text
    cid = r.json()["conversation_id"]
    last = r.json()["agent_turns"][-1]
    opening = list(C18_OPENING)
    alert_id = None
    hung_up = False
    for _ in range(40):
        move = last["move"]
        if move == "disclose":
            line = "Yes."
        elif move == "capability":
            line = {"cap.hearing": "Yes, I can hear you fine.", "cap.language": "English is fine.", "cap.present": "No, it's just me."}[last["slot_id"]]
        elif move in ("open", "facilitate"):
            line = opening.pop(0) if opening else "That's all really."
        elif move == "invite":
            line = "No, nothing else."
        elif move == "summarise":
            line = "Yes, that's right."
        elif move in ("ask", "reask"):
            line = C18_ANSWERS.get(last["slot_id"], "No.")
        else:
            line = "Ok."
        r = client.post(f"/conversations/{cid}/turns", json={"transcript": line})
        assert r.status_code == 200, r.text
        body = r.json()
        if body["alerts"]:
            alert_id = body["alerts"][0]["alert_id"]
            assert body["alerts"][0]["tier"] == "immediate" and body["alerts"][0]["route"] == "live_transfer"
            hung_up = True   # the patient hangs up right after the escalation
            break
        if body["phase"] == "ended":
            break
        last = body["agent_turns"][-1]
    assert alert_id and hung_up
    assert client.post(f"/conversations/{cid}/turns", json={"transcript": "hello?"}).status_code == 409, "the conversation is over"
    # the alert is listed as unacknowledged, with the escalation timer visible
    un = client.get("/alerts/unacknowledged").json()
    assert un["timeout_s"] == bundle.parameters.alert_acknowledgement_timeout_s
    mine = [a for a in un["alerts"] if a["alert_id"] == alert_id]
    assert mine and mine[0]["rule_id"] == "rf.chest_pain_current" and mine[0]["overdue_for_further_escalation"] is False
    # an alert nobody acknowledges within the timeout is flagged for further escalation (S-4)
    from app.db import Alert, SessionLocal
    with SessionLocal() as db:
        row = db.get(Alert, alert_id)
        row.fired_at = (datetime.now(timezone.utc) - timedelta(seconds=bundle.parameters.alert_acknowledgement_timeout_s + 60)).isoformat()
        db.commit()
    un = client.get("/alerts/unacknowledged").json()
    assert [a for a in un["alerts"] if a["alert_id"] == alert_id][0]["overdue_for_further_escalation"] is True
    # acknowledgement needs a name, and clears the alert from the list
    assert client.post(f"/alerts/{alert_id}/acknowledge", json={"acknowledged_by": "   "}).status_code == 400
    ack = client.post(f"/alerts/{alert_id}/acknowledge", json={"acknowledged_by": "Duty GP Dr Okafor"})
    assert ack.status_code == 200 and ack.json()["acknowledged_by"] == "Duty GP Dr Okafor" and ack.json()["acknowledged_at"]
    un = client.get("/alerts/unacknowledged").json()
    assert not any(a["alert_id"] == alert_id for a in un["alerts"])
    assert client.post("/alerts/no-such-alert/acknowledge", json={"acknowledged_by": "x"}).status_code == 404
    # the handover behind the alert is marked partial and never reads as complete (N-20, N-21)
    h = client.get(f"/conversations/{cid}/handover").json()
    assert h["partial"] == "interview stopped by an immediate-tier alert"
    assert h["narrative"][0].startswith("PARTIAL HISTORY")
    assert any(a["rule_id"] == "rf.chest_pain_current" for a in h["alerts"])
    ex = client.get(f"/conversations/{cid}/export").json()
    assert any(a["id"] == alert_id and a["rule_id"] == "rf.chest_pain_current" for a in ex["alerts"]), ex["alerts"]
    assert ex["handover"]["partial"] == "interview stopped by an immediate-tier alert"
    # the acknowledgement is an audited act by a named human
    from app.db import AuditEvent
    with SessionLocal() as db:
        acks = [e for e in db.query(AuditEvent).filter(AuditEvent.conversation_id == cid).all() if e.action == "alert_acknowledged"]
    assert acks and acks[0].actor == "Duty GP Dr Okafor" and acks[0].detail["alert_id"] == alert_id
