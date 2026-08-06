# Plan 23 — Skill Lifecycle (Cable-or-Kill)

**Status:** Proposed

**Depends on:** — (ninguno).

**Referencia:** `plans/rfc/24-skill-lifecycle-model.md` (Proposal); inventario de uso real: solo 2 de 34 skills (`reflection`, `planner`) referenciadas fuera de `.agents/skills/`.

---

# Objetivo

Aplicar la regla cable-or-kill de RFC-24: cada skill del catálogo queda integrada a un punto del workflow donde su output alimenta un artefacto o un gate, o se elimina del directorio activo. El listado de skills expuesto al agente pasa de 34 a las que el protocolo realmente usa.

---

# Contenido

## A. Decisión por skill (inventario ejecutable)

- Re-correr el conteo de referencias por skill (grep del nombre fuera de `.agents/skills/<nombre>/` y `skills/INDEX.md`) para fijar la línea base al momento de ejecutar.
- Para cada skill no integrada, aplicar la tabla de cableado de RFC-24 §Inventory: `requirement-extractor`/`goal-extractor`/`constraint-extractor`/`ambiguity-detector`/`intent-detector` → task_analyst (H00, H11); `extractor`/`deduplicator`/`normalizer`/`summarizer` → context_gatherer (H03); `context-validator`/`completeness-checker` → context_validator (H04); `ears-writer`/`task-spec-validator` → task_specification_writer (H01); `risk-detector`/`tradeoff-analyzer`/`critic`/`execution-plan-reviewer` → planner/reviewer (H05); `self-review`/`tdd-reviewer` → executor; `hallucination-checker`/`consistency-checker`/`rubric-checker`/`artifact-validator`/`reference-resolver` → verifier (H10); `hypothesis-generator` → recovery_analyst (H09); `decision-extractor` → session lifecycle (H07); `terminology-enforcer` → H13; `formatter`/`markdown-formatter` → artifact contracts.
- Registrar en el propio plan (tabla de cierre) la decisión final por skill: `cableada` / `eliminada`.

## B. Cableado

- Agregar la referencia explícita de cada skill cableada en el perfil de worker correspondiente (`.agents/orchestrators/core/workflow/*.md` y perfiles de delegación del orchestrator, §"5. Worker Delegation") y/o en la policy de harness de la fase.
- Sin mecanismo nuevo: se usa la sintaxis de declaración de skills que ya usan `reflection` y `planner` en los archivos donde están integradas (seguir ese patrón exacto).

## C. Eliminación

- Quitar de `.agents/skills/` las skills sin cablear; limpiar referencias cruzadas en front matter ("related skills") de las skills supervivientes.
- Actualizar `.agents/skills/INDEX.md` y `PROTOCOL_TAXONOMY.md` con el catálogo resultante.

## D. Verificación

- Grep de cierre: toda skill restante tiene ≥1 referencia fuera de `.agents/skills/` desde rol/workflow/policy/decision tree.
- Suite de tests del harness verde (`python -m pytest .agents/harness/tests runtime/tests tools/tests`).
- Health-check del system agent sin FAILs.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Tabla de decisión por skill (cableada/eliminada) | este plan, §Cierre |
| 2 | Referencias de skills en perfiles/policies | `.agents/orchestrators/core/workflow/`, `.agents/harness/policies/` |
| 3 | Catálogo depurado | `.agents/skills/`, `.agents/skills/INDEX.md`, `PROTOCOL_TAXONOMY.md` |

# Fuera de alcance

- Reescritura de contenido de skills supervivientes.
- Detección mecánica permanente de skills huérfanas (Future Extension de RFC-24).
- Skills de scope user (fuera de `.agents/`).
