# Plan 23 — Skill Lifecycle (Cable-or-Kill)

**Status:** Executed

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

---

# Cierre

Ejecutado el 2026-08-06 (rama `dev`, working tree limpio al inicio).

## Baseline (A)

Conteo de referencias por skill fuera de `.agents/skills/<nombre>/` y `skills/INDEX.md` (grep en `.agents/` sobre `*.md`, `*.toml`, `*.py`): solo `reflection` y `planner` tenían referencias invoker-side reales (roles, workflow, policies, decision trees, tests). El resto de las coincidencias externas eran falsos positivos de subcadena (`critic`→"critical", `formatter`→"formatters", `extractor`→nombres de otras skills) o autodescripción del catálogo. Las demás 32 skills solo se nombraban entre sí (front matter) y en `skills/INDEX.md`.

## Tabla de decisión por skill (B/C)

| Skill | Decisión | Punto de cableado |
| --- | --- | --- |
| requirement-extractor | cableada | `.agents/roles/task_analyst.md` §Skills |
| goal-extractor | cableada | `.agents/roles/task_analyst.md` §Skills |
| constraint-extractor | cableada | `.agents/roles/task_analyst.md` §Skills |
| ambiguity-detector | cableada | `.agents/roles/task_analyst.md` §Skills |
| intent-detector | cableada | `.agents/roles/task_analyst.md` §Skills |
| extractor | cableada | `.agents/roles/context_gatherer.md` §Skills |
| deduplicator | cableada | `.agents/roles/context_gatherer.md` §Skills |
| normalizer | cableada | `.agents/roles/context_gatherer.md` §Skills |
| summarizer | cableada | `.agents/roles/context_gatherer.md` §Skills |
| context-validator | cableada | `.agents/roles/context_validator.md` §Skills |
| completeness-checker | cableada | `.agents/roles/context_validator.md` §Skills |
| ears-writer | cableada | `.agents/roles/task_specification_writer.md` §Skills |
| task-spec-validator | cableada | `.agents/roles/task_specification_writer.md` §Skills |
| planner | cableada (ya integrada) | `.agents/roles/planner.md` §Skills (refuerzo) |
| risk-detector | cableada | `.agents/roles/planner.md` §Skills |
| tradeoff-analyzer | cableada | `.agents/roles/planner.md` §Skills |
| critic | cableada | `.agents/roles/planner.md` §Skills |
| execution-plan-reviewer | cableada | `.agents/roles/reviewer.md` §Skills |
| self-review | cableada | `.agents/roles/executor.md` §Skills |
| tdd-reviewer | cableada | `.agents/roles/executor.md` §Skills |
| rubric-checker | cableada | `.agents/roles/verifier.md` §Skills |
| artifact-validator | cableada | `.agents/roles/verifier.md` §Skills |
| consistency-checker | cableada | `.agents/roles/verifier.md` §Skills |
| hallucination-checker | cableada | `.agents/roles/verifier.md` §Skills |
| reference-resolver | cableada | `.agents/roles/verifier.md` §Skills |
| hypothesis-generator | cableada | `.agents/roles/recovery_analyst.md` §Skills |
| decision-extractor | cableada | policy `.agents/orchestrators/core/harness/policies/H07-scope-compliance.md` (ítem 5 del checklist) |
| terminology-enforcer | cableada | policy `.agents/harness/policies/H13-protocol-taxonomy.md` §"Agent-side enforcement" |
| formatter | cableada | `.agents/roles/worker.md` §"Skill Consumption" (delegaciones que producen artefactos) |
| markdown-formatter | cableada | `.agents/roles/worker.md` §"Skill Consumption" |
| reflection | ya integrada | sin cambios (roles/profiles, H11, decision trees) |
| decomposer | eliminada | sin punto de consumo real; solapaba con `planner` |
| counterargument | eliminada | sin punto de consumo real; solapaba con `critic` |
| suggest-commits | **conservada (corrección post-ejecución)** | Es una skill de utilidad para el proyecto adoptante (invocada por el usuario sobre su repo git), no una fase del workflow: el criterio "¿qué fase la consume?" no aplicaba. Restaurada el 2026-08-05 por decisión del usuario; queda fuera de la activation table por diseño. |

Catálogo resultante: 32 skills (34 − 2 eliminadas: `decomposer`, `counterargument`).

## Archivos modificados

- `.agents/roles/task_analyst.md`, `context_gatherer.md`, `context_validator.md`, `task_specification_writer.md`, `planner.md`, `reviewer.md`, `executor.md`, `verifier.md`, `recovery_analyst.md`, `worker.md` — sección `## Skills` (o nota en §"Skill Consumption") con las skills activadas por rol.
- `.agents/orchestrators/core/harness/policies/H07-scope-compliance.md` — referencia a `decision-extractor`.
- `.agents/harness/policies/H13-protocol-taxonomy.md` — §"Agent-side enforcement" con `terminology-enforcer`.
- `.agents/skills/INDEX.md` — inventario depurado (32 filas; `suggest-commits` restaurada como skill de utilidad) y activation table extendida a las fases 00–08.

## Archivos eliminados

- `.agents/skills/decomposer/`, `.agents/skills/counterargument/` (directorios completos). `.agents/skills/suggest-commits/` fue eliminado en la ejecución y restaurado tras la revisión del usuario.

## Verificación (D)

- Grep de cierre: las 32 skills resultantes tienen (31 cableadas + suggest-commits como utilidad) ≥1 referencia desde `roles/`, `orchestrators/`, `harness/`, `standards/`, `delegation/` o `contracts/` fuera de `.agents/skills/`. OK.
- `python .agents/harness/runner.py health-check` → 81 PASS, 0 FAIL, exit 0.
- `python -m pytest .agents/harness/tests/ runtime/tests/ tools/tests/` → 354 passed, 2 skipped.

## Desviaciones del plan

- **Mecanismo de cableado:** ni `reflection` ni `planner` tenían una "sintaxis de declaración de skills" propia en archivos invoker-side (sus referencias eran nombres de rol/artefacto); el único mecanismo declarativo existente es la activation table + `skills: [...]` del payload. Se cableó con una sección `## Skills` declarativa en cada archivo de rol (`.agents/roles/*.md` — "rol o perfil de worker" según la definición de skill integrada de RFC-24), sin introducir mecanismo nuevo: la activación sigue pasando por la activation table y SKILLS.md §Activation. La activation table quedó consistente con el cableado.
- **PROTOCOL_TAXONOMY.md no se tocó:** no lista skills por diseño (`standards/orchestration/SKILLS.md` §"Validation": "Skills intentionally stay out of PROTOCOL_TAXONOMY.md").
- **`execution-plan-reviewer` cableada en `reviewer.md`** (rol que revisa `EXECUTION_PLAN.md` antes de `PLAN_READY`) en lugar de `planner.md`: el consumidor real del review es el reviewer, no el planner.
- **RFC-24 menciona policy H10 para el verifier;** la policy de verificación es H06 (H10 es kb-discovery-report). Se cableó en el rol `verifier.md`, que es el punto de consumo real.
- No se hizo commit: cambios en working tree para revisión.
