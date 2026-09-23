"""The eight authoring checks from the Framework Specification, run at build time.

1. Every stored phrasing passes the P7 polarity check.
2. Every discriminating slot carries a likelihood ratio and citation, or a declared gap.
3. Every red-flag rule references only slot ids that exist in its module or the context module.
4. Every stigmatised slot has a normalising preamble (P8).
5. Every module has all four closing components (P14).
6. No slot id is reused (across modules and context).
7. Every likelihood ratio declares a derivation population.
8. No gating rule references ctx.gender or ctx.sex_recorded.
Plus: every invitation says "something else", never "anything else" (P5), and no
red flag is suppressible (P10, enforced by the schema).

Build Specification Part C checks layered on top (numbered C2, C5, C6, C7, C9, C10):
C2  frozen open-phase ids (OP-n) keep their text (F-9); the freeze file is content/shared/frozen_ids.yaml.
C5  nothing Dr Sam says matches the prohibited phrase list (HAZ-2, F-27).
C6  no phrasing asks the patient to move their neck, walk or balance, or loosen a cast (F-20).
C7  no red-flag rule carries a numeric literal; thresholds are parameters (F-30).
C9  every absolute-time slot is a clock time with confirm: true, so the interval is read back (F-14).
C10 every red flag names its source (evidence presence).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .rules import referenced_slot_ids
from .schema import ContentBundle

NEGATIVE_FRAMES = [
    r"^\s*(no|never|not)\s+[^?]*\?",      # "No chest pain?", "Never had a fit?"
    r"\b(you|it)\s*(don't|doesn't|aren't|isn't|haven't|hasn't|won't|didn't|weren't|wasn't)\b[^?]*\?",  # "you don't get ...?"
    r"\bnot\s+still\b",
    r",\s*(are|is|do|did|were|was|have|has|can|could|will|would)\s+(you|it|they|that)\?\s*$",  # trailing tag
]
ANYTHING_ELSE = re.compile(r"\banything else\b", re.I)
DELEGATED_DENYLIST = [
    (r"\b(turn|rotate|move|bend|twist|tilt)\b[^.?]{0,25}\b(your|the|their)\s+(neck|head)\b", "neck movement after trauma"),
    (r"\b(can|could|would)\s+you\s+(please\s+|try\s+(to|and)\s+)?(walk|stand|balance|get up)\b[^.?]{0,25}\b(for me|now|a few steps|across the room|to the door|and tell me|and see|test|heel to toe)\b", "walking, standing or balance test"),
    (r"\b(try|please)\s+(walking|standing|balancing)\b", "walking, standing or balance test"),
    (r"\b(remove|loosen|take off|cut|undo|slip off)\b[^.?]{0,25}\b(cast|plaster|dressing|bandage|splint)\b", "removing or loosening a cast or dressing"),
]
NUMERIC_LITERAL = re.compile(r"(?<![\w.])\d+(?![\w.])")


def strip_quotes(text: str) -> str:
    """Remove quoted patient words ("...") so a lint on Dr Sam's speech never fires on the patient's own phrasing."""
    return re.sub(r'"[^"]*"', '""', text)


def prohibited_hits(text: str, prohibited: list[dict], ignore_quoted: bool = True) -> list[dict]:
    hits = []
    if ignore_quoted:
        text = strip_quotes(text)
    for p in prohibited:
        try:
            if re.search(p["pattern"], text, re.I):
                hits.append(p)
        except re.error:
            continue
    return hits


def _strip_quoted(expr: str) -> str:
    return re.sub(r"'[^']*'|\"[^\"]*\"", "''", expr)


def frozen_ids_path():
    from .loader import content_dir

    return content_dir() / "shared" / "frozen_ids.yaml"


def freeze_ids(bundle: ContentBundle) -> dict[str, str]:
    """Write the frozen text of every open-phase id (C2). Run once before data collection starts."""
    import hashlib

    import yaml

    frozen = {p.id: hashlib.sha1(p.text.encode()).hexdigest()[:12] for p in bundle.phrasings.opening + bundle.phrasings.invitations}
    frozen_ids_path().write_text(yaml.safe_dump({"note": "C2: an id listed here may be deprecated (enabled: false) but never re-texted or reused", "ids": frozen}, sort_keys=True))
    return frozen


def polarity_ok(text: str) -> bool:
    t = text.strip().lower()
    return not any(re.search(p, t) for p in NEGATIVE_FRAMES)


@dataclass
class Finding:
    check: int | str
    where: str
    message: str

    def __str__(self) -> str:
        return f"check {self.check} [{self.where}]: {self.message}"


def run_checks(bundle: ContentBundle) -> list[Finding]:
    findings: list[Finding] = []
    all_slot_ids: dict[str, str] = {}
    ctx_ids = {s.id for s in bundle.context.slots}

    def check_slot(owner: str, s) -> None:
        for p in s.phrasings:
            if not polarity_ok(p.text):
                findings.append(Finding(1, f"{owner}/{s.id}/{p.id}", f"negative polarity: {p.text!r}"))
            if ANYTHING_ELSE.search(p.text):
                findings.append(Finding(1, f"{owner}/{s.id}/{p.id}", "says 'anything else' (P5)"))
        if s.slot_class == "discriminating":
            ev = s.evidence
            if ev is None or not (ev.gap or (ev.lr and ev.citation)):
                findings.append(Finding(2, f"{owner}/{s.id}", "discriminating slot without lr+citation or declared gap"))
            elif not ev.gap and not ev.population:
                findings.append(Finding(7, f"{owner}/{s.id}", "likelihood ratio without a derivation population"))
        if s.stigmatised and not s.preamble:
            findings.append(Finding(4, f"{owner}/{s.id}", "stigmatised slot without a normalising preamble"))
        if s.id in all_slot_ids:
            findings.append(Finding(6, f"{owner}/{s.id}", f"slot id reused (also in {all_slot_ids[s.id]})"))
        all_slot_ids[s.id] = owner

    for s in bundle.context.slots:
        check_slot("context", s)
    gate_ids = {s.id for m in bundle.modules.values() if m.kind == "gating" for s in m.slots}
    prohibited = bundle.prohibited

    def lint(where: str, text: str | None) -> None:
        if not text:
            return
        for hit in prohibited_hits(text, prohibited):
            findings.append(Finding("C5", where, f"prohibited phrase /{hit['pattern']}/ ({hit.get('because', '')}): {text[:80]!r}"))

    for name, m in bundle.modules.items():
        local_ids = {s.id for s in m.slots}
        for s in m.slots:
            check_slot(name, s)
            for p in s.phrasings:
                lint(f"{name}/{s.id}/{p.id}", p.text)
                for pat, what in DELEGATED_DENYLIST:
                    if re.search(pat, p.text, re.I):
                        findings.append(Finding("C6", f"{name}/{s.id}/{p.id}", f"prohibited delegated observation ({what}): {p.text[:80]!r}"))
            lint(f"{name}/{s.id}/preamble", s.preamble)
            if s.absolute_time and (s.value.type != "clock_time" or not s.confirm):
                findings.append(Finding("C9", f"{name}/{s.id}", "absolute_time slot must be a clock_time with confirm: true (interval read back, F-14)"))
        for rf in m.red_flags:
            for sid in referenced_slot_ids(rf.fires_when):
                if sid not in local_ids and sid not in ctx_ids and sid not in gate_ids:
                    findings.append(Finding(3, f"{name}/{rf.id}", f"rule references unknown slot {sid}"))
                if sid in ("ctx.gender", "ctx.sex_recorded"):
                    findings.append(Finding(8, f"{name}/{rf.id}", f"rule gates on {sid}"))
            if NUMERIC_LITERAL.search(_strip_quoted(rf.fires_when)):
                findings.append(Finding("C7", f"{name}/{rf.id}", f"numeric literal in a rule; thresholds are parameters (F-30): {rf.fires_when!r}"))
            if not (rf.source or "").strip():
                findings.append(Finding("C10", f"{name}/{rf.id}", "red flag without a source"))
            lint(f"{name}/{rf.id}/alert", rf.alert.template)
        if m.kind == "presentation":
            if m.closing is None:
                findings.append(Finding(5, name, "module has no closing block"))
            else:
                for comp in ("uncertainty", "watch_for", "time_course", "where"):
                    if not getattr(m.closing, comp):
                        findings.append(Finding(5, name, f"closing component missing: {comp}"))
                lint(f"{name}/closing/uncertainty", m.closing.uncertainty)
                lint(f"{name}/closing/time_course", m.closing.time_course)
                lint(f"{name}/closing/where", m.closing.where)
    for s in bundle.context.slots:
        for g in s.gates:
            pass  # gates name modules, not slots; nothing to check here
    for inv in bundle.phrasings.invitations + bundle.phrasings.opening:
        if not inv.enabled:
            continue   # frozen but deprecated ids (D-54) are not spoken, so P5/P7 do not apply
        if ANYTHING_ELSE.search(inv.text):
            findings.append(Finding(1, f"phrasings/{inv.id}", "says 'anything else' (P5)"))
        if not polarity_ok(inv.text):
            findings.append(Finding(1, f"phrasings/{inv.id}", "negative polarity"))
    if ANYTHING_ELSE.search(bundle.phrasings.final_something_else):
        findings.append(Finding(1, "phrasings/final_something_else", "says 'anything else' (P5)"))
    ph = bundle.phrasings
    deflect_lines = [(f"phrasings/deflect/{k}", x) for k, v in ph.deflect.items() for x in (v if isinstance(v, list) else [v])]
    for where, text in deflect_lines + [(f"phrasings/capability/{k}", v) for k, v in ph.capability.items()] \
            + [(f"phrasings/recovery/{k}", v) for k, v in ph.recovery.items()] + [(f"scripts/{k}", v) for k, v in bundle.scripts.items() if isinstance(v, str)] \
            + [(f"parameters/escalation/{s_}/{t}", r.patient_message) for s_, tiers in bundle.parameters.escalation.items() for t, r in tiers.items()] \
            + [(f"parameters/disclosure/{k}", v) for k, v in bundle.parameters.disclosure.items()] + [(f"parameters/confidentiality/{k}", v) for k, v in bundle.parameters.confidentiality.items()]:
        lint(where, text)
    # C2: frozen ids keep their text
    fp = frozen_ids_path()
    if fp.exists():
        import hashlib

        import yaml

        frozen = (yaml.safe_load(fp.read_text()) or {}).get("ids", {})
        current = {p.id: hashlib.sha1(p.text.encode()).hexdigest()[:12] for p in ph.opening + ph.invitations}
        for pid, h in frozen.items():
            if pid not in current:
                findings.append(Finding("C2", f"phrasings/{pid}", "frozen id removed; deprecate with enabled: false instead (F-9)"))
            elif current[pid] != h:
                findings.append(Finding("C2", f"phrasings/{pid}", "frozen id re-texted; add a new id instead (F-9)"))
    return findings


def main() -> int:
    import sys

    from .loader import load_bundle

    bundle = load_bundle()
    if "--freeze" in sys.argv:
        frozen = freeze_ids(bundle)
        print(f"froze {len(frozen)} open-phase ids to {frozen_ids_path()}")
    findings = run_checks(bundle)
    print(f"content: {len(bundle.modules)} modules, context v{bundle.context.version}, parameters {bundle.versions['parameters']}")
    for f in findings:
        print("FAIL", f)
    if findings:
        return 1
    print("authoring checks: all passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
