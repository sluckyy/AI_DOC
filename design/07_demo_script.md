# 07. Demo script for the TGA

Status: **Proposed**. Twenty minutes. The aim is to show the boundary as clearly
as the conversation: what Dr Sam captures, what it refuses to do, and where a
clinician's act is required. Run on fake providers so nothing depends on a key;
switch to Azure voices if the audition is done.

## Setup

- Backend and frontend running locally or in the dev container apps.
- Two browser tabs: the intake page and, later, the clinician page.
- Open `#/status` once to show the authoring checks passing and the provider
  names ("fake" or "azure").

## Scene 1: consent and disclosure (2 min)

Show the three separate consent switches. Start in the ED room setting, English.
Dr Sam's first words are the fixed disclosure: an AI, not a doctor; who sees the
answers; the same care either way. Point out it is a stored script, reviewable
like a leaflet.

After consent, three short questions from the dialogue pack: can you hear me,
would you rather another language (name Vietnamese and watch the interview
language switch), is anyone with you. Say what each one is for: a hearing
problem hands over to a person, the language offer is how the equity claim
starts, and "someone with you" is where a collateral history comes from.

## Scene 2: a settled chest pain history (8 min)

Speak or type, in this order, answering what Dr Sam asks:

1. "I've had this pain in my chest since this morning. It's like a pressure, and
   I felt a bit sick with it."
2. "It's settled now, it's gone. I was worried because my dad had heart problems."
3. To each "Is there something else…": "No, nothing else." Note three differently
   phrased invitations before Dr Sam summarises (P13, P5: never "anything else").
4. Confirm the summary. Then answer the chest pain questions: "About 7am", "It came
   on suddenly", "Like a pressure", "It went into both arms", "About twenty
   minutes", "No, breathing didn't change it", "No, moving made no difference",
   "I was walking up the stairs", "Yes I was sweating", "My breathing was fine",
   "Never had anything like that".
5. Ask "Is it serious?" at any point. Dr Sam deflects and never answers.
6. Final "something else", read-back, and the four-part safety-net close from the
   module's own closing block.

What to point out: Dr Sam did not ask about the pressure or the timing because
the patient already said them, and the record shows those slots stamped with the
opening turn (P12). Dr Sam asked about both arms explicitly, and about duration
precisely, because those are the discriminating items with likelihood ratios.

## Scene 3: the clinician side (5 min)

Open the handover. Show:

- The narrative, generated from slots: presenting complaint in the patient's
  words, findings, documented negatives each of which was asked, gaps stated
  ("No ECG and no troponin. Every negative is a history negative only").
- The structured record with class, value, verbatim, state and originating turn.
- "Ask Dr Sam": "What did they say about radiation?" answers from the slot;
  "Did they mention a rash?" answers "I didn't ask about that."
- The coding document: provenance on every block, SNOMED CT-AU concepts, no
  ICD-10-AM codes, and the diagnosis block empty with a clinician-only label.
- Attestation: a named clinician edits and signs; only then is there an exportable
  version.
- Export: the study record with the P1 to P14 transcript check reporting no
  violations.

## Scene 4: an immediate-tier alert and the live transfer (4 min)

Before the session, set `DEMO_TRANSFER_NUMBER` to the mobile of the GP in the
room and `TELEPHONY_PROVIDER=acs` (or leave the fake, which shows the number
and a call button instead of dialling). Neither is in the repository.

Start a new conversation, GP booking call setting. Say: "I've got a tight pain in
my chest right now, it's there at the moment." After the summary, the rule
`rf.chest_pain_current` fires from the narrative alone. Dr Sam stops, says it is
putting the patient through to the duty doctor and will pass on their own words,
and asks no further questions. The transfer panel appears; the GP's phone rings.
The alert row shows rule id, tier, route `live_transfer`, the patient's words and
the clock time. Everything after the alert is marked not asked in the handover.

Say out loud what the software does not do: if the duty GP's phone is
unanswered, the practice's own routing sends the call to reception. That is
the practice's workflow, not Dr Sam's logic, and the alert still stands in the
clinician view until someone acknowledges it (the unacknowledged feed is on the
clinician page).

Repeat in the ED setting to show the route change to the triage desk with no
change to the rule. Then show the same-day tier in the GP setting: the patient is
asked to come in for an urgent appointment today, and nothing is booked by the
agent.

## Scene 5: what is deliberately absent (2 min)

- No diagnosis anywhere: search the export for "angina" or "heart attack".
- No urgency score, no Wells or HEART assembled: components only.
- No tone label in the clinical record; if tone consent was on, one attributed
  sentence in the handover, nothing else.
- The mental health section is disabled at runtime until a specialist has
  reviewed it; the switch is visible in the status page.

## Questions the TGA is likely to ask, and the honest answers

- Is the red-flag alert clinical decision support? It is a deterministic rule
  over the patient's own answers that raises a flag to a human; it recommends no
  diagnosis and no disposition. Whether that sits inside the device boundary is
  the question we are asking (D-28).
- Does the coding document generate a codeable record? No. It is patient-reported
  and machine-transcribed until a clinician attests it, and the diagnosis block
  cannot be pre-filled by the software.
- What happens if the model is wrong? The model only proposes wording and slot
  values from the patient's words; every value carries its supporting turn, and
  a clinician can read the transcript. Nothing in the handover exists without a
  slot behind it.
