---
title: "Plan de implementación — Sistema de taxonomía y metadatos de protocolo"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: []
---

# Plan de implementación: Sistema de taxonomía y metadatos de protocolo

## Objetivo

Crear un sistema centralizado de metadatos que homogenice los nombres de estados, artefactos, workflows, harness policies, roles y workers del protocolo ARgentOS. Este sistema permitirá que cualquier agente sepa, en cada momento, qué estado está ejecutando, de dónde viene, hacia dónde va, qué artefactos consume y produce, qué actor lo ejecuta y qué perfil tiene asociado.

## Alcance

- Crear `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, el diccionario maestro del protocolo.
- Definir un bloque de metadatos estándar para cada tipo de archivo: state machine, workflow, harness policy, contract, role, worker.
- Agregar metadatos a los archivos existentes del protocolo.
- Crear un harness de validación que verifique coherencia entre la taxonomía y los archivos.
- No modificar la lógica funcional del protocolo; solo agregar metadatos y validación.
- No renombrar archivos en este paso (eso pertenece al plan de naming convention separado).

## Justificación

Actualmente el protocolo tiene estados, artefactos, workflows y harness policies bien definidos, pero no hay un único lugar de verdad que relacione todos estos elementos. El agente debe inferir relaciones por convenciones de nombres, lo que es frágil. Un sistema de taxonomía centralizado permite:

1. Saber, para cualquier estado, cuáles son sus estados previos y próximos.
2. Saber, para cualquier artefacto, quién lo produce y quién lo consume.
3. Saber, para cualquier archivo, si es un estado, un workflow, un harness, un role o un worker.
4. Validar automáticamente que el protocolo sea coherente.
5. Facilitar la evolución del protocolo: al cambiar un nombre, se sabe qué archivos se ven afectados.

## Estructura de `PROTOCOL_TAXONOMY.md`

El archivo será YAML estructurado con tres secciones principales:

### 1. `lifecycles`

Define los grupos de estados:

- `system`
- `task`
- `context`
- `planning`
- `execution`
- `final`
- `exception`
- `discovery`

### 2. `entities`

Cada estado, artefacto, harness, workflow, actor y worker es una entidad con metadatos:

| Campo | Descripción |
|-------|-------------|
| `kind` | Tipo de entidad: `state`, `artifact`, `workflow`, `harness`, `actor`, `role`, `worker`, `contract`. |
| `lifecycle` | Lifecycle al que pertenece. |
| `name` | Nombre legible. |
| `description` | Descripción. |
| `previous` | Estados previos permitidos. |
| `next` | Próximos estados permitidos. |
| `artifacts_input` | Artefactos que consume. |
| `artifacts_output` | Artefactos que produce. |
| `workflow` | Workflow asociado. |
| `harness` | Harness que valida la transición. |
| `actor` | Actor que ejecuta este estado. |
| `profile` | Worker asociado (si aplica). |
| `produced_by` | Estados que producen el artefacto. |
| `consumed_by` | Estados que consumen el artefacto. |
| `policy_file` | Ruta del archivo de harness (solo para harness). |

### 3. `tags`

Taxonomía de tags para clasificar entidades:

- `lifecycle`: system, task, context, planning, execution, final, exception, discovery.
- `artifact`: analysis, reflection, specification, context, validation_report, plan, summary, report, log, brief, knowledge.
- `harness`: task, context, planning, execution, verification, recovery, discovery, system.
- `kind`: state, artifact, workflow, harness, actor, role, worker, contract.

## Bloque de metadatos por tipo de archivo

Cada archivo relevante debe incluir un bloque YAML al principio con al menos `taxonomy` y `kind`. Además, según el tipo:

### State machine

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
actor: orchestrator
states_defined:
  - TASK_RECEIVED
  - ANALYZING_TASK
  - ...
---
```

### Workflow

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
state: ANALYZING_TASK
lifecycle: task
previous_states: [TASK_RECEIVED]
next_states: [BUILDING_TASK_SPECIFICATION, CONFIRMING_INTENT, NEEDS_CLARIFICATION]
input_artifacts: []
output_artifacts: [TASK_ANALYSIS.md]
harness: [H00-task-analysis]
actor: orchestrator
profile: null
---
```

### Harness policy

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
harness_id: H00
name: task-analysis
state: ANALYZING_TASK
lifecycle: task
gates:
  - ANALYZING_TASK -> BUILDING_TASK_SPECIFICATION
  - ANALYZING_TASK -> CONFIRMING_INTENT
  - ANALYZING_TASK -> NEEDS_CLARIFICATION
artifact_validated: TASK_ANALYSIS.md
---
```

### Contract

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
artifact: TASK_ANALYSIS.md
lifecycle: task
produced_by: [ANALYZING_TASK]
consumed_by: [BUILDING_TASK_SPECIFICATION, CONFIRMING_INTENT]
---
```

### Role

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: role
role_id: orchestrator
actor: orchestrator
states: [TASK_RECEIVED, ANALYZING_TASK, ...]
---
```

### Worker

```yaml
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
worker_id: environment_worker
subsystem: discovery
state: DISCOVERY_ENV
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [discovery_input.json]
output_artifacts: [environment.md]
---
```

## Entidades a definir

### Estados principales

`SYSTEM_READY`, `TASK_RECEIVED`, `ANALYZING_TASK`, `CONFIRMING_INTENT`, `BUILDING_TASK_SPECIFICATION`, `NEEDS_CLARIFICATION`, `TASK_READY`, `GATHERING_CONTEXT`, `CONTEXT_GATHERED`, `VALIDATING_CONTEXT`, `CONTEXT_READY`, `PLANNING`, `PLAN_READY`, `EXECUTING`, `VERIFYING`, `RECOVERY`, `COMPLETED`, `ABORT`.

### Estados de discovery

`DISCOVERY_INIT`, `DISCOVERY_ENV`, `DISCOVERY_STACK`, `DISCOVERY_FRAMEWORK`, `DISCOVERY_PATTERNS`, `DISCOVERY_BUSINESS`, `DISCOVERY_MERGE`, `DISCOVERY_VALIDATE`, `DISCOVERY_READY`, `DISCOVERY_FAILED`.

### Artefactos principales

`TASK_ANALYSIS.md`, `INTENT_REFLECTION.md`, `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`, `CONTEXT_VALIDATION_REPORT.md`, `EXECUTION_PLAN.md`, `EXECUTION_SUMMARY.md`, `VERIFICATION_REPORT.md`, `RECOVERY_REPORT.md`, `SESSION_LOG.md`, `SESSION_BRIEF.md`, `KB_DISCOVERY_REPORT.md`, `KB_DISCOVERY_ENTRY.md`, `KNOWLEDGE_INDEX.md`, `PROJECT_README.md`, `REVIEW_REPORT.md`.

### Harness policies

`H00-task-analysis`, `H11-intent-reflection`, `H01-task-specification`, `H02-context-artifact`, `H03-context-validation`, `H04-execution-plan`, `H05-execution-completed`, `H06-verification-report`, `H07-scope-compliance`, `H09-recovery-report`, `H10-kb-discovery-report`, `H12-discovery-output`, `H13-protocol-taxonomy`.

### Actors

`system_agent`, `orchestrator`, `discovery_orchestrator`.

### Workers

`init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `patterns_worker`, `business_worker`, `synthesis_worker`.

## Archivos a crear

1. `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — diccionario maestro.
2. `.agents/harness/policies/H13-protocol-taxonomy.md` — harness que valida coherencia.
3. `.agents/harness/tests/test_protocol_taxonomy.py` — tests para el harness.
4. `plans/PLAN_PROTOCOL_TAXONOMY.md` — este plan.

## Archivos a modificar

### State machines

- `.agents/states/AGENT_STATE_MACHINE.md` — agregar bloque de metadatos.
- `.agents/states/DISCOVERY_STATE_MACHINE.md` — agregar bloque de metadatos.

### Workflows

- `.agents/workflow/00-analyze-task.md` → `state: ANALYZING_TASK`.
- `.agents/workflow/01-confirm-intent.md` → `state: CONFIRMING_INTENT`.
- `.agents/workflow/02-build-task-specification.md` → `state: BUILDING_TASK_SPECIFICATION`.
- `.agents/workflow/03-gather-context.md` → `state: GATHERING_CONTEXT`.
- `.agents/workflow/04-validate-context.md` → `state: VALIDATING_CONTEXT`.
- `.agents/workflow/05-plan.md` → `state: PLANNING`.
- `.agents/workflow/06-execute.md` → `state: EXECUTING`.
- `.agents/workflow/07-verify.md` → `state: VERIFYING`.
- `.agents/workflow/08-recovery.md` → `state: RECOVERY`.
- `.agents/workflow/09-discovery.md` → `state: DISCOVERY_INIT` + estados de discovery.

### Harness policies

Todas las policies existentes (H00-H12) deben agregar metadatos.

### Contracts

Todos los contratos existentes deben agregar metadatos.

### Roles

- `.agents/roles/orchestrator.md`
- `.agents/roles/worker.md`
- `.agents/roles/discovery_orchestrator.md` (del Plan 02)
- `.agents/roles/discovery_workers/*.md` (del Plan 02)

### Documentación

- `.agents/standards/runtime/INDEX.md` — documentar el sistema de taxonomía.
- `AGENTS.md` — actualizar referencias si es necesario.

## Fases de implementación

### Fase 1: Diseñar el schema

1. Definir la estructura YAML de `PROTOCOL_TAXONOMY.md`.
2. Definir el bloque de metadatos para cada tipo de archivo.
3. Validar que el schema pueda responder: estado previo, próximo estado, actor, perfil, artefactos, harness.

### Fase 2: Crear el diccionario maestro

1. Escribir `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` con todas las entidades actuales.
2. Incluir estados principales, estados de discovery, artefactos, harness, actors, roles y workers.
3. Mapear relaciones entre entidades.

### Fase 3: Crear el harness de validación

1. Escribir `.agents/harness/policies/H13-protocol-taxonomy.md`.
2. Definir reglas:
   - Todo workflow debe referenciar un `state` válido en la taxonomía.
   - Todo harness debe referenciar transiciones permitidas en la taxonomía.
   - Todo artefacto debe tener `produced_by` y `consumed_by` válidos.
   - Todo worker debe referenciar un `state` y un `actor` válidos.
   - No puede haber estados huérfanos (sin workflow o sin transición).
3. Escribir `.agents/harness/tests/test_protocol_taxonomy.py`.

### Fase 4: Agregar metadatos a archivos críticos

1. Agregar metadatos a `.agents/states/AGENT_STATE_MACHINE.md`.
2. Agregar metadatos a `.agents/states/DISCOVERY_STATE_MACHINE.md`.
3. Agregar metadatos a `.agents/roles/orchestrator.md`, `.agents/roles/worker.md`, `.agents/roles/discovery_orchestrator.md`, `.agents/roles/discovery_workers/*.md`.
4. Agregar metadatos a `.agents/harness/policies/H10-kb-discovery-report.md` y `.agents/harness/policies/H12-discovery-output.md`.

### Fase 5: Agregar metadatos a workflows y contratos existentes

1. Agregar metadatos a workflows 00-09.
2. Agregar metadatos a contratos existentes.
3. Agregar metadatos a harness policies restantes.

### Fase 6: Documentar

1. Actualizar `.agents/standards/runtime/INDEX.md`.
2. Actualizar `AGENTS.md` si es necesario.
3. Verificar que el harness H13 pase.

### Fase 7: Verificación final

1. Ejecutar `python .agents/harness/health_check.py`.
2. Ejecutar tests de taxonomía.
3. Verificar que no haya estados huérfanos.
4. Verificar que todos los archivos relevantes tengan metadatos.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | Existe `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`. | `ls` |
| 2 | El diccionario define estados, artefactos, harness, workflows, actors y workers. | Leer el archivo. |
| 3 | Cada estado tiene `previous` y `next` definidos. | Revisar entradas del YAML. |
| 4 | Cada artefacto tiene `produced_by` y `consumed_by` definidos. | Revisar entradas del YAML. |
| 5 | Existe `.agents/harness/policies/H13-protocol-taxonomy.md`. | `ls` |
| 6 | El harness H13 valida coherencia. | Ejecutar tests. |
| 7 | Los archivos críticos (state machine, orchestrator, workflows) tienen bloque de metadatos. | `grep` de `taxonomy:` y `kind:` |
| 8 | No hay estados huérfanos (sin workflow o sin transición). | Ejecutar H13. |
| 9 | El health-check sigue pasando. | `python .agents/harness/health_check.py` |
| 10 | El sistema permite responder: estado actual, previo, próximo, actor, perfil, artefactos, harness. | Revisar ejemplos en el diccionario. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| El diccionario se vuelve obsoleto | H13 lo valida; cambios deben pasar por el diccionario. |
| Archivos con metadatos incompletos | H13 rechaza archivos que no cumplan el schema. |
| Complejidad del YAML | Usar schema claro y documentado; validar con tests. |
| Duplicación de información | El diccionario es la única fuente de verdad; los archivos solo referencian. |
| Impacto en archivos existentes | Cambios no funcionales; solo agregar metadatos al inicio. |
| Mantener sincronizado con Plan 04 | El diccionario debe incluir todos los estados de discovery definidos en Plan 04. |

## Recomendación

Implementar este plan antes de ejecutar el plan de naming convention. El diccionario de taxonomía hará que el plan de renombrado sea mucho más seguro, porque se podrá saber exactamente qué archivos se ven afectados al cambiar un nombre.

## Nota sobre el scope de este plan

Este plan es de **planificación**. No modifica `.agents/` ni `.project/` en su versión documental. La implementación de este plan (crear archivos, agregar metadatos) requiere un paso de ejecución separado, preferiblemente tras la aprobación de este plan y de los planes de Discovery Orchestrator.
