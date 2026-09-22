# AI DOC

AI DOC is a conversational health platform whose face is **Dr Sam**: a
gender-neutral doctor avatar that listens actively, reads and matches emotional
tone, and speaks with an appropriate register to patients, clinicians, students and
people in aged care.

This repository holds the design record and, from phase 0, the code. Nothing is built yet.
Clinical lead: the product owner. Reference material from other design conversations
belongs in `design/reference/` so it can be cited from the pack. Every document in
`design/` proposes a default and marks it **Proposed** until the product owner
confirms it.

| Document | What it settles |
| --- | --- |
| [design/00_product_brief.md](design/00_product_brief.md) | What AI DOC is, who it serves, v1 scope, the regulatory boundary, non-goals |
| [design/01_persona.md](design/01_persona.md) | Who Dr Sam is: identity, pronouns, voice, appearance, boundaries, register per audience |
| [design/02_interaction_design.md](design/02_interaction_design.md) | Modes, active listening moves, tone taxonomy, response policy, safety net, expressions, turn contract |
| [design/03_technical_architecture.md](design/03_technical_architecture.md) | Stack, Azure resources, pipeline, API, data model, latency, testing, privacy |
| [design/04_decision_record.md](design/04_decision_record.md) | Every decision with proposed default, alternatives and status |
| [design/05_build_plan.md](design/05_build_plan.md) | Phased delivery starting with a vertical slice that runs on fakes |
| [design/06_evaluation_and_ethics.md](design/06_evaluation_and_ethics.md) | Simulated-patient testing, then the HREC study in ED and GP; what each phase must show |
| [tools/voice_audition.py](tools/voice_audition.py) | Blind voice audition for D-08; run with your own Azure Speech key |

Start with `04_decision_record.md`: it is the list of choices that change the build.
