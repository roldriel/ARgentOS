# Registro de RFCs — ARgentOS

> Registro/navegación de las RFCs del repo (RFC-69). Los INDEX registran; la
> normativa vive en `docs/CONVENTIONS.md:Convenciones` y la taxonomía en
> `docs/AGENTS.md:Rules`.

## Serie de RFCs (documentos canónicos)

| RFC | Archivo | Status | Pregunta que responde |
|---|---|---|---|
| RFC-00XX | `docs/rfc/00-skill-capability-model.md` | Accepted | ¿Qué es una Skill? (capacidad reutilizable, independiente del mecanismo) |
| RFC-00XY | `docs/rfc/01-execution-context-model.md` | Accepted | ¿Qué es un Execution Context? |
| RFC-00XZ | `docs/rfc/02-execution-context-assembly-process.md` | Accepted (enmiendas 00YB/00YC aplicadas 5 ago 2026, plan 04) | ¿Cómo se construye conceptualmente? |
| RFC-00YA | `docs/rfc/03-context-budget-model.md` | Accepted ⚠ (alcance ampliado por 00YC — banner en el documento) | ¿Qué restricciones limitan su composición? |
| RFC-00YB | `docs/rfc/04-context-candidate-prioritization-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué candidatos parecen más importantes? |
| RFC-00YC | `docs/rfc/05-context-resolution-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué conjunto consistente puede componerse? |
| RFC-00YD | `docs/rfc/06-context-composition-model.md` | Accepted (plan 04, 5 ago 2026) | ¿Cómo se construye el Execution Context a partir del conjunto resuelto? |
| RFC-00YE | `docs/rfc/07-context-conflict-classification-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Qué tipos de conflicto existen conceptualmente entre candidatos? |
| RFC-00YF | `docs/rfc/08-context-tie-breaking-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cómo se decide entre candidatos equivalentes en prioridad? |
| RFC-00YG | `docs/rfc/09-context-merge-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cuándo dos candidatos compatibles se fusionan en uno? |
| RFC-00YH | `docs/rfc/10-context-deduplication-model.md` | Accepted (plan 05, 5 ago 2026) | ¿Cómo se eliminan redundancias conceptuales del conjunto? |
| RFC-00YI | `docs/rfc/11-context-compression-model.md` | Accepted (plan 06, 5 ago 2026) | ¿Cómo se reduce el costo de representación de un conjunto ya resuelto? |
| RFC-00YJ | `docs/rfc/12-context-optimization-model.md` | Accepted (plan 06, 5 ago 2026) | ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget? |
| RFC-00YK | `docs/rfc/13-execution-context-materialization-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime? |
| RFC-00YL | `docs/rfc/14-prompt-rendering-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo materializa un runtime basado en prompts el Execution Context? |
| RFC-00YM | `docs/rfc/15-skill-materialization-model.md` | Accepted (plan 07, 5 ago 2026) | ¿Cómo se materializa una Skill en un runtime concreto? |
| RFC-16 | `docs/rfc/16-core-skills-catalog-model.md` | Accepted | ¿Qué Skills forman el núcleo del protocolo, qué función cumple cada una y qué criterios deciden la membresía? |
| RFC-17 | `docs/rfc/17-orchestrator-decision-model.md` | Accepted (plan 09, 5 ago 2026) | ¿Qué decisiones toma el Orchestrator, sobre qué inputs y con qué autoridad? |
| RFC-18 | `docs/rfc/18-failure-recovery-taxonomy.md` | Accepted (plan 10, 5 ago 2026) | ¿Qué clases de fallo existen conceptualmente y qué destino conceptual tiene cada una? |
| RFC-19 | `docs/rfc/19-delegation-validity-model.md` | Accepted (plan 11, 5 ago 2026) | ¿Qué condiciones conceptuales debe cumplir una delegación (y su return report) para ser válida? |
| RFC-20 | `docs/rfc/20-profile-selection-model.md` | Accepted (plan 12, 5 ago 2026) | ¿Qué hace a una tarea candidata a un perfil especializado y cómo se selecciona? |
| RFC-21 | `docs/rfc/21-skill-activation-model.md` | Accepted (plan 12, 5 ago 2026) | ¿Qué hace a una skill candidata a activarse para una tarea? |
| RFC-22 | `docs/rfc/22-session-iteration-lifecycle-model.md` | Accepted (plan 13, 5 ago 2026) | ¿Qué es una sesión, qué es una iteración, y qué reglas conceptuales gobiernan su ciclo de vida? |
| RFC-23 | `docs/rfc/23-declarative-flag-compliance-model.md` | Accepted (plan 14, 5 ago 2026) | ¿Qué obliga conceptualmente un flag que el harness no puede forzar, y cómo se evidencia su cumplimiento? |
| RFC-24 | `docs/rfc/24-skill-lifecycle-model.md` | Accepted (retroactiva 11 ago 2026; plan 23 Executed) | ¿Qué es una skill integrada y qué destino tienen las skills sin consumidor (cable-or-kill)? |
| RFC-25 | `docs/rfc/25-single-source-required-sections.md` | Accepted (retroactiva 11 ago 2026; plan 24 Executed) | ¿De dónde debe resolver el runner las `required_sections` para que no existan copias desincronizables? |
| RFC-26 | `docs/rfc/26-task-profile-model.md` | Accepted (retroactiva 11 ago 2026; plan 25 Executed) | ¿Cómo se clasifica una tarea por peso (trivial/standard/complex) y qué subconjunto del ciclo obliga cada perfil? |
| RFC-27 | `docs/rfc/27-hook-enforcement-model.md` | Accepted (retroactiva 11 ago 2026; plan 26 Executed) | ¿Cómo pasa el enforcement de voluntario (prompt) a obligatorio (estado persistido + hooks bloqueantes)? |
| RFC-28 | `docs/rfc/28-harness-coverage-closure-model.md` | Accepted (retroactiva 11 ago 2026; plan 27 Executed) | ¿Cómo se declara el nivel de enforcement de cada contrato y qué validación semántica mecánica mínima gana el harness? |
| RFC-29 | `docs/rfc/29-h07-user-authorized-extra-work.md` | Accepted (plan 28 Executed, 11 ago 2026) | ¿Cómo expresa el protocolo el trabajo extra autorizado por el usuario sin que H07 lo convierta en fallo? |
| RFC-30 | `docs/rfc/30-recovery-to-early-phases.md` | Accepted (plan 29 Executed, 11 ago 2026) | ¿Qué transiciones legales corrigen artefactos de fases tempranas desde RECOVERY? |
| RFC-31 | `docs/rfc/31-abort-artifact-flow.md` | Accepted (plan 30 Executed, 11 ago 2026) | ¿Cómo se registra y cierra una sesión que termina en ABORT? |
| RFC-32 | `docs/rfc/32-phase-02-profile-unification.md` | Accepted (12 ago 2026, revisión RFC-56; plan 31, 11 ago 2026) | ¿Quién redacta la TASK_SPECIFICATION y qué skills activa? |
| RFC-33 | `docs/rfc/33-execution-summary-steps-schema.md` | Accepted (12 ago 2026, revisión RFC-56; plan 32, 11 ago 2026) | ¿Cuál es el nombre canónico de la lista de pasos de EXECUTION_SUMMARY? |
| RFC-34 | `docs/rfc/34-ears-criteria-canonical-form.md` | Accepted (12 ago 2026, revisión RFC-56; plan 33, 11 ago 2026) | ¿Cuál es la forma canónica de los criterios de aceptación EARS? |
| RFC-35 | `docs/rfc/35-verify-workflow-inputs.md` | Accepted (12 ago 2026, revisión RFC-56; plan 34 Executed, 11 ago 2026) | ¿Qué inputs consume la fase 07 y con qué valores decide? |
| RFC-36 | `docs/rfc/36-plan-workflow-inputs.md` | Accepted (12 ago 2026, revisión RFC-56; plan 35 Executed, 11 ago 2026) | ¿Qué inputs recibe el worker de planificación? |
| RFC-37 | `docs/rfc/37-gather-context-h10-declaration.md` | Accepted (12 ago 2026, revisión RFC-56; plan 36 Executed, 11 ago 2026) | ¿Qué transición protege H10 y cómo se declara en la fase 03? |
| RFC-38 | `docs/rfc/38-task-analysis-confidence-blocks.md` | Accepted (12 ago 2026, revisión RFC-56; plan 37, 11 ago 2026) | ¿Qué significa cada bloque de confianza del TASK_ANALYSIS? |
| RFC-39 | `docs/rfc/39-discovery-context-budget.md` | Accepted (12 ago 2026, revisión RFC-56; plan 38, 11 ago 2026) | ¿Dónde se configuran los límites de muestreo y presupuesto de discovery? |
| RFC-40 | `docs/rfc/40-kb-discovery-entry-produced-by.md` | Accepted (12 ago 2026, revisión RFC-56; plan 39, 11 ago 2026) | ¿Qué estados producen las entradas de la KB de discovery? |
| RFC-41 | `docs/rfc/41-discovery-artifact-boundaries.md` | Accepted (12 ago 2026, revisión RFC-56; plan 40, 11 ago 2026) | ¿Dónde viven los intermedios de discovery y cómo se numeran sus artefactos? |
| RFC-42 | `docs/rfc/42-rfc-plan-status-governance.md` | Accepted (12 ago 2026, revisión RFC-56; plan 41, 11 ago 2026) | ¿Qué relación de status habilita a un plan a modificar `.agents/`? |
| RFC-43 | `docs/rfc/43-h13-planned-cleanup.md` | Accepted (12 ago 2026, revisión RFC-56; plan 42, 11 ago 2026) | ¿Qué tratamiento reciben las entidades `planned` inexistentes en H13? |
| RFC-44 | `docs/rfc/44-intent-reflection-auto-confirm.md` | Accepted (12 ago 2026, revisión RFC-56; plan 43, 11 ago 2026) | ¿En qué estado se produce la INTENT_REFLECTION con confianza HIGH? |
| RFC-45 | `docs/rfc/45-unattended-clarification.md` | Accepted (12 ago 2026, revisión RFC-56; plan 44, 11 ago 2026) | ¿Cómo resuelve el protocolo la clarificación sin usuario en línea? |
| RFC-46 | `docs/rfc/46-historical-trace-policy.md` | Accepted (12 ago 2026, revisión RFC-56; plan 45, 11 ago 2026) | ¿Cómo se interpretan trazas producidas por un harness que ya no existe? |
| RFC-47 | `docs/rfc/47-enforced-mode-dogfooding.md` | Accepted (12 ago 2026, revisión RFC-56; plan 46, 11 ago 2026) | ¿Cómo se valida empíricamente el modo enforced? |
| RFC-48 | `docs/rfc/48-discovery-per-entry-contracts.md` | Accepted (12 ago 2026, revisión RFC-56; plan 47, 11 ago 2026) | ¿Dónde se definen las secciones requeridas de cada entrada de discovery? |
| RFC-49 | `docs/rfc/49-protocol-skill-mechanical-validation.md` | Accepted (12 ago 2026, revisión RFC-56; plan 48, 11 ago 2026) | ¿Cómo se garantiza estructuralmente la validez de las skills del protocolo? |
| RFC-50 | `docs/rfc/50-delegation-single-instance-model.md` | Accepted (12 ago 2026, revisión RFC-56; plan 49, 11 ago 2026) | ¿Cómo se mantiene la separación de roles en una sola instancia? |
| RFC-51 | `docs/rfc/51-discovery-kb-freshness.md` | Accepted (12 ago 2026, revisión RFC-56; plan 50, 11 ago 2026) | ¿Cómo se evita consumir entradas de KB vencidas o revalidadas fuera del pipeline? |
| RFC-52 | `docs/rfc/52-worker-role-phase-catalog.md` | Accepted (12 ago 2026, revisión RFC-56; plan 51, 11 ago 2026) | ¿Coincide el catálogo de roles de fase y sus skills con la tabla de activación? |
| RFC-53 | `docs/rfc/53-tooling-profile-candidacy.md` | Accepted (12 ago 2026, revisión RFC-56; plan 52, 11 ago 2026) | ¿Cómo clasifican las 7 preguntas las tareas de tooling/CLI? |
| RFC-54 | `docs/rfc/54-discovery-contract-wording.md` | Accepted (12 ago 2026, revisión RFC-56; plan 53, 11 ago 2026) | ¿Cómo se redactan sin ambigüedad el project_shape y el cálculo de hashes? |
| RFC-55 | `docs/rfc/55-protocol-source-containment.md` | Accepted (12 ago 2026) | ¿Cómo se desarrolla ARgentOS sin que el protocolo gobierne el repo fuente? |
| RFC-56 | `docs/rfc/56-governance-fast-track.md` | Accepted (12 ago 2026) | ¿Qué cambios del payload requieren RFC y cuáles pasan por vía plan con verificación mecánica? |
| RFC-57 | `docs/rfc/57-harness-structural-validator.md` | Accepted (15 ago 2026) | ¿Cómo se da soporte mecánico opcional a los ítems `[gate]` sin cambiar el modelo de juicio? |
| RFC-58 | `docs/rfc/58-mandatory-structural-validator.md` | Accepted (15 ago 2026) | ¿Cómo se vuelve obligatorio el validador estructural a nivel de gate sin tocar el fail-open de los hooks? |
| RFC-59 | `docs/rfc/59-recovery-context-session-continuity.md` | Accepted (16 ago 2026) | ¿Cómo se derivan, registran y ordenan las decisiones de recovery (variables de contexto, destinos múltiples) y cómo se reanuda una sesión desde su último artefacto intacto? |
| RFC-60 | `docs/rfc/60-budget-accounting-metrics-trust.md` | Accepted (17 ago 2026) | ¿Cómo se hace mecánicamente verificable la contabilidad del Context Budget (declared vs consumed) y cómo se clasifica la confianza de los datos de métricas auto-reportados? |
| RFC-61 | `docs/rfc/61-kb-transparency-consent-lifecycle.md` | Accepted (2026-08-24) | ¿Cómo hace ARgentOS que el discovery — trabajo no pedido explícitamente — sea consentido y visible para el usuario? |
| RFC-62 | `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md` | Accepted (plan 76, 2026-08-25) | ¿Qué garantiza ARgentOS, qué no, y quién verifica cada garantía? |
| RFC-63 | `docs/rfc/63-state-and-artifact-lifecycle-model.md` | Accepted (plan 77, 2026-08-25) | ¿Qué dimensiones de estado existen y cuál es el lifecycle de los artefactos? |
| RFC-64 | `docs/rfc/64-execution-record-model.md` | Proposal (plan 78) | ¿Cómo se registra y reconstruye una ejecución sin Event Sourcing? |
| RFC-65 | `docs/rfc/65-evidence-and-verification-model.md` | Accepted (plan 79, 2026-08-25) | ¿Qué cuenta como evidencia y cuándo un artefacto puede declararse VERIFIED? |
| RFC-66 | `docs/rfc/66-authorization-and-capability-model.md` | Accepted (plan 80) | ¿Cuándo una capability está autorizada para producir un efecto? |
| RFC-67 | `docs/rfc/67-knowledge-lifecycle-model.md` | Accepted (plan 81) | ¿Qué ciclo mínimo necesita el conocimiento para ser reutilizable y revalidable? |
| RFC-68 | `docs/rfc/68-architecture-evolution-workflow.md` | Accepted (plan 82) | ¿Cómo convierte ARgentOS evidencia de ejecución real en evolución arquitectónica trazable, incremental y versionada? |
| RFC-69 | `docs/rfc/69-documentation-taxonomy-and-layout.md` | Accepted (Plan A, 2026-08-27) | ¿Cómo se organiza la documentación del repo fuente bajo `docs/` para que la raíz quede limpia, la navegación escale con RFC + ADR + plan y los documentos de trabajo no acoplen la batería de verificación? |
| RFC-70 | `docs/rfc/70-project-context-in-discovery-kb.md` | Accepted (plan 84, 2026-08-28) | ¿Son necesarios `project-map.md` y `technical-analysis.md` como artefactos propios si su contenido ya vive en la KB de discovery? |

