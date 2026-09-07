# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by the `.agents/` directory. It is a **documental protocol**: there is nothing to install — adopting it means vendoring `.agents/` + `AGENTS.md` into your project from the `dist` branch (see [`docs/ADOPTION.md`](docs/ADOPTION.md) §1).

In this repository the protocol payload lives in [`protocol/`](protocol/) as
**data**: development sessions are governed by the root [`AGENTS.md`](AGENTS.md),
not by the protocol itself (see `docs/source-layout.md`).

Current protocol version: see [`protocol/.agents/VERSION`](protocol/.agents/VERSION).

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

Do not confuse the DEV `.agents/` with [`protocol/.agents/`](protocol/.agents/):
`protocol/.agents/` belongs to the Protocol domain (its entry point is
`protocol/_AGENTS.md`). For development in this repository it is data, not
instructions; only the root `.agents/` layer is the operational interface for
DEV work.

## Developing in this repository

The development entry point is the root [`AGENTS.md`](AGENTS.md): it explains
the repository layout and the rule that the protocol payload in `protocol/` is
data, not instructions. The product entry point is `protocol/_AGENTS.md`
(renamed so it is not auto-discovered here); `dist` publishes it as
`AGENTS.md` at the adopting project root.

## Adopting ARgentOS in your project

Start here:

- **[`docs/ADOPTION.md`](docs/ADOPTION.md)** — what to copy, what to configure, how to validate (protocol health verification first), and the recommended reading order.
- **[`CHANGELOG.md`](CHANGELOG.md)** — versioned history of the protocol.
- **[`docs/MIGRATION.md`](docs/MIGRATION.md)** — how to move an adopting project between protocol versions.

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
python protocol/.agents/harness/health_check.py
```

Running the probe from this repository targets `protocol/.project/` (the probe
derives its project root from its own location); prefer a scratch adoption
project for real protocol sessions.

Protocol development only (not needed by adopters): the repository's canonical
verification battery (checkers + tests) is defined once in
[`docs/VERSIONING.md`](docs/VERSIONING.md) §4.1 and referenced from the root
[`AGENTS.md`](AGENTS.md) (`## Verifying the protocol`). Run the full command
set from there when working on this repository.

The `tools/` and `runtime/` directories hold development tooling and the
reference implementation; project priorities live in `ROADMAP.md`. They are
not part of the distributed
protocol (adopters get only `.agents/` + `AGENTS.md` from the `dist` branch).

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `docs/plans/` directory at the repository root. The plans and RFCs are the design history of the protocol; they are **not** part of what adopters copy (see `docs/ADOPTION.md`).

## License

[MIT](LICENSE).
