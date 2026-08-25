# No-Assumption Policy

## Purpose

This standard defines when an agent MUST ask the user for clarification instead of making an assumption. It applies to all workflow phases that interpret user intent, primarily the task analysis and task specification phases.

## Rule

The agent MUST NOT assume any of the following when they are not explicitly stated or directly inferable from the user's request:

- Technology choices beyond those specified.
- Behavioral details of endpoints, functions, or user interfaces.
- Scope expansions or exclusions.
- Design or architectural decisions.
- Validation, security, or error-handling behavior.
- Acceptance criteria.
- Facts, context, or decisions invented to avoid clarification or to keep the task "simple".

## When to ask for clarification

Whenever a missing detail would require the agent to choose between two or more reasonable implementations, the agent MUST transition to `NEEDS_CLARIFICATION`.

The agent must also confirm its interpretation of the user's intent when confidence is not high. See the `CONFIRMING_INTENT` state and the `INTENT_REFLECTION.md` artifact contract.

The agent MAY proceed without clarification only when:

- The missing detail has exactly one reasonable interpretation given the context.
- The detail is purely syntactic or formatting and does not affect behavior.
- The user has previously confirmed an equivalent decision in the same session.

The agent MUST NOT reduce rigor, omit required investigation, or invent details to make the task appear simpler than it is.

## Clarification request format

Every clarification request MUST present:

1. A concise description of the ambiguity.
2. The impact of the ambiguity on the implementation.
3. At least two concrete resolution options.
4. An explicit option allowing the user to provide a different answer.

Example:

> **Ambiguity:** The request says "edit a user" but does not specify the HTTP method.
> **Impact:** This determines the API contract and idempotency expectations.
> **Options:**
> 1. Use `PUT /users/<id>` for a full replacement of the user resource.
> 2. Use `PATCH /users/<id>` for partial updates.
> 3. Other (please specify).

## Recording user decisions

When the user provides a clarification:

- If it becomes a fixed rule, record it under `Constraints` in `TASK_SPECIFICATION.md`.
- If it becomes a verifiable behavior, record it as an acceptance criterion in `TASK_SPECIFICATION.md`.
- If it is a confirmed fact that the implementation depends on, record it as an `assumptions` entry in `TASK_SPECIFICATION.md` with `assumption: <text>` and `user_confirmed: true`.
- If it authorizes an out-of-frontier effect, register it in the `Effects`
  section of `TASK_SPECIFICATION.md` (`authorized_by`, `evidence_ref`,
  `status`) and record the confirmation in `SESSION_BRIEF.md`. An assumption
  with `user_confirmed: false` never authorizes an effect
  (`.agents/standards/runtime/AUTHORIZATION.md`).

## Unattended mode (opt-in)

When no user is available to answer clarifications (CI, batch runs, dogfooding), the protocol MUST NOT simulate the user. Unattended mode is an explicit, opt-in alternative:

1. **Declared defaults policy.** Before the session starts, the user (or the executing plan) declares a defaults policy: for each anticipated ambiguity class, a `recommended_default` and its applicability condition. Ambiguities not covered by the policy stop the session as usual.
2. **Applied and marked.** When a covered ambiguity occurs, the Orchestrator applies the default and records it in `SESSION_LOG.md` as `PENDING_USER_CONFIRMATION` and in `SESSION_BRIEF.md` with `source: unattended_default`.
   A default that authorizes an out-of-frontier effect is additionally recorded
   with `authorized_by: unattended_default` and `status:
   pending_user_confirmation`; only that status authorizes the effect until the
   user reviews it.
3. **Deferred confirmation.** Every decision taken by default stays marked until the user reviews the session. A correction triggers the normal re-analysis cycle; an unreviewed default is never treated as user-confirmed.

Unattended mode never lowers the bar of this standard: it replaces "ask and wait" with "apply declared default and mark", never with "assume silently".

## Relationship to other standards

This standard complements `.agents/standards/requirements/EARS.md`. Acceptance criteria derived from unresolved assumptions are not valid under this policy.
