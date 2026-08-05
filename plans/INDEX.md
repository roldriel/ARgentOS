# Índice de planes — ARgentOS

Estado al 2026-07-28. El trabajo activo es el **Execution Context Pipeline** (`feature.md`) y su roadmap de RFCs conceptuales. Los planes de construcción del protocolo (dominios, taxonomía, discovery) están implementados; sus versiones históricas viven en `archive/`.

## Serie de RFCs (documentos canónicos)

| RFC | Archivo | Status | Pregunta que responde |
|---|---|---|---|
| RFC-00XX | `rfc/00-skill-capability-model.md` | Accepted | ¿Qué es una Skill? (capacidad reutilizable, independiente del mecanismo) |
| RFC-00XY | `rfc/01-execution-context-model.md` | Accepted | ¿Qué es un Execution Context? |
| RFC-00XZ | `rfc/02-execution-context-assembly-process.md` | Accepted ⚠ (enmiendas 00YB/00YC pendientes — banner en el documento) | ¿Cómo se construye conceptualmente? |
| RFC-00YA | `rfc/03-context-budget-model.md` | Accepted ⚠ (alcance ampliado por 00YC — banner en el documento) | ¿Qué restricciones limitan su composición? |
| RFC-00YB | `rfc/04-context-candidate-prioritization-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué candidatos parecen más importantes? |
| RFC-00YC | `rfc/05-context-resolution-model.md` | Accepted (regularizado 2 ago 2026: ya estaba aplicado en `.agents/`) | ¿Qué conjunto consistente puede componerse? |
| RFC-16 | `rfc/16-core-skills-catalog-model.md` | Accepted | ¿Qué Skills forman el núcleo del protocolo, qué función cumple cada una y qué criterios deciden la membresía? |

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
| `04-main-pipeline-closure.md` | aprobado | — | RFC-00YD Composition + updates a RFC-00XZ y `feature.md` + regularización de status. |
| `05-resolution-specialization.md` | aprobado | RFC-00YC | RFC-00YE Conflict Classification → 00YF/00YG/00H (paralelizables). |
| `06-composition-specialization.md` | aprobado | Nivel 1 | RFC-00YI Compression, RFC-00YJ Optimization. |
| `07-materialization.md` | aprobado | Nivel 1 (+3 conceptual) | RFC-00YK Materialization → 00YL Prompt Rendering, 00YM Skill Materialization. |

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
| `08-correcciones-transversales.md` | aprobado | — | Contradicción de bootstrap + fixes stale en `.agents/` (gaps 6 y 9). |
| `09-orchestrator-decision-model.md` | aprobado | 08 | Catálogo conceptual de decisiones del Orchestrator + unificación de confianza (gaps 1 y 8). |
| `10-failure-recovery-taxonomy.md` | aprobado | 09 | Clasificación de fallos y audiencia máquina/agente de policies (gap 5). |
| `11-delegation-validity-model.md` | aprobado | 04–07 | Validez conceptual de payloads y return reports; resuelve el huérfano `context_budget: 4000` (gap 2). |
| `12-selection-models.md` | aprobado | 11, 04–07 | Modelos de candidatura/selección de perfil y skill (gap 3). |
| `13-session-iteration-lifecycle.md` | aprobado | — | Ciclo de vida de sesión, iteraciones y `<order>` (gap 4). |
| `14-declarative-flag-compliance.md` | aprobado | — | Obligación y evidencia de flags `[declarative]` (gap 7). |

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
| `15-policy-layer-1-delegation-budget.md` | aprobado | 11, 07 | Primera policy real del protocolo (H15) + materialización del Budget para el runtime prompt. |
| `16-policy-layer-2-resolution-composition.md` | aprobado | 05, 06, 15 | Policies concretas de desempate, deduplicación, merge, compresión y optimización. |
| `17-protocol-metrics-model.md` | aprobado | 09, 10 | Modelo de métricas del protocolo: registro, agregación y señales de salud. |
| `18-segunda-materializacion.md` | aprobado | 07 | Prueba de fuego de la tesis runtime-independent: materialización no-prompt del Execution Context. |
| `19-dogfooding-end-to-end.md` | aprobado | 04–14 (+15, 17) | Proyecto real ejecutado por protocolo; backlog evidenciado de la siguiente generación. |
| `20-release-adoption.md` | aprobado | 19 | Versionado, changelog, migración, onboarding y tag 1.0.0 del protocolo. |

## Cuarta serie: Core Skills Pack

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `21-core-skills-pack.md` | Executed | RFC-16 Accepted | Implementación por tandas del Core Skills Pack definido en RFC-16 (`rfc/16-core-skills-catalog-model.md`). |
| `22-skills-pack-2.md` | Executed | 21 | Segundo pack: 16 Skills complementarias seleccionadas con los criterios C1–C4 de RFC-16 entre las candidatas no excluidas. |

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
  - `plans/rfc/`: solo RFCs, numeración incremental (`00`–`05` existentes; `06`–`15` reservados por el roadmap EC — RFC-00YD…00YM; los RFCs fuera del roadmap EC numeran a partir de `16`). Un implementation plan nunca vive aquí.
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
