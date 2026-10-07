# Plan 150 — Implementación de Memory System (RFC-80)

**Status:** Executed
**Fecha:** 2026-10-06
**RFC:** RFC-80 (`docs/rfc/80-memory-system.md`)
**Clase:** A (toca `protocol/.agents/`; ver RFC-56)
**Change Level:** L3 (`max(coordination, scope, architectural impact, release impact, duration/complexity)`; RFC-75 Mecanismo 2)
**Depende de:** RFC-80 `Accepted` (2026-10-06) — **satisfecho**; placement `ADAPT` de `.project/knowledge/` — **satisfecho** (decisión humana 2026-10-06)
**Origen:** RFC-80 `Accepted` (contrato arquitectónico cerrado) y el implementation discovery previo (mapeo a `runtime/`, `tools/`, `protocol/.agents/`)

> **Estado de autorización.** **AUTORIZADO PARA EJECUCIÓN** (decisión humana explícita,
> 2026-10-06). El `Status` pasa a `Aprobado para ejecución` con alcance acotado a
> `## Entregables`; `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/`. La
> autorización **no** constituye autorización de release, tag, promoción a `master` ni
> publicación, y **no** amplía el alcance aprobado.
> `Aprobado para ejecución ≠ Executed ≠ Committed ≠ Closed ≠ Released`.

---

## Objetivo

Transformar RFC-80 —sin reabrir su arquitectura— en una estrategia de implementación
incremental, verificable, reversible y gobernada para Memory System: las cinco capas
(Episodic, Semantic, Synthesis, Operational, Archive), la extracción/curation de
knowledge, la consolidation idempotente y verificada, el retrieval acotado y la
migración desde el modelo documental actual. Este plan **no** implementa nada: define
fases, dependencias, entregables, verificación, migración, rollback y observabilidad
para una futura ejecución. RFC-80 permanece como única autoridad arquitectónica.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Producir el Plan de Implementación de Memory System derivado normativamente de RFC-80, sin reabrir arquitectura ni ejecutar cambios | humano | instrucción del mantenedor (2026-10-06) |
| `P-2` Confianza de intención | `HIGH` — arquitectura cerrada, RFC-80 `Accepted`, discovery completo, criterios explícitos | agente | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` |
| `P-3` Conjunto de contexto | `AGENTS.md`; `docs/CONVENTIONS.md`; `docs/placement-contract.md`; `.agents/policies/authority.md`; `docs/rfc/80-memory-system.md`; `docs/rfc/56-governance-fast-track.md`; `docs/plans/_TEMPLATE.md`; `docs/plans/121-provider-bound-stable-prefix-readiness-mvp.md`; `docs/plans/INDEX.md`; `docs/rfc/INDEX.md` | agente | lista de rutas leídas |
| `P-4` Derivabilidad | Derivación completa; sin señal bloqueante (`GAP`/`ANOMALY`/`BOUNDARY`/`REQUIRES_HUMAN` salvo la autorización de ejecución declarada) | agente | `docs/rfc/80-memory-system.md` (invariantes I-001…I-030); `docs/placement-contract.md:6. Namespace selection` (PC-20) |
| `P-5` `work_type` | Documentación de planificación (`docs/plans/`); `work_type` derivado: plan de implementación (no ejecución) | agente | criterio de admisión: solo se materializa el plan + su registro |
| `P-6` Conocimiento vigente | RFC-80 `Accepted`; RFC-67/71/73 `Accepted`; ADR-10 `Accepted`; RFC-56 `Accepted` | documento | `docs/rfc/INDEX.md`; `docs/adr/INDEX.md` |
| `P-7` Reglas aplicables | RFC-56 `APPLIES` (Clase A); RFC-75 `APPLIES` (Change Lifecycle); VC-1 `APPLIES` (anchor al validar); HD-K3 `APPLIES` (esta tabla) | agente | `docs/CONVENTIONS.md:Convenciones`; `docs/rfc/75-change-lifecycle.md` |
| `P-8` Autoridad y scope | **Autorizado:** crear el plan y registrarlo en `docs/plans/INDEX.md`. **NO autorizado:** ejecución (requiere humano), `protocol/.agents/`, `runtime/`, `tools/`, `docs/placement-contract.md` | **humano** | declaración del mantenedor; `.agents/policies/authority.md:Stop conditions (authority)` |

## Criterio de entrada

- [x] **RFC-80 `Accepted`** en `docs/rfc/INDEX.md` y su header, con entrada en su `## Amendment Log`. **Satisfecho (2026-10-06).**
- [x] **Autorización humana explícita** de ejecución (el `Status` pasa a `Aprobado para ejecución`), con alcance acotado a `## Entregables`. **Satisfecho (2026-10-06).**
- [x] **Dependencia de placement resuelta**: `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/` (decisión humana 2026-10-06); se reutiliza la familia existente `Project-durable knowledge base`. **Satisfecho.**
- [x] Paso 0 verificado contra el repo: `git status` con los 4 archivos de gobernanza del Plan 150; sin diff en `runtime/`, `tools/`, `protocol/.agents/`.

## Entregables

Resumen de artefactos que produciría la ejecución (detalle por fase en `## Pasos`). Solo se
incluyen los realmente necesarios; ningún artefacto se crea en esta tarea.

| # | Path/family | Purpose | Owner | Depende de | Verificación |
|---|---|---|---|---|---|
| 1 | `protocol/.agents/…/memory/*.md` (contratos nuevos) | contratos de Session/Observation/Evidence/Claim/Synthesis/Operational/Archive | ejecutor | Phase 0 + 2–10 | checker de taxonomía + `check_protocol_invariants` |
| 2 | `runtime/…/memory/*.py` (módulos nuevos) | store, lifecycle, consolidator, verifier, retrieval, projection | ejecutor | Phase 1–9 | pytest |
| 3 | `.project/knowledge/` (ADAPT) o familia `memory` (nueva) | persistencia de memoria | ejecutor | Phase 0 | placement resolver |
| 4 | `tools/check_memory_*.py` | checkers de forma del memory store | ejecutor | Phase 2–8 | pytest + `testsupport` |
| 5 | `tests/…` | suites por invariante | ejecutor | Phase 2–12 | pytest |
| 6 | migration tooling | migración documental → Memory System | ejecutor | Phase 11 | tests de migración |
| 7 | docs/INDEX registros | registros de RFC/ADR/plan | ejecutor | cierre | `check_plan_structure` |

## Pasos

Las fases respetan las dependencias semánticas de RFC-80 (Episodic → Semantic →
Synthesis → Operational → Retrieval → Archive). No se ejecuta ninguna aquí: son la
secuencia autorizada para una futura ejecución.

### Phase 0 — Gobernanza y prerrequisitos

- **Dependencias:** RFC-80 `Accepted` (satisfecho).
- **Decisión de placement (RESUELTA):** `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/` (decisión humana 2026-10-06). Se reutiliza la familia existente `Project-durable knowledge base` de `docs/placement-contract.md` §6; **no** se crea una familia `memory` ni se inicia RFC-56/PC-20.
- **Decision owner:** el mantenedor (autoridad humana); decisión ya tomada (2026-10-06).
- **Registro de la decisión:** en este plan (header `Depende de` + `Criterio de entrada`) y en la trazabilidad de ejecución.
- **Gate de salida:** `PLACEMENT_DECISION = ADAPT` registrada; `Criterio de entrada` de placement marcado satisfecho. **SATISFECHO.**
- **Entradas/salidas:** `docs/placement-contract.md` §6, `docs/rfc/80-memory-system.md:35. Governance boundary`; salida = determinación de placement + autorización.
- **Entregables:** determinación registrada de la familia runtime (`ADAPT`); autorización humana de ejecución (`HUMAN_GRANTED`).
- **Verificación:** RFC-80 `Accepted` en INDEX; la determinación de placement resuelve por la regla existente (familia `Project-durable knowledge base`, sin invención).
- **Riesgos:** iniciar implementación sin resolver placement (rompe `PC-20`); mitigación = placement ya resuelto (`ADAPT`).
- **Criterio de finalización:** familia determinada (`ADAPT` `.project/knowledge/`); autorización de ejecución registrada (`Aprobado para ejecución`, `HUMAN_GRANTED`). **SATISFECHO.**

### Phase 1 — Primitivas de persistencia

- **Dependencias:** Phase 0.
- **Entradas/salidas:** reutiliza `runtime/orchestrator/store.py` (`_write_text`, fail-closed), `runtime/toolcalls/project_store.py` (`write` atómico, `rebuild`), `runtime/toolcalls/identity.py` (`segment_content_identity`, `SegmentIdentity`), `runtime/toolcalls/change_governance.py` (naming content-addressed).
- **Entregables:** store de memoria (IDs, escritura atómica, serialización canónica, lecturas fail-closed, rebuild).
- **Verificación:** tests de atomicidad, corrupción, rebuild determinista.
- **Riesgos:** duplicación de helpers de escritura atómica (precedente `runtime/orchestrator/store.py` vs `runtime/orchestrator/governance.py`); mitigación = reusar, no duplicar.
- **Criterio de finalización:** store roundtrip + rebuild + corrupción verde.

### Phase 2 — Episodic Memory

- **Dependencias:** Phase 1.
- **Entradas/salidas:** `.project/<session>/` (Session), `EVIDENCE.md` (Evidence), observation como entidad de primera clase.
- **Entregables:** contratos + persistencia de Session/Observation/Evidence; inmutabilidad de sesión cerrada; proveniencia resoluble.
- **Verificación:** I-001 (inmutabilidad), I-002/I-003 (proveniencia), I-027 (recuperabilidad).
- **Riesgos:** sesión hoy es `generated`/disposable (`docs/placement-contract.md:Project / session state`); la inmutabilidad histórica exige un namespace durable — depende de Phase 0.
- **Criterio de finalización:** sesión cerrada inmutable; observation/evidence con proveniencia.

### Phase 3 — Modelo semántico

- **Dependencias:** Phase 2.
- **Entradas/salidas:** `claim_class` y clases de evidencia existentes (`EVIDENCE.md`), `curation_status`/`status` actuales.
- **Entregables:** Claim (tipos: fact/constraint/requirement/invariant/decision/lesson/rejected_approach); lifecycle completo; estado epistémico; applicability; proveniencia.
- **Verificación:** I-004/I-005 (epistemic ≠ lifecycle, active ≠ verified), I-006 (applicability), I-023 (edad no invalida), I-024 (memoria vacía válida).
- **Riesgos:** colapsar lifecycle/epistemic/applicability en un solo campo (contradice RFC-80 §4/§5).
- **Criterio de finalización:** Claim con lifecycle/epistemic/applicability separados.

### Phase 4 — Extracción y lifecycle de candidatos

- **Dependencias:** Phase 3.
- **Entradas/salidas:** Closing Feedback (input de extracción), cierre de sesión.
- **Entregables:** session finalization → observations/evidence/candidate claims; cuarentena de candidatos; transiciones (discard/merge/validate/defer/promote/supersede/retire).
- **Verificación:** I-025 (candidato no operacional sin transición), observación → claim no automático.
- **Riesgos:** promover candidatos sin validación; mitigación = cuarentena explícita.
- **Criterio de finalización:** candidate lifecycle completo y testeado.

### Phase 5 — Relaciones, contradicción y supersession

- **Dependencias:** Phase 3.
- **Entradas/salidas:** `invalidated_facts` (precedente de invalidación).
- **Entregables:** vocabulario de relaciones (supports/contradicts/refines/confirms/supersedes/derived_from/causes/constrains/depends_on/duplicates); contradicción explícita; supersession explícita.
- **Verificación:** I-007 (contradicción explícita), I-009/I-010 (supersession explícita, ≠ falso). La exclusión operacional de contradicciones no resueltas (I-008) se verifica en Phase 9 (Retrieval).
- **Riesgos:** suavizar contradicciones; confundir `invalidated` con `superseded`.
- **Criterio de finalización:** contradicción y supersession explícitas y distinguidas.

### Phase 6 — Synthesis

- **Dependencias:** Phase 5.
- **Entradas/salidas:** manifest de discovery no versionado (a reemplazar), `project_segment.json` (proyección).
- **Entregables:** Synthesis versionada con lineage (`SYN-001 → superseded_by → …`); semantic diff; proveniencia.
- **Verificación:** I-021 (verificación previa a publicación), I-022 (no síntesis ante cambio no material).
- **Riesgos:** síntesis como source of truth o evidencia (contradice RFC-80 §19); mitigación = I-012.
- **Criterio de finalización:** síntesis versionada, no-SoT, con lineage.

### Phase 7 — Consolidation

- **Dependencias:** Phase 6.
- **Entradas/salidas:** algoritmo de RFC-80 §22; disparadores §21.
- **Entregables:** consolidator + verifier; scope/source_set/fingerprint/freeze; atomic publication; NO_OP; crash recovery.
- **Verificación:** I-015 (idempotencia), I-016/I-017/I-018 (proveniencia, sin generalizaciones, sin destruir negativo), I-019/I-020 (failure isolation), I-025/I-026 (candidato y no-mutación directa).
- **Riesgos:** publicación parcial; consolidación no-idempotente; crash.
- **Criterio de finalización:** consolidación idempotente, NO_OP, atómica, recuperable.

#### Semantic non-regression gate (I-017 / I-018 / I-021)

El consolidator publica una síntesis `S(n+1)` solo si el verifier declara `PASS` sobre el gate siguiente. El gate responde: *¿cómo demuestra el sistema que `S(n+1)` no pierde información semántica material respecto de las fuentes válidas que consolidó?*

- **Input set:** las fuentes/versiones congeladas que participan (scope + source_set + source_fingerprint de esta fase).
- **Material claims:** los claims materialmente relevantes de las fuentes (los que portan applicability, contradicción, supersession, relación causal, rejected approach, decisión, distinción epistémica o consecuencia material).
- **Semantic comparison (no textual):** comparar el conjunto de material claims de `S(n+1)` contra las fuentes, detectando pérdida o degradación de: claim identity/meaning, applicability, provenance, evidence, **epistemic distinctions**, lifecycle-relevant semantic state, contradiction, supersession, rejected approaches, causal relationships, **relevant consequences**, **decision rationale** (cuando sea material) y **generalización no soportada**.
- **Epistemic distinctions:** la comparación detecta degradación de estado epistémico (`verified`/`attested`/`inferred`, RFC-80 §4); una síntesis no puede convertir `inferred → verified` sin evidencia/autoridad que lo justifique, ni eliminar una distinción epistémica material porque el texto «parezca equivalente».
- **Relevant consequences:** una síntesis no puede eliminar consecuencias materialmente relevantes de decisions/lessons/constraints/rejected approaches/causal knowledge (p. ej. `Decisión X → consecuencia Y`); si conserva X pero pierde Y material para aplicar X correctamente, es semantic regression. No se crea una entidad `consequence`: es información semántica asociada al claim/decision/lesson existente (RFC-80 §25).
- **Decision rationale:** cubre `decision → alternatives → rationale → consequences` solo cuando sean materialmente relevantes para preservar la semántica de la decisión; no convierte cada detalle histórico en material claim.
- **PASS:** ningún material claim perdido; ninguna distinción epistémica material degradada; ninguna consecuencia material perdida; provenance/evidence preservadas; applicability preservada; contradictions/supersession preservadas; negative knowledge preservado; causal relationships materiales preservadas; rationale material preservado; ninguna generalización no soportada.
- **FAIL:** pérdida de un material claim sin declaración explícita de supersession/retire; pérdida o degradación de una distinción epistémica material; pérdida de una consecuencia material; pérdida de rationale material; o generalización no soportada.
- **NO_REGRESSION:** `S(n+1)` es no regresiva sii ningún material claim pierde representación operable sin una decisión de supersession/retire explícita y registrada (I-009); «material claim» incluye las dimensiones de RFC-80 §25 (applicability, provenance, epistemic distinctions, contradictions, negative knowledge, causal relationships, decision rationale, relevant consequences).
- **Rejection:** ante `FAIL` → no publicar; conservar `S(n)` activa; conservar las fuentes; registrar el rechazo (con provenance del verifier); permitir retry/revisión. El rechazo **no** se convierte automáticamente en supersession.

### Phase 8 — Operational Memory

- **Dependencias:** Phase 6–7.
- **Entradas/salidas:** `project_segment.json` (precedente de proyección rebuildable).
- **Entregables:** proyección materializada reconstruible desde semantic memory + syntheses + lifecycle + applicability + retrieval policy.
- **Verificación:** I-011/I-012 (rebuildable, no autoritativa), I-026 (ejecución no muta directamente).
- **Riesgos:** tratar la proyección como SoT.
- **Criterio de finalización:** proyección descartable y reconstruible.

### Phase 9 — Retrieval

- **Dependencias:** Phase 8.
- **Entradas/salidas:** `KB_RECOMMENDATION.md` (`kind`+`path`), `knowledge_entries` en `context.py`.
- **Entregables:** retrieval progresivo (scope → applicability → eligibility → relevance → authority/evidence → budget → context); fallback Operational→Synthesis→Semantic→Archive.
- **Verificación:** I-029 (budget acotado), I-014 (retrieval histórico no reactiva), I-008 (contradicción no resuelta excluida del conocimiento operacional incondicional).
- **Riesgos:** retrieval sin applicability; reactivación histórica.
- **Criterio de finalización:** retrieval acotado y no-reactivo.

### Phase 10 — Archive y frontera de retención

- **Dependencias:** Phase 3 (modelo semántico/lifecycle). Se programa en Phase 10, no antes, porque «fuera del retrieval operacional por defecto» (RFC-80 §28) solo es definible una vez que Retrieval (Phase 9) existe; el mecanismo de Archive puede definirse antes, pero su activación es posterior a Retrieval.
- **Entradas/salidas:** tag `kind` (histórico vs vigente).
- **Entregables:** mecanismo de Archive (fuera del retrieval por defecto); rehydration; retención separada de deletion.
- **Verificación:** I-013 (archive ≠ delete), I-027 (rehidratable), I-023 (edad no invalida).
- **Riesgos:** archive como borrado físico.
- **Criterio de finalización:** archive rehidratable, no destructivo.

### Phase 11 — Migración y compatibilidad

- **Dependencias:** Phase 2–10.
- **Entradas/salidas:** mapeo de RFC-80 §34/§35.
- **Entregables:** estrategia de migración (dual-read/dual-write temporal); transformación de discovery snapshots, `kind: knowledge`, `invalidated_facts`, `project_segment.json`; preservación de historical/legacy.
- **Verificación:** no pérdida de granularidad por claim, `invalidated` vs `superseded`, ni versionado de synthesis; proveniencia histórica preservada.
- **Riesgos:** migración ingenua (pérdida); mitigación = dual-read/dual-write + validación post-migración.
- **Criterio de finalización:** migración reversible sin pérdida semántica (stages M0–M2 del `## Modelo de transición`).

### Phase 12 — Métricas y observabilidad

- **Dependencias:** Phase 8–9.
- **Entradas/salidas:** `aggregate_metrics.py` (reuse por layer), `PROTOCOL_METRICS.md`.
- **Entregables:** métricas conceptuales de memory health, retrieval, utility, consolidation, knowledge debt (sin targets numéricos).
- **Clasificación de métricas:** `CORRECTNESS_REQUIRED` (verifican invariantes — p. ej. semantic preservation, contradiction rate, provenance resolvable), `OPERATIONAL_REQUIRED` (necesarias para operar — p. ej. retrieval cost/budget, operational projection health), `INFORMATIONAL` (salud/ROI — p. ej. rediscovery avoided, consolidation efficiency). Ninguna métrica `INFORMATIONAL` es blocker.
- **Verificación:** métricas medibles sin inventar thresholds.
- **Riesgos:** fijar thresholds prematuros; tratar una métrica informativa como blocker.
- **Criterio de finalización:** observabilidad operativa definida, con cada métrica clasificada.

### Phase 13 — Cutover y deprecación

- **Dependencias:** Phase 11–12.
- **Entradas/salidas:** caminos legacy (`knowledge/discovery`, `knowledge/entries`, `KB_RECOMMENDATION`, `invalidated_facts`).
- **Entregables:** coexistencia temporal, legacy reads, cutover, rollback, deprecación (sin eliminar caminos todavía).
- **Verificación:** compatibilidad legacy sin pérdida de conocimiento histórico.
- **Riesgos:** romper consumidores no documentados (`SESSION_SKIP`, `_LOCATION_RE`, tests hardcodeados).
- **Criterio de finalización:** cutover gobernado con rollback (stages M3–M5 del `## Modelo de transición`).

## Modelo de transición (migración → cutover)

La transición del modelo documental actual (`knowledge/discovery`, `knowledge/entries`,
`KB_RECOMMENDATION`, `invalidated_facts`) al Memory System se rige por la regla de
**una única fuente de verdad (SoT) por etapa** — nunca dos sistemas implícitamente authoritative.

### Stages y Source of Truth

| Stage | Legacy (`.project/knowledge/`) | Memory System | Source of Truth | Reads | Writes | Rollback |
|---|---|---|---|---|---|---|
| M0 — Legacy only | authoritative | ausente | Legacy | Legacy | Legacy | n/a |
| M1 — Build-out | authoritative | construido, no activo | Legacy | Legacy | Legacy | descartar Memory System |
| M2 — Dual-write | read-only (espejo) | activo, recibe espejo | Legacy | Legacy | Legacy → Memory System (espejo) | revertir a Legacy; descartar Memory System |
| M3 — Dual-read | read-only | activo, lectura comparada | Legacy | Memory System (primero) → Legacy (comparación) | Legacy | desactivar dual-read |
| M4 — Cutover | read-only | authoritative | Memory System | Memory System | Memory System | revertir a Legacy (switch reversible) |
| M5 — Legacy retired | histórico / archive | authoritative | Memory System | Memory System | Memory System | n/a |

### Dual-read

- **Comienzo:** al terminar Phase 9 (Retrieval) y validar la equivalencia de lectura en un scope de prueba (M3).
- **Fuente consultada primero:** Memory System; si responde, se compara contra Legacy; si no responde, Legacy es fallback.
- **Divergencia:** una lectura difiere **semánticamente** (no textualmente) entre ambos sistemas para el mismo query/scope/applicability.
- **Ante divergencia:** registrar (query, ambas respuestas, claim/provenance implicados) y **no** resolverla silenciosamente; el stage conserva a Legacy como SoT hasta clasificarla.
- **Registro:** log de divergencia con refs de provenance (no un segundo store).
- **Abandono del dual-read:** cero divergencias no resueltas durante la ventana de observación declarada (la ventana es parámetro de implementación).

### Dual-write

- **Activación:** al validar que el store de Memory System escribe y rebuilda correctamente (Phase 1/8), antes del dual-read (M2).
- **Orden lógico:** escritura a Legacy (SoT) primero; a continuación, espejo a Memory System.
- **Primera escritura OK, segunda falla:** Legacy conserva el estado; la escritura de Memory System queda marcada divergente y se reintenta (retry acotado) o se reconcilia.
- **Primera falla, segunda no ejecutada:** no se escribe en Memory System; Legacy informa el fallo como fallo real de escritura.
- **Inconsistencia:** detectada por dual-read o checksum de espejo; reconciliación = re-derivar desde Legacy (SoT), nunca desde Memory System.
- **Autoridad durante el stage:** Legacy. **Dual-write NO convierte ambos sistemas en SoT.**
- **Desactivación:** cuando Memory System es declarado SoT (M4) o se revierte a Legacy.

### Divergence / conflict handling

- **Detección:** dual-read + checksum de espejo.
- **Registro:** entry de divergencia (query/scope, respuesta Legacy, respuesta Memory System, claim/provenance).
- **Clasificación:** textual vs semántica; resoluble vs no resoluble; por defecto la divergencia se conserva como hecho (nunca se fuerza a una clasificación incorrecta).
- **Autoridad:** la define el stage (M0–M3: Legacy; M4+: Memory System).
- **Reconciliación:** re-derivar desde la SoT del stage; no inventar un ganador semántico que RFC-80 no defina.
- **Retry:** acotado y registrado (parámetro de implementación).
- **Rollback:** revertir al stage anterior (`## Matriz de rollback y recuperación`).
- **Condición de resolución:** la divergencia queda clasificada y reconciliada, o marcada como contradicción explícita (I-007/I-008) cuando RFC-80 lo permite.

### Cutover (gates objetivos)

El cutover (M3 → M4) solo se permite cuando **todos** los gates siguientes son verificables `PASS`:

- **Equivalencia funcional:** dual-read sin divergencias semánticas en la ventana declarada.
- **Integridad de datos:** conteo e identidad de claims/evidence/synthesis coincide por Scoped Content Identity (no por texto).
- **Provenance:** toda entidad migrada conserva provenance resoluble (I-002/I-003/I-016).
- **Semantic preservation:** el semantic non-regression gate (Phase 7) `PASS` sobre el corpus migrado.
- **Divergencia pendiente:** cero divergencias no resueltas.
- **Rollback readiness:** el switch reversible está operativo y probado (M4 → M3).
- **Observabilidad:** métricas de retrieval/migration activas (Phase 12).

### Legacy retirement

1. **Detener dual-write:** al confirmar M4 (Memory System SoT) y validar que el espejo no diverge.
2. **Detener dual-read:** al cumplir la ventana de observación sin divergencias.
3. **Legacy read-only:** al declarar M4 (los consumidores legacy dejan de escribir).
4. **Retirar consumidores legacy:** migrar los consumidores (`SESSION_SKIP`, `_LOCATION_RE`, checkers/tests) una vez que la SoT es Memory System.
5. **Retirar caminos de compatibilidad:** al validar que ningún consumidor vivo depende de Legacy (grep + tests).
6. **Cutover completado:** M5 — Legacy queda histórico/archive; **no** se elimina físicamente (I-013).

La eliminación física de Legacy es política de retención separada (`docs/rfc/80-memory-system.md:28. Archive`) y **no** forma parte de la primera ejecución.

## Criterios de salida

- [ ] Cada componente arquitectónico de RFC-80 tiene una fase o justificación explícita de exclusión.
- [ ] Cada fase tiene dependencias, entregables y criterios de finalización verificables.
- [ ] Los 30 invariantes tienen estrategia de verificación (matriz `## Verificación`).
- [ ] Estrategia de migración (Phase 11), rollback, failure recovery, compatibilidad legacy, testing y observabilidad (Phase 12) definidas.
- [ ] Placement/gobernanza dependencias explícitas (Phase 0).
- [ ] No se reabre RFC-80; parámetros de implementación separados de decisiones arquitectónicas.
- [ ] El plan no autoriza ejecución prematuramente; puede evolucionar sin modificar RFC-80 salvo decisión arquitectónica genuinamente nueva.

## Verificación

Comandos que deben correr en verde al validar (y al cerrar):

- `python tools/check_plan_structure.py --root .`
- `python tools/check_plan_citations.py`
- `python tools/check_protocol_invariants.py --payload protocol .`
- `python -m pytest tests/`

Matriz de invariantes (I-001…I-030) → superficie → verificación:

| Invariante | Superficie de implementación | Verificación | PASS esperado |
|---|---|---|---|
| I-001 closed sessions immutable | store Episodic (Phase 2) | test de inmutabilidad | reescritura de sesión cerrada rechazada |
| I-002 evidence provenance preserved | Evidence (Phase 2) | test de proveniencia | provenance resolvable tras migración/archive |
| I-003 active claims resolvable provenance | Claim (Phase 3) | test de frescura/proveniencia | claim sin provenance no es `active` |
| I-004 active claims retain epistemic state | Claim (Phase 3) | test de estado epistémico | transición lifecycle no borra epistemic |
| I-005 active ≠ verified | Claim (Phase 3) | test de semántica | `active` con `attested`/`inferred` válido |
| I-006 applicability not wildcard | Claim (Phase 3) | test de applicability | applicability desconocida ≠ universal |
| I-007 contradictions explicit | Relation (Phase 5) | test de relación | contradicción registrada explícitamente |
| I-008 unresolved contradiction not unconditional | Retrieval (Phase 9) | test de retrieval | contradicción no resuelta excluida del conocimiento operacional incondicional (relación registrada en Phase 5) |
| I-009 supersession explicit | Relation (Phase 5) | test de supersession | supersession registrada explícitamente |
| I-010 superseded ≠ false | Relation (Phase 5) | test de semántica | superseded sigue recuperable, no re-marcado falso |
| I-011 Operational rebuildable | Operational (Phase 8) | test de rebuild | proyección eliminada y reconstruida idéntica |
| I-012 Operational not authoritative | Operational (Phase 8) | test de autoridad | proyección derivada, no SoT |
| I-013 archive not deletion | Archive (Phase 10) | test de archive | archivar no borra; rehydration posible |
| I-014 historical retrieval no reactivate | Retrieval (Phase 9) | test de retrieval | retrieve histórico no cambia lifecycle |
| I-015 consolidation idempotent | Consolidation (Phase 7) | test de idempotencia | re-run produce sin duplicación |
| I-016 consolidation preserves provenance | Consolidation (Phase 7) | test de proveniencia | provenance intacta post-consolidación |
| I-017 no unsupported generalizations | Consolidation (Phase 7) | test de generalización | sin claim nuevo no respaldado |
| I-018 no destroy negative knowledge | Consolidation (Phase 7) | test de negativo | rejected approach preservado |
| I-019 failed consolidation preserves state | Consolidation (Phase 7) | test de failure | fallo deja estado previo |
| I-020 failed verification preserves state | Verification (Phase 7) | test de rechazo | síntesis rechazada no activa |
| I-021 synthesis must pass verification | Synthesis (Phase 6–7) | test de gate | síntesis sin verificar no publica |
| I-022 no synthesis for non-material change | Synthesis (Phase 6) | test de semantic diff | cambio solo-redacción → NO_OP |
| I-023 age alone not invalidate | Lifecycle (Phase 3) | test de TTL | TTL expirado ≠ inválido (stale ≠ invalid) |
| I-024 empty semantic memory valid | Semantic (Phase 3) | test de estado vacío | Claims=0 aceptado |
| I-025 candidate not automatically operational | Extraction (Phase 4) | test de cuarentena | candidato sin transición no operacional |
| I-026 execution cannot mutate operational | Authority (Phase 8) | test de autoridad | ejecución no escribe proyección directa |
| I-027 historical sessions recoverable | Episodic (Phase 2) | test de rehydration | sesión histórica rehidratable |
| I-028 user attestation ≠ verified | Attestation (Phase 4) | test de clasificación | assertion de usuario retiene `attested` |
| I-029 retrieval budget bounded | Retrieval (Phase 9) | test de budget | retrieval no excede budget |
| I-030 discovery distinct from semantic | Discovery (Phase 11) | test de distinción | snapshot no se vuelve claim automático |

## Validation anchor

- **Declared scope:** el cambio de Plan 150 (28 archivos: RFC-80, Plan 150, índices de planes/RFC, estándar de protocolo `MEMORY_SYSTEM.md`, `runtime/memory/` (14 módulos), `tools/check_memory_store.py` y 8 suites de tests) validado por la batería canónica completa sobre el estado committeado `d668775`.
- **Validation command-set:** `python tools/check_plan_structure.py --root .`; `python tools/check_plan_citations.py`; `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_taxonomy_coherence.py`; `python tools/check_memory_store.py --root .`; `python -m pytest tests/ -q`.
- **Effective inputs (repo content):** todo el repositorio (batería canónica sobre `docs/`, `protocol/.agents/`, `runtime/`, `tools/`, `tests/`).
- **Observed dependencies:** no instrumentado.
- **Environmental factors:** Python 3.11+ (stdlib), git CLI.
- Scoped Content Identity:
  - State identity (estado validado = árbol de `d668775`): `18ada8d80a42602a1a94245d5de4c1485f8df9d6` (tree id; igual a `git rev-parse d668775^{tree}`).
  - Delta scoped identity (scope S = 28 archivos del cambio, orden ordinal; serialización `scoped-v1` + pares `path NUL blob NUL`): `0f62e641a948b4b0ef690927da11e3dfa6c72f4b29d9eed6748297de4bbd91da`.
- **Validity / stale:** vigente (estado validado = `d668775`, working tree limpio).

## Checkpoint / cierre

- **Commits de cierre:**
  - C1 `d668775` — `feat(memory): implement Memory System reference runtime (plan 150, RFC-80)` (contenido de implementación validado por A1).
  - C2 — este commit de registro (`docs(plans): close Plan 150 (plan 150, RFC-80)`); su SHA se identifica por el mensaje y el árbol no embebe su propia identidad (auto-referencia).
- **Estado validado:** `## Validation anchor` de este plan (A1); State identity T1 = `18ada8d80a42602a1a94245d5de4c1485f8df9d6`; Delta scoped identity = `0f62e641a948b4b0ef690927da11e3dfa6c72f4b29d9eed6748297de4bbd91da`.
- **Estado de cierre:** `18ada8d80a42602a1a94245d5de4c1485f8df9d6` (identidad del estado de cierre = State identity del anchor A1; el árbol material del commit de cierre C2 —que añade los registros de governance— se verifica por mensaje tras el commit y difiere legítimamente del declarado).
- **Consistencia checkpoint↔anchor:** A1 ↔ C1: `git rev-parse d668775^{tree}` == T1 (`18ada8d8…`) → **PASS**; el estado final (C2) difiere de C1 únicamente en los registros de cierre (anchor/checkpoint de este plan + índice de planes).
- **Governance aplicada:** RFC-56 Clase A (RFC-80 `Accepted`); Plan 150 `Aprobado para ejecución` (autorización humana 2026-10-06); placement `ADAPT` `.project/knowledge/`.
- **Documentation impact (§5.1):** NOT_REQUIRED — el cambio añade artefactos nuevos (RFC-80, Plan 150, `MEMORY_SYSTEM.md`, `runtime/memory/`, checker, tests) y no modifica documentación de estado actual (`docs/VERSIONING.md`, `ROADMAP.md`, `README.md`, `AGENTS.md`, `.agents/`). La obligación de `CHANGELOG.md` + bump de `protocol/.agents/VERSION` (docs/VERSIONING.md §3/§5) corresponde al acto de release, fuera del alcance de este cierre.
- **Roadmap impact (§5.2):** NOT_REQUIRED — el cambio es la implementación de referencia DEV del Memory System; no completa, cancela ni reclasifica ítems del mapa operativo de trabajo futuro (`ROADMAP.md`, gobernado por Plan 149).
- **Condición derivada:** Closed (con release pendiente) — implementación committeada (`d668775`) y validada; el estándar de protocolo `MEMORY_SYSTEM.md` es un cambio de payload con release pendiente.

## Riesgos

- **Fallo de consolidation** — detección: excepción o invariante roto; safe state: estado previo intacto (I-019); rollback: descartar síntesis candidata; recovery: re-ejecutar con fingerprint.
- **Fallo de verificación** — safe state: síntesis activa sin cambios (I-020); rollback: rechazo/defer.
- **Fallo de proyección** — safe state: semantic + synthesis autoritativas (I-012); rollback: rebuild de la proyección.
- **Fallo de archive** — safe state: sin destrucción (I-013); rollback: rehydration.
- **Fallo de migración** — detección: validación post-migración; safe state: dual-read/dual-write; rollback: revertir cutover; riesgo de pérdida: granularidad por claim, `invalidated` vs `superseded`, versionado de synthesis.
- **Publicación parcial** — safe state: atómica o recuperable (RFC-80 §27); rollback: transacción/recovery.
- **Crash durante consolidation** — safe state: versiones fuente congeladas; recovery: re-ejecutar (idempotente).
- **Corrupción de Operational Memory** — safe state: reconstruible desde SoT (I-011).
- **Incompatibilidad legacy** — mitigación: Phase 11/13 (coexistencia + cutover gobernado).
- **Seguridad/aislamiento** — project scoping (sin leakage cross-project); anti-spoofing de proveniencia; attestation de usuario retiene clasificación; transiciones de lifecycle no autorizadas rechazadas; integridad de sesiones históricas; consolidación concurrente coordinada por scope.
- **Performance/límites** — retrieval acotado (budget), knowledge debt, retrieval cost, consolidation frequency, redundancy, semantic preservation: medir sin thresholds (parámetros de implementación).

## Matriz de rollback y recuperación

Principio: un fallo de una etapa posterior no destruye un estado válido anterior. Cada
transición crítica satisface un **contrato operacional** (el mecanismo concreto es parámetro
de implementación cuando RFC-80 lo delega).

| Transition | Before-state | Change | Failure | Detection | Recovery | Post-rollback state | Provenance preserved | Repeatable |
|---|---|---|---|---|---|---|---|---|
| consolidation | síntesis activa `S(n)` + fuentes congeladas | candidata `S(n+1)` | excepción / crash | journal de consolidación | descartar `S(n+1)`; `S(n)` sigue activa | `S(n)` activa | sí | sí (idempotente, I-015) |
| synthesis publication | `S(n)` activa | publicar `S(n+1)` | publicación parcial | verificación de atomicidad (I-021) | restaurar `S(n)`; descartar `S(n+1)` | `S(n)` activa | sí | sí |
| migration | Legacy (M0) | backfill a Memory System | backfill parcial | checksum de espejo | re-derivar desde Legacy (SoT) | M0 | sí | sí |
| dual-write | Legacy SoT (M2) | espejo a Memory System | espejo falla | marca de divergencia | retry / reconciliar desde Legacy | M2 | sí | sí |
| cutover | Legacy SoT (M3) | Memory System SoT (M4) | divergencia post-cutover | dual-read / métricas | revertir switch a M3 y reconciliar escrituras M4 (ver `## Matriz de rollback y recuperación` §Cutover / deprecation) | M3 (Legacy SoT; Memory System histórico/no-authoritative) | sí | sí |
| legacy deprecation | M4 | Legacy read-only | consumidor legacy falla | tests / grep | reactivar camino legacy | M4 | sí | sí |
| operational projection | proyección válida | corrupción / obsolescencia | proyección no confiable | checksum / invariante roto | descartar y rebuild desde SoT | proyección reconstruida | sí | sí (I-011) |

### Consolidation

- **Preservación de la versión anterior:** `S(n)` permanece activa e inmutable mientras `S(n+1)` es candidata (I-019).
- **Publicación de síntesis nueva:** solo tras el `PASS` del verifier (I-021); el mecanismo es atómico o recuperable (`docs/rfc/80-memory-system.md:27. Atomic publication`).
- **Detección de fallo:** el journal de consolidación registra el estado intermedio; un fallo deja `S(n+1)` no publicada.
- **Sin síntesis parcialmente publicada:** la publicación es un punto atómico; no existe estado observable intermedio.
- **Recovery tras crash:** re-ejecutar la consolidación sobre las fuentes congeladas (idempotente, I-015).
- **Repetición idempotente:** el `source_fingerprint` impide re-consolidar un estado idéntico (I-022 / `NO_OP`).

### Publication

- **Publicación atómica:** el estado visible antes es `S(n)`; el estado visible después es `S(n)` o `S(n+1)` completo — nunca un híbrido.
- **Ante interrupción:** el estado visible es `S(n)` (la versión anterior se conserva hasta que `S(n+1)` es verificada y publicada).
- **Conservación de la versión anterior:** `S(n)` no se destruye al publicar `S(n+1)` (queda en lineage, `superseded_by`).

### Migration / dual-write

- **Partial write:** detectada por checksum de espejo; se re-deriva desde Legacy (SoT).
- **Divergence:** registrada y clasificada (`## Modelo de transición` §Divergence).
- **Reconciliation / retry / rollback / preservation of provenance:** según la matriz; la provenance nunca se pierde (I-016).

### Cutover / deprecation

- **Switch reversible:** el cutover (M3 → M4) es un switch declarado y reversible a nivel de contrato, verificable como `old valid state → transition → failure → recovery → old valid state` sin pérdida de provenance ni modificación destructiva del histórico.

#### Contrato de rollback M4 → M3

Durante M4, Memory System es SoT y Legacy es read-only, por lo que pueden producirse escrituras nuevas solo en Memory System. El rollback (M4 → M3) devuelve `Legacy = SoT` y `Memory System = no authoritative`, **sin destruir** el conocimiento producido durante M4.

- **Identificación de escrituras M4:** el conjunto de escrituras producidas durante M4 se identifica por la provenance/version/session/write metadata ya existente en el modelo de RFC-80 (Session/Observation/Evidence/Claim con `source_sessions`/provenance), sin entidad nueva; una escritura M4 declara `stage = M4` en su provenance.
- **Estado de las escrituras M4:** se distingue **existencia histórica** de **autoridad operacional actual**. Una escritura M4 no desaparece por el cambio de SoT: pasa a estado histórico/no-authoritative, identificable como knowledge producido en M4.
- **Reconciliación (por categoría, derivada de RFC-80):**

| M4 write state | M3 treatment | Provenance |
|---|---|---|
| Already represented in Legacy | no-op (Legacy es SoT; la escritura es redundante) | preserved |
| Not represented in Legacy | retenida en Memory System como histórico/no-authoritative con `stage=M4`; **no** promovida a conocimiento operacional de M3 (I-025) | preserved |
| Divergent | retenida y marcada como divergencia/contradicción explícita (I-007); el valor de Legacy (SoT) prevalece; no se fuerza resolución | preserved |
| Contradictory | retenida como contradicción explícita (I-007/I-008); no operacional incondicional; no se fuerza resolución | preserved |
| Unresolved | retenida como no resuelta (I-008); no se fuerza resolución | preserved |

- **No pérdida de conocimiento:** el rollback no implica que el dato de Memory System desaparezca. Si una escritura M4 no puede promoverse a Legacy, se conserva históricamente y permanece identificable como knowledge producido durante M4; **no** se convierte automáticamente en conocimiento operacional de M3.
- **Nuevo M3:** tras el rollback, `Legacy = SoT` y `Memory System = estado histórico/no-authoritative`. No existe una situación donde `Legacy dice X` y `Memory System dice Y` con ambos tratados simultáneamente como authoritative.
- **Provenance:** se conserva origen, session/provenance, stage de producción (M4), relación con la escritura original y estado de reconciliación. No se altera históricamente una escritura M4 para fingir que fue producida en M3.
- **Repetibilidad:** el rollback/reconciliación es idempotente; un retry no duplica claims ni evidence, no pierde provenance y no genera decisiones semánticas accidentales.

### Operational projection

- **Detección de corrupción:** checksum/identidad de la proyección contra la SoT (I-011/I-012).
- **Determinación de no confiabilidad:** divergencia con la SoT o invariante roto.
- **Descarte:** la proyección es descartable por definición (no es SoT).
- **Reconstrucción:** rebuild desde semantic memory + syntheses + lifecycle + applicability + retrieval policy (`docs/rfc/80-memory-system.md:18. Operational Memory`).
- **Verificación / re-operacionalización:** rebuild determinista + checksum idéntico al estado esperado.

## Trazabilidad

`Origen (RFC-80 Accepted) → Plan 150 → fases → entregables → verificación (I-001…I-030)`.

- **Correcciones Red-Team (2026-10-06):** origen = Red-Team Review del Plan 150. MUST FIX aplicadas: modelo de transición (migración/cutover), matriz de rollback/recovery, semantic non-regression gate. SHOULD FIX aplicadas: I-008 reasignado a Phase 9 (relación registrada en Phase 5), placement owner definido en Phase 0. OPTIONAL aplicadas: clasificación de métricas (Phase 12), nota de scheduling de Archive (Phase 10). RFC-80 no modificado; implementación no iniciada.
- **Corrección Focused Re-Review #2 (2026-10-06):** origen = Focused Re-Review del Plan 150. Aplicadas: contrato de rollback M4 → M3 (identificación y destino de escrituras M4, reconciliación por categoría, preservación de provenance, no-dos-SoT, repetibilidad); semantic non-regression gate completado (epistemic distinctions, relevant consequences, decision rationale). RFC-80 no modificado; implementación no iniciada.
- **Ejecución autorizada (2026-10-06):** decisión humana explícita. `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/`; `Status` → `Aprobado para ejecución`; `EXECUTION_AUTHORIZATION = GRANTED`. Fases ejecutadas registradas en `## Nota de ejecución`.

## Nota de ejecución

### Phase 0 — Gobernanza y prerrequisitos (2026-10-06)

- `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/` (decisión humana).
- `AUTHORIZATION = HUMAN_GRANTED`; `Status` → `Aprobado para ejecución`.
- Gate de salida satisfecho: RFC-80 `Accepted`, placement `ADAPT` (familia existente `Project-durable knowledge base`), autorización registrada.
- Verificación: `python tools/check_plan_structure.py --root .` y `python tools/check_plan_citations.py`.

### Phase 1 — Primitivas de persistencia (2026-10-06)

- `runtime/memory/store.py` (nuevo): `MemoryStore` (write/read/delete/list/rebuild), `atomic_write`, `canonical_json`.
- Reutiliza los patrones de `runtime/orchestrator/store.py` y `runtime/toolcalls/project_store.py` (escritura atómica temp + os.replace, lecturas fail-closed, rebuild determinista).
- `tests/test_memory_store.py` (nuevo): 9 tests (atomicidad, corrupción, rebuild determinista). **PASS.**

### Phase 2 — Episodic Memory (2026-10-06)

- `runtime/memory/episodic.py` (nuevo): `Session`, `Observation`, `Evidence` (dataclasses frozen, inmutables); clases de evidencia cerradas; proveniencia (`source_sessions`/`source_files`).
- `tests/test_memory_episodic.py` (nuevo): 7 tests (inmutabilidad I-001/I-002, proveniencia I-003, roundtrip). **PASS.**

### Phase 3 — Modelo semántico (2026-10-06)

- `runtime/memory/semantic.py` (nuevo): `Claim` (tipos fact/constraint/requirement/invariant/decision/lesson/rejected_approach); lifecycle (candidate/active/stale/contradicted/superseded/retired/archived); estado epistémico (observation/attested/inferred/verified); applicability; proveniencia.
- `tests/test_memory_semantic.py` (nuevo): 9 tests (I-004/I-005/I-006, validación de vocabularios). **PASS.**

### Phase 4 — Extracción y lifecycle de candidatos (2026-10-06)

- `runtime/memory/extraction.py` (nuevo): `promote`, `discard`, `is_operational` (I-025: candidato no operacional sin transición).
- Tests en `tests/test_memory_extraction_relations.py`. **PASS.**

### Phase 5 — Relaciones, contradicción y supersession (2026-10-06)

- `runtime/memory/relations.py` (nuevo): vocabulario de 10 relaciones; `Relation`; contradicción explícita (I-007) ≠ supersession (I-009).
- Tests en `tests/test_memory_extraction_relations.py`. **PASS.**

### Phase 6 — Synthesis (2026-10-06)

- `runtime/memory/synthesis.py` (nuevo): `Synthesis` versionada con lineage (`supersedes`).
- Tests en `tests/test_memory_synthesis_consolidation.py`. **PASS.**

### Phase 7 — Consolidation + semantic non-regression gate (2026-10-06)

- `runtime/memory/consolidation.py` (nuevo): `source_fingerprint` (SHA-256, orden-independiente), `semantic_diff` (`NO_OP`/`PUBLISH`), `verify_non_regression` (I-017/I-018/I-021), `publish` (atómico, rechazo preserva fuentes).
- Tests en `tests/test_memory_synthesis_consolidation.py`. **PASS.**

### Phase 8 — Operational Memory (2026-10-06)

- `runtime/memory/operational.py` (nuevo): proyección reconstruible (I-011), no-autoritativa (I-012), solo claims `active`.
- Tests en `tests/test_memory_operational_retrieval_archive.py`. **PASS.**

### Phase 9 — Retrieval (2026-10-06)

- `runtime/memory/retrieval.py` (nuevo): retrieval progresivo y acotado (I-029), histórico no reactivado (I-014), contradicción no resuelta excluida (I-008).
- Tests en `tests/test_memory_operational_retrieval_archive.py`. **PASS.**

### Phase 10 — Archive (2026-10-06)

- `runtime/memory/archive.py` (nuevo): archive ≠ delete (I-013), rehydrate sin reactivación (I-014/I-027).
- Tests en `tests/test_memory_operational_retrieval_archive.py`. **PASS.**

### Phase 11 — Migración (2026-10-06)

- `runtime/memory/migration.py` (nuevo): `migrate_legacy_fact` (transforma snapshot → claim candidato, I-030/I-025/I-016).
- Tests en `tests/test_memory_migration_metrics_cutover.py`. **PASS.**

### Phase 12 — Métricas (2026-10-06)

- `runtime/memory/metrics.py` (nuevo): `memory_health`, `knowledge_debt` (sin targets numéricos).
- Tests en `tests/test_memory_migration_metrics_cutover.py`. **PASS.**

### Phase 13 — Cutover (2026-10-06)

- `runtime/memory/cutover.py` (nuevo): stages M0–M5, `source_of_truth` (SoT única por stage), `is_memory_authoritative`.
- Tests en `tests/test_memory_migration_metrics_cutover.py`. **PASS.**

### Verificación integral (2026-10-06)

- `python tools/check_plan_structure.py --root .` → **PASS**.
- `python tools/check_plan_citations.py` → **PASS**.
- `python tools/check_protocol_invariants.py --payload protocol .` → **PASS**.
- `python -m pytest tests/` → **1242 passed**.

### Entregable #1 — Contrato de protocolo (2026-10-06)

- `protocol/.agents/standards/context/MEMORY_SYSTEM.md` (nuevo): estándar autocontenido del Memory System (5 capas, entidades, lifecycle, estado epistémico, applicability, provenance, relaciones, síntesis, consolidación, operacional, retrieval, archive, invariantes I-001…I-030). **PASS** (check_protocol_invariants + check_taxonomy_coherence).

### Entregable #4 — Checker de forma (2026-10-06)

- `tools/check_memory_store.py` (nuevo): valida el store de memoria (`.project/knowledge/*.json`) — `kind`, campos requeridos, vocabularios cerrados; ausencia OK.
- `tests/test_check_memory_store.py` (nuevo): 7 tests (stdlib-only, ausencia, válidos, inválidos). **PASS.**
