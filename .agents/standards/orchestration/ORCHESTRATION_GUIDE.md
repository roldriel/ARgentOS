# Orchestration Guide

## 1. Purpose

Provide the Orchestrator with a practical manual for deciding **which worker profile** to delegate an execution task to and how to build the corresponding delegation payload.

This guide aims to:

- Reduce cognitive load and token consumption in the Orchestrator prompt.
- Ensure consistency with the state machine defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.
- Guarantee that the delegation payload complies with `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.

---

## 2. When to use this guide

### Mainly

At the `PLAN_READY → EXECUTING` transition, **before delegating** the `orchestrators/core/workflow/06-execute.md` phase.

### Also applies in optional transitions

- If the `knowledge_base` feature flag is active: delegate `context_discoverer` before the actual phase worker.
- If the `rubrics` feature flag is active: delegate `reviewer` before critical transitions.

### Does not apply to

- `CONFIRMING_INTENT`: the profile is fixed (`intent_reflector`).
- Purely analytical or planning phases (`00-analyze-task.md` to `05-plan.md`), except for optional invocations of `context_discoverer` or `reviewer`.

---

## 3. The 7 decision questions

The questions are **mutually exclusive in their main action**. If a single task triggers more than one, split it into sequential subtasks.

| # | Question | Profile summoned | Workflow phase | Profile `MUST_READ` files |
|---|---|---|---|---|
| 1 | Does the task modify database schemas, migrations, queries, or indexes? | `database_engineer` | `06-execute.md` | `.agents/roles/profiles/database_engineer.md` |
| 2 | Does the task integrate with or consume external systems/APIs? | `integration_engineer` | `06-execute.md` | `.agents/roles/profiles/integration_engineer.md` |
| 3 | Does the task define or execute tests, test cases, or quality verification? | `qa_engineer` | `06-execute.md` | `.agents/roles/profiles/qa_engineer.md` |
| 4 | Does the task produce technical documentation for developers or agents? | `tech_writer` | `06-execute.md` | `.agents/roles/profiles/tech_writer.md` |
| 5 | Does the task produce functional or business documentation? | `functional_writer` | `06-execute.md` | `.agents/roles/profiles/functional_writer.md` |
| 6 | Does the task implement business logic, endpoints, or services? | `backend_engineer` | `06-execute.md` | `.agents/roles/profiles/backend_engineer.md` |
| 7 | Does none of the above apply, or is the task generic (analysis, planning, recovery)? | Generic `worker` | Any | None outside the corresponding workflow |

**Tooling/CLI candidacy:** a tooling or developer-CLI task that does not touch the action domain of any existing profile produces an empty candidacy set — and that is a legitimate outcome, not a classification failure: Q7 applies and the generic `worker` executes it. Do not force a marginal profile (e.g. `backend_engineer` for a CLI with no business logic). If the tooling does touch a covered domain (e.g. it packages or runs tests), the corresponding profile applies instead.

### Alternative profiles that must not be used

| If the task is... | Do not use |
|---|---|
| Database | `backend_engineer`, `integration_engineer` |
| External integration | `backend_engineer`, `database_engineer` |
| QA / tests | Any implementation profile such as `backend_engineer` |
| Technical documentation | `functional_writer`, `backend_engineer` |
| Functional documentation | `tech_writer`, `backend_engineer` |
| Generic backend | `database_engineer`, `integration_engineer`, `qa_engineer` |

### Selection model (concepts)

The 7 questions above are the operational procedure; these are the concepts that frame it:

- **Profile candidacy:** a task is a *candidate* for a profile when its content falls within that profile's domain of action. Each of questions 1–6 *is* the candidacy criterion of one profile: an affirmative answer declares the candidacy. A task may be a candidate for zero, one, or several profiles.
- **Fallback:** the generic worker (`profile: null`) is not a candidate profile; it is the result of a selection with an empty candidate set. Question 7 competes with no other: it applies only when no specialized candidacy exists.
- **Mutual exclusion:** two profiles are mutually exclusive for a task when delegating the whole task to one of them violates the other's domain. The prohibited-profiles table above is a materialized instance of this concept for the domain pairs where the mistake is frequent — not an independent list.
- **Tie:** a tie occurs when a task is a candidate for two or more mutually exclusive profiles. A tie is not resolved by choosing; it is resolved by *dividing*.
- **Divisibility and subtask frontier:** a tied task is divisible when it can be split into subtasks such that each subtask is a candidate for exactly one profile and the subtasks cover the original task. A frontier between subtasks is valid when it satisfies: (1) *coverage* — nothing is left out; (2) *membership* — each subtask falls entirely within one profile's domain; (3) *dependency order* — a subtask that consumes another's result (e.g. documentation consuming `EXECUTION_SUMMARY.md`) is delegated after it. A tied task with no valid frontier is an ambiguity of scope, not a selection problem: transition to `NEEDS_CLARIFICATION`.

Selection produces the `profile` value of the delegation payload; skill activation then applies orthogonally on top of the selected profile (see `.agents/standards/orchestration/SKILLS.md`, §"Activation").

---

## 4. Pre-delegation checklist

Before invoking a worker, the Orchestrator must verify:

- [ ] I have the current state of the protocol according to `.project/<session-uuid>/SESSION_LOG.md`.
- [ ] I have `TASK_SPECIFICATION.md`, `CONTEXT_VALIDATION_REPORT.md` and `EXECUTION_PLAN.md` for the `06-execute.md` phase.
- [ ] I applied the 7 questions and identified whether the task requires a specialized profile.
- [ ] I selected the profile or the generic worker and recorded it in the payload.
- [ ] I determined the profile's mandatory readings according to `.agents/roles/profiles/<profile>.md`.
- [ ] I rewrote the objective using the profile's template, not the original user prompt.
- [ ] I included the acceptance criteria from `TASK_SPECIFICATION.md` in the payload.
- [ ] I verified that the payload follows the format of `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- [ ] I applied context compression according to `.agents/standards/context/CONTEXT.md` if the context exceeded the threshold defined there.
- [ ] I recorded the delegation decision in `.project/<session-uuid>/SESSION_LOG.md`.

---

## 5. Using the layer and profile catalog

This orchestration guide **does not define** architectural layers or technical profiles. It only indicates where to find them:

- Layer catalog: `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
- Profile catalog: `.agents/roles/profiles/README.md`.

### How to use them when deciding

A task that affects a specific layer may summon the corresponding profile:

- **Models** layer or migrations → `database_engineer`.
- **Providers** layer → `integration_engineer`.
- **Services** layer or **Views** → `backend_engineer`.

> **SRP:** `ORCHESTRATION_GUIDE.md` decides *when and to whom to delegate*; `ARCHITECTURE_CONTRACT.md` defines *what the layers are*; the profiles define *how each technical role acts*.

---

## 6. Golden rule: rewrite, do not forward

The Orchestrator **must not forward the raw user prompt**. It must rewrite it using:

1. Compressed context according to `.agents/standards/context/CONTEXT.md`.
2. The profile's prompt template (`## 9. Prompt template` section of `.agents/roles/profiles/<profile>.md`).
3. Acceptance criteria from `TASK_SPECIFICATION.md`.
4. Current state of the protocol.

If the generic worker is used, apply the minimum payload template from the delegation contract.

---

## 7. Mapping to workflow phases

| Workflow phase | Orchestration guide applies | Decision |
|---|---|---|
| `00-analyze-task.md` | No | Fixed profile according to `orchestrator.md`. |
| `01-confirm-intent.md` | No | Fixed profile `intent_reflector`. |
| `02-build-task-specification.md` | No | Fixed phase role `task_specification_writer` (see `worker.md` §Phase roles). |
| `03-gather-context.md` | No | Generic worker (or `context_discoverer` if `knowledge_base` is active). |
| `04-validate-context.md` | No | Generic worker. |
| `05-plan.md` | No | Generic worker. |
| `06-execute.md` | **Yes** | Choose profile using the 7 questions. |
| `07-verify.md` | Partially | If `rubrics` is active, invoke `reviewer`. |
| `08-recovery.md` | Partially | Generic worker; follow the recovery decision table of the failed trigger's policy. |

> **Note:** the 7-question guide applies only to `06-execute.md`. Phases 00–05 use fixed roles assigned by their workflow (phase roles, or fixed-phase profiles such as `intent_reflector` in 01); the Decision column for 00–05 is not resolved with the 7 questions.

---

## 8. Relevant feature flags

Only feature flags that exist in `.agents/features.toml` may be mentioned:

- `rubrics`: if active, invoke `reviewer` before critical transitions.
- `knowledge_base`: if active, attach relevant KB entries (via `context_discoverer`).
- `caveman`: if active, apply the compressed communication style in the payload according to `.agents/standards/communication/CAVEMAN.md`.

> **Note:** `context_engineering` **is not a feature flag**. Context compression is applied according to `.agents/standards/context/CONTEXT.md` when the context exceeds the defined threshold.

---

## 9. Delegation payload template

The payload must be a concrete instance of `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.

```json
{
  "session_uuid": "<uuid>",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "<profile or null>",
  "input_artifacts": [
    ".project/<uuid>/<iteration>/<order>-TASK_SPECIFICATION.md",
    ".project/<uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md",
    ".project/<uuid>/<iteration>/<order>-EXECUTION_PLAN.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "<objective rewritten using the profile prompt template>",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": [], "notes": []}
}
```

### How to fill each field

| Field | Source / Rule |
|---|---|
| `session_uuid` | UUID of the active session. |
| `current_state` | Current state of the state machine (`EXECUTING` for phase 06). |
| `target_phase` | Path of the workflow module to execute (`orchestrators/core/workflow/06-execute.md`). |
| `role_to_adopt` | Always `worker`; the profile is indicated in `profile`. |
| `profile` | Result of the 7 questions (`backend_engineer`, `database_engineer`, etc.) or `null` if generic worker. |
| `input_artifacts` | Artifacts required by the workflow module. |
| `harness_policy` | Harness policy that protects the transition (`orchestrators/core/harness/policies/H05-execution-completed.md`). |
| `task_summary` | Rewritten objective, never the original user prompt. |
| `knowledge_entries` | Populated by `context_discoverer` when `knowledge_base` is active. |
| `context_budget` | Recommended by `context_discoverer` in characters (per `KB_RECOMMENDATION.md`) and converted to estimated tokens per `.agents/standards/context/BUDGET_MATERIALIZATION.md` (`chars / 4`). Default `1000` for a full-KB delegation in planning/execution/verification (the 4000-character KB budget of `.agents/standards/context/CONTEXT.md` §3). |
| `communication_style` | Mandatory when `caveman` is active. |
| `technical_approach` | Populated when technical-practice feature flags are enabled and `TASK_SPECIFICATION.md` includes `## Technical Approach`. |

---

## 10. Examples

### Example 1 — Generic worker

**Original user prompt:** "Fix a typo in README.md".

**Application of the 7 questions:**

1. Database? No.
2. External integration? No.
3. QA / tests? No.
4. Technical documentation? No (it is a project file, not documentation for agents/developers).
5. Functional documentation? No.
6. Business logic / backend? No.
7. Generic? Yes.

**Profile chosen:** generic `worker` (`profile: null`).

**Payload:**

```json
{
  "session_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": null,
  "input_artifacts": [
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/01-TASK_SPECIFICATION.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/03-CONTEXT_VALIDATION_REPORT.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/04-EXECUTION_PLAN.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "Fix the typo identified in README.md per acceptance criterion AC-1 of TASK_SPECIFICATION.md. Do not modify any other files.",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": [], "notes": []}
}
```

**Justification:** The task is purely textual and does not require technical specialization. `tech_writer` was not chosen because it does not produce structured documentation for developers/agents.

---

### Example 2 — `backend_engineer`

**Original user prompt:** "Add a user listing endpoint".

**Application of the 7 questions:**

1. Database? Not directly (it does not modify schemas or migrations).
2. External integration? No.
3. QA / tests? No.
4. Technical documentation? No.
5. Functional documentation? No.
6. Business logic / backend? Yes.
7. Generic? No.

**Profile chosen:** `backend_engineer`.

**Payload:**

```json
{
  "session_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "backend_engineer",
  "input_artifacts": [
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/01-TASK_SPECIFICATION.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/03-CONTEXT_VALIDATION_REPORT.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/04-EXECUTION_PLAN.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "Implement the user listing endpoint respecting the View → Service → Model layering defined in ARCHITECTURE_CONTRACT.md. Acceptance criteria: AC-1 (pagination), AC-2 (name ordering), AC-3 (200 response).",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": ["tdd", "srp"], "notes": ["tdd: escribir test del endpoint antes de implementar.", "srp: mantener lógica de negocio en UserListService."]}
}
```

**Justification:** The task implements an endpoint and service logic. `database_engineer` was not chosen because the schema is not modified. `qa_engineer` was not chosen because the task is not defining tests, although the worker may write tests as part of the `tdd` practice.

---

### Example 3 — `database_engineer`

**Original user prompt:** "Add the `email_verified` field to the users table".

**Application of the 7 questions:**

1. Database? Yes.
2. External integration? No.
3. QA / tests? No.
4. Technical documentation? No.
5. Functional documentation? No.
6. Business logic / backend? No.
7. Generic? No.

**Profile chosen:** `database_engineer`.

**Payload:**

```json
{
  "session_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "database_engineer",
  "input_artifacts": [
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/01-TASK_SPECIFICATION.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/03-CONTEXT_VALIDATION_REPORT.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/04-EXECUTION_PLAN.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "Add the `email_verified` column (BOOLEAN, NOT NULL DEFAULT false) to the `users` table via a migration. Update the corresponding model without introducing business logic. Criteria: AC-1 (reversible migration), AC-2 (model in sync).",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": [], "notes": []}
}
```

**Justification:** The task directly modifies the schema and the persistence model. `backend_engineer` was not chosen because there are no endpoints or business logic to implement.

---

### Example 4 — Multiple sequential profiles

**Original user prompt:** "Integrate external payment API and document the flow".

**Application of the 7 questions:**

- First subtask: integration with external API → `integration_engineer`.
- Second subtask: functional documentation of the flow → `functional_writer`.

It cannot be solved with a single profile without violating the mutual-exclusion rule.

**Subtask A — `integration_engineer`:**

```json
{
  "session_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "integration_engineer",
  "input_artifacts": [
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/01-TASK_SPECIFICATION.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/03-CONTEXT_VALIDATION_REPORT.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/04-EXECUTION_PLAN.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "Implement the `PaymentProvider` provider adapting the external payments API. Include error handling, timeouts, and response mapping. Criteria: AC-1 (isolated provider), AC-2 (contract tests).",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": ["srp", "dip"], "notes": ["srp: el provider solo adapta, sin lógica de negocio.", "dip: inyectar el provider en PaymentService."]}
}
```

**Subtask B — `functional_writer`:**

```json
{
  "session_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_state": "EXECUTING",
  "target_phase": "orchestrators/core/workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "functional_writer",
  "input_artifacts": [
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/01-TASK_SPECIFICATION.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/03-CONTEXT_VALIDATION_REPORT.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/04-EXECUTION_PLAN.md",
    ".project/a1b2c3d4-e5f6-7890-abcd-ef1234567890/01/05-EXECUTION_SUMMARY.md"
  ],
  "harness_policy": "orchestrators/core/harness/policies/H05-execution-completed.md",
  "task_summary": "Document the functional flow of the integration with the external payments API for business readers. Include user steps, payment states, and possible errors. Criterion: AC-3 (approved functional documentation).",
  "knowledge_entries": [],
  "context_budget": 1000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": [], "notes": []}
}
```

**Justification:** The original prompt combines two domains (technical integration + functional documentation). The guide requires splitting it into sequential subtasks. Subtask A is delegated to the integration profile; once completed, Subtask B consumes `EXECUTION_SUMMARY.md` to document the flow.
