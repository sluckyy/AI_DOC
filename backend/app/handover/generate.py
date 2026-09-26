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


def _label(intent: str) -> str:
    """The short label for a slot: the first clause, and after any 'route:'-style prefix."""
    label = intent.split(",")[0].split(";")[0].strip()
    if ": " in label and len(label.split(": ")[0].split()) <= 3:
        label = label.split(": ", 1)[1]
    return label


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


def _num(state: dict, slot_id: str):
    v = state.get("slot_values", {}).get(slot_id)
    if not v or v.get("state") != "filled":
        return None
    try:
        return int(v["value"])
    except (TypeError, ValueError):
        return None


def _family_pattern_lines(state: dict, bundle: ContentBundle) -> list[str]:
    """D-39: hand over the pattern and the threshold it crosses, from the structured follow-ups, never from free text."""
    th = bundle.parameters.family_history_thresholds or {}
    lines: list[str] = []
    knowledge = state.get("slot_values", {}).get("fh.knowledge", {}).get("value")
    if knowledge == "adopted_or_estranged":
        lines.append("Family history: not known to the patient (adopted, estranged or no family contact). This is 'unknown', not 'negative'.")
        return lines
    crc_n, crc_age = _num(state, "fh.crc_first_degree_count"), _num(state, "fh.crc_youngest_age")
    c2, c3 = th.get("colorectal_category_2", {}), th.get("colorectal_category_3", {})
    if crc_n is not None:
        if c3 and crc_n >= c3.get("first_degree_count", 3):
            lines.append(f"Family history pattern: {crc_n} first-degree relatives with bowel cancer. Meets {c3.get('label')}.")
        elif c2 and (crc_n >= c2.get("first_degree_count", 2) or (crc_age is not None and crc_age < c2.get("or_one_first_degree_under_age", 55))):
            lines.append(f"Family history pattern: {crc_n} first-degree relative(s) with bowel cancer" + (f", youngest at {crc_age}" if crc_age is not None else "") + f". Meets {c2.get('label')}.")
        else:
            lines.append(f"Family history: {crc_n} first-degree relative(s) with bowel cancer" + (f", youngest at {crc_age}" if crc_age is not None else "") + "; below the configured referral thresholds, clinician to confirm.")
    br_n, br_age = _num(state, "fh.breast_first_degree_count"), _num(state, "fh.breast_youngest_age")
    bm = th.get("breast_moderate_risk", {})
    if br_n is not None and br_n > 0:
        feats = state.get("slot_values", {}).get("fh.breast_high_risk_feature", {}).get("value") or []
        feats = [f for f in feats if f != "none"] if isinstance(feats, list) else []
        if feats:
            lines.append(f"Family history pattern: {br_n} first-degree relative(s) with breast or ovarian cancer with high-risk feature(s) {', '.join(feats).replace('_', ' ')}. Genetic risk assessment criteria apply (Cancer Australia categories); clinician to confirm.")
        elif bm and br_age is not None and br_age < bm.get("first_degree_under_age", 50):
            lines.append(f"Family history pattern: {br_n} first-degree relative(s) with breast cancer, youngest at {br_age}. Meets {bm.get('label')}.")
        else:
            lines.append(f"Family history: {br_n} first-degree relative(s) with breast cancer" + (f", youngest at {br_age}" if br_age is not None else "") + "; clinician to compare against the configured categories.")
    cvd = state.get("slot_values", {}).get("fh.cvd_premature", {})
    if cvd.get("state") == "filled" and cvd.get("value") == "yes":
        lines.append(f"Family history pattern: premature cardiovascular disease in a first-degree relative, as the patient reports it. {th.get('premature_cvd', {}).get('label', '')}".strip())
    return lines


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
            line = f"ALERT ({a['tier'].replace('_', ' ')}, rule {a['rule_id']}, routed to {a['route']}): {a['text']}"
            if a.get("correction_flag"):
                line += " [the patient later queried something read back that this alert's rule used — see Correction at read-back, below; the alert stands and still needs acknowledgement]"
            narrative.append(line)
    # 2. Reason for encounter in the patient's words
    pv = state.get("presenting_verbatim")
    if pv:
        narrative.append(f"Presenting, in the patient's words: \"{pv}\".")
    problems = [p["term"] for p in state.get("problems", [])]
    if problems:
        narrative.append("Problems named by the patient: " + ", ".join(problems) + ".")
    # 3. Per module findings, per-slot negative reporting. Blocks are built per module, then ordered per D-44:
    #    presenting complaint and its modules; function and situation (three or four lines, D-47); the systems review;
    #    past history (never opening the summary); medicines; family pattern; social; the shared gates.
    blocks: dict[str, list[str]] = {}
    for m in modules:
        found: list[str] = []
        negatives: list[str] = []
        not_asked: list[str] = []
        unknown: list[str] = []
        withheld: list[str] = []
        repeats: dict[str, list[str]] = {}
        instances = [(k, v) for k, v in state["slot_values"].items() if "#" in k and v.get("module") == m.module]
        for s in m.slots:
            v = state["slot_values"].get(s.id)
            if s.repeat_over:
                for k, iv in sorted(instances, key=lambda kv: int(kv[0].split("#")[1]) if kv[0].split("#")[1].isdigit() else 0):
                    if not k.startswith(s.id + "#"):
                        continue
                    structured.append({
                        "slot_id": k, "module": m.module, "module_version": m.version, "class": s.slot_class, "intent": s.intent,
                        "item": iv.get("item"), "value": iv.get("value"), "verbatim": iv.get("verbatim"), "state": iv["state"],
                        "turn_id": iv.get("turn_id"), "source": iv.get("source"), "provenance": "patient_reported" if iv["state"] == "filled" else "structural",
                        "evidence": None, "negative_reporting": s.negative_reporting, "epistemic_status": iv.get("epistemic_status"),
                    })
                    if iv["state"] == "filled":
                        repeats.setdefault(s.intent.split(":")[0], []).append(f'{iv.get("item") or "item"}: "{(iv.get("verbatim") or _fmt(iv.get("value")))[:160]}"')
                    elif iv["state"] == "unknown":
                        unknown.append(f'{iv.get("item") or "item"}: patient could not say; not verified')
                continue
            entry = {
                "slot_id": s.id, "module": m.module, "module_version": m.version, "class": s.slot_class,
                "intent": s.intent, "value": v["value"] if v else None, "verbatim": v.get("verbatim") if v else None,
                "state": v["state"] if v else ("not_asked" if s.required else "not_required"),
                "turn_id": v.get("turn_id") if v else None, "source": v.get("source") if v else None,
                "provenance": "patient_reported" if v and v["state"] == "filled" else "structural",
                "evidence": (s.evidence.lr if s.evidence and not s.evidence.gap else None),
                "negative_reporting": s.negative_reporting, "instrument": s.instrument,
                "epistemic_status": v.get("epistemic_status") if v else None,
            }
            if v is not None and v.get("pass_on") is False:
                # D-47: the patient declined to have this passed on; the record carries the fact, not the content
                entry.update({"value": None, "verbatim": None, "state": "withheld_by_patient", "provenance": "structural"})
                structured.append(entry)
                withheld.append(_label(s.intent))
                continue
            structured.append(entry)
            if v is not None and v["state"] == "not_applicable":
                continue   # an answer-driven branch that did not apply (F-13)
            if v is None or v["state"] == "not_asked":
                if s.required or s.always:
                    not_asked.append(s.intent)
                continue
            if v["state"] == "unknown":
                label = _label(s.intent)
                if m.kind == "closing":
                    unknown.append(f"{label}: asked; the patient did not know")
                else:
                    unknown.append(f"{label}: patient could not say; not verified" + (f' ("{v.get("verbatim", "")[:100]}")' if v.get("verbatim") else ""))
                continue
            val = v["value"]
            is_negative = val in ("no", "none", []) or (isinstance(val, list) and val == ["none"])
            label = _label(s.intent)
            if is_negative:
                if s.negative_reporting == "explicit":
                    negatives.append(f"{label}: no")
                continue
            line = f"{label}: {_fmt(val)}"
            if v.get("verbatim") and s.verbatim and s.value.type != "text":
                line += f' ("{v["verbatim"][:120]}")'
            if s.pass_on_consent and v.get("pass_on") is True:
                line += " (patient agreed to pass this on)"
            epi = v.get("epistemic_status")
            if epi == "hypothesis":
                line += " [mentioned in the interview; the conversation ended before this could be read back for confirmation]"
            elif epi == "correction_pending":
                line += " [read back to the patient, who then said something other than a plain yes; see Correction at read-back, below]"
            found.append(line)
        lines: list[str] = []
        title = (m.display_name or m.module.replace("_", " ")).capitalize()
        if m.kind == "closing" and m.module == "review_of_systems":
            # D-37: benign positives sit in the structured layer; routed ones appear as their own module above.
            groups = sum(1 for s_ in m.slots if state["slot_values"].get(s_.id, {}).get("state") == "filled")
            routed = [r["option"].replace("_", " ") for r in state.get("ros_elicited", [])]
            if found:
                lines.append(f"Systems review (asked in {groups} groups; positives recorded in the structured layer, not explored unless routed): " + "; ".join(found) + ".")
            elif groups:
                lines.append(f"Systems review: asked in {groups} groups; every item asked and denied. Each denial is a documented negative only.")
            if routed:
                lines.append("Routed from the systems review to their own question sets: " + ", ".join(dict.fromkeys(routed)) + " (a separate stratum in the agreement analysis, D-37).")
        else:
            if found:
                lines.append(f"{title}: " + "; ".join(found) + ".")
            for label, items in repeats.items():
                lines.append(f"{label}, per item: " + "; ".join(items) + ".")
            if negatives:
                lines.append("Documented negatives (each was asked): " + "; ".join(negatives) + ".")
        if unknown:
            lines.append("Asked, no usable answer: " + "; ".join(unknown) + ".")
        if withheld:
            lines.append("Withheld at the patient's request (asked and answered; not passed on): " + "; ".join(withheld) + ".")
        if not_asked:
            lines.append("Not asked: " + "; ".join(not_asked) + ".")
        if m.gaps and m.kind == "presentation" and (found or repeats or negatives or unknown):
            lines.append("Gaps: " + " ".join(m.gaps))   # section gaps are reviewer notes; they stay in the coding document
        blocks[m.module] = lines
    fh_lines = _family_pattern_lines(state, bundle)
    order = [m.module for m in modules if m.kind == "presentation"]
    order += [m.module for m in modules if m.kind == "closing" and m.module == "functional_situational"]
    order += [m.module for m in modules if m.kind == "closing" and m.module == "review_of_systems"]
    order += [m.module for m in modules if m.kind == "closing" and m.module in ("past_history", "medications")]
    order += [m.module for m in modules if m.kind == "closing" and m.module == "family_history"]
    order += [m.module for m in modules if m.kind == "closing" and m.module not in ("functional_situational", "review_of_systems", "past_history", "medications", "family_history")]
    order += [m.module for m in modules if m.kind == "gating"]
    for name in order:
        narrative.extend(blocks.get(name, []))
        if name == "family_history":
            narrative.extend(fh_lines)
    undecidable = state.get("undecidable_rules", [])
    if undecidable:
        narrative.append("Red-flag rules that could not be decided because a slot was not asked: " + "; ".join(f"{u['rule_id']} (missing {', '.join(u['missing'])})" for u in undecidable) + ".")
    if state.get("late_concerns"):
        narrative.append("Raised at the end, not explored: " + "; ".join(f'"{c["text"][:120]}"' for c in state["late_concerns"]) + ".")
    if state.get("patient_corrections"):
        narrative.append("Correction at read-back: the patient's reply below was not a plain confirmation. The system cannot reliably tell which item it concerns, so every item in that read-back is marked unconfirmed above rather than being kept or discarded automatically. Please confirm the affected item(s) with the patient or the record.")
        for c in state["patient_corrections"]:
            items = ", ".join(c.get("read_back_slot_ids") or []) or "none tracked (read back before this build tracked items)"
            line = f'"{c["text"][:200]}" (items read back at that point: {items})'
            if c.get("affected_alerts"):
                line += f" — affects alert(s) {', '.join(c['affected_alerts'])}"
            narrative.append(line)
    tone = _tone_sentence(state)
    if tone:
        narrative.append(tone)
    if state.get("closed_by_alert"):
        narrative.append("The interview was stopped by an immediate-tier alert; everything after that point is not asked.")
    asr = (metadata or {}).get("asr") or {}
    if asr.get("spoken_turns"):
        low = asr.get("low_confidence_turns") or []
        line = f"Speech recognition ({', '.join(asr.get('provider', []))}): {asr['spoken_turns']} spoken turns"
        line += f", {asr.get('typed_turns', 0)} typed" if asr.get("typed_turns") else ""
        line += f"; lowest confidence {asr.get('min_confidence')}"
        if low:
            line += f"; {len(low)} below the {asr.get('threshold')} threshold, where the words may be misheard: " + "; ".join(f'{t["turn_id"]} ({t["confidence"]}) "{t["text"][:60]}"' for t in low[:6])
        narrative.append(line + ". Confidence is the recogniser's, per utterance (N-9); a low value means check the transcript, not the patient.")
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
        "pre_existing_conditions": {"items": [e for e in structured if e["slot_id"].startswith("pm.")], "provenance": "patient_reported", "note": "five retrieval routes plus a lay-anchored sweep; the patient's labels as given, never corrected (D-44)"},
        "onset_relative_to_presentation": {"items": [e for e in structured if e["slot_id"].endswith("clock_time")], "provenance": "patient_reported"},
        "medications": {"items": [e for e in structured if e["slot_id"].startswith(("ctx.medications", "md.")) or e["slot_id"] in ("gate.anticoagulant", "gate.immunosuppression")], "provenance": "patient_reported", "note": "category-prompted inventory, per medicine as actually taken; 'patient could not say' is distinct from 'none' and from 'not asked' (F-17, D-38); reconciliation against a dispensing source is phase 3"},
        "external_cause": {"items": [e for e in structured if e["slot_id"] in ("gate.bat_contact", "gate.overseas_animal") or e["slot_id"].startswith("wb.")], "provenance": "patient_reported"},
        "behavioural_risk_factors": {"items": [e for e in structured if e["slot_id"] in ("gate.smoking", "so.smoking") or e["slot_id"].startswith(("au.", "so.audit", "so.drug"))], "provenance": "patient_reported", "note": "instrument items recorded as answered; no score is assembled (F-21, D-41)"},
        "family_history": {"items": [e for e in structured if e["slot_id"].startswith("fh.")], "pattern": _family_pattern_lines(state, bundle), "provenance": "patient_reported", "note": "three states: denied, unknown, not asked (D-39)"},
        "social_and_functional": {"items": [e for e in structured if e["slot_id"].startswith(("fn.", "so.")) and not e["slot_id"].startswith(("so.audit", "so.drug", "so.smoking"))], "provenance": "patient_reported", "note": "inputs only, never a frailty score (D-47); items the patient declined to pass on are marked withheld"},
        "obstetric_status": {"items": [e for e in structured if e["slot_id"] in ("gate.pregnancy_possible", "ab.pregnancy_possible", "ab.home_pregnancy_test", "ab.last_period") or e["slot_id"].startswith(("fm.", "vb."))], "provenance": "patient_reported"},
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
