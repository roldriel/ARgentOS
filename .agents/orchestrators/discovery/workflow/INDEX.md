# Discovery Workflow Index

This index maps each workflow phase of the `discovery` domain to its state, input/output artifacts, harness trigger, default worker profile/role, and next module.

The Discovery Orchestrator role and the `DISCOVERY_STATE_MACHINE.md` are defined by `plans/PLAN_DISCOVERY_ORCHESTRATOR.md`; this index only covers the modules that already exist.

| Phase | Module | Required Initial State | Output State | Primary Output Artifact | Harness Trigger | Default Worker Profile/Role | Next Module |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | [Discovery Init](00-discovery-init.md) | `DISCOVERY_INIT` | `DISCOVERY_RUNNING` | `KB_DISCOVERY_REPORT.md` | D00 | `discovery_orchestrator` | — |

## Notes

- Phases are ordered and must not be skipped without justification.
- The `D00` trigger is documented in `.agents/orchestrators/discovery/harness/policies/D00-discovery-init.md`.
- Discovery artifacts comply with the contracts in `.agents/orchestrators/discovery/contracts/`.
