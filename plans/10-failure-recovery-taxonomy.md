# Plan 10 — Failure & Recovery Taxonomy

**Status:** Aprobado para redacción.

**Depends on:** plan 09 (el routing de decisiones consume esta taxonomía; sin el Decision Model, la clasificación queda huérfana).

**Referencia:** `plans/analisis-explicitud.md` (gap 5); policies H00–H07 y H09–H11 en `orchestrators/core/harness/policies/`, H13 en `harness/policies/`, D00–D01 en `orchestrators/discovery/harness/policies/` y S00 en `orchestrators/system/harness/policies/`; decision trees TOML por trigger; `standards/conduct/ANTI_CIRCUMVENTION.md`.

---

# Objetivo

Definir una **clasificación conceptual de los tipos de fallo** del protocolo y su mapeo a conceptos de routing, de modo que RECOVERY deje de depender de texto libre y de árboles TOML aislados por trigger.

---

# Contenido

## A. RFC — Failure & Recovery Taxonomy

- **Pregunta que responde:** ¿Qué clases de fallo existen conceptualmente y qué destino conceptual tiene cada una?
- **Clases a definir:** blocker, deviation, ambigüedad (clarification-worthy) e inconsistency report (hoy reportadas en texto libre), y harness FAIL (ya estructurado en árboles TOML, pero con su clasificación aislada por trigger). Definir cada clase por su *origen conceptual* y su *destino conceptual* (clarificación, recovery, abort, warning loggeado), no por su trigger.
- **Relación con los TOML decision trees:** los árboles por trigger quedan como *mecanismos* que instancian la taxonomía; la RFC es el modelo que los subsume conceptualmente (misma relación que RFC-00XZ con sus responsabilidades).
- **Audiencia dual de las policies H:** hoy cada checklist mezcla ítems que el runner valida por máquina con ítems que evalúa el agente (p. ej. H04, §Checklist: "The plan is compatible with the existing architecture and conventions"; H07 scope compliance). Introducir el concepto de *ítem machine-evaluated vs. agent-evaluated* y marcarlo explícitamente en cada policy.
- **Criticidad de workers de discovery:** hoy la criticidad está distribuida como regla scope-based en los roles de workers de discovery (`init_worker` y `synthesis_worker` son críticos siempre; `stack_worker`, `framework_worker`, `patterns_worker` y `business_worker` lo son solo cuando el scope coincide — "unless the scope is X"; `environment_worker` siempre es degradable), sin concepto unificado. El insumo que el punto de decisión del plan 09 necesita es otro concepto: la criticidad de la KB para la tarea (`orchestrators/core/roles/orchestrator.md`, §"4.3 Discovery Orchestrator Invocation"). Este plan define si el insumo para esa decisión es la criticidad de la KB por tarea, la de workers por scope, o ambas y cómo se componen.

## B. Aplicación transversal

- Marcar audiencia (máquina/agente) en las policies H00–H07 y H09–H11 (`.agents/orchestrators/core/harness/policies/`), H13 (`.agents/harness/policies/`), D00–D01 (`.agents/orchestrators/discovery/harness/policies/`) y S00 (`.agents/orchestrators/system/harness/policies/`). H08 no existe por diseño (`.agents/harness/INDEX.md`, §"Optional Triggers") ni H12 (liberado: el antiguo H12 pasó a ser D01; `.agents/standards/INDEX.md`, §Runtime), y ambos quedan fuera.
- Actualizar las secciones de reporte de fallo en texto libre para referenciar las clases de la taxonomía. Contratos afectados (criterio: secciones de reporte de fallo en texto libre): `orchestrators/core/contracts/VERIFICATION_REPORT.md` (§"Issues Found"), `contracts/REVIEW_REPORT.md` (§"Critical Failures") y los campos `blockers`/`deviations` del return report de `orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md` (§"Worker Return Report").

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Failure & Recovery Taxonomy | `plans/rfc/` (a partir de `rfc/16`) |
| 2 | Policies marcadas machine/agente | `.agents/orchestrators/core/harness/policies/` (H00–H07, H09–H11), `.agents/harness/policies/` (H13), `.agents/orchestrators/discovery/harness/policies/` (D00–D01), `.agents/orchestrators/system/harness/policies/` (S00) |
| 3 | Updates a contratos de reporte | `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`, `.agents/contracts/REVIEW_REPORT.md`, `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md` |

# Fuera de alcance

- Mecanizar nuevas validaciones en el runner (la RFC es conceptual; nuevas policies de harness serían un plan posterior).
- Modificar los TOML decision trees existentes.
