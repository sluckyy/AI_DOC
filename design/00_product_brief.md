# 00. Product brief

Status: **Proposed**

## One paragraph

AI DOC puts a calm, credible doctor in front of people who need to be heard before
they see a clinician, and puts a clean, structured account of that conversation in
front of the clinician. Dr Sam gathers the story, notices how the person is doing,
responds in the right tone, keeps them safe with a fixed safety net, and hands
over. Dr Sam does not diagnose and does not decide what level of care a person
needs; a human does that, with Dr Sam's summary in hand.

## Audiences (all confirmed in scope)

| Audience | What they get from Dr Sam | v1 |
| --- | --- | --- |
| Patients and the public | A patient, unhurried intake conversation before a consult; plain-language explanation of what happens next; safety-net advice | Yes |
| Clinicians | The intake summary in a structured handover; ability to ask Dr Sam questions about what the patient said; nothing that replaces their judgement | Yes (review only) |
| Aged care and companion settings | Scheduled check-ins with the same familiar face, carer visibility, escalation to a human when something changes | Phase 3 |
| Medical students and trainees | Dr Sam as a simulated patient or as a supervisor debriefing a history-taking exercise | Phase 4 |

## v1 scope and the regulatory boundary

The product owner asked for both **symptom triage and advice** and **staying outside
medical-device regulation** in Australia. Those conflict. Under the Therapeutic
Goods Administration's software rules, software that takes an individual's
symptoms and recommends a level of care, or suggests a diagnosis, is generally a
software-based medical device, whatever it is called in marketing. Software that
gathers information for a clinician to act on, or provides general health
information that is not personalised into a recommendation, generally is not.
This is a summary, not legal advice; a regulatory consultant should confirm the
boundary before launch (decision D-02).

v1 is therefore designed as:

1. **Pre-consult intake.** Dr Sam takes a history the way a good doctor would,
   asks about concerns and expectations, and produces a structured summary for the
   treating clinician. The clinician decides everything clinical.
2. **Fixed safety net.** A small, clinician-authored list of red-flag statements
   (chest pain, difficulty breathing, stroke signs, suicidal thoughts, and so on)
   triggers standard, non-personalised emergency guidance: call 000, or a named
   helpline. The guidance is identical for everyone who triggers it and is
   reviewed like any patient leaflet. It is not an assessment of the individual.
3. **Health information.** Explains terms and what to expect at the appointment,
   drawing on reviewed sources such as healthdirect, and always points back to
   the clinician for anything about the person's own situation.

**Individual triage and advice** (what Dr Sam thinks is wrong, how urgent it is, what
to take) is the v2 product, built on the same platform once a regulatory pathway
is chosen and a clinical evaluation plan exists. The architecture keeps a clean
seam so v2 does not require a rewrite.

## What "appropriate emotional tone" means here

Dr Sam detects how a person seems from what they say and how they say it, and
adjusts pace, wording and expression. Dr Sam does not tell the person what they
are feeling, does not store a mood profile without consent, and never uses the
inference for anything clinical. Where the tone is distress or crisis, the safety
net takes over.

## Non-goals for v1

- Diagnosis, differential diagnosis, urgency scoring, medication advice.
- Replacing a phone triage service or an emergency department.
- Prescribing, referrals, or writing into a clinical record system (the summary is
  exported as a document; integration with practice software is phase 3).
- Video or camera analysis of the person.
- Any use outside Australia until the jurisdiction question is revisited.

## Success measures for v1

- Clinicians rate the intake summary as accurate and useful (target: four of five).
- Patients report feeling listened to (single question after the conversation).
- Every scripted red-flag test transcript triggers the safety net, and no
  scripted benign transcript does.
- Median time from a patient's last word to Dr Sam speaking under two seconds.
