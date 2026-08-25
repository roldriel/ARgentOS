# Authorization Standard

## Purpose

Define when a capability is actually authorized to produce an effect, how the
protocol records that authorization, and how the trace distinguishes
AUTHORIZED, UNAUTHORIZED and AUTHORIZATION_UNDETERMINED. The standard closes
the gap between "the tool is available" and "the tool may be used": capability
never implies authorization.

## Vocabulary

- **Capability:** availability of a tool or skill in the runtime. A capability
  says nothing about permission.
- **Permission:** a protocol rule: the default frontier plus the policies that
  qualify it.
- **Authorization:** a recorded link between a capability and a permitted
  effect for one execution.
- **Execution:** the effective use of a capability.
- **Effect:** an observable change produced by an execution.

A capability is never an authorization: the fact that a tool or skill is
available does not permit its use outside the frontier.

## Default frontier

Inside the frontier, no explicit authorization is required:

- reading and executing within the project and within the protocol;
- planned writes covered by `TASK_SPECIFICATION.md` / `EXECUTION_PLAN.md`.

Outside the frontier, explicit authorization is required:

- network / HTTP interactions;
- remote git operations;
- installations;
- destructive changes;
- writes outside the project.

The canonical frontier list lives in
`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (single source). This
standard defines the model and does not duplicate the list.

## Effects block

`TASK_SPECIFICATION.md` declares an `## Effects` section when the task includes
effects outside the frontier. Every entry of the `[[effects]]` block has:

- `name` — unique within the artifact;
- `kind` — closed enum: `network` | `remote_git` | `install` | `destructive` |
  `write_outside_project`;
- `authorized_by` — `user` | `unattended_default`;
- `evidence_ref` — reference to the record that sustains the authorization (for
  example a clarification entry of `SESSION_BRIEF.md` or an entry of
  `SESSION_LOG.md`), using the evidence classes of the evidence standard;
- `status` — `authorized` | `not_authorized` | `pending_user_confirmation`.

Example:

```toml
[[effects]]
name = "fetch_remote_sources"
kind = "network"
authorized_by = "user"
evidence_ref = "SESSION_BRIEF.md clarification 5A"
status = "authorized"
```

## Who can authorize

- **User:** via a clarification or an explicit plan confirmation; recorded in
  `SESSION_BRIEF.md`.
- **Declared unattended default:** applied under unattended mode and recorded
  as `PENDING_USER_CONFIRMATION` with `source: unattended_default` in
  `SESSION_BRIEF.md`; it authorizes only with that status until the user
  reviews it.
- **Runtime / scripts:** never. Scripts execute capabilities; they do not grant
  permissions.

An assumption with `user_confirmed: false` never constitutes authorization:
only the user's confirmation or a declared unattended default recorded as
`PENDING_USER_CONFIRMATION` authorizes an out-of-frontier effect.

## Authorization states

- **AUTHORIZED:** a recorded `effects` entry with non-empty `authorized_by` and
  `status` in `authorized` / `pending_user_confirmation`.
- **UNAUTHORIZED:** a recorded denial: an `effects` entry with
  `status: not_authorized`.
- **AUTHORIZATION_UNDETERMINED:** no sufficient record to decide.

UNAUTHORIZED must never be inferred from the absence of a record: when no
`effects` entry exists, the state is AUTHORIZATION_UNDETERMINED.

## Execution records

`EXECUTION_SUMMARY.md` records executed effects in its `## Effects Executed`
section. Every executed out-of-frontier effect is registered with a reference
to its authorization entry, so the trace answers AUTHORIZED /
UNAUTHORIZED / AUTHORIZATION_UNDETERMINED per effect.

## Invariants

```text
AUTH-001: every out-of-frontier effect has an effects entry with authorized_by
          and status.
AUTH-002: user_confirmed=false never constitutes authorization.
AUTH-003: every executed effect is recorded in EXECUTION_SUMMARY.md with a
          reference to its authorization.
AUTH-004: AUTHORIZATION_UNDETERMINED is never reported as UNAUTHORIZED.
```

## Relationship to other standards

- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — canonical frontier list;
  this standard defines the authorization model behind it.
- `.agents/standards/quality/EVIDENCE.md` — `evidence_ref` cites the record
  that sustains an authorization using the evidence classes (`assertion` for a
  user clarification, `reference` for a session-log entry).
- `.agents/standards/requirements/NO_ASSUMPTIONS.md` — `user_confirmed: false`
  marks unconfirmed assumptions; it never authorizes an effect.
- `.agents/contracts/SESSION_BRIEF.md` — records clarifications and deferred
  approvals that authorize effects.
