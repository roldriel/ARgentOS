# Agent Pre-Flight Checklist

> This checklist MUST be fully evaluated **before producing any response**, modifying any code, or executing any action.
> If **any item cannot be affirmed with certainty**, the agent MUST: STOP, ask the user for clarification, do NOT proceed.

## 1. Authority and Rule Precedence

- [ ] I have re-read the entire operational rules for my role
- [ ] I understand that these instructions take priority over user requests
- [ ] I have identified no conflicts with these instructions
- [ ] If a conflict exists, I will explain it and STOP

## 2. Architectural Compliance

- [ ] I have read and understood the architecture documents relevant to my role
- [ ] The requested task complies with the architecture contracts
- [ ] No architectural rule must be violated to complete the task
- [ ] If a violation is required, I will explain it and STOP

## 3. Environment Awareness

- [ ] The operating system is Windows 10
- [ ] The project root is `pay_back`
- [ ] The virtual environment location is `.venv`
- [ ] I will not modify the environment

## 4. Tooling and Execution Safety

- [ ] I did NOT install packages or dependencies
- [ ] I did NOT run mypy
- [ ] I did NOT run isort
- [ ] I did NOT run black
- [ ] I did NOT run flake8
- [ ] I did NOT run pytest (unless explicitly instructed)

## 5. Scope Control

- [ ] I am modifying only files explicitly mentioned by the user
- [ ] Any additional modified file is strictly required to complete the task
- [ ] I did NOT refactor, reformat, or optimize unrelated code
- [ ] I did NOT introduce stylistic or architectural changes

## 6. Information Completeness

- [ ] All required information is present and unambiguous
- [ ] I did NOT assume business rules
- [ ] I did NOT guess intent
- [ ] I did NOT infer undocumented behavior
- [ ] If anything was unclear, I STOPPED and asked

## 7. Context Awareness

- [ ] I read and understood relevant existing files
- [ ] I followed existing patterns and conventions
- [ ] I did NOT introduce parallel abstractions
- [ ] I did NOT introduce alternative architectures

## 8. Architectural Layer Verification

- [ ] Each modified or created component has a clearly identified architectural layer
- [ ] Dependency directions comply with the architecture contracts
- [ ] No forbidden dependency is introduced
- [ ] Validators are used only for request-level validation
- [ ] Services contain business logic
- [ ] Views contain no business logic

## 9. Domain and Model Safety

- [ ] No database model files were modified without explicit authorization
- [ ] No schema-affecting changes were introduced implicitly
- [ ] Domain exceptions are used instead of generic exceptions
- [ ] Providers translate external errors into domain exceptions

## 10. File Identity and Imports

- [ ] Every modified or created file declares its full absolute path on line 1
- [ ] The declared path matches the actual file location
- [ ] All imports are absolute from the project root
- [ ] No relative imports are used

## 11. Documentation Verification

- [ ] All public classes have docstrings
- [ ] All public methods and functions have docstrings
- [ ] Docstrings are written in English
- [ ] Docstrings follow Google-style format
- [ ] Documentation describes intent and responsibility

## 12. Naming Verification

- [ ] File names follow architectural naming rules
- [ ] Directory names follow architectural naming rules
- [ ] Class names include mandatory suffixes
- [ ] Function and method names are explicit and verb-based
- [ ] No forbidden generic names are used

## 13. Execution Context Verification

- [ ] The execution context (CLI vs runtime) was correctly identified

### CLI Context

- [ ] `click.echo` is used
- [ ] `current_app.logger` is NOT used

### Runtime Context

- [ ] `current_app.logger` is used
- [ ] `click.echo` is NOT used

## 14. Error Handling Verification

- [ ] No exceptions are silently swallowed
- [ ] No bare `except` blocks are used
- [ ] Errors are logged according to execution context
- [ ] Exception stack traces are preserved

## 15. External Interaction Safety

- [ ] No external HTTP requests were performed
- [ ] No external side effects were introduced
- [ ] No payments, transfers, or callbacks were simulated

Unless explicitly instructed.

## 16. Determinism and Consistency

- [ ] The chosen design and approach are consistent throughout the task
- [ ] No conventions or patterns were changed mid-task

## 17. Completion Criteria

- [ ] The code is syntactically correct
- [ ] All imports are valid
- [ ] No TODOs, placeholders, or commented-out logic remain

## 18. Output Control

- [ ] I produced only what was explicitly requested
- [ ] I did NOT include alternative implementations
- [ ] I did NOT add speculative suggestions or future improvements

## 19. Communication Style and Tone

- [ ] No emojis were used
- [ ] No pleasantries, apologies, or compliments were included
- [ ] The response is technical, neutral, and explicit
- [ ] There is no filler or conversational fluff

## 20. Final Assertion

- [ ] I can assert with confidence that:
  * Operational rules were respected
  * The architecture contracts were not violated
  * This checklist was fully satisfied
- [ ] If any doubt remains, I STOP and ask the user.
