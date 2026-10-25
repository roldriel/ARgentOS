# Plan 176 — Theoretical Execution (DEV complete)

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-24
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 2 — multi-área DEV (`runtime/`, `tools/`, `tests/`, `.agents/`, `docs/`, `CHANGELOG.md`). *architectural impact*: 2 — cambia el contrato local de `TE_RESULT` (schema 2) y la semántica de dos checks; aditivo y reversible; no toca ningún contrato del payload. *release impact*: 0 — sin payload, sin `VERSION`, sin tag (RFC-69). *duration/complexity*: 2 — engine, checks, contrato, CLI, suites, dogfood y documentación.
**Depende de:** plan 175
**Origen:** instrucción directa del mantenedor (2026-10-24): «cerrar TODO Theoretical Execution en DEV» antes de cualquier trabajo de TE en `protocol/`. La instrucción nombra el alcance y autoriza su ejecución; la reconstrucción de alcance y la matriz de gaps están en `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`.
**Superseded por:** —

## Objetivo

Determinar el alcance completo de **Theoretical Execution (TE) en DEV**, contrastarlo
contra el estado real del repositorio y cerrar en la misma ejecución todo lo que falta:
implementar el delta `REQUIRED`, integrarlo con las piezas DEV existentes sin duplicar
responsabilidades, verificarlo, documentarlo y declarar `TE_DEV_STATUS = CLOSED`.

El Plan **no** implementa TE Protocol, no promueve capacidades al payload, no modifica
`protocol/` ni `protocol/.agents/`, y no crea un segundo lifecycle, orquestador, store
ni autoridad. TE sigue siendo una capacidad DEV invocable, no mutativa y no normativa.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Cerrar TE DEV como capacidad integral: reconstruir alcance, implementar el delta `REQUIRED`, verificar y documentar; sin tocar `protocol/` | humano | instrucción del mantenedor (2026-10-24); este Plan |
| `P-2` Confianza de intención | `HIGH` — el pedido nombra el objeto (TE DEV), el límite (no `protocol/`), el criterio de cierre (`TE_DEV_STATUS = CLOSED`) y el formato del reporte; la reconstrucción de alcance está registrada y citable | agente | `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`; este Plan `## Reconstrucción de alcance` |
| `P-3` Conjunto de contexto | `AGENTS.md`; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/{authority,validation-closure,theoretical-execution}.md`; plan 175 y su registro Working; `docs/rfc/75-change-lifecycle.md`; `docs/INVARIANTS.md`; `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md`; `docs/placement-contract.md`; `runtime/theoretical/*`; `runtime/orchestrator/observation.py`; `tools/{check_plan_citations,scoped_content_identity,check_lifecycle_checkpoint,check_session_artifacts}.py`; las ocho suites `tests/test_theoretical_*.py`; `docs/glossary/` | agente | lista de `ruta:sección` de este Plan y del registro de alcance |
| `P-4` Derivabilidad | `DERIVABLE` — la definición operativa de TE DEV COMPLETE es una `DECISION` del mantenedor registrada en este Plan; el delta se deriva de defectos observados en el árbol, no de una preferencia | agente | `## Reconstrucción de alcance`; `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type` |
| `P-6` Conocimiento vigente | `AGENTS.md` raíz, `.agents/` y `docs/` activos; RFC-75 `Accepted`; Plan 175 `Executed`/`Closed`; `docs/INVARIANTS.md` activo (RFC-84) | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (lifecycle, anchor, checkpoint), RFC-46 (no reescribir historia), RFC-56 (N/A), RFC-69 (sin release), RFC-84 / `INV-03` / `INV-05` / `INV-11`, VC-1, GC-1, LC-1, PC-1, `docs/VERSIONING.md:4.1 Batería canónica de verificación` | agente | `docs/VERSIONING.md`; `docs/CONVENTIONS.md` |
| `P-8` Autoridad y scope | Autoridad: mantenedor, por instrucción directa que nombra el alcance y autoriza la ejecución. Scope: deliverables = `## Entregables`; editable = `## Delegación agentiva` | humano | instrucción del mantenedor (2026-10-24); este Plan |

## Reconstrucción de alcance (resumen; detalle en el registro Working)

`FACT` — TE nació para atravesar una propuesta commiteada antes de materializarla, sin
ejecutarla y sin producir evidencia factual (`docs/plans/175-theoretical-execution-dev-v1.md:1. Scope and non-scope`).
`FACT` — el Plan 175 excluyó de **v1**: discovery/audit/post-execution, persistencia
propia, integración con el host y el lifecycle, `scenarios[]` y `ResultContentIdentity`.
`INFERENCE` — esas exclusiones fueron de scope del Plan, no prohibiciones permanentes;
las prohibiciones constitutivas (no ejecutar, no autorizar, no gobernar, no escribir el
payload, no crear un segundo lifecycle) sí son permanentes
(`.agents/policies/theoretical-execution.md:13. Boundaries`).
`DECISION` — TE DEV COMPLETE se define en el registro de alcance §3 y **no** incluye
simulación de operaciones por pasos, ejecución real, post-ejecución como insumo,
persistencia propia, gates ni orquestador embebido. El delta `REQUIRED` es
`D-1`…`D-7` (§`## Delta REQUIRED`).

## Criterio de entrada

- [x] Reconstrucción de alcance y matriz de gaps A–Q registradas con marca `FACT`/`INFERENCE`/`DECISION` y clasificación por gap.
- [x] Autorización humana de ejecución: instrucción directa del mantenedor (2026-10-24) que nombra el alcance; registrada aquí y en el registro de alcance.
- [x] Plan 175 `Executed`/`Closed` y base `f613147` verificada (`dev` = `master` = `f613147` al iniciar).
- [x] Sin cambios de payload: `RFC-56 Class: N/A`; `protocol/` y `protocol/.agents/` fuera del scope.
- [x] Este Plan commiteado en `dev` y registrado en `docs/plans/INDEX.md` (S0).

## Entregables

1. `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`
2. `docs/working/proposals/THEORETICAL_EXECUTION_DEV_COMPLETE_DOGFOOD.md`
3. `docs/working/proposals/INDEX.md`
4. `docs/plans/INDEX.md`
5. `runtime/theoretical/overlay.py`
6. `runtime/theoretical/identity.py`
7. `runtime/theoretical/proposal.py`
8. `runtime/theoretical/checks.py`
9. `runtime/theoretical/result.py`
10. `runtime/theoretical/__main__.py`
11. `runtime/theoretical/__init__.py`
12. `tools/scoped_content_identity.py`
13. `tests/test_theoretical_identity.py`
14. `tests/test_theoretical_proposal.py`
15. `tests/test_theoretical_checks.py`
16. `tests/test_theoretical_result.py`
17. `tests/test_theoretical_cli.py`
18. `tests/test_theoretical_isolation.py`
19. `tests/test_theoretical_dogfood.py`
20. `tests/test_theoretical_adversarial.py`
21. `tests/test_scoped_content_identity.py`
22. `tests/AGENTS.md`
23. `.agents/policies/theoretical-execution.md`
24. `runtime/README.md`
25. `docs/glossary/terms.md`
26. `docs/glossary/INDEX.md`
27. `CHANGELOG.md`

**Deliverable scope ≠ editable scope.** `## Entregables` enumera los artefactos cuyo
contenido mide el Validation Anchor. `## Delegación agentiva` enumera los paths
editables; incluye el propio Plan 176 como registro de gobernanza. Pertenecer al scope
editable no convierte un path en deliverable medido: este Plan queda excluido del scope
medido por anti-auto-referencia.

## Pasos

| Fase | Contenido | Gate |
|---|---|---|
| **S0** | Crear este Plan, el registro de alcance, la fila y serie del INDEX, la fila del Working INDEX; commit en `dev` | Plan commiteado y registrado |
| **S1** | `D-4`: `identity.py` (TOOL_VERSION 2, CHECK_SET CH-1…CH-9, nonce determinista) + tests | Identidad determinista |
| **S2** | `D-5`: `proposal.py` (entregables irresolubles/escape) + `checks.py` CH-9 + tests | CH-9 positivo/negativo |
| **S3** | `D-1`: `tools/scoped_content_identity.py` (`content_ref`) + `checks.py` CH-3/CH-7 contra la base + tests | Checks independientes de working tree e índice |
| **S4** | `D-2`/`D-3`: `result.py` (schema 2, `checks[]`, re-derivación, fingerprint verificado) + `__main__.py` (`computed_fingerprint`) + tests | Finding eliminado y fingerprint mentido rechazados |
| **S5** | `tests/test_theoretical_adversarial.py`, actualización de las suites restantes y del dogfood | Suites TE verdes |
| **S6** | `D-6`: policy, `runtime/README.md`, glosario, `tests/AGENTS.md`, `CHANGELOG.md` y corrección por referencia del INDEX del Plan 175 | Documentación consistente |
| **S7** | **Gate TE**: TE run real sobre este Plan (productor + engine) y registro Working | `CONVERGED` o findings dispositionados |
| **S8** | Batería canónica, C-1/C-2/C-3, revisión adversarial, Validation Anchor y Checkpoint | Cierre |

## Delegación agentiva

- **Task:** Implementar el delta `D-1`…`D-7` de TE DEV completo (determinismo de checks sobre la base, registro de checks y re-derivación en `--validate`, fingerprint de no-progress verificado, etiqueta de corrida determinista, CH-9 de integridad de declaración), actualizar policy/documentación/suites y ejecutar la verificación completa. El productor (agente/humano) realiza `completeness`, `consistency` y `adversarial`; el engine ejecuta CH-1…CH-9, las reglas mecánicas de `authority` y `verification`, y deriva el `status`. El engine no ejecuta dimensiones semánticas.
- **Scope (editable; no es el conjunto medido):** `docs/plans/176-theoretical-execution-dev-complete.md`, `docs/plans/INDEX.md`, `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`, `docs/working/proposals/THEORETICAL_EXECUTION_DEV_COMPLETE_DOGFOOD.md`, `docs/working/proposals/INDEX.md`, `runtime/theoretical/overlay.py`, `runtime/theoretical/identity.py`, `runtime/theoretical/proposal.py`, `runtime/theoretical/checks.py`, `runtime/theoretical/result.py`, `runtime/theoretical/__main__.py`, `runtime/theoretical/__init__.py`, `tools/scoped_content_identity.py`, `tests/test_theoretical_identity.py`, `tests/test_theoretical_proposal.py`, `tests/test_theoretical_checks.py`, `tests/test_theoretical_result.py`, `tests/test_theoretical_cli.py`, `tests/test_theoretical_isolation.py`, `tests/test_theoretical_dogfood.py`, `tests/test_theoretical_adversarial.py`, `tests/test_scoped_content_identity.py`, `tests/AGENTS.md`, `.agents/policies/theoretical-execution.md`, `runtime/README.md`, `docs/glossary/terms.md`, `docs/glossary/INDEX.md`, `CHANGELOG.md`.
- **Resource ceiling:** 30 ejecuciones delegadas.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change solo escribe documentación DEV, código runtime, tooling DEV y tests locales; no hay red, git remoto, instalación, operación destructiva ni escritura fuera del proyecto | instrucción del mantenedor (2026-10-24); este Plan | authorized |

## Criterios de salida

- [x] `D-1`: CH-3 y CH-7 son funciones del commit base; ni el working tree ni el índice staged alteran su señal.
- [x] `D-2`: `TE_RESULT` schema 2 registra `checks[]`; `--validate` recomputa los checks en la base y exige igualdad exacta, finding por check no válido y obligación por check con obligación.
- [x] `D-3`: `no_progress.fingerprint` se verifica contra el fingerprint computado (que incluye los checks y excluye el `status`), y se cruza con `previous_te_id`/`input.previous_te_id`; `--validate` publica `computed_fingerprint`.
- [x] `D-4`: `run_identity` produce la misma etiqueta para los mismos inputs, `created_at`, productor y plan.
- [x] `D-5`: un entregable declarado sin path resoluble o con path que escapa produce finding; una clase de efecto fuera del vocabulario cerrado produce `ANOMALY`.
- [x] `D-6`: policy, `runtime/README.md`, glosario, `tests/AGENTS.md`, `CHANGELOG.md` y el INDEX describen exactamente lo que existe; el Plan 175 no se edita y su fila del INDEX se corrige por referencia.
- [x] `D-7`: schema/tool/check-set versionados; un resultado v1 es `INCOMPARABLE`.
- [x] La suite completa pasa; el dogfood anclado sigue verde y el Gate TE de este Plan queda registrado.
- [x] Revisión adversarial ejecutada con los diez ataques y resultado registrado.
- [x] Sin cambios en `protocol/`, `dist/`, `VERSION`, `ExecutionHost`, `runtime/orchestrator/derivation.py` ni la batería canónica.

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
python -m pytest tests/test_theoretical_identity.py tests/test_theoretical_proposal.py tests/test_theoretical_checks.py tests/test_theoretical_result.py tests/test_theoretical_cli.py tests/test_theoretical_isolation.py tests/test_theoretical_dogfood.py tests/test_theoretical_adversarial.py tests/test_scoped_content_identity.py
python -m runtime.theoretical --plan 176 --base HEAD --emit
python -m runtime.theoretical --validate <result.json>
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --check
```

La salida de `--emit` se redirige a un archivo fuera del repositorio: la CLI no escribe
archivos. El `--validate` del resultado del Gate TE debe aceptar el `status` derivado y
salir 0.

## Delta REQUIRED

| Id | Cambio | Defecto observado (evidencia) | Verificación |
|---|---|---|---|
| `D-1` | CH-3 resuelve citas y estado de artefacto contra el commit base; CH-7 recomputa el delta con blobs del commit base | `runtime/theoretical/checks.py` (`_ch3`: `verify_citation(root)`, `_artifact_status(root)`; `_ch7`: `scoped_content_identity.compute(root)`) | Una edición no commiteada o staged no cambia la señal |
| `D-2` | `checks[]` en `TE_RESULT` + re-derivación en `--validate` | `runtime/theoretical/result.py` (función `validate_result`) no recomputa checks; un finding del engine puede borrarse | Finding eliminado, check faltante y obligación ausente rechazados |
| `D-3` | Fingerprint verificado e inclusivo de los checks (sin el `status`, que es la salida de la comparación); `computed_fingerprint` en el reporte | `_PROGRESS_KEYS`; `fingerprint()` ignora checks y `NO_PROGRESS` era inalcanzable (`F-2`) | Fingerprint mentido e `previous_te_id` incoherente rechazados |
| `D-4` | Nonce de `RunIdentity` derivado de contenido | `runtime/theoretical/identity.py` (función `run_identity`) usa `id(inputs)` | Misma etiqueta con mismos inputs y timestamp |
| `D-5` | CH-9 `declaration integrity` | `runtime/theoretical/proposal.py` (función `_deliverables`) descarta en silencio | Señales por entregable irresoluble, escape y clase de efecto desconocida |
| `D-6` | Documentación y glosario alineados; corrección por referencia del INDEX | INDEX del Plan 175 desactualizado; policy v1 | Checkers de gobernanza y revisión |
| `D-7` | Versiones de contrato, tool y check-set | Plan 175 §`8. Identity and provenance` | Resultado v1 `INCOMPARABLE` |

## Diseño del contrato (schema 2)

```text
TE_RESULT (schema_version "2")
  schema_version · te_id · status · reason
  provenance { kind:"theoretical", method, tool, tool_version, created_at, producer, authority_basis }
  input { factual, proposal{path,blob,status}, check_set, previous_te_id, revision }
  identity { factual, projected, inputs, run }
  model { paths, effects, scope, content:"unknown" }
  coverage { required_items, claims, checked, not_evaluable, not_applicable, dimensions{5} }
  checks[] { id, signal, statement, evidence_refs }        ← NUEVO: registro del engine
  claims[] · assumptions[] · findings[] · corrections[]
  verification_obligations[] · escalations[] · residual_risks[]
  limits { unevaluated_areas[], declared_limits[] }
  no_progress { fingerprint, previous_fingerprint, previous_te_id }
```

Reglas nuevas del validador:

1. `checks[]` es **del engine**: `--validate` recompone la propuesta en la base, ejecuta
   CH-1…CH-9 y exige igualdad exacta de la lista (id, signal, statement, evidence_refs).
   El productor no puede añadir, quitar, reordenar ni reescribir un check.
2. Todo check no `VALID`/`N/A` exige un finding con el mismo `signal`, el mismo
   `statement` y `location == id del check`. El productor decide la disposición
   (`OPEN`/`ESCALATED`/`RESIDUAL`), nunca la desaparición del hallazgo.
3. Todo check con obligación exige la obligación correspondiente enlazada al finding de
   ese check, con el mismo `statement`, `falsified_if` y `candidate`.
4. `no_progress.fingerprint`, si se declara, debe ser igual al fingerprint computado;
   `previous_fingerprint` y `previous_te_id` se declaran juntos y el segundo debe
   coincidir con `input.previous_te_id`.
5. `status` sigue derivándose de forma única; un resultado sin condición aplicable es
   inválido.

## Checks CH-1…CH-9

| Check | Versión | Cambio |
|---|---|---|
| CH-1…CH-2, CH-4…CH-6, CH-8 | 1 | sin cambio |
| CH-3 | 2 | resolución contra la base (archivo, sección, estado del artefacto, mapeo legacy) |
| CH-7 | 2 | delta del ancla recomputado con blobs del commit base |
| CH-9 | 1 | integridad de la declaración: entregable sin path resoluble (`GAP` + obligación), path que escapa del repositorio (`ANOMALY`), clase de efecto fuera del vocabulario cerrado (`ANOMALY`) |

## Revisión adversarial

| Ataque | Qué se intenta | Resultado |
|---|---|---|
| `SCOPE_ATTACK` | Que TE absorba discovery/audit/ejecución «porque el alcance completo lo pide» | `PASS` — frontera declarada; el registro de exclusiones prueba la clasificación |
| `BOUNDARY_ATTACK` | Que el delta introduzca host, payload, store o segundo lifecycle | `PASS` — imports y escritura verificados; sin nuevas dependencias |
| `STATE_ATTACK` | Que un estado parcial sobreviva o se reanude mal | `PASS` — una pasada, sin estado; la recuperación es re-ejecución |
| `AUTHORITY_ATTACK` | Que el productor derive `CONVERGED` sin cobertura, con `applied:true` o con `residual` sin `accepted_by` | `PASS` — rechazado por `--validate` |
| `EVIDENCE_ATTACK` | Que una simulación se presente como evidencia factual | `PASS` — sin estados factuales; `PREDICTION` no verificable; `provenance.kind` obligatorio |
| `IDENTITY_ATTACK` | Que dos corridas con el mismo `InputIdentity` difieran por el working tree o el índice | `PASS` — CH-3/CH-7 son funciones de la base |
| `TEMPORAL_ATTACK` | Que un resultado stale se trate como actual | `PASS` — `--stale` por HEAD; v1 `INCOMPARABLE` |
| `DEPENDENCY_ATTACK` | Que TE importe el host o que el host importe TE | `PASS` — dirección de importación testada |
| `NEGATIVE_PATH_ATTACK` | Inputs malformados, campos desconocidos, estados inválidos | `PASS` — rechazo determinista con exit code |
| `HISTORICAL_INTEGRITY_ATTACK` | Que el cierre reescriba el Plan 175 o el CHANGELOG histórico | `PASS` — Plan 175 intacto; corrección del INDEX por referencia |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-176>:F-1` — estado: `resolved` (corregido por `<PLAN-176>:C-1`); observación: la narración del Plan 175 en `docs/plans/INDEX.md` (párrafo de estado y sección del Plan) describía «cierre en curso (Validation Anchor/Checkpoint)» y «con Validation Anchor/Checkpoint pendientes» cuando `f613147` ya los había registrado y el Plan declaraba condición derivada `Closed`; evidencia original: `docs/plans/INDEX.md` en `f613147` frente a `docs/plans/175-theoretical-execution-dev-v1.md:Checkpoint / cierre`; provenance: reconstrucción de alcance (H-11 del registro Working); resolución: `C-1` corrige el espejo **por referencia**, sin editar el Plan cerrado.
- `<PLAN-176>:F-2` — estado: `resolved` (corregido por `<PLAN-176>:C-2`); observación: `NO_PROGRESS` era inalcanzable. El fingerprint incluía el `status` declarado y, a la vez, `NO_PROGRESS` se deriva de la igualdad de fingerprints: al declarar `NO_PROGRESS` el propio status cambiaba el valor comparado, y al declarar el status anterior la igualdad se cumplía pero el status derivado (`NO_PROGRESS`) no coincidía con el declarado. Las dos ramas producían un resultado inválido; el test heredado solo lo evitaba fijando el status final antes de calcular el fingerprint «anterior», algo que ninguna corrida previa real hace. Evidencia original: `runtime/theoretical/result.py` (`fingerprint` y `_no_progress`) en `f613147`; ejecución conceptual de dos corridas idénticas; `tests/test_theoretical_result.py` (caso 4 de la precedencia). Provenance: revisión adversarial de esta ejecución (`TEMPORAL_ATTACK`); resolución: `C-2` excluye el `status` del fingerprint (el status es la **salida** de la comparación, nunca su entrada) y mantiene ítems, checks y findings materiales.

### Correcciones

- `<PLAN-176>:C-1` — refs origen: `<PLAN-176>:F-1`; alcance de revalidación: el párrafo de estado y la sección del Plan 175 en `docs/plans/INDEX.md`; evidencia: `python tools/check_plan_structure.py` PASS y el Plan 175 sin diff (RFC-46: el artefacto cerrado no se reescribe).
- `<PLAN-176>:C-2` — refs origen: `<PLAN-176>:F-2`; alcance de revalidación: `runtime/theoretical/result.py` (fingerprint), `tests/test_theoretical_result.py`, `tests/test_theoretical_adversarial.py` y la policy; evidencia: `test_temporal_attack_no_progress_needs_a_declared_previous_run` PASS, `test_fingerprint_ignores_cosmetic_edits_and_status_but_tracks_material` PASS y `--validate` verifica el fingerprint declarado.

### Pending decisions

N/A.

## Riesgos

- **Falsa convergencia residual.** El productor puede mentir en las dimensiones semánticas. Mitigación: `computed` del engine, registro de checks, `probed` no vacío, obligaciones para `NOT_EVALUABLE`, `RESIDUAL` con `accepted_by`. Límite declarado, no eliminable.
- **Sobre-scope.** El delta se limita a `D-1`…`D-7`; cualquier capacidad nueva que aparezca durante la ejecución se registra como hallazgo y se clasifica, no se implementa por reflejo.
- **Deriva de checks.** El registro de checks exige versión: un cambio semántico sin bump produce resultados no comparables; el check-set versionado lo hace visible.
- **Costo de `--validate`.** Recomputar checks añade invocaciones Git locales; aceptable y medido por la suite.

## Trazabilidad

```text
instrucción del mantenedor (2026-10-24)
        ↓
reconstrucción de alcance + matriz de gaps (registro Working)
        ↓
este Plan (delta D-1…D-7)
        ↓
runtime/theoretical + tools + tests + docs
        ↓
Gate TE del Plan 176 (productor + engine)
        ↓
batería + revisión adversarial + ancla + checkpoint
        ↓
Closed (dev) · Released = NO (sin payload, RFC-69)
```

## Nota de ejecución

**Pendiente de ejecución.**
