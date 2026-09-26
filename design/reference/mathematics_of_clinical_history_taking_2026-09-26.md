# The Mathematics of Clinical History Taking

_A formal framework for conversational inference, shared meaning, repair, attention, psychological safety and learning in clinical dialogue. Working conceptual paper, prepared from the conceptual development of the Perioperative Conversational AI programme, September 2026. Status: theory-building draft for research, technical specification and prospective validation._

_Reproduced from the product owner's source document (`Mathematics_of_Clinical_History_Taking_Conceptual_Framework.docx`, supplied 2026-09-26) for in-repo traceability. D-63 records which parts of this framework are built into Dr Sam and which are deliberately deferred; see `design/10_mathematics_framework_mapping.md` for the section-by-section mapping._

---

## Abstract

Clinical history taking is usually described as a communication skill or a structured process for eliciting facts. This paper proposes a more formal account: clinical conversation is a cooperative, partially observable, continuous-time stochastic control process in which patient and clinician jointly construct, test, repair and progressively ground a clinically useful representation of reality. The history is therefore not simply extracted from a patient. It emerges through interaction, and the interviewer’s questions, timing, reflections, summaries, silences, explanations and interpersonal behaviour alter the data-generating process itself.

The framework integrates Bayesian inference, information theory, partially observable Markov decision processes, control theory, conversation analysis, grounding, pragmatics, game theory, mechanism design, attention and memory models, causal inference and constrained reinforcement learning. It introduces a Shared Meaning Workspace that separates raw utterance, semantic interpretation, pragmatic inference, clinical hypothesis, patient-grounded proposition, external verification and clinical adjudication. Conversational repair is treated as a first-class safety mechanism, with dependency-aware truth maintenance when corrected information has already influenced downstream inferences.

The model also formalises active listening, silence, interruption, turn-taking, patient agency, psychological safety, epistemic humility, normalisation, appropriate affiliative humour and prospective conversational obligations. A separate learning plane is proposed to determine which conversational actions work best, for whom and under what circumstances, while preventing uncontrolled online experimentation or self-modification. The resulting framework offers a basis for designing, evaluating and governing clinical conversational AI, while also generating testable hypotheses about human history taking itself.

## Keywords

clinical history taking; conversational AI; medical interview; active listening; grounding; conversational repair; pragmatics; psychological safety; causal inference; reinforcement learning; POMDP; FHIR; patient-centred communication

## Central thesis

The purpose of clinical conversation is to minimise consequential uncertainty between two minds sufficiently to enable safe, informed and patient-aligned action.

## 1. Introduction

Clinical history taking is commonly taught as a sequence of communication behaviours: begin openly, listen, clarify, move from open to closed questions, summarise and verify. Clinical curricula also emphasise rapport, empathy, signposting and shared decision-making. These principles are useful, but they are usually taught descriptively rather than as components of a coherent computational or mathematical system.

The distinction matters for conversational AI. A human clinician can rely on tacit expertise developed through thousands of interactions. A clinical conversational agent requires an explicit account of what constitutes conversational state, how uncertainty should be represented, when an inference may be promoted to fact, when silence is preferable to another question, how misunderstanding is repaired and how the system can improve without learning unsafe or manipulative behaviours.

A questionnaire model is insufficient. It assumes that the relevant facts exist in stable form within the patient and that the task is to retrieve them. Real history taking is different. Patients interpret questions, remember while speaking, revise earlier accounts, introduce unanticipated concerns, use imprecise language, infer why questions are being asked and decide whether disclosure is socially safe. The interviewer also influences what is subsequently said. Clinical conversation is therefore both an inference process and an intervention.

## 2. A unified formalisation

We define clinical conversation as a cooperative, partially observable, continuous-time stochastic control process over a dynamically constructed shared epistemic state.

Clinical conversation = cooperative inference + control + grounding + repair + learning

There are two interacting agents: the patient P and the clinician or conversational agent C. Each has private knowledge, goals and uncertainty. The observable interaction consists of words, timing, pauses, prosody, corrections, topic shifts and other conversational signals.

bₜ(Z) = P(Zₜ | O₀:ₜ)

The clinician does not directly observe the patient's complete internal state Z. It maintains a belief distribution b over possible states given the interaction history O. This leads to a foundational safety principle: an interpretation is a belief about reality, not reality itself.

## 2.1 Patient and clinician latent states

Zᴾₜ = {Kᴾₜ, Gᴾₜ, Eᴾₜ, Iᴾₜ, Prefᴾₜ}

Zᶜₜ = {Kᶜₜ, Gᶜₜ, Hᶜₜ, Rᶜₜ, πₜ}

K denotes knowledge, G goals, E emotional state, I intentions, Pref preferences, H hypotheses, R clinical risk representation and π the current conversational policy. The two agents possess overlapping but non-identical information and objectives.

## 3. The Shared Meaning Workspace

A central architectural proposal is an intermediate Shared Meaning Workspace, Wₜ, situated between the conversation and the formal clinical record. This workspace is deliberately permitted to contain ambiguity, competing interpretations, patient language, unresolved references and provisional hypotheses.

Wₜ = {Gₜ, Hₜ, Uₜ, Xₜ, Rₜ, Oₜ, Aₜ, Cₜ}

Component

Meaning

Gₜ

Grounded propositions

Hₜ

Semantic, pragmatic and clinical hypotheses

Uₜ

Uncertainties and unresolved meanings

Xₜ

Contradictions

Rₜ

Repair requirements

Oₜ

Prospective conversational obligations

Aₜ

Patient agenda items

Cₜ

Causal hypotheses

This separation prevents a dangerous architectural shortcut in which an LLM interprets conversational language and writes its inference directly into a structured record. The safer path is:

Conversation → Shared Meaning Workspace → Grounded Clinical Model → FHIR

The conversational representation can remain uncertain and revisable. The clinical representation must be stricter.

## 4. Propositions, provenance and the epistemic ladder

The basic unit of the workspace is a proposition rather than a field. A proposition carries its source, certainty, epistemic status and provenance.

pᵢ = (content, source, confidence, epistemic state, time, provenance)

For example, 'takes a blood thinner' reported by the patient may be highly grounded, while 'possibly apixaban' inferred from context remains a hypothesis. These should never be treated as equivalent.

## 4.1 Epistemic ladder

Level

State

Interpretation

L0

Raw utterance

What was actually said

L1

Literal semantic proposition

Direct linguistic meaning

L2

Pragmatic interpretation

What may be implied by why or how it was said

L3

Clinical hypothesis

A clinically meaningful interpretation proposed by the system

L4

Patient-grounded proposition

Interpretation exposed to and sufficiently confirmed by the patient

L5

Externally verified proposition

Confirmed against an external source where appropriate

L6

Clinically adjudicated conclusion

A clinician-level conclusion supported by the available evidence

Transitions between levels require evidence. In particular, pragmatic inference or model-generated clinical interpretation must not silently become a patient fact.

L₂ ↛ L₄ without grounding

The distinction between 'not mentioned', 'denied', 'unknown' and 'not asked' must also be preserved. Absence of evidence in conversation is not evidence of absence.

## 5. Bayesian inference and information theory

A listener continually infers intended meaning from utterance and context. A simple representation is:

P(M | U, C) = P(U | M, C) P(M | C) / P(U | C)

Question selection can initially be understood through information theory. If X denotes uncertainty over clinically relevant states, entropy is:

H(X) = -Σₓ P(x) log P(x)

The expected information gain from a question Q is:

IG(Q) = H(X) - E[H(X | Q)]

This explains why open questions can be highly valuable early in a history: they permit information outside the interviewer's current hypothesis set to emerge. As uncertainty narrows, focused and closed questions may become more discriminating.

However, maximising immediate information gain alone would create a poor interviewer. Questions have costs, and some apparently low-information behaviours create future value.

## 6. Active listening as a future-value intervention

Active listening changes the data-generating process. A reflection, acknowledgement or brief silence may yield little immediate clinical information but increase later disclosure, correction or trust.

V(aₜ) = IG_immediate + γ E[IG_future] + other future value

This makes active listening naturally compatible with sequential decision theory. Its value lies partly in the state it creates for subsequent interaction.

## 6.1 Functional forms of active listening

Action

Primary mathematical function

Reflection

Expose an interpretation for confirmation, correction, qualification or rejection

Paraphrase

Compress prior information and perform an error check

Minimal encourager

Preserve narrative trajectory without claiming the conversational floor

Silence

Create an opportunity for spontaneous continuation

Clarification

Reduce semantic entropy

Summary

Compression + verification + state synchronisation + topic closure

Signposting

Synchronise topic-state transition between agents

The implication is important: a good orchestration policy must be capable of deciding that the best next action is not another question.

## 7. Joint construction of meaning and grounding

Clinical meaning is often constructed during conversation rather than retrieved intact. A patient who initially reports 'dizziness' may, through clarification, jointly construct a more precise description of postural presyncope. Similarly, the significance of exercise limitation may only emerge when the patient compares current behaviour with prior activities.

Wₜ₊₁ = F(Wₜ, uᴾₜ, aᶜₜ)

The clinician's action affects the patient's next utterance. The measurement process is therefore interventional.

P(uᴾₜ₊₁) = P(uᴾₜ₊₁ | Zᴾₜ, Wₜ, aᶜₜ)

Grounding refers to the collaborative process through which participants establish sufficient evidence of mutual understanding. In clinical AI, reflection and summary are not merely stylistic niceties: they expose the system's evolving model to the patient and permit correction before an interpretation is committed.

## 8. Conversational repair as a safety mechanism

Misunderstanding is inevitable. Safety therefore depends less on eliminating all conversational error than on detecting and repairing error effectively. Conversation analysis has long treated repair as a fundamental organisation of talk, including recurrent problems of speaking, hearing and understanding.

Eₜ = d(Wₜ, Mᴾₜ)

Successful repair requires Eₜ₊₁ &lt; Eₜ

Repair class

Example system need

Recognition

Did the patient say atenolol or amlodipine?

Reference

Who does 'he' refer to?

Semantic

What does 'dizzy' mean here?

Temporal

Did the symptom precede or follow the medication change?

Factual

Correct a date, dose or event

Interpretive

Retract an over-inference

Contradiction

Reconcile incompatible propositions

Scope

Clarify whether a statement was global or domain-specific

Pragmatic

Repair misunderstanding of what the question was asking

Conversational

Restore the patient's narrative after interruption

Emotional

Reopen a topic after misattunement

AI self-repair

Acknowledge and correct the agent's own error

Record repair

Propagate correction into structured downstream representations

Repair should preserve history rather than simply overwrite prior assertions. A corrected proposition is retracted or superseded with provenance. Any downstream inference that depended on it must be reconsidered.

## 8.1 Dependency-aware truth maintenance

pᵢ → {pⱼ : pⱼ depends on pᵢ}

Δpᵢ → re-evaluate descendants(pᵢ)

This is particularly important in clinical systems because an early conversational error may otherwise persist invisibly in risk estimates, summaries or FHIR resources.

## 9. Continuous time, turn-taking and silence

Voice conversation is not naturally a sequence of perfectly alternating turns. It unfolds in continuous time τ. At each moment the agent chooses whether to listen, wait, backchannel, speak, interrupt or repair.

a(τ) ∈ {listen, wait, backchannel, speak, interrupt, repair, ...}

The patient has a latent turn state:

Zᵗᵘʳⁿ_τ ∈ {continuing, thinking, yielding, finished}

The system estimates this state from silence duration, prosody, syntax, breathing, semantic completeness and context. Importantly:

P(turn complete) ≠ P(agent should speak)

A pause after a medication dose and a pause after an emotionally significant disclosure should not be treated identically.

## 9.1 Speaking as an optimal stopping problem

Speak when E[V_speak - C_interrupt] &gt; E[V_wait - C_wait]

Silence itself has expected information value:

IG_wait(Δt) = E[H(Sₜ) - H(Sₜ₊Δt) | WAIT]

Consequently, IG(silence) can exceed IG(question). This formalises the experienced clinician's intuition that the best next move is sometimes to remain quiet.

## 9.2 Narrative momentum and interruption

Nₜ = f(continuity, novelty, emotional salience, spontaneous disclosure, coherence)

As narrative momentum increases, the threshold for interruption should generally rise. Clinical risk can override this. A new report of current chest tightness may justify immediate interruption even during a high-value narrative.

Risk ≫ NarrativeMomentum → interruption may be optimal

## 10. Pragmatics and relevance

Literal semantics cannot explain many clinically important responses. If asked about alcohol, 'not during the week' answers one part of the proposition while leaving weekend use unresolved. It does not justify inferring weekend drinking. Pragmatic reasoning should generate hypotheses and unresolved obligations, not facts.

Rational pragmatic models treat listeners as reasoning about why a speaker selected a particular utterance. A generic form is:

P(M | U) ∝ P(U | M) P(M)

P(U | M) ∝ exp(α · Utility(U, M))

In clinical settings, speaker utility may include informativeness, effort, embarrassment, distress, face-saving and the patient's immediate goal. The same literal question can therefore generate different response distributions depending on social cost and perceived consequences.

## 10.1 Relevance, topic shifts and patient agenda

An apparently off-topic statement may be evidence of a latent patient agenda rather than noise. The system should maintain the patient's agenda separately from the clinical assessment agenda.

Aᴾₜ = patient agenda;  Aᶜₜ = clinical agenda

A good consultation reconciles these agendas rather than allowing the clinical checklist to dominate completely. Repetition by the patient may also carry pragmatic salience even when it adds no new clinical fact.

## 11. Cooperative game theory and mechanism design

Patient and clinician cooperate but have different knowledge, goals and costs. The clinician may value completeness and risk detection while the patient values dignity, reassurance, privacy, control and avoiding unnecessary distress.

Uᴾ = Understanding + Agency + Dignity + Reassurance - Burden - Distress - PrivacyCost

Uᶜ = Safety + Accuracy + Completeness + DecisionValue + Efficiency

The goal is not to maximise one utility at the expense of the other, but to seek Pareto-efficient conversational trajectories subject to hard clinical and ethical constraints.

max Φ(Uᴾ, Uᶜ) subject to Safety ≥ Smin, Validity ≥ Vmin, Agency ≥ Amin

Mechanism design becomes relevant because question framing changes the incentives around disclosure. Explaining why a sensitive question matters, normalising common behaviours and clarifying that disclosure does not automatically cause cancellation can lower the perceived cost of truthful reporting.

## 12. Memory, attention and prospective obligations

Having the complete transcript is not equivalent to remembering well. Natural conversation requires selective attention and the ability to defer a question without forgetting it.

Mₜ = {Mworking, Mepisodic, Msemantic, Mprospective}

Working memory should be deliberately limited to the currently relevant subset, while other information remains retrievable.

|Mworkingₜ| ≤ K

## 12.1 Attention scoring

Aᵢ(t) = f(Risk, Uncertainty, ClinicalValue, PatientSalience, Emotion, Novelty, GoalRelevance, Deadline, Trigger, TopicDistance, Recency)

Some attentional priorities decay over time:

Aᵢ(t) = Aᵢ(t₀) e^[-λᵢ(t-t₀)]

Safety-critical unresolved items may have λ close to zero until resolved.

## 12.2 Prospective memory

Oᵢ = (content, priority, trigger, deadline, risk, status)

This allows the system to record 'identify anticoagulant before completion' or 'return to fear of anaesthesia after current narrative' as explicit future obligations. The optimal time to address an obligation can be defined as the lowest-cost conversational opportunity before its deadline.

t*ᵢ = argminₜ C_interrupt(Oᵢ,t), subject to tᵢ &lt; Deadlineᵢ

## 13. Psychological safety as a clinical state variable

Trust alone is insufficient. A patient may trust the competence of a clinician yet still feel unable to disagree, admit uncertainty, disclose stigmatised behaviour, decline a question or correct an error. We therefore define psychological safety as the perceived ability to take interpersonal risk without unacceptable social cost.

PSₜ = P(patient feels able to take interpersonal risk without unacceptable social cost)

Relevant interpersonal risks include correcting the agent, admitting non-adherence, disclosing sensitive information, saying 'I don't know', expressing fear, asking a basic question, declining to answer and changing an earlier account.

## 13.1 Epistemic vulnerability and humility

Appropriate vulnerability redistributes the social cost of correction. 'I may have misunderstood you' places some responsibility for potential error on the system and can make correction easier. Desirable forms include epistemic uncertainty, acknowledgement of interruption, acknowledgement of knowledge limits and explicit ownership of error.

Fabricated human self-disclosure is different and should not be used. The agent should express genuine epistemic humility rather than pretend to possess human experiences.

P(Correction) = σ(β₀ + β₁PS - β₂FaceCost - β₃AuthorityGradient)

## 13.2 Normalisation, permission and reinforcement of correction

Normalisation can lower the social cost of accurate disclosure. Permission to decline can increase perceived control. After sensitive disclosure, a non-judgemental acknowledgement can reinforce honesty. When corrected, the agent should positively reinforce the repair: 'Thanks for correcting me. I had that wrong.'

PSₜ₊₁ = f(PSₜ, Humility, Validation, Normalisation, Agency, RepairResponse, Judgement, Pressure, Interruption)

## 14. Humour and rapport

Appropriate humour, particularly gentle self-deprecating or situational humour, may reduce status distance, tension and the interpersonal cost of correction. Its proposed value is not entertainment but affiliation and psychological safety.

Humour → reduced status distance → lower correction cost → more repair → better shared model

Humour is highly context dependent. Its utility can be represented as:

U(Hₜ) = Rapport + Affiliation + TensionReduction + StatusReduction - Misinterpretation - Inappropriateness - Distraction

The target of humour matters. Patient-directed humour about mistakes, health literacy, behaviour or disclosure should be strongly constrained. Self-directed humour and benign situational humour have a safer theoretical profile, but excessive self-deprecation may reduce perceived competence.

H* = argmax_H [PsychologicalSafety + Rapport - CompetenceLoss - InappropriatenessRisk]

Humour should therefore be sparse, context-sensitive and empirically evaluated rather than hard-coded as a personality feature.

## 15. The real-time orchestration policy

The agent's action space is broader than question selection.

aₜ ∈ {listen, wait, backchannel, acknowledge, normalise, validate, reflect, clarify, repair, explore, ask, summarise, signpost, invite correction, use affiliative humour, interrupt, escalate}

The agent must choose both action and timing:

(a*, τ*) = argmaxₐ,τ Q(Sτ, a, τ)

A conceptual reward function can include information, grounding, safety, completeness, trust, agency, patient-priority fulfilment and verification, while penalising burden, distortion, unnecessary interruption and unsafe delay.

R = wI·I + wG·G + wS·S + wC·C + wT·T + wA·A + wP·P + wV·V - wB·B - wD·D - wX·X - wL·L

The policy maximises expected future cumulative value rather than immediate yield:

π* = argmax_π Eπ[Σₜ γᵗ R(Sₜ,aₜ)]

Some principles should be implemented as hard constraints rather than tradable reward terms, including minimum safety, clinical validity, patient agency, non-manipulation and maximum permissible distortion.

## 16. Personal adaptation without stereotyping

There is unlikely to be a universally optimal conversational style. The system should learn how this patient responds during this interaction, using uncertain interaction parameters rather than demographic assumptions.

θᴾ = {open-question responsiveness, preferred specificity, processing latency, verbosity, correction pattern, signposting need, uncertainty expression, humour receptivity}

P(response | a, S, θᴾ)

These parameters should remain probabilistic and update as the interaction unfolds. Explicit preference should override covert inference where feasible. For example, the agent may ask whether the patient prefers specific questions or space to describe events in their own words.

## 17. Causal reasoning within the clinical history

Patients frequently report causal claims: 'the dizziness started after my blood pressure tablets changed'. The system should represent chronology, association and causation separately.

A causal hypothesis can be represented as:

Hᶜᵢ = (cause, effect, support, alternatives, confidence, status)

Questions can then be selected according to expected causal discrimination:

ECD(Q) = H(Hypotheses) - E[H(Hypotheses | Answer_Q)]

Temporal sequence, dose-response, dechallenge, rechallenge and alternative explanations can be explored without promoting a plausible story into a causal fact.

Temporal association ≠ causal assertion

## 18. Learning what conversation works

The initial policy should be evidence-informed and governed, but it should not be assumed optimal. The system should learn which safe conversational actions produce better responses, when and for whom.

The unit of learning should be conversational strategy rather than surface wording alone. A functional-capacity construct, for example, may be approached through direct, behavioural, contextual, narrative or anchored questions.

aᵢ = (intent, strategy, wording, timing)

The outcome must be multidimensional. Optimising 'question answered', completion time, satisfaction or disclosure alone would predictably create undesirable behaviours.

R⃗ = [information, grounding, accuracy, completeness, safety, patient experience, burden, distortion]

## 18.1 Fast and slow learning

Two learning loops should be separated. Fast adaptation occurs within the current conversation, updating the interaction model θᴾ. Slow learning occurs across governed datasets and improves the population-level policy.

θᴾₜ₊₁ = Update(θᴾₜ, responseₜ)

Θₙ₊₁ = Update(Θₙ, governed outcomes)

## 18.2 Contextual bandits and constrained reinforcement learning

At a safe decision point, several clinically acceptable actions may be available. A contextual bandit formulation estimates expected reward conditional on context and action.

a* = argmaxₐ E[R | a, xₜ]

Longer-horizon effects require reinforcement-learning concepts:

Q(Sₜ,aₜ) = E[Σₖ γᵏ Rₜ₊ₖ]

However, unrestricted exploration on patients is inappropriate. Learning must be constrained by safety, fairness, non-manipulation, agency and clinical validity. Exploration should primarily occur in simulation, retrospective analysis, consented studies, micro-randomised trials or other governed research settings.

## 19. Causal inference for conversational learning

Observational association between a conversational behaviour and a good response does not establish causation. Reflection may be more common when patients are already communicative, creating confounding. The estimand of interest is therefore interventional:

P(Y | do(A)) rather than P(Y | A)

For each conversational moment there are unobserved counterfactual outcomes under actions not taken. Sequential conversation further creates time-varying confounding because earlier actions change later states and action selection.

Sₜ → Aₜ → Sₜ₊₁ → Aₜ₊₁ → Y

The decision log should therefore retain the context, available actions, chosen action, action propensity and subsequent outcomes.

Dₜ = (Sₜ, Aavailableₜ, Achosenₜ, P(Aₜ|Sₜ), Outcomeₜ:ₜ₊ₖ)

## 19.1 Experimental and quasi-experimental evaluation

Where two strategies are already considered safe and acceptable, randomisation provides the cleanest causal evidence. Micro-randomised trials can randomise suitable conversational decision points and evaluate proximal outcomes such as elaboration, repair, information gain or burden.

Treatment-effect heterogeneity should be examined using conditional effects:

CATE(x) = E[Y(1)-Y(0) | X=x]

This allows the system to discover that a strategy is helpful for one interaction pattern and neutral or harmful for another, without assuming a universal optimum.

## 20. Three-plane architecture

The proposed system separates real-time conversation, clinical compilation and long-term learning.

Plane

Purpose

Core flow

Conversation

Conduct the encounter

Listen → interpret → attend → act → observe

Clinical

Create an epistemically controlled clinical representation

Meaning → grounding → verification → clinical model → FHIR

Learning

Improve policy under governance

Interaction → measurement → causal inference → evaluation → approved policy update

The planes interact but should remain architecturally separable. In particular, the learning system should not directly rewrite the deployed clinical policy.

## 21. Governed policy improvement

πₙ → conversations → governed dataset → offline causal analysis → candidate π'ₙ₊₁ → simulation → retrospective validation → safety/fairness evaluation → prospective evaluation → governance approval → πₙ₊₁

This creates a learning health system for clinical conversation without uncontrolled online self-modification.

## 22. Candidate metrics

A useful evaluation framework should measure not only completion and accuracy but the quality of the conversational process.

| Domain | Candidate measures |
| --- | --- |
| Epistemic quality | Grounded proposition accuracy; unresolved ambiguity; unsupported inference rate; external verification concordance |
| Repair | Repair detection rate; successful repair rate; time-to-repair; recurrence; downstream correction propagation |
| Information | Information gain; clinically relevant yield per unit burden; unexpected agenda discovery |
| Conversation | Interruption rate; overlap recovery; narrative preservation; repetition; topic transition cost |
| Patient agency | Correction frequency; refusal/decline usability; agenda capture; preference adherence |
| Psychological safety | Willingness to correct; uncertainty admission; sensitive disclosure after normalisation; explicit safety ratings |
| Humour/rapport | Appropriateness ratings; effect on correction/disclosure; competence preservation; adverse humour events |
| Clinical safety | Missed high-risk information; unsafe delay; escalation appropriateness; record consistency |
| Learning | ATE/CATE of conversational strategies; policy calibration; fairness across interaction profiles |



## 23. Testable hypotheses

Open-to-focused questioning outperforms early closed-question sequences for discovery of unanticipated clinically relevant information, but the advantage diminishes as hypothesis entropy falls.

Reflective listening increases later clinically relevant disclosure through mediation by psychological safety and grounding.

Patient correction rates initially rise when the agent explicitly invites correction, while downstream unrepaired misunderstanding falls.

Summarisation reduces later contradiction and duplicate questioning when used at natural topic boundaries.

Deferring low-risk clarification to a semantically adjacent topic reduces interruption cost without increasing unresolved error.

Appropriate silence increases spontaneous elaboration in high narrative-momentum states but produces delay cost in low-momentum transactional states.

Self-deprecating or benign situational humour can reduce perceived status distance and correction cost in selected low-risk contexts, but excessive use reduces perceived competence.

Normalisation before sensitive questions increases accurate disclosure without increasing perceived coercion.

Explicit explanation of why a question is being asked reduces anxiety and improves disclosure when the reason is not obvious to the patient.

Interaction-adaptive questioning based on observed response patterns outperforms fixed conversational style while producing less bias than demographic-based personalisation.

Dependency-aware repair reduces propagation of early conversational errors into structured clinical outputs.

Conversational policies optimised for multidimensional utility outperform policies optimised for completion, speed or information gain alone.

## 24. Design requirements for clinical conversational AI

Maintain a Shared Meaning Workspace separate from the structured clinical record.

Represent source, provenance, certainty and epistemic status for every clinically relevant proposition.

Prevent pragmatic or model-generated inference from silently becoming patient-grounded fact.

Support explicit correction, retraction, qualification and downstream truth maintenance.

Maintain unresolved threads and prospective obligations with triggers, deadlines and risk weighting.

Model turn-taking, silence and interruption in continuous time for voice systems.

Treat active listening, normalisation, humility, validation and correction-invitation as functional conversational actions.

Represent psychological safety as a dynamic state relevant to disclosure and repair.

Constrain humour to context-sensitive, low-risk affiliative use with particular caution around patient-directed humour.

Adapt to observed interaction behaviour and explicit patient preference rather than demographic stereotype.

Separate clinical causal hypotheses from causal assertions.

Log policy state and action propensity sufficiently for later causal evaluation.

Prohibit autonomous online policy rewriting in clinical deployment.

Use governed offline learning, prospective evaluation and version-controlled policy release.

Compile only appropriately grounded information into FHIR or other structured clinical outputs.

## 25. Relationship to FHIR and structured clinical data

FHIR should represent the structured clinical state that has been sufficiently established, not dictate the order or surface form of the conversation. A conversational agent that traverses a FHIR-shaped questionnaire risks forcing the patient into the ontology of the record too early.

Natural dialogue → shared meaning → grounded clinical concepts → FHIR

The mapping layer should preserve provenance and uncertainty where the relevant FHIR resources permit it, and retain the richer conversational provenance outside FHIR when the standard cannot express the full epistemic history. Structured interoperability and natural conversation therefore belong to different layers of the architecture.

## 26. Research programme

The framework suggests a staged research programme.

Construct an annotated Clinical Conversation Dataset containing utterances, semantic propositions, pragmatic hypotheses, grounding events, repairs, agenda signals, psychological-safety actions, timing and clinical outcomes.

Develop expert annotation guidance for epistemic state, conversational action, repair class, topic state and causal hypothesis.

Validate automated state extraction against clinician and communication-science annotation.

Evaluate candidate policies in simulation and retrospective replay before patient-facing experimentation.

Run observational studies to characterise naturally occurring conversation trajectories and identify candidate interventions.

Use controlled and micro-randomised studies for safe, clinically equivalent conversational choices.

Measure heterogeneous effects and mediation, particularly through psychological safety, grounding and burden.

Assess fairness, accessibility, cultural safety, health-literacy effects and performance across different communication needs.

Evaluate structured output accuracy separately from conversational quality.

Establish governance for dataset use, policy versioning, safety monitoring and post-deployment learning.

## 27. Discussion

The proposed framework reframes history taking from a sequence of questions into a process of uncertainty reduction between interacting agents. It explains why behaviours often taught as 'soft skills' have direct epistemic and safety functions. Reflection exposes interpretations for correction. Summaries perform compression and error checking. Silence can have positive expected information value. Signposting synchronises topic state. Humility lowers correction cost. Psychological safety changes the probability of disclosure. Appropriate humour may alter status distance and rapport. Repair prevents conversational errors from becoming record errors.

The framework also clarifies why a conversational AI should not be designed as a fluent front end to a questionnaire. Fluency alone does not provide epistemic discipline. A model can sound natural while leading the patient, over-interpreting implication, failing to preserve uncertainty or converting an inferred meaning into a structured fact. The Shared Meaning Workspace and epistemic ladder are intended to make these transitions explicit and auditable.

The mathematical formulation is intentionally pluralistic. No single field provides an adequate theory of history taking. Bayesian inference describes belief updating; information theory describes uncertainty reduction; POMDPs and stochastic control describe sequential action under partial observability; conversation analysis explains repair and turn organisation; pragmatics explains meaning beyond literal semantics; game theory and mechanism design describe interacting goals and disclosure incentives; attention models describe selective conversational focus; causal inference distinguishes association from intervention; and reinforcement learning provides a language for long-horizon policy improvement.

The framework is presently conceptual. Many state variables, reward terms and equations are abstractions rather than validated measurement models. Their value is to make assumptions explicit and generate testable hypotheses. The research task is not to prove that every element should be computed literally, but to determine which representations improve clinical safety, conversational quality and structured data accuracy.

## 28. Conclusion

Clinical history taking can be understood as a cooperative process in which two agents progressively construct a shared model that is accurate enough, grounded enough and complete enough to support safe action. The conversation is inherently uncertain, interactive and revisable. Its quality depends not only on what questions are asked, but on timing, silence, attention, explanation, repair, patient agency, psychological safety and the willingness of the interviewer to expose its own uncertainty.

A good clinical conversation moves patient and clinician towards a sufficiently accurate, mutually grounded and clinically useful shared state at the lowest reasonable human cost.

For clinical conversational AI, this suggests a system that listens and learns without treating the patient as a questionnaire, reasons without confusing inference for fact, invites correction rather than merely tolerating it, builds psychological safety without fabricating humanity and improves through governed causal learning rather than uncontrolled self-modification. Such a system would not merely automate history taking. It could provide a formal experimental platform for understanding the science of clinical conversation itself.

## References

Clark HH, Brennan SE. Grounding in communication. In: Resnick LB, Levine JM, Teasley SD, eds. Perspectives on Socially Shared Cognition. American Psychological Association; 1991:127-149.

Edmondson A. Psychological safety and learning behavior in work teams. Administrative Science Quarterly. 1999;44(2):350-383. doi:10.2307/2666999.

Frank MC, Goodman ND. Predicting pragmatic reasoning in language games. Science. 2012;336(6084):998. doi:10.1126/science.1218633.

Grice HP. Logic and conversation. In: Cole P, Morgan JL, eds. Syntax and Semantics, Volume 3: Speech Acts. Academic Press; 1975:41-58.

Kaelbling LP, Littman ML, Cassandra AR. Planning and acting in partially observable stochastic domains. Artificial Intelligence. 1998;101(1-2):99-134.

Nahum-Shani I, Smith SN, Spring BJ, et al. Just-in-time adaptive interventions in mobile health: key components and design principles for ongoing health behavior support. Annals of Behavioral Medicine. 2018;52(6):446-462. doi:10.1007/s12160-016-9830-8.

Pearl J. Causality: Models, Reasoning, and Inference. 2nd ed. Cambridge University Press; 2009.

Robins JM, Hernán MA, Brumback B. Marginal structural models and causal inference in epidemiology. Epidemiology. 2000;11(5):550-560.

Sacks H, Schegloff EA, Jefferson G. A simplest systematics for the organization of turn-taking for conversation. Language. 1974;50(4):696-735.

Schegloff EA, Jefferson G, Sacks H. The preference for self-correction in the organization of repair in conversation. Language. 1977;53(2):361-382. doi:10.2307/413107.

Sutton RS, Barto AG. Reinforcement Learning: An Introduction. 2nd ed. MIT Press; 2018.

## Appendix A. Compact formal specification

State:

Sₜ = (Wₜ, bₜ, Mₜ, PSₜ, Nₜ, Fₜ, θᴾₜ, Riskₜ)

Observation:

Oₜ = (words, timing, prosody, pauses, overlap, correction, topic movement, explicit feedback)

Action:

aₜ ∈ {listen, wait, backchannel, acknowledge, normalise, validate, reflect, clarify, repair, explore, ask, summarise, signpost, invite correction, humour, interrupt, escalate}

Workspace update:

Wₜ₊₁ = F(Wₜ, Oₜ₊₁, aₜ)

Attention:

Mworkingₜ = TopK(score(Wₜ, Riskₜ, PSₜ, goals, deadlines, topic state))

Policy:

(a*,τ*) = argmaxₐ,τ E[Σ γᵏRₜ₊ₖ] subject to safety, validity, agency, non-manipulation and distortion constraints

Clinical compilation:

Grounded(Wₜ) → ClinicalModelₜ → FHIR

Learning:

Decision logs → causal estimation → candidate policy → validation → governance → versioned deployment

## Appendix B. Proposed annotation schema for a future dataset

Layer

Example labels

Utterance

speaker, timestamp, overlap, pause, prosody markers

Speech act

question, reflection, acknowledgement, summary, repair, signpost, normalisation, humour

Semantic

literal propositions, entities, temporal relations

Pragmatic

implicature hypothesis, unanswered component, salience, agenda signal

Epistemic

source, confidence, grounded status, verification status

Clinical

domain, risk relevance, hypothesis, causal relation

Repair

trigger, initiator, class, success, downstream propagation

Attention

active topic, unresolved obligations, priority, trigger

Psychological safety

invitation to correct, humility, validation, permission, normalisation, judgement signal

Outcome

information gain, burden, repair, patient-rated experience, structured-record concordance

## Appendix C. Important cautions

Psychological safety, trust, emotion and narrative momentum are latent constructs and should not be treated as directly observed facts.

Conversational adaptation must not become covert personality diagnosis or demographic stereotyping.

Humour is culturally and contextually sensitive and requires conservative deployment and explicit evaluation.

Patient disclosure is not an unqualified optimisation target; pressure or manipulation can increase disclosure while reducing autonomy.

Low repair rates are not automatically desirable. A healthy system should expose interpretations and make correction easy.

FHIR is an interoperability representation, not a theory of conversation.

Model confidence is not equivalent to clinical probability unless separately calibrated.

Causal language generated by an LLM should remain hypothesis-level unless appropriately supported and adjudicated.

Any patient-facing learning system requires explicit governance, safety monitoring, privacy protection and research ethics.
