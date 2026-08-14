# RFC-54 — Redacción de contratos de discovery (F-15 y F-19)

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.4
**Pregunta:** ¿Cómo se redactan sin ambigüedad la declaración de `project_shape` del executive summary y el cálculo de hashes de discovery?
**Afectados:** `.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md`, `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`, `.agents/orchestrators/discovery/roles/workers/init_worker.md`, `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`.

## Problema

Dos ambigüedades de redacción en discovery:

1. El contrato `EXECUTIVE_SUMMARY.md` exige que la "primera línea" declare `project_shape` (`.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md:Required sections`), pero la primera línea literal del archivo es el front matter TOML (`+++`), y D01 ítem 9 repite la exigencia (`.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist`). La implementación actual puso el shape como primera línea de contenido, una interpretación ad hoc (`plans/19-anexo-a-bitacora-fricciones.md:F-15`).
2. La sección `Hash Calculation` de la máquina de discovery dice que el core Orchestrator calcula los hashes antes de invocar (`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`), mientras `init_worker` los calcula como parte de su tarea (`.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks`). El dogfooding los calculó en `init_worker` (`plans/19-anexo-a-bitacora-fricciones.md:F-19`).

## Decisión propuesta

1. **`project_shape`**: declarar el shape en una sección explícita `## Project Shape` (primera sección de contenido, después del front matter), y alinear el contrato, D01 ítem 9 y la plantilla. Eliminar el requisito de "primera línea" literal.
2. **Hashes**: actor único = `init_worker` (los calcula y los registra en `discovery_input.json` y en el manifest). La máquina de discovery elimina o anota la atribución al core Orchestrator; el core solo solicita el scope y recibe el resultado.

## Alternativas consideradas

- **Mantener "primera línea" interpretada como primera línea de contenido**: ambigua; se reemplaza por sección explícita.
- **Dejar el cálculo en el core Orchestrator**: duplica el trabajo y contradice la práctica verificada.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `EXECUTIVE_SUMMARY.md` | Sección `## Project Shape`. |
| `D01-discovery-output.md` | Ítem 9 alineado. |
| `DISCOVERY_STATE_MACHINE.md` | Hash Calculation con actor único. |
| `init_worker.md` | Confirmación del actor único. |

## Criterios de aceptación

- [ ] El contrato no exige una "primera línea" literal.
- [ ] Un único actor calcula los hashes.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 6.4; F-15, F-19 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |
