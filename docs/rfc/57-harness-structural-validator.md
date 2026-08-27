# RFC-57 — Validador estructural opcional del harness (F1-B/C)

**Status:** Accepted
**Fecha:** 2026-08-15
**Serie:** Remediación de la auditoría de sistema
**Origen:** `AUDITORIA_SISTEMA.md` F1 (opción C, decisión del usuario 2026-08-15)

## Problema

El modelo de enforcement declarado (F1-A, plan 64) deja los ítems `[gate]`
como "estructuralmente checkables" evaluados por juicio del Orchestrator. En
el producto no hay soporte mecánico para los ítems estructurales (existencia,
secciones normativas, bloques TOML y enums, resolución de citas, EARS,
presencia estructural de rubricas), más allá de los checkers dev-only del repo
de desarrollo.

## Decisión propuesta

Añadir al payload un validador estructural **opcional** de stdlib pura
(`.agents/harness/gate_validator.py`) que implementa el subconjunto
mecánicamente checkable de las checklists `[gate]`. El juicio del Orchestrator
sigue siendo el árbitro del gate; el validador es soporte mecánico opcional,
fail-open, cuyos resultados se registran como evidencia en
`HARNESS_REPORT.md`. No cambia la semántica de los gates ni el modo
declarativo.

## Alcance

- Triggers soportados (subconjunto estructural): H00–H07, H09–H11 y D00.
- Checks: existencia del artefacto; secciones normativas del contrato; bloques
  TOML machine-readable con enums (H05/H06/H07/H01); resolución de citas
  (`path:section`, `path` §section, campos TOML de citas); patrón EARS de los
  bullets de criterios (H01); presencia estructural de `## Rubric Evaluation`
  (H06, cuando el flag `rubrics` está habilitado).

## Reglas de borde

- El validador nunca bloquea: su salida es evidencia, no gate.
- El modo declarativo sigue sin requerir Python para adoptantes; el validador
  es opcional.
- Los ítems `[agent]` no los cubre el validador.
- D01 (ground truth de KB) y S00 (sonda) no los cubre este validador: D01
  requiere juicio y S00 ya es mecánico por `health_check.py`.

## Criterios de aceptación

- [ ] `gate_validator.py` en `.agents/harness/`, stdlib pura.
- [ ] Triggers soportados: H00–H07, H09–H11 y D00.
- [ ] Tests del harness para los checks.
- [ ] `Enforcement model` y documentación actualizados (PYTHON_DEPENDENCIES,
      ADOPTION).

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-15 | Creación. Aceptada por decisión del usuario (opción C). | `AUDITORIA_SISTEMA.md` F1 |
