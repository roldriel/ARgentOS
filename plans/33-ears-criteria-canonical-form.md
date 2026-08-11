# Plan 33 — Forma canónica de Acceptance Criteria (EARS)

**Status:** Executed
**Fecha:** 2026-08-11
**Ejecutado:** 2026-08-11 — autorización explícita del usuario (justificación documentada del gate de gobernanza); RFC-34 permanece `Proposal` (regularización pendiente).
**RFC:** RFC-34 (`plans/rfc/34-ears-criteria-canonical-form.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.1 (informe externo, no versionado en el repo)

## Objetivo

Declarar los bullets Markdown como forma canónica de los criterios de aceptación y eliminar la contradicción contrato ↔ H01.

## Criterio de entrada

- [ ] RFC-34 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gobernanza: RFC-34 `Accepted` o plan re-clasificado a `Aprobado para ejecución` con justificación (regla de `plans/INDEX.md` §Convenciones). Sin ese gate no se ejecutan los Pasos sobre `.agents/`.
- [ ] Verificación contra el repo (estado actual esperado): `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` §Acceptance Criteria, muestra el bloque TOML `acceptance_criteria = [""]` como forma principal y bullets solo en el ejemplo; `.agents/orchestrators/core/harness/policies/H01-task-specification.md` §Gate Checklist, exige bullets; `.agents/skills/ears-writer/SKILL.md` §Output Format, produce bullets. Si el estado difiere, detener y reportar; no asumir.

## Entregables

1. `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` §Acceptance Criteria, con bullets canónicos, bloque TOML opcional/derivado y nota de migración para specs históricas TOML-only.
2. `.agents/orchestrators/core/harness/policies/H01-task-specification.md` §Gate Checklist, con la aclaración de violación de forma (criterios solo en TOML).
3. `.agents/skills/ears-writer/SKILL.md` verificado: su salida produce bullets (sin cambio esperado: ya los produce).

## Pasos

1. Reescribir `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` §Acceptance Criteria:
   a. Forma canónica: un bullet Markdown por criterio EARS, atómico y verificable.
   b. El bloque TOML `acceptance_criteria` pasa a representación machine-readable opcional y derivada de los bullets: si se incluye, se deriva de los bullets y debe ser consistente con ellos; se etiqueta como opcional con la nota "no reemplaza a los bullets; un artefacto con criterios solo en TOML no cumple la forma canónica".
   c. Agregar nota de migración: las specs históricas con criterios solo en TOML deben migrar los criterios a bullets.
2. Actualizar el ejemplo del contrato para que coincida con la forma principal (bullets). Si el ejemplo ya es bullets, verificar y no duplicar.
3. En `.agents/orchestrators/core/harness/policies/H01-task-specification.md` §Gate Checklist, en el ítem que exige bullets en `## Acceptance Criteria` (texto actual: "Verify that `## Acceptance Criteria` contains at least one bullet..."), agregar: "Criterios presentes solo en el bloque TOML constituyen una violación de forma; citar la sección como evidencia."
4. Revisar `.agents/skills/ears-writer/SKILL.md` §Output Format: debe producir bullets Markdown (hoy ya lo hace; si no, alinear la skill).
5. En `plans/INDEX.md`, actualizar la fila B-2 del backlog con una nota: "parte EARS (F-01) cubierta por plan 33; parte retry/`RETRY_WORKER` (F-02) pendiente (plan 29)". No marcar B-2 como resuelto.
6. Ejecutar la verificación documental (comandos de Criterios de salida) y registrar la salida como evidencia.
7. Rollback si falla la verificación: `git restore` de los archivos tocados (contrato, H01, skill, `plans/INDEX.md`), o `git revert` del commit correspondiente.

## Criterios de salida

- [ ] El contrato declara una única forma canónica (bullets); el TOML queda como opcional/derivado con la nota correspondiente.
- [ ] H01 §Gate Checklist, describe el fallo por criterios solo en TOML.
- [ ] El contrato incluye la nota de migración para specs históricas TOML-only.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Caso documental (por juicio del revisor; no existe runner mecánico para H01 y `validate_ears` fue removido con el runner): spec de ejemplo con bullets → PASS esperado; spec con criterios solo en TOML → FAIL esperado. Registrar el caso, la evaluación ítem por ítem del Gate Checklist de H01 y la evidencia en el informe de verificación.
- Consistencia contrato ↔ H01 ↔ skill (skill `consistency-checker`).

## Riesgos

- Medio: cambio de forma canónica de un contrato core; impacto en adoptantes con specs TOML-only. Mitigación: nota de migración en el contrato (paso 1c) y aclaración en H01 (paso 3). Rollback con `git restore`/`git revert`.

## Trazabilidad

- RFC-34; fricción F-01 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-2.
