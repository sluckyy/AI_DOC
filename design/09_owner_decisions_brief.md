# 09 Owner decisions brief

**Product:** AI DOC, Dr Sam
**For:** the product owner and clinical lead
**Date:** 2026-09-23
**Status:** open. Every item below is a call only the owner (or a reviewer the
owner names) can make. Nothing here is a code decision, and nothing here blocks
the simulated-patient build: each item has a recommended default the software
runs on now, marked `pending` on the status page until the owner sets it.

Two lists follow. Part A is the nine configurable clinical parameters from the
Symptom Questioning Library, plus the childbearing range that the pregnancy gate
uses. Part B is the remaining owner-only calls from the Build Specification and
the decision record. For each: what it is, why the evidence does not settle it,
what the software does today, the options, and a recommendation.

How to set a Part A value: edit `content/parameters/sa_health_regional.yaml`,
change `status: pending` to `status: set`, put the value in, bump the file's
`version`, and call `POST /api/content/reload` (or restart). Every handover
records the parameters version it ran on, so a later change is auditable.

---

## Part A: the nine configurable clinical parameters

The library's principle: the agent collects the same features everywhere; the
urgency attached to them is local policy. None of these thresholds is embedded
in a question or a rule. Each module records the raw feature (age, sex where
recorded, exposure, duration) and the handover annotates it against the
parameter. Setting a parameter therefore changes the handover annotation and the
same-day routing note, never what the patient is asked.

### A1. Visible haematuria referral age

- **What it decides.** The age from which painless visible haematuria is
  annotated as meeting the local urological cancer referral criterion.
- **Why it varies.** NICE refers from 45, the American Urological Association
  investigates from 35, and Scotland sets no age threshold at all. The library
  is explicit that the differences reflect each system's cost-effectiveness
  threshold, not different evidence. The positive predictive value in men over
  60 is about 22%; under 45 it is about 1% in men and 0.2% in women.
- **Today.** Pending. The haematuria module records painless or painful,
  timing, clots, recurrence after antibiotics, smoking, and age verbatim. Every
  visible haematuria routes as a flag regardless.
- **Options.** 45 (NICE), 35 (AUA), or none (every painless visible
  haematuria annotated for referral).
- **Recommendation.** 45, with the module's "painless never closes the
  question" rule unchanged. If SA Health's local pathway is "any age", choose
  none: the cost is more annotations, not more questions.

### A2. Bowel symptom referral ages

- **What it decides.** The ages at which rectal bleeding, change in bowel
  habit and iron-deficiency anaemia are annotated against the local colorectal
  referral criteria.
- **Why it varies.** Jurisdictional referral criteria differ (NICE NG12 uses
  50 for rectal bleeding, 60 for change in habit or anaemia; Australian
  guidance tends to key on the combination of features and family history
  rather than age alone).
- **Today.** Pending. The bowel habit module records duration, blood, weight
  loss, family history and age verbatim; rectal bleeding with weight loss or
  with a change in habit routes same-day regardless of age.
- **Options.** NICE ages (50/60/60); the SA Health or Cancer Council
  Australia colorectal pathway ages; or none (combination-only routing).
- **Recommendation.** Adopt the local SA Health pathway ages if the network
  publishes them; otherwise NICE 50/60/60 as the interim, labelled as such in
  the handover.

### A3. Imaging rule for the anticoagulated head injury

- **What it decides.** Whether a head injury in a patient on anticoagulants is
  annotated "scan regardless" (NICE) or run through the Canadian CT Head Rule,
  which excludes anticoagulated patients from its derivation.
- **Why it varies.** The two rules disagree on scope, and the disagreement is
  about the evidence base's population, not about the patient in front of you.
- **Today.** Pending. The trauma and head injury module asks anticoagulant use
  by drug name and routes anticoagulated head injury same-day in every case.
- **Options.** `scan_all` (NICE) or `apply_rule` (Canadian).
- **Recommendation.** `scan_all`. It is the safer annotation and the one
  emergency departments in Australia generally apply. The agent never says
  "scan" to the patient either way.

### A4. Initial imaging for soft tissue lumps

- **What it decides.** Whether the handover note for a soft tissue lump that
  meets the size or growth criteria says "ultrasound first" (UK) or "MRI
  first" (European sarcoma guidance).
- **Why it varies.** Guideline preference and scanner access, not diagnostic
  accuracy evidence.
- **Today.** Pending. The lumps module records change over time, the
  patient's own size comparator (never converted), depth in their words, and
  routes growing or recurrent lumps same-day.
- **Options.** `ultrasound_first` or `mri_first`.
- **Recommendation.** `ultrasound_first`, matching regional access. This is a
  handover note only; the agent never names an investigation to the patient.

### A5. Age and sex thresholds for weight loss investigation

- **What it decides.** The ages, by sex, above which unexpected weight loss is
  annotated as crossing the 3% cancer-risk investigation threshold.
- **Why it varies.** The evidence is English primary care data, and the 2020
  BMJ paper was retracted and replaced by a 2024 update (risk above 3% in men
  from 50 and women from 60, with variation by accompanying features). There
  is no Australian replication.
- **Today.** Pending. The weight loss module establishes "unexpected" first,
  records amount and period in the patient's own words, and routes unintended
  loss with any associated feature same-day regardless of age.
- **Options.** 2024 update values (male 50, female 60); a single age for
  both; or none.
- **Recommendation.** Male 50, female 60, labelled "English data, 2024
  update" in the handover, and revisit if an Australian dataset appears.

### A6. Age threshold for fatigue as a cancer signal

- **What it decides.** The age, by sex, above which new-onset fatigue on its
  own is annotated as a cancer signal.
- **Why it varies.** Two English studies use different cut-offs: one finds
  12-month cancer risk above 3% in men from 65 and women from 80; a later
  analysis supports prioritising men from 70 and not women at any age on
  fatigue alone.
- **Today.** Pending. The fatigue module dates the onset, asks the red-flag
  features (each routes to its own module), and records age verbatim.
- **Options.** Male 65 / female 80; male 70 / female none.
- **Recommendation.** Male 65, female 80. It is the more inclusive of the
  two and the cost is an annotation.

### A7. AUDIT-C positivity threshold and the standard drink

- **What it decides.** The score at which AUDIT-C is annotated positive, by
  sex, and the standard drink the "how many drinks" items are counted in.
- **Why it varies.** Thresholds vary by sex and setting (commonly 4 for men
  and 3 for women; some services use 5 and 4). The Australian standard drink
  is 10 g of alcohol, which differs from the UK unit and the US drink the
  instrument was validated on.
- **Today.** Pending. The alcohol module administers the three AUDIT-C items
  in validated wording and records the answer options. It does not compute a
  score (see B1). The standard drink is set at 10 g for the wording of the
  quantity item.
- **Options.** Male 4 / female 3 (most common); male 5 / female 4; whether
  the patient is offered an Australian standard-drink description before the
  quantity item.
- **Recommendation.** Male 4 / female 3, and offer the standard-drink
  description once, before the first quantity item, in the same words every
  time.

### A8. Sepsis criteria set

- **What it decides.** Which criteria set the fever module's handover
  annotates against: NICE NG51 or a local SA Health set.
- **Why it varies.** The history items are the same in both (altered
  behaviour, urine output against time, immunosuppression, recent procedure,
  repeated presentation). The tiering rules and the wording of the urine
  output question differ.
- **Today.** Pending. The fever module asks urine output as a clock time and
  a count, collateral altered behaviour, immunosuppression by drug name, recent
  procedures and presentations, and treats mottling, blue lips and a
  non-blanching rash as delegated observations. It never assigns a risk
  category.
- **Options.** `nice_ng51` or `sa_health_local`.
- **Recommendation.** `nice_ng51` until SA Health confirms a local set; the
  history items do not change either way.

### A9. Public health notification pathway for bat exposure

- **What it decides.** Whom the handover names for notification when a patient
  reports any bat contact, at any time, in Australia or overseas.
- **Why it varies.** The library's source guidance is Queensland's. South
  Australia's pathway (the Communicable Disease Control Branch) needs to be
  confirmed, with its number and hours.
- **Today.** Pending. The wounds and bites module asks about contact, not
  bites, records exposure type, site, date, animal and country, and routes any
  bat contact same-day with a note that public health notification is needed.
- **Options.** The SA Health CDCB contact, or a network-internal infectious
  diseases contact who notifies.
- **Recommendation.** SA Health CDCB (1300 232 272 is the published number;
  confirm it) named in the alert template, so the receiving clinician does
  not have to look it up.

### A10. Childbearing range (used by the pregnancy gate)

- **What it decides.** The age range in which the pregnancy question is asked
  of anyone with a uterus recorded in the organ inventory.
- **Why it is the owner's.** It is policy about who is asked, not evidence,
  and it interacts with the wording of the gating question, which the O&G
  reviewer owns.
- **Today.** Pending. The early pregnancy and fetal movement modules do not
  gate on recorded gender or sex, by design.
- **Options.** 12 to 55; 10 to 60; ask everyone with a uterus regardless of
  age.
- **Recommendation.** 12 to 55, and let the O&G reviewer set the wording.

---

## Part B: the calls only the owner can make

### B1. Instrument scoring (D-41, F-22)

- **The call.** Whether Dr Sam may compute and report a score for any
  instrument, starting with AUDIT-C, the single-item drug and cannabis screens,
  and the Columbia Protocol.
- **Today.** Components only, no assembly. The handover reports the instrument
  name, each item's answer and the answer option; the clinician adds it up.
- **Why it is yours.** D-41 says an instrument may be scored only if it was
  validated in a mode equivalent to voice administration with no examination,
  witness or judgement items. AUDIT-C comes closest, and the library asks you
  to decide it explicitly. Scoring is also the step most likely to look like a
  clinical assessment to a regulator.
- **Recommendation.** Keep components-only for the TGA demo. Decide AUDIT-C
  scoring after the TGA conversation, because it is the one thing in the
  product that turns answers into a number.

### B2. Interpreter-mediated calls (N-14)

- **The call.** Whether an interview may proceed with a human interpreter on
  the line, and if so who the respondent of record is.
- **Today.** Not supported. The six languages run without an interpreter; a
  language outside the set ends the interview with a bail-out to a person.
- **Why it is yours.** Consent, attribution (whose words are verbatim) and the
  interpreter service contract are governance matters.
- **Options.** Not supported in v1; supported with the interpreter's words
  marked as interpreted; supported only for the disclosure and consent step.
- **Recommendation.** Not supported in v1. Add the language to the set
  instead, with validated translations.

### B3. Audio retention (N-26)

- **The call.** Whether the patient's audio is kept, for how long, and for
  what purpose.
- **Today.** No patient audio is stored. The transcript is stored; Dr Sam's
  synthesised speech may be cached for replay.
- **Why it is yours.** Privacy, research consent (N-27) and the HREC
  application depend on it.
- **Options.** None; 30 days for quality review; the study period for research
  with separate consent.
- **Recommendation.** None for the demo and the simulated bank. For the HREC
  study, the study period with separate consent, if the ASR-error research
  question needs it.

### B4. Availability target (N-19)

- **The call.** What availability the service commits to, and what "degrade to
  the human path" means at each site.
- **Today.** One to three container replicas in one region; a failed interview
  produces a partial handover marked partial, never one that reads complete.
- **Why it is yours.** It sets the infrastructure cost and the site's
  fallback staffing.
- **Options.** Best effort (demo and simulation); 99.5% business hours; 99.9%
  with a second region.
- **Recommendation.** Best effort now; 99.5% business hours for the pilot,
  since the human path exists at both sites.

### B5. Concurrency (N-35)

- **The call.** How many simultaneous interviews each site needs.
- **Today.** Scales to three replicas; no per-site cap.
- **Why it is yours.** It comes from the sites' call and arrival volumes.
- **Recommendation.** Ten concurrent per site for the pilot; revisit from
  telemetry.

### B6. Situational history recipients (D-47)

- **The call.** For each situational domain (transport, accommodation, carer
  availability, home care, services), who at the pilot site receives a positive
  answer. Domains without a named recipient stay out of v1.
- **Today.** Domains are asked only where a recipient is named; none is yet.
- **Recommendation.** Name the discharge planner and social work for the ED
  site and the practice nurse for the GP site, and start with transport and
  carer availability.

### B7. First aid and public health instruction

- **The call.** Whether Dr Sam may give any instruction beyond "call triple
  zero", for example pressure on a bleeding wound, or "do not loosen a cast".
- **Today.** None. The wounds module records what happened and routes; the
  limb pain module never mentions the cast. The library lists prohibited
  delegated observations and leaves this open for you.
- **Why it is yours.** Any instruction is the point where history-taking
  becomes advice, which is the boundary the intended-use wording relies on.
- **Recommendation.** None in v1. Raise it with the TGA as the one boundary
  case you have deliberately left out.

### B8. Verbatim risk disclosures in records reception may see (S-13)

- **The call.** Whether a patient's exact words about self-harm, violence or
  substance use appear in a record that non-clinical staff can open.
- **Today.** Verbatim goes to the clinician handover only; the export is
  clinician-gated. The mental health module is disabled.
- **Why it is yours.** Governance and the mental health specialist's advice on
  disclosure-to-contact intervals.
- **Recommendation.** Clinician-only, as built, and confirm it with the
  specialist when the mental health section returns.

### B9. Alert wording for the immediate tier (N-31, S-6)

- **The call.** Sign-off of the words the patient hears when the call
  transfers, and the words the duty GP and the triage nurse read.
- **Today.** Templated, marked "pending emergency medicine review" in the
  parameters register.
- **Recommendation.** Send the two patient messages and the alert template to
  the emergency medicine reviewer with the chest pain module, since that is
  the demo path.

### B10. Call-drop after an immediate trigger (S-14)

- **The call.** Whether Dr Sam places a call-back when the patient's call
  drops after an immediate-tier alert, and who is told if the call-back fails.
- **Today.** The alert stands, records lost contact and stays in the overdue
  feed until acknowledged. No call-back is placed.
- **Options.** No call-back (the practice or triage desk calls); one automated
  call-back after 60 seconds; call-back from the duty GP's own phone.
- **Recommendation.** No automated call-back in v1. The alert already reaches
  a human, and an automated call-back to a patient in trouble is a step the
  practice should own.

### B11. Overdue alert escalation target (S-4)

- **The call.** When an alert is not acknowledged within the timeout (120 s
  today), who is told next.
- **Today.** The alert appears in the overdue feed on the clinician page;
  nothing else happens.
- **Options.** Overdue feed only; a second recipient (charge nurse, practice
  manager) by SMS; the live transfer path.
- **Recommendation.** Overdue feed for the demo; a named second recipient per
  site for the pilot, chosen by the site.

### B12. The two reviewer gates you have already opened

- **Mental health.** With the specialist. The section is transcribed as a
  disabled placeholder (D-52) so they can read exactly what would run.
- **Emergency medicine and O&G.** The GP immediate-tier wording and the early
  pregnancy and fetal movement routing await their reviewers. Both modules run
  in simulation with `reviewed: false` and are visible as such on the status
  page; `REQUIRE_REVIEWED_CONTENT=true` will refuse to start until they are
  signed off.

---

## What you do not need to decide

- Which Azure voice Dr Sam uses (the audition script chooses; D-08).
- How the avatar is drawn (D-07, agreed).
- Anything about the model prompts, the controller or the handover format:
  those are code decisions traceable to the framework and the build
  specification.
