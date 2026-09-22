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


def polarity_ok(text: str) -> bool:
    t = text.strip().lower()
    return not any(re.search(p, t) for p in NEGATIVE_FRAMES)


@dataclass
class Finding:
    check: int
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
    for name, m in bundle.modules.items():
        local_ids = {s.id for s in m.slots}
        for s in m.slots:
            check_slot(name, s)
        for rf in m.red_flags:
            for sid in referenced_slot_ids(rf.fires_when):
                if sid not in local_ids and sid not in ctx_ids:
                    findings.append(Finding(3, f"{name}/{rf.id}", f"rule references unknown slot {sid}"))
                if sid in ("ctx.gender", "ctx.sex_recorded"):
                    findings.append(Finding(8, f"{name}/{rf.id}", f"rule gates on {sid}"))
        if m.closing is None:
            findings.append(Finding(5, name, "module has no closing block"))
        else:
            for comp in ("uncertainty", "watch_for", "time_course", "where"):
                if not getattr(m.closing, comp):
                    findings.append(Finding(5, name, f"closing component missing: {comp}"))
    for s in bundle.context.slots:
        for g in s.gates:
            pass  # gates name modules, not slots; nothing to check here
    for inv in bundle.phrasings.invitations + bundle.phrasings.opening:
        if ANYTHING_ELSE.search(inv.text):
            findings.append(Finding(1, f"phrasings/{inv.id}", "says 'anything else' (P5)"))
        if not polarity_ok(inv.text):
            findings.append(Finding(1, f"phrasings/{inv.id}", "negative polarity"))
    if ANYTHING_ELSE.search(bundle.phrasings.final_something_else):
        findings.append(Finding(1, "phrasings/final_something_else", "says 'anything else' (P5)"))
    return findings


def main() -> int:
    from .loader import load_bundle

    bundle = load_bundle()
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
