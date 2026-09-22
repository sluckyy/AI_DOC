"""The control layer: deterministic code over filled slots.

Owns the phase, module activation, the saturation count (P13), the coverage sweep,
red-flag evaluation and routing, and every slot write stamped with the turn it came
from (P12). The model (extraction and wording providers) proposes values and
wording; it never decides what happens next.

State is a plain dict so it can be persisted as JSON and exported for the study.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.content.rules import evaluate
from app.content.schema import ContentBundle, Module, Slot
from app.providers.extraction import ExtractionProvider, RulesExtraction
from app.providers.tone import RulesTone, ToneProvider
from app.providers.wording import TemplateWording, WordingProvider, passes_guardrails

AFFIRM = re.compile(r"\b(yes|yeah|yep|ok|okay|sure|fine|go on|all right|alright|that's fine|of course|please|continue)\b", re.I)
DECLINE = re.compile(r"\b(no|nope|stop|don't|do not|a person|a human|real person|someone else|not the ai)\b", re.I)
SERIOUS_Q = re.compile(r"\b(is it serious|am i going to be ok|is this bad|is it my heart|what do you think it is|what is it|is it dangerous|should i be worried)\b", re.I)

MOVE_EXPRESSION = {
    "disclose": "warm", "open": "attentive", "facilitate": "listening", "invite": "attentive",
    "summarise": "thoughtful", "ask": "attentive", "explain_why": "reassuring_neutral", "deflect": "reassuring_neutral",
    "alert": "serious", "read_back": "thoughtful", "close": "reassuring_neutral", "goodbye": "warm", "bail_out": "serious",
    "final_invite": "attentive", "reask": "attentive",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AgentTurn:
    text: str
    move: str
    phase: str
    phrasing_variant_id: str | None = None
    slot_id: str | None = None
    expression: str = "attentive"
    next: str = "wait_for_person"
    alert_id: str | None = None

    def as_dict(self) -> dict:
        return {
            "role": "agent", "text": self.text, "move": self.move, "phase": self.phase,
            "phrasing_variant_id": self.phrasing_variant_id, "slot_id": self.slot_id,
            "expression": self.expression, "next": self.next, "alert_id": self.alert_id,
        }


def new_state(setting: str, language: str, consent: dict, register: str = "patient", record_prefill: dict | None = None) -> dict:
    return {
        "setting": setting, "language": language, "consent": consent, "register": register,
        "phase": "consent", "turn_counter": 0,
        "presenting_verbatim": None, "problems": [], "late_concerns": [],
        "invitations_used": [], "consecutive_empty_invitations": 0, "problem_list_closed": False,
        "facilitator_index": 0, "last_invitation_id": None,
        "module_queue": [], "active_module": None, "current_slot": None,
        "slot_attempts": {}, "slot_values": {}, "record_prefill": record_prefill or {},
        "fired_rules": [], "undecidable_rules": [], "alerts": [], "closed_by_alert": False,
        "closing_delivered": {}, "patient_corrections": [], "read_back_done": False,
        "transition_log": [], "tone_log": [], "bail_out_reason": None, "ended_at": None,
    }


class Controller:
    def __init__(
        self,
        bundle: ContentBundle,
        extraction: ExtractionProvider | None = None,
        wording: WordingProvider | None = None,
        tone: ToneProvider | None = None,
    ) -> None:
        self.b = bundle
        self.extraction = extraction or RulesExtraction()
        self.wording = wording or TemplateWording()
        self.tone = tone or RulesTone()
        self._lexicon = sorted(set(self.b.lexicon), key=len, reverse=True)
        self._trigger_index: list[tuple[str, str]] = []
        for name, m in self.b.modules.items():
            for term in m.activates_on.terms:
                self._trigger_index.append((term.lower(), name))
        self._trigger_index.sort(key=lambda x: len(x[0]), reverse=True)

    # ---------------------------------------------------------------- helpers
    def _next_turn_id(self, state: dict) -> str:
        state["turn_counter"] += 1
        return f"t{state['turn_counter']}"

    def _say(self, state: dict, text: str, move: str, **kw) -> AgentTurn:
        worded = self.wording.word(text, register=state.get("register", "patient"), language=state.get("language", "en"), intent=move)
        if not passes_guardrails(worded) and move not in ("disclose", "alert", "close", "goodbye", "bail_out"):
            worded = text
        return AgentTurn(text=worded, move=move, phase=state["phase"], expression=MOVE_EXPRESSION.get(move, "attentive"), **kw)

    def _detect_symptoms(self, state: dict, text: str) -> list[dict]:
        t = " " + text.lower() + " "
        found: list[dict] = []
        seen_modules = {p["module"] for p in state["problems"] if p.get("module")}
        seen_terms = {p["term"] for p in state["problems"]}
        for term, module in self._trigger_index:
            if re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", t):
                if module in seen_modules or any(f.get("module") == module for f in found):
                    continue
                found.append({"term": term, "module": module})
        for term in self._lexicon:
            if term in seen_terms or any(f["term"] == term for f in found):
                continue
            if re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", t):
                # skip generic 'pain' if a more specific term already matched this turn
                if term == "pain" and (found or any("pain" in p["term"] for p in state["problems"])):
                    continue
                found.append({"term": term, "module": None})
        return found

    def _module(self, name: str) -> Module:
        return self.b.modules[name]

    def _all_slots(self, state: dict) -> list[tuple[str, Slot]]:
        out: list[tuple[str, Slot]] = []
        for name in state["module_queue"]:
            for s in self._module(name).slots:
                out.append((name, s))
        return out

    def _outstanding(self, state: dict, module_name: str) -> list[Slot]:
        m = self._module(module_name)
        return [s for s in m.slots if s.required and s.id not in state["slot_values"]]

    def _write(self, state: dict, module_name: str, slot: Slot, value, verbatim: str, turn_id: str, source: str = "person", st: str = "filled", confidence: float | None = None) -> None:
        state["slot_values"][slot.id] = {
            "slot_id": slot.id, "module": module_name, "value": value,
            "verbatim": verbatim if slot.verbatim else None, "state": st, "turn_id": turn_id,
            "source": source, "confidence": confidence, "written_at": now_iso(),
        }

    def _rule_values(self, state: dict) -> dict:
        return {k: v["value"] for k, v in state["slot_values"].items() if v.get("state") == "filled"}

    def _evaluate_rules(self, state: dict, turn_id: str) -> list[dict]:
        """Evaluate every red-flag rule in the active modules; return newly fired alerts."""
        values = self._rule_values(state)
        new_alerts: list[dict] = []
        state["undecidable_rules"] = []
        for name in state["module_queue"]:
            m = self._module(name)
            for rf in m.red_flags:
                res = evaluate(rf.fires_when, values)
                if res.missing and not res.fired:
                    state["undecidable_rules"].append({"rule_id": rf.id, "missing": res.missing})
                if res.fired and rf.id not in state["fired_rules"]:
                    state["fired_rules"].append(rf.id)
                    route = self.b.parameters.escalation[state["setting"]][rf.tier]
                    verbatim_bits = [v["verbatim"] for v in state["slot_values"].values() if v.get("verbatim") and v["module"] == name]
                    verbatim = state.get("presenting_verbatim") or (verbatim_bits[0] if verbatim_bits else "")
                    fmt = {k: (v["value"] if not isinstance(v["value"], list) else ", ".join(v["value"])) for k, v in state["slot_values"].items()}
                    fmt["verbatim"] = verbatim
                    try:
                        text = rf.alert.template.format_map(_Default(fmt))
                    except Exception:
                        text = rf.alert.template
                    alert = {
                        "id": f"a{len(state['alerts']) + 1}", "rule_id": rf.id, "module": name, "tier": rf.tier,
                        "route": route.route, "text": text, "verbatim": verbatim if rf.alert.include_verbatim else None,
                        "clock_times": {k: v["value"] for k, v in state["slot_values"].items() if k.endswith("clock_time")},
                        "fired_at": now_iso(), "turn_id": turn_id, "patient_message": route.patient_message,
                    }
                    state["alerts"].append(alert)
                    new_alerts.append(alert)
        return new_alerts

    # ---------------------------------------------------------------- lifecycle
    def start(self, state: dict) -> list[AgentTurn]:
        state["phase"] = "consent"
        disclosure = self.b.parameters.disclosure[state["setting"]]
        return [self._say(state, disclosure, "disclose")]

    def person_turn(self, state: dict, text: str, prosody: dict | None = None) -> tuple[str, list[AgentTurn]]:
        """Returns (person_turn_id, agent turns)."""
        turn_id = self._next_turn_id(state)
        tone = self.tone.classify(text, prosody)
        if state["consent"].get("tone_adaptation"):
            state["tone_log"].append({"turn_id": turn_id, "label": tone.label, "confidence": round(tone.confidence, 2)})
        state["_last_tone"] = tone.label if tone.confidence >= 0.6 else "settled"
        phase = state["phase"]
        state["_current_turn"] = [turn_id, text]
        if state["phase"] == "ended":
            return turn_id, []
        if SERIOUS_Q.search(text) and phase not in ("consent",):
            deflect = self._say(state, self.b.phrasings.deflect["serious"], "deflect")
            turn_id2, rest = turn_id, self._dispatch(state, text, turn_id)
            return turn_id2, [deflect] + rest
        return turn_id, self._dispatch(state, text, turn_id)

    def _dispatch(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        phase = state["phase"]
        handler = {
            "consent": self._on_consent, "open": self._on_open, "summary": self._on_summary,
            "module": self._on_module, "final_invite": self._on_final_invite, "read_back": self._on_read_back,
        }.get(phase)
        if handler is None:
            return []
        return handler(state, text, turn_id)

    # ---------------------------------------------------------------- phases
    def _on_consent(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        if DECLINE.search(text) and not AFFIRM.search(text):
            state["phase"] = "ended"
            state["bail_out_reason"] = "declined_consent"
            state["ended_at"] = now_iso()
            return [self._say(state, self.b.scripts["bail_out"], "bail_out", next="end")]
        if AFFIRM.search(text):
            state["phase"] = "open"
            op = self.b.phrasings.opening[0]
            state["opening_used"] = op.id
            return [self._say(state, op.text, "open", phrasing_variant_id=op.id)]
        return [self._say(state, "Is it all right to go on? You can say yes, or ask for a person instead.", "disclose")]

    def _on_open(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        if state["presenting_verbatim"] is None and text.strip():
            state["presenting_verbatim"] = text.strip()
            state["presenting_turn_id"] = turn_id
            state.setdefault("_person_turns", []).append([turn_id, text])
        found = self._detect_symptoms(state, text)
        if found:
            if state.get("presenting_turn_id") != turn_id:
                state.setdefault("_person_turns", []).append([turn_id, text])
            for f in found:
                state["problems"].append({**f, "turn_id": turn_id, "pulled_by": state.get("last_invitation_id")})
            state["transition_log"].append({"turn_id": turn_id, "new": [f["term"] for f in found], "pulled_by": state.get("last_invitation_id")})
            state["consecutive_empty_invitations"] = 0
            state["last_invitation_id"] = None
            fac = self.b.phrasings.facilitators[state["facilitator_index"] % len(self.b.phrasings.facilitators)]
            state["facilitator_index"] += 1
            return [self._say(state, fac.text, "facilitate", phrasing_variant_id=fac.id)]
        state["consecutive_empty_invitations"] += 1
        distinct = len(set(state["invitations_used"]))
        needed = max(1, self.b.parameters.saturation_invitations)
        if state["consecutive_empty_invitations"] >= needed and distinct >= needed:
            return self._close_problem_list(state)
        unused = [p for p in self.b.phrasings.invitations if p.id not in state["invitations_used"]]
        inv = unused[0] if unused else self.b.phrasings.invitations[len(state["invitations_used"]) % len(self.b.phrasings.invitations)]
        state["invitations_used"].append(inv.id)
        state["last_invitation_id"] = inv.id
        return [self._say(state, inv.text, "invite", phrasing_variant_id=inv.id)]

    def _close_problem_list(self, state: dict) -> list[AgentTurn]:
        state["problem_list_closed"] = True
        state["phase"] = "summary"
        terms = [(p["module"].replace("_", " ") if p.get("module") and p["module"] in self.b.modules and not self.b.modules[p["module"]].activates_on.fallback else p["term"]) for p in state["problems"]]
        terms = list(dict.fromkeys(terms))
        listed = ", ".join(terms[:-1]) + (" and " + terms[-1] if len(terms) > 1 else (terms[0] if terms else ""))
        pv = state.get("presenting_verbatim") or ""
        body = f"You've told me about {listed}. " if listed else ""
        if pv:
            body += f"In your words: \"{pv[:220]}\". "
        text = f"{self.b.phrasings.summary['intro']} {body}{self.b.phrasings.summary['check']}"
        return [self._say(state, text, "summarise")]

    def _activate_modules(self, state: dict) -> None:
        queue: list[str] = []
        unmatched: list[str] = []
        for p in state["problems"]:
            if p.get("module") and p["module"] not in queue:
                queue.append(p["module"])
            elif not p.get("module"):
                unmatched.append(p["term"])
        fallback = next((n for n, m in self.b.modules.items() if m.activates_on.fallback), None)
        if unmatched and fallback and fallback not in queue:
            queue.append(fallback)
            state["generic_problem"] = unmatched[0]
        if not queue and fallback:
            queue.append(fallback)
            state["generic_problem"] = "problem"
        state["module_queue"] = queue

    def _opportunistic_fill(self, state: dict, module_name: str, person_turns: list[tuple[str, str]]) -> None:
        """Fill slots from what the person already said in the open phase, keeping the originating turn id."""
        m = self._module(module_name)
        for s in m.slots:
            if s.id in state["slot_values"] or not s.required:
                continue
            for tid, txt in person_turns:
                prop = self.extraction.propose(s, txt, state.get("language", "en"), opportunistic=True)
                if prop is not None and prop.confidence >= 0.6:
                    self._write(state, module_name, s, prop.value, prop.verbatim, tid, source="person_open_phase", confidence=prop.confidence)
                    break

    def _on_summary(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        found = self._detect_symptoms(state, text)
        for f in found:
            state["problems"].append({**f, "turn_id": turn_id, "pulled_by": "summary"})
        if found:
            state.setdefault("_person_turns", []).append([turn_id, text])
        if text.strip() and not AFFIRM.search(text.strip()[:20]):
            state["patient_corrections"].append({"turn_id": turn_id, "phase": "summary", "text": text.strip()})
        self._activate_modules(state)
        state["phase"] = "module"
        person_turns = state.get("_person_turns", [])
        for name in state["module_queue"]:
            self._opportunistic_fill(state, name, person_turns)
        # rules may already fire from the narrative (for example current pain stated in the opening)
        alerts = self._evaluate_rules(state, turn_id)
        out: list[AgentTurn] = []
        if alerts:
            out.extend(self._deliver_alerts(state, alerts))
            if state["phase"] == "ended":
                return out
        out.extend(self._ask_next(state))
        return out

    def _ask_next(self, state: dict) -> list[AgentTurn]:
        while state["module_queue"]:
            name = state["module_queue"][0] if state.get("active_module") is None else state["active_module"]
            state["active_module"] = name
            outstanding = self._outstanding(state, name)
            if outstanding:
                slot = outstanding[0]
                state["current_slot"] = slot.id
                attempts = state["slot_attempts"].get(slot.id, 0)
                phrasing = slot.phrasings[min(attempts, len(slot.phrasings) - 1)] if slot.phrasings else None
                text = phrasing.text if phrasing else slot.intent
                text = text.replace("{problem}", state.get("generic_problem", "problem"))
                turns: list[AgentTurn] = []
                if slot.stigmatised and slot.preamble:
                    turns.append(self._say(state, slot.preamble, "explain_why"))
                turns.append(self._say(state, text, "ask" if attempts == 0 else "reask", phrasing_variant_id=(phrasing.id if phrasing else None), slot_id=slot.id))
                return turns
            # module complete: move to next
            idx = state["module_queue"].index(name)
            if idx + 1 < len(state["module_queue"]):
                state["active_module"] = state["module_queue"][idx + 1]
                continue
            break
        return self._sweep(state)

    def _on_module(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        name = state["active_module"]
        m = self._module(name)
        current = m.slot(state["current_slot"]) if state.get("current_slot") else None
        filled_now = False
        if current is not None and current.id not in state["slot_values"]:
            prop = self.extraction.propose(current, text, state.get("language", "en"))
            if prop is not None:
                self._write(state, name, current, prop.value, prop.verbatim, turn_id, confidence=prop.confidence)
                filled_now = True
            else:
                state["slot_attempts"][current.id] = state["slot_attempts"].get(current.id, 0) + 1
                if state["slot_attempts"][current.id] >= 2:
                    self._write(state, name, current, None, text.strip(), turn_id, st="unknown", confidence=0.0)
        # opportunistic: other outstanding slots in this module answered in the same breath
        for s in self._outstanding(state, name):
            if s.id == (current.id if current else None):
                continue
            prop = self.extraction.propose(s, text, state.get("language", "en"), opportunistic=True)
            if prop is not None and prop.confidence >= 0.6 and s.value.type != "text":
                self._write(state, name, s, prop.value, prop.verbatim, turn_id, source="person_same_turn", confidence=prop.confidence)
        alerts = self._evaluate_rules(state, turn_id)
        out: list[AgentTurn] = []
        if alerts:
            out.extend(self._deliver_alerts(state, alerts))
            if state["phase"] == "ended":
                return out
        out.extend(self._ask_next(state))
        return out

    def _deliver_alerts(self, state: dict, alerts: list[dict]) -> list[AgentTurn]:
        out: list[AgentTurn] = []
        immediate = [a for a in alerts if a["tier"] == "immediate"]
        for a in immediate:
            out.append(AgentTurn(text=f"{self.b.scripts['alert_prefix']} {a['patient_message']}", move="alert", phase=state["phase"], expression="serious", next="alert", alert_id=a["id"]))
        if immediate and not self.b.parameters.continue_after_immediate_alert:
            state["closed_by_alert"] = True
            for name in state["module_queue"]:
                for s in self._module(name).slots:
                    if s.required and s.id not in state["slot_values"]:
                        state["slot_values"][s.id] = {"slot_id": s.id, "module": name, "value": None, "verbatim": None, "state": "not_asked", "turn_id": None, "source": "sweep", "confidence": None, "written_at": now_iso()}
            out.extend(self._close(state, after_alert=True))
        elif immediate:
            out.append(self._say(state, self.b.scripts["after_alert_continue"], "explain_why"))
        return out

    def _sweep(self, state: dict) -> list[AgentTurn]:
        for name in state["module_queue"]:
            for s in self._module(name).slots:
                if s.required and s.id not in state["slot_values"]:
                    state["slot_values"][s.id] = {"slot_id": s.id, "module": name, "value": None, "verbatim": None, "state": "not_asked", "turn_id": None, "source": "sweep", "confidence": None, "written_at": now_iso()}
        self._evaluate_rules(state, "sweep")
        state["phase"] = "final_invite"
        return [self._say(state, self.b.phrasings.final_something_else, "final_invite", phrasing_variant_id="final")]

    def _on_final_invite(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        found = self._detect_symptoms(state, text)
        for f in found:
            state["late_concerns"].append({**f, "turn_id": turn_id, "text": text.strip()})
        if not found and text.strip() and not re.match(r"^\s*(no|nope|nothing|that's it|that's all|no thanks)\b", text.strip(), re.I):
            state["late_concerns"].append({"term": None, "module": None, "turn_id": turn_id, "text": text.strip()})
        state["phase"] = "read_back"
        return [self._say(state, f"{self.b.phrasings.read_back['intro']} {self._read_back_text(state)} {self.b.phrasings.read_back['check']}", "read_back")]

    def _read_back_text(self, state: dict) -> str:
        parts: list[str] = []
        for name in state["module_queue"]:
            m = self._module(name)
            for s in m.slots:
                v = state["slot_values"].get(s.id)
                if not v or v["state"] != "filled":
                    continue
                val = v["value"]
                if isinstance(val, list):
                    val = ", ".join(x.replace("_", " ") for x in val)
                elif isinstance(val, str):
                    val = val.replace("_", " ")
                parts.append(f"{s.intent.split(',')[0]}: {val}")
        return ("; ".join(parts) + ".") if parts else "I have your description in your own words."

    def _on_read_back(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        if text.strip() and not re.match(r"^\s*(yes|yeah|yep|that's right|correct|right|fine|ok|okay|good|nothing)\b", text.strip(), re.I):
            state["patient_corrections"].append({"turn_id": turn_id, "phase": "read_back", "text": text.strip()})
        state["read_back_done"] = True
        return self._close(state, after_alert=False)

    def _close(self, state: dict, after_alert: bool) -> list[AgentTurn]:
        out: list[AgentTurn] = []
        state["phase"] = "closing"
        same_day = [a for a in state["alerts"] if a["tier"] == "same_day"]
        for a in same_day:
            if a.get("patient_message"):
                out.append(AgentTurn(text=a["patient_message"], move="alert", phase="closing", expression="serious", next="continue_speaking", alert_id=a["id"]))
        primary = state["module_queue"][0] if state["module_queue"] else None
        closing = self._module(primary).closing if primary else None
        if closing is not None:
            watch = ", ".join(closing.watch_for)
            text = f"{self.b.scripts['closing_intro']} {closing.uncertainty} {closing.time_course} Watch for {watch}. {closing.where}"
            state["closing_delivered"] = {"module": primary, "uncertainty": closing.uncertainty, "watch_for": closing.watch_for, "time_course": closing.time_course, "where": closing.where, "delivered_at": now_iso()}
            out.append(AgentTurn(text=text, move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
        not_asked = [k for k, v in state["slot_values"].items() if v["state"] == "not_asked"]
        if not_asked:
            out.append(AgentTurn(text=self.b.scripts["not_asked_note"], move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
        out.append(AgentTurn(text=self.b.scripts["goodbye"], move="goodbye", phase="closing", expression="warm", next="end"))
        state["phase"] = "ended"
        state["ended_at"] = now_iso()
        return out


class _Default(dict):
    def __missing__(self, key: str) -> str:
        return "not asked"
