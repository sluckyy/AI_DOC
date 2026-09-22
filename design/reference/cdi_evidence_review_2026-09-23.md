# Reference: Clinical Documentation Improvement in Australia — Evidence Review and Agent Output Requirements

Source: the product owner's Claude Doc, https://claude.ai/artifact/Ntxybr7aHxVBb8MBMQi9Vn (as of 2026-09-23). Plain-text extract; tables and diagrams flattened. The live doc is the source of truth.

---


Clinical Documentation Improvement in Australia — Evidence Review and Agent Output Requirements
 · 
Scope and method
This review answers two questions. What does the Australian evidence say about improving clinical documentation, and what would an AI history-taking agent have to put on paper for that output to be usable under Australian coding rules?
Part 1 is a narrative review of clinical documentation improvement (CDI) in Australia: the documentation–coding–funding chain, measured documentation deficits, the interventions tried, the outcomes reported, and the emerging digital and AI approaches. Part 2 converts that evidence into an output specification for the history-taking agent — the verbal handover plus a parallel coding-ready document.
Sources were identified by targeted searching of the peer-reviewed and professional literature — in practice Health Information Management Journal and HIM-Interchange carry most of the Australian work in this area — together with the primary standards and policy sources: IHACPA for ICD-10-AM/ACHI/ACS, the Australian Coding Standards and activity based funding, the ACSQHC for hospital-acquired complications, state health department coding guidance, and the TGA and Safer Care Victoria for the regulatory position on AI documentation tools. Coverage runs to September 2026.
Two boundaries are worth stating up front. This is a narrative, not a systematic, review — the Australian CDI literature is small, heterogeneous and dominated by single-site before-and-after studies, so a formal synthesis would have little to pool. And "documentation improvement" is used here in its Australian sense: improving the record so that it accurately reflects the episode, not the narrower US sense of revenue-cycle optimisation.
Part 1 — The documentation–coding–funding chain
In Australia the medical record is the only admissible source for classifying an episode of care. A clinical coder reads the record and assigns diagnosis codes from ICD-10-AM and intervention codes from ACHI, applying the Australian Coding Standards (ACS) to decide what may be coded and in what order.
All three are maintained by the Independent Health and Aged Care Pricing Authority (IHACPA) and updated on a three-year cycle. The Thirteenth Edition applies to separations from 1 July 2025; it added a standard ACS template with explicit directives and worked examples, cluster coding to link related diagnoses, and new codes for social determinants of health, vaping and voluntary assisted dying.
Those codes then drive everything downstream:
the only source] --> B[Coder appliesICD-10-AM + ACHIper ACS]
  B --> C[AR-DRG grouper+ age, LOS,separation mode]
  C --> D[AR-DRG+ price weight]
  D --> E[NWAU x nationalefficient price]
  B --> F[Condition onset flag-> hospital-acquiredcomplications]
  B --> G[Casemix-adjustedcomparison + researchdatasets]]]>
Under activity based funding, the AR-DRG's relative weight is expressed as National Weighted Activity Units and multiplied by the national efficient price. A missing comorbidity does not just lose a code — it can move the episode into a lower-complexity DRG split and change what the hospital is paid for that admission.
The same codes carry non-financial weight. Condition onset flags separate conditions present on admission from those arising during it, which is how hospital-acquired complications are identified and how safety-and-quality adjustments are applied. The coded record is also the substrate for casemix-adjusted benchmarking, mortality and morbidity statistics, and most Australian administrative-data research.
This is the structural reason documentation improvement matters here in a way it does not in a purely narrative record. The record is not just a clinical communication artefact — it is the input to a classification system with funding, safety reporting and research consequences, and it is read by someone who was not in the room.
What the Australian evidence shows about documentation deficits
Documentation, not coder skill, is the dominant source of coding error in the Australian studies that have looked. The most-cited example remains a Melbourne tertiary hospital audit in which 16% of 752 surgical episodes changed DRG on blind re-coding, and 56% of those changes were attributable to documentation problems rather than coding mistakes.

Study
Setting and design
Principal finding
Cheng et al. 2009
Melbourne tertiary hospital; blind re-coding audit of 752 surgical separations over 6 months
16% DRG change rate; 56% of changes due to documentation, 29% missed additional diagnoses, 13% wrong principal diagnosis; AU$575,300 revenue variance
Hay et al. 2020
Narrative case for CDI in Australian hospitals
Argues CDI is a data-quality intervention, not a revenue one; cites only 55% of laboratory-confirmed S. aureus bacteraemia appearing in coded data
Shepheard 2020
Editorial, Health Information Management Journal
Coding integrity depends on record quality; EMR copy-paste propagates error; specialty-dependent specificity; mental health and self-harm systematically undercounted
Mahfouz et al. 2017
Cross-sectional survey of 118 Australian GPs and registrars on discharge summary quality
Summaries "overloaded with irrelevant" copied EMR content; 65.5% dissatisfied with documentation of medication change rationale
Lloyd and Cooper 2025
Professional commentary, HIM-Interchange
Data timeliness and quality are the binding constraint on ABF; warns against reducing health information management to coding alone
Four deficit patterns recur across this work.

Omission of comorbidities that were actually managed. The condition was treated during the episode but never named in the record, so it fails the ACS 0002 test on documentation grounds rather than clinical ones.

Ambiguity between symptom and diagnosis. The record carries "chest pain" throughout with no documented conclusion, forcing a Chapter 18 symptom code where a definitive diagnosis existed in the clinician's mind.

Non-specific terminology. "Sepsis", "renal impairment", "delirium" without the qualifiers the classification needs — organism, acute versus chronic, stage, causative agent.

Unclear onset. Nothing in the record states whether a condition was present on admission, which is exactly what the condition onset flag has to capture.
The structural cause is consistent: clinical language and classification language are not the same language, and the record is written in the first for readers who are not the coder. Shepheard's point about copy-paste is worth holding onto — digitisation increased the volume of documentation without increasing the amount of codeable content in it, and in some cases reduced it by burying the specific in the duplicated.
Interventions tried in Australia
Four intervention families appear in the Australian literature, and only one of them has been reported with usable numbers.

Intervention
Mechanism
Australian evidence
Concurrent CDI specialist review
Specialist reads the record mid-admission and queries the treating team while the patient is still there
Best documented. Gold Coast Health "e-Ink the Link": 4,500+ admissions reviewed, 2,450 queries, ~$6.15M recovered complexity in FY2024; team grew 2 → 5 FTE
Clinician education
Teaching doctors what the classification needs and why
Embedded within CDI programs (Gold Coast's "Nail Your Notes" for junior doctors); no Australian controlled evaluation of education alone
Retrospective audit and feedback
Blind re-coding, error attribution, feedback to units
Cheng et al. 2009 is the method exemplar; used widely for assurance, rarely evaluated as an improvement intervention
Structured templates and EMR forms
Force specificity at the point of writing
Widely deployed, essentially unevaluated in the Australian peer-reviewed literature
The Gold Coast model is the one worth studying closely, because it shows what "documentation improvement" actually consists of in practice: targeting by DRG complexity benchmarking against peer hospitals, selecting acute admissions with a 2–8 day length of stay, issuing an electronic query mid-admission, and escalating on a tiered 2–10 day timeline when no answer comes back.
That query is the operative act, and it is tightly constrained. IHACPA's Standards for Ethical Conduct in Clinical Coding prohibit coders from prompting or using leading questions to maximise reimbursement, from seeking documentation for conditions not already apparent in the record, and from using pathology or radiology results as the basis for a query. The standards draw a line between unethical "maximising" — adding codes without documentary support — and acceptable "optimisation", meaning the full and correct use of what is already documented.
This constraint is the single most important thing to carry into Part 2. A query may only ask a clinician to clarify something the record already gestures at. It may not introduce the condition. Any automated system that generates documentation therefore sits on the supply side of that line, not the query side: its job is to make the clinical facts present and specific in the first place, so that fewer queries are needed at all.
Outcomes, and the problem with how they are measured
Almost every Australian CDI report leads with recovered revenue, which is the weakest available endpoint. Revenue change tells you that the coded picture moved. It does not tell you whether it moved towards the truth.

Outcome measure
What it establishes
What it cannot distinguish
Recovered revenue / NWAU delta
That documentation changed code assignment
Correction from complexity creep
DRG change rate on blind re-coding
Disagreement between two coding passes
Which pass was right, without an independent clinical gold standard
Query volume and response rate
Program throughput and clinician engagement
Whether the queries were necessary or appropriate
Agreement with clinician-adjudicated diagnosis list
Whether the record reflects the episode
Nothing — this is the endpoint the field mostly does not use
HAC rates
Apparent safety performance
Real change from changed documentation practice
The last two rows matter most. Under activity based funding, better documentation and complexity creep produce the identical financial signature, so a program that reports only dollars cannot demonstrate which it achieved. IHACPA's ethical standards draw the conceptual line — "maximising" versus "optimisation" — but no routinely reported outcome measure operationalises it.
The safety measures have a parallel problem in the opposite direction. Hospital-acquired complications are derived entirely from coded data plus the condition onset flag, across 16 high-priority complication categories, and attract a pricing adjustment. Yet when the coded flag is validated against clinical surveillance definitions it often performs poorly: Valentine et al. found a positive predictive value of 0.18 for hospital-acquired pneumonia across 41,260 separations at Peter MacCallum, rising to 0.34 after EMR implementation but still leaving most coded cases unconfirmed.
So the coded record is simultaneously under-inclusive of real comorbidity and over-inclusive of some flagged complications, and both failure modes trace back to what was and was not written in the notes. The practical implication for any new documentation intervention is that its evaluation has to be anchored to an independent clinical reference standard, not to the movement it produces in NWAU.
Digital and AI approaches
Automation has been aimed at the wrong end of the problem. Almost all of it tries to extract codes from text that was already written; very little tries to improve what gets written.
Computer-assisted coding. The most substantial Australian work is Nguyen and colleagues' Medtex evaluation at Gold Coast Hospital and Health Service — 569,846 encounters and 8.6 million progress notes from 2011–2015, mapping free text to ICD-10-AM via UMLS and SNOMED CT. Principal diagnosis sensitivity reached 54.1% with a PPV of 70.2%, improving to 65.9% and 73.7% at three-character grouping level.
The finding that matters most is the manual validation: two clinical coders judged that only 76.3% of sampled encounters could be coded from the progress notes at all. That is a ceiling on any text-mining approach, and it is a documentation ceiling, not an algorithmic one. No model can extract a diagnosis nobody wrote down.
Automated ICD coding generally. A 2026 systematic review of 24 studies from 2020–2025 found 87.5% remained at research stage with no real-world clinical validation, performance falling sharply on rare codes, and regional variants such as ICD-10-AM appearing in only a small proportion of studies. The field is trained largely on MIMIC and US English inpatient text.
Ambient scribes. Uptake has run well ahead of evidence, and Australian regulators have responded with governance guidance rather than efficacy claims. Safer Care Victoria's May 2025 sector advisory requires explicit patient consent with an opt-out, Australian data storage, a prohibition on vendor data resale, and — centrally — that the AI output is a first draft for which the clinician retains all responsibility for accuracy and completeness. It names automation bias explicitly as accuracy improves. The Australasian Institute of Digital Health's June 2025 information sheet adds a concrete quality-assurance instrument, the Modified PDQI-9, scoring notes across ten domains including accuracy, thoroughness and freedom from hallucination.
Regulatory position. The TGA has published specific guidance on digital scribes clarifying when such software meets the medical device definition. The boundary is functional rather than categorical, and it is moving: the Victorian advisory of May 2025 described AI scribes as then falling outside TGA regulation. A system that goes beyond transcription into clinical interpretation — suggesting diagnoses, or generating codeable diagnostic statements — should be assumed to sit closer to that line, and the assumption checked against current TGA guidance before deployment rather than after.
The gap this leaves is the one the history-taking agent occupies. Scribes capture a consultation that has already happened. Coding tools read notes that have already been written. Nothing in the current Australian literature addresses generating structured, classification-aware clinical content before the clinical encounter, from the patient directly.
Gaps in the evidence
The Australian CDI literature is thin, and thin in a specific way. It is dominated by single-site before-and-after reports, published in professional rather than trial literature, with revenue as the headline endpoint and no independent clinical reference standard.
Five gaps stand out.

No controlled evaluation of any Australian CDI intervention. Nothing randomised, nothing stepped-wedge, no concurrent control site. The Gold Coast program is well described but is a service report, not a study design that can attribute effect.

No separation of correction from creep. Because revenue is the endpoint and no blinded clinical gold standard is used, the literature cannot tell the two apart — despite IHACPA's ethical standards making the distinction central.

Nothing on the patient as a documentation source. Every intervention acts on what clinicians write. None acts on the quality of the history that reaches the clinician in the first place.

No Australian evidence on whether structured pre-consultation input improves the coded record. The CAC ceiling of 76.3% codeable encounters implies substantial headroom, but nobody has tested filling it at source.

Little on emergency and primary care. The classification literature is almost entirely admitted-patient. ED (URG/UDG) and general practice documentation are comparatively unexamined, which is precisely where the history-taking agent is intended to operate.
This is the opening. A voice agent that takes a structured history before the clinician sees the patient is the first intervention in this space that acts on the supply of clinical facts rather than on the transcription of them — and the evaluation design in the existing agreement study (agent history versus clinician history, consultant-adjudicated) already contains the blinded reference standard the CDI literature lacks.
Part 2 — What the classification actually demands of a document
The Thirteenth Edition contains 117 standards in three parts. Five of them govern almost everything relevant to a history-taking agent's written output.

Standard
What it governs
What it demands of the document
ACS 0001
Principal diagnosis — "the diagnosis established after study to be chiefly responsible for occasioning an episode of admitted patient care"
A definitive diagnosis, where one exists, stated as the reason for the episode. Chapter 18 symptom codes cannot be principal if a definitive diagnosis is documented. Where several conditions equally qualify, the clinician should indicate which; failing that the coder takes the first mentioned — so ordering is not cosmetic
ACS 0002
Additional diagnoses
The condition must be named by a clinician and the record must show it met one of three tests this episode: treatment commenced, altered or adjusted; investigations done to evaluate or monitor it; or increased nursing or clinical care. A pre-existing condition whose medication simply continued unchanged does not qualify
ACS 0010
Clinical documentation and general abstraction
Sources are ranked. See below — this is the standard that constrains the agent most
ACS 0048
Condition onset flag
Whether each condition was present on admission or arose during the episode. This is what separates comorbidity from hospital-acquired complication
ACS 0050
Unacceptable principal diagnosis codes
Some codes may never be principal, so a document that offers only those leaves the coder with nothing usable
ACS 0010 is the binding constraint
The Western Australian summary of ACS 0010 sets out a source hierarchy that determines what an agent-generated document can and cannot do:

Primary source. Documentation in the current episode, written primarily by medical and surgical clinicians.

Conditional source. Specialist nurses, midwives and allied health may document diagnoses within locally defined scope of practice — but that documentation "must be qualified by other documentation in the current episode".

Clarifying source only. Referral letters, emergency department notes, outpatient records and previous episodes may be used to resolve ambiguity, add specificity to an already-documented condition, or establish the reason for admission. They are not primary sources for code assignment.

Not a source. Patient-completed forms. ACS 0010 states directly that coding must not rely on them. Abnormal test values alone do not establish a diagnosis either.
That fourth line is the one to sit with. A history taken from the patient by an agent — however structured, however accurate — is, in classification terms, closest to a patient-completed form. It does not become codeable by being well written.
What the agent can and cannot legitimately contribute
The agent cannot author a codeable diagnosis, and designing as though it could would put the output on the wrong side of ACS 0010 and of IHACPA's ethical standards at once. What it can do is change the state of the information so that a clinician's single act of attestation converts it into a primary source.
 PatientReported: agent interview
  PatientReported: Agent draftpatient-reportedNOT codeable
  PatientReported --> Attested: clinician reviews,edits, signs
  Attested: Clinician documentationcurrent episodeCODEABLE
  PatientReported --> Clarifying: no attestation
  Clarifying: Clarifying source onlyACS 0010 tier 3
  Attested --> [*]]]>
This is the same governance model Australian regulators already apply to ambient scribes: the AI output is a first draft, and the clinician retains all responsibility for its accuracy and completeness. The agent is not exempt from that because it interviewed the patient rather than the clinician — if anything it is further from the record, because no clinician was present.
Three things the agent is uniquely well placed to supply.
First, facts only the patient holds that the classification needs and that routinely go unrecorded. Chapter 20 external cause coding requires mechanism of injury, place of occurrence and activity at the time — three fields that are patient-reported by nature and chronically absent from ED records. Onset timing, prior diagnoses with who made them and when, and whether a regular medication has actually been taken are all in the same category.
Second, the specificity the classification needs but clinical shorthand drops. The agent can ask the question whose answer distinguishes acute from chronic, first episode from recurrence, or one diabetes subtype from another, without the clinician having to remember that the classification cares.
Third, onset relative to admission, which is the whole substance of the condition onset flag. A history taken before or at presentation is the best possible evidence of what was already present, and it is captured at exactly the moment when that is unambiguous.
Three things it must not do.
It must not generate diagnostic labels styled as clinical conclusions — "acute coronary syndrome" where the patient said chest pain. It must not infer a diagnosis from a symptom pattern and present the inference as history. And it must not be tuned towards output that increases coded complexity: a system that preferentially elicits complication-bearing content would be the automated equivalent of a leading query, which the ethical standards prohibit for exactly the reason that it is invisible in the resulting record.
The design principle that follows is provenance labelling at field level. Every element in the coding document should carry whether it is patient-reported, clinician-confirmed, or derived — and the coder should be able to see that distinction without reading the narrative.
The dual-output specification
One interview, two artefacts, one attestation. The handover is the narrative a good registrar would give; the coding document is the same content reshaped for a reader who was not in the room and who works to ACS rules.
Output A — verbal handover. Narrative, ordered by clinical salience, with structured data layered underneath and the agent available for clarifying questions. Unchanged from the existing design.
Output B — coding document. Field-structured, provenance-labelled, and explicitly incomplete: the diagnosis fields are left for the clinician, because those are the fields only a clinician can fill.

Block
Content
Standard served
Provenance
Reason for encounter
The patient's presenting problem in their words, plus the agent's structured symptom set
ACS 0001 — supports later principal diagnosis selection
Patient-reported
Diagnosis block
Left empty by the agent. Labelled slots for principal diagnosis and additional diagnoses, with a prompt for the clinician to nominate which condition occasioned the episode
ACS 0001; the "first mentioned" default means ordering matters
Clinician only
Symptom detail with qualifiers
Per symptom: onset, duration, course, severity, laterality, acute vs chronic, first episode vs recurrence, and the qualifier the classification needs for that symptom family
ACS 0010 — adds specificity to a documented condition
Patient-reported
Pre-existing conditions
One row per condition: condition, who diagnosed it and when, current treatment, whether treatment has changed, whether it is being actively monitored
ACS 0002 — gives the clinician the three significance tests explicitly rather than implicitly
Patient-reported; clinician-confirmed on attestation
Onset relative to presentation
For every condition listed, whether present before arrival, stated as a fact of the history
ACS 0048 condition onset flag
Patient-reported
Medications
Drug, dose, actual adherence, recent changes and why, and the condition each is for
ACS 0002 — "treatment continued unchanged" versus "altered" is the discriminator
Patient-reported
External cause (injury presentations)
Mechanism, place of occurrence, activity at the time, and intent
ICD-10-AM Chapter 20 — mandatory external cause coding
Patient-reported
Behavioural risk factors
Smoking status with quantity and currency, alcohol, other substance use
Z-code assignment; ACS 0002 where actively managed
Patient-reported
Social and functional
Accommodation, supports, mobility, carer status, occupation
Thirteenth Edition social determinants of health codes
Patient-reported
Obstetric status
Pregnancy status, gestation, parity
Chapter 15 standards; changes principal diagnosis selection rules
Patient-reported
Provenance and attestation
Statement that the content is patient-reported and machine-transcribed, the agent version, the interview timestamp, and a clinician sign-off field
ACS 0010 — converts tier 4 to tier 1
Structural
Three design rules that fall out of this
Separate the fields the agent fills from the fields it must not. The diagnosis block sits at the top of the document and is visibly empty. That is not a limitation to be apologised for — it is the feature that makes the rest of the document safe to use, and it shows the clinician exactly what their attestation is adding.
Make the ACS 0002 tests answerable from the document. A coder reading the pre-existing conditions table should be able to see, for each row, whether treatment changed and whether the condition was monitored this episode. Most missed additional diagnoses fail on exactly this evidence, not on the diagnosis itself.
Bind to terminology, not to codes. The agent should emit SNOMED CT-AU concepts, not ICD-10-AM codes. The classification is a coder's instrument applied under standards the agent cannot apply, and the Australian computer-assisted coding work already demonstrates the SNOMED CT → ICD-10-AM mapping route. Emitting codes would also be the point at which the output starts to look like an automated coding claim rather than a history.
For the two deployment settings, the same document serves different ends. In the ED version it arrives before the clinician does and travels with the episode, so it feeds admitted-patient coding directly once attested. In the GP booking-call version it is generated days before the consultation, which makes it — in ACS terms — prior-episode documentation: a clarifying source at best until the GP adopts it. Worth designing the GP version so that adoption is a single deliberate act at the start of the consultation.
Governance, safety and evaluation
Governance
The existing Australian guidance for ambient scribes transfers almost intact, and it is the sensible baseline to design against rather than negotiate later. Explicit patient consent with a genuine opt-out and equivalent care either way; data stored and processed in Australia; no vendor resale or third-party model training on the content; retention schedules covering the AI-generated artefacts as well as the final record; and the clinician retaining all responsibility for accuracy and completeness of what they sign.
Two things need more than the scribe baseline.
Attestation must be an act, not a click. Automation bias is named explicitly in the Victorian advisory, and it gets worse as accuracy improves. The diagnosis block being empty is the main structural defence — the clinician cannot rubber-stamp a diagnosis the agent did not supply. Worth resisting any later pressure to pre-populate it.
Regulatory classification should be settled early. Transcription and structuring sit outside medical device regulation; red flag escalation to a triage desk is clinical decision support and plausibly inside it. The coding document itself is the ambiguous case. Ask the TGA before building, not after — the digital scribes guidance is the entry point, and the boundary has moved recently enough that assumptions will not hold.
Evaluation
The planned agreement study already has what the CDI literature lacks: a blinded, consultant-adjudicated reference standard. Adding the coding question to it costs relatively little.

History agreement (existing primary endpoint). Agreement between agent-elicited and clinician-elicited histories on the same simulated patients, consultant-adjudicated, blinded by having actors or agents read both scripts.

Condition capture. Per-condition sensitivity and positive predictive value of the agent's structured condition list against the adjudicated reference — directly comparable to the 54.1% sensitivity / 70.2% PPV benchmark from the Australian computer-assisted coding work, though that was extraction from notes rather than elicitation from patients.

Coder-facing sufficiency. Blinded dual coding of the same episodes with and without the agent document: DRG concordance, additional diagnosis counts, coder query rate, and coder-rated documentation sufficiency. Crucially, judge concordance against the adjudicated clinical reference, not against the routine coded record.

Note quality. Modified PDQI-9 on the handover and the coding document, since it is already the instrument Australian digital health guidance points to, and it scores freedom from hallucination explicitly.

Safety. Rate of history items present in the document but absent from the reference standard — fabricated or misattributed content is the failure mode that matters most here. Paired with red flag sensitivity and time-to-escalation.

Equity. Stratify everything by interview language, age and health literacy. A multilingual agent whose capture rate falls for interpreted histories would quietly widen a documentation gap rather than close one.
One endpoint to declare as a monitored harm rather than a benefit: coded complexity. NWAU or DRG complexity shift should be reported, watched, and explicitly excluded from the success criteria. If the agent improves capture honestly, complexity may rise as a side effect; if complexity rises without a matching rise in agreement with the adjudicated reference, that is drift toward the "maximising" side of IHACPA's ethical line and should be treated as a finding against the system. Saying so in the protocol before any data exists is the cheapest possible protection against the critique the whole CDI field currently cannot answer.
Sources
All sources below were retrieved and read in full. Two relevant papers could not be retrieved and are listed separately.
Classification, standards and funding

IHACPA. ICD-10-AM/ACHI/ACS — system overview and three-year update cycle.

IHACPA. ICD-10-AM/ACHI/ACS Thirteenth Edition — applicable to separations from 1 July 2025.

IHACPA. Activity based funding for Australian public hospitals — AR-DRG, NWAU and national efficient price.

IHACPA. Standards for Ethical Conduct in Clinical Coding — query constraints; "maximising" versus "optimisation".

Australian Coding Standards sample: ACS 0001 Principal diagnosis.

WA Department of Health. ACS 0010 Clinical documentation and general abstraction guidelines — summary — source hierarchy and the exclusion of patient-completed forms.

TalentMed. Australian Coding Standards guide and Coding comorbidities and additional diagnoses (ACS 0002) — secondary explanatory sources for ACS structure and the ACS 0002 significance tests.

ACSQHC. Hospital-acquired complications (HACs) — 16 categories, condition onset flag, pricing adjustment.
Documentation quality and CDI

Cheng P, Gilchrist A, Robinson KM, Paul L. The risk and consequences of clinical miscoding due to inadequate medical documentation. HIMJ 2009.

Hay P, Wilton K, Barker J, Mortley J, Cumerlato M. The importance of clinical documentation improvement for Australian hospitals. HIM-Interchange 2020 (also published in Health Information Management Journal).

Shepheard J. Clinical coding and the quality and integrity of health data. HIMJ 2020;49(1).

Mahfouz C, Bonney A, Mullan J, Rich W. An Australian discharge summary quality assessment tool: a pilot study. AFP 2017.

Sumner S, Vincent J, Carroll R, Acworth S, White E, Sati V. Targeting complexity: real-time clinical documentation improvement in a tertiary hospital. HIM-Interchange 2025.

Lloyd S, Cooper H. Impacts of activity based funding on the health information management profession. HIM-Interchange 2025.

Valentine JC, Gillespie E, Verspoor KM, Hall L, Worth LJ. Performance of ICD-10-AM codes for quality improvement monitoring of hospital-acquired pneumonia. HIMJ 2024.
AI, NLP and regulation

Nguyen H et al. Computer-assisted diagnostic coding: effectiveness of an NLP-based approach — Medtex at Gold Coast Hospital and Health Service, 569,846 encounters.

Artificial intelligence for automated ICD-10 coding: a systematic review of multi-label text classification in clinical narratives. Frontiers in Digital Health 2026.

Safer Care Victoria. Ambient AI Scribes Sector Advisory, May 2025.

Australasian Institute of Digital Health. Implementation of AI scribes in healthcare workflows, June 2025.

TGA. New information on digital scribes.
Relevant but not retrieved

Shepheard J. What do we really want from clinical documentation improvement programs? HIMJ 2018 (doi:10.1177/1833358317712312) — publisher access refused. Directly on the funding-versus-data-quality tension in the outcomes section; worth chasing through your library.

Incidence and variation of discrepancies in recording chronic conditions in Australian hospital administrative data. PLOS One 2016 — rate-limited. Would strengthen the comorbidity-recording evidence.