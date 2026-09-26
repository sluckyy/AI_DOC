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
from app.control.clock import describe_interval, parse_clock
from app.content.schema import ContentBundle, Module, Slot
from app.providers.extraction import ExtractionProvider, RulesExtraction
from app.providers.tone import RulesTone, ToneProvider
from app.providers.wording import TemplateWording, WordingProvider, passes_guardrails

AFFIRM = re.compile(r"\b(yes|yeah|yep|ok|okay|sure|fine|go on|all right|alright|that's fine|of course|please|continue)\b", re.I)
DECLINE = re.compile(r"\b(no|nope|stop|don't|do not|a person|a human|real person|someone else|not the ai)\b", re.I)
SERIOUS_Q = re.compile(r"\b(is it serious|am i going to be ok|is this bad|is it my heart|what do you think it is|what is it|is it dangerous|should i be worried)\b", re.I)
CONFIDENTIALITY_Q = re.compile(r"\b(police|confidential|who (will|can|gets to) see|who sees|does this go (to|on)|on my record|kept private|tell anyone|tell my)\b", re.I)
HEARING_TROUBLE = re.compile(r"\b(can't hear|cannot hear|pardon|what did you say|say that again|speak up|hard of hearing|hearing aid|you're breaking up|breaking up|muffled)\b", re.I)
NEGATED = re.compile(r"\b(no|not|never|without|haven't|hasn't|didn't|don't|doesn't|isn't|wasn't|nor|any)\b(?:\s+\w+){0,3}\s*$", re.I)
COLLATERAL_PRESENT = re.compile(r"\b(my (wife|husband|partner|daughter|son|mum|mother|dad|father|carer|friend|neighbour|nurse)|someone|is with me|is here|with me|beside me|next to me)\b", re.I)

MOVE_EXPRESSION = {
    "disclose": "warm", "open": "attentive", "facilitate": "listening", "invite": "attentive",
    "summarise": "thoughtful", "ask": "attentive", "explain_why": "reassuring_neutral", "deflect": "reassuring_neutral",
    "alert": "serious", "read_back": "thoughtful", "close": "reassuring_neutral", "goodbye": "warm", "bail_out": "serious",
    "final_invite": "attentive", "reask": "attentive", "capability": "attentive", "confirm_time": "thoughtful", "transition": "attentive",
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
        "capability": {}, "capability_step": 0, "collateral_available": None, "gating_needed": [],
        "pending_confirm": None, "deflections": [], "contact_lost": False,
        "read_back_slot_ids": [], "corrections_affecting_alerts": [],
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
        spans: list[tuple[int, int]] = []

        def negated(mm: re.Match) -> bool:
            before = t[max(0, mm.start() - 40):mm.start()]
            before = before.split(",")[-1].split(".")[-1].split(" but ")[-1].split(" and ")[-1] if before else before
            return bool(NEGATED.search(before))

        for term, module in self._trigger_index:
            mm = re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", t)
            if mm and negated(mm):
                state.setdefault("denied_in_narrative", []).append(term)
                spans.append(mm.span())
                continue
            if mm:
                spans.append(mm.span())
                if module in seen_modules or any(f.get("module") == module for f in found):
                    continue
                found.append({"term": term, "module": module})
        for term in self._lexicon:
            if term in seen_terms or any(f["term"] == term for f in found):
                continue
            mm = re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", t)
            if mm:
                a, b = mm.span()
                if any(a < e and b > s0 for s0, e in spans):
                    continue   # part of a phrase a module already claimed ("lower back" inside "lower back pain")
                if negated(mm):
                    state.setdefault("denied_in_narrative", []).append(term)
                    continue
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
        if m.kind == "gating":
            needed = set(state.get("gating_needed", []))
            self._prefill_gates(state)
            return [s for s in m.slots if s.id in needed and s.id not in state["slot_values"]]
        out: list[Slot] = []
        for s in m.slots:
            if not self._candidate(m, s) or not self._applies(state, s, m.kind):
                continue
            if s.repeat_over:
                out.extend(inst for inst in self._repeat_instances(state, s) if inst.id not in state["slot_values"])
            elif s.id not in state["slot_values"]:
                out.append(s)
        first = state.get("time_first") or []
        if first:
            out.sort(key=lambda s_: 0 if s_.id in first else 1)
        return out

    ITEM_NOISE = re.compile(r"^(and|also|then|plus|just|only|um|er|oh|well|i think|i take|there's|there is|the|a|an|some|my)\b\s*", re.I)
    ITEM_NEGATIVE = re.compile(r"^(nothing|none|no|nope|that's (it|all)|not sure|i don't know|don't know|i'm not sure)\b", re.I)

    @classmethod
    def _split_items(cls, text: str) -> list[str]:
        """Medicine names as the patient listed them (D-38: ask per medicine, never per list). Uncertain
        descriptions ("a little white one for my heart") are kept as items so the uncertainty is asked about, not resolved."""
        raw = re.split(r",|;|\band\b|\bplus\b|\balso\b|\.\s+", text)
        items: list[str] = []
        for r in raw:
            t = r.strip(" .")
            t = cls.ITEM_NOISE.sub("", t).strip(" .")
            if not t or cls.ITEM_NEGATIVE.match(t) or len(t.split()) > 8:
                continue
            if t.lower() in (x.lower() for x in items):
                continue
            items.append(t)
        return items[:10]

    def _mention_corpus(self, state: dict) -> str:
        """Everything the person has said so far, for asked_if_mentioned / skipped_if_mentioned (PMH sweep, family follow-ups)."""
        bits = [state.get("presenting_verbatim") or ""]
        bits += [t for _, t in state.get("_person_turns", [])]
        for v in state["slot_values"].values():
            if v.get("verbatim"):
                bits.append(v["verbatim"])
            if isinstance(v.get("value"), str):
                bits.append(v["value"])
        return " ".join(bits).lower()

    @staticmethod
    def _mentioned(corpus: str, terms: list[str]) -> bool:
        return any(re.search(r"(?<![a-z])" + re.escape(t.lower()) + r"(?![a-z])", corpus) for t in terms)

    def _resolve_slot(self, m: Module, slot_id: str) -> Slot | None:
        """A repeat instance "md.per_medicine#2" resolves to a copy of its parent slot carrying the instance id."""
        base, _, _ = slot_id.partition("#")
        slot = m.slot(base)
        if slot is None or "#" not in slot_id:
            return slot
        return slot.model_copy(update={"id": slot_id})

    def _repeat_instances(self, state: dict, slot: Slot) -> list[Slot]:
        src = state["slot_values"].get(slot.repeat_over or "")
        if not src or src.get("state") != "filled" or src.get("value") in (None, "none", "no", []):
            return []
        items = self._split_items(str(src.get("verbatim") or src.get("value") or ""))
        state.setdefault("repeat_items", {})[slot.id] = items
        return [slot.model_copy(update={"id": f"{slot.id}#{i}"}) for i, _ in enumerate(items)]

    def _candidate(self, m: Module, slot: Slot) -> bool:
        """Which slots a section tries to ask. Presentation modules ask required slots; a closing section also asks
        slots that are conditional on a gate, an answer, a mention, a recipient or a repeat source."""
        if slot.required or slot.always:
            return True
        if m.kind == "closing":
            return bool(slot.gates or slot.asked_when or slot.asked_if_mentioned or slot.repeat_over or slot.recipient_key)
        return False

    def _applies(self, state: dict, slot: Slot, module_kind: str = "presentation") -> bool:
        """F-13: a branch depends only on prior answers. Undecidable (a referenced slot unfilled) means ask."""
        if module_kind == "closing" and slot.gates and not slot.always:
            if not any(g in state["module_queue"] for g in slot.gates):
                return False
        if slot.recipient_key is not None:
            if not self.b.parameters.situational_recipients.get(slot.recipient_key):
                return False   # D-47: no named recipient for a positive answer, so the question is not asked
        if slot.asked_if_mentioned or slot.skipped_if_mentioned:
            corpus = self._mention_corpus(state)
            if slot.asked_if_mentioned and not self._mentioned(corpus, slot.asked_if_mentioned):
                return False
            if slot.skipped_if_mentioned and self._mentioned(corpus, slot.skipped_if_mentioned):
                return False
        if not slot.asked_when:
            return True
        res = evaluate(slot.asked_when, self._rule_values(state))
        return res.fired or bool(res.missing)

    def _write(self, state: dict, module_name: str, slot: Slot, value, verbatim: str, turn_id: str, source: str = "person", st: str = "filled", confidence: float | None = None) -> None:
        # D-63 epistemic ladder (Mathematics of Clinical History Taking, s.4): a value mined
        # opportunistically from narrative is a hypothesis until it has been read back to the
        # patient and not corrected; a value from a direct answer is grounded immediately. This
        # never claims levels the system cannot support (no belief propagation, no calibrated
        # confidence) — it only tracks whether a proposition has been exposed for confirmation.
        epistemic_status = None
        if st == "filled":
            epistemic_status = "hypothesis" if source in ("person_open_phase", "person_same_turn") else "grounded"
        state["slot_values"][slot.id] = {
            "slot_id": slot.id, "module": module_name, "value": value,
            "verbatim": verbatim if slot.verbatim else None, "state": st, "turn_id": turn_id,
            "source": source, "confidence": confidence, "written_at": now_iso(),
            "epistemic_status": epistemic_status,
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
                    from app.content.rules import referenced_slot_ids as _refs
                    rule_bits = [state["slot_values"][sid]["verbatim"] for sid in _refs(rf.fires_when) if state["slot_values"].get(sid, {}).get("verbatim")]
                    verbatim_bits = [v["verbatim"] for v in state["slot_values"].values() if v.get("verbatim") and v["module"] == name]
                    verbatim = " | ".join(dict.fromkeys(rule_bits)) if rule_bits else (state.get("presenting_verbatim") or (verbatim_bits[0] if verbatim_bits else ""))
                    fmt = {k: (v["value"] if not isinstance(v["value"], list) else ", ".join(v["value"])) for k, v in state["slot_values"].items()}
                    fmt["verbatim"] = verbatim
                    text = re.sub(r"\{([A-Za-z_][\w.]*)\}", lambda mm: str(fmt.get(mm.group(1), "not asked")), rf.alert.template)
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
        if phase not in ("consent",):
            key = self._deflection_key(text)
            if key:
                nth = sum(1 for d in state["deflections"] if d["key"] == key)
                state["deflections"].append({"turn_id": turn_id, "key": key, "text": text.strip()[:200]})
                line = self.b.phrasings.deflection(key, nth)
                move = "deflect"
                if key == "confidentiality":
                    line = self.b.parameters.confidentiality.get(state["setting"]) or line
                deflect = self._say(state, line, move)
                # a bare question ("so I don't need to worry then?") carries no answer: repeat the question, never record it
                bare_question = text.strip().endswith("?") and len(text.split()) <= 12
                rest = self._repeat_current(state) if (key in ("why", "confidentiality") or bare_question) else self._dispatch(state, text, turn_id)
                return turn_id, [deflect] + rest
        return turn_id, self._dispatch(state, text, turn_id)

    def _deflection_key(self, text: str) -> str | None:
        t = " " + re.sub(r"[^a-z' ]", " ", text.lower()) + " "
        if CONFIDENTIALITY_Q.search(text) and self.b.parameters.confidentiality:
            return "confidentiality"
        for key, phrases in self.b.phrasings.deflect_triggers.items():
            for ph in phrases:
                if f" {ph.lower()} " in t or re.search(r"\b" + re.escape(ph.lower()) + r"\b", t):
                    return key
        if SERIOUS_Q.search(text):
            return "serious"
        return None

    def _repeat_current(self, state: dict) -> list[AgentTurn]:
        """After answering why or a confidentiality question, ask the current question again without counting an attempt."""
        if state["phase"] == "module" and state.get("current_slot"):
            name = state["active_module"]
            slot = self._module(name).slot(state["current_slot"])
            if slot and slot.id not in state["slot_values"]:
                ph = slot.phrasings[0] if slot.phrasings else None
                text = (ph.text if ph else slot.intent).replace("{problem}", state.get("generic_problem", "problem"))
                return [self._say(state, text, "reask", phrasing_variant_id=(ph.id if ph else None), slot_id=slot.id)]
        return []

    def _dispatch(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        phase = state["phase"]
        handler = {
            "consent": self._on_consent, "capability": self._on_capability, "open": self._on_open, "summary": self._on_summary,
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
            state["consent_timestamp"] = now_iso()
            if self.b.parameters.capability_check and self.b.phrasings.capability:
                state["phase"] = "capability"
                state["capability_step"] = 0
                return [self._capability_question(state)]
            return [self._begin_open(state)]
        return [self._say(state, "Is it all right to go on? You can say yes, or ask for a person instead.", "disclose")]

    def _begin_open(self, state: dict) -> AgentTurn:
        state["phase"] = "open"
        enabled = [p for p in self.b.phrasings.opening if p.enabled] or self.b.phrasings.opening
        op = enabled[0]
        state["opening_used"] = op.id
        return self._say(state, op.text, "open", phrasing_variant_id=op.id)

    CAPABILITY_STEPS = ("hearing", "language", "present")

    def _capability_question(self, state: dict) -> AgentTurn:
        step = self.CAPABILITY_STEPS[state["capability_step"]]
        text = self.b.phrasings.capability[step]
        names = self.b.parameters.language_names
        text = text.replace("{supported_languages}", ", ".join(names.get(l, l) for l in self.b.parameters.languages))
        return self._say(state, text, "capability", slot_id=f"cap.{step}")

    def _on_capability(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        """Dialogue pack 2: hearing, language, someone present. Not announced as an assessment."""
        step = self.CAPABILITY_STEPS[state["capability_step"]]
        state["capability"][step] = {"turn_id": turn_id, "text": text.strip()}
        if step == "hearing":
            if HEARING_TROUBLE.search(text) or (DECLINE.search(text) and not AFFIRM.search(text)):
                state["capability"]["hearing_trouble"] = True
                return self._bail_out(state, "hearing_difficulty")
        elif step == "language":
            names = {v.lower(): k for k, v in self.b.parameters.language_names.items()}
            for lang_name, code in names.items():
                if re.search(r"\b" + re.escape(lang_name) + r"\b", text, re.I) and code != state["language"] and not re.search(r"\b(no|english is fine|english)\b", text, re.I):
                    state["language"] = code
                    state["capability"]["language_switched_to"] = code
        elif step == "present":
            state["collateral_available"] = bool(COLLATERAL_PRESENT.search(text)) and not re.match(r"^\s*(no|nope|just me|on my own|alone|nobody)\b", text.strip(), re.I)
        state["capability_step"] += 1
        if state["capability_step"] < len(self.CAPABILITY_STEPS):
            return [self._capability_question(state)]
        return [self._begin_open(state)]

    def contact_lost(self, state: dict) -> None:
        """S-14: the line dropped. The alert stands and records that contact was lost; nothing is de-escalated."""
        state["contact_lost"] = True
        state["contact_lost_at"] = now_iso()
        for a in state["alerts"]:
            if a["tier"] == "immediate":
                a["contact_lost"] = True
                a["contact_lost_at"] = state["contact_lost_at"]
        if state["phase"] != "ended":
            state["bail_out_reason"] = state.get("bail_out_reason") or "contact_lost"
            state["phase"] = "ended"
            state["ended_at"] = now_iso()

    def _time_slots_first(self, state: dict) -> list[str]:
        """F-14/F-15: when a rule is about to fire from the narrative, the module's clock-time slots are asked first,
        so the alert carries confirmed times rather than 'not asked'. Two questions at most; nothing else waits."""
        values = self._rule_values(state)
        ids: list[str] = []
        for name in state["module_queue"]:
            m = self._module(name)
            if m.kind != "presentation":
                continue
            if any(evaluate(rf.fires_when, values).fired and rf.tier == "immediate" and rf.id not in state["fired_rules"] for rf in m.red_flags):
                for s_ in m.slots:
                    if s_.required and s_.absolute_time and s_.value.type == "clock_time" and s_.id not in state["slot_values"]:
                        ids.append(s_.id)
        return ids

    def _bail_out(self, state: dict, reason: str) -> list[AgentTurn]:
        state["phase"] = "ended"
        state["bail_out_reason"] = reason
        state["ended_at"] = now_iso()
        line = self.b.phrasings.capability.get("bail_out_1") or self.b.scripts["bail_out"]
        return [self._say(state, line, "bail_out", next="end")]

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
        pool = [p for p in self.b.phrasings.invitations if p.enabled] or self.b.phrasings.invitations
        unused = [p for p in pool if p.id not in state["invitations_used"]]
        last = state["invitations_used"][-1] if state["invitations_used"] else None
        candidates = unused or [p for p in pool if p.id != last] or pool
        inv = candidates[0]
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
        superseded = {x for n in queue for x in self._module(n).supersedes}
        if superseded:
            queue = [n for n in queue if n not in superseded]
            state["superseded_modules"] = sorted(superseded)
        fallback = next((n for n, m in self.b.modules.items() if m.activates_on.fallback), None)
        if unmatched and fallback and fallback not in queue:
            queue.append(fallback)
            state["generic_problem"] = unmatched[0]
        if not queue and fallback:
            queue.append(fallback)
            state["generic_problem"] = "problem"
        # F-16 shared gating and the closing sections follow the presentation modules
        needed: list[str] = []
        for name, m in self.b.modules.items():
            if m.kind == "gating":
                for s in m.slots:
                    if s.always or any(g in queue for g in s.gates):
                        needed.append(s.id)
                queue.append(name)
        for name, m in self.b.modules.items():
            if m.kind == "closing":
                queue.append(name)
        state["gating_needed"] = needed
        state["module_queue"] = queue

    def _prefill_gates(self, state: dict) -> None:
        """A gate already answered inside a presentation module is copied, not asked again (F-16)."""
        for name, m in self.b.modules.items():
            if m.kind != "gating":
                continue
            for s in m.slots:
                if s.id in state["slot_values"]:
                    continue
                for src in s.prefill_from:
                    v = state["slot_values"].get(src)
                    if v and v.get("state") == "filled":
                        state["slot_values"][s.id] = {**v, "slot_id": s.id, "module": name, "source": f"prefilled_from:{src}", "written_at": now_iso()}
                        break

    def _opportunistic_fill(self, state: dict, module_name: str, person_turns: list[tuple[str, str]]) -> None:
        """Fill slots from what the person already said in the open phase, keeping the originating turn id."""
        m = self._module(module_name)
        for s in m.slots:
            if s.id in state["slot_values"] or not s.required:
                continue
            if s.absolute_time and s.value.type == "clock_time":
                continue   # F-14: asked explicitly and read back, never lifted from the narrative
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
            if self._module(name).kind == "presentation":
                self._opportunistic_fill(state, name, person_turns)
        self._prefill_gates(state)
        # rules may already fire from the narrative (for example current pain stated in the opening)
        state["time_first"] = self._time_slots_first(state)
        if state["time_first"]:
            return self._ask_next(state)
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
                if "#" in slot.id:
                    base, _, idx = slot.id.partition("#")
                    items = state.get("repeat_items", {}).get(base, [])
                    item = items[int(idx)] if idx.isdigit() and int(idx) < len(items) else "that one"
                    text = text.replace("{item}", item)
                turns: list[AgentTurn] = []
                if not state.get("_transition_said") and self.b.phrasings.transition:
                    state["_transition_said"] = True
                    tr = self.b.phrasings.transition[0]
                    turns.append(self._say(state, tr.text, "transition", phrasing_variant_id=tr.id))
                if slot.stigmatised and slot.preamble and attempts == 0:
                    turns.append(self._say(state, slot.preamble, "explain_why"))
                if slot.absolute_time and slot.value.type == "clock_time" and attempts == 0 and self.b.scripts.get("time_ask_prefix") and "time" not in text.lower():
                    text = f"{self.b.scripts['time_ask_prefix']} {text}"
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
        pending = state.get("pending_confirm")
        if pending:
            # F-14: the computed interval was read back; confirm or re-ask, never derive
            state["pending_confirm"] = None
            sv = state["slot_values"].get(pending["slot_id"])
            if AFFIRM.search(text) and not re.match(r"^\s*(no|nope|not quite|wrong)\b", text.strip(), re.I):
                if sv:
                    sv["confirmed_interval_minutes"] = pending["minutes"]
                    sv["confirmed"] = True
                    sv["confirmed_turn_id"] = turn_id
            else:
                state["slot_values"].pop(pending["slot_id"], None)
                state["slot_attempts"][pending["slot_id"]] = state["slot_attempts"].get(pending["slot_id"], 0) + 1
                state["patient_corrections"].append({"turn_id": turn_id, "phase": "time_read_back", "slot_id": pending["slot_id"], "text": text.strip()})
            alerts = [] if self._times_outstanding(state) else self._evaluate_rules(state, turn_id)
            out = self._deliver_alerts(state, alerts) if alerts else []
            if state["phase"] == "ended":
                return out
            return out + self._ask_next(state)
        pass_on = state.get("pending_pass_on")
        if pass_on:
            # D-47: the written record is a separate consent; a no keeps the answer out of the handover
            state["pending_pass_on"] = None
            sv = state["slot_values"].get(pass_on["slot_id"])
            if sv is not None:
                agreed = bool(AFFIRM.search(text)) and not re.match(r"^\s*(no|nope|rather not|don't|do not|not really)\b", text.strip(), re.I)
                sv["pass_on"] = agreed
                sv["pass_on_verbatim"] = text.strip()
                sv["pass_on_turn_id"] = turn_id
            return self._ask_next(state)
        current = self._resolve_slot(m, state["current_slot"]) if state.get("current_slot") else None
        filled_now = False
        if current is not None and current.id not in state["slot_values"]:
            prop = self.extraction.propose(current, text, state.get("language", "en"))
            if prop is not None:
                self._write(state, name, current, prop.value, prop.verbatim, turn_id, confidence=prop.confidence, st=prop.state)
                if "#" in current.id:
                    base, _, idx = current.id.partition("#")
                    items = state.get("repeat_items", {}).get(base, [])
                    state["slot_values"][current.id]["item"] = items[int(idx)] if idx.isdigit() and int(idx) < len(items) else None
                filled_now = True
                routed = self._route_from_review(state, current, prop.value, turn_id)
                if current.pass_on_consent and prop.state == "filled" and prop.value not in (None, "none", "no", [], ["none"]):
                    state["pending_pass_on"] = {"slot_id": current.id}
                    line = self.b.scripts.get("pass_on_ask", "Is it all right if I pass that on to the doctor?")
                    return [self._say(state, line, "ask", slot_id=f"{current.id}.pass_on")]
                if current.absolute_time and current.value.type == "clock_time":
                    now = datetime.now(timezone.utc).astimezone()
                    dt = parse_clock(text, now)
                    if dt is not None:
                        minutes = int((now - dt).total_seconds() // 60)
                        state["slot_values"][current.id]["stated_time"] = dt.isoformat()
                        state["slot_values"][current.id]["interval_minutes_unconfirmed"] = minutes
                        state["pending_confirm"] = {"slot_id": current.id, "minutes": minutes}
                        rb = self.b.phrasings.time.get("read_back", "So that's about {interval} ago. Have I got that right?")
                        alerts = [] if self._times_outstanding(state) else self._evaluate_rules(state, turn_id)
                        out = self._deliver_alerts(state, alerts) if alerts else []
                        if state["phase"] == "ended":
                            return out
                        return out + [self._say(state, rb.replace("{interval}", describe_interval(minutes)), "confirm_time", slot_id=current.id)]
            else:
                state["slot_attempts"][current.id] = state["slot_attempts"].get(current.id, 0) + 1
                if state["slot_attempts"][current.id] >= 2:
                    self._write(state, name, current, None, text.strip(), turn_id, st="unknown", confidence=0.0)
        # opportunistic: other outstanding slots in this module answered in the same breath (presentation modules only;
        # a gate or closing section is asked explicitly, never inferred from an adjacent answer, F-17)
        for s in (self._outstanding(state, name) if m.kind == "presentation" else []):
            if s.id == (current.id if current else None):
                continue
            if s.absolute_time and s.value.type == "clock_time":
                continue
            prop = self.extraction.propose(s, text, state.get("language", "en"), opportunistic=True)
            if prop is not None and prop.confidence >= 0.6 and s.value.type != "text":
                self._write(state, name, s, prop.value, prop.verbatim, turn_id, source="person_same_turn", confidence=prop.confidence)
        alerts = [] if self._times_outstanding(state) else self._evaluate_rules(state, turn_id)
        out: list[AgentTurn] = []
        if alerts:
            out.extend(self._deliver_alerts(state, alerts))
            if state["phase"] == "ended":
                return out
        out.extend(self._ask_next(state))
        return out

    def _times_outstanding(self, state: dict) -> bool:
        first = [sid for sid in (state.get("time_first") or []) if sid not in state["slot_values"] or state.get("pending_confirm", {}) and state["pending_confirm"].get("slot_id") == sid]
        state["time_first"] = first
        return bool(first)

    def _route_from_review(self, state: dict, slot: Slot, value, turn_id: str) -> list[str]:
        """D-37 / F-10: a systems-review positive routes to its presentation module, inserted right after the review
        so it is questioned before the remaining closing sections. Positives already covered are reconciled silently."""
        if not slot.route_to or not isinstance(value, list):
            return []
        superseded = {x for n in state["module_queue"] for x in self._module(n).supersedes}
        added: list[str] = []
        for opt in value:
            target = slot.route_to.get(opt)
            if not target or target not in self.b.modules or self._module(target).kind != "presentation":
                continue
            state.setdefault("ros_elicited", []).append({"option": opt, "module": target, "turn_id": turn_id, "slot_id": slot.id})
            if target in state["module_queue"] or target in superseded or target in added:
                continue
            idx = state["module_queue"].index(state["active_module"]) if state.get("active_module") in state["module_queue"] else 0
            state["module_queue"].insert(idx + 1 + len(added), target)
            state["problems"].append({"term": opt.replace("_", " "), "module": target, "turn_id": turn_id, "pulled_by": "review_of_systems"})
            self._opportunistic_fill(state, target, state.get("_person_turns", []))
            added.append(target)
        return added

    def _deliver_alerts(self, state: dict, alerts: list[dict]) -> list[AgentTurn]:
        out: list[AgentTurn] = []
        immediate = [a for a in alerts if a["tier"] == "immediate"]
        for a in immediate:
            out.append(AgentTurn(text=f"{self.b.scripts['alert_prefix']} {a['patient_message']}", move="alert", phase=state["phase"], expression="serious", next="alert", alert_id=a["id"]))
        if immediate and not self.b.parameters.continue_after_immediate_alert:
            state["closed_by_alert"] = True
            for name in state["module_queue"]:
                for s in self._module(name).slots:
                    mod = self._module(name)
                    if mod.kind == "gating" and s.id not in state.get("gating_needed", []):
                        continue
                    if s.repeat_over:
                        continue
                    if self._candidate(mod, s) and s.id not in state["slot_values"]:
                        state["slot_values"][s.id] = {"slot_id": s.id, "module": name, "value": None, "verbatim": None, "state": "not_asked", "turn_id": None, "source": "sweep", "confidence": None, "written_at": now_iso(), "epistemic_status": None}
            out.extend(self._close(state, after_alert=True))
        elif immediate:
            out.append(self._say(state, self.b.scripts["after_alert_continue"], "explain_why"))
        return out

    def _sweep(self, state: dict) -> list[AgentTurn]:
        for name in state["module_queue"]:
            for s in self._module(name).slots:
                mod = self._module(name)
                if mod.kind == "gating" and s.id not in state.get("gating_needed", []):
                    continue
                if s.repeat_over:
                    continue   # instances exist only for items named; nothing to sweep
                if self._candidate(mod, s) and s.id not in state["slot_values"]:
                    st = "not_asked" if self._applies(state, s, mod.kind) else "not_applicable"
                    state["slot_values"][s.id] = {"slot_id": s.id, "module": name, "value": None, "verbatim": None, "state": st, "turn_id": None, "source": "sweep", "confidence": None, "written_at": now_iso(), "epistemic_status": None}
        self._evaluate_rules(state, "sweep")
        state["phase"] = "final_invite"
        return [self._say(state, self.b.phrasings.final_something_else, "final_invite", phrasing_variant_id="final")]

    def _on_final_invite(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        found = self._detect_symptoms(state, text)
        for f in found:
            state["late_concerns"].append({**f, "turn_id": turn_id, "text": text.strip()})
        if not found and text.strip() and not re.match(r"^\s*(no|nope|nothing|that's it|that's all|no thanks)\b", text.strip(), re.I):
            state["late_concerns"].append({"term": None, "module": None, "turn_id": turn_id, "text": text.strip()})
        if not self.b.parameters.closing_read_back:
            state["read_back_done"] = False
            return self._close(state, after_alert=False)
        state["phase"] = "read_back"
        statement, slot_ids = self._read_back_text(state)
        state["read_back_slot_ids"] = slot_ids
        for sid in slot_ids:
            # D-63 epistemic ladder: exposing a hypothesis to the patient for confirmation is the
            # act of grounding it (s.4.1, L2->L4); it stays grounded unless the reply below corrects it.
            v = state["slot_values"].get(sid)
            if v and v.get("epistemic_status") == "hypothesis":
                v["epistemic_status"] = "patient_grounded"
        return [self._say(state, f"{self.b.phrasings.read_back['intro']} {statement} {self.b.phrasings.read_back['check']}", "read_back")]

    def _read_back_text(self, state: dict) -> tuple[str, list[str]]:
        parts: list[str] = []
        slot_ids: list[str] = []
        for name in state["module_queue"]:
            m = self._module(name)
            for s in m.slots:
                if m.kind == "closing" and not s.read_back:
                    continue   # the closing summary reads back the presentation and the gates; sections are summarised in the handover
                v = state["slot_values"].get(s.id)
                if not v or v["state"] != "filled":
                    continue
                val = v["value"]
                if isinstance(val, list):
                    val = ", ".join(x.replace("_", " ") for x in val)
                elif s.value.type == "text" and isinstance(val, str):
                    val = f'"{val.strip().rstrip(".")}"'   # the patient's own words are read back as a quotation
                elif isinstance(val, str):
                    val = val.replace("_", " ")
                parts.append(f"{s.intent.split(',')[0]}: {val}")
                slot_ids.append(s.id)
        statement = ("; ".join(parts) + ".") if parts else "I have your description in your own words."
        return statement, slot_ids

    def _on_read_back(self, state: dict, text: str, turn_id: str) -> list[AgentTurn]:
        # D-63 conversational repair (s.8, s.8.1): a reply that isn't a bare confirmation means at
        # least one item just read back may be wrong. The system cannot reliably tell which one from
        # free text alone, so rather than silently keep every item at its current status, or discard
        # the correction as an unlinked note, every item in that read-back is flagged pending
        # clarification and dependants (any alert whose rule used one of them) are flagged too.
        # This never overwrites a value or un-fires an alert; it only marks what needs a human look.
        if text.strip() and not re.match(r"^\s*(yes|yeah|yep|that's right|correct|right|fine|ok|okay|good|nothing)\b", text.strip(), re.I):
            slot_ids = state.get("read_back_slot_ids") or []
            affected_alerts: list[str] = []
            for sid in slot_ids:
                v = state["slot_values"].get(sid)
                if v is not None:
                    v["epistemic_status"] = "correction_pending"
            if slot_ids:
                from app.content.rules import referenced_slot_ids as _refs
                for a in state["alerts"]:
                    m = self._module(a["module"]) if a.get("module") else None
                    rule = next((r for r in (m.red_flags if m else []) if r.id == a["rule_id"]), None)
                    if rule and set(_refs(rule.fires_when)) & set(slot_ids):
                        a["correction_flag"] = True
                        affected_alerts.append(a["id"])
            state["patient_corrections"].append({
                "turn_id": turn_id, "phase": "read_back", "text": text.strip(),
                "read_back_slot_ids": slot_ids, "affected_alerts": affected_alerts,
            })
        state["read_back_done"] = True
        return self._close(state, after_alert=False)

    def _close(self, state: dict, after_alert: bool) -> list[AgentTurn]:
        out: list[AgentTurn] = []
        state["phase"] = "closing"
        same_day = [a for a in state["alerts"] if a["tier"] == "same_day"]
        spoken: set[str] = set()
        for a in same_day:
            if a.get("patient_message") and a["patient_message"] not in spoken:
                spoken.add(a["patient_message"])
                out.append(AgentTurn(text=a["patient_message"], move="alert", phase="closing", expression="serious", next="continue_speaking", alert_id=a["id"]))
        primary = next((n for n in state["module_queue"] if self._module(n).kind == "presentation"), None)
        closing = self._module(primary).closing if primary else None
        if closing is not None:
            watch = ", ".join(closing.watch_for)
            text = f"{self.b.scripts['closing_intro']} {closing.uncertainty} {closing.time_course} Watch for {watch}. {closing.where}"
            state["closing_delivered"] = {"module": primary, "uncertainty": closing.uncertainty, "watch_for": closing.watch_for, "time_course": closing.time_course, "where": closing.where, "delivered_at": now_iso()}
            out.append(AgentTurn(text=text, move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
        not_asked = [k for k, v in state["slot_values"].items() if v["state"] == "not_asked"]
        if not_asked:
            out.append(AgentTurn(text=self.b.scripts["not_asked_note"], move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
        if state["setting"] == "gp_booking" and not after_alert:
            if any(n == "medications" for n in state["module_queue"]) and self.b.scripts.get("bring_medicines"):
                out.append(AgentTurn(text=self.b.scripts["bring_medicines"], move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
            fh = state["slot_values"].get("fh.core")
            if fh and fh.get("state") == "filled" and self.b.scripts.get("family_followup_gp"):
                out.append(AgentTurn(text=self.b.scripts["family_followup_gp"], move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking"))
        if self.b.phrasings.what_next:
            wn = self.b.phrasings.what_next[0]
            out.append(AgentTurn(text=wn.text, move="close", phase="closing", expression="reassuring_neutral", next="continue_speaking", phrasing_variant_id=wn.id))
        out.append(AgentTurn(text=self.b.scripts["goodbye"], move="goodbye", phase="closing", expression="warm", next="end"))
        state["phase"] = "ended"
        state["ended_at"] = now_iso()
        return out


class _Default(dict):
    def __missing__(self, key: str) -> str:
        return "not asked"
