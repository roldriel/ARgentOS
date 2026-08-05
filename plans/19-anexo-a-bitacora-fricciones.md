# Plan 19 — Anexo A: Bitácora de fricciones clasificadas

**Fecha:** 2026-08-05. **Sesión:** `.project/d4ab6a93-8e75-4880-baf3-676fce992936/` (iteración `00`).
**Proyecto de validación:** `tools/check_plan_citations.py` + `tools/tests/test_check_plan_citations.py` (verificador de citas `ruta:sección` de `plans/`), ejecutado end-to-end por protocolo: H00→H07 + H09 + H11 + D00/D01 + H15 (pre/post), estado final `COMPLETED`.

Cada fricción registra: (1) qué pasó, (2) qué decía el protocolo, (3) clase de fallo según la taxonomía vigente (F1 blocker, F2 deviation, F3 ambiguity, F4 inconsistency, F5 harness FAIL — definidas inline en `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` (§Issues Found) y mapeadas en `.agents/contracts/METRICS.md` (§Event catalog); "sin clase" cuando el fallo no encaja), (4) costo estimado, (5) clasificación del plan 19 §C: **modelo** (→ enmienda RFC), **policy** (→ ajuste de policy/contrato), **gap** (→ plan nuevo), **ruido** (descartado con justificación).

---

## A. Fricciones del subsistema core

### F-01 — Contrato de spec vs validador EARS del runner
1. H01 FALLÓ sobre `04-TASK_SPECIFICATION.md`: el criterio estaba en el bloque TOML del contrato (`acceptance_criteria = [...]`) y el validador machine (`validate_ears`) solo lee bullets Markdown `- `.
2. El contrato `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` (§Acceptance Criteria) muestra la forma canónica como array TOML; los bullets aparecen solo en un bloque "Example". La policy H01 declara validación EARS machine.
3. F4 (inconsistency) detectada como F5 (harness FAIL).
4. Costo: 1 gate FAIL + fase RECOVERY completa + re-trabajo del writer (~15 min de sesión).
5. **policy** — alinear contrato y validador (declarar los bullets como forma canónica machine-checkable).

### F-02 — Árbol H01 sin camino de retry para fallos de formato
1. Con `artifact_exists=true, retry_count=0`, objetivo/scope claros, `H01_FAIL.toml` devolvió `RECOVERY_GENERIC`; no existe rama `RETRY_WORKER` para fallos triviales de formato. `.agents/orchestrators/core/harness/decision_trees/VARIABLES.md` (§Optional boolean variables) no tiene variable "formato corregible".
2. `.agents/harness/INDEX.md` (§Failure Handling) dice "the Worker may be re-invoked once to correct it"; el árbol no puede expresarlo para este modo de fallo.
3. F5 con destino forzado desproporcionado; "sin clase" para el gap de expresividad del árbol.
4. Costo: una fase RECOVERY entera (artefacto + gate H09 + decisión) por corregir el formato de una sección.
5. **policy** — agregar variable/rama de retry acotado para fallos machine de formato.

### F-03 — La máquina de estados no modela vuelta a fases tempranas desde RECOVERY
1. La corrección exigía volver a `BUILDING_TASK_SPECIFICATION`; `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (§RECOVERY) solo permite `RECOVERY → PLANNING` y `RECOVERY → NEEDS_CLARIFICATION`. Se ejecutó la vuelta como desviación registrada y justificada (ver `SESSION_LOG.md` entrada 12:45).
2. Los árboles sí nombran fases tempranas como `target_phase` en `RETRY_WORKER` (`.agents/orchestrators/core/harness/decision_trees/H01_FAIL.toml` [nodes.start.true]) — el modelo de estados y los árboles no coinciden.
3. F4 (inconsistency entre modelo de estados y árboles).
4. Costo: 1 desviación de máquina de estados, registrada; riesgo de normalizar desviaciones si se repite.
5. **modelo** — enmienda al modelo de recovery (RFC-18, `plans/rfc/18-failure-recovery-taxonomy.md`) y/o a la máquina de estados.

### F-04 — INTENT_REFLECTION con confianza HIGH sin transición que la produzca
1. `AGENTS.md` (§Intent reflection layer) y `.agents/orchestrators/core/roles/orchestrator.md` (§Intent Reflection Enforcement) piden generar `INTENT_REFLECTION.md` aun con confianza HIGH (auto-confirm); la máquina de estados solo la produce en `CONFIRMING_INTENT`. Se generó igualmente y se gateó con H11 (PASS), pero la norma es ambigua sobre en qué estado ocurre.
2. Ídem (fuentes citadas arriba).
3. F4 (inconsistency documental).
4. Costo: bajo; una decisión de interpretación.
5. **policy** — aclarar en `AGENT_STATE_MACHINE.md` o en `orchestrator.md` dónde se produce la reflexión auto-confirmada.

### F-05 — Dos NEEDS_CLARIFICATION sin usuario disponible
1. Sesión desatendida (dogfooding): el Orchestrator respondió las clarificaciones en nombre del autor del plan (2 veces: regla de extracción inicial y forma de citación dominante `` `path` §Section `` descubierta en el censo de contexto). Decisiones y justificación registradas en `SESSION_BRIEF.md` y `SESSION_LOG.md`.
2. `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (§NEEDS_CLARIFICATION) exige pedir input al usuario; no existe modo desatendido/asíncrono ni política de defaults confirmables.
3. F3 (ambiguity) resuelta fuera del canal previsto; "sin clase" para la ausencia del modo.
4. Costo: 2 desviaciones documentadas; sin el workaround del plan 19 la sesión se bloqueaba.
5. **gap** — plan nuevo: política de clarificación desatendida (defaults declarados + confirmación diferida).

### F-06 — Las 7 preguntas de selección de perfil no cubren tooling/CLI
1. La tarea (CLI de verificación para desarrolladores) no encaja en Q1–Q6; `backend_engineer` queda marginal ("business logic, endpoints, services"). Se seleccionó `profile: null` con justificación (ver `SESSION_LOG.md` 13:05).
2. `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` (§3. The 7 decision questions, 7 preguntas mutuamente excluyentes).
3. "sin clase" (no es fallo de ejecución; es cobertura del modelo de candidatura, RFC-20).
4. Costo: bajo; una decisión judgmental que debió ser mecánica.
5. **modelo** — enmienda menor a RFC-20 (`plans/rfc/20-profile-selection-model.md`) o nota en la guía: tareas de tooling → worker genérico.

### F-07 — Mandato de referenciar KB de discovery sin condición de disponibilidad
1. `.agents/orchestrators/core/roles/orchestrator.md` (§5. Worker Delegation) exige incluir `environment.md` y `development_patterns.md` en delegaciones de ejecución; el refresh de discovery estaba en curso al delegar y el worker no leyó realmente `development_patterns.md`. Desviación declarada en `.project/d4ab6a93-8e75-4880-baf3-676fce992936/00/10-EXECUTION_SUMMARY.md` (§Issues or Deviations).
2. Ídem; el mandato no contempla "KB en refresco" ni fallback.
3. F2 (deviation), declarada.
4. Costo: 1 desviación; riesgo de referencias colgadas en auditoría.
5. **policy** — condicionar el mandato a KB válida (D01 PASS reciente) o definir fallback explícito.

### F-08 — H15 sin subcomando de runner
1. La evaluación machine de H15 se hizo importando `delegation_validity.py` a mano (primera llamada con aridad incorrecta; el post-return inicial FALLÓ por schema inventado: faltaban `output_artifact`, `role_executed`, `phase_completed`, `summary` y el prefijo de clase en `deviations` — corregido según `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` §Worker Return Report → PASS).
2. `.agents/harness/RUNNER.md` (§Module layout): "The runner CLI does not execute H15"; el schema del return report vive en prosa de contrato.
3. "sin clase" (fricción de operación, no fallo); el FAIL de post-return fue F1 detectado correctamente por el gate — señal positiva.
4. Costo: medio (lectura de API + 1 ida y vuelta de schema por gate).
5. **gap** — subcomando `runner.py validate-delegation` / `validate-return` (plan chico).

### F-09 — Worker-per-phase ejecutado en una sola instancia
1. Las fases core se ejecutaron con una única instancia de runtime adoptando cada rol (orchestrator + workers); solo discovery se delegó a un subagente real. Registrado como desviación de proceso en `SESSION_LOG.md` (cierre).
2. `.agents/orchestrators/core/roles/orchestrator.md` (§5. Worker Delegation): "the Orchestrator invokes a new worker subagent" por fase; `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (§Core Rules).
3. F2 (deviation de proceso), declarada.
4. Costo del cumplimiento estricto estimado alto (handoff de contexto por fase); el dato alimenta el modelo de materialización de delegaciones.
5. **gap** — estudio/plan sobre modelo de ejecución de delegaciones en runtimes de contexto único (baja prioridad; ver también RFC-00YK `plans/rfc/13-execution-context-materialization-model.md`).

### F-10 — Deriva de timestamps autor-reportados
1. Los `created_at`/eventos se escribieron con reloj aproximado y derivaron ~15 min por delante del reloj real (verificado con `date -u` al cierre: 13:04Z vs eventos registrados hasta 13:20Z).
2. Los contratos exigen ISO-8601 (`SESSION_LOG.md`, `METRICS.md`); ninguna policy exige disciplina de reloj.
3. "sin clase".
4. Costo: bajo; ruido de traza.
5. **ruido** — justificación: no altera orden ni validez de gates (el runner estampa sus propios timestamps en `HARNESS_REPORT.md`); se registra como dato, sin trabajo derivado.

---

## B. Fricciones del subsistema discovery (reportadas por el Discovery Orchestrator, scope full, 7/7 workers)

### F-11 — Gate D01 no superable tal como está especificado (crítica)
1. `runner.py --trigger D01` FALLÓ en `artifact_exists`: resuelve `artifact_validated: KB_DISCOVERY_ENTRY.md` solo dentro de la iteración de sesión, pero las KB entries viven en `.project/knowledge/discovery/`. Ningún archivo permitido satisface el check machine; se salvó con un artefacto-puente de sesión (`00/02-KB_DISCOVERY_ENTRY.md`, índice de validación explícito).
2. `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` (§Input) ("KB entries: `.project/knowledge/discovery/*.md`") vs resolución de artefactos del runner (`.agents/harness/RUNNER.md` (§Artifact validation)).
3. F5 (harness FAIL) por F4 (inconsistency spec↔runner).
4. Costo: 1 gate FAIL + diseño del artefacto-puente (~10 min); se repite en cada discovery.
5. **policy** — especial-casing de D01 en el runner o artefacto de sesión definido por el workflow.

### F-12 — Marcador `.last_discovery` en ruta y formato distintos a la spec
1. El marcador real estaba en `.project/knowledge/discovery/.last_discovery` (timestamp pelado); la spec exige `.project/.last_discovery` JSON `{timestamp, scope, status}`. La lógica TTL no veía el archivo legado → TTL tratado como expirado → full discovery.
2. `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` (seccion 'The `.last_discovery` marker' — el nombre lleva backticks, no citables en forma §) ("If the file is missing or unparsable, the core Orchestrator treats the TTL as expired").
3. F4 (inconsistency spec↔ejecución previa).
4. Costo: detección + disparo de un full discovery posiblemente evitable.
5. **policy** — una sola ruta canónica + validación (health-check) del marcador.

### F-13 — `context_budget` referenciado pero no configurado
1. Los roles de discovery acotan sampling por `context_budget` "from `.agents/features.toml`", pero `features.toml` no define ese setting (solo `discovery_sample_size` y TTLs). El init_worker declaró 32000 tokens por juicio.
2. `.agents/orchestrators/discovery/roles/discovery_orchestrator.md` (§Sampling); `.agents/features.toml` (archivo TOML, sin encabezados Markdown: bloque de settings de discovery).
3. F4 (inconsistency) / "sin clase".
4. Costo: bajo; una decisión que debía ser lectura de config.
5. **policy** — agregar `discovery_context_budget` a `features.toml` o corregir la referencia.

### F-14 — El manifest no puede expresar marcado legacy
1. El rol ordena marcar entradas legadas `confidence: low` + `status: legacy` "in the manifest", pero `DISCOVERY_MANIFEST.md` solo tiene `[entries] active/stale`. Se registró en `invalidation_report.json`.
2. `.agents/orchestrators/discovery/roles/discovery_orchestrator.md` (§KB consumption and enrichment) vs contrato `.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md` (§Format).
3. F4 (inconsistency instrucción↔contrato).
4. Costo: menor; instrucción inimplementable tal cual.
5. **policy** — campos por entrada en el manifest o corrección del rol.

### F-15 — "Primera línea" del executive summary vs front matter obligatorio
1. `EXECUTIVE_SUMMARY.md` exige que la primera línea declare `project_shape` y a la vez front matter TOML; la primera línea literal sería `+++`. Se puso el shape como primera línea de contenido.
2. Contrato `EXECUTIVE_SUMMARY.md` (Purpose/Constraints).
3. F4 (inconsistency interna del contrato).
4. Costo: trivial.
5. **policy** — redacción del contrato.

### F-16 — `project_shape: unknown` pierde información real
1. Las señales deterministas solo reconocen shapes empaquetados/ejecutables; un repo documental+protocolo con dos codebases Python stdlib clasifica `unknown`, degradando `api.md` y omitiendo `distribution.md`.
2. `init_worker.md` (señales de `project_shape`, vía `00-discovery-init.md`).
3. "sin clase" (modelo de clasificación, no fallo).
4. Costo: KB menos informativa de lo que el repo justifica.
5. **modelo** — enmienda al modelo de clasificación de shape (o shape adicional `documentation/tooling`).

### F-17 — `source_files` sin valor de procedencia para ausencias y hechos de árbol
1. `containers.md`/`database.md` afirman ausencias y `file_map.md` reporta forma de árbol; D01 item 5 exige que todo `source_files` exista; `system_probe` solo es legal para environment. Se citaron raíces escaneadas con nota explícita.
2. `KB_DISCOVERY_ENTRY.md` + `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` (§Checklist).
3. "sin clase" (gap de contrato).
4. Costo: menor.
5. **policy** — valor de procedencia "observado por scan" en el contrato.

### F-18 — Delimitadores de front matter de KB entry no especificados
1. El contrato muestra bloque ```toml; las entradas legadas usan `+++`; `.agents/` usa `---`. Se mantuvo `+++`.
2. `KB_DISCOVERY_ENTRY.md`.
3. "sin clase".
4. Costo: trivial.
5. **policy** — una línea en el contrato fijando el delimitador.

### F-19 — Cálculo de hashes asignado a dos actores distintos
1. `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` (§Hash Calculation) dice que el core Orchestrator los calcula antes de invocar; `init_worker` (task 3) dice que los calcula init_worker. Se calcularon en init_worker (único lugar donde se usan).
2. Fuentes citadas.
3. F4 (inconsistency).
4. Costo: nulo; contradicción latente.
5. **policy** — unificar actor (sugerido: init_worker).

### F-20 — Entradas de discovery en la iteración core colisionan con el orden `<order>`
1. Los artefactos de sesión de discovery (`00/01-KB_DISCOVERY_REPORT.md`, `00/02-KB_DISCOVERY_ENTRY.md`) comparten la carpeta y la secuencia `<order>` de la iteración core (`01-TASK_ANALYSIS.md`, `02-TASK_ANALYSIS.md`); dos dominios numeran el mismo espacio.
2. `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (§Artifact Safety Rule) (regla `<order>` auditable contra `SESSION_LOG.md`).
3. F4 (inconsistency de layout) / "sin clase".
4. Costo: nulo en esta ejecución; riesgo de colisión/confusión de auditoría.
5. **policy** — namespacing por dominio (p. ej. `D01-…` o subcarpeta `discovery/` ya prevista para outputs intermedios).

### F-21 — KB legada con hechos falsos (`language_hint: Java`)
1. `stack.md` legado contenía `language_hint: Java` (sin Java en el repo) y rutas absolutas de otra máquina; las reglas de merge lo resolvieron (reemplazo, confidence low→high).
2. `06-discovery-merge.md` (reglas de merge).
3. F4 detectada y resuelta por el propio mecanismo — señal positiva.
4. Costo: nulo.
5. **ruido** — el mecanismo funcionó como fue diseñado; no deriva trabajo.

---

## C. Clasificación consolidada (plan 19 §C)

| Destino | Fricciones |
|---|---|
| **modelo** (→ enmienda RFC) | F-03 (recovery→fases tempranas; RFC-18), F-06 (perfil tooling; RFC-20), F-16 (project_shape) |
| **policy** (→ ajuste policies/contratos) | F-01, F-02, F-04, F-07, F-11, F-12, F-13, F-14, F-15, F-17, F-18, F-19, F-20 |
| **gap** (→ planes nuevos) | F-05 (clarificación desatendida), F-08 (CLI H15), F-09 (modelo de ejecución de delegaciones, baja prioridad) |
| **ruido** (descartado con justificación) | F-10 (deriva de reloj: sin efecto en gates), F-21 (merge funcionó según diseño) |

## D. Señales positivas (dato complementario)

- H01/H06/H07 y el resto de gates machine corrieron en 1–6 ms con evidencia explícita por check (ver `HARNESS_REPORT.md`).
- H15 post-return detectó un return report mal formado (F1) y lo guió al schema del contrato: el gate aporta valor real.
- El segundo NEEDS_CLARIFICATION (censo de citas) evitó construir una herramienta inútil: la especificación original solo cubría ~0 citas reales; la enmienda v2 cubrió ambas formas. El ciclo contexto→clarificación→spec se pagó solo.
- Las reglas de merge de discovery purgaron una KB legada con hechos falsos sin intervención.
