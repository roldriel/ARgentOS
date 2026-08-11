# Plan 28 — H07: Trabajo extra autorizado por el usuario

**Status:** Executed
**Fecha:** 2026-08-11
**Aprobación:** Autorización explícita del usuario (2026-08-11) para implementar el plan; RFC-29 pasó a `Accepted`. Criterios de salida verificados: invariantes y citas OK.
**RFC:** RFC-29 (`plans/rfc/29-h07-user-authorized-extra-work.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.1
**Revisión:** 2026-08-11 — correcciones de auditoría (Rama B coherente en todas las secciones de H07, semántica de `scope_respected`, rol de `decision-extractor`, gate de gobernanza).

## Objetivo

Permitir que una sesión con trabajo extra autorizado por escrito pase la verificación de alcance, manteniendo el fallo para el trabajo no autorizado.

## Criterio de entrada

- [ ] RFC-29 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gate de gobernanza para ejecución: RFC-29 `Accepted`, o plan `Aprobado para ejecución` con justificación, antes de modificar `.agents/` (regla RFC-42 en `plans/INDEX.md` §Convenciones).
- [ ] Estado actual verificado contra el repo (no contra este plan): las secciones citadas existen en los archivos de `.agents/`.

## Entregables

1. Contrato `VERIFICATION_REPORT.md` con la semántica de dos ramas en `Scope Compliance`.
2. Policy `H07-scope-compliance.md` con la Rama B en Checklist (ítems 3, 5-6), `Decision Criteria` y Gate Checklist (ítems 4-5).
3. `RUBRICS.md` con el criterio Scope Compliance alineado.
4. `orchestrator.md` (§7 Scope and Autonomy Enforcement) con el procedimiento de validación de evidencia escrita.

## Pasos

1. Reescribir la sección `Scope Compliance` del contrato con la semántica de dos ramas:
   - `scope_respected = true`: el trabajo ejecutado está dentro de la tarea asignada, incluyendo las ampliaciones que el usuario autorizó explícitamente por escrito durante la sesión. `scope_respected = false` es fallo de alcance en ambas ramas.
   - `unplanned_changes`: lista todo cambio fuera del plan aprobado (autorizado o no); vacío en Rama A, lista los cambios en Rama B.
   - `user_authorized_extra_work = true` solo con aprobación escrita evidenciada en `SESSION_LOG.md` o un artefacto de la sesión; `false` en Rama A.
   - Rama A: `scope_respected = true`, `unplanned_changes = []`, `user_authorized_extra_work = false`.
   - Rama B: `scope_respected = true`, `unplanned_changes` lista los cambios, `user_authorized_extra_work = true`, evidencia citada en el reporte.
2. Actualizar el bloque machine-readable `[scope_compliance]` del contrato con la regla condicional de la Rama B: `scope_respected = true` con `unplanned_changes` no vacío es válido solo si `user_authorized_extra_work = true` y la evidencia está citada.
3. Actualizar la Checklist de H07 (ítems 3, 5-6), su sección `Decision Criteria` y su Gate Checklist (ítems 4-5) para las dos ramas: la Rama B es PASS solo con evidencia de autorización; `scope_respected = false` sigue siendo FAIL. Ninguna sección puede exigir `unplanned_changes = []` ni `user_authorized_extra_work = false` incondicionalmente.
4. Alinear `RUBRICS.md` (`VERIFICATION_REPORT_RUBRIC`, criterio Scope Compliance) con las dos ramas.
5. Agregar en `orchestrator.md` (§7 Scope and Autonomy Enforcement) la obligación del Orchestrator de citar la evidencia de la Rama B en `HARNESS_REPORT.md` (pudiendo activar la skill `decision-extractor` para recuperar la decisión confirmada del usuario). Alinear la Checklist ítem 5 de H07 con ese rol: la evidencia la declara el verifier en el reporte y la juzga el Orchestrator en el gate.
6. Ejecutar la verificación documental del repo.

## Criterios de salida

- [ ] H07 evalúa la Rama B con evidencia y deja de exigir `user_authorized_extra_work = false` incondicionalmente (Checklist, `Decision Criteria` y Gate Checklist coherentes).
- [ ] Contrato, policy y rúbrica describen las mismas dos ramas; ninguna sección de H07 exige `unplanned_changes = []` ni `user_authorized_extra_work = false` incondicionalmente.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de consistencia entre contrato, H07 y rúbrica (skill `consistency-checker`).
- Caso de prueba documental: Rama A válida → H07 PASS; Rama B con evidencia → H07 PASS; Rama B sin evidencia → H07 FAIL; `scope_respected = false` → H07 FAIL.

## Riesgos

- Que la Rama B se use para legitimar trabajo no autorizado: mitigado exigiendo evidencia escrita y juicio del Orchestrator.
- Cambio de contrato con impacto en adoptantes: es un cambio MAJOR de semántica; debe registrarse en `CHANGELOG.md` al ejecutarse.

## Trazabilidad

- RFC-29, punto 1.1 de la auditoría, fricción del dogfooding (sin ID propio en `19-anexo-a-bitacora-fricciones.md`).
