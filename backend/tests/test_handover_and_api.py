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
