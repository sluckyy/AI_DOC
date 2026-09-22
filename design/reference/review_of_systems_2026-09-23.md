# Reference: Evidence Base for the Comprehensive Review of Systems

Source: the product owner's Claude Doc, https://claude.ai/artifact/Hh5dybspUQwq1BSHQd8GiG (as of 2026-09-23). Condensed extract written from a full read; the live doc is the source of truth.

## Bottom line

No trial has compared a comprehensive review of systems (ROS) against none on any patient outcome. Four or five small observational yield studies, mostly US and 1990s: per-question positive predictive value about 3%, per-patient yield of a new acted-on diagnosis 5 to 10%, and roughly 40% of positives already known from the presenting complaint or past history. US billing rules kept the practice alive; they were withdrawn in 2021 without any claimed diagnostic loss.

## Yield studies

- Verdon and Siemens 1997, 248 new family-medicine patients, 20-item self-completed ROS: 26 new diagnoses (10.5% of patients), PPV per positive answer 3.3%. Of positives: 27.4% already in the chief complaint, 12.1% already in past history, 33.8% addressed and judged benign, 22.3% never referenced in the record.
- Mitchell 1992, 550 medical admissions, cardiopulmonary and GI only: about 5% yield, two patients with plausible life-years gained.
- Boland 1995, periodic health examination, 100 patients: therapeutic yield 7% for ROS, 5% physical examination, 0% ECG and CXR. A screening context, not a presenting-complaint one.

None measured whether the ROS changed the diagnosis of the presenting problem.

## Critique

- Hoffbrand 1989: the complete enquiry generates more false trails than diagnoses; question by the differential in hand.
- Rodriguez 2010, 173 discharged ED patients: serious ROS complaints were only modestly more likely than non-serious ones to prompt a test, be documented, or be expected to be addressed; proposed a short "serious ROS" of red flags.
- Weiner 2020, 105 encounters with unannounced standardised patients against concealed audio: 90% of notes had at least one error; 73% of ROS errors were commissions, documented negatives never asked ("no shortness of breath" in an asthmatic); notes inflated visit level by 74%. The ROS as it appears in the record is substantially fiction.
- Kroenke: symptom prevalence is high and disease prevalence low, so an unselected positive carries almost no information; symptom count tracks distress more than pathology. A comprehensive ROS recruits true-but-irrelevant positives.
- Hampton 1975 and Peterson 1992 are evidence for talking to patients, not for the systems review; neither isolates the ROS.

## What the evidence supports

Not comprehensiveness, but individual items on their own likelihood ratios: red-flag questions attached to a specific presentation; pertinent negatives that move a named differential; case-finding items with independent screening evidence (depression, alcohol, unintentional weight loss, B symptoms, falls). The ROS has some value as a structured prompt against premature closure and for catching the second problem, and essentially none as an undifferentiated screen.

## Implications for the agent

The parsimony argument is about clinician time, which an agent removes; the false-positive load does not vanish but transfers to the handover. So the agent probably should take a full systems review because asking is cheap, and the design question is what the registrar surfaces. Verdon's breakdown as a specification: positives already in the presenting complaint or past history are reconciled silently; benign on the patient's own account go to the collapsed structured layer only; the roughly 10% that move the differential or are red flags go to the narrative handover.

Study design: nobody has measured the yield of an AI-conducted systems review against a reference standard (new-diagnosis yield needs real patients; simulated patients measure elicitation agreement only). Weiner's commission finding gives the cleanest efficacy endpoint: "truthful pertinent negatives", since an agent that asks has true documented negatives while about three quarters of documented ROS negatives in practice were never asked.

One interaction to settle before starting: a full ROS run after symptom saturation will always produce new symptoms. Decide in advance whether ROS-elicited symptoms count toward the agreement endpoint or sit in a separate stratum; otherwise they dominate disagreement against the emergency doctors' histories and the comparison measures the ROS rather than the agent.

## Gaps

No randomised comprehensive-versus-targeted comparison; no study isolating ROS contribution to the presenting complaint; no non-US evidence of substance; no evidence on AI-conducted systems review yield.
