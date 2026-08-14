# Plan 39 — Procedencia real de las entradas de discovery

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-40 (`plans/rfc/40-kb-discovery-entry-produced-by.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.7

## Objetivo

Corregir la metadata de procedencia del contrato `KB_DISCOVERY_ENTRY.md` para que coincida con la máquina de estados.

## Criterio de entrada

- [ ] RFC-40 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: `produced_by` del contrato y estados productores en la máquina de estados.

## Entregables

1. `KB_DISCOVERY_ENTRY.md` con `produced_by` corregido.
2. `PROTOCOL_TAXONOMY.md` alineado.

## Pasos

1. Editar el bloque YAML de `KB_DISCOVERY_ENTRY.md`: lista de estados productores.
2. Verificar la sección `States` de `DISCOVERY_STATE_MACHINE.md` y copiar los estados exactos.
3. Buscar la entidad del contrato en `PROTOCOL_TAXONOMY.md` y alinear `produced_by`.
4. Ejecutar la verificación documental.

## Criterios de salida

- [ ] `produced_by` del contrato == estados productores de la máquina de estados.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Comparación metadata ↔ state machine (skill `consistency-checker`).

## Riesgos

- Bajo: metadata documental; sin cambio de comportamiento.

## Trazabilidad

- RFC-40; punto 2.7 de la auditoría.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-40 Accepted). `produced_by` del contrato
`KB_DISCOVERY_ENTRY.md` y de la entidad en `PROTOCOL_TAXONOMY.md` alineados a
los estados productores de `DISCOVERY_STATE_MACHINE.md` (ENV, STACK,
FRAMEWORK, PATTERNS, BUSINESS, MERGE). Versión 3.2.1. Verificación:
invariantes OK, citas OK, estructura OK, 116 passed.
