# Context Engineer Guide — Prompt Compression for the Orchestrator

> This document contains techniques for the orchestrator to minimize token usage and context noise before delegating to subagents.
> The goal: inject exactly the rules the subagent needs, and nothing more.

## 1. Cherry-Picking from `_common/`

Do not paste entire `_common/` documents into a prompt unless absolutely necessary. Select only the relevant sections.

| Target Role | Minimum required `_common/` modules | Sections to cherry-pick |
|-------------|-------------------------------------|-------------------------|
| Backend Python Dev | All 9 modules | Usually needed in full because this role touches every layer. |
| Database MySQL Architect | 6 modules | Skip `EXECUTION_CONTEXTS.md` unless the task involves CLI commands. |
| Integration Specialist | 7 modules | Skip `ARCHITECTURE_PRINCIPLES.md` if the provider already exists and only the endpoint changes. |
| QA Engineer | 8 modules | Skip `EXECUTION_CONTEXTS.md` unless testing CLI commands. |
| Technical Writer | 2 modules | `ARCHITECTURE_NAMING.md` (§9-10) + `ARCHITECTURE_PRINCIPLES.md` (§4). |
| Functional Writer | 2 modules | `DOMAIN_OVERVIEW.md` + `COMMUNICATION_RULES.md`. |

## 2. Keyword Activation (Replace prose with tags)

Instead of explaining a rule in sentences, use compact tags the subagent already knows from its training on these documents:

```markdown
[AUTHORITY: OPERATIONAL_RULES_PREVAIL]
[SCOPE: ONLY_EXPLICIT_FILES]
[LAYER: Service | NO_HTTP | NO_FLASK_CONTEXT]
[DEPENDENCY: Views->Services->Models OK | Views->Models FORBIDDEN]
[NAMING: PascalCase+Suffix | snake_case | EnglishOnly]
[DOCSTRINGS: GoogleStyle | English]
[MONETARY: AmountVO | NO_float]
[EXCEPTIONS: DomainOnly | NO_generic]
[CONTEXT: Runtime | click.echo FORBIDDEN]
[OUTPUT: ZERO_FlUFF]
```

## 3. Omit the Obvious

If the target file already declares its path on line 1 (`# apps/payments/services/payment_service.py`), do NOT repeat the full path in the prompt prose.

If the task is "add a method to `PaymentService`", the subagent can infer the layer is `Service`. You do not need to paste the entire `ARCHITECTURE_LAYERS.md` §5.4.

## 4. Inline Context vs. Reference

Use **inline** for:
- Specific code fragments to modify.
- Domain rules that are non-obvious (e.g., "Vencido does NOT block callback processing").
- Exact error messages or API contracts.

Use **reference only** for:
- Standard architecture rules the subagent already read in previous tasks (but still mention them as a compliance reminder).
- Naming conventions (one tag is enough).

## 5. One-Shot Examples over Descriptions

If you need the subagent to follow a pattern, provide a 3-line example instead of a paragraph:

```markdown
Pattern:
class PaymentService:
    def create_payment(self, data: dict) -> Payment:
        """Create a new payment."""
```

## 6. The 50% Rule

Before hitting "send" on a `Task` prompt, evaluate: **can I remove 50% of the words without losing a mandatory instruction?**

If yes, compress.

## 7. Multi-turn Decomposition

If a task requires >3 distinct files or layers, split into multiple `Task` calls rather than stuffing everything into one giant prompt.

Example: instead of one prompt for "design DB + implement service + write tests", use:

1. Task 1 → DB Architect (schema only)
2. Task 2 → Backend Dev (service + model changes, using output from Task 1)
3. Task 3 → QA Engineer (tests, using output from Task 2)

This reduces per-prompt context size and improves output quality.
