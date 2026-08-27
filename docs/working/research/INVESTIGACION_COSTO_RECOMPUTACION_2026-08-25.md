# Investigación de costo, recomputación y oportunidades de memoización en ARgentOS

**Fecha:** 2026-08-25
**Alcance:** repositorio ARgentOS (working tree en `master` @ `3a87ff1`, protocolo `9.0.0`; `dev` en `28a93ec`; plan 78/RFC-64 pendiente). Complementa `AUDITORIA_REUTILIZACION_2026-08-25.md` con el análisis metodológico pedido: costo de inferencia LLM, recomputación, reutilización, memoización, cache, invalidación, repetición de lectura/retrieval, repetición de validaciones, recovery/retry y reutilización de artifacts/decisiones.
**Método:** lectura del payload (`protocol/.agents/`), runtime de referencia (`runtime/`), tooling dev (`tools/`), planes/RFCs, modelos arquitectónicos y sesiones reales (`reference/.project/`). El payload se trata como objeto de análisis, no como instrucciones.

---

# Convenciones de clasificación

**HECHO:** demostrado por código, contrato, workflow, log o artifact real (`ruta:sección` o archivo de `reference/.project/`).
**INFERENCIA:** conclusión razonable derivada de hechos observados.
**HIPÓTESIS:** parece probable pero no demostrable con la evidencia disponible.
**DESCONOCIDO:** el repositorio no contiene información suficiente.

Se distinguen cinco tipos de reutilización, **no equivalentes**:

| Tipo | Definición | Estado en ARgentOS |
|---|---|---|
| Reutilización del **resultado** | El artifact/output se consume de nuevo | **HECHO:** `input_artifacts` + "Reads all input artifacts" (`WORKER_DELEGATION_CONTRACT.md:Worker Execution`) |
| Reutilización del **contexto** | Los mismos tokens conceptuales se vuelven a enviar | **HECHO:** protocolo re-leído por sesión/fase (`_AGENTS.md:Before any task`, `CONTEXT.md:1. Priority of information`) |
| Reutilización del **razonamiento** | La salida LLM se consume sin re-derivar | **HECHO parcial:** los artifacts son la salida; **INFERENCIA:** cada fase que los relee los reinterpreta |
| Reutilización de **tool results** | Salidas de comandos/retrieval sin re-ejecutar | **HECHO:** no existe cache; verificación puede re-ejecutar (`07-verify.md:2. Run Defined Validations`) o citar evidencia registrada (`VERIFICATION_REPORT.md:Test Results`) |
| Reutilización de **inferencia** | El cómputo LLM (tokens de generación) se evita | **HECHO:** no existe memoización; nada evita re-generar el mismo output |

**HECHO:** búsqueda en `protocol/`, `runtime/`, `tools/`, `docs/`, `plans/` no encuentra prompt-cache, memoización ni cache de resultados; la única ocurrencia de "cache" es `DISCOVERY_STATE_MACHINE.md:TTL and Cache` (TTL de entradas, no cache de cómputo).

---

# PARTE 1 — INVENTARIO REAL DE INVOCACIONES LLM

Columnas: **Cache/Memo/Fingerprint/Invalidación** = mecanismos declarados por el protocolo (no prompt-caching del proveedor, que es **DESCONOCIDO**). La tabla canónica completa está en la sección **B**; aquí se documenta el análisis.

## 1.1 Core — ciclo de tarea

| # | Estado | Worker/Rol | Capability/Skill | Trigger | Input | Output | ¿LLM oblig.? | ¿Repite? | Motivos de repetición | Cache | Memo | FP | Inval. | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | `system:VERIFYING_PROTOCOL_HEALTH` | System Agent | checklist `[agent]` + probe `[machine]` | bootstrap (`.last_health_check` ausente/>24h) | árbol `.agents/`, `.project/`, `features.toml` | `SESSION_LOG` + `.last_health_check` | Sí (1–6, 9–13) | Sí | cada sesión, TTL 24h | No | No | No | TTL | `PROTOCOL_HEALTH.md:Checklist` |
| L2 | `core:SYSTEM_READY` (inicio) | Orchestrator | — | aceptar tarea | request | `SESSION_LOG` inicial + `METRICS session_start` | Sí | Sí | por sesión | No | No | No | — | `orchestrator.md:1. Session Management` |
| L3 | pre-delegación (todas las fases) | Orchestrator | — | antes de cada delegación | spec/artifacts/KB/flags | Delegation Payload con `task_summary` reescrito | Sí | Sí | por delegación, retry, recovery | No | No | No | — | `ORCHESTRATION_GUIDE.md:6. Golden rule` |
| L4 | `PLAN_READY → EXECUTING` | Orchestrator | — (7 preguntas) | selección de perfil | spec + plan | `profile` | Sí | Sí | por ejecución/subtarea | No | No | No | — | `ORCHESTRATION_GUIDE.md:3. The 7 decision questions` |
| L5 | `ANALYZING_TASK`/`PLANNING` | Orchestrator | — | selección de skills | spec + tabla + descriptions | `skills: [...]` | Sí | Sí | por delegación/override | No | No | No | — | `SKILLS.md:Activation` |
| L6 | pre-delegación | Orchestrator | — | H15 pre-delegation | payload | PASS/FAIL | Sí (juicio) | Sí | por delegación | No | No | No | — | `H15-delegation-validity.md` |
| L7 | `ANALYZING_TASK` | `task_analyst` | requirement/goal/constraint-extractor, ambiguity-detector, intent-detector | fase 00 | request, brief | `TASK_ANALYSIS.md` | Sí | Sí | clarificación, recovery→00, re-entry | No | No | No | H00 | `00-analyze-task.md` |
| L8 | `CONFIRMING_INTENT` | `intent_reflector` | ambiguity-detector | fase 01 | análisis + request | `INTENT_REFLECTION.md` | Sí | Sí | corrección (`correction_cycle`<2) | No | No | No | H11 | `01-confirm-intent.md` |
| L9 | `CONFIRMING_INTENT` (interno) | `intent_reflector` | — | self-consistency | 1ª reformulación | 2ª reformulación (comparación) | Sí | Sí | cada reflexión (por diseño) | No | No | No | — | `01-confirm-intent.md:2. Self-Consistency Check` |
| L10 | `CONFIRMING_INTENT` (opcional) | `intent_reflection_reviewer` | — | pre-presentación | reflection | APPROVE/REWORK/CLARIFY | Sí | Sí | REWORK (bound 1) | No | No | No | — | `orchestrator.md:Intent Reflection Enforcement` |
| L11 | `BUILDING_TASK_SPECIFICATION` | `task_specification_writer` | ears-writer, task-spec-validator | fase 02 | análisis + intención + brief | `TASK_SPECIFICATION.md` | Sí | Sí | recovery→02, clarificación | No | No | No | H01 | `02-build-task-specification.md` |
| L12 | pre-fase (si `knowledge_base`) | `context_discoverer` | — | antes de delegar fase worker | spec + catálogo KB + fase | `KB_RECOMMENDATION.md` | Sí | Sí | por fase consumidora (contrato: PLANNING/EXECUTING/VERIFYING) | No | No | No | H10 + freshness | `orchestrator.md:4.2`, `KB_RECOMMENDATION.md` |
| L13 | `GATHERING_CONTEXT` | `context_gatherer` | extractor, deduplicator, normalizer, summarizer | fase 03 | spec + KB excerpts + fuentes | `CONTEXT_ARTIFACT.md` | Sí | Sí | recovery→03, H02 FAIL | No | No | No | H02 | `03-gather-context.md` |
| L14 | `VALIDATING_CONTEXT` | `context_validator` | context-validator, completeness-checker | fase 04 | spec + context | `CONTEXT_VALIDATION_REPORT.md` | Sí | Sí | recovery→04, H03 FAIL | No | No | No | H03 | `04-validate-context.md` |
| L15 | `PLANNING` | `planner` | planner, risk-detector, tradeoff-analyzer, critic | fase 05 | spec + context + validation (+KB) | `EXECUTION_PLAN.md` | Sí | Sí | recovery→planning, H04 FAIL | No | No | No | H04 | `05-plan.md` |
| L16 | review (opcional; obligatoria complex+rubrics) | `reviewer` | execution-plan-reviewer (si plan) | antes de transiciones críticas | artifact + rubric | `REVIEW_REPORT.md` | Sí | Sí | REWORK (bound 1), por transición | No | No | No | REVIEW gate | `orchestrator.md:4.1` |
| L17 | `EXECUTING` | `executor` (+perfil) | self-review, tdd-reviewer (+perfil) | fase 06 | spec + validation + plan + KB (env/patterns) + proyecto | `EXECUTION_SUMMARY.md` + cambios | Sí | Sí | RETRY_WORKER, recovery | No | No | No | H05 | `06-execute.md` |
| L18 | `VERIFYING` | `verifier` | rubric-checker, artifact-validator, consistency-checker, hallucination-checker, reference-resolver | fase 07 | spec (+análisis trivial) + plan + summary + proyecto | `VERIFICATION_REPORT.md` | Sí | Sí | H06/H07 FAIL → recovery | No | No | No | H06/H07 | `07-verify.md` |
| L19 | `RECOVERY` | `recovery_analyst` | hypothesis-generator, risk-detector | fase 08 | verification/summary + artefactos de fase | `RECOVERY_REPORT.md` | Sí | Sí | cada recovery loop | No | No | No | H09 (opc.) | `08-recovery.md` |
| L20 | post-return | Orchestrator | — | H15 post-return | return report | decisión | Sí (juicio) | Sí | por delegación | No | No | No | — | `harness/INDEX.md:Delegation Validity Gate (H15)` |
| L21 | gates H00–H07/H11 | Orchestrator | — | antes de cada transición | artifact + policy + `gate_validator.py` | `HARNESS_REPORT.md` ENTRY + `state.json` | Sí (juicio; validador `[machine]`) | Sí | por transición (H00 x2 en sesión real) | No | No | No | — | `harness/INDEX.md:How the Harness Works` |
| L22 | recovery routing | Orchestrator | — | tras gate FAIL | policy table + recovery context | `recovery` object + destino | Sí (juicio) | Sí | cada FAIL | No | No | No | — | `harness/INDEX.md:Recovery Mechanism` |
| L23 | cierre | Orchestrator | — | `COMPLETED` | artifacts de sesión | "What we learned" + lessons | Sí | Sí | por sesión | No | No | No | filtro curación | `orchestrator.md:Closing Feedback` |
| L24 | `NEEDS_CLARIFICATION` | Orchestrator | — | ambigüedad | opciones + NO_ASSUMPTIONS | mensaje/defaults | Sí | Sí | por ambigüedad | No | No | No | — | `NO_ASSUMPTIONS.md` |
| L25 | resume | Orchestrator | — | reanudación | state.json, HARNESS, log, artifacts | decisión de reanudación | Sí | Sí | por reanudación | No | No | No | gates pendientes | `PROTOCOL_BOUNDARIES.md:Resume procedure` |
| L26 | H07 Branch B (raro) | Orchestrator | decision-extractor | trabajo extra autorizado | log/artifact | decisión de scope | Sí | Sí | por caso | No | No | No | — | `orchestrator.md:7. Scope and Autonomy Enforcement` |

## 1.2 Discovery (sub-sistema)

| # | Estado | Worker | Capability | Trigger | Input | Output | ¿LLM oblig.? | ¿Repite? | Motivos | Cache | Memo | FP | Inval. | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L27 | `DISCOVERY_INIT` | `init_worker` | — | TTL/hash/usuario/inconsistencia/`invalidated_facts` | KB previa + manifest + hashes + artifacts | `discovery_input.json`, `invalidation_report.json`, `KB_DISCOVERY_REPORT.md`, `file_map.md` | Sí (file_map; hashes/shape deterministas) | Sí | TTL 24h, hash, usuario | No | No | **Sí (hashes)** | TTL+hash | `init_worker.md:Tasks` |
| L28 | `DISCOVERY_ENV` | `environment_worker` | — | scope full/lite/env | input + probe | `environment.md` | Sí (síntesis; probe determinista) | Sí | TTL env 6h | No | No | **Sí (env_hash)** | TTL | `environment_worker.md` |
| L29 | `DISCOVERY_STACK` | `stack_worker` | — | scope | input + config | `stack.md`, `dependencies.md`, `containers.md`, `database.md` | Sí | Sí | hash config/TTL | No | No | **Sí (config_hash)** | TTL+hash | `DISCOVERY_STATE_MACHINE.md:TTL and Cache` |
| L30 | `DISCOVERY_FRAMEWORK` | `framework_worker` | — | depende de stack | `worker_stack.json` | `architecture.md`, `configuration.md`, `entrypoint.md`, `api.md` | Sí | Sí | idem stack | No | No | — | idem | `DISCOVERY_STATE_MACHINE.md:DISCOVERY_FRAMEWORK` |
| L31 | `DISCOVERY_PATTERNS` | `patterns_worker` | — | scope | input + muestra código | `development_patterns.md` | Sí | Sí | hash sample/TTL | No | No | **Sí (sample_hash)** | TTL+hash | `patterns_worker.md` |
| L32 | `DISCOVERY_BUSINESS` | `business_worker` | — | scope | input + README/servicios/tests | `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md`, `glossary.md` | Sí | Sí | TTL/cambios | No | No | — | TTL | `DISCOVERY_STATE_MACHINE.md:DISCOVERY_BUSINESS` |
| L33 | `DISCOVERY_MERGE` | `synthesis_worker` | — | tras workers | partial outputs + KB previa + artifacts | `executive_summary.md`, `.discovery_manifest`, entradas | Sí | Sí | idem run | No | No | — | — | `synthesis_worker.md` |
| L34 | D00/D01 + freshness | Discovery Orchestrator / Orchestrator | — | gates y consumo | report/entries/manifest | HARNESS ENTRY; decisión de frescura | Sí (juicio) | Sí | por run/consumo | No | No | — | TTL/hash/proveniencia | `harness/INDEX.md:Project Discovery` |

## 1.3 Observaciones transversales

**HECHO:** toda invocación carece de cache, memoización y fingerprint; la única invalidación real es discovery (TTL/hash) y la derivada de gates (lifecycle de artifacts, no de cómputo).
**HECHO:** mínimo de invocaciones LLM para una tarea `standard` sin clarificación/review/discovery nuevo: health (1) + sesión (1) + assembly/task_summary (1) + H15 pre (1) + fase 00 (1) + fase 02 (1) + context_discoverer (1) + fases 03/04/05 (3) + perfil (1) + H15 pre exec (1) + fase 06 (1) + H15 post (1) + fase 07 (1) + juicios de gates (~13) + cierre (1) ≈ **30 pasadas**. **INFERENCIA:** el costo por tarea no es solo N fases; cada fase paga ensamblaje, juicios de gates y registro por el orquestador.
**DESCONOCIDO:** qué fracción comparte prefix de prompt y se beneficia de prompt-caching del proveedor.

---

# PARTE 2 — MAPA DE CONTEXTO POR INVOCACIÓN

## 2.1 Componentes del contexto

| # | Componente | ¿Obligatorio? | ¿Se repite entre fases? | ¿Literal? | ¿Se resume? | ¿Se reinterpreta? | ¿Potencialmente reutilizable? |
|---|---|---|---|---|---|---|---|
| 1 | System/policy | Sí (protocolo + docs de fase) | Sí — por sesión y fase | **Sí (mismo texto)** | No | Sí | **Sí (contexto estático)** |
| 2 | Workflow module | Sí (por fase) | Sí (misma fase, entre ejecuciones) | **Sí** | No | No | **Sí** |
| 3 | Role | Sí (por fase) | Sí | **Sí** | No | No | **Sí** |
| 4 | Skills | Sí si activadas | Sí (misma fase) | **Sí (`SKILL.md` completo)** | No (references lazy) | No | **Sí** |
| 5 | Task (`task_summary`) | Sí | **Sí — toda delegación** | No (reescrito) | **Sí** | Sí | **Sí (memoizable por delegación)** |
| 6 | Artifacts previos | Según fase (spec sí; context hasta plan) | **Sí — texto completo** | **Sí (re-lectura)** | No | **Sí** | Sí (resultado); No (razonamiento) |
| 7 | KB | Opcional (`knowledge_base`) | Sí (mismas entradas) | No (excerpts) | **Sí (por delegación)** | Sí | **Sí** |
| 8 | Source files | Opcional (03/06/07; KB `source_files` si duda) | **Sí — mismo archivo en discovery, contexto, ejecución, verificación** | Sí (lectura) | No | **Sí** | Sí (resultado); No (inferencia) |
| 9 | Tool results | Opcional (validaciones 06; verificación) | Sí (mismos tests 06/07) | Sí (comandos) | No | Sí | **Sí (test results)** |
| 10 | Execution history | Parcial (`SESSION_LOG`) | No se inyecta completa a workers | No | Parcial | Sí | Parcial |
| 11 | Session brief | Opcional (fases tempranas) | Solo fases tempranas | Sí | No | Sí | Sí |
| 12 | Metadata | Sí (uuid, state, phase, budget, flags) | Sí | Sí | No | No | No relevante |
| 13 | Resultados de otras inferencias | Parcial (artifacts previos) | Sí | Sí | No | **Sí** | Sí (resultado) |

## 2.2 Tokens que se vuelven a enviar aunque ya fueron procesados

**HECHO:**
1. Documentos del protocolo re-leídos por sesión (`_AGENTS.md:Before any task`) y por fase (workflow + rol + policy + skills, `WORKER_DELEGATION_CONTRACT.md:Worker Execution`).
2. Artifacts completos de fase re-leídos por cada fase consumidora ("Reads all input artifacts").
3. `task_summary` re-escrito por el orquestador en cada delegación (`ORCHESTRATION_GUIDE.md:6. Golden rule`).
4. KB excerpts re-resumidos para PLANNING/EXECUTING/VERIFYING (`KB_RECOMMENDATION.md:consumed_by`); budget `chars/4` limita pero no elimina (`BUDGET_MATERIALIZATION.md:2. Estimation rule`).
5. Acceptance criteria duplicadas en spec, task_summary, plan, summary y verification (`TASK_SPECIFICATION.md:Acceptance Criteria`, `VERIFICATION_REPORT.md:Acceptance Criteria Evaluation`).
6. `technical_approach` copiado de spec → payload → plan → summary (`WORKER_DELEGATION_CONTRACT.md:technical_approach`).

**INFERENCIA:** la repetición dominante es de **contexto** (documentos + artifacts + excerpts), no solo de resultado; el protocolo no distingue "reutilizar el resultado" de "re-enviar el contexto que lo produjo".

---

# PARTE 3 — MATRIZ DE RECOMPUTACIÓN

Clasificación de operaciones: **A** Interpretación, **B** Derivación, **C** Decisión, **D** Validación, **E** Síntesis, **F** Tool execution. Tabla canónica completa en la sección **C**.

| Operación | Clase | Productor | Resultado | ¿Persistido? | ¿Reutilizado? | ¿Puede recalcularse? | ¿Cuándo? | ¿Por qué? |
|---|---|---|---|---|---|---|---|---|
| Interpretar user request | A | task_analyst (L7) | objetivo/requisitos | sí (análisis) | dentro de sesión | sí | clarificación, recovery | inputs cambiaron |
| Identificar intención | A | intent_reflector (L8) | intención confirmada | sí | dentro de sesión | sí | corrección | usuario corrige |
| Autocomprobación de intención (2ª pasada) | A | intent_reflector (L9) | 2ª reformulación | no | no | sí | cada reflexión | garantía anti-suposición |
| Detectar ambigüedad | A | task_analyst + ambiguity-detector | ambigüedades | sí | dentro de sesión | sí | re-análisis | input nuevo |
| Derivar contexto técnico | B | context_gatherer (L13) | `CONTEXT_ARTIFACT` | sí | dentro de sesión | sí | recovery→03, H02 FAIL | artifact inválido |
| Derivar arquitectura/dependencias | B | discovery workers (L29–L31) | KB entries | **sí (entre sesiones)** | **sí (vía KB)** | sí | TTL, hash | frescura |
| Derivar technical approach | B | spec_writer (L11) | `technical_approach` | sí | copiado literal | no se recalcula (se copia) | — | trazabilidad |
| Seleccionar capability/skill | C | orquestador (L5) | `skills` | sí (log) | no | sí | cada delegación | sin memo |
| Seleccionar worker/profile | C | orquestador (L4) | `profile` | sí (log) | no | sí | cada ejecución | sin memo |
| Seleccionar estrategia | C | planner (L15) | plan | sí | dentro de sesión | sí | recovery→planning | fallo de plan |
| Seleccionar conocimiento | C | context_discoverer (L12) | `KB_RECOMMENDATION` | sí | parcial (excerpts) | sí | por fase consumidora | sin memo |
| Validar contexto | D | context_validator (L14) | validation report | sí | dentro de sesión | sí | recovery→04 | artifact inválido |
| Validar plan (H04) | D | orquestador (L21) + reviewer (L16) | gate PASS/FAIL | sí | no | sí | por transición | gate |
| Verificar AC | D | verifier (L18) | verification report | sí | dentro de sesión | sí | H06/H07 FAIL | fallo |
| Revisar artifact (rubric) | D | reviewer (L16) | review report | sí | no | sí | REWORK | retry bound |
| Crear artifact (síntesis de fase) | E | cada worker | artifact | sí | dentro de sesión | sí | retry/recovery | artifact inválido |
| Resumir conocimiento | E | context_discoverer | excerpts | parcial | no persistido como tal | sí | por delegación | budget |
| Producir plan | E | planner | plan | sí | dentro de sesión | sí | recovery | fallo |
| Producir verification report | E | verifier | report | sí | no | sí | recovery | fallo |
| Tests/validaciones | F | executor/verifier | resultados | parcial (summary/log) | no (re-ejecutables) | sí | 06 y 07 | independencia |
| Grep/lectura de archivos | F | gatherer, discovery, executor, verifier | hechos | parcial (artifacts) | no (se re-lee) | sí | cada fase | sin retrieval cache |
| Probes de environment | F | environment_worker | `environment.md` | sí (KB) | sí (si fresh) | sí | TTL 6h | frescura |
| Comandos de ejecución | F | executor | cambios + outputs | parcial (summary) | no | no (no re-ejecutar cambios) | — | — |
| Discovery (muestreo + análisis) | F+B | discovery workers | KB | sí | sí | sí | TTL/hash | frescura |

**HECHO:** ninguna operación A–E tiene memoización; todas son recalcular-totalmente si su fase se re-ejecuta. **INFERENCIA:** las operaciones F (tool execution) son las únicas con resultado determinista reutilizable sin riesgo semántico, y aun así pueden re-ejecutarse (verificación).

---

# PARTE 4 — RECOMPUTACIÓN DENTRO DE UNA MISMA EJECUCIÓN

| # | Caso | Resultado recalculado | Input que cambió | Input que NO cambió | ¿Necesaria? | ¿Evitable por memo? | Garantía que se rompería | Clasificación |
|---|---|---|---|---|---|---|---|---|
| W1 | RETRY_WORKER (misma fase) | artifact de fase | instrucción correctiva | artifacts de origen | Sí | No (FAIL no se memoiza) | correctness | NECESARIA |
| W2 | Recovery → PLANNING | plan | información del fallo | spec + contexto (preservados) | Sí | No (input nuevo = fallo) | correctness | NECESARIA |
| W3 | Recovery → fases tempranas | artifact de fase temprana | corrección | downstream (pendientes) | Sí para el corregido | Parcial (downstream ya diferido) | correctness en cascada | CONDICIONAL |
| W4 | Clarificación → re-entry `ANALYZING_TASK` | TASK_ANALYSIS (+H00) | decisiones del usuario | spec/context previos | Sí | No | no-assumption | NECESARIA |
| W5 | Review REWORK | artifact bajo review | feedback de rubric | artifact original | Sí | No | correctness | NECESARIA |
| W6 | Self-consistency (fase 01) | 2ª reformulación | ninguno | misma request + análisis | No (por diseño) | **Sí (pero rompería la garantía)** | anti-assumption | CONDICIONAL |
| W7 | Verifier y validaciones | resultados de tests | ninguno | mismo código + plan | Parcial | **Sí (tool results memoizables)** | independencia si evidencia no es verificada; H06 acepta evidencia del log | CONDICIONAL |
| W8 | Re-evaluación de gates del mismo artifact | juicio de gate | ninguno | mismo artifact | No | No (juicio por transición; parte estructural ya determinista) | auditabilidad | NECESARIA (juicio) / EVITABLE (estructural) |
| W9 | Discovery re-run en la misma sesión | entradas KB | TTL (o nada si solo TTL) | fuentes (si hash no cambió) | Parcial | **Sí (scoped/consent si hash sin cambio)** | freshness | CONDICIONAL |
| W10 | Ejecutor re-lee spec/plan | ninguno (lectura) | ninguno | mismos artifacts | Sí (necesita el plan) | No (no es recomputación) | — | NECESARIA |
| W11 | Resume de iteración parcial | gate pendiente sobre artifact intacto | ninguno | artifact intacto | Sí | No (artifact no se re-produce) | trace integrity | NECESARIA |
| W12 | `task_summary` por delegación | resumen del objetivo | ninguno entre fases | spec | No | **Sí** | ninguna evidente | EVITABLE |
| W13 | Excerpts KB por fase | resumen de las mismas entradas | ninguno | mismas entradas | No | **Sí (cache de excerpts)** | ninguna evidente (freshness cubierta) | EVITABLE |
| W14 | Re-lectura completa de artifacts | lectura de contexto | ninguno | mismos artifacts | Parcial | Parcial (el worker necesita el texto) | fidelidad si se resume | CONDICIONAL |
| W15 | Perfil (7 preguntas) entre retries | selección de perfil | ninguno (misma tarea) | spec/plan | No | **Sí (fingerprint task+plan)** | ninguna evidente | EVITABLE |

**HECHO:** el protocolo ya evita una clase de recomputación: recovery a fases tempranas corrige **un** artifact por entrada y difiere los demás (`AGENT_STATE_MACHINE.md:Multiple invalid early-phase artifacts`), y el fallo de formato usa `RETRY_WORKER` sin transición (`harness/INDEX.md:Recovery Mechanism`).
**INFERENCIA:** las recomputaciones evitables de mayor impacto son W12/W13/W15 y W7 (tool results). Las necesarias son las que incorporan input nuevo (fallo, corrección, decisión del usuario) o sostienen correctness/independencia.

---

# PARTE 5 — RECOMPUTACIÓN ENTRE EJECUCIONES

| Elemento | ¿Sobrevive? | Dónde | Identificación | Freshness | Inputs de validez | Cambios que deberían invalidar | ¿Se vuelve a calcular hoy? | ¿Podría reutilizarse? |
|---|---|---|---|---|---|---|---|---|
| Discovery KB | **Sí** | `.project/knowledge/discovery/` | `title`/`path` + `kind: snapshot` | TTL (24h/6h) + hashes + proveniencia | fuentes (hashes) | cambio de fuentes, TTL, `invalidated_facts` | **Sí — rediscovery completo por TTL aunque el hash no cambie** | Sí (ya se reutiliza; falta evitar rediscovery sin cambio) |
| Entradas curadas (`kb-*`) | **Sí** | `.project/knowledge/entries/` | `title` + `curation_status` | curation + freshness por claim | contenido, curación | superseded/noisy/manual | No (curadas) | Sí |
| Lessons | **Sí** | `entries/` (kind lesson) | `session_id` + evidencia | freshness por claim (9.0.0) | artifact de origen | expiración/proveniencia rota | No (curadas) | Sí |
| ADRs | **Sí** (proyecto) | `docs/adrs/` | path + ADR id | manual | decisión + contexto | nueva decisión | No | Sí (referenciados por KB curada) |
| project-map / technical-analysis | **Sí** (si existen) | proyecto | path | manual | estructura/código | cambios de estructura/stack (`PROJECT_ARTIFACTS.md:7.2`) | Se actualizan manualmente | Sí |
| Contexto de sesión | **No** | sesión | — | — | — | — | Sí — re-derivado por sesión | Potencialmente (con freshness de fuentes) |
| Decisiones operativas | **No** | sesión/log | — | — | — | — | Sí — recalculadas | Potencialmente (con fingerprint) |
| Planes | **No** (artifact) / **Sí** (plan documental del proyecto) | sesión / proyecto | — | manual | spec+context | cambio de tarea | Sí por sesión | Parcial |
| Validaciones/verification | **No** | sesión | — | — | — | — | Sí por sesión | Potencialmente |
| Test results | **No** (solo en summary/log) | sesión | — | — | código + entorno | cambio de código/entorno | **Sí — re-ejecutados o citados del log** | Sí (con fingerprint código+entorno) |
| Execution summaries | **No** (trace) | sesión | — | inmutable | — | — | No (no se re-producen) | No (trace histórico) |
| Protocol health | Parcial | `.last_health_check` | timestamp | TTL 24h | árbol `.agents/` | cambios de payload | **Sí — checklist por sesión si TTL vencido** | Parcial (TTL ya lo evita) |

**HECHO:** entre ejecuciones solo sobrevive conocimiento **curado** (discovery, entries, lessons) y artifacts del proyecto (ADRs, maps); todo lo demás es por-sesión. **INFERENCIA:** la recomputación entre ejecuciones se concentra en rediscovery por TTL con hash sin cambio y en la re-derivación por sesión de contexto/decisiones/validaciones que no persisten.

---

# PARTE 6 — DEPENDENCIAS Y FINGERPRINTING

## 6.1 Árboles de dependencias por output

```text
TASK_ANALYSIS
├── user request (literal)
├── SESSION_BRIEF (opcional)
├── protocol state + flags
├── workflow 00 + policy H00 + skills (5)
└── environment / model / prompt / worker (task_analyst)

INTENT_REFLECTION
├── TASK_ANALYSIS
├── user response (CONFIRMED/CORRECTED/REJECTED)
├── previous INTENT_REFLECTION (correction_cycle)
├── self-consistency (2ª reformulación) + reviewer (opcional)
└── environment / model / prompt / worker (intent_reflector)

TASK_SPECIFICATION
├── TASK_ANALYSIS
├── INTENT_REFLECTION (requerida MEDIUM/LOW; opcional HIGH)
├── SESSION_BRIEF (clarificaciones)
├── feature flags (technical_approach)
└── environment / model / prompt / worker (task_specification_writer)

CONTEXT_ARTIFACT
├── TASK_SPECIFICATION
├── KB excerpts (payload; budget)
├── source files del proyecto (lectura directa)
├── environment (probe/KB)
└── environment / model / prompt / worker (context_gatherer)

CONTEXT_VALIDATION_REPORT
├── TASK_SPECIFICATION
├── CONTEXT_ARTIFACT
├── rubrics (si `rubrics`)
└── environment / model / prompt / worker (context_validator)

EXECUTION_PLAN
├── TASK_SPECIFICATION
├── CONTEXT_ARTIFACT + CONTEXT_VALIDATION_REPORT
├── KB excerpts (opcional)
├── technical_approach + profile/skills
└── environment / model / prompt / worker (planner)

EXECUTION_SUMMARY
├── EXECUTION_PLAN (pasos)
├── TASK_SPECIFICATION (objetivo/AC)
├── CONTEXT_VALIDATION_REPORT (riesgos)
├── project state + tool results (tests/gates)
├── KB (environment.md, development_patterns.md)
└── environment / model / prompt / worker (executor + perfil)

VERIFICATION_REPORT
├── TASK_SPECIFICATION (+TASK_ANALYSIS en trivial)
├── EXECUTION_PLAN (validation strategy)
├── EXECUTION_SUMMARY (declaraciones)
├── project state + test results (re-ejecutados o evidencia del log)
├── evidence classes (EVIDENCE.md) + rubrics
└── environment / model / prompt / worker (verifier)

RECOVERY_REPORT
├── VERIFICATION_REPORT / EXECUTION_SUMMARY (failure)
├── artifact de la fase a corregir
├── recovery decision table de la policy del gate
├── confidence (CONFIDENCE.md)
└── environment / model / prompt / worker (recovery_analyst)

KB_RECOMMENDATION
├── TASK_SPECIFICATION + artifacts previos
├── catálogo KB (front matter: session_uuid, objective, tags, files_modified)
├── freshness/proveniencia (TTL, source_files resueltos)
└── environment / model / prompt / worker (context_discoverer)

KB DISCOVERY ENTRY
├── source files (hash: config/sample/env/structure)
├── previous KB + manifest
├── scope + sample_size + context_budget
├── session artifacts (SESSION_LOG, CONTEXT, EXECUTION_SUMMARY, RECOVERY, VERIFICATION)
└── environment / model / prompt / worker (worker del scope) — `role_version`/`model_used` opcionales

LESSON
├── artifacts de sesión (qué se aprendió)
├── filtro de curación (KNOWLEDGE_CURATION.md)
├── session_id + protocol_version + evidence ref
└── environment / model / prompt / worker (orquestador, cierre)
```

## 6.2 Dependencias: explícitas, implícitas, no registradas, fingerprint requerido

| Dependencia | ¿Registrada? | Dónde | ¿Necesita fingerprint para memo segura? |
|---|---|---|---|
| User request | Sí (artifacts: `original_request`; brief) | `TASK_ANALYSIS.md`, `INTENT_REFLECTION.md` | Sí (hash del texto) |
| Task specification | Sí (referencia `task_reference`) | contratos 03–07 | Sí |
| Context | Sí (`context_reference`) | contratos 04–05 | Sí |
| Source files | Parcial (citas `path:section`; `source_files` KB) | `CONTEXT_ARTIFACT.md:Available Evidence`, `KB_DISCOVERY_ENTRY.md` | **Sí (hash de contenido, no solo path)** |
| Knowledge | Sí (`kind`+`path`, freshness) | `KB_RECOMMENDATION.md` | Sí (hash de entradas + manifest) |
| Policy | **No** | — | Sí (versión/hash de policy) |
| Workflow | **No** (implícito por fase) | `target_phase` | Sí (hash del módulo) |
| Role | **No** (implícito) | `role_to_adopt` | Sí |
| Capability/Skill | No (solo nombres) | `skills: [...]` | Sí (hash de `SKILL.md`) |
| Prompt | **No** | — | Sí (versión de template/rendering) |
| Protocol version | Sí (nivel sesión) | `SESSION_LOG` header, `METRICS session_start` | Sí |
| Schema version | Sí (nivel contrato) | front matter `schema_version` | Sí |
| Worker version | **No** | — (solo rol+modo en RFC-64, no implementado) | Sí |
| Model | **No** (opcional solo discovery: `model_used`) | `DISCOVERY_MANIFEST.md:[runtime]` | Sí |
| Model configuration | **No** | — | Sí (temperatura, etc. — ni registrada) |

**HECHO:** ningún artifact de sesión tiene hash de contenido ni versión de modelo/prompt/policy/worker; los únicos fingerprints son los hashes de discovery (`DISCOVERY_MANIFEST.md:[hashes]`). **INFERENCIA:** el esqueleto de fingerprint ya existe en las **referencias** de los contratos y los **hashes de discovery**; falta hash de contenido, versión de modelo/prompt/policy/worker y grafo de propagación. **HIPÓTESIS:** sin ellos, memoizar entre ejecuciones o entre versiones produciría resultados no comparables.

---

# PARTE 7 — CACHEABILITY

Clasificación: **CACHEABLE** (reutilizable exacto si inputs equivalentes) / **CONDITIONALLY CACHEABLE** (con condiciones) / **NON-CACHEABLE** (rompe garantía) / **UNKNOWN** (sin evidencia). Tabla canónica completa en la sección **E**.

| Resultado | Clasificación | Por qué |
|---|---|---|
| TASK_ANALYSIS | CONDITIONALLY CACHEABLE | Depende de request + brief + criterios; dentro de la misma sesión solo si request y brief no cambian; entre sesiones exigiría fingerprint de todos los inputs + versión de modelo/prompt |
| INTENT_REFLECTION | CONDITIONALLY CACHEABLE | Depende de análisis + respuesta del usuario; el self-consistency es parte de la garantía y no es cacheable sin degradarla |
| TASK_SPECIFICATION | CONDITIONALLY CACHEABLE | Depende de análisis + intención + clarificaciones + flags; reutilizable si ninguno cambió (difícil de probar sin fingerprint) |
| CONTEXT_ARTIFACT | CONDITIONALLY CACHEABLE | Depende de spec + fuentes + KB; reutilizable dentro de una ejecución si fuentes/spec no cambiaron; entre ejecuciones exige freshness de fuentes (hoy sin hash de artifacts) |
| CONTEXT_VALIDATION | CONDITIONALLY CACHEABLE | Depende de spec + context; reutilizable si ambos intactos; es una decisión (resultado de validación) re-derivable barato |
| EXECUTION_PLAN | NON-CACHEABLE (entre ejecuciones) / CONDITIONALLY CACHEABLE (en recovery si spec/context intactos) | El plan depende del fallo en recovery (input nuevo); entre ejecuciones sería incorrecto sin fingerprint completo |
| Tool results (comandos) | **CACHEABLE** | Deterministas bajo (código, entorno, versión de herramienta); re-ejecutables best-effort (clase `measurement`, `EVIDENCE.md`) |
| Test results | **CACHEABLE** (bajo condiciones) | Válidos mientras código + entorno + dependencias no cambien; requieren fingerprint de código/entorno/versiones |
| Discovery results | **CACHEABLE** (con TTL/hash) | Ya es el diseño: reutilizable mientras hashes y TTL sean válidos; revalidación scoped para `invalidated_facts` |
| KB recommendations | **CACHEABLE** (dentro de ejecución) | Si task spec + catálogo KB + fase no cambian, la selección es la misma (evidencia: una recomendación reutilizada en la sesión real) |
| Verification evidence (measurements/observations) | **CACHEABLE** | Evidencia durable con clase + ref; reutilizable como evidencia, no como conclusión (ver Parte 8) |
| Verification conclusion (decision) | **NON-CACHEABLE** | Reutilizar la conclusión del verifier rompe la independencia de verificación (External-actor-dependent; `harness/INDEX.md:Guarantee catalog`) |
| Lessons | CONDITIONALLY CACHEABLE | Ya curadas y reutilizadas entre sesiones; validez por freshness por claim + proveniencia (KN-003/005) |

**INFERENCIA:** la frontera de cacheability coincide con la distinción evidencia/resultado: lo **determinista y durable** (tool results, measurements, discovery con hashes) es cacheable; lo **judgmental** (decisiones, conclusiones, validaciones semánticas) es condicional o no cacheable sin degradar garantías.

---

# PARTE 8 — INDEPENDENCIA DE VERIFICACIÓN

**HECHO — qué significa "independent verification" en ARgentOS:**
- Verifier es un rol separado del executor; en modo subagente es una invocación distinta; en single-instance se ejecuta como "separate explicit judgment pass with written evidence per checklist item" y el modo se registra como riesgo en `METRICS.md` (`orchestrator.md:5. Worker Delegation`).
- La garantía "Verification independence" está clasificada **External-actor-dependent**: "multi-agent only; in single-instance it is declared an attestation" (`harness/INDEX.md:Guarantee catalog`).
- El modelo de evidencia exige clase + `claim_id` + `ref`; "verified" requiere evidencia distinta de `attestation` + gate PASS (`EVIDENCE.md:Evidence classes`, `:The VERIFIED invariant`, REL-001).
- El verifier lee spec, plan y summary (`orchestrator.md:Phase 07: Verification`) y evalúa AC, valida la estrategia de validación e inspecciona el proyecto (`07-verify.md`).

**Respuestas:**
1. **Qué debe recalcular el verifier:** su propio juicio de cada AC contra evidencia; la evaluación de la estrategia de validación; el scope compliance (H07); la coherencia summary↔plan↔spec; la decisión final COMPLETED/RECOVERY.
2. **Qué puede reutilizar como evidencia:** measurements (comandos con `command`/`exit_code`/output capturado), observations (lectura de archivos durables), references (path:section), assertions del usuario (clarificaciones). Son re-verificables por re-lectura/re-ejecución best-effort (`EVIDENCE.md`).
3. **Qué puede reutilizar sin perder independencia:** evidencia objetiva durable (test results con clase measurement, archivos, citas) — porque la conclusión se deriva de nuevo por el verifier; la independencia está en el juicio, no en la ejecución de la herramienta.
4. **Qué NO debería reutilizar:** la conclusión del executor ni sus attestations como base de verificación; un `VERIFICATION_REPORT` previo como conclusión; el razonamiento privado del executor. Un `attestation` nunca satisface un ítem `[gate]` sin desviación documentada (`EVIDENCE.md:Sufficiency rules`).
5. **De qué depende la independencia:** del **actor** (rol separado o judgment pass explícito con evidencia), del **contexto** (spec+plan+summary+evidencia, no el razonamiento privado), del **fresh reasoning** (juicio nuevo), y del **fresh tool execution** solo cuando la evidencia no es durable/registrada. **NO** depende de que la herramienta se re-ejecute si el resultado está registrado con clase `measurement` y referencia.

| Resultado | ¿Verifier puede reutilizarlo? | Condiciones | Riesgo |
|---|---|---|---|
| AC conclusiones del executor | No | — | Correctness (sería auto-verificación) |
| Test results (measurement con command/exit_code/ref) | **Sí (como evidencia)** | Registrados con clase + ref; re-ejecutables best-effort | Bajo si el registro es íntegro; medio si el entorno cambió sin nota |
| Archivos leídos (observation) | **Sí (como evidencia)** | `ref` resuelve; clase observation | Bajo |
| Comandos registrados en SESSION_LOG | **Sí (como evidencia)** | H06 los acepta (`VERIFICATION_REPORT.md:Test Results`) | Bajo |
| Attestations del executor | No (para ítems `[gate]`) | Solo con desviación documentada | Medio (auto-verificación) |
| Conclusión de un VERIFICATION_REPORT previo | No | — | Alto (rompe independencia) |
| Plan + spec + summary | Sí (como inputs a juzgar) | Lectura completa | Bajo |
| KB / contexto | Opcional | Freshness por claim | Medio (stale) |

**INFERENCIA clave:** reutilizar **evidencia** no equivale a reutilizar la **conclusión**; la frontera que ARgentOS ya traza (clases de evidencia, verifier como juez independiente) es precisamente la que permite memoizar tool results sin degradar la verificación.

---

# PARTE 9 — DISCOVERY VS CONTEXT GATHERING

Comparación por categoría. Fuentes: contratos de discovery (`orchestrators/discovery/contracts/*.md`), `CONTEXT_ARTIFACT.md`, `03-gather-context.md`, sesión real `574bdb2f` (`1/05-CONTEXT_ARTIFACT.md` vs `knowledge/discovery/*`).

| Categoría | Quién la produce (Discovery) | Quién la produce (Context) | ¿Quién la consume? | ¿Ambos leen las mismas fuentes? | ¿Ambos hacen inferencia LLM? | ¿Discovery puede sustituir parte del Context? | Qué debe re-verificarse |
|---|---|---|---|---|---|---|---|
| Arquitectura | `framework_worker` → `architecture.md` | `context_gatherer` → `project_context` | planner, executor | **Sí (módulos del proyecto)** | **Sí** | **Parcialmente sí** (hechos con provenance) | Relevancia a la tarea y frescura del claim |
| Estructura | `init_worker` → `file_map.md` | `relevant_components` | planner, executor | Sí | Sí | **Sí** (file_map es navegación; context la filtra por tarea) | Filtrado por relevancia de tarea |
| Componentes | `file_map` + `architecture.md` | `relevant_components` (ubicación + relevancia) | planner | Sí | Sí | Parcial | Relevancia de la tarea (discovery es project-wide) |
| Dependencias | `stack_worker` → `dependencies.md`, `containers.md`, `database.md` | `dependencies` (con razón por tarea) | planner, executor | Sí | Sí | **Parcialmente sí** | Por qué la dependencia afecta a esta tarea |
| Comportamiento | `business_worker` → `project_flow.md`, `business_rules.md` | `existing_behavior` (del cambio) | planner, executor | Sí | Sí | Parcial (flow general vs comportamiento del área del cambio) | Comportamiento específico de la zona a modificar |
| Environment | `environment_worker` → `environment.md` (probe, TTL 6h) | cita KB/entorno | executor (obligatorio si KB) | No (probe vs lectura) | Sí (síntesis) | **Sí (ya se consume como KB)** | TTL env (6h) y consistencia con lo observado |
| Patterns | `patterns_worker` → `development_patterns.md` | convenciones citadas | executor (obligatorio si KB) | Sí (muestras) | Sí | **Sí (ya se consume como KB)** | Aplicabilidad al archivo modificado (`USING_PATTERNS.md:2`) |
| Business knowledge | `business_worker` → `business_rules.md`, `technical_debt.md`, `known_errors.md` | `constraints` (por tarea) | planner | Sí | Sí | Parcial | Restricciones derivadas de la tarea |
| Source files | workers discovery (muestreo con hash) | `context_gatherer` (lectura directa) | ambos | **Sí** | **Sí** | No (ambos leen; discovery no elimina la lectura del gatherer) | Lo que la tarea necesita y no está en la KB |
| Claims | `Discovered Facts` con `source_files`/`source_sessions` (provenance) | `evidence[]` con `source` | D01 / H02 | Sí | Sí | Parcial (claims de discovery ya son reutilizables si fresh) | Proveniencia resoluble + TTL (KN-003/005) |
| Summaries | `synthesis_worker` → `executive_summary.md` | prosa del `CONTEXT_ARTIFACT` | orquestador, workers | Sí | Sí | Parcial | Resumen no introduce hechos nuevos (regla del contract) |

**INFERENCIA:** hay **solapamiento real** en arquitectura/estructura/dependencias/environment/patterns (ambos leen las mismas fuentes y ambos hacen inferencia LLM); el **no solapamiento** es la relevancia a la tarea, unknowns específicos y comportamiento de la zona del cambio. **HIPÓTESIS:** en la sesión real, parte de `CONTEXT_ARTIFACT.md` (Project Context, Existing Behavior, Dependencies, Constraints) duplica contenido ya presente en `architecture.md`/`project_flow.md`/`dependencies.md`/`environment.md` — no demostrable sin comparación de contenido y medición de tokens.
**Qué necesariamente debe re-verificarse:** frescura de claims KB (TTL/proveniencia — regla ya existente), relevancia a la tarea, y unknowns específicos (el discovery es project-wide, no task-specific).

---

# PARTE 10 — KB_RECOMMENDATION Y SELECCIÓN DE CONTEXTO

**Inputs (`context_discoverer.md:Inputs`):** session UUID, task specification, artifacts previos, workflow module, catálogo KB (front matter: session_uuid, objective, tags, files_modified, outcome + one-line summary), freshness/proveniencia.
**Output (`KB_RECOMMENDATION.md`):** entradas recomendadas con `kind`+`path`, prioridad, confianza, budget recomendado.
**Cuánto cambia entre fases:** el criterio de selección es tags/archivos/keywords del task (`CONTEXT.md:5. Selection criteria`); el **budget por fase** cambia (8000 chars análisis/contexto; 4000 planning/exec/verify — `CONTEXT.md:3. Knowledge Base context budgets`).
**¿PLANNING/EXECUTING/VERIFYING necesitan la misma selección?** El contrato declara `consumed_by: [PLANNING, EXECUTING, VERIFYING]`; el orquestador invoca al discoverer "before delegating the real phase worker" (`orchestrator.md:4.2`). **En la práctica observada** (sesiones `574bdb2f`, `b21e3a56`) la recomendación se produjo **una vez** (antes de context gathering) y sus entradas se reutilizaron en el payload de ejecución (budget 1500 tokens en `574bdb2f`). **INFERENCIA:** cuando el task y el catálogo no cambian, la selección es estable entre fases.
**Qué hace que cambie:** cambio de task (clarificación/recovery), cambio del catálogo (entradas nuevas, `curation_status` noisy/retired), cambio de fase (budget), expiración de freshness.
**¿Puede fingerprintearse?** En principio sí: (hash de task spec + hash del catálogo/manifest + fase + budget + estado de freshness). **HECHO:** hoy no hay fingerprint; la validez solo se controla por juicio en H10 y freshness por claim.
**¿Podría reutilizarse?** CONDITIONALLY: dentro de una ejecución si task y catálogo no cambiaron; entre ejecuciones, solo con fingerprint y reglas de freshness (hoy la re-curación es por juicio y se vuelve a calcular por fase si se invoca).

---

# PARTE 11 — TOOL RESULT REUSE

| Tool result | Quién lo ejecuta | Quién vuelve a necesitarlo | ¿Se vuelve a ejecutar? | ¿Podría persistirse? | Qué determina su validez | Qué lo invalidaría |
|---|---|---|---|---|---|---|
| Tests (unit/integration/E2E) | executor (fase 06) | verifier (fase 07) | **Condicional** (ver análisis abajo) | Sí (summary + SESSION_LOG con comandos) | código + entorno + versiones | cambio de código/entorno/deps |
| Linters (ruff/selene) | executor | verifier | Condicional | Sí | código + config | cambio de código/config |
| Type checkers (mypy) | executor | verifier | Condicional | Sí | código + versión de mypy | cambio de código/versión |
| Build | executor | verifier | Condicional | Sí | código + deps | cambio de inputs |
| Probes de environment | environment_worker | executor (vía KB) | Sí — por TTL 6h | **Sí (ya persiste: `environment.md`)** | entorno | TTL/entorno real |
| Lectura de archivos | gatherer, discovery, executor, verifier | todos | **Sí — se re-lee por fase** | No (no hay retrieval cache) | contenido del archivo | cambio del archivo |
| Grep/búsquedas | cualquiera | otros | Sí — sin cache | No | contenido | cambio de fuentes |
| Discovery probes/muestras | workers discovery | workers downstream (vía `worker_*.json`) | Dentro de un run: los intermedios sí se reutilizan; entre runs: por TTL/hash | **Sí (intermedios `discovery/`)**: `PROTOCOL_BOUNDARIES.md:Discovery intermediates exception` | hashes + TTL | cambio de fuentes |
| Benchmark | executor | verifier (evidencia) | Condicional | Parcial (results file) | entorno | cambio de código/entorno |

## 11.1 EXECUTING → VERIFYING: ¿re-ejecuta el verifier los mismos tests?

**Evidencia:**
- Workflow 07 ordena al verifier: "Run Defined Validations — Execute the validation strategy defined in the execution plan" (`07-verify.md:2. Run Defined Validations`).
- El contrato de `VERIFICATION_REPORT` permite evidencia = archivo o comando registrado en `SESSION_LOG.md`; si no hay `evidence`, el comando debe aparecer en el log (`VERIFICATION_REPORT.md:Test Results`). H06 verifica ese vínculo (`H06-verification-report.md`).
- Sesión real `574bdb2f`: el `VERIFICATION_REPORT` lista los mismos 8 comandos que el executor registró en `SESSION_LOG`, con `evidence` = archivos o "commands recorded in SESSION_LOG"; **no hay evidencia de re-ejecución** por el verifier.
- Sesiones `6bd97320` y `b21e3a56`: mismo patrón — los comandos se registran en el log de ejecución y el verifier cita resultados.

**Conclusión (HECHO):** el flujo `EXECUTOR → runs tests → result → VERIFIER → runs same tests again` **no está demostrado en las sesiones reales**; la práctica observada es reutilizar evidencia registrada (clase measurement con comando en log). El workflow 07 habilita la re-ejecución pero H06 la hace innecesaria cuando la evidencia está registrada. **Clasificación:** CONDICIONAL — la re-ejecución es posible y permitida, pero no exigida de facto.

---

# PARTE 12 — RECOVERY

Fuentes: `AGENT_STATE_MACHINE.md:RECOVERY`, `08-recovery.md`, tablas de recovery de H00–H07/H11 (`harness/policies/*.md:Recovery Decision Table`).

| Transición | Artifacts que permanecen válidos | Artifacts que se recalculan | Qué cambió | Qué NO cambió | Oportunidad concreta de no recalcular |
|---|---|---|---|---|---|
| `RECOVERY → PLANNING` | spec, context, validation (se preservan si válidos — `08-recovery.md:4. Update Artifacts if Needed`) | plan | información del fallo (root cause) | spec + contexto | "No recalcules spec/context/validation: inputs equivalentes" |
| `RECOVERY → ANALYZING_TASK` | intención/spec/context (downstream pendientes, `pending_artifacts`) | TASK_ANALYSIS | corrección de análisis | resto | Downstream ya se difiere (mecanismo existente) |
| `RECOVERY → BUILDING_TASK_SPECIFICATION` | análisis + intención | spec | corrección de spec | análisis/intención | "No recalcules TASK_ANALYSIS" (salvo H00 ya pasó) |
| `RECOVERY → GATHERING_CONTEXT` | spec (H02/H03: gaps accionables → `03-gather-context.md`) | context (re-gather) | gaps de contexto | spec | "No recalcules spec" |
| `RECOVERY → VALIDATING_CONTEXT` | spec + context artifact (solo se reescribe el reporte) | CONTEXT_VALIDATION_REPORT | fallo de validación | spec + context | "No vuelvas a gather; solo re-valida" |
| `RECOVERY → NEEDS_CLARIFICATION` | todo | nada (espera input) | decisión del usuario | todo | — (el input nuevo exige re-análisis posterior) |

**Tablas de recovery (destinos por gate) — HECHO:**
- H00: `RETRY_WORKER`→00 (artifact missing/profile inválido) \| `NEEDS_CLARIFICATION` (ambiguo) \| `RECOVERY_GENERIC` (retry≥1) — `H00-task-analysis.md:Recovery Decision Table`.
- H01: `RETRY_WORKER`→02 (sin transición si solo formato) \| `NEEDS_CLARIFICATION` \| `RECOVERY_GENERIC` — `H01-task-specification.md`.
- H02: `RETRY_WORKER`→03 \| `NEEDS_CLARIFICATION` (user-specific) \| `RECOVERY_GENERIC` — `H02-context-artifact.md`.
- H03: `RECOVERY_GENERIC` (contradictorio) \| `RETRY_WORKER`→03 (vía `RECOVERY→GATHERING_CONTEXT`) \| `NEEDS_CLARIFICATION`; reescritura del reporte → `RECOVERY→VALIDATING_CONTEXT` — `H03-context-validation.md`.
- H04: `RECOVERY_GENERIC` (out of scope) \| `NEEDS_CLARIFICATION` \| `RETRY_WORKER`→05 (retry 0) \| `RECOVERY_GENERIC` (retry≥1) — `H04-execution-plan.md`.
- H05: `ABORT` (irrecuperable) \| `RECOVERY_GENERIC` (bloqueado) \| `RETRY_WORKER`→06 (incompleto) — `H05-execution-completed.md`.
- H06: `ABORT` \| `NEEDS_CLARIFICATION` \| `RECOVERY_GENERIC` — `H06-verification-report.md`.
- H07: `RECOVERY_GENERIC` (severo) \| `NEEDS_CLARIFICATION` (expansión) \| `RETRY_WORKER`→06 (scope no conforme) — `H07-scope-compliance.md`.
- H11: `RETRY_WORKER`→01 \| `NEEDS_CLARIFICATION` (correction_cycle≥2 / rechazo) \| `RECOVERY_GENERIC` — `H11-intent-reflection.md`.

**Oportunidades de "no recalcular" (INFERENCIA):** (a) recovery→PLANNING ya preserva spec/context/validation; (b) recovery→VALIDATING_CONTEXT ya preserva el context artifact; (c) recovery→fases tempranas ya difiere downstream vía `pending_artifacts`. Lo que **no** existe es memoización de artifacts intactos entre loops (se re-leen, no se re-generan — el costo evitable restante es de re-lectura/re-interpretación, no de re-generación).

---

# PARTE 13 — TELEMETRÍA DISPONIBLE Y FALTANTE

Fuentes: `METRICS.md` (contrato), `PROTOCOL_METRICS.md`, `tools/aggregate_metrics.py`, `HARNESS_REPORT.md`, `SESSION_LOG.md`, `DISCOVERY_MANIFEST.md:[runtime]`, sesiones reales.

| # | Pregunta | Respuesta | Evidencia |
|---|---|---|---|
| 1 | ¿Cuántas llamadas LLM tuvo una ejecución? | **NO RESPONDER** | METRICS registra eventos de proceso (`delegation`), no llamadas LLM; gates son juicios no contados (`METRICS.md:Event catalog`) |
| 2 | ¿Cuántas por fase? | **PARCIALMENTE** | `delegation` con `phase` cuenta delegaciones (3 en `574bdb2f`), no llamadas dentro de la fase |
| 3 | ¿Cuántos input tokens? | **NO RESPONDER** | no existe campo de tokens |
| 4 | ¿Cuántos output tokens? | **NO RESPONDER** | ídem |
| 5 | ¿Cuántos cached tokens? | **NO RESPONDER** | ídem |
| 6 | ¿Qué modelo se utilizó? | **PARCIALMENTE** | `model_used` opcional solo en manifest discovery (`DISCOVERY_MANIFEST.md:[runtime]`); en `574bdb2f`: `gpt-5 (Codex)`; ninguna sesión core registra modelo |
| 7 | ¿Cuánto costó cada llamada? | **NO RESPONDER** | sin precios ni tokens |
| 8 | ¿Cuánto costó cada fase? | **NO RESPONDER** | ídem |
| 9 | ¿Cuánto costó una ejecución completa? | **NO RESPONDER** | ídem |
| 10 | ¿Cuántas veces se leyó una misma fuente? | **NO RESPONDER** | no hay retrieval telemetry |
| 11 | ¿Cuántas veces se ejecutó una misma herramienta? | **PARCIALMENTE** | comandos de validación se registran en `SESSION_LOG`/summary (fase 06); sin agregación; reads/greps no registrados |
| 12 | ¿Cuántas veces se recalculó un mismo artifact? | **PARCIALMENTE** | HARNESS FAIL + `retry_count` + log ("TASK_ANALYSIS.md (updated)") + archivos de iteración; sin contador mecánico |
| 13 | ¿Cuánto cuesta Discovery? | **NO RESPONDER** | `execution_time_seconds` opcional y ausente en el manifest real; `model_used` presente |
| 14 | ¿Cuánto cuesta Context Gathering? | **NO RESPONDER** | — |
| 15 | ¿Cuánto cuesta Verification? | **NO RESPONDER** | — |
| 16 | ¿Cuánto cuesta Recovery? | **NO RESPONDER** | — |
| 17 | ¿Cuánto cuesta un retry? | **NO RESPONDER** | — |
| 18 | ¿Cuánto cuesta un recovery loop? | **NO RESPONDER** | — |
| 19 | ¿Cuánto del contexto enviado es info ya procesada? | **NO RESPONDER** | el budget mide solo la porción KB (`BUDGET_MATERIALIZATION.md:3. Scope of context_budget`); no hay medición de artifacts/documentos re-enviados |

**HECHO:** la telemetría mide **proceso**, no **costo** ("Metrics describe the process, not the content" — `PROTOCOL_METRICS.md:Privacy rule`). **INFERENCIA:** ninguna pregunta de costo puede responderse con los datos actuales; la carencia es arquitectónica y es el requisito previo de una RFC de reuse.

---

# PARTE 14 — DOGFOODING / EJECUCIONES REALES

Sesiones en `reference/.project/` (protocolo 3.25.0 salvo 246d4da2, formato antiguo sin HARNESS/METRICS):

| Dimensión | 246d4da2 (simple/moderada, 2 iteraciones) | 574bdb2f (compleja + discovery) | 6bd97320 (retry/recovery) | b21e3a56 (compleja + reuse KB) |
|---|---|---|---|---|
| Perfil | complex (iter 1 y 2) | complex | complex | complex |
| Fases (core) | ciclo completo x2 (análisis→verificación); iter 2 reutilizó "política pendiente-humano" | ciclo completo + H00 re-entry tras clarificación | ciclo completo + H00 re-entry tras clarificación + resume | ciclo completo + H00 re-entry tras clarificación |
| Delegaciones registradas (METRICS) | sin METRICS | 3 (`delegation`: 00, 06, 07) | 4 (00 subagente, 00 single-instance, 06, 00 re-delegación) | sin METRICS (solo log; H15 por fase) |
| Retries / recovery | ninguno | F1 (subagente idle) + fallback single-instance; H00 re-entry | F1 (3 spawns fallidos) + resume + backfill H15 (P18); H00 re-entry | F1 previo (modo elegido preventivamente); H00 re-entry |
| Discovery | no mencionado | **full (18 entradas regeneradas, TTL+hash)** | marker válido — **sin rediscovery** | marker fresco (full 03:25) — **sin rediscovery**; KB consultada: kb-005/003/004/002 |
| KB | no | KB_RECOMMENDATION 8 entradas, budget 6000 chars; executor con budget 1500 tokens | payload fase 00 con budget 12000 sin KB | KB_RECOMMENDATION 4 entradas, budget 4000 chars; executor con refs discovery obligatorias |
| Artifacts | 8+8 core | 10 core + KB_RECOMMENDATION + D01 report + state.json | 9 core + KB_RECOMMENDATION + delegation JSON + state.json | 10 core + KB_RECOMMENDATION + REVIEW + state.json |
| Tests/validaciones | 4 comandos (lune, selene, ls, git status) | 8 validaciones (1455 tests, gates) | 7 validaciones (1438 tests, gates, benchmark) | 6 validaciones (1469 tests, gates) |
| Tool calls registradas | sí (log) | sí (SESSION_LOG: comandos) | sí (log + benchmark) | sí (log) |
| Duración (ventana) | ~1h20 (iter 1) + ~40m (iter 2) | 02:28–04:30 (~2h) | 01:30–03:15 (~1h45) | 03:27–05:25 (~2h) |
| Verifier re-ejecuta tests | no evidenciado (cita comandos) | **no** — cita comandos de SESSION_LOG + archivos | no evidenciado | no evidenciado |

**Hallazgos de ejecuciones reales:**
1. **Verificación sin re-ejecución** (574bdb2f): el verifier cita los comandos del executor; no hay evidencia de re-run. (HECHO)
2. **Rediscovery completo por TTL** (574bdb2f): `invalidation_report.json` marca las 18 entradas por TTL + hash; el diseño permite scoped solo vía `invalidated_facts`. (HECHO)
3. **Reuso de discovery** (6bd97320, b21e3a56): marker válido → sin re-invocación; KB consumida vía recomendación y refs obligatorias para executor. (HECHO)
4. **Costo real de subagentes fallidos** (574bdb2f, 6bd97320): spawns que responden como idle listener "I'm ready to help..." — inferencia LLM desperdiciada antes de la fase. (HECHO del log; costo cuantitativo DESCONOCIDO)
5. **Re-análisis tras clarificación** en las 4 sesiones: H00 re-entry + TASK_ANALYSIS actualizado. (HECHO)
6. **`duration_ms: 0` en todos los ENTRYs** (574bdb2f, 6bd97320): duración por gate no capturada. (HECHO)
7. **Sin eventos `context_budget`/`context_candidates`** en las sesiones con METRICS, pese a ser eventos del catálogo (P4 del Problem Model). (HECHO)

**Limitación explícita (HECHO):** son 5 sesiones de un solo proyecto (BeaconRBX), 4 con el mismo patrón (clarificación + single-instance por fallo de subagentes); no hay muestra de tareas triviales, ni de fallos de gates H01–H07 reales (todos PASS), ni de recovery a fases tempranas ejecutado. La generalización es **DESCONOCIDA**.

---

# PARTE 15 — MODELO DE COSTO CUALITATIVO

```text
Execution Cost ≈ Σ (LLM Calls) × (Input Context + Output)
```

Descomposición conceptual, clasificada por nivel de evidencia (sin números):

| Componente del costo | Clasificación |
|---|---|
| Documentos del protocolo re-leídos por sesión y por fase (system/workflow/role/policy/skills) | **Demostrado** que se envían repetidos (contratos y `_AGENTS.md`); magnitud **desconocida** |
| Artifacts completos re-leídos por fase (`input_artifacts`) | **Demostrado** que se re-leen literalmente; magnitud **desconocida** |
| `task_summary` + acceptance criteria + technical_approach duplicados por delegación | **Demostrado** que se re-emiten; magnitud **desconocida** |
| Juicios de gates y registros del orquestador por transición | **Probable** fuente no trivial (15+ juicios por sesión) pero sin métrica |
| KB excerpts re-resumidos por fase | **Probable** (contrato permite por fase; práctica observada: una vez); magnitud **desconocida** |
| Solape Discovery ↔ Context Gathering | **Hipótesis** (evidencia cualitativa de solape, sin medición) |
| Self-consistency (2ª pasada) + reviewer + intent_reviewer | **Demostrado** que existen (costo explícito por diseño); magnitud **desconocida** |
| Retries/recovery (re-ejecución de fases) | **Demostrado** que recalculan artifacts completos; frecuencia y costo **desconocidos** (ningún gate FAIL real en la muestra) |
| Subagentes fallidos (idle listeners) | **Hipótesis** de costo desperdiciado (observado 2 veces, sin medición) |
| Discovery (muestreo + 7 workers LLM) | **Demostrado** que es la operación más pesada en estructura (7 workers, 18 entradas); costo unitario **desconocido**; rediscovery por TTL sin cambio de hash es **probable** fuente evitable |
| Prompt-caching del proveedor | **Desconocido** (fuera del protocolo) |

**Regla aplicada:** no se afirma "X es el mayor costo" — sin métricas solo se permite demostrado/probable/posible/desconocido.

---

# PARTE 16 — OPORTUNIDADES DE MEMOIZACIÓN

Scope: intra-worker / intra-state / intra-execution / inter-execution / project-wide. (No es diseño de RFC; es identificación de oportunidades.)

| Oportunidad | Resultado reutilizable | Scope | Condición de validez | Potencial ahorro | Riesgo | Confianza |
|---|---|---|---|---|---|---|
| O1 `task_summary` por delegación | resumen del objetivo | intra-execution | spec + perfil sin cambio | Medio (tokens de input por delegación) | prompt drift (perfil) | MEDIA |
| O2 Excerpts KB por fase | resumen de entradas | intra-execution | task + catálogo + freshness sin cambio | Medio | stale | MEDIA |
| O3 Selección de perfil (7 preguntas) | `profile` | intra-execution | fingerprint (task, plan) | Bajo | prompt/policy drift | MEDIA |
| O4 KB_RECOMMENDATION | selección de conocimiento | intra-execution | fingerprint (task spec, catálogo, fase, freshness) | Medio | stale, curation drift | MEDIA |
| O5 Tool results (tests/validaciones) | measurements | intra-execution / inter-execution | fingerprint (código, entorno, versiones); clase measurement con ref | **Alto** | incorrect reuse si el fingerprint falta; verification independence si se reutiliza como conclusión | ALTA (evidencia: verifier ya los reutiliza vía log) |
| O6 Discovery con hash sin cambio | entradas KB | inter-execution | hashes iguales + TTL válido (o revalidación scoped) | **Alto** | stale | ALTA |
| O7 Claims de discovery para CONTEXT_ARTIFACT | hechos con provenance | intra-execution | freshness + relevancia a la tarea | Medio | stale, relevancia | MEDIA |
| O8 `environment.md` probe | environment | inter-execution | TTL env (6h) | Bajo | entorno real cambia | ALTA (ya TTL) |
| O9 Re-lectura de artifacts por fase | contexto | intra-execution | resumen fiel (budget) | Medio | fidelidad/correctness | BAJA (riesgoso) |
| O10 Gates estructurales | juicio determinista | intra-execution | — (ya es `[machine]`) | Bajo | — | ALTA (ya implementado) |
| O11 Lessons/decisiones curadas | decisiones | inter-execution | freshness + provenance | Bajo | curation drift | ALTA (ya existe) |
| O12 Recovery: preservar artifacts intactos | artifacts no afectados | intra-execution | inputs del artifact sin cambio | Medio | correctness en cascada | ALTA (mecanismo ya existente) |

---

# PARTE 17 — QUÉ NECESITAMOS MEDIR ANTES DE UNA RFC

| Prioridad | Métrica | Unidad | Dónde capturarla | Por qué importa | Qué decisión permitiría |
|---|---|---|---|---|---|
| **P0** | Llamadas LLM por sesión y por fase | count | runtime/hook de delegación + gates | Cuantifica el denominador del modelo de costo | Elegir alcance de memo (qué fases) |
| **P0** | Input tokens estimados por delegación (payload + artifacts + docs) | estimated tokens | captura del payload + tamaño de inputs | Mide repetición de contexto (pregunta 19) | Decidir si la repetición de contexto es el costo dominante |
| **P0** | Output tokens por artifact | estimated tokens | tamaño de artifacts | Mide el costo de generación | Priorizar síntesis vs contexto |
| **P0** | Modelo por llamada/delegación | id | METRICS/evento nuevo | Detecta model drift y comparabilidad | Fingerprint de modelo en memo |
| **P0** | Comandos ejecutados con exit code + duración + output hash | log por comando | SESSION_LOG/runtime | Base para reutilización segura de tool results | Reuso de measurements sin re-ejecución |
| **P0** | Re-producción de artifacts (rewrite counter / content hash por path) | count + hash | filesystem de iteración | Mide recomputación intra-ejecución (pregunta 12) | Justificar memo por artifact |
| **P1** | Cached tokens (si el runtime los expone) | tokens | runtime | Ajusta el beneficio real de reuse | No sobre-invertir si el provider ya cachea |
| **P1** | Retrieval counter (lecturas por archivo/fuente) | count por path | tool layer | Mide repetición de lectura (pregunta 10) | Cache de retrieval |
| **P1** | Costo de discovery (modelo, tiempo, entradas) | id + s + tokens | manifest (hacer obligatorios `model_used`/`execution_time_seconds`) | Cuantifica P14 | Scoped revalidation vs full |
| **P1** | Frecuencia/costo de retries y recovery loops | count + tokens | METRICS `failure` + nuevos eventos | Prioriza mejoras de gates vs memo | Dónde atacar primero |
| **P1** | Reutilización de evidencia vs re-ejecución en verificación | flag por TR | VERIFICATION_REPORT | Determina si W7 ocurre | Decidir política de verification reuse |
| **P2** | Fingerprint de policy/prompt/worker por delegación | hash/versión | payload | Habilita invalidación por drift | Memo entre versiones |
| **P2** | Hash de contenido de source files leídos | hash | tool layer | Validez de context/claims | Freshness de context artifact |
| **P2** | Duración por gate | ms | HARNESS ENTRY (`duration_ms` hoy 0) | Costo de juicios | Optimizar gates |

---

# FORMATO FINAL

## A. Executive Findings

1. **HECHO:** no existe cache, memoización ni fingerprinting de artifacts en el protocolo; la única invalidación real es discovery (TTL/hash + `invalidated_facts`) y la derivada de gates.
2. **HECHO:** toda invocación LLM re-lee documentos del protocolo, artifacts completos y, en varias fases, fuentes originales; el mínimo es ~30 pasadas LLM por tarea `standard`.
3. **HECHO:** el verifier de la sesión real `574bdb2f` NO re-ejecutó la suite: citó comandos registrados en SESSION_LOG y archivos como evidencia; H06 acepta esa modalidad.
4. **HECHO:** el rediscovery por TTL regeneró las 18 entradas juntas en `574bdb2f` aunque parte del contenido no cambió; la revalidación scoped existe solo vía `invalidated_facts`.
5. **HECHO:** recovery ya evita recomputación: `RETRY_WORKER` sin transición para fallos de formato, corrección de un artifact por entrada y `pending_artifacts` que difieren downstream.
6. **HECHO:** la telemetría mide proceso, no costo; ninguna de las 19 preguntas de costo de la Parte 13 puede responderse hoy con datos.
7. **HECHO:** las sesiones reales registran `duration_ms: 0`, ausencia de eventos `context_budget`/`context_candidates`, y 2 fallos de entrega de subagentes con respuestas idle (inferencia desperdiciada).
8. **INFERENCIA:** la reutilización actual es de **resultado** (artifacts re-leídos), no de contexto/razonamiento; los mismos tokens conceptuales se re-envían por fase.
9. **INFERENCIA:** las recomputaciones evitables de mayor impacto son síntesis repetidas por delegación (`task_summary`, excerpts KB, perfil) y tool results re-ejecutables; las necesarias incorporan input nuevo o sostienen garantías.
10. **INFERENCIA:** la frontera evidencia/resultado que ARgentOS ya traza (clases de `EVIDENCE.md`, verifier como juez) es la que permite memoizar tool results sin degradar la verificación.
11. **HIPÓTESIS:** el solape Discovery↔Context Gathering (arquitectura/componentes/dependencias/entorno/patterns) genera análisis LLM duplicado de las mismas fuentes; sin medición no es demostrable.
12. **HIPÓTESIS:** los subagentes fallidos y los juicios de gates son fuentes de costo significativas no contadas.
13. **DESCONOCIDO:** magnitud en tokens de cada fuente de costo; prompt-caching del proveedor; frecuencia real de retries/recovery; comparabilidad entre modelos.
14. **DESCONOCIDO:** si la hipótesis central es cuantitativamente cierta — la evidencia es consistente con ella, pero no la demuestra.
15. **CONCLUSIÓN:** no hay evidencia suficiente para diseñar una RFC de reuse; la instrumentación P0 (Parte 17) es el requisito previo.

## B. LLM Invocation Inventory

Tabla completa (L1–L34; columnas Cache/Memo/FP/Inval. = mecanismos del protocolo):

| # | Estado | Worker/Rol | Capability/Skill | Trigger | Input | Output | ¿LLM oblig.? | ¿Repite? | Motivos | Cache | Memo | FP | Inval. | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | system health | System Agent | checklist+probe | bootstrap | árbol+project | log+marker | Sí | Sí | sesión/TTL | No | No | No | TTL | `PROTOCOL_HEALTH.md` |
| L2 | inicio sesión | Orchestrator | — | aceptar tarea | request | log+metric | Sí | Sí | sesión | No | No | No | — | `orchestrator.md:1` |
| L3 | pre-delegación | Orchestrator | — | toda delegación | spec/KB/flags | payload+task_summary | Sí | Sí | delegación/retry/recovery | No | No | No | — | `ORCHESTRATION_GUIDE.md:6` |
| L4 | PLAN_READY→EXECUTING | Orchestrator | 7 preguntas | selección perfil | spec+plan | profile | Sí | Sí | ejecución/subtarea | No | No | No | — | `ORCHESTRATION_GUIDE.md:3` |
| L5 | ANALYZING/PLANNING | Orchestrator | — | selección skills | spec+tabla | skills | Sí | Sí | delegación/override | No | No | No | — | `SKILLS.md:Activation` |
| L6 | pre-delegación | Orchestrator | — | H15 pre | payload | PASS/FAIL | Sí | Sí | delegación | No | No | No | — | `H15-delegation-validity.md` |
| L7 | ANALYZING_TASK | task_analyst | 5 skills | fase 00 | request+brief | TASK_ANALYSIS | Sí | Sí | clarif./recovery/re-entry | No | No | No | H00 | `00-analyze-task.md` |
| L8 | CONFIRMING_INTENT | intent_reflector | ambiguity-detector | fase 01 | análisis+request | INTENT_REFLECTION | Sí | Sí | corrección | No | No | No | H11 | `01-confirm-intent.md` |
| L9 | CONFIRMING_INTENT | intent_reflector | — | self-consistency | 1ª reformulación | 2ª reformulación | Sí | Sí | cada reflexión | No | No | No | — | `01-confirm-intent.md:2` |
| L10 | CONFIRMING_INTENT | intent_reflection_reviewer | — | pre-presentación | reflection | recomendación | Sí | Sí | REWORK | No | No | No | — | `orchestrator.md:Intent Reflection` |
| L11 | BUILDING_TASK_SPEC | spec_writer | ears+validator | fase 02 | análisis+intención+brief | TASK_SPECIFICATION | Sí | Sí | recovery/clarif. | No | No | No | H01 | `02-build-task-specification.md` |
| L12 | pre-fase (KB) | context_discoverer | — | antes de fase worker | spec+catálogo+fase | KB_RECOMMENDATION | Sí | Sí | por fase consumidora | No | No | No | H10+freshness | `orchestrator.md:4.2` |
| L13 | GATHERING_CONTEXT | context_gatherer | 4 skills | fase 03 | spec+KB+fuentes | CONTEXT_ARTIFACT | Sí | Sí | recovery/H02 | No | No | No | H02 | `03-gather-context.md` |
| L14 | VALIDATING_CONTEXT | context_validator | 2 skills | fase 04 | spec+context | CONTEXT_VALIDATION | Sí | Sí | recovery/H03 | No | No | No | H03 | `04-validate-context.md` |
| L15 | PLANNING | planner | 4 skills | fase 05 | spec+context+validation | EXECUTION_PLAN | Sí | Sí | recovery/H04 | No | No | No | H04 | `05-plan.md` |
| L16 | review | reviewer | execution-plan-reviewer | transición crítica | artifact+rubric | REVIEW_REPORT | Sí | Sí | REWORK/por transición | No | No | No | REVIEW gate | `orchestrator.md:4.1` |
| L17 | EXECUTING | executor (+perfil) | self-review+tdd | fase 06 | spec+validation+plan+KB+proyecto | EXECUTION_SUMMARY | Sí | Sí | RETRY/recovery | No | No | No | H05 | `06-execute.md` |
| L18 | VERIFYING | verifier | 5 skills | fase 07 | spec+plan+summary+proyecto | VERIFICATION_REPORT | Sí | Sí | H06/H07→recovery | No | No | No | H06/H07 | `07-verify.md` |
| L19 | RECOVERY | recovery_analyst | 2 skills | fase 08 | verification/summary+artifacts | RECOVERY_REPORT | Sí | Sí | cada loop | No | No | No | H09 | `08-recovery.md` |
| L20 | post-return | Orchestrator | — | H15 post | return report | decisión | Sí | Sí | delegación | No | No | No | — | `harness/INDEX.md:H15` |
| L21 | gates H00–H07/H11 | Orchestrator | — | transiciones | artifact+policy+validator | HARNESS ENTRY | Sí | Sí | por transición | No | No | No | — | `harness/INDEX.md:How the Harness Works` |
| L22 | recovery routing | Orchestrator | — | gate FAIL | tabla+contexto | destino | Sí | Sí | cada FAIL | No | No | No | — | `harness/INDEX.md:Recovery Mechanism` |
| L23 | cierre | Orchestrator | — | COMPLETED | artifacts | lessons | Sí | Sí | sesión | No | No | No | curación | `orchestrator.md:Closing Feedback` |
| L24 | NEEDS_CLARIFICATION | Orchestrator | — | ambigüedad | opciones | mensaje/defaults | Sí | Sí | ambigüedad | No | No | No | — | `NO_ASSUMPTIONS.md` |
| L25 | resume | Orchestrator | — | reanudación | registros+artifacts | decisión | Sí | Sí | reanudación | No | No | No | gates pendientes | `PROTOCOL_BOUNDARIES.md:Resume procedure` |
| L26 | H07 Branch B | Orchestrator | decision-extractor | extra work | log/artifact | decisión | Sí | Sí | caso | No | No | No | — | `orchestrator.md:7` |
| L27 | DISCOVERY_INIT | init_worker | — | TTL/hash/uso | KB+hashes+artifacts | discovery_input+invalidation+report | Sí | Sí | TTL/hash | No | No | **Sí** | TTL+hash | `init_worker.md:Tasks` |
| L28 | DISCOVERY_ENV | environment_worker | — | scope | input+probe | environment.md | Sí | Sí | TTL env | No | No | **Sí** | TTL | `environment_worker.md` |
| L29 | DISCOVERY_STACK | stack_worker | — | scope | input+config | stack/deps/containers/db | Sí | Sí | hash/TTL | No | No | **Sí** | TTL+hash | `DISCOVERY_STATE_MACHINE.md:TTL and Cache` |
| L30 | DISCOVERY_FRAMEWORK | framework_worker | — | tras stack | worker_stack | arch/conf/entry/api | Sí | Sí | idem | No | No | — | idem | `DISCOVERY_STATE_MACHINE.md:DISCOVERY_FRAMEWORK` |
| L31 | DISCOVERY_PATTERNS | patterns_worker | — | scope | input+muestra | development_patterns | Sí | Sí | hash/TTL | No | No | **Sí** | TTL+hash | `patterns_worker.md` |
| L32 | DISCOVERY_BUSINESS | business_worker | — | scope | input+README/tests | business/flow/debt/errors/glossary | Sí | Sí | TTL | No | No | — | TTL | `DISCOVERY_STATE_MACHINE.md:DISCOVERY_BUSINESS` |
| L33 | DISCOVERY_MERGE | synthesis_worker | — | tras workers | partials+KB | executive+manifest+entries | Sí | Sí | run | No | No | — | — | `synthesis_worker.md` |
| L34 | D00/D01+freshness | Discovery/Orchestrator | — | gates/consumo | report/entries | HARNESS/decisión | Sí | Sí | run/consumo | No | No | — | TTL/hash/prov. | `harness/INDEX.md:Project Discovery` |

## C. Recomputation Matrix

Ver Parte 3 (tabla completa de 24 operaciones A–F). Resumen canónico:

| Operación | Clase | Productor | ¿Persistido? | ¿Reutilizado? | ¿Puede recalcularse? | ¿Cuándo? | ¿Por qué? |
|---|---|---|---|---|---|---|---|
| Interpretar request | A | task_analyst | sí | sesión | sí | clarif./recovery | input cambió |
| Identificar intención | A | intent_reflector | sí | sesión | sí | corrección | usuario corrige |
| Autocomprobación (2ª pasada) | A | intent_reflector | no | no | sí | cada reflexión | garantía anti-suposición |
| Detectar ambigüedad | A | task_analyst | sí | sesión | sí | re-análisis | input nuevo |
| Derivar contexto | B | context_gatherer | sí | sesión | sí | recovery/H02 | artifact inválido |
| Derivar arquitectura/deps | B | discovery | **sí (KB)** | **entre sesiones** | sí | TTL/hash | frescura |
| Derivar technical approach | B | spec_writer | sí | copiado literal | no | — | trazabilidad |
| Seleccionar skill | C | orquestador | log | no | sí | delegación | sin memo |
| Seleccionar profile | C | orquestador | log | no | sí | ejecución | sin memo |
| Seleccionar estrategia | C | planner | sí | sesión | sí | recovery | fallo |
| Seleccionar conocimiento | C | context_discoverer | sí | parcial | sí | fase | sin memo |
| Validar contexto | D | context_validator | sí | sesión | sí | recovery | artifact inválido |
| Validar plan (H04) | D | orquestador+reviewer | sí | no | sí | transición | gate |
| Verificar AC | D | verifier | sí | sesión | sí | H06/H07 | fallo |
| Revisar artifact | D | reviewer | sí | no | sí | REWORK | retry bound |
| Crear artifact | E | cada worker | sí | sesión | sí | retry/recovery | artifact inválido |
| Resumir conocimiento | E | context_discoverer | parcial | no | sí | delegación | budget |
| Producir plan | E | planner | sí | sesión | sí | recovery | fallo |
| Producir verification | E | verifier | sí | no | sí | recovery | fallo |
| Tests/validaciones | F | executor/verifier | parcial | no (re-ejecutables) | sí | 06/07 | independencia |
| Grep/lecturas | F | gatherer/discovery/exec/verifier | parcial | no | sí | cada fase | sin retrieval cache |
| Probes env | F | environment_worker | sí (KB) | sí (si fresh) | sí | TTL 6h | frescura |
| Comandos de ejecución | F | executor | parcial | no | no | — | — |
| Discovery | F+B | discovery workers | sí | sí | sí | TTL/hash | frescura |

## D. Artifact Dependency Matrix

| Output | Dependencias explícitas | Dependencias implícitas | No registradas | Necesita fingerprint de |
|---|---|---|---|---|
| TASK_ANALYSIS | user request, brief | workflow/rol/skills/criterios | model, prompt, worker, policy | request, brief, model, prompt |
| INTENT_REFLECTION | análisis, user response, cycle | self-consistency, reviewer | model, prompt | análisis, response, model |
| TASK_SPECIFICATION | análisis, intención, brief, flags | technical approach | model, prompt, worker | análisis, intención, flags |
| CONTEXT_ARTIFACT | spec, KB excerpts | fuentes leídas | hash de fuentes, model | spec, fuentes (hash), KB |
| CONTEXT_VALIDATION | spec, context, rubrics | — | model, prompt | spec, context |
| EXECUTION_PLAN | spec, context, validation, approach | perfil, skills, KB | model, prompt | spec+context+validation, approach |
| EXECUTION_SUMMARY | plan, spec, validation | tool results, KB, perfil | hash de comandos, model | plan, spec, código (tool results) |
| VERIFICATION_REPORT | spec, plan, summary, evidence | proyecto, rubrics | model | spec, plan, summary, evidence refs |
| RECOVERY_REPORT | verification/summary, artifact de fase | tabla de recovery | model | failure artifact, tabla |
| KB_RECOMMENDATION | spec, catálogo KB, freshness | fase, budget | hash de catálogo | spec, catálogo, fase |
| KB discovery entry | source files (hashes), KB previa | scope/sample/budget | model (opcional) | **fuentes (ya hash)**, worker, model |
| LESSON | artifacts de sesión, evidencia | filtro de curación | model | artifact fuente, evidencia |

## E. Cacheability Matrix

| Resultado | Clasificación | Por qué |
|---|---|---|
| TASK_ANALYSIS | CONDITIONALLY CACHEABLE | inputs = request+brief+criterios; sin fingerprint de model/prompt no es seguro entre ejecuciones |
| INTENT_REFLECTION | CONDITIONALLY CACHEABLE | depende de análisis+respuesta; self-consistency no cacheable sin degradar garantía |
| TASK_SPECIFICATION | CONDITIONALLY CACHEABLE | inputs = análisis+intención+clarificaciones+flags |
| CONTEXT_ARTIFACT | CONDITIONALLY CACHEABLE | depende de spec+fuentes+KB; freshness de fuentes sin hash hoy |
| CONTEXT_VALIDATION | CONDITIONALLY CACHEABLE | depende de spec+context; decisión barata de re-derivar |
| EXECUTION_PLAN | CONDITIONALLY CACHEABLE (recovery) / NON-CACHEABLE (entre ejecuciones) | recovery preserva inputs; entre ejecuciones exige fingerprint completo |
| Tool results | **CACHEABLE** | deterministas bajo (código, entorno, versiones); clase measurement re-verificable |
| Test results | **CACHEABLE** (bajo condiciones) | fingerprint código+entorno+versiones |
| Discovery results | **CACHEABLE** | ya el diseño: TTL+hashes; scoped para invalidated_facts |
| KB recommendations | **CACHEABLE** (intra-ejecución) | task+catálogo+fase sin cambio (evidencia: reutilizada en sesión real) |
| Verification evidence | **CACHEABLE** | durable con clase+ref; reutilizable como evidencia |
| Verification conclusion | **NON-CACHEABLE** | rompe independencia de verificación |
| Lessons | CONDITIONALLY CACHEABLE | ya curadas; freshness por claim + provenance (KN-003/005) |

## F. Verification Independence Analysis

**HECHO:** verifier = rol separado o judgment pass explícito con evidencia; en single-instance la independencia se declara atestación (`harness/INDEX.md:Guarantee catalog`). **HECHO:** "verified" exige evidencia distinta de atestación + gate PASS (`EVIDENCE.md:VERIFIED`).
1. Debe recalcular: juicio de cada AC, evaluación de la estrategia de validación, scope compliance, decisión final.
2. Puede reutilizar como evidencia: measurements/observations/references/assertions registradas con clase+ref.
3. Puede reutilizar sin perder independencia: evidencia objetiva durable (test results con comando/exit code), porque la conclusión se deriva de nuevo.
4. NO debe reutilizar: conclusión/attestations del executor, verification previa como conclusión, razonamiento privado.
5. La independencia depende de actor, contexto y fresh reasoning; **no** depende de fresh tool execution si la evidencia está registrada (clase measurement).

## G. Discovery vs Context Gathering

**HECHO:** ambos dominios leen las mismas fuentes (módulos, config, tests) y ambos hacen inferencia LLM; solape en arquitectura/estructura/dependencias/entorno/patterns; no solape en relevancia a la tarea, unknowns y comportamiento de la zona del cambio. **HECHO:** el gatherer no accede a la KB directamente; recibe excerpts en el payload (`context_gatherer.md`). **INFERENCIA:** parte del Context Gathering podría basarse en claims de discovery con provenance (frescura+relevancia), sin eliminar la verificación de relevancia por tarea. **Debe re-verificarse:** freshness (KN-003/005), relevancia por tarea, unknowns específicos. **HIPÓTESIS:** el solape genera duplicación de análisis LLM — no demostrado sin medición.

## H. Tool Result Reuse

**HECHO:** workflow 07 ordena ejecutar la estrategia de validación; H06 acepta evidencia = archivo o comando en SESSION_LOG; la sesión real `574bdb2f` muestra al verifier citando los comandos del executor **sin re-ejecución evidenciada**. **Conclusión:** el flujo `EXECUTOR→tests→VERIFIER→same tests again` no está demostrado; la modalidad real es reuso de evidencia registrada. **Clasificación:** CONDICIONAL. **INFERENCIA:** tool results son el candidato más seguro de memoización (deterministas, clase measurement), con fingerprint de código+entorno+versiones.

## I. Recovery Reuse Opportunities

**HECHO:** recovery→PLANNING preserva spec/context/validation si válidos; recovery→VALIDATING_CONTEXT preserva el context artifact; recovery a fases tempranas difiere downstream vía `pending_artifacts`; fallos de formato usan `RETRY_WORKER` sin transición. **Oportunidades:** "no recalcules" ya implementado para artifacts no afectados; lo evitable restante es la re-lectura/re-interpretación (contexto), no la re-generación. **INFERENCIA:** la memoización de artifacts intactos entre loops es de bajo riesgo pero bajo beneficio; el mayor beneficio está en no re-enviar contexto repetido.

## J. Current Cost Observability

Ver Parte 13: de las 19 preguntas de costo, **2 PARCIALMENTE** (delegaciones por fase; comandos de validación registrados), **17 NO RESPONDER**; ninguna **RESPONDER HOY**. La telemetría mide proceso, no costo (`PROTOCOL_METRICS.md`).

## K. Evidence From Real Executions

Ver Parte 14. Cuatro perfiles comparados: simple/moderada (246d4da2), compleja+discovery (574bdb2f), retry/recovery (6bd97320), compleja+reuso de KB (b21e3a56). Hallazgos: verificación sin re-ejecución, rediscovery full por TTL, reuso de discovery con marker válido, subagentes fallidos con respuestas idle, H00 re-entry tras clarificación en las 4, `duration_ms: 0`, ausencia de eventos `context_budget`. Muestra limitada a un proyecto y sin gate FAIL real → generalización DESCONOCIDA.

## L. Memoization Opportunities

Ver Parte 16 (O1–O12). Orden por potencial×confianza: **O6** (discovery sin hash→ALTA), **O5** (tool results→ALTA), **O2/O4** (excerpts KB y KB_RECOMMENDATION→MEDIA), **O1** (task_summary→MEDIA), **O12** (recovery preserva artifacts→ALTA, ya existente), **O7** (claims discovery para context→MEDIA), **O3** (perfil→MEDIA), **O9** (re-lectura→BAJA/riesgosa).

## M. Required Instrumentation Before RFC

Ver Parte 17. **P0:** llamadas LLM por sesión/fase; input/output tokens estimados por delegación; modelo por llamada; comandos con exit code+hash; contador de re-producción de artifacts. **P1:** cached tokens; retrieval counter; costo de discovery (obligar `model_used`/`execution_time_seconds`); frecuencia/costo de retries y recovery; flag evidencia-vs-re-ejecución en verificación. **P2:** fingerprint de policy/prompt/worker; hash de source files; duración por gate.

## N. Open Questions

1. ¿Qué fracción del costo real es contexto repetido vs generación nueva? (sin telemetría: DESCONOCIDO)
2. ¿Cuánto del `CONTEXT_ARTIFACT` duplica literalmente entradas de discovery? (comparación de contenido no hecha)
3. ¿El prompt-caching del proveedor ya absorbe parte de la repetición de contexto? (fuera del protocolo)
4. ¿La re-ejecución de validaciones por el verifier ocurre en modo subagente real (nunca observado)? (muestra sin gate FAIL)
5. ¿Qué inputs efectivos invalidarían un artifact memoizado? (sin fingerprint no verificable)
6. ¿Debe la independencia de verificación exigir fresh tool execution o basta evidencia durable registrada? (decisión conceptual pendiente, no documentada)
7. ¿La re-curación de KB por fase ocurre en la práctica con `knowledge_base` en modo subagente? (solo observado single-instance)
8. ¿El costo de subagentes fallidos (idle listeners) es recurrente en el runtime real? (2 observaciones, un runtime)

## O. Final Assessment

1. **¿Existe evidencia de recomputación costosa?** Sí, pero **cualitativa**: repetición de contexto documentada (protocolo, artifacts, task_summary, excerpts) y rediscovery por TTL con hash sin cambio (HECHO); la magnitud en tokens es **DESCONOCIDA**.
2. **¿Dónde?** (a) contexto repetido por fase (HECHO documental); (b) rediscovery por TTL (HECHO real); (c) verificación que puede re-ejecutar validaciones (CONDICIONAL; no observado); (d) re-análisis tras clarificación/recovery (HECHO real, necesario); (e) posibles subagentes fallidos (observado 2 veces).
3. **¿Qué parte parece evitable?** Síntesis repetidas por delegación (`task_summary`, excerpts, perfil), tool results re-ejecutables, rediscovery sin cambio de hash, y — condicionalmente — la re-ejecución de validaciones en verificación. Clasificadas EVITABLE/CONDICIONAL en la Parte 4.
4. **¿Qué parte parece necesaria?** Recomputación con input nuevo (fallo, corrección, decisión del usuario), self-consistency (garantía anti-suposición), juicios de gates (auditabilidad), verificación independiente del razonamiento (fresh reasoning del verifier), recovery que incorpora el fallo.
5. **¿Qué parte permanece desconocida?** La magnitud de cada fuente de costo (tokens, modelo, cached), la frecuencia real de retries/recovery, el solape cuantitativo Discovery↔Context, y el comportamiento en modo subagente real (toda la muestra es single-instance tras fallo).
6. **¿Qué deberíamos medir antes de modificar la arquitectura?** La instrumentación P0 de la Parte 17: llamadas LLM por sesión/fase, input/output tokens estimados por delegación, modelo por llamada, comandos con exit code+hash, y contador de re-producción de artifacts; luego P1 (cached tokens, retrieval counter, costo de discovery, retries/recovery).
7. **¿Existe suficiente evidencia para comenzar a diseñar una RFC de reutilización/memoización?** **No.** La hipótesis "ARgentOS reutiliza resultados pero poco del cómputo que los produjo" es consistente con la evidencia documental y las sesiones reales, pero no está **cuantificada**; sin telemetría P0 una RFC carecería de justificación medible y de criterios de invalidación verificables. El patrón sugerido por la evidencia (Evidence/Decision Memoization con fingerprints e invalidación, en lugar de cache tradicional) queda como dirección de investigación, no como decisión.
