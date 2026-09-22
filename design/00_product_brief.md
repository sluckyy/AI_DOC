# 00. Product brief

Status: **Proposed**; scope agreed as a history-taking and documentation tool (D-02).
Grounded in the clinical lead's evidence review, `reference/cdi_evidence_review_2026-09-23.md`.

## One paragraph

AI DOC puts a calm, credible doctor in front of a patient before the clinician
sees them, takes a structured history by listening rather than by form, and turns
that one interview into two artefacts: a verbal handover a good registrar would
give, and a coding-ready document whose every field says where it came from and
whose diagnosis block is left empty for the clinician. Dr Sam acts on the supply of
clinical facts, not on their transcription. Nothing Dr Sam writes is codeable until
a clinician reviews, edits and signs it; that attestation is the product's central
act.

## Why this and not a scribe or a coding tool

The Australian evidence says documentation, not coder skill, is the dominant source
of coding error, and that most automation has aimed at extracting codes from notes
already written. Only about three quarters of encounters in the largest Australian
computer-assisted coding study could be coded from the notes at all. Nothing in the
literature generates structured, classification-aware clinical content from the
patient before the encounter. That is the gap AI DOC occupies, and it is also why
its evaluation can carry the blinded clinical reference standard the field lacks.

## Audiences

| Audience | What they get | v1 |
| --- | --- | --- |
| Patients | An unhurried, spoken history-taking conversation before the clinician, in their language, with a fixed safety net | Yes |
| Clinicians | The verbal handover, the coding document to attest, and the ability to ask Dr Sam clarifying questions about what the patient said | Yes |
| Clinical coders | An attested document in which the ACS 0002 significance tests are answerable row by row, with field-level provenance | Yes, via the clinician's attestation |
| Aged care and companion settings | Recurring check-ins with the same face | Phase 3 |
| Students and trainees | Simulated patient and history-taking debrief | Phase 4 |

## Deployment settings

| Setting | How the document arrives | Classification status |
| --- | --- | --- |
| ED room | Taken in the waiting area on a tablet with headphones and a privacy screen; arrives before the clinician and travels with the episode. No published analogue: undifferentiated walk-in presentation is unstudied | Feeds admitted-patient coding directly once attested |
| GP booking call | Taken at home on the patient's own phone, days before the consult: the private, individual setting that gives the largest disclosure advantage. Nearest analogue is the Boston pre-visit feasibility study | Prior-episode documentation until the GP adopts it, so adoption is designed as one deliberate act at the start of the consult |

## What Dr Sam is uniquely placed to supply

1. Facts only the patient holds that the classification needs and that go
   unrecorded: mechanism, place, activity and intent for injuries; onset timing;
   prior diagnoses with who made them and when; whether regular medicines are
   actually taken.
2. The specificity clinical shorthand drops: acute versus chronic, first episode
   versus recurrence, subtype, laterality.
3. Onset relative to presentation, captured at the one moment it is unambiguous.

## What Dr Sam must never do

- Generate a diagnostic label styled as a clinical conclusion. The patient said
  chest pain; the document says chest pain.
- Infer a diagnosis from a symptom pattern and present it as history.
- Be tuned toward output that raises coded complexity. Preferentially eliciting
  complication-bearing content is the automated form of a leading query.
- Emit ICD-10-AM codes. Dr Sam binds to SNOMED CT-AU concepts; coding is the
  coder's act under standards the agent cannot apply.
- Pre-populate the diagnosis block, now or under later pressure.

## Regulatory position

Transcription and structuring sit outside medical-device regulation. Red-flag
escalation to a triage desk is clinical decision support and plausibly inside it.
The coding document is the ambiguous case. The TGA's digital-scribes guidance is
the entry point and the boundary has moved recently, so the question goes to the
TGA before the build, not after (D-02, D-28).

## The claim we make

Dr Sam does not interrupt at eleven seconds, solicits an agenda every time, never
asks a leading question about substance use, and does not lose a third of reported
symptoms before the note. Against a clinician under time pressure that will look
good, and the comparison is fair, but it is a comparison against degraded practice.
The defensible claim is consistency: the same questioning discipline at 3 am on the
twelfth patient. The evaluation is powered for variance, not only mean agreement,
and the protocol says which claim is being made. On the GP booking call the honest
comparator is the status quo, where none of this information exists at booking.

## Where it will run first

A regional South Australian health network (SA Health), as the library's
parameters register and the social history evidence base assume. Remoteness is
the social determinant that matters most there: transport, accommodation for
accompanying family and the cost of returning for follow-up decide whether a plan
is executable. Local thresholds, notification pathways and escalation routes are
deployment configuration with a named owner (D-45).

## Non-goals for v1

- Diagnosis, urgency scoring, medication advice, any clinical conclusion.
- Writing into a practice or hospital record system without attestation
  (integration is phase 3, and always behind the attestation step).
- Camera or video analysis of the person.
- Use outside Australia.
- Presentations on the refusal list (D-43), and major, penetrating or
  multi-system trauma, which escalate on disclosure without questioning.

## Success measures

Defined by the evaluation plan in `06_evaluation_and_ethics.md`: history
agreement with a clinician-taken history, condition capture, coder-facing
sufficiency, note quality, fabricated-content rate, red-flag sensitivity, equity
across interview language and age. Coded complexity is reported as a monitored
harm, never as a success measure.
