# Plan 164 — Acto de autorización de ejecución de `F-C` y formalización de su Plan

**Status:** Executed
**Fecha:** 2026-10-13
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, docs-only, sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, una capa. *scope*: área acotada — gobernanza documental. *architectural impact*: **0** — registra una autorización y crea un Plan; no crea capacidad, entidad, estado, contrato ni mecanismo. *release impact*: ninguno. *duration/complexity*: menos de una sesión.
**Depende de:** plan 163 (acto de `OD-1` y alcance canónico 1B), plan 162 (instrumento), plan 161 (Etapa A), plan 159 (`F-B`), plan 160
**Origen:** acto del mantenedor (2026-10-13) que autoriza la ejecución de `F-C` bajo el alcance canónico 1B y la creación de su Plan de ejecución
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; no se deriva ni se inventa.

## Acto de autorización registrado (2026-10-13)

**Transcripción del acto (autoridad: mantenedor; fecha efectiva: 2026-10-13):**

> «Autorizo la ejecución de F-C bajo el alcance canónico 1B establecido por OD-1. Autorizo la creación y
> formalización de su Plan de ejecución con `Status: Aprobado para ejecución`, `Change Level ≥ L3` y
> criterios `FC-1`…`FC-10`. La autorización no extiende el scope más allá del `IN SCOPE` de OD-1 ni
> incorpora C-16/C-17/C-21.»

| Campo | Contenido |
|---|---|
| **Decisión** | Autorización de **ejecución** de `F-C` y de creación/formalización de su **Plan de ejecución** — resuelve la pending decision de `<PLAN-163>` («autorización de ejecución del Change de `F-C`») |
| **Autoridad** | **Mantenedor** |
| **Fecha efectiva** | **2026-10-13** |
| **Alcance autorizado** | El alcance canónico **1B** ya registrado por `OD-1` en `docs/CONVENTIONS.md` (subsección «Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)») y en `docs/plans/163-acto-autoridad-od1-alcance-f-c.md:Acto de autoridad registrado (2026-10-12)`. **No** se extiende más allá de ese `IN SCOPE`; **no** incorpora `C-16`/`C-17`/`C-21` |
| **Artefacto designado** | **Plan 165** — `docs/plans/165-f-c-autonomy-frontier-implementation.md`, con `Status: Aprobado para ejecución`, `Change Level ≥ L3` y criterios `FC-1`…`FC-10` |
| **Efecto sobre el estado** | `F-C`: de **`SCOPED`** a **`Aprobado para ejecución`** (alcance y ejecución autorizados; implementación **no iniciada**) |
| **Límite explícito del acto** | La autorización **no** habilita al agente a implementar `F-C` dentro de este Change: el Plan 165 es el **contrato operativo del Change de implementación**, que corre por separado |
| **Evidencia** | El acto del mantenedor (transcrito arriba); `docs/CONVENTIONS.md` (alcance canónico); Plan 163 (pending resuelta y anotada); Plan 165 (creado); `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md` reconciliados |

```text
OD1                = CLOSED  (resuelto por el acto del 2026-10-12; pending de ejecución resuelta por este acto)
F-C_SCOPE          = 1B / CLOSED
F-C_PLAN           = CREATED (docs/plans/165-f-c-autonomy-frontier-implementation.md)
F-C_PLAN_STATUS    = Aprobado para ejecución
F-C_CHANGE_LEVEL   = L3
F-C_IMPLEMENTATION = NOT_STARTED
ETAPA_B            = NOT_STARTED
```

## Objetivo

Registrar el acto que autoriza la ejecución de `F-C` bajo el alcance canónico 1B, crear y formalizar su **Plan de ejecución** con `Status: Aprobado para ejecución`, `Change Level ≥ L3` y los criterios `FC-1`…`FC-10`, dejar explícitas las decisiones de implementación que ese Plan deberá resolver, y reconciliar la gobernanza derivada.

**No implementa `F-C`**: no se toca `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` ni `dist/`, y no se inicia ninguna capacidad.

## Alcance heredado (1B) — sin extensión

### IN SCOPE (idéntico al `IN SCOPE` de `OD-1`)

1. Actor real con **provider/modelo**.
2. **Aislamiento/sandbox**, incluida la posibilidad explícitamente prevista de **declarar una garantía que no se ofrece**.
3. **Memory como contexto**.
4. **Objetivo multi-Change** con trigger explícito.
5. **`C-02`** — contención de autoridad fuera del host.
6. **`C-26`** — recuperación ante fallos reales.

### OUT OF SCOPE (idéntico al `OUT OF SCOPE` de `OD-1`)

`C-16` Discovery · `C-17` Discovery KB · `C-21` Skills · derivación parcial · recurso como eje de autorización · cambio del default de `--sae` · concurrencia · telemetría con backend · evaluación comparativa · cualquier otra capacidad no incluida explícitamente en el `IN SCOPE`.

**Ninguna capacidad se incorpora por simetría, disponibilidad tecnológica, conveniencia de implementación o madurez baja.**

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | El mantenedor autoriza la ejecución de `F-C` bajo el alcance 1B y la creación/formalización de su Plan con `Aprobado para ejecución`, `Change Level ≥ L3` y `FC-1`…`FC-10`. `origin_type` = direct maintainer action | humano | el acto (transcrito arriba) |
| `P-2` Confianza de intención | `HIGH` — el acto fija artefacto, estado, nivel mínimo, criterios, alcance heredado y límites; prohíbe extender el scope e incorporar `C-16`/`C-17`/`C-21` | agente | `INTENT_CONFIDENCE` aplicado sobre el acto |
| `P-3` Conjunto de contexto | `docs/CONVENTIONS.md` (alcance canónico de `F-C`); `docs/plans/163-acto-autoridad-od1-alcance-f-c.md`; `docs/plans/162-instrumento-decision-od1-alcance-f-c.md`; `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`; `docs/plans/159-autonomy-envelope-implementation.md`; `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md`; `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`; `docs/adr/19-autonomy-envelope-authority.md`; `ROADMAP.md`; `docs/plans/_TEMPLATE.md`; `docs/VERSIONING.md` §7/§10; `.agents/policies/authority.md` | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` sin señal bloqueante: el acto existe, es explícito, el alcance está cerrado y sus límites declarados. No hay `REQUIRES_HUMAN` pendiente para **este** Change (las decisiones de implementación pertenecen al Plan 165 y quedan registradas allí) | agente | el acto; `docs/plans/163-acto-autoridad-od1-alcance-f-c.md:Pending decisions` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | Planes 159–163 `Executed`; `ADR-19` y `ADR-16` `Accepted`; `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md` activos; el producto de Etapa A es Working (`active`, no normativo) | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía documental), ADR-16 (`AU-3`/`AU-5`/`AU-6`), `docs/VERSIONING.md` §4/§4.1/§7/§10, VC-1/GC-1/LC-1/PC-1. `NOT_APPLICABLE`: RFC-56 (sin efecto payload); RFC-46 (la anotación de la pending es aditiva) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **acto del mantenedor (2026-10-13)**. Scope declarado: `docs/plans/164-acto-autorizacion-ejecucion-f-c.md` (este artefacto), `docs/plans/165-f-c-autonomy-frontier-implementation.md` (nuevo), `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` (anotación **aditiva** de la resolución de su pending, regla `PC-1`), `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` | **humano** | el acto |

## Criterio de entrada

- [x] Alcance canónico 1B vigente y legible en `docs/CONVENTIONS.md` y en el Plan 163.
- [x] Criterios `FC-1`…`FC-10` establecidos por `OD-1` (Plan 163) y no debilitados.
- [x] `F-A`, `F-B` y Etapa A `Closed`; `OD-1` `RESOLVED`.
- [x] Acto de autorización ejercido (2026-10-13, mantenedor) con alcance, estado, nivel mínimo y límites.
- [x] Baseline verificada (rama `dev`, `HEAD` `3a31c53`, worktree limpio) y baseline de citas rotas (**26**).

## Alcance de este Change

### IN SCOPE

1. Registrar el **acto** con fecha, actor, transcripción, alcance heredado, artefacto designado y límites.
2. **Crear el Plan 165** (`docs/plans/165-f-c-autonomy-frontier-implementation.md`) con `Status: Aprobado para ejecución`, `Change Level L3`, `IN SCOPE`/`OUT OF SCOPE` heredados de `OD-1`, `FC-1`…`FC-10` y las **decisiones de implementación** identificadas sin resolver.
3. Anotar **aditivamente** en `<PLAN-163>` la resolución de su pending decision.
4. Reconciliar `ROADMAP.md` (nuevo `NEXT`; retiro del blocker de autorización ya otorgada), `docs/plans/INDEX.md` y `CHANGELOG.md`.

### OUT OF SCOPE

1. **Implementar `F-C`** o iniciar su Change de implementación.
2. Extender el scope más allá del `IN SCOPE` de `OD-1`; incorporar `C-16`/`C-17`/`C-21` o cualquier capacidad por simetría, disponibilidad tecnológica o madurez baja.
3. Modificar `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` o `dist/`.
4. Cambiar el default de `--sae`, los techos de recurso, el vocabulario de efectos o el envelope de `F-B`; modificar ADR-19.
5. Reabrir `F-A`, `F-B`, Etapa A, `OD-1` o el alcance 1B.
6. Resolver las decisiones de implementación del Plan 165.

### DEPENDENCIES

```text
F-A       = CLOSED   (precondición)
F-B       = CLOSED   (precondición; envelope intocable)
Etapa A   = CLOSED   (evidencia que delimitó el alcance)
OD-1      = RESOLVED (alcance canónico 1B)
F-C       = Aprobado para ejecución · implementación NOT_STARTED
Etapa B   = delimitada dentro de F-C (NOT_STARTED)
```

## Entregables

1. `docs/plans/164-acto-autorizacion-ejecucion-f-c.md` (**este archivo**) — registro del acto y del alcance heredado.
2. `docs/plans/165-f-c-autonomy-frontier-implementation.md` (**nuevo**) — Plan de ejecución de `F-C`, `Status: Aprobado para ejecución`, `Change Level L3`.
3. `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` — anotación aditiva de la resolución de su pending.
4. `ROADMAP.md` — `NEXT` con `F-C` autorizado y pendiente de ejecución; retiro del blocker de autorización; dependencias alineadas.
5. `docs/plans/INDEX.md` — encabezado de estado, serie **Nonagésima tercera** y filas de los Planes 164 y 165.
6. `CHANGELOG.md` — ítem `[Unreleased]` del Change.

## Pasos

1. **Paso 0 — preflight.** Baseline, dependencias y baseline de checkers.
2. **Paso 1 — registrar el acto.** Transcripción, autoridad, fecha, alcance heredado, artefacto designado, efecto sobre el estado y límite explícito (no implementa).
3. **Paso 2 — crear el Plan 165.** Header con `Status: Aprobado para ejecución` y `Change Level L3`; `IN SCOPE`/`OUT OF SCOPE` heredados; `FC-1`…`FC-10` sin debilitar; decisiones de implementación clasificadas; dependencias; pending decisions de implementación; anchor/checkpoint vacíos (no ejecutado).
4. **Paso 3 — anotar la pending.** Resolución aditiva en `<PLAN-163>`, preservando su texto.
5. **Paso 4 — reconciliar.** `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`.
6. **Paso 5 — verificar.** Batería canónica, gates C-1/C-2/C-3, verificación de las quince condiciones de validación del acto y verificación de scope.
7. **Paso 6 — cerrar.** `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y commit atómico.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [x] El acto está registrado con **fecha (2026-10-13)** y **actor (mantenedor)**, su transcripción, su alcance heredado y su límite explícito.
- [x] Existe **un único** Plan de ejecución de `F-C` (`docs/plans/165-f-c-autonomy-frontier-implementation.md`).
- [x] Su `Status` es exactamente **`Aprobado para ejecución`** y su `Change Level` es **`L3`** (≥ L3), con el cálculo registrado.
- [x] Contiene `FC-1`…`FC-10` sin reducción de garantías respecto del Plan 163.
- [x] Su `IN SCOPE` coincide con el de `OD-1` y `C-16`/`C-17`/`C-21` permanecen **fuera**.
- [x] Las ocho decisiones de implementación quedan identificadas con su clasificación, sin resolverlas arbitrariamente.
- [x] La pending decision de `<PLAN-163>` queda anotada como **resuelta** (aditivo, `PC-1` preservado).
- [x] `F-A`, `F-B` y Etapa A permanecen `Closed`; `OD-1` permanece `Resolved`; `F-C` no se implementó.
- [x] **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.
- [x] Batería canónica en verde (con el rojo preexistente declarado) y sin aumento de citas rotas; `## Validation anchor` y `## Checkpoint / cierre` registrados.

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

Verificación factual adicional: las quince condiciones de validación del acto (registro con fecha y actor; unicidad del Plan de `F-C`; estado exacto; `Change Level ≥ L3`; `FC-1`…`FC-10`; coincidencia de `IN SCOPE` con `OD-1`; `C-16`/`C-17`/`C-21` fuera; decisiones de implementación identificadas; `F-A`/`F-B`/Etapa A `Closed`; `OD-1` `Resolved`; ninguna implementación; 0 diff fuera del `Scope`); `git diff --name-only HEAD` ⊆ `Scope`.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las cinco rutas que la identidad de contenido mide — `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` (anotación aditiva de la pending) y `docs/plans/165-f-c-autonomy-frontier-implementation.md` (Plan creado). Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 149/155–163). El scope autorizado por `P-8` tiene una ruta más: este artefacto.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md` §4.1 + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual de las quince condiciones de validación del acto (registro con fecha y actor; unicidad del Plan de `F-C`; estado exacto `Aprobado para ejecución`; `Change Level ≥ L3`; `FC-1`…`FC-10`; coincidencia del `IN SCOPE` con `OD-1`; `C-16`/`C-17`/`C-21` fuera; decisiones de implementación identificadas; `F-A`/`F-B`/Etapa A `Closed`; `OD-1` `Resolved`; ninguna implementación de `F-C`; 0 diff fuera del `Scope`).
- **Effective inputs (repo content):** el scope declarado; `docs/CONVENTIONS.md` (alcance canónico 1B); Plan 163 (criterios y pending anotada); Plan 162; la matriz de Etapa A; `docs/plans/_TEMPLATE.md`; el corpus completo de `docs/plans/`, `docs/rfc/` y `docs/adr/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git`; `pytest` con basetemp externo al repositorio (`tests/pytest_isolation.py`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.0.3; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`); `check_plan_citations.py` sigue rojo por las **26** citas rotas históricas, **sin aumento**. No se consumió red, provider ni credenciales.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `d4a448b2b2ce2b1108c401a392a7f3f402259260` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado antes de escribir los registros de cierre.
  - **Delta scoped identity (scope S = las cinco rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `d37cfd2aab8ff271310d033044d92f6682c5be32252349b5e9038aa8b011035d`.
  - **Scope set (repo-relative paths, ordenados):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/163-acto-autoridad-od1-alcance-f-c.md`, `docs/plans/165-f-c-autonomy-frontier-implementation.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (216 archivos, 10457 referencias); verification-02 (`check_plan_citations`): **FAIL preexistente** — 26 citas rotas, sin aumento; verification-03 (`check_plan_structure`): **PASS** (165 documentos conformes); verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS**; verification-07 (`python -m pytest tests/`): **PASS** — `1316 passed` en 430,03 s; verification-08 (C-1): plan 164 **VALID**, plan 165 **`N/A`** (miembro del régimen sin validación registrada: correcto para `Aprobado para ejecución`), `GAP=0`, `ANOMALY=0`; verification-09 (C-2): plan 165 **`N/A`**, `ANOMALY=0`; verification-10 (C-3): `GAP=0`, `ANOMALY=0`. Verificación factual: el acto queda registrado con fecha (2026-10-13) y actor (mantenedor); existe **un único** Plan de ejecución de `F-C` (165) con `Status: Aprobado para ejecución` y `Change Level L3`; `FC-1`…`FC-10` presentes sin reducción; `IN SCOPE` coincidente con `OD-1`; `C-16`/`C-17`/`C-21` fuera; las ocho decisiones de implementación identificadas y clasificadas; `F-A`/`F-B`/Etapa A `Closed`; `OD-1` `Resolved`; **ninguna** implementación de `F-C`; `git diff --name-only` ⊆ el scope de `P-8`; **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(plans): authorize F-C execution and create its implementation plan (plan 164)`. Se identifica por su mensaje (convención anti-circularidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `d4a448b2b2ce2b1108c401a392a7f3f402259260`, delta scoped identity `d37cfd2aab8ff271310d033044d92f6682c5be32252349b5e9038aa8b011035d`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `d37cfd2aab8ff271310d033044d92f6682c5be32252349b5e9038aa8b011035d` / `d4a448b2b2ce2b1108c401a392a7f3f402259260`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY`.
- **Governance aplicada:** Plan 165 creado con `Status: Aprobado para ejecución` y `Change Level L3` (contrato operativo del Change de implementación, con `FC-1`…`FC-10`, efectos declarados y `ID-1`…`ID-8`); `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` (anotación **aditiva** de la resolución de su pending, regla `PC-1`); `ROADMAP.md` (retiro del blocker de autorización ya otorgada; `F-C` aprobado y pendiente de ejecución en `NEXT`; fecha); `docs/plans/INDEX.md` (encabezado de estado y serie **Nonagésima tercera** + filas de los Planes 164 y 165); `CHANGELOG.md` `[Unreleased]`; `**Status:** Executed`. Sin RFC-56 (0 diff en `protocol/`), sin ADR nuevo, sin `VERSION` bump ni tag.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `docs/plans/165-f-c-autonomy-frontier-implementation.md` (aspecto: no existía contrato operativo para la implementación de `F-C`, de modo que el alcance autorizado habría quedado sin artefacto ejecutable; actualización: Plan completo con autorización, alcance heredado, `FC-1`…`FC-10`, efectos declarados y decisiones de implementación; evidencia: el artefacto y su índice en el anchor). `ROADMAP.md` (aspecto: `F-C` figuraba como alcance resuelto **sin** autorización de ejecución y con una fila de blocker por la autorización faltante; actualización: `F-C` **aprobado para ejecución** y pendiente de implementación, blocker retirado, fecha al 2026-10-13; evidencia: el diff). `docs/plans/163-…md` (aspecto: su pending de autorización de ejecución quedaba `PENDING_AUTHORITY` aunque el acto ya existía; actualización: anotación aditiva de la resolución preservando el texto original; evidencia: el diff). `docs/plans/INDEX.md` y `CHANGELOG.md` por el registro del Change. **No** se actualiza ningún documento histórico (RFC-46): los Planes 149/151–163, ADR-19 y ADR-16 quedan intactos, y `docs/CONVENTIONS.md` **no** se modifica (el alcance 1B ya estaba registrado y este acto no lo cambia).
- **Roadmap impact:** `REQUIRED` — reconciliado en el artefacto que posee el estado. Ítems afectados: la fila de blocker «Ejecución de `F-C` **no autorizada**» **se retira** (la autorización fue otorgada); la card de `NEXT` pasa a declarar `F-C` **aprobado para ejecución** con enlace al Plan 165 y al acto (Plan 164); `Trabajo activo` refleja que la implementación corre en el Change siguiente; el grafo de dependencias no cambia (`A → F-C ← E`, `F-C → Etapa C`). `NOW` y `LATER` conservan sus ítems; las brechas del payload siguen explícitamente **fuera** de `F-C`.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

- `<PLAN-164>` — decisión: **decisiones de implementación de `F-C`** (provider/modelo concreto; arquitectura del actor; diseño del aislamiento/sandbox; esquema de integración de Memory; mecanismo del objetivo multi-Change; contención de autoridad fuera del host; estrategia de recuperación/retry; resolución de la discrepancia declarada entre la política de retry y su implementación); blocking: **sí** para ejecutar `F-C`; **no** para el resto del repositorio; owner: **`<PLAN-165>`** (las registra y clasifica) con escalación al **mantenedor** para las que requieran decisión explícita; resolución: **`PENDING`** — no se resuelven aquí ni en el Plan 163; evidencia: `docs/plans/165-f-c-autonomy-frontier-implementation.md` (sección de decisiones de implementación); efecto downstream: condicionan el diseño del Change de implementación bajo el alcance ya autorizado; ADR-worthiness: a evaluar en el Plan 165.

## Riesgos

1. **Extender el scope al crear el Plan.** Mitigación: `IN SCOPE`/`OUT OF SCOPE` copiados literalmente de `OD-1`; prohibición explícita de incorporar capacidades por simetría o madurez baja.
2. **Autorizar de más.** Mitigación: el acto autoriza la ejecución **bajo el alcance 1B** y la creación del Plan; **no** autoriza implementar dentro de este Change ni extender el scope.
3. **Debilitar `FC-1`…`FC-10`.** Mitigación: los criterios se copian del Plan 163 sin redefinición; cualquier ajuste futuro exigiría un acto propio.
4. **Resolver diseño por conveniencia.** Mitigación: las ocho decisiones de implementación se registran como pendientes con su clasificación; ninguna se resuelve en este Change.
5. **Reabrir artefactos cerrados.** Mitigación: `F-A`, `F-B`, Etapa A, `OD-1` y el alcance 1B no se tocan; sobre `<PLAN-163>` sólo se agrega la anotación aditiva de su pending (regla `PC-1`).

## Trazabilidad

```text
Etapa A (161, Closed) → evidencia
        │
        ▼
OD-1 (163, Closed) → alcance canónico 1B + criterios FC-1…FC-10 + pending de ejecución
        │
        ▼
ACTO DEL MANTENEDOR (2026-10-13) → autoriza ejecución de F-C y creación de su Plan
        │
        ▼
Plan 164 (este) → registra el acto · crea el Plan 165 · reconcilia la gobernanza
        │
        ▼
Plan 165 · Status: Aprobado para ejecución · Change Level L3 · FC-1…FC-10
        │
        ▼
[ Change de implementación de F-C ]  →  Etapa C
```

## Nota de ejecución

*2026-10-13. Ejecutado en `dev` @ `3a31c53` (baseline del preflight: worktree limpio; `dev` ahead 15 de `origin/dev`; `VERSION` del payload `12.0.1` sin tag; batería canónica en verde).*

Una sola pasada, en el orden del `## Pasos`:

1. **Paso 0 — preflight.** Baseline, dependencias (`F-A`/`F-B`/Etapa A `Closed`; `OD-1` `RESOLVED`) y baseline de citas rotas (**26**).
2. **Paso 1 — acto registrado.** Transcripción literal, autoridad (mantenedor), fecha efectiva (2026-10-13), alcance heredado (1B), artefacto designado (Plan 165), efecto sobre el estado (`SCOPED` → `Aprobado para ejecución`) y límite explícito (la autorización **no** habilita implementar en este Change).
3. **Paso 2 — Plan 165 creado.** `Status: Aprobado para ejecución`; `Change Level` **L3** con el cálculo por ejes; `IN SCOPE`/`OUT OF SCOPE` heredados literalmente de `OD-1`; `FC-1`…`FC-10` sin reducción; `## Efectos declarados` (`network` autorizado; `install`/`remote_git`/`destructive`/`write_outside_project` **no** declarados ni autorizados); las ocho decisiones de implementación clasificadas; `## Validation anchor` y `## Checkpoint / cierre` **vacíos** (no ejecutado, sin condición derivada).
4. **Paso 3 — pending resuelta.** Anotación **aditiva** en `<PLAN-163>`, preservando su texto (regla `PC-1`).
5. **Paso 4 — reconciliación.** `ROADMAP.md` (blocker de autorización retirado; `F-C` aprobado en `NEXT`; fecha), `docs/plans/INDEX.md` (serie Nonagésima tercera + filas de los Planes 164 y 165) y `CHANGELOG.md`.
6. **Paso 5 — verificación.** Las quince condiciones de validación del acto: (1) acto registrado con fecha y actor ✓; (2) **un único** Plan de ejecución de `F-C` ✓; (3) `Status` exactamente `Aprobado para ejecución` ✓; (4) `Change Level ≥ L3` (L3) ✓; (5) `FC-1`…`FC-10` presentes ✓; (6) `IN SCOPE` coincide con `OD-1` ✓; (7) `C-16`/`C-17`/`C-21` fuera ✓; (8) decisiones de implementación identificadas ✓; (9) `F-A`/`F-B`/Etapa A `Closed` ✓; (10) `OD-1` `Resolved` ✓; (11) ninguna implementación de `F-C` ✓; (12) **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/` ✓ —no se requirió ninguna modificación documental fuera del `Scope`—; (13) checkers canónicos en verde con **26** citas rotas (baseline) ✓; (14) `git diff` ⊆ `Scope` y worktree limpio al cerrar ✓; (15) sin push, merge, tag, promoción ni release ✓. Gates C-1/C-2/C-3 sin `ANOMALY`.
7. **Paso 6 — cierre.** `## Validation anchor` A1, `## Checkpoint / cierre`, esta nota y commit atómico.

**Resultado.** `RESULT = FC_EXECUTION_AUTHORIZED`: el acto quedó registrado, el Plan de ejecución de `F-C` creado y formalizado en `Aprobado para ejecución` con `Change Level L3`, `FC-1`…`FC-10` y las decisiones de implementación explícitas. **Este Change autoriza y formaliza; no ejecuta `F-C`.** No hubo findings: checkers y gates quedaron verdes en la primera pasada.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

`OD1 = CLOSED` · `F-C_SCOPE = 1B / CLOSED` · `F-C_PLAN = CREATED` · `F-C_PLAN_STATUS = Aprobado para ejecución` · `F-C_CHANGE_LEVEL = L3` · `F-C_IMPLEMENTATION = NOT_STARTED` · `ETAPA_B = NOT_STARTED`.

**Próximo paso exacto.** Iniciar el **Change de implementación de `F-C`** ejecutando el Plan 165: resolver primero `ID-1`, `ID-3` e `ID-5` (actos del mantenedor) y `ID-6` si escala a payload, y sólo entonces diseñar, implementar y falsar por capacidad (`FC-1`…`FC-10`).
