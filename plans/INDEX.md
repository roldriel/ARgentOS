# Índice de planes — ARgentOS

Estado al 2026-07-28. El trabajo activo es el **Execution Context Pipeline** (`feature.md`) y su roadmap de RFCs conceptuales. Los planes de construcción del protocolo (dominios, taxonomía, discovery) están implementados; sus versiones históricas viven en `archive/`.

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
| RFC-24 | `rfc/24-skill-lifecycle-model.md` | Proposal (plan 23, 5 ago 2026) | ¿Qué es una skill integrada y qué destino tienen las skills sin consumidor (cable-or-kill)? |
| RFC-25 | `rfc/25-single-source-required-sections.md` | Proposal (plan 24, 5 ago 2026) | ¿De dónde debe resolver el runner las `required_sections` para que no existan copias desincronizables? |
| RFC-26 | `rfc/26-task-profile-model.md` | Proposal (plan 25, 5 ago 2026) | ¿Cómo se clasifica una tarea por peso (trivial/standard/complex) y qué subconjunto del ciclo obliga cada perfil? |
| RFC-27 | `rfc/27-hook-enforcement-model.md` | Proposal (plan 26, 5 ago 2026) | ¿Cómo pasa el enforcement de voluntario (prompt) a obligatorio (estado persistido + hooks bloqueantes)? |
| RFC-28 | `rfc/28-harness-coverage-closure-model.md` | Proposal (plan 27, 5 ago 2026) | ¿Cómo se declara el nivel de enforcement de cada contrato y qué validación semántica mecánica mínima gana el harness? |

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
| `24-single-source-required-sections.md` | Proposed | — | El runner resuelve `required_sections` del contrato por referencia; se elimina la copia TOML en 15 policies y `sync_required_sections.py` (RFC-25). |
| `25-task-profile-model.md` | Proposed | recomienda 24 | Perfiles `trivial`/`standard`/`complex` con bifurcación de artefactos y gates; meta: tarea trivial ≤ 5 archivos, ≤ 3 gates (RFC-26). |
| `26-hook-enforcement.md` | Proposed | recomienda 25 | `state.json` escrito solo por el runner + hooks bloqueantes `PreToolUse`/`Stop` compartidos entre CLIs, con defensa en capas (RFC-27). |
| `27-harness-coverage-closure.md` | Proposed | 24 | Declaración `enforcement` en los 25 contratos + checks semánticos mecánicos (citas existentes, evidencia de tests) en el runner (RFC-28). |

Nota de status: los planes 23–27 usan `Proposed` como estado previo al ciclo vigente (el ciclo de planes definido en §Convenciones no contempla borradores; al aprobarse pasan a `Aprobado para ejecución` o `Aprobado para redacción` según entregable).

## Backlog evidenciado - plan 19

(5 ago 2026.)

Ítems derivados del dogfooding end-to-end (sesión `.project/d4ab6a93-8e75-4880-baf3-676fce992936/`). Priorización por frecuencia × costo observado, no por intuición; evidencia por ítem en `19-anexo-a-bitacora-fricciones.md` (IDs F-xx). No son planes redactados: son entradas priorizadas de las cuales se redactan planes al tomarlas.

| # | Ítem | Destino | Prioridad | Evidencia |
|---|---|---|---|---|
| B-1 | Gate D01 superable: especial-casing del runner para `KB_DISCOVERY_ENTRY.md` fuera de la iteración, o artefacto de sesión definido por el workflow de discovery | policy | Alta — se repite en cada discovery; hoy exige artefacto-puente | F-11 |
| B-2 | Recovery económico para fallos de formato: variable/rama `RETRY_WORKER` en árboles (H01 primero), alineación contrato↔validador EARS (bullets canónicos) | policy | Alta — un fallo de formato cuesta una fase RECOVERY completa | F-01, F-02 |
| B-3 | Marcador `.last_discovery` único y canónico (ruta `.project/.last_discovery`, JSON de spec) + validación en health-check | policy | Media — dispara full discoveries evitables | F-12 |
| B-4 | Tanda de inconsistencias de contratos/policies: `discovery_context_budget` en features.toml, campos legacy en DISCOVERY_MANIFEST, "primera línea" de EXECUTIVE_SUMMARY, procedencia "observado por scan" en KB_DISCOVERY_ENTRY, delimitador de front matter, actor único de hash calculation, INTENT_REFLECTION auto-confirmada en la máquina de estados, mandato de KB en delegaciones condicionado a disponibilidad, namespacing de `<order>` por dominio | policy | Media — costo unitario bajo, recurrente | F-04, F-07, F-13, F-14, F-15, F-17, F-18, F-19, F-20 |
| B-5 | Política de clarificación desatendida/asíncrona (defaults declarados + confirmación diferida) para sesiones sin usuario en línea | gap → plan nuevo | Media — toda ejecución automatizada choca con esto | F-05 |
| B-6 | Subcomandos del runner para H15 (`validate-delegation`, `validate-return`) | gap → plan nuevo (acotado) | Media — hoy requiere importar el módulo a mano | F-08 |
| B-7 | Enmiendas conceptuales: RFC-18 (recovery→fases tempranas en la máquina de estados), RFC-20 (candidatura de tareas de tooling/CLI), clasificación `project_shape` para repos documentales/de protocolo | modelo → enmienda RFC | Baja — no bloquean; mejoran fidelidad | F-03, F-06, F-16 |
| B-8 | Modelo de ejecución de delegaciones en runtimes de contexto único + distinción "flag no aplica" vs "obligación ignorada" en métricas | gap → estudio/plan | Baja — dato registrado, sin costo observado | F-09, Anexo B §Métricas |

Descartados como ruido (con justificación en el anexo A): F-10 (deriva de reloj autor-reportado), F-21 (merge de KB legada funcionó según diseño).

## Documentos de soporte

| Archivo | Estado | Rol |
|---|---|---|
| `skills-mechanism.md` | implementada | Diseño del mecanismo de skills (SKILL.md + references/); base de RFC-00XX e input de RFC-00YM. |
| `analisis-explicitud.md` | vigente | Catálogo de gaps de explicitud (1–9) con evidencia; referencia canónica de los planes 08–14. |
| `01-execution-context-model.md` | Executed | Cambios documentales de RFC-00XY en `.agents/` (trazabilidad). |
| `02-execution-context-assembly-process.md` | Executed | Cambios documentales de RFC-00XZ (trazabilidad). |
| `03-context-budget-model.md` | Executed | Cambios documentales de RFC-00YA (trazabilidad). |

## Future Extensions sin nivel asignado

Anunciadas en RFCs aprobadas pero fuera del roadmap actual (decidir destino):

- Budget Estimation Model y Adaptive Prioritization Model (RFC-00YB).
- Budget Resource Model y Adaptive Budget Model (RFC-00YA).

## Convenciones

- **Verificación**: `python .agents/harness/runner.py health-check` + `python -m pytest .agents/harness/tests/`.
- **Inmutabilidad**: `.agents/` solo se modifica con acuerdo explícito; una RFC `Accepted` constituye ese acuerdo para sus afectados declarados. Una RFC en `Proposal` NO habilita tocar `.agents/`.
- **Ciclo de status (RFCs)**: `Proposal` (borrador) → `Accepted` (aprobada) → `Superseded` (reemplazada; el header indica por cuál RFC). No existe `Approved`: los documentos que lo usaban se normalizaron a `Accepted` (2 ago 2026).
- **Ciclo de status (planes)**: `Aprobado para redacción` (entregables documentales: RFCs, estándares), `Aprobado para ejecución` (entregables de implementación o cambios en el repo), `Executed` (todos los criterios de salida verificados; si alguno quedó incumplido: `Executed (parcial: <qué falta>)`), `Superseded` (reemplazado; indicar por qué plan). Todo plan con dependencias abiertas declara su **criterio de entrada verificable** (qué archivos/estados deben existir antes de ejecutarlo).
- **Citas verificables**: toda afirmación sobre el estado actual del repo ("hoy X") se ancla a `ruta:sección` (encabezado Markdown) existente al momento de la redacción. Prohibidos: rangos aproximados (p. ej. "H01–H13"), ordinales ("5ª responsabilidad"), números de línea absolutos sobre archivos mutables, y referencias a documentos inexistentes. Criterio de aceptación de todo documento nuevo en `plans/`: cada referencia resuelve contra el repo.
- **Amendment log**: toda RFC lleva una sección `## Amendment Log` (fecha → qué cambió → origen). Cuando una RFC posterior desfasa a una anterior, la anterior recibe además un banner bajo el header: `> ⚠ Enmienda pendiente: <qué cambió y dónde está el modelo vigente>`. Este log es el único registro de "qué decía antes" para documentos sin historia previa.
- **Verificación contra el repo**: este INDEX es un índice descriptivo, no una fuente de verdad. Todo plan nuevo verifica sus premisas contra `.agents/` y git como paso 0, nunca contra este INDEX.
- **Catálogo de gaps**: los "gaps de explicitud" referenciados por los planes 08–14 están definidos en `plans/analisis-explicitud.md`. Se cita el catálogo por ruta; ningún documento referencia IDs de gap que no existan allí.
- **Numeración de archivos**: hay dos secuencias independientes y cada una es única dentro de su espacio:
  - `plans/rfc/`: solo RFCs, numeración incremental (`00`–`15` existentes — los `07`–`15` reservados por el roadmap EC ya fueron asignados a RFC-00YE…00YM; los RFCs fuera del roadmap EC numeran a partir de `16`). Un implementation plan nunca vive aquí.
  - `plans/` (raíz): solo planes de ejecución, numerados por **orden cronológico de ejecución** — esa es la prioridad ante cualquier conflicto. `01`–`03` son los implementation plans de los RFCs base (ejecutados 25–26 jul); `04`–`07` primera serie (Execution Context); `08`–`14` segunda serie (explicitud de decisiones); `15`–`20` tercera serie (protocolo operativo), mapeada el 28 jul.
  - Los identificadores internos de la serie (RFC-00XX … RFC-00YM) se mantienen como IDs conceptuales dentro de los documentos; el número de archivo es solo orden físico.
- **Versionado**: `plans/` completo está versionado en git (política adoptada el 2 ago 2026; antes figuraba como ignorado pese a estar trackeado de facto, y hubo una pérdida y restauración). Los planes ejecutados se conservan como traza histórica: no se borran; si quedan desfasados se marcan `Superseded`. Lo efímero del proyecto son los artefactos de sesión (`.project/`), no los documentos de diseño. `plans/archive/` fue eliminado del working tree; su contenido sigue disponible en la historia de git.
- **Frontera documental**: `.agents/` (versionado, permanente) no referencia `plans/` ni RFCs. Los conceptos que `.agents/` necesita se definen inline, de forma autocontenida. Ningún plan debe instruir referencias `.agents/` → `plans/`; la instrucción correcta es siempre "definir el concepto inline, sin mencionar la RFC".

## Archivo

Nota (2 ago 2026): `plans/archive/` fue eliminado del working tree; estos archivos viven en la historia de git (`git show HEAD:plans/archive/<archivo>`).

| Archivo | Contenido |
|---|---|
| `archive/PLAN_*_v1.md` | Planes de construcción del protocolo (dominios, taxonomía, discovery) sobre estructura plana; reemplazados e implementados. |
| `archive/PLAN_05_CONTEXT_ENGINEERING.md` | Refactor de `.agents/standards/context/CONTEXT.md` (tags, presupuestos). Ejecutado (18 jul). |
| `archive/PLAN_06_PERFILES_WORKER.md` | Perfiles en `.agents/roles/profiles/` + campo `profile` del contrato de delegación. Ejecutado (18 jul). |
| `archive/PLAN_07_ARTEFACTOS_CONTEXTO.md` | Estándar `.agents/standards/context/PROJECT_ARTIFACTS.md`. Ejecutado (18 jul). |
| `archive/PLAN_08_PLANTILLAS_PROYECTO.md` | Plantillas de adopción en `templates/`. Descartado (28 jul): fuentes de `example/` ya no existen, solapa con las plantillas de `PROJECT_ARTIFACTS.md` §9 y su plantilla de IDE era específica de Claude. Idea rescatable: plantillas de dominio como anexo de `PROJECT_ARTIFACTS.md`. |

## Documento de visión (fuera de `plans/`)

`feature.md` vive en la raíz del repositorio: es el documento de visión del Execution Context Pipeline — ni un plan de ejecución ni un RFC. Todos los planes `04`–`07` y los RFCs lo referencian. Está versionado en git (la nota anterior que lo declaraba untracked estaba desfasada; verificado 2 ago 2026).
