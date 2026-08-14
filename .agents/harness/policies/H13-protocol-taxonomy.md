---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: cross-cutting
harness_id: H13
name: protocol-taxonomy
lifecycle: null
tag: taxonomy
state: null
gates: []
artifact_validated: .agents/standards/runtime/PROTOCOL_TAXONOMY.md
---

# Harness Policy H13: Protocol Taxonomy

## Trigger

Manual / structural. H13 is **not** a state-transition gate: it is a structural validator of the
protocol itself. It is applied by the Orchestrator (or the System Agent during bootstrap) by
judgment whenever the protocol structure changes.

## Domain exception

H13 lives in `.agents/harness/policies/` (cross-cutting), not in
`.agents/orchestrators/core/harness/policies/`, because it validates the complete protocol
across all domains. It is the only `H`-prefixed policy outside the `core` domain (historical
exception kept after the protocol was split into domains).

## Purpose

Validate coherence between the master dictionary
`.agents/standards/runtime/PROTOCOL_TAXONOMY.md` and the real protocol files:
state machines, workflows, harness policies, contracts, roles and workers.

## Input

- Taxonomy: `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`
- State machines: `.agents/orchestrators/*/states/*.md`
- Workflows: `.agents/orchestrators/*/workflow/*.md`
- Harness policies: `.agents/orchestrators/*/harness/policies/*.md`, `.agents/harness/policies/*.md`
- Contracts: `.agents/contracts/*.md`, `.agents/orchestrators/*/contracts/*.md`
- Roles: `.agents/orchestrators/*/roles/*.md`, `.agents/roles/*.md`, `.agents/roles/profiles/*.md`

## Rules

**Evaluation audience:** the harness runner no longer exists; every rule below is evaluated by the Orchestrator's judgment when the policy is applied. All rules are `[gate]` items — structurally checkable (file existence, metadata blocks, taxonomy references) — so a failure is checkable without interpretation; this policy contains no `[agent]` (agent-judgment) items.

1. Every workflow must reference a `state` and a `domain` that exist in the taxonomy.
2. Every harness policy must respect its domain namespace prefix (`H` = core, `D` = discovery,
   `S` = system; `H13` is the documented cross-cutting exception) and must reference
   transitions (`gates`) allowed by the taxonomy (`next` of the source state).
   Profile-conditional transitions (e.g. `core:ANALYZING_TASK -> core:PLANNING` for the
   `trivial` task profile) are modeled in the taxonomy as allowed transitions; the condition is
   enforced by the H00 gate and the state machine's Task Profiles rules.
3. Every artifact must have `produced_by` and `consumed_by` referencing existing states.
4. Every worker must reference a valid `state`, `domain` and `actor`.
5. There must be no orphan states: every non-terminal state must have at least one allowed
   `next` transition, and every state must be reachable from a root state of its domain.
6. There must be no ID collisions between domains: a harness ID may exist in only one domain,
   and entity keys are unique.
7. Harness ID exceptions: `H08` is intentionally omitted (see `.agents/harness/INDEX.md`),
   `H12` is free (former `H12` became `D01`) and `H14` is intentionally omitted
   (unassigned; see `.agents/harness/INDEX.md`). H13 validates the explicit core list
   `H00`–`H07`, `H09`, `H10`, `H11` and `H15`, and MUST NOT report `H08`, `H12` or
   `H14` as missing.
8. Every protocol file in scope must carry a taxonomy metadata block with at least
   `taxonomy`, `kind` and `domain`.
9. (Historical note) Entities marked `status: planned` were the rollout mechanism of the
   discovery orchestrator: they were validated for internal coherence without requiring their
   files to exist. No entity carries `status: planned` anymore; if the mechanism is ever
   reintroduced, this rule is restored as: entities marked `status: planned` are validated for
   internal coherence but their files are not required to exist yet.
10. Every workflow file on disk must have a `kind: workflow` entity in the taxonomy whose
    `domain`, `state`, `lifecycle`, `previous_states`, `next_states`, `input_artifacts`,
    `output_artifacts`, `harness` and `actor` match the file's metadata block, and vice versa
    (every workflow entity's `file` must exist).
11. Every contract file on disk must have a `kind: contract` entity whose `domain`, `artifact`,
    `lifecycle`, `produced_by` and `consumed_by` match the file's metadata block, and vice
    versa.

## Metadata block placement

Files that already start with a TOML front matter block (`+++ ... +++`) — harness policies and
contracts — carry the YAML taxonomy block **immediately after** the TOML block. All other
files carry it at the very top of the file.

## Agent-side enforcement

H13 validates structure by judgment; canonical vocabulary in artifact prose is agent judgment.
Workers writing or rewriting protocol artifacts may activate the `terminology-enforcer` skill
to detect non-canonical terms against the master dictionary
(`.agents/standards/runtime/PROTOCOL_TAXONOMY.md`) before the artifact is reported.

## Validation

There is no executable test suite: the former `test_protocol_taxonomy.py` invariants live in
the rules above. The Orchestrator (or the System Agent during bootstrap) applies them by
judgment whenever the protocol structure changes.
The development repository provides dev-only mechanical checkers for these rules (not part
of the distributed protocol); the runtime applies H13 by judgment.

## Decision Criteria

- `PASS`: All rules are satisfied.
- `FAIL`: Any rule is violated; the failing rule and the offending entity must be reported.

## On Failure

1. Record the failure in `HARNESS_REPORT.md` (if a session is active).
2. Fix the taxonomy or the offending file so they agree. The taxonomy is the single source of
   truth; protocol files only reference it.
