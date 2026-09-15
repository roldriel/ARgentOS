# Roadmap

Este documento cataloga los pendientes priorizados del proyecto y sus
prioridades. No implementa nada: cada entrada cita su origen en
`docs/plans/INDEX.md` o en los planes/RFCs. Los ítems que toquen
`protocol/.agents/` requieren su propio RFC/plan antes de ejecutarse.

## Backlog resuelto (origen: `docs/plans/INDEX.md`)

| Prioridad | Ítem | Origen | Cubierto por |
| --- | --- | --- | --- |
| Alta | Gate D01 superable (artefacto-puente de discovery) | Backlog B-1 | planes 40 (`docs/plans/40-discovery-artifact-boundaries.md`) y 47 (`docs/plans/47-discovery-per-entry-contracts.md`) |
| Alta | Recovery económico para fallos de formato (parcialmente cubierto por plan 29) | Backlog B-2, plan 33 | planes 29 (`docs/plans/29-recovery-to-early-phases.md`) y 33 (`docs/plans/33-ears-criteria-canonical-form.md`) |
| Media | Marcador `.last_discovery` canónico + validación en health-check | Backlog B-3, plan 50 | plan 50 (`docs/plans/50-discovery-kb-freshness.md`) |
| Media | Tanda de inconsistencias de contratos/policies | Backlog B-4 | planes 37–43 y 53 (`docs/plans/`, numeración correlativa) |
| Media | Política de clarificación desatendida | Backlog B-5, plan 44 | plan 44 (`docs/plans/44-unattended-clarification.md`) |
| Media | Subcomandos del runner para H15 | Backlog B-6 | plan 46 (`docs/plans/46-enforced-mode-dogfooding.md`) |
| Baja | Enmiendas conceptuales (recovery temprano, tooling, project_shape) | Backlog B-7 | planes 29, 43 y 52 (`docs/plans/52-tooling-profile-candidacy.md`) |
| Baja | Modelo de ejecución de delegaciones en runtimes de contexto único | Backlog B-8, plan 49 | plan 49 (`docs/plans/49-delegation-single-instance-model.md`) |

Los ítems de esta tabla provienen del backlog evidenciado del plan 19 (5 ago
2026) y **ya fueron resueltos**: cada `B-x` se redactó como par plan/RFC en la
Sexta serie (`docs/plans/INDEX.md` §Backlog evidenciado - plan 19 registra la
resolución ítem por ítem). La tabla se conserva como traza de esa resolución,
no como trabajo pendiente. El estado de cada plan se consulta en
`docs/plans/INDEX.md` (fuente de verdad descriptiva); esta tabla solo
referencia, no duplica estados.

Además, las RFCs 39–54 quedaron todas `Accepted` vía RFC-56 (plan 57) y sus
planes asociados están `Executed`, por lo que el tooling que maduraban (budget
de discovery, freshness de KB, validación mecánica de skills, catálogo de roles
de worker, entre otros) ya está materializado; el protocolo pasó de 3.x a
11.x. El estado `Accepted`/`Executed` no es `Released`: la publicación por
versión y tag se consulta en `docs/VERSIONING.md` §9.

## Proceso

1. Cada ítem se toma como par RFC + plan según la gobernanza de `docs/plans/INDEX.md`
   (§Convenciones, RFC-42).
2. Los entregables documentales del repo (`tools/`, `runtime/`, `docs/`) no
   requieren RFC (no tocan
   `protocol/.agents/`); los cambios de código del runtime sí se revisan con la
   suite de tests correspondiente (`tests/`).
3. Este documento se actualiza cuando un ítem pasa a plan o se ejecuta.
