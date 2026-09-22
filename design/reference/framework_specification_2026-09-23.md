# Reference: AI History-Taking Agent — Framework Specification

Source: the product owner's Claude Doc, https://claude.ai/artifact/LWEZvRZimeub5WnUf42PKG (as of 2026-09-23). Plain-text extract; tables and diagrams flattened. The live doc is the source of truth.

---


AI History-Taking Agent — Framework Specification
 · 
This specifies how the agent behaves. What it asks about lives in the [Symptom Questioning Library], and the two are versioned separately because they change at different rates and are reviewed by different people.
The four layers
The agent is four layers with different owners, different evidence bases and different release cycles. Most of the design difficulty in this project comes from material belonging to one layer being written into another.

 | 
Layer | 
Owns | 
Source of truth | 
Changes when
 | 
Process | 
how the agent talks — sequence, question form, when to narrow, when to stop | 
the history-taking evidence review | 
rarely; it is externally evidenced and close to fixed
 | 
Content | 
what the agent asks about — slots, phrasings, likelihood ratios, red flags | 
the Symptom Questioning Library | 
every reviewer pass
 | 
Control | 
which module is active, whether saturation is reached, whether a red flag fires, what gets written where | 
this specification | 
the runtime changes
 | 
Handover | 
what the clinician receives — narrative, structured record, alerts, safety-netting | 
this specification | 
clinicians tell us it does not read right
The separation is not tidiness. It is what allows the dizziness module to be rewritten after a reviewer objects without re-validating the agent's conversational behaviour, and what allows the comparative study to state which library version produced each history while the process layer held constant.
how it talks] --> C[Control layerwhat happens next]
  L[Content layersymptom modules] --> C
  X[Context moduleshared values] --> C
  C --> H[Handover layerwhat the clinician gets]]]>
The control layer is the only place the three inputs meet. Nothing in the process layer knows about chest pain, and nothing in a symptom module knows how to open a conversation.
The process layer
The process layer is the agent's conversational policy: how it talks, independent of what the patient presents with. Every rule is written as a behaviour the agent must exhibit, paired with the observable evidence that it happened in a transcript.
That pairing is the point. The same table is the build specification and the rating rubric for the comparative study, so the rubric does not have to be invented separately once transcripts exist.

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
The slot schema
Every symptom module is written in one shape: a header, a list of slots, and a set of red-flag rules evaluated over those slots. Nothing in a module is prose the agent reads at runtime — the prose in the library is for reviewers, and the schema is what the agent is given.

 | 
Field | 
Holds | 
Why it is there
 | 
module, version, status | 
identifier, semantic version, grounded or first-draft | 
the study must record which library version produced each history
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
Chest pain, abbreviated to three slots. The likelihood ratios are those already tabulated in the library's cardiovascular section.

      cp.onset_character.onset == abrupt
      and cp.onset_character.quality in [tearing, ripping]
      and back in cp.radiation
    action: {ed: alert_triage, gp_booking: alert_gp_callback}
    alert:
      include_verbatim: true
      template: 'Possible aortic dissection. Patient said: {verbatim}. Onset {onset_clock_time}.'
    suppressible: false

closing:
  uncertainty: 'I cannot tell from talking with you whether this is coming from your heart.'
  watch_for: [pain returning at rest, pain with sweating or vomiting, pain with breathlessness]
  time_course: 'Someone will speak with you today.'
  where: 'If it comes back before then, call an ambulance rather than waiting.'

prohibited: [judging pallor, sweating or distress by appearance]
gaps:
  - 'No ECG and no troponin. Every negative in this module is a history negative only.']]>
The four slot classes
Coverage slots exist for completeness. They carry no likelihood ratio and need none, because the recorded negative is the product.
Discriminating slots must carry a likelihood ratio, what it discriminates, a citation, a grade and a derivation population — or evidence: {gap: true} with one line saying why none exists. This is Summerton's argument made mechanical: an unjustified discriminating question is indistinguishable from a coverage question, and the library should not let that difference go unrecorded.
Red flag slots feed rules rather than judgement. The rule is a boolean over filled slots, evaluated by code after the coverage sweep, never suppressed for low prior probability, and the alert carries the patient's own words.
Context slots are shared across modules and filled once per consultation. They are the subject of the next section.
The context module
Context slots are the values several symptom modules gate on. They are filled once per consultation, prefilled from the record wherever it holds them, referenced by id, and never re-asked inside a module.
The module exists because the library's shared gating questions already presuppose values nothing captures. “Could you be pregnant?” has no rule saying who is asked it. The AUDIT-C positivity threshold and the weight-loss investigation thresholds both vary by sex, against a field that did not exist anywhere in the schema.
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

      ctx.organ_inventory.uterus == present
      and ctx.age within param.childbearing_range
    phrasings:
      - {id: p1, form: open, text: 'Is there any chance you could be pregnant?'}
    value: {type: enum, options: [yes, no, unsure]}
    gates: [vaginal_bleeding, abdominal_pain, syncope, dizziness, vomiting, urinary, trauma]

  - id: ctx.medications
    intent: current medicines, with anticoagulants, antiplatelets, immunosuppressants
            and oral steroids named individually
    prefill_from: [booking_record]
    confirm: true          # a wrong value here is dangerous
    gates: [stroke_cluster, trauma, falls, haemoptysis, gi_bleeding, joint, fever, urinary]]]>
The remaining gating values — smoking as pack-years, unexpected weight loss, atrial fibrillation, family history of early sudden death, animal and bat exposure — take the same shape and are mapped in the library's shared gating table. param.childbearing_range belongs in the parameters table, since it is set by guideline rather than by evidence.
Asking, and not asking
Most context slots should never be asked. In the GP booking version the record holds age, recorded sex and usually the medication list; in ED they are on the triage screen. Cold-asking them is the fastest way to make the agent feel like a form, and it spends the two-minute opening budget (P3) on data the system already has. prefill_from with silent use is the default; confirm: true only where a wrong value is dangerous.
Where a slot must be asked, it arrives at the point of need with its reason attached — “because of where the pain is, I need to ask whether…” — rather than in an opening demographic block. Organ inventory in particular is asked only when a gating rule needs a field that is unknown, and P8's normalising preamble applies to it.
Sex as a modifier on the evidence
This reaches further than gating. Sex is the first context value that changes the evidence attached to a slot, not merely whether the slot is asked. The chest pain likelihood ratios above are pooled, and largely derived from cohorts in which women are under-represented. Applying 2.6 for bilateral arm radiation to a woman inherits that imbalance silently.
So evidence carries the derivation population, and says so when it cannot stratify:

Most entries will declare a gap. That is the honest state of the symptom literature, and a library that says so is better than one quietly applying a male-derived number. It also gives the comparative study something concrete to measure: whether the agent narrows or widens documented sex-based gaps is already an open question for reviewers, and this field is where the answer would be traced.
The control layer
The control layer decides what happens next. It is deterministic code over filled slots, not model judgement, and the split is what makes the agent auditable: every consequential decision can be traced to a rule and a value rather than to a generation.
 B[Facilitators only]
  B --> C{New symptom named}
  C -- yes --> B
  C -- no, after 3 phrasings --> D[Summarise back]
  D --> E[Activate symptom modules]
  E --> F[Fill required slots]
  F --> G[Coverage sweep]
  G --> H[Red flag rules over slots]
  H -- fires --> I[Alert carrying verbatim]
  H -- none --> J[Safety-net close]
  I --> J
  J --> K[Handover plus structured data]]]>
The controller owns which module is active, and therefore which slots are in context; the saturation count that closes the problem list (P13); the end-of-consultation sweep for unfilled required slots; red-flag evaluation and routing; and every structured field write, each stamped with the turn it came from (P12).
The model owns which phrasing to use, which cue to follow, when to elaborate, and how to word the handover — all inside the process layer's rules.
Two consequences worth stating plainly.
Retrieval, not prompting. Only the active module's slots enter context. Hand the model the whole library and it interrogates checklist-style, and the history stops feeling like a registrar took it. Coverage is enforced by the sweep at the end, not by having everything present from the start.
The sweep runs before the red-flag rules, and the rules run over slots rather than over the transcript. A red flag that depends on an unfilled required slot is a missing answer, not a negative. The controller distinguishes the two, and the handover carries the difference.
The handover layer
The handover is a contract, not a rendering. It is the only part of the system a clinician acts on, so what it must contain is specified rather than left to generation.

 | 
Part | 
Contains | 
Generated from
 | 
Narrative | 
the registrar handover — the patient presented as a good registrar would present them | 
the filled slots
 | 
Structured record | 
every filled slot with its coded value, its verbatim where flagged, and the turn it came from | 
the slot writes themselves
 | 
Alerts | 
each fired red flag, with the patient's own words and the clock time | 
the red-flag rules
 | 
Safety-net record | 
what the patient was told at the close | 
the module's closing block
The narrative is generated from slots, never from the transcript. Anything in the narrative with no slot behind it is a hallucination surface. This is what makes P12's provenance useful rather than ceremonial: every clause traces to a field, and every field to a turn.
Unfilled required slots appear as not asked, never as negative. The control layer distinguishes a missing answer from a negative answer, and the handover has to preserve that distinction or it silently manufactures reassurance.
Negatives are reported per slot, not by one convention. negative_reporting: explicit where the negative changes what the clinician does; omit where listing it is noise. A single reporting convention across all presentations is exactly what the library's asymmetry rule warns against.
Gaps are stated, not implied. Where the agent cannot see — rash blanching, papilledema, fetal heartbeat, anal tone — the handover says so. A history that looks complete while being structurally incomplete is more dangerous than one that is obviously partial.
The clinician can question it, within limits. The agent stays available for clarifying questions about the handover, answering only from filled slots and verbatim. Asked something it did not ask the patient, it says so. It must not infer to fill a gap under questioning — that is the failure mode this whole layer exists to prevent.
Language. The history may be taken in any supported language; the narrative and structured record return in English. Verbatim quotes are kept in the original alongside a translation, and a translated verbatim is marked as translated. An alert that carries the patient's words needs to be clear about which words those actually were.
The format is a testable arm, not a settled design choice. Whether narrative-plus-structured beats structured-alone for clinician decision-making is unstudied and answerable, and is probably the more novel contribution of the study.
Versioning and authoring checks
Each layer carries its own version, and the study records all four against every history it produces. The process layer is close to fixed; the content layer moves with every reviewer pass. Coupling them would mean re-validating conversational behaviour every time a reviewer rewords a dizziness question, which is the failure this separation exists to prevent.
Within the content layer, versioning is per module. A module carries version and status, and a change to one module does not bump the others. Slot ids are the stable surface: the handover, the alerts and the study dataset all key on them, so an id may not be reused and may not change without a version bump.
Because colleagues edit the library directly, these run over it at build time rather than being left to review:

Every stored phrasing passes the P7 polarity check.

Every discriminating slot carries a likelihood ratio and citation, or a declared gap.

Every red-flag rule references only slot ids that exist in its own module or in the context module.

Every stigmatised slot has a normalising preamble (P8).

Every module has all four closing components (P14).

No slot id is reused, and no id changes without a version bump.

Every likelihood ratio declares a derivation population. Any marked population: pooled on a presentation with known sex-based diagnostic disparity declares either a stratified value or an explicit gap.

No gating rule references ctx.gender or ctx.sex_recorded.
Check 8 is the one that keeps the three-slot split from quietly collapsing back into one the next time someone adds a module.
What this does not settle

 | 
Open question | 
Current position | 
What would settle it
 | 
The voice layer | 
no platform chosen, and every result behind this specification is text or form-based | 
accuracy work of its own on ASR: symptom vocabulary, accented English, and the target non-English languages. No voice claim rides on text evidence
 | 
The ED version's evidence base | 
no published analogue; undifferentiated walk-in presentation is unstudied. The GP version has the Boston pre-visit feasibility study as its nearest analogue | 
the simulated-patient study first, then the paired comparison
 | 
Comparator framing | 
differs by version — GP booking against a status quo where none of this information exists at booking, ED against a clinician history on the same patient | 
decided; stated here so the two arms are not reported as though they were one
 | 
Adjudicating disagreement | 
Stockholm found 80% of patients recorded in the EHR as having jaw or neck radiation denied it to a computer, and 50% with an explicit negative entry reported it | 
an adjudication protocol that lets the consultant record “agent right, clinician wrong” as a distinct outcome
 | 
Whether agreement is the right primary outcome | 
documented under-triage of older patients and of Black and Hispanic patients in abdominal pain assessment suggests equity is the more valuable question | 
a decision before the protocol is written, not after
 | 
The saturation rule (P13) | 
grade B — transferred from qualitative method, not demonstrated in consultations | 
the phrasing-yield log, which records which invitation pulled the last new symptom
 | 
Which presentations the agent refuses to take | 
currently intoxication, significant cognitive impairment and acute distress | 
a runtime decision rule, and an owner for it. Neither exists yet
 | 
Escalation threshold in the GP version | 
differs from ED because the patient is at home and the interval to human contact is longer | 
not yet set
The first and the last of these are the ones that block a pilot. The rest can be settled while building.