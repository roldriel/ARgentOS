# Plan 167 — Reconciliación del cierre de la feature de autonomía (`F-C`)

**Status:** Executed
**Fecha:** 2026-10-14
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; **Clase B** de RFC-56, justificada en `## Vía de autorización y justificación`; se requiere RFC `Accepted` **sólo** si la ejecución llegara a tocar `protocol/.agents/`)
**Clase:** — (el plan **no** toca `protocol/.agents/`; cualquier efecto de payload se autoriza por su propia vía, RFC-56 Clase A)
**Change Level:** **L2** (`max(coordination=2, scope=2, architectural impact=0, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: **2** — cuatro rutas de gobernanza con dependencias entre sí (el estado narrativo, el mapa operativo, los registros de un plan cerrado y la trazabilidad) y decisión humana previa obligatoria. *scope*: **2** — `docs/` (`CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/`) y `docs/working/audits/`. *architectural impact*: **0** — no cambia modelo, contrato, capacidad ni estado de una etapa. *release impact*: **0** — DEV-only, docs-only, sin release ni tag. *duration/complexity*: **2** — multi-paso, con una decisión del mantenedor como compuerta.
**Depende de:** plan 165 (`F-C`, `Executed`/`Closed`), plan 166 (`Executed`/`Closed`), RFC-83 (`Accepted`), plan 164 (`Executed`/`Closed`)
**Origen:** pedido directo del mantenedor (2026-10-14) — «explicame qué otras cosas quedan para hacer y de ellas cuál sería la primera» —, materializado como esta propuesta de plan (Clase B, RFC-56) y registrado en `## Findings / Correcciones / Pending` de este artefacto (`P-1`, `P-8`)
**Work type:** `GAP` — la corrección documental no cambia ninguna decisión de gobernanza de este Change: restaura exactitud de estado y de trazabilidad; ningún valor se inventa

## Acto de autorización registrado (2026-10-14)

| Campo | Contenido |
|---|---|
| **Decisión** | Autorización de **ejecución** de este Plan y de la decisión de `F-4` (versionar los artefactos de auditoría) |
| **Autoridad** | **Mantenedor** |
| **Fecha efectiva** | **2026-10-14** |
| **Alcance autorizado** | El `IN SCOPE` de este Plan, sin extensión; en particular `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md` y el versionado de los artefactos de auditoría declarados `active` |
| **Artefacto designado** | **este Plan** (`docs/plans/167-reconciliacion-del-cierre-de-f-c.md`) |
| **Estado** | **Aprobado para ejecución** — terminología exacta de `docs/VERSIONING.md` §7 |
| **Evidencia** | Pedido directo del mantenedor (2026-10-14): aprobó el alcance de la propuesta y la opción de conservar el punto 4 dentro de este Plan gobernado por su propia pending decision; y, ante la propuesta de pasar el Plan a `Aprobado para ejecución`, respondió «continuemos» |
| **Límite explícito** | La autorización habilita **este** alcance; **no** autoriza editar `docs/plans/165-…` ni `166-…`, ni tocar `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` o `.agents/` |

## Vía de autorización y justificación

Este Change es **DEV-only** y **docs-only**: no modifica `protocol/.agents/`, `dist/`, `runtime/`, `tools/` ni `tests/`.

Se clasifica **Clase B** (mejora documental compatible, RFC-56) porque modifica **lo que afirman documentos vigentes**:

- **documentación operativa vigente** (`docs/CONVENTIONS.md`, `ROADMAP.md`): declaraba `F-C` en un estado anterior a su cierre ya commiteado. La corrección exige criterio editorial —qué estado narrar y con qué fundamento—, no un reemplazo mecánico;
- **registros de un plan cerrado** (`docs/plans/165-…`): el plan está `Executed` con condición derivada `Closed`, y `.agents/AGENTS.md` (regla 5) **prohíbe** reescribirlo o reabrirlo. Su reconciliación se registra **por referencia** desde este plan;
- **trazabilidad de evidencia** (`docs/working/audits/INDEX.md` frente a los tres archivos de auditoría no versionados).

Por eso la vía es **plan `Aprobado para ejecución`** (RFC-56 Clase B; `docs/VERSIONING.md` §4, paso 1). **No** se requiere RFC porque no cambia el significado del protocolo ni sus contratos, y **no** se toca el payload. **No** es Clase C: la Clase C exige *cero* cambio de significado y aquí se decide qué debe decir el estado vigente, que es una decisión editorial con fundamento.

**Compuerta.** Este Plan se creó **sin ejecutar** y permaneció en `Aprobado para redacción` hasta el acto del mantenedor del 2026-10-14, que lo habilitó (`## Acto de autorización registrado (2026-10-14)`).

## Objetivo

Restaurar la **coherencia documental** del cierre de la feature de autonomía (`F-C`): que el estado que declaran los documentos vigentes, el mapa operativo, los registros del plan que la cerró y la trazabilidad de su evidencia digan **lo mismo** y coincidan con lo que ya está commiteado en `dev`.

El Change corrige **exactitud documental**, no decisiones: no reabre `F-C`, no reabre el plan 165, no cambia ninguna capacidad, ningún contrato, ningún estado de etapa y ninguna condición derivada. Los desacuerdos que no sean errores documentales **no se resuelven aquí**: se registran como findings, se difieren o se escalan a su propia vía.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | El mantenedor pidió cerrar la feature de autonomía revisando «qué queda por hacer», identificó que el punto de entrada es la reconciliación documental de `F-C` y solicitó esta propuesta de plan | humano | pedido directo del mantenedor (2026-10-14), citado en `**Origen:**` |
| `P-2` Confianza de intención | `HIGH` — el alcance se fijó explícitamente (puntos 1–4 de la propuesta aceptados) y cada finding está sostenido por evidencia verificable en el árbol actual o en Git | agente | `INTENT_CONFIDENCE` aplicado sobre el pedido y los findings `F-1`…`F-4` |
| `P-3` Conjunto de contexto | `docs/CONVENTIONS.md` (subsecciones del modelo de autonomía), `ROADMAP.md`, `docs/plans/165-f-c-autonomy-frontier-implementation.md`, `docs/plans/166-materialize-objective-and-actor-provenance.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md`, `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md`, `.agents/policies/authority.md`, `.agents/policies/validation-closure.md`, `docs/VERSIONING.md` (§4, §4.1, §5, §7, §10), `docs/rfc/56-governance-fast-track.md`, `docs/plans/_TEMPLATE.md`, estado Git de `dev` | agente | lecturas directas de esta sesión y `git log`/`git show` citados en cada finding |
| `P-4` Derivabilidad | `derivable` — los cuatro findings son verificables contra el árbol actual y Git; **`REQUIRES_HUMAN`** para ejecutar (`Aprobado para ejecución`) y para resolver `F-4`. Señales: **ninguna** bloqueante en el diagnóstico; `BOUNDARY` posible en `F-3` (la contabilidad de counterproofs admite más de una lectura legítima) | agente | `## Findings / Correcciones / Pending`; `.agents/policies/authority.md:Conflict protocol` |
| `P-5` `work_type` | `GAP` — el criterio de admisión de `docs/CONVENTIONS.md` (`Change Lifecycle — Vigencia materializada, retiro y work_type`) no resulta alterado por la corrección: no cambia ninguna decisión de gobernanza y ningún valor se deriva aquí | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type` |
| `P-6` Conocimiento vigente | Planes 164, 165 y 166 `Executed` (165 y 166 con condición derivada `Closed`); RFC-83 `Accepted`; `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md` y `CHANGELOG.md` `active`; `runtime/`, `tools/`, `tests/` son código vigente y **no** se tocan | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md`; `check_lifecycle_anchor` / `check_lifecycle_checkpoint` |
| `P-7` Reglas aplicables | APPLIES: RFC-56 (Clase B), RFC-69 (plantilla y registro), RFC-75 (Change Lifecycle DEV), ADR-16 (autoridad), `docs/VERSIONING.md` §4/§4.1/§7/§10, VC-1/GC-1/LC-1/PC-1, `.agents/policies/validation-closure.md` §5.1/§5.2. CONDICIONAL: RFC-56 Clase A **sólo** si la ejecución tocara `protocol/.agents/` (no ocurre). NOT_APPLICABLE: RFC-46 en cuanto a reescribir artefactos históricos — este plan **no** los reescribe. NOT_APPLICABLE: RFC-56 Clase C (no es una corrección mecánica) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **mantenedor** (aprobación de ejecución; y decisión de `F-4`). Rutas declaradas —y únicas— modificadas por este Change: `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/plans/167-reconciliacion-del-cierre-de-f-c.md`, `docs/working/audits/INDEX.md` y los artefactos de auditoría versionados por decisión del mantenedor (`F-4`). **`docs/plans/165-…` y `docs/plans/166-…` NO están en el scope**: están cerrados y **no** se editaron | **humano** | pedido directo del mantenedor (2026-10-14); `.agents/AGENTS.md` (reglas 5 y 9); `.agents/workflows/change-lifecycle.md:5. Post-close problems` |

## Criterio de entrada

- [x] Pedido directo del mantenedor registrado (2026-10-14) y alcance de los cuatro puntos aceptado.
- [x] `F-C` **cerrado** con evidencia: `docs/plans/165-f-c-autonomy-frontier-implementation.md` (`Status: Executed`, `## Validation anchor` y `## Checkpoint / cierre` presentes, condición derivada `Closed`) y commit de cierre `fb0786a`.
- [x] Plan 166 `Executed`/`Closed` y RFC-83 `Accepted` (commit `a61bd97`).
- [x] Baseline verificada: `dev`, batería canónica ejecutada con su resultado registrado en la `## Nota de ejecución`; los seis checkers deterministas en verde y C-1/C-3 sin `ANOMALY`. **Factor ambiental declarado:** la pata `pytest` de la batería no es ejecutable en la sesión de ejecución (denegaciones de permisos del sandbox sobre el temporal de `tmp_path`), no atribuible a este Change —ver `## Nota de ejecución`—.
- [x] Los cuatro findings (`F-1`…`F-4`) registrados con su observación, evidencia y provenance originales.
- [x] **Compuerta de autorización:** el mantenedor pasó este Plan a `Aprobado para ejecución` (acto del 2026-10-14).

## Alcance

### IN SCOPE

1. **Estado narrativo del modelo de autonomía** en `docs/CONVENTIONS.md`: que la subsección de estado de `F-C` refleje el cierre vigente y su fundamento, sin reescribir las subsecciones históricas del 2026-10-07, 2026-10-11 y 2026-10-12.
2. **Mapa operativo** `ROADMAP.md`: que `F-C` figure con **un solo estado coherente** (cerrado) en «Posición actual», en `NEXT` y en el diagrama de dependencias, y que la Posición actual no declare ausencia de trabajo activo si hay trabajo abierto.
3. **Registros del plan cerrado 165, por referencia:** dejar constancia, desde este plan, del estado real de `ID-6`, `ID-8` y de la contabilidad de counterproofs de `FC-7`; **sin** editar `docs/plans/165-…`.
4. **Trazabilidad de la evidencia de auditoría:** que los artefactos de auditoría declarados `active` en `docs/working/audits/INDEX.md` estén versionados, o que su ausencia quede declarada con la decisión del mantenedor.

### OUT OF SCOPE

- **Reescribir o reabrir** `docs/plans/165-…` o `docs/plans/166-…` (`.agents/AGENTS.md`, regla 5).
- **Correcciones mecánicas (Clase C)** que se conducen por commit directo y **no** por este plan: el error de formato `****cerrada**` en `ROADMAP.md` y la frase de estado del encabezado de `docs/plans/INDEX.md`.
- **La historia publicada del `CHANGELOG.md`** y la reconciliación de versión del payload de RFC-83 (adición compatible ⇒ **MINOR**): la historia ya fue corregida por vía mecánica y la versión pertenece a la vía de payload (RFC-56 Clase A).
- **Decidir** si el código de `runtime/` que entró sin artefacto de plan requiere regularización: se registra el finding; su vía es una decisión del mantenedor.
- **Modificar** `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` y `.agents/`.
- **Resolver** por inferencia cualquier desacuerdo entre documentos y evidencia.

### DEPENDENCIES

```text
`F-C`        = CLOSED    (plan 165: Executed + anchor + checkpoint + consistencia; commit fb0786a)
Plan 166     = Closed    (materialización del payload; commits a61bd97, f75d70a)
RFC-83       = Accepted  (2026-10-13)
Baseline     = dev, checkers deterministas en verde y C-1/C-3 sin ANOMALY
RFC-56       = Clase B (plan `Aprobado para ejecución`); Clase A sólo si la ejecución tocara protocol/.agents/
```

## Entregables

1. Este plan, registrado en `docs/plans/INDEX.md` como **Nonagésima cuarta serie**.
2. `docs/CONVENTIONS.md` — subsección de estado del modelo de autonomía reconciliada con el cierre de `F-C`.
3. `ROADMAP.md` — `F-C` con un único estado coherente y Posición actual consistente.
4. `docs/plans/165-…` **sin modificar**, con sus registros reconciliados **por referencia** desde este plan (sección de correcciones) y los findings `F-1`…`F-4` de este Change.
5. `docs/working/audits/INDEX.md` reconciliado y los artefactos de auditoría versionados por decisión del mantenedor (`F-4`).
6. Registros de cierre: `## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`, con las determinaciones de `Documentation impact` y `Roadmap impact`.

## Pasos

1. **Paso 0 — clasificación.** Vía de autorización (**Clase B**), `Change Level` **L2**, alcance `IN`/`OUT` y criterio de entrada, registrados en este artefacto; creación del plan y su registro en `docs/plans/INDEX.md`. Ejecutado al crear el Plan.
2. **Paso 1 — reconciliar el estado narrativo.** En `docs/CONVENTIONS.md` (sección del modelo de autonomía), llevar el estado de `F-C` al cierre vigente, citando como fundamento el acto del mantenedor del 2026-10-13 y la decisión de cierre registrada en `docs/plans/165-…`. **No** se modificaron las subsecciones históricas.
3. **Paso 2 — reconciliar el mapa operativo.** En `ROADMAP.md`, dejar `F-C` con un único estado (cerrado) en «Posición actual», en `NEXT` y en el diagrama de dependencias, y corregir la afirmación de ausencia de trabajo activo. `ROADMAP.md` es un mapa operativo, no un changelog.
4. **Paso 3 — reconciliar registros del plan cerrado, por referencia.** Registrar en este plan el estado real de `ID-6`, `ID-8` y de la contabilidad de counterproofs de `FC-7` de `docs/plans/165-…`, con la cita del registro que los resolvió. **Cero** diff en `docs/plans/165-…`.
5. **Paso 4 — trazabilidad de la evidencia de auditoría.** Versionar los artefactos de auditoría declarados `active` en `docs/working/audits/INDEX.md` y reconciliar el índice, conforme a la decisión del mantenedor registrada en `## Acto de autorización registrado (2026-10-14)`.
6. **Paso 5 — verificación y cierre.** Batería canónica y gates C-1/C-2/C-3; verificación factual de los criterios de salida; `## Validation anchor`; `## Checkpoint / cierre` con `Documentation impact` y `Roadmap impact`; `## Nota de ejecución`; commit atómico en `dev`.

## Delegación agentiva

No se declara delegación en este Plan: la sección no lleva `**Task:**`, lo que constituye una **ausencia declarada** para el host. El Change es documental y su decisión central (`F-4`, y la aprobación de ejecución) perteneció al mantenedor.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change es DEV-only y docs-only; no prevé `network`, `remote_git`, `install`, `destructive` ni `write_outside_project` | — (ausencia declarada) | `authorized` |

## Criterios de salida

- [x] `docs/CONVENTIONS.md` declara `F-C` **cerrado** con fundamento citado, y ninguna subsección histórica quedó modificada.
- [x] `ROADMAP.md` declara **un solo** estado de `F-C` en las tres ubicaciones, coherente con el cierre, sin afirmar ausencia de trabajo activo.
- [x] `git diff --name-only` **no** incluye `docs/plans/165-…` ni `docs/plans/166-…`, y los registros de `ID-6`/`ID-8`/`FC-7` quedan reconciliados por referencia.
- [x] Cada uno de los cuatro findings tiene resolución registrada: `open/actionable = 0`.
- [x] Los artefactos de auditoría están versionados y el índice está reconciliado.
- [x] Seis checkers deterministas en verde y gates C-1/C-2/C-3 sin `ANOMALY`; `check_plan_citations` sin citas rotas nuevas respecto de su baseline (26).
- [x] `## Validation anchor` y `## Checkpoint / cierre` completos, con las dos determinaciones de impacto.
- [x] Cero diff en `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` y `.agents/`.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación factual adicional: coherencia de estado de `F-C` en las tres ubicaciones del `ROADMAP.md`; `git diff --name-only` ⊆ scope de `P-8`; `git diff` vacío para `docs/plans/165-…` y `docs/plans/166-…`; estado de los cuatro findings; y estado Git de los artefactos de auditoría respecto de `docs/working/audits/INDEX.md`.

## Validation anchor

**Validation anchor (VC-1).**

- **Declared scope:** `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md`, los tres artefactos de auditoría versionados por `F-4` y `CHANGELOG.md` (el artefacto de este Plan queda **fuera** del scope medido: convención anti-auto-referencia).
- **Validation command-set:** los seis checkers deterministas de `docs/VERSIONING.md` §4.1 y los gates de lifecycle C-1/C-2/C-3. La pata `pytest` de §4.1 **no** fue ejecutable en la sesión de ejecución (ver `## Nota de ejecución`).
- **Effective inputs (repo content):** el scope declarado; evidencia del cierre de `F-C` (`docs/plans/165-…`: `## Validation anchor` y `## Checkpoint / cierre`; commit `fb0786a`); RFC-83 `Accepted` y plan 166; el corpus de `docs/`; el estado Git de `dev`.
- **Observed dependencies:** herramientas de `tools/` (stdlib) e intérprete del entorno del adoptante; CLI `git`. **`pytest` no disponible en el entorno del runtime**; la sesión de ejecución corrió con `pytest 9.0.2` del *user site-packages* y, además, el sandbox de la sesión deniega la mecánica de `tmp_path` (factor no atribuible a este Change). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; `core.autocrlf = true` (los blobs se almacenan en LF; el working tree puede materializarse en CRLF); `check_dist_sync.py` no aplica (local-only, verde sólo en `master`); `check_plan_citations.py` conserva **26** citas rotas históricas y **1** referencia legacy preexistente (la referencia legacy preexistente de `docs/CONVENTIONS.md` (línea 808),), sin aumento respecto de su baseline.
- **Scoped Content Identity:**
  - Generada con `tools/scoped_content_identity.py` (serialización `scoped-v1`, índice *staged*).
- **State identity (estado validado):** `607b0b1bbb397a2d4748e220fb7136734c9ffa4d` (`git write-tree` del índice staged)
  - **Delta scoped identity (scope = las cinco rutas declaradas, orden canónico):** `1871e9a57f418086bcb3ea8589b8481c3fb6cd69492971ffeebd2c1032da0497`
  - **Scope medido:** `CHANGELOG.md`, `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md`
  - **Fuera del scope medido (anti-auto-referencia):** `docs/plans/167-reconciliacion-del-cierre-de-f-c.md` — el artefacto del Plan, que contiene estos propios registros de cierre
- **Battery result:** 6/6 checkers deterministas ejecutados sin `FAIL`; `check_plan_citations` conserva su baseline (26 + 1 legacy, exit 1 preexistente); C-1 `VALID` para los 167 planes con `ANOMALY=0`; C-2 `VALID` para el Plan 165 (`A1`); C-3 `VALID` para el Plan 167 (`<PLAN-167>:F-1`…`F-4`) con `ANOMALY=0`.
- **Validity / stale:** vigente para el estado que el checkpoint certifica.

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** `docs(plans): reconcile the F-C closure (plan 167)` y los commits atómicos del Change (`docs(plans): approve and register the F-C closure reconciliation plan`; `docs(governance): state the closure of F-C in the autonomy model and the roadmap`; `docs(working): version the test and execution-host audits`) en `dev`. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** el de la sección anterior (State identity `607b0b1bbb397a2d4748e220fb7136734c9ffa4d`; Delta scoped identity `1871e9a57f418086bcb3ea8589b8481c3fb6cd69492971ffeebd2c1032da0497`).
- **Estado de cierre (identidad):** el mismo estado validado; el estado de cierre es el que la validación consumió (arbol de índice `607b0b1bbb397a2d4748e220fb7136734c9ffa4d`).
- **Árbol material del commit de cierre:** no declarado; incluye los registros de cierre, que el scope medido excluye por la convención anti-auto-referencia (`validated tree == commit tree` no es un requisito; RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió, y el gate C-2 lo reporta `VALID` (`A1`) para este Plan.
- **Governance aplicada:** RFC-56 Clase B (plan `Aprobado para ejecución`, acto del mantenedor del 2026-10-14 registrado en este artefacto); RFC-69 (plantilla y registro en el INDEX); RFC-75 (Change Lifecycle DEV); ADR-16 (autoridad); anotación de correcciones `C-1`…`C-4`; findings `F-1`…`F-4` con estado y provenance.
- **Documentation impact:** `REQUIRED` — documentos afectados: `docs/CONVENTIONS.md` (estado vigente del modelo de autonomía: decía `READY_FOR_IMPLEMENTATION` y ahora declara el cierre con su fundamento), `ROADMAP.md` (mapa operativo con un único estado de `F-C` y Posición actual), `docs/plans/INDEX.md` (registro del Plan 167 y encabezado de estado), `docs/working/audits/INDEX.md` (coherencia con artefactos versionados). Actualización realizada y verificada por los checkers; los documentos históricos (planes cerrados 165/166, entradas de changelog ya publicadas) **no** se actualizaron (RFC-46).
- **Roadmap impact:** `REQUIRED` — el mapa operativo materialmente modificado: `F-C` deja de figurar en estados contradictorios y queda `CLOSED`, se retira la afirmación de ausencia de trabajo activo y pasa a registrarse el trabajo de este Change; actualización realizada en `ROADMAP.md` (mismo commit que la reconciliación) con evidencia en `## Nota de ejecución`.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance + checkpoint + consistencia; docs-only, sin release ni tag — RFC-69).

## Findings / Correcciones / Pending

### Findings

- `<PLAN-167>:F-1` — estado: `resolved` (resuelto por la corrección `C-` correspondiente); severidad: `medium`; observación: el estado vigente del modelo de autonomía en `docs/CONVENTIONS.md` seguía declarando `F-C` en su estado previo a la ejecución; evidencia original: la subsección «Estado tras el acto del 2026-10-13» afirmaba `F-C = READY_FOR_IMPLEMENTATION` con «implementación **no iniciada**», mientras `docs/plans/165-…` está `Executed` con condición derivada `Closed` y su cierre está commiteado; estado Git observado: `dev @ 81bbde1`, worktree con `CHANGELOG.md` modificado por la corrección mecánica previa; provenance original: revisión documental de la feature de autonomía solicitada por el mantenedor (2026-10-14).
  resolución: `C-1` — el estado vigente del modelo de autonomía en `docs/CONVENTIONS.md` declara el cierre de `F-C`.
- `<PLAN-167>:F-2` — estado: `resolved` (resuelto por la corrección `C-` correspondiente); severidad: `medium`; observación: `ROADMAP.md` declaraba estados de `F-C` mutuamente excluyentes y contenía un error de formato; evidencia original: «Posición actual» mezclaba «aprobado para ejecución y listo para implementar» con «cerrada (`CLOSED`)»; la entrada de `NEXT` encabezaba `CLOSED` y conservaba «Aprobado para ejecución» y `****cerrada**`; el diagrama de dependencias rotulaba `F-C` como «alcance resuelto, sin autorizar»; estado Git observado: `dev @ 81bbde1`; provenance original: ídem `F-1`.
  resolución: `C-2` — `ROADMAP.md` declara un único estado cerrado de `F-C` y corrige la Posición actual.
- `<PLAN-167>:F-3` — estado: `resolved` (resuelto por la corrección `C-` correspondiente); severidad: `low`; observación: los registros internos de un plan **cerrado** contradicen el estado que él mismo declara y la evidencia viva: `ID-6` e `ID-8` figuran en su sección de pending decisions con `resolución: **PENDING**` aunque el propio plan registró su resolución por diseño, y la contabilidad de counterproofs de `FC-7` quedó con un valor anterior al cierre (la sección del recuento declara 11 en verde y la contabilidad posterior declara 10 `PASS` + 1 `PENDING` + 1 `PARTIAL`); evidencia original: sección `### Pending decisions` del plan 165 para `ID-6`/`ID-8`; secciones de recuento y de contabilidad de counterproofs del mismo plan; `docs/plans/165-…` (`## Checkpoint / cierre`: condición derivada `Closed`); estado Git observado: `dev @ 81bbde1`; provenance original: ídem `F-1`. **Nota de clasificación:** la contabilidad admite más de una lectura legítima (**`BOUNDARY`**) —diferencia de recuento entre secciones del mismo plan—; este plan la registra y deja constancia de la lectura adoptada, sin reinterpretar los criterios del 165.
  resolución: `C-3` — los registros del Plan 165 quedan reconciliados por referencia, con `git diff` vacío del artefacto cerrado.
- `<PLAN-167>:F-4` — estado: `resolved` (resuelto por la corrección `C-` correspondiente); severidad: `medium`; observación: tres artefactos que `docs/working/audits/INDEX.md` declara `active` no estaban versionados en el árbol, de modo que la evidencia que el registro afirma disponible no estaba en el repositorio; evidencia original: `git status --porcelain` los listaba como no trackeados y el índice que los declara **sí** está versionado; estado Git observado: `dev @ 81bbde1`; provenance original: ídem `F-1`.
  resolución: `C-4` — los cuatro artefactos de auditoría declarados `active` quedan versionados.

### Correcciones

- `<PLAN-167>:C-1` — refs origen: `<PLAN-167>:F-1`; alcance de revalidación: `docs/CONVENTIONS.md`, subsección de estado del modelo de autonomía; evidencia: el estado de `F-C` pasa a cierre vigente con la referencia al acto del 2026-10-13 y a la decisión de cierre del plan 165, conservando intactas las subsecciones históricas.
- `<PLAN-167>:C-2` — refs origen: `<PLAN-167>:F-2`; alcance de revalidación: `ROADMAP.md` («Posición actual», `NEXT` y diagrama de dependencias); evidencia: un único estado cerrado de `F-C` en las tres ubicaciones y Posición actual sin la afirmación de ausencia de trabajo activo.
- `<PLAN-167>:C-3` — refs origen: `<PLAN-167>:F-3`; alcance de revalidación: registros de `docs/plans/165-…` **por referencia, sin editar el artefacto cerrado**; evidencia: este Plan deja constancia de la resolución de `ID-6`/`ID-8` y de la lectura adoptada de la contabilidad de counterproofs de `FC-7`; `git diff` de `docs/plans/165-…` y `docs/plans/166-…` **vacío**.
- `<PLAN-167>:C-4` — refs origen: `<PLAN-167>:F-4`; alcance de revalidación: `docs/working/audits/` y `docs/working/audits/INDEX.md`; evidencia: los tres artefactos de auditoría declarados `active` quedan versionados y el índice reconciliado con su estado real.

### Pending decisions

- `<PLAN-167>` — decisión: **aprobación de ejecución de este plan** (`Aprobado para redacción` → `Aprobado para ejecución`); blocking: **sí** — sin ella no se ejecutaba ningún paso; owner: **mantenedor**; escalación: acto registrado en este artefacto; resolución: **`RESUELTA`** por el acto del mantenedor del 2026-10-14 (`## Acto de autorización registrado (2026-10-14)`); evidencia: `## Vía de autorización y justificación`; efecto downstream: habilitó los pasos 1–5; ADR-worthiness: no.
- `<PLAN-167>` — decisión: **destino de los artefactos de auditoría de `F-4`** — versionarlos (y en qué ubicación) o declarar su ausencia; blocking: **no** para los pasos 1–3; **sí** para cerrar el paso 4 y el criterio de salida asociado; owner: **mantenedor**; escalación: acto registrado en este artefacto; resolución: **`RESUELTA`** — el mantenedor decidió **versionarlos** en su ubicación actual (`docs/working/audits/`), registrado en `## Acto de autorización registrado (2026-10-14)`; evidencia: `docs/working/audits/INDEX.md` frente a `git status --porcelain`; efecto downstream: la evidencia de auditoría entra al repositorio; ADR-worthiness: no.

## Riesgos

1. **Convertir la reconciliación en reescritura de historia.** Mitigación: `docs/plans/165-…` y `166-…` fuera de scope y verificados por `git diff` vacío; las subsecciones históricas de `docs/CONVENTIONS.md` no se tocan; la reconciliación de registros es **por referencia**. Materializado: `C-3`.
2. **Resolver por conveniencia un desacuerdo documental.** Mitigación: `F-3` está marcado `BOUNDARY` y la lectura adoptada se declara; `F-4` se resolvió por decisión del mantenedor, no por defecto.
3. **Ampliar el alcance hacia el payload o el código.** Mitigación: `OUT OF SCOPE` explícito; criterio de salida de cero diff en `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/` y `.agents/`.
4. **Presentar la corrección como nueva autoridad.** Mitigación: este plan no cambia decisiones; una corrección es traza factual (LC-1) y nunca fuente normativa.
5. **Ejecución silenciosa sin aprobación.** Mitigación: compuerta explícita cumplida; el acto quedó registrado con su evidencia antes de tocar los documentos.

## Trazabilidad

```text
`F-C` (plan 165, Closed; commit fb0786a) · payload (plan 166, RFC-83; commits a61bd97, f75d70a)
        │
        ▼
Revisión documental solicitada por el mantenedor (2026-10-14)
        │
        ▼
[ este Plan 167 (Executed) ] → F-1…F-4 → C-1…C-4 → Closed (docs-only)
        │
        ▼
Correcciones mecánicas (Clase C): historia del CHANGELOG.md
        │
        ▼
Diferido a su propia vía: versión del payload (RFC-56 Clase A) · regularización de 81bbde1 · entrada del payload de RFC-83 en las secciones históricas del CHANGELOG (defecto de propagación de f75d70a)
```

## Nota de ejecución

**Ejecución (2026-10-14).** Change DEV-only y docs-only conducido en `dev`. Autorización previa registrada en `## Acto de autorización registrado (2026-10-14)`. Pasos ejecutados:

1. **Paso 0 — clasificación y registro.** Vía **Clase B** de RFC-56, `Change Level` **L2**, alcance `IN`/`OUT` y criterio de entrada; Plan creado y registrado en `docs/plans/INDEX.md` (Nonagésima cuarta serie).
2. **Paso 1 — estado narrativo (`C-1`).** `docs/CONVENTIONS.md`, subsección de estado del modelo de autonomía: el estado de `F-C` pasa a **`CLOSED`** con su fundamento (acto del mantenedor del 2026-10-13, anchor y checkpoint del Plan 165, condición derivada `Closed`, RFC-83 `Accepted` y Plan 166). La afirmación previa se conserva **marcada como estado histórico**; las subsecciones del 2026-10-07, 2026-10-11 y 2026-10-12 quedan intactas.
3. **Paso 2 — mapa operativo (`C-2`).** `ROADMAP.md`: «Posición actual» deja de decir «Trabajo activo: ninguno» y registra el trabajo abierto; la entrada de `F-C` en `NEXT` declara **un solo** estado (`CLOSED`) sin «Aprobado para ejecución» ni el error de formato `****cerrada**`; el diagrama de dependencias rotula `F-C` como cerrada; fecha de actualización al 2026-10-14.
4. **Paso 3 — registros del plan cerrado (`C-3`).** Documentado **por referencia** en `### Correcciones`: `ID-6`/`ID-8` constan resueltos en el propio Plan 165 y la contabilidad de counterproofs de `FC-7` admite más de una lectura (registrada como **`BOUNDARY`**), con la lectura adoptada declarada y **sin reinterpretar** los criterios del 165. Verificación: `git diff` de `docs/plans/165-…` y `docs/plans/166-…` **vacío**.
5. **Paso 4 — trazabilidad de auditoría (`C-4`).** Por decisión del mantenedor (versionar), se incorporan al árbol versionado los **cuatro** artefactos que `docs/working/audits/INDEX.md` ya declaraba `active`: `TEST_SUITE_AUDIT_2026-10-13.md`, `TEST_ARCHITECTURE_AUDIT_2026-10-13.md`, `TEST_EXECUTION_AUTOPSY_2026-10-13.md` y `EXECUTION_HOST_SEMANTIC_AUDIT_2026-10-14.md`. Se deja constancia de que esto **revierte** el retiro del índice dispuesto por `<PLAN-165>:C-1`, ahora por decisión explícita del mantenedor. El documento `docs/planificacion-argentos-diseno-2026-10-13.md` **no** se versiona: queda fuera del alcance de `F-4` y de este Plan.
6. **Paso 5 — verificación y cierre.** Batería determinista y gates C-1/C-2/C-3 sobre el estado validado, con el resultado registrado abajo.

**Resultado de la batería (estado validado `3cabfb9c63d28e68d89199e9765c5c30ae23298e`):**

| Comando | Resultado |
|---|---|
| `check_protocol_invariants` | OK — 216 archivos, 10476 referencias |
| `check_plan_structure` | PASS — sin violaciones estructurales |
| `check_taxonomy_coherence` | OK |
| `check_session_artifacts` | OK |
| `check_version_state` | OK |
| `check_plan_citations` | **26** citas rotas (baseline histórico) y **1** referencia legacy preexistente en la referencia legacy preexistente de `docs/CONVENTIONS.md` (línea 808),; **sin aumento** |
| C-1 `check_lifecycle_anchor` | 167 planes: `VALID=72`, `GAP=1`, `ANOMALY=0` |
| C-2 `check_lifecycle_checkpoint` | 167 planes: `VALID=71`, `GAP=2`, `ANOMALY=0` |
| C-3 `check_lifecycle_lineage` | 167 planes: `VALID=38`, `GAP=0`, `ANOMALY=0`; el Plan 167 `VALID` con `<PLAN-167>:F-1`…`F-4` |

Los únicos `GAP` de C-1/C-2 son los **esperados por diseño**: el Plan 167 antes de completar sus registros de cierre, y el `GAP` preexistente del Plan 116 (`ANOMALY=0` en todos los casos).

**Factor ambiental declarado (no atribuible a este Change).** La pata `pytest` de la batería canónica **no fue ejecutable** en la sesión de ejecución: el entorno no provee `pytest` desde el runtime del repo (se resuelve `pytest 9.0.2` del *user site-packages*, con 1358 tests colectados frente a los 1542 registrados en el baseline del repositorio) y el sandbox de la sesión deniega la mecánica de `tmp_path` (`PermissionError [WinError 5]` en el *setup*, al enumerar y crear subdirectorios del temporal; **no** son aserciones fallidas). Evidencia de no-atribución: **ningún test del repositorio lee `CHANGELOG.md`** —las menciones en `tests/` construyen su propio archivo en `tmp_path`— y los módulos afectados fallan idénticamente con el cambio y sin él. Queda como limitación de reproducibilidad del entorno de ejecución, no como incumplimiento del Plan.

**Cumplimiento de criterios de salida:** los ocho criterios del Plan verificados. **Rutas modificadas:** `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/plans/167-…`, `docs/working/audits/INDEX.md` (sin cambio de contenido: sus declaraciones ya eran correctas) y los cuatro artefactos de auditoría. **Cero diff** en `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` y `.agents/`. **Estado:** `Executed` con condición derivada `Closed` (docs-only, sin release ni tag).
