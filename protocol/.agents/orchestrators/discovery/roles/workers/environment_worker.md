---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: environment_worker
subsystem: discovery
state: discovery:DISCOVERY_ENV
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [discovery_input.json]
output_artifacts: [environment.md]
---

# Worker: environment_worker

## Purpose

Detect the execution environment of the project: operating system, shell, tools
and runtimes, and record them in the `environment.md` KB entry.

The probing procedure — command set per operating system, real shell detection,
timeouts, and the security policy that filters secrets and sensitive
information — is defined in `.agents/standards/context/ENVIRONMENT_PROBE.md`
and is mandatory for this worker.

## Input

- `discovery_input.json` produced by `init_worker` (includes `project_root`,
  `context_budget`, `sample_size` and the previous KB entries to consider).
  For this worker the payload uses `scope: "env"` and may include
  `previous_environment_md`, the previous `environment.md` entry to compare
  against when revalidating.

Example (`INTER_WORKER_MESSAGE` contract):

```json
{
  "message_version": "1.0.0",
  "from_worker": "discovery_orchestrator",
  "to_worker": "environment_worker",
  "payload_type": "discovery_input",
  "payload": {
    "project_root": "/path/to/project",
    "scope": "env",
    "previous_environment_md": "..."
  }
}
```

Example output message:

```json
{
  "message_version": "1.0.0",
  "from_worker": "environment_worker",
  "to_worker": "discovery_orchestrator",
  "payload_type": "partial_output",
  "payload": {
    "environment.md": "..."
  },
  "provenance": {
    "source_files": ["system_probe"],
    "source_sessions": [],
    "confidence": "high"
  }
}
```

## Output

- `environment.md`, written to `.project/knowledge/discovery/environment.md`,
  following the contract
  `.agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md`.
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory) written to `.project/<session-uuid>/discovery/worker_environment.json`.
  Environment facts may declare `"system_probe"` as their source.

## Tasks

1. Detect the operating system, shell, available tools and runtime versions
   using only the commands listed in `ENVIRONMENT_PROBE.md` §2 (Windows and
   Linux/macOS tables). Never use `systeminfo` on Windows; use `where` instead
   of `which` on Windows.
2. Detect the real shell following `ENVIRONMENT_PROBE.md` §3: identify the
   parent process shell when possible; on Windows distinguish Git Bash,
   PowerShell and CMD (Kimi Code CLI on Windows usually defaults to Git Bash);
   record both `primary_shell` and `fallback_shell`.
3. Detect mandatory tools (`python` / `python3`, `git`) and optional tools
   (`node`, `npm`, `yarn`, `pnpm`, `docker`, `uv`, `poetry`, `pip`, `cargo`,
   `go`, `make`) per `ENVIRONMENT_PROBE.md` §4.
4. Document environment variables per `ENVIRONMENT_PROBE.md` §5: only
   variables relevant to agent execution, reported as `present` / `absent`,
   never their values.
5. Execute only safe, read-only commands from the whitelist in
   `ENVIRONMENT_PROBE.md` §6.1. Never install or update tools, never modify
   system or project files, never execute project scripts.
6. Apply the 5-second per-command timeout from `ENVIRONMENT_PROBE.md` §7. On
   failure or timeout, continue with the next command and record the failure in
   the `## Notes` section of `environment.md`.
7. Filter secrets and sensitive information from every captured output before
   writing: drop any line or value containing `TOKEN`, `KEY`, `SECRET`,
   `PASSWORD`, `CRED`, `AUTH` or `PRIVATE` (case-insensitive), replace gaps
   with `<redacted>`, and anonymize personal paths when possible
   (`ENVIRONMENT_PROBE.md` §6.2–6.3).
8. Write `environment.md` following the output format of
   `ENVIRONMENT_PROBE.md` §8, with the provenance fields required by the
   contract (`source_workers` must include `environment_worker`,
   `source_files` may declare `"system_probe"`).

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Read-only: never execute commands that mutate the project or the system.
- Never record secrets, credentials, tokens or sensitive paths.
- The environment entry has a TTL of `discovery_environment_ttl_hours`
  (default 6h, `.agents/features.toml`).

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- On persistent failure the Discovery Orchestrator may continue without this
  output (partial degradation), recording the failure for the manifest.
