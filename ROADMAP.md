# Roadmap

Mapa **operativo actual** del trabajo de ARgentOS: qué se ejecuta ahora, qué
sigue, qué requiere autorización y qué es sólo candidato. No duplica el estado
detallado de los planes —eso vive en `docs/plans/INDEX.md`, en los planes y en
las RFCs, que son la fuente de trazabilidad— y no cataloga la historia ya
cerrada.

Los ítems marcados como **payload** tocan `protocol/.agents/` y requieren su
propia autorización (RFC-56) antes de ejecutarse.

## Trabajo activo / dogfood

| Prioridad | Trabajo | Origen | Estado |
| --- | --- | --- | --- |
| — | — | — | **Sin trabajo activo.** |

`EARS structural validator` (`B-2` derivado) **se ejecutó** (plan 137, 2026-09-21): el
validador estructural del payload existía desde el plan 66/RFC-57 y lo que restaba era la
guarda DEV de paridad `tools/check_ears_coverage.py` con sus tres suites, que audita la
coherencia entre el estándar (`EARS.md`), el contrato (`TASK_SPECIFICATION.md`) y el
validador del payload **sin** reimplementarlo. El Plan 137 está `Executed` con condición
derivada `Closed`. La entrada se retira de trabajo activo porque ya no representa trabajo
futuro: su estado detallado vive en `docs/plans/INDEX.md` y en el Plan 137, que es donde
este documento delega la trazabilidad.

`Mechanical D01 subset — DEV checker for discovery output structure and provenance`
(`B-1` derivado) **se ejecutó** (plan 136): el checker DEV del subconjunto mecánico de
D01 existe en `tools/check_discovery_output.py`, con su suite y su dogfood, y el Plan 136
está `Executed` con condición derivada `Closed`. Los residuos de payload que D01 no podía
resolver (`F-17`, `F-16`) quedaron **resueltos** por la RFC-79 y el Plan 142 (2026-09-21,
versión 11.6.0): el contrato expresa la procedencia de ausencias y hechos de árbol y el
shape documental, y el checker del subconjunto mecánico dejó de tolerar un `source_files`
no resoluble.

**Criterio de prioridad.** La prioridad de una entrada del mapa vigente es la que fija
`ROADMAP.md` al registrarla, no el ítem histórico del que deriva: el ítem histórico `B-2`
fue `Alta` **por su propio motivo y en su propio contexto** («un fallo de formato cuesta
una fase RECOVERY completa», `docs/plans/INDEX.md` §Backlog evidenciado - plan 19), y la
entrada derivada `EARS structural validator` fue registrada `Media` por el Plan 132
(`docs/plans/132-roadmap-current-state.md`). No se recalifica una entrada del mapa sin
evidencia documental nueva; con la entrada ya retirada, `B-2` y su trabajo derivado no
conservan estado en este mapa.

## Pendientes que requieren autorización

**Ninguno.** Los tres residuos de payload que esta sección registraba (`F-14`/`F-17`,
`F-16`, `B-8` residual) están **implementados** desde el Plan 142 (2026-09-21, RFC-79
`Accepted`, versión 11.6.0): el marcado legacy tiene representación, `source_files` admite
`project_scan` para ausencias y hechos de árbol, `project_shape` admite `documentation` y
el catálogo de métricas tiene el evento de sesión `session_risk`. La sección queda como
constancia de que no hay trabajo de payload pendiente de autorización; el estado detallado
vive en `docs/plans/INDEX.md`, en los planes 141/142 y en la RFC-79.

- **`B-4` residual — resuelto.** `F-14` (el manifest no podía expresar marcado legacy) y
  `F-17` (procedencia de `source_files` para ausencias y hechos de árbol) quedaron
  decididos por el Plan 141 y materializados por el Plan 142. `F-18` (delimitador del
  front matter de KB entry) viajó en la misma RFC y está materializado.
- **`B-7` residual — resuelto.** `project_shape` contempla desde el Plan 142 el shape
  `documentation`, de modo que un repositorio documental deja de clasificar `unknown`. La
  corrección de trazabilidad de `docs/plans/INDEX.md` registrada en el Plan 132 sigue
  siendo un problema **documental** distinto, fuera del alcance del Plan 141.
- **`B-8` residual — resuelto.** El catálogo de
  `protocol/.agents/contracts/METRICS.md` tiene el evento de sesión `session_risk` con el
  que el modo single-instance registra su riesgo, y `PROTOCOL_METRICS.md` declara su clase
  de verifiabilidad.
- **Dogfood del perfil `trivial` — actividad externa de adopción, no backlog.** La
  medición del dogfood del perfil `trivial` (`docs/plans/25-task-profile-model.md`, plan
  25) **no es trabajo del repositorio** y deja de figurar como pendiente: exige una
  versión promovida a `master` con `dist` regenerado y una sesión de protocolo real con un
  usuario en un proyecto adoptante, y ninguna de las dos cosas es autoridad del agente
  (`Promoted`/`Released` se reportan `FORBIDDEN`). El trabajo estructural que el plan 25
  pedía está declarado e implementado —el perfil `trivial` con sus tres artefactos y sus
  gates `H00, H04, H06` en
  `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`, con
  comportamiento profile-aware verificado—, de modo que lo que resta es una actividad de
  **adopción/operación** con su criterio de éxito y su procedimiento, registrada como no
  ejecutada. El Plan 143 resolvió el residual de backlog y `<PLAN-141>:PC-2` quedó
  `resuelta`. El dogfood del modo enforced (plan 26) está **satisfecho**: su RFC de origen
  (RFC-47) admitía una simulación de harness con fixtures y el plan 46 la ejecutó y la
  verificó.

## Candidatos futuros

| Trabajo | Origen | Estado |
| --- | --- | --- |
| Mechanical checker de `.last_discovery` | B-3 (extensión) · `docs/plans/50-discovery-kb-freshness.md` | **Candidato futuro** — no autorizado, no planificado |

El ítem histórico `B-3` —marcador `.last_discovery` canónico y su validación en
health-check— está resuelto por el plan 50. La extensión mecánica del checker es
una posibilidad declarada, no trabajo comprometido: no se implementa ni se
planifica desde este documento.

## Trazabilidad histórica

> Los ítems históricos B-1…B-8 fueron resueltos como problemas originales. Sus
> planes y RFCs constituyen la trazabilidad histórica en `docs/plans/INDEX.md`.
> Los trabajos derivados posteriores se registran independientemente y no
> reabren esos ítems.

`B-5` (política de clarificación desatendida) y `B-6` (subcomandos del runner
para H15) están completamente resueltos y no requieren ninguna entrada en este
documento. La política de clarificación desatendida queda **disponible como
capacidad** para los dogfoods siguientes, sin trabajo adicional.

## Proceso

1. Cada ítem se toma como par RFC + plan según la gobernanza vigente
   (`docs/CONVENTIONS.md`); los ítems de payload requieren además RFC `Accepted`
   por RFC-56.
2. Los entregables DEV (`tools/`, `runtime/`, `docs/`) no requieren RFC por no
   tocar `protocol/.agents/`; los cambios de código del runtime se verifican con
   la batería canónica y la suite correspondiente.
3. Este documento se actualiza cuando un ítem pasa a plan, se ejecuta o cambia de
   categoría. El estado detallado de cada plan se consulta en
   `docs/plans/INDEX.md`, que es la fuente descriptiva; este Roadmap no lo
   duplica.
