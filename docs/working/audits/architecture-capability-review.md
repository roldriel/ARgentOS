# Architecture Capability Review — ARgentOS

**Clase documental:** Working / Analysis (provenance) — no normativo.
**Naturaleza:** revisión de capacidad arquitectónica, `READ_ONLY` respecto del sistema.
**Autoridad de este documento:** ninguna. Registra conclusiones y evidencia; no crea
mecanismos, no modifica arquitectura, no autoriza trabajo.

> **Placement.** Este artefacto se creó en la ruta que la instrucción del Change
> especificó de forma explícita (`docs/architecture-capability-review.md`). Por
> su clase (Working / Analysis) la familia `Working analysis` de
> `docs/placement-contract.md:6. Namespace selection` apunta a
> `docs/working/{audits,research,proposals}/`, y `docs/architecture/` está
> declarado `archived` en `docs/AGENTS.md:Folder → class map`; la única excepción de
> raíz documentada en `docs/` es `docs/AUDITORIA_DOCUMENTACION.md`. **Fase 1 (F6):**
> la regla aplicable a una ubicación pedida fuera de la familia canónica **no** es
> `PC-75` (que gobierna el desacuerdo entre el contrato y su enforcement), sino
> `PC-52` («a request is not an authorization»: si quien pide tiene la autoridad del
> dominio, el acto correcto es **registrar la excepción y después colocar**), `PC-27`
> (la excepción se registra en el artefacto que ya posee la decisión —un plan, un RFC,
> un ADR o el contrato de la familia—, de forma atribuible y auditable) y `PC-29` (un
> agente no crea, extiende ni reinterpreta excepciones). **Determinación:** la
> excepción **no** está registrada en ningún artefacto autorizante, y ésta sería la
> **segunda** instancia de la misma desviación (tras `docs/AUDITORIA_DOCUMENTACION.md`;
> `PC-28`). La clase y el namespace canónico quedan determinados (`Working / Analysis`
> → `docs/working/audits/`, con fila en `docs/working/audits/INDEX.md`); **el acto de
> registro y la ubicación física quedan reservados a `HD-INT-G`**
> (`HUMAN_DECISION_REQUIRED`, Diseño §25). Ver §11.8.

**Fecha:** 2026-09-22
**Baseline de ARgentOS:** `dev` @ `820da21`; `protocol/.agents/VERSION` = `11.6.2`.
**Estado Git al iniciar:** una (1) ruta untracked **preexistente y ajena** a este
trabajo (`MASTER_PENDING_WORK_INVENTORY.md`); 0 modificaciones rastreadas.

---

## 1. Executive Summary

1. **No se identificó un prerrequisito arquitectónico que obligue a posponer la
   autonomía supervisada por razones estructurales.** El modelo
   `Human authority → Authorized objective/scope → Orchestrator → Observe →
   Derive → Delegate → Execute → Verify → Correct/Recover → Revalidate →
   Continue → Stop/Escalate` (`ROADMAP.md:Etapa B`) ya tiene, en ARgentOS, un
   mecanismo por cada transición, y esos mecanismos están implementados,
   testeados y dogfoodeados. Ver §5 y §11.

2. **La conclusión no es «nada falta».** Se identificaron **dos carencias
   reales**, ambas de *ejecución*, no de modelo:

   - **PR-1 — Admisión de efectos fuera de frontera en el punto de ejecución.**
     El estándar `AUTHORIZATION.md` define el modelo completo (efecto ⇒ entrada
     `effects` con `authorized_by` y `status`; `AUTHORIZATION_UNDETERMINED`
     nunca es `UNAUTHORIZED`), pero **ningún ejecutor de ARgentOS verifica esa
     admisión**: el host DEV verifica *paths de escritura* contra el Scope, no
     *clases de efecto* contra autorización. Clasificación:
     `ARCHITECTURAL_PREREQUISITE` para una autonomía que ejecute efectos reales.
   - **PR-2 — Presupuesto de ejecución como frontera de recurso, no como guarda
     de bucle.** El host tiene `max_iterations` y un *no-progress guard*
     (`runtime/orchestrator/host.py:105,898-954,1009-1029`), pero no un
     presupuesto declarado, verificable y **persistente a través de reinicios**
     para iteraciones, tiempo, reintentos, delegaciones, llamadas al modelo o
     costo. Clasificación: `ARCHITECTURAL_PREREQUISITE` (de frontera de recurso)
     para ejecución desatendida de duración no trivial.

3. **`Execution Contract / Work Unit` ya existe implícitamente y no requiere un
   concepto nuevo.** La unidad «ejecutable, identificable, delegable,
   persistible, verificable y recuperable» está materializada por
   `Plan + Delegation + WorkerResult + declared_scope + Validation Anchor +
   journal`, con una relación explícita
   `delegation → worker result → ingestion → next action`
   (`.agents/policies/autonomous-orchestration.md:§4`). Lo que **no** existe es
   una *identidad única* de esa unidad; la evidencia demuestra que no se
   necesita (§4).

4. **`Durable Execution` en el sentido de los frameworks externos no es
   necesaria, y el motivo es arquitectónico, no terminológico.** ARgentOS no
   reanuda desde estado de ejecución persistido: **reconstruye su posición desde
   el repositorio** (Git + artefactos de gobernanza + evidencia) y re-deriva.
   Esa propiedad está testeada de forma explícita
   (`tests/test_autonomous_orchestrator.py:970-1006`, «restart reconstructs and
   continues without lost continuity») y declarada
   (`.agents/policies/autonomous-orchestration.md:§9`). Un store perdido es
   `GAP`, nunca un hecho positivo (`runtime/orchestrator/store.py:18-22`).
   `Replay`/`reanudación desde checkpoint` serían un **segundo** modelo de
   verdad, no una mejora del existente.

5. **`Execution Graph` no está justificado.** No hay concurrencia real hoy, ni
   dependencia entre trabajos que el modelo secuencial no resuelva, ni garantía
   concreta que un grafo añada. Las dependencias se derivan del estado del
   repositorio (`derivation.py`), y un grafo explícito introduciría una segunda
   representación de relaciones que ya son legibles desde los artefactos. Ver
   §4.

6. **`Semantic Context` no tiene carencia.** `SemanticContextIdentity`,
   `SegmentIdentity`, `MaterializationIdentity`, la clasificación
   Stable/Dynamic, el prefijo estable y el Prompt Cache ya constituyen una
   arquitectura de contexto completa y con invariantes verificables
   (`I-MAT-001`). Las ideas externas en esta dimensión no aportan una garantía
   nueva. Ver §4.

7. **La evaluación en ARgentOS no es métrica: es una capa de juicio con
   artefacto y evidencia** (`RUBRICS.md`, `reviewer`, `verifier`,
   `## Criteria Evaluation`, `adversarial-deliberation`). Falta, sin embargo,
   una capacidad distinta: **detección de regresión de calidad** — ARgentOS
   verifica *presencia y estructura* (`H06` «no juzga calidad») y *cumplimiento
   de comandos declarados*, pero no compara la calidad de una salida con la de
   una salida previa. Clasificación: `POST_AUTONOMY`. Ver §4.

8. **Nada de lo observado en las cinco fuentes externas cambia materialmente el
   diseño necesario para la autonomía.** Los mecanismos externos más fuertes
   (checkpointing con `FileCheckpointStorage` y reanudación en `agent-framework`)
   resuelven un problema que ARgentOS resolvió de otra forma; los más débiles
   (`microbots`: sin resume, sin HITL, sin telemetría estructurada) son
   estrictamente inferiores al baseline de ARgentOS. El valor de la comparación
   es **confirmatorio** y, en un punto, **correctivo**: `PR-1` (admisión de
   efectos) aparece al contrastar el borde de autoridad de ARgentOS con el de
   sistemas que ejecutan efectos reales. La comparación también produjo un
   hallazgo transversal citable: **tres de las cinco fuentes declaran una
   capacidad que su propio ejecutor no realiza** — `prompty` documenta la regla
   de no-duplicar efectos comprometidos y su runtime Python no persiste
   checkpoints; MACAE pasa un store en memoria a un framework que ofrece uno
   durable; `agent-framework` marca su capa de evaluación como `@experimental`
   mientras su README se presenta como production-grade. ARgentOS no tiene ese
   hueco: donde declara una garantía, la realiza y la testea. Ver §3 y §4.

9. **Respuesta al criterio de éxito del Plan:** el siguiente trabajo puede ser
   `Plan149 / Retrospective → SAE / Autonomy`, **siempre que** `PR-1` y `PR-2`
   se traten como parte de la propia implementación de la siguiente etapa de
   autonomía y no como features posteriores — porque ambas son fronteras del
   *ejecutor*, y el ejecutor es lo que la Etapa B construye. Ninguna de las dos
   invalida el roadmap A → B → C ni exige un cambio de arquitectura previo.

---

## 2. Current ARgentOS Capability Baseline

Sólo las capacidades relevantes para esta revisión. Se cita el mecanismo real y
su evidencia; no se repite la auditoría de mecanismos ya establecida
(Change Lifecycle, SAE, Orchestrator, Prompt Cache, Placement).

### 2.1 Ejecución y conducción (DEV)

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Bucle del host | `observe → derive → authorize → delegate → execute → ingest → verify → decide → continue/stop` | `runtime/orchestrator/host.py:1-26`; `.agents/policies/autonomous-orchestration.md:§1` |
| Derivación de la siguiente acción | función pura sobre la observación; vocabulario cerrado de acciones derivadas | `runtime/orchestrator/derivation.py:195-466`; `contracts.py:86-215` |
| Frontera de autoridad | `AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN`; release/promotion/tag `FORBIDDEN` | `runtime/orchestrator/authority.py`; `contracts.py:226-283` |
| Frontera de autonomía (SAE) | envolvente derivada del Plan; membresía exacta de scope; checkpoint de autorización; no retroactividad | `runtime/orchestrator/autonomy.py`; `.agents/policies/supervised-autonomous-execution.md` |
| Enforzamiento **antes** del efecto | `ExecutionHost._apply_autonomy_gate` sobre el conjunto **completo** de write-targets | `host.py:167-` , `:768-833`; `tests/test_sae_scope_enforcement.py:312-560` |
| Detección **después** del efecto (defensa en profundidad) | comparación de *content snapshots*, independiente del relato del worker | `host.py:741-766`; `tests/test_agent_worker.py:1040` |
| Worker como frontera inyectable | `WorkerAdapter` con tres implementaciones: `CommandWorker`, `NullWorker`, `AgentWorker` | `runtime/orchestrator/worker.py:432,551`; `agent_worker.py:285` |
| Invocación agéntica | `AgentInvoker` (Protocol, un método) + `NullAgentInvoker` honesto por defecto | `agent_worker.py:199-235` |
| Resultado persistente | `WorkerResult` (M4, 12 campos; observaciones y claims separados) | `contracts.py:291-581` |
| Store de evidencia | `.project/orchestrator/plan-<NNN>/{delegations,worker-results,journal.jsonl,runs}`; escritura atómica; lectura *fail-closed* | `runtime/orchestrator/store.py:1-22,101-119,212-252` |
| Reconstrucción | `--reconstruct` reconstruye el recorrido **sólo** de evidencia persistida, sin memoria de sesión | `host.py:1077-1128`; `__main__.py:9-14` |

### 2.2 Límites y presupuesto

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Límite de iteraciones (bucle) | `DEFAULT_MAX_ITERATIONS = 8`, CLI `--max-iterations`; produce `STOP_MAX_ITERATIONS` | `host.py:105,898-954`; `derivation.py:469-476`; `tests/test_autonomous_orchestrator.py:1032` |
| Guarda de no-progreso | *fingerprint* de hechos de gobernanza + repetición de la acción ⇒ `STOP_NO_PROGRESS` | `host.py:920-940`; `observation.py:688-709`; `tests/test_autonomous_orchestrator.py:1009-1029` |
| Pasos del razonamiento local del worker | `DEFAULT_MAX_STEPS = 24`; techo ⇒ resultado **incompleto**, nunca éxito | `agent_worker.py:85-87,296,357` |
| Timeout de comandos | `DEFAULT_TIMEOUT_SECONDS` en la ejecución del command-set | `worker.py`; `agent_worker.py:68,297,529` |
| Context Budget (Protocol) | límite semántico finito y positivo; `declared`/`consumed` medidos y auditables; **no trunca ni bloquea** en delegación | `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:25,50-62`; `CONTEXT.md:38-57` |
| Context Budget (runtime DEV) | `context_budget` declarado y materializado en el prompt; estimación `ceil(chars/4)` | `runtime/toolcalls/budget.py:19-21`; `prompt_rendering.py:32,69`; `agent_worker.py:79-83,298` |
| Gate de coherencia de budget (payload) | `H15` — budget no finito/no positivo ⇒ `F1`; pareja `declared`/`consumed` obligatoria | `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md:53-77`; `METRICS.md:61-67` |

### 2.3 Autoridad y admisión de capacidad

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Capacidad ≠ autorización | estándar explícito: la disponibilidad de una tool/skill no autoriza su uso | `protocol/.agents/standards/runtime/AUTHORIZATION.md:7-23` |
| Admisión de efectos fuera de frontera (Protocol) | `## Effects` en `TASK_SPECIFICATION.md`: `kind` (enum cerrado), `authorized_by`, `evidence_ref`, `status`; estados `AUTHORIZED`/`UNAUTHORIZED`/`AUTHORIZATION_UNDETERMINED` | `AUTHORIZATION.md:44-111`; `PROTOCOL_BOUNDARIES.md:155-191` |
| Admisión de capacidad de ejecución (DEV) | mapeo **total** acción→clase; una acción sin entrada es `STOP_UNCLASSIFIABLE_ACTION` | `host.py:125-150`; `contracts.py:139-143`; `tests/test_autonomous_scope.py:574` |
| Admisión de perfiles/skills (Protocol) | `H15` verifica resolubilidad de profile y skill **antes** de delegar | `H15-delegation-validity.md:53-77` |
| Flags de capacidad | `features.toml`, resueltos por el Orchestrator en H01; un flag habilitado es obligación conductual | `protocol/.agents/features.toml:1-25` |

### 2.4 Reanudación, recuperación y continuidad

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Reanudación de sesión (Protocol) | iteración parcial; «last intact artifact»; re-ejecución del gate de salida pendiente; base de reanudación registrada | `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:35-52` |
| Continuidad del host (DEV) | el host no tiene estado: re-observa y re-deriva; la numeración de iteraciones continúa desde el journal | `.agents/policies/autonomous-orchestration.md:§9`; `host.py:23-25` |
| Continuidad verificada | test de reinicio: dos procesos, sin memoria compartida, continuidad sin cursor y condición terminal idéntica en un tercer host | `tests/test_autonomous_orchestrator.py:970-1006` |
| Ausencia declarada | store perdido/corrupto = `GAP`; líneas ilegibles del journal se **devuelven**, no se descartan | `store.py:45-71,212-242` |
| Revalidación | anchor A2 para identidad de contenido nueva, sin reemplazar A1; `RUN_REVALIDATION` | `runtime/orchestrator/governance.py:364-425`; `host.py:796-817` |
| Recuperación dentro del scope | `failure → diagnose → correct/retry → verify → continue`, con el mismo envolvente | `.agents/policies/supervised-autonomous-execution.md:§7`; `tests/test_autonomous_scope.py:296-316` |

### 2.5 Observabilidad y evaluación

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Journal de iteraciones | un registro por iteración: estado observado, acción derivada, autoridad, delegación, resultado, señales, correcciones, stop y su razón | `.agents/policies/autonomous-orchestration.md:§8`; `host.py:376-443` |
| Resumen de autonomía | vista derivada de evidencia existente; `human_operational_intervention` ≠ `human_authority_decision`; `recoveries` y `findings_autonomously_corrected` con reglas anti-fabricación | `autonomy.py:summarize_autonomy`; `.agents/policies/supervised-autonomous-execution.md:§11` |
| Métricas del Protocol | catálogo de eventos, `seq`/`timestamp`/`clock`, clases `Derived`/`Recorded`/`Verified`; agregación advisory | `protocol/.agents/contracts/METRICS.md`; `PROTOCOL_METRICS.md:188-219` |
| Garantías y su clase de verificación | catálogo cerrado de garantías en cinco clases (Declarative / Verifiable / Mechanically enforced / Agent-judgment-dependent / External-actor-dependent) | `protocol/.agents/harness/INDEX.md:81-118` |
| Evaluación por juicio | `rubrics`, `reviewer`, `verifier`, `## Criteria Evaluation`, `## Rubric Evaluation`, deliberación adversarial atribuida | `protocol/.agents/standards/quality/RUBRICS.md:7,88-95`; `roles/verifier.md:13,45`; `skills/adversarial-deliberation/SKILL.md` |
| Evaluación de salida de gates | `HARNESS_REPORT.md` + `state.json`, conciliación bidireccional | `harness/INDEX.md:99-139` |
| Semántica de fallo | `GAP ≠ ANOMALY ≠ FAIL`; sólo `VALID` es evidencia positiva | `contracts.py:41-83`; `docs/rfc/75-change-lifecycle.md:Mecanismo 13` |

### 2.6 Contexto semántico

| Capacidad existente | Mecanismo real | Evidencia |
|---|---|---|
| Segmentos | Core / Project / Worker como dominios semánticos de un único modelo de persistencia | `protocol/.agents/standards/context/CONTEXT.md:264-278` |
| Identidad de segmento | `SegmentContentIdentity` (SHA-256 canónico) y `SegmentIdentity = {semantic_version, content_identity, namespace}` | `CONTEXT.md:280-301` |
| Identidad semántica del contexto | `SemanticContextIdentity` invariante a la materialización | `CONTEXT.md:303-322` |
| Clasificación Stable/Dynamic | base del prefijo estable y del Prompt Cache | `CONTEXT.md:230-263` |
| Prefijo estable (provider-bound) | regla de elegibilidad, alcance Core+Worker, bootstrap declarado vacío, frontera con composición | `CONTEXT.md:354-378`; `docs/rfc/78-provider-bound-stable-prefix-materialization.md:5` |
| Materialización canónica | `variante + serialización + orden`; invariante `I-MAT-001`; `Ordering Contract v1/v2` | `runtime/toolcalls/canonical.py`; `runtime/README.md:50-125` |
| Invalidación semántica | sólo por cambio de identidad (`content_identity` / `semantic_version`); TTL y freshness gobiernan lifecycle, nunca correctness | `CONTEXT.md:339-352` |

### 2.7 Fronteras declaradas del baseline

- **No hay provider, modelo, red ni credenciales** en este repositorio; el
  invoker real se inyecta desde el entorno de ejecución
  (`runtime/README.md:366-448`; `.agents/policies/autonomous-orchestration.md:§11.2`).
- **No hay evaluación de calidad automatizada**: `H06` valida estructura, no
  juzga calidad (`RUBRICS.md:7`).
- **No hay telemetría ni economía** en el runtime (RFC-74 sin tocar).
- **La correspondencia WorkerResult ↔ contenido** se establece por Scope
  declarado e identidad de contenido, no por vínculo causal
  (`.agents/policies/autonomous-orchestration.md:§10`).
- **El enforzamiento cubre los efectos que el host controla**: prevención donde
  controla la escritura, detección donde no puede interponerse
  (`supervised-autonomous-execution.md:§12`).

---

## 3. External Capability Matrix

| Capability | External Evidence | ARgentOS Equivalent | Gap | Guarantee Added | Autonomy Impact | Prerequisite | Domain | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Execution Contract / Work Unit | `prompty`: `.prompty` como artefacto portable; contratos `inputs`/`outputs` declarados; validación que explícitamente **no** type-checkea (`spec/spec.md:3012-3044`) (P1, EXTERNAL_CODE); `agent-framework`: `SupportsAgentRun` Protocol + sesiones (P3) | `Plan` + `Delegation` + `WorkerResult` (M4) + `declared_scope` + `Validation Anchor` + journal | Identidad única de la unidad (no la capacidad) | Ninguna nueva: la relación ya es explícita y persistida | Delegación | NO | BOTH (Protocol: contrato; DEV: ejecución) | ALREADY_SOLVED |
| Capability Governance / admission | `prompty`: gate de permiso inyectado por el host (`ResolvePermission`, eventos `permission_requested`/`permission_resolved`, `McpTool.approvalMode`) (P1, EXTERNAL_CODE); MACAE: teams declarativos + allow-list MCP `DOMAIN_ALLOWED_TOOLS`, `agent_registry.py` **no** es un gate (P5, EXTERNAL_CODE) | `AUTHORIZATION.md` (capacidad ≠ autorización; `## Effects`), `H15` (resolubilidad), mapeo total acción→clase, `features.toml` | Admisión de **efectos** en el punto de ejecución DEV | Autoridad: ningún efecto real sin autorización declarada | Ejecución real / frontera humana | **YES** (para efectos reales) | DEV (realización) + PROTOCOL (norma) | **ARCHITECTURAL_PREREQUISITE** (PR-1) |
| Durable Execution | `agent-framework`: `WorkflowCheckpoint` + `CheckpointStorage` (InMemory/**File** con escritura atómica) + `Workflow.run(checkpoint_id=…)`; `graph_signature_hash` (P3, EXTERNAL_CODE); `prompty`: contrato `EngineCheckpoint`/`ResumeContext` con `reconciliationRequired` y la regla «MUST NOT duplicate an effect the checkpoint records as committed», pero el store concreto es **Java-only InMemory**; Python emite eventos sin persistir (P1, EXTERNAL_CODE); MACAE: `InMemoryCheckpointStorage()` — **no durable**, sin replay (P5, EXTERNAL_CODE); ACI: durabilidad **de ingesta** (persist-then-202 + receipts SQLite, P4); `microbots`: **ausente** (P2) | Reconstrucción desde el repositorio + journal append-only + store *fail-closed* | Ninguno funcional: la posición se **re-deriva**, no se reanuda desde estado guardado | Continuidad (ya poseída por otra vía) | Recuperación | NO | DEV | ALREADY_SOLVED |
| interruption / resume | `microbots`: sin resume ni kill/restart (P2); `prompty`: `cancellation.py` como control de runtime, y `resumeSameIteration` en el contrato (P1); `agent-framework`: `Workflow.run(checkpoint_id=…, responses=…)` (P3); ACI: replay de ingesta con leases (P4) | Reanudación de iteración parcial por «last intact artifact» (Protocol); reinicio del host sin cursor (DEV) | Ninguno a nivel de capacidad; falta **cancelación/abort** del host en vuelo (no del worker) | Continuidad | Recuperación | NO | PROTOCOL (procedimiento) + DEV (realización) | ALREADY_SOLVED |
| idempotent y race-safe execution | `prompty`: la regla de no-duplicación de efectos ya comprometidos es una **obligación documentada del contrato** de checkpoint, no un mecanismo del runtime Python (P1, EXTERNAL_CODE); `microbots`: `max_retries=3` con mensaje correctivo, sin idempotencia (P2); MACAE: `NOT_FOUND` para idempotency keys/ETags (P5); ACI: `EventIdempotencyCache` en ingesta (P4) | Registros de gobernanza idempotentes (marker-guarded, `_write_atomic`); identidad de contenido; delegación determinista | Ejecución concurrente: no hay coordinación porque no hay concurrencia | Idempotencia de registros (ya poseída); concurrencia segura no aplica | Persistencia / gobernanza | NO | DEV | ALREADY_SOLVED |
| Execution Graph | `agent-framework`: grafo **real** — `WorkflowBuilder`, `Executor`, `FanOutEdgeGroup` con `selection_func` condicional, `FanInEdgeGroup`, `SwitchCaseEdgeGroup`, supersteps, concurrencia por `asyncio.gather` (P3, EXTERNAL_CODE); MACAE, que lo consume, usa **lista plana ordenada, sin DAG** y exige completitud por prompt (P5); `prompty`: sin orquestación multi-paso, sólo un loop de tool-calling (P1) | Estado + derivación desde el repositorio; el orden lo determina la derivación | Ninguno: no hay concurrencia real ni dependencia no derivable | Ninguna: un grafo no añade verificación ni seguridad | Ninguna parte relevante | NO | UNKNOWN | NOT_VALUABLE_FOR_ARGENTOS |
| controlled concurrency | `agent-framework`: concurrencia **dentro** de un workflow por supersteps y edge runners (P3); `microbots`: sub-agente **síncrono**, «run only ONE at a time», sin flota (P2); MACAE: orquestación in-process, sin paralelismo de agentes (P5); `prompty`: sólo dispatch paralelo de tools dentro de una respuesta, `parallel_tool_calls=false` por defecto (P1) | `delegation execution modes`: subagent \| single-instance; single-instance declarado como riesgo con mitigaciones | Ninguno hoy: la ejecución es secuencial por diseño | Concurrencia segura (no requerida todavía) | Ninguna parte relevante (hoy) | NO | DEV | POST_AUTONOMY |
| Execution Budgets | `microbots`: `max_iterations=20`, `timeout_in_seconds=200`, `max_retries=3`, `max_rounds=5`, sub-agente 25/300, padre acumula iteraciones del hijo; `TODO: replace iteration_count with cost management` (P2); MACAE: `max_rounds=30`, `max_stall_count=5`, timeout 300 s, **sin** budget de tokens/costo (P5); `prompty`: `context_budget` en **caracteres**, `MAX_ITERATIONS=10`, `MAX_LLM_RETRIES=3`, `maxOutputTokens`; **sin** budget de costo ni de wall-clock (P1); `agent-framework`: **sin** timeout ni budget de costo/token en el camino de ejecución core — sólo `TokenUsage` contable por OTel (P3) | `max_iterations` (8) + no-progress guard + `DEFAULT_MAX_STEPS` (24) + timeout; Context Budget **semántico** medido | Falta presupuesto de **recurso de ejecución** declarado, verificable y persistente entre reinicios | Control de recursos; garantía de terminación por recurso (no sólo por falta de progreso) | Autonomía desatendida / operación | **YES** | DEV | **ARCHITECTURAL_PREREQUISITE** (PR-2) |
| Observability / Execution Intelligence | `agent-framework`: OpenTelemetry de primera clase, spans `workflow.run`/`executor.process`/`edge_group.process`/`message.send` (P3, EXTERNAL_CODE); `prompty`: tracing con `.tracy` (MUST), Console y OTel `gen_ai.*` (P1); MACAE: Azure Monitor + OTel + eventos custom (P5); ACI: plataforma de telemetría + grafo en Neo4j (P4); `microbots`: logging plano, sin OTel ni métricas (P2) | Journal por iteración + resumen de autonomía + `METRICS.md` + `HARNESS_REPORT.md` + `audit_gates` | Telemetría de ejecución *en vivo* y consultas agregadas (no hay backend) | Trazabilidad y reconstruibilidad (ya poseídas, con otro medio) | Observación | NO | DEV | ALREADY_SOLVED |
| Evaluation | `agent-framework`: `evaluate_agent`/`evaluate_workflow`, `EvalItem.expected_tool_calls`, `RubricScore` — **pero todo `@experimental(feature_id=EVALS)`** (P3, EXTERNAL_CODE); `prompty`: **NOT_FOUND** — sin graders, sin CLI; delega al framework de test del usuario (P1); MACAE: **sin harness** en repo; la afirmación de eval offline es sólo documental (`docs/TRANSPARENCY_FAQ.md:12`, P5, EXTERNAL_DOC); ACI: sin evaluación de calidad de contexto (P4); `microbots`: harness train↔eval propio con `EvalOutcome` y SWE-bench (P2) | Rubricas + reviewer/verifier + `## Criteria Evaluation` + deliberación adversarial + gates con evidencia | No hay comparación de calidad contra una salida previa (regresión de calidad) | Detección de regresión de calidad / evaluación comparativa | Autonomía *después* de ampliada | NO | BOTH | POST_AUTONOMY |
| Semantic Context | ACI: grafo de eventos, **sin** distinción stable/dynamic ni identidad de contexto (P4, EXTERNAL_CODE); `prompty`: frontmatter con `inputs`/`outputs` y `metadata` (dict libre); **sin** versionado de prompt y **sin** modelo de contexto (P1); `agent-framework`: `ContextProvider` con hooks `before_run`/`after_run` y `HistoryProvider`/`VectorStoreHistoryProvider` — memoria/estado del agente, no identidad semántica de contexto (P3, EXTERNAL_CODE) | `SemanticContextIdentity`, `SegmentIdentity`, `MaterializationIdentity`, Stable/Dynamic, prefijo estable, Prompt Cache | Ninguno: los externos **no implementan** un modelo semántico de contexto comparable | Reproducibilidad de la materialización (ya poseída: `I-MAT-001`) | Contexto / persistencia | NO | PROTOCOL + DEV (runtime) | ALREADY_SOLVED |
| desired-state reconciliation | MACAE: estado de orquestación en dicts de módulo + Cosmos a nivel app, sin reconciliación (P5); `prompty`: `reconciliationRequired` es un **campo de contrato** sin realización en el runtime Python (P1, EXTERNAL_CODE) | Anchor ↔ estado actual (`anchor_stale`), checkpoint ↔ closure (`consistency_pass`), conciliación bidireccional `state.json` ↔ `HARNESS_REPORT` | Reconciliación sobre objetos observables de gobernanza, no sobre recursos declarados | Consistencia y detección de deriva (ya poseídas para el dominio que importa) | Gobernanza / cierre | NO | DEV + PROTOCOL | ALREADY_SOLVED |
| execution state persistence | `agent-framework`: `WorkflowCheckpoint` persistido con `messages`, `state`, `pending_request_info_events`, `iteration_count` y linaje `previous_checkpoint_id` (P3); `prompty`: contrato rico (`EngineCheckpoint`, `ResumeContext`, `EventJournalWriter`) con implementación concreta sólo en Java (P1); `microbots`: sólo memoria markdown + `result.json` por ronda (P2) | Store de evidencia + journal + artefactos durables de gobernanza; el repositorio **es** la fuente de verdad | Persistencia de estado *del host* (deliberadamente inexistente) | Continuidad (ya poseída por reconstrucción) | Persistencia | NO | DEV | ALREADY_SOLVED |
| failure recovery | `microbots`: reparación en cuatro capas, nunca aborta; `while` sin try/except (P2); `prompty`: `RetryPolicyRequest`/`max_attempts` y `guardrails` como controles de runtime (P1); ACI: dead-letter + replay de ingesta (P4); `agent-framework`: sin política core de reintento (sólo un `RetryMiddleware` de ejemplo) (P3) | Clases de fallo `GAP/ANOMALY/FAIL/BOUNDARY`; recuperación con el mismo envolvente; `RUN_REVALIDATION`; defensa en profundidad | Ninguno funcional: la recuperación está declarada y testeada | Recuperación (ya poseída) | Recuperación | NO | DEV + PROTOCOL | ALREADY_SOLVED |
| human-in-the-loop / authority boundaries | `prompty`: gate de permiso inyectado por el host (`permission_requested` → `permission_resolved`; denegación visible al modelo como `permission_denied`) (P1, EXTERNAL_CODE); `agent-framework`: `request_info`/`@response_handler` + `IDLE_WITH_PENDING_REQUESTS`, resumen por `run(responses=…)` (P3); MACAE: pausa de aprobación de plan obligatoria + gate de clarificación `always_require`, ambos `asyncio.Event` en proceso (P5); `microbots`: **sin HITL**, «don't seek human intervention» (P2) | Frontera de autoridad (3 veredictos) + SAE (envolvente, checkpoint, no retroactividad) + frontera humana enumerada + `STOP_*` con autoridad nombrada | Ninguno: ARgentOS es estrictamente más fuerte que las referencias, que tienen gates sin frontera verificable por efecto | Autoridad | Autoridad humana | NO | DEV + PROTOCOL | ALREADY_SOLVED |
| *(adicional)* Isolation de ejecución de código no confiable | `microbots` (P2): Docker por contenedor, montajes read-only con overlayfs, `privileged=True` | Ninguno: ARgentOS no ejecuta código no confiable; no hay sandbox en el runtime | No aplica al baseline; sería un prerrequisito de una capacidad futura de ejecución de terceros | Aislamiento (no requerido por el modelo actual) | Ninguna parte relevante (hoy) | NO | UNKNOWN | REQUIRES_EVIDENCE |

**Notas de evidencia externa.** Las referencias `P1`–`P5` remiten al informe de
evidencia por repositorio (§12.2). Cuando una afirmación externa se verificó sólo
en documentación se marca `EXTERNAL_DOC`; cuando se leyó código, se cita el path
en §12.2. **Tres premisas de partida quedaron corregidas por la inspección** y se
registran como tales:

1. MACAE **no** está construido sobre Azure Durable Functions — el backend es
   `FastAPI` y el checkpoint storage es en memoria (P5).
2. `amplifier-context-intelligence` **no** es un sistema de contexto semántico
   sino una plataforma de telemetría/observabilidad con grafo (P4).
3. `prompty` **sí** define contratos de checkpoint/resume
   (`EngineCheckpoint`, `ResumeContext`) y **no** tiene versionado de prompt
   (P1) — dos hechos que la intuición habría invertido.

Un patrón aparece en **tres** de las cinco fuentes y es el hallazgo transversal
más citable: **contrato o capacidad declarada sin realización en el ejecutor**.
`prompty` define el contrato de checkpoint y el store concreto es Java-only
InMemory mientras Python sólo emite eventos; MACAE pasa
`InMemoryCheckpointStorage()` a un framework que ofrece `FileCheckpointStorage`;
`agent-framework` marca toda la capa de evaluación como `@experimental` pese a
que su README se presenta como production-grade (P1, P3, P5, EXTERNAL_CODE).
Ninguna de las tres realiza la garantía que declara.

---

## 4. Detailed Findings

### 4.1 Execution Contract / Work Unit — `ALREADY_SOLVED`

**Problema.** Sin una unidad de trabajo identificable y persistible, un
orquestador no puede delegar sin ambigüedad, ni verificar después *qué* se
ejecutó, ni recuperarse sin repetir trabajo, ni atribuir un efecto a una
autorización.

**Mecanismo externo.** `prompty` (P1) trata el prompt como artefacto portable —
un archivo `.prompty` (YAML frontmatter + markdown) ejecutable por **siete
runtimes** distintos, con `inputs`/`outputs` declarados como tipos y vectores de
conformance cross-runtime; eso da **portabilidad y conformidad de una pieza**, no
una unidad de trabajo con estado. Su validación de inputs es deliberadamente
débil: rellena `default`, falla con `ValueError` si falta un `required` y
**explícitamente no type-checkea** los valores (`spec/spec.md:3012-3044`); en
particular **no existe versionado de prompt**, sólo un `metadata` de diccionario
libre. `agent-framework` (P3) sí compone agentes y workflows con `SupportsAgentRun`
(Protocol con `run`, `create_session`, `get_session`) y sesiones de agente, pero
la unidad de trabajo es una construcción del framework, no un contrato
verificable del sistema.

**Equivalente actual.** La unidad existe, distribuida y con relación explícita:

```text
Plan (autoriza: Task + Scope)
  └── Delegation      (delegation_id, action, declared_scope, command_set,
                       expected_evidence, worker_kind, task, input_artifacts)
        └── WorkerResult (result_id, delegation_id, observaciones, claims,
                          problems, pending, authority_used, effects_executed)
              └── ingestion → next action
```

`delegation_id = f"plan{plan}-it{iteration:04d}-{action.lower()}"`
(`host.py:475`); la relación `delegation → worker result → ingestion → next
action` está declarada como explícita en los artefactos persistidos
(`autonomous-orchestration.md:§4`) y el host la lee de vuelta del store
(`host.py:707-719`). La *verificación* no depende del worker: el host compara
content snapshots fuera del worker (`host.py:741-766`). La *recuperabilidad* no
depende del store: se re-observa (`store.py:18-22`).

**Diferencia.** De garantía, y **favorable**: el `WorkerResult` M4 separa
estructuralmente observaciones de claims y no acepta `exit code 0` como
completitud (`contracts.py:22-29`). No hay diferencia contractual relevante: lo
que un framework externo llama *work unit* aquí es la tupla
`Plan/Delegation/WorkerResult`.

**Garantía.** Trazabilidad y verificabilidad, ya poseídas.

**Impacto sobre autonomía.** Ninguno negativo. La delegación ya funciona con
tres workers distintos sin cambiar el contrato.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `BOTH` — la norma de delegación vive en el Protocol
(`WORKER_DELEGATION_CONTRACT.md`); la ejecución, en DEV.

**Evidencia.** `runtime/orchestrator/contracts.py:322-396,399-497`;
`host.py:446-475,707-739`; `runtime/README.md:366-448`;
`.agents/policies/autonomous-orchestration.md:§4,§11`.

**Conclusión.** Introducir una entidad `WorkUnit` sería una **segunda
representación** de una relación que ya es explícita y persistida, y contradiría
la regla de una sola fuente de verdad por concepto
(`.agents/AGENTS.md:Fundamental operating rules 8`). No se justifica por
terminología.

### 4.2 Capability Governance / capability admission — `ARCHITECTURAL_PREREQUISITE` (PR-1)

**Problema.** Un sistema autónomo con capacidad de ejecutar efectos reales
(red, instalación, git remoto, cambios destructivos, escrituras fuera del
proyecto) necesita responder, **antes del efecto**, si ese efecto está
autorizado — y distinguir «no autorizado» de «no se pudo determinar». Sin esa
admisión, la autonomía es *capacidad sin permiso*: exactamente el estado que
`AUTHORIZATION.md:22-23` declara prohibido.

**Mecanismo externo.** Cuatro formas distintas, y ninguna **verifica
autorización**:

- `prompty` (P1) es el más cercano: un gate de permiso **en el camino de
  ejecución** (`ResolvePermission`, eventos `permission_requested`/`permission_resolved`,
  denegación visible al modelo, `McpTool.approvalMode`). Pero es un **booleano
  delegado al host**: no hay frontera declarada, ni scope, ni registro de qué
  autoridad autorizó, ni la distinción «no se pudo determinar».
- MACAE (P5) consume `agent-framework` con *equipos declarativos* y una allow-list
  de tools MCP (`DOMAIN_ALLOWED_TOOLS`, `src/backend/config/mcp_config.py:22-51`):
  la admisión es configuración declarativa de **disponibilidad**. Su
  `agent_registry.py` es un tracker de ciclo de vida (WeakSet + lock), **no** un
  gate de admisión.
- `agent-framework` (P3) no tiene un gate de admisión propio en el camino core:
  el HITL de `request_info` es un mecanismo de **respuesta**, no de autorización.
- `microbots` (P2) no tiene admisión en absoluto: su único gate es una blocklist
  de regex de comandos peligrosos, evaluada antes de ejecutar.

**Equivalente actual.** ARgentOS tiene el **modelo** completo, y es más fuerte
que las dos referencias:

- `AUTHORIZATION.md` define capacidad ≠ permiso, el bloque `## Effects` con
  `kind` (enum cerrado: `network | remote_git | install | destructive |
  write_outside_project`), `authorized_by` (`user | unattended_default`),
  `evidence_ref`, `status`; y los estados `AUTHORIZED` / `UNAUTHORIZED` /
  `AUTHORIZATION_UNDETERMINED`, con la invariante `AUTH-004`: la
  indeterminación **nunca** se reporta como denegación.
- `PROTOCOL_BOUNDARIES.md:155-191` enumera la frontera y declara que «the
  availability of a tool or skill is never an authorization».
- En DEV, la frontera SAE admite **clases de acción** con un mapeo total: una
  acción sin entrada en `_AUTONOMY_CLASS_BY_ACTION` es
  `STOP_UNCLASSIFIABLE_ACTION` (`host.py:125-150`;
  `tests/test_autonomous_scope.py:574`), y `H15` verifica resolubilidad de
  perfil y skill antes de delegar.

**Diferencia — la carencia concreta.** La admisión de ARgentOS se aplica a
**paths de escritura** y a **clases de acción internas**, no a **efectos**.
Verificado por inspección: el runtime DEV no lee ni evalúa el bloque `## Effects`
en ninguna parte — `effects` aparece sólo como campo de contrato
(`contracts.py:303,428,453,487,541`) y como valor informado por el worker
(`agent_worker.py:473`; `worker.py:524,593`). El host registra *qué efectos se
ejecutaron* (`effects_executed`) pero **no** verifica que exista autorización
para ellos, ni clasifica el resultado como `AUTHORIZATION_UNDETERMINED`. El
`## Effects` del Protocol es, para el ejecutor DEV, **evidencia no consumida**.

**Garantía que produce.** Autoridad: ningún efecto fuera de frontera sin
autorización registrada y verificada antes del efecto, con la distinción
`AUTHORIZED / UNAUTHORIZED / AUTHORIZATION_UNDETERMINED` preservada.

**Impacto sobre autonomía.** **Ejecución real** (Etapa B) y **frontera humana**.
Hoy el impacto es nulo *porque el host no puede ejecutar efectos*: no hay
provider, red ni credenciales (`runtime/README.md:366-448`). El día que se
inyecte un `AgentInvoker` real —la frontera que la Etapa B declara investigar—
la admisión de efectos pasa a ser la única barrera entre una instrucción
autorizada y un efecto no autorizado, porque el host **no puede interponerse**
dentro de la invocación (prevención donde controla el efecto, detección donde no
puede: `supervised-autonomous-execution.md:§12`).

**Prerrequisito.** `PREREQUISITE = YES` **para una autonomía que ejecute efectos
reales**. La autonomía quedaría arquitectónicamente **incompleta** sin ella: el
modelo ya declara qué es un efecto autorizado, y el ejecutor no lo hace cumplir.
No la vuelve insegura *hoy* —no hay efectos— pero sí la vuelve insegura en el
primer cambio que habilite ejecución real.

**Dominio.** `PROTOCOL` (la norma ya existe y no cambia) + `DEV` (falta la
realización del lado ejecutor). **No** corresponde crear un mecanismo nuevo en el
payload: la norma está escrita; lo que falta es que el consumidor la verifique.

**Evidencia.** `protocol/.agents/standards/runtime/AUTHORIZATION.md:1-123`;
`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:155-191`;
`runtime/orchestrator/contracts.py:303,428,453,487,541`;
`runtime/orchestrator/host.py:125-150,167-300`;
`runtime/orchestrator/agent_worker.py:473`;
`runtime/orchestrator/worker.py:524,593`;
`tests/test_sae_scope_enforcement.py:312-560`;
EXTERNAL_CODE: MACAE `src/backend/config/mcp_config.py:22-51`,
`src/backend/config/agent_registry.py`.

**Nota de honestidad.** Es `INFERENCE` que esta carencia *cause* un daño hoy:
no hay ejecución de efectos. Lo verificado es la **ausencia del mecanismo de
verificación**, no la ocurrencia de un incidente.

### 4.3 Durable Execution — `ALREADY_SOLVED`

**Problema.** Un proceso de orquestación puede morir a mitad de un trabajo. La
pregunta es si el sistema puede (1) detenerse, (2) persistir estado relevante,
(3) reiniciarse, (4) reconstruir contexto, (5) continuar desde un punto
reproducible, (6) no repetir efectos incorrectamente, y (7) verificar qué ocurrió
antes de continuar.

**Mecanismo externo.** Cuatro respuestas distintas, y esto es el hallazgo más
útil de la comparación:

- `agent-framework` (`P3`) tiene la realización **más completa** de las cinco
  fuentes: `WorkflowCheckpoint` con `messages`, `state`,
  `pending_request_info_events`, `iteration_count` y linaje
  `previous_checkpoint_id`; `CheckpointStorage` como Protocol;
  `InMemoryCheckpointStorage` **y `FileCheckpointStorage`** con escritura atómica
  y reintento; y `Workflow.run(checkpoint_id=…)` como punto de entrada de
  reanudación. Incluye `graph_signature_hash` para validar compatibilidad de
  topología al restaurar (EXTERNAL_CODE).
- `prompty` (`P1`) define el contrato más **expresivo** que se inspeccionó —
  `EngineCheckpoint` con `lastSequence`, `stablePrefixMessages`,
  `pendingToolRequests`, `completedToolResults`, `reconciliationRequired`,
  `finalOutputReady`, `resumeSameIteration`, y `ResumeContext` con
  `maxIterations`/`maxModelAttempts` — y su propio doc comment establece la regla:
  «A resumed run rebuilt from a checkpoint MUST NOT duplicate a model or tool
  effect that the checkpoint already records as committed». Pero el único store
  concreto del repositorio es `InMemoryCheckpointStore` (Java); el motor Python
  emite eventos `checkpoint_created` y **no persiste**, y la persistencia se
  inyecta desde un harness. **Es un contrato de durabilidad sin realización
  durable en el runtime de referencia.**
- MACAE (`P5`) **declara** el mismo framework que P3 pero pasa
  `InMemoryCheckpointStorage()` y guarda el estado de orquestación en dicts de
  módulo: **no es durable**, no hay replay ni evento externo.
- `amplifier-context-intelligence` (`P4`) sí tiene durabilidad, pero **de
  ingesta** (persist-then-202, log por sesión, receipts SQLite con estados
  `pending_enqueue|enqueued|committed_pending|written|quarantined`).
- `microbots` (`P2`) **no tiene** resume: el estado del bucle vive en memoria y
  el contenedor se destruye al terminar.

**Equivalente actual — y la diferencia arquitectónica.** ARgentOS **no reanuda
desde estado persistido: reconstruye su posición desde el repositorio**.
`observe()` se ejecuta al inicio de cada iteración; la siguiente acción es una
función pura de la observación (`derivation.py`); el host no tiene cursor,
memoria ni sesión (`host.py:11-25`). La numeración de iteraciones se deriva del
journal (`host.py:901,907`), y las delegaciones se identifican por
`(plan, iteration, action)`, de modo que re-derivar la misma acción en la misma
iteración produce la **misma** identidad y sobrescribe evidencia efímera con el
mismo significado, sin duplicar efectos de gobernanza (los registros son
marker-guarded e idempotentes: `governance.py:83-88`).

El punto (6) —«evitar repetir efectos incorrectamente»— se resuelve por una vía
distinta y más fuerte que el replay: **los efectos de gobernanza son
idempotentes y los efectos de contenido son verificados por identidad**. Si un
reinicio re-ejecuta una validación, la identidad de contenido del anchor decide
si hacía falta; si re-ejecuta una escritura, la frontera SAE la admite o la
refusa de nuevo; y si un worker escribió fuera del scope antes de morir, la
comparación de content snapshots lo detecta (`host.py:741-766`).

**Diferencia.** Arquitectónica, y deliberada: un `CheckpointStorage` + replay
sería un **segundo** modelo de verdad sobre el mismo hecho (dónde está el
trabajo), contra la regla de una sola fuente de verdad
(`.agents/AGENTS.md:8`). ARgentOS evita la durabilidad *del proceso* porque su
posición **no es estado**: es derivable.

**Lo que la evidencia externa aporta aquí.** El patrón de §3 (contrato de
durabilidad sin realización) es exactamente el riesgo que ARgentOS evita por
construcción: `prompty` documenta la regla de no-duplicación de efectos y no la
implementa en su runtime de referencia; MACAE usa un store en memoria donde el
framework ofrece uno durable. ARgentOS no tiene ese hueco porque **no tiene la
capacidad**: no hay un contrato de checkpoint que pueda quedar sin realizar. La
no-duplicación de efectos no es una obligación documentada en ARgentOS; es una
propiedad de su admisión (SAE) y de su verificación (identidad de contenido).

**Garantía.** Continuidad y recuperación — **ya poseídas**, con el medio
`reconstrucción` en lugar de `replay`. La garantía que un replay añadiría sería
*exactitud de repetición de efectos internos no registrados en el repositorio*;
ARgentOS no tiene tales efectos en su modelo actual (declara que la
correspondencia con el contenido se establece por Scope e identidad, no por
vínculo causal: `autonomous-orchestration.md:§10`).

**Verificación.** `tests/test_autonomous_orchestrator.py:970-1006` ejecuta
literalmente el escenario: primer proceso interrumpido por su propio límite de
iteraciones, segundo proceso sin memoria compartida que continúa la numeración y
alcanza la condición terminal, tercer proceso que re-deriva la misma condición
terminal. `tests/test_agent_worker.py:762` cubre la recuperación sólo desde
evidencia persistida.

**Impacto sobre autonomía.** Recuperación y persistencia: cubiertas.

**Prerrequisito.** `PREREQUISITE = NO`. **La autonomía no quedaría incompleta sin
durable execution**; quedaría **peor**, porque ganaría un segundo lugar donde
puede vivir la verdad.

**Dominio.** `DEV`.

**Evidencia.** `runtime/orchestrator/host.py:11-25,898-971,1077-1128`;
`runtime/orchestrator/store.py:1-22,45-71`;
`.agents/policies/autonomous-orchestration.md:§9,§11.4`;
`tests/test_autonomous_orchestrator.py:970-1006`;
`tests/test_agent_worker.py:762,792`;
EXTERNAL_CODE: `agent-framework` checkpoint storage; MACAE
`src/backend/orchestration/connection_config.py:25-36`,
`orchestration_manager.py:185-195`; ACI `context_intelligence_server/recovery.py:25-67`;
`microbots` `src/microbots/MicroBot.py:227-228`.

**Límite declarado.** El modelo `reconstrucción` presupone que **todo hecho
relevante es observable desde el repositorio**. Un efecto que ocurra fuera del
repositorio y no se registre allí no es reconstruible. Es el mismo límite que
`PR-1` aborda desde el lado de la autorización, y es la razón por la que `PR-1`
sí es prerrequisito y `Durable Execution` no.

### 4.4 interruption / resume — `ALREADY_SOLVED`

**Problema.** Interrumpir y continuar sin corromper historia ni duplicar trabajo.

**Mecanismo externo.** `microbots` no lo tiene (EXTERNAL_CODE, P2). ACI lo tiene
para ingesta (replay con leases, P4). `agent-framework` lo tiene para workflows
(`Workflow.run(checkpoint_id=…, responses=…)`, P3). `prompty` (P1) modela la
cancelación como **control de runtime** (`core/cancellation.py`) y su contrato
incluye `resumeSameIteration`; es la única fuente con cancelación nombrada en el
camino de ejecución. Ninguna de las cinco ofrece **abort del orquestador en
vuelo**.

**Equivalente actual.** Dos mecanismos complementarios y **declarados**:

- Protocol: iteración parcial; reanudación desde el «last intact artifact»;
  si el estado productor tiene un gate de salida pendiente, se re-ejecuta el gate
  en ese estado; la base de reanudación se registra en `SESSION_LOG.md`
  (`PROTOCOL_BOUNDARIES.md:35-52`). El «intacto» está definido
  operacionalmente (existencia, bloques parseables, secciones requeridas, `PASS`
  registrado) — no es una impresión.
- DEV: reinicio = re-observación; el journal es append-only y una línea
  ilegible se declara `GAP` en lugar de descartarse
  (`store.py:45-71,212-242`).

**Diferencia.** De implementación y de vocabulario; no de garantía. El Protocol
reanuda un *artefacto*; el host DEV reanuda una *derivación*. Ambos preservan
«lo ya producido no se regenera retroactivamente».

**Garantía.** Continuidad, ya poseída.

**Carencia real identificada.** No existe **cancelación/abort del host en vuelo**:
el bucle sólo termina por derivación terminal, stop condition o límite de
iteraciones. No es un defecto del modelo —la autoridad de abortar un Change es
humana (`.agents/policies/authority.md`; `supervised-autonomous-execution.md:§8`)
y el host no la ejerce— pero conviene registrarlo: un stop externo (matar el
proceso) deja evidencia parcial, y la recuperación depende de re-observar, no de
un estado consistente garantizado. Se clasifica `POST_AUTONOMY` como *ergonomía
operativa*; no es prerrequisito.

**Impacto sobre autonomía.** Recuperación.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `PROTOCOL` (procedimiento) + `DEV` (realización).

**Evidencia.** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:35-52`;
`.agents/policies/autonomous-orchestration.md:§9`;
`runtime/orchestrator/store.py:45-71,212-242`;
`tests/test_autonomous_orchestrator.py:970-1006`.

### 4.5 idempotent y race-safe execution — `ALREADY_SOLVED`

**Problema.** Repetir una operación no debe duplicar su efecto; dos ejecuciones
simultáneas no deben corromper el mismo artefacto.

**Mecanismo externo.** `prompty` (P1) es el caso más instructivo: la regla de
no-duplicación de efectos ya comprometidos existe como **obligación documentada
del contrato de checkpoint** («A resumed run rebuilt from a checkpoint MUST NOT
duplicate a model or tool effect that the checkpoint already records as
committed»), y el runtime Python **no la implementa** porque no persiste
checkpoints. Es una obligación escrita sin mecanismo que la haga cumplir.
`microbots` (P2) reintenta la *respuesta del modelo* hasta `max_retries=3` con un
mensaje correctivo, pero no tiene idempotencia ni deduplicación. MACAE (P5):
`NOT_FOUND` para idempotency keys, deduplicación de requests, ETags o escrituras
condicionales; su coordinación es una cancelación de `asyncio.Task` por usuario
(last-write-wins) y un lock. ACI (P4) tiene una `EventIdempotencyCache` y
receipts con claves `UNIQUE` para ingesta.

**Equivalente actual.**

- **Idempotencia de registros de gobernanza:** `append_marked_block` es
  marker-guarded («a second call is a no-op»), `set_status` es idempotente, y la
  revalidación informa «A2 already recorded for this state (idempotent)»
  (`governance.py:77-88`; `host.py:813-817`).
- **Escritura atómica:** temp file en el mismo directorio + `os.replace`
  (`store.py:101-119`), de modo que un lector nunca observa un artefacto a medio
  escribir.
- **Identidad de contenido como discriminador:** repetir una validación sobre
  contenido sin cambios no produce un anchor nuevo (`anchor_stale` es falso).
- **Concurrencia:** hoy no hay ejecución concurrente, así que no hay carrera que
  resolver. El protocolo **declara** el modo single-instance como riesgo con
  mitigaciones obligatorias (`orchestrator.md:§5`;
  `METRICS.md:session_risk`), y el gate de conciliación bidireccional
  `state.json ↔ HARNESS_REPORT` detecta registros divergentes.

**Diferencia.** De garantía, y favorable: ARgentOS produce idempotencia **por
identidad y por estructura**, no por claves de deduplicación ni por locks. No hay
diferencia arquitectónica relevante.

**Garantía.** Idempotencia y aislamiento: ya poseídas para el dominio en uso.

**Límite declarado.** No hay coordinación distribuida (locks, leases, ETags)
porque no hay procesos concurrentes. Si la Etapa B habilitara multi-worker
concurrente sobre el mismo Change, la pregunta «¿quién escribe el anchor?»
reaparecería. Ver §9 (`REQUIRES_EVIDENCE`) y §4.7.

**Impacto sobre autonomía.** Persistencia y gobernanza.

**Prerrequisito.** `PREREQUISITE = NO` **mientras la ejecución sea secuencial**
(que es el modelo actual y el que la Etapa B declara candidato, no comprometido).

**Dominio.** `DEV`.

**Evidencia.** `runtime/orchestrator/governance.py:77-88`;
`runtime/orchestrator/store.py:101-119`;
`runtime/orchestrator/host.py:813-817`;
`tests/test_autonomous_orchestrator.py:1009-1029`;
`protocol/.agents/orchestrators/core/roles/orchestrator.md:§5`;
`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` (P3, conciliación de timestamps).

### 4.6 Execution Graph — `NOT_VALUABLE_FOR_ARGENTOS`

**Problema.** Representar dependencias entre trabajos para poder ejecutarlos en
un orden válido, en paralelo cuando son independientes, y detectar ciclos.

**Mecanismo externo.** `agent-framework` ofrece workflows con nodos, ejecutores
y aristas (EXTERNAL_CODE, `P3`). **MACAE, que lo consume para construir un
sistema multi-agente real, no usa un grafo**: su descomposición es una **lista
plana ordenada** (`MStep{agent,action}` / `MPlan.steps`, `models/plan_models.py:23-41`)
sin campo de dependencia ni de arista, y la completitud se exige **por texto de
prompt** (`plan_review_helpers.py:224-249`), no por un planificador. Esto es
evidencia externa directa de que la existencia de un grafo en el framework no
implica que el sistema lo necesite.

**Equivalente actual.** Las dependencias no se representan porque **se derivan**.
`derive_next_action` recorre el estado observado en un orden determinista y
documentado (autorización → criterios de entrada → pending blocking → findings →
FAIL → gates → anchor → validación → delegación → revalidación → checkpoint →
cierre) y devuelve exactamente una acción (`derivation.py:195-466`). Cada paso
tiene su precondición escrita: no se valida antes de implementar (se derivaría
evidencia sobre un estado que la implementación va a cambiar,
`runtime/README.md:419-427`); no se registra un checkpoint antes del anchor; no
se cierra con findings abiertos (`host.py:1021-1031`).

**Las cuatro preguntas del Plan, respondidas con evidencia:**

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿El modelo secuencial es suficiente? | **Sí, hoy**: el host conduce un Change, una acción por iteración, y satisface el bucle completo de la Etapa B | `host.py:898-971`; `tests/test_autonomous_orchestrator.py` (**31 tests** en el archivo) y la suite completa verde en el baseline `dev @ 820da21` (**1186 passed**, `docs/plans/149-argentos-capability-and-autonomy-roadmap.md:172`) |
| ¿Hay trabajo concurrente real que soportar? | **No evidenciado**. Todo el trabajo autorizado de un Change es secuencial por construcción (una delegación por iteración) | `host.py:906-954` |
| ¿La dependencia entre tareas puede derivarse actualmente? | **Sí**: la precondición de cada acción es una condición sobre el estado observado, y la derivación está ordenada y testeada | `derivation.py:195-466`; `tests/test_autonomous_orchestrator.py` |
| ¿Un grafo aportaría una garantía concreta? | **No identificada.** No hay ciclo que detectar (la autoridad precede, el cierre sucede), no hay paralelismo que planificar, y la verificación no depende del orden representado | `derivation.py`; `supervised-autonomous-execution.md:§2` |

**Diferencia.** Inexistente en garantía; **un grafo introduciría** una segunda
representación de relaciones que ya son legibles desde los artefactos y desde la
derivación — precisamente lo que `ROADMAP.md:Qué no es una entrada de este
roadmap` prohíbe («nuevas state machines», «nuevas entidades globales»).

**Garantía.** Ninguna nueva. Un grafo no verifica, no autoriza y no evidencia.

**Impacto sobre autonomía.** Ninguna parte relevante **del modelo actual**. Si en
el futuro la Etapa B habilitara delegación concurrente de ramas independientes
(que el modelo ya contempla conceptualmente: «Blocked branches do not block
independent work», `supervised-autonomous-execution.md:§6.1`), la pregunta
volvería — pero incluso entonces bastaría un conjunto ordenado de ramas
independientes, no un grafo general.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `UNKNOWN` — no se identificó dominio porque no se identificó
necesidad. Si algún día se justificara, sería `DEV` (representación de ejecución),
nunca `PROTOCOL`.

**Evidencia.** `runtime/orchestrator/derivation.py:195-466`;
`runtime/orchestrator/host.py:898-971`;
`.agents/policies/supervised-autonomous-execution.md:§2,§6.1`;
`ROADMAP.md:Qué no es una entrada de este roadmap`;
EXTERNAL_CODE: MACAE `src/backend/models/plan_models.py:23-41`,
`src/backend/orchestration/plan_review_helpers.py:224-249`.

### 4.7 controlled concurrency — `POST_AUTONOMY`

**Problema.** Ejecutar varios trabajos a la vez sin que compartan estado de forma
insegura, y sin que un trabajo bloquee a los demás.

**Mecanismo externo.** `microbots` (P2) **evita** la concurrencia por diseño: el
sub-agente comparte el mismo contenedor y corre de forma síncrona; el prompt
ordena «run only ONE `microbot_sub` command at a time»; las iteraciones del hijo
se cargan al padre para acotar el presupuesto compartido. MACAE (P5) orquesta
in-process, con `asyncio`, sin paralelismo de agentes. `prompty` (P1) sólo
paraleliza el dispatch de tools dentro de una respuesta, con
`parallel_tool_calls=false` por defecto. `agent-framework` (P3) es la única fuente
con concurrencia real dentro de un workflow (supersteps, edge runners,
`asyncio.gather`), y es **intra-workflow**, no coordinación de agentes
independientes sobre el mismo artefacto.

**Equivalente actual.** ARgentOS tiene el modo de ejecución declarado
(`subagent | single-instance`) con sus mitigaciones obligatorias cuando no hay
subagentes, y el riesgo se registra como evento de sesión
(`orchestrator.md:§5`; `METRICS.md:session_risk`). El host DEV es secuencial.

**Diferencia.** De implementación: ninguno de los sistemas comparados demuestra
concurrencia segura **sobre un mismo artefacto**; todos la evitan o la confinan.
ARgentOS la evita **declarando el riesgo**, lo que es estrictamente mejor que
evitarla sin declararlo.

**Garantía.** Concurrencia segura: **no demostrada en ningún sistema de la
comparación**. No hay garantía nueva que extraer.

**Impacto sobre autonomía.** No afecta la siguiente etapa: la Etapa B busca
profundidad (provider real, ejecución multi-step, presupuestos), no paralelismo.

**Prerrequisito.** `PREREQUISITE = NO`. La autonomía no queda incompleta por
ejecutar de a un trabajo.

**Dominio.** `DEV`.

**Evidencia.** `protocol/.agents/orchestrators/core/roles/orchestrator.md:§5,§334`;
`protocol/.agents/contracts/METRICS.md:session_risk`;
`protocol/.agents/contracts/SESSION_LOG.md:65`;
EXTERNAL_CODE: `microbots` `tools/tool_definitions/microbot_sub_agent.py:75-125`,
`bot/AgentBoss.py:70-88`.

### 4.8 Execution Budgets — `ARCHITECTURAL_PREREQUISITE` (PR-2)

**Problema.** Una ejecución desatendida necesita una frontera de **recurso**, no
sólo de **progreso**. Las dos son distintas: *no progreso* significa «el bucle
está girando»; *presupuesto agotado* significa «el trabajo todavía progresa pero
ya consumió más de lo autorizado». Un guarda de no-progreso no detiene el
segundo caso.

**Mecanismo externo — y es el hallazgo más consistente de la comparación.**

| Sistema | Límites verificados en código |
|---|---|
| `microbots` (P2) | `max_iterations=20`, `timeout_in_seconds=200`, `max_retries=3` (validación de salida del LLM), `max_rounds=5`, `AgentBoss` 50/1200, sub-agente 25/300, eval 40/1800, training 200/3600, `Environment.execute` 300 s. **Presupuesto compartido**: las iteraciones del sub-agente se suman al padre (`parent_bot.iteration_count += sub_bot.iteration_count`). **Sin** tokens/costo, con `TODO` explícito en `MicroBot.py:182`: «Replace iteration_count and max_iterations with cost management» |
| MACAE (P5) | `max_rounds=30` (→ `max_round_count`), `max_stall_count=5` hard-coded, timeouts de aprobación/clarificación `300.0 s`, HTTP 30/180 s. **Sin** budget de tokens ni de costo |
| `prompty` (P1) | `context_budget` en **caracteres** para recorte de ventana (`spec/spec.md:3330`, con `summary_budget = min(5000, budget*0.05)`), `MAX_ITERATIONS=10`, `MAX_LLM_RETRIES=3`, `max_attempts` en `RetryPolicyRequest`, `maxOutputTokens` por modelo, `ResumeContext.maxIterations`/`maxModelAttempts`. **Sin** budget de costo/divisa y **sin** budget de wall-clock |
| `agent-framework` (P3) | **Ninguno** en el camino de ejecución core: sin timeout en `SupportsAgentRun.run` ni en `Workflow.run`, sin budget de token/costo (grep negativo sobre `_workflows/*.py`). Sólo un `RetryMiddleware` de **ejemplo** (usuario) y `TokenUsage` contable por atributos OTel — **contabilidad, no presupuesto** |

Cuatro de los cinco sistemas externos tienen algún límite de bucle o de tiempo, y
todos lo tratan como **constante de construcción**: **ninguno** declara un
presupuesto autorizado por el trabajo. Tres de ellos nombran el hueco de manera
explícita: un `TODO` de gestión de costo (`microbots`), ausencia total de
presupuesto de costo y de wall-clock (`prompty`) y ausencia total en el camino de
ejecución core con sólo contabilidad de uso (`agent-framework`).

**Equivalente actual.**

- **Límite de iteraciones del bucle:** `DEFAULT_MAX_ITERATIONS = 8`,
  configurable por CLI. Es un techo *del bucle del host*, no un presupuesto del
  Change.
- **No-progress guard:** compara el *fingerprint* de hechos de gobernanza; si la
  misma acción se deriva dos veces sin cambios, `STOP_NO_PROGRESS`
  (`host.py:920-940`; `observation.py:688-709`). Garantía de **progreso**.
- **Pasos del razonamiento local del worker:** `DEFAULT_MAX_STEPS = 24`; al
  alcanzarlo el resultado es `INCOMPLETE` y la señal es `GAP`, nunca `VALID`
  (`agent_worker.py:85-107`).
- **Context Budget:** es una frontera **semántica** de composición de contexto,
  declarada finita y positiva, y **medida** (declared/consumed). El estándar es
  explícito: no trunca ni bloquea en la delegación
  (`BUDGET_MATERIALIZATION.md:50-62`), y separa tres magnitudes que no deben
  confundirse: semantic budget, costo físico/provider/storage, y costo de
  materialización del prompt (`BUDGET_MATERIALIZATION.md:77-82`).

**La carencia concreta.** No existe un presupuesto de ejecución **declarado por
el Change autorizado** que sea (a) verificable, (b) acumulativo, (c) persistente
a través de reinicios, y (d) revierta en un `STOP_*` propio cuando se agota. Los
límites actuales son constantes del host o del worker, no un techo autorizado; y
el único acumulador real (`max_iterations`) se reinicia con cada proceso —la
numeración de iteraciones continúa, pero **el consumo no se cuenta** a través de
reinicios (`host.py:900-906`).

**Garantía que produce.** **Control de recursos** y **garantía de terminación por
recurso**. Sin ella, una autonomía desatendida sólo puede prometer «termina si
deja de progresar» — no «termina dentro de lo autorizado». Y el costo no es
teórico: es la magnitud que `microbots` deja como `TODO`, que MACAE y `prompty`
no tienen, y de la que `agent-framework` sólo tiene **contabilidad** (`TokenUsage`
por OTel) sin ningún presupuesto en el camino de ejecución core.

**Impacto sobre autonomía.** **Autonomía desatendida** y **operación**. Es la
frontera que separa «el host conduce un Change de un solo commit» de «el host
recibe un objetivo suficientemente amplio y lo ejecuta de forma autónoma»
(`ROADMAP.md:Etapa B`), porque es lo único que acota el segundo.

**Prerrequisito.** `PREREQUISITE = YES`. La autonomía quedaría
arquitectónicamente **incompleta**: sin frontera de recurso, la única garantía de
terminación es la de progreso, y el sistema no puede declarar ni verificar
«cuánto está autorizado a gastar». El modelo de frontera ya existe (SAE:
`autonomy ⊆ scope ∩ authority`) y **le falta el eje de recurso**: hoy no hay
ningún lugar del envolvente donde escribir «y como máximo N iteraciones, T
segundos, R reintentos, D delegaciones, C llamadas al modelo».

**Distinción de tipos de control (según el Plan).**

| Tipo | ¿Existe? | Dónde |
|---|---|---|
| **Control de seguridad** | **Sí** | Scope/Authority (SAE), admisión de efectos (Protocol, no consumida — `PR-1`) |
| **Control económico** | **Parcial** | Context Budget declarado/consumido (semántico, medido, no bloqueante); **sin** costo de provider/modelo (RFC-74 sin tocar; el repo no invoca providers) |
| **Control operativo** | **Sí** | `CommandWorker` timeouts, clasificación de señales, `GAP` vs `FAIL` |
| **Control de autonomía** | **Parcial** | `max_iterations` (constante del host), no-progress guard, `max_steps` del worker; **sin** acumulación persistente ni techo autorizado |

**Dominio.** `DEV`. El Context Budget es `PROTOCOL` (y ya existe); el
presupuesto de ejecución del host es una frontera del **ejecutor DEV**, no del
payload. Deliberadamente **no** debe convertirse en una entidad del Protocol: el
Protocol no conoce al host DEV (`docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).

**Evidencia.** `runtime/orchestrator/host.py:105,898-954`;
`runtime/orchestrator/derivation.py:469-489`;
`runtime/orchestrator/observation.py:688-709`;
`runtime/orchestrator/agent_worker.py:79-107,296`;
`runtime/orchestrator/authority.py`;
`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:25,50-62,77-82`;
`protocol/.agents/standards/context/CONTEXT.md:38-57`;
`tests/test_autonomous_orchestrator.py:1009-1034`;
`tests/test_measure_context_budget.py`;
EXTERNAL_CODE: `microbots` `src/microbots/MicroBot.py:180-182,227-228`,
`bot/AgentBoss.py:108-109`, `tools/tool_definitions/microbot_sub_agent.py:75-76`;
MACAE `src/backend/orchestration/connection_config.py:25-36`,
`orchestration_manager.py:189-190`.

**Nota.** `PR-2` no pide un mecanismo nuevo en el Protocol ni una entidad. Pide
que el envolvente de autonomía —que ya se **deriva** de declaraciones que el Plan
aprobado ya posee— incluya los techos de recurso que el Plan puede declarar hoy
en su `## Delegación agentiva`. Es la lectura de `PR-1` y `PR-2` como
`AUTONOMY_IMPLEMENTATION` la que decide si van antes o dentro de la Etapa B; ver
§6.

### 4.9 Observability / Execution Intelligence — `ALREADY_SOLVED`

**Problema.** Poder responder, después y sin memoria de conversación, qué se
observó, qué se derivó, qué se autorizó, qué se ejecutó, qué se verificó, qué se
corrigió y por qué se continuó o se detuvo.

**Mecanismo externo.** `agent-framework` (P3): OpenTelemetry de primera clase con
spans `workflow.build`/`workflow.run`/`executor.process`/`edge_group.process`/
`message.send` y atributos de convención GenAI, más un conjunto de atributos
experimentales. `prompty` (P1): tracing **normado en la especificación** con tres
backends — `.tracy` (MUST), Console (SHOULD) y OpenTelemetry `gen_ai.*` (SHOULD) —
y redacción de datos sensibles. MACAE (P5): `configure_azure_monitor` +
`FastAPIInstrumentor` + `track_event` + tracer OTLP standalone, con guard de CI
(`telemetry-template-check.yml`). ACI (P4): plataforma de telemetría completa con
grafo en Neo4j, append-log durable por sesión y receipts SQLite. `microbots` (P2):
logging plano vía `FileHandler`, sin OTel, sin métricas, con reconstrucción de
pasos **post-hoc por parseo de logs** (`utils/multi_agent_log_parser.py:31-76`).

Cuatro de las cinco fuentes tienen telemetría, y esto es informativo: la
telemetría es la capacidad **mejor cubierta** del conjunto externo y, a la vez,
**ninguna** de esas cuatro la usa para decidir algo que ARgentOS no decida sin
ella.

**Equivalente actual.** ARgentOS no tiene backend de telemetría y no lo necesita
para la garantía que busca: tiene **reconstruibilidad**. Cada iteración se
persiste con 16+ campos (estado observado, acción derivada, autoridad, delegación,
resultado, señales de gate y validación, stop y su razón), el journal es
append-only, las líneas ilegibles se **declaran** `GAP` y hay un comando de
reconstrucción que no usa memoria de sesión (`host.py:376-443,1077-1128`;
`store.py:212-252`). A nivel Protocol hay catálogo de eventos con clase de
verifiabilidad (`Derived`/`Recorded`/`Verified`), conciliación bidireccional
`state.json ↔ HARNESS_REPORT`, y un catálogo cerrado de garantías clasificadas por
quién las verifica (`harness/INDEX.md:81-118`).

**Diferencia.** **De observabilidad**, y es una elección explícita y documentada:
ARgentOS no tiene telemetría en vivo ni consultas agregadas sobre backend; tiene
evidencia persistida y verificable. `microbots` demuestra el costo de no tenerla
(reconstruye por regex). MACAE/ACI demuestran que la telemetría agrega valor de
**operación**, no de **corrección**: ninguno de los dos la usa para decidir más
que lo que ARgentOS decide.

**Garantía.** Trazabilidad: ya poseída. Lo que la telemetría de backend añadiría
es latencia de diagnóstico y agregación — valor operativo real, pero no una
garantía arquitectónica, y explícitamente fuera del alcance del MVP del runtime
(`runtime/README.md:124-125,443-445`).

**Impacto sobre autonomía.** Observación: cubierta por evidencia.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `DEV` (si algún día se añade) — nunca `PROTOCOL`: la telemetría de
ejecución es del runtime.

**Evidencia.** `runtime/orchestrator/host.py:376-443,1077-1153`;
`runtime/orchestrator/store.py:212-252`;
`protocol/.agents/contracts/METRICS.md`; `PROTOCOL_METRICS.md:188-219`;
`protocol/.agents/harness/INDEX.md:81-139`;
`tools/aggregate_metrics.py`; `tools/audit_gates.py`;
EXTERNAL_CODE: MACAE `src/backend/app.py:101-113`,
`common/utils/event_utils.py:7-30`; ACI `registry.py:386`;
`microbots` `utils/multi_agent_log_parser.py:31-76`.

### 4.10 Evaluation — `POST_AUTONOMY`

**Problema.** Determinar si una salida es *buena*, no sólo si *existe* y *cumple
su forma*. Y, más allá, si **empeoró** respecto de una salida anterior.

**Mecanismo externo — la comparación es pobre, y eso es informativo.**
`agent-framework` (P3) tiene la capa de evaluación **más completa** de las cinco
fuentes y está **en el core**, no en un paquete aparte: `Evaluator` Protocol,
`LocalEvaluator`, `evaluate_agent(...)`, `evaluate_workflow(...)` (que produce
sub-resultados por agente de un workflow), `EvalItem` con `expected_output` **y
`expected_tool_calls`** (evaluación de corrección de tool calls), `RubricScore`,
`EvalResults` y `EvalNotPassedError`. **Pero todo símbolo está decorado
`@experimental(feature_id=ExperimentalFeature.EVALS)`**
(`_evaluation.py`; `_feature_stage.py:43-88`): la capacidad existe y su propio
framework declara que puede cambiar o desaparecer sin aviso.

`microbots` (P2) es el único con un harness de evaluación **propio y en uso**:
`auto_memory` corre un bucle train↔eval con `EvalOutcome` serializado a
`rounds/round_N/eval/result.json`, feedback de fallo inyectado como material de
entrenamiento, y un backend SWE-bench para el veredicto externo. Evalúa
**ejecuciones contra un benchmark**, no la calidad de una salida respecto de una
anterior.

`prompty` (P1): **NOT_FOUND** — sin graders, sin CLI, sin harness; su
documentación delega la evaluación al framework de test del usuario
(`how-to/testing-prompts.mdx`). MACAE (P5) **no tiene** harness en el repositorio:
la afirmación de evaluación offline de groundedness/harm existe sólo en
`docs/TRANSPARENCY_FAQ.md:12` (**EXTERNAL_DOC**, sin artefacto). ACI (P4) no
evalúa calidad de contexto (grep negativo sobre
`benchmark|accuracy|recall|dataset`).

**Equivalente actual.** ARgentOS ya tiene una capa de evaluación, y no es
telemetría:

| Nivel | Mecanismo | Naturaleza |
|---|---|---|
| Verificación de forma | `H01`–`H07`, `gate_validator`, secciones requeridas, EARS | **Verifiable / Mechanically enforced** |
| Verificación de contenido | `## Acceptance Criteria Evaluation` en `VERIFICATION_REPORT.md` | juicio con evidencia |
| Calidad por rúbrica | `RUBRICS.md` (escala `INSUFFICIENT`/`MEETS`/`EXCEEDS`, criterio crítico ✅), `reviewer` (pre-transición), `verifier` (fase 07), `rubric-checker` | juicio con evidencia; **H06 sólo valida que la sección exista, «does not judge quality»** (`RUBRICS.md:7`) |
| Evaluación adversarial | `adversarial-deliberation`: dos pasadas atribuidas con compromiso previo a la revelación, evaluación comparativa por criterio, síntesis con desacuerdo preservado, veredicto advisory | juicio estructurado con evidencia |
| Cumplimiento de política | gates + `audit_gates` (reproducibilidad de ítems `[gate]`) | Verified (best-effort) |
| Métricas | catálogo de eventos, agregación advisory | Recorded / Derived / Verified |

`HARNESS_REPORT.md` declara de sí mismo: «It is self-reported: it records the
Orchestrator's judgment … it is not independently verified evidence»
(`HARNESS_REPORT.md:25`). Y el catálogo de garantías declara que «verification
independence» es `External-actor-dependent` y en single-instance es **una
atestación** (`harness/INDEX.md:111`).

**Diferencia — qué falta exactamente.** No falta *evaluación*: falta
**evaluación comparativa / detección de regresión de calidad**. Verificado:

- ARgentOS compara **identidad de contenido** (`delta scoped identity`) para
  decidir si una validación quedó *stale* — es decir, detecta que el contenido
  cambió, no que **empeoró**.
- No existe un mecanismo que, ante una nueva salida, la compare con una salida
  previa ya evaluada bajo la misma rúbrica y produzca una señal de regresión.
- La evaluación por rúbrica existe pero es **por artefacto y por vez**; no hay
  serie histórica de puntajes ni umbral que dispare algo.

La evidencia externa **no ofrece un modelo a tomar**: la única capa de evaluación
con `RubricScore` y evaluación de tool calls (`agent-framework`) está marcada
`@experimental` por su propio autor; el único harness en uso (`microbots`) evalúa
contra un benchmark externo, no contra la salida anterior del mismo sistema. La
comparación no aporta, entonces, ni un mecanismo ni una garantía que ARgentOS
pueda adoptar con justificación.

**Garantía que produciría.** Evaluación comparativa: detectar degradación de
calidad entre iteraciones/versiones del mismo artefacto.

**Impacto sobre autonomía.** **No afecta la próxima etapa.** La Etapa B busca
cerrar fronteras de *ejecución* (provider real, resultados, recuperación,
presupuestos, terminación). Una capa de evaluación comparativa es valiosa
*después*: cuando el sistema produzca muchas salidas autónomas, la pregunta «¿esta
salida es peor que la anterior?» se vuelve frecuente. Hoy el volumen no la
justifica y el juicio humano con rúbrica la cubre.

**Prerrequisito.** `PREREQUISITE = NO`. La autonomía no queda insegura sin ella:
podría producir trabajo de calidad estable sin saber si mejoró, y la verificación
de contenido y la rúbrica siguen aplicándose por artefacto.

**Dominio.** `BOTH` — rúbricas y criterios de aceptación son `PROTOCOL` (ya
existen); una serie histórica o un umbral serían `DEV` (y hoy no existen).

**Evidencia.** `protocol/.agents/standards/quality/RUBRICS.md:7,45,73,88-95`;
`protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:28,87,384,411-455`;
`protocol/.agents/roles/verifier.md:13,32,43-45`;
`protocol/.agents/roles/reviewer.md`;
`protocol/.agents/skills/adversarial-deliberation/SKILL.md:3,10,31,155-164`;
`protocol/.agents/contracts/HARNESS_REPORT.md:25`;
`protocol/.agents/harness/INDEX.md:111`;
`tools/audit_gates.py`;
`runtime/orchestrator/observation.py:657-673` (`anchor_stale`);
EXTERNAL_CODE: `microbots` `src/microbots/auto_memory/orchestrator.py:96,155`;
EXTERNAL_DOC: MACAE `docs/TRANSPARENCY_FAQ.md:12` (claim sin artefacto).

### 4.11 Semantic Context — `ALREADY_SOLVED`

**Problema.** Que el contexto entregado a un worker sea identificable,
reproducible, invalidable por causa semántica y reutilizable sin cambiar su
significado.

**Mecanismo externo — y aquí dos premisas de partida también fallaron.**
`amplifier-context-intelligence` (P4) **no es** un sistema de contexto semántico:
es una plataforma de telemetría y observabilidad con grafo en Neo4j
(`README.md:3`), sin distinción stable/dynamic, sin identidad/versionado de
contexto, sin scoring de relevancia (grep negativo sobre
`embedding|vector store|cosine|similarity|semantic search`), sin integración de
prompt cache (grep negativo sobre
`prompt_cache|cache_breakpoint|stable_prefix|cache_control`) y sin evaluación de
calidad de contexto. Su identidad de nodo es
`f"{session_id}__{safe_event}__{epoch_ms}"` con desambiguador
(`utils.py:94-131`) — identidad **de evento**, no de contexto. Su durabilidad es
de ingesta, no de ejecución.

`prompty` (P1) aporta portabilidad de la plantilla (`.prompty` = YAML
frontmatter + markdown, con `inputs`/`outputs` declarados) pero **no** un modelo
de contexto: su `metadata` es un diccionario libre sin semántica, y **no existe
versionado de prompt** — ni campo de versión, ni semver, ni API de revisión. Su
única noción cercana a "estable" es `stablePrefixMessages` **dentro del contrato
de checkpoint**, que es una lista de mensajes a reutilizar, no una clasificación
semántica con regla de elegibilidad.

`agent-framework` (P3) es el único con una abstracción comparable, y es
**distinta en naturaleza**: `ContextProvider` (`_sessions.py:754`) con hooks
`before_run`/`after_run`, estado por provider guardado en `AgentSession.state`, y
subclases `HistoryProvider`/`InMemoryHistoryProvider`/`FileHistoryProvider`/
`VectorStoreHistoryProvider`/`CompactionProvider`/`SkillsProvider`. Eso es
**memoria y estado del agente** (un pipeline de hooks de ejecución), no
**identidad semántica de contexto**: no hay identidad de segmento, ni versión
semántica, ni invariante de reproducibilidad de la materialización. La
`SESSION_STORE` que lo persiste está además marcada `@experimental`
(`_feature_stage.py:65`).

**Equivalente actual.** ARgentOS tiene el modelo completo y con invariantes:

- **Segmentos** Core/Project/Worker como dominios semánticos de un único modelo
  de persistencia (`CONTEXT.md:264-278`).
- **Identidad:** `SegmentContentIdentity` = SHA-256 del contenido canónico;
  `SegmentIdentity = {semantic_version, content_identity, namespace}` — y la
  norma es explícita en que «`SegmentIdentity` is never reduced to a content
  hash» (`CONTEXT.md:288-301`).
- **SemanticContextIdentity** derivada de la composición, **invariante a la
  materialización**, independiente de provider, modelo, serialización, orden y
  caché (`CONTEXT.md:303-322`).
- **Clasificación Stable/Dynamic**, **prefijo estable** con regla de elegibilidad
  de tres condiciones, bootstrap declarado vacío, y frontera explícita con las
  políticas de composición (`CONTEXT.md:354-378`).
- **Materialización canónica**: variante + serialización + orden, con
  `I-MAT-001` («same semantic identity + same materialization identity ⇒
  byte-identical canonical payload») verificable
  (`runtime/README.md:50-125`; `runtime/toolcalls/canonical.py`).
- **Invalidación semántica** sólo por cambio de identidad; TTL y freshness
  gobiernan lifecycle, nunca correctness (`CONTEXT.md:339-352`).
- **Prompt Cache** con las tres dimensiones de invalidación no conflacionables
  (semántica, materialización, provider) y admisión como política sin umbrales
  (`runtime/toolcalls/cache_coordinator.py`; RFC-72 §9-11).

**Las cuatro preguntas del Plan:**

1. **¿Ya resuelto?** **Sí**, y con invariante verificable.
2. **¿Extensión del modelo existente?** No se identificó extensión que el modelo
   no exprese. Lo más cercano es la **memoria/estado del agente** de
   `agent-framework` (`ContextProvider` + session state), que es una necesidad
   **distinta** —de ejecución, no de contexto— y que ARgentOS cubre en otro lugar
   (el journal y el store de evidencia). `stablePrefixMessages` de `prompty` y el
   `stable_prefix_bytes` de ARgentOS **no** son equivalentes: el primero es una
   lista de mensajes en un checkpoint, el segundo una región byte-invariante con
   regla de elegibilidad e invariante `I-MAT-001`.
3. **¿Necesidad diferente?** La única necesidad distinta que aparece en las
   fuentes es **observabilidad histórica de sesiones** (el grafo de ACI) y
   **memoria persistente del agente** (los context providers de P3). La primera
   es §4.9 (Observability); la segunda no tiene demanda declarada en el modelo de
   ARgentOS, donde la memoria del worker es explícitamente *worker-local* y no
   persistida como estado (`autonomous-orchestration.md:§11.1`).
4. **¿Abstracción innecesaria?** Añadir un modelo de contexto paralelo (p. ej.
   adoptar la identidad de evento de ACI) sería exactamente eso: una **segunda
   arquitectura de contexto**, contra la instrucción explícita del Plan y contra
   la regla de una fuente de verdad por concepto.

**Diferencia.** De garantía: ARgentOS tiene reproducibilidad de la materialización
(`I-MAT-001`) que **ninguna** de las fuentes externas inspeccionadas acredita.

**Garantía.** Reproducibilidad, ya poseída.

**Impacto sobre autonomía.** Contexto: cubierto. El Prompt Cache es
intra-sesión por construcción (`runtime/README.md:110-112`), lo que es una
declaración honesta, no una carencia.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `PROTOCOL` (modelo de contexto) + `DEV`/runtime (materialización).

**Evidencia.** `protocol/.agents/standards/context/CONTEXT.md:230-378`;
`BUDGET_MATERIALIZATION.md:64-82`;
`runtime/README.md:50-155`; `runtime/toolcalls/canonical.py`;
`runtime/toolcalls/identity.py`; `runtime/toolcalls/segment_resolution.py`;
`runtime/toolcalls/cache_coordinator.py`; `tests/test_canonical_materialization.py`;
`tests/test_canonical_materialization_v2.py`; `tests/test_prompt_cache_dogfood.py`;
EXTERNAL_CODE: ACI `README.md:3`, `context_intelligence_server/utils.py:94-131`,
`handlers/data_layer_2/iteration.py:151-161`.

### 4.12 desired-state reconciliation — `ALREADY_SOLVED`

**Problema.** Detectar que lo declarado y lo real divergen, y decidir qué hacer
sin reconciliar por reinterpretación.

**Mecanismo externo.** MACAE mantiene el estado de orquestación en dicts de
módulo (`connection_config.py:25-36`) y persiste planes/mensajes en Cosmos a
nivel de aplicación; no hay reconciliación de un estado deseado contra un estado
observado (EXTERNAL_CODE, P5). `prompty` (P1) tiene `reconciliationRequired` como
**campo del contrato de checkpoint** — es decir, **nombra** la necesidad de
reconciliar al reanudar — pero el runtime Python no lo realiza: es un campo
declarado, no un mecanismo. `agent-framework` (P3) reconcilia topología al
restaurar un checkpoint mediante `graph_signature_hash`, que es una verificación
de **compatibilidad de grafo**, no de estado deseado.

**Equivalente actual.** ARgentOS reconcilia en los dominios donde tiene
declaraciones verificables:

- **Anchor ↔ contenido:** `anchor_stale` compara la identidad de contenido
  validada contra la actual, y una identidad actual desconocida **no** se lee
  como fresca: es `GAP` declarado (`observation.py:657-673`).
- **Checkpoint ↔ anchor:** `consistency_pass` y `closure_tree ==
  state_identity` son parte de la condición derivada `Closed`
  (`host.py:1011-1039`).
- **Checkpoint de autorización:** la declaración bajo la que corre una ejecución
  se proyecta, se registra y se compara en cada iteración; una reescritura
  posterior es divergencia, no aclaración
  (`autonomy.py:authorization_projection`/`authorization_drift`;
  `supervised-autonomous-execution.md:§1.2`).
- **`state.json` ↔ `HARNESS_REPORT.md`:** conciliación bidireccional
  (`harness/INDEX.md:104,130`; `docs/adr/07-execution-record.md`).
- **Obligaciones de estado ≠ autorizaciones de escritura:** una obligación cuyo
  artefacto está fuera del scope se registra `DEFERRED` con su pending decision y
  el artefacto **no se escribe** (`supervised-autonomous-execution.md:§1.1,§9`).
- **Placement:** `runtime/placement/` responde `PLACE` o `STOP`, nunca una
  conjetura; si la implementación y el contrato discrepan, gobierna el contrato y
  el defecto se corrige, **nunca se reconcilia reinterpretando el contrato**
  (`PC-75`).

**Diferencia.** De alcance, no de garantía: ARgentOS reconcilia **artefactos y
declaraciones de gobernanza** (que es lo que su modelo declara), no **recursos de
infraestructura** (que no administra). No falta un reconciliador general; falta
—si acaso— reconciliación de algo que no existe en el modelo.

**Garantía.** Verificabilidad y consistencia, ya poseídas en el dominio que
importa.

**Impacto sobre autonomía.** Gobernanza y cierre: cubiertos.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `DEV` + `PROTOCOL`.

**Evidencia.** `runtime/orchestrator/observation.py:651-709`;
`runtime/orchestrator/host.py:1011-1073`;
`runtime/orchestrator/autonomy.py:600-654`;
`.agents/policies/supervised-autonomous-execution.md:§1.1,§1.2,§9`;
`protocol/.agents/harness/INDEX.md:104,130`;
`docs/placement-contract.md:PC-75`;
`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` (P3);
EXTERNAL_CODE: MACAE `src/backend/orchestration/connection_config.py:25-36`.

### 4.13 execution state persistence — `ALREADY_SOLVED`

**Problema.** Que el estado necesario para continuar sobreviva a la muerte del
proceso.

**Mecanismo externo.** `agent-framework` (P3): `WorkflowCheckpoint` persistido con
`messages`, `state`, `pending_request_info_events`, `iteration_count` y linaje
`previous_checkpoint_id`; `CheckpointStorage` con implementación `File` y
escritura atómica. `prompty` (P1): contrato rico (`EngineCheckpoint`,
`ResumeContext`, `EventJournalWriter`, `ReplayJournalRecord`) con implementación
concreta **sólo en Java y en memoria**. ACI (P4): append-log por sesión + blobs +
receipts SQLite. `microbots` (P2): memoria markdown + `result.json` por ronda; el
estado del bucle no se persiste.

**Equivalente actual.** ARgentOS separa tres cosas que los frameworks externos
suelen conflacionar, y las separa **por diseño**:

| Qué se persiste | Dónde | Durabilidad |
|---|---|---|
| Evidencia de ejecución (delegaciones, worker results, journal, runs) | `.project/orchestrator/plan-<NNN>/` | **durable entre procesos, no versionada** (`store.py:11-16`) |
| Gobernanza del Change (status, anchor, checkpoint, notas, findings) | el artefacto del Plan | **versionada en Git** |
| Estado del **host** | **en ningún lugar, deliberadamente** | el host no tiene estado (`host.py:11-25`) |

La tercera fila es el punto. ARgentOS **elimina** la necesidad de persistir estado
de ejecución haciendo que la posición sea una función del repositorio. Un store
perdido es `GAP`, nunca un hecho positivo, y la recuperación **no depende** de que
el store esté intacto: primero reconstruye la vista desde el repositorio y *luego*
relee el store (`store.py:18-22`).

**Diferencia.** Arquitectónica y deliberada: persistir estado de ejecución sería
introducir una **segunda representación** de dónde está el trabajo. Es
exactamente lo que el baseline declara prohibido
(`autonomous-orchestration.md:§2`; `.agents/AGENTS.md:8`).

**Garantía.** Continuidad: ya poseída (por reconstrucción). La persistencia de
estado añadiría *fidelidad de reanudación de efectos no registrados*, que no
existen en el modelo actual.

**Límite declarado.** Un estado que no provenga de hechos observables del
repositorio no es reconstruible. Es el límite que `PR-1` aborda desde la
autorización (registrar el efecto autorizado) y que reforzaría `PR-2` (registrar
el consumo).

**Impacto sobre autonomía.** Persistencia: cubierta.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `DEV`.

**Evidencia.** `runtime/orchestrator/store.py:1-22,101-119,212-296`;
`runtime/orchestrator/host.py:11-25,898-971`;
`.agents/policies/autonomous-orchestration.md:§8,§9`;
`tests/test_autonomous_orchestrator.py:970-1006`;
EXTERNAL_CODE: ACI `context_intelligence_server/recovery.py:25-67`;
`microbots` `src/microbots/auto_memory/orchestrator.py:96`.

### 4.14 failure recovery — `ALREADY_SOLVED`

**Problema.** Ante un fallo, decidir si se corrige, se reintenta, se escala o se
aborta — sin ocultar el fallo ni convertirlo en éxito.

**Mecanismo externo.** `microbots` (P2) repara en cuatro capas (salida inválida del
LLM, comando peligroso bloqueado, comando fallido realimentado, fallo de ronda
registrado) y **nunca aborta**; el `while` no tiene try/except, así que una
excepción de `llm.ask`/`execute` sale de `run()`. `prompty` (P1) declara
`RetryPolicyRequest`/`max_attempts` y `guardrails` como **controles de runtime**
(el propio spec aclara que no son campos de frontmatter). ACI (P4) introduce
dead-letter y replay con receipts y leases. `agent-framework` (P3) **no tiene**
política de reintento en el camino de ejecución core: el único `RetryMiddleware`
es un ejemplo que el usuario compone.

**Equivalente actual.** ARgentOS tiene una semántica de fallo **más fuerte**, que
es su rasgo más distintivo frente a las cuatro fuentes:

```text
GAP      ausencia de evidencia      → advisory, no detiene
FAIL     violación mecánica         → exige corrección o desviación aceptada
ANOMALY  contradicción presente     → detiene y escala
BOUNDARY límite alcanzado           → detiene y escala
N/A / EXCLUDED  no aplica           → esperado
VALID    única evidencia positiva
```

(`contracts.py:41-83`; `.agents/policies/autonomous-orchestration.md:§7`).

Sobre esa base:

- **Recuperación con el mismo envolvente:** `failure → diagnose → correct/retry →
  verify → continue`; una recuperación que necesite scope, autoridad, RFC, ADR,
  Protocol o payload nuevos **se detiene** (`supervised-autonomous-execution.md:§7`).
- **Revalidación:** anchor A2 para la identidad de contenido nueva, sin reemplazar
  A1 (`governance.py:364-425`).
- **Prevención vs detección declaradas por separado:** el host nunca presenta la
  segunda como la primera (`supervised-autonomous-execution.md:§10,§12`).
- **Un recurso vital ausente nunca se reporta como ausente:** `git` irresoluble es
  `GAP` declarado; leer el repositorio y fallar es `ObservationError`, no «no es un
  repositorio» (`runtime/README.md:236-251`).
- **Clase ambiental declarada por el Plan**, no juzgada por el host: un exit
  distinto de cero cubierto por una declaración es `GAP`, nunca `PASS`
  (`autonomous-orchestration.md:§7.1`).

**Diferencia.** De garantía, y favorable: las dos fuentes que «nunca abortan»
(`microbots`) o que reparan sin declarar (`microbots`, y la reparación implícita
del manager de MACAE) no distinguen ausencia de evidencia de violación. ARgentOS
sí, y lo hace estructuralmente.

**Garantía.** Recuperación y verificabilidad: ya poseídas.

**Impacto sobre autonomía.** Recuperación: cubierta.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `DEV` + `PROTOCOL`.

**Evidencia.** `runtime/orchestrator/contracts.py:41-83`;
`.agents/policies/autonomous-orchestration.md:§7,§7.1`;
`.agents/policies/supervised-autonomous-execution.md:§6,§7,§10,§12`;
`runtime/orchestrator/derivation.py:469-543`;
`runtime/README.md:236-251`;
`tests/test_autonomous_scope.py:296-316,615-763`;
`docs/rfc/75-change-lifecycle.md:Mecanismo 13`.

### 4.15 human-in-the-loop / human authority boundaries — `ALREADY_SOLVED`

**Problema.** Que la autonomía no adquiera autoridad: que el sistema haga más sin
decidir más.

**Mecanismo externo.** Tres de las cinco fuentes tienen HITL **real**, y cada una
lo modela distinto:

- `prompty` (P1): gate de permiso **inyectado por el host** —
  `ResolvePermission = Callable[[TurnToolCall], bool]`, con eventos
  `permission_requested` → `permission_resolved`; una tool denegada sigue
  produciendo un resultado visible al modelo (`{"error_kind":"permission_denied"}`),
  y los tools MCP tienen `approvalMode`. Es el modelo más cercano al de ARgentOS
  en **forma** (una decisión de permiso en el camino de ejecución) y el más
  lejano en **contenido**: es un booleano delegado al host, sin frontera de
  autoridad, sin scope y sin registro de la autoridad que autorizó.
- `agent-framework` (P3): `WorkflowContext.request_info(...)` +
  `@response_handler` + estado `IDLE_WITH_PENDING_REQUESTS`, con reanudación por
  `Workflow.run(responses={request_id: data})` y checkpoint del estado pendiente.
  Es el más **completo como mecanismo de interacción**.
- MACAE (P5): pausa de aprobación de plan **obligatoria**
  (`MagenticPlanReviewRequest`) y gate de clarificación con
  `approval_mode="always_require"`; el rechazo lanza `RuntimeError`. Ambos waits
  son `asyncio.Event` **en proceso**, no eventos externos durables.
- `microbots` (P2) **no tiene HITL** y lo declara: «No human is involved in the
  task. So, don't seek human intervention» (EXTERNAL_CODE).

**Equivalente actual.** ARgentOS es estrictamente más fuerte, y la comparación lo
confirma:

- **Tres veredictos** (`AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN`) y
  release/promotion/tag en `FORBIDDEN` **con independencia de cualquier
  autorización** (`authority.py`; `contracts.py:226-283`).
- **Envolvente de autonomía** derivada de declaraciones que el Plan aprobado ya
  posee, con `autonomy ⊆ authorized scope ∧ autonomy ⊆ granted authority`
  (`supervised-autonomous-execution.md:§1,§3`).
- **Checkpoint de autorización y no retroactividad** (§1.2).
- **Escritura autorizada como un todo**: un target no autorizado detiene la
  acción **completa**; un conjunto no establecible también (§1.3) — con la
  regresión F-3 testeada (`tests/test_sae_scope_enforcement.py:312-435`).
- **Frontera humana enumerada**: scope y su ampliación, decisiones normativas,
  conflictos de autoridad, RFC, ADR, Protocol, arquitectura, release, promoción,
  abort, transiciones de estado de un finding (§8).
- **La resolución de un finding es humana**: SAE pre-autoriza la *acción de
  corregir*, no la *resolución* (`§6`; CL-8; ADR-16 `AU-3`).
- **Una recomendación nunca es una autorización**, y `exit code 0` nunca es
  completitud (`contracts.py:22-29`).

**Diferencia.** De garantía, y **ARgentOS es superior a las tres referencias**:
`prompty` tiene un booleano de permiso sin frontera de autoridad, scope ni
registro de autoridad; `agent-framework` tiene el mejor mecanismo de
*interacción* (pausa y reanudación de una sesión viva) pero no una frontera de
autoridad por efecto; MACAE tiene un gate de aprobación obligatorio sin frontera
verificable por efecto. ARgentOS **para y escala** en lugar de pausar y esperar
(`.agents/policies/autonomous-orchestration.md:§5`), lo que significa que **no
tiene** el mecanismo de "sesión viva esperando al humano" — y esa diferencia es
deliberada, no una carencia de autoridad. Si la Etapa B quisiera interacción
humana en vivo en lugar de stop/escalate, ese mecanismo sería nuevo; hoy no hay
necesidad declarada.

**Garantía.** Autoridad: ya poseída, y más fuerte.

**Impacto sobre autonomía.** Autoridad humana y delegación: cubiertos.

**Prerrequisito.** `PREREQUISITE = NO`.

**Dominio.** `DEV` + `PROTOCOL`.

**Evidencia.** `runtime/orchestrator/authority.py`;
`runtime/orchestrator/contracts.py:226-283`;
`runtime/orchestrator/autonomy.py`;
`.agents/policies/supervised-autonomous-execution.md:§1-§12`;
`.agents/policies/autonomous-orchestration.md:§5`;
`tests/test_autonomous_scope.py` (58 tests);
`tests/test_sae_scope_enforcement.py` (38 tests);
`tests/test_sae_scope_enforcement_dogfood.py`;
EXTERNAL_CODE: MACAE `src/backend/orchestration/plan_review_helpers.py:448-503`;
`microbots` `src/microbots/MicroBot.py` (system prompt).

### 4.16 Capacidad adicional identificada — aislamiento de ejecución de código no confiable — `REQUIRES_EVIDENCE`

**Por qué se registra.** El Plan autoriza identificar una capacidad adicional
«si existe evidencia concreta de que es arquitectónicamente relevante para
ARgentOS». La evidencia disponible es **comparativa, no de ARgentOS**: `microbots`
construye todo su modelo de ejecución sobre Docker (un contenedor por bot,
montajes read-only con overlayfs, `privileged=True` justificado por overlayfs,
`LocalDockerEnvironment.py`, P2), y su motivación declarada es
least-privilege y proteger el entorno local. ARgentOS no tiene ningún sandbox, y
tampoco tiene —hoy— código no confiable que ejecutar.

**Por qué no se clasifica como prerrequisito.** No hay evidencia de que la Etapa B
vaya a ejecutar código de terceros. La frontera que la Etapa B declara investigar
es *provider/model* y *ejecución multi-step con presupuestos*, no ejecución de
código ajeno. Añadir aislamiento «porque otro proyecto lo tiene» es exactamente lo
que `ROADMAP.md:Etapa C` prohíbe.

**Qué evidencia falta.** Si la Etapa B habilita un `AgentInvoker` que ejecute
comandos arbitrarios o código generado, la pregunta «¿bajo qué frontera de
aislamiento?» pasa a ser un prerrequisito. Se registra la pregunta, no la
respuesta.

**Dominio.** `UNKNOWN` hasta que exista la necesidad.

---

## 5. Architectural Prerequisites

Existen **dos** capacidades clasificadas `ARCHITECTURAL_PREREQUISITE`. Ninguna de
las dos exige un cambio de arquitectura previo a la Etapa B; ambas son fronteras
del **ejecutor** que la Etapa B construye, y por eso deben tratarse **dentro** de
esa etapa y no después (ver §6).

### PR-1 — Admisión de efectos fuera de frontera en el punto de ejecución

**Qué parte de la autonomía depende de ella.** La transición **Execute** del
modelo `Human authority → Authorized objective/scope → Orchestrator → Observe →
Derive → Delegate → Execute → …` cuando el ejecutor puede producir efectos
observables fuera del proyecto (red, git remoto, instalación, cambio destructivo,
escritura fuera del proyecto). Es la única frontera que hoy existe **en la norma
del Protocol y no en el ejecutor DEV**.

**Por qué la autonomía quedaría arquitectónicamente incompleta o insegura.**
Porque el propio modelo de ARgentOS declara que la disponibilidad de una
capacidad nunca es una autorización
(`AUTHORIZATION.md:22-23`; `PROTOCOL_BOUNDARIES.md:175-177`) y define un
procedimiento de admisión por efecto (`## Effects` con `kind`, `authorized_by`,
`evidence_ref`, `status`). Un ejecutor que produce efectos sin aplicar esa
admisión **contradice la norma que dice cumplir**. Y el host **no puede
interponerse** dentro de la invocación (`supervised-autonomous-execution.md:§12`):
la admisión de efectos es, por construcción, lo único que puede preceder al
efecto.

**Por qué no es un prerrequisito *hoy*.** Porque el host no ejecuta efectos: no
hay provider, red ni credenciales (`runtime/README.md:366-448`), y el invoker por
defecto es `NullAgentInvoker`. La carencia es de **mecanismo ausente**, no de
**daño ocurrido** (`INFERENCE` declarada en §4.2).

**Forma de resolución (no es una propuesta de diseño, es la lectura del modelo
existente).** La norma ya está escrita; falta que el consumidor la verifique. El
lugar natural es donde ya vive la otra mitad de la admisión: el punto de
enforcement anterior al efecto (`ExecutionHost._apply_autonomy_gate`), extendido
de *write-targets* a *efectos declarados*. No requiere entidad, registry, estado
ni contrato nuevos en el payload.

### PR-2 — Presupuesto de ejecución como frontera de recurso

**Qué parte de la autonomía depende de ella.** La transición **Continue → Stop**
del modelo, y la capacidad de recibir «un objetivo suficientemente amplio»
(`ROADMAP.md:Etapa B`). Con ejecución desatendida, el único techo que hoy existe
es «deja de progresar» (`STOP_NO_PROGRESS`) o «se alcanzó el límite de
iteraciones del host» (`STOP_MAX_ITERATIONS`, constante, no acumulada entre
procesos).

**Por qué la autonomía quedaría arquitectónicamente incompleta.** Porque el
modelo de frontera de ARgentOS es explícito y **tiene un eje ausente**:
`autonomy ⊆ authorized scope ∧ autonomy ⊆ granted authority` no dice nada sobre
**cuánto** puede consumir la autonomía. Un objetivo amplio ejecutado sin techo de
recurso no puede declarar terminación por recurso, y la única garantía de
terminación es la de progreso — que es **distinta** (un bucle puede progresar y
consumir indefinidamente).

**Evidencia de que la carencia es real y no teórica.** Dos de los cinco sistemas
inspeccionados dedican constantes explícitas a esto y ambos tienen el mismo
hueco: `microbots` acota iteraciones y tiempo pero deja un `TODO` explícito para
reemplazar el conteo de iteraciones por gestión de costo
(`MicroBot.py:182`), y MACAE acota rondas y estancamiento sin budget de
tokens/costo. Ninguno de los dos declara un presupuesto **autorizado** por el
trabajo.

**Forma de resolución (lectura del modelo existente).** El envolvente de
autonomía ya se **deriva** de declaraciones que el Plan aprobado ya posee
(`supervised-autonomous-execution.md:§3`). Un techo de recurso es una declaración
de la misma naturaleza que `Task` y `Scope`: puede vivir en la misma sección y
derivarse por el mismo mecanismo, sin crear superficie de declaración nueva. La
persistencia del consumo acumulado es la única parte que hoy no existe y necesita
un lugar de evidencia — el candidato natural es el mismo journal que ya persiste
cada iteración.

> **REQUIRES_HUMAN_DECISION.** Si `PR-1`/`PR-2` deben implementarse **dentro** de
> la Etapa B (como parte de la frontera del ejecutor) o como un Change propio
> **previo** es una decisión de secuencia y alcance, no una cuestión técnica que
> este análisis pueda resolver. Este documento no la toma. Lo que sí establece con
> evidencia es que **ninguna de las dos puede quedar para después de la Etapa B**,
> porque ambas son condiciones de seguridad y de terminación del ejecutor que la
> Etapa B habilita.

---

## 6. Autonomy Implications

### 6.1 El modelo de la Etapa B ya es viable

Cada transición del modelo declarado en `ROADMAP.md:Etapa B` tiene mecanismo,
evidencia y test:

| Transición | Mecanismo | Garantía | Evidencia |
|---|---|---|---|
| Human authority → authorized objective/scope | Plan `Aprobado para ejecución`; `## Delegación agentiva` (Task + Scope) | Autoridad | `derivation.py:217-242`; `supervised-autonomous-execution.md:§2,§3` |
| → Orchestrator | `ExecutionHost` | — | `host.py:315-365` |
| → Observe | `observe()` re-lee repositorio + evidencia, sin memoria | Trazabilidad | `observation.py:754`; `host.py:11-25` |
| → Derive | función pura, vocabulario cerrado | Determinismo | `derivation.py:195-466` |
| → Delegate | `Delegation` + `WorkerAdapter` + `AgentInvoker` | Autoridad / aislamiento | `contracts.py:322-396`; `worker.py`; `agent_worker.py:199-235` |
| → Execute | `CommandWorker` / `AgentWorker` | Ejecución | `worker.py:432`; `agent_worker.py:285` |
| → Verify | validación declarada + verificación de scope **fuera** del worker | Verificabilidad | `host.py:640-766`; `worker.py:classify` |
| → Correct / Recover | 11 condiciones de corrección autónoma; recuperación con el mismo envolvente | Recuperación | `autonomy.py:evaluate_finding_resolution`; `supervised-autonomous-execution.md:§6,§7` |
| → Revalidate | anchor A2 sin reemplazar A1; `RUN_REVALIDATION` | Reproducibilidad | `governance.py:364-425` |
| → Continue | `evaluate_autonomy` → `CONTINUE` | Autonomía | `autonomy.py`; `tests/test_autonomous_scope.py:131,905` |
| → Stop / Escalate | 21 acciones de stop; las de autoridad humana nombran la autoridad que decide | Autoridad | `contracts.py:116-210`; `tests/test_autonomous_scope.py:589` («every stop condition is reachable») |

**Conclusión.** El modelo no necesita ninguna capacidad estructural adicional
para ser **viable**. Necesita dos fronteras de **ejecución** (PR-1, PR-2) para
ser **seguro y terminable** bajo ejecución real y de duración no trivial.

### 6.2 Las capacidades adicionales que el Plan pregunta específicamente

| Pregunta | Respuesta | Clasificación |
|---|---|---|
| ¿durable execution? | No: la posición se re-deriva del repositorio | ALREADY_SOLVED |
| ¿ejecución reanudable? | Sí la tiene, para el artefacto (Protocol) y la derivación (DEV) | ALREADY_SOLVED |
| ¿persistencia de execution state? | Deliberadamente inexistente; la sustituye la reconstrucción | ALREADY_SOLVED |
| ¿idempotencia? | Sí, por identidad y por registros marker-guarded | ALREADY_SOLVED |
| ¿replay/recovery? | Recovery sí; replay no, y no debe introducirse (segundo modelo de verdad) | ALREADY_SOLVED |
| ¿work units? | Ya existen distribuidas como Plan/Delegation/WorkerResult | ALREADY_SOLVED |
| ¿execution graph? | No justificado: sin concurrencia real ni dependencia no derivable | NOT_VALUABLE_FOR_ARGENTOS |
| ¿budgets? | **Falta el eje de recurso**: es frontera del ejecutor | **ARCHITECTURAL_PREREQUISITE (PR-2)** |
| ¿resource governance? | Parcial: Context Budget (semántico, medido) + límites de bucle del host | **incluido en PR-2** |
| ¿evaluation? | Existe por rúbrica y por juicio; falta comparación/regresión | POST_AUTONOMY |
| ¿observability? | Reconstruibilidad completa; sin backend de telemetría | ALREADY_SOLVED |
| ¿capability admission? | La norma existe; el ejecutor no la aplica a efectos | **ARCHITECTURAL_PREREQUISITE (PR-1)** |
| ¿reconciliation? | Existe para gobernanza y contenido, que es su dominio declarado | ALREADY_SOLVED |

### 6.3 El efecto de PR-1 y PR-2 sobre la secuencia

Ni `PR-1` ni `PR-2` exigen detener el roadmap. Su efecto es de **alcance de la
Etapa B**:

- Si la Etapa B habilita ejecución real de provider/model y ejecución multi-step,
  **PR-1 y PR-2 están dentro del alcance de la Etapa B**, no después. Son
  condiciones del ejecutor.
- Si la Etapa B se definiera más estrecha (p. ej. sólo persistencia y consumo de
  Worker Results, derivación y ejecución multi-step sin efectos externos), `PR-1`
  seguiría siendo prerrequisito del primer paso que produzca un efecto fuera del
  proyecto, y `PR-2` del primer paso desatendido de duración no trivial.
- En ningún caso corresponde a este análisis decidir la secuencia. El registro
  correcto es: **`Plan149 / Retrospective → SAE / Autonomy` sigue siendo la
  secuencia válida, con PR-1 y PR-2 como condiciones de la Etapa B**.

### 6.4 Corrección al inventario de fronteras candidatas de la Etapa B

`ROADMAP.md:Etapa B` lista trece fronteras candidatas, entre ellas
«presupuestos de ejecución (execution budgets)» y «garantías de terminación
(termination guarantees)». La evidencia de este análisis **confirma** esas dos y
**añade** una que el inventario no nombra:

- **Admisión de efectos** (`PR-1`): el inventario nombra «ejecución real mediante
  provider/model» como frontera, pero no la frontera de autorización de los
  efectos que esa ejecución produce. Es la carencia que la comparación externa
  hizo visible.

Las demás fronteras del inventario no se ven afectadas por este análisis; varias
ya están resueltas por el baseline (persistencia y consumo de Worker Results,
derivación de la siguiente acción, recuperación ante fallos declarados).

---

## 7. Capabilities That Can Wait

Clasificadas `POST_AUTONOMY`. Aportan valor, no bloquean la evolución inmediata.

| Capacidad | Por qué puede esperar | Qué la volvería prioritaria |
|---|---|---|
| **Evaluation comparativa / detección de regresión de calidad** | La verificación de contenido y la rúbrica cubren el juicio por artefacto; el volumen de salidas autónomas todavía no justifica una serie histórica ni un umbral | Que la Etapa B produzca muchas salidas autónomas y que la pregunta «¿esta salida es peor que la anterior?» sea frecuente |
| **controlled concurrency** | La ejecución es secuencial por diseño y ninguno de los cinco sistemas comparados demuestra concurrencia segura; ambos la evitan | Que exista trabajo autorizado genuinamente independiente que convenga ejecutar en paralelo, y que la Etapa B lo declare |
| **Cancelación / abort en vuelo del host** | El abort de un Change es autoridad humana y el host no la ejerce; matar el proceso deja evidencia parcial que la reconstrucción resuelve | Operación desatendida de duración larga, donde detener sin matar el proceso tenga valor operativo |
| **Telemetría de ejecución con backend y agregación en vivo** | La garantía buscada es reconstruibilidad, y está cubierta sin backend | Necesidad operativa de diagnóstico en vivo o de consultas agregadas sobre muchas corridas |
| **Cola durable / dead-letter / replay de ingesta** (patrón de ACI) | Resuelve durabilidad *de ingesta de eventos* de una plataforma de telemetría; ARgentOS no tiene ese problema | Que exista un pipeline de eventos cuya pérdida sea inaceptable |

---

## 8. Already Solved

Capacidades que una comparación por features habría reportado como faltantes y
que ARgentOS ya resuelve. En cada caso la diferencia con el sistema externo es de
**implementación**, no de **garantía**.

1. **Execution Contract / Work Unit** — existe como `Plan + Delegation +
   WorkerResult + declared_scope + anchor + journal`, con la relación
   `delegation → worker result → ingestion → next action` explícita y persistida.
   Lo que falta es la *palabra*, no la capacidad (§4.1).
2. **Durable Execution** — sustituida por **reconstrucción desde el
   repositorio**; más fuerte para este modelo, porque no introduce un segundo
   lugar donde vive la verdad, y verificada por test de reinicio (§4.3).
3. **interruption / resume** — procedimiento de reanudación de iteración parcial
   definido operacionalmente en el Protocol, y continuidad por re-derivación en
   DEV (§4.4).
4. **idempotent y race-safe execution** — registros marker-guarded, escritura
   atómica, identidad de contenido como discriminador, y declaración explícita del
   riesgo de single-instance cuando no hay subagentes (§4.5).
5. **Observability / Execution Intelligence** — reconstruibilidad completa sin
   backend, más catálogo de garantías clasificado por quién las verifica (§4.9).
6. **desired-state reconciliation** — `anchor_stale`, `consistency_pass`,
   checkpoint de autorización, conciliación bidireccional `state.json ↔
   HARNESS_REPORT`, y la regla `PC-75` («gobierna el contrato, nunca se reconcilia
   reinterpretándolo») (§4.12).
7. **execution state persistence** — evidencia durable entre procesos + artefactos
   de gobernanza versionados + estado del host **deliberadamente inexistente**
   (§4.13).
8. **failure recovery** — semántica `GAP/ANOMALY/FAIL/BOUNDARY` que distingue
   ausencia de evidencia de violación; recuperación con el mismo envolvente;
   separación declarada entre prevención y detección (§4.14).
9. **human-in-the-loop / human authority boundaries** — más fuerte que las dos
   referencias externas que tienen algo comparable; MACAE tiene gate de
   aprobación sin frontera verificable por efecto, y `microbots` no tiene ninguno
   (§4.15).
10. **Semantic Context** — `SegmentIdentity`, `SemanticContextIdentity`,
    `MaterializationIdentity`, Stable/Dynamic, prefijo estable, Prompt Cache, con
    `I-MAT-001` verificable, que ninguna fuente externa acredita (§4.11).

---

## 9. Non-valuable / Rejected

Sólo lo que tiene evidencia suficiente para descartarse.

### 9.1 Execution Graph — `NOT_VALUABLE_FOR_ARGENTOS`

Descartado con evidencia, no por diferencia cultural:

- **No hay concurrencia real que planificar** (una delegación por iteración,
  `host.py:906-954`).
- **No hay ciclo que detectar**: la autoridad precede al trabajo y el cierre
  sucede a la validación, por construcción del Change Lifecycle.
- **La dependencia ya es derivable** y la derivación está ordenada y testeada
  (`derivation.py:195-466`).
- **Un grafo no añade ninguna garantía** de las que el Plan enumera: no verifica,
  no autoriza, no evidencia, no controla recursos.
- **Evidencia externa adversa y fuerte**: `agent-framework` (P3) **tiene** el
  grafo completo — `FanOutEdgeGroup` con `selection_func` condicional,
  `FanInEdgeGroup`, `SwitchCaseEdgeGroup`, supersteps, concurrencia por
  `asyncio.gather` — y MACAE, que lo consume para construir un sistema
  multi-agente real, usa una **lista plana ordenada sin campo de dependencia** y
  exige completitud por texto de prompt (P5). La existencia de la capacidad en el
  framework no implica su necesidad. `prompty` (P1), con siete runtimes, tampoco
  tiene orquestación multi-paso.
- **Contradice la dirección declarada**: `ROADMAP.md:Qué no es una entrada de
  este roadmap` prohíbe «nuevas state machines» y «nuevas entidades globales»;
  `docs/architecture` y el resto del baseline insisten en una sola fuente de
  verdad por concepto.

### 9.2 Replay / reanudación desde checkpoint persistido

Descartado como **mecanismo a incorporar** (no como idea a conocer):

- Resolvería un problema que ARgentOS ya resolvió de otra forma (§4.3).
- Introduciría un **segundo modelo de verdad** sobre dónde está el trabajo,
  contra `.agents/AGENTS.md:8` y `autonomous-orchestration.md:§2`.
- La evidencia externa documenta el riesgo de dos maneras complementarias:
  **capacidad no consumida** (MACAE pasa `InMemoryCheckpointStorage()` donde el
  framework ofrece `FileCheckpointStorage`, P5) y **contrato no realizado**
  (`prompty` documenta «MUST NOT duplicate … an effect that the checkpoint
  already records as committed», define `EngineCheckpoint`/`ResumeContext` con
  `reconciliationRequired` y `resumeSameIteration`, y su runtime Python **no
  persiste** checkpoints: el único store concreto es `InMemoryCheckpointStore` en
  Java, P1). Ambos son `EXTERNAL_CODE`.

### 9.3 Segunda arquitectura de contexto / modelo semántico paralelo

Descartado:

- Las fuentes externas **no tienen** un modelo de contexto comparable: ACI modela
  eventos en un grafo sin distinción stable/dynamic ni identidad de contexto;
  `prompty` aporta portabilidad de plantilla.
- Adoptar su identidad (evento + epoch ms) en lugar de `SegmentIdentity`
  (contenido + versión semántica + namespace) **degradaría** la garantía: la
  norma de ARgentOS es explícita en que `SegmentIdentity` «is never reduced to a
  content hash» (`CONTEXT.md:300-301`), y menos aún a un timestamp.

### 9.4 Telemetría como condición de corrección

Descartado como **prerrequisito** (permanece como `POST_AUTONOMY`, §7):

- Ninguno de los sistemas con telemetría fuerte (MACAE, ACI) la usa para
  **decidir** más que lo que ARgentOS decide sin ella.
- `microbots` demuestra el costo de la ausencia (reconstrucción post-hoc por
  regex), pero ARgentOS ya tiene reconstrucción estructurada.
- La telemetría es valor **operativo**, y el runtime DEV declara explícitamente
  que no la incluye (`runtime/README.md:124-125,443-445`; RFC-74 sin tocar).

---

## 10. Requires Evidence

Preguntas abiertas que **impiden** una clasificación definitiva. Ninguna de ellas
bloquea la decisión de secuencia de §6.3.

### RE-1 — Aislamiento de ejecución de código no confiable (§4.16)

- **Qué se intentó verificar:** si la Etapa B implica ejecutar código o comandos
  no confiables, y en ese caso bajo qué frontera de aislamiento.
- **Evidencia disponible:** `microbots` resuelve esto con Docker por contenedor,
  montajes read-only con overlayfs y `privileged=True` justificado (P2).
- **Evidencia faltante:** una declaración de la Etapa B sobre la naturaleza del
  `AgentInvoker` real (¿ejecuta comandos arbitrarios? ¿código generado? ¿sólo
  edita archivos del repositorio?).
- **Efecto sobre la confianza:** alta para `NOT_VALUABLE_FOR_ARGENTOS` **hoy**;
  pasaría a `ARCHITECTURAL_PREREQUISITE` si la Etapa B habilita ejecución de
  código no confiable.

### RE-2 — Naturaleza del `AgentInvoker` real y de sus efectos

- **Qué se intentó verificar:** si el invoker que la Etapa B inyecte producirá
  efectos fuera de frontera (red, instalaciones, git remoto).
- **Evidencia disponible:** el repositorio **no** incluye provider, modelo, red ni
  credenciales, y lo declara como límite
  (`runtime/README.md:366-448`; `autonomous-orchestration.md:§11.2`).
- **Evidencia faltante:** la decisión de entorno de ejecución. Sin ella, `PR-1` no
  puede dimensionarse (no se sabe qué clases de efecto aparecerán) y `PR-2` no
  puede fijar unidades (tokens, llamadas, costo, tiempo).
- **Efecto sobre la confianza:** alta para la **existencia** de la carencia
  (verificada por ausencia de mecanismo); media para su **magnitud**.

### RE-3 — Materialidad del límite de recurso en la operación real

- **Qué se intentó verificar:** si la carencia de presupuesto de recurso (§4.8) se
  manifiesta en operación o queda como riesgo teórico.
- **Evidencia disponible:** el host DEV nunca se ha ejecutado con un invoker real;
  las corridas registradas son de dogfood con `NullAgentInvoker`/`CommandWorker`.
  Los dos sistemas externos con presupuestos los tratan como constantes de
  construcción y uno deja un `TODO` explícito de gestión de costo.
- **Evidencia faltante:** una corrida desatendida real con consumo medido.
- **Efecto sobre la confianza:** la **ausencia del mecanismo** está verificada por
  código; que esa ausencia **cause** un daño operativo es `INFERENCE`, no
  observación. Se clasifica `ARCHITECTURAL_PREREQUISITE` por la garantía faltante
  (terminación por recurso), no por un incidente.

### RE-4 — Efecto de la concurrencia futura sobre los registros de gobernanza

- **Qué se intentó verificar:** qué pasaría con la escritura concurrente del
  anchor/checkpoint si la Etapa B habilitara multi-worker paralelo.
- **Evidencia disponible:** `scope_path` ya modificado + comparación de contenido
  (no de `git status`) resuelve la detección de violaciones en un árbol sucio
  (`runtime/README.md:429-434`; `tests/test_agent_worker.py:1040`); los registros
  son marker-guarded e idempotentes.
- **Evidencia faltante:** no hay coordinación distribuida (locks, leases, ETags)
  en ningún punto del baseline, y no se ha probado el comportamiento bajo dos
  hosts concurrentes sobre el mismo Change.
- **Efecto sobre la confianza:** alta para `POST_AUTONOMY` mientras la ejecución
  sea secuencial; la clasificación cambiaría si la Etapa B declara concurrencia.

### RE-5 — Valor real de una capa de evaluación comparativa (§4.10)

- **Qué se intentó verificar:** si existe en las fuentes externas una práctica de
  evaluación que ARgentOS no tenga y que aporte una garantía.
- **Evidencia disponible:** el único harness de evaluación propio
  (`microbots`/`auto_memory`) evalúa **ejecuciones contra un benchmark externo**
  (SWE-bench), no la calidad de una salida respecto de una anterior. MACAE
  **afirma** evaluación offline en documentación sin artefacto en el repositorio
  (EXTERNAL_DOC). ACI no evalúa calidad de contexto.
- **Evidencia faltante:** no hay evidencia externa de un mecanismo de detección de
  regresión de calidad que ARgentOS pueda tomar como referencia. La clasificación
  `POST_AUTONOMY` se sostiene por ausencia de necesidad demostrada, no por
  evidencia positiva de su valor.
- **Efecto sobre la confianza:** media.

---

## 11. Architectural Conclusions

Conclusiones **estrictamente arquitectónicas**. Ninguna decisión de roadmap.

**11.1.** La arquitectura de ARgentOS para la autonomía supervisada es
**internamente completa**: cada transición del modelo declarado tiene mecanismo,
garantía y evidencia (§6.1). La revisión no encontró ninguna transición sin
respaldo.

**11.2.** Existen exactamente **dos fronteras de ejecución ausentes**, y ambas
tienen la misma forma: una norma o un modelo que ya existe y un consumidor que no
lo aplica. `PR-1` es la norma de admisión de efectos del Protocol no aplicada por
el ejecutor DEV; `PR-2` es el eje de recurso que el modelo de frontera
(`autonomy ⊆ scope ∩ authority`) no cubre.

**11.3.** La ausencia de **durable execution** en el sentido de los frameworks
externos no es una carencia: es una **propiedad arquitectónica** de ARgentOS. El
sistema no reanuda estado, **reconstruye posición**. La consecuencia verificable
es que el store de evidencia puede perderse sin que la continuidad se pierda
(`store.py:18-22`; `tests/test_autonomous_orchestrator.py:970-1006`) — una
garantía que un sistema basado en checkpoints **no** tiene, porque su reanudación
depende del storage.

**11.4.** La capacidad que un `Execution Graph` aportaría **no es verificable** en
el modelo actual: no hay concurrencia, no hay ciclo y no hay dependencia no
derivable. Un grafo sería una segunda representación de relaciones ya legibles, y
por lo tanto una regresión contra el principio de una sola fuente de verdad.

**11.5.** El **Context Budget** de ARgentOS y un **Execution Budget** son dos
magnitudes de naturaleza distinta, y la norma ya lo declara: el primero es un
límite **semántico** de composición, el segundo un límite de **recurso de
ejecución**; el propio estándar separa además `semantic budget`, `physical /
provider / storage cost` y `prompt materialization cost`
(`BUDGET_MATERIALIZATION.md:77-82`). La carencia de `PR-2` no se resuelve
extendiendo el Context Budget: se resuelve declarando un techo de la segunda
naturaleza.

**11.6.** La **idempotencia** de ARgentOS no proviene de claves ni de locks, sino
de **identidad** (identidad de contenido, identidad de segmento) y de
**estructura** (registros marker-guarded, escritura atómica). Es una propiedad más
fuerte que la deduplicación, porque no depende de que el llamador recuerde una
clave.

**11.7.** La capa de **evaluación** de ARgentOS y su capa de **métricas** son
distintas y no deben conflacionarse: las métricas son *advisory* y observacionales
(`PROTOCOL_METRICS.md:166-168`), y la evaluación es **juicio con evidencia
citable**, con la regla explícita de que un claim sólo puede llamarse «verified»
si cita evidencia de una clase distinta de la atestación
(`harness/INDEX.md:151-160`). Cualquier capa futura de evaluación debe respetar
esa distinción o degradará la semántica existente.

**11.8.** El artefacto de este análisis se ubica en una ruta que la instrucción
explícita del Change fijó y que no coincide con la familia que el contrato de
placement resolvería para su clase documental (`Working analysis` →
`docs/working/{audits,research,proposals}/`). Se **registra** la divergencia. **Fase 1
(F6):** la regla aplicable es `PC-52` + `PC-27` + `PC-29` —registrar la excepción en un
artefacto autorizante, de forma atribuible y auditable—, **no** `PC-75`; esa excepción
**no está registrada en ningún artefacto autorizante**, y se trata de la **segunda**
instancia de la misma desviación (`PC-28`). Determinación de F6: clase `Working /
Analysis` y namespace canónico `docs/working/audits/` con fila en
`docs/working/audits/INDEX.md` si el análisis entra al repositorio; **la decisión de
entrar, permanecer externo o registrar una excepción es `HD-INT-G`**
(`HUMAN_DECISION_REQUIRED`; Diseño §25), que este documento **no** resuelve. No se crea
una familia nueva (`PC-20`).

**11.9.** Ninguna capacidad de las cinco fuentes externas inspeccionadas
**cambia materialmente** la arquitectura necesaria para la autonomía supervisada.
El aporte de la comparación fue **confirmatorio** en diez capacidades y
**correctivo** en una: hizo visible la admisión de efectos (`PR-1`), que no estaba
nombrada en el inventario de fronteras candidatas de la Etapa B.

---

## 12. Evidence Index

### 12.1 Fuentes de ARgentOS

| Ref | Path | Símbolo / sección | Nivel |
|---|---|---|---|
| A1 | `runtime/orchestrator/host.py` | `ExecutionHost`, `run`, `iterate`, `_execute_delegation`, `_scope_violations`, `_apply_autonomy_gate`, `derived_conditions`, `reconstruct` | CODE |
| A2 | `runtime/orchestrator/contracts.py` | vocabulario de señales, acciones derivadas, stops, `Delegation`, `WorkerResult`, `validate_worker_result` | CODE / CONTRACT |
| A3 | `runtime/orchestrator/derivation.py` | `derive_next_action`, `max_iterations_action`, `no_progress_action`, `forbidden_scope_action` | CODE |
| A4 | `runtime/orchestrator/autonomy.py` | `AutonomyEnvelope`, `AutonomyCandidate`, `evaluate_autonomy`, `authorization_projection`, `authorization_drift`, `evaluate_finding_resolution`, `summarize_autonomy` | CODE |
| A5 | `runtime/orchestrator/authority.py` | `AuthorityBoundary` | CODE |
| A6 | `runtime/orchestrator/store.py` | `OrchestratorStore`, `JournalRead`, `_write_text`, `read_journal_with_gaps` | CODE |
| A7 | `runtime/orchestrator/observation.py` | `ChangeObservation`, `governance_fingerprint`, `anchor_stale`, `blocking_pending`, `open_findings`, `observe` | CODE |
| A8 | `runtime/orchestrator/governance.py` | `append_marked_block`, `set_status`, `_write_atomic`, `record_revalidation` | CODE |
| A9 | `runtime/orchestrator/agent_worker.py` | `AgentInvoker`, `NullAgentInvoker`, `AgentWorker`, `DEFAULT_MAX_STEPS`, `DEFAULT_CONTEXT_BUDGET` | CODE |
| A10 | `runtime/orchestrator/worker.py` | `CommandWorker`, `NullWorker`, `WorkerAdapter`, `classify`, `repository_snapshot`, `changed_paths` | CODE |
| A11 | `runtime/toolcalls/canonical.py` | `OrderingContract` v1/v2, `PROTOCOL_VERSION`, envelope canónico | CODE |
| A12 | `runtime/toolcalls/identity.py` | `SemanticContextIdentity`, `SegmentIdentity` | CODE |
| A13 | `runtime/toolcalls/budget.py` | `estimate_tokens`, `MaterializationCost` | CODE |
| A14 | `runtime/toolcalls/prompt_rendering.py` | `render_prompt`, `render_dynamic_suffix`, `materialize` | CODE |
| A15 | `runtime/toolcalls/cache_coordinator.py`, `provider_cache.py` | admisión de caché; `ProviderPromptCacheCapability` | CODE |
| A16 | `runtime/placement/resolver.py`, `rules.py` | resolución `PLACE`/`STOP` | CODE |
| A17 | `runtime/README.md` | §Canonical materialization; §Provider adapter; §DEV Autonomous Orchestrator; §SAE; §DEV Agent Worker | DOC |
| A18 | `.agents/policies/supervised-autonomous-execution.md` | §1–§12 | POLICY |
| A19 | `.agents/policies/autonomous-orchestration.md` | §1–§11 | POLICY |
| A20 | `.agents/policies/authority.md`, `validation-closure.md`, `lifecycle-checkers.md` | clases de autoridad, cierre, gates | POLICY |
| A21 | `.agents/workflows/change-lifecycle.md` | ciclo de vida DEV | POLICY |
| A22 | `.agents/AGENTS.md` | reglas operativas fundamentales 1–10 | POLICY |
| A23 | `docs/rfc/75-change-lifecycle.md` | Mecanismo 13 (Observability), 14 (Automation), Dev vs Protocol | DOC |
| A24 | `docs/rfc/72-provider-prompt-cache-capability.md`, `docs/rfc/78-provider-bound-stable-prefix-materialization.md` | materialización canónica, prefijo estable | DOC |
| A25 | `protocol/.agents/standards/runtime/AUTHORIZATION.md` | vocabulario, `## Effects`, estados, invariantes AUTH-001..004 | CONTRACT |
| A26 | `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` | Artifact Safety Rule, iteración parcial, procedimiento de reanudación, Agent Scope and Autonomy, Tooling restrictions, External interaction | CONTRACT |
| A27 | `protocol/.agents/standards/context/CONTEXT.md` | clasificación Stable/Dynamic, segmentos, identidad, scope, isolation, correctness, prefijo estable | CONTRACT |
| A28 | `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md` | §2 regla de estimación, §3 alcance, §6 otros runtimes, §7 enforcement status, §8 caching/persistencia | CONTRACT |
| A29 | `protocol/.agents/contracts/METRICS.md`, `standards/runtime/PROTOCOL_METRICS.md` | catálogo de eventos, clases de verifiabilidad, agregación, I-ECO-001..006 | CONTRACT |
| A30 | `protocol/.agents/harness/INDEX.md` | §Guarantee catalog (5 clases), §Enforcement boundaries, §Claims rule | POLICY |
| A31 | `protocol/.agents/standards/quality/RUBRICS.md` | escala, criterio crítico, `## Rubric Evaluation` | POLICY |
| A32 | `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` | `## Acceptance Criteria Evaluation`, `## Rubric Evaluation` | CONTRACT |
| A33 | `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md` | admisión de profile/skill/budget antes de delegar | POLICY |
| A34 | `protocol/.agents/orchestrators/core/roles/orchestrator.md` | §5 delegation execution modes; single-instance; sesión y reanudación | CONTRACT |
| A35 | `protocol/.agents/contracts/HARNESS_REPORT.md` | auto-reporte y su límite | CONTRACT |
| A36 | `protocol/.agents/skills/adversarial-deliberation/SKILL.md` | pasadas atribuidas, evaluación comparativa, veredicto advisory | CONTRACT |
| A37 | `protocol/.agents/features.toml` | flags declarativos y su obligación de consumo | CONTRACT |
| A38 | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md` | payload de invocación, `context_budget` | CONTRACT |
| A39 | `protocol/.agents/VERSION` | `11.6.2` | CONTRACT |
| A40 | `tests/test_autonomous_orchestrator.py` | reinicio/continuidad, no-progress, max-iterations | TEST |
| A41 | `tests/test_autonomous_scope.py` | 58 tests: frontera, autoridad, scope, recuperación, resumen de autonomía | TEST |
| A42 | `tests/test_sae_scope_enforcement.py` | 38 tests: enforcement completo, F-3, drift, pureza | TEST |
| A43 | `tests/test_sae_scope_enforcement_dogfood.py` | enforcement sobre el árbol real | TEST |
| A44 | `tests/test_agent_worker.py` | recuperación tras reinicio, transcript, violación de scope en árbol sucio | TEST |
| A45 | `tests/test_canonical_materialization.py`, `tests/test_canonical_materialization_v2.py`, `tests/test_prompt_cache_dogfood.py` | `I-MAT-001`, orden v1/v2, dogfood del payload real | TEST |
| A46 | `tests/test_measure_context_budget.py`, `tests/test_aggregate_metrics.py`, `tests/test_check_session_artifacts.py` | presupuesto, métricas, gates de sesión | TEST |
| A47 | `tools/aggregate_metrics.py`, `tools/audit_gates.py`, `tools/measure_context_budget.py`, `tools/check_lifecycle_*.py` | verificación mecánica | CODE |
| A48 | `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md`, `ARCHITECTURAL_DECISION_MODEL.md` | P3 (timestamps), P4 (budget sin par), D10 (Observability/Budget) | DOC |
| A49 | `ROADMAP.md` | Etapas A → B → C; fronteras candidatas; qué no es una entrada | DOC |
| A50 | `docs/plans/149-argentos-capability-and-autonomy-roadmap.md` | origen del roadmap estratégico | DOC |
| A51 | `MASTER_PENDING_WORK_INVENTORY.md` (untracked, ajeno) | verificación read-only de baseline | INFERENCE — **referencia de provenance no versionada** (Fase 1, F6): no resuelve contra copia versionada (`docs/AGENTS.md:References`); su registro es `HD-INT-G` |
| A52 | `docs/placement-contract.md` | §6 familias, PC-20, PC-56, PC-64, PC-75 | CONTRACT |
| A53 | `docs/AGENTS.md` | carta documental, `Folder → class map` | POLICY |

### 12.2 Fuentes externas

| Ref | Repositorio | Mecanismo relevante | Verificado en | Nivel |
|---|---|---|---|---|
| P1 | `microsoft/prompty` | `.prompty` (YAML frontmatter + markdown) con `inputs`/`outputs` tipados, `model`/`connection`, `metadata` libre; **sin versionado de prompt**. Validación de inputs que rellena defaults y **no type-checkea** (`spec/spec.md:3012-3044`). Provider = executor+processor por proveedor; `Connection` como unión discriminada. Tracing normado con `.tracy` (MUST), Console y **OpenTelemetry** `gen_ai.*` (SHOULD) — `tracing/otel.py:51`. **Sin evaluación**: no hay graders, CLI ni harness; delega al framework de test del usuario. **Contrato de durabilidad no realizado**: `EngineCheckpoint` (`pipeline/checkpoint.tsp:20-96`, con `lastSequence`, `stablePrefixMessages`, `pendingToolRequests`, `completedToolResults`, `reconciliationRequired`, `finalOutputReady`, `resumeSameIteration`) y `ResumeContext` (`:105-121`), más `CheckpointStore` como Protocol generado; el único store concreto es Java `InMemoryCheckpointStore`; el motor Python sólo emite eventos. HITL como gate inyectado por el host (`ResolvePermission`, `permission_requested`/`permission_resolved`, `McpTool.approvalMode`); `guardrails`/`steering`/`cancellation` como controles de runtime. Límites: `context_budget` en caracteres, `MAX_ITERATIONS=10`, `MAX_LLM_RETRIES=3`, `maxOutputTokens`; **sin** costo ni wall-clock. Un repo, `spec/spec.md` normativo + TypeSpec como fuente de verdad + 7 runtimes con vectores de conformance | Código y spec (`main`, tree `290c8006`) | EXTERNAL_CODE / EXTERNAL_DOC |
| P2 | `microsoft/microbots` | Bucle `while` con `max_iterations=20`/`timeout_in_seconds=200`; sub-agente síncrono que **comparte contenedor** y cuyas iteraciones se cargan al padre («run only ONE at a time»); Docker + overlayfs read-only con `privileged=True`; **sin** resume (estado en memoria, contenedor destruido en `stop()`); **sin** HITL («don't seek human intervention»); logging plano, reconstrucción **post-hoc por regex** (`utils/multi_agent_log_parser.py:31-76`); `auto_memory` con harness train↔eval (`EvalOutcome` → `rounds/round_N/eval/result.json`) y SWE-bench; `TODO` explícito de gestión de costo (`MicroBot.py:182`). `insights`/`journal`: **NOT_FOUND**; el equivalente funcional es `memory/` (markdown), llevado adelante entre corridas | Código (clone read-only, `main` @ `713b5515`) | EXTERNAL_CODE |
| P3 | `microsoft/agent-framework` | `SupportsAgentRun` Protocol (`_agents.py:272`) con `run(..., stream=)` y sesiones; **grafo real** de workflows (`WorkflowBuilder`, `Executor`, `Edge`/`EdgeGroup`, `FanOutEdgeGroup` con `selection_func`, `FanInEdgeGroup`, `SwitchCaseEdgeGroup`, supersteps como eventos, concurrencia por `asyncio.create_task`/`gather`); **checkpointing en código** (`WorkflowCheckpoint` con `messages`/`state`/`pending_request_info_events`/`iteration_count`/`previous_checkpoint_id`/`graph_signature_hash`, `CheckpointStorage` Protocol, `InMemory`+`File` con escritura atómica, `Workflow.run(checkpoint_id=…)`); HITL por `request_info` + `@response_handler` + `IDLE_WITH_PENDING_REQUESTS`; **OpenTelemetry de primera clase** (spans `workflow.run`/`executor.process`/`edge_group.process`/`message.send`); **evaluación en core** (`Evaluator`, `evaluate_agent`, `evaluate_workflow`, `EvalItem.expected_tool_calls`, `RubricScore`) pero **todo `@experimental(EVALS)`**; `ContextProvider` con hooks `before_run`/`after_run` y `HistoryProvider`/`VectorStoreHistoryProvider`; DevUI self-declarado **no** production; durabilidad de hosting vive en un repo aparte | Código (`main`, `agent-framework-core` 1.19.0) | EXTERNAL_CODE / EXTERNAL_DOC |
| P4 | `microsoft/amplifier-context-intelligence` | Plataforma de **telemetría/observabilidad** con grafo en Neo4j (`README.md:3`); **no** es contexto semántico: sin stable/dynamic, sin identidad/versionado de contexto, sin scoring de relevancia, sin prompt cache integration, sin evaluación de calidad. Identidad de nodo `f"{session_id}__{safe_event}__{epoch_ms}"` (`utils.py:94-131`). Durabilidad **de ingesta**: append-log por sesión, dead-letter, receipts SQLite con leases (`recovery.py:25-67`). Proyecto experimental sin soporte (`SUPPORT.md:5`), sin releases ni tags, 4 estrellas | Código y doc (clone read-only, `main` @ `c4fd590`) | EXTERNAL_CODE / EXTERNAL_DOC |
| P5 | `microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator` (slug nuevo; el anterior `…-Solution` responde 404) | Orquestación **in-process** con MAF Magentic (`MagenticBuilder` + `StandardMagenticManager`); **no** usa Azure Durable Functions — los matches de «durable» son dependencias transitivas en `uv.lock`, y el backend es `FastAPI` (`app.py:96`); `InMemoryCheckpointStorage()` (`orchestration_manager.py:185-195`); HITL obligatorio de aprobación de plan + clarificación `always_require` con `asyncio.Event` en proceso; **lista plana** de pasos sin DAG (`plan_models.py:23-41`), completitud por prompt (`plan_review_helpers.py:224-249`); `max_rounds=30`, `max_stall_count=5`, timeout 300 s, **sin** budget de tokens/costo; Azure Monitor + OTel + `track_event`; **sin** harness de evaluación en repo (la afirmación de eval offline es `docs/TRANSPARENCY_FAQ.md:12`, sólo doc); admisión por equipos declarativos JSON + allow-list MCP `DOMAIN_ALLOWED_TOOLS`; `agent_registry.py` es tracker de ciclo de vida, **no** gate. Gran parte del repo es scaffolding de acelerador (infra Bicep, 20+ workflows, UI) | Código (clone read-only, HEAD `c10216e`) | EXTERNAL_CODE / EXTERNAL_DOC |

### 12.3 Inferencias registradas

| Ref | Inferencia | Base |
|---|---|---|
| I-1 | `PR-1` (admisión de efectos) *causaría* un daño si el ejecutor produjera efectos sin autorización | La **ausencia del mecanismo** está verificada; la ocurrencia de un daño **no**. Es una inferencia arquitectónica, no un incidente observado |
| I-2 | `PR-2` (presupuesto de recurso) *causaría* consumo no acotado en operación desatendida | Misma estructura: ausencia verificada por código; materialidad operativa no observada (el host nunca corrió con invoker real) |
| I-3 | La conclusión de que las fuentes externas no aportan capacidades nuevas se apoya, en parte, en evidencia **negativa** | Greps negativos reproducibles citados (ACI: sin modelo de contexto ni scoring ni prompt cache; `prompty`: sin evaluación y sin versionado de prompt; MACAE: sin eval en repo; `agent-framework`: sin budget ni timeout en el camino core). No se descartó exhaustivamente cada directorio de cada repositorio |
| I-4 | `Execution Graph` no se justifica | Deriva de la ausencia de concurrencia y de la derivabilidad de las dependencias — ambas verificadas — más la evidencia adversa de MACAE (P5) sobre un framework que **sí** implementa el grafo (P3) |
| I-5 | El patrón «capacidad declarada sin realización» (P1, P3, P5) es el hallazgo transversal más citable de la comparación | Es una lectura de tres casos verificados en código, no una propiedad demostrada del ecosistema externo. No se generaliza más allá de esas tres fuentes |

### 12.4 Limitaciones de evidencia

1. **Los repositorios externos se inspeccionaron sin ejecutarlos.** Ninguna
   afirmación externa describe comportamiento observado en runtime: son lecturas
   estáticas de código y documentación en el commit/revisión citados. En
   particular, las afirmaciones «NOT_FOUND» y «sin realización» descansan en
   lecturas de código y greps negativos, no en una ejecución que demuestre la
   ausencia.
2. **No se ejecutó la batería canónica** en este trabajo: el Change es `READ_ONLY`
   y el análisis no lo requiere. La verificación de no-modificación se realizó por
   estado Git (§12.5). El baseline declara la batería verde en **dos cortes
   distintos**, ambos registrados en artefactos versionados, y las dos cifras son
   totales de la **suite completa**, no de un archivo:
   - **1010 passed** — corte de los planes 139/140/141
     (`docs/plans/139-sae-governance-boundary-closure.md:332`;
     `docs/plans/140-governance-residual-closure.md:393`;
     `docs/plans/141-human-decision-backlog-resolution.md:22`);
   - **1186 passed** — corte del Plan 149, `dev @ 820da21`
     (`docs/plans/149-argentos-capability-and-autonomy-roadmap.md:172`).

   La diferencia (176) es el crecimiento de `tests/` entre ambos cortes, registrado
   por los planes 141–147 (`git diff --stat 3b0a321..820da21 -- tests/`: 14 archivos,
   +2883 líneas, entre ellos `tests/test_check_ears_coverage*.py`).
3. **Tres premisas de partida quedaron corregidas** y se registran: (a) MACAE
   **no** usa Azure Durable Functions (P5); (b) `amplifier-context-intelligence`
   **no** es un sistema de contexto semántico sino una plataforma de telemetría
   (P4); (c) `prompty` **sí** define contratos de checkpoint/resume y **no**
   tiene versionado de prompt (P1). Cualquier conclusión anterior basada en las
   dos primeras premisas debe revisarse contra §4.
4. **Cobertura desigual entre runtimes y entre repositorios externos.** En
   `prompty` se leyó el runtime Python en profundidad y los otros seis se
   confirmaron por existencia de paths y tablas de propiedad del spec; en
   `agent-framework` no se leyó código .NET (sólo nombres de paquete); la
   durabilidad de hosting de `agent-framework` vive en un repositorio separado
   que no se inspeccionó; en MACAE el camino de durabilidad dentro de los
   paquetes MAF externos no se auditó (se verificó que MACAE **no** lo usa).
5. **Dos clasificaciones se sostienen por ausencia de necesidad demostrada**, no
   por evidencia positiva de valor: `Execution Graph`
   (`NOT_VALUABLE_FOR_ARGENTOS`) y evaluación comparativa (`POST_AUTONOMY`). Si
   apareciera evidencia de que el trabajo autorizado tiene ramas genuinamente
   independientes, la primera revisión sería la del grafo.
6. **El alcance externo fue acotado**: se inspeccionaron las partes necesarias
   para responder preguntas arquitectónicas concretas, según la instrucción del
   Plan. No se auditó exhaustivamente ningún repositorio externo, ni se
   inspeccionaron sus repositorios hermanos o dependencias de terceros
   (`swebench.harness`, `github-copilot-sdk`, `agent-framework-durable-extension`,
   paquetes MAF de durabilidad).

### 12.5 Verificación de read-only

El trabajo modificó **un único archivo**, el artefacto autorizado
(`docs/architecture-capability-review.md`). No se modificó `runtime/`,
`protocol/`, `.agents/`, `tools/`, `tests/`, CI, RFC, ADR, `ROADMAP.md`,
`VERSION`, `CHANGELOG.md`, Plan 149, releases ni tags. No se crearon archivos
temporales dentro del repositorio. No se crearon commits, tags, releases ni push.
No se corrigió ningún finding detectado durante el análisis.

**Evidencia registrada (ejecutada al cierre, sobre el árbol final):**

| Verificación | Resultado |
|---|---|
| `git status --porcelain` | `?? MASTER_PENDING_WORK_INVENTORY.md` (untracked **preexistente, ajeno** al Change) y `?? docs/architecture-capability-review.md` (el artefacto autorizado). Ninguna otra entrada |
| `git diff --name-only HEAD` | **vacío** — 0 modificaciones rastreadas |
| `git diff --cached --name-only` | **vacío** — 0 archivos staged |
| Búsqueda de temporales (`*.tmp`, `*.orig`, `*.rej`, `*.bak`) fuera de `.git/` | **ninguno** |
| `python tools/check_protocol_invariants.py --payload protocol .` | PASS — 215 archivos, 10334 referencias verificadas |
| `python tools/check_plan_structure.py` | PASS — sin violaciones estructurales |
| `python tools/check_taxonomy_coherence.py` | PASS |
| `python tools/check_plan_citations.py` | PASS — ninguna cita `ruta:sección` rota |
| `python tools/check_session_artifacts.py` | PASS |

Rama `dev`, HEAD `820da21` (sin cambio). **Fase 1 (F6):** el artefacto **no** es un
documento numerado de `docs/plans/` y **no** requiere fila en `docs/plans/INDEX.md`
—su clase es `Working / Analysis`, no `Governance / Plan`—, pero **sí** queda
pendiente una decisión: su registro y su ubicación física son `HD-INT-G`
(`HUMAN_DECISION_REQUIRED`). Si el mantenedor decide que entra al repositorio, su
namespace canónico es `docs/working/audits/` y su INDEX es
`docs/working/audits/INDEX.md`. La batería canónica completa y los gates C-1/C-2/C-3
pertenecen al Change gobernante que consuma este análisis, no a este documento.

> **REQUIRES_HUMAN_DECISION — `HD-INT-G`.** Cómo se registra este análisis en la
> gobernanza (¿entra como artefacto `Working` registrado? ¿como provenance de un
> Change? ¿permanece externo al repositorio?) no es una cuestión que este documento
> pueda resolver: crearlo, registrarlo o autorizarlo es autoridad del mantenedor
> (`PC-52`), y la excepción de ubicación —si se mantiene la ruta actual— debe
> registrarse en un artefacto autorizante, atribuible y auditable (`PC-27`; `PC-28`
> para una segunda instancia). El análisis queda entregado como artefacto de
> evidencia.

El estado Git y el diff acotado se registran en el informe de cierre de este
trabajo, no en este documento (que es un artefacto de análisis, no un registro de
ejecución).
