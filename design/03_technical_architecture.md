# 03. Technical architecture

Status: **Proposed**

## Stack

Reuse the MedExec Coach foundation, as agreed: FastAPI (Python 3.11, SQLAlchemy 2,
Alembic), React 18 + TypeScript (Vite), PostgreSQL, Docker, Azure Container Apps
via Bicep, GitHub Actions. AI DOC is a new repository that starts from the
MedExec backend and frontend skeletons (auth, settings, job queue, cost tracking,
security middleware, test harness) with the exam-specific code removed.

Additions specific to AI DOC: Azure AI Speech, Azure OpenAI, Azure AI Content
Safety, Key Vault with managed identity, Entra External ID for patient sign-in,
and a Rive avatar in the frontend.

## Principles

1. Every external provider has a fake so the whole pipeline runs in tests and in
   `docker compose` with no keys.
2. Keys stay on the server. The browser receives audio, timelines and captions,
   or a short-lived speech token, never a key.
3. The safety net is deterministic code, not model output.
4. Health information is sensitive information under the Australian Privacy Act.
   Everything is designed for Australia East residency, minimal retention, and an
   audit trail.
5. Pipeline first, realtime later: transcribe → think → speak is slower than a
   speech-to-speech model but testable, auditable, cheaper, and gives visemes.

## Components

```
Browser (patient / clinician / companion device)         API (FastAPI)                         Azure
------------------------------------------------         -------------                         -----
Mic capture, end-of-utterance, prosody features ──────►  POST /conversations/{id}/turns
                                                         ├─ SafetyNet (rules)  ───────────────► (none; local)
                                                         ├─ ToneClassifier ────────────────────► Azure OpenAI (tone prompt)
                                                         ├─ Orchestrator (persona prompt) ────► Azure OpenAI (streamed)
                                                         ├─ ContentSafety ────────────────────► Azure AI Content Safety
                                                         ├─ Synthesiser ──────────────────────► Azure AI Speech (audio + visemes)
                                                         └─ TurnStore, SummaryStore (Postgres)
Avatar (Rive) + captions + controls ◄── audio, visemes, expression, caption ──┘
Clinician review UI ◄── GET /conversations/{id}/summary
```

### Browser

- `src/drsam/`: `DrSamPanel.tsx`, `Avatar.tsx` (Rive runtime; inputs
  `expression`, `viseme`, `speaking`, `reduced_motion`), `useTurnPlayer.ts`
  (schedules visemes and expression changes against `AudioContext.currentTime`),
  `useUtteranceRecorder.ts` (capture, 1.2 s silence end-point, upload),
  `prosody.ts` (rate, pauses, loudness variance, fillers), `barge.ts`.
- `src/intake/`: consent screen, conversation screen, read-back screen.
- `src/clinician/`: summary view, question box, flag handling.
- `src/companion/`: large-type, slow-rate variant of the panel (phase 3).

### Backend

- `app/services/drsam/safety_net.py`: versioned rule set (YAML), pattern matching
  on the transcript window, fixed responses, unit-tested against scripted
  transcripts in `tests/safety_net_cases/`.
- `app/services/drsam/tone.py`: `ToneProvider` protocol, `llm` and `fake`.
- `app/services/drsam/orchestrator.py`: builds the persona prompt from mode,
  audience register, transcript window, summary so far and tone; streams the
  model; validates the turn contract; applies the response policy constraints;
  requests synthesis per sentence; persists.
- `app/services/drsam/speech.py`: `SpeechProvider` protocol, `azure` and `fake`;
  returns audio bytes and a viseme timeline; caches by SSML hash in Blob Storage.
- `app/services/drsam/content_safety.py`: screens model output before synthesis;
  on a hit the turn is replaced by a `decline` and logged.
- `app/services/drsam/summary.py`: merges `summary_delta` into the structured
  history; renders Output A (handover narrative) and Output B (coding document)
  with field-level provenance; never fills the diagnosis block.
- `app/services/drsam/terminology.py`: `TerminologyProvider` protocol binding
  free-text concepts to SNOMED CT-AU via a FHIR terminology server (the National
  Clinical Terminology Service's Ontoserver, or Azure Health Data Services with
  the SNOMED CT-AU edition loaded); `fake` returns stable placeholder concept ids.
  Emits concepts only, never ICD-10-AM codes.
- `app/services/drsam/attestation.py`: clinician edit-and-sign workflow; records
  who signed what version when; the signed document is the only one exported.
- `app/prompts/`: `drsam_persona_v1.md`, `drsam_register_patient_v1.md`,
  `drsam_register_clinician_v1.md`, `drsam_tone_v1.md`. Versioned, reviewed by
  the clinical lead before release.
- `app/api/conversations.py`, `app/api/clinician.py`, `app/api/consent.py`.

### Providers

| Concern | v1 | Alternatives | Fake |
| --- | --- | --- | --- |
| Persona and tone model | Azure OpenAI, Australia East, a current GPT-4-class model, temperature low for tone | OpenAI direct; another vendor behind the same protocol | Canned turns by mode and tone |
| Speech-to-text | Azure AI Speech, per utterance via the API | Azure real-time STT from the browser with a token (phase 4); OpenAI transcription | Placeholder transcript |
| Text-to-speech | Azure AI Speech neural TTS with viseme events | OpenAI TTS (no visemes) | Silent audio plus synthetic visemes |
| Output screening | Azure AI Content Safety | Model-side only | Pass-through |
| Avatar | Rive character with a state machine | glTF + three.js with blend shapes | Static SVG with expression swap |

## API

All routes authenticated. Patients authenticate with Entra External ID or a
clinic-issued one-time link; clinicians with Entra ID.

| Route | Purpose |
| --- | --- |
| `POST /conversations` | Start: `{mode, audience, clinic_id, consent: {ai_disclosure, tone_adaptation, summary_to_clinician}}` |
| `POST /conversations/{id}/turns` | Person's turn: `{transcript?, audio_ref?, prosody, interrupted_at_ms?}` → turn contract, `audio_url`, `visemes`, `caption` |
| `POST /conversations/{id}/say` | Dr Sam speaks a fixed script (disclosure, safety net, read-back) |
| `POST /conversations/{id}/read-back` | Generate the read-back from the summary so far |
| `POST /conversations/{id}/end` | Close and finalise the summary |
| `GET /conversations/{id}` | Conversation with turns, for resume |
| `GET /conversations/{id}/handover` | Output A: narrative handover, text and optional spoken audio (clinician scope) |
| `GET /conversations/{id}/coding-document` | Output B: field-structured, provenance-labelled document, diagnosis block empty (clinician scope) |
| `POST /conversations/{id}/attest` | Clinician's edited document plus signature; creates an attested version; the only exportable form |
| `POST /conversations/{id}/clinician-questions` | Clinician asks what the patient said about something; answers quote the transcript only |
| `GET /audio/{turn_id}` | Streams cached audio |
| `GET /speech-token` | Phase 4: ten-minute Azure Speech token for browser-side STT |

## Data model

- `clinics`: `id`, `name`, `helplines_override` (JSON), `retention_days`.
- `people`: `id`, `clinic_id`, identity provider subject, display name, preferences
  (JSON: avatar, voice, reduced motion, caption size).
- `conversations`: `id`, `clinic_id`, `person_id`, `mode`, `audience`,
  `setting` (ed | gp), `language`, `consent` (JSON), `started_at`, `ended_at`,
  `safety_net_flags` (JSON), `history` (JSON, the structured capture),
  `handover_ref`, `coding_document_ref`, `is_simulation` (bool),
  `agent_version`, `prompt_version`, `ruleset_version`.
- `history_items`: `id`, `conversation_id`, `block` (symptom | condition |
  medicine | external_cause | risk_factor | social | obstetric), `fields` (JSON),
  `snomed_concept_id`, `snomed_term`, `provenance` (patient_reported |
  clinician_confirmed | derived | structural), `transcript_turn_ids`.
- `attestations`: `id`, `conversation_id`, `clinician_id`, `document_version`,
  `diagnosis_block` (JSON, clinician-entered), `edits` (JSON diff),
  `signed_at`.
- `turns`: `id`, `conversation_id`, `order`, `role`, `text`, `move`,
  `expression`, `tone_label`, `tone_confidence` (null unless consent), `prosody`
  (JSON), `audio_ref`, `viseme_ref`, `model`, `latency_ms` (JSON),
  `interrupted_at_ms`, `content_safety_result`, `created_at`.
- `audit_events`: who viewed or exported which conversation or summary, when.
- `ai_cost_events`: reuse from MedExec, with `drsam_turn`, `drsam_tone`,
  `drsam_stt`, `drsam_tts` event types.

## Multilingual

Azure AI Speech transcribes and synthesises in the languages the pilot needs, and
the persona model converses in them; the structured capture and both outputs are
always produced in English for the clinician. The interview language is recorded
on the conversation so every evaluation measure can be stratified by it. Which
languages ship in v1 is decision D-29.

## Latency budget

Target: Dr Sam begins speaking within two seconds of the person's last word.

| Stage | Budget |
| --- | --- |
| End-of-utterance silence | 1.2 s (floor; real-time STT in phase 4 removes most of it) |
| Upload and transcribe the utterance | 0.6 s |
| Safety net | 0.01 s |
| Tone classification, parallel with the persona call | 0 s added |
| Persona model, first sentence streamed | 0.8 s |
| Content safety on the first sentence | 0.2 s |
| Synthesis of the first sentence | 0.4 s |
| Playback start | 0.1 s |

A `listening` → `thoughtful` expression change at end of utterance covers the gap.

## Azure resources

| Resource | Bicep | Notes |
| --- | --- | --- |
| Resource group, Log Analytics, Container Apps environment, ACR, PostgreSQL Flexible Server, storage | As in MedExec `infra/azure/main.bicep` | Australia East |
| Azure OpenAI | `Microsoft.CognitiveServices/accounts` kind `OpenAI`, plus deployments for the persona model and the tone model | Data stays in the region; not used for training; abuse-monitoring exemption can be requested for health data |
| Azure AI Speech | kind `SpeechServices`, sku `S0` | TTS with visemes; STT per utterance |
| Azure AI Content Safety | kind `ContentSafety` | Screens model output |
| Key Vault + user-assigned managed identity | `Microsoft.KeyVault/vaults`, `Microsoft.ManagedIdentity/userAssignedIdentities` | All secrets; container apps read via identity |
| Blob containers | `audio-cache`, `summaries` | Lifecycle rules: audio 7 days, summaries per clinic retention |
| Entra External ID | Tenant configured outside Bicep | Patient sign-in; clinicians via Entra ID |
| Application Insights | Linked to Log Analytics | Per-stage latency traces |
| Azure Health Data Services (FHIR) | Phase 3 | Summary as a FHIR `Composition` for practice-software integration |

Container Apps support WebSockets and streaming responses natively, so no SignalR.
No Redis until sessions are held in memory across replicas.

Environment variables:

```
AIDOC_MODE_DEFAULT=intake
MODEL_PROVIDER=azure_openai            # azure_openai | openai | fake
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT_PERSONA=
AZURE_OPENAI_DEPLOYMENT_TONE=
TTS_PROVIDER=azure                     # azure | fake | browser
STT_PROVIDER=azure                     # azure | fake
AZURE_SPEECH_REGION=australiaeast
AZURE_SPEECH_VOICE=                    # chosen after the audition
CONTENT_SAFETY_PROVIDER=azure          # azure | fake
TONE_PROVIDER=llm                      # llm | fake
TONE_THRESHOLD=0.6
DISTRESS_THRESHOLD=0.4
SAFETY_NET_RULESET=v1
AIDOC_HELPLINES=000|Lifeline 13 11 14|Beyond Blue 1300 22 4636|1800RESPECT 1800 737 732|healthdirect 1800 022 222
AUDIO_CACHE_DAYS=7
```

Secrets (`AZURE_OPENAI_KEY`, `AZURE_SPEECH_KEY`, `CONTENT_SAFETY_KEY`, database
credentials, JWT secret) live in Key Vault and are referenced, never copied.

## Testing

- Unit: safety-net rules against scripted transcripts (must-trigger and
  must-not-trigger sets, maintained by the clinical lead); turn-contract
  validation; response-policy constraints; summary merging; prosody extraction;
  viseme scheduling.
- API: conversation lifecycle, consent flags honoured (no tone labels stored when
  off), safety-net path ends the intake, clinician scope, audit events, cost
  events, all on fakes.
- Playwright: patient intake with the fake microphone, assertions on captions,
  expression attributes, barge-in and the read-back screen; clinician review.
- Prompt regression: a fixed set of intake transcripts run through the persona
  prompt on every prompt change, reviewed for boundary violations (any diagnosis,
  urgency or medication language fails the build).
- Manual: voice audition; expression review on phone, tablet and desktop; reduced
  motion; a waiting-room noise test for end-of-utterance detection.

## Privacy, security and clinical governance

- Consent is collected in three separate switches: AI disclosure acknowledged,
  tone adaptation, summary shared with the named clinician. Tone off means no
  labels stored and no "how the patient seemed" line.
- Data minimisation: no camera; audio deleted after transcription plus a short
  cache; prosody stored as aggregates; transcripts retained per clinic setting.
- Residency: every Azure service in Australia East. Documented per environment.
- Access: clinicians see only their clinic's conversations; every view and export
  is audited; patients can request their transcript and deletion.
- Notifiable Data Breaches: incident runbook before pilot.
- Clinical governance: a named clinical lead owns the safety-net rule set, the
  persona prompts and the summary format, and signs off each version. Prompt and
  rule versions are recorded on every turn.
- Regulatory: written advice on the v1 boundary before pilot; a v2 pathway
  document before any triage feature is built.
- Logging: turn IDs, latencies, providers and versions; never turn text.
