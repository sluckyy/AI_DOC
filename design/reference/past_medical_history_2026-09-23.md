# Reference: Past Medical History — Evidence Base and Question Set

Source: the product owner's Claude Doc, https://claude.ai/artifact/Uf2Ls7Y7TbqYCNijLoaZye (as of 2026-09-23). Plain-text extract; tables and diagrams flattened. The live doc is the source of truth.

---


Past Medical History — Evidence Base and Question Set
 · 
There is no direct evidence that screening for past medical history changes diagnosis: no study isolates it as a component of the history. The section is justified by its downstream uses, and its yield depends almost entirely on how it is asked — which is where an agent has an advantage over a clinician under time pressure.
The evidence position
The studies that established "the history gives most of the diagnosis" never decomposed the history. [Hampton 1975] (66 of 80 medical outpatients), [Peterson 1992] (76%), Sandler 1980 (56%), Roshan & Rao 2000 (78.6%) and [Paley 2011] (~80% of ED admissions) all treat it as a single block. None reports presenting complaint, past history, medications and social history separately, and none attributes a diagnosis to a component. [Summerton's review] accepts the headline figure while noting the field never measured the history's operating characteristics.
The nearest thing to a measured screening yield comes from the review of systems, and it is unflattering. [Verdon & Siemens 1997] put 20 screening questions to 248 new adult patients: 785 positive answers produced 26 new diagnoses — 10.5% yield per patient but 3.3% positive predictive value per positive answer, with seven questions yielding nothing at all. [Mitchell 1992] found 26 new diagnoses across 550 admissions, of which 2 plausibly changed survival.
So the section is not justified as a diagnostic screen. It is justified by four downstream uses, three of which have decent evidence:

Medication and allergy safety. The strongest strand. [Tam 2005] found 10–67% of admitted patients had at least one medication history error, 11–59% clinically important. A wrong allergy label carries measurable harm: in [Blumenthal 2018], 301,399 matched UK adults, a penicillin allergy label gave adjusted HR 1.69 for MRSA and 1.26 for C. difficile.

Conditional probability within a presentation. Past history modifies pre-test probability once a complaint exists. In [Downie 2013], a history of cancer in back pain gives a post-test probability of 33% (22–46) in ED but only 7% (3–16) in primary care — the same answer, ten times the meaning, by setting.

Risk scores and disposition. Wells, PERC, HEART, CHA₂DS₂-VASc and the Canadian Syncope Risk Score all carry past-history items with independent weight.

Closing an information gap. [Stiell 2003] found information gaps in 32.2% of 1,002 ED visits, the missing item being medical history in 58% of them and judged essential in 47.8%; gaps added 1.2 hours to length of stay.
What follows is built on that position: cover the routes that feed those four uses, and stop asking questions whose only justification is completeness.
The five retrieval routes
Questions like "any ongoing medical problems", "ever been in hospital", "do you see a doctor for anything" and "any regular medicines" all aim at the same target, but they are not rephrasings of one question. They are different retrieval routes, and the routes recover systematically different conditions.
The proof is in the agreement data. Rheumatoid arthritis has κ 0.25 and 17.5% sensitivity by self-label ([Hale 2020], 964 community-dwelling adults aged 75+) — yet those same patients will name a rheumatologist and a weekly methotrexate dose. Heart failure sits at κ 0.46 by label ([Okura 2004]) but is reliably reachable through frusemide. The route determines the miss.

 | 
Route | 
What it recovers well | 
What it misses | 
Why it earns a slot
 | 
Self-label — "what health problems are you dealing with?" | 
Conditions the patient owns as an identity: diabetes, hypertension, asthma, epilepsy | 
Label-ambiguous and silent conditions; anything the patient was told once and did not retain | 
Fastest route to the majority of active problems; κ 0.83 for diabetes in [Lin 2023]
 | 
Treatment — "what medicines do you take, and what is each one for?" | 
Treated-but-unlabelled conditions; the drug list itself | 
Diet-controlled, remitted or surveillance-only conditions | 
Highest-yield route, and the one with real evidence behind it; also the safety deliverable in its own right
 | 
Event — admissions, operations | 
Discrete, memorable, dated events; surgical anatomy that changes later reasoning | 
Chronic conditions never requiring admission | 
Anchored recall; patients date events better than diagnoses
 | 
Care contact — "which doctors, clinics or therapists do you see?" | 
Specialist-managed conditions the patient cannot name; allied health involvement; functional problems | 
Conditions managed entirely in general practice | 
Recovers exactly the conditions the self-label route loses (the rheumatologist test)
 | 
Surveillance — "is anyone keeping an eye on anything — regular blood tests, scans, scopes?" | 
Monitored-but-untreated: early CKD, small AAA, Barrett's, a lung nodule, hepatitis B, a watched aneurysm | 
Little — but has the lowest hit rate, so it goes late | 
The only route that reaches conditions with no label, no drug and no admission
The fifth route is the one missing from the usual clerking structure. A patient under surveillance has nothing to report on any of the other four routes: no name for it, no tablet, no operation, and they may not count a six-monthly scan as "seeing a doctor for a problem".
Two questions from the conventional set do not earn a slot. "Have you ever had to see a doctor for anything" is answered yes by essentially everyone, so it discriminates nothing and generates precisely the low-PPV noise Verdon measured. "Have you ever taken any regular medicines" is weak standing alone but valuable as a follow-up thread — see the tense rule below.
Tense: when "ever" earns its place
Asking every route twice — once for now, once for ever — doubles the interview and is where most of the apparent redundancy in a conventional question list comes from. "Have you ever had any medical problems" as a free-standing question mostly returns childhood tonsillitis.
The rule: ask every route in the present tense, and add a lifetime sweep only where the past changes current management. Four places qualify.

 | 
Lifetime sweep | 
Wording | 
Why the past matters
 | 
Stopped medicines | 
"Anything you were taking and have stopped, or finished a course of?" | 
Ceased anticoagulant, recent steroid course, completed chemotherapy, a drug stopped for a reaction — all change current reasoning
 | 
Cancer | 
"Have you ever been treated for cancer, even years ago?" | 
The single highest-weight past-history red flag: [post-test probability 33% for spinal malignancy in ED]
 | 
Operations | 
"Any operations, however long ago?" | 
Altered anatomy is permanent; previous abdominal surgery, splenectomy, valve or joint prosthesis, bariatric surgery
 | 
Admissions | 
"Have you ever been in hospital overnight — what for?" | 
Recovers severity the patient does not otherwise convey, and anchors dates
Everything else is asked in the present. The event routes (operations, admissions) are inherently lifetime, so they carry no separate present-tense form.
One exception applies regardless of tense: where the library already specifies that elapsed time never de-escalates — bat exposure, and wounds and bites — the lifetime form is mandatory and the finding is actionable however distant.
The question set
Routes run in this order. The ordering is deliberate: self-label first because it is fastest and most patients have something ready; treatment second because it is the highest-yield route and converts drugs into diagnoses; surveillance last because its hit rate is lowest.
1. Self-label — present
"What health problems are you dealing with at the moment?"
Follow-up threads: for each condition named — how long, who looks after it, is it settled or causing trouble lately. Do not correct the patient's label at this stage; record it as given and reconcile later.
2. Treatment — present, then the conversion
"What medicines do you take regularly? Include inhalers, injections, patches, eye drops, and anything you buy yourself."
then, for each: "What's that one for?"
The conversion step is the most important question in the section. It recovers conditions the patient cannot name, which is exactly the population the self-label route loses. It is also the only part of this section with trial-grade support: structured, protocolised medication history produced 28 discrepancies across 106 patients (2% of prescriptions) versus 287 (27%) for physician-obtained history in [Henriksen 2015].
Mandatory sub-probes: anticoagulants and antiplatelets asked explicitly by name and by purpose ("anything to thin your blood?"), steroids, immunosuppressants, insulin, opioids. Then the allergy question, recording what happened rather than the drug name alone.
3. Event — lifetime
"Have you ever been in hospital overnight? What for?"
"Any operations, however long ago?"
Follow-up threads: approximate year, which hospital, any complications, anything left in place (stents, mesh, prosthesis, pacemaker).
4. Care contact — present
"Which doctors or clinics do you see regularly, apart from your GP?"
"Anyone else — physio, psychologist, podiatrist, dietitian, anyone like that?"
Follow-up thread: for each, what they are seeing them about. Named exemplars belong here as prompts within one question, not as separate questions — they work as retrieval cues, and [prompting roughly doubled reporting] in the one randomised comparison of structured versus open-ended elicitation.
5. Surveillance — present
"Is anyone keeping an eye on anything — regular blood tests, scans, or scopes you go back for?"
Follow-up thread: what is being watched, how often, when the last one was, whether anything was found.
6. Lifetime sweep
The four questions from the tense table: stopped medicines, cancer, operations (already covered at route 3, skipped if answered), admissions (same).
7. Named-condition sweep
Run only for conditions not already surfaced by routes 1–6 — see the next section.
8. Catch-all
"Is there anything in your medical history you think I should know about that I haven't asked?"
Cheap, and it closes the section on the patient's own judgement rather than the agent's checklist.
Named-condition sweep
Some conditions are both high-consequence and poorly self-reported. For these the agent asks by name at the end of the section — but using a lay anchor, not the medical label, because the label is precisely what fails.
The pattern across the agreement literature is consistent: specificity is high, sensitivity is variable. Patients rarely invent conditions; they routinely fail to report ones they have. [Lin 2023], a meta-analysis of 27 studies, concluded that patient-reported comorbidity is poor-to-moderately reliable except for endocrine disease, and "should be avoided as a standalone measure".

 | 
Condition | 
Agreement by self-label | 
Lay-anchored wording
 | 
Diabetes | 
κ 0.83 (0.80–0.86), Lin 2023 | 
Label works — no anchor needed
 | 
Hypertension | 
κ 0.30–0.82, Lin 2023 | 
"Are you on anything for blood pressure?"
 | 
Atrial fibrillation | 
κ 0.69, sensitivity 65% ([Zeynalova 2025]); κ 0.28 in [Coste 2025] | 
"Has anyone told you your heart beats irregularly, or that you have an irregular pulse?"
 | 
Heart failure | 
κ 0.46, sensitivity 69% (Okura 2004); κ 0.26, sensitivity 20% (Zeynalova 2025) | 
"Do you take fluid tablets? Have you ever been admitted with fluid on the lungs or swollen legs?"
 | 
Ischaemic heart disease | 
MI κ 0.36–0.75, Lin 2023 | 
"Have you ever had a heart attack, a stent, or bypass surgery?"
 | 
Stroke or TIA | 
κ 0.34–0.55, Lin 2023; PPV 27% ([Darvishian 2022]) | 
"Have you ever had a stroke, or a mini-stroke where the weakness or speech trouble went away?"
 | 
Chronic kidney disease | 
κ 0.52, single estimate, Lin 2023 | 
"Has anyone told you your kidneys don't work as well as they should?"
 | 
COPD or asthma | 
κ 0.29–0.83 across studies; COPD κ 0.38, sensitivity 35% (Darvishian 2022) | 
"Do you use any puffers or inhalers?"
 | 
Cancer | 
κ 0.22–0.92, Lin 2023 | 
"Have you ever been treated for cancer — surgery, chemotherapy or radiotherapy?"
 | 
Immunosuppression | 
Not separately studied | 
"Are you on steroids, methotrexate, or anything that affects your immune system? Have you had your spleen removed?"
 | 
Bleeding or clotting | 
Not separately studied | 
"Do you bleed or bruise easily? Have you ever had a clot in the leg or lung?"
 | 
Rheumatoid arthritis | 
κ 0.25, sensitivity 17.5% (Hale 2020) | 
"Do you see a rheumatologist? Are you on methotrexate or anything like it?"
 | 
Pregnancy | 
— | 
Per the library's existing shared gating rule
Two cautions on interpreting these numbers.
The record is not a gold standard. Disagreement runs in both directions. [Violan 2013] compared 15,926 survey interviews against 1,597,258 electronic records in Catalonia and found self-reported morbidity exceeded the record for 80% of health problems; multimorbidity was 60% by survey against 43% by record. [Corser 2008] found the same direction in 525 ACS inpatients: mean 1.78 comorbidities by self-report against 1.27 by record, self-report exceeding the record for every condition except heart failure and renal disease. Where the agent's history and the record disagree, the handover should show both rather than resolving silently.
Accuracy degrades in exactly the populations the agent will meet. Age, education, multimorbidity and cognitive impairment are the most replicated modifiers (Lin 2023, Hale 2020). In an ED trauma unit, [only 15.4% of patients aged 75 and over] could supply the necessary history without documents or a third party. No well-powered validation study of ED-obtained past medical history against a reference standard appears to exist — a gap directly relevant to version two.
Saturation here differs from the symptom rule
The library's symptom rule is saturation by rephrasing: keep asking open questions in different words until the patient stops producing new symptoms. That works because the rephrasings are near-equivalent probes of the same memory.
Past medical history is not like that. The routes are categorically different, so rephrasing within a route hits diminishing returns quickly while switching route can still produce a major condition. The stopping rule therefore has two levels:

Within a route, work it until it stops producing — including one rephrasing, since a patient who says "no" to "any health problems" often says yes to "anything you see the doctor about".

Across routes, do not stop early. Run all five regardless of how much the first one produced. A productive self-label route is not evidence that the surveillance route will be empty — it is the routes' independence that makes them worth running.

Stop the named-condition sweep at the conditions already surfaced. If frusemide appeared at route 2, do not ask the heart failure anchor.
The cost of running all five is interview length, not clinician time — which is the structural advantage here. A clinician choosing between the self-label question and the care-contact question is rationing; the agent is not. Against that, [computer-assisted history takes about 5–6 minutes] for a focused history and patient acceptability is consistently high, so the binding constraint is patient tolerance and it should be measured rather than assumed. Bail-out rules from the library's cross-cutting section apply unchanged: cognitive impairment, distress, or a patient who is simply unwell ends the section early and flags what was not covered.
Sequencing in the handover
Collecting past history well creates a problem the section has to answer: where it appears in the handover changes what the clinician concludes.
[Yamauchi 2019] randomised 207 residents across five hospitals to vignettes with or without additional patient information, counterbalanced. Adding a past diagnosis of schizophrenia significantly reduced diagnostic accuracy (partial η² 0.063) and sharply reduced rated likability (partial η² 0.378), with lower likability tracking reduced resource allocation. At population scale, [Liberati 2025] reviewed 79 studies: of 37 with comparator groups, 29 showed increased under-diagnosis or delayed diagnosis in people with mental illness, including adjusted OR 1.48 for missed myocardial infarction.
The obvious mitigation does not work. [Sherbino 2014] randomised 191 students to cognitive forcing strategy training and found no reduction in diagnostic error on any bias type. Telling the clinician to beware of anchoring is not a control.
What an agent can do instead is control presentation order, which a paper chart cannot:

The handover narrative leads with the presenting complaint and its own findings, as a registrar's would. Past history follows; it does not open the summary.

Past psychiatric diagnoses are not omitted — that would be unsafe and would defeat the mental health section — but they sit with the rest of the past history rather than in the opening line, and are not used as a framing descriptor for the patient.

The structured data layer beneath the narrative carries everything, unordered and complete, for the clinician who wants it.

Where the past history item is doing genuine diagnostic work in this presentation — prior DVT in a swollen leg, prior cancer in back pain, prior cardiac workup in chest pain — it is promoted into the presenting-complaint narrative, because there it is a likelihood ratio rather than a label.
That last rule aligns with what the library already says under leg swelling and chest pain: medication and past cardiac workup are diagnostic content for those rows, not background, and should be pulled forward.
This is a design position, not an evidence-based one. No study has tested handover ordering as an intervention. It should be flagged to reviewers as such.
What to log
The library already commits to logging which open-question phrasing pulls the extra symptom. Here that logging is worth more, because the routes are categorically different rather than rephrasings, so the log produces a route-by-condition yield table — a direct measurement of something not currently in the literature.
Minimum fields per condition elicited:

Which route first surfaced it, and at which question within that route

Whether any later route independently surfaced it (route overlap)

Whether it came from free recall or from the named-condition sweep

Whether it was present in the record, absent from the record, or contradicted by it

Time cost of each route
Two results fall out of this with no extra study machinery.
Per-route incremental yield. What each route adds over the routes before it. If the surveillance route adds nothing across a few hundred histories, it should be dropped; if it adds one significant condition in twenty, it stays. This is the empirical answer to the question that prompted this section.
Free recall versus prompted elicitation for past medical history. The named-condition sweep at step 7 is, in effect, the prompted arm running after the free-recall arm in every patient. [Gama 2009] is the only randomised comparison of structured versus open-ended elicitation and it is a medication study — reporting of two or more drugs rose from 43.0% to 66.2% with prompting. No equivalent exists for past medical history. A within-patient design here would produce it as a by-product of normal operation.
One methodological caution worth carrying into any comparison against clinicians. The existing computer-history studies benchmark against clinician documentation, not against what the clinician actually elicited — [Zakim 2021] found primary pain location absent or imprecise in 213 of 410 emergency department records, and complete entries for four key chest pain attributes in 3 of 410 records against 409 of 410 computer histories. That gap partly measures documentation practice rather than history-taking skill. The adjudicated-agreement design already planned for this project avoids that trap and should be described as doing so explicitly.
Open questions for reviewers

Should the GP booking-call version and the ED version run the same five routes? The Downie finding argues they should not — the same past-history answer carries very different weight at different prevalence — but running a reduced set in general practice risks missing the one patient it mattered for.

Is the named-condition sweep acceptable to patients, or does it read as an interrogation after five routes of open questioning?

Where should the anticoagulation question sit? It is currently inside the treatment route, but the library flags it as disposition-changing for several presentations, which argues for asking it earlier.

Does the surveillance route survive contact with real patients, or do people simply not know what is being watched?

Is withholding a past psychiatric diagnosis from the opening line of the handover defensible, or does it read as concealment to a clinician who later finds it in the structured layer?

For the non-English versions: the lay anchors above are English idiom. "Fluid tablets" and "mini-stroke" do not translate directly, and the anchors will need to be built per language rather than translated.
Sources
Pages opened for this section.
Contribution of the history

[Hampton et al. 1975, BMJ] · [Peterson et al. 1992, West J Med] · [Paley et al. 2011, Arch Intern Med] · [Summerton 2008, BJGP]
Screening yield

[Verdon & Siemens 1997, J Am Board Fam Pract] · [Mitchell et al. 1992, J Gen Intern Med] · [Downie et al. 2013, BMJ]
Accuracy of self-reported history

[Lin et al. 2023, Postgrad Med J] · [Okura et al. 2004, J Clin Epidemiol] · [Hale et al. 2020, Age Ageing] · [Darvishian et al. 2022, Front Epidemiol] · [Zeynalova et al. 2025, Arch Public Health] · [Coste et al. 2025, Eur J Public Health] · [Violan et al. 2013, BMC Public Health] · [Corser et al. 2008, BMC Health Serv Res] · [Lindner et al. 2015, Emerg Med Int]
Elicitation method and automated history

[Gama et al. 2009, BMC Med Res Methodol] · [Zakim et al. 2021, PLOS ONE] · [Benaroia et al. 2007, Int J Med Inform] · [Berdahl et al. 2022, JMIR] · [Sourial et al. 2024, Ann Fam Med]
Medication, allergy and information gaps

[Tam et al. 2005, CMAJ] · [Henriksen et al. 2015, Int J Clin Pharm] · [Blumenthal et al. 2018, BMJ] · [Stiell et al. 2003, CMAJ]
Bias from prior diagnoses

[Yamauchi et al. 2019, BMC Med Educ] · [Liberati et al. 2025, eClinicalMedicine] · [Sherbino et al. 2014, CJEM]
Cited by verified citation only — full text not retrievable during this pass, so no figures are attached to them: Sandler 1980 (Am Heart J 100:928–31), Roshan & Rao 2000 (JAPI 48:771–5), Harlow & Linet 1989 (Am J Epidemiol 129:233–48), Kriegsman et al. 1996 (J Clin Epidemiol), Zakim et al. 2008 (BMC Med Inform Decis Mak 8:50).