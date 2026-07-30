---
title: "Plan maestro — Discovery Orchestrator (arquitectura descompuesta + KB acumulativo)"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
replaces: "plans/PLAN_HYBRID_DISCOVERY.md"
---

# Plan de implementación: Discovery Orchestrator

**Responsable:** Orchestrator principal + Discovery Orchestrator  
**Tipo:** subsistema de descubrimiento con máquina de estados propia y workers especializados  
**Prioridad recomendada:** implementar primero.

## Objetivo

Construir un **subsistema de discovery autónomo** dentro del protocolo ARgentOS, compuesto por un Discovery Orchestrator, workers especializados y un **KB acumulativo**. El sistema debe descubrir:

1. **El entorno de ejecución** (SO, shell, herramientas, runtime).
2. **El stack tecnológico** del proyecto (lenguajes, frameworks, dependencias, contenedores, bases de datos).
3. **La arquitectura y configuración** del proyecto.
4. **Los patrones de desarrollo** del equipo (estilo, convenciones, hábitos).
5. **Las reglas de negocio, flujos, deuda técnica y errores conocidos**.

Además, el subsistema debe **consumir y enriquecer** el conocimiento generado en sesiones previas, en lugar de regenerar todo desde cero en cada invocación.

Paralelamente, **deprecar y eliminar el extractor Python** de `.agents/harness/project_discovery/`.

## Principios rectores

> **`.agents/` son instrucciones. El agente es el executor. El harness es el guardián.**

> **Determinismo por contrato, no por código.**

> **El knowledge base es una memoria del proyecto, no un snapshot descartable.**

## Arquitectura general

```text
┌─────────────────────────────────────────────────────────────┐
│                  Orchestrator principal                     │
│  (TASK_RECEIVED → ... → EXECUTING → VERIFYING → COMPLETED)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ invoca con scope
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Discovery Orchestrator                      │
│  Máquina de estados propia + workers especializados          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ environment_    │ │ stack_worker    │ │ patterns_       │
    │ worker          │ │                 │ │ worker          │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ framework_worker│ │ business_worker │ │ synthesis_      │
    │                 │ │                 │ │ worker          │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              .project/knowledge/discovery/                  │
│  KB acumulativo: stack, env, patterns, architecture,         │
│  business_rules, project_flow, technical_debt,                 │
│  known_errors, summary, .discovery_manifest                  │
└─────────────────────────────────────────────────────────────┘
```

## Máquina de estados del Discovery Orchestrator

El Discovery Orchestrator no reutiliza el state machine de tareas de ARgentOS. Tiene estados propios, orientados a fases de descubrimiento.

```text
DISCOVERY_INIT
    │
    ▼
DISCOVERY_ENV
    │
    ▼
DISCOVERY_STACK
    │
    ▼
DISCOVERY_FRAMEWORK
    │
    ▼
DISCOVERY_PATTERNS
    │
    ▼
DISCOVERY_BUSINESS
    │
    ▼
DISCOVERY_MERGE
    │
    ▼
DISCOVERY_VALIDATE
    │
    ▼
DISCOVERY_READY
```

### Estados

| Estado | Descripción | Worker asociado | Output |
|--------|-------------|-----------------|--------|
| `DISCOVERY_INIT` | Leer KB previo, artefactos de sesión, calcular hashes, preparar input. | `init_worker` | input estructurado para los workers |
| `DISCOVERY_ENV` | Detectar entorno de ejecución. | `environment_worker` | `environment.md` |
| `DISCOVERY_STACK` | Detectar lenguajes, dependencias, contenedores, bases de datos. | `stack_worker` | `stack.md`, `dependencies.md`, `containers.md`, `database.md` |
| `DISCOVERY_FRAMEWORK` | Detectar framework, arquitectura, configuración. | `framework_worker` | `architecture.md`, `configuration.md` |
| `DISCOVERY_PATTERNS` | Detectar patrones de código y estilo. | `patterns_worker` | `development_patterns.md` |
| `DISCOVERY_BUSINESS` | Detectar reglas de negocio, flujos, deuda técnica, errores. | `business_worker` | `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md` |
| `DISCOVERY_MERGE` | Fusionar outputs parciales, resolver conflictos, enriquecer con sesiones. | `synthesis_worker` | `summary.md`, `.discovery_manifest` + entradas KB actualizadas |
| `DISCOVERY_VALIDATE` | Validar estructura y ground truth. | harness (H10/H12) | `HARNESS_REPORT.md` |
| `DISCOVERY_READY` | KB actualizado y válido. | — | — |
| `DISCOVERY_FAILED` | Falló el proceso; reporta al Orchestrator principal. | — | `RECOVERY_REPORT.md` opcional |

### Transiciones permitidas

- `DISCOVERY_INIT` → `DISCOVERY_ENV`, `DISCOVERY_STACK`, `DISCOVERY_PATTERNS`, `DISCOVERY_BUSINESS` (paralelo).
- `DISCOVERY_STACK` → `DISCOVERY_FRAMEWORK` (dependencia).
- `DISCOVERY_ENV`, `DISCOVERY_FRAMEWORK`, `DISCOVERY_PATTERNS`, `DISCOVERY_BUSINESS` → `DISCOVERY_MERGE`.
- `DISCOVERY_MERGE` → `DISCOVERY_VALIDATE`.
- `DISCOVERY_VALIDATE` → `DISCOVERY_READY` o `DISCOVERY_FAILED`.
- Cualquier estado → `DISCOVERY_FAILED` ante fallo no recuperable.

## Workers especializados

| Worker | Responsabilidad | Input | Output |
|--------|-----------------|-------|--------|
| `init_worker` | Preparar el contexto del discovery: leer KB previo, artefactos de sesión, calcular hashes, determinar scope. | `project_root`, `scope`, `previous_kb`, `session_artifacts` | `discovery_input.json` + `invalidation_report.json` |
| `environment_worker` | Detectar el entorno de ejecución. | `discovery_input.json` | `environment.md` |
| `stack_worker` | Detectar stack tecnológico y dependencias. | `discovery_input.json` | `stack.md`, `dependencies.md`, `containers.md`, `database.md` |
| `framework_worker` | Detectar framework, arquitectura y configuración. | output de `stack_worker` + archivos de config | `architecture.md`, `configuration.md` |
| `patterns_worker` | Detectar patrones de código y estilo. | muestra de código + guías de estilo | `development_patterns.md` |
| `business_worker` | Detectar reglas de negocio, flujos, deuda técnica, errores. | README + código de servicios + tests | `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md` |
| `synthesis_worker` | Fusionar outputs parciales, resolver conflictos, enriquecer con sesiones, escribir manifest. | todos los outputs parciales + KB previo + artefactos de sesión | `summary.md`, `.discovery_manifest` + entradas KB consolidadas |

### Dependencias entre workers

```text
environment_worker ──────┐
stack_worker ───┬─────────┼───┐
                │         │   │
                ▼         │   │
         framework_worker  │   │
                │          │   │
                ▼          ▼   ▼
            DISCOVERY_MERGE (synthesis_worker)
```

`environment_worker`, `stack_worker`, `patterns_worker` y `business_worker` pueden ejecutarse en paralelo. `framework_worker` depende de `stack_worker`. `synthesis_worker` depende de todos.

## KB acumulativo

El KB no se regenera completo en cada invocación. Se comporta como una **memoria de proyecto**:

1. **Lectura:** en `DISCOVERY_INIT` se lee el KB previo y los artefactos de sesión.
2. **Invalidación selectiva:** si un hash de configuración cambió, se invalidan las entradas afectadas.
3. **Actualización parcial:** cada worker actualiza solo las entradas que le corresponden.
4. **Fusión:** el `synthesis_worker` resuelve conflictos entre KB previo y nuevos hallazgos.
5. **Versionado:** cada entrada lleva `generated_at` y `updated_at`; se puede rastrear qué cambió y por qué worker.
6. **Procedencia:** cada entrada registra `source_workers` y `source_sessions`.

### Fuentes de enriquecimiento por sesiones

| Artefacto de sesión | Qué aporta |
|---------------------|------------|
| `SESSION_LOG.md` | Historia de estados y decisiones. |
| `CONTEXT_ARTIFACT.md` | Contexto ya recolectado sobre el proyecto. |
| `EXECUTION_SUMMARY.md` | Cambios realizados, comandos ejecutados, decisiones tomadas. |
| `RECOVERY_REPORT.md` | Problemas encontrados, deuda técnica emergente. |
| `VERIFICATION_REPORT.md` | Validaciones realizadas, comportamientos observados. |

### Reglas de fusión

- Si un hallazgo nuevo contradice uno previo:
  - Si el nuevo tiene `confidence: high` y el previo `confidence: low`, reemplazar.
  - Si ambos tienen `confidence: high`, reportar conflicto en `summary.md` y `## Notes` de la entrada.
  - Si el previo proviene de una sesión reciente, mantener el previo y marcar el nuevo como `confidence: low`.
- Nunca eliminar una entrada sin dejar traza en el manifest.
- Las entradas invalidadas se marcan con `status: stale` en el manifest, no se borran del historial.

## Integración con el Orchestrator principal

El Orchestrator principal no conoce los detalles internos del Discovery Orchestrator. Solo:

1. **Detecta la necesidad de KB:**
   - No existe `.project/knowledge/discovery/`.
   - El KB está stale según TTL.
   - Cambió el hash de configuración.
   - Un worker de ejecución reporta inconsistencia.
   - El usuario solicita refresh.

2. **Invoca al Discovery Orchestrator** con un `scope`:
   - `full`: ejecutar todo el pipeline.
   - `env`: solo `environment_worker`.
   - `stack`: solo `stack_worker` + `framework_worker`.
   - `patterns`: solo `patterns_worker`.
   - `business`: solo `business_worker`.

3. **Recibe el resultado:** `DISCOVERY_READY` o `DISCOVERY_FAILED`.

4. **Usa el KB** en los workers de ejecución, mediante referencias a `environment.md` y `development_patterns.md`.

## Contratos entre workers

Cada worker produce un artefacto intermedio con metadatos de procedencia. El `synthesis_worker` consume estos artefactos y genera el KB final. Ver contrato completo en Plan 01.

## Contratos de KB

Cada entrada KB debe extender el contrato base con campos de procedencia: `updated_at`, `source_workers`, `source_sessions`, `status`. Ver contrato completo en Plan 01.

## Harness de validación

### H10: KB Discovery Report (estructural)

- Verificar que todas las entradas KB existan y cumplan el contrato.
- Verificar que los headers TOML sean válidos.
- Verificar que los campos obligatorios estén presentes.
- Verificar que cada patrón tenga `source_files`, `confidence` y `example`.
- Verificar que el manifest esté completo.

### H12: Discovery Output Validation (ground truth)

- Verificar que `source_files` sean rutas reales del proyecto (o `system_probe` para entorno).
- Verificar que el stack detectado provenga de archivos de configuración reales.
- Verificar que los patrones de código tengan ejemplos verificables en sus `source_files`.
- Verificar que `environment.md` no contenga secrets.
- Verificar que no haya afirmaciones sin fuente.
- Verificar que la fusión del KB no haya introducido conflictos sin resolver.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Complejidad del sistema | Documentar claramente estados, workers y contratos; empezar con un pipeline secuencial y luego paralelizar. |
| Costo elevado por múltiples workers | Cada worker es más pequeño; se pueden limitar tokens por worker; se cachean entradas individuales. |
| Coordinación entre workers | Definir contratos de mensajes y directorio de trabajo intermedio; usar el `synthesis_worker` como punto de fusión único. |
| Conflicto en la fusión de KB | Reglas de fusión explícitas basadas en `confidence`, `updated_at` y `source_sessions`. |
| El Orchestrator principal no detecta stale KB | TTL y hashes calculados por el Orchestrator principal; invalidación selectiva. |
| Workers ignoran entorno y patrones | Incluir referencias al KB en el payload de los workers de ejecución (Plan 05). |

## Roadmap de implementación

El plan maestro se desglosa en 5 sub-planes:

| Plan | Foco | Archivos principales |
|------|------|----------------------|
| [PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md](PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md) | Contratos de KB, contratos entre workers, H10. | `.agents/contracts/DISCOVERY_MANIFEST.md`, `.agents/contracts/DEVELOPMENT_PATTERNS.md`, `.agents/contracts/ENVIRONMENT_DISCOVERY.md`, `.agents/contracts/INTER_WORKER_MESSAGE.md`, `.agents/harness/policies/H10-kb-discovery-report.md` |
| [PLAN_DISCOVERY_ORCHESTRATOR_02_EXECUTION.md](PLAN_DISCOVERY_ORCHESTRATOR_02_EXECUTION.md) | Discovery Orchestrator, workers especializados, pipeline de ejecución. | `.agents/roles/discovery_orchestrator.md`, `.agents/roles/discovery_workers/*.md`, `.agents/features.toml` |
| [PLAN_DISCOVERY_ORCHESTRATOR_03_ENVIRONMENT.md](PLAN_DISCOVERY_ORCHESTRATOR_03_ENVIRONMENT.md) | `environment_worker`: comandos, seguridad, shell. | `.agents/roles/discovery_workers/environment_worker.md`, `.agents/standards/context/ENVIRONMENT_PROBE.md` |
| [PLAN_DISCOVERY_ORCHESTRATOR_04_ORCHESTRATION.md](PLAN_DISCOVERY_ORCHESTRATOR_04_ORCHESTRATION.md) | Integración con Orchestrator principal, state machine del Discovery Orchestrator, TTL, cache. | `.agents/workflow/09-discovery.md`, `.agents/roles/orchestrator.md`, `.agents/states/DISCOVERY_STATE_MACHINE.md` |
| [PLAN_DISCOVERY_ORCHESTRATOR_05_VALIDATION.md](PLAN_DISCOVERY_ORCHESTRATOR_05_VALIDATION.md) | H12, métricas, rollback, riesgo, integración en workers de ejecución. | `.agents/harness/policies/H12-discovery-output.md`, `.agents/harness/health_check.py`, `.agents/standards/context/USING_PATTERNS.md`, `.agents/roles/worker.md`, `.agents/workflow/06-execute.md` |

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | `plans/PLAN_DISCOVERY_ORCHESTRATOR.md` existe y define la arquitectura de dos orquestadores. | Leer el plan. |
| 2 | El Discovery Orchestrator tiene al menos 6 workers definidos. | Revisar Plan 02. |
| 3 | El KB acumulativo soporta `updated_at`, `source_workers` y `source_sessions`. | Revisar Plan 01. |
| 4 | El Discovery Orchestrator tiene una máquina de estados propia. | Revisar Plan 04. |
| 5 | El extractor Python de `.agents/harness/project_discovery/` fue eliminado. | El directorio no existe. |
| 6 | H10 valida estructura y H12 valida ground truth. | Revisar Plan 05. |
| 7 | El KB consume artefactos de sesión previos. | Revisar Plan 02. |
| 8 | El Orchestrator principal puede invocar discovery con scopes. | Revisar Plan 04. |
| 9 | El health-check pasa sin importar `project_discovery`. | Ejecutar `python .agents/harness/health_check.py`. |
| 10 | El plan maestro anterior está archivado o redireccionado. | `ls plans/archive/PLAN_HYBRID_DISCOVERY_v1.md` o redirección en el plan anterior. |


