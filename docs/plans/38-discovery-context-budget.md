# Plan 38 — Configuración de presupuesto y muestreo en discovery

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-39 (`plans/rfc/39-discovery-context-budget.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.6

## Objetivo

Convertir `context_budget` y los límites de muestreo de discovery en configuración real de `features.toml`.

## Criterio de entrada

- [ ] RFC-39 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: apariciones de `context_budget` en roles/workflows de discovery.

## Entregables

1. `features.toml` con `discovery_context_budget` (y `discovery_sample_size_per_language` si se decide mantener el límite por lenguaje).
2. `init_worker.md` con lectura de settings.
3. Roles `stack_worker`, `patterns_worker`, `business_worker`, `framework_worker` sin defaults propios.
4. `discovery_input.json` con los límites materializados.

## Pasos

1. Decidir la semántica del muestreo: tope por grupo (`sample_size`) y tope por lenguaje (opcional).
2. Agregar los settings a `features.toml` con comentario de unidad.
3. Editar `init_worker.md`: leer los settings y escribirlos en `discovery_input.json`.
4. Editar los cuatro workers de muestreo: usar solo los valores del input.
5. Actualizar la sección `Sampling` de `discovery_orchestrator.md` si duplica defaults.
6. Actualizar el backlog B-4 de `plans/INDEX.md` (resolución de F-13).
7. Ejecutar la verificación documental.

## Criterios de salida

- [ ] `features.toml` define ambos límites (o declara la ausencia del de lenguaje).
- [ ] Ningún worker declara defaults de `context_budget` propios.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda de `context_budget` en `.agents/orchestrators/discovery/` y revisión de cada aparición.

## Riesgos

- Bajo: cambio de configuración y referencias; sin cambio de contratos.

## Trazabilidad

- RFC-39; fricción F-13 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-4.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-39 Accepted). Decisión de muestreo: se
mantiene el tope por lenguaje como setting configurable. `features.toml`
gana `discovery_context_budget = 32000` y
`discovery_sample_size_per_language = 50`; `init_worker` los lee y los
escribe en `discovery_input.json`; la sección Sampling del orquestador de
discovery y los cuatro workers de muestro quedan sin defaults propios (verificado: no
quedan literales "per directory/per language"). Cubre el ítem
`discovery_context_budget` del backlog B-4. Versión 3.2.0. Verificación:
invariantes OK, citas OK, estructura OK, 116 passed.
