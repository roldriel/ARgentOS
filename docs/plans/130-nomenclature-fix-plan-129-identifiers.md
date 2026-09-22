# Plan 130 — Corrección nomenclatural de Plan 129 (colisión de identificadores)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=0, architectural impact=0, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única. *scope*: un dominio DEV, corrección de identificadores en 3 archivos + este registro. *architectural impact*: **ninguno** — no toca arquitectura, invariantes, autoridad, lifecycle, identidad, state machine ni registry. *release impact*: ninguno. *duration/complexity*: acotada.
**Depende de:** Plan 129 (`docs/plans/129-pc1-pc2-pc3-closure.md`) y su finding `<PLAN-129>:F-2`. Consume, sin modificarlas: ADR-17, ADR-18, RFC-46, RFC-75 y el Placement Contract materializado.
**Origen:** Directiva del mantenedor (2026-09-15) que autoriza corregir **únicamente** los identificadores de decisión de Plan 129, sin tocar las reglas del Placement Contract.

## Objetivo

Eliminar la colisión de namespaces textuales entre los identificadores de decisión de Plan 129 (`PC-1`, `PC-2`, `PC-3`) y las etiquetas de regla internas de `docs/placement-contract.md` (`PC-1`…`PC-80`), renombrando **solo** los identificadores del Plan 129 a `PLAN-129:DEC-1`, `PLAN-129:DEC-2` y `PLAN-129:DEC-3`.

No se modifica el Placement Contract, no se crea ADR, no se introduce convención global de nomenclatura, no se migra nada y no cambia ninguna semántica.

## Criterio de entrada

- [x] `dev` limpio en `46081760fcda51eab2da8aaff087ae6f4cab66cf` (verificado con `git status --short` y `git rev-parse HEAD`); coincide con el commit de cierre de Plan 129.
- [x] `docs/plans/129-pc1-pc2-pc3-closure.md` existe.
- [x] `docs/placement-contract.md` existe y usa `PC-1`…`PC-80` como etiquetas de regla (80 reglas + 3 variantes `PC-31a`…`PC-31c`).
- [x] `<PLAN-129>:F-2` registra la colisión.

## Entregables

1. `docs/plans/129-pc1-pc2-pc3-closure.md` — identificadores de decisión renombrados a `PLAN-129:DEC-1/2/3`; `<PLAN-129>:F-2` marcado `resolved`; `<PLAN-129>:C-2` registrada; nota de nomenclatura actualizada; pending de nomenclatura retirado.
2. `docs/plans/INDEX.md` — encabezado de serie, fila del Plan 129 y referencias al pending de Plan 128 alineados.
3. `CHANGELOG.md` — ítems de los planes 128 y 129 alineados.
4. `docs/plans/130-nomenclature-fix-plan-129-identifiers.md` (**este archivo**).
5. `docs/plans/INDEX.md` — registro del Plan 130.
6. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 130).

## Pasos

1. Verificar baseline, existencia de Plan 129 y del contrato, y el rango de etiquetas de regla del contrato.
2. Localizar contextualmente cada uso de `PC-1`/`PC-2`/`PC-3` como identificador de decisión del Plan 129, distinguiéndolo de las referencias a reglas del contrato.
3. Renombrar únicamente esos usos; preservar las referencias a reglas (`PC-67`…`PC-71`, `PC-72`…`PC-77`, `PC-79`/`PC-80`, `PC-31`, `PC-31a`…`PC-31c`) y las citas históricas del nombre anterior.
4. Marcar `<PLAN-129>:F-2` como `resolved`, registrar `<PLAN-129>:C-2` y retirar el pending de nomenclatura.
5. Alinear las referencias equivalentes en `INDEX.md` y `CHANGELOG.md`.
6. Registrar Plan 130, validar y cerrar.

## Criterios de salida

- [ ] Plan 129 usa `PLAN-129:DEC-1/2/3` como identificadores de decisión y `PLAN-129:F-2` figura como `resolved`.
- [ ] No queda ninguna referencia **activa** que use `PC-1`/`PC-2`/`PC-3` para las decisiones de Plan 129.
- [ ] Las referencias a reglas del contrato siguen siendo exactamente `PC-1`…`PC-80` y `PC-31a`…`PC-31c`, intactas.
- [ ] `docs/placement-contract.md` **sin cambios** (0 diff).
- [ ] Semántica de las tres decisiones sin alterar; ninguna otra decisión tocada.
- [ ] Sin ADR, sin registry, sin checker, sin schema, sin migración, sin convención global nueva.
- [ ] Batería canónica y gates de lifecycle registrados.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --stat -- docs/placement-contract.md   # debe ser vacío
git diff --name-status
```

## Mapeo before → after

| Before (Plan 129) | After | Naturaleza |
|---|---|---|
| `PC-1` (decisión: project-durable / Git persistence) | **`PLAN-129:DEC-1`** | identificador de decisión de nivel de plan |
| `PC-2` (decisión: enforcement autorizado, implementación diferida) | **`PLAN-129:DEC-2`** | idem |
| `PC-3` (decisión: excepciones documentales, sin representación machine-locatable) | **`PLAN-129:DEC-3`** | idem |
| `<PLAN-129>:PC-1` (pending de nomenclatura) | retirado — resuelto por esta corrección; su contenido pasa a `<PLAN-129>:C-2` | pending → corrección |
| `<PLAN-129>:PC-2` (pending de implementación del enforcement) | **`<PLAN-129>:DEC-2`** | identificador de pending alineado |
| `<PLAN-129>:F-2` | sin cambio de identificador; estado pasa a `resolved` | finding |
| Referencias a reglas del contrato (`PC-67`…`PC-71`, `PC-72`…`PC-77`, `PC-79`, `PC-80`, `PC-31`, `PC-31a`…`PC-31c`) | **sin cambio** | reglas normativas del contrato |
| «Deferred: PC-1» (nombre histórico de una sección del contrato, citado como historia) | **sin cambio** | cita histórica legítima |
| Referencias de planes previos a su propio pending `PC-1` (Change Lifecycle, planes 95–117) | **sin cambio** | fuera de alcance: no son decisiones de Plan 129 |

**Alcance ampliado documentado.** Además de los identificadores del Plan 129, se alinearon **dos** referencias al pending de persistencia en las entradas del Plan 128 (`docs/plans/INDEX.md` y `CHANGELOG.md`), que usaban la misma etiqueta `PC-1` para la misma decisión heredada. Se reemplazaron por una descripción explícita («persistencia Git de `.project/changes/`»). Es la misma clase de identificador y dejarlas habría conservado la ambigüedad que esta corrección elimina; **no** se renumeró ninguna regla del contrato ni se tocó ningún otro plan.

## Archivos afectados

| Archivo | Acción |
|---|---|
| `docs/plans/129-pc1-pc2-pc3-closure.md` | modificado — 15 referencias de decisión renombradas; F-2 `resolved`; C-2 registrada; pending retirado; nota de nomenclatura reescrita |
| `docs/plans/INDEX.md` | modificado — encabezado de serie del Plan 129, fila del Plan 129 (4 referencias) y pending del Plan 128 |
| `CHANGELOG.md` | modificado — ítems de los planes 128 y 129 (6 referencias) |
| `docs/plans/130-nomenclature-fix-plan-129-identifiers.md` | **creado** — este registro |
| `docs/placement-contract.md` | **NO modificado** — 0 diff |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-130>:F-1` — estado: `resolved` (transición `open` → `resolved` aplicada el 2026-09-21 por decisión humana del mantenedor, Change del Plan 141); severidad: `low`; observación: el namespace textual `PC-n` representaba simultáneamente decisiones de nivel de plan (Plan 129) y reglas normativas internas del Placement Contract (`PC-1`…`PC-80`), de modo que el significado de un identificador sólo podía determinarse por contexto; evidencia original: `docs/plans/129-pc1-pc2-pc3-closure.md` (identificadores de decisión) frente a `docs/placement-contract.md` (etiquetas de regla); estado Git observado: `dev` @ `4608176`, working tree limpio; provenance original: `<PLAN-129>:F-2` y decisión humana de corrección (2026-09-15); resolución: corregido por `<PLAN-130>:C-1`.

### Correcciones

- `<PLAN-130>:C-1` — refs origen: `<PLAN-130>:F-1`, `<PLAN-129>:F-2`; alcance de revalidación: `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `docs/plans/130-nomenclature-fix-plan-129-identifiers.md`; evidencia (Git/commit/estado): renombrado a `PLAN-129:DEC-1/2/3`; `docs/placement-contract.md` con 0 diff (80 reglas + 3 variantes intactas); batería canónica en verde; commit atómico de cierre.

### Pending decisions

- `<PLAN-130>:PC-1` — decisión: si conviene adoptar de forma **general** una convención de identificadores de decisión a nivel de plan (por ejemplo `PLAN-<N>:DEC-<N>`) para todos los planes, o mantener la práctica actual. **No decidida aquí**: esta corrección arregla únicamente Plan 129 y **no** generaliza la convención; blocking: no; owner: mantenedor; escalación: decisión directa si la ambigüedad reaparece en otro plan; resolución: **resuelta** (decisión humana del mantenedor, determinada por el Plan 141 el 2026-09-21): **no** se adopta una convención general `PLAN-<N>:DEC-<N>` —el identificador del Plan 129 es local, la ambigüedad no reapareció en otro plan y no se crea taxonomía nueva—; evidencia: el brief prohíbe explícitamente crear una política global en este Change.
- `<PLAN-130>:PC-2` — decisión: implementar el enforcement mecánico autorizado por `PLAN-129:DEC-2` (heredada, sin cambios); blocking: no; owner: mantenedor; escalación: nuevo Change/Plan autorizado; resolución: **superseded** (determinada por el Plan 141 el 2026-09-21): ownership duplicado de `<PLAN-129>:DEC-2`; evidencia: `docs/placement-contract.md:22. Enforcement` y `24. Enforcement deferred`.

## Riesgos

- **Renombrar por búsqueda ciega y corromper las reglas del contrato.** Mitigación: cada reemplazo se hizo contextualizado; verificado que `docs/placement-contract.md` tiene 0 diff y que conserva 80 reglas más las 3 variantes, sin etiquetas corruptas (`DEC-6x`/`DEC-7x`/`DEC-31x` = 0).
- **Ampliar el alcance a otros planes.** Mitigación: no se modificó ninguna referencia de otros planes a su propio pending; sólo se alinearon las dos referencias al pending heredado del Plan 128, documentado arriba.
- **Convertir la corrección en política global.** Mitigación: la nota de nomenclatura y `<PLAN-130>:PC-1` declaran explícitamente que no se generaliza.

## Trazabilidad

Plan 127 (diseño) → Plan 128 (materialización del contrato) → Plan 129 (cierre de `DEC-1`/`DEC-2`/`DEC-3`, con `<PLAN-129>:F-2`) → **este plan** (corrección nomenclatural) → implementación del enforcement (Change futuro, no autorizado).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la corrección nomenclatural: `CHANGELOG.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/130-nomenclature-fix-plan-129-identifiers.md`, `docs/plans/INDEX.md`. Total 4 paths. `docs/placement-contract.md` **no** forma parte del scope: se verificó con 0 diff.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `git diff --stat -- docs/placement-contract.md`.
- **Effective inputs (repo content):** el scope declarado (4 paths) más `docs/placement-contract.md` como **entrada de verificación** (se comprueba que sus 80 reglas y 3 variantes permanecen intactas), y `docs/plans/`, `docs/rfc/`, `docs/adr/` y `protocol/.agents/` consumidos por los checkers canónicos.
- **Observed dependencies:** `git` (identidad de contenido y estado; el diff del contrato es la evidencia directa de su no-modificación); `python` (intérprete de los checkers y del verificador de identidad); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; sin red. **La pierna de tests no se ejecutó y no se declara como validación de este plan:** el cambio es exclusivamente documental (renombrado de identificadores en dos planes, un índice y el changelog), no modifica código, checkers, runtime ni payload, y no hay superficie de producto que validar. La suite DEV arrastra la clase ambiental conocida de temporales de pytest (`PermissionError [WinError 5]`) declarada por los Planes 121–129; se clasifica como **GAP ambiental** conforme al precedente, sin reabrir C-2/CI ni modificar CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `ddc29a98f8bbad6d888a2f010a52fbf59f1eb7d5`.
  - **Delta scoped identity (scope S = los 4 paths del cambio, ordenados; serialización `scoped-v1`):** `ae1d78fd26decc7fbbf2307d9b3538a967dca10fc7d9b1d66d576c28976667b1`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `ddc29a98f8bbad6d888a2f010a52fbf59f1eb7d5`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`ddc29a98f8bbad6d888a2f010a52fbf59f1eb7d5`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/130-nomenclature-fix-plan-129-identifiers.md`, `docs/plans/INDEX.md`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`). Gates sobre el árbol final: C-1 `VALID`, C-2 `VALID`, C-3 `VALID` para el Plan 130; C-3 `VALID` también para el Plan 129 tras registrar su `resolución`. **Evidencia de no-modificación del contrato:** `git diff --stat -- docs/placement-contract.md` vacío (0 diff); 80 reglas `PC-n` y 3 variantes `PC-31a`…`PC-31c` intactas; 0 etiquetas corruptas. **Evidencia de disjunción:** los identificadores de decisión de Plan 129 son `PLAN-129:DEC-1/2/3`; las reglas del contrato siguen siendo `PC-1`…`PC-80`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(plans): fix plan 129 decision identifiers to remove namespace collision (plan 130)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `ae1d78fd26decc7fbbf2307d9b3538a967dca10fc7d9b1d66d576c28976667b1`, tree `ddc29a98f8bbad6d888a2f010a52fbf59f1eb7d5`.
- **Estado de cierre (tree id):** `ddc29a98f8bbad6d888a2f010a52fbf59f1eb7d5` — el árbol del índice que la validación A1 consumió, con el scope declarado (4 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–129) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 130 (tabla + serie, Sexagésima segunda) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 130); `## Validation anchor` y `## Checkpoint / cierre` registrados; finding `F-1`, corrección `C-1` y pendientes `PC-1`/`PC-2` registrados; `<PLAN-129>:F-2` marcado `resolved` con su `resolución` y `<PLAN-129>:C-2` registrada; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — documentos afectados: `docs/plans/129-pc1-pc2-pc3-closure.md` (aspecto: sus identificadores de decisión colisionaban con las etiquetas de regla del contrato; actualización: renombrado a `PLAN-129:DEC-1/2/3`, `<PLAN-129>:F-2` a `resolved` con `resolución`, `<PLAN-129>:C-2` registrada, nota de nomenclatura reescrita y pending de nomenclatura retirado; evidencia: C-3 `VALID` para el Plan 129), `docs/plans/INDEX.md` (aspecto: serie, fila del Plan 129 y pending heredado del Plan 128 usaban la etiqueta colisionante; actualización: alineados + registro del Plan 130; evidencia: `check_plan_structure` PASS) y `CHANGELOG.md` (aspecto: ítems de los planes 128/129 usaban la etiqueta colisionante; actualización: alineados + ítem del Plan 130; evidencia: `check_version_state` PASS). `docs/placement-contract.md` **no** requiere ni admite cambio: se verificó con 0 diff. `AGENTS.md`, `docs/AGENTS.md` y `docs/source-layout.md` no se modifican. No se actualiza ningún documento histórico (RFC-46). Sin `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. **Clasificación de estado final:** `Nomenclature collision = RESOLVED` · `Placement Contract = UNCHANGED` · `Plan 129 decision IDs = PLAN-129:DEC-1/2/3` · `ADR = NONE CREATED` · `Migration = NOT STARTED` · `Release = NOT AUTHORIZED`. `Committed` es estado del repositorio. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `4608176`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: seis checkers PASS (`check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0; `check_protocol_invariants` PASS). Gates sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`** para el Plan 130, y C-3 `VALID` también para el Plan 129. Corpus C-2 con único GAP preexistente `116-adversarial-deliberation-mvp-closure.md`, no modificado. Verificaciones específicas: `docs/placement-contract.md` con **0 diff** y 80 reglas más 3 variantes intactas; 0 etiquetas corruptas; identificadores de decisión de Plan 129 disjuntos de las reglas del contrato.

**Incidencias corregidas durante la ejecución.** (a) Al marcar `<PLAN-129>:F-2` como `resolved` faltaba el campo `resolución`, que C-3 exige (`R-L1-5`); se registró la resolución con su autoridad y su provenance. (b) Se detectaron dos referencias al pending de persistencia heredado del Plan 128 que usaban la misma etiqueta colisionante en `docs/plans/INDEX.md` y `CHANGELOG.md`; se alinearon con una descripción explícita, documentado como alcance ampliado en `## Mapeo before → after`.

**Alcance.** 4 archivos modificados/creados, todos documentales. Ningún artefacto movido, renombrado ni eliminado. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`, `.gitignore`, `AGENTS.md` y `docs/placement-contract.md` sin cambios.

**No realizado (por diseño).** Sin ADR, sin registry, sin checker, sin schema, sin state machine, sin autoridad nueva, sin lifecycle nuevo, sin migración y **sin** convención global de nomenclatura: la corrección se limita a Plan 129 (más las dos referencias documentadas al pending heredado). La semántica de `DEC-1`/`DEC-2`/`DEC-3` y del Placement Contract permanece idéntica.
