# Plan 41 — Gobernanza de status entre RFCs y planes

**Status:** Executed (parcial cerrado el 2026-08-12: RFC-42 `Accepted` en la revisión RFC-56 y referencia en `ANTI_CIRCUMVENTION.md` agregada por el plan 56, 3.0.7)
**Fecha:** 2026-08-11
**RFC:** RFC-42 (`plans/rfc/42-rfc-plan-status-governance.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.9

**Nota de ejecución (2026-08-11):** aplicada la regularización de las RFC-24…28
(`Proposal` → `Accepted` retroactivo, con evidencia) y la regla de gobernanza en
`plans/INDEX.md` (vía RFC Accepted / vía plan Aprobado para ejecución), por
decisión del usuario. Queda pendiente, condicionada a la aceptación de RFC-42,
la referencia en `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

## Objetivo

Definir y documentar las vías de autorización para modificar `.agents/` y regularizar el desfase RFC-24-28 vs planes 23-27.

## Criterio de entrada

- [ ] RFC-42 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: status actuales en `plans/INDEX.md`.

## Entregables

1. Regla de gobernanza en `plans/INDEX.md` (vía RFC Accepted / vía plan Aprobado para ejecución).
2. Regularización del backlog 23-28 (accepted retroactivo o `Executed (parcial: ...)`).
3. Referencia en `ANTI_CIRCUMVENTION.md`.

## Pasos

1. Redactar la regla en `plans/INDEX.md:Convenciones` (dos vías + registro en `CHANGELOG.md`).
2. Auditar los planes 23-27 y sus RFCs 24-28: verificar actas de aprobación en los propios documentos.
3. Aplicar la regularización elegida: marcar RFCs como `Accepted` con evidencia, o marcar los planes como `Executed (parcial: gobernanza pendiente)`.
4. Agregar la referencia cruzada en `ANTI_CIRCUMVENTION.md`.
5. Ejecutar la verificación documental.

## Criterios de salida

- [ ] `plans/INDEX.md` describe las dos vías y el estado regularizado.
- [ ] Ningún plan futuro puede ejecutarse sin vía de autorización declarada.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de consistencia entre status de RFCs y planes (skill `consistency-checker`).

## Riesgos

- Medio: decisión de gobernanza; requiere acuerdo del usuario sobre la regularización (retroactiva vs pendiente).

## Trazabilidad

- RFC-42; punto 2.9 de la auditoría.
