# Plan 21 — Core Skills Pack

**Status:** Executed (4 ago 2026: 17 skills creadas, índice y tabla de activación actualizados, health-check verde, 278 passed / 2 skipped)

**Depends on:** RFC-16 Accepted. Criterio de entrada verificable: `plans/rfc/16-core-skills-catalog-model.md` con header `Status: Accepted` (verificado 4 ago 2026).

**Autoriza:** la creación de archivos bajo `.agents/skills/<nombre>/SKILL.md` y la edición de `.agents/skills/INDEX.md`. La RFC-16 Accepted constituye el acuerdo explícito requerido por la política de inmutabilidad de `.agents/` (convención en `plans/INDEX.md` §Convenciones → Inmutabilidad). Ningún otro archivo de `.agents/` se modifica.

---

# Objetivo

Materializar el Core Skills Pack definido en RFC-16 (`plans/rfc/16-core-skills-catalog-model.md` §Core Skills Pack): 17 Skills nuevas del protocolo, cada una como `.agents/skills/<nombre>/SKILL.md`, listadas en `.agents/skills/INDEX.md`, con el harness verde.

# Formato obligatorio de cada Skill

Según el contrato `.agents/skills/README.md` (§SKILL.md front matter, §SKILL.md body):

- Directorio `.agents/skills/<nombre>/`; `name` del frontmatter igual al nombre del directorio.
- Frontmatter: `name`, `description` (qué hace y cuándo aplica; es la vía de activación por juicio), `when_to_activate`, `when_not`.
- Cuerpo, en orden: procedimiento, reglas de seguridad/restricciones, formato de salida, tabla de references.
- **Idioma: inglés** (convención de `.agents/`).
- `references/` solo si hay material denso que lo justifique; en este pack es la excepción. Si una Skill no tiene references, no lleva la tabla.
- Toda cita a estándares o contratos del protocolo debe resolver contra el repo (ej. `.agents/standards/requirements/EARS.md`).
- Modelo de estilo: `.agents/skills/suggest-commits/SKILL.md` (Mission, reglas, workflow, output format), pero **conciso**: estas Skills son acotadas; apuntar a ~40–90 líneas por SKILL.md, no a 400.

## Sección de frontera (obligatoria en cada Skill)

Toda Skill del pack incluye una sección breve equivalente a la de `suggest-commits` (§Protocol Boundary): la Skill asiste al Worker dentro de la fase que la delega; su salida se embebe en el artefacto de la fase según el contrato correspondiente; ante conflicto, gana el protocolo; la Skill no otorga autoridad.

# Tandas

## Tanda A — Protocolo y calidad (9)

| Skill | Función (RFC-16) | Anclaje que debe citar el SKILL.md |
|---|---|---|
| `ears-writer` | Redacta requisitos en formato EARS. | `.agents/standards/requirements/EARS.md`; fase `02-build-task-specification` |
| `task-spec-validator` | Verifica una Task Specification contra su contrato y EARS. | `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`; `.agents/standards/requirements/EARS.md` |
| `artifact-validator` | Valida un artefacto contra su contrato. | `.agents/contracts/` y `.agents/orchestrators/core/contracts/` |
| `rubric-checker` | Evalúa un entregable contra las rúbricas. | `.agents/standards/quality/RUBRICS.md`; fase `07-verify` |
| `execution-plan-reviewer` | Revisa un plan de ejecución antes de aprobarlo. | `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`; fase `05-plan` |
| `critic` | Critica una propuesta antes de ejecutarla. | Rol `.agents/roles/reviewer.md` |
| `ambiguity-detector` | Detecta ambigüedades que disparan `NEEDS_CLARIFICATION`. | `.agents/standards/requirements/NO_ASSUMPTIONS.md`; fases `00-analyze-task`/`01-confirm-intent` |
| `consistency-checker` | Detecta inconsistencias dentro de o entre artefactos. | Fases `04-validate-context`/`07-verify` |
| `completeness-checker` | Detecta información faltante contra lo que la fase exige. | Fases `04-validate-context`/`07-verify`; contratos de artefactos |

## Tanda B — Análisis y razonamiento (5)

| Skill | Función | Anclaje |
|---|---|---|
| `requirement-extractor` | Extrae requisitos funcionales y no funcionales del pedido. | `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`; fase `00-analyze-task` |
| `extractor` | Extrae hechos relevantes de material extenso. | Fase `03-gather-context` |
| `summarizer` | Resume preservando lo decisional. | Fase `03-gather-context` |
| `planner` | Descompone un objetivo en pasos ordenados y verificables. | `.agents/roles/planner.md`; fase `05-plan` |
| `self-review` | Autoevaluación del resultado antes de reportarlo. | `.agents/roles/verifier.md`; fases `06-execute`/`07-verify` |

## Tanda C — Transformación (3)

| Skill | Función | Anclaje |
|---|---|---|
| `markdown-formatter` | Produce Markdown consistente con las convenciones de artefactos. | Contratos en `.agents/contracts/` |
| `normalizer` | Normaliza terminología y formato entre fuentes. | Fase `03-gather-context` |
| `reference-resolver` | Resuelve referencias entre documentos. | Fases `03-gather-context`/`06-execute` |

# Actualización de `.agents/skills/INDEX.md`

1. Una fila por Skill nueva en §Skill inventory (descripción de una línea, coherente con el frontmatter).
2. §Activation table: poblar solo filas inequívocas (eje fase + perfil, perfiles existentes en `.agents/roles/profiles/`):
   - `02-build-task-specification` | `functional_writer` | `ears-writer`, `task-spec-validator`
   - `01-confirm-intent` | `intent_reflector` | `ambiguity-detector`
   - `07-verify` | `qa_engineer` | `rubric-checker`, `self-review`
3. El resto queda activable por juicio vía `description` (mismo criterio que `suggest-commits`), y la fila del inventario lo indica cuando aplique.

# Verificación (tras cada tanda y al cierre)

- `python .agents/harness/runner.py health-check`
- `python -m pytest .agents/harness/tests/`
- El test estructural `.agents/harness/tests/test_protocol_skills.py` cubre automáticamente las Skills nuevas listadas en el índice.

# Criterios de salida

1. Las 17 Skills existen en disco con frontmatter válido y cuerpo conforme al contrato.
2. `.agents/skills/INDEX.md` lista las 18 Skills (17 + `suggest-commits`) y la tabla de activación tiene las filas declaradas.
3. Health-check y suite de tests en verde.
4. `plans/INDEX.md` actualizado: plan 21 → `Executed` (o `Executed (parcial: …)`).

# Fuera de alcance

- Skills excluidas por RFC-16 (su destino ya está documentado en la RFC).
- `references/` salvo justificación explícita.
- Modificar `SKILLS.md`, contratos, harness, roles o cualquier otro archivo de `.agents/` fuera de `.agents/skills/`.
- Skills de proyecto (`.project/skills/`).
