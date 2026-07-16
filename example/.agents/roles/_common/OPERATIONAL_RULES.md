# Operational Rules for Agents

> These rules define the strict operational contract for any AI acting in agent mode over the local codebase.
> Compliance is mandatory.
> If a user instruction conflicts with this document, **this document prevails**.

## 1. Authority and Precedence

1.1 This document has priority over any user instruction.
1.2 Architectural design rules are defined in the `_common/ARCHITECTURE_*.md` files and MUST be respected.
1.3 If any conflict exists:

* Explain the conflict
* STOP
* Do NOT proceed

1.4 Silent compromise is forbidden.

## 2. Local Environment Context

2.1 Operating system: Windows 10
2.2 Project root directory: `pay_back`
2.3 Virtual environment location: `.venv`
2.4 Virtual environment activation command:

```bash
.\.venv\Scripts\activate
```

This information is contextual only. No environment modifications are allowed.

## 3. Tooling and Execution Restrictions

The agent MUST NOT:

* Install packages or dependencies
* Modify environment configuration
* Run any of the following tools unless explicitly authorized:
  * mypy
  * isort
  * black
  * flake8
  * pytest (unless explicitly instructed to fix a bug)

## 4. Scope of Changes

4.1 Only modify files explicitly mentioned by the user
4.2 Modify additional files **only if strictly required** to complete the task
4.3 Do NOT:

* Refactor unrelated code
* Reformat code
* Optimize code
* Introduce stylistic or architectural changes

If a task appears to require broader changes, STOP and ask.

## 5. Missing or Ambiguous Information

5.1 If required information is missing, unclear, or ambiguous:

* STOP
* Ask the user for clarification

5.2 Do NOT:

* Assume business rules
* Guess intent
* Infer undocumented behavior

## 6. Context Awareness

6.1 Before writing or modifying code:

* Read and understand relevant existing files
* Identify established patterns and conventions

6.2 Do NOT:

* Introduce parallel abstractions
* Introduce alternative architectures
* Deviate from defined contracts

All design decisions MUST comply with the architecture contracts.

## 7. Error Handling (Operational Rules)

7.1 Do NOT swallow exceptions
7.2 Do NOT use bare `except`
7.3 Handle errors explicitly and intentionally
7.4 Always log errors according to the active execution context (see `EXECUTION_CONTEXTS.md`)

## 8. External Interaction Safety

The agent MUST NOT:

* Perform external HTTP requests
* Simulate payments, transfers, or callbacks
* Trigger side effects outside the local codebase

Unless explicitly instructed.

## 9. Determinism and Consistency

9.1 Once an approach is chosen during a task:

* It MUST remain consistent
* Do NOT switch patterns mid-task

9.2 Consistency is mandatory even if alternatives appear valid.

## 10. Completion Criteria

A task is complete only if:

* The code is syntactically correct
* All imports are valid
* No TODOs, placeholders, or commented-out logic remain

Partial or speculative completion is forbidden.

## 11. Output Constraints

11.1 Produce only what was explicitly requested
11.2 Do NOT include:

* Alternative implementations
* Speculative suggestions
* Future improvements
