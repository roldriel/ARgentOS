# Plan 128 — Materialización del Repository/Artifact Placement Contract

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=1, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única. *scope*: un dominio DEV y cuatro artefactos documentales. *architectural impact*: materializa decisiones ya registradas (ADR-17, ADR-18, Plan 127) sin introducir arquitectura nueva. *release impact*: ninguno. *duration/complexity*: acotada.
**Depende de:** Plan 127 (`docs/plans/127-repository-artifact-placement-contract-design.md`) como design record, y ADR-17 / ADR-18 como arquitectura upstream. Consume, sin modificarlas: RFC-46 (inmutabilidad histórica), RFC-56 (clases de cambio), RFC-75 (lifecycle DEV), ADR-15 y ADR-16.
**Origen:** Directiva del mantenedor (2026-09-15) que autoriza materializar el Placement Contract con las decisiones humanas **OQ-2 = NO**, **OQ-3 = A** y **OQ-4 = NO**, manteniendo **PC-1 OPEN / DEFERRED**.

## Objetivo

Materializar el **Repository/Artifact Placement Contract** como documento normativo independiente bajo `docs/`, derivado del diseño cerrado en Plan 127 y de las tres decisiones humanas autorizadas, de modo que un agente pueda determinar de forma determinista dónde debe ubicarse un artefacto nuevo —o detenerse— sin adivinar.

Este plan **no** crea registry, checker, schema, namespace nuevo, state machine, clase de autoridad ni ADR; **no** integra enforcement en runtime, Orchestrator, Worker, checkers ni CI; **no** autoriza ni ejecuta migración alguna; **no** resuelve PC-1.

## Criterio de entrada

- [x] `dev` limpio en `a70f1c671a752184eacfaeb2e712d3ca398a0527` (verificado con `git status --short` y `git rev-parse HEAD`); coincide con el commit de cierre de Plan 127.
- [x] El design record de Plan 127 existe y corresponde al diseño que se materializa.
- [x] Decisiones humanas explícitas: `OQ-2 = NO`, `OQ-3 = A`, `OQ-4 = NO`.
- [x] `PC-1` confirmado `OPEN / DEFERRED`.
- [x] Verificado que no existe otro Placement Contract ni un nombre en conflicto bajo `docs/`.

## Entregables

1. `docs/placement-contract.md` (**nuevo**) — el Placement Contract normativo.
2. `AGENTS.md` — referencia de discovery al contrato (sin duplicarlo).
3. `docs/plans/128-placement-contract-materialization.md` (**este archivo**).
4. `docs/plans/INDEX.md` — registro del plan.
5. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 128).

## Pasos

1. Verificar baseline y coherencia con el Plan 127 cerrado.
2. Elegir el path del contrato conforme a la convención existente, sin crear namespace nuevo.
3. Materializar el contrato derivándolo del diseño (norma operativa, no copia del plan).
4. Añadir la referencia de discovery en `AGENTS.md`.
5. Registrar Plan 128, INDEX y changelog; determinar Documentation Impact.
6. Ejecutar la batería canónica, los gates de lifecycle y la verificación de alcance.

## Criterios de salida

- [ ] Existe `docs/placement-contract.md` como documento normativo independiente, con las 21 secciones requeridas y la regla central `canonicality qualifies placement; it does NOT determine placement`.
- [ ] El algoritmo termina en `PLACE` o `STOP`; `GUESS` no es un resultado admisible.
- [ ] `OQ-2 = NO`: sin exigencia de machine-locatability, sin registry/schema/database/global index/identity primitive; y **sin prohibir** que una decisión futura la introduzca.
- [ ] `OQ-3 = A`: documento independiente bajo `docs/`, sin namespace nuevo; `AGENTS.md` sólo lo referencia.
- [ ] `OQ-4 = NO`: sin ADR nuevo.
- [ ] PC-1 registrado como diferenciación `project-durable ≠ git-committed`, sin política de Git y sin reglas `always/never/auto commit/ignore`.
- [ ] Sin migración, sin registry/checker/schema, sin integración runtime/Orchestrator/CI.
- [ ] `protocol/`, `runtime/`, `tools/`, `tests/` sin cambios; DEV ≠ Protocol intacto; sin `VERSION` bump ni tag.
- [ ] Batería canónica y gates de lifecycle registrados con resultado real.

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
git diff --name-status
```

Comprobaciones específicas de la materialización:

1. El contrato no contradice ADR-17 ni ADR-18 (referencia, no restate).
2. `AGENTS.md` sólo referencia el contrato; no lo duplica.
3. PC-1 permanece deferred y sin política de Git.
4. No existe otro Placement Contract.
5. No se creó ADR.
6. No hubo movimientos de archivos.

## Decisiones humanas materializadas

| ID | Decisión | Materialización |
|---|---|---|
| **OQ-2** | **NO** — el contrato no exigirá que todas las excepciones sean machine-locatable | `docs/placement-contract.md:9. Exceptions`: la excepción se registra en el artefacto que ya posee la decisión, debe ser localizable y comprensible por los mecanismos documentales existentes, acotada al artefacto o la familia (nunca a un namespace o prefijo), atribuida al owner que la autoriza; si el agente no puede localizarla o interpretarla → **STOP**. Se declara explícitamente que **no** se crea registry, schema, database, índice global ni identity primitive, y que una decisión futura **puede** introducir una representación machine-locatable (no se prohíbe) |
| **OQ-3** | **A** — documento independiente bajo `docs/` | `docs/placement-contract.md`. Nombre en kebab-case conforme a la convención existente de los archivos Policy de `docs/` (precedente directo de Policy de layout: `docs/source-layout.md`). **Sin namespace nuevo.** Canonical, normativo, repository-wide, consumido por agentes y maintainers, separado de `AGENTS.md` |
| **OQ-4** | **NO** — sin ADR adicional | No se creó ADR. El contrato **materializa** ADR-17 y ADR-18 y se declara downstream de ambos. Durante la materialización **no apareció** ninguna arquitectura, invariante, autoridad, semántica de lifecycle, identidad, state machine, registry ni frontera nueva: **no se registró ningún `DECISION REQUIRED`** |
| **PC-1** | `OPEN / DEFERRED` | Sección `Deferred: PC-1`: registra `project-durable ≠ git-committed` (ADR-17 `RS-5`) y **no** establece política de Git; prohíbe expresamente formular `always commit` / `never commit` / `auto-commit` / `auto-ignore`. La única sección afectada (la declaración del namespace durable) queda marcada `DEFERRED — PC-1` |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-128>:F-1` — estado: `open`; observación: el diseño cerrado en Plan 127 y las decisiones humanas `OQ-2`/`OQ-3`/`OQ-4` no tenían consecuencia normativa en el árbol: no existía ningún documento que un agente pudiera consultar para determinar el placement de un artefacto nuevo, de modo que la regla permanecía en el design record y seguía siendo necesario inferir; evidencia original: ausencia de documento de contrato bajo `docs/` (barrido recursivo sin coincidencias) y `git status` limpio en `a70f1c6`; estado Git observado: `dev` @ `a70f1c6`, working tree limpio; provenance original: cierre de Plan 127 y decisión humana de materializar (2026-09-15); resolución: materializado por `<PLAN-128>:C-1`.

### Correcciones

- `<PLAN-128>:C-1` — refs origen: `<PLAN-128>:F-1`; alcance de revalidación: `docs/placement-contract.md` (nuevo), `AGENTS.md` (referencia de discovery), `docs/plans/128-placement-contract-materialization.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`; evidencia (Git/commit/estado): batería canónica en verde y gates C-1/C-2/C-3 `VALID`; commit atómico de cierre.

### Pending decisions

- `<PLAN-128>:PC-1` — decisión: relación exacta entre `project-durable` y Git persistence para `.project/changes/`; blocking: no para esta materialización (el contrato queda semánticamente correcto sin la política), **sí** para que esa sección sea plenamente normativa; owner: mantenedor; escalación: vía RFC-56 si se autoriza cambiar la semántica de persistencia del contrato Protocol; resolución: pendiente; evidencia: ADR-17 `RS-5`; `git ls-files .project` = 0 y `.gitignore` ignora `.project/`. Declarado `DEFERRED — PC-1` en `docs/placement-contract.md:21. Deferred: PC-1`.
- `<PLAN-128>:PC-2` — decisión: si y cuándo se integra enforcement mecánico del Placement Contract (checker, Orchestrator, CI); blocking: no; owner: mantenedor; escalación: decisión/trabajo separado; resolución: pendiente; evidencia: `docs/placement-contract.md:22. Non-goals` declara que el contrato no crea ni implica enforcement y que su existencia no implica verificación mecánica.
- `<PLAN-128>:PC-3` — decisión: si en el futuro se introduce una representación machine-locatable de excepciones; blocking: no; owner: mantenedor; escalación: decisión posterior; resolución: pendiente; evidencia: `OQ-2 = NO` se materializó sin prohibir esa vía; `docs/placement-contract.md:9. Exceptions` la deja explícitamente admisible bajo una decisión futura.

## Riesgos

- **Que el contrato se convierta en fuente de autoridad arquitectónica.** Mitigación: `Relationship with ADR-17 and ADR-18` declara el contrato downstream y establece que, ante conflicto, **el ADR gobierna** y el conflicto se escala.
- **Que la tabla de familias se lea como un enum cerrado.** Mitigación: `kind` se declara clave de lookup domain-scoped, no vocabulario global, y ampliar la tabla se declara cambio de governance.
- **Que el contrato se lea como autorización de migración.** Mitigación: `Move / rename semantics` declara que el contrato nunca autoriza un movimiento (`RS-7`).
- **Duplicar el contrato en `AGENTS.md`.** Mitigación: la referencia lo declara separado y no reafirmado; verificable por inspección.

## Trazabilidad

Diseño del Placement Contract (plan 127) → decisiones humanas `OQ-2 = NO`, `OQ-3 = A`, `OQ-4 = NO` → **este plan** → `docs/placement-contract.md` (norma operativa) → integración/enforcement (no autorizada) → migración (no autorizada).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la materialización: `AGENTS.md`, `CHANGELOG.md`, `docs/placement-contract.md`, `docs/plans/128-placement-contract-materialization.md`, `docs/plans/INDEX.md`. Total 5 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`.
- **Effective inputs (repo content):** el scope declarado (5 paths) más `docs/plans/`, `docs/rfc/`, `docs/adr/` y `protocol/.agents/` consumidos por los checkers canónicos. El contrato referencia ADR-17, ADR-18 y `.agents/policies/authority.md`, que son entradas efectivas de su corrección semántica.
- **Observed dependencies:** `git` (identidad de contenido y estado; el checker de citas resuelve `docs/placement-contract.md` + sección contra los encabezados numerados del contrato); `python` (intérprete de los checkers); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; sin red. **La pierna de tests no se ejecutó y no se declara como validación de este plan:** el cambio es exclusivamente documental (un contrato nuevo, una referencia de discovery, un plan, su registro y el changelog), no modifica código, checkers, runtime ni payload, y la suite DEV arrastra la clase ambiental conocida de temporales de pytest (`PermissionError [WinError 5]`) declarada por los Planes 121–127. No hay superficie de producto que validar; la verificación exigible es la batería de checkers, que corre completa. No se reabre el aislamiento de pytest ni se modifica CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `ef2278ce2ff3644c8259b3d8289a5b568dac8b25`.
  - **Delta scoped identity (scope S = los 5 paths del cambio, ordenados; serialización `scoped-v1`):** `f8b35a3c1aa46892b87965f369df576f508c16ca7b031feadfb5c2882a176505`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `ef2278ce2ff3644c8259b3d8289a5b568dac8b25`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`ef2278ce2ff3644c8259b3d8289a5b568dac8b25`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `AGENTS.md`, `CHANGELOG.md`, `docs/placement-contract.md`, `docs/plans/128-placement-contract-materialization.md`, `docs/plans/INDEX.md`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0, 215 files checked); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`). Gates de lifecycle sobre el árbol final: C-1 `VALID`, C-2 `VALID`, C-3 `VALID` para el Plan 128. Comprobaciones específicas: el contrato tiene 22 secciones numeradas y 70 reglas normativas; la regla central aparece literalmente; `AGENTS.md` referencia el contrato una sola vez sin duplicarlo; existe `## 21. Deferred: PC-1`; existe **un solo** Placement Contract (`docs/placement-contract.md` — los otros dos archivos que coinciden con «placement» son los planes 127 y 128); 0 ADR nuevos.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(placement): materialize repository artifact placement contract (plan 128)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `f8b35a3c1aa46892b87965f369df576f508c16ca7b031feadfb5c2882a176505`, tree `ef2278ce2ff3644c8259b3d8289a5b568dac8b25`.
- **Estado de cierre (tree id):** `ef2278ce2ff3644c8259b3d8289a5b568dac8b25` — el árbol del índice que la validación A1 consumió, con el scope declarado (5 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–127) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 128 (tabla + serie, Sexagésima) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 128); `## Validation anchor` y `## Checkpoint / cierre` registrados; finding `F-1`, corrección `C-1` y pendientes `PC-1`..`PC-3` registrados; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — documentos afectados: `AGENTS.md` (aspecto: no exponía ningún camino de discovery hacia la norma de placement; actualización: una referencia que declara a `docs/placement-contract.md` como fuente normativa para determinar la ubicación de un artefacto nuevo, sin duplicar el contrato; evidencia: `check_plan_citations` PASS y recuento de una sola referencia), `docs/plans/INDEX.md` (aspecto: materialización no registrada; actualización: serie + tabla + encabezado; evidencia: `check_plan_structure` PASS) y `CHANGELOG.md` (aspecto: par del plan; actualización: ítem `[Unreleased]`; evidencia: `check_version_state` PASS). `docs/AGENTS.md` **no** requiere cambio: el contrato es un archivo Policy de la raíz de `docs/`, categoría ya declarada por la carta, y no introduce naturaleza, clase ni lifecycle nuevos. No se modifica `docs/source-layout.md`. No se actualiza ningún documento histórico (RFC-46). `protocol/.agents/VERSION` y el changelog del payload no se tocan: el contrato es DEV y no tiene efecto payload. Sin `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. **Clasificación de estado final:** `Design: CLOSED (plan 127)` · `Contract: MATERIALIZED` · `Enforcement: NOT IMPLEMENTED` · `Migration: NOT STARTED` · `Release: NOT AUTHORIZED`. `Committed` es estado del repositorio. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `a70f1c6`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: seis checkers PASS (`check_protocol_invariants` 215 files checked; `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0). Gates sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`**; corpus C-2 con único GAP preexistente `116-adversarial-deliberation-mvp-closure.md`, no modificado. Incidencia corregida durante la ejecución: cuatro citas al contrato usaban el encabezado sin su número (por ejemplo «Exceptions»), y el checker de citas —que compara contra encabezados literales— las reportó como `section not found`; se corrigieron a `9. Exceptions`, `21. Deferred: PC-1` y `22. Non-goals`. También se corrigió una referencia duplicada en el propio plan.

**Alcance.** 5 archivos, todos documentales. Ningún artefacto movido, renombrado ni eliminado. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/` y `.gitignore` sin cambios. Ningún documento histórico reescrito.

**No realizado (por diseño).** Sin registry, checker, schema, database, índice global de excepciones, identity primitive, namespace nuevo, state machine, clase de autoridad, lifecycle nuevo ni ADR. Sin integración de enforcement en Orchestrator, Worker, runtime, checkers ni CI: `docs/placement-contract.md:22. Non-goals` lo declara explícitamente. Sin migración — el contrato describe la arquitectura objetivo ya decidida y `10. Move / rename semantics` declara que nunca autoriza un movimiento. PC-1 no fue resuelto: se registra `project-durable ≠ git-committed` sin política de Git.

**Registro de decisiones.** `OQ-2 = NO`, `OQ-3 = A`, `OQ-4 = NO` y `PC-1` (deferred) quedan materializados en `docs/placement-contract.md` y atribuidos al mantenedor en `## Decisiones humanas materializadas` de este plan. **No se registró ningún `DECISION REQUIRED`**: la materialización no requirió arquitectura, invariante, autoridad, semántica de lifecycle, identidad, state machine, registry ni frontera nuevos.
