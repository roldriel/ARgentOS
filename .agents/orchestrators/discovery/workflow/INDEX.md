# Discovery Workflow Index

This index maps each workflow phase of the `discovery` domain to its state, input/output artifacts, harness trigger, default worker profile/role, and next module.

The Discovery Orchestrator role is defined in `.agents/orchestrators/discovery/roles/discovery_orchestrator.md` and the full state machine in `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`.

| Phase | Module | Required Initial State | Output State | Primary Output Artifact | Harness Trigger | Default Worker Profile/Role | Next Module |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | [Discovery Init](00-discovery-init.md) | `DISCOVERY_INIT` | `DISCOVERY_RUNNING` | `KB_DISCOVERY_REPORT.md` | D00 | `init_worker` | scope-dependent ([01](01-discovery-env.md), [02](02-discovery-stack.md), [04](04-discovery-patterns.md), [05](05-discovery-business.md)) |
| 01 | [Discovery Env](01-discovery-env.md) | `DISCOVERY_RUNNING` | `DISCOVERY_MERGE` | `environment.md` | — | `environment_worker` | [06](06-discovery-merge.md) |
| 02 | [Discovery Stack](02-discovery-stack.md) | `DISCOVERY_RUNNING` | `DISCOVERY_FRAMEWORK` | `stack.md` | — | `stack_worker` | [03](03-discovery-framework.md) |
| 03 | [Discovery Framework](03-discovery-framework.md) | `DISCOVERY_STACK` | `DISCOVERY_MERGE` | `architecture.md` | — | `framework_worker` | [06](06-discovery-merge.md) |
| 04 | [Discovery Patterns](04-discovery-patterns.md) | `DISCOVERY_RUNNING` | `DISCOVERY_MERGE` | `development_patterns.md` | — | `patterns_worker` | [06](06-discovery-merge.md) |
| 05 | [Discovery Business](05-discovery-business.md) | `DISCOVERY_RUNNING` | `DISCOVERY_MERGE` | `business_rules.md` | — | `business_worker` | [06](06-discovery-merge.md) |
| 06 | [Discovery Merge](06-discovery-merge.md) | `DISCOVERY_ENV` / `DISCOVERY_FRAMEWORK` / `DISCOVERY_PATTERNS` / `DISCOVERY_BUSINESS` | `DISCOVERY_VALIDATE` | `.discovery_manifest` | — | `synthesis_worker` | [07](07-discovery-validate.md) |
| 07 | [Discovery Validate](07-discovery-validate.md) | `DISCOVERY_MERGE` | `DISCOVERY_READY` or `DISCOVERY_FAILED` | `HARNESS_REPORT.md` | D01 | — | [08](08-discovery-ready.md) |
| 08 | [Discovery Ready](08-discovery-ready.md) | `DISCOVERY_VALIDATE` | `DISCOVERY_READY` (terminal) | — | — | — | — |

## Notes

- Phases 01–05 run according to the invocation scope (`full`, `env`, `stack`, `patterns`, `business`); `environment_worker`, `stack_worker`, `patterns_worker` and `business_worker` may run in parallel, and `framework_worker` depends on `stack_worker`.
- Phases are ordered and must not be skipped without justification; partial scopes enter at the phase that owns the scope and rejoin at phase 06.
- The `D00` trigger is documented in `.agents/orchestrators/discovery/harness/policies/D00-discovery-init.md`; its decision tree lives in `.agents/orchestrators/discovery/harness/decision_trees/D00_FAIL.toml`.
- `D01-discovery-output` validates the KB structure and ground truth at phase 07.
- Discovery artifacts comply with the contracts in `.agents/orchestrators/discovery/contracts/`.
