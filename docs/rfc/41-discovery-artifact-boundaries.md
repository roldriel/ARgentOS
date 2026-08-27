# RFC-41 — Fronteras de artefactos de discovery y namespacing de `<order>`

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.8 (y 5.2)
**Pregunta:** ¿Dónde viven los artefactos intermedios de discovery y cómo se numeran los artefactos de sesión sin colisionar entre dominios?
**Afectados:** `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`, `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`.

## Problema

La regla general de artefactos exige que los artefactos de sesión vivan dentro de `.project/<session-uuid>/<iteration>/` con `<order>` auditable (`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`). El subsistema de discovery escribe intermedios en `.project/<session-uuid>/discovery/` (`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_INIT`), sin que el documento canónico de fronteras registre esa excepción.

Además, los artefactos de sesión de discovery comparten la secuencia `<order>` de la iteración core: el dogfooding produjo `01-KB_DISCOVERY_REPORT.md` junto a `01-TASK_ANALYSIS.md` y `02-KB_DISCOVERY_ENTRY.md` junto a `02-TASK_ANALYSIS.md` (`plans/19-anexo-a-bitacora-fricciones.md:F-20`). La regla exige que `<order>` refleje el orden real de generación y sea auditable contra `SESSION_LOG.md`; dos dominios numerando el mismo espacio rompen esa garantía. El artefacto-puente `02-KB_DISCOVERY_ENTRY.md` (índice de validación) fue un workaround para un runner que ya no existe (`plans/19-anexo-a-bitacora-fricciones.md:F-11`).

## Decisión propuesta

1. **Frontera explícita en `PROTOCOL_BOUNDARIES.md`**: los intermedios de discovery (JSON de workers, `discovery_input.json`, `invalidation_report.json`) viven en `.project/<session-uuid>/discovery/`, como excepción documentada de la regla de artefactos; no se numeran con `<order>`.
2. **Namespacing por dominio del `<order>`**: los artefactos de sesión del dominio `discovery` que sí viven en la iteración usan prefijo de dominio: `D<order>-ARTIFACT.md` (por ejemplo `D01-KB_DISCOVERY_REPORT.md`); los del dominio `core` mantienen `<order>` plano. La regla de `<order>` se actualiza para exigir unicidad por dominio.
3. **D01 valida las entradas en `.project/knowledge/discovery/` directamente** (juicio del agente, sin artefacto-puente en la iteración), eliminando la necesidad de `02-KB_DISCOVERY_ENTRY.md`.
4. Las trazas históricas (iteración `00` de la sesión `d4ab6a93-...`) se conservan sin reescribir; la regla aplica a ejecuciones futuras.

## Alternativas consideradas

- **Mover los intermedios a la iteración**: contamina la secuencia core y mezcla dominios; se descarta.
- **Subcarpeta `discovery/` dentro de la iteración**: válida, pero el mecanismo actual ya usa `.project/<session>/discovery/`; se prefiere documentar lo existente.
- **Seguir con el artefacto-puente**: perpetúa un workaround para un runner eliminado.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `PROTOCOL_BOUNDARIES.md` | Excepción de discovery + regla de namespacing por dominio. |
| `DISCOVERY_STATE_MACHINE.md` | Outputs con prefijo `D<order>` donde corresponda. |
| `D01-discovery-output.md` | Validación directa en `knowledge/discovery/`, sin puente. |

## Criterios de aceptación

- [ ] Ningún artefacto de la iteración core comparte `<order>` con un artefacto de discovery.
- [ ] La excepción de `.project/<session>/discovery/` está documentada en el doc canónico de fronteras.
- [ ] D01 no requiere artefactos puente en la iteración.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, puntos 2.8 / 5.2; F-11, F-20 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |
