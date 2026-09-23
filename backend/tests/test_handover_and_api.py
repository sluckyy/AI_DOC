from app.control.controller import Controller, new_state
from app.handover.generate import answer_clinician_question, generate
from app.process.rules import check_transcript
from tests.test_controller import SETTLED_ANSWERS, SETTLED_OPEN, run


def test_handover_from_slots_only(bundle):
    state, log = run(bundle, SETTLED_OPEN, SETTLED_ANSWERS)
    doc = generate(state, bundle, versions={"content": {"chest_pain": "0.1.0"}})
    text = " ".join(doc["narrative"]).lower()
    assert "presenting, in the patient's words" in text
    assert "documented negatives" in text
    assert "heart attack" not in text and "angina" not in text
    cd = doc["coding_document"]
    assert cd["diagnosis_block"]["principal_diagnosis"] is None
    assert cd["diagnosis_block"]["provenance"] == "clinician_only"
    assert cd["terminology"].startswith("SNOMED CT-AU")
    assert all(e["provenance"] in ("patient_reported", "structural") for e in doc["structured_record"])
    assert doc["safety_net_record"]["watch_for"]


def test_not_asked_never_reads_as_negative(bundle):
    state, _ = run(bundle, ["I've got chest pain right now."], SETTLED_ANSWERS)
    doc = generate(state, bundle)
    text = " ".join(doc["narrative"])
    assert "Not asked:" in text
    for e in doc["structured_record"]:
        if e["state"] == "not_asked":
            assert e["value"] is None


def test_clinician_question_answers_only_from_slots(bundle):
    state, log = run(bundle, SETTLED_OPEN, SETTLED_ANSWERS)
    turns = [{"role": r, "text": a["text"]} for r, a in log]
    ans = answer_clinician_question("What did they say about radiation to the arms?", state, bundle, turns)
    assert "both arms" in ans["answer"]
    ans = answer_clinician_question("Did they mention any rash on the legs?", state, bundle, turns)
    assert "didn't ask" in ans["answer"]


def test_process_checks_pass_on_scripted_conversation(bundle):
    state, log = run(bundle, SETTLED_OPEN, SETTLED_ANSWERS)
    turns = [({"role": "agent", **a} if r == "agent" else {"role": "person", "text": a["text"]}) for r, a in log]
    violations = check_transcript(turns, list(state["slot_values"].values()), state["alerts"], state)
    assert violations == [], violations


def test_api_end_to_end(client):
    r = client.post("/conversations", json={"setting": "ed", "language": "en", "consent": {"tone_adaptation": True}})
    assert r.status_code == 200, r.text
    cid = r.json()["conversation_id"]
    assert r.json()["agent_turns"][0]["move"] == "disclose"
    assert r.json()["agent_turns"][0]["visemes"]
    last = r.json()["agent_turns"][-1]
    open_lines = list(SETTLED_OPEN)
    for _ in range(60):
        move = last["move"]
        if move == "disclose":
            line = "Yes."
        elif move in ("open", "facilitate"):
            line = open_lines.pop(0) if open_lines else "That's all."
        elif move == "invite":
            line = "No, nothing else."
        elif move == "summarise":
            line = "Yes, that's right."
        elif move in ("ask", "reask"):
            line = SETTLED_ANSWERS.get(last["slot_id"], "Not sure.")
        elif move == "final_invite":
            line = "No."
        elif move == "read_back":
            line = "Yes."
        else:
            line = "Ok."
        r = client.post(f"/conversations/{cid}/turns", json={"transcript": line, "prosody": {"words_per_minute": 140}})
        assert r.status_code == 200, r.text
        if r.json()["phase"] == "ended":
            break
        last = r.json()["agent_turns"][-1]
    h = client.get(f"/conversations/{cid}/handover")
    assert h.status_code == 200
    assert h.json()["narrative"]
    cd = client.get(f"/conversations/{cid}/coding-document").json()["coding_document"]
    assert cd["diagnosis_block"]["principal_diagnosis"] is None
    q = client.post(f"/conversations/{cid}/clinician-questions", json={"question": "what did they say about sweating"}).json()
    assert "sweat" in q["answer"].lower()
    a = client.post(f"/conversations/{cid}/attest", json={"clinician": "Dr Test", "diagnosis_block": {"principal_diagnosis": "left for demo"}})
    assert a.status_code == 200
    ex = client.get(f"/conversations/{cid}/export").json()
    assert ex["process_check"] == []
    assert ex["attestations"][0]["clinician"] == "Dr Test"
    st = client.get("/content/status").json()
    assert st["authoring_checks"]["passed"]


def test_api_rejects_unconfigured_language(client):
    r = client.post("/conversations", json={"setting": "ed", "language": "de"})
    assert r.status_code == 400


def test_partial_handover_is_marked(bundle):
    from app.control.controller import Controller, new_state
    ctrl = Controller(bundle)
    state = new_state("ed", "en", {"ai_disclosure": True, "tone_adaptation": False, "summary_to_clinician": True})
    ctrl.start(state)
    ctrl.person_turn(state, "No, I want a person.")
    doc = generate(state, bundle)
    assert doc["partial"] and doc["narrative"][0].startswith("PARTIAL HISTORY")
    state, _ = run(bundle, ["I've got chest pain right now."], SETTLED_ANSWERS)
    doc = generate(state, bundle)
    assert "immediate-tier alert" in doc["partial"]


def test_alert_acknowledgement_flow(client):
    r = client.post("/conversations", json={"setting": "gp_booking", "language": "en"})
    cid = r.json()["conversation_id"]
    last = r.json()["agent_turns"][-1]
    alert_id = None
    for line in ["Yes.", "Yes I can hear you.", "English is fine.", "No, just me.", "I've got a tight pain in my chest right now.", "No.", "No.", "No.", "No.", "Yes that's right."]:
        r = client.post(f"/conversations/{cid}/turns", json={"transcript": line})
        assert r.status_code == 200, r.text
        if r.json()["alerts"]:
            alert_id = r.json()["alerts"][0]["alert_id"]
        if r.json()["phase"] == "ended":
            break
    assert alert_id
    un = client.get("/alerts/unacknowledged").json()
    assert any(a["alert_id"] == alert_id for a in un["alerts"])
    assert client.post(f"/alerts/{alert_id}/acknowledge", json={"acknowledged_by": ""}).status_code == 400
    ack = client.post(f"/alerts/{alert_id}/acknowledge", json={"acknowledged_by": "Duty GP Dr Nguyen"})
    assert ack.status_code == 200
    un = client.get("/alerts/unacknowledged").json()
    assert not any(a["alert_id"] == alert_id for a in un["alerts"])
    h = client.get(f"/conversations/{cid}/handover").json()
    assert h["partial"] and h["metadata"]["consent_timestamp"] and h["metadata"]["language"] == "en"


def test_reviewed_content_guard(bundle, monkeypatch):
    import pathlib as _p
    from app.content.loader import load_bundle
    monkeypatch.setenv("REQUIRE_REVIEWED_CONTENT", "true")
    root = _p.Path(__file__).resolve().parents[2] / "content"
    try:
        load_bundle(root)
        raised = False
    except RuntimeError as e:
        raised = "HAZ-8" in str(e)
    assert raised


def test_live_transfer_setup_and_content_reload(client):
    r = client.post("/conversations", json={"setting": "gp_booking", "language": "en"})
    cid = r.json()["conversation_id"]
    assert client.post(f"/conversations/{cid}/transfer").status_code == 409, "no alert yet"
    for line in ["Yes.", "Yes I can hear you.", "English is fine.", "No, just me.", "I've got a tight pain in my chest right now.", "No.", "No.", "No.", "No.", "Yes that's right."]:
        r = client.post(f"/conversations/{cid}/turns", json={"transcript": line})
        if r.json()["phase"] == "ended":
            break
    t = client.post(f"/conversations/{cid}/transfer")
    assert t.status_code == 200, t.text
    assert t.json()["route"] == "live_transfer" and t.json()["alert"]["tier"] == "immediate"
    rl = client.post("/content/reload")
    assert rl.status_code == 200 and rl.json()["reloaded"] and rl.json()["authoring_checks"]["passed"]


def test_disabled_module_is_listed_but_never_runs(client):
    """D-52: a module with enabled: false stays in the repository, is reported on the status page, and never activates."""
    s = client.get("/content/status").json()
    assert "mental_health" in s["disabled_modules"], s["disabled_modules"]
    assert all(m["module"] != "mental_health" for m in s["modules"])
    assert "haematuria_referral_age" in s["clinical_parameters"]
    assert s["clinical_parameters"]["haematuria_referral_age"]["status"] == "pending"
    r = client.post("/conversations", json={"setting": "ed", "language": "en"})
    cid = r.json()["conversation_id"]
    for line in ["Yes.", "Yes I can hear you.", "English is fine.", "No, just me.", "I've been feeling really low and I can't cope."]:
        client.post(f"/conversations/{cid}/turns", json={"transcript": line})
    state = client.get(f"/conversations/{cid}").json()["state"]
    assert "mental_health" not in state.get("module_queue", [])
