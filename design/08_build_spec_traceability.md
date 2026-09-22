# 08. Build Specification traceability

Status: **Living**. Maps every requirement in the product owner's Build
Specification (`reference/build_specification_2026-09-23.md`) to the phase 1
slice on `feature/phase-1-vertical-slice`. States: **Met**, **Partial**,
**Not yet**, **Blocked** (waiting on a gate or decision), **Conflict**.

## Invariants

| Invariant | State | Where |
| --- | --- | --- |
| 1 No assertion without a span | Met for the slice | Narrative generated from slots only; every slot carries `turn_id`; `answer_clinician_question` says "I didn't ask" |
| 2 Never reassures | Met | Guard rails in wording (`STAND_DOWN`), deflection script, transcript test P11 |
| 3 Never names a diagnosis | Met | `DIAGNOSIS_WORDS` guard, prompt-regression list, handover has no diagnosis field the agent can fill |
| 4 Collect components, assemble nothing | Met by omission | No instrument scoring exists; D-41 keeps it that way |
| 5 Negatives not uniform | Met | `negative_reporting` per slot; no global summary phrase in the handover |
| 6 Escalation never silent or deferred | Partial | Immediate fires on the slot write; acknowledgement endpoint added; timed further escalation not built |
| 7 Original language preserved | Partial | Language recorded; verbatim stored as spoken; translation marking only when the Azure wording provider is used |

## Functional

| Req | State | Notes |
| --- | --- | --- |
| F-1, F-2 | Met | Disclosure script per setting; decline at any turn ends with the bail-out script; the UI offers "ask for a person" through the same route |
| F-3 | Not yet | No capability check for intoxication or hearing difficulty; distress detection exists but does not bail out (see D-43) |
| F-4 | Not yet | Collateral interview route exists in the API design, not built |
| F-5 | Partial | State is persisted per turn so a resumed session continues; no configurable window or call-back flow |
| F-6, F-7 | Met | Open phase allows facilitators and invitations only; four invitation variants |
| F-8 | Conflict | Spec says two consecutive empty prompts; Framework Specification P13 says three. Now a parameter `saturation_invitations` (default 3). Owner to settle (D-48) |
| F-9 | Met | `transition_log` records new symptoms and the pulling phrasing; `invitations_used` gives position |
| F-10 | Met | Any trigger term routes to its module regardless of framing |
| F-11 | Met | YAML modules; the content model differs in field names from the spec's sketch but carries every field (see D-32) |
| F-12 | Partial | Generic module uses six of the eleven domains; chest pain has its own grounded set |
| F-13 | Met | No branching on inference; rules are booleans over filled slots |
| F-14 | Partial | Clock time captured verbatim; interval computation and read-back confirmation not built |
| F-15 | Not yet | Stroke cluster module not built |
| F-16 | Partial | Context module with `ctx.medications.anticoagulant` and others; only prefill, not yet asked at point of need |
| F-17 | Not yet | Medication closing section not built |
| F-18 to F-20 | Not yet | No delegated observations in the chest pain module; prohibitions are documented, not enforced by code |
| F-21, F-23 | Met by omission | Nothing scored; no screeners in the slice |
| F-22 | Blocked | D-41 |
| F-24 | Met | See invariant 1 |
| F-25 | Met | "Not asked:" line and `state: not_asked` in the structured record |
| F-26 | Partial | Two of the three classes (`explicit`, `omit`); "reported as reassuring" is deliberately absent until a presentation authorises it |
| F-27 | Met | Nothing in the handover can hold a diagnosis, probability, severity or tier beyond the alert tier |
| F-28 | Partial | Prose, structured, transcript layers exist; age and sex now travel in handover metadata when prefilled; not yet attached per finding |
| F-29 | Met | Slots and verbatim only |
| F-30 | Met | Parameters register versioned; active values in handover metadata |
| F-31 to F-33 | Partial | Language plumbed and stated in the handover; per-language authored phrasings not written; machine translation flagged as unvalidated when used |
| F-34 | Partial | `is_simulation` marks the record "research, not for clinical use"; no separate storage |
| F-35 | Partial | Phrasing yields, saturation, alert timestamps, ASR confidence stored; per-turn latency not yet measured |
| F-36 | Not yet | No question-group flagging |

## Safety

| Req | State | Notes |
| --- | --- | --- |
| S-1 | Met | Rules and tiers in YAML; routes in the parameters register |
| S-2 | Met | Rules evaluated after every slot write; immediate interrupts |
| S-3 | Met | Verbatim, rule id, timestamp, turn id, clock times |
| S-4 | Partial | `POST /alerts/{id}/acknowledge` added; timed further escalation not built; no acknowledgement UI at the triage desk |
| S-5 | Met | Nothing lowers a tier; rules are monotonic |
| S-6 | Blocked | Routes agreed (D-42); wording awaits EM review; no-human case open |
| S-7, S-8 | Not yet | See F-3, F-4 |
| S-9 | Blocked | Mental health section disabled until sign-off |
| S-10 | Not yet | Trauma module not built |
| HAZ-1 | Partial | Mitigations F-24 and F-29 built; F-15 and F-17 not; adversarial test set not written |
| HAZ-2 | Partial | Per-slot policy built; prohibited-phrase test exists only for stand-down and diagnosis lists |
| HAZ-3 | Partial | Acknowledgement exists; timer, fault injection and N-22 stop-on-channel-loss not built |
| HAZ-4 | Met | Handover states not-asked and the module's gaps ("no ECG and no troponin") |
| HAZ-5 | Met by omission | |
| HAZ-6 | Not yet | Per-cohort ASR study is a Stage B prerequisite |
| HAZ-7 | Partial | No confidentiality claims are made; scripted governance answer not written |
| HAZ-8 | Met | `reviewed` flag per module; `REQUIRE_REVIEWED_CONTENT=true` refuses to start on unreviewed content; versions in every handover |
| S-11 | Met | Consent recorded with timestamp at start |
| S-12 | Met | No claims made; deflection only |
| S-13, S-14 | Blocked / Not yet | Mental health reviewer; call-drop alert standing not built |
| S-15 | Partial | Tests exist for HAZ-1 provenance, HAZ-4 and HAZ-8; not for every hazard |
| S-16 | Met by policy | Mental health section disabled in content |
| S-17 | Not yet | Evaluation harness |

## Non-functional

| Req | State | Notes |
| --- | --- | --- |
| N-1 | Met | Browser barge-in, except during alert turns |
| N-2 | Not measured | Browser pipeline; p90 to be measured on the Azure path |
| N-3 | Partial | 1.2 s silence end-point in the browser; not yet a deployment parameter |
| N-4 | Met | Re-ask with the second phrasing; the record marks `reask` |
| N-5 | Met | No truncation |
| N-6 | Not yet | Web only; no telephony |
| N-7, N-8 | Not yet | ASR study |
| N-9 | Met | `asr_confidence` per person turn |
| N-10 | Not yet | Read-back of numbers, times and drug names |
| N-11 | Met | Six languages configured (D-29) |
| N-12, N-13 | Partial | Language recorded; no translated screeners exist yet |
| N-14 | Blocked | Owner decision |
| N-15, N-16 | Blocked | Site integration targets |
| N-17 | Met | Content, parameters, model provider, language and consent timestamp in handover metadata |
| N-18 | Met by design | No identity resolution in the agent |
| N-19 | Blocked | Owner decision |
| N-20, N-21 | Met | Bail-out and alert-stopped interviews produce a handover marked partial with where and why |
| N-22 | Not yet | Alert channel health gate |
| N-23 | Assumed | Australia East throughout |
| N-24 | Partial | TLS by platform; retention per artefact [TBC] |
| N-25 | Met | Audit events for handover, coding document and questions |
| N-26 | Blocked | Owner decision; the slice keeps no audio unless Azure TTS caches it |
| N-27 | Partial | `is_simulation` flag; separate consent basis not modelled |
| N-28 | Partial | Provider and deployment names recorded; model version pin depends on the Azure deployment |
| N-29 | Met | CI runs checks and tests on every change |
| N-30 | Met | Stored questions are delivered verbatim; the Azure wording provider is now limited to non-English translation and marks its output unvalidated |
| N-31 | Met | Alert wording is templated |
| N-32 to N-34 | Partial | Telemetry stored in state; no dashboards |
| N-35, N-36 | Blocked / Not yet | Owner decision; cost events not yet recorded |
