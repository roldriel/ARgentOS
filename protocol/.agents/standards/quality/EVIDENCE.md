# Evidence Standard

## Purpose

Define what counts as evidence, how evidence is recorded, and when a claim or an
artifact may be declared VERIFIED. The standard closes the gap between "this was
verified" and "the agent said it was verified": every claim emitted by the
protocol is either evidence-cited with a class, or explicitly marked as an
attestation or inference.

## Evidence classes

Every evidence entry belongs to exactly one of five classes:

| Class | Definition | Required fields | Optional fields |
|---|---|---|---|
| `observation` | Direct reading of a durable object (file, artifact, configuration). Re-verifiable by re-reading. | `class`, `claim_id`, `ref` | — |
| `measurement` | Output of a command or tool with recorded command, exit code and a reference to the captured output. Re-executable best-effort under the recorded environment. | `class`, `claim_id`, `ref` | `command`, `exit_code` |
| `attestation` | The agent's claim about its own process or state, not re-derivable from durable objects. Always carries actor, statement and the explicit mark. | `class`, `claim_id`, `ref`, `actor`, `statement` | — |
| `assertion` | Data or confirmation provided by the user (for example a clarification). Registered in `SESSION_BRIEF.md` / `SESSION_LOG.md`. | `class`, `claim_id`, `ref` | — |
| `reference` | Citation to an artifact or rule: path (optional hash) and section. | `class`, `claim_id`, `ref` | `section`, `hash` |

An `attestation` is the agent's statement about its own process; it is never a
substitute for externally verifiable evidence. An `assertion` is a user-provided
fact or confirmation, not the agent's own statement.

## Evidence entries

Evidence is recorded in structured `[[evidence]]` blocks. Each entry has:

- `class` — one of the five classes above;
- `claim_id` — the identifier of the claim it supports (an acceptance criterion
  `AC-01`, a test result `TR-01`, or a gate check id `H06-5`);
- `ref` — the artifact or rule it references (path, `path:section`, or command
  output).

Example:

```toml
[[evidence]]
class = "measurement"
claim_id = "AC-07"
ref = "tests/sync/test_tree_exporter.py"
command = "python -m pytest tests/sync/test_tree_exporter.py"
exit_code = 0

[[evidence]]
class = "attestation"
claim_id = "AC-11"
actor = "executor"
statement = "sources/ were not opened while writing the kit"
```

### How `ref` resolves

`ref` carries the artifact or rule an entry stands on. Its meaning is decided by
the **evidence class**, never by the caller (ADR-21):

- `reference` and `observation` name a durable object. `ref` is a **project-relative**
  path: `path` or `path:section`. It is resolved against the project root — the
  directory the session belongs to, passed explicitly by the caller and never
  discovered from the artifact path. For a Markdown target, `:section` must name
  a heading that exists in it.
- The following are rejected: absolute paths (POSIX root-relative or Windows
  drive/UNC), any traversal that leaves the project root, targets that do not
  exist, and sections that do not exist. Containment is decided on the resolved
  path, so `..` and junctions cannot name something outside the project.
- `measurement` is backed by `command` and `exit_code`; its `ref` identifies the
  captured output and is not resolved as a filesystem path.
- `attestation` and `assertion` are not resolved against the filesystem at all:
  their content is a statement, and a path-like string in them does not acquire
  evidentiary force by looking like a path.

There is no `hash` field. This standard defines no algorithm, no bytes to hash,
no normalization and no moment of verification, so a hash is neither required
nor read: adding one without that definition would claim an integrity the
protocol cannot check.

## Sufficiency rules

1. A `[gate]` item of a PASS gate is satisfied only by `observation`,
   `measurement` or `reference` evidence, or by a documented deviation. An
   `attestation` never satisfies a `[gate]` item without a documented deviation.
2. An `[agent]` item must cite evidence; when the evidence is an `attestation`,
   it must carry the mark (actor + statement).
3. "Verified" in a report requires an evidence entry with a class other than
   `attestation` for the claim; without it the permitted term is "attested".
4. Every evidence entry carries `class`, `claim_id` and `ref`.

## Claim classes

`claim_class` (`verified` | `attested` | `inference`) records the claim-level
result:

- `verified` — the claim is supported by at least one evidence entry of class
  `observation`, `measurement`, `assertion` or `reference`.
- `attested` — the claim rests only on the agent's attestation (marked) or on no
  citable evidence; it is declared explicitly and never presented as verification.
- `inference` — the claim is an explicit semantic extrapolation; it is declared
  without evidence entries.

A claim with a non-empty `evidence` field but no explicit `claim_class` is
treated as `verified` and must satisfy the same requirement.

## The VERIFIED invariant

An artifact declares "verified" for a claim if and only if:

- the corresponding gate records PASS (Gate State in `state.json`, for example
  H06/H07 for VERIFICATION_REPORT), and
- the claim is supported by evidence of a class other than `attestation`.

Otherwise the permitted term is "attested". The artifact lifecycle value
`validated` is a different dimension: `validated` is derived from the exit-gate
PASS record and never written by hand (see `.agents/harness/INDEX.md`, §State
dimensions).

## Recording locations

- `VERIFICATION_REPORT.md` — `## Evidence` section with `[[evidence]]` blocks;
  acceptance criteria and test results reference entries by `claim_id`.
- `HARNESS_REPORT.md` — ENTRY comments may carry an `evidence` array; each
  entry's `claim_id` is the check id it supports.

## Invariants

```text
EV-001: every gate PASS has, per [gate] item, observation/measurement/reference
        evidence or a documented deviation.
EV-002: every attestation carries actor, statement and the mark.
EV-003: every evidence entry carries class, claim_id and ref.
EV-004: "verified" in a report requires an evidence entry of a class other than
        attestation for that claim (or the term "attested" is used).
REL-001: an artifact declares "verified" iff Gate State PASS + non-attestation
         evidence for the claim (or "attested" is used).
REL-002: `validated` in the artifact lifecycle iff the exit gate has PASS in
         state.json.
REL-003: every evidence entry references the artifact and the claim it supports.
```

## Relationship to other standards

- `.agents/standards/quality/CONFIDENCE.md` — confidence levels are derived from
  evidence; the classes here define what counts as citable evidence for a level.
- `.agents/standards/runtime/PROTOCOL_METRICS.md` — metrics events are
  self-reported; a claim about metrics is verified only with non-attestation
  evidence (for example the declared/consumed pair).
- `.agents/contracts/HARNESS_REPORT.md` — the review trail records gate checks;
  each check cites evidence with class or declares its claim class.
