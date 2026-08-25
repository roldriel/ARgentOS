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

La política de migración entre versiones vive en [`docs/MIGRATION.md`](docs/MIGRATION.md).
La política de versionado, changelog, tags y estados de planes vive en
[`docs/VERSIONING.md`](docs/VERSIONING.md).

---

## [Unreleased]

### Modelo conceptual

- **Revisión de la serie Proposal completada** (plan 57, RFC-56): las 23 RFCs
  de la serie 32–54 quedaron `Accepted` y sus planes asociados (31–53) están
  `Executed`. Sin cambio de payload; solo estados y traza de gobernanza.

(sin ítems de payload por ahora — los cambios de repo que no tocan el payload no se
listan; ver `docs/VERSIONING.md` §5)

---

## [9.0.0] — 2026-08-25

### Added

- **Modelo de lifecycle de conocimiento** (plan 81, RFC-67):
  `.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` define los tipos
  `snapshot`/`claim`/`lesson`, la frescura por claim con proveniencia
  resoluble, los disparadores de invalidación (incluida la post-ejecución) y
  la revalidación scoped por el pipeline de discovery; `standards/INDEX.md` lo
  referencia.
- **`kind`/`path` en KB_RECOMMENDATION** (plan 81, RFC-67): cada entrada
  recomendada declara `kind` (`discovery`|`knowledge`|`lesson`) y `path`
  resoluble (schema `2.0.0`); `session_uuid` queda como proveniencia, no como
  ubicación.
- **`invalidated_facts` en EXECUTION_SUMMARY** (plan 81, RFC-67): sección
  `## Invalidated Facts` con `fact`/`entry`/`reason` (schema `4.0.0`),
  obligatoria cuando la ejecución cambió hechos descubiertos; el pipeline
  revalida las entradas afectadas con el scope que las posee.
- **Checks mecánicos de conocimiento** (plan 81, RFC-67): `gate_validator.py`
  valida la forma de `invalidated_facts` (H05) y de `kind`/`path` (H10);
  `check_session_artifacts.py` aplica los checks a sesiones `>= 9.0.0` y
  valida la provenance de lessons (`kind: lesson`).

### Changed

- **Frescura por claim con proveniencia resoluble** (plan 81, RFC-67, MAJOR):
  `KB_DISCOVERY_ENTRY.md` declara `kind: snapshot` y semántica de claims por
  hecho; la Freshness Rule del discovery evalúa por claim y excluye de
  recomendaciones/consumo las claims vencidas o sin proveniencia;
  `DISCOVERY_STATE_MACHINE.md` agrega la condición de invocación
  post-ejecución y la medición previa para cambios de TTL; `docs/MIGRATION.md`
  §10 documenta la migración y las trazas históricas.
- **Lessons con proveniencia en el cierre** (plan 81, RFC-67, MAJOR): el
  Closing Feedback persiste lessons con `kind: lesson`, `session_id`,
  `protocol_version` y evidencia (RFC-65); `KNOWLEDGE_CURATION.md` y
  `context_discoverer.md` alineados.

### Removed

- **Reutilización de claims vencidas o con proveniencia no resoluble** (plan 81,
  RFC-67, MAJOR): deja de ser válida en entradas y recomendaciones nuevas; sin
  etiqueta de tipo no se mezclan snapshot/current/historical knowledge.

### Modelo conceptual

RFC-67 aceptada (plan 81, 2026-08-25): lifecycle mínimo de conocimiento (D9).

---

## [8.0.0] — 2026-08-25

### Added

- **Estándar de autorización** (plan 80, RFC-66):
  `.agents/standards/runtime/AUTHORIZATION.md` define el vocabulario
  Capability/Permission/Authorization/Execution/Effect, la frontera por
  defecto, quién autoriza y los estados AUTHORIZED/UNAUTHORIZED/
  AUTHORIZATION_UNDETERMINED; `standards/INDEX.md` lo referencia.
- **Bloque `effects` en el payload** (plan 80, RFC-66):
  `TASK_SPECIFICATION.md` gana la sección `## Effects`
  (`name`/`kind`/`authorized_by`/`evidence_ref`/`status`, schema `3.0.0`)
  obligatoria cuando hay efectos fuera de frontera; `EXECUTION_SUMMARY.md` gana
  `## Effects Executed` (`effect`/`executed`/`authorization_ref`, schema
  `3.0.0`); `SESSION_BRIEF.md` registra `[[effects]]` para autorizaciones de
  clarificación o default desatendido.
- **Checks mecánicos de autorización** (plan 80, RFC-66): `gate_validator.py`
  valida la forma del bloque `effects` (H01) y rechaza una sección `Effects`
  propia en EXECUTION_PLAN (H04); `check_session_artifacts.py` clasifica los
  efectos ejecutados para sesiones `>= 8.0.0`.

### Changed

- **Policies H01/H04/H05 con autorización** (plan 80, RFC-66, MAJOR): H01/H04
  exigen autorización registrada para efectos fuera de frontera y rechazan
  suposiciones no confirmadas como autorización; H05 verifica el registro de
  efectos ejecutados; `NO_ASSUMPTIONS.md` y `PROTOCOL_BOUNDARIES.md` usan el
  vocabulario del estándar.
- **Frontera verificable** (plan 80, RFC-66, MAJOR): la frontera por defecto se
  mantiene pero cada efecto fuera de frontera se vincula a una entrada de
  autorización; `docs/MIGRATION.md` §9 documenta la migración y las trazas
  históricas.

### Removed

- **Efectos fuera de frontera con suposición no confirmada sin registro**
  (plan 80, RFC-66, MAJOR): dejan de ser válidos en specs nuevos; sin registro
  la traza es AUTHORIZATION_UNDETERMINED, nunca UNAUTHORIZED por ausencia.

### Modelo conceptual

RFC-66 aceptada (plan 80, 2026-08-25): modelo de autorización y capacidades
(D8, D11).

---

## [7.0.0] — 2026-08-25

### Added

- **Clases de evidencia y estándar EVIDENCE** (plan 79, RFC-65):
  `.agents/standards/quality/EVIDENCE.md` define las cinco clases
  (`observation`/`measurement`/`attestation`/`assertion`/`reference`), el
  esquema `[[evidence]]` (`class`/`claim_id`/`ref`) y los invariantes
  EV-001…EV-004 / REL-001…REL-003; `standards/INDEX.md` y `harness/INDEX.md`
  lo referencian.
- **Bloques `[[evidence]]` en el payload** (plan 79, RFC-65):
  `VERIFICATION_REPORT.md` gana la sección `## Evidence` y `claim_id` en
  criterios/resultados (`schema_version` 3.0.0); los ENTRY de
  `HARNESS_REPORT.md` pueden registrar el array `evidence` con clase por check.
- **Checks mecánicos de evidencia** (plan 79, RFC-65): `gate_validator.py`
  (H06) valida las entries y rechaza un criterio PASS sin evidencia con clase
  válida; `audit_gates.py` marca atestaciones sin etiquetar y checks `verified`
  sin evidencia no-atestación; `check_session_artifacts.py` aplica los checks a
  sesiones `>= 7.0.0`.

### Changed

- **Policies H05/H06/H07 con evidencia con clase por ítem** (plan 79, RFC-65,
  MAJOR): los checklists citan evidencia con clase por ítem; H06 agrega el ítem
  `[gate]` de `## Evidence`/VERIFIED; H07 exige `reference`/`assertion` para la
  autorización escrita de la Rama B.
- **Significado de PASS/"verificado"** (plan 79, RFC-65, MAJOR): un claim es
  `verified` solo con una entrada de evidencia de clase distinta de
  `attestation`; un ítem `[gate]` se satisface con observación/medición/
  referencia o desviación documentada; `docs/MIGRATION.md` §8 documenta la
  migración y las trazas históricas.

### Removed

- **"Verificado" sin entrada de evidencia** (plan 79, RFC-65, MAJOR): la
  declaración "verificado" sin entrada de evidencia con clase deja de ser
  válida en reportes nuevos; el término permitido es "atestado".

### Modelo conceptual

RFC-65 aceptada (plan 79, 2026-08-25): clases de evidencia y regla VERIFIED
(D4, D12).

---

## [5.0.0] — 2026-08-25

### Added

- **Dimensiones de estado y lifecycle de artefactos** (plan 77, RFC-63): el
  payload declara tres dimensiones con entidad propia (Task State, Gate State,
  Artifact Lifecycle) y cuatro derivadas (Execution, Verification, Approval,
  Plan) con sus fuentes de verdad en `harness/INDEX.md` (§State dimensions); el
  Artifact Lifecycle (`draft`/`validated`/`superseded`) es derivado del registro
  de gates y nunca se escribe a mano.
- **`Deferred Items` y review gate** (plan 77, RFC-63):
  `VERIFICATION_REPORT.md` gana la sección `## Deferred Items` (aprobaciones
  humanas diferidas con confirmación) y `SESSION_BRIEF.md` registra los
  diferidos; para `complex` con `rubrics` habilitado, el review sobre
  `REVIEW_REPORT.md` es un Gate State obligatorio (`review_passed` /
  `review_failed`) registrado en `HARNESS_REPORT.md` (trigger `REVIEW`).
- **Checks mecánicos de lifecycle** (plan 77, RFC-63): `gate_validator.py`
  rechaza secciones en conflicto (H00/H03), `complex` sin `REVIEW_REPORT.md` y
  `Deferred Items` inválidos; `check_session_artifacts.py` detecta campos
  manuales de estado y COMPLETED sin gates in-scope para sesiones `>= 5.0.0`.

### Changed

- **Semántica de COMPLETED relativa al alcance** (plan 77, RFC-63, MAJOR):
  COMPLETED exige gates en-scope PASS, sin criterios FAIL/PENDING y aprobaciones
  completadas o diferidas con confirmación; H05/H06/H07 citan la dimensión de
  cada check en sus Gate Checklists; `protocol/.agents/orchestrators/core/roles/orchestrator.md`
  §4.1 hace determinista el review gate.

### Removed

- **Campos manuales de estado** (plan 77, RFC-63, MAJOR): `status` (Metadata),
  sección `## State`, `validation.complete` y `approved` (Plan Decision)
  desaparecen de los siete contratos de artefactos; `schema_version` 2.0.0.

### Modelo conceptual

RFC-63 aceptada (plan 77, 2026-08-25): dimensiones de estado, lifecycle de
artefactos y semántica de COMPLETED (D1, D2, D3).

---

## [4.0.0] — 2026-08-25

### Added

- **Catálogo de garantías y matriz de enforcement** (plan 76, RFC-62): `harness/INDEX.md` declara el catálogo cerrado de 12 garantías clasificadas en cinco clases (declarativa, verificable, mecánicamente enforceada, juicio del agente, actores externos) y la matriz por capa (agente / harness / runtime / externo / humano) con las invariantes ENF-001…ENF-003; `docs/ADOPTION.md` §6.4 la expone para adoptantes.
- **Regla de claims y campos de clase** (plan 76, RFC-62): "zero hallucinations" deja de ser una garantía técnica; todo claim es evidencia-citado o está marcado como atestación/inferencia. Los checks de `HARNESS_REPORT.md` y los criterios/resultados de `VERIFICATION_REPORT.md` ganan `claim_class` (`verified` / `attested` / `inference`); `clock` (`utc` | `agent_clock`) en los ENTRY y en los eventos de `METRICS.md`; `Evidence` opcional en `SESSION_LOG.md`; checklist de `PROTOCOL_HEALTH.md` con presencia de registros raíz, identidad de sesión y reloj.
- **Checkers dev de las celdas External** (plan 76, RFC-62): `check_session_artifacts.py` valida presencia/versión/UUID de sesión, atestaciones sin marca y timestamps UTC para sesiones `>= 4.0.0`; `aggregate_metrics.py --audit` reconcilia `state.json` ↔ `HARNESS_REPORT.md` en ambas direcciones para los gates de estado.

### Changed

- **Significado declarado de "verificado"** (plan 76, RFC-62, MAJOR): un claim es `verified` solo con evidencia de clase distinta de atestación; sin evidencia el término es `attested`. Las policies H01/H06/H07 citan evidencia con clase en sus Gate Checklists; `docs/MIGRATION.md` §6 documenta la migración y las trazas históricas.

### Modelo conceptual

RFC-62 aceptada (plan 76, 2026-08-25): modelo híbrido de garantías y fronteras de enforcement (D0, D11).

---

## [3.26.0] — 2026-08-24

### Added

- **Consentimiento del discovery** (plan 75, RFC-61): flag declarativo `discovery_require_consent` (default `true`) que convierte la detección automática del discovery en una consulta No-Assumption al usuario (condición disparada, opciones `full`/`lite`/sin discovery + opción libre); ante silencio o respuesta vaga se pide clarificación (sin default), en sesión no interactiva no se ejecuta y el bypass queda registrado en `SESSION_LOG.md`; con `false` se restaura la invocación automática.
- **Scope `lite` de discovery** (plan 75, RFC-61): `init_worker` + `environment_worker` + `stack_worker` + `framework_worker` + `synthesis_worker`, respetando el grafo de dependencias; figura en la tabla de scopes, en la invocación y en el marcador `.last_discovery`.
- **Skill `/discovery`** (plan 75, RFC-61): skill user-invoked fuera de la activation table; `/discovery` y `/discovery full` ejecutan `full`, `/discovery lite` ejecuta `lite`; reporta entradas escritas/actualizadas, stale marcados y duración.
- **Evento de métricas `discovery_consent`** (plan 75, RFC-61): catálogo del contrato `METRICS.md` con `condition`, `options`, `decision`; métrica `discovery.consent_by_decision` de clase Recorded en `PROTOCOL_METRICS.md`.

### Changed

- **Cierre de tarea con "What we learned"** (plan 75, RFC-61): el feedback de cierre posterior a `VERIFYING → COMPLETED` (gated por H06/H07) incluye la sección condicional "Qué aprendimos" con el conocimiento persistido en `.project/knowledge/entries/`, informativa y sin acción requerida del usuario; `VERIFICATION_REPORT.md` no se modifica.

## [3.20.0] — 2026-08-16

### Fixed

- **Conteo de scripts del harness y literal de budget de discovery** (plan 69,
  bloque 0 de la auditoría de sistema 3.1): `harness/INDEX.md` pasa de "three
  pure-stdlib scripts" a cuatro (incluye `gate_validator.py`); el ejemplo de
  invocación al Discovery Orchestrator en `orchestrator.md` usa
  `context_budget: 32000`, alineado con `discovery_context_budget` de
  `features.toml`.
- **Modelo produced_by/consumed_by de contratos de discovery** (plan 69,
  Clase B): la taxonomía refleja los productores reales de
  `INTER_WORKER_MESSAGE.md` y `KB_DISCOVERY_ENTRY.md` (los workers por scope),
  coherente con el front matter TOML de los contratos.
- **Snapshot del índice y conteos de auditorías previas** (plan 69): header de
  `plans/INDEX.md` alineado con el estado real (3.19.0, `dev` en sync),
  `[Unreleased]` del changelog sin claims stale, y conteos de tests de
  `docs/AUDITORIA_DOCUMENTACION.md` / `AUDITORIA_SISTEMA.md` actualizados.

## [3.21.0] — 2026-08-16

### Added

- **Chequeo mecánico de salidas de state machines** (plan 70):
  `check_taxonomy_coherence.py` compara los "Required Output Artifacts" de
  cada state machine contra los `output_artifacts` del workflow mapeado
  (bidireccional, con normalización de prefijos de orden). Sobre el payload
  previo a esta versión detecta 21 mismatches de discovery; tras la
  alineación queda en verde.

### Changed

- **Contrato de verificación y H06 alineados** (plan 70): `[[test_results]]`
  de `VERIFICATION_REPORT.md` declara el campo opcional `evidence` (archivo
  existente o comando en `SESSION_LOG.md`); el ítem 7 del Gate Checklist de
  H06 verifica el campo cuando está declarado, con fallback a `SESSION_LOG.md`.
- **Listas de salidas de discovery completas y con paths reales** (plan 70):
  los front matters de los workflows 01–06 de discovery y sus entidades en la
  taxonomía usan los nombres de archivo de KB reales (`environment.md`,
  `development_patterns.md`, etc.) e incluyen todas las entradas de KB por
  estado; la entidad de estado `discovery:DISCOVERY_INIT` corrige su
  `artifacts_output` (incluye `discovery_input.json`, `invalidation_report.json`
  y `file_map.md`; elimina el `KB_DISCOVERY_ENTRY.md` erróneo).
- **Convención de naming de contratos por entrada** (plan 70):
  `KB_DISCOVERY_ENTRY.md` documenta que el nombre del contrato (p.ej.
  `ENVIRONMENT_DISCOVERY.md`) no es el path del artefacto (p.ej.
  `environment.md`).

## [3.22.0] — 2026-08-16

### Added

- **Cobertura bidireccional de gates en el checker** (plan 71):
  `check_taxonomy_coherence.py` verifica que el origen de cada gate coincide
  con el `state` declarado por su policy y que el header TOML `transition` y
  los `gates:` de cada policy nombran las mismas transiciones, con tests.

### Fixed

- **Validador estructural profile-aware para H04** (plan 71, F-A): para tareas
  de perfil `trivial`, `gate_validator.py` ya no exige `## Context Reference`
  (el contrato de `EXECUTION_PLAN.md` la omite en el ciclo reducido); el perfil
  se lee de `TASK_ANALYSIS.md` de la sesión, con tests de producto del camino
  trivial.
- **Gate trivial declarado en H00** (plan 71, F-B): el front matter de H00
  (header `transition` y `gates:`) y la tabla de triggers de `harness/INDEX.md`
  declaran `ANALYZING_TASK → PLANNING` (solo perfil trivial), alineados con la
  máquina de estados.

## [3.23.0] — 2026-08-16

### Added

- **Auditoría post-hoc de gates** (plan 72): nuevo tool dev-only
  `tools/audit_gates.py` que recomputa el subconjunto estructural de los PASS
  registrados en `HARNESS_REPORT.md` invocando el validador del producto y
  reporta los PASS que el validador rechaza sin desviación registrada.

### Changed

- **Evidencia determinista de tests en H06** (plan 72): `gate_validator.py`
  valida el bloque `[[test_results]]` de `VERIFICATION_REPORT.md` — resultados
  no `SKIPPED` deben declarar `evidence` que resuelva a un archivo existente o
  tener el comando `test` en `SESSION_LOG.md` (semántica del contrato 3.21.0 y
  de H06 ítem 7); sin bloque TOML el chequeo es SKIP.
- **Registro de desviaciones documentadas** (plan 72): `HARNESS_REPORT.md`
  define el campo opcional `deviation` (cause + evidence) en los ENTRY como
  única vía para que un FAIL estructural se registre como PASS, y
  `harness/INDEX.md` declara su regla (nunca silenciosa, no afecta el fail-open
  de los hooks, auditable post-hoc); `check_session_artifacts.py` valida la
  forma del objeto.

## [3.24.0] — 2026-08-16

### Modelo conceptual

- **Recovery context, ranking de destinos múltiples y continuidad de sesión**
  (plan 73, RFC-59): definidas la derivación de las variables de las recovery
  decision tables (mecánicas desde el validador/filesystem; de juicio con
  evidencia al momento del fallo) y su registro como objeto `recovery` en la
  entrada FAIL de `HARNESS_REPORT.md`; el ranking de destinos de recovery (fase
  más temprana con artefacto inválido, un destino por entrada,
  `pending_artifacts` en `RECOVERY_REPORT.md`); y el procedimiento de
  reanudación de iteraciones parciales ("artefacto intacto" + 5 pasos) en
  `PROTOCOL_BOUNDARIES.md`.

## [3.25.0] — 2026-08-17

### Modelo conceptual

- **Contabilidad del Context Budget y clases de confianza de métricas**
  (plan 74, RFC-60): el Budget materializado pasa de advisory a measured —
  `consumed` se computa con la regla de estimación sobre los excerpts de
  `knowledge_entries`, se registra en el evento `context_budget` y los overruns
  post-compresión son desviaciones registradas; `PROTOCOL_METRICS.md` declara
  las clases Derived / Recorded / Verified para el catálogo y el agregador gana
  el modo `--audit` (gates de `state.json` vs entradas de `HARNESS_REPORT.md`).

### Changed

- **Superficie de bypass del hook endurecida** (plan 74, ítem 20): `Write`/
  `Edit` cuyo `tool_input` es un dict sin target (`file_path`/`path`/
  `filename`) pasan de fail-open a deny (exit 2); `tool_input` ausente y los
  errores internos siguen fail-open; `Read`/`Glob`/`Grep`/`Bash` siguen sin
  gate, con la cobertura por el scan post-hoc documentada en
  `harness/INDEX.md` (§Bypass surface and coverage).

### Added

- **Tool de medición del budget** (plan 74): `tools/measure_context_budget.py`
  computa `consumed` desde un payload de delegación y falla en overrun.

## [3.19.0] — 2026-08-15

### Changed

- **Validador estructural obligatorio en los gates** (plan 68, RFC-58, F1-B):
  para los triggers soportados (H00–H07, H09–H11, D00) el Orchestrator MUST
  invocar `gate_validator.py` antes de juzgar PASS; un FAIL estructural
  bloquea el PASS salvo desviación documentada. El fail-open de los hooks y
  los ítems `[agent]` no cambian.

---

## [3.18.0] — 2026-08-15

### Added

- **Soporte estructural de H15 en el runner** (plan 67, B-6):
  `runner_state.py validate-delegation` y `validate-return` validan el payload
  de delegación y el return report contra el contrato (campos requeridos,
  tipos, enums de `profile`, `context_budget` finito positivo, prefijos de
  clase en `deviations`). El gate H15 sigue siendo juicio del Orchestrator;
  los subcomandos son soporte mecánico de schema.

---

## [3.17.0] — 2026-08-15

### Added

- **Validador estructural opcional del harness** (plan 66, RFC-57):
  `.agents/harness/gate_validator.py` implementa el subconjunto
  mecánicamente checkable de los ítems `[gate]` (existencia, secciones
  normativas, bloques TOML y enums, resolución de citas, EARS, rubricas
  estructurales) para H00–H07, H09–H11 y D00. Es soporte opcional de revisión:
  el juicio del Orchestrator sigue siendo el árbitro, nunca bloquea, y sus
  resultados se registran como evidencia en `HARNESS_REPORT.md`.

---

## [3.16.0] — 2026-08-14

### Changed

- **Evidencia de flags declarada (F7-A)** (plan 65): procedimiento canónico de
  evidencia en `standards/INDEX.md` (expected = `declarative_flags` de
  `session_start`; evidenced = eventos `flag_evidence`; unevidenced = expected
  − evidenced), con la agregación de métricas como mecanismo declarado y la
  honestidad de que los eventos son auto-reportados. La "unevidenced
  compliance" pasa a ser detectable.
- **Modelo de determinismo de contexto declarado (F5-A)** (plan 65):
  `CONTEXT.md` declara que la asamblea de contexto es juicio con criterios
  ordenados (determinismo procedimental, no machine-enforced), coherente con
  el budget advisory (P2.1); las "harness Future Extensions" quedan como
  posibilidades, no garantías.

---

## [3.15.0] — 2026-08-14

### Changed

- **Modelo de enforcement declarado honestamente** (plan 64, F1-A): el payload
  distingue tres capas — enforced (caparazón de hooks, fail-open), reviewed
  (gates por juicio del Orchestrator, trail auto-reportado) y verified
  (checkers de desarrollo, dev-only). `harness/INDEX.md` gana la sección
  "Enforcement model"; las policies dejan de decir que un ítem `[gate]` es
  machine-gateable ("structurally checkable"); `HARNESS_REPORT.md` pasa a ser
  el "review trail" auto-reportado; H13 nota los checkers dev-only.

---

## [3.14.0] — 2026-08-14

### Changed

- **Resolución determinista de sesión en el hook** (plan 63, P4.2):
  `hook_gate.py` resuelve la sesión del protocolo por mapeo persistido
  (`.project/.sessions.json`), directorio exacto, sesión única o —solo en el
  primer evento de una CLI session— la más reciente, registrando el mapeo.
  `runner_state.py link --cli-session <id>` permite la vinculación explícita
  (p. ej. al reanudar entre conversaciones CLI). El fail-open y la semántica
  de los gates no cambian.

---

## [3.13.0] — 2026-08-14

### Changed

- **Context Budget declarado advisory** (plan 62, P2.1): `context_budget` no se
  mide ni se trunca mecánicamente; el estado de enforcement queda declarado en
  el contrato de delegación, `BUDGET_MATERIALIZATION.md` y `CONTEXT.md`. La
  contabilidad declarado vs consumido sigue registrándose por el evento de
  métricas.
- **Contratos versionados con `schema_version`** (plan 62, P4.3): todo contrato
  declara `schema_version` (semver) en su front matter; el checker de
  coherencia taxonómica valida presencia y formato; `MIGRATION.md` documenta
  el uso para adoptantes. Adición compatible de metadata: los artefactos
  válidos previos siguen siendo válidos.

---

## [3.12.0] — 2026-08-14

### Changed

- **Dominio canónico de `produced_by` en contratos** (plan 61, P1.2):
  `produced_by` en el front matter TOML usa nombres canónicos de la taxonomía
  (actor, `role_id` o `worker_id`); los estados viven solo en el bloque YAML
  del taxonomy (`PROTOCOL_HEALTH.md` ítem 3). Contratos normalizados:
  `KNOWLEDGE_INDEX.md`/`PROJECT_README.md` (`system_agent`) y
  `KB_DISCOVERY_ENTRY.md` (roles de workers). Cierra la contradicción §18.9.
- **`profile` de workflows validado** (plan 61): nombre canónico de
  worker/rol o `null`; el checker de coherencia taxonómica valida
  `produced_by`, `profile` y el catálogo de perfiles ↔ taxonomía.

---

## [3.11.0] — 2026-08-14

### Changed

- **Convención de `[Unreleased]`** (plan 60): `[Unreleased]` vuelve a la cima
  del changelog (Keep a Changelog); las secciones con fecha sin tag en `dev`
  quedan definidas como releases en curso que se oficializan al promover
  (`docs/VERSIONING.md` §5).
- **Esquema de evento de hook documentado** (plan 60): `harness/INDEX.md`
  define el contrato JSON del evento de hook (enforced mode) y su semántica
  fail-open.
- **Semántica de `retry_count`** (plan 60): derivada de las entradas `FAIL`
  del `HARNESS_REPORT.md` por trigger e iteración; documentada en
  `harness/INDEX.md` y `orchestrator.md`.
- **Modelo D01 aclarado** (plan 60): hoy no hay runner ejecutable en el
  harness; la validación mecánica de D01 es una extensión futura posible, no
  parte del payload distribuido.

### Fixed

- **Contradicción de la política single-source (§18.6)** (plan 60):
  `PROTOCOL_BOUNDARIES.md` declara la excepción aprobada del restatement de
  inmutabilidad en `ANTI_CIRCUMVENTION.md`.

---

## [3.10.0] — 2026-08-14

### Changed

- **Camino trivial legalizado** (plan 59, RFC-26 enmendada):
  `ANALYZING_TASK → PLANNING` queda como transición permitida solo para el
  perfil `trivial`, con `TASK_ANALYSIS.md` como referencia de tarea y sin
  artefactos de contexto. Se alinean la máquina de estados (Task Profiles,
  No-Skip Rule), los workflows 00/05/06/07 y su INDEX, las policies
  H00/H04/H06 y los contratos `TASK_ANALYSIS`, `EXECUTION_PLAN` y
  `VERIFICATION_REPORT`. Adición compatible: los artefactos válidos previos
  siguen siendo válidos.
- **Taxonomía alineada con la máquina de estados** (plan 59, RFC-30):
  `core:RECOVERY.next` incluye las cuatro fases tempranas y
  `core:ANALYZING_TASK.next` incluye `PLANNING`; H13 documenta las
  transiciones condicionales por perfil.

### Fixed

- **Contradicciones §18.1 (taxonomía vs máquina de estados en RECOVERY) y
  §18.2 (ciclo trivial con transición e inputs indefinidos)** (plan 59):
  cerradas; el ciclo trivial es ejecutable sin transiciones ni inputs
  indefinidos.

---

## [3.9.0] — 2026-08-14

### Changed

- **RECOVERY_REPORT — destinos de fases tempranas** (plan 58, RFC-30):
  `corrective_action.recommended_next_state` admite `ANALYZING_TASK`,
  `BUILDING_TASK_SPECIFICATION`, `GATHERING_CONTEXT` y `VALIDATING_CONTEXT`,
  alineando el contrato con las aristas de recovery ya legales en la máquina
  de estados; `08-recovery.md` alinea la recomendación. Adición compatible:
  los reportes válidos previos siguen siendo válidos.

### Fixed

- **Actor único de hashes en discovery** (plan 58, RFC-54): `orchestrator.md`
  (sección 4.3) ya no instruye al core Orchestrator a computar hashes ni a
  transportarlos en el payload de invocación; los computa `init_worker`
  (`DISCOVERY_STATE_MACHINE.md`, sección Hash Calculation), completando la
  ejecución del plan 53.
- **Metadata de contratos de discovery** (plan 58): `INTER_WORKER_MESSAGE.md`
  declara `produced_by` con roles explícitos de los workers de discovery;
  `DISCOVERY_MANIFEST.md` aclara la relación contrato ↔ artefacto
  (`.discovery_manifest`).

---

## [3.8.0] — 2026-08-14

### Added

- **Contratos por entrada del discovery** (plan 47, RFC-48): 14 contratos
  nuevos en `.agents/orchestrators/discovery/contracts/` (FILE_MAP, STACK,
  DEPENDENCIES, CONTAINERS, DATABASE, DISTRIBUTION, ARCHITECTURE,
  CONFIGURATION, ENTRYPOINT, BUSINESS_RULES, PROJECT_FLOW, TECHNICAL_DEBT,
  KNOWN_ERRORS, GLOSSARY) con el formato base de `KB_DISCOVERY_ENTRY.md` más
  sus secciones específicas. Las 14 entidades quedaron registradas en
  `PROTOCOL_TAXONOMY.md`.

### Changed

- **D01 single-source** (plan 47, RFC-48): el ítem 12 de
  `D01-discovery-output.md` verifica las secciones contra los contratos por
  entrada y elimina el listado duplicado de secciones.

---

## [3.7.0] — 2026-08-12

### Added

- **Test de integración del modo enforced** (plan 46, RFC-47):
  `.agents/harness/tests/test_enforced_flow.py` verifica end-to-end el flujo
  `state.json` + hooks en layout adoptado (deny sin H04, allow con H04, deny
  de `Stop` sin cierre, allow con H06/terminal, alerta del scan de bypass).
  El modo enforced queda verificado empíricamente (dogfooding, F-09/B-6).

---

## [3.6.3] — 2026-08-12

### Fixed

- **Redacción de contratos de discovery** (plan 53, RFC-54): el
  `project_shape` se declara en sección explícita `## Project Shape`
  (elimina el requisito ambiguo de "primera línea", F-15) y el actor único
  del cálculo de hashes es `init_worker` (F-19).

---

## [3.6.2] — 2026-08-12

### Fixed

- **Candidatura de tareas tooling/CLI** (plan 52, RFC-53):
  `ORCHESTRATION_GUIDE.md` declara que tooling/CLI sin dominio cubierto
  produce candidatura vacía → worker genérico (resultado legítimo de Q7);
  enmienda menor registrada en RFC-20 (F-06).

---

## [3.6.1] — 2026-08-12

### Fixed

- **Catálogo de fases y skills de workers** (plan 51, RFC-52): `worker.md`
  agrega la fase 01 (`intent_reflector`, perfil de fase) al catálogo;
  `recovery_analyst.md` alinea sus skills con la tabla de activación
  (`hypothesis-generator`, `risk-detector`).

---

## [3.6.0] — 2026-08-12

### Added

- **Regla de frescura de la KB de discovery** (plan 50, RFC-51): las
  entradas se consumen solo frescas (verificación de TTL antes de delegar);
  las vencidas se marcan `[entries] stale` y se revalidan solo por pipeline;
  `.project/.last_discovery` es el marcador único (legado deprecado) y el
  health checklist lo valida (F-12).

---

## [3.5.0] — 2026-08-12

### Added

- **Modos de ejecución de delegaciones** (plan 49, RFC-50): modo subagente
  (recomendado) y modo single-instance (permitido con mitigaciones:
  verificación como pasada separada con evidencia escrita, prohibición de
  auto-aceptar recomendaciones sin evidencia, registro de riesgo en
  `METRICS.md`); el modo se declara en `SESSION_LOG.md` y `DECISIONS.md`
  aclara que la autoridad del orquestador es independiente del modo (F-09).

---

## [3.4.2] — 2026-08-12

### Fixed

- **Validación mecánica de skills del protocolo** (plan 48, RFC-49): el
  checker de invariantes del repo de desarrollo gana el invariante SKILLS
  (front matter, `name` == directorio, referencias citadas, inventario INDEX
  ↔ directorios); `skills/README.md` e `skills/INDEX.md` actualizan su
  Enforcement para declararlo (dev-only, no bloqueante).

---

## [3.4.1] — 2026-08-12

### Added

- **Versión de protocolo en trazas de sesión** (plan 45, RFC-46):
  `SESSION_LOG.md`, `METRICS.md` (`session_start`) y `HARNESS_REPORT.md`
  declaran `protocol_version`; las trazas son registros inmutables de la
  versión vigente (gates por runner antes de 2.0.0, por juicio desde 2.0.0).

---

## [3.4.0] — 2026-08-12

### Added

- **Modo desatendido de clarificación (opt-in)** (plan 44, RFC-45):
  `NO_ASSUMPTIONS.md` define el modo (política de defaults declarada,
  aplicación marcada, confirmación diferida — nunca asumir en silencio);
  `AGENT_STATE_MACHINE.md` lo integra en `NEEDS_CLARIFICATION`;
  `SESSION_BRIEF.md` gana `source: unattended_default` y `SESSION_LOG.md` el
  registro `PENDING_USER_CONFIRMATION` (F-05).

---

## [3.3.2] — 2026-08-12

### Fixed

- **Estado productor de INTENT_REFLECTION en confianza HIGH** (plan 43,
  RFC-44): `ANALYZING_TASK` declara la reflexión como salida opcional en la
  vía HIGH (auto-confirmada, H11 la gates antes de
  `BUILDING_TASK_SPECIFICATION`); `orchestrator.md` y el workflow 00
  describen ambas vías de producción (F-04).

---

## [3.3.1] — 2026-08-12

### Fixed

- **Regla muerta de entidades `planned` en H13** (plan 42, RFC-43): la regla
  9 de la policy pasa a nota histórica (el mecanismo `planned` ya no existe
  en la taxonomía; se documenta cómo restaurarla si se reintroduce).

---

## [3.3.0] — 2026-08-12

### Changed

- **Namespacing de artefactos de discovery y excepción de intermedios**
  (plan 40, RFC-41): `PROTOCOL_BOUNDARIES.md` declara la unicidad de
  `<order>` por dominio (discovery usa prefijo `D<order>-`) y la excepción de
  intermedios de discovery en `.project/<session-uuid>/discovery/`; la
  máquina de discovery numera su reporte con el prefijo. Resuelve las
  colisiones de `<order>` entre dominios (F-20) y el workaround del
  artefacto-puente (F-11). Guía en `MIGRATION.md` §3.2.

---

## [3.2.1] — 2026-08-12

### Fixed

- **Procedencia real de las entradas de discovery** (plan 39, RFC-40):
  `produced_by` de `KB_DISCOVERY_ENTRY.md` y de la taxonomía pasa a la lista
  de estados productores de la máquina de discovery (ENV, STACK, FRAMEWORK,
  PATTERNS, BUSINESS, MERGE); `DISCOVERY_INIT` deja de figurar como productor
  de las entradas generales.

---

## [3.2.0] — 2026-08-12

### Added

- **Configuración real de presupuesto y muestreo de discovery** (plan 38,
  RFC-39): `features.toml` define `discovery_context_budget` (estimated
  tokens) y `discovery_sample_size_per_language`; `init_worker` los
  materializa en `discovery_input.json` y los workers de discovery dejan de
  declarar defaults propios (fricción F-13).

---

## [3.1.0] — 2026-08-12

### Changed

- **Semántica de los bloques de confianza de TASK_ANALYSIS** (plan 37,
  RFC-38): el bloque `[confidence]` queda redefinido como confianza de la
  calidad del análisis (evidencia que sostiene sus afirmaciones), gobernado
  por `CONFIDENCE.md`; `intent_confidence` es el bloque canónico de la
  interpretación de intención, gobernado por `INTENT_CONFIDENCE.md`.
  Contrato y policy H00 alineados; los criterios de completitud nombran
  ambos bloques explícitamente.

---

## [3.0.7] — 2026-08-12

### Fixed

- **Inmutabilidad del payload declarada en anti-circumvention** (plan 56):
  `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` ahora cuenta como
  circunvention modificar `.agents/` por fuera del cauce de releases (la
  versión publicada es la única unidad de cambio válida) y define la
  consecuencia en Enforcement (payload inválido hasta coincidir con una
  versión publicada; revert o `RECOVERY`). Regla inline, autocontenida.

---

## [3.0.6] — 2026-08-12

### Fixed

- **Autocontención del setup de hooks en el payload** (plan 55): la
  configuración de hooks por CLI (Kimi Code, Claude Code, managed settings)
  se trasladó de `ADOPTION.md` —que no se distribuye— a
  `.agents/harness/INDEX.md` (sección "Hook setup (enforced mode)"), y se
  eliminó la referencia del payload a `ADOPTION.md`. El modo enforced es
  configurable desde el payload solo; `ADOPTION.md` apunta a la sección del
  payload.

---

## [3.0.5] — 2026-08-12

**Source containment: protocol payload in `protocol/`** (plan 54, RFC-55):
el payload del protocolo se mueve a `protocol/` (`protocol/.agents/` +
`protocol/_AGENTS.md`) y el repo fuente pasa a ser un workspace de desarrollo
con `AGENTS.md` propio (dev). `dist` no cambia: sigue publicando `.agents/` +
`AGENTS.md` en la raíz del adoptante; el workflow renombra `_AGENTS.md` a
`AGENTS.md` al publicar. Incluye: nuevo AGENTS.md raíz (dev), tooling dev con
`--payload protocol` y mapeo legacy de citas, consolidación de `dev/`
(`README.md`, `ROADMAP.md`, `source-layout.md`), y actualización de CI y
documentación raíz. El contenido distribuido es semánticamente idéntico; el
entry file se renombra solo en el árbol fuente.

### Modelo conceptual

- RFC-55 (`plans/rfc/55-protocol-source-containment.md`) — `Accepted`.

---

## [3.0.4] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 36, RFC-37):
declaración de H10 como gate opcional de uso en la fase 03. Cambio documental;
sin cambios en el modelo conceptual ni en el comportamiento opcional.

### Fixed

- **H10 como gate opcional de uso** (plan 36, RFC-37): el front matter de
  `03-gather-context.md` declara solo `H02-context-artifact` como gate de
  transición y el cuerpo documenta cuándo se evalúa H10 (recomendaciones de KB
  con `knowledge_base` habilitado); la policy H10 pasa a `gates: []` y su
  `Trigger` aclara que no protege transiciones; los entries `H10-kb-discovery-report`,
  `core:GATHERING_CONTEXT` y `workflow:03-gather-context` de
  `PROTOCOL_TAXONOMY.md` quedan alineados. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-37 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 36 quedó `Executed`.

---

Nota: el tag git `3.0.4` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.3] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 35, RFC-36):
inputs completos del workflow 05. Cambio documental; sin cambios en el modelo
conceptual.

### Fixed

- **Workflow 05 — inputs completos** (plan 35, RFC-36): el front matter de
  `05-plan.md` declara `CONTEXT_ARTIFACT.md` como input junto con
  `TASK_SPECIFICATION.md` y `CONTEXT_VALIDATION_REPORT.md`; el rol `planner`
  y los entries `workflow:05-plan`, `core:PLANNING` y el worker `planner` de
  `PROTOCOL_TAXONOMY.md` quedan alineados. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-36 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 35 quedó `Executed`.

---

Nota: el tag git `3.0.3` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.2] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 34, RFC-35):
inputs y decisión coherentes del workflow 07. Cambio documental; sin cambios
en el modelo conceptual.

### Fixed

- **Workflow 07 — inputs y decisión coherentes** (plan 34, RFC-35): el front
  matter de `07-verify.md` declara los tres inputs reales
  (`TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`, `EXECUTION_SUMMARY.md`); el
  cuerpo gana la subsección `## Execution Summary`; la decisión final del
  reporte pasa de `FAILED` a `RECOVERY`, alineada con el contrato
  `VERIFICATION_REPORT.md` y el gate H06; el entry `workflow:07-verify` de
  `PROTOCOL_TAXONOMY.md` queda alineado. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-35 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 34 quedó `Executed`.

---

Nota: el tag git `3.0.2` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

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
