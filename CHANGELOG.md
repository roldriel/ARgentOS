# Changelog — Protocolo ARgentOS

Todos los cambios notables del protocolo `.agents/` se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el protocolo sigue [Semantic Versioning](https://semver.org/lang/es/) de forma
conceptual, según lo definido en `plans/20-release-adoption.md` §A:

- **MAJOR**: cambios del modelo conceptual o contratos incompatibles con versiones anteriores.
- **MINOR**: adiciones compatibles (nuevas policies, contratos nuevos que no rompen los existentes, skills nuevas).
- **PATCH**: fixes documentales (correcciones de redacción, enlaces, ejemplos).

## Estructura de cada entrada

Cada versión se agrupa en secciones según el tipo de cambio:

- **Added** — capacidades, contratos, policies o documentos nuevos.
- **Changed** — modificaciones compatibles a comportamiento o documentos existentes.
- **Deprecated** — capacidades que se mantienen pero serán eliminadas.
- **Removed** — capacidades o contratos eliminados (siempre MAJOR).
- **Fixed** — correcciones de errores documentales o de contratos.
- **Modelo conceptual** — RFCs aceptadas o enmendadas (viven en `plans/rfc/`; se listan aquí porque gobiernan el significado de `.agents/`).

Regla de trazabilidad: cada ítem del changelog referencia la policy, el plan o la
RFC que originó el cambio. Los planes viven en `plans/`, las RFCs en `plans/rfc/`
y las policies del harness en `.agents/harness/policies/` y
`.agents/orchestrators/*/harness/policies/`.

La política de migración entre versiones vive en [`MIGRATION.md`](MIGRATION.md).

---

## [3.0.1] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (planes 31-33, RFC-32…34):
unificación del perfil de la fase 02, canonicalización de la lista de pasos de
`EXECUTION_SUMMARY.md` y forma canónica de los criterios de aceptación EARS.
Cambios documentales y de redacción de contratos/policies; sin cambios en el
modelo conceptual.

### Fixed

- **Perfil unificado de la fase 02** (plan 31, RFC-32): la tabla de activación
  de skills (`.agents/skills/INDEX.md`) y la guía de orquestación
  (`ORCHESTRATION_GUIDE.md` §7) ahora nombran el rol de fase
  `task_specification_writer` para `02-build-task-specification.md`, eliminando
  la contradicción con el front matter del workflow 02 y el uso de
  `functional_writer` fuera de su dominio (documentación funcional de fase 06).
- **Schema único de pasos en `EXECUTION_SUMMARY.md`** (plan 32, RFC-33):
  `[[steps_executed]]` es el único nombre de la lista de pasos (template del
  cuerpo y sección machine-readable); `[[steps]]` desaparece del contrato y los
  artefactos históricos que lo usen son no conformes (nota de migración en el
  contrato).
- **Forma canónica de Acceptance Criteria (EARS)** (plan 33, RFC-34): los
  bullets Markdown son la forma canónica de `## Acceptance Criteria` en
  `TASK_SPECIFICATION.md`; el bloque TOML `acceptance_criteria` queda como
  representación machine-readable opcional y derivada; H01 declara que los
  criterios presentes solo en TOML constituyen una violación de forma.

### Modelo conceptual

RFC-32…34 permanecen en `Proposal` (regularización de gobernanza pendiente,
mismo tratamiento que RFC-24…28); los planes 31-33 quedaron `Executed` con
autorización explícita del usuario.

---

Nota: el tag git `3.0.1` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.0] — 2026-08-11

Release MAJOR de la remediación de la auditoría 2.0.1 (planes 28-30, RFC-29…31):
H07 con dos ramas de scope compliance, recovery a fases tempranas con retry
acotado, y soporte de cierre por `ABORT` en artefacto, estado y hook.

### Changed

- **H07 — dos ramas de scope compliance** (plan 28, RFC-29): `VERIFICATION_REPORT.md`
  define la Rama A (sin extra) y la Rama B (trabajo extra autorizado por escrito
  con evidencia citada); H07 pasa con la Rama B solo si la evidencia existe y la
  juzga el Orchestrator; `RUBRICS.md` y `orchestrator.md` alineados. Cambio MAJOR
  de semántica.
- **Recovery a fases tempranas** (plan 29, RFC-30): `AGENT_STATE_MACHINE.md`
  agrega las aristas `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION |
  GATHERING_CONTEXT | VALIDATING_CONTEXT` y define `RETRY_WORKER` como acción
  correctiva sin transición; H01 gana una rama de retry acotado para fallos de
  formato; workflow 08 y H03 alineados. Cambio MAJOR del modelo de estados.
- **ABORT en el flujo de artefacto y de cierre** (plan 30, RFC-31):
  `RECOVERY_REPORT.md` admite `ABORT` en `corrective_action.recommended_next_state`
  (abort fundado); `runner_state.py` registra estado terminal
  (`terminal --state ABORT|COMPLETED`); `hook_gate.py` permite el cierre por
  `Stop` con estado terminal; `DECISIONS.md` D5 y `harness/INDEX.md` alineados.
  Cambio MAJOR de contrato.

### Modelo conceptual

RFCs aceptadas que gobiernan esta versión: RFC-29 (H07, trabajo extra autorizado
por el usuario), RFC-30 (recovery a fases tempranas) y RFC-31 (ABORT en el flujo
de artefacto y de cierre). Índice completo con status: `plans/INDEX.md` §Serie de
RFCs.

---

Nota: el tag git `3.0.0` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [2.0.1] — 2026-08-11

Release de mantenimiento documental tras la migración 2.0.0: restaura los
invariantes del protocolo en el propio repo y agrega verificación mecánica
dev-only para que no vuelvan a romperse. Origen: auditoría de referencias y
revisión de documentación (10–11 ago 2026).

### Added

- **Verificación mecánica de invariantes (dev-only)**: checker
  `dev/tools/check_protocol_invariants.py` (resolución de referencias, frontera
  `.agents/` autocontenido, metadata H13) con 50 tests, y workflow CI
  `check-protocol` que lo ejecuta en push/PR. No forma parte de lo distribuido
  a adoptantes (`dist`).

### Fixed

- **Metadata de taxonomía restaurada en los roles de fase**: `executor`,
  `planner`, `reviewer`, `verifier`, `task_analyst`, `task_specification_writer`,
  `recovery_analyst`, `context_discoverer`, `context_gatherer` y
  `context_validator` ahora llevan el bloque `taxonomy`/`kind`/`domain` que exige
  la policy H13, con campos alineados a sus entidades en
  `PROTOCOL_TAXONOMY.md`.
- **Frontera documental `.agents/` restaurada**: eliminada la referencia a
  `plans/rfc/24-...` en `.agents/skills/INDEX.md`; `.agents/` vuelve a ser
  autocontenido (solo `.agents/` + `AGENTS.md`).
- **Mención histórica corregida**: la nota sobre `technical_practices.py` en
  `.agents/standards/INDEX.md` ya no se escribe como una ruta inexistente.
- **`.project/README.md` creado** desde la plantilla del contrato, cumpliendo el
  rol del system agent en el bootstrap.

---

Nota: el tag git `2.0.1` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

## [2.0.0] — 2026-08-10

Segunda versión etiquetada del protocolo. Cierre de la migración "menos Python,
más texto": el runner de validación desaparece por completo y los gates del
harness se evalúan por juicio del orquestador contra checklists en prosa. El
Python sobreviviente son tres scripts stdlib (`hook_gate.py`, `runner_state.py`,
`health_check.py`); el modo declarativo no requiere Python. Origen:
`plans/26-hook-enforcement.md`, `plans/27-harness-coverage-closure.md` y los
commits `0fa9ce4` / `adb5b68`.

### Changed

- **Refactor "menos Python, más texto" del protocolo**: la lógica con forma de
  juicio sale del código Python y pasa a texto de protocolo; el Python restante
  solo verifica afirmaciones contra el filesystem. Criterio acordado: *Python
  verifies claims against the filesystem; the LLM verifies documents against
  documents*.
- **Recovery por tablas de decisión en Markdown**: los árboles de decisión TOML
  (H00–H07, H11, H15, D00, D01) se convierten en secciones
  «Recovery Decision Table» dentro de cada policy del harness
  (`.agents/orchestrators/*/harness/policies/`). El orquestador evalúa la tabla
  por juicio (primera regla que coincide); H09/H10 mantienen el fallback
  `RECOVERY_GENERIC`.
- **Verificación de salud del protocolo como checklist en prosa**: nuevo
  estándar `.agents/standards/runtime/PROTOCOL_HEALTH.md` aplicado por el
  system agent ArgentOS en el bootstrap. Solo la sonda de escritura/lectura de
  `state.json` queda mecánica (`health_check.py`, reducido a `probe()`). La
  regla TTL de `.project/.last_health_check` pasa a ser una regla en prosa
  (timestamp + `ttl_hours` de `features.toml`, default 24, override
  `AGENTS_HEALTH_CHECK_TTL_HOURS`).
- **Feature flags declarativos**: la resolución de flags se documenta en
  `.agents/standards/INDEX.md` (§"Feature flags") y la aplica el orquestador al
  evaluar la checklist de H01 (env `AGENTS_FEATURE_*` > `features.toml` >
  default). Se elimina el flag `decision_trees` (las tablas de recovery son
  siempre la policy). Los agentes leen `.agents/features.toml` directamente.
- **Métricas del protocolo por procedimiento en prosa**: la agregación pasa a
  `PROTOCOL_METRICS.md` §"Aggregation" como procedimiento aplicado por el
  agente bajo demanda (las métricas son advisory, nada las gatea).
- **Gates del harness evaluados en prosa; fin del runner de validación**:
  cada policy del harness declara ahora una sección «Gate Checklist» en prosa
  que el orquestador evalúa por juicio (secciones requeridas, EARS, citas,
  evidencia de tests, rúbricas, scope compliance, delegación H15). El estado
  del protocolo sigue siendo mecánico: tras un PASS juzgado por el orquestador,
  `python .agents/harness/runner_state.py --session <uuid> --trigger <HXX>
  --iteration <N> pass` registra el gate en `state.json` (escritura
  transaccional, único escritor, detección de bypass post-H04 incluida).
  `HARNESS_REPORT.md` pasa a escribirlo el orquestador (resuelve la
  contradicción latente entre el contrato y `harness/INDEX.md`). Requisitos de
  entorno por modo, documentados en `ADOPTION.md`: modo declarativo sin
  requisitos; modo enforced con Python 3.x stdlib pura (solo `hook_gate.py` +
  `runner_state.py` + `health_check.py`), sin `pip`.
- **Catálogo de prácticas técnicas en prosa**: la tabla flag → (rúbrica,
  estándar) pasa de `technical_practices.py` a `.agents/standards/INDEX.md`;
  la resolución de flags (env `AGENTS_FEATURE_*` > `features.toml` > default)
  la aplica el orquestador al evaluar H01.

### Removed

- `.agents/harness/runner.py` y los módulos `runner_models.py`,
  `runner_markdown.py`, `runner_policies.py`, `runner_artifacts.py`,
  `runner_validators.py`, `runner_citations.py`, `runner_profiles.py`,
  `runner_report.py`, `runner_paths.py` (sus validadores pasan a las
  checklists en prosa de las policies; `runner_state.py` sobrevive, reescrito
  autocontenido con un CLI mínimo de registro de estado).
- `.agents/harness/technical_practices.py` (catálogo movido a
  `.agents/standards/INDEX.md`).
- `.agents/harness/delegation_validity.py` (chequeos V1–V5 convertidos en la
  «Gate Checklist» de la policy H15).
- `.agents/harness/RUNNER.md` (documento del runner eliminado).
- Suite de tests reducida al trío sobreviviente (`test_hook_gate.py`,
  `test_runner_state.py`, `test_health_probe.py`); los tests de los módulos
  eliminados y los invariantes documentales basados en ellos se eliminan — sus
  invariantes pasan a las checklists en prosa.

- `.agents/harness/decision_tree_evaluator.py` y los árboles TOML
  `.agents/orchestrators/*/harness/decision_trees/`; subcomandos `decide`,
  `features`, `health-check` y `metrics` de `runner.py`.
- `.agents/harness/feature_flags.py` (reemplazado por la documentación
  declarativa de `.agents/standards/INDEX.md`; los flags los resuelve el
  orquestador al evaluar H01).
- `.agents/harness/runner_metrics.py` (reemplazado por el procedimiento de
  agregación de `PROTOCOL_METRICS.md`).
- `.agents/harness/skill_validation.py` (su chequeo esencial queda plegado en
  `PROTOCOL_HEALTH.md`, ítem 7).
- `.agents/task.py` (utilidad de desarrollo sin referencias en el protocolo).
- Tests de los módulos eliminados (incluida la suite `test_recovery_tables.py`);
  los invariantes pasan a las checklists en prosa y a la suite reducida del
  trío sobreviviente.

### Fixed

- **Referencias residuales al runner eliminadas**: citas a
  `runner.py`/`runner_validators`/`delegation_validity.py` y suites de test
  inexistentes en H13, H15, S00, D00, D01, `PROTOCOL_TAXONOMY`,
  `PYTHON_DEPENDENCIES`, `standards/INDEX`, `skills/INDEX`,
  `terminology-enforcer` y `features.toml`, alineadas con la evaluación por
  juicio (auditoría de referencias, 10 ago 2026).

---

Nota: el tag git `2.0.0` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

## [1.0.0] — 2026-08-05

Primera versión etiquetada del protocolo. Punto de corte validado por dogfooding
end-to-end (`plans/19-dogfooding-end-to-end.md`, Executed): health-check verde,
suite de tests verde (335 passed, 2 skipped), changelog retroactivo completo.
Origen del release: `plans/20-release-adoption.md`.

Esta entrada consolida retroactivamente toda la construcción previa del protocolo,
hasta entonces sin versionar. Las fechas internas son las de la historia de git.

### Added

- **Construcción del protocolo por dominios** (22 jul 2026): reestructura de
  `.agents/` en dominios de orquestación (`core`, `discovery`, `system`), con el
  orquestador central, el system agent y la máquina de estados. Origen: planes de
  construcción archivados (`plans/archive/PLAN_*_v1.md`, hoy solo en historia de
  git) y el merge `PLAN_ORCHESTRATORS_DOMAIN`.
- **Taxonomía del protocolo** (22 jul 2026): diccionario maestro
  `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, bloques de metadatos
  taxonómicos en los archivos del protocolo y policy de validación
  `.agents/harness/policies/H13-protocol-taxonomy.md`.
- **Discovery orchestrator** (22 jul 2026): subsistema de discovery con
  Knowledge Base en `.project/knowledge/`, contratos
  `.agents/orchestrators/discovery/contracts/`, enriquecimiento de la KB
  (`project_shape`, executive summary, API surface, file map; 24 jul) y estándar
  de curación con ciclo de vida `curation_status` (24 jul).
- **Mecanismo de skills** (25 jul 2026): estándar de skills (`SKILL.md` +
  `references/`), campo `skills` del contrato de delegación, selección por el
  orquestador y consumo por el worker, validación estructural en health-check.
  Diseño: `plans/skills-mechanism.md`; conceptualización posterior en RFC-00XX
  (`plans/rfc/00-skill-capability-model.md`) y RFC-00YM
  (`plans/rfc/15-skill-materialization-model.md`).
- **Estándares de contexto y perfiles** (18 jul 2026): estándar de artefactos de
  contexto `.agents/standards/context/PROJECT_ARTIFACTS.md` y perfiles de worker
  en `.agents/roles/profiles/`. Origen: `plans/archive/PLAN_05_CONTEXT_ENGINEERING.md`,
  `PLAN_06_PERFILES_WORKER.md`, `PLAN_07_ARTEFACTOS_CONTEXTO.md` (historia de git).
- **Serie de RFCs del Execution Context** (25 jul – 5 ago 2026): modelo
  conceptual completo del pipeline de contexto — RFC-00XY (Execution Context
  Model), RFC-00XZ (Assembly Process), RFC-00YA (Budget), RFC-00YB
  (Prioritization), RFC-00YC (Resolution), RFC-00YD (Composition) y sus
  especializaciones RFC-00YE…00YM (conflicto, desempate, merge, deduplicación,
  compresión, optimización, materialización, prompt rendering, skill
  materialization). Documentos en `plans/rfc/00`–`15`; trazabilidad de
  implementación en `plans/01`–`07`.
- **Explicitud de decisiones** (segunda serie, `plans/08`–`14`): corrección de la
  contradicción de bootstrap (08), catálogo de decisiones del Orchestrator y
  confianza unificada (09, RFC-17), taxonomía de fallos y recovery (10, RFC-18),
  validez de delegaciones y return reports (11, RFC-19), modelos de selección de
  perfil y skill (12, RFC-20/21), ciclo de vida de sesión e iteración (13,
  RFC-22), cumplimiento de flags `[declarative]` (14, RFC-23). Catálogo de gaps:
  `plans/analisis-explicitud.md`.
- **Policy layer y métricas** (tercera serie, `plans/15`–`17`): primera policy
  real del protocolo H15 (validez de delegaciones) y Budget materializado para el
  runtime prompt (15); policies de desempate, deduplicación, merge, compresión y
  optimización (16); modelo de métricas del protocolo (17).
- **Segunda materialización** (plan 18): materialización no-prompt del Execution
  Context (tool calls) en `runtime/`; tesis runtime-independent verificada.
- **Core Skills Pack** (`plans/21`–`22`, RFC-16
  `plans/rfc/16-core-skills-catalog-model.md`): catálogo núcleo de skills del
  protocolo en `.agents/skills/` implementado en dos tandas.
- **Versionado y adopción** (este release): `.agents/VERSION`, este
  `CHANGELOG.md`, `MIGRATION.md`, `ADOPTION.md` y plantillas de dominio en
  `.agents/standards/context/PROJECT_ARTIFACTS.md` §9. Origen:
  `plans/20-release-adoption.md`.

### Changed

- **Corrección transversal del 2 ago 2026**: política anti-alucinación aplicada a
  todo `plans/` — citas verificables `ruta:sección`, normalización de status
  (`Approved` → `Accepted`), versionado completo de `plans/` en git, eliminación
  de `plans/archive/` del working tree y frontera documental `.agents/` ↛
  `plans/`. Origen: commit `4109deb` y `plans/INDEX.md` §Convenciones.
- **Carga de skills** (4 ago 2026): la activación de skills se describe como
  lectura del worker, no como inyección en el prompt (fix documental en
  `.agents/skills/`).

### Removed

- `plans/archive/` eliminado del working tree (2 ago 2026); su contenido sigue en
  la historia de git (`git log --diff-filter=D -- plans/archive/`).
- Extractor Python `project_discovery` deprecado, reemplazado por el discovery
  orchestrator (22 jul 2026).

### Modelo conceptual

RFCs aceptadas que gobiernan esta versión: RFC-00XX y RFC-00XY…RFC-00YM (serie
Execution Context), RFC-16…RFC-23 (skills núcleo, decisiones del orquestador,
fallos, delegaciones, selección, ciclo de vida, flags declarativos). Índice
completo con status: `plans/INDEX.md` §Serie de RFCs.

---

Nota: el tag git `1.0.0` que fija esta versión se crea como entregable del release
(`plans/20-release-adoption.md`, entregable 5).
