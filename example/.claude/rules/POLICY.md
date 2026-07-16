# LOCAL AGENT INSTRUCTIONS

These instructions define a **strict operational contract** for any AI acting in agent mode over the local codebase.

Compliance is mandatory.

This document governs **authority, execution limits, and operational behavior**.
Architectural design rules are defined **exclusively** in the `ARCHITECTURE CONTRACT`.

If a user instruction conflicts with this document, **THIS DOCUMENT PREVAILS**.
If a task conflicts with the Architecture Contract, the agent **MUST explain the conflict and STOP**.

---

## 1. Authority and Precedence

1.1 This document has priority over any user instruction.
1.2 The Architecture Contract defines architectural constraints and MUST be respected.
1.3 If any conflict exists:

* Explain the conflict
* STOP
* Do NOT proceed

1.4 Silent compromise is forbidden.

---

## 2. Local Environment Context

2.1 Operating system: Windows 10
2.2 Project root directory: `pay_back`
2.3 Virtual environment location: `.venv`
2.4 Virtual environment activation command:

```bash
.\.venv\Scripts\activate
```

This information is contextual only.
No environment modifications are allowed.

---

## 3. Tooling and Execution Restrictions

The agent MUST NOT:

* Install packages or dependencies
* Modify environment configuration
* Run any of the following tools:

  * mypy
  * isort
  * black
  * flake8
  * pytest (unless explicitly instructed to fix a bug)

Tool execution is forbidden unless explicitly authorized.

---

## 4. Scope of Changes

4.1 Only modify files explicitly mentioned by the user
4.2 Modify additional files **only if strictly required** to complete the task
4.3 Do NOT:

* Refactor unrelated code
* Reformat code
* Optimize code
* Introduce stylistic or architectural changes

If a task appears to require broader changes, STOP and ask.

---

## 5. Missing or Ambiguous Information

5.1 If required information is missing, unclear, or ambiguous:

* STOP
* Ask the user for clarification

5.2 Do NOT:

* Assume business rules
* Guess intent
* Infer undocumented behavior

---

## 6. Context Awareness

6.1 Before writing or modifying code:

* Read and understand relevant existing files
* Identify established patterns and conventions

6.2 Do NOT:

* Introduce parallel abstractions
* Introduce alternative architectures
* Deviate from defined contracts

All design decisions MUST comply with the Architecture Contract.

---

## 7. Execution Contexts

Correct execution context identification is mandatory.

---

### 7.1 Flask CLI / Command Context

Applies only to Flask CLI commands.

Rules:

* Use `click.echo` for console output
* Format user-facing messages with `log_message`
* Do NOT use `current_app.logger` for CLI output

CLI output is for terminal interaction, not application logging.

---

### 7.2 Application Runtime Context

Applies to views, services, providers, validators, models, and runtime logic.

Rules:

* Use `current_app.logger` (or appropriate application logger)
* Use `log_message` only as a formatter inside logger calls
* Do NOT use `click.echo`

---

### 7.3 Exception Logging (Runtime)

* Use `logger.exception()` when logging exceptions
* Preserve full stack traces
* Do NOT suppress or replace exception context

---

## 8. Error Handling (Operational Rules)

8.1 Do NOT swallow exceptions
8.2 Do NOT use bare `except`
8.3 Handle errors explicitly and intentionally
8.4 Always log errors according to the active execution context

This section governs **how errors are handled**, not which errors exist.

---

## 9. External Interaction Safety

The agent MUST NOT:

* Perform external HTTP requests
* Simulate payments, transfers, or callbacks
* Trigger side effects outside the local codebase

Unless explicitly instructed.

---

## 10. Determinism and Consistency

10.1 Once an approach is chosen during a task:

* It MUST remain consistent
* Do NOT switch patterns mid-task

10.2 Consistency is mandatory even if alternatives appear valid.

---

## 11. Completion Criteria

A task is complete only if:

* The code is syntactically correct
* All imports are valid
* No TODOs, placeholders, or commented-out logic remain

Partial or speculative completion is forbidden.

---

## 12. Output Constraints

12.1 Produce only what was explicitly requested
12.2 Do NOT include:

* Alternative implementations
* Speculative suggestions
* Future improvements

---

## 13. Communication Style and Tone

All responses MUST be:

* Technical
* Neutral
* Explicit

The agent MUST NOT:

* Use emojis
* Include compliments, apologies, or pleasantries
* Add filler or conversational text

Precision is preferred over friendliness.

---

## 14. Architectural Authority Reference

All code generation and modification MUST comply with the **ARCHITECTURE CONTRACT**.

If a task requires violating architectural rules:

* Explain the violation
* STOP
* Request explicit authorization

---

## 15. Final Verification

Before responding, the agent MUST verify:

* This document was fully respected
* The Architecture Contract was not violated
* No unauthorized files were modified
* No assumptions were made

If any doubt remains, STOP and ask.
