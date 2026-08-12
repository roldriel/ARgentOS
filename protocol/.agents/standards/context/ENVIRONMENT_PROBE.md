# Environment Probe Standard

This standard defines how the `environment_worker` (Discovery Orchestrator)
probes the execution environment: the exact command set per operating system,
real shell detection, timeouts, and the security policy that filters secrets
and sensitive information before writing `environment.md`.

It is applied by the worker role defined in
`.agents/orchestrators/discovery/roles/workers/environment_worker.md` and the
output must comply with the contract
`.agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md`.

## 1. Supported operating systems

- Windows 10/11
- Linux (common distributions)
- macOS

## 2. Detection commands per OS

Every command in this standard is read-only. The worker must not execute any
command that is not listed here (see §6, whitelist).

### 2.1 Windows

| Section | Commands |
|---------|----------|
| OS | `ver` or `powershell -Command "(Get-CimInstance Win32_OperatingSystem).Caption"` |
| Architecture | `powershell -Command "(Get-CimInstance Win32_OperatingSystem).OSArchitecture"` |
| Shell | `powershell -Command "$PSVersionTable.PSVersion"` + `$SHELL` if running under Git Bash |
| Python | `where python`, `python --version` |
| Git | `git --version` |
| Node | `where node`, `node --version` |
| Docker | `where docker`, `docker --version` |
| Others | `where npm yarn uv poetry cargo go make` |

Notes:

- Never use `systeminfo`: it is too slow for the per-command timeout.
- Use `where` to locate executables; `which` does not exist on Windows.

### 2.2 Linux / macOS

| Section | Commands |
|---------|----------|
| OS | `uname -a` |
| Architecture | `uname -m` |
| Shell | `echo $SHELL` and `$SHELL --version` |
| Python | `which python python3`, `python3 --version` |
| Git | `git --version` |
| Node | `which node`, `node --version` |
| Docker | `which docker`, `docker --version` |
| Others | `which npm yarn uv poetry cargo go make pip pip3` |

## 3. Real shell detection

The shell actually executing the probe may differ from the system default
shell. The worker must:

1. Detect the parent process shell when possible.
2. On Windows, identify whether the command runs from Git Bash, PowerShell or
   CMD. In Kimi Code CLI on Windows, the default shell is usually Git Bash.
3. Record both `primary_shell` (the shell that executed the probe) and
   `fallback_shell` (an alternative available shell) in `environment.md`.

## 4. Tools to detect

- Mandatory: `python` / `python3`, `git`.
- Optional: `node`, `npm`, `yarn`, `pnpm`, `docker`, `uv`, `poetry`, `pip`,
  `cargo`, `go`, `make`.

A missing mandatory tool is recorded with its absence and an execution
recommendation; a missing optional tool is recorded as `not available`.

## 5. Environment variables

- Only document variables relevant to agent execution (e.g. `PYTHONPATH`,
  `VIRTUAL_ENV`, `CI`, runtime/tool locations).
- **Never record the value** of a variable; only report `present` / `absent`.
- Exclude any variable whose name contains a forbidden string (§6.2).
- Anonymize personal paths when possible (§6.3).

## 6. Security policy

### 6.1 Command whitelist and general rules

The worker may only execute the commands listed in §2. In addition:

1. Only read-only commands.
2. Never install or update tools.
3. Never modify system or project files.
4. Never execute project scripts (build scripts, hooks, package entry points).

### 6.2 Forbidden strings (secret filtering)

Before writing any captured output to `environment.md`, the worker must scan
it and drop any line or value containing (case-insensitive):

```text
TOKEN, KEY, SECRET, PASSWORD, CRED, AUTH, PRIVATE
```

If a dropped fragment leaves a gap, record `<redacted>` instead of the
original text.

### 6.3 Path anonymization

Personal paths (home directories, user names) should be anonymized or omitted
when they are not required to execute the agent. Tool executables needed for
execution recommendations (e.g. the Python executable path) may be kept.

## 7. Timeouts and failure handling

- Each command has a 5-second timeout.
- If a command fails or times out, continue with the next command.
- Record every failure in the `## Notes` section of `environment.md`.

## 8. Output format

The output must comply with
`.agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md`.

Summarized example:

```markdown
## Operating System
- **os**: Windows
- **version**: "11"
- **architecture**: AMD64

## Shell
- **primary_shell**: Git Bash
- **fallback_shell**: PowerShell 7

## Python Runtime
- **version**: 3.11.4
- **executable**: `C:\Python311\python.exe`
- **package_manager**: pip

## Available Tools
- **docker**: not available
- **node**: 20.10.0
- **npm**: 10.2.3
- **git**: 2.42.0

## Execution Recommendations
- Use Git Bash for shell commands.
- Python is available at `C:\Python311\python.exe`.
- Do not use Docker; it is not installed.

## Notes
- `where yarn` failed: command not found.
```
