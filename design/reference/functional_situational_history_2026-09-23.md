# Reference: Functional & Situational History — Evidence Base

Source: the product owner's Claude Doc, https://claude.ai/artifact/8nr97sPdCRjZ5obph9F5m5 (as of 2026-09-23). Plain-text extract; tables flattened. The live doc is the source of truth.

---


Functional & Situational History — Evidence Base
 · 
Scope
The evidence here is strong for why functional and situational information changes outcomes, and much weaker for asking it as a history being the thing that helps. Those are different claims, and the agent's design should keep them apart.
Working definitions used throughout:

 | 
Domain | 
What it covers | 
Typical elicitation
 | 
Functional history | 
Basic ADLs (washing, dressing, toileting, transfers, feeding), instrumental ADLs (shopping, cooking, finances, medications, transport), mobility and gait aids, continence, cognition and communication, vision and hearing, falls in the last 6–12 months | 
Self-report, carer/proxy report, direct observation, performance tests
 | 
Situational history | 
Where and with whom the person lives, type of dwelling and access (stairs, bathroom), who helps and how often, formal services in place, carer strain, transport, food and medication security, financial strain, housing stability, safety at home, language and health literacy, advance care planning and substitute decision-maker | 
Self-report, carer report, service records
Three questions the evidence has to answer for the agent to be worth building this into:

Does functional and situational status predict outcomes that matter (mortality, readmission, length of stay, discharge destination, diagnostic accuracy)?

Does systematically collecting it change those outcomes, and under what conditions?

Is it currently collected well enough that an agent adds nothing — or badly enough that it adds a lot?
The short answers: yes, strongly; yes, but only when collection is coupled to a team that can act on it; and it is collected poorly and inconsistently, which is where the agent's case sits.
Functional status predicts outcomes, consistently and independently
This is the strongest part of the evidence base. Baseline function and the situational context around it predict readmission, institutionalisation and death after adjustment for diagnosis and comorbidity.

 | 
Finding | 
Effect | 
Design and sample | 
Source
 | 
IADL limitations predict 30-day readmission | 
Adjusted RR 1.17 (1.06–1.29); ADL limitations ranked the single most important predictor in random-forest models, IADL second; IADL + diabetes subgroup 26% readmitted | 
Retrospective cohort, 20,007 hospitalisations in 6,617 people aged 65+, Health and Retirement Study linked to Medicare, 2002–2011 | 
[Schiltz et al. 2020, JGIM]
 | 
Functional dependency predicts discharge to institutional care | 
Pooled OR 2.06 (1.58–2.69), 6 studies / 7,796 participants; dementia or cognitive impairment OR 2.14 (1.24–3.70) | 
Systematic review and meta-analysis, 23 studies, 354,985 participants | 
[Predicting discharge to institutional long-term care, 2017]
 | 
Function itself deteriorates during admission | 
Pooled incidence of hospital-associated disability 37% (95% CI 30–43); patient-reported 27–32% per task, proxy-reported 59–70% | 
Rapid systematic review, 10 studies | 
[PeerJ 2023]
 | 
Brief functional/vulnerability screens carry prognostic signal but poor specificity | 
ISAR for in-hospital mortality: pooled sensitivity 92% (88–95), specificity 26% (21–33), AUC 0.82; for ED revisits AUC 0.64 | 
Systematic review and meta-analysis, 62 ED studies, 40 instruments | 
[Ku et al. 2025, Innovation in Aging]
Two things follow for the agent. First, the prognostic payload sits in a small number of items — ADL and IADL dependency, cognition, mobility — not in an exhaustive inventory. Second, the discharge-destination meta-analysis explicitly flags that living alone and social support were inadequately evaluated in the primary studies: the situational half of the history is under-measured rather than shown not to matter.
Collecting it only helps when a team acts on it
Comprehensive geriatric assessment is the closest thing to a trial of "take a systematic functional and situational history". It works on the ward and stops working as you move away from the ward — which locates the active ingredient in the multidisciplinary response, not in the data capture.

 | 
Setting | 
Result | 
Evidence
 | 
Inpatient ward | 
Alive and in own home at 3–12 months RR 1.06 (1.01–1.10); nursing home admission RR 0.80 (0.72–0.89); cost +£234 per patient (−£144 to £605); no mortality benefit | 
29 trials, 13,766 participants — [Gardner, Shepperd, Godfrey et al. 2019, NIHR/Cochrane update]
 | 
Hospital outpatient clinic | 
Mortality RR 1.04 (0.88–1.23); hospitalisation RR 1.01 (0.77–1.32); no effect on function, cognition or cost; very-low-quality signal of modest QoL gain | 
7 RCTs, 3,254 participants — [BMC Geriatrics 2025]
 | 
Emergency department | 
Hospital days over 365 days 3,470 vs 3,149 per 100 person-years, rate ratio 1.10 (0.55–2.19), p=.78; no difference in admissions, ED revisits, mortality or QoL | 
Single-centre RCT, 432 patients, median age 85 — [Alakare et al. 2021, BMC Geriatrics]
The Cochrane definition of CGA is explicit that it is a process — "a multidisciplinary diagnostic process that determines a frail older person's medical, functional, psychological and social capability" — delivered by staff who then own the coordinated management and follow-up. The assessment is the input; the geriatric team is the mechanism.
For the agent, this is the central design constraint. An agent that elicits a good functional and situational history in an ED waiting room, in a system with no one to hand it to, is reproducing the outpatient and ED null results. The plausible value is in the handover — getting the information in front of the clinician, allied health and discharge planner early enough to change what they do — not in the elicitation itself.
Situational factors carry risk comparable to medical ones
The association evidence for living situation, support and social circumstance is large and old; the intervention evidence is thin and recent. Both matter, for different parts of the design argument.

 | 
Factor | 
Effect | 
Evidence
 | 
Social isolation | 
OR 1.29 for mortality; loneliness OR 1.26; living alone OR 1.32 — after adjustment, comparable to established mortality risk factors | 
70 prospective studies, 3,407,134 participants, mean 7-year follow-up — [Holt-Lunstad et al. 2015]
 | 
Social isolation in heart failure | 
OR 1.55 (1.39–1.73) for readmission; perceived and objective isolation performed similarly | 
Meta-analysis, 13 studies, 6,468 patients — [Heidari Gorji et al. 2019, Gen Hosp Psychiatry]
 | 
Financial, housing and food insecurity | 
ED visits 115 vs 86.9 per 1,000 person-years with vs without social risk exposure; hospitalisation difference (40.6 vs 33.8) not statistically significant | 
Prospective cohort, 9,785 insured adults, Kaiser Permanente — [Clennin et al. 2025, JAMA Netw Open]
Two caveats worth carrying forward. The isolation literature is overwhelmingly observational, with confounding by health status that adjustment handles imperfectly — people become isolated partly because they are unwell. And the most recent, best-designed utilisation study found the ED signal but not the admission signal, which is a reminder that social risk predicts contact with services more reliably than it predicts clinical deterioration.
For an ED or GP-booking agent, the ED-contact association is arguably the more relevant one: these are the presentations where situational factors drive the encounter.
It is currently taken badly — which is the agent's actual case
The strongest argument for building this into the agent is not that the history is valuable in theory. It is that it demonstrably is not being taken now, and that the failure is structural (time, not knowledge).
Omission rates

 | 
Finding | 
Figure | 
Evidence
 | 
ED records with no reference to functional ability at all | 
75% (75/101); only 9% mentioned two or more ADLs | 
101 frail older patients, 4 teaching hospitals — [Rodríguez-Molinero et al. 2006, BMC Geriatrics]
 | 
Documentation missing in ED fall presentations (age ≥75) | 
Functional status 58.2%; cognition 64.1%; social history / living situation 55.8%; frailty screening 85.3% | 
Retrospective review, 778 patients — [Bergström et al. 2025, Int Emerg Nurs]
 | 
Admissions carrying any structured social-risk (Z) code | 
1.9% | 
14,289,644 hospitalisations, US National Inpatient Sample — [Truong et al. 2020, Medical Care]
 | 
Social information in free text vs structured fields | 
4–30× more prevalent in notes: social isolation 4.60% vs 0.38%, employment 4.60% vs 0.09%, finance 2.64% vs 0.09% | 
4,283 adults with diabetes, 30,288 notes — [Mehta et al. 2023, JMIR Med Inform]
Accuracy when it is taken
ED physicians' assessment of function agreed with family respondents at 0.47 (0.38–0.57), and the medical record with family at 0.41 (0.27–0.55) — but where two or more ADLs had actually been documented, physician concordance rose to 0.82 ([Rodríguez-Molinero 2006]). Asking properly fixes most of the accuracy problem.
Proxy report is not a clean substitute. Patient–caregiver agreement was ICC 0.71 for the Barthel Index and 0.60 for the Frenchay Activities Index in stroke survivors, with limits of agreement the authors judged too wide for clinical use ([Chen et al. 2007]); for symptoms it is worse — ICC 0.28 for anxiety and 0.25 for depression across 188 dyads ([Kroenke et al. 2022]). Proxy-reported hospital-associated disability also runs roughly twice patient-reported (59–70% vs 27–32%).
Why it is missed
Consultation length is the binding constraint, not clinician attitude: across 179 studies and >28.5 million consultations in 67 countries, countries representing about half the world's population have primary care consultations of five minutes or less ([Irving et al. 2017, BMJ Open]). A GP-booking-call agent is adding time that does not currently exist rather than competing for it.
What machine-administered history does to disclosure
Computer self-administration has a long-established mode effect on sensitive disclosure. In 398 participants completing both audio computer-assisted self-interview and face-to-face interview on the same day, reporting rose sharply on the computer: women paying for sex 49.3% vs 5.8%, men reporting rape 8.9% vs 3.9%, injecting drug use 10.8% vs 2.3% ([van der Elst et al. 2009, PLoS ONE]).
The counterweight: in a review of 18 studies of chatbot history-taking, patients found chatbots "less intimidating than traditional face-to-face conversations" yet still preferred to disclose medical information to a physician ([Hindelang et al. 2024]). And in a randomised crossover OSCE against 20 primary care physicians, the LLM was rated superior on 30 of 32 specialist axes — but the two "acquired similar amounts of information"; the advantage lay in interpreting it ([Tu, Schaekermann et al. 2025, Nature]). That finding should temper any claim that the agent will elicit more; its defensible claim is that it elicits at all, in encounters where nothing is currently asked.
Instruments worth mapping the agent's questions onto
None of these was designed for conversational voice elicitation, but anchoring the agent's questions to validated items means the structured layer under the handover is comparable to something.

 | 
Instrument | 
What it covers | 
Performance | 
Fit for a voice agent
 | 
Katz ADL, Barthel Index | 
Basic ADLs; Katz was the most frequently used instrument across hospital-associated disability studies | 
Patient–proxy ICC 0.71 for Barthel in stroke survivors | 
Good — concrete, observable, self-reportable; Barthel scores 0/5/10 per item map poorly to conversation, Katz yes/no maps well
 | 
Lawton IADL | 
Shopping, cooking, housekeeping, laundry, transport, medications, finances | 
— | 
Good — all seven items are natural conversational questions; note the original scale is sex-biased in scoring
 | 
PRISMA-7 | 
7 yes/no items on age, general health, activities and social support; cutoff ≥3 | 
Pooled sensitivity 72% (54–84), specificity 87% (76–93), 12 studies; against frailty phenotype 82%/79%. Predicts 2.66 h more ED time, 1.89 days more inpatient stay, ED re-attendance RR 1.37, admission RR 1.56 | 
Best fit of the frailty screens — short, yes/no, self-report by design — [meta-analysis 2025]
 | 
ISAR | 
6-item ED vulnerability screen | 
Sensitivity 92%, specificity 26%, AUC 0.82 for in-hospital mortality | 
Trivially easy to ask; specificity too low to drive any consequential action
 | 
Clinical Frailty Scale | 
9-point clinician judgement of baseline function ~2 weeks before presentation | 
Widely used in ED (15 of 62 studies in the ED screening review) | 
Not directly askable — it is a clinician judgement, and the agent could at most surface the inputs. Free for non-profit clinical, research and educational use; commercial products need a licence from [Dalhousie GMR]
 | 
AHC Health-Related Social Needs tool | 
5 core domains (housing instability, food insecurity, transport, utilities, interpersonal safety) + 8 supplemental (financial strain, employment, family/community support and loneliness, education and language, physical activity, substance use, mental health, disability) | 
Developed for the CMS Accountable Health Communities model, screened >1 million beneficiaries | 
Closest thing to a ready-made situational question set; US framing (utilities shutoff, insurance) needs Australian adaptation — [CMS tool]
One licensing note that matters for a deployed product: the Clinical Frailty Scale is the tool Australian EDs actually use, and it is the one with a commercial licence condition. Katz, Lawton, Barthel, PRISMA-7 and the AHC tool carry no comparable barrier.
Counter-evidence: what goes wrong when you ask
This is the part of the literature most likely to be raised by a reviewer or an ethics committee, and it is stronger than the enthusiasm literature suggests.
Asking does not connect people to services. In a three-arm VA RCT of 479 veterans with a social need, escalating from a generic resource postcard to social-worker navigation did not significantly increase connection to a new resource at 8 weeks (high-intensity vs control OR 1.60, 95% CI 0.96–2.67) — [Gurewich et al. 2025, JGIM]. At national scale, CMS screened 1,020,864 beneficiaries and "more than half of beneficiaries had no HRSNs resolved and were not connected to a community service provider" — [CMS Accountable Health Communities second evaluation, 2023].
The leak is in the pathway, not the question. An ED implementation study at the University of Utah approached 4,608 patients: 61% completed the screener, 47% of those reported a need, 34% of those accepted follow-up — and 98 people were finally connected to a community service — 7% of those with an identified need. Registration staff used "professional intuition" to screen selectively by appearance and insurance status, contradicting the universal-screening protocol — [Wallace et al. 2021, Implement Sci Commun]. An earlier phase of the same programme found patients with identified social needs went on to use the ED more, not less (1.07 vs 1.36 visits, p=.03) — [Wallace et al. 2020, Prev Chronic Dis].
Screening may not even be the best way to find out what people want. In a pragmatic RCT of 3,949 caregiver–patient dyads across an ED and two primary care clinics, simply offering a resource menu produced nearly 10% more caregivers expressing a desire for resources than the screening arm, with 2.7× greater odds among non-English-preferring caregivers — [SECURE RCT, Cullen et al. 2026, Pediatrics].
Acceptability is conditional — and conditional specifically on the record. 85% of 218 primary care patients were comfortable being asked about social needs, and fewer than 10% of those with needs were uncomfortable being asked. But 20% were uncomfortable with that information entering the EHR, rising to 37% among those with two to five social needs — [Albert et al. 2022, BMC Health Serv Res]. The people with most to gain are the most wary of it being written down. For an agent that produces a structured, persistent handover, this is the sharpest design tension in the whole review.
Screening without services has a standing ethical objection. Garg, Boynton-Jarrett and Dworkin argued in JAMA that screening in isolation, without capacity to link to treatment, "is ineffective and, arguably, unethical", and risks patients perceiving clinicians as "judgmental, presumptuous, or even callous" — [JAMA 2016].
Over-triage and burden. Vulnerability screens flag almost everyone: ISAR's 26% specificity means the majority of positives are not the target population. And documentation burden is already the dominant complaint — physicians spend roughly twice as long on electronic documentation and clerical work as on direct patient care ([Moy et al. 2021, JAMIA]). A handover that adds a page of social findings to every presentation will be skimmed or ignored.
Generalisability. The one robustly positive body of evidence (inpatient CGA) is in selected frail inpatients on geriatric wards. The social-care trials are US Medicaid, Medicare, VA and paediatric. There is very little evidence from undifferentiated adult ED presentations or from Australian primary care, and none for a voice agent doing this.
What the evidence supports building
Ask a short core of everyone, and go deep only on trigger. The prognostic weight sits in a handful of items — ADL and IADL dependency, mobility, cognition, who helps at home. An exhaustive inventory buys little and costs specificity, attention and goodwill. A reasonable universal core is Lawton's seven IADL items, a Katz-style basic ADL set, mobility aids and falls in the last 6–12 months, who the person lives with, who helps and how often, and what services are already in place. Deeper situational questioning is triggered by age, reported dependency, repeat presentation or a reported gap in support.
Capture the delta, not the level. The single most useful thing the agent can record is the difference between usual function two weeks ago and function now — the framing the Clinical Frailty Scale already uses, and precisely what is absent from records. Hospital-associated disability affects around 37% of older inpatients, and without a baseline nobody can tell new disability from old.
Output the inputs, not a score. Given ISAR's 26% specificity and the CFS's status as a clinician judgement, the agent should surface the constituent facts — "manages her own medications, has not shopped since March, daughter visits twice weekly" — rather than a frailty grade. That also sidesteps the CFS licensing question and keeps the clinician as the person making the judgement.
Don't ask what nothing can answer. The clearest lesson from the social-care trials is that identification without a route to action changes nothing and may erode trust. Before a situational domain goes into the question set, there should be a named recipient for a positive answer — discharge planner, social work, Aboriginal liaison, home care referral, GP recall. Domains without a recipient are the ones to leave out of v1.
Treat the written record as a separate consent. 37% of people with multiple social needs were uncomfortable with that information entering the EHR. An agent that automatically writes a structured social profile into a persistent handover is doing exactly the thing that group objects to. Options worth testing: telling the patient plainly where the information goes, a per-item "is it OK if I pass this on?", or holding some social items as clinician-visible-but-not-filed.
Design the handover for a skimmer. Physicians already spend about twice as long documenting as with patients. The functional and situational material belongs as three or four lines near the top — baseline function, change from baseline, who is at home, what would need to be in place to go home — with the rest available on request through the clarifying-question channel already in the design.
Implications for the comparative study. The literature predicts where the agent will look best: 75% of ED records contained no reference to function at all, and 55–85% of fall presentations were missing function, cognition, social situation or frailty screening. Functional and situational completeness should therefore be a pre-specified secondary outcome, scored separately from symptom agreement — not folded into a single agreement figure, where it will be diluted by the presenting-complaint content on which clinicians do well. Two design notes follow from the same literature: agreement needs a reference standard better than the ED doctor's own note (collateral from a family member, or a structured research assessment), and the AMIE result — similar information acquired, better interpretation — suggests the measurable advantage may be in what the handover makes of the information rather than in raw elicitation.
Sources
All figures above come from pages opened for this review. Two are secondary routes and are flagged as such.
Prognostic value of function and situation

Schiltz et al. 2020, JGIM — [IADL limitations and 30-day readmission]

[Predicting discharge to institutional long-term care: systematic review and meta-analysis, 2017]

[Assessment tools and incidence of hospital-associated disability: rapid systematic review, PeerJ 2023]

Ku et al. 2025 — [ED frailty and vulnerability screening instruments, Innovation in Aging]

Holt-Lunstad et al. 2015 — [Loneliness and social isolation as risk factors for mortality]

Heidari Gorji et al. 2019 — [Social isolation and heart failure readmission]

Clennin et al. 2025, JAMA Netw Open — social risk and acute care utilisation, read via [AJMC summary]
Assessment as an intervention

Gardner, Shepperd, Godfrey et al. 2019 — [CGA in hospital and hospital-at-home, NIHR/Cochrane update]

[CGA in hospital outpatient clinics: systematic review and meta-analysis, BMC Geriatrics 2025]

Alakare et al. 2021 — [Systematic geriatric assessment in the ED: RCT, BMC Geriatrics]
Current documentation and elicitation

Rodríguez-Molinero et al. 2006 — [Functional assessment of older patients in the ED, BMC Geriatrics]

Bergström et al. 2025 — [Documentation in ED fall presentations, Int Emerg Nurs]

Truong et al. 2020, Medical Care — [SDOH Z-code use in 14.3M hospitalisations]

Mehta et al. 2023 — [Structured vs free-text capture of SDOH, JMIR Med Inform]

Chen et al. 2007 — [Patient–proxy agreement on Barthel and Frenchay, Clin Rehabil]

Kroenke et al. 2022 — [Caregiver proxy report of symptoms, J Patient Rep Outcomes]

Irving et al. 2017 — [International variation in primary care consultation length, BMJ Open]

Beck, Klein & Kahn 2012 — [EHR-embedded clinical social history, Clin Pediatr] (>80% of visits documented ≥1 of 7 questions; single-arm, well-infant visits, so not evidence of improvement over baseline)
Machine-administered history

van der Elst et al. 2009 — [ACASI vs face-to-face disclosure, PLoS ONE]

Hindelang, Sitaru & Zink 2024 — [Conversational agents for history taking: systematic review]

Tu, Schaekermann et al. 2025 — [Towards conversational diagnostic AI (AMIE), Nature]

Hong, Smith & Lin 2022 — [Patient acceptability of a conversational intake agent, JMIR Form Res]
Instruments

[PRISMA-7 diagnostic and predictive accuracy: systematic review and meta-analysis, BMC Geriatrics 2025]

[Clinical Frailty Scale permission for use, Dalhousie Geriatric Medicine Research]

[AHC Health-Related Social Needs Screening Tool, CMS]
Counter-evidence

Gurewich et al. 2025 — [Social needs screening and referral RCT, JGIM]

Cullen et al. 2026, Pediatrics — SECURE RCT, read via [CHOP research summary]

[Accountable Health Communities second evaluation report, CMS 2023]

Wallace et al. 2021 — [ED social needs screening implementation, Implement Sci Commun]

Wallace et al. 2020 — [ED social needs screening feasibility, Prev Chronic Dis]

Albert et al. 2022 — [Patient comfort with social needs screening and its documentation, BMC Health Serv Res]

Garg, Boynton-Jarrett & Dworkin 2016 — [Avoiding the unintended consequences of screening for social determinants of health, JAMA]

Moy et al. 2021 — [Measurement of clinical documentation burden: scoping review, JAMIA]
Adjacent, for the extraction side of the build

Patra et al. 2021 — [NLP for extracting SDOH from clinical text: systematic review, JAMIA]

Keloth et al. 2025 — [Instruction-tuned LLMs for SDOH extraction across four corpora, npj Digital Medicine]

Fu et al. 2022 — [How functional status is documented across three institutions, Front Digit Health]
Not retrieved — worth chasing directly, all blocked by publisher access during this review: Ellis et al. 2017 Cochrane CD006211.pub3 (the primary review, quoted here through its 2019 NIHR update); Carpenter et al. 2015 ED risk-stratification meta-analysis; De Marchis and Byhoff on social risk screening acceptability; the SOLAR trial.