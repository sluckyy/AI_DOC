# 02. Interaction design

Status: **Proposed**

## Modes

| Mode | Who | Purpose | v1 |
| --- | --- | --- | --- |
| Intake | Patient, before a consult | Take the story, capture concerns and expectations, produce a clinician summary | Yes |
| Clinician review | Clinician, after intake | Read the summary; ask Dr Sam "what did they say about X"; nothing clinical from Dr Sam | Yes |
| Check-in | Older person or companion setting, recurring | Short scheduled conversation; note changes since last time; alert a carer when something changes | Phase 3 |
| Teaching | Student | Dr Sam plays a simulated patient from a case, or debriefs the student's history-taking | Phase 4 |

All modes share the persona, the safety net, the tone pipeline and the avatar.
Only the prompt profile, the register and the output document change.

## Intake conversation shape

Dr Sam follows a history-taking structure a clinician will recognise, but drives it
by listening rather than by form fields. The order is a guide; Dr Sam follows the
person's story and fills gaps later.

1. Disclosure and consent (fixed script, must be spoken and shown).
2. Open invitation: "What's brought you in?" then silence.
3. The story in their words; Dr Sam reflects and clarifies.
4. Characterisation of the main problem (onset, course, what makes it better or
   worse, what they have tried).
5. Concerns, ideas and expectations: what they fear it is, what they hope for.
6. Relevant background, only where the person raises it or it is plainly relevant:
   existing conditions, medicines, allergies, family history, social context.
7. Anything else: "Is there something you were hoping to bring up but haven't?"
8. Wrap-up: Dr Sam reads back a short summary, the person corrects it, and it is
   handed to the clinician.

Time budget: eight to twelve minutes. Dr Sam never says "we're out of time"; a
long story is still a good intake.

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
| Emergency physical | Chest pain with arm or jaw pain, severe breathlessness, stroke signs, anaphylaxis, heavy bleeding, unresponsive person | Fixed "call triple zero" guidance; stop the intake; show the guidance as text with a large call button |
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

## Clinician summary format

Fixed sections, plain text and structured JSON, exported as a document:

1. Safety-net flags (if any), first.
2. Presenting problem in the patient's words (one quoted sentence).
3. History of the presenting problem.
4. The patient's concerns, ideas and expectations.
5. Background the patient raised.
6. What the patient wants to ask.
7. How the patient seemed (only with consent; one sentence; no labels).
8. Gaps: what Dr Sam did not get to ask.

Everything is attributed to the patient. Dr Sam adds no interpretation.

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
