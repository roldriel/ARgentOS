# Plan 179 — Minimal Adversarial Review: diseño, prototipo y experimento de validación

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-25
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2
**Depende de:** —
**Origen:** solicitud directa del mantenedor (2026-10-25; insumo local no versionado, no citable como `ruta:sección`); evidencia: campaña T1–T3, RFC-77 y planes 114/116/117/120, auditoría de integración del Plan 178, y la decisión de campaña `REFORMULATE`
**Superseded por:** —

## Objetivo

Diseñar, prototipar y validar experimentalmente en DEV la capacidad **Minimal Adversarial Review (MAR)** —selectiva, advisory, presupuestada y no normativa— que conserva una fracción material del valor observado en la campaña T1–T3 reduciendo el coste del mecanismo completo (4,01×–5,21×) hacia el objetivo experimental ≤2,0×. El valor que se busca conservar es el descubrimiento material nuevo que la campaña atribuyó a la falsificación dirigida, con el caso favorable como operación condicional a una reversión decisional advisory; la reducción de coste no es un fin en sí misma y no se acepta si destruye ese valor.

El plan debe (i) comparar el protocolo anterior y determinar qué operaciones produjeron el valor; (ii) definir el mecanismo mínimo y su trigger; (iii) materializar un prototipo aislado; (iv) ejecutar un experimento de validación preregistrado comparando baseline, mecanismo completo y MAR sobre un caso real; y (v) decidir `ADOPT_DEV_EXPERIMENT` | `REFINE` | `REJECT` | `DEFER` aplicando una regla congelada antes de ver resultados.

El plan **no** busca convertir MAR en Protocol feature, normative mechanism, governance rule, execution gate, authority, estado obligatorio, reemplazo de Jury, Court, voting ni infraestructura multi-juror, ni modificar `protocol/.agents/`, `.agents/`, RFCs, ADRs, `VERSIONING` o release policy. MAR es una capacidad experimental DEV que produce evidencia advisory; la autoridad existente decide y ningún resultado de este Plan promueve el Protocol.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Mantener la reducción de la hipótesis de deliberación adversarial a un mecanismo mínimo, por decisión de campaña `REFORMULATE` | humano | campaña T1–T3 (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:8. Decisión de la campaña`); solicitud directa del mantenedor (insumo local no versionado) |
| `P-2` Confianza | HIGH en la decisión de experimentar; LOW/NONE en cualquier afirmación arquitectónica o de promoción | agente | solicitud directa; `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:12. Estado, límites y no-conclusiones` |
| `P-3` Contexto | DEV layer; prior art payload (RFC-77, planes 114/116/117/120) leído como datos; convención Working; campaña 2026-10-25; auditoría de integración (Plan 178) | agente | `docs/rfc/77-protocol-native-adversarial-deliberation.md`; `docs/plans/114-adversarial-deliberation-mvp.md`; `docs/plans/116-adversarial-deliberation-mvp-closure.md`; `docs/plans/117-adversarial-deliberation-feature-adoption.md`; `docs/plans/120-adversarial-deliberation-materialization.md`; `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:4. Matriz principal`; `docs/AGENTS.md:Folder → class map` |
| `P-4` Derivabilidad | APPLIES: reconstruir evidencia → operaciones con valor → mecanismo mínimo → preregistro → experimento → evaluación → decisión (no al revés) | agente | `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:2.2 Atribución por operación`; `:9. PREREGISTRO CONGELADO` |
| `P-5` `work_type` | No se declara: el valor no cambia una decisión de gobernanza; se deriva en el cierre si corresponde (nunca se inventa) | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K`; `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada` |
| `P-6` Conocimiento vigente | DEV instructions gobiernan DEV; `protocol/.agents/` es payload y no se toca | documento | `.agents/AGENTS.md:Hard boundary: DEV vs Protocol`; `docs/AGENTS.md:Folder → class map`; `protocol/_AGENTS.md` |
| `P-7` Reglas aplicables | APPLIES: change lifecycle, authority, placement, evidence, findings y validación/anchor | agente | `.agents/workflows/change-lifecycle.md:2. Authorization gate`; `.agents/policies/authority.md:Document discovery`; `docs/placement-contract.md:DEV families`; `.agents/policies/validation-closure.md:1. Registered validation and anchors`; `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones`; `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions` |
| `P-8` Autoridad y scope | Scope: `docs/working/research/` (diseño, FRAME congelado, informe de validación y INDEX), `runtime/adversarial_review/`, `tests/` (sólo 2 suites nuevas), este Plan, `docs/plans/INDEX.md`, `CHANGELOG.md` y el staging no versionado `sessions/` (FRAME operativo, ledger, artefactos crudos; PC-44/PC-45). NO: `protocol/`, `.agents/`, RFCs, ADRs, `VERSIONING`, `ROADMAP.md`, `_TEMPLATE.md`, `tools/`, batería canónica, `runtime/orchestrator/`, `runtime/theoretical/`, `runtime/placement/`, `runtime/toolcalls/`, tests existentes, `dist`, tags, `master` | humano | solicitud directa del mantenedor (2026-10-25); este Plan |
| `P-9` Autorización | La instrucción directa del mantenedor del 2026-10-25 autoriza el Change y su alcance; el Change Level L2 exige Plan autorizado (RFC-75 Mecanismo 2; `.agents/workflows/change-lifecycle.md:2. Authorization gate`), por lo que este Plan es el artefacto de autorización y su Status es `Aprobado para ejecución` con entrada satisfecha | humano | `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`; `.agents/workflows/change-lifecycle.md:2. Authorization gate` |
| `P-10` Límites | `n=1`; mismo modelo/proveedor; sin independencia epistémica; coste en agent-seconds sin tokens; sin punto de integración limpio; ningún resultado promueve el Protocol | agente | `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:12. Estado, límites y no-conclusiones`; `:9.9 Desviaciones declaradas de antemano` |

## Criterio de entrada

- [x] Rama `dev` y HEAD `ac7f68074edbb9d67a1f231fac99c9e543a301aa` identificados.
- [x] Al intake, working tree sólo con los dos untracked preexistentes del mantenedor; los artefactos propios de este Change (diseño, prototipo y suites) se agregan después y se commitean en el paso 7.
- [x] Decisión de campaña `REFORMULATE` documentada (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:8. Decisión de la campaña`).
- [x] Ausencia de punto de integración limpio documentada (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:6.1 No hay punto de integración limpio hoy`).
- [x] Placement del prototipo resuelto por `docs/placement-contract.md:DEV families` (family Reference runtime → `runtime/<package>/`; tests en `tests/`).
- [x] Autorización directa registrada (mantenedor, 2026-10-25; campo `**Origen:**` de este Plan).
- [x] Alcance DEV-only verificado: `RFC-56 Class: N/A`, sin payload delta.

## Entregables

1. **E-1** — este Plan (`docs/plans/179-minimal-adversarial-review.md`) y su registro en `docs/plans/INDEX.md`.
2. **E-2** — diseño + preregistro congelado en `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md` y FRAME del caso congelado y Git-verificable en `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`; congelados antes de ejecutar cualquier pasada; cualquier cambio posterior se registra como desviación con su efecto sobre la validez (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9. PREREGISTRO CONGELADO`).
3. **E-3** — prototipo `runtime/adversarial_review/` con model, selectivity, budget, record, metrics y CLI; read-only, stdlib y advisory-only, sin consumidor (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:6.3 Prototipo`).
4. **E-4** — suites aisladas `tests/test_adversarial_review.py` y `tests/test_adversarial_review_isolation.py`.
5. **E-5** — experimento de validación preregistrado (baseline congelado → mecanismo completo → MAR → evaluación independiente → auditoría de integridad) y su informe `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_VALIDATION_2026-10-25.md`.
6. **E-6** — actualización de índices (`docs/working/research/INDEX.md`, `docs/plans/INDEX.md`) y `CHANGELOG.md` `[Unreleased]`.
7. **E-7** — decisión experimental y respuesta a las 10 preguntas de la iniciativa, con la regla de decisión congelada (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.7 Regla de decisión congelada`).

Quedan explícitamente fuera del alcance de este Plan: `protocol/`, `.agents/`, RFCs, ADRs, `VERSIONING`, `ROADMAP.md`, `docs/plans/_TEMPLATE.md`, `tools/`, la batería canónica, `runtime/orchestrator/`, `runtime/theoretical/`, `runtime/placement/`, `runtime/toolcalls/`, los tests existentes, `dist`, tags y `master`; y ningún entregable crea autoridad, estado, gate, contrato del Protocol ni release.

## Pasos

1. Intake y clasificación registrada en este Plan: `RFC-56 Class: N/A` (sin payload delta), Change Level L2, alcance DEV-only; fijar rama, HEAD y árbol.
2. Reconstruir desde los artefactos T1–T3 qué operaciones produjeron el valor material y cuáles fueron redundantes —evidencia, no re-ejecución— (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:4.3 Coste`; `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:2.2 Atribución por operación`).
3. Inspeccionar la implementación y documentación existentes (RFC-77, planes 114/116/117/120, `protocol/.agents/contracts/DELIBERATION_REPORT.md`, skill `adversarial-deliberation`, decisión `D7`, autoridad, evidencia/provenance, Theoretical Execution y superficies de integración) y declarar si existe un punto de integración limpio (`docs/rfc/77-protocol-native-adversarial-deliberation.md:Non-Goals / DEFERRED`; `.agents/policies/theoretical-execution.md:13. Boundaries`; `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:6.1 No hay punto de integración limpio hoy`).
4. Escribir el diseño y el preregistro congelado —mecanismo mínimo, alternativas descartadas, trigger, presupuesto, autoridad, provenance, disagreement, integration surface, Theoretical Execution y criterios de promoción— antes de ejecutar (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:4. Mecanismo mínimo propuesto`; `:5. Alternativas descartadas`; `:9. PREREGISTRO CONGELADO`).
5. Revisión independiente del diseño, del preregistro y de la FRAME antes de ejecutar; registrar la disposición de cada finding en el registro de corrección pre-freeze del diseño (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:14. Registro de corrección pre-freeze`), no en staging.
6. Materializar el prototipo y sus suites; verde dirigido.
7. Commit 1 atómico: Plan + diseño/preregistro + FRAME congelado + prototipo + tests, cuya evidencia de orden es que el preregistro y la FRAME preceden a la ejecución (el preregistro queda Git-verificable; el ledger y los artefactos crudos son staging atestiguado, §9.10).
8. Registrar en el ledger el SHA de Commit 1, el sha256 del FRAME congelado (HEAD de evidencia `ac7f680`, ya congelado) y el HEAD de ejecución; verificar las anclas del FRAME contra `ac7f680`; ejecutar y **congelar** BASELINE (hash en el ledger) antes de iniciar el tratamiento (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.1 Caso y FRAME`; `:9.10 Ledger`).
9. Ejecutar el comparador FULL (DEFENSE + PROSECUTION con commit-before-reveal, SYNTHESIS; REBUTTAL solo si la síntesis identifica un desacuerdo material) y MAR (PASS 1 + PASS 2 + síntesis corta) con ejecutores frescos y aislados, declarando la recepción de material (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.2 Condiciones del experimento`; `:9.3 Orden, aislamiento y validez`).
10. Evaluación independiente (taxonomía congelada, dedupe, impacto, mapa de retención FULL→MIN) y auditoría de integridad (orden, hashes, no contaminación, desviaciones D1/D2/D3) (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.5 Taxonomía y materialidad`; `:9.6 Retención`).
11. Escribir el informe de validación; aplicar la regla de decisión congelada; declarar retención, coste, impacto, trigger y límites (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.7 Regla de decisión congelada`).
12. Batería canónica + gates C-1/C-2/C-3; registrar Validation Anchor (`docs/VERSIONING.md:4.1 Batería canónica de verificación`; `.agents/policies/lifecycle-checkers.md:C-1 — Lifecycle anchor check`).
13. Governance de cierre: índices, `CHANGELOG.md`, condiciones derivadas y Checkpoint; `Status` → `Executed` (`.agents/policies/validation-closure.md:5. Checkpoint`; `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git`).
14. Commit 2 (atómico restante) y entrega del informe ejecutivo final al mantenedor.

## Delegación agentiva

El Change se ejecuta con un equipo agentivo coordinado por el Lead del Change, que conserva la autoridad de ejecución: ninguna delegación transfiere autoridad, ningún miembro puede aprobar el Change, declarar `Closed`, ampliar el scope ni modificar governance, y el resultado de cada miembro es advisory respecto de este Plan aprobado.

- **Task:** materializar E-2…E-7 —evidencia y comparación de la campaña T1–T3, diseño/preregistro congelado, prototipo y suites, experimento de validación, evaluación independiente, auditoría de integridad y governance de cierre— dentro del scope declarado en `P-8`.
- **Scope (editable; no es el conjunto medido):** `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md`, `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_VALIDATION_2026-10-25.md`, `docs/working/research/INDEX.md`, `runtime/adversarial_review/`, `tests/test_adversarial_review.py`, `tests/test_adversarial_review_isolation.py`, `docs/plans/179-minimal-adversarial-review.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`.
- **Equipo y scopes de escritura disjuntos:** Lead (ledger, revisión del diff final, ejecución de la batería y commits); tres analistas read-only (evidencia T1–T3, integración existente, selección de caso — sin escritura); `prereg-reviewer` (revisión independiente pre-ejecución, read-only; su disposición se registra en `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:14. Registro de corrección pre-freeze`); `prototype-dev` (sólo `runtime/adversarial_review/` y las dos suites nuevas); `plan-writer` (sólo este Plan y `docs/plans/INDEX.md`); ejecutores frescos y aislados (baseline, FULL y MAR; reciben únicamente la FRAME congelada y su postura, no resultados de otras condiciones); evaluador y adjudicador independientes (clasificación, dedupe, impacto y mapa de retención FULL→MIN; reciben los hallazgos, no las conclusiones del Lead); auditor de integridad (hashes, orden, no contaminación y desviaciones).
- **Aislamiento y orden:** el baseline se congela antes de iniciar el tratamiento; cada pasada compromete su hash antes de la revelación; la evaluación, la adjudicación y la auditoría se ejecutan después de que todas las condiciones estén congeladas y no modifican sus artefactos.
- **Staging no versionado:** durante la ejecución se escriben artefactos en `sessions/minimal-adversarial-review/` (copia operativa de la FRAME, ledger append-only encadenado por hash, artefactos crudos de las pasadas, revisión pre-ejecución). Es scratch (PC-44/PC-45): no se commitea, no se cita como provenance y su contenido se resume en el informe de validación versionado.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change sólo escribe documentación Working/DEV, código runtime read-only, dos suites nuevas y registros de gobernanza; no produce `network`, `remote_git`, `install`, `destructive` ni `write_outside_project` | instrucción directa del mantenedor (2026-10-25); este Plan | authorized |

Detalle declarado. **Escrituras versionadas:** `docs/working/research/` (diseño, FRAME congelado, informe de validación y su INDEX), `runtime/adversarial_review/`, dos suites nuevas (`tests/test_adversarial_review.py`, `tests/test_adversarial_review_isolation.py`), este Plan, `docs/plans/INDEX.md` y `CHANGELOG.md` `[Unreleased]`. **Escrituras de staging no versionadas:** `sessions/minimal-adversarial-review/` (copia operativa de la FRAME, ledger, artefactos crudos, revisión pre-ejecución) — scratch PC-44/PC-45, nunca commiteado ni citado como provenance. **Network:** no. **Install:** no. **Destructive:** no. **Escrituras fuera del repo:** no. **Estado oculto:** no. **Release/tag/push/`master`/`dist`:** no. Nada de lo escrito crea autoridad, estado, gate ni contrato del Protocol.

## Criterios de salida

- [ ] `D-1`: el diseño responde las 10 preguntas de la iniciativa y el preregistro está congelado antes de ejecutar cualquier pasada.
- [ ] `D-2`: el prototipo es read-only, stdlib y advisory-only, y sus dos suites pasan en verde.
- [ ] `D-3`: el experimento se ejecutó con BASELINE congelado antes del tratamiento, con hashes de orden y ledger append-only auditables (preregistro y FRAME Git-verificables en Commit 1; orden del ledger atestiguado con hashes).
- [ ] `D-4`: evaluación independiente y auditoría de integridad ejecutadas y registradas.
- [ ] `D-5`: la decisión se aplicó según la regla congelada, sin cambiarla después de ver resultados.
- [ ] `D-6`: el informe declara evidencia, límites y no-conclusiones con las etiquetas `OBSERVED`/`MEASURED`/`INFERRED`/`HYPOTHESIS`.
- [ ] `D-7`: ningún path prohibido fue modificado y no hay payload delta (RFC-56 N/A).
- [ ] `D-8`: índices y `CHANGELOG.md` actualizados; Validation Anchor y Checkpoint registrados; batería PASS y C-1/C-2/C-3 sin `ANOMALY`.
- [ ] `D-9`: Git en `dev` sin operaciones destructivas y la campaña T1–T3 intacta.
- [ ] `D-10`: informe ejecutivo final entregado al mantenedor con los campos exigidos.

## Verificación

Batería canónica definida una sola vez en `docs/VERSIONING.md:4.1 Batería canónica de verificación`; los gates C-1/C-2/C-3 son gates de lifecycle adicionales, fuera del bloque canónico (`.agents/policies/lifecycle-checkers.md:C-1 — Lifecycle anchor check`).

| Id | Comando | Resultado |
|---|---|---|
| verification-01 | `python tools/check_protocol_invariants.py --payload protocol .` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-02 | `python tools/check_plan_citations.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-03 | `python tools/check_plan_structure.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-04 | `python tools/check_taxonomy_coherence.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-05 | `python tools/check_session_artifacts.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-06 | `python tools/check_version_state.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-07 | `python tools/check_invariants_equivalence.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-08 | `python tools/check_enforcement_declarations.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-09 | `python -m pytest tests/` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-10 | `python -m pytest tests/test_adversarial_review.py tests/test_adversarial_review_isolation.py -q` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-11 | `python tools/check_lifecycle_anchor.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-12 | `python tools/check_lifecycle_checkpoint.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |
| verification-13 | `python tools/check_lifecycle_lineage.py` | PENDIENTE DE EJECUCIÓN (se completa en el paso 12) |

## Validation anchor

*Validación A1 — se registra al validar (VC-1; `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity`).*

- **Declared scope:** PENDIENTE — se completa en el paso 12.
- **Validation command-set:** PENDIENTE — se completa en el paso 12.
- **Effective inputs (repo content):** PENDIENTE — se completa en el paso 12.
- **Observed dependencies:** PENDIENTE — se completa en el paso 12.
- **Environmental factors:** PENDIENTE — se completa en el paso 12.
- **Scoped Content Identity:** PENDIENTE — se completa en el paso 12 (state identity y delta scoped identity).
- **Validity / stale:** PENDIENTE — se completa en el paso 12.

## Checkpoint / cierre

*Registro GC-1 — se completa al cerrar (`.agents/policies/validation-closure.md:5. Checkpoint`; `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git`).*

- **Commits de cierre:** PENDIENTE — se completa en el paso 13.
- **Estado validado (ref al Validation anchor):** PENDIENTE — se completa en el paso 13.
- **Estado de cierre (identidad):** PENDIENTE — se completa en el paso 13.
- **Árbol material del commit de cierre (tree id):** PENDIENTE — se completa en el paso 13.
- **Consistencia checkpoint↔anchor:** PENDIENTE — se completa en el paso 13.
- **Governance aplicada:** PENDIENTE — se completa en el paso 13.
- **Documentation impact:** PENDIENTE — se completa en el paso 13; determinación independiente (§5.1 de `.agents/policies/validation-closure.md:5.1 Documentation impact`), valor a registrar.
- **Roadmap impact:** PENDIENTE — se completa en el paso 13; determinación independiente (§5.2 de `.agents/policies/validation-closure.md:5.2 Roadmap impact`), valor a registrar.
- **Condición derivada:** PENDIENTE — se completa en el paso 13.

## Findings / Correcciones / Pending

### Findings

- Se completan durante la ejecución (pasos 9–13); no se crean findings de lineage para los hallazgos experimentales, que viven en el informe de validación.

### Correcciones

- Se completan durante la ejecución (pasos 9–13), con referencia de origen y alcance de revalidación (`.agents/policies/validation-closure.md:4. Findings / corrections / revalidation lineage`).

### Pending decisions

- `<PLAN-179>` — decisión: decisión experimental final del mantenedor sobre la continuidad de MAR; blocking: no para completar el experimento, sí para cualquier promoción; owner: mantenedor; escalación: mantenedor; resolución: pendiente, se registra en el paso 13; evidencia: informe de validación y `## Checkpoint / cierre`.

## Riesgos

- **Confundir coste bajo con valor retenido.** El coste reducido sólo cuenta si la retención material se mide; un mecanismo barato que dejó de mirar lo que producía el valor es un fracaso, no un éxito (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9.6 Retención`).
- **Contaminación por casos pre-analizados.** Un caso ya deliberado infla artificialmente la retención; el experimento usa un caso no deliberado y declara el techo de contaminación en el FRAME.
- **Medir atribución sin contrafáctico.** Toda atribución de impacto exige diferencia con el baseline, cita del ID y verificación de la cadena; sin contrafáctico se reporta como no atribuida.
- **Convertir el trigger en gate.** La selectivity es advisory por diseño: recomienda y explica, no invoca, no enruta, no bloquea ni elige profundidad automáticamente (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:4.10 Trigger / selectivity`).
- **Que el prototipo gane consumidores no autorizados.** `runtime/adversarial_review/` no se integra en el host, en TE, en la batería ni en la CLI de DEV; una suite de aislamiento lo verifica.
- **Introducir autoridad o estado por naming o por campos.** El registro es `ADVISORY_ONLY`, sin campos de autorización, voto o juez, y no escribe estados del lifecycle; el prototipo lo verifica mecánicamente.
- **Que el experimento pequeño no generalice.** `n=1`, mismo modelo/proveedor y sin independencia epistémica: ningún resultado autoriza promoción ni se extrapola a otros casos (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:12. Estado, límites y no-conclusiones`).
- **Que el prototipo se lea como capacidad del Protocol.** El informe y el Plan declaran que MAR es una capacidad experimental DEV, no un contrato, feature ni mecanismo del payload.

## Trazabilidad

`Priority 3.7` (insumo local, no versionado) → campaña T1–T3 → decisión `REFORMULATE` y recomendación de review mínima (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:8.3 Recomendación arquitectónica`) → Plan 179 → diseño/preregistro (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9. PREREGISTRO CONGELADO`) → prototipo `runtime/adversarial_review/` → experimento → informe de validación → decisión experimental → (si aplica) nuevo trabajo autorizado; el Protocol sólo cambia por RFC-56 (`docs/rfc/77-protocol-native-adversarial-deliberation.md:Non-Goals / DEFERRED`).

## Nota de ejecución

2026-10-25 — HEAD `ac7f68074edbb9d67a1f231fac99c9e543a301aa`; árbol con los dos untracked preexistentes del mantenedor preservados. PENDIENTE — se completa durante la ejecución (intake, commit 1, experimento, batería, cierre, commit 2).
