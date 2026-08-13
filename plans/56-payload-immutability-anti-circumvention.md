# Plan 56 — Regla de inmutabilidad del payload en ANTI_CIRCUMVENTION

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-12
**RFC:** — (vía plan, ver justificación)
**Depende de:** —
**Origen:** Auditoría de documentación (2026-08-12), `docs/AUDITORIA_DOCUMENTACION.md` §Cabos sueltos (punto 1); pendiente registrado en `plans/INDEX.md` (plan 41, RFC-42: "pendiente la referencia en `ANTI_CIRCUMVENTION.md`").

**Justificación de la vía plan:** regularización documental de una regla de
gobernanza ya vigente (RFC-42, planes 34–36 y 41); el cambio es una sola
sección declarativa sin modelo conceptual nuevo. Autorización explícita del
usuario del 12 ago 2026.

## Objetivo

Que `protocol/.agents/standards/conduct/ANTI_CIRCUMVENTION.md` declare, de
forma autocontenida, la regla de inmutabilidad del payload: el contenido de
`.agents/` solo cambia con una versión nueva publicada del protocolo; ninguna
edición fuera de ese cauce es válida, y proponerla cuenta como circunvention.

Restricción de frontera documental (`plans/INDEX.md` §Convenciones): la regla
se define **inline**, sin referenciar RFCs, planes ni documentos del repo.

## Criterio de entrada

- [ ] Verificación contra el repo de `protocol/.agents/standards/conduct/ANTI_CIRCUMVENTION.md` (secciones actuales: Purpose, Rule, What counts as circumvention, Enforcement, Relationship to other standards).
- [ ] Batería en verde antes de tocar el payload.

## Entregables

1. `ANTI_CIRCUMVENTION.md` con la regla de inmutabilidad del payload integrada: un ítem en "What counts as circumvention" (editar `.agents/` fuera del cauce de versiones publicadas del protocolo) y su consecuencia en "Enforcement" (tratarlo como desviación de protocolo).
2. `CHANGELOG.md` con sección `## [3.0.7]` e ítem `(plan 56)`.
3. `protocol/.agents/VERSION` bumped a `3.0.7`.
4. Este plan con `Nota de ejecución` y `plans/INDEX.md` actualizado (incluido el cierre del pendiente del plan 41) en el mismo commit.

## Pasos

1. Redactar la regla inline en "What counts as circumvention": modificar el contenido de `.agents/` por fuera del cauce de releases del protocolo (la versión publicada es la unidad de cambio válida).
2. Agregar en "Enforcement" la consecuencia: toda edición fuera de cauce se trata como desviación (artefactos marcados, `RECOVERY`).
3. Revisar "Relationship to other standards" por si la regla nueva merece una línea allí; sin referencias externas.
4. Bump de versión + changelog + estados.
5. Correr la batería completa.

## Criterios de salida

- [ ] La regla está escrita inline, sin mencionar RFC-42, planes ni `plans/`.
- [ ] `plans/INDEX.md` registra el cierre del pendiente del plan 41.
- [ ] Checkers y tests en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
```

## Nota de ejecución

<!-- Se completa al ejecutar. -->
