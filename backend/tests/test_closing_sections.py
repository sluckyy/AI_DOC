"""The closing sections (D-37, D-38, D-39, D-40, D-44, D-47): medicines per item, five past-history routes with a
lay-anchored sweep, family history in three states with named thresholds, situational items only where a recipient
exists and with per-item pass-on consent, the systems review routing positives to their modules, and the D-44 handover order."""
import re

from app.control.controller import Controller
from app.handover.generate import generate
from tests.simulation.runner import ActorScript, run_case


SAFE = {"cw.sentences": "Yes, easily.", "cw.haemoptysis_screen": "No blood, never.", "hd.thunderclap": "No, it built up slowly.",
        "hd.worst_ever": "No.", "cp.current": "No, it's gone now."}


def _sections(bundle):
    return [n for n, m in bundle.modules.items() if m.kind == "closing"]


def test_sections_load_in_order(bundle):
    names = _sections(bundle)
    assert names == ["review_of_systems", "medications", "past_history", "family_history", "functional_situational", "social_history"], names


def test_split_items_keeps_uncertain_descriptions():
    items = Controller._split_items("I take a few things. There's one for my sugar, metformin I think, and a little white one for my heart, I don't know the name of it.")
    assert any("metformin" in i for i in items)
    assert any("white one for my heart" in i for i in items)
    assert not any(i.lower().startswith("i don't know") for i in items)
    assert Controller._split_items("No, nothing.") == []


def test_medicines_are_asked_per_item_and_none_is_a_value(bundle):
    script = ActorScript(
        opening=["I've had a cough for three weeks."],
        answers={
            **SAFE, "md.list": "Metformin, and amlodipine for blood pressure.",
            "md.per_medicine#0": "Five hundred milligrams twice a day, for my sugar, the GP started it, I don't miss it.",
            "md.per_medicine#1": "One a day, five milligrams, for blood pressure. Sometimes I forget it.",
            "md.allergies": "No allergies that I know of.",
            "pm.self_label": "Diabetes and blood pressure.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert r.state["repeat_items"]["md.per_medicine"] == ["Metformin", "amlodipine for blood pressure"]
    assert r.slot("md.per_medicine#0")["item"] == "Metformin" and "twice a day" in r.slot("md.per_medicine#0")["verbatim"]
    assert r.slot("md.per_medicine#1")["item"].startswith("amlodipine")
    assert r.value("md.allergies") == "none", "a 'none that I know of' answer is the value none, not free text"
    assert "md.allergy_reaction" not in r.asked_slots, "the reaction branch does not apply when there is no allergy"
    # the named-condition sweep skips conditions that already surfaced (hypertension via amlodipine, diabetes via metformin)
    asked = set(r.asked_slots)
    assert "pm.hypertension" not in asked and "pm.diabetes" not in asked, sorted(a for a in asked if a.startswith("pm."))
    assert r.slot("pm.hypertension")["state"] == "not_applicable"
    assert "pm.heart_failure" in asked
    # per-item lines and the bring-your-medicines close in the GP setting
    assert any("per item" in line and "Metformin" in line for line in r.handover["narrative"]), r.handover["narrative"]
    assert r.said(r"bring all your medicines")
    meds = r.handover["coding_document"]["medications"]["items"]
    assert any(e["slot_id"] == "md.per_medicine#0" and e.get("item") == "Metformin" for e in meds)


def test_family_history_three_states_and_threshold(bundle):
    script = ActorScript(
        opening=["I've had a headache for a week."],
        answers={
            **SAFE, "fh.knowledge": "Yes, I know it fairly well.",
            "fh.core": "My dad and my brother both had bowel cancer, and my aunt on my mum's side had breast cancer in her seventies.",
            "fh.crc_first_degree_count": "Two.",
            "fh.crc_youngest_age": "My brother was 48.",
            "fh.breast_first_degree_count": "None, that was my aunt.",
            "fh.breast_youngest_age": "About 72.",
            "fh.sah_pkd": "I don't know, we never talked about that.",
            "fh.cvd_premature": "No.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="ed")
    assert r.value("fh.crc_first_degree_count") == 2 and r.value("fh.crc_youngest_age") == 48
    sah = r.slot("fh.sah_pkd")
    assert sah and sah["state"] == "unknown", "'I don't know' is the third state, distinct from no"
    pattern = r.handover["coding_document"]["family_history"]["pattern"]
    assert any("Category 2" in p for p in pattern), pattern
    assert any("Family history pattern" in line and "Category 2" in line for line in r.handover["narrative"])
    assert any("asked; the patient did not know" in line for line in r.handover["narrative"])


def test_adopted_patient_closes_the_family_section_gracefully(bundle):
    script = ActorScript(opening=["I've had a cough for three weeks."], answers={**SAFE, "fh.knowledge": "I'm adopted, I don't know anything about them."}, default="No.")
    r = run_case(bundle, script, setting="ed")
    assert r.value("fh.knowledge") == "adopted_or_estranged"
    assert "fh.core" not in r.asked_slots
    assert any("not known to the patient" in line and "'unknown', not 'negative'" in line for line in r.handover["narrative"])


def test_situational_items_need_a_recipient_and_pass_on_consent(bundle):
    script = ActorScript(
        opening=["I've had a cough for three weeks."],
        answers={
            **SAFE, "fn.transport": "Getting in is hard, I don't drive and the bus is twice a day.",
            "so.context": "My husband has dementia and I can't leave him for long.",
            "so.context.pass_on": "No, I'd rather you didn't pass that on.", "fn.transport.pass_on": "Yes, that's fine.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "fn.transport" in r.asked_slots, "a recipient is configured, so transport is asked"
    ctx = r.slot("so.context")
    assert ctx and ctx.get("pass_on") is False and "dementia" in ctx["verbatim"]
    assert r.slot("fn.transport").get("pass_on") is True
    assert "Getting in is hard" in r.narrative and "(patient agreed to pass this on)" in r.narrative
    assert "dementia" not in r.narrative, "a declined item never reaches the narrative"
    assert any("Withheld at the patient's request" in line for line in r.handover["narrative"])
    entry = next(e for e in r.handover["structured_record"] if e["slot_id"] == "so.context")
    assert entry["state"] == "withheld_by_patient" and entry["value"] is None and entry["verbatim"] is None
    export_text = " ".join(str(e) for e in r.handover["coding_document"]["social_and_functional"]["items"])
    assert "dementia" not in export_text


def test_situational_item_not_asked_without_a_recipient(bundle):
    m = bundle.modules["functional_situational"]
    ctrl = Controller(bundle)
    slot = m.slot("fn.accommodation")
    assert slot.recipient_key == "accommodation"
    saved = bundle.parameters.situational_recipients.get("accommodation")
    try:
        bundle.parameters.situational_recipients["accommodation"] = None
        assert ctrl._applies({"module_queue": [], "slot_values": {}}, slot, "closing") is False
    finally:
        bundle.parameters.situational_recipients["accommodation"] = saved


def test_review_of_systems_routes_a_positive_and_reconciles_known_ones(bundle):
    script = ActorScript(
        opening=["I've had a cough for three weeks."],
        answers={**SAFE, "ros.cardiorespiratory": "I've had some chest pain actually, and the cough."},
        default="No.",
    )
    r = run_case(bundle, script, setting="ed")
    assert "chest_pain" in r.state["module_queue"], r.state["module_queue"]
    q = r.state["module_queue"]
    assert q.index("chest_pain") > q.index("review_of_systems") and q.index("chest_pain") < q.index("medications")
    assert any(e["module"] == "chest_pain" for e in r.state["ros_elicited"])
    assert not any(e["module"] == "cough_wheeze" and e["option"] != "cough" for e in r.state["ros_elicited"])
    assert any(p.get("pulled_by") == "review_of_systems" for p in r.state["problems"])
    assert any("Routed from the systems review" in line for line in r.handover["narrative"])
    assert not re.search(r"unremarkable|no red flags", r.narrative, re.I)


def test_handover_order_presenting_first_past_history_later(bundle):
    script = ActorScript(
        opening=["I've had a cough for three weeks."],
        answers={**SAFE, "pm.self_label": "Schizophrenia, and high blood pressure.", "md.list": "Olanzapine and ramipril.", "fn.delta": "Nothing has changed."},
        default="No.",
    )
    r = run_case(bundle, script, setting="ed")
    lines = r.handover["narrative"]
    first_finding = next(i for i, l in enumerate(lines) if l.startswith("Cough or wheeze:"))
    pmh = next(i for i, l in enumerate(lines) if "Schizophrenia" in l)
    assert first_finding < pmh, "the presenting complaint opens the summary; past history follows (D-44)"
    assert "Schizophrenia" not in lines[0] and "Schizophrenia" not in lines[1]
    assert not re.search(r"\b(known|history of) schizophreni", r.narrative, re.I), "a psychiatric diagnosis is never a framing descriptor"


def test_closing_sections_swept_after_an_immediate_alert(bundle):
    script = ActorScript(opening=["I've got a tight pain in my chest right now."], default="No.")
    r = run_case(bundle, script, setting="ed")
    assert r.alerts("immediate")
    md = r.slot("md.list")
    assert md and md["state"] == "not_asked"
    assert any("Not asked:" in line for line in r.handover["narrative"])
