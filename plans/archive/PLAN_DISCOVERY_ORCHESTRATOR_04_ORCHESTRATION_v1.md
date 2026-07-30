---
title: "Plan de implementación — Discovery Orchestrator: Integración con Orchestrator principal"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: ["plans/PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_02_EXECUTION.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_03_ENVIRONMENT.md"]
---

# Plan 04: Integración con Orchestrator principal

## Objetivo

Definir cómo el Orchestrator principal invoca al Discovery Orchestrator, la máquina de estados del Discovery Orchestrator, y el protocolo de comunicación entre ambos.

## Alcance

- Crear `.agents/workflow/09-discovery.md`.
- Crear `.agents/states/DISCOVERY_STATE_MACHINE.md`.
- Actualizar `.agents/roles/orchestrator.md`.
- Definir TTL, cache, scopes y condiciones de invocación.
- No implementar workers ni contratos en este paso.

## Relación entre orquestadores

```text
Orchestrator principal
    │
    │ invoca con scope
    ▼
Discovery Orchestrator
    │
    ├─ coordina workers
    ├─ máquina de estados propia
    └─ valida con H10/H12
    │
    ▼
DISCOVERY_READY / DISCOVERY_FAILED
    │
    ▼ (devuelve control al Orchestrator principal)
Orchestrator principal
    │
    ├─ CONTINÚA la tarea (PLANNING → EXECUTING → VERIFYING → COMPLETED)
    ├─ ABORTA la tarea si DISCOVERY_FAILED es crítico
    └─ RECOVERY si puede continuar con un discovery mínimo
```

**Regla clave:** el Discovery Orchestrator no conoce la tarea del usuario ni le responde. Solo produce/actualiza el KB. El Orchestrator principal es el único que gobierna el lifecycle de la tarea y comunica el resultado final al usuario.

## State machine del Discovery Orchestrator

### Estados

| Estado | Descripción | Worker / Harness |
|--------|-------------|------------------|
| `DISCOVERY_INIT` | Preparar input, leer KB previo, calcular invalidaciones. | `init_worker` |
| `DISCOVERY_ENV` | Detectar entorno. | `environment_worker` |
| `DISCOVERY_STACK` | Detectar stack. | `stack_worker` |
| `DISCOVERY_FRAMEWORK` | Detectar framework. | `framework_worker` |
| `DISCOVERY_PATTERNS` | Detectar patrones. | `patterns_worker` |
| `DISCOVERY_BUSINESS` | Detectar reglas de negocio. | `business_worker` |
| `DISCOVERY_MERGE` | Fusionar outputs. | `synthesis_worker` |
| `DISCOVERY_VALIDATE` | Validar H10/H12. | harness |
| `DISCOVERY_READY` | KB actualizado y válido. | — |
| `DISCOVERY_FAILED` | Fallo; reporta al Orchestrator principal. | — |

### Transiciones

```text
DISCOVERY_INIT
    │
    ├─→ DISCOVERY_ENV
    ├─→ DISCOVERY_STACK
    ├─→ DISCOVERY_PATTERNS
    └─→ DISCOVERY_BUSINESS

DISCOVERY_STACK → DISCOVERY_FRAMEWORK

DISCOVERY_ENV, DISCOVERY_FRAMEWORK, DISCOVERY_PATTERNS, DISCOVERY_BUSINESS
    │
    ▼
DISCOVERY_MERGE
    │
    ▼
DISCOVERY_VALIDATE
    │
    ├─→ DISCOVERY_READY
    └─→ DISCOVERY_FAILED
```

### Archivo de state machine

`.agents/states/DISCOVERY_STATE_MACHINE.md` debe contener:

- Descripción de cada estado.
- Required input/output artifacts.
- Allowed transitions.
- Harness triggers.

## Condiciones de invocación

El Orchestrator principal invoca al Discovery Orchestrator cuando:

1. No existe `.project/knowledge/discovery/`.
2. `.last_discovery` supera el TTL de proyecto (24h).
3. El hash de archivos de configuración cambió.
4. El hash de la muestra de código cambió.
5. El usuario pidió refresh explícito.
6. Un worker de ejecución reporta inconsistencia.
7. El TTL de entorno (6h) venció y el scope es `env`.

## Scopes de invocación

| Scope | Workers invocados | Uso |
|-------|-------------------|-----|
| `full` | Todos | Primera vez o cambio importante. |
| `env` | `init_worker`, `environment_worker`, `synthesis_worker` | Cambio de herramientas. |
| `stack` | `init_worker`, `stack_worker`, `framework_worker`, `synthesis_worker` | Nuevas dependencias. |
| `patterns` | `init_worker`, `patterns_worker`, `synthesis_worker` | Cambio de convenciones. |
| `business` | `init_worker`, `business_worker`, `synthesis_worker` | Cambio de lógica. |

## Cálculo de hashes

El Orchestrator principal calcula los hashes antes de invocar:

1. **Config files hash:** SHA-256 de archivos de configuración relevantes en orden determinista.
2. **Sample files hash:** SHA-256 de la muestra de código seleccionada.
3. **Environment hash:** SHA-256 de los resultados del probe de entorno.

El `init_worker` usa estos hashes para determinar invalidaciones.

## TTL y cache

| Aspecto | TTL | Detalle |
|---------|-----|---------|
| Proyecto | 24h | Reinvoca todo el pipeline si cambia. |
| Entorno | 6h | Reinvoca solo `environment.md`. |
| Stack | 24h | Reinvoca `stack_worker` + `framework_worker` si cambia el hash de config. |
| Patterns | 24h | Reinvoca `patterns_worker` si cambia la muestra de código. |
| Business | 24h | Reinvoca `business_worker` si cambia README o servicios principales. |

## Payload de invocación

```json
{
  "project_root": "/path/to/project",
  "scope": "full",
  "context_budget": 100000,
  "sample_size": 10,
  "hashes": {
    "config_files_hash": "sha256:abc...",
    "sample_files_hash": "sha256:def...",
    "environment_hash": "sha256:ghi..."
  }
}
```

## Respuesta del Discovery Orchestrator

El Discovery Orchestrator devuelve un resultado estructurado al Orchestrator principal. **No responde al usuario y no genera artefactos de sesión de la tarea.**

### Caso DISCOVERY_READY

```json
{
  "status": "DISCOVERY_READY",
  "knowledge_base_path": ".project/knowledge/discovery/",
  "manifest": ".project/knowledge/discovery/.discovery_manifest",
  "harness_report": ".project/<session-uuid>/HARNESS_REPORT.md"
}
```

**Acción del Orchestrator principal:** continúa con su state machine. El KB queda disponible para `GATHERING_CONTEXT`, `PLANNING` y `EXECUTING`.

### Caso DISCOVERY_FAILED

```json
{
  "status": "DISCOVERY_FAILED",
  "reason": "H12 rejected outputs 3 times",
  "recovery_report": ".project/<session-uuid>/RECOVERY_REPORT.md"
}
```

**Acciones posibles del Orchestrator principal:**

1. **Abortar la tarea** (`ABORT`) si el KB es indispensable y no se puede continuar.
2. **Ir a `RECOVERY`** para replanificar con un discovery mínimo o con un scope reducido.
3. **Continuar con un discovery mínimo** si aplica: README + stack por extensión de archivos, sin análisis cualitativo.

La decisión depende de la criticidad del KB para la tarea.

## Archivos a crear

- `.agents/workflow/09-discovery.md`
- `.agents/states/DISCOVERY_STATE_MACHINE.md`

## Archivos a modificar

- `.agents/roles/orchestrator.md`
  - Detectar necesidad de discovery.
  - Invocar al Discovery Orchestrator con scope.
  - Recibir `DISCOVERY_READY` o `DISCOVERY_FAILED`.
  - Decidir la transición del state machine principal según la respuesta: continuar, abortar o ir a `RECOVERY`.
  - Incluir `environment.md` y `development_patterns.md` en payloads de workers de ejecución.

## Fases de implementación

### Fase 1: State machine

1. Escribir `.agents/states/DISCOVERY_STATE_MACHINE.md`.
2. Documentar estados, transiciones, artifacts, harness triggers.

### Fase 2: Workflow

1. Escribir `.agents/workflow/09-discovery.md`.
2. Definir input/output, condiciones de invocación, scopes.

### Fase 3: Orchestrator principal

1. Actualizar `.agents/roles/orchestrator.md`.
2. Agregar lógica de invocación y manejo de respuesta.

### Fase 4: Verificación

1. Asegurar que el workflow 09 no contradiga los workflows 00-08.
2. Asegurar que el Discovery Orchestrator no viole el No-Skip Rule del state machine principal.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | `.agents/states/DISCOVERY_STATE_MACHINE.md` existe. | `ls` |
| 2 | `.agents/workflow/09-discovery.md` existe. | `ls` |
| 3 | El Orchestrator principal invoca al Discovery Orchestrator. | Revisar `.agents/roles/orchestrator.md`. |
| 4 | Se definen scopes de invocación. | Revisar Plan 04. |
| 5 | TTL de proyecto (24h) y entorno (6h) están definidos. | Revisar `.agents/features.toml` y `.agents/roles/orchestrator.md`. |
| 6 | El Discovery Orchestrator reporta `DISCOVERY_READY` o `DISCOVERY_FAILED`. | Revisar Plan 04. |
| 7 | El workflow 09 no salta estados del state machine principal. | Revisar `.agents/states/AGENT_STATE_MACHINE.md`. |
| 8 | El Orchestrator principal decide la transición tras recibir `DISCOVERY_READY`/`DISCOVERY_FAILED`. | Revisar `.agents/roles/orchestrator.md`. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| El Orchestrator principal invoca discovery en cada tarea | Cache por TTL y hash; scopes parciales. |
| Inconsistencia entre TTL de proyecto y entorno | TTL separados; reinvocación parcial. |
| Hashes calculados incorrectamente | Orden determinista de archivos; validación en H12. |
| El Orchestrator principal no expone patrones a workers | Incluir referencias en payload del worker (Plan 05). |
| El state machine del Discovery Orchestrator se mezcla con el principal | Archivos separados: `AGENT_STATE_MACHINE.md` y `DISCOVERY_STATE_MACHINE.md`. |
