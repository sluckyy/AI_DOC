"""The handover layer: a contract, not a rendering.

Narrative from filled slots, never from the transcript; a structured record of every
slot with its coded value, verbatim where flagged, and the turn it came from; alerts
with verbatim and clock times; the safety-net record; and the coding document with
field-level provenance and an empty diagnosis block. Unfilled required slots appear
as not asked, never as negative.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from app.content.schema import ContentBundle
from app.providers.terminology import TerminologyProvider, FakeTerminology


def _fmt(value) -> str:
    if value is None:
        return "not asked"
    if isinstance(value, list):
        return ", ".join(str(v).replace("_", " ") for v in value) if value else "none"
    return str(value).replace("_", " ")


def _tone_sentence(state: dict) -> str | None:
    if not state["consent"].get("tone_adaptation") or not state.get("tone_log"):
        return None
    labels = [t["label"] for t in state["tone_log"] if t["label"] != "settled" and t["confidence"] >= 0.6]
    if not labels:
        return "Seemed settled throughout."
    top = max(set(labels), key=labels.count)
    return f"Seemed {top.replace('_', ' ')} at times during the interview (derived from wording and pace; not a clinical finding)."


def generate(state: dict, bundle: ContentBundle, terminology: TerminologyProvider | None = None, versions: dict | None = None, metadata: dict | None = None) -> dict:
    terminology = terminology or FakeTerminology()
    modules = [bundle.modules[n] for n in state["module_queue"] if n in bundle.modules]
    alerts = state.get("alerts", [])
    structured: list[dict] = []
    narrative: list[str] = []
    partial_reason = None
    if state.get("bail_out_reason"):
        partial_reason = f"interview did not run: {state['bail_out_reason'].replace('_', ' ')}"
    elif state.get("closed_by_alert"):
        partial_reason = "interview stopped by an immediate-tier alert"
    elif state.get("phase") != "ended":
        partial_reason = f"interview incomplete; stopped in phase {state.get('phase')}"
    if state.get("contact_lost"):
        partial_reason = (partial_reason + "; " if partial_reason else "") + "contact with the patient was lost"
    if partial_reason:
        narrative.append(f"PARTIAL HISTORY: {partial_reason}. Everything not listed below was not asked. No examination was performed. This must not be read as a complete assessment.")
    if state.get("contact_lost"):
        narrative.append(f"CONTACT LOST at {state.get('contact_lost_at')}: the line dropped. Every alert below stands and needs acknowledgement; no call-back was placed by the agent (S-14, owner decision B10).")
    ctx = state.get("slot_values", {})
    demo = [f"age {ctx['ctx.age']['value']}" for _ in [0] if ctx.get("ctx.age", {}).get("value") is not None]
    if ctx.get("ctx.sex_recorded", {}).get("value"):
        demo.append(f"recorded sex {ctx['ctx.sex_recorded']['value']}")
    if demo:
        narrative.append("Context from the record: " + ", ".join(demo) + ".")

    # 1. Alerts first
    if alerts:
        for a in alerts:
            narrative.append(f"ALERT ({a['tier'].replace('_', ' ')}, rule {a['rule_id']}, routed to {a['route']}): {a['text']}")
    # 2. Reason for encounter in the patient's words
    pv = state.get("presenting_verbatim")
    if pv:
        narrative.append(f"Presenting, in the patient's words: \"{pv}\".")
    problems = [p["term"] for p in state.get("problems", [])]
    if problems:
        narrative.append("Problems named by the patient: " + ", ".join(problems) + ".")
    # 3. Per module findings, per-slot negative reporting
    for m in modules:
        found: list[str] = []
        negatives: list[str] = []
        not_asked: list[str] = []
        unknown: list[str] = []
        for s in m.slots:
            v = state["slot_values"].get(s.id)
            entry = {
                "slot_id": s.id, "module": m.module, "module_version": m.version, "class": s.slot_class,
                "intent": s.intent, "value": v["value"] if v else None, "verbatim": v.get("verbatim") if v else None,
                "state": v["state"] if v else ("not_asked" if s.required else "not_required"),
                "turn_id": v.get("turn_id") if v else None, "source": v.get("source") if v else None,
                "provenance": "patient_reported" if v and v["state"] == "filled" else "structural",
                "evidence": (s.evidence.lr if s.evidence and not s.evidence.gap else None),
                "negative_reporting": s.negative_reporting,
            }
            structured.append(entry)
            if v is not None and v["state"] == "not_applicable":
                continue   # an answer-driven branch that did not apply (F-13)
            if v is None or v["state"] == "not_asked":
                if s.required:
                    not_asked.append(s.intent)
                continue
            if v["state"] == "unknown":
                label = s.intent.split(",")[0].split(";")[0]
                unknown.append(f"{label}: patient could not say; not verified" + (f' ("{v.get("verbatim", "")[:100]}")' if v.get("verbatim") else ""))
                continue
            val = v["value"]
            is_negative = val in ("no", "none", []) or (isinstance(val, list) and val == ["none"])
            label = s.intent.split(",")[0].split(";")[0]
            if is_negative:
                if s.negative_reporting == "explicit":
                    negatives.append(f"{label}: no")
                continue
            line = f"{label}: {_fmt(val)}"
            if v.get("verbatim") and s.verbatim and s.value.type != "text":
                line += f' ("{v["verbatim"][:120]}")'
            found.append(line)
        if found:
            narrative.append(f"{(m.display_name or m.module.replace('_', ' ')).capitalize()}: " + "; ".join(found) + ".")
        if negatives:
            narrative.append("Documented negatives (each was asked): " + "; ".join(negatives) + ".")
        if unknown:
            narrative.append("Asked, no usable answer: " + "; ".join(unknown) + ".")
        if not_asked:
            narrative.append("Not asked: " + "; ".join(not_asked) + ".")
        if m.gaps:
            narrative.append("Gaps: " + " ".join(m.gaps))
    undecidable = state.get("undecidable_rules", [])
    if undecidable:
        narrative.append("Red-flag rules that could not be decided because a slot was not asked: " + "; ".join(f"{u['rule_id']} (missing {', '.join(u['missing'])})" for u in undecidable) + ".")
    if state.get("late_concerns"):
        narrative.append("Raised at the end, not explored: " + "; ".join(f'"{c["text"][:120]}"' for c in state["late_concerns"]) + ".")
    if state.get("patient_corrections"):
        narrative.append("Patient corrections to the read-back, verbatim: " + "; ".join(f'"{c["text"][:160]}"' for c in state["patient_corrections"]) + ".")
    tone = _tone_sentence(state)
    if tone:
        narrative.append(tone)
    if state.get("closed_by_alert"):
        narrative.append("The interview was stopped by an immediate-tier alert; everything after that point is not asked.")
    lang = state.get("language", "en")
    narrative.append(f"Interview language: {lang}. " + ("Quoted words are in the language spoken; no translation was applied." if lang == "en" else "Quoted words are as transcribed in the interview language; any translation is marked in the structured record and is not validated."))
    if state.get("is_simulation"):
        narrative.append("RESEARCH RECORD: this interview was run in simulation mode and is not for clinical use.")
    narrative.append("Nothing in this handover is a clinician's finding. Everything is patient-reported and machine-transcribed until a clinician attests it.")

    # Coding document (CDI review specification)
    concept_terms = list(dict.fromkeys(problems))
    concepts = [terminology.bind(t) for t in concept_terms]
    symptom_detail = [e for e in structured if e["class"] in ("coverage", "discriminating", "red_flag")]
    coding_document = {
        "diagnosis_block": {"principal_diagnosis": None, "additional_diagnoses": [], "provenance": "clinician_only",
                              "prompt": "Left empty by the agent. The clinician nominates which condition occasioned the episode."},
        "reason_for_encounter": {"patient_words": pv, "structured_symptom_set": concept_terms, "concepts": concepts, "provenance": "patient_reported"},
        "symptom_detail": {"items": symptom_detail, "provenance": "patient_reported"},
        "pre_existing_conditions": {"items": [e for e in structured if e["slot_id"] == "cs.past_history"], "provenance": "patient_reported", "note": "in the patient's words; full past history section is a later slice"},
        "onset_relative_to_presentation": {"items": [e for e in structured if e["slot_id"].endswith("clock_time")], "provenance": "patient_reported"},
        "medications": {"items": [e for e in structured if e["slot_id"].startswith("ctx.medications") or e["slot_id"] in ("cs.medications", "cs.allergies", "gate.anticoagulant", "gate.immunosuppression")], "provenance": "patient_reported", "note": "captured by name and read back; 'patient could not say' is distinct from 'none' and from 'not asked' (F-17)"},
        "external_cause": {"items": [e for e in structured if e["slot_id"] in ("gate.bat_contact", "gate.overseas_animal") or e["slot_id"].startswith("wb.")], "provenance": "patient_reported"},
        "behavioural_risk_factors": {"items": [e for e in structured if e["slot_id"] in ("gate.smoking",) or e["slot_id"].startswith("au.")], "provenance": "patient_reported"},
        "social_and_functional": {"items": [], "provenance": "patient_reported"},
        "obstetric_status": {"items": [], "provenance": "patient_reported"},
        "safety_net_events": {"items": alerts, "provenance": "structural"},
        "how_the_patient_seemed": {"text": tone, "provenance": "derived"},
        "gaps": {"items": [g for m in modules for g in m.gaps] + [e["intent"] for e in structured if e["state"] == "not_asked"], "provenance": "structural"},
        "provenance_and_attestation": {
            "statement": "Content is patient-reported and machine-transcribed. It is not a primary source for coding until a clinician reviews, edits and signs it.",
            "versions": versions or {}, "interview_started": None, "interview_ended": state.get("ended_at"),
            "clinician_sign_off": None, "provenance": "structural",
        },
        "terminology": "SNOMED CT-AU concepts only; no ICD-10-AM codes are emitted (D-24)",
    }
    return {
        "narrative": narrative,
        "structured_record": structured,
        "alerts": alerts,
        "safety_net_record": state.get("closing_delivered") or {},
        "coding_document": coding_document,
        "partial": partial_reason,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "versions": versions or {},
        "metadata": {**(metadata or {}), "language": state.get("language"), "setting": state.get("setting"),
                     "consent": state.get("consent"), "consent_timestamp": state.get("consent_timestamp"),
                     "is_simulation": bool(state.get("is_simulation")), "saturation_invitations": state.get("saturation_invitations"),
                     "content_version": (versions or {}).get("content_version"), "content_mode": (versions or {}).get("content_mode"),
                     "review_status": {n: (versions or {}).get("review_status", {}).get(n) for n in state.get("module_queue", [])},
                     "collateral_available": state.get("collateral_available"), "capability": state.get("capability")},
    }


def answer_clinician_question(question: str, state: dict, bundle: ContentBundle, turns: list[dict]) -> dict:
    """Answers only from filled slots and verbatim. Anything else is 'I didn't ask'."""
    q = question.lower()
    words = [w for w in re.findall(r"[a-z]+", q) if len(w) > 3 and w not in ("what", "did", "they", "say", "about", "patient", "have", "there", "their", "with", "does", "that", "this")]
    hits: list[str] = []
    for name in state["module_queue"]:
        for s in bundle.modules[name].slots:
            v = state["slot_values"].get(s.id)
            hay = f"{s.id.replace('.', ' ').replace('_', ' ')} {s.intent}".lower()
            if any(re.search(r"\b" + re.escape(w) + r"\b", hay) for w in words):
                if v is None or v["state"] == "not_asked":
                    hits.append(f"I didn't ask about {s.intent}.")
                elif v["state"] == "unknown":
                    hits.append(f"I asked about {s.intent} and didn't get a usable answer. They said: \"{v.get('verbatim') or ''}\".")
                else:
                    line = f"On {s.intent}: {_fmt(v['value'])}"
                    if v.get("verbatim"):
                        line += f'. They said: "{v["verbatim"]}"'
                    hits.append(line + ".")
    if not hits:
        person_lines = [t["text"] for t in turns if t["role"] == "person" and any(w in t["text"].lower() for w in words)]
        if person_lines:
            return {"answer": "I didn't ask about that directly, but the patient said: " + " | ".join(f'"{l[:160]}"' for l in person_lines[:3]), "grounded": True}
        return {"answer": "I didn't ask about that.", "grounded": True}
    return {"answer": " ".join(hits[:4]), "grounded": True}
