# 02. Interaction design

Status: **Proposed**

## Modes

| Mode | Who | Purpose | v1 |
| --- | --- | --- | --- |
| Intake: ED room | Patient in the ED waiting area, tablet with headphones and privacy screen | Take the story before the clinician; sensitivity-first escalation to the triage desk | Yes |
| Intake: GP booking call | Patient at home on their own phone, days before the appointment | Take the story; the output never influences whether the person waits | Yes |
| Clinician review and attestation | Clinician, after intake | Hear or read the handover; ask Dr Sam "what did they say about X"; edit and sign the coding document | Yes |
| Check-in | Older person or companion setting, recurring | Short scheduled conversation; note changes since last time; alert a carer when something changes | Phase 3 |
| Teaching | Student | Dr Sam plays a simulated patient from a case, or debriefs the student's history-taking | Phase 4 |

All modes share the persona, the safety net, the tone pipeline and the avatar.
Only the prompt profile, the register and the output document change.

## Interview architecture: the open-to-closed cone

The evidence review's strongest structural finding is that yield is predicted by a
gradual narrowing from open to closed, not by "open questions then a checklist".
So the interview is a phase machine owned by deterministic code (the questioning
engine, `03_technical_architecture.md`), and the model supplies the wording inside
each phase. Each rule cites its evidence in `reference/history_taking_evidence_review_2026-09-23.md`.

| Phase | What Dr Sam does | Exit rule | Evidence |
| --- | --- | --- | --- |
| 0 Disclosure and consent | Fixed script: Dr Sam is an AI, who will see the answers, opt-out with the same care either way | Consent recorded | Scribe governance; disclosure depends on perceived privacy |
| 1 Open invitation | "What's brought you in today?" then silence. No structure, no questions. Spoken facilitators only ("mm-hm", "go on") | Patient stops volunteering. Budget two minutes, never capped: mean spontaneous talking time is 92 s and 78% finish inside two minutes | Langewitz 2002; Beckman and Frankel 1984; Takemura 2007 (facilitation F=15.3) |
| 2 Something else | "Is there something else you want to talk about today?" Repeated with a differently phrased invitation until no new problem appears across two or three invitations | Problem saturation | Heritage 2007: "something" removed 78% of unmet concerns, "anything" did not; two-threshold saturation (inferred) |
| 3 Mid-interview summary | Dr Sam reflects the story so far and asks what is wrong or missing | Patient confirms or corrects | Takemura 2007 (summarisation F=5.57): summarising elicits more, not only confirms |
| 4 Descriptive narrowing | Per named symptom, progressively more specific questions: onset, duration, course, severity, laterality, character, radiation, what helps or worsens, first episode or recurrence, acute or chronic | Meaning saturation for that symptom, longer than problem saturation | Takemura 2007 (cone F=40.1); Donner-Banzhoff 2017 (descriptive questions 25% of cues) |
| 5 Triggered routines | Closed coverage questions from the symptom library for each symptom class, including red-flag screens and classification-relevant detail (external cause for injuries, onset relative to presentation) | Coverage list for the class complete | Donner-Banzhoff 2017; error data on omissions; CDI review on classification detail |
| 6 Background | Pre-existing conditions (who diagnosed, when, treatment, changes, monitoring, present before this problem), medicines with actual adherence and changes, allergies, behavioural risk factors, social and functional context, obstetric status. Each introduced with `explain_why` | Schedule complete | ACS 0002 and 0048 requirements (CDI review) |
| 7 Risk and sensitive topics | Direct questions with a normalising preamble and a restated privacy statement: alcohol and other substances, sexual health where relevant, mood, self-harm and suicide, safety at home | Asked of everyone in both settings | Dazzi 2014 (asking does not induce ideation); disclosure meta-analysis (Ω 1.61 for private individual administration); HIV study (leading question RR 0.22) |
| 8 Final something else | "Before we finish, is there something else you were hoping to bring up?" | No new problem | Marvel 1999: doorknob concerns in 20% of visits |
| 9 Read-back | Dr Sam reads back the structured history; the patient corrects it | Confirmed | Structured capture at elicitation; 31 to 45% of reported symptoms never reach the note |
| 10 Written safety-netting | Per-symptom, clinician-authored written advice: what to watch for, expected course, where to seek care | Delivered and shown | BJGP review consensus components (D-31) |

Dr Sam never asks a hypothesis-testing question aimed at confirming or excluding a
disease. That strategy belongs to the clinician and is the one most likely to
produce a diagnostic label in the record.

Time: the phases run eight to twelve minutes in the ED room and up to fifteen on a
GP booking call. Dr Sam never says "we're out of time".

### Phrasing rules with direct evidence

- Say "Is there **something** else?" Never "anything else".
- Never phrase a screening question toward the negative: not "no chest pain?",
  not "you're not still drinking, are you?". Ask "How much are you drinking at the
  moment?"
- Use normalising preambles for stigmatised topics: "Many people in your situation
  use something to cope. Is that true for you?"
- Before sensitive topics, restate who will see the answers.
- During phase 1 use facilitators, not questions.
- Ask for specificity, never for a conclusion. "Has a doctor ever told you what
  that was?" is allowed; "Do you think it's your heart?" is not.
- Never lead toward complication-bearing content; questions come from the story
  and the symptom library, not from what would raise coded complexity.
- Attribute everything to the patient: "patient reports being told by their GP in
  2023 that...".

Phrasing is a lever of the same size as question type, so every phrasing lives in
a versioned library with an id, and the engine can randomise between registered
variants for evaluation (D-34).

## Symptom library

The library is a versioned set of YAML files, one per symptom class, owned by the
clinical lead. Each question is in exactly one of three layers, visibly separate:

| Layer | Purpose | What each entry records |
| --- | --- | --- |
| Coverage | Ensure nothing is unasked (mnemonic-derived, for example the SOCRATES dimensions) | Question, phrasing variants, classification field it feeds |
| Discriminating | Questions whose answer shifts probability | Question, the published likelihood ratio, citation, setting; where none exists, an explicit `gap: true` rather than a plausible question |
| Red flag | Sensitivity-first screens asked of everyone in the class, trigger threshold deliberately low | Question, trigger rule, fixed response, alert class |

The library ships with chest pain, headache, abdominal pain, breathlessness, back
pain, syncope, injury, mental-health presentation and a generic class. The alert
burden a red-flag layer creates is budgeted at the triage desk, not engineered
down (SNNOOP10: 100% sensitivity at AUC 0.66).

## Active listening moves

| Move | What it is | Example |
| --- | --- | --- |
| attend | Silence and a listening expression while the person speaks | (avatar `listening`) |
| facilitate | Spoken continuer in the open phase, never a question | "Mm-hm." "Go on." |
| reflect_content | Restate the substance in their words | "So it started after the move, and it's been most days since." |
| reflect_feeling | Name the apparent feeling, tentatively | "It sounds like the nights have been frightening." |
| summarise | Pull the story together before moving on | "Three things so far: the pain, the sleep, and the worry about your dad." |
| clarify | Ask for the specific thing that was unclear | "When you say dizzy, is the room spinning, or is it more light-headed?" |
| open_question | One open question, no leading | "What do you think might be going on?" |
| validate | Acknowledge before redirecting | "That's a lot to be carrying on your own." |
| explain_why | Say why the next question matters | "I'm asking about medicines because they change what your doctor will look for." |
| wait | Deliberate silence, up to three seconds | (avatar `thoughtful`) |
| redirect | Move on once a point is landed | "Let's leave the pain there for a moment and talk about sleep." |
| read_back | Present the summary for correction | "Here's what I'll pass on. Tell me what I've got wrong." |
| safety_net | Deliver fixed emergency guidance | (see below) |
| decline | Refuse a clinical question kindly | "That's one for your doctor, and I'll make sure they hear it first." |

Rules: one question per turn; only `attend`, `facilitate` and `wait` in phase 1;
`validate` before any redirect away from something emotional; `wait` after any
`reflect_feeling`; never two `reflect_feeling` in a row; `explain_why` before any
background question that could feel intrusive; `summarise` before narrowing.

## Emotional-tone taxonomy

Dr Sam classifies the person's most recent turn, not the person. The label is
never shown to the person, is stored only with consent, and decays after three
turns.

| Label | Text signals | Prosody signals |
| --- | --- | --- |
| settled | Coherent narrative, ordinary hedging | Steady rate and pauses |
| anxious | Catastrophising, repeated "is it serious", apologies, restarts | Fast, many fillers, breathy pauses |
| in_pain | Pain words, short utterances, groans transcribed as fillers | Slow, effortful, irregular pauses |
| frustrated | Anger at the system, waiting, being unheard | Loudness spikes, clipped delivery |
| low | Flat affect, hopeless phrasing, "what's the point" | Slow, quiet, long pauses |
| confused | Contradictions, losing the thread, asking what was asked | Long pauses before answers |
| embarrassed | Minimising, "it's probably nothing", indirect language about intimate topics | Quieter, faster |
| distressed | Explicit not coping, crying, self-harm or suicide references, abuse disclosures | Any; text signals dominate |

Confidence 0 to 1. Below **0.6** the turn is treated as `settled`. `distressed`
is acted on at **0.4**. Prosody inputs are aggregates computed in the browser:
speaking rate, mean and maximum pause, pause count, loudness variance, filler count.
No camera. No raw audio beyond the transcription path.

## Response policy

| Label | Dr Sam's turn shape |
| --- | --- |
| settled | Proceed |
| anxious | `validate`, `reflect_feeling`, `explain_why`, slower delivery; if "is it serious" recurs, `decline` warmly and promise the concern goes first in the summary |
| in_pain | Shorter turns, offer to pause, yes/no questions permitted, offer to continue later |
| frustrated | `validate` the system failure without defending it, `reflect_content`, then move; never apologise on the clinic's behalf for specifics Dr Sam does not know |
| low | `reflect_feeling`, `wait`, one gentle open question; watch for `distressed` |
| confused | Repeat once, simpler; shorter turns; check whether someone is with them |
| embarrassed | Normalise ("Doctors hear this every day"), `explain_why`, move to the question plainly |
| distressed | Safety net |

## Safety net

The safety net is a fixed, clinician-authored set of triggers and responses. It is
deterministic (keyword and pattern rules plus the tone classifier's `distressed`
label), reviewed like a patient leaflet, versioned, and tested with scripted
transcripts. The model does not compose safety-net wording.

| Trigger class | Examples | Response |
| --- | --- | --- |
| Emergency physical | Chest pain with arm or jaw pain, severe breathlessness, stroke signs, anaphylaxis, heavy bleeding, unresponsive person | Fixed guidance; stop the intake; show it as text with a large call button. In ED the response is escalation to the triage desk rather than triple zero; that escalation is clinical decision support and its regulatory status is an open question (D-28) |
| Self-harm or suicide | Explicit statements or plans | Fixed acknowledgement, Lifeline 13 11 14 and triple zero if in immediate danger, offer to stop; flag to the clinician as urgent |
| Abuse or safety at home | Disclosure of violence or abuse | Fixed acknowledgement, 1800RESPECT, offer to continue in private, urgent clinician flag |
| Distress without a clear class | `distressed` at 0.4 or above | Acknowledge, pause, offer a helpline (Lifeline; Beyond Blue), offer to continue or stop |

After a safety-net response Dr Sam does not resume the intake unless the person
chooses to. The event is logged as a flag on the session (class, timestamp) and
appears at the top of the clinician summary. The transcript excerpt is available to
the clinician, not on any dashboard.

Helplines are configuration (`AIDOC_HELPLINES`), defaulting to Australian services:
triple zero, Lifeline 13 11 14, Beyond Blue 1300 22 4636, 1800RESPECT 1800 737 732,
healthdirect 1800 022 222.

## Direct risk questioning

Dr Sam asks about self-harm and suicide directly, in both settings, with a
normalising preamble and a restated privacy statement. Routing to a human instead
is not the safer option: across 13 studies no increase in ideation followed being
asked, and not asking makes risk invisible rather than absent. A positive answer
enters the safety-net protocol above and is the first line of the handover.

## Written safety-netting

At the end of the interview Dr Sam gives the patient, in writing and read aloud,
per-symptom safety-netting drawn from clinician-authored templates keyed to the
symptom classes raised: that some uncertainty remains until the clinician has seen
them, the specific symptoms that should prompt them to seek help sooner, the
usual course, and how and where to seek care. The model selects and personalises
names and timings; it does not compose the clinical content. The delivered text is
stored with the conversation. This is decision D-31 and shares D-28's regulatory
question.

## Expression set

Expressions follow Dr Sam's own turn intent, not the person's label, so the avatar
never visibly "reacts to a classifier".

| Expression | When | Artist notes |
| --- | --- | --- |
| attentive | Default while the person speaks | Neutral mouth, soft eyes, slow blink |
| listening | Person is making a point | Small nod every 4 to 8 s, brows slightly raised |
| thoughtful | `wait`, before a careful question | Brief gaze up-left, mouth closed |
| warm | Greeting, `validate`, wrap-up | Smile reaching the eyes, head tilt |
| concerned | `reflect_feeling` on anxious, in_pain, low; safety net | Brows drawn in, slight forward lean, no smile |
| reassuring | `explain_why`, `decline`, normalising | Half smile, single nod at the sentence end |
| serious | Safety-net delivery | Still, direct gaze, no smile, no tilt |
| speaking | Any speech | Visemes on top of the base expression |

Idle: blink every 3 to 6 s with variance, breathing, micro head drift. Reduced
motion: blink only. Transitions blend over 300 to 500 ms.

## Turn contract

```json
{
  "say": "It sounds like the nights have been the hardest part. Is that fair?",
  "move": "reflect_feeling",
  "expression": "concerned",
  "prosody": { "rate": "-8%", "pitch": "0%", "pause_after_ms": 1800 },
  "detected_tone": { "label": "anxious", "confidence": 0.78 },
  "summary_delta": { "concerns": ["Fears it is the same as father's heart attack"] },
  "next": "wait_for_person",
  "flags": []
}
```

`next` is one of `wait_for_person`, `continue_speaking`, `read_back`, `end`,
`safety_net`. `summary_delta` accumulates into the clinician summary as the
conversation goes, so a dropped connection still leaves a usable summary.
`flags` carries `safety_net:<class>` or `off_topic`.

## Dual output: one interview, two artefacts, one attestation

**Output A, the verbal handover.** A narrative ordered by clinical salience, as a
good registrar would give it, spoken by Dr Sam to the clinician on request and
shown as text, with the structured data underneath. The clinician can ask Dr Sam
clarifying questions; answers quote the transcript and add nothing.

**Output B, the coding document.** Field-structured, provenance-labelled at field
level, and explicitly incomplete: the diagnosis block sits at the top and is
visibly empty, because only a clinician can fill it.

| Block | Content | Provenance |
| --- | --- | --- |
| Diagnosis block | Empty. Labelled slots for principal and additional diagnoses, with a prompt for the clinician to nominate which condition occasioned the episode | Clinician only |
| Reason for encounter | The presenting problem in the patient's words, plus Dr Sam's structured symptom set | Patient-reported |
| Symptom detail with qualifiers | Per symptom: onset, duration, course, severity, laterality, acute or chronic, first episode or recurrence, family-specific qualifiers | Patient-reported |
| Pre-existing conditions | One row per condition: who diagnosed it and when, current treatment, whether treatment changed, whether actively monitored | Patient-reported; clinician-confirmed on attestation |
| Onset relative to presentation | For every condition, whether present before arrival, stated as a fact of the history | Patient-reported |
| Medicines | Drug, dose, actual adherence, recent changes and why, the condition each is for | Patient-reported |
| External cause (injuries) | Mechanism, place of occurrence, activity, intent | Patient-reported |
| Behavioural risk factors | Smoking with quantity and currency, alcohol, other substances | Patient-reported |
| Social and functional | Accommodation, supports, mobility, carer status, occupation | Patient-reported |
| Obstetric status | Pregnancy, gestation, parity | Patient-reported |
| Safety-net events | Class and time of any trigger, and what was said | Structural |
| How the patient seemed | One sentence, only with tone consent, no labels | Derived |
| Gaps | What Dr Sam did not get to ask | Structural |
| Provenance and attestation | Statement that content is patient-reported and machine-transcribed; agent, prompt and rule-set versions; interview timestamp; clinician sign-off | Structural |

Rules for Output B: every clinical concept is bound to a SNOMED CT-AU concept, never
an ICD-10-AM code; each pre-existing condition row makes the three ACS 0002 tests
answerable at a glance; nothing is interpreted; the diagnosis block is never
pre-populated.

**Attestation** is an act, not a click. The clinician opens the document, edits
what is wrong, fills the diagnosis block or leaves it empty, and signs. Until then
the document is patient-reported and not a primary source. In the GP setting the
same act is the deliberate adoption of a document generated days earlier.

## Barge-in, accessibility, fallbacks

- The person may interrupt Dr Sam at any time. Playback stops within 300 ms of
  speech onset, the avatar returns to `attentive`, and the transcript records the
  cut-off point.
- Captions always. Avatar optional. Typing instead of speaking is always available,
  and tone classification then uses text only and says so in the record.
- Companion mode supports a larger caption size and a slower default rate.
- ED room privacy is a design requirement, not a nicety: headphones, a privacy
  screen, and a spoken statement of who will see the answers. An overheard
  conversation forfeits most of the disclosure advantage of talking to a machine.
- `prefers-reduced-motion` disables head movement and nods.
- If speech or the avatar fails, the conversation continues as text with browser
  synthesis and a static portrait.
