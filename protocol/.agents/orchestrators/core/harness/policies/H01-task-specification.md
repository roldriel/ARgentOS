+++
trigger = "H01"
transition = "BUILDING_TASK_SPECIFICATION → TASK_READY"
artifact = "TASK_SPECIFICATION.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H01
name: task-specification
state: core:BUILDING_TASK_SPECIFICATION
lifecycle: task
gates:
  - "core:BUILDING_TASK_SPECIFICATION -> core:TASK_READY"
artifact_validated: TASK_SPECIFICATION.md
---

# Harness Policy H01: Task Specification

## Trigger

`BUILDING_TASK_SPECIFICATION → TASK_READY`

## Purpose

Validate that `TASK_SPECIFICATION.md` exists and complies with its contract before allowing the task to enter the context-gathering phase.

## Input

- Current state: `BUILDING_TASK_SPECIFICATION`
- Target state: `TASK_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md`
- Contract: `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` have objectively verifiable structure and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The artifact contains an `Objective` section. `[gate]`
3. The artifact contains an `Expected outcome` section. `[gate]`
4. The artifact contains a `Scope` section. `[gate]`
5. The artifact contains a `Constraints` section. `[gate]`
6. The artifact contains `Acceptance Criteria`. `[gate]`
7. The artifact contains `Assumptions`. `[gate]`
8. The artifact contains `Unknowns`. `[gate]`
9. The artifact contains a `Validation` section. `[gate]`
10. The acceptance criteria are specific and verifiable. `[agent]`
11. Each acceptance criterion follows one of the EARS patterns defined in `.agents/standards/requirements/EARS.md`. `[gate]`
12. No acceptance criterion is compound: it must describe a single action or condition. A criterion is compound when "and" or "or" separate independent actions or conditions (for example, "create X and send Y", "validate A or B"). A criterion is not compound when "and" or "or" enumerate values within the same domain (for example, "return HTTP 200 or 201", "accept JSON and XML"). `[agent]`
13. The scope is bounded and does not introduce unplanned work. `[agent]`
14. Every practice listed in `technical_approach.enabled` corresponds to an enabled technical-practice feature flag (for example, `tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`). `[gate]`
15. If `technical_approach.enabled` is non-empty, `technical_approach.notes` explains why each listed practice applies to this task. `[gate]` (notes present and non-empty) / `[agent]` (the explanation actually justifies each practice).
16. No acceptance criterion is derived from an unconfirmed assumption. `[agent]`
17. Every entry under `Assumptions` is an object with `assumption` text and an accessible `user_confirmed` field, or resolved through a prior clarification exchange. `[agent]`

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, section name, declared value, or offending bullet) in `HARNESS_REPORT.md`.

1. Verify that `TASK_SPECIFICATION.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that the artifact contains each of the following sections (heading comparison is case-insensitive): `Objective`, `Expected Outcome`, `Scope`, `Constraints`, `Acceptance Criteria`, `Assumptions`, `Unknowns`, `Validation`. Cite any missing section as failure evidence.
3. Verify that `## Acceptance Criteria` contains at least one bullet (`-` or `*`) and that each bullet matches one of the EARS patterns defined in `.agents/standards/requirements/EARS.md`: ubiquitous (`The <system> shall <response>`), event-driven (`When <trigger>, the <system> shall <response>`), state-driven (`While <state>, the <system> shall <response>`), unwanted-behavior (`If <undesired condition>, then the <system> shall <response>`), optional-feature (`Where <feature is included>, the <system> shall <response>`). Cite each non-conforming bullet. Criteria present only in the `acceptance_criteria` TOML block constitute a form violation; cite the section as evidence.
4. Verify that no acceptance criterion is compound: each criterion describes a single action or condition. A criterion is compound when "and"/"or" separate independent actions or conditions ("create X and send Y"); it is not compound when they enumerate values within the same domain ("return HTTP 200 or 201", "accept JSON and XML"). Cite each compound criterion.
5. Verify the technical approach declaration. First resolve each technical-practice feature flag: the environment variable `AGENTS_FEATURE_<FLAG>` wins over `.agents/features.toml` (`[features]` table), which wins over the default (enabled). If no technical-practice flag is enabled, this item passes trivially — record the flag resolution as evidence. Otherwise, if a `## Technical Approach` section with a TOML block is present, verify that: `technical_approach.enabled` is a list; when the list is non-empty, `technical_approach.notes` is a list with at least one non-empty entry; and every practice in `enabled` is a known technical-practice flag (see `technical_practices` in the protocol standards) and is enabled at protocol level per the flag resolution above. An absent `## Technical Approach` section means no practices were selected and passes. Cite the flag resolution, the declared `enabled` list, and each violation.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or any criterion is not met.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Apply the §"Recovery Decision Table" (first matching rule, top to bottom). A `RETRY_WORKER` result re-invokes the `task_specification_writer` on `02-build-task-specification.md` without a state transition (bounded by `retry_count`); `NEEDS_CLARIFICATION` requests user input; `RECOVERY_GENERIC` routes to `08-recovery.md`.

## Recovery Decision Table

When H01 fails, the Orchestrator populates the context variables from the session (`artifact_exists`, `objective_is_ambiguous`, `scope_is_clear`, `retry_count` = retries already attempted for this failure) and applies the first rule that matches, top to bottom. `artifact_exists` means: `false` — the artifact is missing or must be regenerated; `true` — the artifact exists but fails validation (for example, a format failure).

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `artifact_exists == false` | `RETRY_WORKER` | `02-build-task-specification.md` | `task_specification_writer` | TASK_SPECIFICATION.md is missing or incomplete; retry writer. |
| 2 | `objective_is_ambiguous == true` or `scope_is_clear == false` | `NEEDS_CLARIFICATION` | — | — | Objective or scope is ambiguous; request clarification. |
| 3 | `artifact_exists == true` and `objective_is_ambiguous == false` and `scope_is_clear == true` and `retry_count == 0` | `RETRY_WORKER` | `02-build-task-specification.md` | `task_specification_writer` | TASK_SPECIFICATION.md exists but fails structural/format checks; retry writer once without a state transition. |
| 4 | `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Repeated failure after retry; route to generic recovery. |
| 5 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Task specification validation failed; falling back to generic recovery. |
