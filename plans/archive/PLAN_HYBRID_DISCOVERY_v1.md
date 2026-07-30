---
title: "Plan maestro — Discovery basado en roles (proyecto + entorno + patrones)"
version: "2.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
---

# Plan de implementación: Discovery basado en roles

**Responsable:** Orchestrator + role `discovery_agent`  
**Tipo:** role/profile determinista con validación por harness  
**Prioridad recomendada:** implementar primero.

## Objetivo

Hacer que el **agente LLM** sea la única fuente de descubrimiento del proyecto, guiado por un role de texto en `.agents/roles/`. El role descubre:

1. **Stack, dependencias, configuración, contenedores, bases de datos, arquitectura, reglas de negocio, deuda técnica, errores conocidos y flujo del proyecto.**
2. **El entorno de ejecución:** sistema operativo, shell, terminal, herramientas disponibles, Python runtime, etc.
3. **Las costumbres y patrones de desarrollo** del equipo (estilo de código, convenciones, hábitos de formato) para que futuros roles de ejecución los adopten.

Paralelamente, **deprecar y eliminar el extractor Python** de `.agents/harness/project_discovery/`.

## Principio rector

> **`.agents/` son instrucciones. El agente es el executor. El harness es el guardián.**

> **Determinismo por contrato, no por código.**

> **Un agente que desarrolla código debe respetar los patrones del proyecto, no imponer su propio estilo.**

> **El agente debe conocer tanto el proyecto como el entorno donde lo va a ejecutar.**

## Arquitectura general

```text
┌─────────────────────────────────────────────────────────────┐
│                        .agents/ (texto)                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │ roles/           │  │ workflow/        │  │ harness/    │ │
│  │ discovery_agent  │  │ 09-discovery.md  │  │ policies/   │ │
│  │ .md              │  │                  │  │ H10-*       │ │
│  │                  │  │                  │  │ H12-*       │ │
│  └──────────────────┘  └──────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ delega
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator (role)                      │
│  - Detecta si discovery está stale o vacío                │
│  - Calcula hashes de config, muestra y entorno             │
│  - Delega al discovery_agent cuando corresponde             │
│  - Valida output con harness H10 / H12                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    discovery_agent (LLM)                    │
│  - Lee archivos del proyecto                                │
│  - Lee configuración del entorno                            │
│  - Detecta patrones de desarrollo                           │
│  - Escribe KB_DISCOVERY_ENTRY.md en .project/knowledge/     │
│    discovery/                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            .project/knowledge/discovery/ (output)          │
│  stack.md, dependencies.md, configuration.md,               │
│  containers.md, database.md, architecture.md,               │
│  business_rules.md, technical_debt.md,                     │
│  known_errors.md, project_flow.md,                          │
│  development_patterns.md, environment.md,                   │
│  summary.md, .discovery_manifest                           │
└─────────────────────────────────────────────────────────────┘
```

## Estructura de sub-planes

Este plan maestro se desglosa en 5 planes temáticos. Cada uno tiene el detalle operativo:

| Plan | Propósito | Archivos principales |
|------|-----------|----------------------|
| [PLAN_HYBRID_DISCOVERY_01_CONTRACTS.md](PLAN_HYBRID_DISCOVERY_01_CONTRACTS.md) | Contratos, formato, manifest y H10. | `.agents/contracts/DISCOVERY_MANIFEST.md`, `.agents/contracts/DEVELOPMENT_PATTERNS.md`, `.agents/contracts/ENVIRONMENT_DISCOVERY.md`, `.agents/harness/policies/H10-kb-discovery-report.md` |
| [PLAN_HYBRID_DISCOVERY_02_EXECUTION.md](PLAN_HYBRID_DISCOVERY_02_EXECUTION.md) | Role `discovery_agent`, muestreo, reintentos, decisiones pendientes. | `.agents/roles/discovery_agent.md`, `.agents/features.toml` |
| [PLAN_HYBRID_DISCOVERY_03_ENVIRONMENT.md](PLAN_HYBRID_DISCOVERY_03_ENVIRONMENT.md) | Environment discovery (Windows, shell, seguridad). | `.agents/standards/context/ENVIRONMENT_PROBE.md` |
| [PLAN_HYBRID_DISCOVERY_04_ORCHESTRATION.md](PLAN_HYBRID_DISCOVERY_04_ORCHESTRATION.md) | Integración con Orchestrator, state machine, TTL, cache. | `.agents/workflow/09-discovery.md`, `.agents/roles/orchestrator.md` |
| [PLAN_HYBRID_DISCOVERY_05_VALIDATION.md](PLAN_HYBRID_DISCOVERY_05_VALIDATION.md) | H12, métricas, rollback, riesgo, integración en workers. | `.agents/harness/policies/H12-discovery-output.md`, `.agents/harness/health_check.py`, `.agents/standards/context/USING_PATTERNS.md`, `.agents/roles/worker.md`, `.agents/workflow/06-execute.md` |

## Decisiones arquitectónicas clave

- **Extractor Python:** se elimina sin coexistencia. El descubrimiento es 100% role LLM.
- **Worker separado:** `discovery_agent` es un role propio, no un perfil del worker genérico.
- **Hash:** el Orchestrator calcula los hashes antes de invocar al role.
- **TTL:** 24h para el proyecto, 6h para el entorno.
- **Muestreo:** 10 archivos por directorio relevante, límite global de 50 por idioma.
- **Payload de workers:** tag compacto a `environment.md` y `development_patterns.md`.
- **H10:** validación estructural.
- **H12:** validación de ground truth.

## Archivos afectados (resumen)

### Nuevos archivos

- `.agents/roles/discovery_agent.md`
- `.agents/workflow/09-discovery.md`
- `.agents/harness/policies/H12-discovery-output.md`
- `.agents/contracts/DISCOVERY_MANIFEST.md`
- `.agents/contracts/DEVELOPMENT_PATTERNS.md`
- `.agents/contracts/ENVIRONMENT_DISCOVERY.md`
- `.agents/standards/context/ENVIRONMENT_PROBE.md`
- `.agents/standards/context/USING_PATTERNS.md`

### Archivos a modificar

- `.agents/roles/orchestrator.md`
- `.agents/roles/worker.md`
- `.agents/harness/policies/H10-kb-discovery-report.md`
- `.agents/harness/INDEX.md`
- `.agents/harness/health_check.py`
- `.agents/contracts/KB_DISCOVERY_ENTRY.md`
- `.agents/features.toml`
- `.agents/workflow/06-execute.md`
- `.project/knowledge/INDEX.md`

### Archivos a eliminar

- `.agents/harness/project_discovery/` (completo)
- `.agents/harness/tests/test_project_discovery.py`
- `plans/PLAN_ENVIRONMENT_DISCOVERY.md` (si existe)

## Criterios de éxito

| # | Criterio | Cómo verificar |
| --- | --- | --- |
| 1 | `.agents/harness/project_discovery/` fue eliminado. | El directorio no existe. |
| 2 | `.agents/roles/discovery_agent.md` existe y es puro texto. | Leer el archivo. |
| 3 | El Orchestrator delega al `discovery_agent` sin código Python. | Revisar `orchestrator.md`. |
| 4 | Se genera `environment.md` con datos reales del sistema. | Leer el archivo en la máquina actual. |
| 5 | `environment.md` **no contiene secrets** (filtra correctamente). | Buscar `TOKEN`, `KEY`, `SECRET`, `PASSWORD`, `CRED`, `AUTH`, `PRIVATE`. |
| 6 | Se genera `development_patterns.md` con al menos 3 patrones reales. | Leer el archivo en un proyecto real. |
| 7 | Cada patrón tiene `source_files`, `confidence` y `example`. | H10 pasa. |
| 8 | El role detecta stacks no Python solo con el role. | Probar con `Cargo.toml`, `package.json`, `go.mod`. |
| 9 | El worker incluye `environment.md` y `development_patterns.md` al escribir código. | Revisar `worker.md` / `06-execute.md`. |
| 10 | El cache evita reinvocar cuando no cambia el proyecto. | Comparar `.last_discovery` y `.discovery_manifest`. |
| 11 | El harness H12 rechaza outputs inventados. | Test con `architecture.md` sin fuente. |
| 12 | El health-check sigue pasando. | `python .agents/harness/health_check.py`. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
| --- | --- |
| **El LLM alucina stack, entorno o patrones.** | H12 exige `source_files` reales; H10 valida formato. |
| **Costo alto por leer muchos archivos.** | Muestreo representativo con `sample_size` y cache por hash. |
| **Comandos de entorno son inseguros.** | Solo comandos de lectura (`--version`, `which`, `where`, `echo`); filtrar secrets. |
| **Patrones inconsistentes.** | Documentar excepciones; no forzar un patrón si no es consistente. |
| **No determinismo entre modelos.** | Contrato fijo y harness igualan el comportamiento observable. |
| **Ruptura del health-check al eliminar el Python.** | Actualizar `health_check.py` para que solo valide el KB. |
| **Agente ignora patrones al ejecutar.** | Incluir `development_patterns.md` en el payload del worker y documentar en `USING_PATTERNS.md`. |
| **Eliminación del extractor sin fallback.** | Rollback por git; discovery mínimo en caso de fallo total; reintentos controlados. |

## Cómo usar este plan

1. Implementar los sub-planes en orden: 01 → 02 → 03 → 04 → 05.
2. Cada sub-plan puede ejecutarse de forma independiente, pero respeta las dependencias indicadas.
3. Al finalizar, verificar los criterios de éxito de este plan maestro.
4. El plan maestro se mantiene como documento de visión; el detalle operativo vive en los sub-planes.

## Decisiones históricas

- **v1.0.0:** Plan monolítico de 582 líneas con todas las fases, checklist y comandos.
- **v2.0.0:** Rediseño en plan maestro + 5 sub-planes temáticos para facilitar mantenimiento y ejecución.
