# Plan 175 — Theoretical Execution (DEV v1)

**Status:** Executed (parcial: Validation Anchor y Checkpoint pendientes de registro)
**Fecha:** 2026-10-24
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 2 — multi-área DEV (`runtime/`, `tests/`, `.agents/`, `docs/`). *architectural impact*: 2 — nuevo paquete y contrato local, aditivo y reversible; no cambia ningún contrato del payload. *release impact*: 0 — sin payload, sin versión ni tag (RFC-69). *duration/complexity*: 2 — engine, checks, CLI, suite y dogfood.
**Depende de:** —
**Origen:** instrucción directa del mantenedor (2026-10-24) y diseño TE cerrado en la sesión de diseño; no hay tracker de origen.
**Superseded por:** —

## Objetivo

Implementar **Theoretical Execution (TE) v1** exclusivamente en DEV: un engine determinista que construye un `DeclaredOverlay` sobre un commit, enumera los ítems de un Implementation Plan commiteado, ejecuta CH-1…CH-8, aplica las reglas mecánicas de autoridad y verificación, valida un `TE_RESULT` y deriva su `status`; más una policy que define cómo el **productor** (agente/humano que invoca TE) realiza las dimensiones semánticas y entrega su atestación.

TE v1 no escribe, no ejecuta el Plan, no persiste, no se integra al `ExecutionHost` y no toca el Protocol.

## Derivación y premisas

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Implementar TE v1 en DEV según el diseño cerrado; sin payload, sin host, sin persistencia propia | humano | instrucción del mantenedor (2026-10-24); este Plan |
| `P-2` Confianza de intención | `HIGH` — el diseño está cerrado y las tres ambigüedades (Gate B, precedencia de status, `--compare`) tienen regla única | agente | este Plan, §Design detail 5/7/12 |
| `P-3` Conjunto de contexto | `AGENTS.md`; `.agents/AGENTS.md`; `docs/plans/_TEMPLATE.md`; `docs/placement-contract.md`; `docs/rfc/75`; `docs/adr/16`; `docs/adr/19`; planes 122, 135, 138, 159, 173, 174; `runtime/orchestrator/{observation,contracts,worker,authority}.py`; `tools/check_plan_citations.py`; `tools/check_lifecycle_checkpoint.py`; `tools/scoped_content_identity.py`; `tests/AGENTS.md`; `PRIORITY.md` | agente | lista de `ruta:sección` de este Plan |
| `P-4` Derivabilidad | `DERIVABLE` — la normativa vigente (RFC-75, RFC-56 N/A, RFC-46, VC-1/GC-1/LC-1/PC-1) y el diseño cerrado determinan el trabajo; no hay decisión de autoridad pendiente. La única puerta es la autorización de ejecución del mantenedor | agente | este Plan; `## TE self-evaluation` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type` |
| `P-6` Conocimiento vigente | `AGENTS.md` raíz, `.agents/` y `docs/` activos; RFC-75 `Accepted`; ADR-16/19 `Accepted`; planes 122/135/138/159/173/174 `Closed` | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (lifecycle), RFC-46 (no reescribir historia), RFC-56 (N/A), RFC-69 (sin release), VC-1, GC-1, LC-1, PC-1, `docs/VERSIONING.md:4.1` | agente | `docs/VERSIONING.md`; `docs/CONVENTIONS.md` |
| `P-8` Autoridad y scope | Autoridad: mantenedor, por instrucción directa que autoriza la redacción; la ejecución requiere `Aprobado para ejecución`. Scope: deliverables = `## Entregables`; editable = `## Delegación agentiva` | humano | este Plan |

## Criterio de entrada

- [x] Diseño TE cerrado (`TE_DEV_DESIGN_STATUS = READY_FOR_IMPLEMENTATION`, con las tres correcciones de este Plan).
- [x] Este Plan commiteado en `dev` y registrado en `docs/plans/INDEX.md`.
- [x] `## TE self-evaluation` ejecutada conceptualmente, con `OPEN_FINDINGS = 0` o findings dispositionados.
- [x] Autorización humana de ejecución (`Aprobado para ejecución`); la redacción no la sustituye.
- [x] S0 (redacción) no requiere autorización de ejecución; S1–S7 se ejecutan bajo `Aprobado para ejecución` y S8 (validación/cierre) comienza bajo esa autorización y puede registrar `Executed`/`Closed`. Gate B (S7) precede al cierre (S8).

## Entregables

1. `runtime/theoretical/__init__.py`
2. `runtime/theoretical/overlay.py`
3. `runtime/theoretical/identity.py`
4. `runtime/theoretical/proposal.py`
5. `runtime/theoretical/checks.py`
6. `runtime/theoretical/result.py`
7. `runtime/theoretical/__main__.py`
8. `.agents/policies/theoretical-execution.md`
9. `.agents/AGENTS.md` (fila de puntero)
10. `runtime/README.md` (sección TE)
11. `tests/test_theoretical_overlay.py`
12. `tests/test_theoretical_identity.py`
13. `tests/test_theoretical_proposal.py`
14. `tests/test_theoretical_checks.py`
15. `tests/test_theoretical_result.py`
16. `tests/test_theoretical_cli.py`
17. `tests/test_theoretical_isolation.py`
18. `tests/test_theoretical_dogfood.py`
19. `tests/AGENTS.md` (fila del test anclado)
20. `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`
21. `docs/working/proposals/INDEX.md` (fila del registro)
22. `docs/plans/INDEX.md` (fila de este Plan)
23. `CHANGELOG.md` (`[Unreleased]`)

**Deliverable scope ≠ delegation/editable scope.** `## Entregables` enumera los artefactos de implementación cuyo contenido mide el Validation Anchor. `## Delegación agentiva` enumera los paths que el agente puede modificar durante la ejecución; incluye el propio Plan 175 como registro de gobernanza (y `docs/plans/INDEX.md` como deliverable/registro). Pertenecer al scope editable no convierte un path en deliverable medido: el Plan 175 es editable y está excluido del scope medido por anti-auto-referencia.

## Pasos

| Fase | Contenido | Gate |
|---|---|---|
| **S0** | Crear este Plan, registrarlo en el INDEX y ejecutar `## TE self-evaluation` (Gate A conceptual; redacción, sin ejecución) | Sin findings materiales abiertos |
| **A** | Autorización humana de ejecución (`Aprobado para ejecución`); la redacción no la sustituye | Entry criteria cumplidos; autorización registrada |
| **S1** | `overlay.py` + `identity.py` + tests | Unit verde |
| **S2** | `proposal.py` (carga, enumeración, DCM) + tests | Enumeración estable |
| **S3** | `checks.py` CH-1…CH-8 + tests (un check por vez) | Cada check con positivo/negativo |
| **S4** | `result.py` (contrato, validación, status derivado, staleness) + tests | `--validate` deriva status |
| **S5** | `__main__.py` (CLI) + tests | Exit codes y no-escritura |
| **S6** | `__init__.py`, `test_theoretical_isolation.py`, policy y documentación | No writes/no import |
| **S7** | **Gate B**: TE run del Plan 175 (productor semántico + engine) y registro Working | `CONVERGED` o findings dispositionados |
| **S8** | Batería, C-1/C-2/C-3, Validation Anchor, Checkpoint, `Executed`/`Closed` | Cierre |

## Delegación agentiva

- **Task:** Implementar TE v1 en DEV según este Plan. El productor (agente/humano) realiza `completeness`, `consistency` y `adversarial` y entrega su atestación en el `TE_RESULT`; el engine ejecuta CH-1…CH-8, las reglas mecánicas de `authority` y `verification`, valida la cobertura y deriva el `status`. El engine no ejecuta dimensiones semánticas y no puede declarar `CONVERGED` por sí mismo.
- **Scope (editable; no es el conjunto medido):** `docs/plans/175-theoretical-execution-dev-v1.md`, `docs/plans/INDEX.md`, `runtime/theoretical/__init__.py`, `runtime/theoretical/overlay.py`, `runtime/theoretical/identity.py`, `runtime/theoretical/proposal.py`, `runtime/theoretical/checks.py`, `runtime/theoretical/result.py`, `runtime/theoretical/__main__.py`, `.agents/policies/theoretical-execution.md`, `.agents/AGENTS.md`, `runtime/README.md`, `tests/test_theoretical_overlay.py`, `tests/test_theoretical_identity.py`, `tests/test_theoretical_proposal.py`, `tests/test_theoretical_checks.py`, `tests/test_theoretical_result.py`, `tests/test_theoretical_cli.py`, `tests/test_theoretical_isolation.py`, `tests/test_theoretical_dogfood.py`, `tests/AGENTS.md`, `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`, `docs/working/proposals/INDEX.md`, `CHANGELOG.md`.
- **Resource ceiling:** 24 ejecuciones delegadas.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change solo escribe documentación DEV, código runtime y tests locales; no hay red, git remoto, instalación, operación destructiva ni escritura fuera del proyecto | instrucción del mantenedor (2026-10-24) + este Plan | authorized |

## Criterios de salida

- [x] `runtime/theoretical/` implementa `DeclaredOverlay`, `InputIdentity`, `RunIdentity`, enumeración, CH-1…CH-8, contrato, validación, status derivado, staleness y CLI.
- [x] `--emit` produce un skeleton con dimensiones de productor `PENDING` y dimensiones de engine computadas; `--validate` rechaza `CONVERGED` con `PENDING` o con status no derivado.
- [x] `--stale` usa solo `InputIdentity`; `--compare` no afirma `resolved`/`reopened`.
- [x] La suite cubre no-mutación, no-store, dirección de importación, overlay, identidad, contrato, estados, checks, obligaciones y dogfood.
- [x] El Gate B deja un registro Working con el `TE_RESULT` y los findings; `CONVERGED` o findings dispositionados por el humano.
- [x] `runtime/README.md`, `.agents/policies/theoretical-execution.md`, `.agents/AGENTS.md`, `tests/AGENTS.md` y `CHANGELOG.md` actualizados.
- [ ] Batería canónica, C-1/C-2/C-3 en verde; `## Validation anchor` y `## Checkpoint / cierre` registrados; condición derivada evaluada.
- [x] Sin cambios en `protocol/`, `dist/`, `VERSION`, `ExecutionHost`, `runtime/orchestrator/derivation.py` ni la batería.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python tools/check_enforcement_declarations.py
python -m pytest tests/
python -m pytest tests/test_theoretical_overlay.py tests/test_theoretical_identity.py tests/test_theoretical_proposal.py tests/test_theoretical_checks.py tests/test_theoretical_result.py tests/test_theoretical_cli.py tests/test_theoretical_isolation.py tests/test_theoretical_dogfood.py
python -m runtime.theoretical --plan 175 --base HEAD --emit
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

La salida de `--emit` se redirige a un archivo fuera del repositorio; la CLI no escribe archivos. `--validate` sobre el skeleton debe aceptar el `status=GAP` estructural (dimensiones de productor `PENDING`) y salir 0.

## Validation anchor

<!-- Se completa al validar (VC-1). -->

## Checkpoint / cierre

<!-- Se completa al cerrar (GC-1). -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A.

### Correcciones

N/A.

### Pending decisions

N/A.

## Riesgos

- **Atestación semántica no verificable.** El productor puede declarar dimensiones que no ejecutó. Mitigación: `producer` + `probed` + `INV-03`; límite declarado, no eliminable.
- **Deriva de checks.** Un cambio semántico en CH-x sin bump de versión deja resultados incomparables sin detectarlo. Mitigación: `check_set {id, version}` + `INCOMPARABLE`.
- **Falsa convergencia.** Mitigación: cobertura enumerada, status derivado, `PREDICTION` no verificable, `NOT_EVALUABLE → obligación`, cinco dimensiones, `probed` no vacío, `RESIDUAL` con `accepted_by`.
- **Bootstrapping del dogfood.** No se puede ejecutar el engine antes de implementarlo. Mitigación: Gate A conceptual (productor) + Gate B real (productor + engine) antes del cierre.
- **Acoplamiento a `observation.py`.** El módulo importa `store`; no se instancia. Mitigación: `test_theoretical_isolation.py`.
- **Sobre-scope.** 23 deliverables (24 paths editables, incluido el Plan como registro). Mitigación: fases S0–S8, cada una verde antes de la siguiente; la autorización de ejecución precede a S1.

## Trazabilidad

```text
diseño TE cerrado (auditoría + TE del diseño)
        ↓
Plan 175 (este documento)
        ↓
autorización humana (Aprobado para ejecución)
        ↓
runtime/theoretical + policy + tests + docs
        ↓
Gate B (TE run del Plan 175)
        ↓
batería + anclas + checkpoint
        ↓
Closed (dev) · Released = NO (sin payload, RFC-69)
```

## Nota de ejecución

**Ejecutado el 2026-10-24.** Change DEV **RFC-56 Class: N/A**, Change Level L2, sin payload, sin release (RFC-69). Implementación en `dev`.

- **S1–S6:** `runtime/theoretical/` (`overlay.py`, `identity.py`, `proposal.py`, `checks.py`, `result.py`, `__main__.py`, `__init__.py`), `.agents/policies/theoretical-execution.md` y su puntero, `runtime/README.md`, las ocho suites `tests/test_theoretical_*.py`, `tests/AGENTS.md`, el registro Working del Gate B y su INDEX, y `CHANGELOG.md`.
- **Gate B (S7):** base `86a7cb0`; productor `agent:deepseek-harness` (declarado, no verificado); el engine validó CH-1…CH-8, cobertura, identidad y obligaciones; `TE_RESULT` **`CONVERGED`** con 49/49 ítems, cinco dimensiones `PERFORMED` y sin findings. Registro: `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`.
- **Validación (S8):** 8 checkers PASS (`check_plan_structure` con los 2 `GAP` declarados 157/158; `check_version_state` con sus warnings históricos); `python -m pytest tests/` **1481 passed**; `git diff --check` limpio; CLI `--validate`/`--stale`/`--compare` con los exit codes previstos. `C-1/C-2/C-3` y el `## Validation anchor`/`## Checkpoint / cierre` se registran en el commit de cierre.
- **Condición derivada:** `Executed` (implementación + validación); `Closed` se deriva al registrar el anchor/checkpoint; `Committed` es estado del repositorio; `Released = NO`.

---

# Design and implementation detail

## 1. Scope and non-scope

**In scope:** los deliverables de `## Entregables` (medidos por el Validation Anchor); el conjunto editable se declara en `## Delegación agentiva`.

**Out of scope:** `protocol/`, `dist/`, `VERSION`, `ExecutionHost`, `runtime/orchestrator/derivation.py`, la batería canónica (no se agrega TE), discovery/audit/post-execution TE, RFC adapter, persistencia propia, `.project` store, provider/model/network/credentials, nuevo lifecycle/Change/findings/decisiones, `scenarios[]`, `ResultContentIdentity`.

## 2. Architecture

```text
                    ┌──────────────────────────────────────────┐
                    │ productor (agente/humano que invoca TE)  │
                    │  completeness · consistency · adversarial│
                    └───────────────┬──────────────────────────┘
                                    │ atestación (JSON)
base commit/tree ──► proposal.py ──► checks.py ──► result.py ◄── CLI
   (Git objects)      overlay/items   CH-1..CH-8    contract
                                    │                derive status
                                    ▼                validate
                              TE_RESULT (valor) ──► stdout
```

| Componente | Responsabilidad | Pureza |
|---|---|---|
| `overlay.py` | `DeclaredOverlay` trivaluado sobre el base | Puro, inmutable |
| `identity.py` | `InputIdentity`, `RunIdentity`, canonicalización | Puro |
| `proposal.py` | Carga el Plan, valida, enumera ítems, construye overlay | Puro, read-only |
| `checks.py` | CH-1…CH-8 deterministas | Puro, read-only |
| `result.py` | Contrato, validación, derivación de `status`, staleness | Puro |
| `__main__.py` | CLI | Sin escritura, sin red, sin shell |
| `.agents/policies/theoretical-execution.md` | Procedimiento del productor | Documento |

No hay motor, state machine, store, lifecycle, orquestador ni worker. El productor es el llamador; TE no lo invoca.

## 3. Contracts

| Tipo | Campos mínimos | Notas |
|---|---|---|
| `BaseState` | `commit`, `tree` | Resueltos con Git |
| `DeclaredOverlay` | `base`, `declared_paths`, `effects`, `content_policy="DECLARED_UNKNOWN"` | `frozen`; `touched`, `existence`, `content`, `paths`, `identity` |
| `InputIdentity` | `factual`, `projected`, `tool_version`, `check_set` | Estructural; gobierna staleness |
| `RunIdentity` | `te_id`, `input_identity`, `producer`, `created_at` | `te_id` es etiqueta, no identidad |
| `TE_RESULT` | §7 | JSON canónico |
| `DimensionRecord` | `executor`, `status`, `computed`, `capability`, `probed`, `claim_refs`, `finding_refs`, `escalation_refs`, `evidence_refs` | `computed` si incluye `engine`; `capability`+`probed` si incluye `producer` |
| `Claim` | `id`, `item`, `kind`, `support`, `evidence_class`, `evidence_refs`, `rule_ref`, `obligation_ref`, `statement`, `reason` | `PREDICTION` nunca `CHECKED` |
| `Assumption` | `id`, `statement`, `source`, `invalidated_by`, `affects` | `source ∈ {PREMISE_REF, ANALYSIS}` |
| `Finding` | `id`, `signal`, `statement`, `location`, `evidence_refs`, `disposition`, `escalation_ref`, `accepted_by` | `RESIDUAL` exige `accepted_by` resoluble |
| `Correction` | `id`, `finding_ref`, `target`, `statement`, `authority_required`, `applied=false` | `applied` siempre `false` |
| `VerificationObligation` | `id`, `for_claim`, `statement`, `falsified_if`, `depends_on`, `candidate`, `status="OPEN"` | `depends_on` = assumptions |
| `Escalation` | `id`, `decision`, `alternatives`, `why_not_derivable`, `consequences`, `recommendation`, `reversibility`, `affected_contracts` | No crea decisión |
| `ResidualRisk` | `id`, `description`, `why_not_resolvable`, `owner` | Límite de la evaluación |

Reglas de `falsified_if` / `depends_on` / `invalidated_by`:

- `assumptions[].invalidated_by` declara la condición que **anula la premisa**.
- `verification_obligations[].depends_on` lista las premisas de la predicción.
- `falsified_if` declara la observación que **refuta la predicción mientras las premisas se mantienen**.
- Si una premisa se invalida, la obligación es `NOT_APPLICABLE`, no `FAILED`; la predicción no se considera falsificada. TE no decide aplicabilidad: la registra y la obligación la evalúa el owner real.

## 4. Engine

- `overlay.py` lee solo objetos Git (`git rev-parse`, `git cat-file`, `git ls-tree`); nunca el working tree.
- `proposal.py` importa parsers de `runtime.orchestrator.observation`; no importa `host`, `worker` ni `store` (la importación de módulo arrastra `store`, pero el test verifica que no se instancia y no se escribe).
- `checks.py` importa `tools/check_plan_citations.py` y `tools/check_lifecycle_checkpoint.py` insertando `tools/` en `sys.path` la primera vez (mismo patrón que `observation.py` con `scoped_content_identity`).
- `result.py` no importa nada del host.
- `runtime/orchestrator/` no importa `runtime/theoretical/` (test estructural).

Pipeline de una pasada:

```text
load_proposal → build_overlay → enumerate_items → run_checks
→ emit_skeleton → [productor completa dimensiones/claims/findings]
→ validate_result → derive_status → (stdout)
```

No hay bucle en el engine. El productor itera editando el Plan y re-ejecutando.

## 5. Producer contract and Gate B

### 5.1 Quién ejecuta qué

| Dimensión | Ejecutor | Aporta el productor | Aporta el engine |
|---|---|---|---|
| `completeness` | productor | `probed` (requisitos/artefactos examinados), claims/findings | Inventario mecánico en `coverage.required_items` |
| `consistency` | productor | `probed` (pares comparados), findings | Citaciones y referencias resueltas |
| `adversarial` | productor | `probed` (escenarios/supuestos), claims `PREDICTION`, findings | Nada semántico |
| `authority` | engine+productor | `probed` (decisiones examinadas), `escalation_refs` | CH-1/CH-2/CH-4/CH-5 + esquema |
| `verification` | engine | Claims correctamente clasificados | Regla `NOT_EVALUABLE → obligación` |

### 5.2 Gate B — definición corregida

`FACT`: el engine no puede ejecutar `completeness`, `consistency` ni `adversarial` (no hay skill executor en DEV; las skills son `.md` y `runtime/orchestrator/agent_worker.py` (línea 76) declara que DEV no las consume). `INFERENCE`: llamar «TE automático» a Gate B atribuye al engine una capacidad que no posee. `DESIGN_DECISION`: Gate B es un **TE run con atestación semántica del productor y validación del engine**:

```text
Plan 175 commiteado
  ↓
productor ejecuta completeness/consistency/adversarial
  ↓
productor completa TE_RESULT (claims/findings/dimensiones) y lo guarda fuera del repo
  ↓
python -m runtime.theoretical --validate <result.json>
  ↓
engine: CH-1..CH-8, cobertura, identidad, obligaciones, status derivado
  ↓
CONVERGED | OPEN_FINDINGS | REQUIRES_HUMAN | GAP | NO_PROGRESS | RESOURCE_LIMIT
  ↓
registro Working del Gate B (producer + engine + resultado)
```

Reglas:

1. El engine **nunca** marca `PERFORMED` una dimensión de productor; solo acepta la atestación completa.
2. El engine **nunca** afirma haber ejecutado `completeness`, `consistency` o `adversarial`.
3. El test automático `test_theoretical_dogfood.py` verifica que el Plan 175 es enumerable, que el skeleton tiene las dimensiones de productor `PENDING`, que `authority`/`verification` están computadas, que una **fixture attestation** (etiquetada `producer: "test-fixture"`, `provenance.authority_basis: "TEST_FIXTURE"`) valida y que el engine no reclama semántica. La fixture **no** es un TE run real ni evidencia.
4. El Gate B real es el run del productor sobre el Plan 175, con su resultado registrado en `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`; el test no lo sustituye.
5. El `## TE self-evaluation` de este Plan es una atestación conceptual del productor (el autor del Plan), no una ejecución del engine.

### 5.3 Cómo entrega el productor la atestación

El productor ejecuta `--emit`, recibe el skeleton JSON y completa:

```jsonc
"coverage": { "dimensions": {
  "completeness": { "executor": "producer", "status": "PERFORMED",
                    "capability": "completeness-checker",
                    "probed": ["## Entregables", "## Criterios de salida"],
                    "claim_refs": ["TC-01"] },
  "consistency": { "executor": "producer", "status": "PERFORMED", "capability": "consistency-checker",
                   "probed": ["artifact set", "claim pairs"] },
  "adversarial": { "executor": "producer", "status": "PERFORMED", "capability": "critic",
                   "probed": ["T1", "T2"] },
  "authority":   { "executor": "engine+producer", "status": "PERFORMED",
                   "computed": true, "probed": ["scope", "effects"],
                   "evidence_refs": ["CH-1", "CH-5"] },
  "verification":{ "executor": "engine", "status": "PERFORMED",
                   "computed": true, "evidence_refs": ["TV-01"] }
}}
```

`PERFORMED` de productor exige `capability` no vacía y `probed` no vacía; `PERFORMED` de engine exige `computed: true` y `evidence_refs`; `PENDING` bloquea `CONVERGED`. No hay `scenarios[]`: la cobertura de escenarios examinados se registra en `dimensions.adversarial.probed`.

## 6. Checks CH-1…CH-8

| Check | Input | Lógica | Output | Failure modes | Tests |
|---|---|---|---|---|---|
| **CH-1** | `RFC-56 Class`, `declared_paths`, `scope` | ¿Hay paths `protocol/.agents/**`? ¿Clase N/A? ¿Clase A/B/C sin payload? | `ANOMALY` / `VALID` | Clase multi; comentarios; paths con `./` | `test_ch1_*` |
| **CH-2** | `## Entregables`, `Scope` | Si `Scope` explícito: todo entregable ∈ scope | `ANOMALY` / `GAP` (scope ausente) | Scope omitido (se usan entregables) | `test_ch2_*` |
| **CH-3** | Citas `ruta:sección` | `extract_citations` + `verify_citation`; path tocado → `GAP`+obligación; ausente no declarado → `ANOMALY`; target `Superseded` → `BOUNDARY`+obligación | `ANOMALY`/`BOUNDARY`/`GAP`/`VALID` | Citas a drafts; secciones retiradas; CRLF | `test_ch3_*` |
| **CH-4** | `declared_paths` que son plan/RFC/ADR | `status_base` + `post_close_violations` (R5) | `ANOMALY`/`BOUNDARY`/`VALID` | Plan no en HEAD → N/A; Git ausente → GAP | `test_ch4_*` |
| **CH-5** | Paths payload + `## Pasos`/`## Entregables` | Si payload y no se declara `VERSION`/`CHANGELOG` → obligación | `BOUNDARY`/`VALID` | No aplicar a RFC-56 N/A | `test_ch5_*` |
| **CH-6** | `## Criterios de salida`, `## Verificación`, obligaciones | Criterio sin comando ni `TV` → obligación | `BOUNDARY`/`VALID` | Verificación no mapeable 1:1 | `test_ch6_*` |
| **CH-7** | `## Validation anchor` (si existe) | Recomputar `scoped_content_identity` + `git rev-parse` | `ANOMALY`/`GAP`/`VALID`/`N/A` | Pre-ejecución sin anchor → N/A | `test_ch7_*` |
| **CH-8** | `base`, `proposal` | `git rev-parse <base>:<path>`; `git rev-parse <base>^{tree}` | `GAP`/`VALID` | Git ausente; base no commit | `test_ch8_*` |

CH-3 no produce `ANOMALY` por un target `Superseded` (evita falsos positivos en citas históricas legítimas); produce `BOUNDARY` + obligación de revisión. Un path tocado y desconocido produce `GAP`, nunca `ANOMALY`.

## 7. TE_RESULT and status

Campos obligatorios:

```text
schema_version · te_id · status · reason
provenance { kind:"theoretical", method, tool, tool_version, created_at, producer, authority_basis }
input { factual, proposal{path,blob,status}, check_set, previous_te_id, revision }
identity { factual, projected, inputs, run }
model { paths, effects, scope, content:"unknown" }
coverage { required_items, claims, checked, not_evaluable, not_applicable, dimensions{5} }
claims[] · assumptions[] · findings[] · corrections[]
verification_obligations[] · escalations[] · residual_risks[]
limits { unevaluated_areas[], declared_limits[] }
no_progress { fingerprint, previous_te_id }
```

Estados: `CONVERGED`, `OPEN_FINDINGS`, `REQUIRES_HUMAN`, `GAP`, `NO_PROGRESS`, `RESOURCE_LIMIT`.

### 7.1 Precedencia única (corregida)

`DESIGN_DECISION` — Una sola regla, la del diseño cerrado:

```text
CONVERGED
  > RESOURCE_LIMIT
  > NO_PROGRESS
  > GAP
  > REQUIRES_HUMAN
  > OPEN_FINDINGS
```

Derivación por `result.py`, en este orden exacto:

1. Si se cumplen las condiciones de `CONVERGED` → `CONVERGED`.
2. Si no, y `revision.index >= revision.ceiling` → `RESOURCE_LIMIT`.
3. Si no, y `previous` + fingerprint idéntico → `NO_PROGRESS`.
4. Si no, y hay una condición de GAP → `GAP`.
5. Si no, y hay ≥1 `ESCALATED` o escalación → `REQUIRES_HUMAN`.
6. Si no, y hay ≥1 `OPEN` → `OPEN_FINDINGS`.
7. Si no se cumple ninguna → el resultado es inválido (no existe un séptimo estado).

`reason` debe nombrar **todas** las condiciones aplicables, incluidas las preemptadas (p. ej. `RESOURCE_LIMIT` con un GAP de fondo). El productor no puede fijar el `status`; `--validate` lo recomputa y exige igualdad. Si el `status` declarado difiere del derivado, `--validate` imprime el valor derivado y sale 1; el productor actualiza el archivo y vuelve a validar (no hay un bucle en el engine).

Ejemplos que fijan la regla:

| # | Condiciones | Status |
|---|---|---|
| 1 | Sin findings; 5 dimensiones `PERFORMED`; sin GAP | `CONVERGED` |
| 2 | Sin findings; 5 dimensiones; ceiling alcanzado | `CONVERGED` (el límite no invalida un resultado completo) |
| 3 | 1 `OPEN`; ceiling alcanzado | `RESOURCE_LIMIT` |
| 4 | 1 `OPEN`; `previous` con mismo fingerprint | `NO_PROGRESS` |
| 5 | 1 `OPEN`; claim `UNCHECKED` | `GAP` |
| 6 | 1 `ESCALATED`; claim `UNCHECKED` | `GAP` |
| 7 | 1 `ESCALATED`; sin GAP | `REQUIRES_HUMAN` |
| 8 | 1 `OPEN`; sin GAP/escalación | `OPEN_FINDINGS` |
| 9 | 1 `RESIDUAL` con `accepted_by`; sin OTROS | `CONVERGED` |
| 10 | 1 `RESIDUAL` sin `accepted_by` | inválido (exit 1); no es un status |
| 11 | Sin findings; dimensión `PENDING` | `GAP` |
| 12 | Ceiling alcanzado; `previous` idéntico; GAP | `RESOURCE_LIMIT` |
| 13 | 1 `OPEN` + 1 `ESCALATED`; sin GAP | `REQUIRES_HUMAN` |
| 14 | Sin findings; `verification` sin obligaciones porque no hay `NOT_EVALUABLE` | `CONVERGED` |
| 15 | `PREDICTION` marcada `CHECKED` | inválido (no es un status) |

## 8. Identity and provenance

| Concepto | Definición | Uso |
|---|---|---|
| `FactualContentIdentity` | `{commit, tree}` | Base |
| `ProjectedContentIdentity` | `{kind:"declared_overlay", base, paths, effects, content:"unknown"}` | Overlay |
| `InputIdentity` | `{factual, projected, tool_version, check_set}` | Staleness, comparación |
| `RunIdentity` (`te_id`) | `te-<plan>-<base12>-<blob8>-<producer>-<utc>` | Referencia del run; **nunca** staleness |

- `--stale` recomputa `InputIdentity`; mismatch → `STALE`; tool/check-set distinto → `INCOMPARABLE`; no recomputable → `GAP`.
- Reproducible: checks, enumeración, validación, `InputIdentity`. No reproducible: claims/findings/status/reason semánticos.
- Dos productores pueden evaluar el mismo `InputIdentity` y producir resultados distintos; ambos son runs válidos. `--compare` lo reporta; no es un status.
- `producer` = declarado, no verificado (misma semántica que `ActorProvenance`, sin reutilizar la clase).

## 9. Convergence

`CONVERGED` = sin findings `OPEN`/`ESCALATED`, sin `UNCHECKED`, cinco dimensiones `PERFORMED`, todo `NOT_EVALUABLE` con obligación, límites declarados. No significa correcto, verificado, seguro ni listo para release.

- Falsa convergencia: cobertura enumerada, una claim por ítem, `PREDICTION` no verificable, `NOT_EVALUABLE → obligación`, cinco dimensiones, `probed` no vacío, `RESIDUAL` con `accepted_by`, `limits.unevaluated_areas`.
- No-progress: `(items, findings materiales, status)`; sin `previous`, N/A.
- Resource limit: `revision.index >= ceiling`; no autoriza.
- `OPEN_FINDINGS` es el estado normal de una revisión con problemas corregibles.

## 10. Authority

| TE puede | TE escala |
|---|---|
| Observar, analizar, detectar | Scope |
| Proponer correcciones | Clase RFC-56 / Level |
| Derivar obligaciones | Contradicción normativa |
| Clasificar escalaciones | RFC/ADR/Protocol/payload |
| Recomendar | Irreversible / reservado |
| Detenerse | Resolver finding |

- `escalations[]` con los campos completos; no crea `pending decision` (PC-1).
- `accepted_by` debe resolver a un artefacto commiteado (`ruta:sección`).
- Reinicio: decisión humana → nueva revisión commiteada → TE(N+1); o `accepted_by` → TE(N) re-ejecutado. No hay resume.

## 11. Verification bridge

```text
claim/prediction → verification_obligation → mecanismo real → evidencia → owner
```

| Campo | Regla |
|---|---|
| `falsified_if` | Observación que refuta la predicción **mientras las premisas se mantienen** |
| `depends_on` | Ids de `assumptions`; si una premisa se invalida, la obligación es `NOT_APPLICABLE`, no `FAILED` |
| `candidate` | `structural_checker`, `unit_test`, `integration_test`, `dogfood_test`, `runtime_check`, `manual_review`, `git_evidence`, `declared_environmental_gap` |
| `status` | Siempre `OPEN` |

No todo escenario es unit test. TE no satisface la obligación; la incorpora al Plan (`## Verificación`/`## Criterios de salida`) en la revisión siguiente.

## 12. CLI and compare

```bash
python -m runtime.theoretical --plan N [--base REF] --emit
python -m runtime.theoretical --validate FILE
python -m runtime.theoretical --stale FILE
python -m runtime.theoretical --compare PREV CUR
```

| Comando | stdout | Exit |
|---|---|---|
| `--emit` | Esqueleto JSON (status `GAP`, dimensiones de productor `PENDING`) | 0 ok; 2 base/plan ilegible o no commiteado |
| `--validate` | Problemas + status derivado | 0 válido; 1 inválido; 2 archivo ilegible |
| `--stale` | `fresh/stale/incomparable/gap` + identidades | 0 fresh; 1 stale/incomparable; 2 gap |
| `--compare` | Diferencias observadas; nunca `resolved`/`reopened` | 0 mismo input sin divergencia; 1 mismo input con divergencia; 2 input distinto/ilegible |

La CLI **nunca escribe archivos** (no `--out`); el llamador redirige stdout. No usa shell, red, modelo ni credenciales. `--base` se valida con `git rev-parse --verify` y se rechaza si empieza con `-`.

### 12.1 `--compare` corregido

`FACT`: los findings semánticos dependen del productor y no hay `ResultContentIdentity`. `INFERENCE`: un finding ausente en CUR no implica `resolved`; pudo no ser detectado. `DESIGN_DECISION`: Opción A, comparación estructural/observacional.

| Situación | Salida | Exit |
|---|---|---|
| `InputIdentity` distinta | `INPUT_CHANGED`; solo diferencias estructurales; semántica `NOT_COMPARABLE` | 2 |
| Mismo input; mismos findings materiales | `SAME_INPUT`; `only_in_prev=[]`, `only_in_cur=[]`, `semantic_divergence=false` | 0 |
| Mismo input; findings distintos | `SAME_INPUT`; `only_in_prev`, `only_in_cur`, `semantic_divergence=true` | 1 |
| Mismo input; cambia `support` de un claim | `claim_support_changes` | 1 si es material |
| Archivo inválido/ilegible | error | 2 |

`--compare` **no** emite `resolved`, `reopened` ni `progress`; solo diferencias observadas. La interpretación es humana. No se introduce un tracker ni una identidad de continuidad.

## 13. Tests

| Archivo | Casos MUST |
|---|---|
| `test_theoretical_overlay.py` | path declarado → `DECLARED_UNKNOWN`; no declarado → base; working tree ignorado; inmutable; identidad estable |
| `test_theoretical_identity.py` | mismo input → misma `InputIdentity`; runs distintos → `te_id` distinto; staleness solo por inputs; `te_id` no gobierna staleness |
| `test_theoretical_proposal.py` | enumeración de entregables/pasos/criterios/efectos/premises; secciones ausentes → GAP; scope≠paths; status aceptado/rechazado |
| `test_theoretical_checks.py` | CH-1…CH-8 positivo/negativo; CH-3 path tocado → GAP; target superseded → BOUNDARY; CH-4 plan cerrado; CH-8 no commiteado |
| `test_theoretical_result.py` | schema; claves desconocidas; `PREDICTION` no `CHECKED`; `RESIDUAL` sin `accepted_by`; `applied=true`; status derivado y mismatch; los 15 ejemplos de §7.1; `depends_on`/`falsified_if` |
| `test_theoretical_cli.py` | `--emit`/`--validate`/`--stale`/`--compare`; exit codes; stdout only; JSON válido; `--compare` nunca emite `resolved`/`reopened` |
| `test_theoretical_isolation.py` | no writes (`git status` + hashes); no `.project`; no store; `orchestrator` no importa `theoretical`; stdlib-only |
| `test_theoretical_dogfood.py` | Plan 175 real: enumerable; skeleton con productor `PENDING`; `authority`/`verification` computadas; fixture attestation válida (etiquetada fixture); el engine no reclama semántica |

`DESIGN_DECISION` — La suite usa `pytest_isolation.scratch_root("theoretical")`; no escribe en el repo. `test_theoretical_dogfood.py` se registra en `tests/AGENTS.md` como anclado.

## 14. Documentation

| Documento | Cambio | Contenido |
|---|---|---|
| `.agents/policies/theoretical-execution.md` | Crear | Definición, unidad, inputs, overlay, identidad, dimensiones/ejecutores, checks, productor, Gate B, resultado, convergencia, autoridad, verificación, CLI/compare, persistencia, fallos, non-goals |
| `.agents/AGENTS.md` | Editar | Fila: «Evaluating a proposal theoretically (TE) → `policies/theoretical-execution.md`» |
| `runtime/README.md` | Editar | Sección «Theoretical Execution (plan 175)»: módulos, CLI, límites |
| `tests/AGENTS.md` | Editar | Fila del test anclado `test_theoretical_dogfood.py` |
| `docs/plans/INDEX.md` | Editar | Fila del Plan 175 |
| `CHANGELOG.md` | Editar | `[Unreleased]` `(plan 175, RFC-56 N/A)` |
| `docs/working/proposals/INDEX.md` | Editar | Fila del registro del Gate B |

No se modifica `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` raíz ni `docs/glossary/`. `Documentation impact: REQUIRED` (los seis primeros); `Roadmap impact: NOT_REQUIRED` (no hay iniciativa TE en `ROADMAP.md`).

## 15. Integration

```text
Plan 175 commiteado (Aprobado para redacción)
  ↓ S0: Gate A conceptual (redacción; sin ejecución)
  ↓ A: autorización humana (Aprobado para ejecución)
  ↓ S1–S6: implementación de TE v1
  ↓ S7: Gate B (productor semántico + engine) → CONVERGED o findings dispositionados
  ↓ S8: validación, Validation Anchor, Checkpoint, cierre
```

- Discovery/audit/context recovery/orchestration: **sin integración**.
- Execution: TE no participa; el host no lee TE.
- Recovery: rerun desde inputs; sin resume.
- `## Delegación agentiva` del Plan: `Task` = implementar TE v1; `Scope` editable = los paths de `## Entregables` + el Plan (no es el conjunto medido); `Resource ceiling` = 24. El host puede conducir la implementación si el Plan está `Aprobado para ejecución`; TE no lo requiere.

## 16. Failure / recovery

| Caso | Comportamiento |
|---|---|
| Base inexistente/ilegible | `--emit` exit 2, error estructurado, sin JSON parcial |
| Proposal no commiteada | `GAP` (`PROPOSAL_NOT_IN_BASE`), exit 2 |
| Plan `Superseded` | `GAP` (`PROPOSAL_SUPERSEDED`), exit 2 |
| Contenido declarado desconocido | Normal: overlay `DECLARED_UNKNOWN`; CH-3 → GAP + obligación |
| Input stale | `--stale` exit 1; no se reutiliza |
| GAP de información | `status=GAP`; el productor obtiene el insumo |
| Attestation incompleta | `--validate` exit 1, dimensión `PENDING` |
| No-progress | `status=NO_PROGRESS` si hay `previous` |
| Resource limit | `status=RESOURCE_LIMIT`; no autoriza |
| Schema inválido | exit 1 con problemas deterministas |
| Git ausente | `GAP` (factor ambiental) |
| Plan sin `premises(D)` | `GAP` finding + obligación; no bloquea `--emit`; bloquea `CONVERGED` salvo `RESIDUAL` aceptado |

Recovery = re-ejecutar con los mismos inputs; el resultado semántico puede diferir (declarado). No hay reanudación parcial.

## 17. Security / authority

- **No escritura**: la CLI no abre archivos en modo escritura; test de `git status` + hashes.
- **No ejecución**: no shell, no tests reales, no `ExecutionHost`.
- **No red/modelo/credenciales**.
- **Path handling**: paths normalizados POSIX repo-relative; el overlay lee solo objetos Git; `--base` validado con `git rev-parse --verify` y rechazo de `-`.
- **Working tree**: nunca se usa como estado proyectado; no contamina.
- **Evidencia**: esquema sin estados factuales; el host no importa TE; `TF`/`TCOR`/`TV` no son LC-1.
- **Autoridad**: TE no escribe el Plan; `applied=false`; `accepted_by` resoluble; `status` derivado.
- **Bypass**: no hay comando de escritura, aplicación o release.

## 18. Implementation sequence

| Fase | Contenido | Gate |
|---|---|---|
| **S0** | Plan 175 + INDEX + Gate A conceptual (redacción) | Sin findings materiales |
| **A** | Autorización humana de ejecución (`Aprobado para ejecución`) | Entry criteria cumplidos |
| **S1** | `overlay.py` + `identity.py` + tests | Unit verde |
| **S2** | `proposal.py` + tests | Enumeración estable |
| **S3** | `checks.py` CH-1…CH-8 + tests (uno por vez) | Cada check con positivo/negativo |
| **S4** | `result.py` + tests | `--validate` deriva status |
| **S5** | `__main__.py` + tests | CLI/exit codes |
| **S6** | `__init__.py` + isolation + policy/docs | No writes/no import |
| **S7** | **Gate B**: TE run del Plan 175 + registro Working | `CONVERGED` o findings dispositionados |
| **S8** | Batería, C-1/C-2/C-3, anchor, checkpoint, `Executed`/`Closed` | Cierre |

## 19. TE self-evaluation

Aplicación conceptual de las cinco dimensiones al Plan 175. Es una **atestación del productor** (el autor del Plan), no una ejecución del engine.

| ID | Dimensión | Finding | Corrección aplicada |
|---|---|---|---|
| FT-01 | completeness | Faltaba `tests/AGENTS.md` (test anclado) | Añadido a `## Entregables` y §14 |
| FT-02 | completeness | Faltaban `runtime/README.md` y el puntero `.agents/AGENTS.md` | Añadidos |
| FT-03 | consistency | `--out` contradecía «TE no escribe» | Eliminado; solo stdout |
| FT-04 | consistency | `status` autoral permitía autoproclamar `CONVERGED` | Derivado por `result.py` |
| FT-05 | adversarial | «TE automático» atribuía al engine dimensiones semánticas | Gate B = productor + engine; test con fixture etiquetada |
| FT-06 | adversarial | CH-3 con target `Superseded` generaba falsos `ANOMALY` | `BOUNDARY` + obligación |
| FT-07 | adversarial | `falsified_if` confundía falsificación con pérdida de aplicabilidad | `depends_on` + `invalidated_by` |
| FT-08 | authority | `accepted_by` como texto libre | Referencia commiteada resoluble |
| FT-09 | verification | CH-5/CH-6 eran juicio sin mecanismo | Reglas declarativas + obligaciones |
| FT-10 | verification | Faltaba test de dirección de importación/no store | `test_theoretical_isolation.py` |
| FT-11 | completeness | Faltaba matriz de fallos/recovery | §16 |
| FT-12 | consistency | El scope no incluía el Plan ni el registro del Gate B | `## Delegación agentiva` (Plan editable) y `## Entregables` (registro del Gate B); §15 |
| FT-13 | consistency | Precedencia de status contradictoria | §7.1, una sola regla + 15 ejemplos |
| FT-14 | adversarial | `--compare` afirmaba `resolved`/`reopened` | §12.1, solo diferencias observadas |

```text
NEW_PROBLEMS = 0
OPEN_FINDINGS = 0
REQUIRES_HUMAN = 0
GAP = 0
TE_SELF_EVALUATION = CONVERGED (conceptual, producer-attested)
```

Límite declarado: la autoevaluación la produce el mismo autor; no es independiente ni evidencia de eficacia. Gate B la repite con el engine real.

## 20. Open questions

```text
BLOCKING = NONE
```

| ID | Cuestión | Clasificación | Estado |
|---|---|---|---|
| OQ-01 | Formato exacto de `te_id` (slug del producer, precisión de timestamp) | `NON_BLOCKING` | Se fija en implementación; no afecta staleness |
| OQ-02 | Orden de campos del JSON canónico | `NON_BLOCKING` | `sort_keys=True` |
| OQ-03 | Exit code de `--compare` con divergencia | `NON_BLOCKING` | Propuesta: 1; test lo fija |
| OQ-04 | ¿`authority` productor usa `probed` o solo `escalation_refs`? | `NON_BLOCKING` | Propuesta: ambos; test lo fija |
| OQ-05 | Nombre exacto del registro Working del Gate B | `NON_BLOCKING` | `THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md` |

No hay decisión arquitectónica abierta.

## 21. Readiness

El Plan es autocontenido: §2–§21 fijan arquitectura, contratos, checks, estados, CLI, tests y límites; la conversación de diseño no es una fuente requerida para implementar.

| # | Criterio | Estado |
|---|---|---|
| 1 | Gate B distingue producer semantics de engine mechanics | ✅ §5.2 |
| 2 | El engine no reclama dimensiones semánticas | ✅ §5.2, §13 |
| 3 | Precedencia única e inequívoca | ✅ §7.1 |
| 4 | `--compare` no confunde divergencia con resolución | ✅ §12.1 |
| 5 | Sin findings materiales abiertos | ✅ §19 |
| 6 | Áreas no evaluables con obligaciones | ✅ §9, §11 |
| 7 | Predicciones no verificadas por TE | ✅ §7 |
| 8 | Correcciones `applied=false` | ✅ §3 |
| 9 | Sin persistencia propia | ✅ §1 |
| 10 | Sin lifecycle/tracker/Change paralelo | ✅ §1 |
| 11 | Sin provider/model/network | ✅ §1, §17 |
| 12 | DEV scope intacto | ✅ §1 |
| 13 | Protocol fuera del cambio | ✅ §1 |
| 14 | Verificaciones ejecutables | ✅ §Verificación |
| 15 | Sin conocimiento implícito de la conversación | ✅ este documento |

```text
IMPLEMENTATION_PLAN_STATUS = READY_FOR_TE_EXECUTION
```
