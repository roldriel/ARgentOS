# Plan 169 — Regularización de `81bbde1` y reconciliación de pending decisions cerradas

**Status:** Executed
**Fecha:** 2026-10-14
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; **Clase B** de RFC-56. El Change es DEV-only y no toca `protocol/.agents/`: regulariza por referencia un cambio de `runtime/` ya publicado y reconcilia registros de gobernanza. La aclaración de la vía de acción directa se escribe en la **capa operacional DEV** (`.agents/`), no en el payload; si tocara `protocol/.agents/` sería Clase A y requeriría RFC `Accepted`)
**Clase:** — (no aplica: el Change no modifica `protocol/.agents/`)
**Change Level:** **L2** (`max(coordination=2, scope=2, architectural impact=0, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: **2** — regulariza un cambio publicado, reconcilia registros de cinco planes cerrados y registra una decisión de gobernanza operacional. *scope*: **2** — `docs/plans/`, `docs/plans/INDEX.md` y `.agents/AGENTS.md`. *architectural impact*: **0** — no cambia modelo, contrato ni capacidad; la aclaración no crea autoridad. *release impact*: **0** — DEV-only, sin versión ni tag. *duration/complexity*: **2** — varios registros y una aclaración operacional que debe evitar ambigüedad.
**Depende de:** plan 168 (`Executed`/`Closed`/`Released`), plan 167 (`Executed`/`Closed`), plan 166 (`Executed`/`Closed`), plan 165 (`Executed`/`Closed`), plan 164 (`Executed`/`Closed`), plan 161 (`Executed`/`Closed`), RFC-75 (Change Lifecycle DEV)
**Origen:** decisión del mantenedor (2026-10-14) que confirmó las tres afirmaciones sobre la vía de acción directa y pidió **un solo plan pequeño** que cierre los dos puntos accionables del inventario de pendientes (ver `## Acto de autorización registrado (2026-10-14)`)
**Work type:** `GAP` — el Plan no cambia ninguna decisión de gobernanza del Change: regulariza y reconcilia registros; su única decisión es la registrada por el acto del mantenedor

## Acto de autorización registrado (2026-10-14)

| Campo | Contenido |
|---|---|
| **Decisión** | Autorización de este Plan y **confirmación de las tres afirmaciones** sobre la vía de acción directa del mantenedor: (1) una instrucción directa del mantenedor **autoriza** un cambio; (2) esa instrucción debe quedar **declarada con la forma que el repo ya define** (el mensaje del commit como primer artefacto de un cambio sin plan, `RFC-75` Mecanismo 1), no sólo implícita; (3) eso debe **escribirse en `.agents/AGENTS.md`** como **aclaración**, no como regla nueva |
| **Autoridad** | **Mantenedor** |
| **Fecha efectiva** | **2026-10-14** |
| **Alcance autorizado** | Regularizar `81bbde1` por referencia; reconciliar por referencia las pending decisions obsoletas de los planes 161, 164 y 165; registrar la decisión de las tres afirmaciones; y escribir la aclaración correspondiente en `.agents/AGENTS.md` |
| **Artefacto designado** | **este Plan** (`docs/plans/169-regularizacion-de-81bbde1-y-reconciliacion-de-pendientes.md`) |
| **Estado** | **Aprobado para ejecución** — terminología exacta de `docs/VERSIONING.md` §7 |
| **Evidencia** | Pedido directo del mantenedor (2026-10-14): «Perfecto, confirmo las tres afirmaciones», tras la propuesta de un solo plan pequeño que cierre los puntos 1 y 2 con la decisión de fondo |
| **Límite explícito** | La autorización **no** permite reescribir el commit `81bbde1` ni el tag `12.1.0` (RFC-46); **no** permite editar los planes 161/164/165 cerrados (`.agents/AGENTS.md`, regla 5); **no** toca `protocol/.agents/`, `dist/`, `runtime/`, `tools/` ni `tests/`; y la aclaración **no** crea autoridad, mecanismo, estado ni excepción nueva |

## Vía de autorización y justificación

Es **Clase B** (mejora documental compatible, RFC-56): el Change modifica **lo que afirman documentos vigentes** (registros de gobernanza y la capa operacional DEV) sin cambiar el significado del protocolo, sin tocar el payload y sin alterar ninguna decisión ya registrada. Su vía es por tanto **plan `Aprobado para ejecución`** con la justificación documentada que `docs/VERSIONING.md` §4 paso 1 pide.

**No es Clase C:** una corrección mecánica exige *cero* cambio de significado, y aquí se decide y se registra cómo se autoriza y se declara una vía de cambio, además de reconciliar registros con criterio editorial. **No es Clase A:** no hay cambio de modelo conceptual ni de contratos, y `protocol/.agents/` no se toca.

## Objetivo

Cerrar los dos puntos accionables del inventario de pendientes, sin reescribir nada publicado:

1. **Regularizar `81bbde1`**: un cambio de `runtime/` ejecutado bajo instrucción directa del mantenedor, ya publicado en `master` y en el tag `12.1.0`, cuyo mensaje declara su propia falta de artefacto de autorización. El Plan lo regulariza **por referencia**, con su evidencia, y registra su finding.
2. **Reconciliar las pending decisions obsoletas** de planes ya cerrados: hoy tres planes registran decisiones como `PENDING` que ya fueron resueltas por actos posteriores, de modo que quien los lea ve pendiente lo que está cerrado. La reconciliación se hace **por referencia**, sin editar los artefactos cerrados.
3. **Registrar la decisión de fondo** sobre la vía de acción directa y escribir su **aclaración** en la capa operacional DEV, para que el hueco no se repita.

El Plan **no** cambia ninguna decisión de gobernanza, **no** reescribe historia publicada, **no** toca el payload y **no** crea mecanismo, estado, autoridad ni excepción nueva.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | El mantenedor confirmó las tres afirmaciones sobre la acción directa y pidió un solo plan pequeño que cierre los puntos 1 y 2 con esa decisión incluida | humano | `## Acto de autorización registrado (2026-10-14)` |
| `P-2` Confianza de intención | `HIGH` — las tres afirmaciones fueron explicitadas y confirmadas; el alcance quedó acotado a tres entregables y los límites están declarados | agente | `INTENT_CONFIDENCE` sobre el pedido |
| `P-3` Conjunto de contexto | `git show 81bbde1`; `docs/working/audits/EXECUTION_HOST_OBSERVATION_PILOT_2026-10-14.md`; `docs/plans/161-…`, `164-…` y `165-…` (secciones de pending decisions); `docs/plans/167-…` (correcciones por referencia); `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/authority.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md` (§3, §4, §7); estado Git de `dev` y `master` | agente | lecturas directas de esta sesión |
| `P-4` Derivabilidad | `derivable` — el commit, su contenido y su estado de publicación son hechos de Git; las siete pending y el artefacto que las resolvió están citados uno por uno; la aclaración de la vía ya está implícita en el vocabulario vigente (`direct maintainer action`, `RFC-75` Mecanismo 1), de modo que el Plan la hace explícita y no la crea. Señales: **ninguna** bloqueante; `GAP` del Plan 116 declarado fuera de alcance | agente | `git show`; `## Findings / Correcciones / Pending`; `.agents/workflows/change-lifecycle.md:1. Change detection and classification` |
| `P-5` `work_type` | `GAP` — la regularización y la reconciliación no cambian ninguna decisión de gobernanza; ningún valor se inventa | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type` |
| `P-6` Conocimiento vigente | Planes 161, 164, 165, 166, 167 y 168 `Executed` (165–168 con condición `Closed`; 168 además `Released = TRUE`); `docs/plans/INDEX.md`, `CHANGELOG.md` y `ROADMAP.md` `active`; `.agents/AGENTS.md` es la capa operacional DEV vigente | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | APPLIES: RFC-56 (Clase B), RFC-75 (`Mecanismo 1` registro del intake; `Mecanismo 15` ausencia de registros no es invalidez), RFC-69 (registro), ADR-16 (autoridad), VC-1/GC-1/LC-1/PC-1, `docs/VERSIONING.md` §3/§4/§7/§10. NOT_APPLICABLE: RFC-46 en cuanto a reescribir historia — este Plan **no** la reescribe, la referencia. NOT_APPLICABLE: RFC-56 Clase A (no hay efecto de payload) y Clase C (no es mecánico) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **mantenedor**. Rutas que este Plan escribe: `docs/plans/169-…`, `docs/plans/INDEX.md` y `.agents/AGENTS.md`. **No** escribe `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` ni los planes cerrados 161/164/165/166/167/168 | **humano** | acto registrado; `.agents/AGENTS.md` (reglas 5 y 9) |

## Criterio de entrada

- [x] Acto del mantenedor registrado (2026-10-14): tres afirmaciones confirmadas y alcance acotado.
- [x] `81bbde1` identificado como hecho de Git: commit de `perf(runtime)`, ancestro de `master` y del tag `12.1.0`, sin entrada en el changelog (no toca payload).
- [x] Las siete pending obsoletas identificadas con su artefacto de resolución: `ID-1`, `ID-3`, `ID-5`, `ID-6` e `ID-8` del Plan 165; la revisión de alcance de `F-C`/Etapa B del Plan 161; y las decisiones de implementación de `F-C` del Plan 164.
- [x] `.agents/AGENTS.md` vigente leído y su regla 2 identificada como el lugar de la aclaración.
- [x] Batería canónica ejecutada con su resultado registrado en la `## Nota de ejecución`.

## Alcance

### IN SCOPE

1. **Regularización de `81bbde1`** por referencia, con su finding, su evidencia y la declaración de que se ejecutó bajo instrucción directa del mantenedor.
2. **Reconciliación por referencia** de las siete pending decisions obsoletas, con el artefacto que resolvió cada una.
3. **Registro de la decisión de fondo** (las tres afirmaciones) y su **aclaración en `.agents/AGENTS.md`**, en la regla de autorización ya existente.
4. Registro de este Plan en `docs/plans/INDEX.md` y sus propios registros de cierre.

### OUT OF SCOPE

- **Reescribir** `81bbde1`, el tag `12.1.0`, `master` o cualquier historia publicada (RFC-46).
- **Editar** los planes 161, 164, 165, 166, 167 y 168 (cerrados; `.agents/AGENTS.md`, regla 5). La reconciliación es **por referencia**.
- **El `GAP` del Plan 116**: es un aviso **advisory** de C-2 sobre un plan histórico cerrado (`multiple declared revalidations … ambiguity`). La regla del repo es explícita: un `GAP` no es una invalidación y no requiere corrección; se declara aquí y no se toca.
- **`docs/planificacion-argentos-diseno-2026-10-13.md`**: decisión del mantenedor ya tomada — se deja como está, sin versionar y sin inferir nada sobre ella.
- **Etapa C**: es la fase siguiente del roadmap (capacidad nueva, `LATER`), no deuda de cierre; requiere su propia decisión de alcance.
- **Modificar** `protocol/.agents/`, `dist/`, `runtime/`, `tools/` y `tests/`.
- **Crear** autoridad, excepción, estado, mecanismo, registry o checker nuevos.

### DEPENDENCIES

```text
81bbde1  = publicado en master y en el tag 12.1.0 (cambio de runtime/, sin efecto de payload)
Planes 161/164/165 = Executed/Closed; sus pending quedaron resueltas por actos y planes posteriores
.agents/AGENTS.md  = capa operacional DEV vigente (lugar de la aclaración)
RFC-56   = Clase B (plan `Aprobado para ejecución`); Clase A sólo si se tocara protocol/.agents/ (no ocurre)
```

## Entregables

1. Este Plan, registrado en `docs/plans/INDEX.md`.
2. `## Findings / Correcciones / Pending` con: el finding de `81bbde1` y su corrección por referencia; el finding de las pending obsoletas y su reconciliación; y la decisión de fondo registrada.
3. `.agents/AGENTS.md`: aclaración de la vía de acción directa dentro de la regla de autorización existente.
4. Registros de cierre: `## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`, con las dos determinaciones de impacto.

## Pasos

1. **Paso 0 — clasificación y registro.** Vía **Clase B**, `Change Level` **L2**, alcance y criterio de entrada; creación del Plan y registro en `docs/plans/INDEX.md`.
2. **Paso 1 — regularizar `81bbde1`.** Registrar en `### Findings` el vacío de declaración de autorización, con la observación, la evidencia (commit, informe del piloto, estado Git) y su provenance; y en `### Correcciones` la regularización **por referencia**, declarando que el cambio se ejecutó bajo instrucción directa del mantenedor y que **no** se reescribe.
3. **Paso 2 — reconciliar las pending.** Registrar en `### Correcciones` el estado real de las siete decisiones, cada una con el artefacto que la resolvió, sin editar los planes cerrados.
4. **Paso 3 — aclaración operacional.** En `.agents/AGENTS.md`, dentro de la regla de autorización existente, hacer explícito que una **instrucción directa del mantenedor autoriza** el cambio que nombra, que su declaración va en el primer artefacto del cambio (mensaje del commit cuando no hay plan, RFC-75 Mecanismo 1), y que **no** otorga autorización más allá de lo nombrado ni exime de RFC-56 cuando hay efecto de payload. **Sin** crear regla, estado ni excepción nueva.
5. **Paso 4 — verificación y cierre.** Batería canónica y gates C-1/C-2/C-3; `## Validation anchor`; `## Checkpoint / cierre` con las dos determinaciones; `## Nota de ejecución`; commit atómico en `dev`.

## Delegación agentiva

No se declara delegación: la sección no lleva `**Task:**` (ausencia declarada para el host). El Change es documental y la decisión de fondo ya fue tomada por el mantenedor.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change es DEV-only y docs-only; no prevé `network`, `remote_git`, `install`, `destructive` ni `write_outside_project` | — (ausencia declarada) | `authorized` |

## Criterios de salida

- [x] `81bbde1` está regularizado **por referencia**, con su finding y su evidencia, y `git diff` de `81bbde1` y del tag `12.1.0` **vacío** (nada reescrito).
- [x] Las siete pending obsoletas quedan reconciliadas por referencia, cada una con el artefacto que la resolvió; `git diff` de los planes 161/164/165 **vacío**.
- [x] `.agents/AGENTS.md` aclara la vía de acción directa dentro de la regla existente, sin crear regla, estado, autoridad ni excepción nueva.
- [x] La decisión de fondo queda registrada en `### Pending decisions` como **resuelta** por el acto del 2026-10-14, con sus tres afirmaciones y su fundamento.
- [x] Batería canónica en verde y gates C-1/C-2/C-3 sin `ANOMALY`; `check_plan_citations` sin citas rotas nuevas respecto de su baseline (26).
- [x] `## Validation anchor` y `## Checkpoint / cierre` completos, con las dos determinaciones de impacto.
- [x] Cero diff en `protocol/.agents/`, `dist/`, `runtime/`, `tools/` y `tests/`.

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

Verificación factual adicional: `git diff --name-only` ⊆ scope de `P-8`; `git diff` vacío para `81bbde1`, el tag `12.1.0` y los planes 161/164/165; y que `.agents/AGENTS.md` conserve intactas sus diez reglas fundamentales (sólo se agrega texto a una de ellas).

## Validation anchor

**Validation anchor (VC-1).**

- **Declared scope:** `docs/plans/INDEX.md` y `.agents/AGENTS.md` (el artefacto de este Plan queda **fuera** del scope medido: convención anti-auto-referencia).
- **Validation command-set:** los seis checkers deterministas de `docs/VERSIONING.md` §4.1 y los gates de lifecycle C-1/C-2/C-3. La pata `pytest` de §4.1 **no** fue ejecutable en la sesión de ejecución (ver `## Nota de ejecución`).
- **Effective inputs (repo content):** el scope declarado; el commit `81bbde1` y su informe de piloto; los planes 161, 164 y 165 (leídos, **no** modificados); el tag `12.1.0`; el estado Git de `dev`.
- **Observed dependencies:** herramientas de `tools/` (stdlib) e intérprete del entorno del adoptante; CLI `git`. `pytest` no disponible en el entorno del runtime. Sin red.
- **Environmental factors:** Windows 11 + PowerShell; `core.autocrlf = true` (los blobs se almacenan en LF; el working tree puede materializarse en CRLF); `check_dist_sync.py` no aplica (local-only, verde sólo en `master`); `check_plan_citations.py` conserva **26** citas rotas históricas y **1** referencia legacy preexistente, sin aumento.
- **Scoped Content Identity:**
  - **State identity (estado validado):** `5889503fcf8eed8e4caccd5bcce709e4db61c81e` (árbol del commit del Change `74c9ebb`)
  - **Delta scoped identity (scope = las dos rutas declaradas, orden canónico):** `521bf137462657844fb27b0120f40b00cfe399f8f271c6e99732bb2559568cae`
- **Battery result:** 6/6 checkers deterministas en verde; `check_version_state` OK; C-1/C-2/C-3 sin `ANOMALY` (los `GAP` son los de los registros propios antes de completarse y el preexistente del Plan 116).
- **Validity / stale:** vigente.

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** el commit del Change en `dev` (`docs(plans): regularize 81bbde1 and reconcile stale pending decisions`), que incluye el Plan, el registro en el INDEX y la aclaración de `.agents/AGENTS.md`. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** el de la sección anterior (State identity `5889503fcf8eed8e4caccd5bcce709e4db61c81e`; Delta scoped identity `521bf137462657844fb27b0120f40b00cfe399f8f271c6e99732bb2559568cae`).
- **Estado de cierre (identidad):** el mismo estado validado (`5889503fcf8eed8e4caccd5bcce709e4db61c81e`), por correspondencia con el anchor aplicable.
- **Árbol material del commit de cierre:** no declarado; incluye los registros de cierre, que el scope medido excluye por la convención anti-auto-referencia (`validated tree == commit tree` no es un requisito; RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió.
- **Governance aplicada:** RFC-56 Clase B (plan `Aprobado para ejecución`, acto del mantenedor del 2026-10-14); RFC-75 (Mecanismo 1 registro del intake; Mecanismo 7 checkpoints); RFC-69 (registro en el INDEX); ADR-16; findings `F-1`/`F-2` con correcciones `C-1`…`C-3`; decisión de fondo registrada y resuelta.
- **Documentation impact:** `REQUIRED` — documentos afectados y actualizados: `.agents/AGENTS.md` (la regla de autorización hace explícita la vía de instrucción directa, con sus límites) y `docs/plans/INDEX.md` (registro del Plan y encabezado de estado). Los documentos históricos (planes 161/164/165/166/167/168 cerrados y el commit `81bbde1`) **no** se actualizaron (RFC-46); su reconciliación es por referencia.
- **Roadmap impact:** `NOT_REQUIRED` — el Change no crea, completa, cancela, reclasifica ni re-prioriza trabajo del mapa operativo: regulariza un cambio ya publicado, reconcilia registros de planes cerrados y aclara una regla operacional existente. Ninguno de los tres mueve el mapa de trabajo futuro.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance aplicada + checkpoint + consistencia; docs-only, sin release ni tag — RFC-69).

## Findings / Correcciones / Pending

### Findings

- `<PLAN-169>:F-1` — estado: `open`; severidad: `medium`; observación: el commit `81bbde1` (`perf(runtime): reuse run() observation in iterate`) modificó `runtime/orchestrator/host.py` y se publicó en `master` y en el tag `12.1.0` **sin artefacto de autorización** —ni plan `Aprobado para ejecución` ni RFC—; su propio mensaje declara el hueco («the pilot itself was executed under a direct instruction with no plan artifact, so this commit carries no plan ref»); evidencia original: `git show --stat 81bbde1` (3 archivos: `runtime/orchestrator/host.py`, el informe del piloto y `docs/working/audits/INDEX.md`); `git merge-base --is-ancestor 81bbde1 master` verdadero y ancestro del tag `12.1.0`; el `CHANGELOG.md` no menciona el cambio; estado Git observado: `dev @ 2cb0d10`, `master @ 45809c1`; provenance original: inventario de pendientes solicitado por el mantenedor (2026-10-14). **Nota:** la ausencia de entrada en el changelog **no** es un defecto: `docs/VERSIONING.md` §2 ata el changelog a los cambios de `protocol/.agents/` y este commit no toca el payload.
- `<PLAN-169>:F-2` — estado: `open`; severidad: `low`; observación: tres planes **cerrados** registran siete decisiones como `PENDING` que ya fueron resueltas por actos y planes posteriores, de modo que su lectura actual muestra como pendiente lo que está cerrado; evidencia original: Plan 165 `### Pending decisions` (`ID-1`, `ID-6`, `ID-8` con `resolución: **PENDING**`/`PENDING_AUTHORITY`, e `ID-3`/`ID-5` en el mismo estado) frente al `### Decisiones de autoridad cerradas (acto del mantenedor, 2026-10-13)` del propio Plan y a su `## Checkpoint / cierre` con condición `Closed`; Plan 161 (revisión del alcance de `F-C`/Etapa B, resuelta por el acto `OD-1` del Plan 163 y por el cierre de `F-C`); Plan 164 (decisiones de implementación de `F-C`, resueltas por `ID-1`…`ID-8` y registradas por el Plan 167); estado Git observado: `dev @ 2cb0d10`; provenance original: ídem `F-1`. **Naturaleza:** es un defecto de **registro**, no semántico; los checkers de lifecycle no lo detectan (`ANOMALY=0`) y los planes cerrados no se editan.

### Correcciones

- `<PLAN-169>:C-1` — refs origen: `<PLAN-169>:F-1`; alcance de revalidación: registro de `81bbde1` **por referencia, sin editar el commit ni el tag**; evidencia: este Plan declara que el cambio se ejecutó bajo **instrucción directa del mantenedor** (el piloto y su verificación constan en `docs/working/audits/EXECUTION_HOST_OBSERVATION_PILOT_2026-10-14.md`, versionado por ese mismo commit) y que su falta de artefacto de autorización es un vacío **de declaración**, no del cambio en sí; `git diff` de `81bbde1` y del tag `12.1.0` **vacío**; el hecho no se corrige retroactivamente con una autorización ficticia.
- `<PLAN-169>:C-2` — refs origen: `<PLAN-169>:F-2`; alcance de revalidación: registros de los planes 161, 164 y 165 **por referencia, sin editarlos**; evidencia: `git diff` de `docs/plans/161-…`, `164-…` y `165-…` **vacío**, y el estado real de cada una de las siete decisiones queda declarado en la lista que sigue — Plan 165 `ID-1` (provider/modelo concreto): **resuelta** por el acto del mantenedor del 2026-10-13, registrado en el propio Plan 165 (`### Decisiones de autoridad cerradas`) y en `docs/CONVENTIONS.md`; `ID-1` quedó `CLOSED` por agnosticismo. `ID-3` (aislamiento) e `ID-5` (mecanismo multi-Change): **resueltas** por el mismo acto del 2026-10-13. `ID-6` (contención de autoridad fuera del host): **resuelta DEV-side** en el diseño del propio Plan (`### Decisiones de diseño`), sin escalar a `protocol/.agents/`. `ID-8` (discrepancia del retry): **resuelta** alineando la política con el código (commit `1ce6813`, verificado en lockstep). Plan 161 (revisión del alcance de `F-C`/Etapa B): **resuelta** por el acto `OD-1` del Plan 163 y consumada por la ejecución y el cierre de `F-C` (Plan 165). Plan 164 (decisiones de implementación de `F-C`): **resueltas** por `ID-1`…`ID-8`, registradas por referencia por el Plan 167 (`<PLAN-167>:C-3`).
- `<PLAN-169>:C-3` — refs origen: `<PLAN-169>:F-1`, `<PLAN-169>:F-2` (decisión de fondo); alcance de revalidación: `.agents/AGENTS.md` (regla de autorización); evidencia: la regla hace explícito que una instrucción directa del mantenedor autoriza el cambio que nombra, que su declaración pertenece al primer artefacto del cambio (mensaje del commit cuando no hay plan, `RFC-75` Mecanismo 1) y que **no** otorga autorización más allá de lo nombrado ni exime de RFC-56 cuando hay efecto de payload; el archivo conserva sus diez reglas fundamentales y no se crea estado, autoridad, excepción ni mecanismo nuevos.

### Pending decisions

- `<PLAN-169>` — decisión: **vía de autorización de una acción directa del mantenedor** — si una instrucción directa autoriza un cambio, con qué forma debe declararse y si eso debe escribirse en `.agents/AGENTS.md`; blocking: **no** para este Plan; owner: **mantenedor**; escalación: acto registrado en este artefacto; resolución: **`RESUELTA`** por el acto del mantenedor del 2026-10-14 (tres afirmaciones confirmadas): (1) una instrucción directa del mantenedor **autoriza** el cambio que nombra; (2) esa instrucción debe quedar **declarada en el primer artefacto del cambio** —el mensaje del commit cuando no hay plan, `RFC-75` Mecanismo 1—, y esa declaración debe nombrar la vía y el alcance; (3) la aclaración se escribe en `.agents/AGENTS.md` **dentro de la regla de autorización existente**, como explicitación de lo que el vocabulario vigente ya reconoce (`direct maintainer action`), **sin** crear autoridad, estado, excepción ni mecanismo nuevos, y **sin** eximir de RFC-56 cuando el cambio tiene efecto de payload; evidencia: `## Acto de autorización registrado (2026-10-14)`; efecto downstream: cierra el vacío que `81bbde1` expuso y evita repetirlo; ADR-worthiness: no (no es un invariante arquitectónico persistente; es una aclaración operacional de una regla existente).

## Riesgos

1. **Convertir la regularización en una autorización retroactiva ficticia.** Mitigación: la corrección declara **qué pasó** (instrucción directa sin artefacto) y **no** afirma que un plan autorizó el cambio; el commit y el tag no se tocan.
2. **Reescribir historia publicada.** Mitigación: `81bbde1` y el tag `12.1.0` fuera de alcance, verificados por `git diff` vacío; los planes cerrados se reconcilian por referencia.
3. **Ampliar la aclaración hasta crear una excepción.** Mitigación: el texto se agrega a la regla existente y declara explícitamente lo que **no** otorga (autorización más allá de lo nombrado, exención de RFC-56 con efecto de payload), sin estados ni mecanismos nuevos.
4. **Presentar la reconciliación como nueva autoridad.** Mitigación: una corrección es traza factual (LC-1), nunca fuente normativa; la autoridad de la decisión de fondo es el acto del mantenedor.
5. **Editar un plan cerrado.** Mitigación: criterio de salida con `git diff` vacío para los planes 161/164/165.

## Trazabilidad

```text
81bbde1 (runtime/, publicado en master y en el tag 12.1.0 sin artefacto de autorización)
        │
        ▼
Inventario de pendientes solicitado por el mantenedor (2026-10-14)
        │
        ▼
[ este Plan 169 ] → F-1 (81bbde1) + F-2 (pending obsoletas) → C-1…C-3 → decisión de fondo → Closed (docs-only)
        │
        ▼
Diferido a su propia vía: GAP del Plan 116 (advisory, plan cerrado) · docs/planificacion-argentos-diseno-2026-10-13.md (decisión del mantenedor) · Etapa C (trabajo futuro)
```

## Nota de ejecución

**Ejecución (2026-10-14).** Change DEV-only y docs-only conducido en `dev`, bajo el acto del mantenedor registrado. Pasos:

| Paso | Resultado |
|---|---|
| 0 — clasificación y registro | Vía **Clase B**, `Change Level` **L2**; Plan creado y registrado en `docs/plans/INDEX.md` (Nonagésima sexta serie) |
| 1 — regularización de `81bbde1` | Registrado **por referencia** con su finding (`F-1`) y su evidencia; declarado como cambio ejecutado bajo **instrucción directa del mantenedor**, sin artefacto de autorización. **No** se reescribió el commit ni el tag |
| 2 — reconciliación de pending | Las **siete** decisiones obsoletas de los planes 161, 164 y 165 quedan declaradas **por referencia** con el artefacto que resolvió cada una (`C-2`); los planes cerrados **no** se editaron |
| 3 — aclaración operacional | `.agents/AGENTS.md`, regla 2: la vía de instrucción directa queda explícita, con su forma de declaración y con lo que **no** otorga (`C-3`). Sin regla, estado, autoridad ni excepción nuevos |
| 4 — verificación y cierre | Anchor, checkpoint y determinaciones de impacto; condición derivada `Closed` |

**Verificación factual del resultado:**

- `git diff` del commit `81bbde1` y del tag `12.1.0`: **vacío** (nada reescrito).
- `git diff` de `docs/plans/161-…`, `164-…` y `165-…`: **vacío** (reconciliación por referencia).
- `.agents/AGENTS.md` conserva sus **diez** reglas fundamentales; sólo se agregó texto a la regla 2.
- Cero diff en `protocol/.agents/`, `dist/`, `runtime/`, `tools/` y `tests/`.

**Factor ambiental declarado (no atribuible a este Change).** La pata `pytest` de la batería **no fue ejecutable** en la sesión de ejecución: el entorno no provee `pytest` desde el runtime del repositorio (se resuelve `pytest 9.0.2` del *user site-packages*, con 1358 tests colectados frente a los 1542 del baseline del repositorio) y el sandbox de la sesión deniega la mecánica de `tmp_path` (`PermissionError` en el *setup*, no aserciones). Es la misma limitación declarada por los planes 167 y 168. Ninguno de los archivos de este Change es leído por la suite.

**Estado:** `Executed`, condición derivada **`Closed`** (docs-only, sin release ni tag).
