# RFC-58 — Validador estructural obligatorio en los gates (F1-B)

**Status:** Accepted
**Fecha:** 2026-08-15
**Serie:** Remediación de la auditoría de sistema
**Origen:** `AUDITORIA_SISTEMA.md` F1 (opción B, decisión del usuario 2026-08-15)

## Problema

RFC-57 dejó el validador estructural como opcional (`MAY`). Los ítems `[gate]`
siguen dependiendo de que el Orchestrator decida invocarlo; un FAIL estructural
no bloquea el PASS por defecto.

## Decisión propuesta

Para los triggers soportados (H00–H07, H09–H11, D00), el Orchestrator **debe**
invocar `gate_validator.py` antes de juzgar PASS; un FAIL estructural bloquea
el PASS salvo desviación documentada (override por juicio registrado en
`HARNESS_REPORT.md`/`SESSION_LOG.md`). El validador no se invoca desde los
hooks (no bloquea a nivel de entorno); el enforcement es a nivel de gate
(proceso). Los ítems `[agent]` siguen siendo juicio puro.

## Reglas de borde

- FAIL estructural → gate FAIL; el override requiere desviación documentada.
- Los hooks no invocan el validador (fail-open intacto).
- D01 y S00 no cubiertos (ver RFC-57).
- El modo declarativo no cambia: el validador es stdlib opcional de entorno.

## Criterios de aceptación

- [ ] Policies H00–H07, H09–H11 y D00: MUST invocar `gate_validator.py`
      antes del PASS.
- [ ] `Enforcement model` actualizado (layer 2: obligatorio para triggers
      soportados).
- [ ] Docstring de `gate_validator.py` actualizado.
- [ ] Batería en verde (incluye tests del harness).

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-15 | Creación. Aceptada por decisión del usuario (opción B). | `AUDITORIA_SISTEMA.md` F1 |
