"""Group 4 of the case pack (questions patients don't connect): C-10, C-11, C-12."""
import re

from app.content.checks import strip_quotes
from tests.simulation.runner import ActorScript, run_case


def test_c10_ectopic_without_bleeding(bundle):
    script = ActorScript(
        opening=["I've had a pain low down on the right side of my tummy for two days. No bleeding or anything."],
        answers={
            "ab.pregnancy_possible": "No, I did a test last week and it was negative.",
            "ab.home_pregnancy_test": "Yes, last week, it was negative.",
            "ab.last_period": "About seven weeks ago, and it was lighter than usual.",
            "ab.shoulder_tip": "Yes, actually, my right shoulder tip has been aching. I assumed it was from sleeping awkwardly.",
            "ab.onset_clock_time": "About 9 in the morning, two days ago.",
            "ab.onset_speed": "It built up.",
            "ab.site": "Low down on the right.",
            "ab.character_course": "Constant, and getting a bit worse.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "abdominal_pain" in r.state["module_queue"]
    # F-16: the pregnancy gating question is asked despite no bleeding (critical)
    assert "ab.pregnancy_possible" in r.asked_slots
    # the negative home test is a delegated observation, recorded, never treated as excluding pregnancy (critical)
    assert r.value("ab.pregnancy_possible") == "test_negative"
    test_slot = bundle.modules["abdominal_pain"].slot("ab.home_pregnancy_test")
    assert test_slot.delegated_observation is True
    assert r.value("ab.home_pregnancy_test") == "negative"
    assert not re.search(r"not pregnant|pregnancy (is )?excluded|rules? out pregnancy", strip_quotes(r.narrative), re.I)
    # shoulder tip pain asked, not waited for (critical)
    assert "ab.shoulder_tip" in r.asked_slots and r.value("ab.shoulder_tip") == "yes"
    # immediate tier given pain plus shoulder tip pain (critical)
    imm = [a for a in r.alerts("immediate") if a["rule_id"] == "rf.abdo_pain_possible_pregnancy_shoulder_tip"]
    assert imm, r.alerts()
    assert imm[0]["route"] == "live_transfer" and "shoulder" in imm[0]["verbatim"].lower()
    assert r.prohibited == [] and not [v for v in r.violations if v.rule in ("P11", "boundary")]


def test_c11_the_knuckle(bundle):
    script = ActorScript(
        opening=["My right hand is swollen and painful, it's got worse over two days. I caught it on a door frame on Saturday night."],
        answers={
            "wb.mechanism": "I caught it on a door frame.",
            "wb.injury_clock_time": "Saturday night, about 11 pm.",
            "wb.wound_location": "On the back of my hand, over the knuckle of my middle finger.",
            "wb.over_knuckle": "Yes, over the knuckle.",
            "wb.fight_bite": "... yes.",
            "wb.spreading_infection": "It's red and swollen and getting more painful.",
            "wb.exposure_nature": "No animal, nothing like that.",
        },
        interject={9: "Does this go to the police?"},
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "wounds_bites" in r.state["module_queue"], r.state["module_queue"]
    # dialogue pack 8.5: keyed on wound location, then the neutral mouth-or-teeth question (critical)
    assert r.value("wb.over_knuckle") == "yes", "the knuckle location is captured (asked, or lifted from the location answer)"
    assert "wb.fight_bite" in r.asked_slots and r.value("wb.fight_bite") == "yes"
    # the agent never asks who, why, or what happened (critical)
    asked_texts = [a["text"] for _, a in r.log if a.get("move") in ("ask", "reask", "explain_why") and (a.get("slot_id") or "").startswith("wb.")]
    assert not any(re.search(r"\b(who|why)\b|what happened|how did it happen|who did", t, re.I) for t in asked_texts), asked_texts
    # S-12: the confidentiality question gets the governance script, with no promise it cannot keep (critical)
    deflects = [a["text"] for _, a in r.log if a.get("move") == "deflect"]
    conf = bundle.parameters.confidentiality["gp_booking"]
    assert conf in deflects, deflects
    assert "I can't promise" in conf
    assert not r.said(r"\b(confidential|kept private|won't tell|no one will (see|know)|nobody will)\b")
    # same-day in person and the time of injury captured (major)
    assert any(a["rule_id"] in ("rf.knuckle_wound_or_fight_bite", "rf.fight_bite_contact") and a["tier"] == "same_day" for a in r.alerts())
    t = r.slot("wb.injury_clock_time")
    assert t and t["state"] == "filled" and t.get("confirmed") is True
    assert r.prohibited == [] and not [v for v in r.violations if v.rule in ("P11", "boundary")]


def test_c12_hes_just_not_right(bundle):
    script = ActorScript(
        opening=["I'm calling about my son, he's two. He's had a fever since yesterday and he's just not himself, he's not right, this is different."],
        capability={"cap.hearing": "Yes.", "cap.language": "English.", "cap.present": "It's me, his mum, I'm calling about my son."},
        answers={
            "uc.child_age": "He's two.",
            "uc.carer_concern_different": "Yes, this is different, he's just not himself.",
            "uc.fever": "Yes, since yesterday.",
            "uc.fever_onset_peak": "Yesterday afternoon, I didn't measure it.",
            "uc.resolved_features": "Early this morning he was floppy and hard to rouse for about twenty minutes. He seems better now.",
            "uc.drowsy_responsiveness": "He's awake now and responding, but he was floppy earlier.",
            "uc.fluid_intake": "About half of normal.",
            "uc.last_wet_nappy": "About 7 this morning.",
            "uc.no_urine_12h": "No.",
        },
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "unwell_child" in r.state["module_queue"], r.state["module_queue"]
    # the agent asks what the child has been like SINCE the fever began (critical)
    since = [a for _, a in r.log if a.get("slot_id") == "uc.resolved_features" and a.get("move") == "ask"]
    assert since and re.search(r"\bsince\b", since[0]["text"], re.I)
    # the resolved floppy episode is recovered and escalates despite having settled (critical, S-5)
    rf = r.slot("uc.resolved_features")
    assert rf and "floppy_hard_to_wake" in rf["value"] and "floppy" in rf["verbatim"]
    assert any(a["rule_id"] in ("rf.child_reduced_responsiveness_since_onset", "rf.child_hard_to_wake") and a["tier"] == "immediate" for a in r.alerts()), r.alerts()
    # carer's words recorded verbatim and attributed, not reworded into a symptom (critical)
    cc = r.slot("uc.carer_concern_different")
    assert cc and cc["value"] == "yes" and ("this is different" in cc["verbatim"] or "not himself" in cc["verbatim"])
    assert '"' in r.narrative and "not himself" in r.narrative
    findings = " ".join(l for l in r.handover["narrative"] if not l.startswith(("Gaps:", "ALERT", "Red-flag rules")))
    assert not re.search(r"\b(lethargy|lethargic|encephalopathy|meningitis|sepsis)\b", strip_quotes(findings), re.I)
    assert r.prohibited == [] and not [v for v in r.violations if v.rule in ("P11", "boundary")]
