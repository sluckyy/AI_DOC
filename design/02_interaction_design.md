# 02. Interaction design

Status: **Proposed**

## Modes

| Mode | Who | Purpose | v1 |
| --- | --- | --- | --- |
| Intake | Patient, before a consult, in ED or via a GP pre-appointment link | Take the story, capture classification-relevant specificity, produce the verbal handover and the coding document | Yes |
| Clinician review and attestation | Clinician, after intake | Hear or read the handover; ask Dr Sam "what did they say about X"; edit and sign the coding document | Yes |
| Check-in | Older person or companion setting, recurring | Short scheduled conversation; note changes since last time; alert a carer when something changes | Phase 3 |
| Teaching | Student | Dr Sam plays a simulated patient from a case, or debriefs the student's history-taking | Phase 4 |

All modes share the persona, the safety net, the tone pipeline and the avatar.
Only the prompt profile, the register and the output document change.

## Intake conversation shape

Dr Sam follows a history-taking structure a clinician will recognise, but drives it
by listening rather than by form fields. The order is a guide; Dr Sam follows the
person's story and fills gaps later. Each stage names the classification-relevant
detail Dr Sam is expected to elicit, drawn from the evidence review; the wording
is conversational, the capture is structured.

1. Disclosure and consent (fixed script, spoken and shown, with a genuine opt-out
   and the assurance that care is the same either way).
2. Open invitation: "What's brought you in?" then silence.
3. The story in their words; Dr Sam reflects and clarifies.
4. Characterisation of each symptom: onset and duration, course, severity,
   laterality, what makes it better or worse, what they have tried, whether it is
   the first episode or a recurrence, and any qualifier the symptom family needs
   (for example, for injuries: mechanism, place, activity at the time, intent).
5. Concerns, ideas and expectations.
6. Pre-existing conditions, one at a time: the condition, who diagnosed it and
   when, current treatment, whether treatment has changed recently and why,
   whether it is being actively monitored, and whether it was present before
   today's problem started.
7. Medicines: drug, dose, what it is for, whether it is actually being taken,
   recent changes and why. Allergies.
8. Behavioural risk factors (smoking with quantity and currency, alcohol, other
   substances), social and functional context (accommodation, supports, mobility,
   carer, occupation), and obstetric status where relevant. Each introduced with
   `explain_why`.
9. Anything else: "Is there something you were hoping to bring up but haven't?"
10. Wrap-up: Dr Sam reads back a short summary, the person corrects it, and the
    handover and coding document are prepared for the clinician.

Elicitation rules that protect the record:

- Ask for specificity, never for a conclusion. "Has a doctor ever told you what
  that was?" is allowed; "Do you think it's your heart?" is not.
- Never lead toward complication-bearing content. Questions come from the
  person's story and the standard structure above, not from what would raise
  coded complexity.
- Record what the person said, attributed to them. A prior diagnosis is "patient
  reports being told by their GP in 2023 that...", never a bare label.
- Time budget: eight to twelve minutes in ED, up to fifteen for a GP pre-consult.
  Dr Sam never says "we're out of time".

## Active listening moves

| Move | What it is | Example |
| --- | --- | --- |
| attend | Silence and a listening expression while the person speaks | (avatar `listening`) |
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

Rules: one question per turn; `validate` before any redirect away from something
emotional; `wait` after any `reflect_feeling`; never two `reflect_feeling` in a row;
`explain_why` before any background question that could feel intrusive.

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
- `prefers-reduced-motion` disables head movement and nods.
- If speech or the avatar fails, the conversation continues as text with browser
  synthesis and a static portrait.
