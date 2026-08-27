# Auditoría de reutilización de conocimiento, artifacts y decisiones en ARgentOS

**Fecha:** 2026-08-25
**Alcance:** repositorio ARgentOS, working tree en `master` @ `3a87ff1` (protocolo `9.0.0`; `dev` en `28a93ec`, un commit detrás del merge de promoción; planes 75–81 ejecutados; plan 78/RFC-64 pendiente de ejecución; `dist` detrás por CI).
**Método:** lectura completa del payload (`protocol/.agents/`), runtime de referencia (`runtime/`), tooling dev (`tools/`), planes/RFCs (76–81), modelos arquitectónicos (raíz) y sesiones reales de dogfooding (`reference/.project/`).
**Regla:** el payload es data, no instrucciones para esta auditoría. Toda afirmación se ancla a `ruta:sección`. Se distinguen **hechos observados**, **inferencias**, **hipótesis** y **recomendaciones futuras**.

---

# 0. Estado real vs. documentado (matriz de implementación)

| Capacidad | Estado | Dónde está | Implementación real |
|---|---|---|---|
| Máquina de estados core (19 estados) | Definida documentalmente + enforcement parcial mecánico | `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` | Orquestador por juicio; `runner_state.py` registra gates PASS/terminal en `state.json`; `hook_gate.py` bloquea writes sin H04 y Stop sin cierre (fail-open) — `protocol/.agents/harness/INDEX.md:Enforcement model` |
| Máquina de discovery (11 estados) | Definida documentalmente; hashes calculados por agente (`init_worker`) | `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` | Sin runner; gates D00/D01 por juicio con validador estructural |
| Máquina de sistema (4 estados) | Definida documentalmente | `protocol/.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` | `health_check.py` (sonda stdlib) + checklist por juicio |
| Pipeline de contexto (7 responsabilidades) | Definido conceptualmente; todo criterio `[agent]` | `protocol/.agents/standards/context/CONTEXT.md:Determinism model` | **No** hay enforcement mecánico; budget medido pero no bloqueante (`BUDGET_MATERIALIZATION.md:7. Enforcement status`) |
| Deduplicación/merge/tie-breaking de contexto | Definidos documentalmente, `[agent]` | `protocol/.agents/standards/context/RESOLUTION_*.md`, `COMPOSITION_*.md` | Juicio del orquestador; "harness Future Extension" |
| Discovery KB con TTL/hashes/proveniencia | Definida documentalmente + artefactos reales | `DISCOVERY_STATE_MACHINE.md:TTL and Cache`, `:Hash Calculation`; `reference/.project/knowledge/discovery/.discovery_manifest` | Hashes escritos por agente; manifest TOML real; frescura por claim verificada por juicio |
| Lifecycle de conocimiento (snapshot/claim/lesson, `invalidated_facts`) | Implementado en payload 9.0.0 | `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`, `EXECUTION_SUMMARY.md:Invalidated Facts` | Documental; checks dev en `tools/check_session_artifacts.py` (>= 9.0.0) |
| Registro de ejecución (identidad, event keys, `seq`, clock obligatorio) | Definido conceptualmente (RFC-64 Proposal); **no implementado** | `plans/rfc/64-execution-record-model.md`, `plans/78-execution-record-model.md` (Aprobado, gated a Accepted) | Contratos actuales: `clock` opcional; ENTRY sin `iteration`; METRIC sin `seq` — `protocol/.agents/contracts/METRICS.md:Event catalog` |
| Telemetría de proceso | Implementada documentalmente + agregador dev | `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`, `tools/aggregate_metrics.py` | Mide proceso (transiciones, delegaciones, budget), **no** costo LLM |
| `model_used` / `execution_time_seconds` | Opcionales, solo en manifest de discovery | `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:[runtime]` | Presente en `reference/.project/knowledge/discovery/.discovery_manifest` (`model_used = "gpt-5 (Codex)"`) |

**Hecho:** no existe un runtime ejecutable del protocolo en producción: el "runtime" es un agente LLM leyendo documentos; lo único mecánico son los scripts stdlib del harness y los checkers dev (`harness/INDEX.md:Enforcement model`). **Consecuencia para esta auditoría:** cualquier "recomputación" de conocimiento ocurre dentro de la inferencia del LLM (costo de tokens), no en código.

---

# 1. Máquina de estados efectiva

Existen **tres** máquinas declaradas: core (`AGENT_STATE_MACHINE.md`, 19 estados), discovery (`DISCOVERY_STATE_MACHINE.md`, 11 estados) y system (`SYSTEM_STATE_MACHINE.md`, 4 estados). La máquina core es la del ciclo de tarea; discovery es un subsistema invocado por el core; system es bootstrap.

## 1.1 Core — estados, transiciones y actores

Fuentes: `AGENT_STATE_MACHINE.md` (estados, transiciones, inputs/outputs, retry/recovery), `orchestrators/core/workflow/INDEX.md` (worker por fase), `orchestrators/core/roles/orchestrator.md` (delegación, discovery, review), `skills/INDEX.md` (capabilities por fase), policies H00–H11 (gates y tablas de recovery), `orchestrators/core/contracts/*` (schemas).

| Estado | Propósito | Inputs | Output | Worker (rol) | Capabilities (skills) | Gate | LLM | Sucesores |
|---|---|---|---|---|---|---|---|---|
| `SYSTEM_READY` | Health OK, `.project/` inicializado | `.last_health_check`, `knowledge/` | — | system agent | — | S00 (salida de system) | No (chequeos) | `TASK_RECEIVED` |
| `TASK_RECEIVED` | Request recibida, sin análisis | user request, `SESSION_BRIEF.md` (opcional) | — | — | — | — | No | `ANALYZING_TASK` |
| `ANALYZING_TASK` | Clasificar tarea (perfil), confianza de intención, ambigüedades | user request, session brief | `TASK_ANALYSIS.md` (+`INTENT_REFLECTION.md` HIGH) | `task_analyst` | requirement/goal/constraint-extractor, ambiguity-detector, intent-detector | H00 | **Sí** | `BUILDING_TASK_SPECIFICATION` \| `CONFIRMING_INTENT` \| `NEEDS_CLARIFICATION` \| `PLANNING` (trivial) |
| `CONFIRMING_INTENT` | Reflejar y confirmar intención; self-consistency (segunda reformulación LLM) | `TASK_ANALYSIS.md`, user request, brief | `INTENT_REFLECTION.md` | `intent_reflector` (+`intent_reflection_reviewer`) | ambiguity-detector | H11 | **Sí (mín. 2 pasadas: reflector + reviewer)** | `BUILDING_TASK_SPECIFICATION` \| `ANALYZING_TASK` \| `NEEDS_CLARIFICATION` |
| `BUILDING_TASK_SPECIFICATION` | Definir qué se hace (objetivo, AC EARS, alcance, technical approach) | `TASK_ANALYSIS.md`, `INTENT_REFLECTION.md`, brief | `TASK_SPECIFICATION.md` | `task_specification_writer` | ears-writer, task-spec-validator | H01 | **Sí** | `TASK_READY` \| `NEEDS_CLARIFICATION` |
| `NEEDS_CLARIFICATION` | Preguntar al usuario; defaults declarados en modo desatendido | respuesta del usuario | actualiza `SESSION_BRIEF.md` | orquestador | — | — | Parcial (formulación de opciones) | `TASK_RECEIVED` |
| `TASK_READY` | Spec validada, listo para contexto | `TASK_SPECIFICATION.md` | — | — | — | — | No | `GATHERING_CONTEXT` |
| `GATHERING_CONTEXT` | Colectar contexto técnico de fuentes originales | `TASK_SPECIFICATION.md`, KB excerpts (payload) | `CONTEXT_ARTIFACT.md` | `context_gatherer` | extractor, deduplicator, normalizer, summarizer | H02 (+H10 opcional antes de usar KB) | **Sí** | `CONTEXT_GATHERED` \| `NEEDS_CLARIFICATION` |
| `CONTEXT_GATHERED` | Contexto recolectado, pendiente evaluación | `CONTEXT_ARTIFACT.md` | — | — | — | — | No | `VALIDATING_CONTEXT` |
| `VALIDATING_CONTEXT` | Evaluar suficiencia/relevancia/consistencia/riesgo | `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md` | `CONTEXT_VALIDATION_REPORT.md` | `context_validator` | context-validator, completeness-checker | H03 | **Sí** | `CONTEXT_READY` \| `NEEDS_CLARIFICATION` |
| `CONTEXT_READY` | Contexto validado | spec + context + validation | — | — | — | — | No | `PLANNING` |
| `PLANNING` | Definir cómo (pasos, riesgos, estrategia de validación) | spec + context + validation (o `TASK_ANALYSIS.md` trivial) | `EXECUTION_PLAN.md` | `planner` | planner, risk-detector, tradeoff-analyzer, critic | H04 | **Sí** | `PLAN_READY` \| `NEEDS_CLARIFICATION` |
| `PLAN_READY` | Plan aprobado | `EXECUTION_PLAN.md` | — | — | — | — | No | `EXECUTING` |
| `EXECUTING` | Aplicar cambios; lee también KB discovery (`environment.md`, `development_patterns.md`) | spec + context-validation + plan | `EXECUTION_SUMMARY.md` + cambios de proyecto | `executor` (perfil por 7 preguntas) | self-review, tdd-reviewer (+ skills de perfil) | H15 pre-delegación; H05 salida | **Sí** | `VERIFYING` \| `RECOVERY` |
| `VERIFYING` | Evaluar cumplimiento de AC; **vuelve a ejecutar la estrategia de validación del plan** | spec (+análisis trivial) + plan + summary + estado del proyecto | `VERIFICATION_REPORT.md` | `verifier` | rubric-checker, artifact-validator, consistency-checker, hallucination-checker, reference-resolver | H06, H07 (+REVIEW gate si complex) | **Sí** | `COMPLETED` \| `RECOVERY` |
| `RECOVERY` | Analizar fallo, clasificar causa raíz, elegir destino | `VERIFICATION_REPORT.md`/`EXECUTION_SUMMARY.md` + artefactos de fase | `RECOVERY_REPORT.md` | `recovery_analyst` | hypothesis-generator, risk-detector | H09 (opcional) | **Sí** | `PLANNING` \| `ANALYZING_TASK` \| `BUILDING_TASK_SPECIFICATION` \| `GATHERING_CONTEXT` \| `VALIDATING_CONTEXT` \| `NEEDS_CLARIFICATION` \| `ABORT` |
| `COMPLETED` | Terminal: gates PASS, sin AC FAIL/PENDING, aprobaciones cerradas o diferidas | `VERIFICATION_REPORT.md` | — | — | — | — | No | — |
| `ABORT` | Terminal: aborto fundado | — | — | — | — | — | No | — |

**Precondiciones generales (hecho):** toda transición exige (1) requisitos del estado cumplidos, (2) inputs existentes, (3) artifact de salida conforme a su contrato, (4) transición permitida (`AGENT_STATE_MACHINE.md:Core Rules`). **Retry:** re-invocación del mismo worker sin transición cuando la tabla de recovery del gate arroja `RETRY_WORKER` con target = fase actual; de lo contrario `RECOVERY` (`harness/INDEX.md:Recovery Mechanism`). **Failure:** gate FAIL → aplicar tabla de recovery de la policy del trigger; default `RECOVERY_GENERIC` → `08-recovery.md` (`orchestrator.md:6. Decision Making`). **Escalation:** no existe escalación a un nivel superior de autoridad; existe `NEEDS_CLARIFICATION` (usuario) y `ABORT` fundado (`DECISIONS.md:D5`).

## 1.2 Discovery (sub-máquina de conocimiento)

Estados: `DISCOVERY_INIT → DISCOVERY_RUNNING → {ENV, STACK→FRAMEWORK, PATTERNS, BUSINESS} → DISCOVERY_MERGE → DISCOVERY_VALIDATE → DISCOVERY_READY | DISCOVERY_FAILED` (`DISCOVERY_STATE_MACHINE.md:Transition Graph`). Workers: `init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `patterns_worker`, `business_worker`, `synthesis_worker`. Todos LLM salvo la parte de hashes/probe que hace `init_worker`/`environment_worker` con comandos deterministas (`init_worker.md:Tasks` 3 y 9). Es la única parte del protocolo con invalidación por hash y TTL real (`DISCOVERY_STATE_MACHINE.md:TTL and Cache`).

## 1.3 System (bootstrap)

`SYSTEM_INIT → VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY → core:SYSTEM_READY`; fallo → `BOOTSTRAP_FAILED` con única excepción de autorización explícita (`SYSTEM_STATE_MACHINE.md:BOOTSTRAP_FAILED`).

---

# 2. Inventario de artifacts

## 2.1 Categorías

**Hecho:** ARgentOS **no** define las categorías `RAW / DERIVED / DECISION / VALIDATION / PLAN / EXECUTION / RESULT / OTHER` para artifacts. Su taxonomía clasifica artifacts por `kind: artifact` con dominio y contrato (`protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md:Artifacts`), y el conocimiento por `kind: snapshot | claim | lesson` (`KNOWLEDGE_LIFECYCLE.md:Knowledge types`). La clasificación pedida se aplica aquí como **lente de auditoría**, no como modelo del protocolo.

## 2.2 Tabla de artifacts

| Artifact | Propósito | Productor | Consumidores | Schema/versión | Metadata/provenance | Dependencias | Contenido | Persistencia | Clasificación (lente) |
|---|---|---|---|---|---|---|---|---|---|
| `TASK_ANALYSIS.md` | Interpretación de la request + perfil + confianza | `task_analyst` | spec writer, intent reflector, recovery | contrato `TASK_ANALYSIS.md` (schema 2.0.0) | `id`, `created_at`; lifecycle derivado del gate | user request | decisiones: perfil, confianza, ambigüedades | sesión (histórica) | DECISION + ANALYSIS |
| `INTENT_REFLECTION.md` | Intención reformulada + confirmación | `intent_reflector` | spec writer, analyst (corrección) | contrato 1.0.0 | `id`, `created_at`, `status`, `correction_cycle` | `TASK_ANALYSIS.md`, user response | decisión de intención confirmada | sesión | DECISION |
| `TASK_SPECIFICATION.md` | Definición validada de la tarea | `task_specification_writer` | context gatherer/validator, planner, executor, verifier, discoverer | contrato 3.0.0 | `id`, `created_at`; `effects` con `evidence_ref` | análisis + intención + brief | AC EARS, alcance, technical approach, assumptions, effects | sesión | PLAN (especificación) + DECISION (technical approach) |
| `CONTEXT_ARTIFACT.md` | Contexto técnico recolectado | `context_gatherer` | context validator, planner | contrato 2.0.0 | `id`, `created_at`; `evidence[]` (fuentes) | spec + KB excerpts | hechos derivados de fuentes originales (comportamiento, componentes, dependencias) | sesión | DERIVED (de fuentes + KB) |
| `CONTEXT_VALIDATION_REPORT.md` | Evaluación de suficiencia/relevancia/consistencia | `context_validator` | planner, executor | contrato 2.0.0 | `id`, `created_at`; `context_reference` | spec + context | decisión de validación + riesgos | sesión | VALIDATION + DECISION |
| `EXECUTION_PLAN.md` | Estrategia de ejecución | `planner` | executor, verifier, recovery | contrato 2.0.0 | `id`, `created_at`; `task_reference`, `context_reference` | spec + context + validation | pasos, riesgos, validación, rollback | sesión | PLAN + DECISION |
| `EXECUTION_SUMMARY.md` | Qué se hizo y estado final | `executor` | verifier, recovery, discovery (`invalidated_facts`) | contrato 4.0.0 | `id`, `created_at`; `plan_reference` | plan + spec + context-validation | evidencia de ejecución, pasos, validaciones, invalidated_facts | sesión | EXECUTION + RESULT + EVIDENCE |
| `VERIFICATION_REPORT.md` | Evaluación de cumplimiento | `verifier` | orquestador, recovery, discovery | contrato 3.0.0 | `id`, `created_at`; `evidence[]` con `class/claim_id/ref` | spec + plan + summary + proyecto | validación de AC, test results, scope, deferred | sesión | VALIDATION + RESULT + EVIDENCE |
| `RECOVERY_REPORT.md` | Causa raíz + acción correctiva | `recovery_analyst` | orquestador | contrato 1.0.0 | `id`, `created_at`, `status`; `failure_reference` | verification/summary + artefactos | decisión de recovery | sesión | DECISION |
| `REVIEW_REPORT.md` | Recomendación sobre artifact (rubric) | `reviewer` | orquestador (review gate) | contrato 1.0.0 | rubric, recommendation | artifact bajo revisión | decisión de revisión | sesión | VALIDATION + DECISION |
| `KB_RECOMMENDATION.md` | Selección de entradas KB por fase | `context_discoverer` | orquestador → payload | contrato 2.0.0 | `kind`+`path` por entrada, prioridad, confianza | KB + task | decisión de selección de conocimiento | sesión | DECISION (curation) |
| `SESSION_LOG.md` | Narrativa de decisiones/eventos | orquestador | audit, resumen, KB | contrato 1.1.0 | session_uuid, protocol_version, flags | — | decisiones, evidencia, desviaciones | sesión | EXECUTION (registro) |
| `HARNESS_REPORT.md` | Trail de gates | orquestador | orquestador, audit, discovery | contrato 1.1.0 | ENTRY JSON con checks/evidence/claim_class | artifacts gateados | resultados de validación | sesión | VALIDATION (registro) |
| `METRICS.md` | Observables de proceso | orquestador | agregador, audit | contrato 1.1.0 | METRIC JSON | — | transiciones, delegaciones, budget | sesión | EXECUTION (registro) |
| `SESSION_BRIEF.md` | Memoria corta de la sesión (intención, clarificaciones, efectos) | orquestador | analyst, reflector, spec writer | contrato 1.0.0 | metadata, clarifications `[[ ]]`, effects | intención + clarificaciones | decisiones del usuario | sesión | DECISION (acumulador) |
| `state.json` | Verdad mecánica de gates/terminal | `runner_state.py` | hooks, orquestador, audit | shape runner | session/iteration/profile/gates/status | gates | resultados de gates | sesión | EXECUTION (registro mecánico) |
| Entradas KB discovery (`*.md`) | Conocimiento pre-procesado del proyecto | workers discovery | orquestador → payload → workers | contrato `KB_DISCOVERY_ENTRY.md` (2.0.0) | `kind: snapshot`, `generated_at/updated_at`, `source_files`, `source_workers`, `source_sessions`, `status`, `previous_versions` | manifest hashes + TTL | claims derivados de fuentes | **persistente entre sesiones** | DERIVED (snapshot) |
| `.discovery_manifest` | Metadata de la KB | `synthesis_worker` | init, validate | contrato `DISCOVERY_MANIFEST.md` | hashes, ttl, shape, workers, `[runtime] model_used` | — | estado de invalidez | persistente | OTHER (registro) |
| `discovery_input.json` / `invalidation_report.json` / `worker_*.json` | Intermedios de un run | init/workers | workers downstream | `INTER_WORKER_MESSAGE` | `provenance` en partial outputs | hashes | inputs y claims parciales | sesión (`.project/<uuid>/discovery/`) | OTHER |
| Entradas curadas (`entries/kb-*.md`, lessons) | Decisiones/lecciones reutilizables | context_discoverer/cierre "What we learned" | orquestador → payload | `kind: knowledge\|lesson` | `session_id`, `protocol_version`, evidencia (lessons) | — | decisiones (con alternativa descartada), lecciones | **persistente** | DECISION (curada) |
| `project-map.md` / `technical-analysis.md` | Contexto estable del proyecto | workers del proyecto | context gatherer, planner | `PROJECT_ARTIFACTS.md` | — | — | derivados | persistente (proyecto) | DERIVED (si existen; no producidos por el protocolo) |

**Hechos relevantes para reutilización:**
- Solo `knowledge/` (discovery + curada) y marcadores (`.last_health_check`, `.last_discovery`) sobreviven a la sesión; el resto es trace histórico por sesión (`PROTOCOL_BOUNDARIES.md:Persistent project state`).
- Los artifacts de sesión **no llevan hash ni versión de instancia**; la `schema_version` es del contrato, no del artifact.
- El lifecycle (`draft/validated/superseded`) es **derivado** del registro de gates y nunca escrito a mano (`harness/INDEX.md:State dimensions`, AL-001/AL-002).
- Los intermedios de discovery son la única excepción al Artifact Safety Rule (`PROTOCOL_BOUNDARIES.md:Discovery intermediates exception`).

---

# 3. Flujo real de información

## 3.1 Flujo core (documentado y observado en sesión real `574bdb2f`)

```text
User Request
    ↓  (LLM: interpretación)
TASK_ANALYSIS.md  ──► INTENT_REFLECTION.md (HIGH auto-confirmado en la sesión real)
    ↓  (LLM: re-estructuración)
TASK_SPECIFICATION.md
    ↓  (LLM: re-lectura de fuentes originales + KB)
CONTEXT_ARTIFACT.md ──► CONTEXT_VALIDATION_REPORT.md
    ↓  (LLM: re-síntesis)
EXECUTION_PLAN.md ──► (REVIEW_REPORT.md si complex)
    ↓  (LLM: ejecución)
EXECUTION_SUMMARY.md + cambios de proyecto
    ↓  (LLM: re-evaluación contra spec/plan/summary + validaciones)
VERIFICATION_REPORT.md
    ↓
COMPLETED | RECOVERY
```

Flujo de conocimiento persistente:

```text
proyecto (fuentes originales)
    ↓  (discovery: muestreo + análisis LLM)
KB discovery (18 entradas + manifest, TTL/hashes)
    ↓  (context_discoverer: selección LLM)
KB_RECOMMENDATION.md → excerpts en payload (budget chars/4)
    ↓
worker de fase (lee excerpts + rutas a source_files si duda)
    ↓  (cierre "What we learned", 3.26.0/9.0.0)
lesson (kind: lesson, session_id, evidencia)
```

## 3.2 Tipos de reutilización observados

| Tipo | Ejemplo real/documentado | Dónde |
|---|---|---|
| Reutilizado directamente | Artefactos pasados por path en `input_artifacts`; verifier lee spec+plan+summary; planner lee spec+context+validation | `WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`; workflows 05/06/07 |
| Reconstruido | `context_gatherer` vuelve a describir comportamiento/componentes/dependencias leyendo el código, cuando la KB discovery ya los describió (sesión real: `CONTEXT_ARTIFACT.md` cita directamente `src/beaconrbx/sync/*.py`) | `03-gather-context.md:2. Gather Context` |
| Resumido | KB entries entran al payload como excerpts con budget (`context_budget`); `summarizer` en fase 03 | `CONTEXT.md:3-5`, `BUDGET_MATERIALIZATION.md` |
| Recuperado nuevamente | Discovery y context gathering y execution y verification acceden a las mismas fuentes originales; `USING_PATTERNS.md:1` manda "open them" si hay duda | workflows 03/06/07 |
| Reinterpretado por LLM | Cada worker relee los inputs completos y los reinterpreta (verifier, planner, recovery, reviewer) | todas las fases |

**Hecho:** la priority list de contexto dice que el payload incluye "Previous artifacts produced in the current session" (`CONTEXT.md:1. Priority of information`) — los artifacts **sí** fluyen hacia adelante. **Inferencia:** el costo dominante no es la falta de transporte de artifacts, sino que cada fase **reinterpreta con LLM** los mismos artifacts y puede **volver a las fuentes** que una fase previa ya analizó.

---

# 4. Auditoría de contexto por fase (construcción de cada llamada LLM)

Elementos del Execution Context por delegación (`WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`): `session_uuid`, `current_state`, `target_phase`, `role_to_adopt`, `profile`, `input_artifacts` (paths), `harness_policy`, `task_summary`, `knowledge_entries` (excerpts), `skills`, `context_budget`, `communication_style`, `technical_approach`.

El worker además lee: workflow module, rol, perfil (si aplica), skills completas (`SKILL.md`) y **el contenido completo de los artifacts de input** (`WORKER_DELEGATION_CONTRACT.md:Worker Execution`).

| Fase (LLM) | system prompt / políticas | task spec | estado | artifacts previos | fuentes originales | KB | historial | tool results | outputs previos |
|---|---|---|---|---|---|---|---|---|---|
| 00 analyze | rol+workflow+policy H00 | no (request) | sí | brief (opcional) | no | no (payload sin KB en fase 00; sesión real: `knowledge_entries: []`) | brief | no | no |
| 01 intent | rol+workflow+H11 | no | sí | análisis | no | no | brief | no | no |
| 02 spec | rol+workflow+H01 | no | sí | análisis + intención | no | no | brief | no | intención |
| 03 context | rol+workflow+H02 | sí | sí | spec | **sí (fuentes del proyecto)** | **sí (excerpts)** | brief | no | — |
| 04 validate | rol+workflow+H03 | sí | sí | spec + context | no | no | — | no | — |
| 05 plan | rol+workflow+H04 | sí | sí | spec + context + validation | no (vía context) | **sí (recomendación + excerpts)** | brief | no | — |
| 06 execute | rol+perfil+workflow+H05 | sí | sí | spec + context-validation + plan | **sí (KB manda abrir source_files si duda; proyecto a modificar)** | **sí (`environment.md`, `development_patterns.md` obligatorios si KB existe)** | brief | **sí (resultados de comandos/tests)** | plan |
| 07 verify | rol+workflow+H06/H07 | sí | sí | spec + plan + summary | **sí (estado del proyecto, tests)** | opcional | — | **sí (re-ejecuta validaciones del plan)** | summary |
| 08 recovery | rol+workflow+H09 | sí | sí | verification/summary + artefactos de fase | no | no | log | no | — |
| review (opcional/complex) | rol+rubric | sí | sí | artifact bajo revisión | no | no | — | no | — |
| context_discoverer | rol+contrato H10 | sí | sí | spec + artifacts previos | no | **sí (catálogo completo + entradas)** | — | no | — |

**Respuesta a la pregunta A/B/C/D:** la mayoría de las fases recibe **C — ambas**: conocimiento ya procesado (artifacts, excerpts) **y** acceso a fuentes originales (paths citados, `source_files`, proyecto). La fase 03 y 06/07 re-acceden a fuentes pese a existir derivados previos.

---

# 5. Detección de inferencia repetida

Convención de clasificación: `NECESARIO` = repetición requerida por el diseño (independencia/seguridad); `POTENCIALMENTE REDUNDANTE` = la arquitectura permite inferir repetición sin evidencia suficiente; `REDUNDANTE` = repetición demostrable; `DESCONOCIDO` = no se puede determinar con la evidencia actual.

| # | Qué se repite | Dónde | Por qué aparentemente | Necesaria | Evidencia | Impacto | Clasificación |
|---|---|---|---|---|---|---|---|
| R1 | Interpretación de la misma request | `ANALYZING_TASK` y `CONFIRMING_INTENT` (self-consistency genera **una segunda reformulación LLM** y la compara) | Validación de fidelidad | Sí por diseño (anti-suposición); la segunda pasada es una autocomprobación | `01-confirm-intent.md:2. Self-Consistency Check` | 2 pasadas LLM en fase 01 | NECESARIO (por diseño); la autocomprobación es costo explícito asumido |
| R2 | Re-lectura y re-interpretación del mismo artifact | Cada worker lee inputs completos; verifier relee spec+plan+summary; recovery relee verification | Workers stateless por fase | Sí para independencia de verificación; **parcial** para los demás | `WORKER_DELEGATION_CONTRACT.md:Worker Execution` | Tokens de input repetidos por fase | NECESARIO (verificación) / POTENCIALMENTE REDUNDANTE (resto) |
| R3 | Re-derivación de hechos del proyecto ya cubiertos por discovery | `GATHERING_CONTEXT` (context artifact cita fuentes: `src/beaconrbx/sync/*.py`) vs KB discovery (`architecture.md`, `development_patterns.md`, `environment.md`) | El diseño separa roles: discovery = pre-procesado; gatherer = contexto de tarea | No está claro; hay solapamiento de contenido (comportamiento, componentes, dependencias) | Sesión real `574bdb2f`: `1/05-CONTEXT_ARTIFACT.md` (Project Context/Existing Behavior) vs `knowledge/discovery/*` | Duplicación de análisis LLM de las mismas fuentes | POTENCIALMENTE REDUNDANTE |
| R4 | Selección de entradas KB por fase | `context_discoverer` corre "before delegating the real phase worker" (orquestador §4.2); contrato consume por PLANNING/EXECUTING/VERIFYING | Cada delegación re-curre el catálogo | No necesariamente; el catálogo cambia poco entre fases | `orchestrator.md:4.2`, `KB_RECOMMENDATION.md:consumed_by`; en la sesión real se produjo 1 recomendación y se reutilizó | LLM por fase si se invoca por delegación | POTENCIALMENTE REDUNDANTE |
| R5 | Re-ejecución de validaciones/tests | `VERIFYING` manda "Run Defined Validations: execute the validation strategy defined in the execution plan" cuando `EXECUTING` ya corrió validaciones intermedias y gates | Independencia de verificación | Sí parcialmente (el verifier debe verificar), pero re-ejecuta la misma suite sin memoización | `07-verify.md:2. Run Defined Validations`; sesión real: executor corrió 8 validaciones, verifier registró 8 con evidencia (comandos/log) | Duplicación de tiempo/costo de cómputo (tests) | POTENCIALMENTE REDUNDANTE (falta evidencia de re-ejecución real; H06 acepta evidencia en log) |
| R6 | Regeneración completa de la KB de discovery | `DISCOVERY_INIT→…→READY` regenera entradas cuyo input no cambió cuando vence el TTL (24h proyecto / 6h env) | Invalidación por tiempo, no por contenido | Parcial: el TTL garantiza frescura pero paga rediscovery completo | `DISCOVERY_STATE_MACHINE.md:TTL and Cache`; `reference/.project/574bdb2f/.../invalidation_report.json` (18 entradas invalidadas por TTL + hash); P14 rechazado como defecto en `ARCHITECTURAL_PROBLEM_MODEL.md:6` | Rediscovery completo = LLM + probe | POTENCIALMENTE REDUNDANTE (el modelo ya permite scoped revalidation para `invalidated_facts`; el TTL de proyecto es grueso) |
| R7 | Re-análisis tras clarificación | `NEEDS_CLARIFICATION → TASK_RECEIVED → ANALYZING_TASK` re-analyza y H00 re-corre; la spec se reescribe | Los inputs (decisiones del usuario) cambiaron | Sí: hubo cambio real de input | Sesión real: H00 re-entry + `TASK_ANALYSIS.md` actualizado | Re-análisis completo LLM | NECESARIO (input cambió) |
| R8 | Re-análisis en recovery loop | `RECOVERY → PLANNING/ANALYZING_TASK/…` re-ejecuta fases previas completas | Fallo de gate | Depende: si el defecto es de formato, el diseño ya previó `RETRY_WORKER` sin transición; si es semántico, el re-análisis es necesario | `harness/INDEX.md:Recovery Mechanism`; H04 tabla (#3 `retry_count>=1 → RECOVERY_GENERIC`) | Costo de re-análisis de fases completas | NECESARIO (semántico) / REDUNDANTE evitable ya mitigado (formato → RETRY_WORKER, B-2) |
| R9 | Registro duplicado del mismo hecho | Un gate PASS se registra en `state.json` + `HARNESS_REPORT.md` + `SESSION_LOG.md` + `METRICS.md` | Roles de registros no disjuntos (RFC-64 lo formaliza) | No (duplicación de registro, costo bajo determinista) | `harness/INDEX.md:State dimensions`; sesión real (15 ENTRYs, 16 METRICs, log) | Casi nulo (texto) | REDUNDANTE (pero costo ~0; parte del diseño documental) |
| R10 | Re-validación estructural del mismo artifact | Cada gate corre `gate_validator.py` sobre el artifact; H00 se corrió 2 veces en la sesión real | Gate por transición | Sí (barato, determinista) | sesión real HARNESS (H00 x2) | Bajo | NECESARIO |
| R11 | Re-derivación de decisiones de implementación | `technical_approach` se decide en spec, se repite en plan y en summary; `task_profile` se decide en análisis y se revalida en cada gate | Trazabilidad | Parcial (copias de trazabilidad vs re-decisión) | contratos 02/05/06 | Tokens bajos | NECESARIO (trazabilidad) |
| R12 | Múltiples workers producen conocimiento equivalente | discovery workers + context_gatherer + (opcionalmente) planner describen arquitectura/comportamiento | Solape de dominios | Desconocido | R3 + KB discovery entries | Depende del proyecto | DESCONOCIDO |

---

# 6. Dependencias de artifacts

**Hecho:** no existe un **dependency graph explícito** ni fingerprinting de inputs para los artifacts de sesión. Existen:

- **Dependencias declaradas por referencia:** `task_reference`, `context_reference`, `plan_reference`, `failure_reference`, `evidence.ref` (`VERIFICATION_REPORT.md:Evidence`), citas `path:section` validadas por `gate_validator.py` y H04/H05/H06.
- **Dependencias implícitas:** EXECUTION_SUMMARY depende de los pasos del plan; VERIFICATION depende de AC; contexto depende de la spec; plan depende de contexto validado; delegación depende de artifacts previos.
- **Grafo real aproximado (derivado de la arquitectura, no del ejemplo del prompt):**

```text
USER_REQUEST → TASK_ANALYSIS → INTENT_REFLECTION → TASK_SPECIFICATION
        │                                              │
        │                                              ▼
        │                              CONTEXT_ARTIFACT ← (KB discovery + fuentes)
        │                                              │
        │                                              ▼
        │                              CONTEXT_VALIDATION_REPORT
        │                                              │
        │                                              ▼
        │                              EXECUTION_PLAN ← (KB_RECOMMENDATION)
        │                                              │
        │                                              ▼
        │                              EXECUTION_SUMMARY (+ invalidated_facts)
        │                                              │
        │                                              ▼
        │                              VERIFICATION_REPORT → COMPLETED/RECOVERY
        └── (SESSION_BRIEF / SESSION_LOG / HARNESS / METRICS / state.json: registros)

KB discovery: fuentes → [hashes] → entradas → manifest → (freshness) → KB_RECOMMENDATION → payload
```

- **Único grafo con invalidación mecánica:** discovery (`config_files_hash`, `sample_files_hash`, `environment_hash`, `structure_hash` → entradas stale) — `DISCOVERY_STATE_MACHINE.md:Hash Calculation`, `DISCOVERY_MANIFEST.md:[hashes]`.
- **Provenance de KB:** `source_files`/`source_workers`/`source_sessions` por entrada y por claim (`KB_DISCOVERY_ENTRY.md:Required Front Matter`; freshness per claim en `KNOWLEDGE_LIFECYCLE.md`).

**Carencias (hecho):** no hay hashes de artifacts de sesión; no hay versión de worker/capability/prompt/modelo en ninguna dependencia; no hay grafo de dependencias de artifacts; `previous_versions` es opcional y solo en KB.

---

# 7. Invalidación

| Cambio | ¿ARgentOS puede detectarlo hoy? | Mecanismo | Evidencia |
|---|---|---|---|
| Cambio de task | Sí (nueva iteración/sesión; clarificación re-analyza) | state machine / iteration boundary | `PROTOCOL_BOUNDARIES.md:Iteration boundary` |
| Cambio de contexto (proyecto) | **Parcial** | discovery hashes (config/sample/env/structure) + TTL; contexto de sesión no se revalida salvo recovery | `DISCOVERY_STATE_MACHINE.md:Invocation Conditions` |
| Cambio de source | **Sí, solo KB discovery** | hashes; `invalidated_facts` post-ejecución (9.0.0) | `EXECUTION_SUMMARY.md:Invalidated Facts`, `KNOWLEDGE_LIFECYCLE.md:Invalidation` |
| Cambio de knowledge asset | **Parcial (juicio)** | `curation_status` noisy/retired; frescura por claim + proveniencia resoluble; sin detección automática de deriva entre entradas | `KNOWLEDGE_CURATION.md:Entry lifecycle` |
| Cambio de policy | **No** | — | no existe versión de policy en dependencias |
| Cambio de worker | **No** | workers son transitorios; actor = rol+modo solo en RFC-64 (no implementado) | `plans/rfc/64-execution-record-model.md:D-004` |
| Cambio de capability | **No** | — | — |
| Cambio de prompt | **No** | — | — |
| Cambio de modelo | **No** | `model_used` opcional solo en manifest discovery, sin regla de invalidación | `DISCOVERY_MANIFEST.md:[runtime]` |
| Cambio de schema | **Parcial** | `schema_version` en contratos; trazas históricas no se reescriben (RFC-46); sin invalidación de artifacts existentes | `protocol/.agents/contracts/*.md` front matter |
| Cambio de artifact dependency | **No explícito** | lifecycle `superseded` derivado de gates (AL-003: no consumir superseded); recovery corrige el artifact más temprano inválido | `harness/INDEX.md:State dimensions`; `AGENT_STATE_MACHINE.md:RECOVERY` |

**Hecho:** la invalidación real existe **solo** en el dominio de conocimiento (discovery + lessons) y es de consumo (TTL/hash/proveniencia), no de dependencias entre artifacts de sesión. Los artifacts de sesión son registros inmutables; su "invalidación" es la corrección en fases previas vía recovery.

---

# 8. Reutilización dentro de una misma ejecución

**Mecanismos que existen (hecho):**
1. **Artifacts como moneda de transición:** cada estado exige inputs existentes y outputs validados (`AGENT_STATE_MACHINE.md:Artifact-Based Transitions`); los artifacts fluyen por `input_artifacts`.
2. **`SESSION_BRIEF.md`:** evita re-preguntar decisiones ya resueltas en la sesión (`CONTEXT.md:6. Session Brief`).
3. **Recovery conservador:** si el contexto sigue válido, se preserva al volver a planning (`08-recovery.md:4. Update Artifacts if Needed`).
4. **Resume:** reanudar una iteración parcial reutiliza el último artifact intacto y no reescribe los previos (`PROTOCOL_BOUNDARIES.md:Resume procedure`).
5. **Deduplicación/compresión de contexto:** skills `deduplicator`/`summarizer` en fase 03 y reglas de `RESOLUTION_DEDUPLICATION.md`/`COMPOSITION_COMPRESSION.md` (juicio del orquestador).
6. **KB excerpt con budget:** los excerpts viajan en el payload; no se incluyen artifacts completos de sesiones previas (`CONTEXT.md:2. Omission rules`).

**Lo que NO existe (hecho):**
- Memoización de análisis/decisiones/validaciones/planes: nada impide re-calcular una decisión ya tomada en la misma ejecución cuando una fase se re-ejecuta (recovery, clarificación).
- Cache de resultados de herramientas/retrieval: si dos fases consultan la misma fuente (archivo, test, web), la segunda vuelve a leer/ejecutar.
- Deduplicación entre artifacts de fases distintas (el `deduplicator` opera dentro de la fase 03, no entre artifacts).

**Inferencia:** la reutilización intra-ejecución es **de transporte** (artifacts), no **de cómputo** (resultados de inferencia). El protocolo reutiliza outputs, pero no evita re-derivar el mismo output dos veces en la misma ejecución (R2, R8).

---

# 9. Reutilización entre ejecuciones

**Qué sobrevive (hecho):** `knowledge/` (discovery + entradas curadas + lessons), `.last_health_check`, `.last_discovery`, `.project/skills/` (`PROTOCOL_BOUNDARIES.md:Persistent project state`). Las carpetas de sesión quedan como trace histórico.

**Cómo se identifica:** entradas KB por `title`/`path` + `kind` (`discovery|knowledge|lesson`); lessons por `session_id`; sesiones por UUID (`KB_RECOMMENDATION.md:Required sections`).

**Cómo se versiona:** manifest con `generated_at/updated_at/ttl_hours/role_version/task_scope/project_shape` + hashes; entradas con `updated_at`/`previous_versions` (opcional); `role_version` solo describe al orquestador de discovery.

**Cómo se relaciona con inputs:** por `source_files`/`source_workers`/`source_sessions` y por hashes; una claim es reutilizable si está fresca y su proveniencia resuelve (`KNOWLEDGE_LIFECYCLE.md:Freshness per claim`).

**Validez:** TTL (24h/6h) + hash + `invalidated_facts` + `curation_status`.

**Reutilización por otra ejecución:** **sí, solo vía KB** — el `context_discoverer` recomienda entradas y el orquestador las incluye como excerpts en el payload. Prohibido incluir artifacts completos de sesiones previas (`CONTEXT.md:2`).

**Aislamiento entre ejecuciones:** sesiones aisladas por UUID; resume solo dentro de la misma sesión. **No hay** cache/memoization de artifacts entre ejecuciones.

**Hecho:** la única reutilización entre ejecuciones es conocimiento **curado** (discovery + lessons + entradas), con freshness; no existe reutilización de análisis/decisiones/validaciones/planes entre ejecuciones.

---

# 10. Decision Memoization

**Hecho:** ARgentOS **no distingue formalmente** `DATA / INFORMATION / DERIVED INFORMATION / DECISION / VALIDATION RESULT` como categorías. Las decisiones viven embebidas en artifacts:

| Decisión | Dónde se produce | ¿Se reutiliza durablemente? | ¿Se vuelve a calcular? |
|---|---|---|---|
| Perfil de tarea (trivial/standard/complex) | `TASK_ANALYSIS.md` | Solo en la sesión (referencia en gates) | Se recalcula si `ANALYZING_TASK` se re-entra (clarificación/recovery) |
| Confianza de intención | `TASK_ANALYSIS.md` / `INTENT_REFLECTION.md` | Solo sesión | Se recalcula en re-análisis |
| Interpretación de la request | `TASK_ANALYSIS.md` | No | Sí (cada re-entrada) |
| Selección de technical approach | `TASK_SPECIFICATION.md` | Solo sesión | Copiada, no recalculada, en plan/summary (R11) |
| Selección de capability/skill | `SESSION_LOG.md` (delegación) | No | Se recalcula por delegación (tabla de activación) |
| Selección de worker/profile | `SESSION_LOG.md` | No | Se recalcula por ejecución (7 preguntas) |
| Validación de contexto | `CONTEXT_VALIDATION_REPORT.md` | Solo sesión | Se recalcula si la fase 04 se re-ejecuta |
| Estrategia de ejecución | `EXECUTION_PLAN.md` | No | Se recalcula en recovery→planning |
| Verificación | `VERIFICATION_REPORT.md` | No | Se recalcula por cada verificación |
| Causa raíz recovery | `RECOVERY_REPORT.md` | No (salvo lección curada) | Cada recovery |
| Decisión del usuario (clarificación) | `SESSION_BRIEF.md` | **Sí, dentro de la sesión** (evita re-preguntar) | No vuelve a preguntarse |
| Decisión arquitectónica del proyecto | KB curada (`kb-001`), ADRs | **Sí, entre sesiones** (curada manualmente) | No (si está curada) |
| Lección de sesión | cierre "What we learned" → `kind: lesson` | **Sí, entre sesiones** (9.0.0) | No (si pasa el filtro de curación) |

**Hallazgo clave:** las decisiones operativas del protocolo (perfil, capacidad, estrategia, validación, verificación) **no son artifacts durables reutilizables**; se recalculan cada vez que su fase se re-ejecuta. Las únicas decisiones que se vuelven durables son las del usuario (brief) y las curadas como conocimiento (ADRs/lessons), con curation manual y sin fingerprint de inputs.

---

# 11. Evidencia de costo (telemetry, logs, execution reports)

**Lo que existe (hecho):** `METRICS.md` + `HARNESS_REPORT.md` + `SESSION_LOG.md` + `state.json` por sesión; agregador `tools/aggregate_metrics.py` (catálogo de `PROTOCOL_METRICS.md`); medidor `tools/measure_context_budget.py` (rule `ceil(chars/4)`).

**Datos de la sesión real `574bdb2f` (hecho):**
- 15 invocaciones de harness (H15 x2, H00 x2, H11, H01, D00, D01, H10, H02, H03, H04, H05, H06, H07), todas PASS.
- 24 eventos METRIC: 1 `session_start`, 14 `state_transition`, 3 `delegation` (solo 3 fases registradas por delegación; el resto single-instance), 1 `failure` F1, 5 `flag_evidence`; **sin** `context_budget` ni `context_candidates` registrados (eventos que la sesión no produjo — P4 del Problem Model).
- `duration_ms: 0` en todos los ENTRYs; `session.duration_ms` mezcla relojes (NBI-1: no confiable).
- Ejecución: 1455 tests, 8 validaciones, 2h de ventana de sesión.

**Lo que NO se mide (hecho):**
- **No hay** input tokens, output tokens, cached tokens, ni conteo de llamadas LLM por fase.
- No hay costo aproximado por sesión/fase.
- No hay modelo por llamada (solo `model_used` opcional en manifest discovery).
- No hay retries/duraciones por gate (duration_ms=0).
- No hay telemetry de retrieval (qué fuente se leyó cuántas veces) ni de inferencia repetida.

**Conclusión del apartado (hecho):** la telemetría mide el **proceso** (transiciones, gates, delegaciones, budget declarado/consumido), explícitamente "never the content" (`PROTOCOL_METRICS.md:Privacy rule`), y **no** permite responder con números cuánto cuesta la inferencia repetida. La ausencia de medición de costo/tokens es en sí una carencia arquitectónica para evaluar Artifact/Decision Reuse.

---

# 12. Hallazgos

## H1 — Redundancias comprobadas

1. **Registro duplicado del mismo hecho en 4 registros** (`state.json` + HARNESS + SESSION_LOG + METRICS): demostrable en la sesión real (15 ENTRYs, 24 METRICs, log por evento); costo bajo (texto determinista). Clasificación R9. Es duplicación de representación, no de inferencia.
2. **Re-interpretación LLM del mismo artifact por múltiples fases**: los workers releen inputs completos (delegación → lectura). Demostrable en el contrato; costo de tokens por fase. Parte necesaria del modelo de verificación independiente, redundante en el resto (R2).
3. **Doble pasada LLM en fase 01** (reflection + self-consistency, más reviewer opcional): demostrable en `01-confirm-intent.md`; costo asumido por diseño (R1).

## H2 — Redundancias probables

1. **Context gathering re-deriva hechos que discovery ya produjo** (arquitectura, comportamiento, dependencias, environment): la sesión real muestra solape de contenido entre `CONTEXT_ARTIFACT.md` y la KB discovery; sin medición de tokens no es demostrable (R3).
2. **`context_discoverer` por fase** puede re-curar el mismo catálogo para PLANNING/EXECUTING/VERIFYING (R4); en la sesión real se usó una sola recomendación.
3. **Verificación re-ejecuta la estrategia de validación** que ejecución ya corrió (R5); H06 acepta evidencia del log, así que la re-ejecución puede evitarse en la práctica — indeterminado.
4. **Rediscovery completo por TTL** aunque los hashes no cambiaron (R6): el diseño permite revalidación scoped solo vía `invalidated_facts`; el TTL de proyecto invalida las 18 entradas juntas (evidencia real en `invalidation_report.json`). El Problem Model rechazó P14 como defecto, pero la medición de costo real sigue ausente.

## H3 — Oportunidades de reutilización

1. **Decisiones del usuario** (`SESSION_BRIEF.md`) y **lecciones curadas** (lessons): ya reutilizables; ampliables a decisiones operativas.
2. **KB discovery con hashes/TTL/proveniencia**: el mecanismo de invalidación más completo del protocolo; candidato natural de patrón para otros derivados.
3. **`EXECUTION_SUMMARY`/`VERIFICATION_REPORT` como evidencia reutilizable**: hoy solo alimentan `invalidated_facts` y lecciones; podrían alimentar reutilización de validaciones (resultados de tests) sin re-ejecución.
4. **`KB_RECOMMENDATION.md`** ya es un artifact de decisión (selección de conocimiento) con `kind`+`path`; reutilizable como patrón de "decision memo".
5. **Resume/recovery**: ya reutilizan artifacts intactos; extensible a memoización de fases no afectadas por el fallo.

## H4 — Falta de mecanismos

1. **Identidad/fingerprint de artifacts** (hash de contenido, versión de instancia, dependencias con inputs): no existe para artifacts de sesión.
2. **Dependency graph explícito** con invalidación por dependencia (policy/worker/capability/prompt/modelo/schema): no existe.
3. **Cache/memoization de inferencia y de resultados de herramientas**: no existe.
4. **Telemetría de costo** (tokens por llamada, modelo, cached, retrieval): no existe; sin ella no se puede justificar ni medir una RFC de reuse.
5. **Registro de ejecución correlacionado** (RFC-64: `execution_id`, `seq`, `clock` obligatorio, `context_budget` pareado): definido, no implementado.
6. **Distinción formal DATA/INFORMATION/DERIVED/DECISION/VALIDATION** como categorías de artifacts: no existe.

## H5 — Riesgos de reutilizar artifacts o decisiones

1. **Staleness de contexto**: reutilizar `CONTEXT_ARTIFACT`/KB sin revalidar cuando las fuentes cambiaron produce planes sobre hechos viejos (mitigación parcial: TTL/hashes; sin hash de artifacts de sesión).
2. **Decisiones dependientes de la conversación**: reutilizar decisiones sin capturar su dependencia de clarificaciones (brief) puede propagar supuestos no confirmados.
3. **Verificación no independiente**: memoizar resultados de validación de la fase de ejecución para la verificación degradaría la garantía de independencia (la verificación es External-actor-dependent/multi-agent).
4. **Versionado de protocolo**: reutilizar artifacts producidos con un `protocol_version` distinto viola la regla de trazas inmutables (RFC-46) y la semántica de `COMPLETED`/gates; requiere registrar versión en el artifact reutilizado.
5. **Proveniencia rota**: reutilizar conocimiento cuya `source_files`/`source_sessions` ya no resuelven viola KN-003/KN-005; el diseño ya lo prohíbe para KB, habría que extenderlo.
6. **Invalidación por modelo/prompt/policy**: sin versión de estos, un artifact memoizado puede ser válido bajo un modelo y no bajo otro.
7. **Budget**: reutilizar contextos completos podría inflar el payload sin control (los budgets actuales limitan solo la porción KB, no artifacts de sesión — `BUDGET_MATERIALIZATION.md:3`).

---

# 13. Matriz final

| Artifact / conocimiento | Productor | Consumidores | ¿Se reutiliza? | ¿Se regenera? | Dependencias conocidas | Invalidación | Riesgo |
|---|---|---|---|---|---|---|---|
| TASK_ANALYSIS | task_analyst | spec, intent, recovery | Dentro de sesión | Sí, en re-entradas | user request, brief | gates H00 (derivado) | Bajo |
| INTENT_REFLECTION | intent_reflector | spec, analyst | Dentro de sesión | Sí, en correcciones | análisis, usuario | H11 | Bajo |
| TASK_SPECIFICATION | spec_writer | context, plan, exec, verify, discovery | Dentro de sesión | Sí, en recovery/clarificación | análisis, intención, brief | H01 | Medio (supuestos) |
| CONTEXT_ARTIFACT | context_gatherer | validator, planner | Dentro de sesión | Sí | spec, fuentes, KB | H02; sin hash de fuentes | **Alto** (staleness) |
| CONTEXT_VALIDATION | context_validator | planner, executor | Dentro de sesión | Sí | spec, context | H03 | Medio |
| EXECUTION_PLAN | planner | executor, verifier, recovery | Dentro de sesión | Sí, en recovery | spec, context, validation | H04 | Medio |
| EXECUTION_SUMMARY | executor | verifier, recovery, discovery | Dentro de sesión; `invalidated_facts` persiste efecto | No (inmutable) | plan, spec | H05 | Bajo |
| VERIFICATION_REPORT | verifier | orquestador, recovery | Dentro de sesión | No | spec, plan, summary, proyecto | H06/H07 | Bajo |
| RECOVERY_REPORT | recovery_analyst | orquestador | No | No | verification/summary | H09 (opcional) | Bajo |
| REVIEW_REPORT | reviewer | orquestador | No | No | artifact revisado | REVIEW gate | Bajo |
| KB_RECOMMENDATION | context_discoverer | orquestador→payload | Dentro de sesión (excerpts) | Potencialmente por fase | KB, task | H10 | Medio (selección stale) |
| SESSION_BRIEF | orquestador | analyst, spec, reflector | Dentro de sesión | No (acumula) | usuario | — | Bajo |
| state.json/HARNESS/METRICS/SESSION_LOG | orquestador/runner | audit, hooks | No (trace) | No | gates | versión de protocolo | Bajo |
| KB discovery (18 entradas) | workers discovery | payload→workers | **Entre sesiones** | Sí, por TTL/hash | fuentes (hashes), manifest | **TTL + hashes + invalidated_facts + provenance** | Medio (TTL grueso) |
| `.discovery_manifest` | synthesis_worker | init, validate | Entre sesiones | No (se actualiza) | hashes, workers | — | Bajo |
| Entradas curadas / lessons | discoverer / cierre | payload→workers | **Entre sesiones** | No (curation) | sesión, evidencia | freshness + curation_status | Medio (deriva no detectada) |
| project-map / technical-analysis | proyecto | gatherer, planner | Entre sesiones (si existen) | Manual | fuentes | reglas de `PROJECT_ARTIFACTS.md` | Medio |

---

# 14. Conclusión

## Respuestas

1. **¿Dónde existe recomputación actualmente?** En tres capas: (a) **intra-fase**: cada worker LLM reinterpreta artifacts completos y puede volver a fuentes originales (context gathering, execution, verification); (b) **intra-ejecución**: recovery/clarificación re-ejecutan fases completas; la fase 01 hace doble pasada LLM por diseño; (c) **entre ejecuciones**: rediscovery completo por TTL (6h/24h) aunque los hashes no cambien; verificación puede re-ejecutar validaciones ya corridas.
2. **¿Dónde existe conocimiento reutilizable?** KB de discovery (snapshots con hashes/TTL/proveniencia), entradas curadas y lessons (9.0.0), `SESSION_BRIEF` (decisiones del usuario), y los artifacts de sesión como evidencia (summary/verification).
3. **¿Qué mecanismos actuales permiten reutilizarlo?** Artifacts como moneda de transición; payload con excerpts con budget; `context_discoverer` + `KB_RECOMMENDATION`; frescura por claim con proveniencia resoluble; `invalidated_facts` → revalidación scoped; resume/recovery que preservan artifacts intactos; deduplicación/compresión de contexto por juicio.
4. **¿Qué mecanismos faltan?** Fingerprint/dependencias de artifacts (hash, versión de instancia, grafo); memoización de inferencia y de resultados de herramientas; telemetría de costo/tokens/modelo/retrieval; registro de ejecución correlacionado (RFC-64); categorías formales DATA/DERIVED/DECISION/VALIDATION; invalidación por policy/worker/capability/prompt/modelo.
5. **¿Qué riesgos tendría reutilizar artifacts o decisiones?** Staleness de contexto, decisiones sin dependencia de clarificaciones, degradación de la independencia de verificación, violación de inmutabilidad de trazas por versión de protocolo, proveniencia rota (KN-003/005), dependencia de modelo/prompt, y desborde de budget.
6. **¿Qué información adicional necesitamos para evaluar una RFC de Artifact/Decision Reuse?** Mediciones reales de tokens por fase y por llamada, modelo y cached tokens; conteo de re-lecturas de fuentes por ejecución; costo real de rediscovery (TTL vs hash); frecuencia de recovery loops y su costo; cuánto de `CONTEXT_ARTIFACT` duplica KB discovery; y una decisión sobre si la verificación independiente debe re-ejecutar o puede reutilizar evidencia con clase verificada.
7. **¿Qué partes de la arquitectura deberían permanecer sin cambios?** El modelo de artifacts como moneda de transición; el flujo de verificación independiente (H06/H07 + evidencia con clases); la separación core/discovery/system; la regla de trazas inmutables y versionado de protocolo; el lifecycle de conocimiento con freshness/proveniencia; los budgets de KB y su medición.

## Separación rigurosa

- **Hechos observados:** todo lo citado a `protocol/.agents/…:sección`, `plans/…`, `reference/.project/…` y sesiones reales (secciones 0–11).
- **Inferencias:** el costo dominante es reinterpretación LLM (sección 3.2, 4), reutilización de transporte no de cómputo (sección 8), y que las decisiones operativas se recalculan por diseño (sección 10).
- **Hipótesis:** R3/R4/R5/R6/R12 (solape context↔KB, re-curation por fase, re-ejecución de validaciones, rediscovery por TTL, equivalencia de knowledge entre workers) — sin telemetría de costo no son demostrables.
- **Recomendaciones futuras (fuera de alcance de esta auditoría):** medir antes de proponer; ningún diseño de RFC se adelanta aquí.
