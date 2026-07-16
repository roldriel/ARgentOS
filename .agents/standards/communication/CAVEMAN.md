# CAVEMAN — Compressed communication standard

> **Protocol language note:** This standard applies to **all** protocol communication. Internal communication (orchestrator ↔ worker, session artifacts, logs, harness reports) uses **English**. User-facing communication uses **neutral Spanish**.

## Purpose

This document defines the optional compressed communication mode for the ARgentOS protocol. When active, CAVEMAN applies to **all** protocol communication.

CAVEMAN seeks:

- Reduce tokens without losing technical precision.
- Eliminate filler, unnecessary courtesies, and verbal hedges.
- Keep technical substance intact.
- Use exact technical terms.

When active, CAVEMAN applies to **all** protocol communication:

- Messages to the user → neutral Spanish.
- Free text in session artifacts → English.
- Worker-to-orchestrator return reports → English.
- `SESSION_LOG.md` and `HARNESS_REPORT.md` entries → English.

## Central principle

> Technical substance intact. Filler dies.

## Activation

CAVEMAN is activated via the `caveman` feature flag in `.agents/features.toml` or the `AGENTS_FEATURE_CAVEMAN` environment variable.

When the flag is disabled, the protocol uses its base communication style.

## Levels

| Level | Description | When to use |
|---|---|---|
| **lite** | No filler or hedges. Keeps articles and full sentences. Professional but tight. | Formal user communication or documentation that must be easy to read. |
| **full** | Drops unnecessary articles, fragments OK, short synonyms. Compressed. | Default for all protocol communication. |
| **ultra** | Abbreviates everything (DB/auth/config/req/res/fn/impl), no conjunctions, arrows for causality (X → Y), one word when enough. | Summaries, dense logs, messages where context is already clear. |

The default level is **full**. The orchestrator may pass another level in the delegation payload.

## Rules

### 1. Remove what does not add value

- Extra articles (`the/a/an`, `el/la/los/las`) when they do not add clarity.
- Filler: `mira`, `fíjate`, `básicamente`, `realmente`, `en realidad`, `por favor` as opener; `look`, `basically`, `actually`, `really`.
- Courtesies: `con gusto`, `de nada`, `servido`, `por supuesto`, `un placer`; `my pleasure`, `you're welcome`, `of course`, `happy to help`.
- Verbal hedges: `probablemente`, `tal vez`, `posiblemente`, `parece ser`, `quizás`, `creo que`; `probably`, `maybe`, `possibly`, `seems`, `perhaps`, `I think`.

### 2. Use short synonyms

- `corrige` / `fix` instead of `implementa una solución para` / `implement a solution for`.
- `revisa` / `review` instead of `realiza una revisión de` / `perform a review of`.
- `verifica` / `verify` instead of `verifica la correctitud de` / `verify the correctness of`.
- `elimina` / `remove` instead of `elimina de forma permanente` / `remove permanently`.

### 3. Keep technical terms exact

Do not abbreviate project-specific names or terms that lose meaning. Examples of terms that remain intact:

- `TASK_ANALYSIS.md`, `EXECUTION_PLAN.md`
- `orchestrator`, `worker`, `harness`
- file names, paths, functions, variables, and errors

### 4. Do not touch code blocks

Code, YAML, JSON, SQL, and terminal command blocks remain unchanged. CAVEMAN applies to the surrounding text, not to their content.

### 5. Quote errors exactly

When reporting an error, copy the exact message or traceback. Do not paraphrase.

### 6. Suggested pattern

```text
[thing] [action] [reason]. [next step].
```

Example (internal, English):

> Bug in auth middleware. Token validation uses `<` not `<=`. Fix:
>
> ```python
> if expires_at <= now:
> ```

Example (user-facing, neutral Spanish):

> Bug en middleware de auth. Validación de token usa `<` no `<=`. Corrige:
>
> ```python
> if expires_at <= now:
> ```

## Examples by level

### User-facing clarification request (neutral Spanish)

- **lite**: "Necesito saber si quieres persistir el token en la base de datos o solo en memoria."
- **full**: "¿Token en DB o en memoria?"
- **ultra**: "Token → DB? memoria?"

### Internal artifact generation report (English)

- **lite**: "Artifact `02-CONTEXT_ARTIFACT.md` was generated successfully in the current iteration."
- **full**: "Artifact `02-CONTEXT_ARTIFACT.md` generated. Ready for validation."
- **ultra**: "`02-CONTEXT_ARTIFACT.md` → OK."

### User-facing plan description (neutral Spanish)

- **lite**: "El plan consiste en agregar el campo `email` al schema de usuario, crear la migración correspondiente y actualizar el endpoint POST /users."
- **full**: "Plan: agregar `email` al schema, migrar DB, actualizar POST /users."
- **ultra**: "Schema +email → migración → POST /users."

### Internal plan description (English)

- **lite**: "The plan is to add the `email` field to the user schema, create the migration, and update the POST /users endpoint."
- **full**: "Plan: add `email` to schema, migrate DB, update POST /users."
- **ultra**: "Schema +email → migration → POST /users."

### User-facing intent reflection (neutral Spanish)

- **lite**: "Entendí que quieres un microservicio en Flask con CRUD de usuarios, persistiendo en SQLite. ¿Confirmas?"
- **full**: "Microservicio Flask + CRUD usuarios + SQLite. ¿OK?"
- **ultra**: "Flask CRUD users SQLite → confirm?"

## Clarity exceptions

Drop CAVEMAN (or switch to a clearer register) for:

1. Security warnings.
2. Confirmations of irreversible actions.
3. Multi-step sequences where fragment order could be misread.
4. When the user explicitly asks to clarify or repeat something.

After the clear part, return to CAVEMAN.

Example (user-facing):

> **Advertencia:** Esto elimina permanentemente todas las filas de `users` y no se puede deshacer.
>
> ```sql
> DROP TABLE users;
> ```
>
> Verifica el backup primero. Seguimos con estilo comprimido.

## Relationship to OUTPUT_EFFICIENCY.md

- [`OUTPUT_EFFICIENCY.md`](OUTPUT_EFFICIENCY.md) is the universal base for minimal output. It applies always.
- `CAVEMAN.md` is the optional compressed mode activated by feature flag. It applies to **all** protocol communication, adding compression on top of [`OUTPUT_EFFICIENCY.md`](OUTPUT_EFFICIENCY.md).
- Language rule: internal communication uses English; user-facing communication uses neutral Spanish.
- In case of conflict, the Cold Robot Principle prevails.

## Application by communication type

### User-facing (orchestrator / worker talking to the user)

Use CAVEMAN in neutral Spanish. Use **full** by default. Switch to **lite** if the user asks or the context is formal. Use **ultra** only when the user already knows the context.

This includes the final task summary delivered to the user: it must be short, concise, and contain no extra information outside the requested scope.

### Session artifacts

Use CAVEMAN in English. Use **full** for free-text sections. YAML/JSON/code blocks remain intact.

### Worker-to-orchestrator return report

Use CAVEMAN in English. Use **full** or **ultra** depending on complexity.

Example:

```text
Artifact generated: 05-EXECUTION_SUMMARY.md.
Changes: app/schemas/user.py, app/routes/users.py.
Next state: VERIFYING.
Blockers: none.
```

### Session logs and harness

Use CAVEMAN in English, ultra level if applicable:

```text
H01 → PASS | 12ms | TASK_SPECIFICATION.md OK
```

## Limits

- CAVEMAN does not apply to source code, commits, variable names, or user project PRs.
- CAVEMAN does not justify ambiguity. If a compressed phrase can be read two ways, rewrite it more clearly (even if it uses more words).
- CAVEMAN does not replace other standards (`EARS.md`, `RUBRICS.md`, `CONTEXT.md`, [`OUTPUT_EFFICIENCY.md`](OUTPUT_EFFICIENCY.md)). Artifacts and messages must comply with all applicable standards.
