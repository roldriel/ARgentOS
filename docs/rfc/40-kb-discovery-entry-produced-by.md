# RFC-40 — Procedencia real de las entradas de discovery

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.7
**Pregunta:** ¿Qué estados producen las entradas de la KB de discovery?
**Afectados:** `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`, `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`.

## Problema

El contrato `KB_DISCOVERY_ENTRY.md` declara en su metadata `produced_by: [discovery:DISCOVERY_INIT]` (`.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:KB Discovery Entry Contract`), pero la máquina de estados asigna la producción de entradas a los estados de worker: `DISCOVERY_ENV` produce `environment.md`, `DISCOVERY_STACK` produce `stack.md`, `dependencies.md`, etc., `DISCOVERY_FRAMEWORK` produce `architecture.md`, etc., y `DISCOVERY_MERGE` consolida (`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:States`). `DISCOVERY_INIT` produce el reporte, los JSON de entrada y `file_map.md`.

Consecuencia: la metadata de procedencia del contrato contradice la máquina de estados; la trazabilidad (`produced_by`) de todas las entradas apuntaría al estado equivocado.

## Decisión propuesta

1. `produced_by` del contrato pasa a la lista de estados productores: `[discovery:DISCOVERY_ENV, discovery:DISCOVERY_STACK, discovery:DISCOVERY_FRAMEWORK, discovery:DISCOVERY_PATTERNS, discovery:DISCOVERY_BUSINESS, discovery:DISCOVERY_MERGE]`.
2. `DISCOVERY_INIT` se documenta como productor exclusivo de `file_map.md` (y del reporte `KB_DISCOVERY_REPORT.md`), no de las entradas generales.
3. La taxonomía (`PROTOCOL_TAXONOMY.md`) se alinea si su entidad del contrato repite `produced_by`.

## Alternativas consideradas

- **Declarar `produced_by: [discovery:DISCOVERY_INIT]` como "iniciador"**: la metadata del contrato no distingue iniciador de productor; genera la misma confusión.
- **No declarar procedencia**: degrada la trazabilidad que D01 exige.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `KB_DISCOVERY_ENTRY.md` | Metadata `produced_by` corregida. |
| `PROTOCOL_TAXONOMY.md` | Entidad del contrato alineada si aplica. |

## Criterios de aceptación

- [ ] `produced_by` coincide con los estados que producen entradas en la máquina de estados.
- [ ] `DISCOVERY_INIT` no aparece como productor de entradas generales.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.7 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |
