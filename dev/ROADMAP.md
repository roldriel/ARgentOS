# Roadmap del workspace dev

Este documento cataloga la cobertura actual de `dev/`, lo que falta y las
prioridades. No implementa nada: cada entrada cita su origen en `plans/INDEX.md`
o en los planes/RFCs. Los ítems que toquen `protocol/.agents/` requieren su
propio RFC/plan antes de ejecutarse.

## Cobertura actual

- Invariantes documentales del payload (checker + 50 tests, serie 27/28).
- Citas de planes (`check_plan_citations.py`).
- Materializaciones de referencia del Execution Context (prompt y tool calls,
  planes 07/18) con tests.
- Tests del harness (`protocol/.agents/harness/tests/`): probe, hook y runner.

## Pendientes priorizados (origen: `plans/INDEX.md`)

| Prioridad | Ítem | Origen |
| --- | --- | --- |
| Alta | Gate D01 superable (artefacto-puente de discovery) | Backlog B-1 |
| Alta | Recovery económico para fallos de formato (parcialmente cubierto por plan 29) | Backlog B-2, plan 33 |
| Media | Marcador `.last_discovery` canónico + validación en health-check | Backlog B-3, plan 50 |
| Media | Tanda de inconsistencias de contratos/policies | Backlog B-4 |
| Media | Política de clarificación desatendida | Backlog B-5, plan 44 |
| Media | Subcomandos del runner para H15 | Backlog B-6 |
| Baja | Enmiendas conceptuales (recovery temprano, tooling, project_shape) | Backlog B-7 |
| Baja | Modelo de ejecución de delegaciones en runtimes de contexto único | Backlog B-8, plan 49 |

Además, las RFCs 39–54 (en `Proposal`) madurarán tooling a medida que se
acepten: budget de discovery, freshness de KB, validación mecánica de skills,
catálogo de roles de worker, entre otros.

## Proceso

1. Cada ítem se toma como par RFC + plan según la gobernanza de `plans/INDEX.md`
   (§Convenciones, RFC-42).
2. Los entregables documentales de `dev/` no requieren RFC (no tocan
   `protocol/.agents/`); los cambios de código del runtime sí se revisan con la
   suite de tests correspondiente.
3. Este documento se actualiza cuando un ítem pasa a plan o se ejecuta.
