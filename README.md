# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by the `.agents/` directory. It is a **documental protocol**: there is nothing to install — adopting it means vendoring `.agents/` + `AGENTS.md` into your project from the `dist` branch (see [`ADOPTION.md`](ADOPTION.md) §1).

Current protocol version: see [`.agents/VERSION`](.agents/VERSION).

## Using the protocol in this repository

The full protocol entry point is [`AGENTS.md`](AGENTS.md). An agent that reads it bootstraps the system agent, the state machine, and the orchestrator, which then governs the task lifecycle.

## Adopting ARgentOS in your project

Start here:

- **[`ADOPTION.md`](ADOPTION.md)** — what to copy, what to configure, how to validate (protocol health verification first), and the recommended reading order.
- **[`CHANGELOG.md`](CHANGELOG.md)** — versioned history of the protocol.
- **[`MIGRATION.md`](MIGRATION.md)** — how to move an adopting project between protocol versions.

## Testing the protocol

The `.agents/` workflow is exercised by the dev-only test suites and the
protocol invariant checker listed under "Verifying the protocol" below. There
is no separate sample application in this repository: `dev/` holds the test
tooling and reference implementations, none of which ships to adopters.

## Verifying the protocol

In declarative mode (no Python required), the document-level health checklist (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) is applied by the ArgentOS System Agent at bootstrap — that is the whole verification.

In enforced mode, the state-storage probe also applies:

```bash
python .agents/harness/health_check.py
```

Protocol development only (not needed by adopters):

```bash
python dev/tools/check_protocol_invariants.py .
python -m pytest .agents/harness/tests/ dev/runtime/tests/ dev/tools/tests/
```

The `dev/` directory holds development tooling and reference implementations; it is not part of the distributed protocol (adopters get only `.agents/` + `AGENTS.md` from the `dist` branch).

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `plans/` directory at the repository root. The plans and RFCs are the design history of the protocol; they are **not** part of what adopters copy (see `ADOPTION.md`).
