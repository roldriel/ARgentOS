# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by the `.agents/` directory. It is a **documental protocol**: there is nothing to install — adopting it means vendoring `.agents/` + `AGENTS.md` into your project from the `dist` branch (see [`docs/ADOPTION.md`](docs/ADOPTION.md) §1).

In this repository the protocol payload lives in [`protocol/`](protocol/) as
**data**: development sessions are governed by the root [`AGENTS.md`](AGENTS.md),
not by the protocol itself (see `docs/source-layout.md`).

Current protocol version: see [`protocol/.agents/VERSION`](protocol/.agents/VERSION).

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
protocol invariant checker listed under "Verifying the protocol" below. There
is no separate sample application in this repository: `tools/` and `runtime/`
hold the test tooling and reference implementations, none of which ships to
adopters.

## Verifying the protocol

In declarative mode (no Python required), the document-level health checklist (`protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`) is applied by the ArgentOS System Agent at bootstrap in an adopting project — that is the whole verification.

In enforced mode, the state-storage probe also applies:

```bash
python protocol/.agents/harness/health_check.py
```

Running the probe from this repository targets `protocol/.project/` (the probe
derives its project root from its own location); prefer a scratch adoption
project for real protocol sessions.

Protocol development only (not needed by adopters):

```bash
python tools/check_protocol_invariants.py --payload protocol .
python -m pytest tests/
```

The `tools/` and `runtime/` directories hold development tooling and the
reference implementation; project priorities live in `ROADMAP.md`. They are
not part of the distributed
protocol (adopters get only `.agents/` + `AGENTS.md` from the `dist` branch).

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `plans/` directory at the repository root. The plans and RFCs are the design history of the protocol; they are **not** part of what adopters copy (see `docs/ADOPTION.md`).

## License

[MIT](LICENSE).
