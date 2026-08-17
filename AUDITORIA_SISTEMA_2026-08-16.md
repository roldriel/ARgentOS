# ARgentOS — Exhaustive System Audit 3.1 (2026-08-16)

> **Status:** auditoría nueva (remediación en curso). Los ítems y bloques de
> remediación se listan en la sección "Plan de remediación por bloques"; cada
> ítem se marca `Resolved` con evidencia (plan/RFC/commit) al cerrarse.
> **Fecha de auditoría:** 2026-08-16
> **Alcance:** repositorio en `master` @ `e912dac` (VERSION 3.19.0;
> `master`/`dev`/`dist` en sync).
> **Método:** auditoría read-only sobre el payload, tooling, runtime, tests,
> planes/RFCs, docs y CI. Batería canónica ejecutada en verde: invariantes
> (200 archivos, 8.384 referencias), citas, estructura de planes, coherencia
> taxonómica, artefactos de sesión, estado de versiones, sync de dist, 145
> tests de desarrollo y 64 tests del harness del producto.

---

# Executive Verdict

ARgentOS es hoy un **framework de especificación declarativa coherente y con
gobernanza inusualmente disciplinada, con un caparazón mecánico delgado y
honesto — pero sigue sin ser un sistema operativamente determinista y
mecánicamente enforceable.** La auditoría anterior (2026-08-14) sigue siendo
válida en lo esencial, con una mejora material: el modelo de enforcement está
ahora *declarado explícitamente* en tres capas (enforced / reviewed /
verified), el validador estructural es obligatorio a nivel de gate (plan 68,
RFC-58) y la coherencia taxonómica es mecánica. Esas remediaciones convirtieron
contradicciones **ocultas** en limitaciones **declaradas**, lo cual es progreso
real.

Sin embargo, la propia remediación introdujo una contradicción nueva de
implementación contra especificación:

- El `gate_validator.py` obligatorio (3.19.0) exige `## Context Reference` en
  `EXECUTION_PLAN.md` para H04, mientras el contrato (plan 59, 3.10.0) dice
  que los planes de perfil `trivial` **omiten** esa sección. Todo plan trivial
  conforme produce un FAIL estructural que debe ser salvado como "desviación
  documentada" — el validador "obligatorio" queda rutinariamente override, y
  el camino trivial (legalizado por el plan 59) es el punto de enforcement
  menos determinista. Además, la metadata de H00 no declara la transición
  trivial (`ANALYZING_TASK → PLANNING`) que la máquina de estados dice que
  H00 gatea.

**Respuesta a la pregunta primaria:** No — ARgentOS es principalmente un
framework de arquitectura/especificación con gaps semánticos y de enforcement
sin resolver. Es internamente disciplinado, declara sus límites con honestidad
(hooks fail-open, gates por juicio, budget advisory) y su batería de
verificación de desarrollo es sustantiva y verde. Pero las garantías centrales
del producto — composición de contexto determinista, budget mecánicamente
enforced, enforcement de harness más allá de dos eventos de hook, validación
de ground truth — están **declaradas, no entregadas**. Un sistema cuyo propio
diccionario dice "la determinismo se logra por contrato, no por código"
(`orchestrators/discovery/roles/discovery_orchestrator.md`) no es todavía un
sistema determinista; es un prompt bien especificado.

---

# 1. System Reconstruction

Qué es ARgentOS, según evidencia del repositorio:

- **Producto:** protocolo documental de orquestación de agentes basado en
  estados. Adoptar = vendorizar `dist` (`.agents/` + `AGENTS.md`) en un
  proyecto. El "runtime" es un LLM leyendo esos documentos; el único código
  ejecutable del payload son `harness/hook_gate.py`, `harness/runner_state.py`,
  `harness/health_check.py`, `harness/gate_validator.py` y los tests del
  producto bajo `harness/tests/`.
- **Repo fuente:** `protocol/` contiene el payload como **data** (gobernado por
  el `AGENTS.md` raíz, no por el protocolo). `tools/` contiene 7 checkers y un
  agregador de métricas; `runtime/` contiene dos materializaciones de
  referencia (prompt y tool-call); `tests/` contiene 145 tests de desarrollo;
  `plans/` + `plans/rfc/` contienen 68 planes ejecutados y 58 RFCs aceptadas;
  `docs/` contiene adopción, migración, versionado y layout fuente;
  `AUDITORIA_SISTEMA.md` es el tracker vivo de la auditoría 2.0.1 (cerrado).
- **Ciclo de vida:** `dev` (integración) → `master` (releases con tags) →
  `dist` (regenerado por CI `publish-dist`). Verificado: `dist` en sync con el
  payload de `master`; `VERSION` = 3.19.0; invariante versión↔changelog↔tag en
  verde.
- **Dominios:** `core` (máquina de 18 estados, orquestador, gates H),
  `discovery` (máquina de 11 estados, gates D), `system` (bootstrap de 4
  estados, S00), `cross-cutting` (estándares, contratos, roles, skills,
  delegación).

# 2. Architecture Map

```text
User request
  → ArgentOS System Agent (dominio system): checklist de salud + sonda → SYSTEM_READY
  → Orchestrator (core): máquina de 18 estados; delega cada fase a un Worker transitorio
      gates H00–H07, H09–H11, H15 (checklists en prosa + validador estructural
      obligatorio para el subconjunto [gate])
  → Discovery Orchestrator (discovery): máquina de 11 estados; workers; D00/D01;
      KB bajo .project/knowledge/discovery/
  → Artefactos: .project/<session>/<iteration>/<order>-*.md + HARNESS_REPORT.md
      + METRICS.md + state.json
  → Caparazón de enforcement: hook_gate.py (PreToolUse Write/Edit + Stop),
      runner_state.py (único escritor de state.json), health_check.py (sonda)
```

Dependencias: core → cross-cutting; core invoca discovery; discovery es
autocontenido; `protocol/.agents/` nunca referencia `plans/` (frontera
documental, enforced por checker); `runtime/` depende unidireccionalmente del
payload; `tests/` no depende de ninguno. No se encontraron dependencias
circulares.

# 3. Source-of-Truth Model

| Hecho | Autoridad declarada | Autoridad real | ¿Conflicto? |
|---|---|---|---|
| Transiciones de estado | `AGENT_STATE_MACHINE.md` | También listas `next` de la taxonomía y front matter de workflows | Alineada mecánicamente; **pero** H00 no declara la transición trivial que dice gatear |
| Diccionario maestro | `PROTOCOL_TAXONOMY.md` | H13 por juicio + `check_taxonomy_coherence.py` dev-only | El checker es unidireccional: verifica workflow⊆taxonomía, no salidas del state machine vs workflow/taxonomía (salidas de discovery difieren) |
| Salidas de discovery | `DISCOVERY_STATE_MACHINE.md` | Front matter de workflows + taxonomía + roles de workers + D01 | **Sí** — mismos artefactos con nombres distintos y listas parciales |
| Budget de discovery | `features.toml` `discovery_context_budget = 32000` | Ejemplo de payload en `orchestrator.md` §4.3 (`100000`) | **Sí** — dos docs canónicos discrepan |
| Versión | `protocol/.agents/VERSION` | tags + CHANGELOG + `docs/VERSIONING.md` §9 | Consistente (3.19.0) |
| Estado de planes/RFCs | headers individuales | `plans/INDEX.md` (espejo descriptivo) | **Header stale** — dice 3.6.3/2 commits; el estado real es 3.19.0 en sync |
| Estado de enforcement | `state.json` (único escritor: `runner_state.py`) | hooks + Orchestrator lo leen | Consistente |
| `dist` | CI desde `master` | byte-idéntico (verificado) | Consistente |

La detección mecánica de desacuerdos es real pero **unidireccional y parcial**:
referencias, metadata, estructura de planes, citas, skills, artefactos de
sesión, versión/tags y sync de dist están chequeados. El acuerdo semántico
entre la taxonomía y los *cuerpos* de las máquinas de estado **no** está
chequeado.

# 4. Ontology Audit

| Concepto | Definición (primera fuente autoritativa) | Notas |
|---|---|---|
| Orchestrator | Rol core que gobierna el ciclo de vida; único que cambia estado (`orchestrator.md`) | |
| Worker | Subagente transitorio que ejecuta exactamente una fase (`worker.md`) | No cambia estado, no invoca harness, no delega |
| Harness | Políticas de revisión aplicadas por juicio del Orchestrator antes de transiciones críticas (`harness/INDEX.md`) | Explícitamente sin runner de validación; **la palabra tiene 4 referentes**: conjunto de policies, runner anterior, "harness code" opcional (D01), scripts de estado |
| Policy | Checklist de gate + tabla de recovery por trigger | Mixto `[gate]` (estructural) / `[agent]` (juicio) |
| Contract | Estructura requerida de un artefacto de sesión (front matter + secciones + bloques TOML) | `schema_version` en todos; `enforcement`/`gated_by` declarados |
| Context / Candidate / Budget | Modelo de asamblea (`standards/context/*`) | Todos los criterios del pipeline `[agent]`; budget advisory |
| Skill | Capacidad acotada: `SKILL.md` + `references/` lazy (`skills/README.md`) | "Nunca otorga permisos"; tabla de activación + override por juicio |
| Profile | 3 conceptos: rol de fase en front matter, especialización en payload (`profiles/README.md`), task profile | Sobrecargado, desambiguado por notas |
| Task Profile | trivial/standard/complex (`AGENT_STATE_MACHINE.md` §Task Profiles) | Legalizado; conflicta con el validador (§20) |
| Runtime | 3 referentes: runtime conceptual, `runtime/` (implementaciones de referencia), CLI adoptante | |
| Sesión/Iteración | UUID + carpetas de iteración secuenciales, `<order>` por dominio (`PROTOCOL_BOUNDARIES.md`) | |

# 5. Naming and Semantic Coherence

- **Colisión "profile"** (reconocida): front matter de workflow (rol de fase),
  payload de delegación (especialización) y "task profile"
  (trivial/standard/complex) — tres conceptos distintos bajo un mismo token;
  desambiguada por notas pero con costo semántico real.
- **"harness"** — cuatro referentes (arriba).
- **"runtime"** — tres referentes (arriba).
- **Nombres de entradas de KB de discovery** — el mismo artefacto se llama
  `ENVIRONMENT_DISCOVERY.md` (taxonomía/front matter/contrato) y
  `environment.md` (state machine, cuerpo del workflow, rol de worker, D01,
  `USING_PATTERNS.md`); lo mismo para `DEVELOPMENT_PATTERNS.md` vs
  `development_patterns.md`. Es una **ambigüedad semántica, no cosmética**: un
  implementador estricto que resuelva el `output_artifacts` de la taxonomía
  literalmente escribiría archivos que ningún consumidor lee.
- **`INTER_WORKER_MESSAGE.md`** — el YAML de taxonomía declara
  `produced_by: [discovery:DISCOVERY_INIT]`, `consumed_by:
  [discovery:DISCOVERY_MERGE]`, pero es un canal usado por todos los workers
  en todas las etapas; el front matter TOML (los siete workers) es correcto.
  Igual para `KB_DISCOVERY_ENTRY.md` (la taxonomía dice INIT; los productores
  reales son los workers por scope).

# 6. Reference Integrity

- **Mecánico:** las 8.384 referencias de path resuelven; todas las citas
  `ruta:sección` resuelven (mapeo legacy para `feature.md`); la estructura de
  planes conforma; `dist` en sync. Verde.
- **Semántico (no mecánico):**
  1. **Metadata de salidas de discovery incompleta/inconsistente (Alto):**
     front matter + taxonomía listan `[worker_stack.json]` para stack (la
     state machine lista 6 salidas), `[worker_framework.json]` para framework
     (5), `[worker_business.json]` para business (6), `[DISCOVERY_MANIFEST.md]`
     para merge (la state machine agrega `executive_summary.md` + KB
     consolidada), mientras env/patterns sí listan sus entradas de KB (bajo
     nombres de contrato). El checker compara front matter ↔ taxonomía
     únicamente; la state machine (tercer origen) discrepa en silencio.
  2. **Header de `plans/INDEX.md` stale/autocontradictorio (Medio):** dice
     "Estado al 2026-08-14… `dev` está 2 commits adelante… `master`/`dist`
     están en 3.6.3", mientras el mismo párrafo y la tabla de la octava serie
     dicen que los planes 58–68 produjeron 3.9.0–3.19.0; git muestra
     master/dist en 3.19.0 y dev en sync.
  3. **`[Unreleased]` del CHANGELOG stale (Bajo-Medio):** dice que los planes
     37–40/42 están "hoy `Aprobado para redacción`" y los 43–47 "ejecución
     pendiente", contradiciendo `plans/INDEX.md` (todos `Executed`).
  4. **`docs/AUDITORIA_DOCUMENTACION.md` stale (Bajo):** "121 tests"
     (medido: 145 dev), "4 checkers + 114 tests", "la CI del repo sigue sin
     ejecutarlos" (la CI sí ejecuta los 64 tests del harness).
  5. **H06 vs contrato (Bajo-Medio):** el ítem 7 del Gate Checklist de H06
     requiere un campo `evidence` en `[[test_results]]`; el contrato de
     `VERIFICATION_REPORT.md` define solo `test`, `result`, `details`. El
     validador tampoco lo chequea.

# 7. Harness Audit

Por gate, desde policies y código:

| Gate | Realidad de enforcement |
|---|---|
| H04 / H06 | Parcialmente mecánico vía hooks (solo `PreToolUse` Write/Edit y `Stop`; fail-open por contrato) + validador estructural obligatorio (exit code + JSON) |
| H00–H03, H05, H07, H09–H11, H15, D00, D01, S00, H13 | Juicio del Orchestrator; el validador cubre el subconjunto `[gate]` (secciones, enums TOML, citas, EARS, rubricas) pero la decisión sigue siendo juicio; un FAIL estructural "bloquea el PASS salvo desviación documentada" |
| D01 (ground truth) | `[agent]` por declaración explícita — "Mechanical validation … a possible future extension" |

Hechos estructurales clave:

- **El "validador obligatorio" es bypasseable por diseño** ("desviación
  documentada"), y el camino trivial hace ese bypass rutinario (§20). No hay
  contador que impida al Orchestrator documentar una desviación en cada gate.
- **Superficie de bypass de los hooks:** solo `Write|Edit` están gated;
  `Bash`, `Read`, `Glob`, `Grep` no; un `Write`/`Edit` con target no
  identificable (`file_path`/`path`/`filename` ausente) es fail-open; los hooks
  son fail-open ante crash/timeout por contrato; el fallback de sesión
  "directorio más recientemente modificado" se usa solo en el primer evento y
  luego se fija vía `.project/.sessions.json`.
- **Orden de enforceability:** definido por transición; las tablas de recovery
  son first-match; las variables de contexto de las tablas (`artifact_exists`,
  `profile_valid`, `plan_out_of_scope`, …) **no tienen almacenamiento ni
  cómputo definido** — son juicio del Orchestrator al momento del fallo.
- **Gap de cobertura H00 (nuevo):** la transición trivial
  `ANALYZING_TASK → PLANNING` está declarada "gated by H00" en la máquina de
  estados, pero H00 `gates:` lista solo `BUILDING_TASK_SPECIFICATION`,
  `CONFIRMING_INTENT`, `NEEDS_CLARIFICATION`, y la tabla de triggers de
  `harness/INDEX.md` tampoco la incluye. El checker valida gates
  unidireccionalmente (target ∈ source.next) y no lo detecta.

**Veredicto:** el harness es una convención de revisión documentada con un
lint estructural obligatorio y un caparazón de hooks fail-open. No es un
sistema de validación enforceable. Esto es ahora una limitación **declarada**
(modelo de 3 capas), no oculta — pero sigue siendo el gap central.

# 8. Policy Audit

- **Solo declarativas (compliance del modelo):** H00–H03 (ítems `[agent]`),
  H05, H07, H09, H10, H11 (partes semánticas), H15 (juicio; existen
  subcomandos de schema), D00, D01, S00 (excepto la sonda), H13 (juicio en
  runtime; checker dev existe).
- **Parcialmente mecánicas:** H04/H06 (registro de estado + deny de hooks +
  validador estructural). El *juicio de que un gate PASS* sigue siendo del
  Orchestrator.
- **Precedencia:** sin precedencia global entre policies; conflictos resueltos
  por la política single-source, que tiene una excepción sancionada
  (`ANTI_CIRCUMVENTION.md` restate inline, declarada en
  `PROTOCOL_BOUNDARIES.md`).
- **Recovery:** todas las policies excepto H09/H10 tienen tablas de decisión;
  H09/H10 caen a `RECOVERY_GENERIC` (documentado). Semántica de `retry_count`
  definida (entradas FAIL previas por trigger e iteración en
  `HARNESS_REPORT.md`).
- **Determinismo de la evaluación:** el ítem 7 de H06 verifica evidencia
  *declarada* (resuelve o aparece en `SESSION_LOG.md`) — ambas mitades
  autoescritas; no verifica que un test realmente haya corrido.
- **Flags declarativos:** compliance = join de `session_start` auto-reportado
  y eventos `flag_evidence` auto-reportados; la "unevidenced compliance" es
  ahora *detectable* vía `aggregate_metrics.py`, pero los inputs son
  auto-reportados (nota de honestidad en `standards/INDEX.md`).

# 9. Contract Audit

- **Mecánicamente chequeable ahora:** forma de front matter
  (artifact/phase/produced_by/schema_version, validado por checker), headings
  ATX requeridos (validador), enums TOML (`final_state`, `steps_executed`,
  `decision`, `acceptance_criteria`, `scope_compliance`,
  `technical_approach`), resolución de citas, bullets EARS, estructura de
  rubricas. Mejora real desde la auditoría anterior.
- **Solo textual:** todos los requisitos semánticos (suficiencia, relevancia,
  evidencia que realmente soporta las afirmaciones, no inventar contexto).
- **Inconsistencias internas encontradas:**
  1. **Trivial vs validador H04** (§20, F-A) — el contrato dice omitir
     `## Context Reference`; el validador lo exige.
  2. **H06 ítem 7 vs contrato** — el campo `evidence` en `test_results` no
     existe en el contrato.
  3. **`WORKER_DELEGATION_CONTRACT.md`** — `recommended_next_state`
     deprecado pero aún en el schema JSON; `runner_state.py validate-return`
     no valida `recommendation` ni `project_changes` (solo campos requeridos,
     tipos de blockers/deviations y prefijos).
  4. **Contratos por entrada de discovery** — nombre del contrato
     (`ENVIRONMENT_DISCOVERY.md`) ≠ path del artefacto (`environment.md`);
     la nota de naming existe solo para el manifest, no para los contratos por
     entrada.
- **Completitud:** los contratos definen secciones y criterios de completitud
  pero no precondiciones/postcondiciones/invariantes chequeables;
  `schema_version` existe pero sin reglas de migración mecánicamente
  chequeables más allá de presencia/formato.

# 10. Runtime Audit

El runtime como máquina de estados ejecutable:

```text
Inicial: system:SYSTEM_INIT → VERIFYING_PROTOCOL_HEALTH (S00) → ENVIRONMENT_READY → core:SYSTEM_READY
Tarea: TASK_RECEIVED → ANALYZING_TASK → (CONFIRMING_INTENT | NEEDS_CLARIFICATION | BUILDING_TASK_SPECIFICATION | PLANNING*)
      → TASK_READY → GATHERING_CONTEXT → CONTEXT_GATHERED → VALIDATING_CONTEXT → CONTEXT_READY
      → PLANNING → PLAN_READY → EXECUTING → VERIFYING → COMPLETED | RECOVERY → (loop) → ABORT
   * solo perfil trivial
```

- **Partes computacionalmente deterministas:** `state.json`
  (read-modify-write transaccional, fail-closed para consumidores), decisiones
  de hooks (stdlib, orden de fallback documentado), scan de bypass
  (mtime-based, advisory), chequeos del validador (regex/TOML-subset
  deterministas).
- **Transiciones/decisiones subespecificadas:**
  - Elegir entre varios destinos de RECOVERY cuando varios artefactos de fases
    tempranas requieren corrección (la tabla elige por artefacto pero no
    ordena).
  - Poblar las variables de contexto de las tablas de recovery — sin
    almacenamiento ni derivación definidos más allá de `retry_count`.
  - Reanudación de sesión ("desde su último artefacto intacto") — sin
    procedimiento para determinar "intacto" ni reconstrucción desde el log.
  - Modo single-instance ("paso de juicio explícito y separado") — sin
    separación mecánica.
  - Concurrencia: sesiones paralelas aisladas por UUID, pero
    `latest_iteration` defaults y el fallback "más reciente" solo se fijan en
    el primer evento.
- **Terminación:** COMPLETED/ABORT terminales; el hook de Stop enforce el
  cierre solo en modo enforced.

# 11. Context Audit

- El pipeline `discover → collect → organize → prioritize → resolve → compose
  → deliver` es **"juicio con criterios ordenados"** (declarado canónico en
  `CONTEXT.md` §Determinism model). El procedimiento está ordenado; cada
  criterio es juicio del agente. Nada es machine-enforced; budget advisory
  (`BUDGET_MATERIALIZATION.md` §7).
- **Invariantes del budget:** finito/positivo declarado; concepto
  independiente de representación con unidades por runtime. Enforcement =
  declarativo + eventos de métricas (`context.budget_declared/consumed`),
  auto-reportados.
- **Contradicción del budget:** `orchestrator.md` §4.3 payload de ejemplo
  `"context_budget": 100000` vs `features.toml`
  `discovery_context_budget = 32000`, que `init_worker` lee como tope total
  ("Workers never declare their own defaults"). Un implementador no puede
  saber cuál es autoritativo.
- **Puntos de no-determinismo:** selección de candidatos, tie-breaking
  (criterios ordenados, juicio), dedup/merge por juicio, umbral de compresión
  ("se aproxima al budget"), scoring de relevancia, distribución del budget de
  KB (`budget/N`, mínimo 500 — aritmética, pero N es juicio).
- **Provenance/orden:** `<order>` monótono por dominio, auditable contra
  `SESSION_LOG.md`; frescura de KB vía `.last_discovery` + provenance del
  manifest — definida y mecánicamente chequeable en principio, pero el
  enforcement de consumo es juicio.

# 12. Determinism Audit

| Fuente de no-determinismo | Controlabilidad | Mitigación actual | Residual |
|---|---|---|---|
| Generación del LLM | No controlable | EARS, rubricas, contratos, validador | Inherente |
| Umbrales de PASS de gates (`[agent]`) | Juicio declarado | Checklists ordenadas + citación de evidencia | **Umbrales indefinidos** — dos evaluadores pueden diferir |
| Composición/resolución de contexto | Juicio declarado | Criterios ordenados, conjuntos cerrados | Cada criterio es juicio del agente |
| Budget de contexto | Advisory | Declarado + eventos de métricas | Sin medición/truncamiento |
| Sampling/merge/ground-truth de discovery | Juicio declarado | Config de sample-size, provenance | Heurística "nombres representativos"; D01 `[agent]` |
| Routing de recovery | Parcial | Tablas first-match | Variables de tabla indefinidas; destinos múltiples sin orden |
| Reanudación de sesión/iteración | Indefinido | Reglas en prosa | Sin procedimiento |
| Enforcement de hooks | Parcial | Scripts deterministas | Fail-open; Bash/Read/Glob/Grep sin gate; dependiente del CLI |
| Disponibilidad de tools / diferencias de provider | No controlable | Spec runtime-neutral | Diferencias de materialización |
| Orden de versionado/registro | Controlado | tags, VERSION, checkers | Staleness de INDEX/changelog |

**Clasificación:** determinismo computacional: parcial (estado/hooks/
validador); determinismo procedural: parcial (ordenado, por juicio);
determinismo de contexto: no entregado (juicio declarado); determinismo de
policy: parcial; determinismo de ejecución: parcial (fail-open); determinismo
semántico: **no entregado** — la especificación permite múltiples
interpretaciones válidas (ver Pregunta Final).

# 13. Zero-Hallucination Audit

- **Prevención:** prohibiciones en `ANTI_CIRCUMVENTION.md`,
  `NO_ASSUMPTIONS.md`, `CONFIDENCE.md` (anti-inflation), EARS, contratos, y la
  skill `hallucination-checker` — todo a nivel de prompt.
- **Detección:** D01 ground-truth `[agent]`; evidencia declarada de H06
  `[agent]`; no existe comparación mecánica claim-vs-source en el payload.
- **Contención/corrección:** flujo de recovery + gate H07 (procedural);
  clases de fallo F1–F5 (declaradas).
- **Observabilidad:** `HARNESS_REPORT.md`/`SESSION_LOG.md` auto-reportados;
  chequeos de schema dev-only post-hoc.
- **Frontera de confianza:** artefactos escritos por el LLM se vuelven estado
  confiable a través de una decisión de gate autoescrita; los únicos gates
  deterministas son estructurales. **No hay mecanismo** que impida a un LLM
  violar cualquier requisito de anti-halucinación excepto el prompt
  diciéndoselo. El protocolo ahora lo *dice* explícitamente (D01: "every item
  is `[agent]`") — honesto, pero "zero hallucination" es una **aspiración**, no
  una garantía.

# 14. Specification vs Implementation

| Spec | Intención | Implementado | Validado | Enforced | Divergencia |
|---|---|---|---|---|---|
| Task profile trivial | Omitir Context Reference en el plan (3.10.0) | Sí | Sí | **No — el validador lo FALLA** | **F-A: validador obligatorio contradice el contrato** |
| H00 gatea la transición trivial | "gated by H00" | Prosa sí; metadata `gates:` no | Checker unidireccional | No | **F-B: declaración de gate ausente** |
| Context budget | Tope finito positivo | Advisory | Solo eventos | No | Divergencia declarada (documentada) |
| H15 validity | Schema completo de payload+return | Subcomandos validan subconjunto | Sí | Juicio | `recommendation`/`project_changes` sin validar |
| D01 ground truth | Claims con source | Prosa | Juicio | No | Divergencia declarada (documentada) |
| H06 evidencia de test | Evidencia resuelve | Prosa | Parcial (citas) | No | Campo `evidence` ausente del contrato |
| Salidas de discovery | Metadata declarativa consistente | Archivos producidos según cuerpos | No | No | Front matter/taxonomía ≠ state machine |

# 15. Failure and Recovery

Bien especificado: clases de fallo F1–F5 (blocker/deviation/ambiguity/
inconsistency/harness FAIL), tablas de recovery por policy con semántica
first-match, derivación de `retry_count`, distinción RETRY_WORKER vs RECOVERY,
abort fundado, transiciones de RECOVERY a fases tempranas, modo desatendido con
defaults declarados.

Caminos indefinidos/inseguros:

1. **Población de variables de las tablas de recovery** — sin almacenamiento
   ni cómputo para `artifact_exists`, `plan_out_of_scope`,
   `merge_inconsistent`, etc.; juicio al momento del fallo → routing
   no-determinista.
2. **Fallos multi-artefacto de fases tempranas** — selección de destino de
   RECOVERY sin orden cuando más de un artefacto temprano es inválido.
3. **Riesgo de ignore silencioso** — un FAIL de harness puede registrarse como
   "desviación documentada" y el gate PASSear; nada valida la legitimidad de
   la desviación.
4. **Semántica de reanudación** — la reconstrucción "último artefacto
   intacto" es prosa procedimental; la continuidad depende de la
   interpretación del LLM.
5. **Falla de hooks** — fail-open por diseño; el scan de bypass es advisory y
   mtime-based (ventana = mtime del dir de sesión → PASS de H04); un archivo
   modificado y revertido dentro de la ventana, o modificado tras H04 vía
   Bash, es invisible.

# 16. Testability and Verification

- **Unit/integración testeado:** tools (145 tests), scripts del harness del
  producto (64 tests incl. flujo enforced end-to-end vía subprocesos),
  materializaciones del runtime (fixtures desacopladas del payload). Todo
  verde.
- **Schema/static testeado:** referencias, citas, estructura de planes,
  coherencia taxonómica, artefactos de sesión, estado de versiones, sync de
  dist, inventario de skills.
- **No falsificable hoy:** umbrales de PASS de ítems `[agent]`; resultados de
  composición de contexto; compliance de budget; ground truth de discovery;
  claims de zero-hallucination; routing de recovery; reconstrucción de
  reanudación; veracidad de flag-evidence. Cada uno es juicio declarado o
  auto-reporte.
- **Test faltante:** ninguno cubre la interacción trivial × validador (F-A) —
  la batería está verde mientras un plan trivial conforme falla H04
  estructuralmente. Es el gap de falsificación más agudo.

# 17. Hidden Assumptions

- Autoridad de gate = un único Orchestrator honesto (sin captura/colusión
  entre evaluador y productor en single-instance más allá de las
  mitigaciones declaradas).
- El CLI entrega eventos de hook en el schema documentado y respeta el exit
  code 2.
- `python` resuelve a un intérprete stdlib-capable en modo enforced.
- Los timestamps (scan de bypass mtime-based) son confiables y monótonos.
- El orden de enumeración del filesystem no afecta resultados de gate (los
  hooks ordenan donde hace falta; el orden de `os.walk` del bypass scan afecta
  solo el orden de alertas, cap 20 archivos).
- La capacidad del LLM de leer `.agents/` equivale a la intención del
  protocolo (asunción del runtime documental).
- Las variables de entorno (`AGENTS_FEATURE_*`, `AGENTS_HEALTH_CHECK_TTL_HOURS`)
  son consistentes entre sesiones.
- Una "desviación documentada" es rara y honesta; nada enforce la rareza.
- Dos sesiones nunca escriben el mismo `.project/<uuid>` (unicidad de UUID
  asumida).
- El mapping `.project/.sessions.json` es exacto tras el primer evento
  (escritura best-effort).
- Los nombres de front matter y secciones de contratos son identificadores
  estables (los bumps de schema_version son el único canal de cambio).

# 18. Contradictions

1. **Plan trivial vs validador obligatorio (ALTO, cierto)** — `EXECUTION_PLAN.md`
   ("For trivial-profile tasks this section is omitted") vs `gate_validator.py`
   (H04 exige `Context Reference`) vs `H04-execution-plan.md` (FAIL estructural
   bloquea PASS).
2. **Budget de discovery (MEDIO, cierto)** — `orchestrator.md`
   (`"context_budget": 100000`) vs `features.toml`
   (`discovery_context_budget = 32000`) vs `init_worker.md` (lee features.toml
   como tope).
3. **Metadata de salidas de discovery (ALTO, cierto)** — listas de salidas de
   la state machine vs front matter/taxonomía (naming + cobertura).
4. **Cobertura de gate H00 (MEDIO, cierto)** — la máquina de estados declara
   `ANALYZING_TASK → PLANNING` gated por H00; H00 `gates:` y la tabla de
   `harness/INDEX.md` lo omiten.
5. **Campo de evidencia H06 (BAJO-MEDIO, cierto)** — la policy exige
   `test_results.evidence`; el contrato define solo `test/result/details`.
6. **Espejos stale (MEDIO, cierto)** — header de `plans/INDEX.md` (3.6.3/2
   commits) vs sus propias tablas y el estado git (3.19.0); `[Unreleased]` del
   CHANGELOG (planes "Aprobado para redacción"/"pendiente") vs `plans/INDEX.md`
   (Executed); `docs/AUDITORIA_DOCUMENTACION.md` (121 tests; "CI sigue sin
   ejecutarlos") vs 145/64 medidos y el workflow de CI.
7. **Single-source vs duplicación sancionada (BAJO, declarada)** —
   `ANTI_CIRCUMVENTION.md` restate la regla de inmutabilidad del payload; la
   excepción está documentada en `PROTOCOL_BOUNDARIES.md` — resuelta como
   declarada.

# 19. Technical Debt

| Clase | Ítem | Severidad | Detectabilidad |
|---|---|---|---|
| Specification | Población de variables de tablas de recovery indefinida | Alta | Manual |
| Contract | Camino trivial vs validador H04 | Alta | Testeable (no hay test) |
| Reference | Metadata de salidas de discovery (naming + cobertura) | Alta | Testeable (checker unidireccional) |
| Determinism | Asamblea de contexto = juicio; budget advisory | Alta (declarada) | Automática (declarada en docs) |
| Hallucination-control | Ground truth `[agent]`; evidencia auto-reportada | Alta (declarada) | Manual |
| Enforcement | Validador obligatorio bypasseable vía "desviación documentada" | Media | Manual |
| Enforcement | Superficie de bypass de hooks (Bash/Read/Glob/Grep, fail-open, target desconocido) | Media | Testeable |
| Documentation | Header de INDEX, `[Unreleased]` del CHANGELOG, AUDITORIA_DOCUMENTACION stale | Media | Automática (ningún checker cubre claims) |
| Naming | ENVIRONMENT_DISCOVERY.md vs environment.md; profile/harness/runtime sobrecargados | Media | Manual |
| Test | Sin test trivial×validador; sin test de evidencia H06 | Media | — |
| Contract | `test_results.evidence` inexistente; subconjunto de schema H15 | Baja-Media | Manual |
| Semantic | YAML de taxonomía produced_by/consumed_by de INTER_WORKER_MESSAGE / KB_DISCOVERY_ENTRY inexacto | Baja | Manual |
| Documentation | "Three pure-stdlib scripts" (INDEX.md) vs cuatro scripts (ADOPTION.md) | Baja | Automática (sin checker) |
| Evolution | Ceremonia de gobernanza por cambio; regularizaciones recurrentes | Media | Manual |

# 20. Critical Findings

**Finding: camino trivial roto por el validador estructural obligatorio (F-A)**

- **Clasificación:** CONTRADICTORIO / NO IMPLEMENTADO (enforcement diverge de
  la spec)
- **Severidad:** Alta
- **Evidencia:** `EXECUTION_PLAN.md` §Context Reference ("For trivial-profile
  tasks this section is omitted"); `gate_validator.py` TRIGGERS["H04"].sections
  incluye "Context Reference"; `H04-execution-plan.md` §Decision Criteria
  ("MUST run gate_validator.py … a structural FAIL blocks PASS unless recorded
  as a documented deviation"); `AGENT_STATE_MACHINE.md` §Task Profiles.
- **Problema:** un plan trivial conforme siempre produce FAIL estructural; la
  única salida es una desviación documentada por gate, que no es
  profile-aware. El validador es "obligatorio" pero sistemáticamente
  override, y el camino trivial — legalizado por el plan 59 — es el punto de
  enforcement menos determinista.
- **Por qué importa:** las dos series de remediación más recientes (59
  legalizó el camino; 68 hizo obligatorio el validador) produjeron una
  interacción silenciosa que ningún test detecta.
- **Impacto en determinismo:** los resultados de gates del camino trivial
  dependen de si el Orchestrator documenta una desviación; inputs idénticos
  pueden producir registros PASS distintos.
- **Impacto en anti-halucinación:** el mecanismo de desviación es
  autoautorizado; nada constriñe su uso.
- **Confianza:** Alta

**Finding: H00 no declara la transición trivial que gatea (F-B)**

- **Clasificación:** INCONSISTENTE / NO ESPECIFICADO
- **Severidad:** Alta
- **Evidencia:** front matter `gates:` de H00 (3 transiciones, sin PLANNING) vs
  `AGENT_STATE_MACHINE.md` ("This transition is available only for
  trivial-profile tasks … gated by H00") vs taxonomía `core:ANALYZING_TASK.next`
  (incluye PLANNING); `check_taxonomy_coherence.py` chequea solo
  gate-target ⊆ source.next (unidireccional).
- **Problema:** el mapa declarativo gate→transición contradice la prosa; un
  modelo de máquina construido desde front matter no gatearía la transición
  trivial.
- **Confianza:** Alta

**Finding: metadata de contratos de salida de discovery inconsistente (F-C)**

- **Clasificación:** REFERENCE DEBT / INCONSISTENTE
- **Severidad:** Alta
- **Evidencia:** `DISCOVERY_STATE_MACHINE.md` §Required Output Artifacts (p.ej.
  stack: 6 salidas) vs front matter de workflows (`02-discovery-stack.md`:
  `[worker_stack.json]`; la taxonomía lo refleja) vs división de naming
  `ENVIRONMENT_DISCOVERY.md`/`environment.md`.
- **Problema:** el diccionario single-source y su checker no cubren el tercer
  origen (cuerpos de la state machine); un implementador estricto recibe dos
  contratos de salida distintos.
- **Confianza:** Alta

**Finding: el enforcement sigue siendo auto-evaluación en el núcleo (F-D)**

- **Clasificación:** LIMITACIÓN DECLARADA (no oculta)
- **Severidad:** Crítica (fundacional), por declaración
- **Evidencia:** `harness/INDEX.md` §Enforcement model; `HARNESS_REPORT.md`
  ("self-reported … not independently verified evidence"); D01 ("every item is
  [agent]"); BUDGET_MATERIALIZATION §7 (advisory).
- **Problema:** el enforceability mecánico sigue limitado a dos eventos de
  hook, un registrador de estado, una sonda y un lint estructural; todos los
  gates semánticos dependen del compliance del LLM.
- **Confianza:** Alta

# 21. Missing Foundations

- Un **validador estructural profile-aware** (o un modo trivial declarado en
  `gate_validator.py`) — cierra F-A.
- **Chequeo bidireccional de cobertura de gates** (toda transición de la
  taxonomía cubierta por una policy) — cierra F-B.
- **Reconciliación cuerpo-de-state-machine ↔ taxonomía/workflows** para
  discovery — cierra F-C.
- **Semántica mecánica de variables de recovery** (dónde se almacenan/calculan
  `artifact_exists`, `plan_out_of_scope`, etc.).
- **Contabilidad mecánica del budget** (declarada como future extension; hasta
  entonces los claims de budget son infalsificables).
- **Verificación independiente de decisiones de gate** (p.ej. una auditoría
  post-hoc determinista que recompute los ítems `[gate]` desde artefactos, no
  desde la prosa de HARNESS_REPORT).
- **Procedimiento de reanudación de sesión** ("último artefacto intacto").
- **Checker de frescura de claims de CHANGELOG/INDEX** (o retirar claims de
  `[Unreleased]` cuando los planes se ejecutan).
- **Modelo de evidencia de test** — un campo `evidence` definido en
  `test_results` y un chequeo determinista de existencia.
- **Branch protection server-side** (decisión aceptada del owner; mitigación
  documentada).

# 22. Architectural Risk

Si la arquitectura sigue evolucionando sin resolver estos puntos, la
trayectoria esperada:

1. Cada policy nueva agrega ítems de juicio; la cobertura de enforcement se
   mantiene constante → el gap entre "documentado" y "enforced" crece en
   silencio.
2. El loophole de desviación del camino trivial se vuelve precedente para
   desviaciones rutinarias en otros gates, normalizando la "desviación
   documentada" como sello de goma.
3. Discovery crece (más contratos por entrada, más tipos de KB) mientras su
   metadata declarativa de salidas queda parcial/inconsistente → dos
   implementadores divergen sobre dónde van las salidas; los consumidores de
   KB se rompen contra uno de ellos.
4. El aparato de gobernanza (ceremonia RFC/plan/INDEX/changelog) acumula
   espejos stale más rápido de lo que los checkers los cubren; la staleness
   del INDEX reapareció un día después de la promoción de 3.19.0.
5. Las métricas siguen siendo advisory y auto-reportadas; el protocolo no
   puede distinguir sus propias señales de salud del optimismo del agente.

# 23. Recommended Remediation Order

## P0 — Debe resolverse antes de expandir la arquitectura

- Hacer `gate_validator.py` profile-aware (modo trivial para H04: omitir
  Context Reference) + test de regresión del camino trivial. *Ref: F-A.*
- Agregar `ANALYZING_TASK → PLANNING` a `gates:` de H00 y a la tabla de
  triggers de `harness/INDEX.md`; extender `check_taxonomy_coherence.py` para
  verificar cobertura bidireccional de gates. *Ref: F-B.*

## P1 — Requerido para ejecución coherente

- Reconciliar declaraciones de salidas de discovery (state machine ↔ front
  matter ↔ taxonomía), una convención de naming, y extender el checker a los
  cuerpos de state machines. *Ref: F-C.*
- Corregir el literal `context_budget: 100000` en `orchestrator.md` (usar el
  valor de features.toml o un placeholder explícito). *Ref: F-D.*

## P2 — Requerido para determinismo y verificación

- Definir almacenamiento/cómputo de las variables de las tablas de recovery;
  ordenar destinos multi-artefacto de recovery.
- Agregar `test_results.evidence` al contrato y un chequeo determinista de
  evidencia al validador.
- Agregar el test trivial×validador y el test de cobertura H00 a la suite del
  producto.

## P3 — Requerido para mantenibilidad

- Refrescar el snapshot del header de `plans/INDEX.md`, `[Unreleased]` del
  CHANGELOG y los conteos de `docs/AUDITORIA_DOCUMENTACION.md`; agregar un
  chequeo de frescura de claims o hacer que las notas de gobernanza de
  `[Unreleased]` expiren al ejecutarse el plan.
- Corregir "three scripts" de INDEX.md vs "cuatro scripts" de ADOPTION.md.

## P4 — Mejoras

- Auditoría post-hoc independiente de gates (recomputar ítems `[gate]` desde
  artefactos).
- Contabilidad mecánica del budget; procedimiento de reanudación de sesión;
  modelo de confianza de eventos de métricas.

---

# Plan de remediación por bloques (orden de menor a mayor complejidad e impacto)

La "clase de cambio" es la vía de gobernanza según RFC-56: **C** = corrección
mecánica (commit directo en `dev`), **B** = mejora documental compatible (plan
aprobado), **A** = modelo conceptual/contratos (RFC `Accepted`). Los ítems que
tocan solo `tools/`, `docs/` o `tests/` no requieren plan ni RFC.

## Bloque 0 — Quick wins (complejidad baja, impacto bajo)

| # | Ítem | Resuelve | Complejidad | Impacto | Clase |
|---|---|---|---|---|---|
| 1 | Corregir `harness/INDEX.md`: "Three pure-stdlib Python scripts" → cuatro (agregar `gate_validator.py`). Inconsistencia con `ADOPTION.md` ("cuatro scripts"). | §19 Doc | Muy baja | Bajo | C (payload) |
| 2 | Corregir el literal `"context_budget": 100000` en `orchestrator.md` §4.3 → alinear con `features.toml` (`discovery_context_budget = 32000`) o placeholder. | F-D / §18.2 | Muy baja | Bajo | C o B |
| 3 | Actualizar el snapshot del header de `plans/INDEX.md` (3.6.3 / 2 commits → 3.19.0 en sync). | §6.2 | Muy baja | Bajo | Sin clase (repo) |
| 4 | Limpiar `[Unreleased]` del CHANGELOG: planes 37–40/42 "Aprobado para redacción" y 43–47 "pendiente" (ya Executed y publicados). | §6.3 | Muy baja | Bajo | Sin clase (repo) |
| 5 | Actualizar conteos stale en `docs/AUDITORIA_DOCUMENTACION.md` (121 → 145; "CI no ejecuta harness tests" → sí, 64) y `AUDITORIA_SISTEMA.md` (39 → 64). | §6.4 | Muy baja | Bajo | Sin clase (repo) |
| 6 | Corregir el modelo produced_by/consumed_by del YAML de taxonomía para `INTER_WORKER_MESSAGE.md` y `KB_DISCOVERY_ENTRY.md` (productores reales: los 7 workers por scope). | §5, §19 | Baja | Bajo | B (payload) |

## Bloque 1 — Coherencia de contratos (complejidad baja-media, impacto medio)

| # | Ítem | Resuelve | Complejidad | Impacto | Clase |
|---|---|---|---|---|---|
| 7 | Alinear H06 ítem 7 con el contrato: campo `evidence` (opcional) en `[[test_results]]` de `VERIFICATION_REPORT.md` + reformular el checklist. | §6.5, §9.2 | Baja-media | Medio | A/B |
| 8 | Reconciliar la metadata de salidas de discovery: una lista canónica por estado y una convención de nombre. | F-C / §6.1 | Media | Medio-alto | B (payload) |
| 9 | Extender `check_taxonomy_coherence.py` para comparar los "Required Output Artifacts" de los state machines contra taxonomía/workflows. | F-C / §6.1 | Media | Medio | Sin clase (tools) + tests |

## Bloque 2 — Cierre de las contradicciones P0 (complejidad media, impacto alto)

| # | Ítem | Resuelve | Complejidad | Impacto | Clase |
|---|---|---|---|---|---|
| 10 | Hacer `gate_validator.py` profile-aware (modo trivial para H04) + test de regresión del camino trivial. | F-A / §18.1 / §20 | Media | Alto | B |
| 11 | Agregar `ANALYZING_TASK → PLANNING` a `gates:` de H00 y a la tabla de triggers de `harness/INDEX.md`. | F-B / §18.4 | Baja-media | Alto | B (payload) |
| 12 | Extender el checker a cobertura bidireccional de gates (toda transición del taxonomy cubierta por exactamente una policy). | F-B / §7 | Media | Alto | Sin clase (tools) + tests |

## Bloque 3 — Determinismo y verificación (complejidad media-alta, impacto alto)

| # | Ítem | Resuelve | Complejidad | Impacto | Clase |
|---|---|---|---|---|---|
| 13 | Definir almacenamiento/cómputo de las variables de las recovery decision tables. | §15.1 / §19 | Media-alta | Alto | A (modelo) |
| 14 | Definir ranking de destinos de recovery con múltiples artefactos de fases tempranas fallidos. | §15.2 | Media | Medio | A (modelo) |
| 15 | Evidencia determinista de test (`test_results.evidence` con verificación de existencia/SESSION_LOG) en el validador de H06. | §9.2 / §14 | Media | Medio | B + tools |
| 16 | Especificar el procedimiento de reanudación de sesión ("último artefacto intacto"). | §15.4 / §17 | Media | Medio | A (modelo) |
| 17 | Endurecer la semántica de "desviación documentada": límites, registro, auditoría post-hoc. | §15.3 / §20 | Media-alta | Alto | A/B (policy) + tools |
| 18 | Auditar post-hoc e independiente los gates: recomputar ítems `[gate]` desde artefactos y comparar con HARNESS_REPORT. | F-D / §16 | Alta | Alto | B (payload) + tools |

## Bloque 4 — Modelo y runtime (complejidad alta, impacto crítico)

| # | Ítem | Resuelve | Complejidad | Impacto | Clase |
|---|---|---|---|---|---|
| 19 | Contabilidad mecánica del Context Budget (medir el payload contra `context_budget`; al menos alertar). | §11 / §19 | Alta | Crítico | A (modelo + runtime) |
| 20 | Reducir la superficie de bypass de los hooks (evaluar gating de Bash/Read/Glob/Grep y el fail-open ante target desconocido). | §7 / §15.5 | Alta | Alto | A/B (hook + payload) |
| 21 | Modelo de confianza de métricas: separar eventos auto-reportados de evidencia verificable. | §13 / §16 | Alta | Alto | A (modelo) |
| 22 | (Opcional, organizacional) Revisar la ceremonia de gobernanza: fast-track real para cambios menores con checker verde. | §19 Evolución | Media | Medio | Sin clase |

## Notas de orden

- El orden es por complejidad creciente; dentro de cada bloque, los ítems con
  más impacto van después porque dependen de los anteriores: el validador
  profile-aware (10) necesita la metadata de H00 (11) para ser testeable
  end-to-end, y la auditoría post-hoc (18) solo tiene sentido cuando el
  validador y el registro de desviaciones (17) estén definidos.
- Los ítems 1–6 desbloquean la lectura del repo: eliminan afirmaciones que
  contradicen el estado real y evitan que el próximo cambio se apoye en
  números viejos.
- Los ítems 10–12 son el P0 de la auditoría: sin ellos, el camino trivial
  (legalizado en 3.10.0) queda en contradicción con el validador obligatorio
  (3.19.0) y la batería sigue verde mientras un plan trivial conforme falla
  estructuralmente.
- Los ítems 19–21 no deberían empezarse antes de cerrar 10–18: son "Future
  Extensions" declaradas que, si se construyen sobre las contradicciones
  actuales, las cristalizan en código.

---

# Pregunta Final

> **Si un equipo de ingeniería totalmente independiente recibiera el repositorio
> actual e intentara implementar un runtime compatible solo a partir de sus
> especificaciones, contratos, policies, harnesses, manifests y documentación
> arquitectónica, ¿cuántas decisiones importantes tendría que tomar por su
> cuenta?**

Muchas, concentradas en: (1) el umbral de PASS de cada ítem `[agent]` de los
checklists; (2) selección de candidatos de contexto, tie-breaking,
dedup/merge y decisiones de compresión; (3) unidades/accounting/truncación del
budget (advisory); (4) población de variables de routing de recovery y orden
de destinos múltiples; (5) sampling de discovery, resolución de conflictos de
merge y juicio de ground truth (D01); (6) reconstrucción de reanudación de
sesión; (7) si/cómo usar el validador opcional, los hooks y los subcomandos — y
qué hacer con la desviación del camino trivial; (8) validación semántica del
return report de H15; (9) el significado de "desviación documentada" como
override; (10) cuál de las listas contradictorias de salidas de discovery es
autoritativa.

> **¿Podrían dos equipos competentes implementar ARgentOS de forma diferente
> creyendo ambos razonablemente que siguieron la especificación?**

**Sí.** Los puntos de divergencia concretos: (a) ejecución del camino trivial
(FAIL del validador vs omisión del contrato → desviación o inclusión de la
sección); (b) gating de H00 de la transición trivial (metadata vs prosa); (c)
salidas de discovery (naming + cuál lista es autoritativa); (d) todo umbral de
gate `[agent]`; (e) resultados de composición de contexto y enforcement del
budget; (f) routing de recovery; (g) reanudación de sesión; (h) si D01/H15
reciben alguna implementación mecánica; (i) fuente del budget de discovery
(features.toml vs payload de invocación).

**Conclusión:** el valor de ARgentOS hoy es su disciplina de especificación y
gobernanza — el framework de protocolo documental más maduro y
auto-chequeado de su tipo — no su determinismo de runtime. La implementación
actual garantiza estructura, trazabilidad y honestidad sobre sus propios
límites; no garantiza comportamiento determinista. Un sistema más chico con
semántica explícita e invariantes enforced sigue siendo preferible a este más
grande cuyo comportamiento central depende de la interpretación — y los ítems
P0 (10–12) son los dos pasos más chicos y de mayor palanca para cerrar el gap
de enforcement más reciente.

---

# Remediation Tracker

## Cómo usar

1. Cuando un ítem se resuelva, cambiar su Status a `Resolved` y agregar la
   evidencia (plan/RFC, commit, fecha).
2. Trabajar en orden de bloque: 0 → 1 → 2 → 3 → 4.
3. Si el ítem toca `protocol/.agents/`, respetar la clase de cambio según
   RFC-56 y mantener la batería en verde.

## Estado de bloques

| Bloque | Status | Evidencia / Notas |
|---|---|---|
| 0 — Quick wins | ☑ Resolved | Plan 69 `Executed` (2026-08-16, versión 3.20.0); ítems 1–6 aplicados en `dev` con batería en verde |
| 1 — Coherencia de contratos | ☑ Resolved | Plan 70 `Executed` (2026-08-16, versión 3.21.0); ítems 7–9 aplicados en `dev` con batería en verde |
| 2 — Cierre P0 | ☑ Resolved | Plan 71 `Executed` (2026-08-16, versión 3.22.0); ítems 10–12 aplicados en `dev` con batería en verde |
| 3 — Determinismo y verificación | En curso (parcial) | ítems 15/17/18 ☑ Resolved (plan 72, 2026-08-16, versión 3.23.0); ítems 13/14/16 pendientes (Clase A, requieren RFC) |
| 4 — Modelo y runtime | Pendiente | Ítems 19–22 |
