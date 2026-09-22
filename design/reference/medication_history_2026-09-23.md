# Reference: AI History-Taking Agent — Medication History Evidence Base

Source: the product owner's Claude Doc, https://claude.ai/artifact/M2sKE16QcLoHY7nwuXXXgR (as of 2026-09-23). Plain-text extract; tables and diagrams flattened. The live doc is the source of truth.

---


AI History-Taking Agent — Medication History Evidence Base
 · 
Companion evidence document to the Symptom Questioning Library. Domain: medication history.
Purpose and scope
The medication history is the one history domain with a large, quantified evidence base on how badly humans do it — which makes it the strongest single argument for an agent-taken history, and the easiest place to be caught overclaiming.
This document covers what the literature establishes about taking a comprehensive medication history: how accurate usual care is, which sources contribute what, who should take it and at what cost, which categories get missed, and whether any of it changes outcomes. It is written to ground the medication history section of the Symptom Questioning Library and to inform evaluation design.
Two framings run through it and should be kept apart. The process evidence (does a structured history produce a more accurate medication list?) is strong. The outcome evidence (does that prevent harm?) is weak and has weakened further since 2024. Claims made for the agent should sit on the first, not the second.
How accurate are usual-care medication histories
Between a quarter and two-thirds of patients arrive on the ward with at least one error in their recorded medication history, and omission is the dominant error type.
[Tam et al, CMAJ 2005] remains the anchor systematic review: 22 studies, 3,755 patients.

 | 
Finding | 
Range across studies
 | 
Patients with ≥1 prescription medication history error | 
10–67%
 | 
Patients with ≥1 error including non-prescription drugs and allergies | 
27–95%
 | 
Patients with ≥1 omission error | 
10–61%
 | 
Patients with ≥1 commission error | 
13–22%
 | 
Patients with errors after excluding intentional changes | 
27–54%
 | 
Errors judged clinically important | 
11–59%
In one included study, 22% of errors could have caused harm if continued during admission, rising to 59% if continued after discharge. Cornish (cited within Tam) found 54% of patients had ≥1 error, mean 0.9 errors per patient.
[Pippins et al, J Gen Intern Med 2008] is the most useful attribution study for this project. Across 180 general medical patients, 2,066 discrepancies were identified; 257 (12%) were unintentional with potential for harm — 1.4 potential adverse drug events per patient. 72% of these arose from inaccurate preadmission history collection, not from the reconciliation step against discharge orders. Independent predictors were low patient understanding of their preadmission medicines, more medication changes, and the history being obtained by an intern.
Australian local data is consistent. [Crook et al, Pharm Pract 2007], at the Royal Adelaide Hospital, compared medical-staff and pharmacist documentation for 100 patients aged over 70: 966 of 1,151 medicines (83.9%) showed inconsistency, and 563 (48.9%) were complete omissions.
Does inaccuracy actually harm patients
The causal thread from a bad medication history to observed patient harm is thin, and should not be overstated in grant or governance documents.
Almost all the harm evidence is expert-adjudicated potential harm — a panel judging that an error could have caused injury, not an injury observed. Tam's 11–59% "clinically important" and Pippins' 1.4 potential ADEs per patient are both of this kind. [Quélennec et al, Eur J Intern Med 2013] graded 173 errors in 256 elderly inpatients: 72.8% no potential harm, 20.8% requiring monitoring or intervention, 6.4% potential clinical deterioration.
The closest thing to observed harm at scale is [Bell et al, JAMA 2011], a population cohort of 396,380 Ontarians aged ≥66. Unintentional discontinuation of chronic medicines after admission was common and dose-dependent on acuity:

 | 
Drug class | 
Adjusted OR, discontinuation at 90 days (hospitalised) | 
After ICU
 | 
Antiplatelets / anticoagulants | 
1.86 (1.77–1.97) | 
2.31 (2.07–2.57)
 | 
Statins | 
1.33 (1.29–1.37) | 
1.48 (1.39–1.57)
 | 
Gastric acid suppressants | 
1.50 (1.43–1.56) | 
—
 | 
Levothyroxine | 
1.18 (1.14–1.23) | 
—
 | 
Respiratory inhalers | 
1.50 (1.15–1.97) | 
—
But downstream harm — death, emergency department visit or emergency admission over days 91–365 — was significant for only two of five drug classes, and the effects were small: statins AOR 1.07 (1.03–1.11), antiplatelets/anticoagulants AOR 1.10 (1.03–1.16).
Defensible position: inaccurate medication histories reliably produce medication list errors, a meaningful minority of which clinicians judge clinically important. Whether they cause measurable population-level harm is unproven. The claim the agent should make is about list accuracy and clinician time, not about preventing deaths.
Information sources and how they combine
No single source is adequate, and what matters is combining types of source — one showing what the patient actually takes, one showing what was supplied — rather than simply consulting more of them.
[Chen et al, Emerg Med Australas 2018] is the best source-comparison study and is Australian: 455 ED patients at a major tertiary referral hospital, median age 71, median 6 regular and 2 PRN medicines, each source compared against a pharmacist Best Possible Medication History.

 | 
Source | 
Median discrepancies per patient | 
Range
 | 
Residential care facility medication chart | 
0 | 
0–3
 | 
Dose administration aid contents | 
2.0 | 
0–9
 | 
Patient's own medication list | 
2.5 | 
0–16
 | 
Dose administration aid label | 
3.0 | 
0–7
 | 
Community pharmacy dispensing history | 
3.0 | 
0–19
 | 
GP letter | 
3.0 | 
0–18
 | 
Patient's own medicine containers | 
4.0 | 
0–16
40.4% of discrepancies were rated moderate or high clinical significance, and 55.6% were omissions. Every source other than the RCF chart carried two to four discrepancies per patient.
Why two sources, and which two
[Francis et al, Int J Clin Pharm 2023] supplies the mechanism behind the Australian "at least two sources" rule. Across 91 patients and 1,170 medicines, what independently predicted an accurate history was pairing an administration source (patient or carer interview, own medicines, dose administration aid, RCF chart — what is actually taken) with a supplier source (dispensing or prescribing record — what was issued): OR 1.65 (95% CI 1.09–2.50, p=0.02). Source count alone was not the predictor.
Marginal yield of combining is quantified in a Jordanian study of 196 inpatients ([Asakrh et al, Int J Clin Pract 2020]): completeness was 71.4% for patient interview alone, 35.3% for the pharmacy database, 28.2% for the medical file, and 93.0% for the pharmacist-compiled history using all sources. Completeness fell as medication count rose (R = −0.392, p<0.001).
[ACSQHC] requires at least two sources for a BPMH; NSW CEC and WA Health audit tools operationalise this by requiring documented evidence of which two were used.
Who takes it, and what it costs
Who takes the history is the single largest determinant of its accuracy in the comparative literature — and the reason a good history is rationed is that it takes roughly an hour.

 | 
Study | 
Design and setting | 
Comparison | 
Result
 | 
[Pevnick, BMJ Qual Saf 2018] | 
3-arm RCT, US ED, n=278, mean 15 medicines | 
Usual care vs pharmacist vs pharmacy technician | 
Mean errors per patient 8.0 vs 1.4 vs 1.5; downstream order errors 3.2 vs 0.6 vs 0.6
 | 
[Henriksen, Int J Clin Pharm 2015] | 
Prospective comparative, Danish ED, n=106, 1,075 prescriptions | 
Physician vs pharmacy technician | 
Discrepancies in 27% vs 2% of prescriptions (~3 vs <1 per patient)
 | 
[Aag, Eur J Clin Pharmacol 2014] | 
RCT, Norwegian cardiology ward, n=201 | 
Clinical pharmacist vs nurse | 
Similar yield (3.1 vs 2.8 discrepancies per patient, p=0.53); 22.9 vs 32.2 min (p<0.001); physicians acted on pharmacist findings more often (p=0.001)
 | 
[Venturini, Pharmacy 2023] | 
Observational, Italian preoperative clinic, n=140 | 
Clinical pharmacist vs nursing staff | 
Omissions 2.0% vs 57.4%; data completion 98.0% vs 42.6%
Two things follow. First, pharmacy technicians performed as well as pharmacists in the only randomised head-to-head — the skill is procedural, not clinical judgement, which is precisely the kind of task an agent can be built to do. Second, nurses found as many discrepancies as pharmacists but took longer and were acted on less, so the bottleneck is partly credibility of the output, not just its content.
Time cost
[Nguyen et al, J Hosp Med 2017], time-and-motion at Cedars-Sinai ED, 30 histories with complete data:

Pharmacist: 58.5 min (95% CI 46.9–70.1). Technician: 79.4 min (95% CI 59.1–99.8), plus 26 min pharmacist supervision.

42.8% of total time was spent in the electronic record, not with the patient.

With a caregiver or facility list available: 58.1 min. Without: 90.5 min (p=0.02).
This is the core economic argument for an agent. A BPMH is not withheld because clinicians doubt its value; it is withheld because an hour per patient does not exist. [Ryan et al, Hosp Pharm 2026], at a quaternary Australian hospital, found only 54% of 280 admissions had a BPMH within 24 hours — and their prioritisation tool classified 64% of patients as urgent or high risk, so it barely discriminated.
Structured prompting and what gets missed
Systematic prompting by medicine category is the single intervention with a clean before-and-after effect on history quality, and it is directly implementable as agent questioning logic.
[Huber et al, Int J Clin Pharm 2017] introduced an IT-guided checklist on a surgical ward (n=228, before/after):

 | 
Measure | 
Before | 
After
 | 
Patients with ≥1 discrepancy | 
69.9% | 
29.6%
 | 
Mean discrepancies per patient | 
2.3 | 
0.6
 | 
Proportion of errors that were omissions | 
76.4% | 
44.1%
 | 
Ophthalmological preparation discrepancies | 
15 | 
8
 | 
Analgesic discrepancies | 
34 | 
4
The effect is concentrated in exactly the categories patients do not volunteer. [Monte et al, J Emerg Med 2015], 502 ED patients, found only 21.9% of electronic medication lists accurate, with omission rates by category: herbal medicines 89.1%, non-prescription 76.1%, vitamins 73.0%, supplements 67.3%. In the Australian prescription-repository study below, 72.1% of all omissions were over-the-counter medicines. PRN medicines account for roughly a third of all errors.
Prompt inventory
The categories the evidence says must be asked about individually, because they are not produced by an open question:

Over-the-counter and pharmacy-only medicines (analgesics, antihistamines, laxatives, antacids)

Vitamins, minerals and nutritional supplements

Herbal and complementary medicines

Eye drops, ear drops, nasal sprays

Inhalers and nebulised medicines

Topical creams, ointments and transdermal patches

Injectables — insulin, anticoagulants, biologics, depot antipsychotics

Intermittent dosing — weekly, monthly, three-monthly, annual (methotrexate, bisphosphonates, denosumab, B12, depots)

Contraception and hormone therapy

PRN and "only when I need it" medicines

Recently started, changed or ceased medicines, including short courses

Medicines obtained from someone else, from overseas, or online

Recreational substances, alcohol and nicotine products
ACSQHC guidance additionally requires asking about medicine storage at home and anything affecting administration — swallowing difficulty, dexterity, vision, cognition.
Actual use versus what is prescribed
Getting the drug name right is not enough: a quarter of correctly identified medicines carry the wrong regimen, and roughly one in six recorded medicines is one the patient has stopped taking.
[Elliott et al, Intern Med J 2023] quantified this across two Australian tertiary health services (n=154, median age 76, median 10 pre-admission medicines), comparing histories derived from the national prescription exchange repository against a pharmacist BPMH:

 | 
Error type | 
Rate
 | 
Patients with ≥1 error | 
153/154 (99.4%)
 | 
Median errors per patient | 
6.0 (IQR 4.0–9.0)
 | 
Current medicines omitted | 
549/1,648 (33.3%), of which 72.1% were OTC
 | 
Dose-regimen errors among medicines captured | 
276/1,099 (25.1%)
 | 
Commission errors (recorded but not taken) | 
224/1,323 (16.9%)
The same pattern appears elsewhere: 78.9% of inaccurate electronic lists in Monte's ED cohort contained medicines the patient had stopped, and [Fung et al, Ann Emerg Med 2013] found only 60% of patients with active medicines had a recent electronic prescription on file.
The implication is structural. Dispensing and prescribing records are blind to three things by design: cessation, actual regimen, and anything not dispensed on prescription. Only a conversation recovers them. This is the strongest functional argument for the agent — it occupies the source category that no data feed can replace.
The history should therefore establish, per medicine and not just per list:

What dose and how often the patient actually takes it, not what the label says

Whether they have missed doses recently, and roughly how often

Whether anything has been stopped, and by whom — themselves, a GP, a specialist

Whether they can physically take it: swallowing, inhaler technique, dexterity for eye drops or injections, vision for labels

Who administers it — self, carer, dose administration aid, community nurse
Allergies and adverse drug reactions
Allergy documentation is worse than medication documentation and is routinely reduced to a drug name with no reaction description, which makes it clinically unusable.
[Kiechle et al, J Med Toxicol 2018], a prospective study of 1,014 patients in an urban academic ED:

416 patients (41%) had a discrepancy between self-reported allergy or ADR and the electronic record; omission was the commonest discrepancy.

A full description of the allergy or reaction was present in only 18.4% of charts.

57 patients (5.6%) received a medicine potentially interacting with a documented allergy or ADR.
The Australian minimum dataset is explicit and is what the agent should capture: medicine name, type of reaction, and date of reaction — or an affirmative "nil known". NSW CEC and WA Health audit tools check specifically for the type of reaction, not merely the agent name.
Practically, the agent should distinguish and record separately:

True allergy (rash, urticaria, angioedema, anaphylaxis, bronchospasm)

Intolerance or side effect (nausea, dizziness, myalgia) — frequently recorded as "allergy" and wrongly barring a useful drug

What happened, in the patient's own words

When it happened, and whether the medicine has been taken since

Whether it required treatment, and what treatment
The verbatim-words principle already agreed for red flag alerts applies here directly: "my lips swelled up and I went to hospital" carries information that "penicillin allergy" destroys.
Australian digital medication data
None of My Health Record, the prescription exchange services or the Active Script List constitutes a medication history; each is a supplier source that must be paired with a conversation.

 | 
Source | 
Best available accuracy figure | 
Principal blind spots
 | 
My Health Record ([Francis et al, Health Inf Manag J 2025], n=82, mean age 77, 1,207 medicines) | 
59.2% of medicines complete or partial match to pharmacist BPMH; 40.8% mismatched; 10.3% of mismatches clinically relevant (4.2% of all medicines) | 
Non-prescription, PRN and parenteral routes significantly worse than regular oral prescriptions; consumer can delete records
 | 
Prescription exchange / dispense repository ([Elliott et al, Intern Med J 2023], n=154) | 
≥1 error in 99.4% of patients; median 6 errors | 
33.3% of current medicines omitted (72.1% OTC); 25.1% dose-regimen errors; 16.9% commission errors; cannot detect cessation
 | 
[Active Script List] | 
Not formally evaluated as a history source | 
OTC and complementary medicines out of scope entirely; non-barcoded paper scripts excluded; hospital-supplied medicines excluded; per-encounter patient consent required; patients can exclude individual medicines
My Health Record prescription and dispense records carry brand, strength, generic name, dosage instructions, repeats and last dispense date — but they are uploaded by the pharmacist, and the consumer may delete any record from their own file ([Australian Digital Health Agency]).
For the build: treat these feeds as the supplier half of the Francis source-type pairing. The agent is the administration half. The reconciliation between the two — and the explicit list of where they disagree — is arguably a more valuable output to the clinician than either list alone, and is something neither a pharmacist reading a screen nor a data feed currently produces at the point of triage.
Governance note: accessing My Health Record or ASL data within an agent pipeline raises consent questions distinct from those for the conversation itself. ASL access in particular is consented per encounter, not standing.
Patient-entered, tablet and conversational AI approaches
Patient self-entry without a clinician has been tested and is not accurate enough to stand alone; conversational AI for medication history is essentially unstudied, which is the gap this project sits in.
Self-administered forms
[Wai et al, Am J Emerg Med 2020], an Australian ED (n=138), had patients complete a medication form in the waiting room, with pharmacist BPMH as reference:

 | 
Discrepancies vs BPMH | 
Patients
 | 
0 | 
25% (34)
 | 
1 | 
34% (47)
 | 
2 | 
11% (15)
 | 
≥3 | 
30% (42)
20% had at least one high-risk medication discrepancy. Discrepancies rose with medication count (IRR 1.11 per medicine, 1.09–1.14) and more than doubled when community pharmacy details were missing (IRR 2.10, 1.64–2.68). The authors' conclusion — that self-administered forms need verification by a BPMH — is the obvious comparator claim the agent has to beat.
A companion paper found 87% of 113 surveyed patients reported no difficulty completing the form, but it did not stratify by cognition, frailty, acuity or language — so the "who cannot do this" question is unanswered in that dataset.
Tablet-assisted
[Kripalani et al, AJHP 2019], 244 intervention vs 244 matched controls in a large academic ED: medication lists were updated in 41.4% vs 17.6% of cases, an absolute difference of 23.8% (95% CI 16.0–31.6). Critically, half the intervention cohort needed moderate-to-substantial assistance, and need for help tracked with older age and polypharmacy — not with education or health literacy. That is the exact population a medication history matters most for, and it argues for voice over screen.
Conversational AI
The literature here is thin enough to be worth stating plainly as a gap.

[AMREC (medRxiv 2025)] is the only conversational medication reconciliation agent I could find. Prescription-signature extraction 98.3% across 18 elements; fine-tuning cut conversation failures from 75/179 to 5/179, failures being broken conversational patterns under user digression. User testing n=2. Proof of concept, no reference-standard accuracy.

The [JMIR Med Inform 2024 systematic review] of history-taking chatbots (18 studies, 3 RCTs) reports high usability (mean 96) and reduced documentation time, including a 57.3% reduction in allergy history assessment time — but explicitly notes limited medication-history-specific data, and completion is the weak point (22.7% full completion for family history assessment).

LLM work in this space is otherwise about medication review — interactions, dosing — not history elicitation.
No published study compares an AI-elicited medication history against a pharmacist BPMH reference standard. That is a clean, publishable, well-powered question with an established gold standard and an established outcome measure.
Does the intervention change outcomes
Structured history taking reliably reduces medication discrepancies; it has not been shown to reduce readmissions, adverse drug events or mortality, and the two best recent trials are null on utilisation despite large process effects.
What works on process
[MARQUIS2] (18 North American hospitals, 4,947 patients) reduced discrepancies from 2.85 to 0.98 per patient, adjusted IRR 0.95 per month (0.93–0.97). Its [component analysis] gives the most relevant numbers for this project:

 | 
Component | 
Adjusted rate ratio for discrepancies
 | 
BPMH in the ED by a trained clinician | 
0.40 (0.37–0.43)
 | 
Admission reconciliation by a trained clinician | 
0.57 (0.50–0.64)
 | 
Discharge reconciliation by a trained clinician | 
0.64 (0.57–0.73)
 | 
System-level components (7 of 8 categories) | 
0.75–0.97
Patients receiving both an ED BPMH and discharge reconciliation had 0.08 discrepancies per medication per patient — the lowest rate observed. Note the caveat: these are on-treatment, non-randomised comparisons within a quality improvement cohort.
The less-cited counterpart is [MARQUIS1], which missed its primary endpoint — potentially harmful discrepancies IRR 0.97 (0.86–1.08) — and whose on-treatment analysis found that training existing staff to take medication histories was associated with more harmful discrepancies. Training without dedicated resource did not work.
What does not work on outcomes

The two Cochrane reviews disagree. [Redmond 2018] (25 RCTs): ADEs RR 1.09 (0.91–1.30); unplanned rehospitalisation RR 0.72 (0.44–1.18), moderate certainty for "probably little or no difference". [Ciapponi 2021]: ADEs OR 0.38 (0.18–0.80), moderate certainty. Do not cite "Cochrane" without saying which.

[Anderson et al, AJHP 2019], an overview of 11 high-AMSTAR reviews: of the reviews examining clinically significant discrepancies, neither found an effect; of four examining clinical outcomes, none found benefit.

Observational and randomised evidence diverge systematically. Mekonnen's meta-analysis (17 studies, only 8 RCTs) reports readmission RR 0.81 and ED visits RR 0.72; RCT-restricted syntheses do not reproduce this.

[Jošt et al, Front Pharmacol 2024] (n=414): clinically important discharge errors 9.3% vs 61.9% (OR 0.05) — and 30-day unplanned utilisation 33.9% vs 27.8%, p=0.227, numerically worse in the intervention arm.

[PHARM-DC, JAMA Netw Open, March 2026], 6,478 hospitalisations already enriched for risk (age ≥55 plus ≥10 long-term medicines or ≥3 high-risk medicines): primary outcome null, 25.6% vs 26.4% 30-day unplanned utilisation, difference 0.9 percentage points (−1.7 to 3.5).
The one positive targeting signal
PHARM-DC's prespecified subgroup of 589 patients with low medication adherence and low literacy showed same-hospital unplanned utilisation of 18.3% vs 28.8% — a 10.4 percentage point absolute reduction (3.4–17.4, p=0.003), with significant effect modification. This converges with Pippins' finding that low patient understanding of preadmission medicines independently predicted errors.
It suggests the productive axis for targeting is patient comprehension and adherence, not medication count — which is notable because every deployed risk-stratification tool stratifies on medication count. The best-validated tool, [MED-REC Predictor], reaches AUC 0.67–0.68: usable for triage, not for excluding patients. Treat the subgroup finding as hypothesis-generating — one subgroup, in a null trial, on a secondary endpoint.
Implications for the agent's questioning design
Eight rules fall out of the evidence above and should govern the medication history section of the Symptom Questioning Library.

Do not rely on an open question. "What medicines are you on?" recovers prescribed oral medicines and little else. Category-by-category prompting is what produced Huber's fall from 69.9% to 29.6% of patients with a discrepancy. The open-then-narrow structure used for symptoms is the wrong shape here — medication history is a systematic inventory, not a saturation search.

Ask per medicine, not per list. For each medicine: what it is, what dose, how often actually taken, what for, who started it, how long, and whether any doses are missed. The 25.1% dose-regimen error rate in Elliott sits entirely in this gap.

Ask what has stopped. Cessation is invisible to every data source. Recently ceased medicines, short courses finished, and things the patient decided to stop should be elicited explicitly.

Capture allergy reactions verbatim, with type and timing, not just the agent name — 18.4% of charts carry a usable description.

Capture administration capability, not just the regimen: swallowing, inhaler technique, dexterity for drops and injections, vision for labels, who actually gives the medicine. This is where the half of Kripalani's cohort who needed help with a tablet lives, and where voice has an advantage over a screen.

Reconcile against a supplier source and surface the disagreements. The output to the clinician should carry three things: what the patient says they take, what the dispensing record says, and an explicit list of where they differ. The Francis source-type finding says this pairing is what produces accuracy.

Flag confidence, not just content. Where the patient is uncertain, says "a small white one", or defers to a carer, that uncertainty should reach the handover rather than being resolved into a confident list. A confidently wrong medication list is worse than a flagged incomplete one.

Escalate high-risk gaps. 20% of patients in Wai had a high-risk medication discrepancy. Anticoagulants, antiplatelets, insulin and other antihyperglycaemics, opioids, immunosuppressants and antiepileptics warrant a targeted confirmation loop and, where unresolved, an explicit note to the clinician — the same verbatim-words principle already agreed for red flags.
One structural note: the medication history is the part of the interview most likely to require a carer, a dose administration aid or a bag of boxes. The GP booking-call version cannot assume any of these are present; the ED room version can prompt for them. The two versions may need different closing logic here — the booking call should probably end by asking the patient to bring their medicines.
Implications for evaluation and study design
The medication history is the one domain where a validated reference standard and an established outcome measure already exist — which makes it the easiest section of the agent to evaluate rigorously, and the one most likely to produce a standalone publication.
Reference standard. A pharmacist-conducted BPMH is the accepted gold standard across Chen, Wai, Elliott, Francis and Pevnick. It is defensible to reviewers, familiar to Australian hospital pharmacy, and available at SA Health sites. Adopt it rather than consultant adjudication for this domain.
Primary endpoint. Discrepancies per patient against the BPMH, with severity grading. The convention in this literature is a three- or four-level clinical significance scale adjudicated by a blinded pharmacist and physician. Report both total and clinically significant discrepancies — Anderson's overview notes that interventions which move the first often fail to move the second.
Comparators worth having. The literature gives three natural arms, and the agent's claim differs against each:

 | 
Comparator | 
Published error rate | 
What a win means
 | 
Doctor-taken admission history | 
8.0 errors/patient (Pevnick); 27% of prescriptions (Henriksen) | 
The headline claim — plausible to beat
 | 
Patient self-administered form | 
75% of patients with ≥1 discrepancy (Wai) | 
Shows the conversation adds value over a form
 | 
Dispensing record alone | 
≥1 error in 99.4% (Elliott) | 
Shows the agent adds value over a data feed
Do not power on utilisation. PHARM-DC enrolled 6,478 hospitalisations in an already-enriched population and returned a null primary outcome; Jošt achieved a 20-fold reduction in clinically important errors with no effect on 30-day utilisation. Any protocol that promises readmission reduction is promising something two well-conducted recent trials failed to deliver. Frame the value proposition as accuracy at scale and clinician time released.
Secondary endpoints with precedent. Time to a complete medication history (against 58–90 minutes for a pharmacist); proportion of patients receiving any structured history at all (against 54% within 24 hours in the Brisbane audit); completion rate stratified by age, cognition, frailty and language — which Wai's companion paper did not report and which remains an open question in the self-entry literature.
A finding worth designing for. The PHARM-DC subgroup and Pippins both point at patient comprehension rather than medication count as the axis that matters. An agent can measure comprehension during the conversation — whether the patient can say what a medicine is for, what dose, why it was started. That is a variable no existing risk-stratification tool has access to, and capturing it prospectively would be novel in itself.
Open questions and reviewer status

 | 
Item | 
Status
 | 
Literature pass for medication history domain | 
Complete — first draft, not yet reviewed
 | 
Prompt inventory (13 categories) | 
Drafted from evidence; needs pharmacist review
 | 
Per-medicine questioning routes (dose, adherence, capability) | 
Drafted as principles, not yet written as question sets
 | 
Allergy / ADR question set | 
Drafted as principles, not yet written as question sets
 | 
Reconciliation logic against MHR or dispensing data | 
Not started — depends on data access decision
Open questions for review:

Should the medication history be a fixed inventory (the evidence favours this) even though the symptom sections use open-then-narrow? The two logics conflict and the transition between them needs a rule.

How long can the medication section run before the patient disengages? No published data on conversational fatigue for a 13-category inventory; the booking-call version is more constrained than the ED version.

Is there value in the agent asking the patient to read labels aloud, or to photograph boxes, where the channel allows it? Chen's data says containers are the worst single source (median 4 discrepancies), so this may add less than expected.

Should the agent attempt a cognitive screen before relying on self-reported medicines? Kripalani found need-for-help tracked with age and polypharmacy rather than literacy, which suggests a capability check is more useful than a literacy assumption.

Who reviews this domain — a hospital pharmacist is the obvious reviewer, and a different reviewer set from the symptom sections.
A paper worth retrieving that I could not access: Accuracy of best possible medication history documentation by pharmacists at an Australian tertiary referral metropolitan hospital, Integr Pharm Res Pract 2019 (PMID 31157067) — relevant Australian pharmacist-accuracy data, blocked at every route tried.
Sources
Accuracy of usual care and attribution of harm

[Tam VC, Knowles SR, Cornish PL, et al. Frequency, type and clinical importance of medication history errors at admission to hospital: a systematic review. CMAJ 2005;173(5):510–515]

[Pippins JR, Gandhi TK, Hamann C, et al. Classifying and predicting errors of inpatient medication reconciliation. J Gen Intern Med 2008;23(9):1414–1422]

[Quélennec B, Beretz L, Paya D, et al. Potential clinical impact of medication discrepancies at hospital admission. Eur J Intern Med 2013;24(6):530–535]

[Bell CM, Brener SS, Gunraj N, et al. Association of ICU or hospital admission with unintentional discontinuation of medications for chronic diseases. JAMA 2011;306(8):840–847]

[Crook M, Ajdukovic M, Angley C, et al. Eliciting comprehensive medication histories in the emergency department: the role of the pharmacist. Pharm Pract 2007;5(2):78–84]
Sources, method and who takes it

[Chen HH, Taylor SE, Harding AM, Taylor DMcD. Accuracy of medication information sources compared to the best possible medication history for patients presenting to the emergency department. Emerg Med Australas 2018;30(5):654–661]

[Francis M, Deep L, Schneider CR, et al. Accuracy of best possible medication histories by pharmacy students. Int J Clin Pharm 2023;45:414–420]

[Asakrh N, Abu Farha RK, Abu Hammour K, Al-Hashar A. Evaluation of the completeness of information sources used to prepare the best possible medication histories. Int J Clin Pract 2020;74(10):e13597]

[Pevnick JM, Shane R, Schnipper JL, et al. Improving admission medication reconciliation with pharmacists or pharmacy technicians in the emergency department: a randomised controlled trial. BMJ Qual Saf 2018;27(7):512–520]

[Henriksen JP, Noerregaard S, Buck TC, Aagaard L. Medication histories by pharmacy technicians and physicians in an emergency department. Int J Clin Pharm 2015;37(6):1121–1127]

[Aag T, Garcia BH, Viktil KK. Should nurses or clinical pharmacists perform medication reconciliation? A randomized controlled trial. Eur J Clin Pharmacol 2014;70:1325–1332]

[Venturini F, et al. Best possible medication history collection by clinical pharmacist in a preoperative setting. Pharmacy 2023;11(5):142]

[Nguyen CB, Shane R, Bell DS, et al. A time and motion study of pharmacists and pharmacy technicians obtaining admission medication histories. J Hosp Med 2017;12(3):180–183]

[Ryan M, Dunsdon J, Winckel K, et al. Evaluating the effectiveness of risk categories for prioritising patients for best possible medication history completion. Hosp Pharm 2026;61(1):81–88]
Prompting, categories and allergies

[Huber T, Brinkmann F, Lim S, et al. Implementation of an IT-guided checklist to improve the quality of medication history records at hospital admission. Int J Clin Pharm 2017;39(6):1312–1319]

[Monte AA, Anderson P, Hoppe JA, et al. Accuracy of electronic medical record medication reconciliation in emergency department patients. J Emerg Med 2015;49(1):78–84]

[Kiechle ES, McKenna CM, Carter H, et al. Medication allergy and adverse drug reaction documentation discrepancies in an urban, academic emergency department. J Med Toxicol 2018;14(4):272–277]
Australian data sources and guidance

[Elliott RA, Taylor SE, Koo SMK, et al. Accuracy of medication histories derived from an Australian cloud-based repository of prescribed and dispensed medication records. Intern Med J 2023;53(6):1002–1009]

[Francis M, Francis P, Makeham M, et al. Using personal health records for medication continuity during transition of care: an observational study. Health Inf Manag J 2025;54(2):150–159]

[Fung KW, Kayaalp M, Callaghan F, McDonald CJ. Comparison of electronic pharmacy prescription records with manually collected medication histories in an emergency department. Ann Emerg Med 2013;62(3):205–211]

[ACSQHC. Get it right! Taking a Best Possible Medication History]

[ACSQHC. Match Up Medicines: a guide to medication reconciliation]

[Australian Digital Health Agency. My Health Record prescription and dispense records]

[Australian Digital Health Agency. Electronic prescriptions and the Active Script List]
Patient-entered, digital and AI

[Wai A, Salib M, Aran S, Edwards J, Patanwala AE. Accuracy of patient self-administered medication history forms in the emergency department. Am J Emerg Med 2020;38(1):50–54]

[Wai A, et al. Patient completion of self-administered medication history forms in the emergency department. Australas Emerg Care 2019;22(2):103–106]

[Kripalani S, Hart K, Schaninger C, et al. Use of a tablet computer application to engage patients in updating their medication list. Am J Health-Syst Pharm 2019;76(5):293–300]

[Deo RC, et al. A conversational artificial intelligence agent for medication reconciliation and review. medRxiv 2025.06.16.25329719]

[Transforming health care through chatbots for medical history-taking: comprehensive systematic review. JMIR Med Inform 2024;26:e56628]
Outcome evidence

[Schnipper JL, et al. Effects of a refined evidence-based toolkit and mentored implementation on medication reconciliation (MARQUIS2). BMJ Qual Saf 2022;31(4):278–286]

[Schnipper JL, Reyes Nieva H, Yoon C, et al. What works in medication reconciliation: an on-treatment and site analysis of the MARQUIS2 study. BMJ Qual Saf 2023;32(8):457–469]

[Schnipper JL, et al. Effects of a multifaceted medication reconciliation quality improvement intervention on patient safety: final results of the MARQUIS study. BMJ Qual Saf 2018;27(12):954–964]

[Redmond P, et al. Impact of medication reconciliation for improving transitions of care. Cochrane Database Syst Rev 2018;CD010791]

[Ciapponi A, et al. Reducing medication errors for adults in hospital settings. Cochrane Database Syst Rev 2021;CD009985]

[Anderson LJ, Schnipper JL, Nuckols TK, et al. Effect of medication reconciliation interventions on outcomes: a systematic overview. Am J Health-Syst Pharm 2019;76(24):2028–2040]

[Lehnbom EC, Stewart MJ, Manias E, Westbrook JI. Impact of medication reconciliation and review on clinical outcomes. Ann Pharmacother 2014;48(10):1298–1312]

[Jošt M, Kerec Kos M, Kos M, Knez L. Effectiveness of pharmacist-led medication reconciliation on medication errors at hospital discharge and healthcare utilization. Front Pharmacol 2024;15:1377781]

[Pevnick JM, Kennelty K, Nguyen AT, et al. Pharmacist-led discharge care to reduce postdischarge health care utilization (PHARM-DC): a randomized clinical trial. JAMA Netw Open 2026;9(3):e260719]

[Van De Sijpe G, Gijsen M, Van der Linden L, et al. MED-REC Predictor: development and validation of a prediction model for clinically relevant medication discrepancies. J Med Internet Res 2024;26:e55185]