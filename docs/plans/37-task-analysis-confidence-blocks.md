# Plan 37 — Bloques de confianza en TASK_ANALYSIS

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-38 (`plans/rfc/38-task-analysis-confidence-blocks.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.5

## Objetivo

Definir la semántica de los bloques de confianza de `TASK_ANALYSIS.md` y alinear H00.

## Criterio de entrada

- [ ] RFC-38 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. Contrato `TASK_ANALYSIS.md` con semántica canónica y criterios de completitud explícitos.
2. Policy H00 alineada.

## Pasos

1. Decidir y documentar la semántica: `intent_confidence` canónico; `confidence` redefinido como confianza del análisis o eliminado.
2. Editar el contrato: secciones, ejemplos y criterios de completitud.
3. Editar H00: ítems 12, 17-20 para referenciar el bloque canónico.
4. Verificar `INTENT_CONFIDENCE.md` y `CONFIDENCE.md` como fuentes de cada bloque.
5. Ejecutar la verificación documental.

## Criterios de salida

- [ ] No hay bloques de confianza sin semántica definida en el contrato.
- [ ] H00 y contrato concuerdan.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Consistencia contrato ↔ H00 ↔ `INTENT_CONFIDENCE.md` (skill `consistency-checker`).

## Riesgos

- Medio si se redefine `confidence`: cambio de contrato MAJOR; registrar en `CHANGELOG.md`.
- Bajo si solo se documenta la semántica existente.

## Trazabilidad

- RFC-38; punto 2.5 de la auditoría.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-38 Accepted). Decisión aplicada: opción 2
de la RFC — `[confidence]` redefinido como confianza del análisis (gobernado
por `CONFIDENCE.md`), `intent_confidence` canónico de la interpretación de
intención. Contrato `TASK_ANALYSIS.md` (sección + criterios de completitud
nombrando ambos bloques) y policy H00 ítem 12 alineados. Versión 3.1.0
(MINOR: clarificación compatible, sin eliminación de bloques). Verificación:
invariantes OK, citas OK, estructura OK, 116 passed.
