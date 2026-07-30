# Plan 10 — Failure & Recovery Taxonomy

**Status:** Aprobado para redacción.

**Depends on:** plan 09 (el routing de decisiones consume esta taxonomía; sin el Decision Model, la clasificación queda huérfana).

**Referencia:** análisis de explicitud (gap 5); policies `harness/policies/H*.md`; decision trees TOML por trigger; `standards/conduct/ANTI_CIRCUMVENTION.md`.

---

# Objetivo

Definir una **clasificación conceptual de los tipos de fallo** del protocolo y su mapeo a conceptos de routing, de modo que RECOVERY deje de depender de texto libre y de árboles TOML aislados por trigger.

---

# Contenido

## A. RFC — Failure & Recovery Taxonomy

- **Pregunta que responde:** ¿Qué clases de fallo existen conceptualmente y qué destino conceptual tiene cada una?
- **Clases a definir** (hoy reportadas en texto libre): blocker, deviation, harness FAIL, ambigüedad (clarification-worthy), inconsistency report. Definir cada clase por su *origen conceptual* y su *destino conceptual* (clarificación, recovery, abort, warning loggeado), no por su trigger.
- **Relación con los TOML decision trees:** los árboles por trigger quedan como *mecanismos* que instancian la taxonomía; la RFC es el modelo que los subsume conceptualmente (misma relación que RFC-00XZ con sus responsabilidades).
- **Audiencia dual de las policies H:** hoy cada checklist mezcla ítems que el runner valida por máquina con ítems que evalúa el agente (p. ej. H04 ítem 10 "compatible con la arquitectura existente"; H07 scope compliance). Introducir el concepto de *ítem machine-evaluated vs. agent-evaluated* y marcarlo explícitamente en cada policy.
- **Criticidad de workers de discovery:** definir qué hace a un worker "crítico" para degradación parcial (hoy no está listado en ningún lado); alimenta el punto de decisión de criticidad del plan 09.

## B. Aplicación transversal

- Marcar audiencia (máquina/agente) en las policies H01–H13, D00–D01, S00.
- Actualizar las secciones de reporte de los contratos afectados para referenciar las clases de la taxonomía en lugar de texto libre.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Failure & Recovery Taxonomy | `plans/rfc/` (número libre) |
| 2 | Policies marcadas machine/agente | `.agents/harness/policies/` |
| 3 | Updates a contratos de reporte | `.agents/orchestrators/core/contracts/` |

# Fuera de alcance

- Mecanizar nuevas validaciones en el runner (la RFC es conceptual; nuevas policies de harness serían un plan posterior).
- Modificar los TOML decision trees existentes.
