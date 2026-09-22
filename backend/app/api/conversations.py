from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.content.loader import get_bundle
from app.control.controller import AgentTurn, Controller, new_state
from app.db import Alert, Attestation, AuditEvent, Conversation, Handover, SlotValue, Turn, get_db
from app.handover.generate import answer_clinician_question, generate
from app.process.rules import check_transcript
from app.providers.content_safety import get_content_safety_provider
from app.providers.extraction import get_extraction_provider
from app.providers.speech import get_speech_provider, word_count
from app.providers.telephony import get_telephony_provider
from app.providers.terminology import get_terminology_provider
from app.providers.tone import get_tone_provider
from app.providers.wording import get_wording_provider

router = APIRouter()

PROCESS_VERSION = "P1-P14@1.0"
CONTROL_VERSION = "0.1.0"
HANDOVER_VERSION = "0.1.0"


class Consent(BaseModel):
    ai_disclosure: bool = True
    tone_adaptation: bool = False
    summary_to_clinician: bool = True


class StartRequest(BaseModel):
    setting: str = Field(pattern="^(ed|gp_booking)$")
    language: str = "en"
    consent: Consent = Field(default_factory=Consent)
    persona_register: str = "patient"
    record_prefill: dict[str, Any] = Field(default_factory=dict)
    is_simulation: bool = True


class TurnRequest(BaseModel):
    transcript: str
    prosody: dict[str, Any] | None = None
    interrupted_at_ms: int | None = None
    asr_confidence: float | None = None


class QuestionRequest(BaseModel):
    question: str


class AttestRequest(BaseModel):
    clinician: str
    diagnosis_block: dict[str, Any]
    edits: dict[str, Any] = Field(default_factory=dict)


def _controller() -> Controller:
    return Controller(get_bundle(), extraction=get_extraction_provider(), wording=get_wording_provider(), tone=get_tone_provider())


def _versions(bundle) -> dict:
    return {"process": PROCESS_VERSION, "control": CONTROL_VERSION, "handover": HANDOVER_VERSION, **bundle.versions}


def _persist_agent_turns(db: Session, conv: Conversation, turns: list[AgentTurn], language: str) -> list[dict]:
    speech = get_speech_provider()
    safety = get_content_safety_provider()
    bundle = get_bundle()
    out: list[dict] = []
    order = db.query(Turn).filter(Turn.conversation_id == conv.id).count()
    for t in turns:
        ok, verdict = safety.screen(t.text)
        text = t.text if ok else bundle.phrasings.deflect["diagnosis"]
        rate = "-8%" if conv.state.get("register") != "older" else "-15%"
        syn = speech.synthesise(text, language=language, rate=rate, pitch="0%")
        tid = f"{conv.id}-a{order + 1}"
        row = Turn(
            id=tid, conversation_id=conv.id, order=order + 1, role="agent", text=text, phase=t.phase, move=t.move,
            phrasing_variant_id=t.phrasing_variant_id, slot_id=t.slot_id, expression=t.expression, alert_id=t.alert_id,
            audio=syn.audio, audio_content_type=syn.content_type or None, visemes=syn.visemes,
        )
        db.add(row)
        order += 1
        out.append({
            "turn_id": tid, "role": "agent", "caption": text, "move": t.move, "phase": t.phase, "expression": t.expression,
            "next": t.next, "alert_id": t.alert_id, "phrasing_variant_id": t.phrasing_variant_id, "slot_id": t.slot_id,
            "audio_url": f"/audio/{tid}" if syn.audio else None, "visemes": syn.visemes, "duration_ms": syn.duration_ms,
            "prosody": {"rate": rate, "pitch": "0%", "pause_after_ms": 1500 if t.move in ("invite", "ask", "reask", "open") else 600},
            "content_safety": verdict,
        })
    return out


def _sync_alerts_and_slots(db: Session, conv: Conversation) -> None:
    state = conv.state
    existing = {a.id for a in db.query(Alert).filter(Alert.conversation_id == conv.id).all()}
    for a in state.get("alerts", []):
        aid = f"{conv.id}-{a['id']}"
        if aid in existing:
            continue
        db.add(Alert(id=aid, conversation_id=conv.id, rule_id=a["rule_id"], tier=a["tier"], route=a["route"], text=a["text"],
                     verbatim=a.get("verbatim"), clock_times=a.get("clock_times"), fired_at=a.get("fired_at"), turn_id=a.get("turn_id")))
        db.add(AuditEvent(conversation_id=conv.id, actor="controller", action=f"alert_routed:{a['route']}", detail={"rule_id": a["rule_id"], "tier": a["tier"]}))
    db.query(SlotValue).filter(SlotValue.conversation_id == conv.id).delete()
    for sid, v in state.get("slot_values", {}).items():
        db.add(SlotValue(conversation_id=conv.id, slot_id=sid, module=v["module"], value=v["value"], verbatim=v.get("verbatim"),
                         state=v["state"], source=v.get("source"), turn_id=v.get("turn_id"), written_at=v.get("written_at")))


def _maybe_generate_handover(db: Session, conv: Conversation) -> None:
    if conv.state.get("phase") != "ended":
        return
    if db.query(Handover).filter(Handover.conversation_id == conv.id).count():
        return
    metadata = {"model_provider": get_extraction_provider().name, "tts_provider": get_speech_provider().name,
                "model_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_PERSONA", "") or None}
    doc = generate(conv.state, get_bundle(), terminology=get_terminology_provider(), versions=conv.versions, metadata=metadata)
    db.add(Handover(conversation_id=conv.id, version=1, document=doc))
    from app.db import utcnow
    conv.ended_at = utcnow()


@router.post("/conversations")
def start_conversation(req: StartRequest, db: Session = Depends(get_db)):
    bundle = get_bundle()
    if req.language not in bundle.parameters.languages:
        raise HTTPException(400, f"language {req.language} is not configured; allowed: {bundle.parameters.languages}")
    ctrl = _controller()
    state = new_state(req.setting, req.language, req.consent.model_dump(), req.persona_register, req.record_prefill)
    from app.db import utcnow
    state["consent_timestamp"] = utcnow().isoformat()
    state["is_simulation"] = req.is_simulation
    state["saturation_invitations"] = bundle.parameters.saturation_invitations
    for sid, val in req.record_prefill.items():
        slot = bundle.context.slot(sid)
        if slot and not slot.confirm:
            state["slot_values"][sid] = {"slot_id": sid, "module": "context", "value": val, "verbatim": None, "state": "filled",
                                         "turn_id": None, "source": "prefill:record", "confidence": 1.0, "written_at": None}
    conv = Conversation(id=uuid.uuid4().hex[:12], setting=req.setting, language=req.language, consent=req.consent.model_dump(),
                        is_simulation=1 if req.is_simulation else 0, versions=_versions(bundle), state=state)
    db.add(conv)
    db.flush()
    turns = ctrl.start(state)
    conv.state = dict(state)
    agent = _persist_agent_turns(db, conv, turns, req.language)
    db.add(AuditEvent(conversation_id=conv.id, actor="api", action="conversation_started", detail={"setting": req.setting, "language": req.language}))
    db.commit()
    return {"conversation_id": conv.id, "versions": conv.versions, "agent_turns": agent, "phase": conv.state["phase"]}


@router.post("/conversations/{cid}/turns")
def person_turn(cid: str, req: TurnRequest, db: Session = Depends(get_db)):
    conv = db.get(Conversation, cid)
    if conv is None:
        raise HTTPException(404, "conversation not found")
    if conv.state.get("phase") == "ended":
        raise HTTPException(409, "conversation has ended")
    ctrl = _controller()
    state = dict(conv.state)
    prosody = dict(req.prosody or {})
    prosody.setdefault("word_count", word_count(req.transcript))
    person_tid, turns = ctrl.person_turn(state, req.transcript, prosody)
    order = db.query(Turn).filter(Turn.conversation_id == conv.id).count()
    tone = state["tone_log"][-1] if state.get("tone_log") and state["tone_log"][-1]["turn_id"] == person_tid else None
    db.add(Turn(id=f"{conv.id}-{person_tid}", conversation_id=conv.id, order=order + 1, role="person", text=req.transcript,
                phase=conv.state.get("phase"), tone=tone, prosody={**prosody, "asr_confidence": req.asr_confidence, "interrupted_at_ms": req.interrupted_at_ms}))
    conv.state = state
    agent = _persist_agent_turns(db, conv, turns, conv.language)
    _sync_alerts_and_slots(db, conv)
    _maybe_generate_handover(db, conv)
    db.commit()
    return {"person_turn_id": person_tid, "agent_turns": agent, "phase": state["phase"],
            "detected_tone": ({"label": state.get("_last_tone"), "stored": bool(tone)}),
            "alerts": [{**a, "alert_id": f"{conv.id}-{a['id']}"} for a in state.get("alerts", []) if a.get("turn_id") == person_tid]}


class AckRequest(BaseModel):
    acknowledged_by: str


@router.post("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, req: AckRequest, db: Session = Depends(get_db)):
    """S-4: every alert requires positive acknowledgement by a named human."""
    a = db.get(Alert, alert_id)
    if a is None:
        raise HTTPException(404, "alert not found")
    if not req.acknowledged_by.strip():
        raise HTTPException(400, "acknowledgement requires a name")
    from app.db import utcnow
    a.acknowledged_at = utcnow()
    db.add(AuditEvent(conversation_id=a.conversation_id, actor=req.acknowledged_by.strip(), action="alert_acknowledged", detail={"alert_id": alert_id, "rule_id": a.rule_id}))
    db.commit()
    return {"alert_id": alert_id, "acknowledged_at": a.acknowledged_at.isoformat(), "acknowledged_by": req.acknowledged_by.strip()}


@router.get("/alerts/unacknowledged")
def unacknowledged_alerts(db: Session = Depends(get_db)):
    """S-4 / N-33: what a triage desk or duty GP dashboard polls; anything older than the
    configured timeout is flagged for further escalation."""
    from datetime import timedelta
    from app.db import utcnow
    timeout = get_bundle().parameters.alert_acknowledgement_timeout_s
    rows = db.query(Alert).filter(Alert.acknowledged_at.is_(None)).all()
    now = utcnow()
    out = []
    for a in rows:
        fired = None
        try:
            from datetime import datetime
            fired = datetime.fromisoformat(a.fired_at) if a.fired_at else None
        except Exception:
            fired = None
        overdue = bool(fired and (now - fired.replace(tzinfo=None) if fired.tzinfo is None else now - fired) > timedelta(seconds=timeout))
        out.append({"alert_id": a.id, "conversation_id": a.conversation_id, "tier": a.tier, "route": a.route, "rule_id": a.rule_id,
                    "text": a.text, "fired_at": a.fired_at, "overdue_for_further_escalation": overdue})
    return {"timeout_s": timeout, "alerts": out}


@router.get("/audio/{turn_id}")
def audio(turn_id: str, db: Session = Depends(get_db)):
    t = db.get(Turn, turn_id)
    if t is None or not t.audio:
        raise HTTPException(404, "no audio for this turn")
    return Response(content=t.audio, media_type=t.audio_content_type or "audio/mpeg")


def _turn_dicts(db: Session, cid: str) -> list[dict]:
    rows = db.query(Turn).filter(Turn.conversation_id == cid).order_by(Turn.order).all()
    return [{"id": r.id, "order": r.order, "role": r.role, "text": r.text, "phase": r.phase, "move": r.move,
             "phrasing_variant_id": r.phrasing_variant_id, "slot_id": r.slot_id, "expression": r.expression,
             "tone": r.tone, "alert_id": r.alert_id, "created_at": r.created_at.isoformat() if r.created_at else None} for r in rows]


@router.get("/conversations/{cid}")
def get_conversation(cid: str, db: Session = Depends(get_db)):
    conv = db.get(Conversation, cid)
    if conv is None:
        raise HTTPException(404, "conversation not found")
    state = {k: v for k, v in conv.state.items() if not k.startswith("_")}
    return {"conversation_id": conv.id, "setting": conv.setting, "language": conv.language, "consent": conv.consent,
            "versions": conv.versions, "state": state, "turns": _turn_dicts(db, cid)}


@router.get("/conversations/{cid}/handover")
def get_handover(cid: str, db: Session = Depends(get_db)):
    h = db.query(Handover).filter(Handover.conversation_id == cid).order_by(Handover.version.desc()).first()
    if h is None:
        raise HTTPException(404, "no handover yet; the conversation has not ended")
    db.add(AuditEvent(conversation_id=cid, actor="clinician", action="handover_viewed", detail={"version": h.version}))
    db.commit()
    doc = h.document
    return {"version": h.version, "narrative": doc["narrative"], "structured_record": doc["structured_record"],
            "alerts": doc["alerts"], "safety_net_record": doc["safety_net_record"], "versions": doc["versions"],
            "generated_at": doc["generated_at"], "partial": doc.get("partial"), "metadata": doc.get("metadata", {})}


@router.get("/conversations/{cid}/coding-document")
def get_coding_document(cid: str, db: Session = Depends(get_db)):
    h = db.query(Handover).filter(Handover.conversation_id == cid).order_by(Handover.version.desc()).first()
    if h is None:
        raise HTTPException(404, "no handover yet")
    db.add(AuditEvent(conversation_id=cid, actor="clinician", action="coding_document_viewed", detail={"version": h.version}))
    db.commit()
    return {"version": h.version, "coding_document": h.document["coding_document"]}


@router.post("/conversations/{cid}/clinician-questions")
def clinician_question(cid: str, req: QuestionRequest, db: Session = Depends(get_db)):
    conv = db.get(Conversation, cid)
    if conv is None:
        raise HTTPException(404, "conversation not found")
    ans = answer_clinician_question(req.question, conv.state, get_bundle(), _turn_dicts(db, cid))
    db.add(AuditEvent(conversation_id=cid, actor="clinician", action="question_asked", detail={"question": req.question}))
    db.commit()
    return ans


@router.post("/conversations/{cid}/attest")
def attest(cid: str, req: AttestRequest, db: Session = Depends(get_db)):
    h = db.query(Handover).filter(Handover.conversation_id == cid).order_by(Handover.version.desc()).first()
    if h is None:
        raise HTTPException(404, "no handover to attest")
    if not req.clinician.strip():
        raise HTTPException(400, "attestation requires a named clinician")
    att = Attestation(conversation_id=cid, clinician=req.clinician.strip(), handover_version=h.version,
                      diagnosis_block=req.diagnosis_block, edits=req.edits)
    db.add(att)
    db.add(AuditEvent(conversation_id=cid, actor=req.clinician.strip(), action="attested", detail={"handover_version": h.version}))
    db.commit()
    db.refresh(att)
    return {"attestation_id": att.id, "clinician": att.clinician, "handover_version": att.handover_version,
            "signed_at": att.signed_at.isoformat(), "status": "attested: this version is now the exportable form"}


@router.get("/conversations/{cid}/export")
def export(cid: str, db: Session = Depends(get_db)):
    conv = db.get(Conversation, cid)
    if conv is None:
        raise HTTPException(404, "conversation not found")
    turns = _turn_dicts(db, cid)
    h = db.query(Handover).filter(Handover.conversation_id == cid).order_by(Handover.version.desc()).first()
    atts = db.query(Attestation).filter(Attestation.conversation_id == cid).all()
    alerts = [{"id": a.id, "rule_id": a.rule_id, "tier": a.tier, "route": a.route, "text": a.text, "verbatim": a.verbatim, "fired_at": a.fired_at} for a in db.query(Alert).filter(Alert.conversation_id == cid).all()]
    state = {k: v for k, v in conv.state.items() if not k.startswith("_")}
    slot_values = list(state.get("slot_values", {}).values())
    violations = check_transcript(turns, slot_values, alerts, state)
    return {"conversation_id": cid, "is_simulation": bool(conv.is_simulation), "versions": conv.versions, "state": state, "turns": turns,
            "alerts": alerts, "handover": h.document if h else None,
            "attestations": [{"clinician": a.clinician, "handover_version": a.handover_version, "diagnosis_block": a.diagnosis_block, "signed_at": a.signed_at.isoformat()} for a in atts],
            "process_check": [{"rule": v.rule, "turn_index": v.turn_index, "detail": v.detail} for v in violations]}


@router.post("/conversations/{cid}/transfer")
def transfer_setup(cid: str, db: Session = Depends(get_db)):
    """D-42 live transfer. Returns what the browser needs to connect the patient to the duty GP,
    and records the transfer attempt against the conversation's open immediate alert."""
    conv = db.get(Conversation, cid)
    if conv is None:
        raise HTTPException(404, "conversation not found")
    alerts = [a for a in conv.state.get("alerts", []) if a["tier"] == "immediate"]
    if not alerts:
        raise HTTPException(409, "no immediate-tier alert on this conversation")
    setup = get_telephony_provider().setup()
    route = get_bundle().parameters.escalation[conv.setting]["immediate"]
    db.add(AuditEvent(conversation_id=cid, actor="controller", action="live_transfer_initiated",
                      detail={"provider": setup.provider, "route": route.route, "target": route.transfer_target, "number_configured": bool(setup.transfer_number)}))
    db.commit()
    return {"route": route.route, "transfer_target": route.transfer_target, "unanswered": route.unanswered,
            "provider": setup.provider, "transfer_number": setup.transfer_number, "caller_id": setup.caller_id,
            "token": setup.token, "user_id": setup.user_id, "expires_on": setup.expires_on,
            "alert": {**alerts[-1], "alert_id": f"{cid}-{alerts[-1]['id']}"}}


@router.post("/content/reload")
def content_reload():
    """D-51: reload content from disk without a restart. A failing load keeps the old bundle."""
    from app.content.checks import run_checks
    from app.content.loader import reload_bundle

    try:
        bundle = reload_bundle()
    except Exception as exc:
        raise HTTPException(422, f"content not reloaded: {exc}")
    findings = run_checks(bundle)
    return {"reloaded": True, "modules": len(bundle.modules), "versions": bundle.versions,
            "authoring_checks": {"passed": not findings, "findings": [str(f) for f in findings]}}


@router.get("/content/status")
def content_status():
    from app.content.checks import run_checks

    bundle = get_bundle()
    findings = run_checks(bundle)
    return {
        "modules": [{"module": m.module, "display_name": m.display_name or m.module.replace("_", " "), "version": m.version, "status": m.status,
                     "reviewed": m.reviewed, "reviewed_by": m.reviewed_by, "reviewed_on": m.reviewed_on, "slots": len(m.slots),
                     "red_flags": [{"id": r.id, "tier": r.tier} for r in m.red_flags], "review_notes": m.review_notes} for m in bundle.modules.values()],
        "escalation": {setting: {tier: {"route": r.route, "transfer_target": r.transfer_target} for tier, r in tiers.items()} for setting, tiers in bundle.parameters.escalation.items()},
        "telephony": get_telephony_provider().name,
        "disabled_modules": bundle.versions.get("disabled_modules", {}),
        "clinical_parameters": {k: {"status": v.get("status", "pending"), "value": v.get("value", v.get("positive_threshold"))} for k, v in bundle.parameters.clinical_parameters.items()},
        "context_version": bundle.context.version, "parameters": bundle.versions["parameters"], "languages": bundle.parameters.languages,
        "authoring_checks": {"passed": not findings, "findings": [str(f) for f in findings]},
        "providers": {"model": get_extraction_provider().name, "tts": get_speech_provider().name, "content_safety": get_content_safety_provider().name, "terminology": get_terminology_provider().name},
    }
