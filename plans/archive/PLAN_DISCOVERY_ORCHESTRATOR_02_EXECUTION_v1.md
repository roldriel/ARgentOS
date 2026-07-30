---
title: "Plan de implementación — Discovery Orchestrator: Ejecución de workers"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: ["plans/PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md"]
---

# Plan 02: Ejecución de workers

## Objetivo

Definir el Discovery Orchestrator, sus workers especializados, el pipeline de ejecución y el modelo de reintentos.

## Alcance

- Crear `.agents/roles/discovery_orchestrator.md`.
- Crear `.agents/roles/discovery_workers/*.md`.
- Actualizar `.agents/features.toml`.
- Definir el mecanismo de comunicación entre workers.
- Definir cómo se consume el KB previo y los artefactos de sesión.
- No implementar el workflow ni el harness en este paso.

## Mecanismo de ejecución

El Discovery Orchestrator es un **prompt de instrucciones** que guía al LLM para coordinar workers. Cada worker también es un prompt de instrucciones. El LLM materializa las acciones con tool calls (Read, Glob, Grep, Bash, Write).

El Discovery Orchestrator:

1. Lee el KB previo y artefactos de sesión.
2. Determina qué workers invocar según el `scope`.
3. Ejecuta workers en paralelo donde sea posible.
4. Recoge outputs parciales.
5. Invoca al `synthesis_worker` para fusionar y escribir el KB.
6. Valida con H10/H12.

## Workers

### 1. `init_worker`

- **Ubicación:** `.agents/roles/discovery_workers/init_worker.md`
- **Input:** `project_root`, `scope`, `previous_kb`, `session_artifacts`.
- **Output:** `discovery_input.json` + `invalidation_report.json`.
- **Tareas:**
  - Leer KB previo.
  - Leer artefactos de sesión relevantes.
  - Calcular qué entradas están stale por hash.
  - Preparar input para los demás workers.

### 2. `environment_worker`

- **Ubicación:** `.agents/roles/discovery_workers/environment_worker.md`
- **Input:** `discovery_input.json`.
- **Output:** `environment.md`.
- **Tareas:**
  - Detectar SO, shell, herramientas, runtime.
  - Ejecutar comandos seguros de solo lectura.
  - Filtrar secrets e información sensible.

### 3. `stack_worker`

- **Ubicación:** `.agents/roles/discovery_workers/stack_worker.md`
- **Input:** `discovery_input.json`.
- **Output:** `stack.md`, `dependencies.md`, `containers.md`, `database.md`.
- **Tareas:**
  - Detectar lenguajes y frameworks por extensión y archivos de config.
  - Listar dependencias de `package.json`, `requirements.txt`, `Cargo.toml`, etc.
  - Detectar `Dockerfile`, `docker-compose.yml`.
  - Detectar configuraciones de base de datos.

### 4. `framework_worker`

- **Ubicación:** `.agents/roles/discovery_workers/framework_worker.md`
- **Input:** output de `stack_worker`.
- **Output:** `architecture.md`, `configuration.md`.
- **Tareas:**
  - Detectar patrones arquitectónicos del framework principal.
  - Leer archivos de configuración (settings, blueprints, etc.).
  - Documentar scripts de build, test, deploy.

### 5. `patterns_worker`

- **Ubicación:** `.agents/roles/discovery_workers/patterns_worker.md`
- **Input:** `discovery_input.json` + muestra de código.
- **Output:** `development_patterns.md`.
- **Tareas:**
  - Seleccionar muestra representativa de código.
  - Detectar convenciones de estilo, naming, imports, error handling, testing, logging, typing.
  - Documentar excepciones.

### 6. `business_worker`

- **Ubicación:** `.agents/roles/discovery_workers/business_worker.md`
- **Input:** `discovery_input.json`, README, código de servicios, tests.
- **Output:** `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md`.
- **Tareas:**
  - Leer README y servicios principales.
  - Identificar flujos de negocio.
  - Detectar deuda técnica y errores conocidos (comentarios, TODO, FIXME, `RECOVERY_REPORT.md`).

### 7. `synthesis_worker`

- **Ubicación:** `.agents/roles/discovery_workers/synthesis_worker.md`
- **Input:** outputs parciales + KB previo + artefactos de sesión.
- **Output:** `summary.md`, `.discovery_manifest` + entradas KB consolidadas.
- **Tareas:**
  - Fusionar outputs parciales.
  - Aplicar reglas de fusión del KB.
  - Resolver conflictos.
  - Escribir manifest.

## Pipeline de ejecución

```text
init_worker
    │
    ├─→ environment_worker ──┐
    ├─→ stack_worker ───┬────┼────┐
    │                   │    │    │
    │                   ▼    │    │
    │            framework_worker  │
    │                   │    │    │
    │                   ▼    ▼    ▼
    │                 DISCOVERY_MERGE
    │                       │
    │                       ▼
    │                 synthesis_worker
    │                       │
    │                       ▼
    │                 DISCOVERY_VALIDATE
    │                       │
    │                       ▼
    │                 DISCOVERY_READY
    │
    └─→ business_worker ────┘
```

## Comunicación entre workers

### Opción A: Directorio de trabajo intermedio

Cada worker escribe su output en `.project/<session-uuid>/discovery/worker_<name>.json`. El siguiente worker lee de ahí.

**Ventaja:** los outputs intermedios son auditables.
**Desventaja:** más archivos temporales.

### Opción B: Payload directo entre estados

El Discovery Orchestrator mantiene el estado en memoria y pasa el output de un worker al siguiente como parte del payload.

**Ventaja:** menos archivos temporales.
**Desventaja:** menos trazabilidad; depende del contexto del LLM.

**Recomendación:** Opción A para producción, Opción B para optimización futura.

## Muestreo

Cada worker que lee código (stack, patterns, business, framework) aplica su propio muestreo, limitado por `context_budget` y `sample_size`.

Reglas generales:

1. Excluir directorios de dependencias/build.
2. Agrupar por extensión y directorio funcional.
3. Seleccionar hasta `sample_size` archivos por grupo, priorizando nombres representativos.
4. Limitar total por `context_budget`.

## Reintentos

- Máximo 3 reintentos por worker.
- Backoff: 1s, 2s, 4s.
- Si un worker falla, el Discovery Orchestrator puede:
  - Reintentar el worker.
  - Continuar sin ese output (degradación parcial).
  - Reportar `DISCOVERY_FAILED` si es crítico.

## Decisiones resueltas

| Decisión | Resolución |
|----------|------------|
| Worker separado o perfil | **Workers separados** bajo un Discovery Orchestrator. |
| Quién calcula el hash | **Orchestrator principal** inicia; `init_worker` calcula invalidaciones por hash. |
| `sample_size` por defecto | 10 por directorio, 50 por idioma. |
| Inline o tag compacto | **Tag compacto** en payload de workers de ejecución. |
| `git log` | Permitido limitado a `--oneline -n 50`. |
| TTL entorno | 6h; TTL proyecto 24h. |

## Archivos a crear

- `.agents/roles/discovery_orchestrator.md`
- `.agents/roles/discovery_workers/init_worker.md`
- `.agents/roles/discovery_workers/environment_worker.md`
- `.agents/roles/discovery_workers/stack_worker.md`
- `.agents/roles/discovery_workers/framework_worker.md`
- `.agents/roles/discovery_workers/patterns_worker.md`
- `.agents/roles/discovery_workers/business_worker.md`
- `.agents/roles/discovery_workers/synthesis_worker.md`

## Archivos a modificar

- `.agents/features.toml`
  - `llm_discovery = true`
  - `discovery_orchestrator = true`
  - `discovery_sample_size = 10`
  - `discovery_environment_ttl_hours = 6`
  - `discovery_project_ttl_hours = 24`

## Fases de implementación

### Fase 1: Crear el Discovery Orchestrator

1. Escribir `.agents/roles/discovery_orchestrator.md`.
2. Definir su máquina de estados interna (Plan 04).

### Fase 2: Crear workers

1. Escribir cada worker en `.agents/roles/discovery_workers/`.
2. Cada worker debe tener: input, output, tareas, guardrails, reintentos.

### Fase 3: Configuración

1. Actualizar `.agents/features.toml`.

### Fase 4: Verificación

1. Revisar que cada worker sea puro texto.
2. Revisar que no haya asunciones de Python.
3. Revisar que los workers sean agnósticos al modelo.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | Existe `.agents/roles/discovery_orchestrator.md`. | `ls` |
| 2 | Existen 7 workers en `.agents/roles/discovery_workers/`. | `ls` |
| 3 | El pipeline de ejecución está documentado. | Leer Plan 02. |
| 4 | La comunicación entre workers está definida. | Leer `INTER_WORKER_MESSAGE.md` (Plan 01). |
| 5 | El muestreo y reintentos están especificados. | Leer Plan 02. |
| 6 | `.agents/features.toml` tiene los flags nuevos. | Leer el archivo. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| El Discovery Orchestrator se vuelve demasiado complejo | Empezar con pipeline secuencial; paralelizar después. |
| Workers muy pequeños generan muchos tool calls | Agrupar lecturas similares; cache por worker. |
| El `synthesis_worker` pierde información | Requerir que preserve todos los `source_files` y `source_workers`. |
| Inconsistencia entre workers | Contratos `INTER_WORKER_MESSAGE` y H10. |
