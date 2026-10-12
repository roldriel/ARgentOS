# Roadmap

Mapa **operativo actual** del trabajo de ARgentOS: qué se ejecuta ahora, qué
sigue, qué requiere autorización y qué es sólo candidato. No duplica el estado
detallado de los planes —eso vive en `docs/plans/INDEX.md`, en los planes y en
las RFCs, que son la fuente de trazabilidad— y no cataloga la historia ya
cerrada.

Los ítems marcados como **payload** tocan `protocol/.agents/` y requieren su
propia autorización (RFC-56) antes de ejecutarse.

El documento declara además, desde el 2026-09-22, el **roadmap estratégico
vigente** (Etapas A → B → C, sección siguiente), del que el mapa operativo es
consecuencia: las etapas se ejecutan **en ese orden** y ninguna entrada de
trabajo se incorpora fuera de él. El mapa operativo —trabajo activo, pendientes
que requieren autorización y candidatos futuros— sigue más abajo.

## Roadmap estratégico — Etapas A → B → C

ARgentOS ya posee una cantidad significativa de mecanismos: governance, Change
Lifecycle, autoridad, checkpoints, validación, SAE, Agent Worker, context
engineering, materialización, delegación, deliberación, Discovery, harness,
métricas, CI y distribución del Protocol. El objetivo siguiente **no** es seguir
agregando features de forma incremental sin validar primero las garantías que
esas features pretenden proporcionar.

El cambio de enfoque que este roadmap registra es:

> Primero determinar qué capacidades y garantías de ARgentOS están realmente
> demostradas; luego completar las fronteras necesarias para alcanzar una
> autonomía operacional mayor; recién después incorporar nuevas features basadas
> en las necesidades descubiertas.

Las tres etapas y su dependencia son:

```text
Etapa A — Capability & Guarantee Retrospective
                    |
                    v
Etapa B — Complete ARgentOS Autonomy
                    |
                    v
Etapa C — New Features
```

No son tres iniciativas independientes: **B depende de A** y **C depende de los
resultados de A y B**. Ninguna etapa se ejecuta desde este documento; cada una
es un Change propio que requiere su propia autorización.

### Etapa A — Capability & Guarantee Retrospective

**Objetivo.** Revisión integral de las capacidades y garantías que ARgentOS
afirma proporcionar. La unidad de análisis **no** es el archivo ni la feature
individual, sino:

> capacidad + garantía + evidencia

La pregunta central es:

> ¿Qué puede afirmar ARgentOS que hace, qué mecanismo lo implementa y qué
> evidencia tenemos de que realmente funciona bajo las condiciones en las que
> pretendemos utilizarlo?

**Alcance conceptual mínimo.** La retrospectiva examina, como mínimo: Change
Lifecycle; Authority; Scope enforcement; Validation / Closure; C1/C2/C3; SAE;
Autonomous Orchestrator; Agent Worker; WorkerResult; Delegation; Context
engineering; Context identity; Materialization; Prompt Cache; Placement;
Discovery; Discovery KB; Protocol gates; enforced mode / hooks; EARS; Skills;
Deliberation; Change Governance; Metrics / health; Feature flags; recovery;
CI / validation; y distribución y sincronización de `dist`.

No se asume que todas estas capacidades tengan el mismo nivel de madurez. La
revisión debe distinguir explícitamente entre:

| Nivel | Qué significa |
| --- | --- |
| implementado | el mecanismo existe en el repositorio |
| testeado | existe cobertura automatizada que lo ejercita |
| dogfoodeado | fue ejercitado en el propio repositorio |
| demostrado bajo condiciones reales | funcionó en las condiciones de uso pretendidas |
| parcialmente demostrado | sólo un subconjunto de esas condiciones fue ejercitado |
| dependiente de una condición externa | su garantía depende de algo fuera del control de ARgentOS |
| no demostrado | existe sin evidencia de que funcione |
| limitado por un boundary conocido | funciona dentro de un límite declarado |

**Resultado esperado.** Un **Capability & Guarantee Matrix** que permita
distinguir, para cada capacidad relevante:

- qué afirma hacer;
- qué mecanismo lo implementa;
- qué tests existen;
- qué dogfooding existe;
- qué condiciones se probaron;
- qué condiciones no se probaron;
- qué garantía puede considerarse demostrada;
- qué garantía permanece sin demostrar;
- qué limitaciones existen.

No se asume que una feature está "completa" simplemente porque exista código o
tests.

**Regla fundamental.** La Etapa A **no** es una limpieza documental ni una
auditoría de archivos: evalúa la validez de las garantías operacionales.

### Etapa B — Complete ARgentOS Autonomy

La Etapa B comienza a partir de los resultados de la Etapa A. No se define aquí
una lista rígida de features a implementar: la Etapa A determina cuáles
fronteras son realmente necesarias.

La Etapa B **no** declara inexistente la autonomía ya implementada: nombra el
cierre de las fronteras que esa capacidad todavía no cubre (ver
`### Estado del que parte este roadmap`). No declara terminada ninguna capacidad
futura ni convierte las fronteras candidatas en compromisos de implementación.

**Objetivo.**

> Cerrar las fronteras reales que impiden que ARgentOS pueda recibir un objetivo
> suficientemente amplio y ejecutarlo de manera autónoma bajo supervisión
> humana, manteniendo sus garantías de autoridad, contexto, evidencia,
> recuperación y terminación.

**Dirección.**

```text
Human
  |
  | authorized objective / scope
  v
ARgentOS Orchestrator
  |
  +-- observe
  +-- derive
  +-- plan
  +-- delegate
  +-- execute
  +-- ingest
  +-- verify
  +-- correct
  +-- revalidate
  +-- continue
  +-- stop
```

**Fronteras a investigar y completar**, según lo que la Etapa A demuestre
necesario: las que separan Orchestrator, Agent Worker real, provider/model,
contexto, delegación, resultado de ejecución, evidencia, verificación,
recuperación, continuación y terminación.

**Fronteras candidatas conocidas** — explícitamente **candidatas, no
compromisos de implementación**; no se convierten automáticamente en features
del roadmap, y la Etapa A determina cuáles son realmente necesarias:

- ejecución real mediante provider/model;
- persistencia y consumo de Worker Results;
- derivación de la siguiente acción;
- ejecución multi-step;
- recuperación ante fallos reales;
- fallos del provider (provider failures);
- salidas inválidas del Worker (invalid Worker outputs);
- presupuestos de ejecución (execution budgets);
- garantías de terminación (termination guarantees);
- ejecución multi-worker;
- deliberación cuando realmente aporte valor;
- integración real de Prompt Cache;
- persistencia de Project/Knowledge.

**Resultado esperado.** Una ARgentOS capaz de avanzar autónomamente dentro de

```text
Autonomy ⊆ Scope ∩ Authority
```

manteniendo la frontera humana para: decisiones normativas; ampliación de
Scope; ampliación de Authority; cambios de objetivos; decisiones de release; y
decisiones explícitamente reservadas al mantenedor.

### Etapa C — New Features

Las nuevas features vuelven a incorporarse **después** de completar A y B. La
regla es:

> No agregar features por disponibilidad tecnológica o porque exista un
> mecanismo equivalente en otro sistema.

Una nueva feature entra al roadmap cuando:

1. existe una necesidad identificada;
2. esa necesidad está sustentada por la retrospectiva o por experiencia
   operacional;
3. existe una justificación clara;
4. la feature contribuye a una capacidad o garantía real de ARgentOS.

La expansión funcional queda **subordinada** al conocimiento obtenido en A y a
las necesidades descubiertas durante B.

### Qué no es una entrada de este roadmap

Este documento es **estratégico**, no un backlog de implementación. No se
convierten en ítems del roadmap, por el hecho de existir o de ser técnicamente
posibles:

- nuevas auditorías documentales;
- nuevos checkers por el simple hecho de existir;
- nuevos RFCs sin necesidad identificada;
- nuevas capas de governance;
- nuevas state machines;
- nuevos registries;
- nuevas entidades globales;
- más artefactos administrativos;
- más métricas sin hipótesis operacional;
- features copiadas de otros proyectos;
- integraciones de providers únicamente por disponibilidad tecnológica.

### Estado del que parte este roadmap

- ARgentOS DEV ya posee un conjunto significativo de mecanismos de ejecución y
  governance.
- El Protocol está publicado en **`12.0.0`** (release del plan 154, RFC-81:
  lifecycle de adopción y layout canónico `.argentos/`; MAJOR por
  `docs/VERSIONING.md` §3). DEV y Protocol son dominios separados.
- `dist` publica el payload del Protocol desde `master` (`78ca512`), con
  `VERSION` = `12.0.0`.
- `dev` lleva **una corrección de payload no publicada**: el PATCH **`12.0.1`**
  (plan 156, RFC-82), que reconcilia prosa del payload con el layout canónico
  `.argentos/` sin cambiar comportamiento. `dev` y `master` dejan de apuntar al
  mismo commit por esa única razón; su promoción es un acto de release separado y
  no autorizado.
- No existe **ninguna otra** feature de Protocol pendiente de publicación
  simplemente por estar en `dev`: el `[Unreleased]` del changelog acumula ítems
  de gobernanza de planes docs-only (RFC-69), no payload sin publicar.
- **ARgentOS Autonomy: qué existe hoy y qué pertenece a la Etapa B.** Existe una
  capacidad de autonomía **implementada y testeada** en DEV —el host DEV
  Autonomous Orchestrator (`runtime/orchestrator/`) con Supervised Autonomous
  Execution (`--sae`) y su frontera de scope/autoridad, con sus suites—, y existe
  además un **modelo de autoridad ya decidido** para su envelope
  (`docs/adr/19-autonomy-envelope-authority.md`, `AE-1`…`AE-10`, planes 151–153).
  Ambas cosas están **en el estado publicado del repositorio** (`master` y tag
  `12.0.0`) y son **DEV-only**: no forman parte del payload que distribuye `dist`.
  Lo que **no** está hecho, y es lo que la Etapa B agrupa, es la **implementación
  del envelope** —gate de efectos, clases de efecto, presupuesto de recurso, actor
  con provider/modelo, aislamiento, integración de Memory y superficie de
  derivación— junto con el resto de fronteras candidatas, que siguen declaradas
  como candidatas y no como compromisos:
  `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación`.
- El siguiente objetivo estratégico **no** es resolver una supuesta divergencia
  de publicación.
- El estado histórico sobre el que se construye este roadmap —Planes 146–154,
  Change Lifecycle MVP, SAE MVP, Prompt Cache MVP, Jury Trial MVP, Placement
  Contract, Memory System, cierre de autoridad del modelo de autonomía y
  lifecycle de adopción, RFC-75, ADR-15, ADR-16, ADR-17, ADR-18 y ADR-19— no se
  reabre: es el punto de partida, no trabajo pendiente.

## Trabajo activo / dogfood

| Prioridad | Trabajo | Origen | Estado |
| --- | --- | --- | --- |
| — | — | — | **Sin trabajo activo.** |

La tabla está **sin trabajo activo**: ninguna etapa del roadmap estratégico está
en ejecución. El **próximo trabajo declarado es la Etapa A — Capability &
Guarantee Retrospective**; su ejecución es un Change propio que requiere su
propia autorización, y este documento no la concede ni la sustituye.

Trabajo **posterior a esta tabla** ya ejecutado y **cerrado**, que no pertenece al
roadmap estratégico y por eso no se reabre aquí: el **lifecycle de adopción
ARgentOS** (plan 154, RFC-81; ejecutado el 2026-10-11) —layout canónico
`.argentos/`, `install`/`update`/`uninstall`/`doctor` y release MAJOR `12.0.0`—,
que entró por necesidad identificada de adopción y no como Etapa C, y el
**Memory System reference runtime** (plan 150, RFC-80; versión `11.7.0`). Su
estado detallado vive en `docs/plans/INDEX.md` y en sus planes, que es donde este
documento delega la trazabilidad.

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
4. Las etapas del roadmap estratégico **no** son entradas de trabajo ejecutables
   desde este documento: cada una requiere su propio Change autorizado, y este
   mapa registra la dirección y el estado, no autoriza trabajo. Ninguna entrada
   nueva se incorpora por disponibilidad tecnológica ni por simetría con otro
   sistema, y las fronteras candidatas de la Etapa B no se convierten en
   features sin que la Etapa A determine que son necesarias.
