# Plan 57 — Implementación de las clases de gobernanza (RFC-56)

**Status:** Executed
**Fecha:** 2026-08-12
**RFC:** RFC-56 (`plans/rfc/56-governance-fast-track.md`)
**Depende de:** —
**Origen:** RFC-56 §Criterios de aceptación.

**Justificación de la vía:** los entregables 1–4 tocan solo documentación del
repo (no el payload) — no requieren RFC propia. El entregable 5 (revisión de
la serie Proposal) es la aplicación de RFC-56 `Accepted`.

## Objetivo

Dejar vigente el modelo de clases A/B/C de RFC-56 en las fuentes de verdad
del repo y ejecutar la revisión individual de las RFC-32…54.

## Criterio de entrada

- [ ] RFC-56 `Accepted`.
- [ ] Batería en verde.

## Entregables

1. `plans/INDEX.md` §Convenciones: bullet de Inmutabilidad reescrito en
   términos de clases A/B/C con las reglas de borde de la RFC.
2. `docs/VERSIONING.md` §7 (y §4 si aplica): el flujo referencia las clases.
3. `AGENTS.md` raíz: Task lifecycle menciona las clases.
4. `plans/_TEMPLATE.md`: campo `Clase:` en el header para planes que tocan el
   payload.
5. Revisión individual de RFC-32…54: veredicto por RFC (Accepted / descartada
   / pendiente con causa) registrado en su Amendment Log; estados en
   `plans/INDEX.md`; ítem de changelog por cada grupo coherente cerrado.

## Pasos

1. Reescribir los bullets de `plans/INDEX.md` §Convenciones (Inmutabilidad y
   ciclo de status) con las clases.
2. Alinear `docs/VERSIONING.md` y `AGENTS.md`.
3. Agregar el campo `Clase` al template de plan.
4. Ejecutar la revisión de la serie Proposal en grupos coherentes (por serie
   temática), una RFC a la vez, registrando cada veredicto.
5. Batería completa al cierre de cada grupo.

## Criterios de salida

- [ ] Las tres clases legibles desde `plans/INDEX.md` §Convenciones.
- [ ] Ninguna RFC de la serie 32…54 queda en `Proposal` sin veredicto
      registrado.
- [ ] Checkers y tests en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
```

## Riesgos

La revisión de 23 RFCs es larga; se hace por grupos para que cada cierre sea
commiteable y verde por sí mismo.

## Nota de ejecución

Ejecutado el 2026-08-12. Entregables 1–4: clases A/B/C vigentes en
`plans/INDEX.md` §Convenciones (Inmutabilidad), `docs/VERSIONING.md` §4/§7,
`AGENTS.md` raíz (Task lifecycle + Do NOT) y campo `Clase` en
`plans/_TEMPLATE.md`. Entregable 5: las 23 RFCs de la serie (32…54) revisadas
individualmente en cuatro grupos; veredicto unánime `Accepted` con evidencia
registrada en cada Amendment Log, espejo en `plans/INDEX.md` y registro en
`CHANGELOG.md` [Unreleased] §Modelo conceptual. Ninguna queda en `Proposal`.
Verificación por grupo y final: citas OK, estructura OK, 116 passed.
