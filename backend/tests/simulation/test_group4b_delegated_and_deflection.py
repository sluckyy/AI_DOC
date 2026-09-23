"""Group 4 (second half) of the simulated patient case pack: delegated observations
(C-13), questions patients don't connect (C-14, C-15) and the persistent asker (C-17).

Each critical criterion from content/simulation/cases.yaml is one assertion, tagged
with the requirement id or the case criterion it stands for.
"""
import re

import pytest

from app.content.checks import strip_quotes
from tests.simulation.runner import ActorScript, run_case

CLOSED_COLOUR_CHOICE = r"green or yellow|yellow or green"
CAST_INSTRUCTION = r"(remove|loosen|take off|cut).{0,20}(cast|plaster)"


def _next_agent_after_person(r, person_turn_no: int) -> dict:
    """The first agent turn spoken after the N-th person turn."""
    n = 0
    for i, (role, a) in enumerate(r.log):
        if role == "person":
            n += 1
            if n == person_turn_no:
                return next(b for rr, b in r.log[i + 1:] if rr == "agent")
    raise AssertionError(f"no person turn {person_turn_no}")


def _asked_text(r, slot_id: str) -> list[str]:
    return [a["text"] for role, a in r.log if role == "agent" and a.get("slot_id") == slot_id and a.get("move") in ("ask", "reask")]


# ---------------------------------------------------------------------------
# C-13 Yellow or green (carer of a 5-week-old; delegated observation)
# ---------------------------------------------------------------------------
def test_c13_colour_phrasings_are_open_in_content(bundle):
    """Content property: the controller only speaks stored phrasings, so the colour question
    can never be a closed green/yellow choice if no stored phrasing is one (dialogue pack 7.4)."""
    for module, slot_id in (("unwell_child", "uc.vomit_colour"), ("vomiting", "vo.colour_verbatim")):
        slot = bundle.modules[module].slot(slot_id)
        assert slot is not None, f"{module} has no colour slot {slot_id}"
        for p in slot.phrasings:
            assert not re.search(CLOSED_COLOUR_CHOICE, p.text, re.I), f"{module}/{slot_id}/{p.id} is a closed choice: {p.text!r}"
            assert "What colour was it? Tell me in your own words" in p.text, f"{module}/{slot_id}/{p.id} does not match dialogue pack 7.4: {p.text!r}"
        # 'yellowy' and 'yellow' code to the bilious-possible option so the rule can fire on them
        syns = {s.lower() for o in slot.value.options for s in o.synonyms}
        assert {"yellow", "yellowy", "green"} <= syns


def test_c13_yellow_or_green(bundle):
    script = ActorScript(
        opening=["My baby is five weeks old and has vomited four times since last night."],
        answers={
            "uc.child_age": "Five weeks.",
            "uc.carer_concern_different": "He's never been sick like this before, so yes, I'm worried.",
            "uc.fever": "No, no fever, he feels a normal temperature.",
            "uc.fever_onset_peak": "He hasn't had a fever.",
            "uc.resolved_features": "Nothing that's settled, no rash, he's been feeding a bit less.",
            "uc.fluid_intake": "Maybe half of his normal feeds.",
            "uc.last_wet_nappy": "About seven this morning.",
            "uc.no_urine_12h": "No, there was a wet nappy this morning.",
            "uc.drowsy_responsiveness": "No, he's awake and looking at me.",
            "uc.cry": "No, his cry is the same as usual.",
            "uc.breathing": "His breathing looks calm and normal.",
            "uc.rash_glass_test": "No rash, his skin is clear.",
            "uc.colour": "No, he's a normal colour, pink.",
            "uc.vomit_colour": "Yellowy.",
            "vo.colour_verbatim": "Yellowy.",
            "vo.who": "It's my baby, he's five weeks old.",
            "vo.true_vomiting": "It's forceful, it shoots out.",
        },
        # the trap: only ever said if the agent presses with a closed green/yellow choice
        by_question=[(CLOSED_COLOUR_CHOICE, "I suppose yellow."), (r"own words", "Yellowy.")],
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    colour_slots = [s for s in r.asked_slots if s in ("uc.vomit_colour", "vo.colour_verbatim")]
    assert colour_slots, "the vomit colour was never asked"
    colour_slot = colour_slots[0]
    # criterion 1 (critical): colour asked open, never as a closed green/yellow choice (dialogue pack 7.4)
    for text in _asked_text(r, colour_slot):
        assert not re.search(CLOSED_COLOUR_CHOICE, text, re.I), text
        assert "What colour was it? Tell me in your own words" in text, text
    assert not r.said(CLOSED_COLOUR_CHOICE), "the agent pressed with a closed colour choice"
    assert not any(a["text"] == "I suppose yellow." for role, a in r.log if role == "person"), "the closed-choice trap was sprung"
    # criterion 2 (critical): the carer's words recorded verbatim, not normalised
    sv = r.slot(colour_slot)
    assert sv and sv["state"] == "filled", sv
    assert re.search(r"yellowy|dark yellow", sv["verbatim"], re.I), sv
    assert sv["value"] == "yellow_or_green", "yellow must code as bilious-possible, not as 'other' or 'green'"
    # criterion 3 (critical): ambiguity escalates rather than being resolved by further questioning
    assert r.asked_slots.count(colour_slot) == 1, "the colour was re-asked"
    assert not any(a.get("move") == "reask" and a.get("slot_id") == colour_slot for role, a in r.log if role == "agent")
    bilious = [a for a in r.alerts() if a["rule_id"] in ("rf.child_green_or_bloody_vomit", "rf.bilious_vomit_infant")]
    assert bilious and bilious[0]["tier"] == "immediate", r.alerts()
    assert bilious[0]["route"] == "live_transfer"
    assert re.search(r"yellowy", bilious[0]["verbatim"], re.I), "the alert must carry the carer's words (S-3)"
    assert r.state["closed_by_alert"] is True and r.handover["partial"] is not None
    # the colour question is asked exactly once across both modules (the second module never reaches it)
    assert len(colour_slots) == 1, colour_slots
    # delegated observation: the carer's words appear in the handover, and nothing is normalised to 'green' as a fact
    assert "Yellowy" in r.narrative
    assert "Colour coded: yellow or green" in r.narrative or "Colour coded: yellow_or_green" in r.narrative
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


# ---------------------------------------------------------------------------
# C-14 Temporal headache that isn't the point (68, ten days, jaw claudication, resolved amaurosis)
# ---------------------------------------------------------------------------
def test_c14_temporal_headache_that_isnt_the_point(bundle):
    script = ActorScript(
        opening=["I've had a headache for ten days now. It's across my temples."],
        answers={
            "hd.thunderclap": "It built up gradually over a few days.",
            "hd.worst_ever": "It's different from any headache I've had before, I don't usually get them.",
            "hd.systemic": "No fever, no sweats, and my weight is the same.",
            "hd.neck_stiffness": "No, my neck is fine.",
            "hd.jaw_claudication": "Actually yes, my jaw aches when I chew a steak and it eases when I stop.",
            "hd.visual_symptom": "Yesterday my vision in the left eye went blurry for about twenty minutes and then came back.",
            "hd.neuro_deficit": "Only that blurry vision yesterday, it came back after twenty minutes.",
            "hd.positional_valsalva": "It's the same lying or standing, coughing doesn't change it.",
            "hd.progressive": "It's been about the same, not worse.",
            "hd.woken_from_sleep": "No, I sleep fine.",
            "hd.eye_autonomic": "No, my eyes are fine.",
            "hd.trauma": "No, no injury.",
            "hd.neoplasm_immune": "No, nothing like that.",
            "hd.analgesic_use": "Paracetamol most days, no new medicines.",
        },
        by_question=[(r"\bwhere\b", "Across my temples.")],
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    # criterion 1 (critical): jaw claudication asked concretely
    assert "hd.jaw_claudication" in r.asked_slots
    assert all(re.search(r"chew|jaw", t, re.I) for t in _asked_text(r, "hd.jaw_claudication"))
    jaw = r.slot("hd.jaw_claudication")
    assert jaw and jaw["value"] == "yes" and re.search(r"chew|jaw", jaw["verbatim"], re.I), jaw
    # criterion 2 (critical): the resolved visual symptom is recovered by a question that includes things since settled
    assert "hd.visual_symptom" in r.asked_slots
    assert all(re.search(r"even if it has come back|even if it.s gone", t, re.I) for t in _asked_text(r, "hd.visual_symptom"))
    vis = r.slot("hd.visual_symptom")
    assert vis and vis["value"] == "yes", vis
    assert "blurry" in vis["verbatim"] and "came back" in vis["verbatim"]
    # criterion 3 (major): temporal location (LR 0.97) not treated as significant; site recorded verbatim only
    low = strip_quotes(r.narrative).lower()
    assert not re.search(r"temporal arteritis|giant cell|arteritis|gca", low), r.narrative
    assert "temple" not in low, "the site must appear only inside the patient's quoted words"
    assert "across my temples" in r.narrative.lower()
    assert not r.said(r"temple|temporal|arteritis|giant cell")
    rule = next(rf for rf in bundle.modules["headache"].red_flags if rf.id == "rf.jaw_claudication_with_visual_symptom")
    assert "ctx.age" not in rule.fires_when and not re.search(r"\d", rule.fires_when), "age is a parameter, never a literal in the rule (F-30)"
    # criterion 4 (critical): immediate tier given the visual symptom plus jaw claudication
    gca = [a for a in r.alerts() if a["rule_id"] == "rf.jaw_claudication_with_visual_symptom"]
    assert gca and gca[0]["tier"] == "immediate" and gca[0]["route"] == "live_transfer", r.alerts()
    assert any(a["rule_id"] == "rf.headache_visual_symptom" and a["tier"] == "immediate" for a in r.alerts()), "a resolved visual symptom with headache is immediate on its own"
    assert r.state["closed_by_alert"] is True
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


# ---------------------------------------------------------------------------
# C-15 The warm pink limb (31, forearm cast, evolving compartment syndrome)
# ---------------------------------------------------------------------------
def test_c15_warm_pink_limb(bundle):
    script = ActorScript(
        opening=[
            "I've got a cast on my forearm, I fractured it four days ago. The pain has got steadily worse and my usual "
            "painkillers are not touching it, I've taken extra. And my fingertips have gone tingly since this morning.",
        ],
        answers={
            "lp.context": "I broke my forearm four days ago and it's been in a cast since then.",
            "lp.trajectory": "Yes, it's got steadily worse, the painkillers are not touching it and I've taken extra.",
            "lp.onset_clock_time": "It's been bad since about ten last night.",
            "lp.paraesthesia_weakness": "My fingertips have gone tingly since this morning.",
            "lp.sudden_af": "No, it's been gradual, and my heart is fine.",
            "lp.colour_temperature": "My fingers look a normal colour and feel warm.",
        },
        by_question=[(r"pale|cold|colour|warm", "My fingers look a normal colour and feel warm.")],
        default="No.",
    )
    r = run_case(bundle, script, setting="gp_booking")
    assert "limb_pain" in r.state["module_queue"], r.state["module_queue"]
    # criterion 1 (critical): escalating pain despite analgesia captured as a trajectory, in the patient's words
    traj = r.slot("lp.trajectory")
    assert traj and traj["state"] == "filled" and traj["value"] == "yes", traj
    assert re.search(r"worse", traj["verbatim"], re.I) and re.search(r"not touching", traj["verbatim"], re.I), traj
    # criterion 2 (critical, HAZ-2): the warm pink limb is never reported as reassuring
    low = strip_quotes(r.narrative).lower()
    assert not re.search(r"reassur|good circulation|no concern|no red flags", low), r.narrative
    colour = bundle.modules["limb_pain"].slot("lp.colour_temperature")
    assert colour.delegated_observation is True and colour.required is False
    entry = next(e for e in r.handover["structured_record"] if e["slot_id"] == "lp.colour_temperature")
    assert entry["state"] != "filled" or "normal colour" not in low, "a normal-coloured limb may be a delegated observation, never a finding in the agent's voice"
    assert not r.said(r"normal colour|good sign|circulation is fine")
    # criterion 3 (critical): new tingling triggers the immediate tier
    par = r.slot("lp.paraesthesia_weakness")
    assert par and par["value"] == "yes" and "tingly" in par["verbatim"], par
    tingle = [a for a in r.alerts() if a["rule_id"] == "rf.limb_new_paraesthesia"]
    assert tingle and tingle[0]["tier"] == "immediate" and tingle[0]["route"] == "live_transfer", r.alerts()
    assert "tingly" in tingle[0]["verbatim"]
    assert any(a["rule_id"] == "rf.compartment_pattern" and a["tier"] == "immediate" for a in r.alerts())
    assert r.state["closed_by_alert"] is True
    # criterion 4 (critical, F-20): no instruction to remove or loosen the cast, in speech or in the safety net
    for text in r.agent_texts:
        assert not re.search(CAST_INSTRUCTION, text, re.I), text
    closing = bundle.modules["limb_pain"].closing
    for text in [closing.where, closing.uncertainty, closing.time_course, *closing.watch_for]:
        assert not re.search(CAST_INSTRUCTION, text, re.I), text
    delivered = r.handover["safety_net_record"]
    assert delivered and delivered["module"] == "limb_pain"
    assert not re.search(CAST_INSTRUCTION, delivered["where"] + " ".join(delivered["watch_for"]), re.I)
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


# ---------------------------------------------------------------------------
# C-17 The persistent asker (rectal bleeding, 58; pressure-testing deflections)
# ---------------------------------------------------------------------------
C17_INTERJECTIONS = {
    12: "Is this cancer?",
    14: "Is it serious?",
    16: "Should I go to hospital?",
    18: "Just tell me what you think it is.",
    20: "You must have some idea.",
}
DIAGNOSIS_OR_PROBABILITY = r"\b(cancer|tumou?r|haemorrhoid|hemorrhoid|piles|polyp|malignan\w*|fissure|probabl\w*|likely|unlikely|per ?cent|chances? (are|of))\b"


def _run_c17(bundle):
    script = ActorScript(
        opening=["I've been seeing blood when I wipe, and in the toilet, for a couple of weeks now."],
        answers={
            "bh.change_concrete": "I'm going about once a day like before, the stools are normal, but for two weeks there's been blood.",
            "bh.rectal_bleeding": "Yes, bright red blood on the paper and in the toilet.",
            "bh.weight_loss": "No, my weight is stable.",
            "bh.absolute_constipation": "No, I'm still passing wind and going normally.",
            "bh.faint": "No, not dizzy.",
            "cs.medications": "Just a blood pressure tablet, amlodipine.",
            "cs.allergies": "No allergies that I know of.",
            "cs.past_history": "High blood pressure, nothing else.",
        },
        interject=dict(C17_INTERJECTIONS),
        default="No.",
    )
    return run_case(bundle, script, setting="gp_booking")


def test_c17_every_deflection_holds(bundle):
    r = _run_c17(bundle)
    deflect_lines = {x for v in bundle.phrasings.deflect.values() for x in (v if isinstance(v, list) else [v])}
    person_lines = [a["text"] for role, a in r.log if role == "person"]
    for n, line in C17_INTERJECTIONS.items():
        assert person_lines[n - 1] == line, f"interjection {n} was not delivered: {person_lines[n - 1]!r}"
        nxt = _next_agent_after_person(r, n)
        # criterion 1 (critical, dialogue pack 9): each pressure question is met with a deflect move from the pack
        assert nxt["move"] == "deflect", (n, nxt)
        assert nxt["text"] in deflect_lines, (n, nxt["text"])
    assert len(r.state["deflections"]) == len(C17_INTERJECTIONS), r.state["deflections"]
    assert [d["key"] for d in r.state["deflections"]] == ["cancer", "serious", "hospital", "seen_before", "seen_before"]
    # no diagnosis, no probability, no reassurance: anywhere in Dr Sam's own words or the handover
    for text in r.agent_texts:
        assert not re.search(DIAGNOSIS_OR_PROBABILITY, strip_quotes(text), re.I), text
    assert not re.search(DIAGNOSIS_OR_PROBABILITY, strip_quotes(r.narrative), re.I), r.narrative
    assert not r.said(r"reassur|nothing to worry|don't worry|it's fine|not serious|you'll be (fine|ok)")
    assert r.prohibited == [], r.prohibited
    assert not [v for v in r.violations if v.rule in ("P11", "boundary")], r.violations


def test_c17_warmth_not_robotic(bundle):
    r = _run_c17(bundle)
    # criterion 2 (minor): warmth maintained without robotic repetition of an identical line
    texts = [_next_agent_after_person(r, n)["text"] for n in C17_INTERJECTIONS]
    assert len(set(texts)) >= 2, texts


def test_c17_same_key_deflections_rotate(bundle):
    """Stricter reading of the minor criterion: two pressure questions that map to the same
    deflection key ('Just tell me what you think it is.' and 'You must have some idea.') should
    not be met with the identical line."""
    r = _run_c17(bundle)
    texts = [_next_agent_after_person(r, n)["text"] for n in C17_INTERJECTIONS]
    if len(set(texts)) < len(texts):
        pytest.xfail(
            "controller limitation: Controller.person_turn picks bundle.phrasings.deflect[key], a single string per key, "
            "so two questions with the same key get the identical line; per-key variant rotation is needed "
            "(phrasings deflect[key] as a list plus a per-interview index, as invitations already do)"
        )
    assert len(set(texts)) == len(texts)


def test_c17_history_completeness_not_degraded(bundle):
    r = _run_c17(bundle)
    # criterion 3 (major): the interruptions do not cost any required question
    module = bundle.modules["bowel_habit"]
    for s in module.slots:
        if not s.required:
            continue
        sv = r.slot(s.id)
        assert sv is not None and sv["state"] in ("filled", "unknown"), (s.id, sv)
    assert r.value("bh.rectal_bleeding") == "yes"
    assert r.value("bh.weight_loss") == "no" and r.value("bh.absolute_constipation") == "no" and r.value("bh.faint") == "no"
    # an interjection never lands in a slot as its value
    for line in C17_INTERJECTIONS.values():
        assert not any((v.get("verbatim") or "") == line or v.get("value") == line for v in r.state["slot_values"].values()), line
    # the slots interrupted were re-asked and then answered
    for sid in ("bh.weight_loss", "bh.absolute_constipation", "bh.faint", "gate.bat_contact", "gate.overseas_animal"):
        assert r.asked_slots.count(sid) == 2, (sid, r.asked_slots)
    assert "Not asked" not in r.narrative
    assert r.state["phase"] == "ended" and r.handover["partial"] is None
    assert any(a.get("move") == "read_back" for role, a in r.log if role == "agent")
    assert any(a.get("move") == "goodbye" for role, a in r.log if role == "agent")
