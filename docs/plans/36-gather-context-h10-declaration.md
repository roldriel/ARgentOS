# Plan 36 — Declaración del gate H10 en la fase 03

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-37 (`plans/rfc/37-gather-context-h10-declaration.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.4
**Vía de autorización:** Vía plan (RFC-42): plan `Aprobado para ejecución` con justificación documentada — el usuario autorizó el 2026-08-11 corregir y dejar implementables los planes 34–36 tras la auditoría (RFC-37 sigue en `Proposal`; la vía plan habilita el cambio de `.agents/`).
**Nota de ejecución (2026-08-11):** implementado por decisión del usuario; criterios de salida verificados (`check_protocol_invariants.py` y `check_plan_citations.py` en verde); registro en `CHANGELOG.md` 3.0.4.

## Objetivo

Reconciliar la metadata de H10 (policy y taxonomía) con su naturaleza de gate opcional de uso y limpiar el front matter del workflow 03.

## Criterio de entrada

- [ ] RFC-37 existe en `plans/rfc/` (status `Proposal` o `Accepted`; la vía plan no depende del status de la RFC).
- [ ] Vía de autorización declarada (este plan: `Aprobado para ejecución` + justificación en `**Vía de autorización:**`; registro en `CHANGELOG.md` al ejecutar).
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. `03-gather-context.md` con front matter corregido y nota de H10 en el cuerpo.
2. `H10-kb-discovery-report.md` con YAML sin transición de gate.
3. `PROTOCOL_TAXONOMY.md` sin H10 como gate de transición (catálogo H10, estado `core:GATHERING_CONTEXT` y `workflow:03-gather-context`).

## Pasos

1. Editar el front matter de `03-gather-context.md`: `harness: [H02-context-artifact]`.
2. Agregar en el cuerpo de 03 una sección o nota: "cuando `knowledge_base` está habilitado y se incorporan recomendaciones de KB, el Orchestrator evalúa H10 antes de usarlas".
3. Editar el YAML de H10: `gates: []`, mantener `state: core:GATHERING_CONTEXT` (sin transición asociada) y aclarar en `## Trigger` que H10 no protege transiciones (gate opcional de uso).
4. Actualizar `PROTOCOL_TAXONOMY.md`:
   - catálogo `H10-kb-discovery-report`: `gates: []` (mantener `state: core:GATHERING_CONTEXT` y `artifact_validated: KB_RECOMMENDATION.md`);
   - estado `core:GATHERING_CONTEXT`: `harness: [H02-context-artifact]`;
   - entry `workflow:03-gather-context`: `harness: [H02-context-artifact]`.
5. Verificar `harness/INDEX.md` y `workflow/INDEX.md` para consistencia (H10 como optional; ya lo describen así; sin cambios esperados).
6. Verificar el contrato `KB_RECOMMENDATION.md`: `gated_by = ["H10"]` sigue siendo válido como gate de uso del artefacto (sin cambio).
7. Registrar la vía de autorización en `CHANGELOG.md`.
8. Ejecutar la verificación documental (tools + H13 por juicio).

## Criterios de salida

- [ ] H10 no aparece como gate de transición ni en front matter, ni en el YAML de la policy, ni en `PROTOCOL_TAXONOMY.md`.
- [ ] La policy describe cuándo se invoca.
- [ ] H13 aplicado por juicio: reglas 2 y 10 coherentes entre taxonomía, policy H10 y workflow 03.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda de `H10` en `.agents/` y revisión de cada aparición: esperadas menciones no-gate en `harness/INDEX.md`, `workflow/INDEX.md`, `orchestrator.md`, `AGENT_STATE_MACHINE.md`, `D01-discovery-output.md` y `KB_RECOMMENDATION.md`; ninguna debe declarar una transición protegida.

## Riesgos

- Bajo: cambio documental; el comportamiento opcional no cambia. Requiere tocar `PROTOCOL_TAXONOMY.md` (fuente única según H13); verificar coherencia con H13.

## Trazabilidad

- RFC-37; punto 2.4 de la auditoría; correcciones de la auditoría de planes 34–36 (2026-08-11).
