# Plan 60 — Remediación Nivel 6 (lote fácil: clarificaciones documentales y contrato de hooks)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (mejoras documentales compatibles; sin cambio de significado)
**Depende de:** —
**Origen:** `AUDITORIA_SISTEMA.md` (lote fácil, ítems 1–5; contradicciones §18.6 y §18.8)

## Objetivo

Cerrar cinco clarificaciones documentales del payload y la convención de
changelog, sin cambiar el modelo:

1. Excepción de la política single-source (el restatement de inmutabilidad en
   `ANTI_CIRCUMVENTION.md` es la única duplicación sancionada).
2. Convención de `[Unreleased]` en el changelog (siempre arriba) y semántica
   de las secciones con fecha sin tag en `dev`.
3. Contrato de esquema de eventos de hook (enforced mode).
4. Modelo D01: hoy no hay runner ejecutable en el harness; la validación
   mecánica es una extensión futura posible, no parte del payload.
5. Semántica de `retry_count`: derivada de las entradas `FAIL` del
   `HARNESS_REPORT.md` por trigger e iteración.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `PROTOCOL_BOUNDARIES.md` declara la excepción de la política
   single-source.
2. `CHANGELOG.md`: `[Unreleased]` arriba + sección `[3.11.0]`;
   `docs/VERSIONING.md` §5 documenta la convención.
3. `harness/INDEX.md`: sección "Hook event schema (enforced mode)" +
   semántica de `retry_count` en Recovery Mechanism.
4. `.agents/orchestrators/core/roles/orchestrator.md` §6: derivación de
   `retry_count`.
5. `D01-discovery-output.md`: Implementation Note alineado con el modelo
   actual (sin runner ejecutable).
6. `protocol/.agents/VERSION` = `3.11.0`; registro en `plans/INDEX.md`.

## Pasos

1. Editar `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (sección
   `## Single-source documentation policy`): declarar la excepción aprobada.
2. Editar `CHANGELOG.md`: mover `[Unreleased]` a la cima y agregar
   `[3.11.0]` con los ítems `(plan 60)`.
3. Editar `docs/VERSIONING.md` (§5): convención de `[Unreleased]` y de
   secciones sin tag en `dev`.
4. Editar `.agents/harness/INDEX.md`: contrato de evento de hook y semántica
   de `retry_count`.
5. Editar `.agents/orchestrators/core/roles/orchestrator.md` (§6):
   derivación de `retry_count` desde `HARNESS_REPORT.md`.
6. Editar `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`
   (`## Implementation Note`): modelo sin runner ejecutable hoy.
7. Bump de versión `3.11.0`, changelog y registro en INDEX.

## Criterios de salida

- [ ] La política single-source declara su excepción.
- [ ] El changelog respeta Keep a Changelog (`[Unreleased]` arriba) y la
      convención `dev` queda documentada.
- [ ] El esquema del evento de hook queda especificado en el payload.
- [ ] D01 y `harness/INDEX.md` no se contradicen sobre el runner.
- [ ] `retry_count` tiene semántica definida y verificable.
- [ ] Batería canónica en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

## Riesgos

- Bajo: clarificaciones documentales; sin cambio de modelo ni de contratos.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` lote fácil (ítems 1–5) y contradicciones §18.6/§18.8.

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.11.0` (MINOR: adiciones documentales
compatibles). Verificación: invariantes OK, citas OK, estructura OK, taxonomía
OK, tests OK; `check_dist_sync` rojo en `dev` por diseño. La herramienta de
agregación de métricas (ítem 6 del lote) vive en `tools/` y no requiere plan.
