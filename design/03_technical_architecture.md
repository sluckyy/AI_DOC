# 03. Technical architecture

Status: **Proposed**. Implements the four-layer agent defined in the Framework
Specification and the Symptom Questioning Library (`reference/`).

## Stack

Reuse the MedExec Coach foundation as agreed: FastAPI (Python 3.11, SQLAlchemy 2,
Alembic), React 18 + TypeScript (Vite), PostgreSQL, Docker, Azure Container Apps
via Bicep, GitHub Actions. AI DOC is a new repository seeded from those skeletons
with exam code removed. Additions: Azure OpenAI, Azure AI Speech, Azure AI Content
Safety, Key Vault with managed identity, Entra External ID for patient sign-in, a
FHIR terminology server for SNOMED CT-AU, and a Rive avatar.

## Principles

1. The four layers are four codebases with four version numbers, and every
   history records all four (Framework Specification, "Versioning").
2. Code owns every consequential decision: module activation, saturation counts,
   the coverage sweep, red-flag rules, escalation routing and every slot write.
   The model owns wording, which cue to follow, when to elaborate, and the
   handover narrative inside the process rules.
3. Retrieval, not prompting: only the active module's slots enter the model's
   context. The whole library is never in the prompt.
4. Every external provider has a fake so the pipeline runs in tests and in
   `docker compose` with no keys.
5. Keys stay on the server. The browser receives audio, timelines and captions.
6. Health information is sensitive information under the Privacy Act. Australia
   East residency, minimal retention, audit trail.
7. Pipeline first, realtime later: transcribe, think, speak.

## Components

```
Browser                                       API (FastAPI)                                   Azure / services
-------                                       -------------                                   ----------------
Mic, end-of-utterance, prosody, barge-in ──►  POST /conversations/{id}/turns
                                              ├─ Controller (control layer, deterministic)
                                              │    module activation · saturation · sweep · red-flag rules · slot writes
                                              ├─ Process rules P1..P14 (config + transcript tests)
                                              ├─ Content: library loader (YAML modules, context module, closing sections)
                                              ├─ Tone classifier ────────────────────────────► Azure OpenAI (tone prompt)
                                              ├─ Persona model (wording only) ───────────────► Azure OpenAI (streamed)
                                              ├─ Content Safety ─────────────────────────────► Azure AI Content Safety
                                              ├─ Synthesiser ────────────────────────────────► Azure AI Speech (audio + visemes)
                                              ├─ Terminology binder ─────────────────────────► FHIR terminology server (SNOMED CT-AU)
                                              ├─ Alert router ───────────────────────────────► triage desk / GP callback (per setting)
                                              └─ Stores: conversations, slot_values, alerts, handovers, attestations
Avatar (Rive) + captions ◄── audio, visemes, expression, caption ──┘
Clinician review and attestation UI ◄── handover, structured record, alerts
Collateral interview UI (separate conversation linked to the index one)
```

### Content layer on disk

`content/` in the repository, edited by clinicians, with build-time authoring checks.

- `content/modules/<presentation>.yaml`: the Framework Specification's slot schema
  exactly: `module`, `version`, `status`, `activates_on`, `setting`, `slots[]`
  with `id`, `class` (coverage | discriminating | red_flag | context), `intent`,
  `phrasings[]` (id, form, text, use_when), `value`, `evidence` (lr, discriminates,
  citation, grade, population, or `gap: true`), `verbatim`, `negative_reporting`;
  `red_flags[]` with `fires_when`, `action` per setting, `alert` template,
  `suppressible: false`; `closing` with the four safety-net components;
  `prohibited`; `gaps`.
- `content/context.yaml`: the context module, including `ctx.gender`,
  `ctx.sex_recorded`, `ctx.organ_inventory`, `ctx.pregnancy_status`,
  `ctx.medications` (with anticoagulant, antiplatelet, immunosuppressant named),
  `ctx.smoking.pack_years`, `ctx.weight_change`, `ctx.conditions.atrial_fibrillation`,
  `ctx.family_history.sudden_death`, `ctx.exposure.animal_bite`, each with
  `prefill_from`, `confirm`, `gates`.
- `content/closing/*.yaml`: past medical history (five routes, tense rule,
  lay-anchored condition sweep per language), medication inventory (thirteen
  categories, per-medicine fields, allergy fields), family history (trigger
  patterns with thresholds, extended-family phrasing, three-state values), social
  history (contextual prompts; systematic items only where a local response
  exists), functional baseline, ideas-concerns-expectations, review of systems.
- `content/mental_health.yaml`: Columbia Protocol wording and branching,
  escalation per setting. Blocked from runtime until the specialist review flag
  is set.
- `content/parameters/<deployment>.yaml`: the configurable parameters register
  (age thresholds, imaging rules, AUDIT-C threshold, sepsis criteria set, bat
  exposure notification pathway, childbearing range, helplines, escalation
  routes), versioned and visible to reviewers.
- `content/phrasings/`: shared phrasing variants with ids, for P5 invitations
  and the standard closing questions.

Authoring checks (CI, fail the build): every phrasing passes the P7 polarity
check; every discriminating slot has evidence or a declared gap; every red-flag
rule references existing slot ids; every stigmatised slot has a preamble; every
module has all four closing components; no slot id reused or changed without a
version bump; every likelihood ratio declares a derivation population, and pooled
values on presentations with known sex-based disparity declare a stratified value
or a gap; no gating rule references `ctx.gender` or `ctx.sex_recorded`.

### Control layer

`app/control/`: the controller. Holds conversation state: phase, active modules,
the problem list with per-problem saturation state, filled and required slots,
context slot values with prefill provenance, the transition log, the
phrasing-yield log, the route-yield log for past medical history, fired rules and
alerts. Each turn it hands the persona model the phase, the allowed moves, the
active module's outstanding slots (never the whole library), the P-rule
constraints and the register. It parses the person's turn into slot values with
the model's help but writes them itself, stamped with the turn id, and evaluates
red-flag rules after every write and again after the coverage sweep. It never
lets the model skip a phase, cap the opening, ask a hypothesis-testing question,
stand down, or reassure. Immediate-tier rules interrupt the flow and call the
alert router.

### Process layer

`app/process/rules.py`: P1 to P14 as constraints the controller enforces and as
transcript tests the evaluation harness runs over every stored conversation. The
same table, two uses.

### Handover layer

`app/handover/`: narrative generator (from slots only; a narrative clause without
a slot behind it fails validation), structured record renderer, coding document
renderer with provenance and the empty diagnosis block, alert record, safety-net
record, clinician question answering (slots and verbatim only; "I didn't ask"
otherwise), attestation workflow. Ordering rules per D-44. Terminology binding
via `TerminologyProvider` (SNOMED CT-AU through the National Clinical Terminology
Service's Ontoserver or Azure Health Data Services; fake returns stable ids).
Never emits ICD-10-AM codes.

### Dr Sam layer (this pack's contribution)

`app/drsam/`: `ToneProvider` (llm, fake); persona prompt builder (register,
moves, style, P-rule reminders); `SpeechProvider` (azure, fake) returning audio
and a viseme timeline; expression mapper from move to expression; content-safety
gate on every spoken turn. Prompts in `app/prompts/` versioned as the fourth
layer's own component: `drsam_persona_v1.md`, `drsam_register_*_v1.md`,
`drsam_tone_v1.md`, `drsam_handover_narrative_v1.md`.

### Browser

`src/drsam/` (panel, avatar, turn player, utterance recorder with silence
end-point, prosody features, barge-in), `src/intake/` (consent, interview,
read-back, safety-net display), `src/collateral/`, `src/clinician/` (handover
playback, structured record, alerts, question box, attestation editor), `src/companion/` (phase 3).

## Providers

| Concern | v1 | Fake |
| --- | --- | --- |
| Persona and tone model | Azure OpenAI, Australia East | Canned turns by phase and tone |
| Speech-to-text | Azure AI Speech per utterance; real-time from the browser in phase 4 | Placeholder transcript |
| Text-to-speech | Azure AI Speech neural TTS with viseme events | Silent audio plus synthetic visemes |
| Output screening | Azure AI Content Safety | Pass-through |
| Terminology | FHIR terminology server, SNOMED CT-AU | Stable placeholder concept ids |
| Alert routing | ED: triage desk endpoint agreed with the site; GP: callback queue | Logged alert |
| Supplier medication source (phase 3) | My Health Record, Active Script List or dispensing repository, with per-encounter consent | Static list |

## API

| Route | Purpose |
| --- | --- |
| `POST /conversations` | `{setting: ed | gp_booking, language, consent: {ai_disclosure, tone_adaptation, summary_to_clinician}, record_prefill}` |
| `POST /conversations/{id}/turns` | Person's turn: `{transcript?, audio_ref?, prosody, interrupted_at_ms?}`; returns the turn contract, `audio_url`, `visemes`, `caption`, and any alert |
| `POST /conversations/{id}/say` | Fixed scripts: disclosure, alert wording, read-back, safety-net close |
| `POST /conversations/{id}/collateral` | Open the linked collateral interview |
| `POST /conversations/{id}/end` | Close; finalise the handover |
| `GET /conversations/{id}/handover` | Narrative (text and spoken), structured record, alerts, safety-net record |
| `GET /conversations/{id}/coding-document` | Provenance-labelled document, diagnosis block empty |
| `POST /conversations/{id}/clinician-questions` | Answers from slots and verbatim only |
| `POST /conversations/{id}/attest` | Clinician's edited document plus signature; the only exportable form |
| `GET /conversations/{id}/export` | The whole record for the study: transcript, turns, slots, logs, versions |

## Data model

- `conversations`: `id`, `clinic_id`, `person_id`, `setting`, `language`,
  `consent` (JSON), `is_simulation`, `process_version`, `content_version`
  (per-module map), `control_version`, `handover_version`, `prompt_versions`
  (JSON), `parameters_version`, `started_at`, `ended_at`, `bail_out_reason`.
- `turns`: `id`, `conversation_id`, `order`, `role`, `text`, `text_original_language`,
  `move`, `phase`, `active_module`, `slot_id`, `phrasing_variant_id`,
  `expression`, `tone_label`, `tone_confidence` (null without consent), `prosody`,
  `asr_confidence`, `audio_ref`, `viseme_ref`, `latency_ms`, `interrupted_at_ms`,
  `content_safety_result`, `created_at`.
- `slot_values`: `id`, `conversation_id`, `slot_id`, `module`, `module_version`,
  `value`, `verbatim`, `verbatim_original_language`, `state` (filled | not_asked
  | unknown | denied), `source` (person | collateral | prefill | delegated_observation),
  `observer`, `turn_id`, `written_at`. The three-state rule for family history
  and the "not asked versus negative" rule are enforced here.
- `alerts`: `id`, `conversation_id`, `rule_id`, `tier`, `fired_at`, `verbatim`,
  `clock_times` (JSON), `routed_to`, `acknowledged_at`.
- `handovers`: `id`, `conversation_id`, `version`, `narrative`, `structured_record`
  (JSON), `coding_document` (JSON), `safety_net_record`, `rendered_at`.
- `attestations`: `id`, `conversation_id`, `clinician_id`, `handover_version`,
  `diagnosis_block`, `edits`, `signed_at`.
- `collateral_interviews`: linked conversations with `informant_relationship`.
- `experiments`: registered phrasing, stopping-rule and handover-format arms.
- `audit_events`, `ai_cost_events` as before.

## Latency budget

Target: Dr Sam speaks within two seconds of the person's last word. Silence
end-point 1.2 s; upload and transcribe 0.6 s; controller 0.05 s; persona model
first sentence 0.8 s streamed; content safety 0.2 s; synthesis 0.4 s; playback
0.1 s. Immediate-tier alerts fire from the controller on the slot write and do
not wait for speech.

## Voice layer

Every result behind the design is text or form based. The build carries: echo
cancellation and gating so spoken facilitators do not pollute transcription; an
ASR accuracy sub-study on symptom vocabulary, accented English and each v1
language before Stage B; `asr_confidence` per turn with low confidence routing to
`clarify`; silence tolerance of at least three seconds before a facilitator;
per-language lay anchors authored, not translated (D-29).

## Azure resources

| Resource | Notes |
| --- | --- |
| MedExec base: Container Apps environment, ACR, PostgreSQL Flexible Server, storage, Log Analytics | Australia East |
| Azure OpenAI | Persona and tone deployments; no training on data |
| Azure AI Speech | TTS with visemes; STT per utterance; real-time STT token in phase 4 |
| Azure AI Content Safety | Screens every spoken turn |
| Key Vault and managed identity | All secrets |
| Blob containers | Audio cache 7 days; handover documents per clinic retention |
| Entra External ID | Patient sign-in; clinicians via Entra ID |
| Application Insights | Per-stage traces |
| Azure Health Data Services (phase 3) | FHIR export; terminology service if not using Ontoserver |

Environment variables as in the earlier draft, plus `CONTENT_DIR`,
`PARAMETERS_DEPLOYMENT` (for example `sa_health_regional`),
`ALERT_ROUTE_ED`, `ALERT_ROUTE_GP`, `MENTAL_HEALTH_SECTION_ENABLED` (false until
specialist review), `REFUSAL_LIST`.

## Testing

- Content: the authoring checks above; a scripted transcript per module that
  must fire each red-flag rule and a benign one that must not.
- Control: unit tests for saturation counting, module activation by trigger
  phrasing, coverage sweep, rule evaluation over slots including the
  unfilled-required-slot case, tier routing per setting, prohibited actions.
- Process: the P1 to P14 transcript tests run over every stored conversation in
  CI against the fake providers.
- Handover: a clause without a slot fails; not-asked never renders as negative;
  per-slot negative reporting; ordering rules; empty diagnosis block; "I didn't ask".
- API and Playwright as before, plus the collateral interview and the attestation editor.
- Prompt regression: fixed transcripts through the persona prompt; any diagnosis,
  urgency, medication advice, reassurance or stand-down language fails.

## Privacy, security and governance

As before (three consent switches, residency, audit, retention, breach runbook,
scribe-advisory baseline), plus: supplier medication sources need their own
per-encounter consent; the mental health section is disabled until specialist
sign-off; the configurable parameters register has a named deployment owner;
the refusal list has a runtime owner (D-43).
