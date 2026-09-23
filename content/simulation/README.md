# Simulated patient case pack

`cases.yaml` is a machine-readable transcription of the Build Specification's
"Simulated patient case pack" (tab 7, Simulated patient cases, 2026-09-23).
It holds the run protocol, pass-criteria convention, assessment sheet template,
coverage map, known gaps, and cases C-01 to C-19. Actor briefs are quoted
verbatim from the specification, not paraphrased. Each assessment criterion
carries the requirement id(s) it cites (F-n, S-n, N-n, dialogue pack section),
its severity (critical / major / minor) and the hazard under test.

## Who may see what

Each case has three parts: `actor_brief` (the simulated patient only),
`ground_truth` (assessors only) and `assessment` (assessors only).
**Actors must not see the ground truth or the assessment sheet.** An actor who
knows what the agent is being tested on will play the case differently, which
defeats the test. Anything shown to an actor must be derived from
`actor_brief` alone.

## Automated harness

The automated simulation harness under `backend/tests/simulation` drives the
agent with scripted answers derived from each case's `actor_brief`. Those
scripted answer sets are written separately from this file; `cases.yaml` is the
source of truth for the brief, the ground truth and the pass criteria they are
scored against. Failures are recorded against requirement ids, not as free
text.

## Blocked cases

C-19 (Disclosure during an unrelated history) is `status: blocked` and must not
be run until the mental health specialist has signed off wording, thresholds
and escalation pathway (S-16, Overview gates). Its actor brief, escalation
wording and assessor criteria are to be written by the mental health reviewer,
not adapted from this pack.
