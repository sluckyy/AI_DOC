# 10. The Mathematics of Clinical History Taking: what maps to what

D-63 agreed to build a scoped part of the product owner's conceptual paper
(`design/reference/mathematics_of_clinical_history_taking_2026-09-26.md`) into Dr Sam. This
document is the section-by-section accounting: what runs in code now, what an existing
mechanism already does in effect (built before the paper, for the same reason), and what is
deliberately deferred, with why.

The paper itself says the mathematics is "intentionally pluralistic" and that "the research
task is not to prove that every element should be computed literally, but to determine which
representations improve clinical safety, conversational quality and structured data accuracy"
(s.27). This document takes that instruction literally: build what closes a real gap using
information the deterministic pipeline already has; don't decorate the code with formulas that
have no calibrated inputs behind them.

## Built now (D-63, this iteration)

| Paper section | Concept | What runs |
| --- | --- | --- |
| s.4, s.4.1 | Epistemic ladder: a proposition's confirmation status, not just its value | Every filled slot carries `epistemic_status`: `grounded` (a direct answer to the question that produced it), `hypothesis` (mined from the patient's narrative, not yet confirmed), `patient_grounded` (a hypothesis that was read back and not corrected — s.4.1's L2→L4 transition, made explicit rather than silent), `correction_pending` (flagged at read-back, below) |
| s.8, s.8.1 | Conversational repair as a safety mechanism; dependency-aware truth maintenance (`Δpᵢ → re-evaluate descendants(pᵢ)`) | A read-back reply that isn't a plain confirmation marks every item just read back as `correction_pending`, and any already-fired alert whose rule used one of those items gets `correction_flag: true`. Nothing is silently kept as still-grounded, and nothing is silently discarded; the handover surfaces exactly what was read back, what the patient said, and which alerts it may touch, for a clinician to resolve |
| s.4.1 ("absence of evidence in conversation is not evidence of absence") | Not-mentioned / denied / unknown / not-asked stay distinct | Already built before the paper (D-38, D-39): `none_terms`, `unknown_terms`, `not_asked`/`not_applicable` states, explicit closing-section wording ("asked; the patient did not know" vs "asked and denied" vs "not asked") |

What this deliberately does *not* claim: there is no belief distribution, no calibrated
probability, and no NLU that identifies *which* item a free-text correction concerns. The
system flags every candidate and asks a person to resolve it, which is the honest thing a
rule-based extractor can do; claiming more would be exactly the "sound natural while... failing
to preserve uncertainty" failure mode the paper warns against (s.27).

## Already covered by an existing mechanism, before this paper

The build has independently arrived at several of the paper's structures, because they follow
from the same clinical-safety reasoning. No change made here; listed so the mapping is
complete.

| Paper section | Concept | Existing mechanism |
| --- | --- | --- |
| s.3 (Shared Meaning Workspace, `Conversation → Shared Meaning Workspace → Grounded Clinical Model → FHIR`) | Conversational state kept separate from, and stricter than, the structured record | `slot_values` (conversational, revisable) vs the handover's `structured_record` and coding document (compiled, provenance-tagged); D-24's SNOMED-only, no diagnosis inference |
| s.6.1 (functional forms of active listening: reflection, paraphrase, minimal encourager, silence, clarification, summary, signposting) | Active listening as scripted conversational moves, not just questions | The deflection table, `Phrasings.deflection`, the capability check, the closing summary and read-back (D-55), signposting between closing sections |
| s.9, s.9.1 (turn-taking, silence, "speaking as an optimal stopping problem") | Endpointing tuned by register rather than a fixed timeout | `silence_end_of_turn_ms_by_register`, `initial_silence_timeout_ms` (D-61); slow-speech endpointing for the older and aged-care registers |
| s.11 (patient utility includes dignity, privacy, burden) | Consent that can withhold content from the record, not just refuse the question | Per-item `pass_on_consent` (D-60): a "no" keeps the item's content out of the narrative, coding document and export, and the record states only that it was asked and withheld |
| s.12.2 (prospective memory, "return to X after the current narrative", deadline-bound obligations) | Standing questions deferred to a fixed point, never dropped | The shared gating pass after presentation modules (D-57: bat contact, overseas animal), `route_to` inserting a routed module after the current one, time-first slot ordering before immediate-alert evaluation |
| s.13.2 (normalisation, permission to decline, reinforcement after disclosure) | Scripted normalisation and confidentiality language | `content/parameters/*.confidentiality`, the deflection/confidentiality script, `capability_check` phrasing |

## Deliberately deferred, and why

| Paper section | Concept | Why not now |
| --- | --- | --- |
| s.2, s.2.1 | Belief state `bₜ(Z) = P(Zₜ \| O₀:ₜ)` over latent patient/clinician state | No calibrated model produces this distribution; a plausible-looking number here would be worse than no number, since it would look like evidence |
| s.5 | Information-theoretic question selection (`IG(Q) = H(X) - E[H(X\|Q)]`) | The module and slot order is authored by the clinical lead against the library's evidence review (grounded/reviewed states, D-56); replacing that with an entropy-maximising policy needs a real prior over presentations this project doesn't have yet |
| s.6, s.9.1 | Active listening / silence as an explicit expected-value calculation (`V(aₜ)`, `IG_wait(Δt)`) | The *behaviours* are built (see above); the *value function* choosing between them by computed expected value is not — the deterministic controller decides by authored rule, not by optimisation |
| s.13, s.13.1, s.14 | Psychological safety as a continuous state variable (`PSₜ`); humour policy (`H\* = argmax_H[...]`) | These are exactly the "latent constructs" the paper's own Appendix C warns must not be treated as directly observed facts; no humour is scripted anywhere in Dr Sam today, and inventing a safety score to gate one would be the ungrounded-inference failure mode the rest of this document exists to avoid |
| s.16 | Per-patient interaction parameters (`θᴾ`) learned within a conversation | No fast-adaptation loop exists; the register (patient/older) is the only personalisation axis today, and it is explicit and owner-set, not inferred |
| s.17, s.19 | Causal hypothesis representation; `P(Y \| do(A))`, CATE | Nothing in Dr Sam infers causation from conversational behaviour; clinical causal claims from the patient (s.17) stay in the narrative as reported, never promoted to a system-asserted causal link — consistent with existing content authoring checks (C7: no numeric literals in rules) and D-56's evidence-only posture |
| s.18, s.18.1, s.18.2, s.19.1, s.21 | The learning planes: contextual bandits, constrained RL, governed offline policy improvement, micro-randomised trials | There is no interaction dataset, no decision log of `(state, available actions, chosen action, propensity, outcome)`, no simulation environment for candidate policies, and no governance body to approve a policy change. Building the RL/bandit code without any of that would be inert scaffolding, not a working system. This is the largest piece of the paper and the one most explicitly flagged by the paper itself as requiring "explicit governance, safety monitoring, privacy protection and research ethics" (Appendix C) before any of it touches a patient |
| s.20 | Three-plane architecture (conversation / clinical / learning) as a formal separation | The conversation and clinical planes already exist in effect (see the Shared Meaning Workspace row above); the learning plane doesn't exist because there is no learning system yet |
| s.22, s.23, Appendix B | Candidate metrics; testable hypotheses; annotation schema for a future dataset | These describe a research programme (s.26), not a feature to build. They're preserved verbatim in the reference document for when that programme starts |

## Revisiting this

Re-open this mapping when any of the following becomes true, since each removes the specific
reason a row above is deferred: a governed decision log exists and the product owner wants a
first contextual-bandit experiment on a safe, low-stakes conversational choice (unlocks s.18.2);
a real correction dataset exists to validate whether keyword-matching a correction to a specific
slot beats flagging the whole read-back (sharpens the built s.8.1 mechanism instead of widening
it); or the product owner asks for humour or an explicit psychological-safety signal, at which
point s.13/s.14 need their own decision record entry and a conservative, reviewed default, not a
retrofit of this one.
