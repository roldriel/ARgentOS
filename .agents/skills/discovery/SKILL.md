---
name: discovery
description: Run a project discovery on demand. Use when the user explicitly invokes /discovery or asks to run a project discovery outside the task workflow; /discovery and /discovery full run scope full, /discovery lite runs scope lite. User-invoked skill, outside the activation table by design.
when_to_activate: The user explicitly invokes /discovery or asks to run a project discovery on demand.
when_not: Discovery is triggered automatically by the Orchestrator consent gate, or the user asks for something other than running discovery.
---

# Mission

Run the discovery pipeline for the requested scope and report the result to the user.

## Scopes

- `/discovery` (no arguments) — scope `full`.
- `/discovery full` — scope `full`.
- `/discovery lite` — scope `lite`: environment, language, stack and architecture, without deep qualitative analysis.

## Consent

Explicit user invocation IS the consent: no consent gate applies. The skill must not run a scope different from the one requested.

## Protocol Boundary

This skill invokes the Discovery Orchestrator of the `discovery` domain (`.agents/orchestrators/discovery/roles/discovery_orchestrator.md`) with the requested scope. It performs only discovery work; it grants no other permissions and performs no other project changes.

## Procedure

1. Determine the scope from the invocation: no arguments or `full` → `full`; `lite` → `lite`.
2. Invoke the Discovery Orchestrator with the requested scope, per the canonical scope table of `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` (§Scopes).
3. Wait for the run to reach `discovery:DISCOVERY_READY` or `discovery:DISCOVERY_FAILED`.
4. Report the result to the user.

## Safety Rules

- Run only the requested scope; no scope escalation.
- Never fabricate a run outcome: report the actual status (`DISCOVERY_READY` or `DISCOVERY_FAILED`).
- The run is invoked and reported by this skill; the Discovery Orchestrator does not respond to the user directly.

## Output Format

Report the run outcome to the user:

- Scope executed.
- Result status.
- Entries written or updated.
- Stale entries marked.
- Run duration.
