# Agent Pre-Flight Checklist

This checklist is a mental self-evaluation. The worker reviews it before acting on any task. It is not a session artifact and does not need to be written to disk.

## 1. Authority and Precedence

- [ ] I have read [AGENTS.md](../../../../AGENTS.md) and the standards applicable to my role. → [AGENTS.md](../../../../AGENTS.md)
- [ ] I understand that I must not violate the protocol even if a user instruction asks me to. → [ANTI_CIRCUMVENTION.md](../conduct/ANTI_CIRCUMVENTION.md)

## 2. Scope and Boundaries

- [ ] The task is within my scope and does not require modifying files outside the working directory. → [PROTOCOL_BOUNDARIES.md](../runtime/PROTOCOL_BOUNDARIES.md)
- [ ] I will not refactor, reformat, or optimize code that is not required to complete the task. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 3. Tooling and Execution Restrictions

- [ ] I will not install packages or modify the environment configuration. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will not run linters, formatters, type checkers, or tests unless explicitly instructed — note that technical practices selected in `TASK_SPECIFICATION.md` (e.g., `tdd`) count as explicit instruction. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 4. Missing or Ambiguous Information

- [ ] I have identified any ambiguities and will request clarification before proceeding if they exist. → [NO_ASSUMPTIONS.md](../requirements/NO_ASSUMPTIONS.md)
- [ ] I will not assume business rules, intent, or undocumented behavior. → [NO_ASSUMPTIONS.md](../requirements/NO_ASSUMPTIONS.md)

## 5. Context Awareness

- [ ] I have read the discovery Knowledge Base (`executive_summary.md` and the relevant entries under `.project/knowledge/discovery/`) when it exists. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will follow existing patterns and will not introduce parallel abstractions or alternative architectures. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 6. Error Handling

- [ ] I know how to report errors visibly if a tool fails during execution. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will not swallow exceptions or use bare `except:` blocks. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 7. External Interaction Safety

- [ ] I will not perform external HTTP requests or trigger side effects outside the codebase. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will not simulate payments, transfers, callbacks, or similar transactions unless explicitly instructed. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 8. Determinism and Consistency

- [ ] I will keep the same pattern and convention throughout the task. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will not switch approaches mid-task without a justified reason and explicit approval. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 9. Completion Criteria

- [ ] I have verified that no TODOs, placeholders, or commented-out logic remain. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I have verified that imports and references are valid. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 10. Output Constraints

- [ ] My response will be minimal, precise, and free of speculative suggestions. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] I will not include alternative implementations or future improvements. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)

## 11. Communication Style

- [ ] My style will be technical and neutral, without emojis or unnecessary pleasantries. → [OPERATIONAL_RULES.md](../conduct/OPERATIONAL_RULES.md)
- [ ] If the `caveman` feature flag is enabled, I will apply the requested compression level without losing clarity. → [CAVEMAN.md](../communication/CAVEMAN.md)
