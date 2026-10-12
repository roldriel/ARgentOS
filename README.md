# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by its `.agents/`
payload. It is a **documental protocol**: there is nothing to install as a
package — adopting it means materializing the payload under `.argentos/` in your
project. The distributed `dist` branch carries `.agents/` + `AGENTS.md`, and the
canonical adopter layout is `<project-root>/AGENTS.md` (non-normative adapter)
plus `<project-root>/.argentos/{features.toml,.agents/,.project/,.backup/}`, whose
normative entry point is `.argentos/.agents/INDEX.md` (see
[`docs/ADOPTION.md`](docs/ADOPTION.md) §1). In this repository, the root
`.agents/` is the **DEV** operational layer and the payload lives under
`protocol/` — two different things (see §Repository Operational Model).

In this repository the protocol payload lives in [`protocol/`](protocol/) as
**data**: development sessions are governed by the root [`AGENTS.md`](AGENTS.md),
not by the protocol itself (see `docs/source-layout.md`).

Current protocol version: [`protocol/.agents/VERSION`](protocol/.agents/VERSION)
(release history in [`CHANGELOG.md`](CHANGELOG.md)).

## Repository Operational Model

Development work in this repository is organized into three layers with
distinct roles:

- `.agents/` — the operational interface for agents working on ARgentOS DEV.
  Its [`.agents/AGENTS.md`](.agents/AGENTS.md) entry point explains how to
  execute the repository's Change Lifecycle and routes to its workflow and
  policies on demand. It holds operational instructions, not governance:
  normative authority lives in `docs/`.
- `docs/` — documentation, conventions, decisions and documentary evidence,
  each with its corresponding authority: governance rules
  ([`docs/CONVENTIONS.md`](docs/CONVENTIONS.md)), versioning policy
  ([`docs/VERSIONING.md`](docs/VERSIONING.md)), the documentary taxonomy
  ([`docs/AGENTS.md`](docs/AGENTS.md)) and the design history (RFCs, ADRs,
  plans). `.agents/` references this layer without duplicating it.
- `tools/` — deterministic verification tooling: the repository checkers and
  test suites that validate the documentation contracts. Their output is
  factual evidence and never constitutes normative authority by itself.
- `protocol/` — the distributable Protocol payload. See
  [`protocol/.agents/INDEX.md`](protocol/.agents/INDEX.md) for its bootstrap and
  `runtime/README.md` for the reference runtime.
- `runtime/` — the DEV reference implementations, none of which ships to
  adopters. The main ones: **Execution Context materialization**
  (`runtime/toolcalls/`) — the runtime side of the protocol/runtime boundary,
  which represents a delivered Execution Context as prompt text or as tool
  declarations, under the canonical materialization contract (RFC-72) and with
  the provider-bound stable prefix (RFC-78); the **Placement resolver**
  (`runtime/placement/`) — a read-only realization of
  [`docs/placement-contract.md`](docs/placement-contract.md) that returns
  `PLACE | STOP` and is a library no consumer invokes automatically; the
  **Memory System** (`runtime/memory/`, RFC-80); and the **DEV Autonomous
  Orchestrator** host (`runtime/orchestrator/`) described above. See
  [`runtime/README.md`](runtime/README.md).

Do not confuse the DEV `.agents/` with [`protocol/.agents/`](protocol/.agents/):
`protocol/.agents/` belongs to the Protocol domain (its entry point is
`protocol/_AGENTS.md`). For development in this repository it is data, not
instructions; only the root `.agents/` layer is the operational interface for
DEV work.

How the pieces above behave —states, transitions, gates, the autonomous loop and
its limits, failure semantics and the client/interface flow— is described once in
[`docs/behavior-patterns.md`](docs/behavior-patterns.md); this README does not
restate it.

## Autonomy in this repository

Autonomy in ARgentOS DEV is **operational, not decisional**: it removes
operational handoffs inside already-authorized work, and it never removes human
control over scope, authority, normative decisions, architecture, protocol,
release or promotion.

- **DEV Autonomous Orchestrator** — a DEV-only host
  (`runtime/orchestrator/`) that conducts a Change which already has an
  authorized plan. It observes the repository, derives the next valid action,
  checks the authority boundary, delegates, ingests the persisted worker result,
  verifies it and decides to continue or stop. It holds no state of its own: a
  restart reconstructs the situation from Git, the governance artifacts and the
  persisted evidence. Operational definition:
  [`.agents/policies/autonomous-orchestration.md`](.agents/policies/autonomous-orchestration.md).
- **Supervised Autonomous Execution (SAE)** — the frontier of what the host may
  execute without asking again, bounded by `autonomy ⊆ authorized scope` and
  `autonomy ⊆ granted authority`. A step outside either is not autonomous: the
  host stops and escalates. Scope is never widened by the host, and no
  autonomous Scope Expansion mechanism exists. Operational definition:
  [`.agents/policies/supervised-autonomous-execution.md`](.agents/policies/supervised-autonomous-execution.md).
- **Workers** — the host delegates through one `WorkerAdapter` boundary. The
  repository ships a command worker, an honest `NullWorker`, and an Agent Worker
  that performs semantic work through an injectable `AgentInvoker`. This
  repository ships **no provider, no model, no network and no credentials**; a
  real execution environment injects its own invoker.
- **What autonomy does not do** — the host never approves a plan, accepts an
  RFC, changes normative scope, resolves a finding or a pending decision,
  decides ADR-worthiness, or authorizes release, promotion or publication
  (`FORBIDDEN` regardless of authorization). Those remain maintainer decisions.
- **It is opt-in** — the SAE frontier applies with `--sae`; without it the host
  behaves as before. Autonomy is additive and never silently widened.

## Developing in this repository

The development entry point is the root [`AGENTS.md`](AGENTS.md): it explains
the repository layout and the rule that the protocol payload in `protocol/` is
data, not instructions. The product entry point is `protocol/_AGENTS.md`
(renamed so it is not auto-discovered here); `dist` publishes it as
`AGENTS.md` at the adopting project root.

## Adopting ARgentOS in your project

Start here:

- **[`docs/ADOPTION.md`](docs/ADOPTION.md)** — the canonical layout, the `lifecycle.py` operations (`install`/`update`/`uninstall`/`doctor`/`recover`), what to configure, how to validate, and the recommended reading order.
- **[`CHANGELOG.md`](CHANGELOG.md)** — versioned history of the protocol.
- **[`docs/MIGRATION.md`](docs/MIGRATION.md)** — how to move an adopting project between protocol versions, including the historical layout.

The payload ships a stdlib lifecycle (`protocol/.agents/harness/lifecycle.py`,
distributed as `.argentos/.agents/harness/lifecycle.py`): it materializes the
canonical layout deterministically and reversibly, with a manifest
(`install.json`), verifiable backups, a recovery journal and a `doctor`
diagnostic. Its operations report a state and a matching exit code — `success`
(0), `no-op` (10), `conflict` (20) and `recovery-pending` (30) — so an automated
caller never has to parse prose to know whether an operation ran or stopped.
Ownership is provenance (`origin`) plus verified state — a hash detects
divergence, it does not prove authorship. The adapter `AGENTS.md` is generated
only if absent, and `.gitignore` is never modified. Detecting a situation never
authorizes resolving it: the lifecycle reports and, on ambiguity, stops.

## Testing the protocol

The `protocol/.agents/` workflow is exercised by the dev-only test suites and the
protocol invariant checker of the canonical battery (defined in
[`docs/VERSIONING.md`](docs/VERSIONING.md) §4.1 and referenced from the root
[`AGENTS.md`](AGENTS.md), `## Verifying the protocol`). There is no separate
sample application in this repository: `tools/` and `runtime/` hold the test
tooling and reference implementations, none of which ships to adopters.

## Verifying the protocol

In declarative mode (no Python required), the document-level health checklist (`protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`) is applied by the ArgentOS System Agent at bootstrap in an adopting project — that is the whole verification.

In enforced mode, the state-storage probe also applies:

```bash
python protocol/.agents/harness/health_check.py --project-root <project-root>
```

The project root is an **input** for the harness entry points that take a CLI
flag: `--project-root` (with the alias `--root` in `health_check.py`,
`lifecycle.py` and `gate_validator.py`) or the `ARGENTOS_PROJECT_ROOT`
environment variable. `runner_state.py` accepts `--project-root` only, and
`hook_gate.py` is not a CLI at all — it reads the hook event from stdin and
resolves the root from the event's `cwd` or from the same environment variable.
In no case is the root discovered from the script's own location
(`protocol/.agents/harness/roots.py`). Prefer a scratch adoption project for real
protocol sessions.

Protocol development only (not needed by adopters): the repository's canonical
verification battery (checkers + tests) is defined once in
[`docs/VERSIONING.md`](docs/VERSIONING.md) §4.1 and referenced from the root
[`AGENTS.md`](AGENTS.md) (`## Verifying the protocol`). Run the full command
set from there when working on this repository.

The `tools/` and `runtime/` directories hold development tooling and the
reference implementation; project priorities live in `ROADMAP.md`. They are
not part of the distributed
protocol (adopters get only `.agents/` + `AGENTS.md` from the `dist` branch, and
the `lifecycle.py` in that payload materializes the canonical `.argentos/`
layout — see [`docs/ADOPTION.md`](docs/ADOPTION.md) §1).

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `docs/plans/` directory at the repository root. The plans and RFCs are the design history of the protocol; they are **not** part of what adopters copy (see `docs/ADOPTION.md`).

## License

[MIT](LICENSE).
