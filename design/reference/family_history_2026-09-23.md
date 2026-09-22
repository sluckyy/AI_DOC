# Reference: Comprehensive Family History — Evidence Base

Source: the product owner's Claude Doc, https://claude.ai/artifact/K5aj96b2E4iH3qA5qBzC6R (as of 2026-09-23). Plain-text extract; tables and diagrams flattened. The live doc is the source of truth.

---


Comprehensive Family History — Evidence Base
 · 
Family history is well supported as a risk marker at defined thresholds and poorly supported as a routine comprehensive activity — but the trials that produced the negative findings tested collection without action, in a setting where 15–30 minutes of clinician time dominated the trade-off. An agent that removes the time cost and attaches thresholds to the output is not the intervention those trials evaluated.
Summary
The evidence base splits cleanly into three questions that are usually run together, and they have different answers. Whether family history predicts disease: yes, robustly, at defined thresholds. Whether patients report it accurately: yes for first-degree relatives and common sites, poorly otherwise, and asymmetrically — a report is worth much more than a denial. Whether routinely collecting a comprehensive family history improves outcomes: unproven, with the only substantial randomised test returning null.

 | 
Claim | 
Evidence strength | 
What it rests on
 | 
A positive family history is associated with elevated disease risk | 
Strong | 
Consistent across disease categories in the NIH State-of-the-Science review
 | 
Self-report is accurate for first-degree breast and colon cancer | 
Strong | 
Rational Clinical Examination meta-analysis, 14 validation cohorts
 | 
Self-report is accurate for second-degree relatives and less common sites | 
Weak | 
Same meta-analysis; wide and variable confidence intervals
 | 
Family history definitions discriminate risk at the individual level | 
Weak | 
NIH review: "low discriminatory accuracy" for most definitions
 | 
Structured collection identifies people who meet guideline thresholds others miss | 
Moderate | 
Family Healthware, MeTree, EMR-concordance studies
 | 
Collecting family history changes screening behaviour or outcomes | 
Insufficient | 
One adequately sized RCT, null; NIH review found insufficient evidence
 | 
Collection causes psychological harm | 
No evidence of harm | 
Only three studies, all reassuring
The practical reading is that the negative evidence is about what happens after collection, not about the information itself. Family Healthware identified a third of its cohort as at moderate or strong familial risk for at least one cancer and still moved nothing, because identification without clinician engagement and decision support does not act on itself. The 15–30 minutes of clinician time that comprehensive collection has historically required is what made that trade-off look bad, and it is the part an agent removes.
Accuracy of what patients report
Reporting error is overwhelmingly one-directional: people under-report rather than invent. The NIH review found [high specificity and low sensitivity] across every disease category examined, which means a positive report is close to conclusive and a negative report carries much less information than clinicians treat it as carrying.
The [Rational Clinical Examination meta-analysis] of 14 validation cohorts quantifies the asymmetry by site and degree of relationship.

 | 
Report | 
LR+ (95% CI) | 
LR− (95% CI) | 
Reading
 | 
Breast cancer, first-degree relative | 
41.0 (23.0–75.0) | 
0.07 (0.03–0.13) | 
Both directions informative
 | 
Colon cancer, first-degree relative | 
23.0 (8.1–64.0) | 
0.29 (0.13–0.67) | 
A denial only weakly lowers risk
 | 
Ovarian, endometrial, prostate | 
Similar point estimates | 
Wider intervals | 
Treat as provisional
 | 
Second-degree relatives, any site | 
Variable | 
Variable | 
Not reliable without verification
The authors' conclusion is that first-degree breast and colon cancer reports are accurate enough not to require independent verification, and that other sites and second-degree relatives are not.
Two findings matter more for agent design than the likelihood ratios do, because they are about the question rather than the patient.
The first is that a brief enquiry and a structured questionnaire are not interchangeable. A [comparison across two randomised trials] (310 participants for coronary heart disease, 557 for diabetes) found the simple enquiry missed most positive histories it should have caught.

 | 
Family history sought | 
Sensitivity of simple enquiry | 
Specificity | 
False negatives
 | 
Coronary heart disease, first-degree | 
44.2% | 
89.3% | 
55.8%
 | 
Diabetes, first-degree | 
81.9% | 
97.0% | 
18.1%
 | 
Diabetes, second-degree | 
35.4% | 
94.5% | 
64.6%
The authors concluded that the simple enquiry identifies most people with no significant family history but misses a significant proportion of those with one — which is the wrong error to make, since the whole purpose is finding the positives.
The second is that reporting is [sensitive to small changes in wording]. In a randomised web survey of 2,917 parents, adding the parenthetical "(including your extended family)" to an otherwise identical question raised reported cancer history from 45.7% to 65.1% and cardiovascular history from 56.0% to 72.5%, and raised the mean number of conditions reported from 3.4 to 4.4. Nineteen percentage points of apparent prevalence sat in five words of prompt.
What a positive family history actually buys
Association and discrimination come apart here, and conflating them is the most common error in this literature. Family history is reliably associated with elevated risk and is a poor individual-level discriminator. The NIH review put it plainly: despite consistent associations with elevated risk, [many family history definitions showed low discriminatory accuracy] in predicting disease risk in individuals.
The cardiovascular literature shows the pattern well. In the [Aberdeen Study of Cardiovascular Health in Women] (945 women, 22% with coronary heart disease), family history was independently significant at an odds ratio of 1.7 (95% CI 1.26–2.47), and adding it to guideline-defined risk factors moved the c-statistic from 0.603 to 0.631 with a net reclassification index of 0.015 that did not reach significance. Eighteen women were correctly reclassified and four incorrectly.
That is the honest general picture for common multifactorial disease: real signal, small incremental discrimination once conventional risk factors are known. It is why guidelines that use family history for cardiovascular risk almost always use it as a threshold-crossing or reclassification factor for people already near a decision boundary, rather than as a variable inside the risk equation.
The value concentrates in two places instead.

Monogenic and syndromic conditions, where the family history pattern is not a weak continuous predictor but the main diagnostic clue — familial hypercholesterolaemia, Lynch syndrome, BRCA-associated cancer, inherited arrhythmia, connective tissue disease, thrombophilia. Here a pedigree pattern changes the diagnostic category, not the decimal place on a risk estimate.

Presentation-specific decision points, where family history shifts the differential in front of you — sudden cardiac death in a relative under 40 in a patient with syncope, a first-degree relative with venous thromboembolism in a patient with pleuritic chest pain, bipolar disorder in a relative of a patient presenting with depression.
The design consequence is that "comprehensive" should mean comprehensive across the trigger patterns that have actions attached, not comprehensive in the sense of enumerating every condition in every relative. Those are different targets, and only the first has evidence behind it.
Does collecting it change anything?
This is where the evidence is thinnest, and where the field's own summaries are most cautious. The NIH panel found [insufficient evidence] to assess the effect of family-history-based risk assessment on preventive behaviours — not evidence of no effect, but too little to judge.

 | 
Study | 
Design and size | 
Identification | 
Downstream effect
 | 
[Family Healthware] | 
Cluster RCT, 41 practices, 3,283 patients aged 35–65 | 
34% at moderate or strong familial risk for ≥ 1 cancer; 4.4% eligible for earlier colonoscopy; 9% of women 35–39 eligible for earlier mammography | 
No significant difference in screening rates overall or within risk strata
 | 
[MeTree] | 
Hybrid implementation–effectiveness, 3 clinics, 1,184 patients, 27,406 relatives | 
Risk stratification for breast, ovarian and colorectal cancer, hereditary syndromes, thrombosis | 
39% learned of relatives' conditions they had not known; high acceptability; guideline-change proportions not clearly reported
 | 
[Systematic review of familial cancer interventions] | 
3 studies from 11,842 abstracts — 2 cluster RCTs, 1 NRSI | 
All used risk assessment software | 
Guideline-concordant breast genetic referrals improved (OR 4.5, 95% CI 1.6–13.1); no difference in screening adherence in the other RCT
Three things are worth saying about the null results rather than simply reporting them.
Family Healthware was badly underpowered for its screening endpoint — statistical power of 0.06 to 0.19 — because the volunteer population was affluent, well educated and already screening well above national rates (76% versus 61% for mammography). A null in a population with little room to improve is weak evidence of no effect.
The trials tested information delivery, not care redesign. Family Healthware's authors concluded that engagement of clinicians and patients, integration with clinical decision support, and inclusion of non-familial risk factors may be necessary for computerised risk assessment to reach its potential. Tailored written messages to patients, with no clinician in the loop, is a weak intervention by design.
The one positive signal is the one closest to an actionable threshold: referrals that met guideline criteria rose more than fourfold. Where the output was a specific referral decision rather than a general risk message, something moved.
The reviewers' summary is the fair conclusion — no study measured the primary outcomes of interest, and no outcome was consistent across the three studies. The negative evidence is an absence of well-designed trials, not a demonstration of futility.
What actually gets recorded, and what it costs
The comparator for any new method of collecting family history is not a good family history. It is a mostly absent one.
The clearest demonstration comes from a [BJGP analysis] of 867 adults diagnosed with breast cancer under 40. Roughly 1,474 children at genetic risk would have been expected; 382 were identifiable in the records, and of those only 31% had a family history recorded. Of the children of 198 men with breast cancer, one had any family history documented.
A comparison of a [focused hereditary cancer questionnaire against EMR documentation] found agreement degraded exactly where it mattered most.

 | 
Patient's familial risk level | 
Agreement between questionnaire and EMR
 | 
Low | 
56.4%
 | 
Medium | 
22.9%
 | 
High | 
0%
None of the high-risk patients had an EMR family history that matched what they reported when asked systematically. The questionnaire identified 25 high-risk and 76 medium-risk patients who warranted genetic counselling consideration and were not flagged by routine documentation.
The cost side explains most of this. The BJGP authors cite 15 to 30 minutes of practitioner time to collect a family history, with completeness limited by what the patient can recall in the room. MeTree's patient-completed version averaged [27 minutes] with a range of 8 to 118. In a 15-minute consultation with a presenting complaint to address, that is not a marginal cost — it is the entire consultation.
Clinician attitudes are consistent with cost rather than scepticism being the binding constraint. In a [2025 survey of 257 family physicians], mean perceived usefulness of family history was 4.07 out of 5 and only 3.5% never asked — but perceived usefulness and perceived barriers were positively correlated (rho 0.341, p < 0.001). The doctors who take it most seriously are the ones most aware of why it does not happen.
Where family history changes management
These are the patterns with an action attached in Australian practice. They define what the agent has to be able to elicit — not conditions, but relationships, ages at diagnosis and counts.

 | 
Pattern to elicit | 
Threshold | 
Action | 
Source
 | 
Colorectal cancer in relatives | 
One first-degree relative diagnosed < 55, or two first-degree relatives at any age | 
Category 2: biennial iFOBT from 40–49, then colonoscopy 5-yearly from 50 | 
[Revised national guidelines, MJA 2018]
 | 
Colorectal cancer in relatives | 
Three or more first-degree relatives at any age, or three first- or second-degree with one < 55 | 
Category 3: biennial iFOBT from 35–44, then colonoscopy 5-yearly from 45 | 
As above
 | 
Breast cancer in relatives | 
One or two first-degree relatives diagnosed < 50 | 
Moderately increased risk: annual clinical examination, annual mammography from 40 | 
[BreastScreen WA / Cancer Australia categories]
 | 
Breast and ovarian cancer on one side | 
Two close relatives plus a high-risk feature — onset < 40, bilateral disease, male breast cancer, Ashkenazi Jewish ancestry | 
Refer for genetic risk assessment | 
As above
 | 
Premature cardiovascular disease | 
Coronary heart disease or stroke in a first-degree female relative < 65 or male relative < 55 | 
Reclassification factor — consider moving to a higher risk category when calculated risk is near a threshold | 
[2023 Australian CVD guideline]
 | 
Familial hypercholesterolaemia | 
Premature CVD in relatives, known FH in a relative, or relatives with markedly elevated cholesterol | 
Lipid assessment, Dutch Lipid Clinic Network scoring, cascade testing of relatives | 
[Australian integrated guidance for FH]
Family history is not in the [Aus CVD Risk Calculator] itself — a point worth noting, because it means the information has no home in the calculation and only earns its place through a clinician's judgement at the margin. That is exactly the kind of step that gets skipped when it was never collected.
The acute presentations where family history changes the differential in front of you are a shorter list, and they matter for the emergency department version of the agent.

 | 
Presentation | 
Family history that changes the assessment
 | 
Syncope, palpitations, cardiac arrest in a young person | 
Sudden or unexplained death in a first-degree relative under 40; known inherited arrhythmia or cardiomyopathy
 | 
Chest or back pain | 
Aortic dissection, aneurysm, Marfan or other connective tissue disease in a first-degree relative
 | 
Pleuritic chest pain, breathlessness, limb swelling | 
Venous thromboembolism in a first-degree relative, especially unprovoked or under 50
 | 
Thunderclap headache | 
Subarachnoid haemorrhage or polycystic kidney disease in a first-degree relative
 | 
Depressive presentation | 
Bipolar disorder in a first-degree relative — changes antidepressant risk–benefit
 | 
Unwell child | 
Consanguinity, prior unexplained infant or childhood death, known metabolic or genetic condition
Outside these lists, a comprehensive family history is best understood as risk information for someone else to act on later, not as a contribution to today's decision.
Harms, acceptability, and the meaning of a negative
The harm case against asking is weak. The NIH review found [no evidence of significant harm] from family history collection on psychological outcomes, though it rested on only three studies. The familial cancer systematic review found [no change in psychological distress] among patients identified at increased familial breast cancer risk, and reduced anxiety among those found to be at population risk — the reassurance effect outweighing the alarm effect.
Acceptability is high. In MeTree, patients rated the tool [easy to use (93%), easy to understand (97%) and useful (98%)]; 85% said it raised their awareness of disease risk. Fourteen physicians reported it improved their practice (86%) and made practice easier (79%).
The real risk is different, and it is a risk the agent creates rather than inherits. A structured family history section produces a negative result where previously there was silence, and a documented negative is treated as information in a way that an absent field is not. Given low sensitivity across every disease category, and a simple enquiry missing 55.8% of positive coronary heart disease histories, the negatives will often be wrong.
Three specific failure modes follow.

Adoption not knowledge. A patient who is adopted, estranged, donor-conceived or from a family that does not discuss illness has no family history to give. "No family history of bowel cancer" and "does not know their family history" must be different values with different downstream behaviour.

Recall at the point of asking. In MeTree, 39% of patients learned about relatives' conditions only after going and asking them. Anything asked in a single synchronous encounter is bounded by what the patient happens to remember.

False reassurance downstream. A clinician reading a clean structured family history in a handover has been given more confidence than the underlying data supports, particularly for second-degree relatives, where reporting sensitivity falls below 40% in both the diabetes and coronary heart disease comparisons.
The mitigation is representational, not conversational: the agent should distinguish asked and denied, asked and unknown, and not asked, and the handover should carry the distinction rather than collapsing all three into an absent finding.
Implications for the agent
The design decision is to always ask. The evidence does not contradict this, because the evidence against comprehensive collection is really evidence about a 15–30 minute clinician-time cost and about information delivered without an action attached. Remove the time cost and attach the thresholds, and neither objection survives. The defensible framing for a reviewer or an ethics committee is that the agent is not the intervention that Family Healthware tested.
The argument has the same shape as the one already made about red flags at booking: the comparator is not a good family history, it is the 69% of at-risk children with nothing recorded at all.
Structure the section around triggers, not conditions
Ask what the thresholds in the table above need: who (degree of relationship, which side), what (specific diagnosis, not "heart problems"), when (age at diagnosis), how many (count of affected relatives). A section built as an open-ended "any illnesses in the family?" will not produce a single guideline-actionable output.
Ask about extended family explicitly
The wording study is the cheapest available gain in the whole document. Naming extended family in the prompt raised reported cancer history by 19 percentage points and cardiovascular history by 17. The agent should ask about second- and third-degree relatives by name of relationship — grandparents, aunts, uncles, cousins, on each side — rather than relying on the patient's own definition of "family".
Record three states, not two
Denied, unknown and not asked are different. Adoption and estrangement need an early branch that closes the section gracefully rather than generating a long run of "no" answers that will read as a clean negative history.
Exploit asynchrony in the GP version
This is the design advantage the emergency department version does not have. More than half of MeTree's patients went and talked to relatives, and 39% learned something new. The booking-call version can end the family history section with a specific ask — which relatives to check with, about what — and pick it up on a short second pass before the appointment. That is a testable arm in its own right and, as far as I can find, nobody has run it with a conversational agent.
Hand over the pattern, not the list
The registrar framing applies here more than anywhere. What the clinician needs is "two first-degree relatives with bowel cancer, one diagnosed at 48 — meets category 2 criteria for earlier colonoscopy", not a table of eleven relatives. The structured data sits underneath; the narrative line states the pattern and names the threshold it crosses.
Evaluation: score family history separately
This is a methodological warning for the comparative study. Family history is a domain where the agent will show high apparent superiority for an uninteresting reason — the emergency doctor did not ask, because in that setting it is usually not worth the time. Pooling it with the presenting complaint will inflate overall disagreement and invite the criticism that the comparison was rigged.
Two options, both defensible:

Adjudicate family history as its own domain with its own agreement statistic, and report it separately from the presenting complaint.

Score it against a reference standard — a consultant-taken structured family history on the same patient — rather than against what the treating doctor happened to document.
The second is more work and answers a better question: not "did the agent capture more than the doctor wrote down", but "did the agent capture what a careful clinician with unlimited time would have captured". Given that simulated patients come with a known scripted family history, that reference standard is available to you for free in the first phase.
References
Evidence reviews

[NIH State-of-the-Science Conference: Family History and Improving Health] (2009) — the core appraisal of accuracy, validity, utility and harms

[Does this patient have a family history of cancer? An evidence-based analysis of the accuracy of family cancer history] — Rational Clinical Examination, 14 validation cohorts

[Effectiveness of interventions to identify and manage patients with familial cancer risk in primary care: a systematic review], J Community Genet 2019

[Family history tools for primary care: a systematic review], Eur J Gen Pract 2022
Trials and comparative studies

[Clinical utility of family history for cancer screening and referral in primary care: a report from the Family Healthware Impact Trial], Genet Med 2011

[Patient and primary care provider experience using a family health history collection, risk stratification, and clinical decision support tool (MeTree)], BMC Fam Pract 2013

[How does a simple enquiry compare to a detailed family history questionnaire to identify coronary heart disease or diabetic familial risk?], Genet Med

[Family health history reporting is sensitive to small changes in wording], Genet Med 2016

[Comparison of a focused family cancer history questionnaire to family history documentation in the electronic medical record], J Prim Care Community Health 2022

[Family history: impact on coronary heart disease risk assessment beyond guideline-defined factors], Public Health Genomics 2013
Practice and documentation

[Time to rethink the capture and use of family history in primary care], Br J Gen Pract 2016

[Routine family history inquiry among family physicians: associations with perceived clinical usefulness and barriers], Front Med 2026
Australian guidance

[Revised Australian national guidelines for colorectal cancer screening: family history], MJA 2018

[2023 Australian guideline for assessing and managing cardiovascular disease risk], MJA 2024, and the [Aus CVD Risk Calculator]

[Family history guidelines for GPs — breast cancer risk categories], BreastScreen WA, 2022

[Synopsis of an integrated guidance for enhancing the care of familial hypercholesterolaemia: an Australian perspective]
Companion documents: Medical History Taking — Evidence Review and Design Implications, Evidence Base for the Comprehensive Social History, Functional & Situational History — Evidence Base, and the AI History-Taking Agent — Symptom Questioning Library.