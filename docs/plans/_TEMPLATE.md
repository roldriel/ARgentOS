# Plan NN — <Título corto y operativo>

<!-- Antes de crear el archivo:
     - Numeración: consultar docs/plans/INDEX.md para el próximo número libre; los
       planes numeran por orden cronológico de ejecución, nunca se reusan.
     - Nombre de archivo: NN-slug-descriptivo.md en minúsculas con guiones.
     - Este template no se numera ni se registra en el INDEX. -->

**Status:** Aprobado para redacción | Aprobado para ejecución
**Fecha:** YYYY-MM-DD
**Tipo:** Plan | Nota (opcional; **ausencia ⇒ `Plan`**; `Nota` = forma mínima dentro de la **misma** familia)
**Lifecycle:** active | archived | superseded | deprecated (opcional; **ausencia ⇒ `active`**)
**RFC:** RFC-NN (`docs/rfc/NN-slug.md`) | —
**RFC-56 Class:** N/A | A | B | C (multi-clase: `A, B`) — **solo payload deltas**:
efecto sobre `protocol/.agents/` (ver RFC-56). `N/A` = sin payload delta. La ruta
efectiva la fija la clase más estricta presente (`A > B > C > N/A`); **no** existe
una clase `AB`. No confundir con `**Change Level:**` (dimensión independiente).
**Change Level:** L0–L3 (ver RFC-75 Mecanismo 2:
`Level = max(coordination, scope, architectural impact, release impact,
duration/complexity)`; el número de commits no es dimensión; Change Level ≠
clase RFC-56)
**Depende de:** plan NN | —
**Origen:** <auditoría, bitácora, decisión — con referencia verificable>
**Work type:** <valor derivado por el criterio de admisión de `docs/CONVENTIONS.md` | GAP> (opcional: se declara **sólo** cuando el valor cambia una decisión de gobernanza; el valor **no** se inventa)
**Superseded por:** <identidad del sucesor (RFC, ADR, plan o ruta) | —>
**Motivo de retiro:** <razón explícita y verificable> (obligatorio **sólo** cuando no existe sucesor)

<!-- `**RFC-56 Class:**` pertenece al **payload delta**, no al Plan ni al Change: un
Change con un delta A y un delta C declara `A, C` y su ruta es RFC `Accepted` +
Plan; un Change sin efecto sobre `protocol/.agents/` declara `N/A` y no se clasifica
A/B/C. Los planes históricos que usan `**Clase:**` conservan su header (RFC-46); a
partir de la enmienda 2026-10-23 (Plan 174) el campo canónico es
`**RFC-56 Class:**`. Ver
`docs/rfc/56-governance-fast-track.md:Modelo vigente (enmienda 2026-10-23)`. -->

<!-- Campos adoptados por el acto de autoridad del Plan 152 (2026-10-07; ver
`docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note` y
`docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type`):
`**Tipo:** Nota` habilita la **forma mínima** de `Note` dentro de esta misma familia — nace de este
template con las secciones mínimas, se registra en `docs/plans/INDEX.md` y **no** crea familia,
namespace ni identidad nueva. `**Lifecycle:**` no se fusiona con `**Status:**`, su default es `active`
por ausencia y la guarda es **hacia adelante**. `Abandoned` es una **condición derivada**
(`Superseded` **sin** sucesor **∧** `Motivo de retiro`), nunca un valor nuevo. `**Work type:**` se
declara sólo si el valor cambia una decisión de gobernanza, y **no** se deriva aquí. -->

<!-- El Status inicial define la clase de entregable (ciclo de status de
planes en docs/CONVENTIONS.md:Convenciones). La RFC puede ser "—" solo por vía
plan, con justificación documentada en este archivo. Al crear el plan,
registrarlo en docs/plans/INDEX.md (tabla + serie) en el mismo commit.

El campo Change Level es la clasificación de intake del cambio (regla
operacional del Incremento 1; docs/CONVENTIONS.md:Change Lifecycle — Intake y
clasificación (regla operacional; Incremento 1)): se computa al crear el plan
(L0 provisional si aplica) y es mutable con justificación documentada
(upgrade obligatorio ante triggers; downgrade con nota). -->

## Objetivo

<!-- Qué logra el plan en uno o dos párrafos. Sin mecánica: eso va en Pasos. -->

## Derivación y premisas (`premises(D)`)

<!-- Obligatorio para una derivación completa (`HD-K3`, adoptado por el acto de autoridad del
Plan 151, 2026-10-07; ver `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K`).
La EXISTENCIA de esta sección depende de la adopción de `premises(D)`; `HD-K3` y `HD-M5`
determinan contenido/forma y NO son precondiciones de existencia (ver
`docs/plans/151-autonomy-authority-decision-closure.md`).
Si una premisa obligatoria no puede establecerse, el resultado documental
correspondiente es `GAP` (falta de información): nunca se asume. Cada clase
declara su valor y su fuente citada (`ruta:sección`). -->

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | texto normalizado del pedido + su `origin_type` | humano | identidad del artifact de intake |
| `P-2` Confianza de intención | nivel `HIGH`/`MEDIUM`/`LOW` + criterios aplicados | agente | `INTENT_CONFIDENCE.md` |
| `P-3` Conjunto de contexto | fuentes efectivamente leídas | agente | lista de `ruta:sección` |
| `P-4` Derivabilidad | condición con su señal (sin señal bloqueante · `GAP`/`ANOMALY`/`BOUNDARY` · `REQUIRES_HUMAN`) y su evidencia (una cita por ítem) | agente | el propio registro |
| `P-5` `work_type` | valor derivado y su criterio de admisión | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` |
| `P-6` Conocimiento vigente | lifecycle declarado de cada fuente citada | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | veredictos `APPLIES`/`NOT_APPLICABLE` con su cita | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | autoridad requerida y conjunto declarado de rutas | **humano** | declaración del humano |

## Criterio de entrada

<!-- Checklist verificable de lo que debe existir ANTES de ejecutar: archivos,
estados de RFCs/planes previos, verificación contra el repo (paso 0). -->

- [ ] ...

## Entregables

<!-- Lista numerada de artefactos concretos con ruta. Es lo que Verificación
chequea. -->

1. ...

## Pasos

<!-- Secuencia operativa ordenada. Cada paso referencia rutas y secciones
exactas (`ruta:sección`), nunca números de línea ni ordinales. -->

1. ...

## Delegación agentiva

<!-- OPCIONAL (regla operacional del Plan 123). Declara el trabajo semántico que
el DEV Autonomous Orchestrator puede delegar a un Agent Worker
(`runtime/orchestrator/agent_worker.py`). Sección aditiva-optional: un Plan sin
ella no delega trabajo semántico (ausencia declarada) y el host conduce sólo
validación y gates como hasta ahora. No se inventa trabajo: sin `Task` no hay
delegación.

- **Task:** <instrucción de trabajo autorizada: QUÉ debe hacerse, no cómo>. La
  autoridad es este Plan aprobado; el Agent Worker no adquiere autoridad propia.
- **Scope:** `<ruta/uno.py>`, `<ruta/dos.py>` (rutas repo-relative que el Worker
  queda autorizado a modificar). Si se omite, se usan los entregables declarados
  y la observación registra que el scope no fue explícito. El host verifica este
  scope **después** de la delegación comparando snapshots de contenido: una ruta
  modificada fuera de él produce `STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN`.

El resultado del Worker es un `WorkerResult` (contrato M4) con
`claims.self_reported_completion = false`; no declara `Closed` ni ninguna
condición derivada, y su recomendación es advisory. Ver
`.agents/policies/autonomous-orchestration.md` §11. -->

- **Task:** ...
- **Scope:** `<ruta/uno.py>`
- **Resource ceiling:** `<n>` ejecuciones delegadas <!-- OPCIONAL. Techo operativo de ejecuciones
  **delegadas** de este Change: el runtime lo lee, acumula el consumo desde las delegaciones
  efectivamente registradas en el journal y detiene la autonomía al agotarse
  (`STOP_MAX_ITERATIONS`). Es una **guarda operativa de terminación, nunca una dimensión de
  autorización** (ADR-19 `AE-6`, decisión `D-3`): no entra en el envelope de autonomía, no produce
  veredicto de autoridad y no sustituye a `Scope` ni a `Authority`. Debe ser un entero positivo; un
  valor ilegible se registra como `GAP` y **no** se asume. Ver
  `docs/CONVENTIONS.md:Modelo de autonomía — vocabulario de efectos y techo de recurso (adoptado 2026-10-11)`. -->

## Efectos declarados

<!-- OPCIONAL: obligatoria únicamente si el Change prevé efectos fuera de la frontera inmediata.
Decidido por el acto de autoridad del Plan 151 (2026-10-07): `D-2a` la frontera se decide y se
declara en DEV; `D-2b` los efectos se declaran donde vive la autorización —el Plan—; `D-2d`
`Effect` es ortogonal a `Scope` y un efecto puede no tener path. El **vocabulario de clases de
efecto** fue adoptado por el acto de autoridad del Plan 159 (2026-10-11). Ver
`docs/CONVENTIONS.md:Modelo de autonomía — vocabulario de efectos y techo de recurso (adoptado 2026-10-11)`
y `docs/adr/19-autonomy-envelope-authority.md`.

Cada entrada declara: el nombre del efecto, qué produce, la referencia a su autorización (quién lo
autorizó y dónde consta) y su estado. **Clases admitidas (vocabulario cerrado):** `network`,
`remote_git`, `install`, `destructive`, `write_outside_project`. **Estado:** `authorized`,
`not_authorized`, `pending_user_confirmation`. Una clase **no reconocida o no determinable NO se
interpreta como autorizada**: se detiene con autoridad humana (`STOP`/`REQUIRES_HUMAN`). Un efecto
autorizado puede no tener path. Un efecto que el worker ejecute sin estar declarado y autorizado es
una violación de la frontera: se registra como finding y detiene el ciclo.

Para declarar explícitamente la **ausencia** de efectos se deja una sola fila negativa
(`| — | ninguno: ... | — | authorized |`): declara que el Change no produce efectos y no autoriza
ninguno. Un Plan que no lleva esta sección no ha declarado nada sobre efectos, y una acción que
puede producirlos se detiene. -->

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| ... | ... | ... | ... |

## Criterios de salida

<!-- Checklist específico del plan que define "terminado". Complementa el DoD
general de docs/VERSIONING.md §10, no lo reemplaza. -->

- [ ] ...

## Verificación

<!-- Comandos exactos que deben correr en verde, y juicios manuales si aplican
(ej. H13). Solo los que este plan exige. -->

## Validation anchor

<!-- Se completa al validar (regla operacional VC-1, Incremento 1;
docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)):

- Declared scope: ...
- Validation command-set: ...
- Effective inputs (repo content): ...
- Observed dependencies: ... | no instrumentado
- Environmental factors: ...
- Scoped Content Identity: delta (path → blob) y state identity
  (git write-tree / tree id)
- Validity / stale: vigente | stale (motivo) | revalidada -->

## Checkpoint / cierre

<!-- Se completa al cerrar (regla operacional GC-1, Incremento 3;
docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)):

- Commits de cierre: ...
- Estado validado (ref al Validation anchor): ...
- Estado de cierre (identidad): delta scoped identity + state identity del anchor
  aplicable (el tree id del índice staged en el momento de la validación). Es el
  estado que el checkpoint **certifica** por correspondencia GC-1. **No** es el
  árbol del commit de cierre.
- Árbol material del commit de cierre (tree id): solo cuando el commit ya existe;
  es un hecho de Git, no la identidad del estado de cierre, y puede diferir
  legítimamente del declarado porque el commit de cierre incluye governance
  (RFC-75 Mecanismo 7).
- Consistencia checkpoint↔anchor: PASS/FAIL + evidencia (revalidación si difiere)
- Governance aplicada: ...
- Documentation impact (§5.1 de `.agents/policies/validation-closure.md`):
  REQUIRED | NOT_REQUIRED | DEFERRED. `REQUIRED` → documentos afectados
  (rutas), aspecto afectado, actualización y evidencia; `NOT_REQUIRED` → razón
  explícita ligada al alcance real; `DEFERRED` → documentación pendiente,
  motivo y pending decision existente (PC-1) con owner. Nunca en blanco.
  Historical docs (RFCs, ADRs, planes cerrados, reportes, auditorías) no se
  actualizan por describir un estado antiguo (RFC-46).
- Roadmap impact (§5.2 de `.agents/policies/validation-closure.md`):
  REQUIRED | NOT_REQUIRED | DEFERRED — determinación **independiente** de la
  anterior. `REQUIRED` → trabajo creado/completado/cancelado/reclasificado/
  re-priorizado, artefacto que lo posee (ownership/source of truth: `ROADMAP.md`
  como mapa operativo, `docs/plans/INDEX.md`, índices de RFC/ADR, un plan
  activo), actualización y evidencia. **No** significa "editar `ROADMAP.md`":
  el `ROADMAP.md` sigue siendo un mapa operativo, no un changelog.
  `NOT_REQUIRED` → razón explícita (sin efecto sobre el mapa de trabajo
  futuro); `DEFERRED` → impacto pendiente, motivo y pending decision existente
  (PC-1) con owner. Nunca en blanco.
- Condición derivada: Closed (docs-only) | Closed (con release pendiente) |
  no cerrado (motivo) -->

## Findings / Correcciones / Pending

<!-- Opcional: se completa solo cuando el artifact posee registros reales
(regla operacional del Incremento 2;
docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla
operacional; LC-1, Incremento 2) y docs/CONVENTIONS.md:Change Lifecycle —
Pending decisions (regla operacional; PC-1, Incremento 2)). Los artifacts
legacy (creados antes del Incremento 2) o sin registros no necesitan esta
sección: la ausencia no es invalidez (RFC-75 Mecanismo 15). Los escenarios
sintéticos de verificación no se registran aquí. Si no hay registros reales al
cerrar: "No findings detected / N/A". -->

### Findings

<!-- Formato: ref calificada `<artifact>:F-<n>` con namespace del artifact.
Inmutables: identidad, observación original, evidencia original, estado Git
observado y provenance original. Evolucionable: metadata de estado preservando
histórico. Estados: open | partially-resolved | resolved | deferred
(owner/destino) | superseded. Reapertura: finding nuevo con ref al original o
metadata reopened. N:M con corrections/revalidaciones. -->

- `<PLAN-NN>:F-01` — estado: ...; observación: ...; evidencia original: ...

### Correcciones

<!-- Formato: ref calificada `<artifact>:C-<n>`. Registro FACTUAL/TRACEABILITY
(no fuente normativa; la acción la autoriza el Plan aprobado). Provenance a
finding(s) de origen y alcance de revalidación (CL-6). -->

- `<PLAN-NN>:C-01` — refs origen: ...; alcance de revalidación: ...; evidencia
  (Git/commit/estado): ...

### Pending decisions

<!-- Pending per-artifact (PC-1). Metadata: blocking/no-blocking, owner,
escalación, resolución, evidencia, efecto downstream y ADR-worthiness. -->

- `<PLAN-NN>` — decisión: ...; blocking: sí/no; owner: ...; escalación: ...;
  resolución: ...; evidencia: ...

## Riesgos

<!-- Opcional en planes chicos. Qué puede salir mal y mitigación. -->

## Trazabilidad

<!-- Opcional. Origen → RFC → este plan → entregables. Útil en series. -->

## Nota de ejecución

<!-- No se crea con el plan: se agrega al ejecutar, con fecha, verificación
realizada y resultado. Si quedó algo incumplido: Status Executed (parcial: ...). -->
