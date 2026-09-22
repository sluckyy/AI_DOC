# 04. Decision record

Reply with the ID and "agree", or the change you want. Status moves from
**Proposed** to **Agreed** with a date and who agreed.

| ID | Decision | Proposed default | Alternatives | Why | Status |
| --- | --- | --- | --- | --- | --- |
| D-01 | Audiences | Patients and clinicians in v1; companion in phase 3; students in phase 4 | All four in v1 | Intake plus clinician review is one coherent product; the others reuse it | Proposed |
| D-02 | Clinical scope versus regulation | AI DOC is a history-taking and documentation tool (transcription and structuring; see the evidence review's regulatory section): intake, fixed safety net, health information. No individual triage or advice. Triage, if ever, is a separate v2 under a chosen TGA pathway | Triage in v1 and accept device regulation | The clinical lead set the aim as history taking and documentation. Keeps v1 outside device scope; confirm with a regulatory consultant before the HREC submission | **Agreed** 2026-09-22, clinical lead (product owner) |
| D-03 | Safety net | Deterministic, clinician-authored rules with fixed wording; model never composes it | Model-generated safety responses | Predictable, testable, reviewable like a leaflet | Proposed |
| D-04 | Conversation engine | Transcribe → model → synthesise, streamed per sentence | Speech-to-speech realtime model | Testable, auditable, cheaper, gives visemes; realtime is phase 4 | Proposed |
| D-05 | Tone inputs | Transcript plus browser-computed prosody; no camera | Text only; audio-capable model; camera | Camera emotion recognition is withdrawn on Azure and unacceptable for patients; prosody is cheap signal | Proposed |
| D-06 | Tone thresholds | 0.6 to act; 0.4 for distress | Single threshold | Missing distress costs more than a gentle false alarm | Proposed |
| D-07 | Avatar rendering | Two steps. Simulated-patient testing uses a code-drawn SVG avatar (built in React, animated by CSS and viseme events) that needs no artist. The HREC study uses a stylised 2D character in Rive, commissioned once the SVG version has settled the expression set | 3D glTF; Azure photoreal TTS avatar; static portrait | Nothing blocks the slice on an illustrator; gender-neutral is far easier in stylised art; Azure prebuilt avatars are gendered humans and custom ones need limited-access approval | Proposed |
| D-08 | Voice | Azure AI Speech neural TTS, en-AU, chosen by the blind audition in `tools/voice_audition.py`, SSML-tuned | OpenAI TTS; browser only | Visemes come free; pace and pause control; Australian accent | Proposed; audition pending an Azure Speech resource |
| D-09 | Model hosting | Azure OpenAI in Australia East from day one | OpenAI direct with a switch | Health data: residency, no training on data, enterprise terms. The MedExec helper is adapted, not rewritten | Proposed |
| D-10 | Expression driver | Dr Sam's own turn intent | Person's tone label | Avoids the avatar reacting to a classifier the person cannot see | Proposed |
| D-11 | Barge-in | Supported in all modes | None | People interrupt doctors; Dr Sam should stop and listen | Proposed |
| D-12 | Summary construction | Incremental `summary_delta` per turn, finalised at read-back | Generated once at the end | A dropped call still leaves a summary; the read-back is cheap | Proposed |
| D-13 | Memory | Per-conversation only in v1; check-in mode (phase 3) adds "since last time" from stored summaries with consent | Long-term profile | Minimal by default | Proposed |
| D-14 | Consent | Three explicit switches: AI disclosure, tone adaptation, summary sharing | One blanket consent | Sensitive information; separable purposes | Proposed |
| D-15 | Identity | Entra External ID for patients (or clinic-issued one-time link); Entra ID for clinicians | Own username and password | Less to secure; clinic SSO later | Proposed |
| D-16 | Output screening | Azure AI Content Safety on every model turn plus a prompt-regression suite that fails on diagnosis, urgency or medication language | Prompt only | Two independent layers on the boundary that matters most | Proposed |
| D-17 | Pronouns and neutrality | they/them; enforced in name, voice, art, copy | Selectable gendered variants | One consistent character | Proposed |
| D-18 | Region | Australia East for everything | Cheapest region | Sensitive information, Australian users | Proposed |
| D-19 | Repository | New `AI_DOC` repo seeded from the MedExec skeleton, with exam code removed | Monorepo with MedExec | Separate product, separate compliance story | Proposed |
| D-20 | Fallbacks | Captions always; text conversation continues if speech or avatar fails | Hard requirement on speech | Nobody is blocked from being heard by an animation | Proposed |
| D-21 | Clinician review in v1 | Hear or read the handover, ask what the patient said, attest the coding document; no Dr Sam opinions | Decision support | Keeps v1 outside device scope and builds clinician trust first | Proposed |
| D-22 | Dual output | One interview produces Output A (verbal handover) and Output B (coding document), one attestation covers both | Handover only; coding document only | The evidence review's specification; the coding document is where the documentation-improvement value lives | Proposed, from the evidence review |
| D-23 | Diagnosis block | Always empty when generated; only a clinician fills it; never pre-populated under later pressure | Pre-fill with the patient's stated prior diagnoses | The structural defence against automation bias and the thing that keeps the document on the right side of ACS 0010 | Proposed, from the evidence review |
| D-24 | Terminology binding | SNOMED CT-AU concepts only; no ICD-10-AM codes ever emitted | Emit ICD-10-AM | Coding is the coder's act under standards the agent cannot apply; emitting codes would make the output an automated coding claim | Proposed, from the evidence review |
| D-25 | Provenance | Every field labelled patient-reported, clinician-confirmed, derived or structural, visible without reading the narrative | Provenance in the narrative only | A coder must see the distinction at a glance | Proposed, from the evidence review |
| D-26 | Attestation | An act: open, edit, fill or leave the diagnosis block, sign; the signed version is the only exportable one | A confirm button | Automation bias worsens as accuracy improves; the Victorian scribe advisory names it | Proposed, from the evidence review |
| D-27 | Complexity neutrality | No prompt, rule or metric may reward complication-bearing content; coded complexity shift is a monitored harm in every evaluation | Optimise capture of comorbidities | IHACPA's ethical line between optimisation and maximising; a leading elicitation is invisible in the record | Proposed, from the evidence review |
| D-28 | Red-flag escalation in ED | Fixed safety net escalates to the triage desk; treated as clinical decision support whose regulatory status is asked of the TGA before build, with the digital-scribes guidance as entry point | Assume it is outside scope | The boundary has moved recently; assumptions will not hold | Proposed, needs the owner's call on who asks the TGA |
| D-29 | Interview languages in v1 | English plus the two or three most common non-English languages at the pilot ED, chosen from its interpreter statistics; outputs always in English | English only | Equity is an evaluation endpoint; a capture rate that falls for interpreted histories widens the gap | Proposed, needs the pilot site's data |
| D-30 | GP adoption | The GP version is generated days before the consult and is adopted by one deliberate act at the start of the consult, which is also the attestation | Auto-attach to the record | In ACS terms it is prior-episode documentation until adopted | Proposed, from the evidence review |

## Open questions for the product owner

1. Clinical lead: the product owner (agreed 2026-09-22).
2. Which ED and which GP practice will host the HREC study, and what practice software do they use (for phase 3)?
3. Budget for an illustrator for the Rive character, or a purchased asset for v1?
4. Should companion-mode check-ins be initiated by Dr Sam (scheduled) or only by
   the person or carer?
