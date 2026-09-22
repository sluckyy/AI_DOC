# Reference: Medical History Taking — Evidence Review and Design Implications

Source: the product owner's Claude Doc, https://claude.ai/artifact/67k7T6qWdtJCVj11vS7V52 (as of 2026-09-23). Plain-text extract; tables flattened. The live doc is the source of truth.

---


Medical History Taking — Evidence Review and Design Implications
 · 
Scope and method
This is a structured narrative review, not a systematic review: the search was documented and deliberate, but screening was pragmatic and no formal quality appraisal or PRISMA flow was applied.
It answers five questions:

How much diagnostic work does the history actually do?

What interview structure, sequence and question form produce the most complete and accurate history?

How well do automated, computer-assisted and AI agents take histories compared with clinicians?

What is the evidence for direct questioning on red flags, risk and sensitive topics?

What teaching methods produce durable history-taking skill?
A final section translates the findings into explicit design rules for the AI history-taking agent, separated by the GP booking-call version and the ED room version.
Search

Element
Detail
Sources
PubMed/PMC, Cochrane Library, BMJ/JAMA/Springer/ScienceDirect/PLOS via open web, JMIR, NEJM AI
Core terms
history taking, medical interview, clinical interview, open-ended questions, patient agenda, question phrasing, symptom elicitation, diagnostic contribution of history, computer-assisted history taking, conversational agent history, LLM history taking, risk screening, safety netting, communication skills teaching
Design filters
Systematic reviews, meta-analyses, RCTs and observational studies prioritised; consensus guides and textbook frameworks included but labelled as such
Dates
No hard limit — landmark work from the 1970s–90s retained where it is still the primary evidence; digital/AI evidence restricted to 2015 onward
Language
English
Limitations

Access was largely to abstracts, full texts in open repositories, and Cochrane summaries. Where only an abstract was read, the finding is reported at the level the abstract supports.

The history-taking literature is dominated by small single-centre studies, simulated-patient work and cross-sectional audio analysis. Very little of it has hard patient outcomes.

Many widely taught frameworks (Calgary-Cambridge, SOCRATES) are consensus structures with limited direct comparative evidence. This review labels them accordingly rather than treating teaching authority as evidence.

Search was English-language only, which matters given the agent's multilingual requirement.
How much of the diagnosis comes from the history?
The familiar claim that history alone yields ~80% of diagnoses rests on a small set of studies, most with fewer than 120 patients, none randomised, and none systematically reviewed. The direction of the finding is robust; the number is not.

Study
Setting
n
Diagnosis from history alone
Platt 1947
General medicine
100
68% (74% including "substantially correct")
Hampton 1975
Medical outpatients
80
82.5% (66/80); exam and labs each changed the diagnosis in ~9%
Sandler 1980
Hospital, mixed complaints
630
56% — varied sharply by presenting complaint
Peterson 1992
Ambulatory, Salt Lake City
80
76.3% (61/80)
Roshan & Rao 2000
Hospital, India
98
78.6% (77/98)
Wang 2009
Neuro-ophthalmology clinic
115
88%
Pooled informally, these give roughly 76% ± 8%. The variance is the interesting part, not the mean.
What the number actually means
Three caveats matter for anyone designing a history-taking system.
Sequencing inflates the estimate. In every one of these studies the history came first and generated the hypothesis that the examination and tests then confirmed. Credit for the diagnosis accrues to whichever step got there first, which is structurally the history. This does not make the history less necessary — it makes the percentage a poor measure of its independent contribution.
The yield is complaint-dependent. Sandler's 56% is the outlier that proves the point: in a cardiology-weighted hospital sample where imaging carries more of the load, history's share drops by a third. A per-symptom questioning library should expect the history to be near-decisive for headache, back pain and syncope, and much weaker for undifferentiated breathlessness or abdominal pain.
Individual history features are usually weak. Summerton's BJGP analysis makes the sharpest point available in this literature: single symptoms carry poor discriminatory value — dysuria for UTI has a likelihood ratio of about 1.5 — and history's power comes from combining many weak features, not from finding one strong one. He argues for setting-specific likelihood ratios attached to history elements, treating the interview as a pre-test-probability engine rather than a diagnostic act.
The modern counterpoint
Paley et al. (Arch Intern Med 2011) found that four in five internal-medicine ED admissions could be correctly diagnosed from history, examination and basic laboratory tests together, and argued this showed the limited marginal value of the physical examination. The accompanying commentary contended the study had in fact re-demonstrated the primacy of the history, since that was the step doing most of the work within the bundle. Both readings are compatible with the older literature.
At the same time, quality of history-taking is not a free variable. A randomised simulator trial of 198 medical students assessing simulated pulmonary embolism found diagnostic accuracy driven by whether specific content was asked — immobilisation (coefficient 0.42, p<0.001), PE risk factors (0.15), dyspnoea (0.12) — while more systematic history-taking was associated with lower accuracy (−0.27, p<0.001) (Signa Vitae 2023). Breadth without targeting does not help.
Structure and sequence: the opening phase
The strongest and most replicated finding in the entire history-taking literature is that clinicians cut patients off too early, and that letting patients finish costs almost nothing.
Interruption

Study
n
Patients who completed their opening statement
Time to interruption
Beckman & Frankel 1984
74 visits
23% (17/74); physicians interrupted in 69%
Not reported in abstract; widely cited as ~18 s
Marvel 1999
Family practice consults
28%
Completed statements took 23.8 s vs 27.7 s for redirected ones (p=0.14)
Singh Ospina 2019
112 encounters (61 primary, 51 specialty)
Agenda solicited in only 36% (49% primary, 20% specialty)
Median 11 s after elicitation; uninterrupted patients needed a median of 6 s
Fifteen years apart, Beckman and Marvel found essentially the same completion rate. Marvel's control comparison is the decisive number: letting the patient finish took four seconds longer. The time argument for interrupting does not survive contact with data.
Langewitz 2002 measured the upper bound directly — 335 patients, Swiss university internal-medicine outpatients, hidden stopwatch. Mean spontaneous talking time was 92 s (SD 105), median 59 s, and 78% finished their initial statement within two minutes.
Consequences of truncating the opening
Marvel found that when physicians redirected early, patients went on to state one or more additional concerns in 33% of cases once given the chance, and in just over 20% of visits a new concern surfaced after the formal history was over — the "doorknob" problem. Concerns raised late are the hardest to work up properly.
Singh Ospina's finding that specialists elicit an agenda in only 20% of encounters is the relevant warning for a triage-adjacent agent: the narrower the perceived remit, the more likely the opening is skipped entirely.
Agenda completeness and the "something else" effect
The single most directly actionable trial in this literature is Heritage et al. 2007: 20 physicians, 224 patients, 20 offices in Los Angeles County and Pennsylvania. After the chief concern was stated, physicians were randomised to ask one of two questions.

Question asked
Effect on unmet concerns
"Is there something else you want to address today?"
Eliminated 78% of unmet concerns (OR 0.154, p=0.001)
"Is there anything else you want to address today?"
No significant difference from control (p=0.122)
No question (control)
Reference
Neither version lengthened the visit. One word changed the yield; the grammatically negative-polarity "anything" invites a "no", and patients take it.
This is the clearest evidence in the field that exact question wording, not just question type, changes what gets disclosed — and it is directly testable in an agent, which can randomise phrasings at scale in a way a clinical trial cannot.
Question form: open, closed, leading
Open questions produce more information and more accurate information. Closed and leading questions produce less of both. The effect has been shown in medical interviews, in forensic child interviews, and in disclosure of stigmatised behaviour.
Volume of information
Two Japanese studies give the cleanest medical evidence, both using the Takemura Medical Interview Rating Scale.

Takemura 2005 — 1,220 medical students, five-minute standardised-patient interviews. Use of open-ended questions was positively related to the amount of information elicited (F=41.0, p<0.0001).

Takemura 2007 — 315 real outpatients, videotaped and rated. Three behaviours independently predicted information obtained, after adjusting for interview duration:

Behaviour
F
p
Open-to-closed cone (progressive narrowing from non-directive to specific)
40.1
<0.0001
Facilitation ("mm-hm", "go on" — continuers that keep the patient talking)
15.3
<0.0001
Summarisation (explicit verbal summary of what has been gathered)
5.57
0.019
The open-to-closed cone is the single most important structural finding for an automated agent: it is not "open questions are good", it is that the transition from open to closed, done gradually, is what predicts yield. That is an architecture, not a style note. Summarisation earning independent significance is the second: reflecting the history back mid-interview elicits more, not just confirms.
Accuracy of information
Volume and accuracy are different outcomes, and the accuracy evidence comes mostly from outside medicine.
A Norwegian Institute of Public Health systematic review (7 field studies, 239 children aged 3–16, forensic interviews) validated question type against criteria-based content analysis, self-contradiction and later confirmation:

Open prompts produced responses meeting roughly three times as many credibility criteria as directive or suggestive prompts (Craig 1999, p<0.05).

Invitational questions produced fewer details the child later contradicted than directive or option-posing questions (Lamb 2001, p<0.001).

Open-ended prompts yielded ~30% confirmed details versus 18–21% for focused prompts (Lamb 2007, p<0.03).

One study found no significant relationship (Leander 2009).
The mechanism — recognition memory is more suggestible than free recall — is not child-specific, but the transfer to adult medical interviewing is an inference, not a demonstration.
Phrasing and disclosure of stigmatised information
Among 162 HIV-care encounters with patients reporting past-month cocaine, heroin or heavy alcohol use (Boston University summary):

Question form
Disclosure rate
RR vs open/normalising
Open-ended
100%
reference
Normalising ("many people in your situation…")
100%
reference
Closed-ended
58%
0.60
Leading toward non-use ("you're not still using, are you?")
22%
0.22
Substance use went entirely undiscussed in 50% of encounters. Only 11% of encounters used an open question and 9% a normalising one — the effective techniques were the rarely used ones.
Together with Heritage's "some" vs "any" result, this establishes that phrasing effects are of the same order as question-type effects. Polarity and normalisation are levers, not decoration.
What the clinician then records
Even information successfully elicited is frequently lost at documentation. In 1,119 Mayo Clinic patients, intake-form symptoms were compared with NLP-extracted clinical notes (Am J Manag Care 2008):

Symptom
Positive agreement
κ
Chest pain
74%
0.52
Dyspnoea
70%
0.46
Cough
63%
0.38
Between 31% and 45% of patients who reported a symptom had no mention of it in the note. This is a strong argument for an agent that captures structured data at the point of elicitation rather than relying on the clinician to transcribe.
Completeness, error, and when to stop asking
History failure is the commonest identified cause of diagnostic error
Singh et al. (JAMA Intern Med 2013) reviewed 190 confirmed diagnostic errors identified by EHR triggers across 212,165 primary care visits at two US sites.

Process step that broke down
Share of errors
The patient–practitioner encounter itself
78.9%
— ordering diagnostic tests
57.4%
— history-taking
56.3%
— physical examination
47.4%
Referrals
19.5%
Patient-related factors
16.3%
Follow-up and tracking of results
14.7%
Test performance or interpretation
13.7%
43.7% of cases involved more than one process. The encounter, not the laboratory, is where primary care diagnosis fails — and within the encounter, the history is the single most frequently implicated step.
Where diagnostic cues actually come from
Donner-Banzhoff et al. (Med Decis Making 2017) video-recorded 134 consultations (163 diagnostic episodes) by 12 experienced German GPs and coded every question into one of four strategies. This is the closest thing in the literature to a specification for the agent's questioning engine.

Strategy
What it is
Used in
Share of diagnostic cues
Inductive foraging
Patient-guided open search — the patient leads the clinician to the relevant problem areas
91% of consultations
31%
Descriptive questions
Physician-controlled probing of detail on symptoms already mentioned
84% of episodes
25%
Triggered routines
Closed questions systematically exploring a problem area or organ system
38% of episodes
12%
Hypothesis testing
Closed questions aimed at confirming or excluding a specific disease
39% of episodes
12%
Inductive foraging — open, patient-led, hypothesis-free — produces more diagnostic cues than any other strategy, and more than the two closed strategies combined. The implication runs directly against how history taking is usually taught and structured: the undirected phase is the productive one, and it is the phase most often shortened.
When to stop the open phase
There is no direct medical evidence on symptom saturation as a stopping rule. The nearest evidence base is qualitative methodology, where the same problem — when have you heard everything? — has been measured empirically.
Hennink et al. distinguish two thresholds:

Code saturation — no new topics appear. Typically reached by about 9–12 interviews.

Meaning saturation — no new dimensions or nuances of already-named topics appear. Requires substantially more, with some codes still developing past 24 interviews.
Translated to a single consultation: the point at which a patient stops naming new symptoms (code saturation) arrives well before the point at which they stop adding detail that changes the meaning of symptoms already named (meaning saturation). A stopping rule set at symptom saturation alone will exit the open phase early relative to full information yield. This argues for two open thresholds rather than one — stop soliciting new problems when no new symptom appears across two or three differently-phrased invitations, but keep soliciting elaboration on named symptoms for longer.
Documentation loss compounds elicitation loss
Even when information is elicited, 31–45% of patient-reported symptoms never reach the clinical note (see Question form above). Elicitation failure and documentation failure are independent losses that multiply.
Consultation frameworks and what they are actually supported by
The frameworks taught in every medical school are consensus structures, not empirically derived ones. They are well validated as assessment instruments and as teaching scaffolds; they are weakly validated as interventions that change patient outcomes. That distinction should be made explicit in any work that grounds an agent in them.

Framework
Status of the structure
Status of the evidence
Calgary–Cambridge Guide
Expert consensus, derived from the communication-skills literature; five sequential phases (initiating, gathering information, examination, explanation and planning, closing) plus two continuous threads (providing structure, building the relationship), decomposed into ~70 discrete skills
Validated mainly as a rating instrument. A BMC Med Educ codebook study exists precisely because reliable operationalisation of the guide needed to be established separately from the guide itself. No trial shows the full guide outperforms an alternative structure on diagnostic outcomes.
Four Habits Model
Consensus model (invest in the beginning, elicit the patient's perspective, demonstrate empathy, invest in the end)
Best trial evidence of the frameworks. A crossover RCT of 72 hospital doctors (51 analysed) found a 20-hour course raised Four Habits Coding Scheme scores by 7.5 points (p=0.01) — but global patient satisfaction and consultation length were unchanged. Behaviour moved; the outcome did not.
Patient-centred approach (generic)
Family of models
Cochrane review of 43 RCTs: generally positive effects on consultation process, but "mixed results on satisfaction, behaviour and health status". Notably, training under 10 hours was as effective as longer training. Authors flag heterogeneity and single-item measures as limiting conclusions.
SOCRATES and symptom mnemonics
Teaching mnemonic, no derivation study
See Symptom-specific questioning below.
What this means for grounding an agent
Two honest readings follow.
First, the frameworks are the right scaffold and the wrong evidence claim. Calgary–Cambridge's phase structure is compatible with everything in the sections above — open before closed, explicit agenda, summarising, structured closing — and those individual components do have evidence. Adopt the structure because its components are supported, not because the framework as a whole has been validated.
Second, the process-outcome gap is the field's central weakness. Communication training reliably changes coded behaviour and unreliably changes anything a patient experiences. An agent's evaluation should therefore not stop at "the agent's transcript scores well on a Calgary–Cambridge rating" — that is the outcome the literature shows is easiest to move and least connected to benefit. Agreement with a clinician-taken history on clinically actionable content, as planned in the comparative study design, is a better primary endpoint than any process rating.
Symptom-specific questioning: mnemonics versus likelihood ratios
There are two quite different traditions here, and only one of them is evidence.
Mnemonics are teaching aids, not derived instruments
SOCRATES (Site, Onset, Character, Radiation, Associations, Time course, Exacerbating/relieving, Severity) has no derivation study, no named originator and no validation as a diagnostic instrument (overview). Its documented empirical finding is a negative one: clinicians using it rarely cover all eight dimensions.
That is not a reason to discard it. A mnemonic's job is completeness of coverage, and completeness is exactly the failure mode the error literature identifies. But it should be treated as a coverage checklist with unknown discriminative value, and an agent using it should not claim evidence-based questioning on that basis alone. The evidence sits one level down, in which specific answers shift probability.
Likelihood ratios are the evidence layer
Summerton's argument (see How much of the diagnosis comes from the history?) is the right frame: individual history features are mostly weak, and the value comes from combining them. Chest pain is the best-characterised example.

History feature
Direction
LR
Source
Pain radiating to both arms
Raises
LR+ 7.1
Panju 1998
Pain radiating to right shoulder
Raises
LR+ 2.9–4.7
Panju 1998; Swap 2005
Pleuritic pain
Lowers
LR− 0.2
Panju 1998
Sharp or stabbing quality
Lowers
LR− 0.3
Panju 1998
Positional pain
Lowers
LR− 0.3
Panju 1998
Pain reproduced by palpation
Lowers
LR− 0.3
Panju 1998
Compiled in ALiEM's review of the chest pain history, whose conclusion is the operative one: history alone can raise or lower probability but cannot exclude ACS without ECG and biomarkers. An agent that characterises chest pain well is doing triage input, not diagnosis.
Red-flag lists: sensitive, not specific
The SNNOOP10 secondary-headache red-flag list was tested prospectively in 100 ED headache patients in Madrid, with blinded questionnaire administration and blinded neurologist diagnosis at three months (Cephalalgia 2022).

Metric
Result
Sensitivity for high-risk headache
100% (95% CI 90.2–100)
Discrimination (AUC)
0.66
Most sensitive items
Neurologic deficit 75.5%; pattern change/recent onset 64.4%; age >50 64.4%
Most specific items
Post-traumatic onset 94.5%; cancer history 89.1%; systemic symptoms 89%
This is the archetypal red-flag performance profile and it is the right one for the agent's purpose: every dangerous case triggered at least one flag, at the cost of flagging many non-dangerous ones. A red-flag screen is a sensitivity instrument. Designing it for specificity would defeat its function, and the alert rate it generates has to be budgeted for at the triage desk rather than engineered down.
Practical consequence for the questioning library
The two layers should stay visibly separate in the symptom inventory:

Coverage questions — mnemonic-derived, ensure nothing is unasked. Justified by completeness and by the error data, not by diagnostic performance.

Discriminating questions — attached to a published LR or a validated rule where one exists, with the citation and the LR recorded against the question.

Red-flag questions — asked of everyone in the relevant symptom class, tuned to sensitivity, with the trigger threshold set deliberately low.
Where no LR exists for a symptom, that should be recorded as a gap rather than papered over with a plausible-sounding question set.
Risk, sensitive topics and safety-netting
Asking about suicide does not induce suicidal ideation
This is the single most important evidence finding for the decision to build direct risk questioning into the agent rather than routing to a human.
Dazzi et al. (Psychological Medicine 2014) reviewed 13 peer-reviewed studies (2001–2013) across high-school students, adolescents aged 12–17, adults seeking mental health treatment, people with serious mental illness, people with borderline personality disorder, and suicide-bereaved parents.

No study found a statistically significant increase in suicidal ideation after being asked about suicide.

High-school students asked about suicidality showed lower distress than controls (p=0.01).

Reductions in suicidal ideation and psychiatric symptoms were observed in several treatment-seeking samples.

Among suicide-bereaved parents, 94% found participation valuable; 2 of 1,043 reported lasting negative effects.
The authors' conclusion is that talking about suicide may reduce rather than increase ideation. The reasoning already applied to the agent — that not asking makes risk invisible rather than absent — is supported by this literature, and the iatrogenic-harm objection is not.
Machines get more honest answers about stigmatised topics
A meta-analysis of 48 independent samples, 125,672 participants, 460 effect sizes compared self-administered paper surveys with computerised modes.

Behaviour disclosed
Corrected OR (Ω)
p
Overall socially undesirable behaviour
1.19
<.05
Sexual behaviours
1.29
<.05
Substance use
1.17
<.05
Delinquent behaviours
1.14
.09
Victimisation
1.07
.22
The strongest moderator was privacy of administration: computerised surveys taken individually gave Ω = 1.61 versus 1.18 in group settings, explaining half the between-study heterogeneity.
Two design consequences follow. The disclosure advantage is real but modest, and it is largest for exactly the sensitive domains the agent needs — substance use, sexual health, and by extension self-harm. And it depends on perceived privacy: an ED room where the patient believes they can be overheard will forfeit most of the effect. Room design and an explicit statement about who will see the answers are not peripheral to this.
The converse also holds: the substance-use disclosure study in Question form above showed that a leading question destroys disclosure (RR 0.22) regardless of who or what is asking. Modality advantage does not survive bad phrasing.
Safety-netting is near-universally recommended and almost unevaluated
A BJGP literature review screened 9,949 articles and included 47; over half were expert opinion, 12 qualitative, 3 systematic reviews. The authors' headline finding is blunt: "the most compelling finding of this review is the lack of empirical research on safety netting."
The consensus components are nonetheless clear and directly implementable:

Communicate the uncertainty explicitly.

Name the specific worrying symptoms and red flags to watch for.

Give the likely time course of the illness.

Say how and where to seek further care.

Arrange planned follow-up where indicated.

Document it, and give it in writing.
An agent is unusually well placed on points 2, 3, 4 and 6 — it can deliver specific, written, per-symptom safety-netting advice consistently, which is precisely what human consultations do inconsistently. This is a plausible superiority claim for an agent rather than a non-inferiority one, and given the empty evidence base it is also a research opportunity.
Automated, computer-assisted and AI history taking
The literature splits cleanly into three generations, and they have different evidence profiles. Conflating them is the commonest error in this field.
Generation 1 — structured computer-assisted history taking (CAHT)
Form-based or expert-system questionnaires, no natural language. The evidence here is the most mature and the most favourable, because the claim is modest: better data capture, not better diagnosis.
A 2025 systematic review of 19 studies, 11,885 patients and 151 clinicians across emergency, anaesthetic, orthopaedic, oncology and surgical settings found:

Domain
Finding
Completion
>75% in five of seven reporting studies (8,887 patients); 51–67% in two smaller ones
Acceptability
Consistently high; >90% found systems easy to access; ease rated 8.0/10
Data completeness
Superior to usual care — one study captured 100% of primary pain locations versus 52% in the EHR
Consultation time
Mixed — reductions of 50–58.6% in some studies, 50% increases in others
Main barrier
Poor EHR integration
Weak point
Usability for elderly patients
The sharpest single study is a Swedish within-person comparison (PLOS One 2021): 410 ED chest-pain patients each had a physician history recorded in the EHR and a computerised history in the same visit.

52% of EHRs had no specific pain location; 55% had no radiation data. Computerised files were near-complete (409/410 captured all four dimensionality attributes).

Agreement was poor, in both directions: 80% of patients recorded in the EHR as having jaw/neck radiation denied it to the computer, and 50% with an explicit negative EHR entry reported radiation to the computer.
This matters directly for the planned comparative study. It predicts substantial disagreement between agent-elicited and clinician-elicited histories on the same patient, in both directions, and it means a disagreement is not automatically an agent error. The adjudication design — consultant review of both, blinded — is the right response, but the analysis should be set up expecting two-directional discordance rather than an accuracy ranking.
Generation 2 — symptom checkers
Rule-based or shallow-ML consumer triage apps. The evidence here is poor and should not be borrowed as support for an LLM agent.

Review
Finding
npj Digital Medicine 2022, 10 studies
Primary diagnosis accuracy 19–37.9%; top-3 accuracy 33–58%; triage accuracy 48.8–90.1%. Authors warn reliance "could pose significant patient safety hazards".
npj Digital Medicine 2025, 19 studies
Self-triage accuracy: apps 11.5–90.0%; LLMs 57.8–76.0% (GPT-4 71.3%); laypeople 47.3–62.4%. Apps 74.5% accurate on emergencies but 42.1% on self-care; LLMs 94.1% on non-emergencies but 10.8% on self-care.
Note the shape of the LLM failure: excellent at not missing emergencies, poor at confidently standing down. For an ED-adjacent agent whose escalation design is sensitivity-first, that failure mode is the tolerable one. For the GP booking-call version, where the agent's output may influence whether someone waits, it is less benign.
Generation 3 — LLM conversational diagnostic agents
AMIE, Nature 2025 — randomised, double-blind crossover remote OSCE. 159 case scenarios from Canada, UK and India; 20 board-certified primary care physicians as comparator; patient-actors consulted both in randomised order.

Significantly higher top-k diagnostic accuracy than PCPs at all values of k.

Rated superior by specialist physicians on 30 of 32 axes, and by patient-actors on 25 of 26 axes, including history-taking and empathy.

Authors' caveats are substantial: text chat is not how medicine is practised, the consultations were simulated, fairness and bias were not adequately assessed, and results "should be interpreted with caution".
The text-chat caveat is worth dwelling on, because the planned agent is voice. AMIE's advantage may partly be an artefact of a medium that lets a model deliberate without time pressure while constraining the human comparator to typing. Voice removes that asymmetry and adds ASR error, disfluency, interruption handling and latency — none of which AMIE's result speaks to.
Prospective clinical feasibility (preprint, 2026) — the first real-patient data. Single-arm, ambulatory primary care in Boston, April–November 2025; 100 patients enrolled, 98 completing both the AI conversation and the subsequent provider visit; all interactions under real-time physician oversight by video.

Outcome
Result
Safety stops required
0
Supervisor interventions
3, all minor clarifications
Patient attitudes to AI, pre vs post
Significantly improved (p<0.001)
Provider-rated helpfulness of output
75% of cases
Final diagnosis in AMIE's differential
90%; top-3 accuracy 75%
Diagnostic quality vs provider
Comparable (p=0.6); providers better on cost-effectiveness and practicality
This is a preprint, single-arm, 100 patients, with a clinician watching every conversation — it is a feasibility signal, not an efficacy result. But it is the closest published analogue to the planned deployment, and the structure it validates is precisely the one under consideration: a pre-visit AI conversation whose output is handed to the clinician who then sees the patient.
What none of this evidence covers

Voice. Every study above is text or form-based. There is no comparable evidence for voice-based history taking.

Undifferentiated presentation at first contact. AMIE's cases were scenario-based; the feasibility study was scheduled primary care, not walk-in ED.

Multilingual elicitation with cross-language handover. No located evidence on accuracy when the history is taken in one language and handed over in another.

The handover artefact itself. No study evaluates whether a narrative handover plus structured data improves clinician performance relative to structured data alone. That is an open and answerable question, and arguably the more novel one.
Teaching and training history taking
What is taught, and how well it works
Keifenheim et al. (BMC Med Educ 2015) systematically reviewed 23 studies (1990–2014) of history-taking instruction.

Approach
Studies
Verdict
Instructional — scripts, lectures, video demonstrations, online courses
3
Effective but least studied
Experiential — small-group workshops, role-play, simulated patients, virtual patients, real patients with feedback
17
Best evidenced; the recommended approach
Creative — improvisational theatre, Lego-based simulation
2
Promising, lower study quality
22 of 23 studies reported positive outcomes, which mostly reflects publication and design bias — mean quality score 10.4 (range 6.5–14). The authors' recommendation is small-group work combining role-play and real-patient interviews with feedback and discussion, with videotape feedback singled out as particularly instructive. They also note that pre-clinical students learn interview skills better when diagnostic reasoning is deliberately removed from the task.
The best-powered evidence: Cochrane
Gilligan et al. (Cochrane 2021) — 76 studies, 10,124 medical students, 42 in meta-analysis.

Communication-skills interventions may improve overall skills and empathy when rated by experts, but not when rated by simulated patients.

Tailored feedback probably beats generic feedback.

Online teaching matched face-to-face on empathy and rapport, but was possibly inferior for information-giving skills.

Simulated patients and peer role-play differed little on empathy.

Certainty: low to very low, from risk of bias and heterogeneity. No long-term outcomes; almost no real patients.
The expert-versus-simulated-patient divergence is the most important line in this review, and it mirrors the process-outcome gap in section 6: training reliably shifts what trained raters score, and does not reliably shift what the person on the other side of the conversation experiences.
Skills do not persist automatically
The Cochrane patient-centredness review found short training (<10 hours) as effective as longer training — which cuts both ways, since it suggests the effect is shallow rather than that teaching is efficient. A separate literature documents decline in patient-centred attitudes across clinical clerkships even in cohorts explicitly trained in communication skills (Bombeke et al. 2011), consistent with the everyday observation that the interruption behaviour in section 3 is learned on the wards, not in the classroom.
Implications
For teaching: use experiential small-group work with recorded review and individually tailored feedback, teach interview skills separately from diagnostic reasoning early on, and expect decay — build refreshers into the clinical years rather than front-loading.
For the agent: three things transfer directly.

Tailored feedback beats generic feedback. An agent that logs its own transcripts can deliver exactly this to clinicians — and can do it against their own consultations, which is the scarce resource in communication teaching.

Recorded review is the highest-yield teaching modality and the most expensive. An agent generates recordings and structured coding of them as a by-product.

An agent does not decay. Whatever questioning discipline is built in is applied identically at 3am on the twelfth consecutive patient. Consistency, not peak performance, is the most defensible claim an agent can make against a human comparator — and the comparative study should be powered to detect it (variance, not just mean agreement).
Evidence gaps and methodological weaknesses
For a field that underpins most of clinical medicine, the evidence base is surprisingly thin. Five weaknesses recur.
1. Process outcomes substitute for patient outcomes. Almost every interventional study measures coded behaviour, rating-scale scores or information counts. The Four Habits RCT moved coding scores by 7.5 points and patient satisfaction not at all; Cochrane found improvement when experts rated and none when simulated patients rated. No study in this review demonstrates that a change in history-taking technique changed morbidity, mortality, length of stay or time to diagnosis.
2. The foundational numbers were never replicated at scale. The "80% from history" literature is six small studies across 60 years, none randomised, never systematically reviewed, with sample sizes of 80–630 and no shared operational definition of "diagnosis made by history".
3. Frameworks are consensus dressed as evidence. Calgary–Cambridge and SOCRATES are taught with the authority of validated instruments and have none of the supporting derivation work. The components have evidence; the frameworks do not.
4. Almost nothing is symptom-specific. The general interviewing literature says "ask open questions first"; it does not say which questions, for which symptom, in which order, with what yield. The likelihood-ratio literature that would answer this exists only for a handful of presentations — chest pain, headache, a few others — and is sparse or absent for most of a general symptom inventory.
5. Voice is unstudied. Every automated history-taking study located here is form-based or text-chat. There is no evidence base for voice-elicited histories, and the differences are not cosmetic: turn-taking, interruption handling, silence tolerance, prosody as a cue, ASR error on symptom vocabulary and accents, and the absence of a scroll-back for the patient.
Specific unanswered questions this project could answer

Question
Why it is answerable here
Does symptom saturation, as a stopping rule, capture as much as a fixed comprehensive schedule?
Directly testable by randomising stopping rules against a fixed-schedule arm in simulation
Which open-question phrasings pull the additional symptom?
Already planned. Heritage's "some/any" result proves the effect exists and is large; no one has systematically mapped the phrasing space, and an agent can randomise at a scale no human trial can
Does a narrative handover plus structured data outperform structured data alone for clinician decision-making?
No located study addresses this. It is a clean two-arm question with clinician performance as the outcome
Does the disclosure advantage of machines extend to voice, and to risk questioning specifically?
The meta-analytic effect is established for text and forms only; voice may lose the privacy advantage or amplify it
Does accuracy hold when the history is taken in one language and handed over in another?
No located evidence at all
Does an agent reduce the 31–45% documentation loss of patient-reported symptoms?
A measurable, high-value, low-controversy endpoint
Design implications for the agent
Each rule is traced to its evidence. Where a rule rests on consensus or on transfer from another field, that is stated rather than hidden.
Rules with direct empirical support

#
Design rule
Evidence
1
Architect the questioning engine as an open-to-closed cone, not as open questions followed by a checklist. The gradual narrowing itself predicts yield, independently of duration.
Takemura 2007: F=40.1, p<0.0001, adjusted for interview length
2
Let the patient lead the opening entirely — no clinician-derived structure until they stop volunteering. Inductive foraging produced 31% of all diagnostic cues, more than both closed strategies combined (24%).
Donner-Banzhoff 2017, 163 diagnostic episodes
3
Do not cap the opening statement. Budget two minutes: mean spontaneous talking time is 92 s and 78% finish within two minutes.
Langewitz 2002, n=335
4
Use facilitators ("mm-hm", "go on") rather than questions during the open phase — they independently predict information yield.
Takemura 2007: F=15.3, p<0.0001; Beckman & Frankel 1984
5
Ask "Is there something else?" — never "anything else".
Heritage 2007: 78% reduction in unmet concerns (OR 0.154, p=0.001); "anything" non-significant
6
Summarise back mid-interview, before narrowing. This elicits further information, not merely confirmation.
Takemura 2007: F=5.57, p=0.019
7
Never phrase a screening question toward the negative ("no chest pain?", "you're not still…?").
HIV disclosure study: leading-toward-non-use RR 0.22; closed RR 0.60
8
Use normalising preambles for stigmatised domains, and state explicitly who will see the answers. The machine-disclosure advantage depends on perceived privacy.
Disclosure meta-analysis: Ω 1.19 overall, 1.29 sexual behaviour; individual administration Ω 1.61 vs group 1.18
9
Ask risk questions directly, including self-harm, in both settings. Route-to-human is not the safer option.
Dazzi 2014: 13 studies, no significant increase in ideation; several showed reduction
10
Tune red-flag screens for sensitivity and accept the alert burden.
SNNOOP10: 100% sensitivity for high-risk headache at AUC 0.66
11
Deliver per-symptom safety-netting in writing: uncertainty, specific red flags, expected time course, where to seek care.
BJGP review: consensus components; the review's own finding is that empirical evaluation is absent — so this is also a research opportunity
12
Capture structured data at elicitation. Do not rely on downstream transcription.
31–45% of patient-reported symptoms never reach the note (Mayo, n=1,119); 52% of ED chest-pain EHRs lacked pain location vs near-complete computerised capture (Stockholm, n=410)
Rules resting on inference rather than direct evidence
These are defensible but should be flagged as design hypotheses, and ideally tested.

Two saturation thresholds, not one. Stop soliciting new problems when no new symptom appears across two or three differently-phrased invitations; keep soliciting elaboration on named symptoms for longer. Transferred from the code-saturation/meaning-saturation distinction in qualitative methodology, not demonstrated in consultations.

Separate coverage questions from discriminating questions in the symptom library. Record a likelihood ratio and citation against every discriminating question; record an explicit gap where none exists. Justified by Summerton's argument, not by a trial.

Do not evaluate the agent primarily on a communication-rating scale. Process ratings are the outcome the literature shows is easiest to move and least connected to benefit — the Four Habits RCT moved coded behaviour by 7.5 points with zero change in patient satisfaction, and Cochrane found improvement on expert ratings but not simulated-patient ratings.
Version-specific implications

Consideration
GP booking call
ED room
Disclosure conditions
Patient is at home, alone, on their own phone — close to the individual-administration condition that gave the largest disclosure advantage (Ω 1.61)
Room privacy is a design requirement, not a nicety; an overheard conversation forfeits most of the effect
Triage failure mode that matters
LLMs are poor at confidently standing down (10.8% accuracy on self-care advice). The agent must not be the thing that decides someone can wait
Sensitivity-first escalation is aligned with the known LLM strength (94.1% on identifying non-emergencies)
Nearest validated analogue
The Boston feasibility study — pre-visit AI conversation, output handed to the clinician who then sees the patient. 0 safety stops, 90% of final diagnoses in the differential, patient attitudes improved (p<0.001)
No published analogue. Undifferentiated walk-in presentation is unstudied
Comparator framing
The honest comparator is the status quo, where none of this information exists at booking. Non-inferiority against a doctor is the wrong frame
Comparator is a real clinician history on the same patient — the planned design
Implications for the planned comparative study

Expect two-directional disagreement, and design for it. The Stockholm study is the warning: 80% of patients recorded in the EHR as having jaw/neck radiation denied it to the computer, and 50% with an explicit negative EHR entry reported it to the computer. Discordance is not the same as agent error, and the adjudication protocol should let a consultant record "agent right, clinician wrong" as a distinct outcome.

Measure variance, not only mean agreement. Consistency is the most defensible advantage an agent has over a human comparator — no decay across a shift, no drift from the protocol.

Add a documentation-loss endpoint. Comparing agent-captured symptoms against what reaches the clinical note is a clean, high-value, low-controversy measurement with a published baseline (31–45%).

Treat the handover format as a testable arm, not a fixed design choice. Whether narrative-plus-structured beats structured-alone for clinician decision-making is unstudied, answerable, and probably the more novel contribution.

Do not let voice ride on text evidence. Every result in section 9 is text or form-based. The voice layer needs its own accuracy work — particularly ASR performance on symptom vocabulary, accented English and the target non-English languages.
One caution
The strongest findings in this review are about what clinicians do badly: interrupt at 11 seconds, solicit an agenda in 36% of encounters, ask leading questions about substance use, lose a third of reported symptoms before the note. An agent that simply does not do those things will look good against a human comparator, and that comparison is fair. But it is a comparison against degraded practice under time pressure, not against good history taking. Being explicit about which claim is being made will make the work considerably harder to dismiss.
Sources
All pages below were opened and read. Where only an abstract was accessible, findings are reported at that level.
Diagnostic contribution of the history

Hampton JR et al. Relative contributions of history-taking, physical examination, and laboratory investigation. BMJ 1975 — PubMed

Peterson MC et al. Contributions of the history, physical examination, and laboratory investigation. West J Med 1992 — PubMed

Platt, Sandler, Roshan & Rao, Wang — compiled in A History of Patient History-Taking, Clinical Correlations, NYU 2022

Summerton N. The medical history as a diagnostic technology. BJGP 2008 — bjgp.org

Paley L et al. Utility of clinical examination in ED admissions. Arch Intern Med 2011 — JAMA Network; commentary

Simulator RCT of history quality and diagnostic accuracy in simulated PE — Signa Vitae 2023

80% of Diagnosis is History Taking. Myth or Fact? — secondary compilation
Interview structure, interruption and agenda

Beckman HB, Frankel RM. The effect of physician behavior on the collection of data. Ann Intern Med 1984 — ACP Journals

Marvel MK et al. Soliciting the patient's agenda: have we improved? JAMA 1999 — JAMA Network; summary

Singh Ospina N et al. Eliciting the patient's agenda. J Gen Intern Med 2019 — Springer

Langewitz W et al. Spontaneous talking time at start of consultation. BMJ 2002 — PDF

Heritage J et al. Reducing patients' unmet concerns: the difference one word can make. J Gen Intern Med 2007 — Springer
Question form and disclosure

Takemura Y et al. Open-ended questions: are they really beneficial? Tohoku J Exp Med 2005 — J-Stage

Takemura Y et al. Identifying medical interview behaviors that best elicit information. 2007 — PubMed

Norwegian Institute of Public Health. Accuracy of open-ended questions in structured conversations with children. 2019 — PDF

Open-ended and normalizing questions and substance-use disclosure in HIV care — BU AOD Health

GPSA. Open versus closed questions information sheet — PDF

Agreement between patient-reported symptoms and medical record documentation. Am J Manag Care 2008 — AJMC
Error, cues and stopping rules

Singh H et al. Types and origins of diagnostic errors in primary care. JAMA Intern Med 2013 — PDF

Donner-Banzhoff N et al. The phenomenology of the diagnostic process. Med Decis Making 2017 — PDF

Hennink M et al. Code saturation versus meaning saturation — seminar slides, UCSD
Frameworks

Codebook for rating clinical communication skills based on the Calgary–Cambridge Guide. BMC Med Educ 2020 — Springer

Short course in clinical communication skills for hospital doctors: crossover RCT — PubMed

Lewin S et al. Interventions for providers to promote a patient-centred approach. Cochrane — plain summary
Symptom-specific questioning

SOCRATES (pain assessment) overview

Chest pain history likelihood ratios (Panju 1998; Swap 2005; Body 2010; Goodacre 2002), compiled — ALiEM

García-Azorín D et al. Sensitivity of the SNNOOP10 list. Cephalalgia 2022 — SAGE
Risk, disclosure and safety-netting

Dazzi T et al. Does asking about suicide induce suicidal ideation? Psychol Med 2014 — PDF

Disclosure of sensitive behaviors across self-administered survey modes: meta-analysis. Behav Res Methods 2015 — Springer

Safety netting for primary care: evidence from a literature review. BJGP 2019 — bjgp.org
Automated and AI history taking

Computer-assisted history taking in elective and acute care: systematic review. 2025 — ScienceDirect

Computerized history-taking improves data quality: EHR vs computer-acquired history in chest pain. PLOS One 2021 — PLOS

Diagnostic and triage accuracy of digital symptom checkers: systematic review. npj Digit Med 2022 — Nature

Kopka M et al. Accuracy of symptom assessment apps, LLMs and laypeople for self-triage. npj Digit Med 2025 — Nature

Towards conversational diagnostic artificial intelligence (AMIE). Nature 2025 — Nature

Prospective clinical feasibility study of a conversational diagnostic AI — arXiv preprint, 2026 (preprint, not peer reviewed)
Teaching

Keifenheim KE et al. Teaching history taking to medical students: a systematic review. BMC Med Educ 2015 — PDF

Gilligan C et al. Interventions for improving medical students' interpersonal communication. Cochrane 2021 — Cochrane Library; plain summary

Bombeke K et al. Medical students trained in communication skills show a decline in patient-centred attitudes. Patient Educ Couns 2011 — PubMed
Pages that could not be read
PubMed Central, Europe PMC, Tandfonline and Wiley returned CAPTCHA, robots or 403/429 responses. Where this happened, the finding was sourced from an alternative accessible version and cited to that version, except for two items not retrieved at all: the full text of Paley 2011 (reported from the JAMA landing page and the AHRQ PSNet summary) and the full text of Krupat 2017 on premature closure (not used).