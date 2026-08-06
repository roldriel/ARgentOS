# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by the `.agents/` directory. It is a **documental protocol**: there is nothing to install — adopting it means vendoring `.agents/` + `AGENTS.md` into your project from the `dist` branch (see [`ADOPTION.md`](ADOPTION.md) §1).

Current protocol version: see [`.agents/VERSION`](.agents/VERSION).

## Using the protocol in this repository

The full protocol entry point is [`AGENTS.md`](AGENTS.md). An agent that reads it bootstraps the system agent, the state machine, and the orchestrator, which then governs the task lifecycle.

## Adopting ARgentOS in your project

Start here:

- **[`ADOPTION.md`](ADOPTION.md)** — what to copy, what to configure, how to validate (health-check first), and the recommended reading order.
- **[`CHANGELOG.md`](CHANGELOG.md)** — versioned history of the protocol.
- **[`MIGRATION.md`](MIGRATION.md)** — how to move an adopting project between protocol versions.

## Testing the protocol

To validate the `.agents/` workflow, a Flask ABM-style microservice with endpoints, validations, persistence, and tests is used as a model. This microservice is only a test model and may not be available depending on the tests executed at any given time.

## Verifying the protocol

```bash
python .agents/harness/runner.py health-check
python -m pytest .agents/harness/tests/ runtime/tests/
```

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `plans/` directory at the repository root. The plans and RFCs are the design history of the protocol; they are **not** part of what adopters copy (see `ADOPTION.md`).
