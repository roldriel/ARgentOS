# Orchestration

This category groups the standards that guide the Orchestrator in deciding **when, to whom, and how to delegate** tasks to workers.

## Files

- [`ORCHESTRATION_GUIDE.md`](./ORCHESTRATION_GUIDE.md) — decision procedure for selecting worker profiles and building delegation payloads.
- [`DECISIONS.md`](./DECISIONS.md) — conceptual catalog of the Orchestrator's discretionary decision points and their concepts of authority.

## Responsibility

Orchestration is exclusively responsible for:

- Selecting the right profile before delegating the `06-execute.md` phase.
- Building payloads that comply with `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- Recording delegation decisions in `.project/<session-uuid>/SESSION_LOG.md`.

It does not define architectural layers (that is `ARCHITECTURE_CONTRACT.md`), context compression techniques (that is `CONTEXT.md`), nor the internal rules of each profile (that is `.agents/roles/profiles/<perfil>.md`).
