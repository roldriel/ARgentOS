# Roadmap

Este documento cataloga los pendientes priorizados del proyecto y sus
prioridades. No implementa nada: cada entrada cita su origen en
`plans/INDEX.md` o en los planes/RFCs. Los ítems que toquen
`protocol/.agents/` requieren su propio RFC/plan antes de ejecutarse.

## Pendientes priorizados (origen: `plans/INDEX.md`)

| Prioridad | Ítem | Origen | Cubierto por |
| --- | --- | --- | --- |
| Alta | Gate D01 superable (artefacto-puente de discovery) | Backlog B-1 | planes 40 (`plans/40-discovery-artifact-boundaries.md`) y 47 (`plans/47-discovery-per-entry-contracts.md`) |
| Alta | Recovery económico para fallos de formato (parcialmente cubierto por plan 29) | Backlog B-2, plan 33 | planes 29 (`plans/29-recovery-to-early-phases.md`) y 33 (`plans/33-ears-criteria-canonical-form.md`) |
| Media | Marcador `.last_discovery` canónico + validación en health-check | Backlog B-3, plan 50 | plan 50 (`plans/50-discovery-kb-freshness.md`) |
| Media | Tanda de inconsistencias de contratos/policies | Backlog B-4 | planes 37–43 y 53 (`plans/`, numeración correlativa) |
| Media | Política de clarificación desatendida | Backlog B-5, plan 44 | plan 44 (`plans/44-unattended-clarification.md`) |
| Media | Subcomandos del runner para H15 | Backlog B-6 | plan 46 (`plans/46-enforced-mode-dogfooding.md`) |
| Baja | Enmiendas conceptuales (recovery temprano, tooling, project_shape) | Backlog B-7 | planes 29, 43 y 52 (`plans/52-tooling-profile-candidacy.md`) |
| Baja | Modelo de ejecución de delegaciones en runtimes de contexto único | Backlog B-8, plan 49 | plan 49 (`plans/49-delegation-single-instance-model.md`) |

Los estados de esos planes/RFCs se consultan en `plans/INDEX.md` (fuente de
verdad descriptiva); esta tabla solo referencia, no duplica estados.

Además, las RFCs 39–54 (en `Proposal`) madurarán tooling a medida que se
acepten: budget de discovery, freshness de KB, validación mecánica de skills,
catálogo de roles de worker, entre otros.

## Proceso

1. Cada ítem se toma como par RFC + plan según la gobernanza de `plans/INDEX.md`
   (§Convenciones, RFC-42).
2. Los entregables documentales del repo (`tools/`, `runtime/`, `docs/`) no
   requieren RFC (no tocan
   `protocol/.agents/`); los cambios de código del runtime sí se revisan con la
   suite de tests correspondiente (`tests/`).
3. Este documento se actualiza cuando un ítem pasa a plan o se ejecuta.
