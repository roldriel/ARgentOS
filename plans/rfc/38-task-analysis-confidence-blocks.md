# RFC-38 — Bloques de confianza en TASK_ANALYSIS

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.5
**Pregunta:** ¿Qué significa cada bloque de confianza del análisis de tarea y cuál es el canónico?
**Afectados:** `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`, `.agents/orchestrators/core/harness/policies/H00-task-analysis.md`.

## Problema

El contrato `TASK_ANALYSIS.md` define dos bloques de confianza superpuestos:

- `[intent_confidence]` con `level`, `score`, `applied_criteria` y `explanation` (`.agents/orchestrators/core/contracts/TASK_ANALYSIS.md:Intent Confidence Assessment`).
- `[confidence]` con `level` y `explanation` (`.agents/orchestrators/core/contracts/TASK_ANALYSIS.md:Confidence`).

Los criterios de completitud dicen "se provee un nivel de confianza" sin aclarar cuál de los dos (`.agents/orchestrators/core/contracts/TASK_ANALYSIS.md:Completion Criteria`), y H00 verifica ambos por separado (`.agents/orchestrators/core/harness/policies/H00-task-analysis.md:Checklist`). El estándar `INTENT_CONFIDENCE.md` define el modelo de puntaje para la interpretación de intención (`.agents/standards/requirements/INTENT_CONFIDENCE.md:Scoring model`), que corresponde a `intent_confidence`; el segundo bloque no tiene definición.

## Decisión propuesta

1. `intent_confidence` es el bloque canónico de la confianza en la interpretación de intención, alimentado por `INTENT_CONFIDENCE.md`.
2. El bloque `[confidence]` se elimina o se redefine explícitamente como *confianza del análisis* (calidad de la evidencia del propio análisis), con criterios definidos; no puede coexistir sin definición.
3. Los criterios de completitud nombran explícitamente `intent_confidence` (y `confidence` solo si se redefine).
4. H00 se alinea: los ítems 12 y 17-20 referencian `intent_confidence`; si `confidence` se mantiene, se define su semántica.

## Alternativas consideradas

- **Mantener ambos sin definición**: la opción actual; fuente de confusión para el `task_analyst` y el orquestador.
- **Fundir ambos en uno**: pierde la distinción entre confianza de intención y confianza del análisis, que el contrato sugiere.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `TASK_ANALYSIS.md` | Semántica canónica de los bloques; criterios de completitud explícitos. |
| `H00-task-analysis.md` | Checklist alineado con el bloque canónico. |

## Criterios de aceptación

- [ ] Cada bloque de confianza del contrato tiene una semántica definida.
- [ ] Los criterios de completitud no son ambiguos sobre qué bloque se exige.
- [ ] H00 verifica el bloque canónico sin duplicar semánticas.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.5 |
