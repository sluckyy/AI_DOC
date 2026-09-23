"""Scripted-actor harness for the Build Specification's simulated patient case pack.

A case is driven by an ActorScript: what the actor opens with, what they answer
when asked for a given slot (keyed by slot id, or by a regex over the agent's
question), what they volunteer only when asked, and lines they interject
(pressure questions, hanging up). The harness records everything the agent
said, the state, the handover, the process violations and any prohibited
phrase, so a test can assert the case's critical criteria against requirement
ids rather than free text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.content.checks import prohibited_hits, strip_quotes
from app.control.controller import Controller, new_state
from app.handover.generate import generate
from app.process.rules import check_transcript

CONSENT = {"ai_disclosure": True, "tone_adaptation": True, "summary_to_clinician": True}
CAPABILITY = {"cap.hearing": "Yes, I can hear you fine.", "cap.language": "English is fine.", "cap.present": "No, it's just me."}


@dataclass
class ActorScript:
    opening: list[str]
    answers: dict[str, str] = field(default_factory=dict)        # slot id -> answer
    by_question: list[tuple[str, str]] = field(default_factory=list)   # (regex over agent text, answer), checked in order
    default: str = "No."
    capability: dict[str, str] = field(default_factory=lambda: dict(CAPABILITY))
    summary_reply: str = "Yes, that's right."
    final_reply: str = "No, that's everything."
    read_back_reply: str = "Yes, that's right."
    confirm_time_reply: str = "Yes, that's about right."
    interject: dict[int, str] = field(default_factory=dict)      # after N person turns, say this instead
    hang_up_after_alert: bool = False
    max_turns: int = 320

    def answer_for(self, agent_turn: dict) -> str:
        sid = agent_turn.get("slot_id")
        if sid and sid in self.answers:
            return self.answers[sid]
        text = agent_turn.get("text") or ""
        for pat, ans in self.by_question:
            if re.search(pat, text, re.I):
                return ans
        return self.default


@dataclass
class CaseRun:
    state: dict
    log: list[tuple[str, dict]]
    handover: dict
    violations: list
    prohibited: list[dict]
    hung_up: bool = False

    @property
    def agent_texts(self) -> list[str]:
        return [a["text"] for r, a in self.log if r == "agent"]

    @property
    def asked_slots(self) -> list[str]:
        return [a["slot_id"] for r, a in self.log if r == "agent" and a.get("move") in ("ask", "reask") and a.get("slot_id")]

    @property
    def narrative(self) -> str:
        return " ".join(self.handover["narrative"])

    def value(self, slot_id: str):
        v = self.state["slot_values"].get(slot_id)
        return v["value"] if v else None

    def slot(self, slot_id: str) -> dict | None:
        return self.state["slot_values"].get(slot_id)

    def alerts(self, tier: str | None = None) -> list[dict]:
        return [a for a in self.state["alerts"] if tier is None or a["tier"] == tier]

    def said(self, pattern: str, include_quoted: bool = False) -> bool:
        """Did Dr Sam say this in their own words? Quoted patient words are excluded unless asked for."""
        return any(re.search(pattern, t if include_quoted else strip_quotes(t), re.I) for t in self.agent_texts)


def run_case(bundle, script: ActorScript, setting: str = "gp_booking", language: str = "en") -> CaseRun:
    ctrl = Controller(bundle)
    state = new_state(setting, language, dict(CONSENT))
    state["is_simulation"] = True
    log: list[tuple[str, dict]] = [("agent", t.as_dict()) for t in ctrl.start(state)]
    opening = list(script.opening)
    n = 0
    hung_up = False
    while state["phase"] != "ended" and n < script.max_turns:
        n += 1
        last = next((a for r, a in reversed(log) if r == "agent"), None)
        move = last["move"] if last else "disclose"
        if script.hang_up_after_alert and any(a.get("move") == "alert" for _, a in log):
            hung_up = True
            state["contact_lost"] = True
            break
        if n in script.interject:
            line = script.interject[n]
        elif move == "disclose":
            line = "Yes, that's fine."
        elif move == "capability":
            line = script.capability.get(last["slot_id"], "Yes.")
        elif move in ("open", "facilitate"):
            line = opening.pop(0) if opening else "That's all really."
        elif move == "invite":
            line = opening.pop(0) if opening else "No, nothing else."
        elif move == "summarise":
            line = script.summary_reply
        elif move in ("ask", "reask"):
            line = script.answer_for(last)
        elif move == "confirm_time":
            line = script.confirm_time_reply
        elif move == "final_invite":
            line = script.final_reply
        elif move == "read_back":
            line = script.read_back_reply
        elif move in ("deflect", "explain_why", "transition"):
            line = "Ok."
        else:
            break
        tid, turns = ctrl.person_turn(state, line)
        log.append(("person", {"text": line, "turn_id": tid, "slot_id": last.get("slot_id") if last else None}))
        log.extend(("agent", t.as_dict()) for t in turns)
        if script.hang_up_after_alert and any(t.move == "alert" for t in turns):
            hung_up = True
            ctrl.contact_lost(state)
            break
    handover = generate(state, bundle, versions=bundle.versions)
    turns = [{"role": r, **a} for r, a in log]
    violations = check_transcript(turns, list(state["slot_values"].values()), state["alerts"], state)
    hits: list[dict] = []
    for t in [a for r, a in log if r == "agent"]:
        for h in prohibited_hits(t["text"], bundle.prohibited):
            hits.append({"turn": t["text"], "pattern": h["pattern"]})
    for line in handover["narrative"]:
        for h in prohibited_hits(line, bundle.prohibited):
            hits.append({"handover": line, "pattern": h["pattern"]})
    return CaseRun(state=state, log=log, handover=handover, violations=violations, prohibited=hits, hung_up=hung_up)
