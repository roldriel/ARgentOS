# Índice de planes — ARgentOS

Estado al 2026-08-16. La **serie de remediación de la auditoría 2.0.1** está
completa: RFC-29…56 `Accepted` (las 23 RFCs de la serie 32…54 se revisaron una
por una vía RFC-56, plan 57) y todos los planes numerados `Executed`. El
trabajo activo es la remediación de la **auditoría de sistema 3.1**
(`AUDITORIA_SISTEMA_2026-08-16.md`). `master`/`dist` están en `3.19.0` (tags
anotados `3.16.0`–`3.19.0`); `dev` lleva las versiones en curso `3.20.0`–
`3.25.0` sin publicar. El 12 ago 2026 se
completó la remediación de la auditoría de documentación
(`docs/AUDITORIA_DOCUMENTACION.md`, fuera del payload): AGENTS.md raíz
operativo, plantillas de plan/RFC + `tools/check_plan_structure.py`, tests
centralizados en `tests/`, batería en CI sin path filters, disolución de `dev/`
(`tools/`, `runtime/`, `docs/` en raíz) y `tools/check_dist_sync.py`. El 14 ago
2026 se agregó `AUDITORIA_SISTEMA.md` (tracker vivo de remediación del sistema)
y se unificó la definición de batería en `docs/VERSIONING.md` §4.1. El 14–15
ago 2026 se ejecutaron los planes 58–68 (remediación de la auditoría de
sistema, cierre de backlog B-6 y validador obligatorio F1-B, versiones
3.9.0–3.19.0). Los planes de construcción del protocolo (dominios, taxonomía,
discovery) están implementados; sus versiones históricas viven en `archive/`.

## Novena serie: remediación de la auditoría de sistema 3.1 (16 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `69-remediacion-bloque-0.md` | — (vía plan, Clase B) | Executed | Bloque 0 de `AUDITORIA_SISTEMA_2026-08-16.md`: conteo de scripts del harness, literal de discovery budget, snapshot del INDEX, `[Unreleased]` del changelog, conteos de auditorías previas y modelo produced_by/consumed_by de contratos de discovery. Versión 3.20.0. |
| `70-remediacion-bloque-1.md` | — (vía plan, Clase B) | Executed | Bloque 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: alineación del contrato de verificación con H06 (campo `evidence` opcional), reconciliación de salidas de discovery (workflows + taxonomía, naming de contratos por entrada) y chequeo mecánico bidireccional de salidas de state machines en el checker de coherencia taxonómica. Versión 3.21.0. |
| `71-remediacion-bloque-2.md` | — (vía plan, Clase B) | Executed | Bloque 2 de `AUDITORIA_SISTEMA_2026-08-16.md`: validador estructural profile-aware para H04 (camino trivial, F-A), declaración del gate trivial en H00 e INDEX (F-B) y cobertura bidireccional de gates en el checker de coherencia taxonómica. Versión 3.22.0. |
| `72-remediacion-bloque-3-parte-1.md` | — (vía plan, Clase B) | Executed | Bloque 3 parte 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: evidencia determinista de tests en el validador H06, registro de desviaciones documentadas en `HARNESS_REPORT.md`/`harness/INDEX.md` con validación en el checker de sesión, y tool dev-only de auditoría post-hoc de gates. Versión 3.23.0. |
| `73-remediacion-bloque-3-parte-2.md` | RFC-59 | Executed | Bloque 3 parte 2 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 13/14/16): recovery context con derivación/registro de variables de las tablas, ranking de destinos múltiples de recovery y procedimiento de reanudación de sesión. Versión 3.24.0. |
| `74-remediacion-bloque-4.md` | RFC-60 | Executed | Bloque 4 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 19/20/21): contabilidad mecánica del Context Budget (estado measured + tool de medición), modelo de confianza de métricas (clases Derived/Recorded/Verified + `--audit` del agregador) y endurecimiento de la superficie de bypass del hook (deny de Write/Edit sin target). Versión 3.25.0. |

## Décima serie: consentimiento y visibilidad del discovery (24 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `75-discovery-consent-visibility.md` | RFC-61 | Executed | Gate de consentimiento del discovery (`discovery_require_consent`), scope `lite`, sección "Qué aprendimos" en el cierre de tarea y skill `/discovery`. Versión 3.26.0. |

## Undécima serie: decisiones arquitectónicas post-auditoría (25 ago 2026)

RFCs de modelo conceptual derivadas de `ARCHITECTURAL_DECISION_MODEL.md` (basado en
`ARCHITECTURAL_PROBLEM_MODEL.md`). RFC-62 `Accepted` (plan 76); RFC-63
`Accepted` (plan 77); RFC-64 tiene plan de ejecución redactado (plan 78, gated
a `Accepted` — Clase A de RFC-56); RFC-65 `Accepted` (plan 79); RFC-66
`Accepted` (plan 80); RFC-67 `Accepted` (plan 81); ninguna RFC habilita
modificar `protocol/.agents/` hasta su plan de ejecución con la vía de
autorización completa.

| RFC | Status | Descripción |
|---|---|---|
| `rfc/62-guarantee-model-and-enforcement-boundaries.md` | Accepted (plan 76) | Garantías clasificadas y matriz de enforcement (D0, D11). |
| `rfc/63-state-and-artifact-lifecycle-model.md` | Accepted (plan 77) | Dimensiones de estado, lifecycle de artefactos y semántica de COMPLETED (D1, D2, D3). |
| `rfc/64-execution-record-model.md` | Proposal (plan 78) | Identidad, registros, temporalidad y observabilidad de la ejecución (D5, D6, D7, D10). |
| `rfc/65-evidence-and-verification-model.md` | Accepted (plan 79) | Clases de evidencia y regla VERIFIED (D4, D12). |
| `rfc/66-authorization-and-capability-model.md` | Accepted (plan 80) | Frontera de efectos y bloque `effects` (D8, D11). |
| `rfc/67-knowledge-lifecycle-model.md` | Accepted (plan 81) | Lifecycle mínimo de conocimiento (D9). |

## Duodécima serie: modelo de garantías y fronteras de enforcement (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `76-guarantee-model-enforcement-boundaries.md` | RFC-62 | Executed | Catálogo cerrado de garantías con cinco clases, matriz de enforcement por capa en el payload y la guía de adopción, regla operacional de claims (evidencia o atestación/inferencia), reemplazo de "zero hallucinations" como garantía técnica y celdas External en los checkers dev. Versión 4.0.0 (MAJOR). |

## Decimotercera serie: modelo de estado y lifecycle de artefactos (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `77-state-artifact-lifecycle-model.md` | RFC-63 | Executed | Dimensiones de estado con entidad propia (Task State, Gate State, Artifact Lifecycle) y cuatro derivadas (Execution, Verification, Approval, Plan), lifecycle de artefactos derivado del registro de gates (nunca escrito a mano), semántica de COMPLETED relativa al alcance confirmado con `Deferred Items`, y resolución del review gate como Gate State sobre REVIEW_REPORT. Versión 5.0.0 (MAJOR). |

## Decimocuarta serie: modelo de registro de ejecución (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `78-execution-record-model.md` | RFC-64 | Aprobado para ejecución | Identidad de ejecución por composición (`execution_id = (session_id, iteration)`), roles disjuntos de los cuatro registros, alcance de `state.json` (gates de transición H00–H07, H11 + status terminal), semántica temporal UTC con `clock` declarado, event keys en ENTRY/METRIC (`iteration`/`seq`), reconciliación bidireccional y de timestamps en `--audit`, y registro obligatorio de `context_budget` por delegación con budget. Gated a RFC-64 `Accepted` (Clase A, RFC-56). Versión 6.0.0 (MAJOR). |

## Decimoquinta serie: modelo de evidencia y verificación (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `79-evidence-and-verification-model.md` | RFC-65 | Executed | Clases de evidencia mínimas (`observation`/`measurement`/`attestation`/`assertion`/`reference`), bloques `[[evidence]]` con `class`/`claim_id`/`ref` en VERIFICATION_REPORT y en los ENTRY de HARNESS_REPORT, reglas de suficiencia por ítem `[gate]`/`[agent]`, invariante VERIFIED (evidencia distinta de atestación o término ATESTADO) y detección de atestaciones sin marca en `audit_gates.py` y el validador estructural H06. Versión 7.0.0 (MAJOR). |

## Decimosexta serie: modelo de autorización y capacidades (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `80-authorization-and-capability-model.md` | RFC-66 | Executed | Distinción formal de Capability/Permission/Authorization/Execution/Effect, frontera por defecto (red/HTTP, git remoto, instalaciones, cambios destructivos y escrituras fuera del proyecto requieren autorización), bloque `effects` en TASK_SPECIFICATION con `authorized_by`/`evidence_ref`/`status`, checks de autorización en H01/H04/H05, registro de efectos ejecutados en EXECUTION_SUMMARY, estados AUTHORIZED/UNAUTHORIZED/AUTHORIZATION_UNDETERMINED sin inferir UNAUTHORIZED por ausencia de registro. Versión 8.0.0 (MAJOR). |

## Decimoséptima serie: modelo de lifecycle de conocimiento (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `81-knowledge-lifecycle-model.md` | RFC-67 | Executed | Tipos de conocimiento (`snapshot`/`claim`/`lesson`), frescura por claim con proveniencia resoluble, invalidación post-ejecución (`invalidated_facts` en EXECUTION_SUMMARY) con revalidación scoped por pipeline, lessons del cierre con `session_id`/`protocol_version`/evidencia, y `kind`/`path` en KB_RECOMMENDATION. Versión 9.0.0 (MAJOR). |

## Decimoctava serie: workflow de evolución arquitectónica (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `82-architecture-evolution-workflow.md` | RFC-68 | Executed | Fase 1 de la RFC-68: capability de evolución arquitectónica en dos niveles, módulo `orchestrators/architecture/` (state machine + contratos PROJECT_REGISTRY/SESSION_REGISTRY/EVIDENCE_SNAPSHOT/EVIDENCE_SET/ARCHITECTURAL_CHANGE_SET/ARCHITECTURE_MANIFEST), checker de trazabilidad, Import Workspace `sessions/` gitignored y backfill de refs. Versión 9.1.0 (MINOR). |

## Serie de RFCs (documentos canónicos)

| RFC | Archivo | Status | Pregunta que responde |
|---|---|---|---|
| RFC-00XX | `rfc/00-skill-capability-model.md` | Accepted | ¿Qué es una Skill? (capacidad reutilizable, independiente del mecanismo) |
| RFC-00XY | `rfc/01-execution-context-model.md` | Accepted | ¿Qué es un Execution Context? |
| RFC-00XZ | `rfc/02-execution-context-assembly-process.md` | Accepted (enmiendas 00YB/00YC aplicadas 5 ago 2026, plan 04) | ¿Cómo se construye conceptualmente? |
| RFC-00YA | `rfc/03-context-budget-model.md` | Accepted ⚠ (alcance ampliado por 00YC — banner en el documento) | ¿Qué restricciones limitan su composición? |
| RFC-00YB | `rfc/04-context-candidate-prioritization-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué candidatos parecen más importantes? |
| RFC-00YC | `rfc/05-context-resolution-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué conjunto consistente puede componerse? |
| RFC-00YD | `rfc/06-context-composition-model.md` | Accepted (plan 04, 5 ago 2026) | ¿Cómo se construye el Execution Context a partir del conjunto resuelto? |
| RFC-00YE | `rfc/07-context-conflict-classification-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Qué tipos de conflicto existen conceptualmente entre candidatos? |
| RFC-00YF | `rfc/08-context-tie-breaking-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cómo se decide entre candidatos equivalentes en prioridad? |
| RFC-00YG | `rfc/09-context-merge-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cuándo dos candidatos compatibles se fusionan en uno? |
| RFC-00YH | `rfc/10-context-deduplication-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cómo se eliminan redundancias conceptuales del conjunto? |
| RFC-00YI | `rfc/11-context-compression-model.md` | Accepted (plan 06, 5 ago 2026) | ¿Cómo se reduce el costo de representación de un conjunto ya resuelto? |
| RFC-00YJ | `rfc/12-context-optimization-model.md` | Accepted (plan 06, 5 ago 2026) | ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget? |
| RFC-00YK | `rfc/13-execution-context-materialization-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime? |
| RFC-00YL | `rfc/14-prompt-rendering-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo materializa un runtime basado en prompts el Execution Context? |
| RFC-00YM | `rfc/15-skill-materialization-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo se materializa una Skill en un runtime concreto? |
| RFC-16 | `rfc/16-core-skills-catalog-model.md` | Accepted | ¿Qué Skills forman el núcleo del protocolo, qué función cumple cada una y qué criterios deciden la membresía? |
| RFC-17 | `rfc/17-orchestrator-decision-model.md` | Accepted (plan 09, 5 ago 2026) | ¿Qué decisiones toma el Orchestrator, sobre qué inputs y con qué autoridad? |
| RFC-18 | `rfc/18-failure-recovery-taxonomy.md` | Accepted (plan 10, 5 ago 2026) | ¿Qué clases de fallo existen conceptualmente y qué destino conceptual tiene cada una? |
| RFC-19 | `rfc/19-delegation-validity-model.md` | Accepted (plan 11, 5 ago 2026) | ¿Qué condiciones conceptuales debe cumplir una delegación (y su return report) para ser válida? |
| RFC-20 | `rfc/20-profile-selection-model.md` | Accepted (plan 12, 5 ago 2026) | ¿Qué hace a una tarea candidata a un perfil especializado y cómo se selecciona? |
| RFC-21 | `rfc/21-skill-activation-model.md` | Accepted (plan 12, 5 ago 2026) | ¿Qué hace a una skill candidata a activarse para una tarea? |
| RFC-22 | `rfc/22-session-iteration-lifecycle-model.md` | Accepted (plan 13, 5 ago 2026) | ¿Qué es una sesión, qué es una iteración, y qué reglas conceptuales gobiernan su ciclo de vida? |
| RFC-23 | `rfc/23-declarative-flag-compliance-model.md` | Accepted (plan 14, 5 ago 2026) | ¿Qué obliga conceptualmente un flag que el harness no puede forzar, y cómo se evidencia su cumplimiento? |
| RFC-24 | `rfc/24-skill-lifecycle-model.md` | Accepted (retroactiva 11 ago 2026; plan 23 Executed) | ¿Qué es una skill integrada y qué destino tienen las skills sin consumidor (cable-or-kill)? |
| RFC-25 | `rfc/25-single-source-required-sections.md` | Accepted (retroactiva 11 ago 2026; plan 24 Executed) | ¿De dónde debe resolver el runner las `required_sections` para que no existan copias desincronizables? |
| RFC-26 | `rfc/26-task-profile-model.md` | Accepted (retroactiva 11 ago 2026; plan 25 Executed) | ¿Cómo se clasifica una tarea por peso (trivial/standard/complex) y qué subconjunto del ciclo obliga cada perfil? |
| RFC-27 | `rfc/27-hook-enforcement-model.md` | Accepted (retroactiva 11 ago 2026; plan 26 Executed) | ¿Cómo pasa el enforcement de voluntario (prompt) a obligatorio (estado persistido + hooks bloqueantes)? |
| RFC-28 | `rfc/28-harness-coverage-closure-model.md` | Accepted (retroactiva 11 ago 2026; plan 27 Executed) | ¿Cómo se declara el nivel de enforcement de cada contrato y qué validación semántica mecánica mínima gana el harness? |
| RFC-29 | `rfc/29-h07-user-authorized-extra-work.md` | Accepted (plan 28 Executed, 11 ago 2026) | ¿Cómo expresa el protocolo el trabajo extra autorizado por el usuario sin que H07 lo convierta en fallo? |
| RFC-30 | `rfc/30-recovery-to-early-phases.md` | Accepted (plan 29 Executed, 11 ago 2026) | ¿Qué transiciones legales corrigen artefactos de fases tempranas desde RECOVERY? |
| RFC-31 | `rfc/31-abort-artifact-flow.md` | Accepted (plan 30 Executed, 11 ago 2026) | ¿Cómo se registra y cierra una sesión que termina en ABORT? |
| RFC-32 | `rfc/32-phase-02-profile-unification.md` | Accepted (12 ago 2026, revisión RFC-56; plan 31, 11 ago 2026) | ¿Quién redacta la TASK_SPECIFICATION y qué skills activa? |
| RFC-33 | `rfc/33-execution-summary-steps-schema.md` | Accepted (12 ago 2026, revisión RFC-56; plan 32, 11 ago 2026) | ¿Cuál es el nombre canónico de la lista de pasos de EXECUTION_SUMMARY? |
| RFC-34 | `rfc/34-ears-criteria-canonical-form.md` | Accepted (12 ago 2026, revisión RFC-56; plan 33, 11 ago 2026) | ¿Cuál es la forma canónica de los criterios de aceptación EARS? |
| RFC-35 | `rfc/35-verify-workflow-inputs.md` | Accepted (12 ago 2026, revisión RFC-56; plan 34 Executed, 11 ago 2026) | ¿Qué inputs consume la fase 07 y con qué valores decide? |
| RFC-36 | `rfc/36-plan-workflow-inputs.md` | Accepted (12 ago 2026, revisión RFC-56; plan 35 Executed, 11 ago 2026) | ¿Qué inputs recibe el worker de planificación? |
| RFC-37 | `rfc/37-gather-context-h10-declaration.md` | Accepted (12 ago 2026, revisión RFC-56; plan 36 Executed, 11 ago 2026) | ¿Qué transición protege H10 y cómo se declara en la fase 03? |
| RFC-38 | `rfc/38-task-analysis-confidence-blocks.md` | Accepted (12 ago 2026, revisión RFC-56; plan 37, 11 ago 2026) | ¿Qué significa cada bloque de confianza del TASK_ANALYSIS? |
| RFC-39 | `rfc/39-discovery-context-budget.md` | Accepted (12 ago 2026, revisión RFC-56; plan 38, 11 ago 2026) | ¿Dónde se configuran los límites de muestreo y presupuesto de discovery? |
| RFC-40 | `rfc/40-kb-discovery-entry-produced-by.md` | Accepted (12 ago 2026, revisión RFC-56; plan 39, 11 ago 2026) | ¿Qué estados producen las entradas de la KB de discovery? |
| RFC-41 | `rfc/41-discovery-artifact-boundaries.md` | Accepted (12 ago 2026, revisión RFC-56; plan 40, 11 ago 2026) | ¿Dónde viven los intermedios de discovery y cómo se numeran sus artefactos? |
| RFC-42 | `rfc/42-rfc-plan-status-governance.md` | Accepted (12 ago 2026, revisión RFC-56; plan 41, 11 ago 2026) | ¿Qué relación de status habilita a un plan a modificar `.agents/`? |
| RFC-43 | `rfc/43-h13-planned-cleanup.md` | Accepted (12 ago 2026, revisión RFC-56; plan 42, 11 ago 2026) | ¿Qué tratamiento reciben las entidades `planned` inexistentes en H13? |
| RFC-44 | `rfc/44-intent-reflection-auto-confirm.md` | Accepted (12 ago 2026, revisión RFC-56; plan 43, 11 ago 2026) | ¿En qué estado se produce la INTENT_REFLECTION con confianza HIGH? |
| RFC-45 | `rfc/45-unattended-clarification.md` | Accepted (12 ago 2026, revisión RFC-56; plan 44, 11 ago 2026) | ¿Cómo resuelve el protocolo la clarificación sin usuario en línea? |
| RFC-46 | `rfc/46-historical-trace-policy.md` | Accepted (12 ago 2026, revisión RFC-56; plan 45, 11 ago 2026) | ¿Cómo se interpretan trazas producidas por un harness que ya no existe? |
| RFC-47 | `rfc/47-enforced-mode-dogfooding.md` | Accepted (12 ago 2026, revisión RFC-56; plan 46, 11 ago 2026) | ¿Cómo se valida empíricamente el modo enforced? |
| RFC-48 | `rfc/48-discovery-per-entry-contracts.md` | Accepted (12 ago 2026, revisión RFC-56; plan 47, 11 ago 2026) | ¿Dónde se definen las secciones requeridas de cada entrada de discovery? |
| RFC-49 | `rfc/49-protocol-skill-mechanical-validation.md` | Accepted (12 ago 2026, revisión RFC-56; plan 48, 11 ago 2026) | ¿Cómo se garantiza estructuralmente la validez de las skills del protocolo? |
| RFC-50 | `rfc/50-delegation-single-instance-model.md` | Accepted (12 ago 2026, revisión RFC-56; plan 49, 11 ago 2026) | ¿Cómo se mantiene la separación de roles en una sola instancia? |
| RFC-51 | `rfc/51-discovery-kb-freshness.md` | Accepted (12 ago 2026, revisión RFC-56; plan 50, 11 ago 2026) | ¿Cómo se evita consumir entradas de KB vencidas o revalidadas fuera del pipeline? |
| RFC-52 | `rfc/52-worker-role-phase-catalog.md` | Accepted (12 ago 2026, revisión RFC-56; plan 51, 11 ago 2026) | ¿Coincide el catálogo de roles de fase y sus skills con la tabla de activación? |
| RFC-53 | `rfc/53-tooling-profile-candidacy.md` | Accepted (12 ago 2026, revisión RFC-56; plan 52, 11 ago 2026) | ¿Cómo clasifican las 7 preguntas las tareas de tooling/CLI? |
| RFC-54 | `rfc/54-discovery-contract-wording.md` | Accepted (12 ago 2026, revisión RFC-56; plan 53, 11 ago 2026) | ¿Cómo se redactan sin ambigüedad el project_shape y el cálculo de hashes? |
| RFC-55 | `rfc/55-protocol-source-containment.md` | Accepted (12 ago 2026) | ¿Cómo se desarrolla ARgentOS sin que el protocolo gobierne el repo fuente? |
| RFC-56 | `rfc/56-governance-fast-track.md` | Accepted (12 ago 2026) | ¿Qué cambios del payload requieren RFC y cuáles pasan por vía plan con verificación mecánica? |
| RFC-57 | `rfc/57-harness-structural-validator.md` | Accepted (15 ago 2026) | ¿Cómo se da soporte mecánico opcional a los ítems `[gate]` sin cambiar el modelo de juicio? |
| RFC-58 | `rfc/58-mandatory-structural-validator.md` | Accepted (15 ago 2026) | ¿Cómo se vuelve obligatorio el validador estructural a nivel de gate sin tocar el fail-open de los hooks? |
| RFC-59 | `rfc/59-recovery-context-session-continuity.md` | Accepted (16 ago 2026) | ¿Cómo se derivan, registran y ordenan las decisiones de recovery (variables de contexto, destinos múltiples) y cómo se reanuda una sesión desde su último artefacto intacto? |
| RFC-60 | `rfc/60-budget-accounting-metrics-trust.md` | Accepted (17 ago 2026) | ¿Cómo se hace mecánicamente verificable la contabilidad del Context Budget (declared vs consumed) y cómo se clasifica la confianza de los datos de métricas auto-reportados? |
| RFC-61 | `rfc/61-kb-transparency-consent-lifecycle.md` | Accepted (2026-08-24) | ¿Cómo hace ARgentOS que el discovery — trabajo no pedido explícitamente — sea consentido y visible para el usuario? |
| RFC-62 | `rfc/62-guarantee-model-and-enforcement-boundaries.md` | Accepted (plan 76, 2026-08-25) | ¿Qué garantiza ARgentOS, qué no, y quién verifica cada garantía? |
| RFC-63 | `rfc/63-state-and-artifact-lifecycle-model.md` | Accepted (plan 77, 2026-08-25) | ¿Qué dimensiones de estado existen y cuál es el lifecycle de los artefactos? |
| RFC-64 | `rfc/64-execution-record-model.md` | Proposal (plan 78) | ¿Cómo se registra y reconstruye una ejecución sin Event Sourcing? |
| RFC-65 | `rfc/65-evidence-and-verification-model.md` | Accepted (plan 79, 2026-08-25) | ¿Qué cuenta como evidencia y cuándo un artefacto puede declararse VERIFIED? |
| RFC-66 | `rfc/66-authorization-and-capability-model.md` | Accepted (plan 80) | ¿Cuándo una capability está autorizada para producir un efecto? |
| RFC-67 | `rfc/67-knowledge-lifecycle-model.md` | Accepted (plan 81) | ¿Qué ciclo mínimo necesita el conocimiento para ser reutilizable y revalidable? |
| RFC-68 | `rfc/68-architecture-evolution-workflow.md` | Accepted (plan 82) | ¿Cómo convierte ARgentOS evidencia de ejecución real en evolución arquitectónica trazable, incremental y versionada? |

## Roadmap de implementación (planes activos)

```text
Nivel 1  Cierre del pipeline principal ──┐ (paralelizable)
Nivel 2  Especialización de Resolution ──┘ (solo depende de RFC-00YC)
   │
Nivel 3  Especialización de Composition  (requiere Nivel 1)
   │
Nivel 4  Materialización                 (requiere Nivel 1; conceptualmente Nivel 3)
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `04-main-pipeline-closure.md` | Executed | — | RFC-00YD Composition + updates a RFC-00XZ y `feature.md` + regularización de status. |
| `05-resolution-specialization.md` | Executed | RFC-00YC | RFC-00YE Conflict Classification → 00YF/00YG/00YH + updates a RFC-00YC y `feature.md`. |
| `06-composition-specialization.md` | Executed | Nivel 1 | RFC-00YI Compression, RFC-00YJ Optimization. |
| `07-materialization.md` | Executed | Nivel 1 (+3 conceptual) | RFC-00YK Materialization → 00YL Prompt Rendering, 00YM Skill Materialization. |

## Segunda serie: explicitud de decisiones (después de 04–07)

```text
08  Correcciones transversales ─── ejecutable YA, en paralelo (no toca el roadmap EC)
09  Orchestrator Decision Model ── depende de 08
10  Failure & Recovery Taxonomy ── depende de 09
11  Delegation Validity Model ──── depende de 04–07
12  Selection Models ───────────── depende de 11 y 04–07
13  Session & Iteration Lifecycle ─ independiente, paralelizable
14  Declarative-Flag Compliance ── independiente, paralelizable
```

| Plan | Status | Depende de | Cierra |
|---|---|---|---|
| `08-correcciones-transversales.md` | Executed | — | Contradicción de bootstrap + fixes stale en `.agents/` (gaps 6 y 9). |
| `09-orchestrator-decision-model.md` | Executed | 08 | Catálogo conceptual de decisiones del Orchestrator + unificación de confianza (gaps 1 y 8). |
| `10-failure-recovery-taxonomy.md` | Executed | 09 | Clasificación de fallos y audiencia máquina/agente de policies (gap 5). |
| `11-delegation-validity-model.md` | Executed | 04–07 | Validez conceptual de payloads y return reports; resuelve el huérfano `context_budget: 4000` (gap 2). |
| `12-selection-models.md` | Executed | 11, 04–07 | Modelos de candidatura/selección de perfil y skill (gap 3). |
| `13-session-iteration-lifecycle.md` | Executed | — | Ciclo de vida de sesión, iteraciones y `<order>` (gap 4). |
| `14-declarative-flag-compliance.md` | Executed | — | Obligación y evidencia de flags `[declarative]` (gap 7). |

## Tercera serie: de protocolo explícito a protocolo operativo (después de 04–14)

```text
15  Policy Layer I (H15 + Budget materializado) ── depende de 11, 07
16  Policy Layer II (Resolution/Composition) ──── depende de 05, 06, 15
17  Protocol Metrics Model ────────────────────── depende de 09, 10; paralelo a 15
18  Segunda Materialización (MCP/tools/memoria) ─ depende de 07
19  Dogfooding End-to-End ─────────────────────── depende de 04–14 (+15, 17)
20  Release & Adoption ────────────────────────── depende de 19
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `15-policy-layer-1-delegation-budget.md` | Executed | 11, 07 | Primera policy real del protocolo (H15) + materialización del Budget para el runtime prompt. |
| `16-policy-layer-2-resolution-composition.md` | Executed | 05, 06, 15 | Policies concretas de desempate, deduplicación, merge, compresión y optimización. |
| `17-protocol-metrics-model.md` | Executed | 09, 10 | Modelo de métricas del protocolo: registro, agregación y señales de salud. |
| `18-segunda-materializacion.md` | Executed | 07 | Prueba de fuego de la tesis runtime-independent: materialización no-prompt del Execution Context. Tesis verificada: modelo intacto; segunda materialización (tool calls) en `runtime/`. |
| `19-dogfooding-end-to-end.md` | Executed | 04–14 (+15, 17) | Proyecto real ejecutado por protocolo; backlog evidenciado de la siguiente generación. Anexos: `19-anexo-a-bitacora-fricciones.md`, `19-anexo-b-reporte-estado.md`. |
| `20-release-adoption.md` | Executed | 19 | Versionado, changelog, migración, onboarding y tag 1.0.0 del protocolo. |

## Cuarta serie: Core Skills Pack

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `21-core-skills-pack.md` | Executed | RFC-16 Accepted | Implementación por tandas del Core Skills Pack definido en RFC-16 (`rfc/16-core-skills-catalog-model.md`). |
| `22-skills-pack-2.md` | Executed | 21 | Segundo pack: 16 Skills complementarias seleccionadas con los criterios C1–C4 de RFC-16 entre las candidatas no excluidas. |

## Quinta serie: de protocolo declarativo a protocolo enforced (5 ago 2026)

Serie derivada del análisis crítico de adopción (5 ago 2026): enforcement voluntario, validación solo estructural, coste operativo uniforme, skills huérfanas y duplicación policy↔contrato. Cada plan implementa su RFC homóloga (24–28, todas Proposal).

```text
23  Skill Lifecycle (cable-or-kill) ──── independiente, paralelizable
24  Single-Source Required-Sections ──── independiente, paralelizable
25  Task Profile Model ───────────────── recomienda 24
26  Hook-Based Enforcement ───────────── recomienda 25
27  Harness Coverage Closure ─────────── depende de 24
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `23-skill-lifecycle.md` | Executed | — | Cable-or-kill de skills: ~30 skills huérfanas se cablean a fases/policies o se eliminan del catálogo activo (RFC-24). |
| `24-single-source-required-sections.md` | Executed | — | El runner resuelve `required_sections` del contrato por referencia (8 policies derivadas; 7 conservan override explícito); `sync_required_sections.py` eliminado (RFC-25). |
| `25-task-profile-model.md` | Executed (dogfooding verificado 12 ago 2026, plan 46) | recomienda 24 | Perfiles `trivial`/`standard`/`complex` con bifurcación de artefactos y gates; meta: tarea trivial ≤ 5 archivos, ≤ 3 gates (RFC-26). |
| `26-hook-enforcement.md` | Executed (dogfooding verificado 12 ago 2026, plan 46) | recomienda 25 | `state.json` escrito solo por el runner + hooks bloqueantes `PreToolUse`/`Stop` compartidos entre CLIs, con defensa en capas (RFC-27). |
| `27-harness-coverage-closure.md` | Executed | 24 | Declaración `enforcement` en los 25 contratos + checks semánticos mecánicos (citas existentes, evidencia de tests) en el runner (RFC-28). |

Nota de status: los planes 23–27 usan `Proposed` como estado previo al ciclo vigente (el ciclo de planes definido en §Convenciones no contempla borradores; al aprobarse pasan a `Aprobado para ejecución` o `Aprobado para redacción` según entregable).

**Regularización de gobernanza (11 ago 2026, RFC-42/plan 41):** las RFC-24…28
pasan a `Accepted` retroactivamente, con evidencia en sus Amendment Logs (planes
23–27 `Executed` + `CHANGELOG.md` 2.0.0); el status `Proposal` era un desfase
documental, no una falta de aprobación. Regla vigente para el futuro: una
modificación de `.agents/` requiere **vía RFC Accepted** o **vía plan Aprobado
para ejecución** con justificación documentada; la referencia en
`ANTI_CIRCUMVENTION.md` queda pendiente de la aceptación de RFC-42 (plan 41
`Executed (parcial: ...)`).

## Sexta serie: remediación de la auditoría 2.0.1 (11 ago 2026)

Serie derivada de la auditoría de estado del protocolo 2.0.1 (2026-08-11). Cada
par RFC + plan corresponde a un subpunto de la auditoría; los defectos idénticos
detectados en más de una sección se cubren una sola vez (mapeo en la columna
"Origen"). Las RFCs están en `Proposal` y los planes en `Aprobado para
redacción`; según la regla de gobernanza (RFC-42), ningún cambio de `.agents/`
se ejecuta antes de que la RFC esté `Accepted` o el plan esté `Aprobado para
ejecución` con justificación. Excepción aplicada el 11 ago 2026: los planes
34–36 pasaron a `Aprobado para ejecución` por vía plan (RFC-42) tras la
auditoría de planes y quedaron `Executed`, con justificación documentada en
cada plan.

Estado al cierre del 11 ago 2026: RFC-29…31 `Accepted` y planes 28–30 `Executed`
por implementación autorizada explícitamente por el usuario; el resto de la serie
sigue en `Proposal` / `Aprobado para redacción` salvo los planes 34–36, que
pasan a `Aprobado para ejecución` el 11 ago 2026 tras la auditoría de planes;
los planes 34–36 quedaron `Executed` el 11 ago 2026 (RFC-35…37 permanecen en
`Proposal`, pendientes de regularización de gobernanza).

| Plan | RFC | Origen (auditoría 2.0.1) | Descripción |
|---|---|---|---|
| `28-h07-user-authorized-extra-work.md` | RFC-29 | 1.1 | H07: dos ramas de scope compliance (extra autorizado con evidencia). |
| `29-recovery-to-early-phases.md` | RFC-30 | 1.2 / 3.1 | Aristas de RECOVERY a fases tempranas + retry sin transición (F-02/F-03). |
| `30-abort-artifact-flow.md` | RFC-31 | 1.3 / 3.4 | ABORT en RECOVERY_REPORT, workflow 08 y hook de cierre. |
| `31-phase-02-profile-unification.md` | RFC-32 | 1.4 | Rol único `task_specification_writer` para la fase 02. |
| `32-execution-summary-steps-schema.md` | RFC-33 | 1.5 | Unificar la lista de pasos en `steps_executed`. |
| `33-ears-criteria-canonical-form.md` | RFC-34 | 2.1 | Bullets EARS como forma canónica (F-01). |
| `34-verify-workflow-inputs.md` | RFC-35 | 2.2 | Inputs y decisión del workflow 07. |
| `35-plan-workflow-inputs.md` | RFC-36 | 2.3 | Inputs del workflow 05. |
| `36-gather-context-h10-declaration.md` | RFC-37 | 2.4 | H10 como gate opcional de uso, no de transición. |
| `37-task-analysis-confidence-blocks.md` | RFC-38 | Executed (12 ago 2026, 3.1.0) | Semántica de los bloques de confianza del análisis. |
| `38-discovery-context-budget.md` | RFC-39 | Executed (12 ago 2026, 3.2.0) | Config de `context_budget` y muestreo (F-13). |
| `39-kb-discovery-entry-produced-by.md` | RFC-40 | Executed (12 ago 2026, 3.2.1) | Procedencia real de las entradas de KB. |
| `40-discovery-artifact-boundaries.md` | RFC-41 | Executed (12 ago 2026, 3.3.0) | Fronteras de intermedios + namespacing `<order>` (F-11/F-20). |
| `41-rfc-plan-status-governance.md` | RFC-42 | 2.9 | Gobernanza RFC Proposal vs planes Executed (23-28). **Regularización aplicada el 11 ago 2026** (RFC-24…28 → Accepted retroactivo); referencia en `ANTI_CIRCUMVENTION.md` cerrada por el plan 56 (12 ago 2026). |
| `42-h13-planned-cleanup.md` | RFC-43 | Executed (12 ago 2026, 3.3.1) | Limpieza de la regla de entidades `planned`. |
| `43-intent-reflection-auto-confirm.md` | RFC-44 | Executed (12 ago 2026, 3.3.2) | Estado productor de la reflexión HIGH (F-04). |
| `44-unattended-clarification.md` | RFC-45 | Executed (12 ago 2026, 3.4.0) | Modo desatendido de clarificación (F-05). |
| `45-historical-trace-policy.md` | RFC-46 | Executed (12 ago 2026, 3.4.1) | Versión de protocolo en trazas e interpretación histórica. |
| `46-enforced-mode-dogfooding.md` | RFC-47 | Executed (12 ago 2026, 3.7.0) | Dogfooding del modo enforced (state.json + hooks). |
| `47-discovery-per-entry-contracts.md` | RFC-48 | Executed (14 ago 2026, 3.8.0) | Contratos por entrada de discovery; single-source en D01. |
| `48-protocol-skill-mechanical-validation.md` | RFC-49 | Executed (12 ago 2026, 3.4.2) | Verificación mecánica dev-only de skills. |
| `49-delegation-single-instance-model.md` | RFC-50 | Executed (12 ago 2026, 3.5.0) | Modos de ejecución de delegaciones (F-09). |
| `50-discovery-kb-freshness.md` | RFC-51 | Executed (12 ago 2026, 3.6.0) | Frescura de KB, marcador único y revalidación por pipeline (F-12). |
| `51-worker-role-phase-catalog.md` | RFC-52 | Executed (12 ago 2026, 3.6.1) | Catálogo de fases y skills de los roles de worker. |
| `52-tooling-profile-candidacy.md` | RFC-53 | Executed (12 ago 2026, 3.6.2) | Candidatura tooling/CLI (F-06). |
| `53-discovery-contract-wording.md` | RFC-54 | Executed (12 ago 2026, 3.6.3) | Redacción de EXECUTIVE_SUMMARY y hash calculation (F-15/F-19). |

## Séptima serie: source containment del repo fuente (12 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `54-protocol-source-containment.md` | RFC-55 | Executed (12 ago 2026) | Payload del producto en `protocol/` (`protocol/.agents/` + `protocol/_AGENTS.md`), AGENTS.md raíz de desarrollo, tooling/CI con `--payload protocol`, y consolidación de `dev/` (README, ROADMAP, source-layout). `dist` no cambia. |
| `55-hook-setup-self-containment.md` | — (vía plan) | Executed (12 ago 2026) | Autocontención del setup de hooks en el payload; elimina la referencia a `ADOPTION.md` desde `harness/INDEX.md`. |
| `56-payload-immutability-anti-circumvention.md` | — (vía plan) | Executed (12 ago 2026) | Regla inline de inmutabilidad del payload en `ANTI_CIRCUMVENTION.md` (cierra el pendiente del plan 41). |
| `57-governance-classes-rollout.md` | RFC-56 | Executed (12 ago 2026) | Implementación de las clases A/B/C en las fuentes de verdad + revisión individual de RFC-32…54. |

## Octava serie: remediación de la auditoría de sistema (14 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `58-remediacion-nivel-2.md` | RFC-30, RFC-54 | Executed | Alineación del payload con modelos Accepted: actor único de hashes (completa plan 53), enum de `RECOVERY_REPORT` con fases tempranas (completa plan 29), metadata de contratos de discovery. Versión 3.9.0. |
| `59-remediacion-nivel-3.md` | RFC-26 (enmendada), RFC-30 | Executed | Camino trivial legalizado (`ANALYZING_TASK → PLANNING` condicionada al perfil, inputs reducidos) y taxonomía `RECOVERY`/`ANALYZING_TASK` alineada con la máquina de estados. Versión 3.10.0. |
| `60-remediacion-nivel-6.md` | — (Clase B) | Executed | Lote fácil: excepción single-source, convención `[Unreleased]`, contrato de evento de hook, modelo D01 aclarado, semántica de `retry_count`. Versión 3.11.0. |
| `61-remediacion-p1-2.md` | — (Clase B) | Executed | Dominios canónicos de `produced_by` (contratos) y `profile` (workflows), con enforcement en el checker de coherencia taxonómica. Versión 3.12.0. |
| `62-remediacion-p2-1-p4-3.md` | — (Clase B) | Executed | Context Budget declarado advisory (P2.1) y contratos versionados con `schema_version` (P4.3), con enforcement en el checker. Versión 3.13.0. |
| `63-remediacion-p4-2.md` | — (Clase B) | Executed | Mapeo determinista de sesión CLI ↔ protocolo (`.project/.sessions.json`) en `hook_gate.py` + `runner_state.py link`. Versión 3.14.0. |
| `64-remediacion-f1-a.md` | — (Clase B) | Executed | Modelo de enforcement declarado en tres capas (enforced/reviewed/verified); rewordings de policies, HARNESS_REPORT y H13. Versión 3.15.0. |
| `65-remediacion-f7-f5.md` | — (Clase B) | Executed | Evidencia de flags declarada (expected/evidenced/unevidenced) y modelo de determinismo de contexto declarado. Versión 3.16.0. |
| `66-harness-structural-validator.md` | RFC-57 | Executed | Validador estructural opcional del harness (`gate_validator.py`) como soporte mecánico de los ítems `[gate]`. Versión 3.17.0. |
| `67-remediacion-b-6.md` | — (Clase B) | Executed | Soporte estructural de H15 en el runner (`validate-delegation`/`validate-return`). Versión 3.18.0. |
| `68-mandatory-structural-validator.md` | RFC-58 | Executed | Validador estructural obligatorio a nivel de gate (MUST antes del PASS; FAIL estructural bloquea salvo desviación documentada). Versión 3.19.0. |

## Backlog evidenciado - plan 19

(5 ago 2026.)

Ítems derivados del dogfooding end-to-end (sesión `.project/d4ab6a93-8e75-4880-baf3-676fce992936/`). Priorización por frecuencia × costo observado, no por intuición; evidencia por ítem en `19-anexo-a-bitacora-fricciones.md` (IDs F-xx). No son planes redactados: son entradas priorizadas de las cuales se redactan planes al tomarlas.

| # | Ítem | Destino | Prioridad | Evidencia |
|---|---|---|---|---|
| B-1 | Gate D01 superable: especial-casing del runner para `KB_DISCOVERY_ENTRY.md` fuera de la iteración, o artefacto de sesión definido por el workflow de discovery | policy | Alta — se repite en cada discovery; hoy exige artefacto-puente | F-11 |
| B-2 | Recovery económico para fallos de formato: rama `RETRY_WORKER` en tablas de recovery (H01 primero) — implementada por el plan 29 (2026-08-11); alineación contrato↔validador EARS (bullets canónicos) cubierta por el plan 33 (2026-08-11) | policy | Alta — un fallo de formato cuesta una fase RECOVERY completa | F-01, F-02 |
| B-3 | Marcador `.last_discovery` único y canónico (ruta `.project/.last_discovery`, JSON de spec) + validación en health-check | policy | Media — dispara full discoveries evitables | F-12 |
| B-4 | Tanda de inconsistencias de contratos/policies: `discovery_context_budget` en features.toml, campos legacy en DISCOVERY_MANIFEST, "primera línea" de EXECUTIVE_SUMMARY, procedencia "observado por scan" en KB_DISCOVERY_ENTRY, delimitador de front matter, actor único de hash calculation, INTENT_REFLECTION auto-confirmada en la máquina de estados, mandato de KB en delegaciones condicionado a disponibilidad, namespacing de `<order>` por dominio | policy | Media — costo unitario bajo, recurrente | F-04, F-07, F-13, F-14, F-15, F-17, F-18, F-19, F-20 |
| B-5 | Política de clarificación desatendida/asíncrona (defaults declarados + confirmación diferida) para sesiones sin usuario en línea | gap → plan nuevo | Media — toda ejecución automatizada choca con esto | F-05 |
| B-6 | Subcomandos del runner para H15 (`validate-delegation`, `validate-return`) | gap → plan nuevo (acotado) | Media — hoy requiere importar el módulo a mano | F-08 |
| B-7 | Enmiendas conceptuales: RFC-18 (recovery→fases tempranas en la máquina de estados), RFC-20 (candidatura de tareas de tooling/CLI), clasificación `project_shape` para repos documentales/de protocolo | modelo → enmienda RFC | Baja — no bloquean; mejoran fidelidad | F-03, F-06, F-16 |
| B-8 | Modelo de ejecución de delegaciones en runtimes de contexto único + distinción "flag no aplica" vs "obligación ignorada" en métricas | gap → estudio/plan | Baja — dato registrado, sin costo observado | F-09, Anexo B §Métricas |

Descartados como ruido (con justificación en el anexo A): F-10 (deriva de reloj autor-reportado), F-21 (merge de KB legada funcionó según diseño).

Resolución: los ítems B-1…B-8 se redactan como pares RFC + plan en la **Sexta
serie** (tabla arriba); cada plan referencia su fricción F-xx. B-1 → plan 40
(y 47), B-2 → planes 29 y 33, B-3 → plan 50, B-4 → planes 37-43 y 53, B-5 →
plan 44, B-6 → planes 46 y 67 (tests del flujo enforced + subcomandos
validate-delegation/validate-return), B-7 → planes 29, 43 y 52, B-8 → plan 49.
El actor único de hashes de B-4 (F-17) se completa con el plan 58.

## Documentos de soporte

| Archivo | Estado | Rol |
|---|---|---|
| `skills-mechanism.md` | implementada | Diseño del mecanismo de skills (SKILL.md + references/); base de RFC-00XX e input de RFC-00YM. |
| `analisis-explicitud.md` | vigente | Catálogo de gaps de explicitud (1–9) con evidencia; referencia canónica de los planes 08–14. |
| `01-execution-context-model.md` | Executed | Cambios documentales de RFC-00XY en `.agents/` (trazabilidad). |
| `02-execution-context-assembly-process.md` | Executed | Cambios documentales de RFC-00XZ (trazabilidad). |
| `03-context-budget-model.md` | Executed | Cambios documentales de RFC-00YA (trazabilidad). |
| `docs/VERSIONING.md` | vigente | Política de versionado, changelog, tags y estados de planes. |

## Future Extensions sin nivel asignado

Anunciadas en RFCs aprobadas pero fuera del roadmap actual (decidir destino):

- Budget Estimation Model y Adaptive Prioritization Model (RFC-00YB).
- Budget Resource Model y Adaptive Budget Model (RFC-00YA).

## Convenciones

- **Verificación**: la batería canónica es la de `docs/VERSIONING.md` §4.1
  (`python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
  `python -m pytest tests/`, H13 por juicio). `python tools/check_dist_sync.py`
  es local-only y se espera verde solo en `master` (CI no la fetchea);
  `python protocol/.agents/harness/health_check.py` es la sonda del producto
  (adoptantes, modo enforced), no parte de la batería del repo. Los tests del
  harness (`protocol/.agents/harness/tests/`) no corren en la batería del repo:
  son tests del producto, se ejecutan en proyectos adoptantes.
- **Idioma**: inglés en el protocolo (`protocol/.agents/`), en su entry file (`protocol/_AGENTS.md`) y en el `AGENTS.md` raíz de desarrollo (es lo que leen los agentes), en el código y en los commits (Conventional Commits en inglés); español en la documentación de adopción (`docs/ADOPTION.md`, `docs/MIGRATION.md`, `CHANGELOG.md`), en `plans/` y en la documentación del tooling (`tools/`, `runtime/`, `docs/` — el código en inglés); `README.md` en inglés (público). Los documentos nuevos siguen esta regla; los existentes se alinean de forma incremental.
- **Inmutabilidad y clases de cambio (RFC-56)**: `protocol/.agents/` solo se modifica por la vía que corresponde a la clase del cambio. **Clase A** (modelo conceptual, contratos, breaking): requiere RFC `Accepted`; una RFC en `Proposal` NO habilita tocar el payload. **Clase B** (mejora documental compatible, sin cambio de significado): plan `Aprobado para ejecución` con justificación documentada + batería en verde. **Clase C** (corrección mecánica: typos, formato, links; cero cambio de significado): commit directo en `dev` con la batería en verde, registrado en el changelog de la próxima versión. Reglas de borde: ante la duda se elige la clase más estricta; la clase se declara en el plan (A/B) o en el commit (C) y es revisable; la batería de verificación corre en las tres clases.
- **Ciclo de status (RFCs)**: `Proposal` (borrador) → `Accepted` (aprobada) → `Superseded` (reemplazada; el header indica por cuál RFC). No existe `Approved`: los documentos que lo usaban se normalizaron a `Accepted` (2 ago 2026).
- **Ciclo de status (planes)**: `Aprobado para redacción` (entregables documentales: RFCs, estándares), `Aprobado para ejecución` (entregables de implementación o cambios en el repo), `Executed` (todos los criterios de salida verificados; si alguno quedó incumplido: `Executed (parcial: <qué falta>)`), `Superseded` (reemplazado; indicar por qué plan). Todo plan con dependencias abiertas declara su **criterio de entrada verificable** (qué archivos/estados deben existir antes de ejecutarlo).
- **Trazas históricas (RFC-46)**: los artefactos de sesión son registros inmutables de la versión del protocolo vigente al momento de la sesión; no se reescriben ni se "reproducen" con una versión nueva. Las entradas de gates previas a 2.0.0 fueron evaluadas por runner (checks machine); las posteriores, por juicio del agente contra checklists en prosa. Los contratos de sesión declaran `protocol_version` desde 3.4.1.
- **Citas verificables**: toda afirmación sobre el estado actual del repo ("hoy X") se ancla a `ruta:sección` (encabezado Markdown) existente al momento de la redacción. Prohibidos: rangos aproximados (p. ej. "H01–H13"), ordinales ("5ª responsabilidad"), números de línea absolutos sobre archivos mutables, y referencias a documentos inexistentes. Criterio de aceptación de todo documento nuevo en `plans/`: cada referencia resuelve contra el repo.
- **Plantillas**: todo plan nuevo nace de `plans/_TEMPLATE.md` y toda RFC nueva de `plans/rfc/_TEMPLATE.md` (estructura completa; las secciones marcadas como opcionales pueden omitirse). Los templates no se numeran ni se registran en este INDEX; el resto de los documentos referencia la estructura, no la duplica. El cumplimiento estructural (nombre de archivo, status dentro del ciclo vigente, ausencia de placeholders, Amendment Log en RFCs, registro en este INDEX) se verifica mecánicamente con `python tools/check_plan_structure.py`.
- **Amendment log**: toda RFC lleva una sección `## Amendment Log` (fecha → qué cambió → origen). Cuando una RFC posterior desfasa a una anterior, la anterior recibe además un banner bajo el header: `> ⚠ Enmienda pendiente: <qué cambió y dónde está el modelo vigente>`. Este log es el único registro de "qué decía antes" para documentos sin historia previa.
- **Verificación contra el repo**: este INDEX es un índice descriptivo, no una fuente de verdad. Todo plan nuevo verifica sus premisas contra `.agents/` y git como paso 0, nunca contra este INDEX.
- **Catálogo de gaps**: los "gaps de explicitud" referenciados por los planes 08–14 están definidos en `plans/analisis-explicitud.md`. Se cita el catálogo por ruta; ningún documento referencia IDs de gap que no existan allí.
- **Numeración de archivos**: hay dos secuencias independientes y cada una es única dentro de su espacio:
  - `plans/rfc/`: solo RFCs, numeración incremental (`00`–`15` existentes — los `07`–`15` reservados por el roadmap EC ya fueron asignados a RFC-00YE…00YM; los RFCs fuera del roadmap EC numeran a partir de `16`). Un implementation plan nunca vive aquí.
  - `plans/` (raíz): solo planes de ejecución, numerados por **orden cronológico de ejecución** — esa es la prioridad ante cualquier conflicto. `01`–`03` son los implementation plans de los RFCs base (ejecutados 25–26 jul); `04`–`07` primera serie (Execution Context); `08`–`14` segunda serie (explicitud de decisiones); `15`–`20` tercera serie (protocolo operativo), mapeada el 28 jul.
  - Los identificadores internos de la serie (RFC-00XX … RFC-00YM) se mantienen como IDs conceptuales dentro de los documentos; el número de archivo es solo orden físico.
- **Versionado**: `plans/` completo está versionado en git (política adoptada el 2 ago 2026; antes figuraba como ignorado pese a estar trackeado de facto, y hubo una pérdida y restauración). Los planes ejecutados se conservan como traza histórica: no se borran; si quedan desfasados se marcan `Superseded`. Lo efímero del proyecto son los artefactos de sesión (`.project/`), no los documentos de diseño. `plans/archive/` fue eliminado del working tree; su contenido sigue disponible en la historia de git.
- **Política de versionado, changelog, tags y estados**: definida en `docs/VERSIONING.md`. Resumen: trabajo e integración en `dev` con detalle por plan; releases estables solo en `master` vía tags; modelo por plan (cada plan ejecutado = una versión, atada a su RFC); invariante versión ↔ changelog ↔ tag; los estados de planes y RFCs cambian en el commit del plan y se reflejan en este INDEX.
- **Frontera documental**: `.agents/` (versionado, permanente) no referencia `plans/` ni RFCs. Los conceptos que `.agents/` necesita se definen inline, de forma autocontenida. Ningún plan debe instruir referencias `.agents/` → `plans/`; la instrucción correcta es siempre "definir el concepto inline, sin mencionar la RFC".
- **Layout fuente (RFC-55)**: el payload del producto vive en `protocol/` (`protocol/.agents/` + `protocol/_AGENTS.md`); el layout adoptado (`dist`) mantiene `.agents/` + `AGENTS.md` en la raíz. Los docs del payload describen el layout adoptado; los links a `AGENTS.md` rotos en fuente son intencionales y se documentan en `docs/source-layout.md`.

## Archivo

Nota (2 ago 2026): `plans/archive/` fue eliminado del working tree; estos archivos viven en la historia de git (`git show HEAD:plans/archive/<archivo>`).

| Archivo | Contenido |
|---|---|
| `archive/PLAN_*_v1.md` | Planes de construcción del protocolo (dominios, taxonomía, discovery) sobre estructura plana; reemplazados e implementados. |
| `archive/PLAN_05_CONTEXT_ENGINEERING.md` | Refactor de `.agents/standards/context/CONTEXT.md` (tags, presupuestos). Ejecutado (18 jul). |
| `archive/PLAN_06_PERFILES_WORKER.md` | Perfiles en `.agents/roles/profiles/` + campo `profile` del contrato de delegación. Ejecutado (18 jul). |
| `archive/PLAN_07_ARTEFACTOS_CONTEXTO.md` | Estándar `.agents/standards/context/PROJECT_ARTIFACTS.md`. Ejecutado (18 jul). |
| `archive/PLAN_08_PLANTILLAS_PROYECTO.md` | Plantillas de adopción en `templates/`. Descartado (28 jul): fuentes de `example/` ya no existen, solapa con las plantillas de `.agents/standards/context/PROJECT_ARTIFACTS.md` §9 y su plantilla de IDE era específica de Claude. Idea rescatable: plantillas de dominio como anexo de `.agents/standards/context/PROJECT_ARTIFACTS.md`. |

## Documento de visión

`plans/ec-pipeline-vision.md` es el documento de visión del Execution Context Pipeline — ni un plan de ejecución ni un RFC. Vivió en la raíz como `feature.md` hasta el 12 ago 2026, cuando se movió a `plans/` con banner de cierre (visión completada: los 4 niveles ejecutados; el modelo vigente vive en las RFCs 00XX–00YM). Los planes `04`–`07` y las RFCs lo citan como `feature.md`; `check_plan_citations.py` resuelve ese path histórico con un mapeo legacy (`feature.md` → `plans/ec-pipeline-vision.md`). **No reescribir las citas históricas**: son traza.
