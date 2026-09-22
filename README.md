# AI DOC

AI DOC is a conversational health platform whose face is **Dr Sam**: a
gender-neutral doctor avatar that takes a patient's history in their own words
before the clinician sees them, listens actively, and hands the clinician a
narrative handover, a structured record and a provenance-labelled coding document
whose diagnosis block is left empty. Dr Sam does not diagnose, does not decide
urgency, and does not give advice.

The agent's behaviour and content are defined by the product owner's own
documents (the Framework Specification, the Symptom Questioning Library and the
seven domain evidence bases), saved under `design/reference/`. The design pack
under `design/` covers the product, the persona and avatar, emotional tone as a
subordinate modifier, the technical implementation of the four layers, the
evaluation pathway and the decision record. Start with
`design/04_decision_record.md`.

## What is in this repository

| Path | What it is |
| --- | --- |
| `content/` | The content layer on disk in the Framework Specification's slot schema: symptom modules, the context module, the parameters register, phrasings, lexicon, fixed scripts. Edited by clinicians; checked at build time |
| `backend/` | FastAPI API: content loader and the eight authoring checks, the deterministic controller, red-flag rules, handover and coding document, providers (fakes plus Azure OpenAI, Azure Speech, Content Safety, FHIR terminology), persistence, audit, export with the P1 to P14 transcript check |
| `frontend/` | React + TypeScript: consent screen, Dr Sam panel with the SVG avatar and browser speech, clinician handover, structured record, coding document with attestation, study export |
| `infra/azure/` | Bicep for Azure OpenAI, AI Speech, Content Safety, Key Vault with managed identity, blob containers and the container apps, Australia East |
| `tools/` | Blind voice audition for decision D-08 |
| `design/` | The design pack and reference material |

## Quick start (no keys needed)

Everything runs on fake providers: template wording from the library's own
phrasings, rule-based slot extraction, browser speech synthesis and recognition.

```bash
# backend
cd backend
pip install -r requirements-test.txt
CONTENT_DIR=../content python -m app.content.checks     # the eight authoring checks
CONTENT_DIR=../content python -m pytest                  # 20 tests
CONTENT_DIR=../content python -m uvicorn app.main:app --reload

# frontend (second terminal)
cd frontend
npm install
npm run dev            # http://127.0.0.1:5173, proxies /api to the backend
```

Open http://127.0.0.1:5173, accept the consent switches, tap to talk (Chrome or
Edge for microphone recognition) or type. When the conversation ends, follow the
link to the clinician handover.

Docker: `cp .env.docker.example .env.docker && docker compose up --build`.

## Switching on Azure providers

Set these in `backend/.env` or the container app. Each provider falls back to its
fake if unconfigured, so the demo never breaks.

| Variable | Effect |
| --- | --- |
| `MODEL_PROVIDER=azure_openai` plus `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT_PERSONA` | JSON slot extraction and re-wording for register and language, guard-railed against P5, P7, stand-down and diagnosis language |
| `TTS_PROVIDER=azure_rest` plus `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`, `AZURE_SPEECH_VOICE` or `AZURE_SPEECH_VOICES=en=...,vi=...` | Azure neural voices; viseme events are estimated until the Speech SDK is wired |
| `CONTENT_SAFETY_PROVIDER=azure` plus endpoint and key | Screens every spoken turn |
| `TERMINOLOGY_PROVIDER=fhir` plus `TERMINOLOGY_FHIR_BASE` | SNOMED CT-AU binding through a FHIR terminology server |

## The boundary, as the software enforces it

- The controller never asks a hypothesis-testing question, never caps the
  opening, never reassures, never stands down (P11). Any wording that trips the
  guard rails falls back to the stored phrasing.
- Red flags are booleans over filled slots evaluated by code, never model
  judgement; an alert carries the patient's words and routes per setting from the
  parameters register (ED: triage desk; GP booking call: duty GP review for the
  Immediate tier, urgent appointment today for Same-day).
- Every filled slot carries the turn it came from. Unfilled required slots are
  "not asked", never negative. The narrative is generated from slots only.
- The coding document's diagnosis block is generated empty and only a named
  clinician fills it, by attestation, which is the only exportable form.
- Emotional tone changes pace and wording only, is stored only with consent, and
  never enters any clinical logic.

## Demo script for the TGA

See `design/07_demo_script.md`.

## Status

Phase 1 vertical slice: one grounded module (chest pain) plus a generic fallback,
the open phase, saturation, summary, per-slot questioning, red-flag alerts with
three tiers, read-back, safety-net close, handover, coding document, attestation,
export. Not yet built: the standard closing sections (past medical history,
medications, allergies, family, social, functional, ICE, review of systems), the
mental health section (blocked on specialist review), the remaining library
modules, per-language phrasings, real-time speech, the Rive avatar.
