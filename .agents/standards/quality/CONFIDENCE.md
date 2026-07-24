# Confidence Standard

## Purpose

Define a single, falsable confidence model for every conclusion the protocol records in an artifact (verification results, recovery diagnoses, KB recommendations, intent interpretations). Its goal is that two artifacts with the same label always mean the same thing, and that a conclusion never claims more certainty than its evidence supports.

## Levels

| Level | Definition | Requirement |
|---|---|---|
| `HIGH` | Every claim traces to concrete evidence: a file read, a command executed, a test that passed. | Evidence MUST be cited in the artifact (path, command output, or test result). |
| `MEDIUM` | Partial evidence, or a reasoned inference built on top of concrete evidence. | The inference step MUST be made explicit in the explanation. |
| `LOW` | Unverified assumption, or evidence that could not be obtained. | The missing evidence MUST be named in the explanation. |

## The anti-inflation rule

Confidence is derived from the evidence available, never from the convenience of the moment (a deadline, a desire to close the phase, pressure to avoid `RECOVERY` or `NEEDS_CLARIFICATION`).

Declaring a level higher than the evidence supports is a conduct violation: it MUST be recorded as a deviation in `SESSION_LOG.md`, under the same policy as `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`. When in doubt between two levels, the lower one MUST be used.

## Operational consequences

- A verification criterion marked `PASS` with `LOW` confidence does not close verification; the `verifier` MUST either gather the missing evidence or recommend `RECOVERY`.
- A recovery analysis whose root cause has `LOW` confidence SHOULD prefer the least invasive corrective action (`RETRY_WORKER` or `NEEDS_CLARIFICATION`) over structural changes.
- A KB recommendation with `LOW` relevance confidence MUST say so explicitly in `## Notes`, so the consuming worker can discount it.

## Relationship to other standards

- `.agents/standards/requirements/INTENT_CONFIDENCE.md` is a specialization of this model for intent interpretation: its numeric score decides the next state (`CONFIRMING_INTENT` or not), and the resulting `HIGH`/`MEDIUM`/`LOW` label uses the levels defined here.
- Reviewers applying `.agents/standards/quality/RUBRICS.md` SHOULD treat an inflated or unjustified confidence level as a quality defect of the artifact.
