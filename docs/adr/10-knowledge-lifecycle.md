# ADR-10 — Knowledge Lifecycle (D9)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D9 (2026-08-25; provisional en el modelo, formalizada por RFC-67)
**RFC:** [RFC-67](docs/rfc/67-knowledge-lifecycle-model.md) (`Accepted`, plan 81)
**Plan:** [plan 81](docs/plans/81-knowledge-lifecycle-model.md) (`Executed`)
**Clase de cambio:** MAJOR (contratos y pipeline de discovery; RFC-56)
**Problemas que resuelve:** P5, P12, P13, P14 (CG-04)

## Contexto

CG-04 agrupa P5 (KB stale post-ejecución), P12 (identidad de entradas ambigua), P13
(sin aprendizaje de sesión) y P14 (costo de discovery). Sin transiciones formales,
la KB es un snapshot sin ciclo
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`). El
pipeline de discovery y sus TTL/hashes ya existen; 3.26.0 agregó el cierre "What we
learned".

## Alternativas consideradas

### A — Knowledge como snapshot inmutable

Estado actual. Cero cambios, pero reproduce P5/P13.

### B — Lifecycle mínimo con tres tipos y transiciones explícitas

`snapshot` (entradas de discovery con TTL + hashes), `claim` (unidad dentro de una
entrada; frescura por claim), `lesson` (aprendizaje de sesión con proveniencia).
Invalidación post-ejecución vía `invalidated_facts` en EXECUTION_SUMMARY; identidad
con `kind` + `path` en KB_RECOMMENDATION.

### C — Motor de conocimiento completo

Claims con confianza y derivación. Rigor total, pero fuera del objetivo.

## Decisión

**Opción B.** Lifecycle mínimo: `snapshot` / `claim` / `lesson`, invalidación
post-ejecución vía `invalidated_facts`, reutilización por claim fresco con
proveniencia resoluble e identidad con `kind`+`path`. Las lessons son claims con
proveniencia, reutilizables bajo las mismas reglas de frescura
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D9`).

## Consecuencias

- El executor declara qué hechos descubiertos cambió; el pipeline revalida solo esas
  entradas (reduce el costo de P14).
- Las recomendaciones de KB resuelven su ubicación.
- El cierre "What we learned" persiste lessons con evidencia.

## Invariantes

- KN-1: toda entrada de discovery es `snapshot` con TTL y hashes.
- KN-2: toda `lesson` tiene `session_id`, `protocol_version` y referencia de
  evidencia.
- KN-3: una claim fresca requiere proveniencia resoluble.
- KN-4: toda ejecución que cambia hechos descubiertos declara `invalidated_facts`.

## Relaciones

- Depende de: D6 (los eventos de ejecución alimentan `invalidated_facts`; ADR-07).
- Formalizada en: RFC-67 (`docs/rfc/67-knowledge-lifecycle-model.md:Decision`),
  plan 81.

## Estado de implementación

El modelo la marcó `PROVISIONALLY_DECIDED`; RFC-67 `Accepted` (plan 81 `Executed`,
2026-08-25) la formalizó y payload 9.0.0 la implementó (KNOWLEDGE_LIFECYCLE,
`kind`/`path` en KB_RECOMMENDATION, `invalidated_facts` en EXECUTION_SUMMARY, checks
en `gate_validator.py` y `check_session_artifacts.py`).
