# Reference: AI History-Taking Agent — Symptom Questioning Library

Source: the product owner's Claude Doc, https://claude.ai/artifact/B2kqavBzi9zU4EdwHGvKUX (as of 2026-09-23), linked from the Framework Specification. Plain-text extract of both pages; tables, YAML and diagrams flattened. The live doc is the source of truth and is the content layer of the agent.

---


AI History-Taking Agent — Symptom Questioning Library
 · 
Purpose and how to use this library
This is the symptom-by-symptom questioning backbone for the AI history-taking agent. The agent's conversational logic is built from the bottom up: rather than specifying an abstract state machine and hoping it survives contact with real presentations, we enumerate the presentations first and let the common structure emerge from them.
Each symptom entry carries four things:

Trigger — the patient phrasings, lay terms included, that route the agent into this entry.

Core question set — what must be asked for the history to count as complete for this symptom. Grounded in a validated or widely taught framework where one exists, rather than invented.

Conditional branches — follow-ups that open only when a particular answer is given.

Red flags — answers that trigger the interrupt and escalation described below.
This draft populates the presentation inventory and trigger lists. The core question sets are a second pass, to be grounded in a literature search on evidence-based history-taking frameworks per domain — SOCRATES for pain as the starting point, with validated equivalents sought for the other domains.
Status for reviewers
This document is circulated for clinical review. It is not complete and is not intended to look complete. The table below states exactly how far each presentation has been taken, so reviewers can direct effort at what is weakest rather than re-reading what is settled.
Grounded means a literature search was done and the questioning approach reflects it. First draft means the row was written from general clinical knowledge and has not been checked against evidence — treat these as hypotheses, not recommendations. The dizziness row is the cautionary example: its first draft encoded an approach the evidence has since discredited.

 | 
Presentation | 
Status | 
What review is most needed on
 | 
Symptom characterisation field set | 
Grounded | 
Whether the eleven empirical domains are the right default, and where radiation should remain
 | 
Chest pain | 
Grounded | 
Whether duration prompting is specific enough to capture the seconds/hours/days distinction
 | 
Headache | 
Grounded | 
Whether all fourteen history items of SNNOOP10 are askable without the interview becoming unwieldy
 | 
Dizziness | 
Grounded | 
Whether timing-and-triggers can be elicited reliably by voice without examination
 | 
Back pain | 
Grounded | 
The handover wording, given negatives carry no reassurance
 | 
Abdominal pain | 
Grounded | 
The under-triage mitigation for older patients; whether the bias finding should become a study outcome
 | 
Breathlessness | 
Grounded | 
Concrete phrasings for orthopnoea and PND
 | 
Syncope | 
Grounded | 
Whether patients can estimate prodrome duration reliably enough for the 2.5 min vs 3 sec distinction to survive
 | 
Unwell child | 
Grounded | 
Paediatric escalation thresholds; whether carer concern should itself trigger escalation
 | 
GI bleeding | 
Grounded | 
Melaena phrasing; confirmation that partial GBS fields should not be scored
 | 
Reduced fetal movements | 
Grounded | 
The GP-version escalation route, which needs obstetric input
 | 
Mental health | 
Grounded, needs specialist review | 
Everything: question wording, thresholds, escalation wording, the disclosure-to-contact interval
 | 
Testicular torsion | 
Grounded | 
Whether clock-time capture and confirmation works by voice; that long duration never de-escalates
 | 
Palpitations | 
Grounded | 
Whether symptoms occurring during the call should change GP-version appointment urgency
 | 
Leg swelling | 
Grounded | 
Confirmation that Wells components are listed but never assembled
 | 
Haemoptysis | 
Grounded | 
Which household volume comparators to offer, and confirmation that low volume never reassures
 | 
Cough and wheeze | 
Grounded, weaker evidence base | 
Whether the no-diagnosis-naming rule is enforceable; the paediatric choking question wording
 | 
Weakness, sensation, speech, visual (stroke cluster) | 
Grounded | 
The collateral-history branch for dysphasia; GP-version handling of immediate escalation
 | 
Seizure | 
Grounded | 
Whether refusing to assemble a purely historical instrument is the right call here
 | 
Vaginal bleeding / early pregnancy | 
Grounded | 
Obstetric and gynaecological review; wording of the pregnancy gating question; same-day-in-person pathway for the GP version
 | 
Haematuria | 
Grounded | 
Which SA Health referral thresholds to configure; urology review
 | 
Dysphagia | 
Grounded | 
Confirmation of the uncited saliva-obstruction immediate-tier item
 | 
Bowel habit / rectal bleeding | 
Grounded | 
Whether repeated low-risk presentations should raise priority; setting-specific weighting
 | 
Urinary symptoms | 
Grounded | 
Whether the agent should ever flag the history-only rule-in combination; downstream pathway governance
 | 
Vomiting | 
Grounded (paediatric); adult half thin | 
Paediatric surgical review of the colour rules; whether an SMS colour reference is feasible
 | 
Confusion | 
Grounded | 
The structured collateral interview; confirmation the agent never records \\\"confused\\\" as a finding
 | 
Rash | 
Grounded | 
Glass-test instruction wording; the lighter-skin-area prompts
 | 
Neck pain after trauma | 
Grounded; non-traumatic neck pain is a gap | 
Emergency medicine review of the GP-version instruction for high-risk callers
 | 
Falls | 
Grounded | 
Geriatric review; whether the agent should run the full World Falls Guidelines question set in the GP version
 | 
Trauma / head injury | 
Grounded | 
Which rule SA Health adopts for anticoagulated head injury; evaluation of anticoagulant capture in both error directions
 | 
Joint pain / swelling | 
Grounded | 
Wording and placement of the sexual history question
 | 
Limb pain | 
Grounded (time-critical causes only) | 
Whether the agent may ever mention loosening a cast; ordinary MSK and claudication not yet covered
 | 
Wounds and bites | 
Grounded (bat and rabies exposure); human bites a gap | 
SA public health notification pathway; whether the agent may give first-aid or keep-the-bat advice
 | 
Lumps | 
Grounded (soft tissue); breast, testicular, nodal lumps not yet covered | 
Imaging pathway to configure; growth-question wording
 | 
Weight loss | 
Grounded | 
Thresholds from the Australian replication; check no retracted figures are quoted
 | 
Alcohol and substance use | 
Grounded | 
Whether the agent may score self-administered instruments; Australian standard drink; addiction medicine review
 | 
Fever / sepsis (adult) | 
Grounded | 
Urine-output question wording; whether SA Health uses NICE or local sepsis criteria
 | 
Fatigue | 
Grounded | 
Age threshold to configure, given two studies with different cut-offs
 | 
Feeling generally unwell | 
Grounded — no instrument, by evidence | 
Whether SA Health has a non-specific-symptom pathway to feed
 | 
Visual disturbance — monocular branch | 
Grounded | 
Ophthalmology and rheumatology review of the GCA thresholds; the uncited cover-each-eye proposal
 | 
Alcohol withdrawal | 
Grounded, setting mismatch | 
Whether a community-validated alternative to PAWSS exists
 | 
Clenched-fist injuries and human bites | 
Grounded | 
Wording of the neutral mechanism question; what the agent says if asked about confidentiality
 | 
Neck pain without significant trauma | 
Partly grounded — no validated tool exists | 
Neurology review of the proposed same-day threshold; cord and infection red flags
 | 
Breast, testicular and nodal lumps | 
Grounded; male breast symptoms a gap | 
Whether isolated breast pain should be handed over as lower priority
 | 
Claudication and ordinary limb pain | 
Claudication grounded; rest pain and ordinary MSK pain by design choice | 
Vascular review of rest pain; the mode-of-administration finding
Cross-cutting questions for reviewers

Is the handover asymmetry rule workable in practice? Negatives mean different things per presentation, so the agent cannot use one reporting convention. Does this survive contact with how clinicians actually read handovers?

Should the comparative study measure equity rather than agreement? The documented under-triage of older patients and of Black and Hispanic patients in abdominal pain assessment suggests the more valuable question is whether the agent narrows or widens those gaps.

Where can the agent not see? Rash blanching, papilledema, fetal heartbeat, anal tone. Each is a place where a history that looks complete is structurally incomplete, and the handover wording has to carry that.

What is the right escalation threshold for the GP booking call? It differs from ED because the patient is at home and the interval to human contact is longer.

Which presentations should the agent refuse to take at all? Currently intoxication, significant cognitive impairment and acute distress. Is that list right, and who decides at runtime?
Suggested reviewer allocation
No single reviewer can check this document. Rows are grouped below by the expertise they most need; several rows appear under more than one heading.

 | 
Reviewer | 
Rows and decisions
 | 
Mental health (specialist) | 
Mental health section in full — wording, thresholds, escalation, disclosure-to-contact interval
 | 
Obstetrics and gynaecology | 
Reduced fetal movements; vaginal bleeding and early pregnancy; wording of the pregnancy gating question
 | 
Emergency medicine | 
Stroke cluster; neck pain after trauma; trauma and head injury; limb pain; the GP-version immediate-tier instructions throughout
 | 
Paediatrics, including paediatric surgery | 
Unwell child; vomiting and the colour rules; paediatric choking in cough
 | 
Geriatrics | 
Falls; confusion and the collateral interview
 | 
General practice | 
Chest pain, headache, back pain, fatigue, weight loss, generally unwell; feasibility of every GP-version routing decision
 | 
Urology and gastroenterology | 
Haematuria; dysphagia; bowel habit; GI bleeding
 | 
Public health and infectious diseases | 
Bat and animal exposure; SA notification pathway; fever and sepsis
 | 
Addiction medicine | 
Alcohol and substance use; withdrawal risk (currently a gap)
 | 
Governance / deployment owner | 
The configurable-parameters register; the proposed refinement of the assembly rule; whether the agent may give any first-aid or public-health instruction
Reviewers should know the error history. Two first-draft rows — dizziness and confusion — were found clinically wrong during the grounding pass and rewritten, and one citation was found to point to a mistyped URL and corrected. First drafts in this project were wrong often enough that nothing here should be assumed right because it reads plausibly. Rows marked as resting on thinner evidence (cough and wheeze; adult vomiting) and items marked as uncited (saliva obstruction in dysphagia) deserve particular scrutiny.
Known gaps after the gap pass. The seven gaps listed at consolidation have each been worked through. What remains ungrounded is narrower: rest pain and non-healing foot wounds; cord compression, infection and malignancy red flags in non-traumatic neck pain; breast symptoms in men; painful red eye; and a proposed cover-each-eye observation for visual loss. Each is marked in its row. Ordinary musculoskeletal limb pain is handled deliberately by the field set and symptom saturation, since no anchoring instrument was found.
Cross-cutting questioning rules
These govern every symptom entry and override the entry's own sequence.
The symptom characterisation field set
The agent uses a domain list, not a mnemonic. Mnemonics are memory aids for humans under time pressure; an agent has no memory constraint and needs the correct field set instead.
A [qualitative content analysis of core clinical texts] derived the domains of the history of presenting illness empirically and compared them against SOCRATES. In decreasing order of representation across the texts: associated symptoms, site or location, functional aspects, character or nature, onset, timing, triggers, severity, exacerbating factors, ameliorating factors, and progression of symptom.
Measured against that set, SOCRATES carried one unwarranted domain — radiation, not represented across the dataset — and was missing three: triggers, functional implications, and progression. The authors proposed a replacement mnemonic as better suited to general history-taking than SOCRATES.
Two consequences for this build:

Use the eleven domains as the default field set, with radiation retained as a conditional branch for the presentations where it carries diagnostic weight (chest pain, back pain, loin pain) rather than as a universal field.

Do not let one framework become the default for every symptom. SOCRATES was designed for pain specifically, and the same analysis notes it gets used as a default history-taking tool by inexperienced clinicians. An agent with one framework and many presentations fails the same way — applying a pain structure to breathlessness because it is the structure it has. Per-symptom field sets are specified in the tables below for this reason.
Progression and functional implications deserve particular attention: they are domains the empirical set contains and the most-taught mnemonic omits, and functional baseline is separately the field clinicians most often find missing from a handover.
Negatives do not mean the same thing across presentations
The literature pass surfaced a pattern that governs how the handover is worded, not just what is asked. Each framework has its own asymmetry between what a positive answer means and what a negative one means, and they do not point the same way.

 | 
Presentation | 
A positive answer | 
A negative answer | 
Handover convention
 | 
Headache (SNNOOP10) | 
Raises concern | 
Genuinely reassuring — 100% sensitivity across the list | 
A complete negative screen may be reported as reassuring
 | 
Back pain | 
Justifies workup | 
Uninformative — does not lower the likelihood of serious pathology | 
Never report a negative screen as reassurance
 | 
Breathlessness (orthopnoea, PND) | 
Weak — 13% PPV in the community | 
Informative — 97% NPV | 
Report documented negatives explicitly; do not over-read positives
 | 
Chest pain | 
Radiation to both arms raises; duration extremes lower sharply | 
Informative in both directions via duration | 
Report the specific feature and its direction, not a summary
 | 
Haemoptysis | 
Risk features and larger volume raise concern | 
Uninformative — small volume and light smoking history do not lower risk | 
Never report low volume as reassurance; record the patient's own comparator
 | 
Paediatric cough (foreign body) | 
Weak — specificity 7–24% | 
Informative — sensitivity 90–98% | 
Report an explicit negative choking history; do not over-read a positive
 | 
Palpitations | 
Modest — LRs 2.0 to 2.7 | 
Modest and dangerous to lean on — anxiety history does not exclude an organic cause | 
Report features individually; never summarise as likely anxiety
 | 
Testicular torsion | 
Raises urgency | 
Does not lower it — and neither does a long elapsed interval | 
Report clock time of onset with the computed interval, never duration alone
 | 
Leg swelling (Wells) | 
Collectable by the agent | 
Systematically incomplete — the only score-lowering item is clinician judgement | 
List components; state explicitly that no score has been assembled
 | 
Cough and wheeze | 
Not diagnostic — symptoms alone must not support a diagnosis | 
Not diagnostic either | 
Report the pattern; never name an obstructive diagnosis in either direction
 | 
Stroke cluster | 
Escalate on suspicion | 
Does not lower urgency — resolved symptoms still count | 
Report last known well and symptom onset as separate clock times
 | 
Seizure (tongue bite) | 
Strong — lateral bite LR near 49 | 
Uninformative — negative LR around 0.85 | 
Record bite location verbatim; treat absence as no information
 | 
Early pregnancy / ectopic | 
Risk factors and shoulder-tip pain raise concern | 
Uninformative — no bleeding, no risk factors, passed tissue and negative home test all fail to exclude | 
Never imply completed miscarriage or excluded ectopic
 | 
Dysphagia | 
Weak — PPV about 12% | 
Informative — NPV about 98%, but history cannot finish the job | 
Report duration as a number; short duration is the danger sign
 | 
Urinary (uncomplicated UTI) | 
Rule-in combination LR 24.6 | 
Vaginal discharge and irritation are the strongest items and point away | 
Report the combination as present or absent with components and exclusions; never \\\"likely UTI\\\"
 | 
Falls (older adults) | 
High-risk criteria are specific | 
Uninformative — sensitivity 26–52% | 
Never report \\\"no previous falls\\\" as low risk
 | 
Joint pain (septic joint) | 
Three features with LR above 3 | 
Uninformative — negative LRs 0.64–0.93; fever absent in 43% | 
Never let \\\"no fever\\\" read as evidence against infection
 | 
Lumps (soft tissue) | 
Growth is the best single indicator | 
Painlessness is the typical sarcoma history, not reassurance | 
Report growth against dates; never record painless as reassuring
 | 
Bat or animal exposure | 
Any contact is actionable | 
No visible wound does not exclude exposure | 
Record contact, not only bites; elapsed time never de-escalates
The consequence is that the agent cannot carry one reporting convention across all presentations. \\\"No red flags\\\" is a safe phrase after a headache screen, a misleading one after a back pain screen, and an incomplete one after a breathlessness screen where the absence itself was the finding.
The practical rule: the handover reports what was asked and what was answered, and the convention for interpreting negatives is specified per presentation. Any summary phrase that flattens this — \\\"systems review unremarkable\\\", \\\"no red flags elicited\\\" — is prohibited unless the per-presentation entry authorises it.
This also sets an expectation for the remaining domains. Each needs its own asymmetry established from the evidence rather than assumed, and the default assumption where evidence is absent is the back pain case: a negative means only that the question was asked.
Delegated observations
Some findings are not history and not examination, but something in between: the agent asks the patient or carer to look at something, press something, or perform a manoeuvre, and report back. This started as a single note in the rash row and is now load-bearing across several presentations, so it belongs here.
Current delegated observations across this document:

 | 
Presentation | 
Observation | 
Who performs it
 | 
Rash | 
Glass or tumbler test; checking lighter-skinned areas | 
Patient or carer
 | 
Palpitations | 
Visible neck pulsations; tapping out the rhythm | 
Patient
 | 
Leg swelling | 
Pitting oedema; whether the whole leg is swollen | 
Patient
 | 
Unwell child | 
Features present since onset of fever | 
Carer
 | 
Vaginal bleeding | 
Home pregnancy test result | 
Patient
 | 
Vomiting (infant) | 
Colour of vomit; bulging fontanelle | 
Carer
 | 
Trauma / head injury | 
Clear fluid from nose or ear; bruising around the eyes or behind the ear | 
Patient or carer
 | 
Fever / sepsis | 
Mottled or ashen skin; blue lips | 
Patient or carer
 | 
Limb pain | 
Coldness and pallor of the limb (late signs; negatives actively misleading) | 
Patient
 | 
Weight loss | 
Self-weighing | 
Patient
 | 
Lumps | 
Size estimate against a comparator | 
Patient
The rules are the same in every case:

A positive may be usable; a negative usually is not. The patient is untrained, the conditions are uncontrolled, and the sign may not yet have developed. The rash row is the worked example: a negative glass test is near-worthless because the rash appears late and may blanch early.

The handover records who observed, in the same line as the finding. \\\"Patient reports the rash did not blanch\\\" is a different clinical object from \\\"non-blanching rash\\\", and the two must never be collapsed. This is an instance of the no-answer-without-a-transcript-span rule, applied to observations rather than statements.

Instructions must be givable by voice and checkable. The agent should ask the patient to describe what they did, not only what they saw, so the clinician can judge whether the manoeuvre was performed at all.

Equity is checked at the point of instruction, not afterwards. Any delegated observation whose reliability varies by skin tone, body habitus, language, or dexterity needs its prompt written so it works for everyone — the rash row's requirement to check palms, soles, eyelids and mouth in every patient is the template.

A delegated observation never substitutes for the escalation it might have triggered. If the history already warrants escalation, the agent escalates without waiting for the patient to look.
Prohibited delegated observations. Some manoeuvres must never be delegated, because performing them by phone would execute a later step of a clinical algorithm without its earlier safety steps, or would put the patient at risk:

Neck rotation after trauma. In the Canadian C-spine rule, active rotation is the final step, performed only after a clinician has established a low-risk factor. Asking a patient to turn their head to see if it hurts skips the steps that make it safe.

Walking or standing tests in a patient who has fallen, including any attempt at gait speed or Timed Up and Go. These are physical tests for a clinician, and asking a recently fallen patient to walk on the call risks a second fall.

Any instruction to remove or loosen a cast or dressing in a patient with limb pain. Whether the agent may ever mention this is an open question in the limb pain row; until resolved, it is prohibited.
The unwell-child row sits slightly apart from the rest of the table: the carer is reporting a trajectory the examination cannot recover, rather than performing a manoeuvre. The attribution rule applies to it fully; the positive/negative asymmetry applies less cleanly, and a reviewer may want it separated.
Validated instruments: collect components, assemble nothing
Many presentations in this document have a validated clinical score, and many of those scores contain history items the agent can collect. The agent collects those items and reports them; it does not compute, report or imply a score. This began as a note in the GI bleeding row and has since been independently justified in several rows, each by a different mechanism:

 | 
Instrument | 
Row | 
Why the agent must not assemble it
 | 
Glasgow-Blatchford | 
GI bleeding | 
Half the components are laboratory and examination values; a partial score understates risk
 | 
Wells (DVT) | 
Leg swelling | 
The only score-lowering item is clinician judgement, so an agent score is biased upward
 | 
ROSIER | 
Stroke cluster | 
The only history items are the score-lowering mimic items, so an agent score is biased downward
 | 
Sheldon (seizure vs syncope) | 
Seizure | 
Pure history, but several items require a witness the agent is usually not speaking to
 | 
Canadian C-spine, Canadian CT Head | 
Neck, trauma | 
History items rule in; only examination can rule out
 | 
TWIST | 
Testicular torsion | 
Includes examination findings
 | 
Uncomplicated UTI combination | 
Urinary | 
Effectively diagnostic, but only inside a population whose boundaries need judgement
 | 
4AT | 
Confusion | 
Requires observed attention and alertness
 | 
Columbia Protocol | 
Mental health | 
Administered faithfully, but interpretation is reserved to a trained clinician
Three different structural biases, arrived at independently, point to the same rule. The handover lists the components found, states explicitly that no score has been assembled, and names the instrument so the clinician can complete it.
Proposed refinement, for explicit reviewer decision. The alcohol and substance screens (AUDIT-C, single-item drug and cannabis questions) are the first instruments in the document where none of the above reasons applies: they were validated for self-administration and contain no examination, witness or judgement items. The proposed wording of the rule is therefore: the agent may score an instrument only if it was validated for self-administration and contains no examination, witness or judgement items. Under that wording the substance screens qualify and nothing else in this document does. This should be adopted or rejected deliberately, not by drift.
Qualification added after the claudication row. The Edinburgh Claudication Questionnaire produced a [sevenfold higher rate of positive results when administered by an interviewer rather than self-completed]. An AI voice agent asking questions aloud is closer to an interviewer than to a form, so validation for self-administration does not establish validity when the agent asks. The proposed wording should therefore be tightened to: the agent may score an instrument only if it was validated in a mode equivalent to voice administration and contains no examination, witness or judgement items. On current evidence it is not clear that any instrument in this document meets that standard, including the substance screens. The single-item drug question was validated in interviewer-administered form, which makes it the strongest candidate — but reviewers should decide this deliberately, and the comparative study could test it directly.
Parameters SA Health must configure
Several rows depend on thresholds that differ between health systems for reasons of cost-effectiveness and policy rather than evidence. These are deployment parameters, not question-set content. The agent collects the same features everywhere; the urgency attached to them is set locally and should be configurable, versioned, and visible to reviewers.

 | 
Parameter | 
Row | 
Why it varies
 | 
Age threshold for visible haematuria referral | 
Haematuria | 
NICE 45, AUA 35, Scotland none
 | 
Age thresholds for bowel symptom referral | 
Bowel habit | 
Jurisdictional referral criteria
 | 
Imaging rule for anticoagulated head injury | 
Trauma | 
Canadian rule excludes these patients; NICE scans all
 | 
Initial imaging for soft tissue lumps | 
Lumps | 
UK ultrasound-first; European MRI-first
 | 
Age and sex thresholds for weight loss investigation | 
Weight loss | 
English data vs Australian replication
 | 
Age threshold for fatigue as a cancer signal | 
Fatigue | 
Two studies, two cut-offs
 | 
AUDIT-C positivity threshold | 
Alcohol | 
Varies by sex and setting
 | 
Sepsis criteria set | 
Fever | 
NICE vs local SA Health criteria
 | 
Public health notification pathway for bat exposure | 
Wounds and bites | 
Source guidance is Queensland
All predictive values in this document also come from particular settings, and referred populations overestimate risk relative to unselected primary care. Any future decision to weight findings differently in the GP and ED versions should be taken explicitly and should cite the setting each number came from.
Shared gating questions
Some questions are asked once and populate several rows. They should be asked early, stored once, and referenced by every row that depends on them, so the agent neither repeats them nor skips them because a different row was active.

 | 
Question | 
Rows that depend on it | 
Context slot
 | 
Could you be pregnant? | 
Vaginal bleeding, abdominal pain, syncope, dizziness, vomiting, urinary, trauma | 
ctx.pregnancy_status, itself gated by ctx.organ_inventory.uterus
 | 
Anticoagulants and antiplatelets, each by name | 
Stroke cluster, trauma, falls, haemoptysis, GI bleeding | 
ctx.medications.anticoagulant, ctx.medications.antiplatelet
 | 
Family history of early sudden death, recurrent syncope, or events described as seizures | 
Syncope, palpitations, seizure | 
ctx.family_history.sudden_death
 | 
Unexpected weight loss | 
Weight loss, dysphagia, bowel habit, haemoptysis, haematuria, fatigue, generally unwell | 
ctx.weight_change
 | 
Smoking, as pack-years with components | 
Haemoptysis, haematuria, weight loss | 
ctx.smoking.pack_years
 | 
Immunosuppression, by drug name including oral steroids | 
Joint, fever, urinary | 
ctx.medications.immunosuppressant
 | 
Atrial fibrillation | 
Palpitations, limb pain, stroke cluster | 
ctx.conditions.atrial_fibrillation
 | 
Any bat contact, or animal bite abroad, at any time | 
Wounds and bites — asked in the standard closing sections, since elapsed time never de-escalates | 
ctx.exposure.animal_bite
The pregnancy question in particular was added late, from the vaginal bleeding row, after the abdominal pain, syncope and dizziness rows had been written without it. Up to 30% of ectopic pregnancies present without vaginal bleeding, so those rows cannot rely on the patient raising it. Its wording needs review for patients who are not women, patients who may not know, and patients who may not want to answer in front of others in the room.
The family history question in the table above should also cover unexplained drowning and single-vehicle crashes, as the syncope row specifies.
Principles that recurred across rows
The grounding pass was done presentation by presentation, but several findings turned up independently in multiple rows. Each is stated once in its home row; they are collected here because their recurrence is itself the evidence that they are general.

The taught mnemonic is often the wrong instrument. Dizziness quality-typing was discredited and replaced by TiTrATE; SOCRATES carries one unwarranted domain and misses three; the five or six Ps for limb ischaemia and compartment syndrome are mostly late signs. In each case an agent working faithfully through the checklist would collect the wrong items, and in the limb case would produce systematic false reassurance. Mnemonics are memory aids for humans; the agent needs the evidence, not the aid.

Trajectory beats level. Pain rising despite analgesia (compartment syndrome), lump growth (sarcoma), short rather than long duration (dysphagia), features since fever onset (unwell child), prodrome duration in seconds versus minutes (syncope). Change over time, anchored to dates, is repeatedly the most informative thing a patient can report — and the thing a single consultation captures worst.

Capture absolute time, and never let elapsed time de-escalate. Clock-time capture with a confirmed interval is required in torsion, stroke, head injury, limb pain and sepsis. Separately, a long interval never reduces urgency: torsion at 20 hours is still an emergency, and bat exposure at any distance in time is still actionable.

The feature patients read as reassuring is often the dangerous one. Painless haematuria, painless lumps, short-duration dysphagia, small-volume haemoptysis, no fever with a hot joint, an anxiety explanation for palpitations, a straining explanation for rectal bleeding. The agent records the patient's explanation and the finding separately, and never lets the first stand in for the second.

Patient and carer judgement is sometimes measured data. Carer concern in the unwell child, self-diagnosis in recurrent UTI (LR 4.0). Where it is measured, it is recorded verbatim and attributed. Where it is not — adult \\\"something is wrong\\\" in the generally unwell row — it is recorded and flagged, not asserted.

Stigmatised questions are where the agent may differ most from a clinician, in either direction: sphincter and sexual function in back pain, vaginal symptoms in urinary, sexual history in joint pain, substance use, and direct suicide-risk questions. Whether patients disclose more or less to an AI voice is unknown and is a candidate secondary outcome for the comparative study.
Added after the gap pass. Principle 1 gained a fourth instance: in giant cell arteritis, asking whether the headache is at the temples — the question the disease's name invites — carries a likelihood ratio of 0.97, while jaw claudication carries 4.9. Principle 6 gained its first direct evidence: the Edinburgh Claudication Questionnaire returned a sevenfold higher positive rate when interviewer-administered rather than self-completed. That is not about stigma, but it shows that the mode of asking can change the answer by a large margin, which is the mechanism principle 6 was speculating about. It is the strongest argument in the document for measuring agent-versus-clinician disclosure directly rather than assuming either direction.
Open phase runs to symptom saturation. The agent opens with a broad invitation and keeps asking open questions until the patient stops producing new symptoms — saturation, not diagnostic sufficiency. The rule is two consecutive open prompts yielding no new symptom, then move on. The point is asking the same thing in different ways: \\\"anything else at all?\\\", \\\"is there anything that's been bothering you that you haven't mentioned?\\\" Log which phrasing pulls the extra symptom — that is a finding in its own right.
The agent decides the transition, not a turn budget. A fixed number of turns cuts off the patient who is still unspooling something important.
Red flags escalate at the moment they are heard, by tier. A red flag does not wait for the end of the interview. Immediate-tier triggers break the flow and escalate at once — in the ED version, as an alert to the triage desk carrying the patient's actual words, not a generic \\\"red flag detected\\\". Same-day and Flag triggers are recorded at the moment they are heard and shape the handover, but do not interrupt. The tiers are defined in the red flag master list.
The agent never reassures. No \\\"that sounds like it's probably nothing\\\". It flags, it hands over, it stays neutral. Patient questions of the form \\\"do you think this is serious?\\\" get a consistent graceful deflection.
No answer without a transcript span. When the clinician interrogates the handover, any answer not grounded in the transcript is \\\"I didn't ask\\\" — never a plausible reconstruction. This is the single biggest safety failure mode in the design.
Bail out when out of depth — but switch rather than stop where a row says so. Intoxication, deafness, or distress severe enough that the interview is not working: the agent recognises this and hands to a human rather than grinding on. Two exceptions govern this rule. Where the patient cannot give a reliable history because of confusion or speech disturbance, the agent switches to the structured collateral interview described in the confusion and stroke rows, rather than abandoning the history. And distress alone does not stop the mental health questions: the direct risk questions are asked as the mental health section specifies, and a positive answer escalates.
Consent and opt-out. The patient is told they are talking to an AI and can choose a human instead — particularly important in ED, where they are unwell and not placed to negotiate.
Language. Histories can be taken in the patient's own language, with the handover rendered in English for the clinician. The original-language transcript is preserved underneath, so translation never sits unexamined between the patient's words and the record.
The process layer
The process layer is the agent's conversational policy — how it talks, independent of what the patient presents with. It governs every consultation in this library and is versioned separately from the symptom modules below, because it is fixed and externally evidenced while the modules change with every reviewer pass.
Each rule is written as a behaviour the agent must exhibit, paired with the observable evidence that it happened in a transcript. That pairing is the point: the same table is the build specification and the rating rubric for the comparative study, so the rubric does not have to be invented separately once transcripts exist.

 | 
# | 
Agent behaviour | 
Transcript test | 
Grade and evidence
 | 
P1 | 
Narrow gradually from open to closed. Never jump from an open invitation to a slot checklist. | 
Question forms coded by turn index show monotonic narrowing. No closed question before the open phase closes. | 
A — Takemura 2007, F=40.1, p<0.0001, adjusted for interview length
 | 
P2 | 
Contribute no clinician-derived content in the opening. The patient leads entirely until they stop volunteering. | 
No agent turn in the open phase names a symptom, body system or timeframe the patient has not already named. | 
A — Donner-Banzhoff 2017: inductive foraging yielded 31% of diagnostic cues, against 24% for both closed strategies combined
 | 
P3 | 
Do not cap the opening statement. Budget two minutes. | 
No interrupting or redirecting turn before 120 s of patient speech, unless a red flag fires. | 
A — Langewitz 2002, n=335: mean spontaneous talking time 92 s, 78% finish inside two minutes
 | 
P4 | 
Use facilitators, not questions, during the open phase. | 
Agent turns in the open phase are continuers or silence, not interrogatives. | 
A — Takemura 2007, F=15.3, p<0.0001; Beckman and Frankel 1984
 | 
P5 | 
Ask “Is there something else?”. Never “anything else”. | 
Exact string check on every screening invitation. | 
A — Heritage 2007: OR 0.154, a 78% reduction in unmet concerns, p=0.001; “anything” non-significant
 | 
P6 | 
Summarise back before narrowing. | 
A summary turn exists at the open-to-closed transition, and the patient's reply to it is logged as elicited content, not as confirmation. | 
A — Takemura 2007, F=5.57, p=0.019
 | 
P7 | 
Never phrase a screening question toward the negative. | 
No question carries a negative frame — “no chest pain?”, “you're not still…?”, a trailing “are you?”. Checked at authoring time on every stored phrasing, and again in transcript. | 
A — leading toward non-use RR 0.22, closed 0.60, against open and normalising at 1.00
 | 
P8 | 
Precede every stigmatised slot with a normalising preamble, and state once who will see the answers. | 
Each stigmatised slot is immediately preceded by its preamble. A disclosure statement appears exactly once. | 
A — disclosure meta-analysis Ω 1.19 overall, 1.29 for sexual behaviour; individual administration Ω 1.61 against group 1.18
 | 
P9 | 
Ask risk questions directly, self-harm included, in both settings. Route-to-human is not the safer option. | 
Risk slots are asked and filled, never deferred to a handoff. | 
A — Dazzi 2014: 13 studies, no significant increase in ideation, several showed reduction
 | 
P10 | 
Tune red-flag screens for sensitivity and accept the alert burden. | 
Every alert traces to a named rule over filled slots, not to model judgement. No alert suppressed for low prior probability. | 
A — SNNOOP10 reaches 100% sensitivity for high-risk headache at AUC 0.66
 | 
P11 | 
Never stand down. The agent does not tell a patient they can wait. | 
No agent turn contains a de-escalating disposition statement. | 
A — LLM accuracy 10.8% on self-care advice, against 94.1% on identifying non-emergencies
 | 
P12 | 
Capture structured data at elicitation, never by parsing the transcript afterwards. | 
Every filled field carries the turn id it came from. | 
A — 31–45% of patient-reported symptoms never reach the note (Mayo, n=1,119); 52% of ED chest-pain records lacked pain location against near-complete computerised capture (Stockholm, n=410)
 | 
P13 | 
Run two saturation thresholds. Close the problem list when three differently-phrased invitations return nothing new. Keep soliciting elaboration on named symptoms for longer. | 
The transition log shows at least three distinct phrasings before the problem list closes, and records which phrasing pulled the last new symptom. | 
B — transferred from code and meaning saturation in qualitative method, not demonstrated in consultations
 | 
P14 | 
Close with per-symptom safety-netting: the uncertainty, the named red flags, the expected time course, where to seek care. | 
All four components present in the closing turn and in the written output. | 
B — BJGP review consensus components; that review's own finding is that empirical evaluation is absent
Grade A means the rule rests on a measured effect in the evidence review. Grade B means it is consensus, or transferred from another field — a candidate for study in its own right rather than an assumption to build on quietly.
This table is not the primary outcome. Process behaviour is the easiest thing to move and the least connected to benefit: the Four Habits trial shifted coded behaviour by 7.5 points with no change in patient satisfaction, and Cochrane found improvement on expert ratings but not on simulated-patient ratings. The table exists to make the agent's behaviour auditable and reproducible, not to score it.
How the layers meet at runtime
 B[Facilitators only]\\n  B --> C{New symptom named}\\n  C -- yes --> B\\n  C -- no, after 3 phrasings --> D[Summarise back]\\n  D --> E[Activate symptom modules]\\n  E --> F[Fill required slots]\\n  F --> G[Coverage sweep]\\n  G --> H[Red flag rules over slots]\\n  H -- fires --> I[Alert carrying verbatim]\\n  H -- none --> J[Safety-net close]\\n  I --> J\\n  J --> K[Handover plus structured data]]]>
Code owns the diamond and the two rule boxes — saturation counting, the coverage sweep and red-flag evaluation are deterministic over filled slots. The model owns the phrasing inside every other box.
Slot schema
Every symptom module in this library is written in one shape: a header, a list of slots, and a set of red-flag rules evaluated over those slots. Nothing in a module is prose the agent reads at runtime — the prose in this document is for reviewers, and the schema is what the agent is given.

 | 
Field | 
Holds | 
Why it is there
 | 
module, version, status | 
identifier, semantic version, grounded or first-draft | 
the study must record which library version produced each history; status is already tracked per row in the reviewer table above
 | 
activates_on | 
patient terms and referring modules that switch the module on | 
activation is retrieval, not prompting: only the active module's slots enter context
 | 
setting | 
ed, gp_booking, or both | 
escalation route and what the agent can observe differ by version
 | 
slots[].id | 
stable identifier | 
the handover, the alert and the study dataset all key on it, so it must survive rewording
 | 
slots[].class | 
coverage, discriminating, red_flag or context | 
decides what evidence the slot must carry and who evaluates it
 | 
slots[].intent | 
what is to be established, in one line | 
the unit of coverage; phrasings vary, intent does not
 | 
slots[].phrasings[] | 
several ways of asking, each with a form and an optional use_when | 
saturation requires re-asking differently, P7 is checked against form at authoring time, and logging which phrasing pulled the answer is a planned finding
 | 
slots[].value | 
type and option set | 
this is where structured capture happens, at elicitation (P12)
 | 
slots[].evidence | 
likelihood ratio, what it discriminates, citation, grade, derivation population — or an explicit gap | 
a discriminating slot has to justify itself; an unjustified one becomes visible rather than silent
 | 
slots[].verbatim | 
whether to store the patient's own words beside the coded value | 
alerts carry the patient's words, and so must any slot where the patient's explanation and the finding have to stay separate
 | 
slots[].negative_reporting | 
explicit or omit | 
negatives mean different things per presentation, so this is set per slot rather than by one handover convention
 | 
red_flags[] | 
fires_when over filled slots, action per setting, alert template, suppressible: false | 
deterministic and code-evaluated, never model judgement
 | 
closing | 
the four safety-net components for this presentation | 
P14
 | 
prohibited, gaps | 
what the agent cannot do or see here | 
the handover has to carry structural incompleteness — rash blanching, anal tone, fetal heart
A worked module
Chest pain, abbreviated to three slots. The likelihood ratios are the ones already tabulated in the cardiovascular section below.
\\n      cp.onset_character.onset == abrupt\\n      and cp.onset_character.quality in [tearing, ripping]\\n      and back in cp.radiation\\n    action: {ed: alert_triage, gp_booking: alert_gp_callback}\\n    alert:\\n      include_verbatim: true\\n      template: 'Possible aortic dissection. Patient said: {verbatim}. Onset {onset_clock_time}.'\\n    suppressible: false\\n\\nclosing:\\n  uncertainty: 'I cannot tell from talking with you whether this is coming from your heart.'\\n  watch_for: [pain returning at rest, pain with sweating or vomiting, pain with breathlessness]\\n  time_course: 'Someone will speak with you today.'\\n  where: 'If it comes back before then, call an ambulance rather than waiting.'\\n\\nprohibited: [judging pallor, sweating or distress by appearance]\\ngaps:\\n  - 'No ECG and no troponin. Every negative in this module is a history negative only.']]>
The four slot classes
Coverage slots exist for completeness. They carry no likelihood ratio and need none, because the recorded negative is the product.
Discriminating slots must carry a likelihood ratio, what it discriminates, a citation and a grade — or evidence: {gap: true} with one line saying why none exists. This is Summerton's argument made mechanical: an unjustified discriminating question is indistinguishable from a coverage question, and the library should not let that difference go unrecorded.
Red flag slots feed rules rather than judgement. The rule is a boolean over filled slots, evaluated by code after the coverage sweep, never suppressed for low prior probability, and the alert carries the patient's own words.
Context slots — age, medications, pregnancy status, anticoagulation — are shared across modules, filled once per consultation, and referenced by gating rules rather than re-asked. They are the schema home for the shared gating conditions set out above.
What the controller owns, and what the model owns
The controller decides which module is active and therefore which slots are in context; whether saturation has been reached, by the P13 count; the end-of-consultation sweep for unfilled required slots; red-flag evaluation and routing; and every structured field write, each stamped with the turn it came from.
Everything else is the model's: which phrasing to use, which cue to follow, when to elaborate, how to phrase the handover. The split matters for a practical reason as much as a governance one — hand the model the whole library and it interrogates checklist-style, and the history stops feeling like a registrar took it.
Authoring checks
Because colleagues will edit this library directly, these run over it at build time rather than being left to review:

Every stored phrasing passes the P7 polarity check.

Every discriminating slot carries a likelihood ratio and citation, or a declared gap.

Every red-flag rule references only slot ids that exist in its own module or in the context module.

Every stigmatised slot has a normalising preamble (P8).

Every module has all four closing components (P14).

No slot id is reused, and no id changes without a version bump.

Every likelihood ratio declares a derivation population. Any marked population: pooled on a presentation with known sex-based diagnostic disparity declares either a stratified value or an explicit gap.

No gating rule references ctx.gender or ctx.sex_recorded.
The context module
Context slots are the values that several symptom modules gate on. They are filled once per consultation, prefilled from the record wherever it holds them, referenced by id, and never re-asked inside a module.
The module exists because the shared gating questions already presuppose values the library never captures. “Could you be pregnant?” has no rule saying who is asked it. The AUDIT-C positivity threshold and the weight-loss investigation thresholds in the parameters table both vary by sex, against a field that does not exist anywhere in the schema.
Sex is three slots, not one

 | 
Slot | 
Holds | 
Used for
 | 
ctx.gender | 
how the patient describes themselves and wishes to be addressed | 
the conversation, and the opening line of the handover. Never referenced by a gating rule
 | 
ctx.sex_recorded | 
the sex held in the booking record or on the triage screen | 
matching the handover to the record, and audit
 | 
ctx.organ_inventory | 
uterus, ovaries, testes, prostate — each present, absent or unknown | 
every gating rule
Gating on gender or on recorded sex fails in both directions: an ectopic missed in a trans man, a torsion missed in a trans woman who has testes, and a record field that reliably reflects neither. A rule reading uterus == present says what it actually needs and degrades safely — unknown routes to asking rather than to assuming. The inventory defaults from ctx.sex_recorded, is overridable, and treats unknown as a real state rather than a missing value.
The slots
\\n      ctx.organ_inventory.uterus == present\\n      and ctx.age within param.childbearing_range\\n    phrasings:\\n      - {id: p1, form: open, text: 'Is there any chance you could be pregnant?'}\\n    value: {type: enum, options: [yes, no, unsure]}\\n    gates: [vaginal_bleeding, abdominal_pain, syncope, dizziness, vomiting, urinary, trauma]\\n\\n  - id: ctx.medications\\n    intent: current medicines, with anticoagulants, antiplatelets, immunosuppressants\\n            and oral steroids named individually\\n    prefill_from: [booking_record]\\n    confirm: true          # a wrong value here is dangerous\\n    gates: [stroke_cluster, trauma, falls, haemoptysis, gi_bleeding, joint, fever, urinary]]]>
The remaining gating values — smoking as pack-years, unexpected weight loss, atrial fibrillation, family history of early sudden death, animal and bat exposure — take the same shape and are mapped in the shared gating table below. param.childbearing_range belongs in the parameters table, since it is set by guideline rather than by evidence.
Asking, and not asking
Most context slots should never be asked. In the GP booking version the record holds age, recorded sex and usually the medication list; in ED they are on the triage screen. Cold-asking them is the fastest way to make the agent feel like a form, and it spends the two-minute opening budget (P3) on data the system already has. prefill_from with silent use is the default; confirm: true only where a wrong value is dangerous.
Where a slot must be asked, it arrives at the point of need with its reason attached — “because of where the pain is, I need to ask whether…” — rather than in an opening demographic block. Organ inventory in particular is asked only when a gating rule needs a field that is unknown, and P8's normalising preamble applies to it.
Sex as a modifier on the evidence
This is the part that reaches further than gating. Sex is the first context value that changes the evidence attached to a slot, not merely whether the slot is asked. The chest pain likelihood ratios in the worked module above are pooled, and largely derived from cohorts in which women are under-represented. Applying 2.6 for bilateral arm radiation to a woman inherits that imbalance silently.
So evidence carries the derivation population, and says so when it cannot stratify:

Most entries will declare a gap. That is the honest state of the symptom literature, and a library that says so is better than one that quietly applies a male-derived number. It also gives the comparative study something concrete to measure: whether the agent narrows or widens the documented sex-based gaps is already an open question for reviewers, and this field is where the answer would be traced.
Cardiovascular and respiratory

 | 
Presentation | 
Patient trigger phrasings | 
Framework to ground in | 
Red flags
 | 
Chest pain | 
chest pain, tightness, pressure, heaviness, \\\"like an elephant on my chest\\\", indigestion that won't shift | 
Symptom field set, not SOCRATES; duration asked precisely | 
Any current or recent-onset chest pain escalates; radiation (both arms is the informative pattern), sweating and duration are recorded, not used to gate. Sudden tearing pain to the back
 | 
Breathlessness | 
short of breath, puffed, can't catch my breath, winded, can't get air in | 
Onset speed, exertional threshold, orthopnoea, PND | 
Sudden onset; speaking in single words; breathlessness at rest; associated chest pain
 | 
Palpitations | 
heart racing, fluttering, pounding, skipping, thumping | 
Rate, regularity, onset/offset abruptness, triggers, duration | 
Associated syncope, chest pain, breathlessness; sustained fast rate
 | 
Cough | 
cough, chesty, hacking, bringing stuff up | 
Duration, productive vs dry, sputum character, diurnal pattern | 
Haemoptysis; duration over three weeks; associated weight loss, night sweats, fever
 | 
Haemoptysis | 
coughing up blood, blood in my phlegm, streaks of blood | 
Volume, frequency, first episode vs recurrent | 
Any volume — small volume does not reassure; cancer-risk features (age, pack-years); associated breathlessness or chest pain
 | 
Syncope / collapse | 
blacked out, fainted, passed out, went down, came over funny | 
Before/during/after structure; posture; prodrome; witness account | 
Exertional syncope; no prodrome; associated chest pain or palpitations; injury sustained
 | 
Leg swelling | 
swollen legs, ankles puffed up, one leg bigger | 
Unilateral vs bilateral, onset, pain, calf tenderness | 
Unilateral with pain — DVT; associated breathlessness or chest pain
 | 
Wheeze | 
wheezy, whistling, chest tight, asthma playing up | 
Trigger, diurnal variation, reliever use and response | 
Reliever not working; unable to complete sentences; previous ICU admission for asthma
Core question sets to be attached per row in the literature pass. SOCRATES is the obvious anchor for chest pain; the breathlessness and syncope rows need a validated structure identified rather than authored.
Chest pain: ask the features that carry likelihood ratios. The [Rational Clinical Examination systematic review] and the [chest pain history evidence synthesis] identify which history features actually move the probability of acute coronary syndrome. Most are history, not examination — so they are all askable by the agent.

 | 
History feature | 
Effect on ACS probability | 
LR
 | 
Prior abnormal stress test | 
Raises | 
3.1
 | 
Peripheral arterial disease | 
Raises | 
2.7
 | 
Pain radiating to both arms | 
Raises | 
2.6
 | 
Stabbing, pleuritic, positional, or reproducible by palpation | 
Lowers | 
0.2–0.3
 | 
Episodic pain lasting seconds | 
Lowers sharply | 
0.0
 | 
Pain lasting over 24 hours | 
Lowers sharply | 
0.1
Pain radiating to both arms separately [raised the probability of 30-day major adverse cardiac events], with the same short-duration and long-duration findings holding for that outcome.
Three build implications:

Duration must be asked precisely. \\\"How long does it last?\\\" is doing more diagnostic work than almost any other question in this document, and seconds versus minutes versus over a day are three different answers. A vague answer needs a follow-up, not a shrug.

Ask about both arms explicitly, not just \\\"does it go anywhere\\\" — the bilateral finding is the one with the specificity.

Past cardiac workup is a history question. Prior stress test result and known peripheral arterial disease are among the most specific findings available, and both sit in past medical history rather than the presenting complaint.
This also strengthens the handover case. [Patient-reported history is a key component of the HEART score, HEART Pathway and EDACS], and past diagnosis of coronary artery disease and abnormal stress test are among the most specific history findings for ACS — [more specific than ECG changes]. A complete, reliably elicited history is a direct input to the risk tool the clinician will use, not merely context for it.
Breathlessness: the classic questions are specific, not sensitive — and their value runs the other way. Orthopnoea and paroxysmal nocturnal dyspnoea are the questions every student is taught to ask, and the evidence supports asking them, but not for the reason usually assumed.

 | 
Feature | 
Value | 
Source
 | 
Either orthopnoea or PND, sensitivity | 
52% | 
[Prospective population studies]
 | 
Either orthopnoea or PND, specificity | 
83% | 
Same
 | 
Positive predictive value | 
13% | 
Same
 | 
Negative predictive value | 
97% | 
Same
 | 
PND, positive LR | 
2.6 | 
[ED dyspnoea review]
 | 
Orthopnoea, positive LR | 
2.2 | 
Same
 | 
Dyspnoea on exertion, positive LR | 
1.3 | 
Same
The pattern is the mirror image of back pain. Here a negative is informative and a positive is weak: the negative predictive value is 97%, while the positive predictive value in a community population is 13%. In primary care, [dyspnoea was the only symptom with high sensitivity at 89% but poor specificity at 51%, while orthopnoea and history of myocardial infarction both reached 89% specificity].
Build implications:

Ask orthopnoea and PND in concrete terms, not jargon. \\\"How many pillows do you sleep on, and has that changed?\\\" and \\\"do you ever wake up in the night fighting for breath?\\\" elicit better than the textbook phrasings. Record the concrete answer, not the label.

Record negatives explicitly. Given the 97% negative predictive value, a documented absence carries real information — but only if the question was genuinely asked. This is a presentation where the \\\"I didn't ask\\\" rule earns its keep.

Exertional threshold belongs in the handover as a functional statement. \\\"Could walk to the shops last week, now breathless crossing the room\\\" is more useful than a severity rating, and feeds the functional baseline field.

Ask about prior myocardial infarction — it carries the same 89% specificity as orthopnoea and sits in past history rather than the presenting complaint, so it is easy to miss under time pressure.
Syncope: the history carries almost the entire diagnostic load, and one field is a number. The ED priority is [distinguishing cardiac from non-cardiac syncope], and most of the discriminating information is historical.
The single most useful field is prodrome duration, because it is a quantity rather than an impression. Duration of symptoms preceding the episode [averages 2.5 minutes in vasovagal syncope and around 3 seconds in arrhythmia-related cardiac syncope]. The agent should push for a number — \\\"did you have any warning at all, and roughly how long?\\\" — and record the patient's estimate verbatim rather than converting it to \\\"brief prodrome\\\".

 | 
History field | 
Discriminating value
 | 
Prodrome duration | 
~2.5 min vasovagal vs ~3 sec cardiac arrhythmia
 | 
Position at onset | 
[Standing suggests vasovagal; supine or no prodrome suggests neurocardiac]; [syncope lying down excludes orthostatic hypotension]
 | 
Relation to exertion | 
[During exercise is high-risk and needs prompt cardiovascular evaluation; post-exercise is more often reflex]
 | 
Palpitations before loss of consciousness | 
[In the absence of known heart disease, their absence allows a cardiac cause to be excluded]
 | 
Family history of premature sudden death | 
Ask also about [unexplained drownings and single-vehicle collisions] — these may point to inheritable cardiac disease
 | 
Witness account | 
Separate field; the patient cannot report the event itself
Two cautions. The clinical features of unexplained and neurally mediated syncope [are very similar, and the same study did not support the usefulness of several clinical variables commonly used in practice] — so the agent collects the fields and does not attempt the classification. And exertional syncope is [infrequent, at 1.3% of athletes with syncope], so a positive is rare but high-consequence: exactly the pattern that suits a tireless asker.
The family history question is a good example of where an agent may outperform. Asking about drownings and single-vehicle collisions when someone presents having fainted feels tangential under time pressure, and is the kind of question a busy registrar drops first.
Added in consolidation: syncope in a patient who could be pregnant raises ruptured ectopic pregnancy; the pregnancy gating question is asked early, and any positive routes to the vaginal bleeding row's escalation rules.
Palpitations: the only row where the agent's timing is itself diagnostic. The [outpatient approach] notes that the yield of a single ECG is low, but [approaches 50% when the ECG is recorded during ongoing palpitations]. The GP booking agent is frequently speaking to the patient while the symptom is happening — which a clinic appointment three days later is not. If the patient reports palpitations right now, that is not just a history item; it is a live opportunity that expires, and the handover should say so explicitly.
History features with published likelihood ratios for an arrhythmic cause:

 | 
Feature | 
LR
 | 
Visible neck pulsations | 
[2.7]
 | 
Palpitations affect sleep | 
[2.3]
 | 
Palpitations at work | 
[2.2]
 | 
Known heart disease | 
[2.0]
 | 
Episodes lasting under 5 minutes | 
[0.38]
 | 
Family history of panic disorder | 
[0.26]
Build implications:

Do not let an anxiety story close the question. Panic may be [comorbid with an organic cause in up to 13% of cases], and the source guidance is explicit that even where a psychiatric comorbidity exists, [it should not be assumed the palpitations are non-cardiac]. The two negative LRs above are the weakest-sounding but most dangerous items in the table: an agent that hears \\\"I get anxious\\\" and stops asking will systematically under-call the 13%.

Visible neck pulsations is a delegated observation, and falls under the rule established in the rash row — a positive is usable, a negative is not, and the handover must record that the patient observed it, not a clinician.

Ask the patient to tap out the rhythm. Regular versus irregular, and sudden versus gradual onset and termination, are the discriminating features in the [suggestive-findings table], and both are recoverable by voice. Tapping is more reliable than asking a patient to characterise a rhythm in words.

Exertional palpitations and exertional syncope are separate red flags and are asked separately, as in the syncope row above.

Family history question is shared with syncope — recurrent syncope or early sudden death, [including deaths sometimes described as seizures]. Ask it once and populate both rows.
Leg swelling: the mirror image of the GI bleeding row. Where Glasgow-Blatchford let the agent pre-populate half a validated score, Wells does not — and the reason is instructive.
Of the ten Wells criteria, four are pure history: active cancer, paralysis or recent immobilisation, recently bedridden three days or major surgery within twelve weeks, and previously documented DVT. Three more are patient-observable rather than historical (entire leg swollen, pitting oedema confined to the symptomatic leg, collateral superficial veins). Two require examination or measurement — localised tenderness along the deep venous system, and [calf swelling more than 3 cm larger than the asymptomatic side measured 10 cm below the tibial tuberosity].
The tenth is the problem. The −2 item, an alternative diagnosis at least as likely as DVT, is [the most subjective element but also one of the most powerful discriminators in the model]. It is pure clinician judgement, and it is the only item that can move the score downward. An agent-assembled Wells would therefore be systematically biased upward — it can collect every point that raises the score and none of the one that lowers it.
Build rules:

The agent collects Wells components and never assembles them, for the reason above and for the reason given in the GI bleeding row. The handover lists the history items found; the clinician scores.

Unilateral versus bilateral is the first fork and is fully recoverable by voice. [Acute unilateral leg oedema means rule out DVT]; bilateral moves toward heart failure, medications, and renal causes, which changes the whole downstream question set.

Ask about injury explicitly. Once DVT is excluded, [40% of cases are muscle strain, tear or twisting injury, where the history of injury is the thing being looked for]. This is a question an agent can ask as well as anyone.

Medication history is diagnostic here, not background. Calcium channel blockers, vasodilators and hormone therapies are named causes of bilateral oedema, so the standard medication section needs to be pulled forward into this row rather than left to the closing sections.

Pitting oedema is a delegated observation — the patient can press and report — and falls under the rash-row rule: positive usable, negative not, and the handover records who observed.
Haemoptysis: the first question is whether it is haemoptysis at all. Before any characterisation, the [approach requires ruling out pseudohaemoptysis] — distinguishing blood from the lungs from blood originating in the nose, mouth or stomach, [each of which requires different treatment]. That fork is entirely historical: was it coughed or vomited, was there nosebleed or dental bleeding first, what did it look and taste like. An agent can work this fork as well as a clinician, and it is the one part of the assessment that imaging cannot settle.
The cancer-risk features are [age over 40, a smoking history of at least 30 pack-years, or a bleeding volume of at least 30 mL]. Two of the three are pure history. Published predictors of malignancy:

 | 
Predictor | 
Odds ratio
 | 
Former airways malignancy (multivariate) | 
[22.1]
 | 
Smoking ≥30 pack-years | 
[6.0]
 | 
Former airways neoplasm | 
[6.0]
 | 
Smoking ≥10 pack-years | 
[3.2]
 | 
Age ≥50 years | 
[9.9]
Build rules:

Volume is the weakest field in this row and must be treated as such. The agent cannot ask for millilitres. Household comparators (streaks in sputum, a teaspoon, a tablespoon, half a cup) are the only usable form, and even then the literature's own thresholds for massive haemoptysis vary from [100–150 mL up to 600 mL depending on the source]. Record the patient's words and comparator, never a number the agent derived.

A small volume does not reassure, and the handover must not imply it does. Guidance is to [assume even a small volume is life-threatening until proven otherwise], and light or non-smokers with haemoptysis [should be considered at risk of lung neoplasm when other risk factors are present, regardless of the amount of bleeding]. This row therefore sits with back pain, not with breathlessness, in the negatives table.

Pack-years is arithmetic, not a score. The prohibition elsewhere in this document is on assembling validated instruments. Collecting cigarettes per day and years smoked and reporting the product is a unit conversion, and is permitted — but the components must appear in the handover alongside it.

Ask about anticoagulants explicitly, and, in women, about [any association with menses]. Catamenial haemoptysis is rare, but the question is almost never asked in a time-pressured consultation and costs the agent nothing.

Duration over a week, weight loss and night sweats raise the intensity of evaluation and are all historical. Expect substantial overlap with the constitutional section — ask once, populate both.
Cough and wheeze: the row where the agent must most carefully not help. Unlike the presentations above, there is no validated history instrument to anchor to, and the guidance actively warns against the thing an agent is most tempted to do. GINA and others carry a [strong recommendation that an asthma diagnosis is not based on symptoms alone], against a background of [over-diagnosis and over-treatment in high-income countries]. Even spirometry has a sensitivity of only [29% for airway obstruction in asthma, against 90% specificity] — asthma can be ruled in but not ruled out, and the authors note this uncertainty itself drives overestimation of asthma.
So the agent's contribution here is not pattern recognition. It is capturing the features that a history-based model found discriminatory — [smoking status, exacerbation history, response to treatment, symptomatic periodicity, and history of allergy or atopy] — and handing them over uninterpreted. Periodicity is the item best suited to voice and worst served by a rushed consultation: worse at night, worse in the early morning, worse on exertion, seasonal, better away from home or work.
The exception is choking. In suspected foreign body aspiration in children, the clinical history has a sensitivity of [90.5% with specificity 24.1%], and reported symptoms [97.8% sensitivity with 7.4% specificity]. Abrupt-onset cough is [highly sensitive but not specific]. This is the breathlessness pattern rather than the back pain one: a genuinely negative history does useful work, while a positive one does not narrow much. A direct, explicit question about a choking or witnessed-swallowing episode belongs in every paediatric cough interview, and the answer is worth recording verbatim.
Build rules:

The agent does not name asthma, COPD or any obstructive diagnosis, and does not summarise a symptom cluster as suggestive of one. This is a stronger version of the general no-reassurance rule, and it is specific to a presentation where symptom-based diagnosis is a documented harm.

Duration determines the question set — acute, subacute and chronic cough have different differentials — and is one of the few fields here that is reliable by voice.

Haemoptysis is screened for in every cough interview and routes to the row above.

This row is marked as anchored on weaker evidence than its neighbours. Reviewers should be told that, rather than left to infer it from the absence of a table.
Neurological

 | 
Presentation | 
Patient trigger phrasings | 
Framework to ground in | 
Red flags
 | 
Headache | 
headache, migraine, head pain, pressure in my head | 
SNNOOP10 on the symptom field set, not SOCRATES | 
Thunderclap onset; worst ever; fever and neck stiffness; woken from sleep; worse on coughing or lying flat; new headache over 50; focal deficit
 | 
Weakness | 
weak, can't move it, arm won't work, dragging my leg, heavy | 
Distribution, onset speed, progression | 
Sudden onset; unilateral; facial involvement; speech disturbance — including symptoms that have since resolved — stroke pathway
 | 
Altered sensation | 
numb, pins and needles, tingling, burning, dead feeling | 
Distribution, dermatomal vs glove-and-stocking, onset | 
Saddle anaesthesia; bilateral leg symptoms; associated bladder or bowel change
 | 
Dizziness | 
dizzy, light-headed, room spinning, off balance, woozy | 
TiTrATE — timing and triggers, NOT symptom quality | 
Associated focal deficit, diplopia, dysarthria, ataxia; sudden onset with headache
 | 
Seizure | 
fit, seizure, convulsion, shaking episode, blanked out | 
Sheldon history items, collected not scored; witness account as a separate interview; ask where on the tongue | 
First seizure; prolonged or repeated; head injury; pregnancy; failure to return to baseline
 | 
Confusion | 
muddled, not making sense, forgetful, not themselves | 
Acute vs chronic; fluctuation; collateral history essential | 
Acute onset or fluctuation; fever; head injury; new focal deficit. Not a bail-out: the agent takes a structured collateral history and never records \\\"confused\\\" as a finding — see the confusion entry
 | 
Visual disturbance | 
blurred, double vision, lost vision, curtain across my eye, flashes and floaters | 
Monocular vs binocular; onset; transient vs persistent | 
Sudden painless loss; curtain descending; associated headache or jaw claudication; new flashes with floaters
 | 
Speech disturbance | 
slurred, can't find words, talking funny, gibberish | 
Expressive vs receptive vs dysarthric; onset | 
Any sudden onset — stroke pathway
The dizziness row was drafted wrongly on the first pass and has been corrected — see the framework note below. It remains the row most worth watching, because the intuitive approach is the discredited one.
Dizziness: use timing and triggers, not symptom quality. The intuitive approach — asking the patient to sort their dizziness into vertigo, presyncope or disequilibrium and branching from there — is [inconsistent with current best evidence]: it does not distinguish benign from dangerous causes. Triage [based on type of dizziness has never been validated, is unreliable because it is not evidence-based, and has not been shown to accurately correlate with the cause].
[TiTrATE] replaces it: the Timing of the symptom, the Triggers that provoke it, and a Targeted Examination. Timing and triggers are both history, so the agent can carry that half properly and hand the examination to the clinician. The [algorithm sorts presentations into acute and episodic vestibular syndromes by timing and triggers], which is exactly the shape of a branching question tree.
Two caveats for the build. The [evidence base in the dizziness literature is weak overall], and no emergency medicine guidelines exist — most studies come from settings or subspecialists that do not transfer to ED practice. And [structured history-taking matters most precisely for vague presentations like vertigo, dizziness and gait unsteadiness], which is an argument for the agent rather than against it: consistency is the thing a tired clinician loses first.
This row is also a caution for the whole project. The first draft of this document encoded the intuitive approach, which happens to be the discredited one. Every framework in these tables needs checking against current evidence rather than against what feels clinically familiar.
Added in consolidation: dizziness in a patient who could be pregnant is asked the pregnancy gating question. In one case series of ectopic pregnancy, [dizziness was reported in 23%] — a minority, so its absence says little, but combined with pain or shoulder-tip pain it moves the patient to the immediate tier under the vaginal bleeding row.
Confusion: the first draft was wrong to make this a bail-out. The row originally treated confusion as a presentation where the agent recognises it is out of its depth and hands over. The evidence suggests a more useful role, and identifies a genuine gap the agent might fill.
The [ED diagnostic accuracy meta-analysis] found that no studies were identified exploring the accuracy of findings on history for delirium detection, and that while clinicians can accurately rule delirium in, clinician gestalt is inadequate to rule it out. Detection rests on structured instruments rather than impression.
The 4AT is the best fit for this setting:

 | 
Property | 
Value
 | 
Pooled positive likelihood ratio | 
[7.5]
 | 
Pooled negative likelihood ratio | 
[0.18]
 | 
Sensitivity / specificity at ED triage | 
[89.7% / 84.1%]
 | 
Administration time | 
[Under 2 minutes]
 | 
Training required | 
[Designed for routine use without special training]
Revised handling:

Collateral history is the agent's strongest contribution. Distinguishing delirium from pre-existing cognitive decline [requires a structured collateral history], and establishing baseline versus current mental status is exactly what an unhurried interview with a relative can do. This is a separate interview from the patient's, and the design should support it explicitly.

Never record \\\"confused\\\" as a finding. Confusion is [a symptom, not a diagnosis, and documenting a patient as simply confused without further detail is medically inadequate]. The handover states baseline, current state, time course, fluctuation, and who provided the account.

The bail-out still applies to the patient interview, not to the presentation. If the patient cannot engage, the agent hands over — but it should still offer the collateral interview rather than abandoning the presentation entirely.

Do not administer the 4AT itself. Parts of it require observed assessment of attention and alertness. The agent collects the history around it and the clinician administers the instrument.
The gap is worth naming for the study: there is no evidence base on history findings for delirium detection. A structured collateral history, reliably obtained, is a plausible contribution to an area the literature has not examined.
Headache: use SNNOOP10. The [SNNOOP10 list] is the best-fitting framework in this document for an agent, because it is an explicit enumerated checklist rather than a judgement heuristic. A [validation study found 100% sensitivity for detecting high-risk headache disorders], with [every patient having a serious cause carrying at least one red flag from the list].
Of the fifteen items, twelve are pure history and directly askable:

 | 
Item | 
Asked as
 | 
Systemic symptoms including fever | 
Fever, weight loss, night sweats, systemic illness
 | 
Neoplasm history | 
Known or past cancer
 | 
Neurologic deficit including decreased consciousness | 
Weakness, numbness, speech or vision change, drowsiness
 | 
Sudden or abrupt onset | 
Time from nothing to worst — seconds or minutes
 | 
Older age, onset after 65 | 
Age plus first presentation of this headache
 | 
Pattern change or recent onset of new headache | 
Different from usual headaches, or the first of its kind
 | 
Positional headache | 
Worse lying flat or standing up
 | 
Precipitated by sneezing, coughing or exercise | 
Direct question
 | 
Progressive headache and atypical presentation | 
Worsening over days or weeks
 | 
Pregnancy or puerperium | 
Pregnancy status, recent delivery
 | 
Painful eye with autonomic features | 
Eye pain, redness, tearing, lid droop
 | 
Posttraumatic onset | 
Head injury before onset
 | 
Pathology of the immune system such as HIV | 
Immunosuppression, immune condition
 | 
Painkiller overuse or new drug at onset | 
Analgesic frequency, new medications
 | 
Papilledema | 
Examination only — not available to the agent
Only papilledema requires examination. The agent collects the other fourteen and the handover states explicitly which were positive, which were negative, and that the fundoscopic item was not assessed.
One caution against over-reading the sensitivity figure: 100% sensitivity across a checklist of fifteen items is achieved partly by breadth, and the [absence of red flags is what supports the conclusion that no further workup is needed]. A negative screen is only as good as the completeness of the asking — which is the argument for the agent, provided it never infers a negative it did not ask.
Weakness, altered sensation, speech and visual disturbance: the stroke cluster. These four first-draft rows are treated together because in practice they converge on one time-critical question, and because there is directly relevant prior art.
Prior art, and a documented failure mode. A [voice AI agent system for prehospital stroke assessment] has been evaluated across ten simulated cases. It captured gender, prior stroke history and glucose in all ten, and age, last known well time and symptom onset time in nine. The two failures are precisely the ones this document has been designing against: in one case the system [recorded symptom onset time rather than last known well time when both were provided], and in another [an anticoagulant was hallucinated on the basis of the user mentioning an unrelated diabetes medication]. Anticoagulant history was correct in only eight of ten.
That is a real instance of the confabulation failure identified early in this project as the single biggest safety risk, occurring in the exact deployment being proposed. It should be cited in the protocol, and the evaluation should be powered to detect it rather than assume it away.
Last known well and symptom onset are two fields, not one. They diverge whenever onset was unwitnessed, and the prehospital literature notes onset time [remains unknown in approximately 25% of patients], either because nobody saw it or because the stroke itself prevents the patient from giving the history. The agent must ask for both separately, store both separately, and where they differ, hand over both. Collapsing them is the documented error above.
This is the absolute-time rule from the testicular torsion row, and stroke is its second instance: capture clock times, confirm the computed interval back to the patient, and never let elapsed time soften the escalation.
The agent's relationship to the stroke scales is the inverse of its relationship to Wells. ROSIER combines examination items — facial, arm and leg weakness, visual fields — with two history items, loss of consciousness and seizure. Those two history items are the negative ones: they subtract points, because they mark common mimics. So where an agent-assembled Wells could only ever be biased upward, an agent-assembled ROSIER could only ever be biased downward. The rule is the same in both directions: collect the components, assemble nothing.
For context on what the scales do and do not deliver: FAST shows [sensitivity of 94–95% with specificity of 55–60%], and a meta-analysis of ROSIER at a cut-off of ≥1 found [sensitivity 0.89 and specificity 0.76].
Build rules:

Speech disturbance is the one presentation where the symptom attacks the interview itself. Dysphasia, dysarthria and reduced conscious level all degrade the history at exactly the moment it matters most. This row needs an explicit early branch to collateral history, and a low threshold for abandoning the interview and escalating — a partial history with a fast handover beats a complete one obtained slowly.

Escalate on suspicion, before completing the interview. This is the strongest case in the document for the immediate-interrupt tier, and the GP-version handling of it is one of the open questions that most needs resolving.

Medication history is verified, not inferred. Given the hallucinated-anticoagulant finding above, the agent asks for anticoagulants by name and by indication, records the patient's words, and states plainly when it did not ask or the patient did not know. It never infers a drug class from an adjacent mention.

Resolved symptoms still count. A deficit that has fully recovered is a TIA until proven otherwise and does not de-escalate. Ask explicitly whether anything has already resolved, as the unwell-child row does for fever features.

Visual disturbance has its own branch, for monocular versus binocular loss and transient monocular loss — now drafted and grounded immediately below.
Visual disturbance — the monocular branch (closes the gap in rule 5 above). Two time-critical diagnoses sit here, each with a different clock.
Retinal artery occlusion is a stroke, and should be routed as one. Central retinal artery occlusion is [a stroke equivalent with a treatment window of under 4.5 to 6 hours], and any acute retinal ischaemia is [recognised as a stroke equivalent by the AHA/ASA]. It carries a [44-fold increased risk of ischaemic stroke in the first week compared with subsequent weeks]. Transient monocular loss — amaurosis fugax — [suggests TIA or carotid disease], so the stroke cluster's rule that resolved symptoms still count applies unchanged.
There is a documented referral gap the agent can close. In one survey, [only 64.2% of ophthalmologists would refer a patient with central retinal artery occlusion for urgent stroke evaluation]. Patients with sudden monocular loss often present to eye services rather than stroke pathways. An agent that routes painless sudden monocular loss into the stroke cluster's escalation — with clock-time capture — sends these patients down the pathway the guidelines say they belong on.
Giant cell arteritis: the clock is the second eye. In GCA, vision loss [once it has occurred is irreversible]; in untreated patients the [other eye can be lost within a week], and [starting steroids before vision loss significantly reduces the chance of ocular complications]. So in any patient over 50 with visual symptoms, or with new headache, the GCA history is asked — because a positive answer is what gets steroids started before the second eye goes.
From a meta-analysis of 68 studies and 14,037 patients:

 | 
Feature | 
LR+ | 
LR−
 | 
Limb claudication | 
[6.01] | 
—
 | 
Jaw claudication | 
[4.90] | 
[0.68]
 | 
Scalp tenderness | 
[1.85] | 
[0.77]
 | 
Age over 70 | 
[1.64] | 
[0.48]
 | 
Headache | 
[1.33] | 
[0.61]
 | 
Temporal headache | 
[0.97] | 
[1.07]
 | 
Age over 60 | 
[1.25] | 
[0.15]
Another intuitive question that does not work. \\\"Is the headache at your temples?\\\" is the question the name of the disease invites, and it carries a likelihood ratio of 0.97 — no information in either direction. Jaw claudication — pain in the jaw muscles when chewing that eases on stopping — is the history item with real weight, and limb claudication stronger still. This joins dizziness quality-typing and the five Ps in the recurring-principles section. Also note the pattern of negatives: [absence of these findings does not sufficiently reduce probability to exclude further work-up] — the back pain pattern — except for age under 60, which does lower it substantially.
Build rules:

Sudden painless loss of vision in one eye, current or resolved, is immediate tier, handled through the stroke cluster with onset captured as a clock time. It is not routed to a routine eye appointment.

Ask jaw claudication and limb claudication concretely. \\\"Does your jaw ache when you chew, and does it ease when you stop?\\\" and the equivalent for arms. Scalp tenderness is asked as \\\"is your scalp sore, for example when brushing your hair?\\\" — a history question, not an examination.

Ask about any previous diagnosis of polymyalgia rheumatica, a [feature that raises suspicion].

Over 50 with jaw or limb claudication and any visual symptom is immediate tier, because the second eye is at risk. Over 50 with jaw or limb claudication and no visual symptom is same-day. These thresholds are proposals for ophthalmology and rheumatology review.

Ask which eye, and whether it is one eye or one side. The history of [monocular versus binocular loss distinguishes eye from brain]. Patients with a field defect affecting both eyes on one side often report it as loss in the eye on that side. Asking the patient to cover each eye in turn is a candidate delegated observation that could help, but it is not grounded in the sources above and is proposed for ophthalmology review rather than adopted.

Painful red eye is a different presentation and is not covered by this branch.
Seizure: the best-fitting instrument in this document, and the clearest argument for still not assembling it. Where SNNOOP10 was fourteen history items out of fifteen, the Sheldon rule for [distinguishing seizure from syncope] is history in its entirety — no examination, no investigation — and reports overall accuracy of 96% in development and 94% in testing, with 94% sensitivity and 94% specificity.

 | 
Criterion | 
Points
 | 
Waking with a cut tongue | 
+2
 | 
Abnormal behaviour noted | 
+1
 | 
Loss of consciousness with emotional stress | 
+1
 | 
Postictal confusion | 
+1
 | 
Head turning to one side during loss of consciousness | 
+1
 | 
Prodromal déjà vu or jamais vu | 
+1
 | 
Any presyncope | 
−2
 | 
Loss of consciousness with prolonged standing or sitting | 
−2
 | 
Diaphoresis before a spell | 
−2
Individual discriminators, for the handover rather than for scoring:

 | 
Feature | 
Sensitivity | 
Specificity | 
LR
 | 
Cut tongue | 
[45%] | 
[97%] | 
[17]
 | 
Head turning during the event | 
[43%] | 
[97%] | 
[14]
 | 
Unusual posturing during the event | 
[35%] | 
[97%] | 
[13]
 | 
Absence of presyncope | 
[77%] | 
[86%] | 
[5.6]
Ask where on the tongue. This is the highest-yield voice-recoverable detail in the row. Pooled analysis gives lateral tongue biting a positive LR of [49.3 for epileptic seizure with specificity 99.8%], while biting at the tip points the other way, [towards syncope]. Sensitivity is low — around 11% for lateral biting — so this is a strongly positive-only finding, and the negative LR of roughly 0.85 to 0.89 means absence tells you almost nothing. Most clinicians ask whether the tongue was bitten; fewer ask where.
Why the agent still does not score it, despite the instrument being pure history:

Several items require a witness, not the patient. Head turning, abnormal behaviour and postictal confusion are observations the patient cannot make about themselves. The agent is usually speaking to the patient alone, so an agent-assembled score would be built from systematically missing items — the same structural bias identified for Wells and ROSIER, arriving by a third route.

Amnesia is the expected condition, not an edge case. Where patients are amnesic or [witness descriptions are unclear, misdiagnosis is frequent].

The administer-do-not-judge constraint from the mental health section applies unchanged. Several criteria require interpretation — whether behaviour was abnormal, whether confusion was postictal — and that judgement is the clinician's.
Build rules:

Collect the witness account as a separate, explicitly labelled interview, as the confusion row does for collateral history. Who saw it, what they saw, and whether they are available to speak.

Record tongue-bite location verbatim, and treat absence as uninformative in the handover.

First seizure and known epilepsy are different pathways. Ask early which this is.

This row shares its family history question with syncope and palpitations — recurrent syncope, early sudden death, and events described as seizures. Ask once, populate three rows.
Gastrointestinal and genitourinary

 | 
Presentation | 
Patient trigger phrasings | 
Framework to ground in | 
Red flags
 | 
Abdominal pain | 
tummy pain, guts hurting, cramps, stomach ache, colicky | 
Symptom field set, not SOCRATES, with region; pregnancy gating question | 
Sudden severe onset; rigidity; pain out of proportion; associated shock symptoms; pregnancy
 | 
Nausea and vomiting | 
sick, throwing up, queasy, heaving | 
Content, frequency, timing, relation to food | 
Haematemesis; faeculent vomiting; associated severe abdominal pain or headache
 | 
Haematemesis | 
vomiting blood, coffee grounds, red in my vomit | 
Volume, frequency, preceding retching | 
Any volume — escalate immediately
 | 
Bowel habit change | 
constipated, diarrhoea, loose, going more often, can't go | 
Baseline vs current; duration; consistency; blood or mucus | 
Blood in stool; unintentional weight loss; over 50 with new change; absolute constipation with vomiting
 | 
Rectal bleeding | 
blood when I wipe, blood in the toilet, black stools | 
Colour, mixed vs on surface, volume | 
Melaena; large volume; associated dizziness or weight loss
 | 
Dysphagia | 
trouble swallowing, food sticking, catches on the way down | 
Solids vs liquids asked separately; duration as a number; timing of sticking; level recorded but carries little weight | 
Short duration (under about 8 weeks); progressive; solids only; weight loss; unable to swallow saliva
 | 
Urinary symptoms | 
burning when I go, going all the time, can't go, urgency | 
Storage vs voiding symptom split | 
Fever with loin pain; acute retention; haematuria
 | 
Haematuria | 
blood in my urine, urine gone red or brown | 
Visible vs reported; timing in stream; clots; pain | 
Painless visible haematuria; clot retention
 | 
Testicular or scrotal pain | 
pain in my balls, groin pain, swelling down there | 
Onset speed, radiation, associated nausea | 
Acute pain, including intermittent pain, whatever the time elapsed — torsion, escalate immediately. New lump or swelling, even if painful
 | 
Vaginal bleeding | 
bleeding, spotting, heavy periods, bleeding between periods | 
LMP, pattern, volume, pregnancy status | 
Pain or bleeding in possible early pregnancy (ectopic can present without bleeding); postmenopausal bleeding; heavy bleeding with dizziness
Abdominal pain is the highest-volume undifferentiated presentation in both settings and is probably where the agent's branching is most tested.
Abdominal pain: severity self-report is unreliable, and so is who gets believed. Two findings here bear on the whole project rather than this row alone.
Older patients are systematically under-triaged: they [often do not complain of \\\"severe\\\" pain or show abnormal vital signs when presenting with serious causes, which increases wait times and biases assessment toward benign diagnoses]. An agent that asks a standard severity question and records the answer faithfully will reproduce this, because the problem is in the patient's report, not the asking. The mitigation is to weight functional change and progression over the severity score in older patients, and to state the patient's age alongside any severity claim in the handover.
Second, and more consequential for the study design: in a retrospective study of acute abdominal pain evaluation, [symptoms reported by Black and Hispanic patients were 26% and 56% less likely to be categorised as high acuity, and these patients were half as likely to receive equivalent care]. That is a documented bias in the human comparator arm. It should be treated as a measurable outcome in the comparative study rather than a footnote — whether the agent's elicitation and handover narrows or widens that gap is arguably a more important question than raw agreement between arms.
Other build notes for this row:

Diagnostic humility in the handover wording. The ED literature holds that it is [preferable to record \\\"nonspecific abdominal pain\\\" or \\\"abdominal pain of unknown aetiology\\\" than to assign a specific but unsupported diagnosis]. The agent should never name a likely diagnosis in the handover; it presents the history and lets the clinician reason.

Pain location does not reliably localise pathology. Appendicitis can present with right flank, right upper quadrant, left lower and rarely left upper quadrant pain. Site is a field to record, not a branch to trust.

Ask about cardiac symptoms in epigastric pain. Myocardial infarction [can present as epigastric pain with or without nausea and vomiting], so the chest pain branch should open from an abdominal presentation, not only a thoracic one.

Pregnancy status is mandatory in anyone of reproductive age, given ectopic pregnancy sits among the [life-threatening causes warranting urgent evaluation].
Added in consolidation: in any patient who could be pregnant, the pregnancy gating question (cross-cutting section) is asked early in this row. Ectopic pregnancy can present with abdominal pain alone, without vaginal bleeding — see the vaginal bleeding row.
GI bleeding: the agent can pre-populate half a validated score. The Glasgow-Blatchford Score is built from [four components — medical history (hepatic disease, heart failure), symptoms (melaena, syncope), signs (tachycardia, blood pressure), and blood tests (haemoglobin, urea)].
Two of the four are pure history. A structured interview can deliver the medical history and symptom components complete and verbatim before the clinician sees the patient, leaving only observations and bloods outstanding.

 | 
GBS component | 
Source | 
Agent can supply
 | 
Hepatic disease | 
Past medical history | 
Yes
 | 
Heart failure | 
Past medical history | 
Yes
 | 
Melaena | 
Presenting symptoms | 
Yes
 | 
Syncope | 
Presenting symptoms | 
Yes
 | 
Heart rate, systolic BP | 
Observations | 
No
 | 
Haemoglobin, urea | 
Bloods | 
No
This matters because of what the score is for: [a score of exactly 0 identifies patients at very low risk of needing intervention, under 1%], and the score exists to [stratify which upper GI bleeding patients are low-risk candidates for outpatient management]. A complete, reliably elicited history is therefore a direct input to a disposition decision, not merely background.
Build notes:

Melaena needs describing, not naming. Patients do not use the word, and \\\"black stools\\\" invites confusion with iron tablets or bismuth. Ask about colour, consistency, smell and any recent iron supplementation, and record the description rather than a clinical label.

Syncope belongs in the GI history. It is a GBS variable, so the syncope fields above should open from a GI bleeding presentation rather than being confined to the collapse entry.

Do not compute or report a partial score. The agent supplies the fields; the clinician calculates. A partial score in a handover invites a disposition decision on incomplete data — the same failure class as the agent offering a diagnosis.
Testicular torsion: time of onset is the highest-stakes single field in this document. Every other presentation treats onset as one domain among eleven. Here it determines the outcome, and it is pure history.

 | 
Time from symptom onset | 
Testicular salvage rate
 | 
Within 6 hours | 
[90–100%]
 | 
First 12 hours | 
[90.4%]
 | 
13 to 24 hours | 
[54.0%]
 | 
Beyond 24 hours | 
[18.1%]
Build rules:

Capture the clock time of onset, not a duration. \\\"Since last night\\\" is not usable; the handover needs a time the clinician can compute an ischaemia interval from. The agent should convert and confirm: \\\"so that's about nine hours ago — is that right?\\\"

Do not let a long duration reduce urgency. Survival is [significant beyond the commonly held 6 to 8 hour time frame], and overall salvage across the literature is [41.5%]. A patient presenting at 20 hours is still an emergency, and the escalation tier does not change with elapsed time.

Intermittent pain still counts. Torsion [often presents as abrupt onset unilateral scrotal pain, which may be constant or intermittent]. A history of previous self-resolving episodes is relevant, not reassuring.

Do not score TWIST. It includes examination findings. The agent collects the history components and flags that the score is available to the clinician.
This row also argues for a design feature elsewhere: a general rule that any presentation with a time-critical intervention gets onset captured as an absolute time with confirmation, rather than as a relative duration. Stroke and chest pain qualify on the same grounds.
Vaginal bleeding: the row is misnamed, and the question it depends on belongs in three other rows. The time-critical diagnosis behind early-pregnancy bleeding is ectopic pregnancy, which is [the leading cause of pregnancy-related death in the first trimester] — and up to [30 percent of patients with ectopic pregnancy have no vaginal bleeding at all]. The classic triad of pain, amenorrhoea and bleeding [is uncommon]. A row keyed to bleeding will miss the patients who matter most.

So pregnancy status is a gating question, not a row. Guidance is that a woman of reproductive age presenting with [abdominal pain, vaginal bleeding, syncope, or hypotension] should have pregnancy considered. That means the abdominal pain, syncope and dizziness rows already in this document are each missing a question. It should be asked once, early, and populate all four — with wording reviewed for patients who are not women, patients who may not know, and patients who may not want to say in front of whoever else is in the room.
Negatives are uninformative, in three separate ways:

Risk factors. [About half of patients with ectopic pregnancy have no known risk factors], and guidance is explicit that [a lack of risk factors does not rule it out]. Positives still matter: a history of one ectopic [confers a 10% risk in subsequent pregnancies, rising to more than 25% after two or more].

Passage of tissue. Patients often report this as though it settles things. It does not: bleeding and passage of tissue [cannot be relied on to differentiate ectopic pregnancy from early intrauterine pregnancy failure]. The agent must record it verbatim and must never let the handover imply a completed miscarriage.

A negative home pregnancy test. This is a delegated observation under the cross-cutting rule — the patient performed it — and [urine pregnancy tests can produce false negatives]. A positive home test is usable; a negative one is recorded with who did it and when, and does not close the question.
Ask about shoulder-tip pain and an urge to open the bowels. Both [may indicate blood leaking from the tube], both are pure history, and neither is something patients connect to a gynaecological problem unless asked. Together with dizziness or collapse they move this from same-day to immediate.
Escalation — this breaks the warm-handback model for the same reason fetal movements did. Guidance is that [all patients with suspected ectopic pregnancy should be considered potentially unstable]. On the GP booking call, pain or bleeding with possible early pregnancy routes to same-day in-person assessment at minimum, and shoulder-tip pain, dizziness or collapse routes to the immediate tier. Two rows now require this, which suggests the GP version needs a defined same-day-in-person pathway rather than handling each as an exception. Needs the same obstetric and gynaecological reviewer as the fetal movements row.
Haematuria: the agent collects; the jurisdiction decides. Visible haematuria has [the highest positive predictive value of any symptom for urological cancer in primary care, at 5.1%], and it is almost entirely age- and sex-dependent. In men over 60 the PPV for urological malignancy is [22.1%, against 8.3% in women of the same age]; under 45, it falls to [0.99% in men and 0.22% in women].
The referral threshold is not a clinical fact, and the agent must not embed one. NICE refers from age 45, the American Urological Association investigates from 35, and the Scottish guidelines [set no age threshold for painless visible haematuria at all]. The source is explicit that these differences [reflect the cost-effectiveness thresholds of each health system] rather than differing evidence. The agent's job is to capture age, sex, and the features below; the urgency attached to them is a local policy parameter, set by whoever deploys the agent in SA Health, and should be configurable rather than written into the question set. This is the first row where that distinction has mattered, and it will apply equally to the weight loss and bowel habit rows.
Painless is the discriminating word, and pain is the reason for delay. Painless visible haematuria is [the commonest presentation of bladder cancer], and diagnosis is [often delayed because the symptoms resemble benign disorders such as infection or passage of stones]. An agent that asks the same questions every time addresses that delay mechanism directly:

Was it painless? Recorded verbatim. A painful episode does not close the question.

Has it happened before, and did it come back after antibiotics? Referral criteria specifically include [visible haematuria that persists or recurs after successful treatment of urinary tract infection]. This is a pure-history item that depends on the patient connecting two episodes weeks apart, which a single consultation often misses.

Smoking, including pack-years, under the same arithmetic rule as the haemoptysis row.

Occupation. Exposure to urothelial carcinogens is an established risk factor, with [metal workers, painters and rubber manufacturing] named. Occupational history is routinely omitted under time pressure and costs an agent nothing. Ask about past as well as current work.

Pelvic irradiation, chronic catheter use and recurrent infection, all [listed risk factors].
Australian context for reviewers. Bladder cancer is [substantially more common in men, with lifetime risk to age 85 of one in 43 for men against one in 166 for women]. The sex gradient is steep enough that the handover must always carry sex and age alongside the finding — a bare "visible haematuria" without them is close to uninterpretable.
Scope limit. The agent can only elicit visible haematuria, since non-visible haematuria is a laboratory finding. The row should not be read as covering it.
Dysphagia: history does the localising, and the intuitive localising question is the one that fails. A careful history distinguishes oropharyngeal from oesophageal dysphagia in [about 80 to 85% of cases] — but the same guidance states that [more precise localisation is not reliable]. In one cohort of 1,400 patients, malignancy was no more likely at one level than another: [11.9% for pharyngeal-level dysphagia against 12.4% for mid or lower sternal]. "Point to where it sticks" is the question patients and clinicians both reach for first, and it carries almost no weight. Same lesson as the dizziness row: record the answer, do not reason from it.
What does discriminate is what the patient can swallow. Solids and liquids together suggest a motility disorder; liquids only suggests oropharyngeal pathology; solids only suggests [mechanical obstruction — stricture, web, or tumour]. Oropharyngeal dysphagia usually involves difficulty starting the swallow, whereas oesophageal dysphagia is felt as [food getting stuck after swallowing]. Both are voice-recoverable, and the agent should ask about solids and liquids as separate questions rather than "what gives you trouble".
Short duration is the danger sign, not long duration. This runs against intuition, and against the default instinct that a longstanding symptom is more worrying. In the same cohort, malignancy was found in [16.6% of those with dysphagia of eight weeks or less, 14.5% at eight to twenty-six weeks, and 2.5% beyond twenty-six weeks]. Malignant oesophageal dysphagia [progresses more rapidly]. The handover must carry duration as a number and must not let a short history read as "early, so less concerning".
True dysphagia versus globus is worth one precise question. Malignancy was more likely in those describing food or drink sticking [within five seconds of swallowing — 15.1% against 5.2%]. That timing question is exactly the kind a rushed consultation skips.
Negatives are the informative half. A history-based score in the same cohort had [sensitivity 98.4%, specificity 9.3%, PPV 11.8% and NPV 98.0%] — the breathlessness pattern, not the back pain one. But the agent does not assemble it, under the cross-cutting rule, and in any case history cannot finish the job: a [definitive diagnosis cannot be established in most instances by history alone], and NICE recommends [open-access endoscopy within two weeks for all patients with dysphagia]. So in primary care the history does not decide whether to refer — it decides which pathway, and how fast.
Build rules:

New oropharyngeal dysphagia routes to the stroke cluster for its onset-time and escalation handling, and the two rows share their onset questions.

Weight loss is asked here and populates the constitutional row. It is a named feature in the malignancy profile alongside [short duration, progression, and solids more than liquids].

Inability to swallow saliva — complete obstruction — should sit in the immediate tier. This is standard clinical teaching but is not grounded in the sources cited above; included for reviewer confirmation rather than as an evidenced row.
Bowel habit change and rectal bleeding: the red flags are real, and most cancers don't have them. In a primary care case-control study of 5,477 colorectal cancers, [only 27% of patients had reported either of the two higher-risk symptoms], and [the presenting symptoms for 73% had predictive values below 1.2%]. A red-flag screen, however faithfully administered, will miss most of the disease. That is the finding reviewers most need to see in this row.

 | 
Feature | 
PPV for colorectal cancer
 | 
Rectal bleeding, age 50 and over (pooled) | 
[8.1%]
 | 
Rectal bleeding, male aged 80 and over | 
[4.5%]
 | 
Change in bowel habit | 
[3.9%]
 | 
Abdominal pain | 
[1.2%]
 | 
Diarrhoea | 
[1.2%]
 | 
Weight loss | 
[0.8%]
 | 
Constipation | 
[0.7%]
PPVs were [lower in females and younger patients], so as with haematuria, age and sex travel with every finding in the handover.
Combinations matter, and not in the direction patients expect. Rectal bleeding with weight loss or with change in bowel habit raises risk, with [pooled positive LRs of 1.9 and 1.8]. But rectal bleeding accompanied by abdominal pain, diarrhoea or constipation has [a positive LR of one or less]. Patients often explain bleeding by the accompanying symptom — "it's from straining", "it's because I've had the runs" — and a clinician can be carried along by the explanation. The agent records the explanation and the finding separately, and never lets the first stand in for the second. The source concludes that rectal bleeding [warrants investigation irrespective of whether other symptoms are present].
The published numbers belong to a setting, and this row makes that visible. Predictive values from referred populations [generally overestimate the likelihood of cancer] when applied to primary care — rectal bleeding carried a PPV of [5.2% in a referred population against 2.4% in unselected primary care]. This applies to every table in this document, not just this one. The GP and ED versions see different base rates, so the same patient words carry different weight in each. Any future decision to weight findings differently by setting should be taken explicitly, and should cite the setting each number came from.
Build rules:

Ask about bowel habit concretely. Frequency, consistency, direction of change, and how long ago it started — not "any change in your bowels?", which patients answer against their own shifting baseline. Duration as a number, as in dysphagia.

Rectal bleeding is asked in every bowel habit interview and vice versa, since the pair is where most of the predictive weight sits.

The jurisdiction rule from the haematuria row applies unchanged. Age thresholds for referral are local policy parameters, not question-set content.

Low-risk symptoms are still recorded in full. Given that 73% of cancers present this way, a handover that only surfaces red flags would systematically deprioritise most of the disease. Whether repeated presentation with low-risk symptoms should itself raise priority is a reasonable design question, but it is not grounded in the sources above and is left open for reviewers.
Urinary symptoms: the only row in this document where history alone can make the diagnosis. In women, the combination of dysuria and frequency without vaginal discharge or irritation carries a [likelihood ratio of 24.6] and raises the probability of UTI [to more than 90%, effectively ruling in the diagnosis based on history alone]. Guidance supports treating women with this uncomplicated history [without other evaluation], with studies reporting lower costs and better satisfaction [with no increase in adverse outcomes]. Physical examination has been questioned as adding [little diagnostic utility].

 | 
Feature | 
LR
 | 
Dysuria + frequency, no vaginal discharge or irritation | 
[24.6]
 | 
Self-diagnosis, in women with recurrent UTI | 
[4.0]
 | 
Haematuria | 
[2.0]
 | 
Frequency | 
[1.8]
 | 
Dysuria | 
[1.5]
 | 
History of vaginal discharge | 
[0.3]
 | 
History of vaginal irritation | 
[0.2]
The most powerful single items point away from the diagnosis. Of all individual features, the two strongest were [vaginal discharge and vaginal irritation, which decrease the likelihood of UTI when present]. These are the questions a hurried or embarrassed consultation is most likely to skip — the same reasoning as the sphincter and sexual function questions in the back pain row. An agent asks them every time. Without them, the combination cannot be assessed, and roughly [50% of women with UTI symptoms who lack the specific combination do not have cystitis] — so misdiagnosis is common when the question set is incomplete.
Patient self-diagnosis is data, and this row is its second appearance. A woman with recurrent UTI saying "this is another one" carries an LR of 4.0 and, in a population with around 50% prevalence, the [highest positive predictive value of any single feature, at 86%]. This parallels carer concern in the unwell-child row: the patient's own prior-experience judgement is a measured predictor, not noise to be filtered. Record it verbatim, attributed.
Why the agent still does not diagnose. The collect-not-assemble rule is under the most pressure here, because the rule-in combination is effectively a diagnosis. It still holds, for two reasons. First, the evidence applies only to a narrow population: uncomplicated UTI is defined as infection in a [non-catheterised, non-pregnant adult with no urologic abnormalities or immunocompromise] and no systemic illness, and outside young women [the specificity of dysuria falls]. Establishing that a patient is inside that population is a judgement, not a lookup. Second, the handover is to a clinician who decides; if SA Health later wants a nurse-led or pharmacist-led pathway that acts on this combination, that is a governance decision about the downstream pathway, not a change to what the agent does.
Build rules:

Collect the exclusion criteria explicitly and hand them over as a set: pregnancy (the gating question from the vaginal bleeding row), catheter, known urological abnormality, immunocompromise, fever, and loin or back pain. The handover should state which were asked and answered, so the clinician can see at a glance whether the patient is inside the population the evidence covers.

Report the rule-in combination as present or absent, with its components — never as "likely UTI".

Men, older adults and children are outside this evidence and should not have the combination reported against them as though it applied.

Recurrence after treatment routes to the haematuria row where there has been visible blood, because persisting or recurring haematuria after a treated infection is itself a referral criterion there.
Vomiting: a routing row, and the first place the voice channel itself is the limitation. There is no anchoring instrument here, and the paediatric emergency literature is candid that [evidence to guide diagnosis is limited], with history doing most of the work. The row's job is to recognise which other row the patient belongs in, fast.
Colour is the critical field, and it is the one voice handles worst. Bilious vomiting in an infant [always warrants emergent evaluation to exclude bowel obstruction], because malrotation with volvulus [can lead to devastating intestinal infarction]. But caregivers may describe bile as [green or bright yellow], and in clinic it can help to have the family [identify the colour using a colour card]. A voice agent has no colour card. "Yellow" is genuinely ambiguous — it covers both bile and ordinary stomach contents — and a telephone interview cannot resolve it.
Rules for this field:

Record the carer's colour words verbatim, never a normalised category. "Bright yellow, like highlighter" and "yellowish" are different findings.

Green in an infant is immediate tier. Yellow in an infant is not resolved by further questioning and should escalate rather than be talked down.

Reassuring accompaniments do not reassure. In neonatal malrotation, [abdominal distension is often absent, and infants will typically have passed meconium]. About [30% present in days three to seven of life and half by one month] — well past the newborn check.

Open design question: whether the GP version could send the carer a colour reference by SMS during the call. This is a proposal, not an evidenced intervention, and would need its own validation — but it is the one place in the document where a non-voice adjunct would close a gap the voice channel cannot.
Distinguish vomiting from its lookalikes first. Effortless regurgitation and non-forceful rumination are [different entities from vomiting], and parents use the words interchangeably. Ask what happens, not what they call it.
Routing — each of these hands off to a row that already exists:

Blood → GI bleeding row. [Haematemesis, especially with the first episode], is a red flag in its own right.

Vomiting on waking, lethargy, or a bulging fontanelle → headache and unwell-child rows, for [raised intracranial pressure]. A bulging fontanelle is a carer-performed observation under the delegated-observation rule.

Neck stiffness, photophobia and fever in an older child → unwell-child row; [listed together as a red flag].

Possible early pregnancy → the gating question from the vaginal bleeding row, which this row also needs.

Signs of dehydration → urine output and oral intake, which [should be noted] in every paediatric vomiting interview.
The adult half of this row is thinner in the sources found and is flagged for reviewers rather than extended by inference.
Musculoskeletal, skin and trauma

 | 
Presentation | 
Patient trigger phrasings | 
Framework to ground in | 
Red flags
 | 
Back pain | 
bad back, back's gone, spasm, sciatica, shooting down my leg | 
Symptom field set, not SOCRATES, with spinal red flag screen — negatives do not reassure | 
Bladder or bowel dysfunction; saddle anaesthesia; bilateral leg symptoms; fever; history of cancer; trauma; night pain; age under 20 or over 50 with new pain
 | 
Neck pain | 
stiff neck, crick, neck's locked up | 
Symptom field set; Canadian C-spine history items after trauma; dissection questions without trauma | 
Fever with photophobia; after trauma: age 65 or over, dangerous mechanism, limb tingling; any neurological symptom with new neck pain, including one that has resolved
 | 
Joint pain or swelling | 
sore joint, swollen knee, arthritis flare, can't bend it | 
Single vs multiple joints; inflammatory vs mechanical pattern; duration of morning stiffness | 
Hot swollen single joint — fever not required (absent in 43% of septic joints); prosthesis with skin infection over it; joint surgery or injection within 3 months; inability to weight bear
 | 
Limb pain | 
leg hurts, arm aching, calf pain, dead arm | 
Symptom field set, not SOCRATES; the five Ps are late signs and are not a screening checklist | 
Pain rising despite painkillers after injury, cast, crush or surgery; new tingling or weakness in a painful limb; sudden limb pain with atrial fibrillation; unilateral calf pain and swelling. Pale, pulseless and cold are late signs — never wait for them
 | 
Injury or trauma | 
fell over, twisted it, hit my head, car accident, had a fall | 
Mechanism, timing, immediate function, anticoagulation status | 
Head injury on anticoagulants; loss of consciousness; high-energy mechanism; inability to weight bear
 | 
Falls | 
had a fall, went down, keep falling, legs gave way | 
Mechanism-focused; distinguish mechanical fall from syncope | 
Syncopal mechanism; recurrent falls; head strike; long lie
 | 
Rash | 
rash, spots, come out in a rash, itchy patches, hives | 
Distribution, onset, evolution, itch, new exposures | 
Non-blanching rash with fever; mucosal involvement; rapidly spreading; blistering or skin peeling; associated swelling or breathing difficulty
 | 
Wound or bite | 
cut, gash, bite, animal bite, burn | 
Mechanism, time since, contamination, tetanus status | 
Deep or contaminated; animal or human bite; any bat contact at any time; cut over a knuckle; signs of spreading infection; circumferential burn
 | 
Swelling or lump | 
lump, swelling, bump, found something | 
Site, duration, change in size, pain, systemic symptoms | 
Growing over weeks to months (more concerning than rapid painful growth over days); larger than about 5 cm; recurrence after removal; above the collarbone; associated weight loss or night sweats. Painless is not reassuring
Falls deserve their own row rather than folding into trauma: the critical question is whether it was mechanical or syncopal, and patients rarely volunteer that distinction.
Back pain: red flags are asymmetric, and the handover must say so. This is the opposite case to headache, and the difference matters for how the agent reports.
A [systematic review of 40 observational studies found individual red flags possess limited standalone diagnostic accuracy for serious thoracolumbar pathology and frequently generate high rates of false positives]. More pointedly, a prospective evaluation concluded that [while a positive response to a red flag question may indicate the presence of disease, a negative response to one or two red flag questions does not meaningfully decrease the likelihood of a red flag diagnosis]. The [international framework] states plainly that there is an absence of high-quality evidence for the diagnostic accuracy of most red flags.
For cauda equina specifically, [red flags appear more specific than sensitive, and when present justify prompt diagnostic workup] — but [no single finding or combination is sufficient to exclude it]. Suspicion is warranted with any of: urinary retention or incontinence, faecal retention or incontinence, loss of anal sphincter tone, sexual dysfunction, or saddle hypoesthesia.
Build implications:

Ask the full set, not one or two. The negative-response finding specifically concerns partial screening. Combinations carry more weight than singles — [recent trauma with age over 50 was associated with vertebral fracture].

Never render a negative screen as reassurance in the handover. "No red flags elicited" is a statement about what was asked, not about what is absent. The wording must not let a clinician read absence of positives as evidence of absence of pathology.

Sexual dysfunction and sphincter tone are in the cauda equina set and are among the questions a human clinician is most likely to skip from embarrassment or time pressure. This is a plausible place for an agent to outperform, and worth measuring specifically in the comparative study.
Rash: the agent can delegate the examination, but not trust the result. This row was flagged as likely wrong in the first draft, and the literature bears that out — though not in the expected direction.
The agent cannot see the rash, but it can instruct the glass test, which patients and carers perform routinely: [a glass tumbler pressed firmly against the rash, with a petechial or purpuric rash remaining visible through the glass]. That makes a positive result genuinely available by voice.
A negative result is close to worthless, for three separate reasons:

The rash [often appears late in the illness, so do not wait for it].

Early in the illness the rash [may blanch at first and later develop into a non-blanching rash].

[On dark skin the rash is harder to see], and lighter areas — palms, soles, inside the eyelids, roof of the mouth — need checking specifically. An agent that does not prompt for this will systematically under-detect in darker-skinned patients, compounding the equity problem already noted under abdominal pain.
Build rules for this row:

Instruct the test, record the answer, never score it. The handover reports what the patient or carer observed and where they looked, in their words.

A negative glass test never lowers the escalation tier. Escalation is driven by the illness picture — [if someone is ill and getting worse, get medical help immediately] — not by the rash finding.

Prompt explicitly for the lighter-area check in every patient, not selectively. Making it conditional on the agent's guess about skin tone is both unreliable and inappropriate.

Fever plus petechiae is an immediate interrupt regardless of the glass test result, consistent with [NICE guidance that an unexplained petechial rash with fever warrants urgent assessment].
This row generalises. Wherever the agent delegates an observation to the patient, the positive may be usable and the negative usually is not — and the handover must record who made the observation, not just what it was.
Neck pain after trauma: the agent can identify who needs imaging, and cannot clear anyone. The Canadian C-spine rule is a three-step algorithm, and its first step is entirely history. Its three high-risk criteria — [age 65 or over, a dangerous mechanism, or paraesthesia in the extremities] — each independently mandate imaging. A voice agent can establish all three. Head to head, the rule outperformed NEXUS, with [sensitivity 99.4% against 90.7% and specificity 45.1% against 36.8%].
The later steps are a different matter. Step two uses low-risk criteria that mix history with examination, and step three is [active neck rotation] — a manoeuvre performed only once a clinician has established a low-risk factor. For both rules [a negative test was the more informative result], but a negative requires the examination steps. So the asymmetry is structural: the agent can complete the part that rules patients in for imaging, and none of the part that rules them out.
Build rules:

The agent never asks the patient to move their neck to test it. Rotation is the last step of the algorithm for a reason, and asking a patient on the phone to "turn your head and see if it hurts" performs step three without steps one and two. This is the first prohibited delegated observation in the document and should be added to the delegated-observations section as a named exclusion.

Ask mechanism concretely. Dangerous mechanism is defined operationally — [a fall from more than one metre or five stairs, axial load to the head, high-speed collision, rollover or ejection, motorised recreational vehicle, or a bicycle collision]. "How far did you fall?" in metres or stairs, not "was it a bad fall?".

Paraesthesia is asked for every limb separately and at any time since the injury, including symptoms that have since resolved — the same resolved-symptoms principle as the stroke cluster.

Capture the rule's exclusions as history. It applies only to [stable patients over 16, injured within 48 hours, with no known vertebral disease and no penetrating trauma]. Known cervical disease — [prior surgery, ankylosing spondylitis, rheumatoid arthritis] — takes the patient outside the rule entirely, and the handover must say so rather than reporting criteria against it.

Any high-risk criterion on the GP booking call is immediate tier. The patient should not be booked into a routine appointment and should not be told to come in by their own means; the wording of that instruction needs emergency medicine review.
Non-traumatic neck pain is not covered by this evidence, and the sources found for this pass do not support a separate framework for it. Flagged as a gap rather than extended by inference.
Neck pain without significant trauma (partly closes the gap above): the dangerous diagnosis looks musculoskeletal. Cervical artery dissection causes [up to 25% of strokes in young patients], and its early symptoms — neck pain and headache — [may mimic migraine or a musculoskeletal presentation before clear neurological signs arise, days or even weeks later]. Stroke symptoms occur in about two-thirds and [may be delayed, fluctuating, or completely resolved by the time the patient presents]. The concern named in the literature is exactly the one a booking agent could either cause or prevent: patients [presenting for inappropriate musculoskeletal treatment of their neck, or being discharged prematurely].
What the history can contribute. [Up to 80% of dissections are preceded by trauma to the head or neck], often minor — dissection has been associated with [chiropractic manipulation, weight lifting, roller coasters and wrestling]. Whether manipulation causes dissection is genuinely unsettled: [it is unknown whether dissections after manipulation were caused by it, or by prior minor trauma that brought the patient to the chiropractor]. Either way, the question is relevant, and one review suggested [44.8% of adverse events after cervical manipulation could have been prevented had red flags been ruled out].
Why this row is only partly grounded. There are [currently no clear diagnostic criteria for dissection, and red flags for neck pain and headache are not always clearly described]; a primary care decision tool is in development but not yet validated. The rules below are the best available synthesis, not an evidenced instrument, and should be reviewed by neurology and emergency medicine.
Build rules:

Any neurological symptom with new neck pain — including one that has fully resolved — routes to the stroke cluster at the immediate tier. Dizziness, visual disturbance, speech change, numbness, weakness, unsteadiness. This is the stroke cluster's resolved-symptoms rule applied to a younger population that may not think of stroke.

Ask about minor trauma by activity, not by the word "injury". Patients do not describe a gym session, a roller coaster or a neck manipulation as trauma. Ask specifically about neck manipulation, heavy lifting, contact sport, fairground rides and sudden neck movement in the past few weeks, and record the answers with dates.

New neck pain with new headache after any such event is same-day in person, proposed rather than evidenced. The handover should state explicitly that dissection has not been excluded, because the natural next step for a patient with neck pain is often manipulation.

Ask whether this pain is different from their usual neck pain. Dissection has presented in patients returning for [what seemed like a familiar episode]. This mirrors the pattern-change item in the headache row.

Fever with neck stiffness routes to the fever and sepsis row. Other non-traumatic neck red flags — cord compression, infection, malignancy — are not grounded in this pass. Until they are, the back pain row's red flag set is the nearest analogue, applied with its asymmetry: positives escalate, negatives do not reassure.
Falls in older adults: a validated stratification the agent can complete entirely from history. The first-draft note above — that the critical question is mechanical versus syncopal — is confirmed by the evidence. The 2022 World Falls Guidelines go further, defining a high-risk group whose every criterion is historical. An older adult who has fallen is high risk if any of the following apply: [an injury requiring medical treatment, two or more falls in the previous 12 months, known frailty, lying on the floor unable to rise independently for at least an hour, or suspected transient loss of consciousness]. High-risk adults should be offered a multifactorial assessment, and [suspicion of a syncopal fall should trigger syncope evaluation].
The guidelines also specify what the history should contain: [details of the event and its consequences, previous falls, transient loss of consciousness or dizziness, pre-existing mobility impairment, and concerns about falling that limit usual activities]. That is close to a ready-made question set.
Negatives do not reassure — this is the back pain pattern. In validation across eight cohorts, the high-risk classification showed [good specificity but sensitivity of only 26.5% to 52.3%] for future falls. The single screening question has its own gap: sensitivity of "have you fallen in the past 12 months" [rises from 43% in those aged 65 to 74 to 67% in those over 85]. A patient who reports no previous falls, particularly a younger-old patient, has not been shown to be low risk.
Build rules:

The syncope fork comes first. Any suggestion of loss of consciousness, a gap in memory for the fall, or prodromal symptoms routes to the syncope row, including its exertional and family-history questions. Patients describe syncopal falls as trips because they do not remember the moment of falling.

Ask about the long lie by duration. "How long were you on the floor?" as a time, not "could you get up?". An hour is the threshold, and patients who got up eventually often answer the second question yes.

Anticoagulants and head strike are asked in every fall. Medication history is verified by name, under the stroke-cluster rule against inferring drug classes. A head strike routes to the trauma and head injury row, whose rules — including the anticoagulant override — now govern.

Gait and balance cannot be assessed by voice. Gait speed is the recommended stratification measure, with Timed Up and Go as an alternative — [both physical tests]. The agent does not attempt them and must not ask the patient to walk while on the call.

Ask the three key screening questions — worried about falling, unsteady when standing or walking, fallen in the past year — [a yes to any is a positive screen]. Record each answer separately.

Sensory impairment is asked, not assumed. Hearing loss, vision loss and dizziness are [associated with falls], and hearing loss is also a bail-out criterion for this agent. A patient who struggles to hear the agent is itself a data point for this row, and the handover should record it.
Trauma and head injury: one history field can decide imaging on its own, and it is the field the prior art got wrong. This closes the gap flagged in the falls row.
The Canadian CT Head Rule has [five high-risk and two medium-risk factors]. Four of the seven are history:

 | 
Criterion | 
Tier | 
Recoverable by voice?
 | 
GCS below 15 at two hours | 
High | 
No — examination
 | 
Suspected open or depressed skull fracture | 
High | 
No — examination
 | 
Signs of basal skull fracture | 
High | 
Partly — delegated observation only
 | 
Vomiting, two or more episodes | 
High | 
Yes
 | 
Age 65 or over | 
High | 
Yes
 | 
Amnesia before impact of more than 30 minutes | 
Medium | 
Partly — needs a witness
 | 
Dangerous mechanism | 
Medium | 
Yes
The high-risk factors were [100% sensitive for injuries needing neurosurgical intervention] in the original validation, and the combined high- and medium-risk set [98.4% sensitive for clinically important brain injury]. As with C-spine, the historical items can rule patients in; ruling out requires the examination items.
Anticoagulant status overrides the rule entirely. The Canadian rule [excludes patients on oral anticoagulants or with bleeding disorders] — it simply does not apply to them. NICE goes further and recommends [CT within 8 hours for any anticoagulated patient with a head injury, even without other criteria]. So for this presentation, one medication question can determine imaging on its own. The voice agent in the stroke cluster's prior art [hallucinated an anticoagulant from an unrelated medication mention]. In a head injury interview, the same error sends a patient to CT unnecessarily; the opposite error — a missed anticoagulant — sends a patient home who should have been scanned. This is the highest-consequence single field in the trauma group, and the evaluation should test both error directions specifically.
Antiplatelets are asked separately and by name. Rules treat them differently from anticoagulants and from each other: the Canadian rule [does not account for antiplatelet agents], while recent NICE guidance for medium-risk patients [includes antiplatelet regimes but excludes aspirin monotherapy]. "Any blood thinners?" does not produce a usable answer; the agent asks for each drug by name.
Build rules:

Amnesia is asked as two anchors, not a duration. "What is the last thing you remember before the injury, and the first thing after?" A patient cannot directly report how long they have forgotten, and [retrograde amnesia refers to events before the injury], which patients easily confuse with memory loss afterwards. Where a witness is available, their account goes in the separate collateral interview.

Count the vomits. Two or more is a high-risk criterion, and "I was sick" does not tell you whether it was once or twice.

Establish that trauma was the primary event. The rule excludes patients where [a primary seizure or syncope preceded the injury]. This routes to the seizure and syncope rows, and is the same fork the falls row starts with.

Clear fluid from the nose or ear and bruising around the eyes or behind the ear are basal skull fracture signs that a patient or carer may see. They are delegated observations under the cross-cutting rule: a positive is usable and escalates; a negative is uninformative.

Dangerous mechanism uses the same operational questions as the neck row — pedestrian struck, ejection, a [fall from more than 3 feet or five stairs] — and should be asked once to populate both.

Anticoagulated head injury on the GP booking call is not a routine appointment. Whether it is same-day or immediate depends on the jurisdictional rule adopted, which makes this another configurable parameter rather than question-set content — alongside the haematuria and bowel habit thresholds.
Major trauma, penetrating injury and multi-system trauma are outside this agent's scope and should trigger the immediate tier on disclosure, without further questioning.
Joint pain and swelling: history can raise suspicion of a septic joint, and cannot lower it. Among emergency patients with a single acutely painful joint, the prevalence of non-gonococcal septic arthritis is [approximately 27%] — high enough that the joint gets aspirated on clinical grounds regardless of what the history shows. The agent's job is to make sure the few history features that genuinely move probability are captured precisely.
Only three historical factors have a likelihood ratio above 3:

 | 
Feature | 
LR+
 | 
Prosthetic joint with overlying skin infection | 
[15]
 | 
Joint surgery within the preceding 3 months | 
[6.9]
 | 
Age over 80 | 
[3.5]
Negatives do not reassure. The absence of risk factors [does not significantly reduce the probability of septic arthritis, with negative likelihood ratios of 0.64 to 0.93]. This is the back pain pattern.
Fever is the negative most likely to be misread. Joint pain and a history of swelling are present in [85% and 78% of cases, but fever in only 57%]. Patients and clinicians both expect an infected joint to come with a temperature. The handover must never let "no fever" read as evidence against infection, and the summary-phrase prohibition in the negatives section applies here specifically.
Build rules:

Ask about skin over a joint replacement as its own question. The strongest predictor in this row is a combination the patient will not connect: a hip or knee prosthesis and a skin infection, sore or cellulitis over it. Ask whether they have a joint replacement, and if so, separately whether there is any redness, wound or infection on the skin near it.

Ask for the date of any joint procedure, not whether there was one. Surgery within three months is the threshold, and an absolute date lets the clinician compute it — the same clock-time principle as torsion and stroke. Include joint injections and aspirations: in one series [42% of adult cases were iatrogenic], from arthrocentesis, open surgery and arthroscopy.

Immunosuppression is asked by drug name. Risk factors include [diabetes, rheumatoid arthritis and immunosuppressive medication], and patients on biologic therapy may not describe it as immunosuppression.

One joint or several. The evidence above concerns [peripheral, monoarticular arthritis]. Polyarticular presentations follow a different pathway and should be recorded as such.

Sexual history is relevant here because [gonococcal septic arthritis] is a distinct entity. As with the sphincter questions in back pain, this is a question clinicians skip and an agent asks consistently — but its wording, and whether it belongs in the GP version at all, needs reviewer input.
Crystal arthritis, osteoarthritis and inflammatory arthritis are the common alternatives, but the history cannot separate them from sepsis reliably enough to change the pathway. The row is built around not missing the septic joint, not around diagnosing the others.
Limb pain: the textbook checklist is the wrong tool, for the same reason as dizziness. Two time-critical diagnoses sit inside this row — acute compartment syndrome and acute limb ischaemia — and both are taught through the five or six Ps: pain, pallor, pulselessness, paraesthesia, paralysis, and coldness. For compartment syndrome, the Ps are [not clinically reliable and may manifest only in the late stages, by which time extensive and irreversible damage may have occurred]. Pulselessness, paraesthesia and complete paralysis are [late-stage findings], and in the upper limb [pulses and capillary refill remain normal in most cases].
An agent that works through the Ps as a checklist would collect mostly late signs, and most of them would come back negative in an early, salvageable case. That is the worst possible pattern: a structured screen that systematically produces false reassurance. This is the third row, after dizziness and the field-set analysis, where the mnemonic taught to students turns out to be the wrong instrument for the agent.
Compartment syndrome — the early signal is the trajectory of pain. The classic early feature is [pain out of proportion to the injury, often requiring increasing doses of strong opiates], frequently described as [burning, deep and aching, with a tense feeling in the limb]. Pain is subjective and [has poor sensitivity], but it is the only early feature a patient can report, and its direction over time is more informative than its level. Damage may become [irreversible within six hours]; paraesthesia may appear [after about two hours of ischaemia and indicates irreversible muscle damage will soon follow].
Acute limb ischaemia — the history is the embolic source. Embolic ischaemia has [sudden onset, severe symptoms and normal pulses in the other limb], and the history should cover embolic sources such as atrial fibrillation, peripheral arterial disease and smoking. Symptoms must have appeared [within the last 14 days] to be classed as acute.
Build rules:

Ask about the trajectory of pain, not its severity. "Is it getting worse despite painkillers? Have you needed more, or stronger ones, since it started?" Record the answers against clock times, as with torsion and stroke.

Ask about context before symptoms. A recent fracture, a cast or tight bandage, a crush injury, a burn, a drip site, or recent vascular surgery each raise the prior probability of compartment syndrome, and constricting casts and dressings are [the first thing treated]. The agent does not advise removing a cast or dressing — that is a clinical instruction — but whether it should ever say so on the GP booking call is an open question for emergency and orthopaedic review.

Coldness and pallor are late delegated observations, and negatives are actively misleading. A patient reporting a warm, normal-coloured limb has told you nothing reassuring about compartment syndrome. The handover must not record them as reassuring findings.

Paraesthesia or weakness in a painful limb is immediate tier, because by the time it appears the window may already be closing.

Atrial fibrillation is asked here and populates the palpitations row. Sudden limb pain in a patient with known AF is an embolic question until proven otherwise.
The row is built around the two diagnoses that cannot wait. Ordinary musculoskeletal limb pain, and chronic claudication, need their own treatment in a later pass.
Claudication (closes part of the gap above): a self-administered questionnaire exists, and it is a cautionary tale. The Edinburgh Claudication Questionnaire is a six-item patient questionnaire that originally showed [91% sensitivity and 99% specificity against a primary care physician's diagnosis]. Later studies have not reproduced this. In general practice it had [sensitivity of 52.5% and specificity of 87.1%, positive LR 4.06 and negative LR 0.55]; in a vascular cohort, [sensitivity of 46.8% and accuracy of 53%], leading the authors to conclude that [questionnaires are inadequate substitutes for ankle-brachial pressure assessment]. A positive answer is informative; a negative one is not — the back pain pattern.
The finding that matters beyond this row. When the questionnaire was [completed with a trained interviewer rather than self-administered, the rate of positive diagnoses was sevenfold higher], and whether that assistance improves or worsens accuracy is unknown. A voice agent asking the questions aloud is closer to an interviewer than to a paper form. So a questionnaire validated for self-administration cannot be assumed to behave the same way when the agent administers it. This qualifies the proposed refinement of the assembly rule in the cross-cutting section.
Two further findings are relevant to the agent's design:

One item degraded the whole instrument. Omitting the question ["does this pain ever begin when you are sitting or standing?" improved performance substantially], transforming the tool from useless to potentially useful in that cohort. Item-level wording matters, and faithful administration of a validated instrument does not guarantee each item is doing useful work.

Translation does not automatically preserve validity. Translated versions in [Punjabi and Bengali performed variably in small samples], though literacy made no significant difference. The multilingual design should assume each translated instrument needs its own validation.
Build rules:

Ask the claudication questions as history, and do not score them. Pain in the calf or leg on walking, whether it eases within about ten minutes of stopping, whether it comes on faster uphill or when hurrying, and how far the patient can walk before it starts, as a distance.

Report positives with the patient's words; never report a negative as excluding arterial disease.

Smoking and diabetes travel with this row. The questionnaire [performed better in male current smokers] and [in patients with diabetes].

Pain at rest, especially at night, or a wound on the foot that will not heal, is outside this evidence and indicates more advanced ischaemia. It is not grounded in this pass; until it is, it should be same-day in person, and it is flagged for vascular review.
Ordinary musculoskeletal limb pain has no anchoring instrument in the sources found. It is handled by the standard field set and symptom saturation, with the red flags from the limb pain, joint, lumps and back pain rows applied as the nearest analogues. This is recorded as a deliberate choice rather than an omission.
Wounds and bites: the dangerous question is what the patient was exposed to, not how the wound looks. For an Australian deployment, the highest-stakes item in this row is bat contact. Australian bat lyssavirus infection is [rare but fatal, with no proven effective therapy], and it has caused [three known human deaths in Australia since 1996]. It is preventable by post-exposure prophylaxis, and [all Australian bats — flying foxes and microbats — should be considered to be carrying it unless proven otherwise].
This is the torsion rule inverted: elapsed time never de-escalates, in either direction. Any bat-related injury should be reported [no matter how small the injury or how long ago it occurred], and prophylaxis should be offered for [any history, no matter how distant]. A patient mentioning in passing that they were scratched by a bat last year, while calling about something else, has disclosed a finding that needs action. That makes this a question for the standard closing sections, not only for this row.
Negatives are uninformative, and "were you bitten?" is the wrong question. Some bats have [small teeth and claws, so bites or scratches may not be apparent], and direct contact with a bat is itself classed as a [category III severe exposure]. The guidance explicitly covers people who cannot report an exposure — [a child, an intoxicated person, a person with a developmental disability, or someone who has been sleeping in a confined space with a bat present]. The agent asks whether the patient touched or handled a bat, or whether a bat was in a room where they or their child slept — not only whether they were bitten.
Overseas exposures widen the question to any mammal. The exposure definition includes [any bat in Australia or overseas, and any wild or domestic mammal in a rabies-enzootic country]. Country of exposure is a required field, and a dog bite abroad is a different finding from a dog bite in Adelaide.
Build rules:

Capture the exposure categories as history: the nature of the exposure — [bite, scratch, or mucous membrane contact] — its location, with head and neck and highly innervated areas such as fingers recorded specifically, the animal, the country, and the date.

Any bat contact is same-day, and should reach a clinician who can notify public health. Clinicians receiving reports of bat bites or scratches [are required to notify public health], and advice is to seek care [preferably on the same day or early the next]. That source is a Queensland public health unit; the South Australian notification pathway should be confirmed by reviewers. The GP booking call must not book this into a routine appointment.

Whether the agent should advise first aid or keeping the bat is an open question. Guidance recommends [washing the wound for at least 15 minutes with soap and water], and, if safe, keeping the bat for testing, since a result within 48 hours can avoid prophylaxis. Both are public-health instructions rather than clinical advice, and both are time-sensitive; whether the agent may give them is a governance decision for public health and emergency medicine reviewers, not something to default either way.

Tetanus status and immune status are asked in every wound interview. Both [feed the public health assessment] as well as ordinary wound management.
Gaps. Human bites and clenched-fist injuries — where patients may conceal the mechanism — and wound infection risk stratification are not grounded in this pass and are flagged for reviewers rather than extended by inference.
Clenched-fist injuries and human bites (closes the first gap above): key the question on location, because the mechanism is often concealed. A fight bite happens when a closed fist strikes teeth, and it [tends to involve the metacarpophalangeal joint region] — typically [a small laceration over the third and fourth knuckles of the dominant hand] that looks innocuous. Diagnosis is complicated because [patients are often reluctant to admit how the injury happened]; some are [embarrassed about the mechanism or fear legal repercussions], and a [misleading history] is named as a direct contributor to inadequate assessment. The injury [can easily be missed without an investigative history and a high index of suspicion].
The stakes are time-dependent. Infection follows in [10% to 50% of fight bites], and destruction of cartilage and bone can begin [as early as 12 hours after injury]. Patients presenting [more than 18 hours after injury are more likely to show infection]. Many [ignore the wound until it becomes painful] — often waking days later with a throbbing, swollen hand, which is exactly the call a GP booking agent will receive.
Build rules:

A cut or puncture over a knuckle is treated as a possible fight bite regardless of the story. The agent asks where the wound is, and if it is over a knuckle, asks neutrally whether the hand made contact with anyone's mouth or teeth — without asking who, why, or what happened. The row does not depend on the patient volunteering a fight.

Ask about knuckle wounds in every hand injury after a punch or fall on a closed fist. In apparent fractures, clinicians are advised to [ask whether the patient noticed a laceration or bleeding around the knuckle at the time].

Record time of injury as a clock time. The 12- and 18-hour points make the absolute-time rule apply here too.

Any suspected fight bite is same-day in person. Pain, swelling, redness, discharge or fever route additionally to the joint row, and fever to the sepsis row. Pain out of proportion [should raise concern for bone involvement].

Diabetes is asked, as it was associated with [an odds ratio of 2.6 for][ needing multiple debridements] in one series.

The agent does not promise confidentiality. Patients who fear legal consequences may ask whether the call is recorded or reported. The agent must answer truthfully under whatever the deployment's governance says, and must not offer reassurance it cannot guarantee. What it says in that moment is a governance decision, and this row is the clearest instance of the stigmatised-disclosure question in the recurring-principles section: the verbatim transcript that makes the agent safe may also be what makes some patients withhold.
Lumps: change over time is the best single predictor, and it is pure history. For soft tissue masses, the standard red flags are a lump [larger than 5 cm, growing, deep, or painful], plus recurrence after previous excision; lumps meeting these criteria are treated as malignant until proven otherwise because [86% of tumours meeting them are malignant]. Of these, [increasing size is the best individual indicator of malignancy].

 | 
Red flag | 
Recoverable by voice?
 | 
Increasing in size | 
Yes — the patient's own observation over time
 | 
Recurrence after previous excision | 
Yes
 | 
New-onset pain | 
Yes
 | 
Larger than 5 cm | 
Partly — patient estimate only
 | 
Deep to the fascia | 
No — examination
 | 
Firmer than surrounding tissue | 
No — examination
Pain is the red flag most likely to mislead. The common presentation of soft tissue sarcoma is [a painless, gradually enlarging mass], and [the belief that only painful masses are worrisome is wrong]. Counter-intuitively, a mass [growing slowly over weeks to months, painful or not, should raise more concern than a painful mass growing rapidly over days]. A patient who says "it doesn't hurt, so I left it" is describing the typical sarcoma history, and the handover must never record painlessness as reassuring. This is the dysphagia pattern again: the feature patients read as benign is the one that should worry.
Delay is the documented harm. In the UK it takes [an average of 92 weeks from a patient noticing symptoms to referral and investigation], and [lesion size at diagnosis tracks almost linearly with poorer prognosis]. An agent that asks every patient with a lump about growth, and records the answer against a date, directly targets that delay.
Build rules:

Ask about growth with anchors. "When did you first notice it? Has it changed size since? Compared with what?" Record when it was first noticed as a date, and the patient's own comparison — the same trajectory principle as limb pain.

Size is a patient estimate and is recorded as one, with the comparator the patient used, under the same rule as haemoptysis volume. A golf ball is often used as a reference for about 5 cm, but the agent records the patient's own words and never converts them to a measurement.

Size alone should not drive the handover's emphasis. In one series [99.8% of low-risk lesions under 5 cm were benign], yet the authors conclude [size alone should not be the sole indicator] for escalation, and referral to specialist centres on size alone [can overuse limited resources]. Report all the features together.

Ask about previous removal. Recurrence after excision is a named red flag, and patients rarely mention a procedure from years earlier unless asked.

Imaging pathway is a configurable parameter. UK guidance uses [ultrasound as the initial triaging tool, while 2021 European guidance still recommends MRI] — another jurisdictional choice for SA Health rather than question-set content.
Routing. A breast lump is one of [eight features with a positive predictive value of 5% or more for cancer in specific primary care groups] and needs its own pathway. Testicular lumps route to the GU section, and lymphadenopathy to the constitutional rows. None of these three is grounded in this pass.
Breast, testicular and nodal lumps (closes the routing gap above).
Breast lump: the lump is the finding, and age sets its weight. In primary care, a breast lump carried an [odds ratio of 110 for breast cancer, with PPV rising from 4.8% at age 40–49 to 48% over 70]; in a recent cohort the risk when consulting for a lump was [8.96%]. [Nipple retraction and nipple discharge] are also significant, and women [may delay presenting for over a year].
Isolated breast pain is the rare genuinely reassuring negative — and over-investigated. In one cohort there were [no cancers among 588 episodes of isolated breast pain, yet 39.6% of those women underwent imaging]. The authors conclude imaging [may often be safely deferred for short-duration isolated breast pain], while pain [combined with other breast symptoms may indicate higher risk]. This row therefore joins the headache row as one where a clean negative carries real information — but only if the agent has established that the pain is truly isolated. The handover should state "breast pain, no lump, no nipple or skin change reported" as three separate answers, never "breast pain only".
Testicular lump: the misdiagnosis is the documented harm. Testicular cancer is the [most common solid malignancy in young men, peaking between 20 and 40]. It typically presents as a painless mass, but [nearly one third of patients are initially misdiagnosed with epididymitis, orchitis or hydrocele], and [painful swelling does not exclude malignancy]. About [20% have metastatic disease at diagnosis and may present with back or abdominal pain, malaise or lethargy]. Young men with a GI bleed from metastasis [may not volunteer testicular swelling even when present].
Lymph nodes: most are benign, and the history can find the ones that are not. Only [1.1% of unexplained lymphadenopathy in primary care is malignant, rising to about 4% at age 40 and over against 0.4% below]. Supraclavicular nodes are the exception, with a [34–86% risk of malignancy, especially over 40]. Risk factors include [duration beyond four to six weeks, a node not back to baseline after eight to 12 weeks, generalised nodes in two or more regions, and fever, night sweats or weight loss] — all history. For neck nodes, suspicion rises in people [over 40 who drink or smoke, with sore throat, difficulty swallowing, recent hearing loss or voice change].
Build rules:

Breast: ask separately about a lump, nipple change or discharge, and skin change, and record each. A lump in any woman routes to referral regardless of the presence of pain; [PPVs were lower when pain accompanied a lump], but that is not a reason to deprioritise it. Breast symptoms in men are not grounded in these sources and are flagged for reviewers.

Testicular: a new testicular lump or swelling in a young man is flagged even if painful, and the handover must note if a previous diagnosis of epididymitis or orchitis has not resolved after treatment. Sudden severe testicular pain remains the torsion row's immediate trigger and takes precedence.

Ask young men about testicular changes in the back pain, abdominal pain and GI bleeding interviews. This is the metastatic presentation, and the one patients do not connect.

Nodes: ask location in the patient's own words, and treat "above my collarbone" as the high-risk site. Location is a delegated observation, but for this site a positive is highly informative. Ask duration as a date, whether it is getting bigger, and whether there are lumps elsewhere; route night sweats, fever and weight loss to the constitutional rows.

Neck lump over 40: add the head-and-neck questions above — alcohol, smoking, sore throat, swallowing, hearing and voice.

Size, hardness and fixation are examination findings. The agent records patient estimates under the lumps rule and never converts them.
Constitutional, mental health, paediatric and obstetric

 | 
Presentation | 
Patient trigger phrasings | 
Framework to ground in | 
Red flags
 | 
Fever | 
temperature, burning up, shivers, chills, sweats | 
Duration, pattern, travel, exposures, immune status | 
Rigors; immunosuppression; recent travel; non-blanching rash; confusion; no source identified
 | 
Fatigue | 
tired all the time, no energy, worn out, exhausted | 
Duration, sleep, functional impact, associated symptoms | 
Weight loss; night sweats; breathlessness on exertion
 | 
Weight loss | 
losing weight, clothes are loose, dropped weight | 
Intentional vs not, quantum, timeframe, appetite | 
Unintentional and significant; associated night sweats, lumps, bleeding
 | 
Feeling generally unwell | 
just not right, feel terrible, something's wrong | 
Pure open phase; no framework fits — saturation rule does the work | 
Any red flag surfacing from the open phase; patient or carer conviction that something is seriously wrong
 | 
Mental health presentation | 
anxious, low, can't cope, panicking, not myself | 
Its own section — Columbia Protocol administered faithfully | 
Direct risk questions are asked in both settings; any positive escalates per the mental health section. The agent administers and escalates; it does not judge
 | 
Alcohol or substance concern | 
drinking too much, using, withdrawal, shakes | 
Quantity, pattern, last use, withdrawal history | 
Seizure, hallucinations or new confusion after stopping — immediate; past complicated withdrawal — same-day in person; intoxication at the time of the call — bail out
 | 
Unwell child | 
not feeding, floppy, crying differently, hot, rash | 
Carer-reported throughout; feeding, output, activity, behaviour | 
Reduced feeding or wet nappies; drowsiness; non-blanching rash; carer concern; any infant under three months with fever
 | 
Pregnancy-related | 
pregnant and, bleeding, contractions, baby not moving | 
Gestation, parity, antenatal care, fetal movements | 
Reduced fetal movements; bleeding; severe headache or visual change; abdominal pain
Two rows need explicit design decisions rather than question sets. Mental health presentations and intoxication are both bail-out categories under the cross-cutting rules — risk assessment does not belong to the agent. The "feeling generally unwell" row is the purest test of the saturation rule, since there is no anchoring symptom to branch from.
The unwell child: the carer holds information the examination cannot recover. This is the presentation where an agent has the clearest structural advantage, for two reasons.
First, resolved features. NICE directs clinicians to [ask parents or carers about the presence of these features since the onset of fever, because they may have resolved by the time of assessment]. A clinician examining the child sees a snapshot; the carer holds the trajectory. An unhurried structured interview is well suited to recovering it, and this is a concrete, checkable thing to measure in the comparative study.
Second, carer concern as data. A [literature review on parental concerns in paediatric sepsis] notes that root cause analyses after fatal sepsis outcomes often report recurrent presentations to hospital, and that parents in such cases often indicated concerns that "this disease is different" — suggesting they sensed severity before clinicians recognised it. The same review observes that the potential value of including parental assessment in discriminating mild infection from sepsis has received little attention. The agent should ask directly whether this illness seems different from previous ones, and carry the answer into the handover in the carer's own words.

 | 
Element | 
Handling
 | 
Features since onset of fever, now resolved | 
Asked explicitly and reported as historical, not current
 | 
"Is this different from previous illnesses?" | 
Asked directly; verbatim answer in handover
 | 
Age and temperature thresholds | 
[Under 3 months with temperature ≥38°C is red; 3–6 months with ≥39°C is amber]
 | 
Non-blanching rash | 
Immediate escalation; [consider meningococcal disease, especially with purpura, prolonged capillary refill or neck stiffness]
 | 
Recent travel abroad | 
[Asked routinely in feverish illness]
 | 
Feeding, wet nappies, responsiveness, breathing | 
Core carer-reported fields
One caution on thresholds. The NICE red features were [validated across 6,260 acutely ill children in seven primary care and ED settings], but specificity is a live problem: [50% of children aged 1–2 years triggered the NICE red high-risk criteria on tachycardia alone]. Since tachycardia is a vital sign rather than a history item, the agent's flag rate will differ from a clinician's, and the escalation threshold for the paediatric pathway needs setting deliberately rather than inherited from the adult one.
Reduced fetal movements: history alone is not a safe endpoint. This is the clearest case in the document where the agent's output cannot stand on its own, and it has a specific consequence for the GP version.
The [Green-top Guideline No. 57] directs that when a woman presents with reduced fetal movements between 24+0 and 28+0 weeks, the presence of a fetal heartbeat should be confirmed by auscultation with a handheld Doppler and a history taken to determine other risk factors. The history is half of a two-part assessment, and the other half is an immediate physical check the agent cannot perform or defer.
Maternal perception is itself imperfect but meaningful: maternally perceived movements account for [around 30.8% of all movements compared with 31.4–57.2% detected by ultrasound], and [maternal perception of decreased movement is associated with a modest increase in odds of late stillbirth]. Perception is also affected by [advanced maternal age, high BMI, primiparity, anterior placenta, fetal growth restriction and small for gestational age] — all history fields the agent should capture, since they change how the report is read.

 | 
Setting | 
Handling
 | 
ED | 
Immediate interrupt to triage, as elsewhere
 | 
GP booking call | 
Not a warm handback. The contact cannot end with an appointment booked for later; escalation must route to same-day in-person assessment, and the wording needs obstetric input.
This is also a useful boundary case for the whole design. Everywhere else, a thorough history arriving early is an unambiguous gain. Here, a history taken without the accompanying Doppler creates a record that looks like an assessment but is not one — which argues for the handover stating explicitly what could not be assessed, in this row above all.
Weight loss: the operative word is "unexpected", and the evidence base has a retraction in it.
A caution for reviewers first. The 2020 BMJ diagnostic accuracy study on unexpected weight loss and cancer in primary care [has been retracted] and replaced by a [2024 update]. Secondary sources and teaching material may still quote the retracted figures. This row cites only the update and independent studies, and anyone adding numbers later should check which version they are quoting.
In the 2024 update, cancer risk after unexpected weight loss was [above the 3% investigation threshold in men aged 50 and over and women aged 60 and over]; of those diagnosed with cancer within six months, [96.3% were aged 50 or over]. In younger adults the risk is [below 3%, but concurrent clinical features change that], and features usually tied to one cancer site [become markers of several cancer types when they occur with unexpected weight loss]. Separately, measured weight loss of 5% or more carried a one-year cancer PPV of [3.41% in men and 3.47% in women aged 60 to 69], with risk rising [linearly with the amount of weight lost].
Australian data exist, and should be preferred. The update has been [replicated in Australian general practice], using [cancer registry data linked to primary care records for 1.8 million patients in Victoria]. Its figures were not retrieved in this pass; reviewers setting SA Health thresholds should work from it rather than the English data. This is the fifth configurable threshold in the document.
Build rules:

Establish "unexpected" explicitly, before anything else. Weight loss is [often missed or misattributed to diurnal fluctuation, ageing, diet or exercise]. The agent asks whether the patient was trying to lose weight, and if they were, whether the amount lost is more than they expected. A patient who has been dieting can still have unexpected weight loss.

Record how the patient knows. The evidence base is largely measured weight. "I've lost 6 kilos on my scales" and "my clothes are looser" are different findings, and self-weighing is a delegated observation under the cross-cutting rule. Record the source alongside the amount.

Capture amount, period and baseline. Percentage loss is arithmetic under the pack-years rule: permitted if the components appear alongside it. The agent does not round a vague answer into a number.

This row feeds every cancer row, and they feed it. Weight loss is asked in the haemoptysis, dysphagia, bowel habit and haematuria interviews, and any of those symptoms is asked here. The handover should present weight loss together with whatever accompanies it, since the combination is where the predictive value sits.

Smoking status travels with this row, as the update stratifies risk by it; pack-years under the existing rule.

Blood tests are out of scope, and the evidence cautions against over-reading them anyway: [no normal blood test result in isolation ruled out cancer]. If a patient reports that recent bloods were normal, that is recorded as the patient's report and not as reassurance.
Alcohol and substance use: the first instruments the agent may be allowed to score. Unlike every other row in this document, the screening instruments here were designed and validated for self-administration. For alcohol, current guidance suggests [single-item screening for most primary care settings, with the AUDIT-C offering additional information useful to treatment]. The AUDIT-C is three items scored 0 to 12, with [more than three points considered positive] in one primary care validation. For drugs, a single screening question is [as well validated as longer questionnaires]:

 | 
Single drug-use question, detecting | 
Sensitivity | 
Specificity | 
LR+ | 
LR−
 | 
Self-reported current use | 
[82.8%] | 
[93.6%] | 
[12.9] | 
[0.2]
 | 
Drug problem or use disorder | 
[87.0%] | 
[92.8%] | 
[12.0] | 
[0.1]
Test characteristics were [affected very little by participant demographic characteristics]. A single past-year cannabis question has also been [validated as a screen for cannabis use disorder].
Why the no-assembly rule may not apply here — a proposal for reviewers. Wells, ROSIER and Sheldon were each excluded from agent scoring for a specific reason: examination items the agent cannot perform, witness items the patient cannot supply, or judgement items that belong to a clinician. None of those applies to the AUDIT-C or the single-item screens. They contain only the patient's own answers, and they were validated in formats with no clinician present. That suggests the cross-cutting rule is better stated as: the agent may score an instrument only if it was validated for self-administration and contains no examination, witness or judgement items. Under that wording, the substance screens qualify and everything else in this document still does not. This is a proposed refinement, not a settled one, and reviewers should decide it explicitly rather than let it happen by default.
Superseded in part. The claudication row later found that interviewer administration changed one questionnaire's positive rate sevenfold. The cross-cutting assembly section now requires validation in a mode equivalent to voice administration, and on that standard it is not established that the substance screens qualify. The single-item drug question, validated in interviewer-administered form, is the strongest candidate.
The research question this row opens. Self-administered formats may elicit [more honest reporting of risky alcohol use than a face-to-face interview], and substance use is a stigmatised disclosure. Validation studies distinguish self-administered from interviewer-administered versions, and self-administered single-item questions [may be less accurate than interviewer-administered ones] — so the direction of the effect is not settled even for paper and tablets. An AI voice agent is neither format: it asks aloud like an interviewer, but there is no person listening. Whether patients disclose more, or less, to it than to a clinician is unknown, and the comparative study is well placed to measure it. The same question applies to the sexual history items in the joint and urinary rows, the sphincter questions in back pain, and the direct risk questions in mental health — this could be a secondary outcome across all of them.
Build rules:

Administer validated wording exactly, under the same principle as the Columbia Protocol in the mental health section.

Localise the unit of a "drink" before deployment. The AUDIT-C asks about drinks per typical day, and the definition of a standard drink varies by country; the Australian definition should be confirmed by reviewers and used consistently.

Positivity thresholds vary by sex and setting. Trials have used [a threshold of 4 or more for both sexes in one setting, and 5 for men and 4 for women in another]. This is another configurable parameter, not question-set content.

A positive screen is information, not a diagnosis. The handover reports the score, the answers behind it, and the instrument name — and never a label such as "alcohol dependence".

Current intoxication remains a bail-out criterion. This row is for patients who can take part; it does not override the cross-cutting rule for patients who cannot.
Withdrawal risk, and patients who call specifically seeking help to stop, are not grounded in this pass and are flagged for addiction medicine review.
Alcohol withdrawal (closes the gap above). Most withdrawal is uncomplicated, but [up to 20% of cases involve seizures or delirium tremens], and withdrawal [usually begins within the first 24 hours after stopping]. Seizures [may develop early, before the autonomic signs that would otherwise warn staff] — which is why prediction from history, before withdrawal starts, matters.
The best predictor is the patient's own past. The [strongest predictor for withdrawal syndromes is a personal or family history of alcohol withdrawal or delirium tremens]. In a Hungarian validation, a history of complicated withdrawal made current complicated withdrawal [almost seven times more likely]. These are history questions, and exactly the kind a patient phoning to say they want to stop drinking will not volunteer unless asked.
A validated tool exists, but not for this setting. The Prediction of Alcohol Withdrawal Severity Scale has [threshold criteria, ten yes/no items from the patient interview, and clinical evidence items including blood alcohol and autonomic signs]. At a cut-off of 4, its prospective validation reported [sensitivity 93.1% and specificity 99.5%], and it is [recommended by the American Society of Addiction Medicine]. But three cautions apply. It was validated in [hospitalised medically ill patients], not community callers. A smaller later evaluation reported [sensitivity of 46% and specificity of 97%] — a student capstone, so low weight, but a reason not to treat the headline figures as settled. And its clinical-evidence items mean the agent cannot assemble it under the cross-cutting rule; unlike the AUDIT-C, it fails the proposed self-administration test.
Build rules:

Capture the time of the last drink as a clock time. Withdrawal starts within about a day of stopping, so "I stopped a couple of days ago" needs converting to a time and confirming, under the same absolute-time principle as torsion and stroke.

Ask directly about past withdrawal, past withdrawal seizures and past delirium tremens — including "have you ever seen or heard things that weren't there when you stopped drinking?" — and about family history of the same. Record each separately.

Any history of complicated withdrawal, in a patient who has stopped or plans to stop, is same-day in person. The agent does not advise the patient whether to keep drinking or stop; that is a clinical instruction and belongs to the clinician the patient is routed to.

Current seizure, hallucinations, or new confusion after stopping is immediate tier, and new confusion routes to the confusion row's collateral interview.

The PAWSS interview items are collected and listed, not scored. Addiction medicine reviewers should decide whether a community-validated alternative exists or whether PAWSS items are the best available anchor despite the setting mismatch.
Fever in adults: the row is really sepsis recognition, and the guideline already anticipates remote history-taking. NICE's sepsis guidance addresses the GP booking scenario directly: during a remote assessment, when deciding whether to offer face-to-face assessment and how urgently, clinicians should identify [factors that increase sepsis risk and new-onset abnormalities of behaviour, circulation or respiration]. That is close to a specification of what the agent's handover should contain.
Many of the risk-stratification criteria are history. For adults, the tool's history criteria include [a history from the patient, friend or relative of new altered behaviour or mental state, acute deterioration of functional ability, impaired immune system including oral steroids, and trauma, surgery or invasive procedures in the last six weeks]. Urine output is also historical: [not passing urine in the previous 18 hours] is a high-risk criterion, and 12 to 18 hours a moderate-to-high one. The guidance separately directs clinicians to ask [how often the person urinated in the past 18 hours], about [recent fever or rigors], and whether the person has [recently presented to a GP or hospital with symptoms that could indicate sepsis].
That last item partly answers a question left open in the bowel habit row: for sepsis at least, repeated presentation is an explicit guideline criterion, not just a design idea.
The guideline names the agent's equity argument. NICE says to assess with extra care people who [cannot give a good history, for example people with English as a second language or people with communication problems], including [learning disabilities or autism]. A history taken in the patient's own language, with the original preserved beneath the English handover, targets one of the groups the guideline itself singles out. This belongs alongside the abdominal pain equity finding as a candidate outcome for the comparative study.
Build rules:

Ask urine output as a count against time. "When did you last pass urine?" as a clock time, then "how many times since yesterday?" — not "are you passing urine normally?". The 12- and 18-hour thresholds need an absolute time, the same principle as torsion and stroke.

Collateral counts explicitly here. The tool accepts altered behaviour reported by a friend or relative. Where one is present, their account goes in the separate collateral interview used by the confusion row, and a new change in behaviour routes to that row.

Ask about recent presentations by date. Has the patient seen anyone about this illness already, and when? Record verbatim.

Immunosuppression is asked by drug name, including oral steroids, under the same rule as the joint row.

Mottled or ashen skin, blue lips and a non-blanching rash are delegated observations when reported by patient or carer. Under the cross-cutting rule a positive is usable and escalates; a negative says nothing about the physiology the agent cannot measure. The rash row's lighter-skin prompts apply to all three.

The agent cannot stratify. Heart rate, blood pressure, respiratory rate and objective mental state are examination findings, and the high-risk tier depends on them. The agent collects the history criteria and routes; it does not assign a sepsis risk category. The paediatric equivalent is the unwell child row.
Fatigue: a routing row for most patients, and a cancer-risk row for older men on its own. Fatigue is the principal complaint in [around one in 15 primary care consultations], and for most patients its value is in what accompanies it. Across 237 conditions studied, those most strongly associated with new-onset fatigue were [depression, respiratory tract infections, insomnia and sleep disturbance, and thyroid disease in women]. Blood tests change management in [only about 5% of patients], which makes the history carry more weight here than in most rows, not less.
The exception is age. In a cohort of 250,606 patients presenting with new-onset fatigue, 12-month cancer risk [exceeded 3% in men aged 65 and over and women aged 80 and over, and 6% in men aged 80 and over], and [nearly half of those cancers were diagnosed within three months]. A later analysis supports [prioritising cancer investigation in men aged 70 and over with fatigue, but not in women at any age, on fatigue alone]. The two studies use different cut-offs, which is one more reason the threshold belongs in configuration, and both are English data.
Build rules:

Establish new-onset versus longstanding, with a date. The cancer-risk evidence concerns new-onset fatigue.

The red flags are all history, and all route elsewhere. Weight loss, persistent fever, night sweats, unexplained bleeding or bruising, chest pain or palpitations, and breathlessness on exertion are listed [red flag features in fatigue]. Each has its own row; this row's job is to ask for them and hand off.

Mood, sleep and substances are part of this interview, not a separate one. Depression and sleep disturbance head the association list, and the recommended history covers [alcohol, drug and medication history, sleep patterns and shift work]. This row routes to the mental health section's PHQ-9 candidate and the substance screens.

Function is the severity measure. Ask what the patient has stopped doing, not how tired they feel on a scale — impact on function is in the recommended history and is more comparable between patients.

Never summarise fatigue as "non-specific" in the handover. In older men it carries a cancer risk above referral thresholds without any other feature, and the word invites exactly the deprioritisation the evidence argues against.
"Feeling generally unwell": there is a pathway but no instrument, and the reason is the justification for this agent's core design.
This row was flagged at the outset as having no anchoring framework. That turns out to be half right. A pathway does exist: Denmark introduced a dedicated cancer pathway for [non-specific symptoms and signs of cancer in 2012], later copied in Norway, Sweden and the UK, because [more than half of patients with cancer present with vague or non-specific symptoms such as unexplained weight loss, fatigue or anaemia]. These pathways find a lot of disease: diagnostic yields of [11% to 21%], exceeding the roughly 8% for English alarm-symptom referrals, and among those diagnosed, [one-year mortality was 44.2%].
But the history instrument that would feed such a pathway does not exist, and the evidence suggests it could not. In referred patients, [no single non-specific symptom was significantly associated with a cancer diagnosis]; [the predictive value of the presenting symptoms was poor, and age and biochemical markers were better predictors]. What those patients did have was breadth: [a median of four symptoms].
So the method for this row is the agent's own method. No single question carries the weight; the constellation does. The design principle adopted at the very start of this project — keep asking open questions until the patient stops producing new symptoms, asking the same thing in different ways — is not a stopgap for this row in the absence of a framework. It is the only approach consistent with the evidence. A structured checklist would underperform here, because what matters is the set of things the patient has noticed, and patients with vague illness are exactly those least likely to volunteer the fourth symptom unprompted. The research finding logged by the agent — which open-question phrasing pulled out the extra symptom — is most valuable in this row.
Build rules:

Separate acute from subacute before anything else. Feeling unwell for two days routes to the fever and sepsis row; feeling unwell for two months routes here. Ask for a start date.

Run symptom saturation fully and report every symptom elicited, with the count. "Four symptoms over three months" is itself the finding.

Weight loss, fatigue and night sweats are asked in every interview in this row, since they dominate referrals to these pathways, and populate their own rows.

The agent does not interpret the constellation. Age and blood tests outperform symptoms as predictors here, and both belong to the clinician.

Whether SA Health has an equivalent non-specific-symptom pathway should be confirmed by reviewers; if it does, the handover should be designed to feed it.
An open question. A patient saying "something is wrong with me, I just don't feel right" may carry information, in the way carer concern did in the unwell-child row and self-diagnosis did in the urinary row. No evidence for that in adults was found in this pass. It is recorded verbatim, attributed, and flagged as a candidate for the comparative study rather than asserted.
Standard closing sections
After the presenting complaint is saturated and drilled, every history collects the same closing set. These run in a fixed order and are not symptom-dependent.

Past medical and surgical history — asked as five retrieval routes rather than one question: self-label, treatment (with each medicine converted to its indication), events, care contacts, and surveillance. Lifetime form only where the past changes management. Full wording, lay-anchored condition sweep and evidence in [Past Medical History — Evidence Base and Question Set].

Medications — prescribed, over-the-counter, supplements; adherence; recent changes. Anticoagulation asked explicitly, since it changes the disposition of several presentations above.

Allergies and adverse reactions — the agent records what happened, not just the drug name, since patients report intolerance as allergy.

Family history — targeted by presentation rather than exhaustive.

Social history — living situation, who is at home, supports, occupation, smoking, alcohol, other substances, driving.

Functional baseline — what the patient could do a week ago compared with now. This is the field clinicians most often find missing and most often need.

Ideas, concerns and expectations — what the patient thinks is going on and what they are worried about. Cheap to ask and disproportionately informative.
The functional baseline and the ICE questions are where an unhurried agent may outperform a time-pressured registrar, and are worth watching as a specific comparison in the study.
Mental health presentations
Mental health is handled as a full questioning section rather than a bail-out, in both settings. The rationale is the same as for chest pain: not asking does not remove the risk, it removes the visibility of it. In the ED the patient is already in a monitored environment; on a GP booking call, the answers are what determine whether the contact needs escalating to reception or the GP at all.
Design constraint: administer, do not judge
The agent administers a validated screener faithfully and escalates on any positive response. It does not rate, score, stratify, or form a clinical impression of risk.
This constraint is not conservatism for its own sake. The [Columbia-Suicide Severity Rating Scale] states in its own documentation that it is intended for use by individuals trained in its administration, that its questions are suggested probes, and that determining the presence of suicidal ideation or behaviour ultimately depends on the judgement of the individual administering the scale. The instrument presumes a human exercising judgement. The agent is not that, so it takes the part of the task that is mechanical — asking the questions in validated wording, recording the answers verbatim — and routes the judgement to a clinician.
Why the Columbia Protocol

 | 
Property | 
Relevance to this build
 | 
Designed to be asked with no mental health training required | 
Matches an agent administering standardised wording
 | 
Shortest screeners run two to six questions depending on responses | 
Fits a voice interview without becoming unwieldy
 | 
Branching is answer-driven, not judgement-driven | 
The branch logic is implementable without inference
 | 
Large validation base across populations and settings | 
Defensible to a human research ethics committee
The [ASQ] is worth considering alongside it: a four-item questionnaire validated in paediatric patients in medical settings, within a three-tiered pathway that starts with a roughly twenty-second screen and steps up to a brief suicide safety assessment. The tiered structure maps well onto the agent-then-human split proposed here.
What the agent collects around the screener
The surrounding psychiatric history follows the settled structure: onset and timeline of symptoms, symptom characterisation including severity and frequency, triggers and psychosocial context, functional impact on work and daily life, prior treatment and response including medications, therapy and previous admissions, and current supports at home.
PHQ-9 and GAD-7 are candidate structured additions for the GP version, where the consultation is planned rather than acute.
Escalation

 | 
Setting | 
On any positive screener response
 | 
ED | 
Immediate interrupt. Alert to triage desk carrying the patient's own words. Interview stops; the patient is not left alone with the agent.
 | 
GP booking call | 
Immediate interrupt. Warm handback to the GP or reception for a call back, not a booked appointment. Decide whether the agent also directs the patient to an urgent service before the call ends.
The agent never reassures and never offers a view on severity. It records, flags, and hands over.
Required before any simulation
This section needs review by a mental health clinician before it is built or tested, covering the exact question wording, the escalation thresholds, what the agent says at the moment of escalation, and what happens in the interval between disclosure and human contact. The failure mode here is not an incomplete history — it is a person who discloses and is not reached in time. That is a different class of risk from every other section in this document, and it should not be signed off on the strength of a good draft.
Red flag master list
Consolidated from the tables above. Each triggers the interrupt: the agent stops the interview, alerts, and passes the patient's own words through. Escalation tiers are a design decision still open — the list below distinguishes immediate interrupt from flag-and-continue.
Rebuilt after the grounding pass. Every trigger below traces to a grounded row, named in the right-hand column; the row is authoritative where the two differ. This list is a summary for reviewers and for the escalation logic, not a substitute for the rows. In particular, the absence of any trigger here is never reassurance — the negatives table governs what a negative screen may be reported as.
Three tiers, not two — a proposal. The original list had Immediate and Flag. Four grounded rows (reduced fetal movements, early pregnancy, bat exposure, anticoagulated head injury) each needed the same exception: not an emergency interrupt, but not safe to book into a routine appointment either. A third tier makes that explicit rather than handling it as repeated exceptions.

Immediate — interrupt the interview. ED version: alert the triage desk carrying the patient's own words. GP version: handling is an open question requiring emergency medicine review of the exact instruction given to the patient.

Same-day in person — the patient must be seen face to face today; never a routine booking and never a warm handback alone. Proposed tier, for governance decision.

Flag — continue the interview and flag prominently in the handover; urgency is set by the configurable parameters register.

 | 
Tier | 
Trigger | 
Source row
 | 
Immediate | 
Current or recent-onset chest pain. Features are recorded, not used to gate: qualifiers such as sweating or radiation are not required to trigger | 
Chest pain
 | 
Immediate | 
Sudden severe (thunderclap) headache | 
Headache
 | 
Immediate | 
New focal weakness, numbness, speech or visual disturbance — including symptoms that have since resolved | 
Stroke cluster
 | 
Immediate | 
Speech disturbance or reduced alertness degrading the interview itself — switch to collateral and escalate without completing | 
Stroke cluster
 | 
Immediate | 
Syncope during exertion; syncope with palpitations; syncope with family history of early sudden death | 
Syncope
 | 
Immediate | 
Breathlessness at rest or speaking in single words | 
Breathlessness (retained from original; not re-grounded)
 | 
Immediate | 
Haematemesis or melaena | 
GI bleeding
 | 
Immediate | 
Acute testicular pain, including intermittent pain, whatever the time elapsed since onset | 
Testicular torsion
 | 
Immediate | 
Non-blanching rash with fever, as reported by patient or carer | 
Rash
 | 
Immediate | 
Infant under three months with fever | 
Unwell child (retained from original)
 | 
Immediate | 
Green or bright yellow vomit in an infant | 
Vomiting
 | 
Immediate | 
Bladder or bowel dysfunction, or saddle numbness, with back pain | 
Back pain
 | 
Immediate | 
Painful limb with new numbness, tingling or weakness; or limb pain rising despite painkillers after injury, cast, crush, burn or surgery | 
Limb pain (replaces "pale, pulseless, cold limb")
 | 
Immediate | 
Sudden painful limb in a patient with atrial fibrillation | 
Limb pain
 | 
Immediate | 
After trauma with neck pain: age 65 or over, dangerous mechanism, or tingling in any limb | 
Neck pain after trauma
 | 
Immediate | 
Head injury with two or more episodes of vomiting | 
Trauma
 | 
Immediate | 
Major, penetrating or multi-system trauma — escalate on disclosure, no further questioning | 
Trauma
 | 
Immediate | 
Possible early pregnancy with abdominal pain plus shoulder-tip pain, dizziness or collapse | 
Vaginal bleeding
 | 
Immediate | 
Suspected infection and has not passed urine in 18 hours | 
Fever / sepsis
 | 
Immediate | 
Unable to swallow saliva | 
Dysphagia (uncited; for reviewer confirmation)
 | 
Immediate | 
Any positive answer to the direct suicide-risk questions | 
Mental health — its own escalation table governs
 | 
Same-day in person | 
Reduced fetal movements | 
Reduced fetal movements
 | 
Same-day in person | 
Pain or bleeding in possible early pregnancy | 
Vaginal bleeding
 | 
Same-day in person | 
Head injury in a patient on anticoagulants, or as set by the configured rule | 
Trauma
 | 
Same-day in person | 
Any bat contact at any time, or animal bite or scratch abroad | 
Wounds and bites
 | 
Same-day in person | 
Hot swollen joint with a prosthesis and skin infection over it, or joint surgery or injection within three months | 
Joint pain
 | 
Same-day in person | 
Suspected infection with new confusion or behaviour change reported by patient or relative, urine not passed for 12–18 hours, or immunosuppression | 
Fever / sepsis
 | 
Same-day in person | 
Fall with suspected loss of consciousness | 
Falls, routing to Syncope
 | 
Same-day in person | 
Palpitations occurring during the GP booking call | 
Palpitations (design proposal, not literature)
 | 
Flag | 
Unexpected weight loss | 
Weight loss (thresholds configurable)
 | 
Flag | 
New-onset fatigue in older adults | 
Fatigue (thresholds configurable)
 | 
Flag | 
Rectal bleeding, or change in bowel habit | 
Bowel habit (thresholds configurable)
 | 
Flag | 
Visible haematuria — painless, or recurring after a treated infection | 
Haematuria (thresholds configurable)
 | 
Flag | 
Dysphagia — especially short duration, solids only, or with weight loss | 
Dysphagia
 | 
Flag | 
Haemoptysis of any volume | 
Haemoptysis
 | 
Flag | 
Lump that is growing, larger than about 5 cm, or recurrent after removal | 
Lumps
 | 
Flag | 
Fall with injury, long lie over an hour, frailty, or two or more falls in a year | 
Falls
 | 
Flag | 
Choking or witnessed swallowing episode in a child with cough | 
Cough and wheeze
 | 
Flag | 
Carer conviction that a child is seriously unwell | 
Unwell child (whether this should escalate is a reviewer question)
 | 
Flag | 
Positive alcohol or drug screen | 
Alcohol and substance use
What changed from the previous version, and why.

"Pale, pulseless, cold limb" was removed as the limb trigger. Those are late signs; pulses stay normal in most upper-limb compartment syndrome. The old trigger would have fired only once the salvage window was closing. Early triggers — escalating pain, new paraesthesia — replace it.

Chest pain qualifiers were removed. "Chest pain with sweating, radiation, or at rest" gated in the wrong direction: pain without those qualifiers would not have triggered.

"Bleeding in pregnancy" was split and widened. Ectopic pregnancy can present without bleeding, so pain in possible early pregnancy now triggers; and the tier depends on shoulder-tip pain, dizziness or collapse.

Anticoagulated head injury moved up from Flag. NICE recommends CT within 8 hours regardless of other criteria; "flag and continue" was too low.

"Progressive dysphagia" was broadened. Short duration is the stronger danger sign than progression.

Resolved neurological symptoms are now explicit, and roughly twenty triggers that emerged from grounding were added.

Age thresholds were taken out of the triggers and moved to the configurable parameters register.
Triggers added after the gap pass. These come from the rows grounded after the master list was rebuilt, and follow the same three tiers.

 | 
Tier | 
Trigger | 
Source row
 | 
Immediate | 
Sudden painless loss of vision in one eye, current or resolved | 
Stroke cluster — monocular branch
 | 
Immediate | 
Over 50 with jaw or limb claudication and any visual symptom | 
Stroke cluster — monocular branch (proposed threshold)
 | 
Immediate | 
New neck pain with any neurological symptom, including one that has resolved | 
Neck pain without significant trauma
 | 
Immediate | 
Seizure, hallucinations or new confusion after stopping alcohol | 
Alcohol withdrawal
 | 
Same-day in person | 
Over 50 with jaw or limb claudication, no visual symptom | 
Stroke cluster — monocular branch (proposed threshold)
 | 
Same-day in person | 
New neck pain with new headache after neck manipulation, heavy lifting, contact sport or a fairground ride | 
Neck pain without significant trauma (proposed)
 | 
Same-day in person | 
Past complicated withdrawal, in a patient who has stopped or plans to stop drinking | 
Alcohol withdrawal
 | 
Same-day in person | 
Cut or puncture over a knuckle, whatever the stated cause | 
Clenched-fist injuries
 | 
Same-day in person | 
Leg pain at rest, especially at night, or a foot wound that will not heal | 
Claudication (ungrounded; for vascular review)
 | 
Flag | 
Breast lump, nipple change or discharge, or skin change — isolated breast pain alone is not a trigger | 
Breast lumps
 | 
Flag | 
New testicular lump or swelling in a young man, including if painful or previously called epididymitis | 
Testicular lumps
 | 
Flag | 
Lump above the collarbone; or a node persisting beyond four to six weeks, in two or more places, or with night sweats, fever or weight loss | 
Lymph nodes
 | 
Flag | 
Leg pain on walking that eases with rest | 
Claudication
Red flags from the first-draft system tables not yet carried into the master list. The consistency pass found clinically sound triggers in the system-section summary tables that no grounded row picked up. They are listed here rather than assigned a tier, because none was grounded in the literature during this project. Each needs a reviewer to confirm it and set its tier.

Severe headache or visual change in pregnancy (pre-eclampsia) — obstetrics

Postmenopausal bleeding — gynaecology; listed among features with a PPV of 5% or more in the lumps row's source

Acute urinary retention; clot retention — urology

Absolute constipation with vomiting; faeculent vomiting — surgery

Fever after recent travel — infectious diseases

Rash with mucosal involvement, blistering or skin peeling, or with swelling or breathing difficulty — dermatology and emergency medicine

Circumferential burn — emergency medicine

First seizure; prolonged or repeated seizure; seizure in pregnancy; failure to return to baseline — neurology; the seizure row set no tier

Exertional palpitations — cardiology; named as a red flag in the palpitations row but given no tier

Large-volume or ongoing haemoptysis — respiratory; the haemoptysis row insists small volume does not reassure but sets no immediate threshold for large volume

Reliever not working, or previous intensive care admission for asthma — respiratory
Consistency pass, recorded for reviewers. Before circulation, the document was checked for contradictions between rows written at different times. The main findings were in the summary tables at the head of each system section, which predated the grounding pass: six still named SOCRATES as the framework; the limb row led with pale, pulseless and cold; the joint row required fever; the lumps row flagged rapid growth; and the confusion, mental health and alcohol rows each described the agent bailing out or routing to a human in ways later reversed by evidence or by explicit design decision. These cells were corrected. The patient trigger-phrasing column in those tables was not changed and remains current. The early cross-cutting rules on red flags and bail-out were rewritten to match the three-tier system and the collateral-interview approach. Where any summary table and a grounded entry still disagree, the grounded entry governs.
Open questions

Whether the proposed three-tier split (Immediate, Same-day in person, Flag) holds, and whether the ED and GP versions need different thresholds given the difference in time to clinician review. The original question asked whether two tiers were enough; the grounding pass suggests they were not.

What the GP booking-call version does with an immediate-tier flag, given the patient is at home on the phone rather than in a waiting room. This is now the most pressing open question in the document: stroke, torsion, early pregnancy, neck trauma, limb pain and sepsis each place a caller in this tier, and several rows note that the exact wording given to the patient needs emergency medicine review.

Whether the agent's alert wording is standardised or generated, and how that is validated.

Who operates the Same-day in person tier in the GP version — reception, the duty GP, or a direct referral elsewhere — and what happens when no same-day appointment exists.