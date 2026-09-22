# 05. Build plan

Status: **Proposed**

Each phase ends with something a person can use. Phases 1 and 2 run on fakes, so
they need only D-02, D-07 and D-08 agreed and a first safety-net rule set from the
clinical lead.

## Phase 0: foundations

- Seed the `AI_DOC` repo from the MedExec skeleton: auth, settings, migrations,
  job queue, cost tracking, security middleware, tests, Docker, Bicep. Remove exam
  code. First CI run green.
- Bicep: Azure OpenAI, AI Speech, Content Safety, Key Vault, managed identity,
  blob containers. Deploy to a dev resource group.
- Voice audition. Avatar asset commissioned or chosen.
- Regulatory advice on the v1 boundary requested.

## Phase 1: vertical slice, Dr Sam speaks and listens

Goal: a patient hears the disclosure, tells Dr Sam a story, is reflected back to,
and sees a read-back. Lip sync and three expressions. Runs on fakes.

- `SpeechProvider` (azure, fake), `SttProvider` (azure, fake), `/say`, `/turns`
  with a minimal persona prompt, `summary_delta`, read-back.
- Frontend: consent screen, `DrSamPanel`, `Avatar` with placeholder Rive file
  (attentive, speaking, warm), `useTurnPlayer`, utterance recorder with silence
  end-point, captions, barge-in.
- Tests: API lifecycle on fakes; Playwright intake with the fake microphone.

## Phase 2: safe intake

Goal: the v1 product for patients and clinicians.

- Safety-net rule set v1 with must-trigger and must-not-trigger transcripts.
- Tone classifier and prosody features; response policy; consent switches.
- Full persona prompt with registers; prompt-regression suite on the boundary.
- Content Safety screening.
- Full expression set.
- Structured summary, rendered document, clinician review UI, clinician question
  box (transcript quotes only), audit events.
- Privacy runbook, retention jobs, incident procedure.
- Pilot with one clinic on a waiting-room tablet and a pre-appointment link.

## Phase 3: companion check-ins and integration

- Check-in mode: scheduled conversations, "since last time" with consent, carer
  alerts on change or safety-net events.
- FHIR export of the summary; practice-software integration for the pilot clinic.
- Large-type, slow-rate companion panel.

## Phase 4: latency, realism, teaching

- Real-time STT from the browser with a speech token.
- Evaluate a speech-to-speech model for intake, keeping the pipeline as fallback.
- Teaching mode: Dr Sam as simulated patient from a case file, and as debriefer.
- Blend-shape output for a 3D avatar if the 2D character proves limiting.

## v2 gate: individual triage

Not started until: a regulatory pathway is chosen in writing, a clinical evaluation
plan exists, and the clinical lead has approved a triage protocol. The architecture
reserves the seam: a `TriageProvider` that v1 never calls.

## Definition of done for v1 (phases 1 and 2)

- A patient can complete an intake with Dr Sam on a phone and a tablet, and the
  clinician can read the summary and ask what was said.
- With no keys configured, the whole flow runs on fakes and the suite passes.
- Every scripted red-flag transcript triggers the safety net and ends the intake;
  no scripted benign transcript does.
- The prompt-regression suite finds no diagnosis, urgency or medication language.
- Tone adaptation can be switched off and leaves no labels behind.
- Every view and export of a summary is audited.
- Captions and the text fallback work with speech disabled.
