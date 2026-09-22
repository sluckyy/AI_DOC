# 06. Evaluation and ethics pathway

Status: **Proposed**; the pathway itself (simulated patients, then HREC for ED and
GP patients) was set by the clinical lead on 2026-09-22.

## Stage A: simulated patients

Purpose: prove that Dr Sam takes a usable history, documents it faithfully, keeps
its boundaries, and behaves safely, before any real patient is involved. No ethics
approval is needed when the "patients" are clinicians, actors or scripted personas
and no health information about a real person is collected.

Materials, owned by the clinical lead:

- A case bank drawn from the library's presentations, covering ED and GP: chest pain,
  abdominal pain, headache, breathlessness, mental-health presentations, paediatric
  via a parent, an older person with a carer present, low-literacy and
  English-as-a-second-language presentations, and at least five that contain a
  red flag and five that look alarming but are benign.
- For each case: a script or persona brief for the simulated patient, the
  "ground truth" history a clinician would expect to be captured, and the expected
  safety-net outcome.
- A documentation rubric: completeness against the ground truth, fidelity (nothing
  invented, nothing interpreted), structure, and clinician time saved.
- A boundary checklist: any diagnosis, urgency, medication or reassurance-about-
  outcome language is a fail.
- A listening rubric for the simulated patient: felt heard, was not rushed, tone
  matched, could interrupt, understood the AI disclosure.

Runs: each case at least twice with different simulated patients; every prompt or
rule-set version re-runs the full bank. Results are stored as a table in
`evaluation/` in this repo, with the prompt and rule-set versions recorded.

The Stage A comparator is a real clinician history on the same simulated patient.
The GP booking call's honest comparator is the status quo, where none of this
information exists at booking, so non-inferiority against a doctor is the wrong
frame there. The protocol states which claim is made (see the product brief).

The planned agreement study is the spine of Stage A: agreement between the
Dr Sam-elicited history and a clinician-elicited history on the same simulated
patients, consultant-adjudicated, blinded by having actors or agents read both
scripts. The evidence review adds the endpoints below at little extra cost.

| Endpoint | Measure | Reference |
| --- | --- | --- |
| History agreement (primary) | Agreement between agent and clinician histories, consultant-adjudicated, blinded | Adjudicated history |
| Condition capture | Per-condition sensitivity and positive predictive value of the structured condition list | Adjudicated history; comparable to the Australian computer-assisted coding benchmark of 54.1% sensitivity and 70.2% PPV, noting that was extraction from notes |
| Coder-facing sufficiency | Blinded dual coding with and without the attested document: DRG concordance, additional diagnosis counts, query rate, coder-rated sufficiency | Adjudicated clinical reference, never the routine coded record |
| Note quality | Modified PDQI-9 on the handover and the coding document, including freedom from hallucination | Instrument scores |
| Safety | Rate of history items present in the document but absent from the reference (fabricated or misattributed); red-flag sensitivity; time to escalation | Reference standard; scripted red-flag cases |
| Equity | Everything above stratified by interview language, age and health literacy | Stratified analysis |
| Monitored harm | NWAU or DRG complexity shift, reported and explicitly excluded from success criteria; a rise without a matching rise in agreement is a finding against the system | Declared in the protocol before data exists |
| Discordance direction | Adjudication records "agent right, clinician wrong" as a distinct outcome; two-directional disagreement is expected (Stockholm chest-pain study: 80% denied to the computer a radiation the EHR recorded, and 50% reported one the EHR denied) | Consultant adjudication with three outcomes, not an accuracy ranking |
| Consistency | Variance of agreement across time of day, patient order in a session and case, not only mean agreement | Powered for variance |
| Documentation loss | Agent-captured symptoms versus what reaches the clinical note, against the published 31 to 45% loss baseline | Note review |
| Handover format | Narrative-plus-structured versus structured-alone as a randomised arm, with clinician decision quality as the outcome | Two-arm comparison; unstudied in the literature |
| Voice accuracy | ASR word error on symptom vocabulary, accented English and each v1 language; disfluency and interruption handling | Sub-study before Stage B |
| Phrasing and stopping rules | Registered experiments: "something" versus "anything" and other phrasing variants; symptom-saturation stopping versus a fixed comprehensive schedule | Randomised in simulation (D-34) |
| Process adherence | P1 to P14 transcript tests over every conversation, reported as an audit, not as the outcome | The Framework Specification's table |
| Truthful pertinent negatives | Every documented negative traces to an asked question; compared with the 73% of documented ROS negatives never asked in practice | Weiner 2020 |
| ROS stratum | Symptoms elicited by the systems review analysed separately from the presenting complaint | D-37 |
| Family history | Scored as its own domain against a consultant-taken structured family history on the same simulated patient, not against what the treating doctor documented | Family history evidence base |
| Medication history | Discrepancies per patient against a pharmacist Best Possible Medication History with severity grading; comparators: doctor-taken history, self-administered form, dispensing record alone; time to a complete history | Medication evidence base; never powered on utilisation |
| Confabulation | Rate of slot values or narrative clauses with no transcript span; anticoagulant capture tested in both error directions | The prehospital stroke voice-agent prior art |
| Route yield | Per-route incremental yield for past medical history; free recall versus the named-condition sweep | PMH evidence base |
| Disclosure direction | Whether patients disclose more or less to the voice agent on stigmatised items (substances, sexual history, sphincter function, risk questions) than to a clinician | Library recurring principle 6 |
| Equity | Whether elicitation and handover narrow or widen documented under-triage of older patients and of minority patients in abdominal pain; stratified by interview language, age, health literacy | Library cross-cutting question |

Exit criteria for Stage A: zero narrative clauses or slot values without a transcript span across the bank; every
red-flag case triggers the safety net and every benign case does not; boundary
checklist clean (no diagnosis, urgency or medication language; diagnosis block
empty in every document); history agreement and condition capture at the
thresholds the clinical lead sets in the protocol; simulated patients rate "felt
heard" at four of five or better.

Stage A cannot start on the mental health section until its specialist review
is complete, and cannot start on the GP booking call's Immediate tier until
D-42 is settled.

## Stage B: HREC-approved study with ED and GP patients

Purpose: show the same properties with real patients and real clinicians, and
measure what the tool does to the consult.

What the HREC submission will need from this project, beyond the protocol the
clinical lead writes:

- A plain-language participant information and consent form covering: Dr Sam is
  an AI, what is recorded (audio transcribed then deleted, transcript retained for
  the study period), who sees the summary, the right to stop and to have data
  deleted, and that Dr Sam does not diagnose or advise.
- A data management plan: Australia East residency, encryption, access limited to
  named investigators, audit log of every view, retention and destruction dates,
  and the Notifiable Data Breaches procedure. `03_technical_architecture.md`
  section "Privacy, security and clinical governance" is the source.
- A safety plan: the fixed safety-net rule set and wording, who is notified when
  it triggers in the ED waiting room and in the GP setting, and the clinical
  escalation path. Stage A results as evidence.
- A clear statement of the regulatory position (transcription and structuring,
  not a medical device), with the TGA's answer on the ED red-flag escalation and
  the coding document attached (D-28).
- The governance baseline from the Safer Care Victoria ambient-scribe advisory,
  adopted as written: explicit consent with a genuine opt-out and equivalent care
  either way; data stored and processed in Australia; no vendor resale and no
  third-party model training on the content; retention schedules that cover the
  AI-generated artefacts as well as the final record; the clinician responsible
  for everything they sign.
- Study measures: documentation fidelity judged by the treating clinician, time
  to complete the history, clinician-rated usefulness, patient-rated experience,
  safety-net events and false alarms, and technical reliability.
- A stopping rule: any invented clinical fact in a summary, or any missed red
  flag in the study, pauses recruitment for review.

Settings: an ED waiting room on a tablet with a privacy screen and headphones,
and a GP practice via a pre-appointment link on the patient's own phone. Both
need a clinician-facing review screen that shows the summary before the consult.

## What the software must provide for both stages

- Versioned prompts and safety-net rules recorded on every turn.
- Export of a whole conversation (transcript, turns, summary, flags, versions) as
  a single file for the study record.
- A "simulation" flag on conversations so Stage A data is never mixed with study
  data.
- A per-conversation kill switch for the investigator.
