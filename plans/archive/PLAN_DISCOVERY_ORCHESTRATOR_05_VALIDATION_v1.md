---
title: "Plan de implementación — Discovery Orchestrator: Validación, calidad y riesgo"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: ["plans/PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_02_EXECUTION.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_03_ENVIRONMENT.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_04_ORCHESTRATION.md"]
---

# Plan 05: Validación, calidad y riesgo

## Objetivo

Definir la validación de ground truth (H12), las métricas de calidad, el plan de rollback, el análisis de riesgo y la integración de los artefactos de discovery en los workers de ejecución.

## Alcance

- Crear `.agents/harness/policies/H12-discovery-output.md`.
- Actualizar `.agents/harness/INDEX.md`, `.agents/harness/health_check.py`.
- Crear `.agents/standards/context/USING_PATTERNS.md`.
- Actualizar `.agents/roles/worker.md` y `.agents/workflow/06-execute.md`.
- Definir métricas de calidad y criterios de rollback.
- Eliminar el código Python legacy del discovery.
- No implementar workers ni workflows en este paso.

## H12: Discovery Output Validation

### Responsabilidad exclusiva

Validar que el contenido del KB tenga fuente en el proyecto real o en el entorno real, y que la fusión no haya introducido inconsistencias.

### Verificaciones

1. **Stack real:** cada lenguaje/framework en `stack.md` debe provenir de un archivo de configuración real.
2. **Dependencias reales:** cada dependencia en `dependencies.md` debe aparecer en un archivo de configuración real.
3. **Patrones observados:** cada patrón en `development_patterns.md` debe tener un ejemplo verificable en sus `source_files`.
4. **Entorno sin secrets:** `environment.md` no debe contener strings sensibles ni valores de variables de entorno.
5. **Source files reales:** cada `source_files` debe apuntar a una ruta existente, excepto `"system_probe"`.
6. **No afirmaciones sin fuente:** afirmaciones cualitativas deben estar respaldadas por `source_files` o artefactos de sesión.
7. **Fusión consistente:** el `synthesis_worker` no debe haber perdido información ni generado conflictos sin marcar.

### Implementación

H12 puede implementarse en Python como parte del harness. El harness es el guardián del protocolo y puede contener código; esto no viola el principio de que `.agents/` son instrucciones, porque el harness no es una instrucción para el agente.

### Rechazo de outputs inventados

Si H12 detecta una afirmación sin fuente:

1. Marcar el archivo como inválido.
2. Reportar al Discovery Orchestrator.
3. El Discovery Orchestrator decide reintentar el worker afectado o reportar `DISCOVERY_FAILED`.

## Métricas de calidad

| Métrica | Definición | Umbral mínimo |
|---------|------------|---------------|
| Cobertura de stack | Lenguajes/frameworks detectados vs. presentes en config. | 100% de los presentes en config. |
| Precisión de dependencias | Dependencias listadas con fuente real. | 100% deben tener fuente. |
| Cobertura de patrones | Patrones con `confidence: high` y `source_files` verificables. | Al menos 3 patrones reales. |
| Tasa de rechazo de H12 | Outputs rechazados por afirmaciones sin fuente. | < 10% en pruebas. |
| Tiempo de ejecución | Tiempo total del discovery. | < 5 minutos para proyectos medianos. |
| Costo en tokens | Tokens consumidos por worker. | Documentado y presupuestado. |

## Plan de rollback y criterios de abort

### Rollback

Como el extractor Python se elimina sin coexistencia, el rollback no es a código. Es un rollback de estado:

1. Si la implementación genera un estado roto, restaurar desde git (`git checkout` o `git reset`).
2. El plan maestro y los sub-planes deben estar versionados en git.

### Criterios de abort

El Discovery Orchestrator debe abortar si:

1. H10 o H12 fallan 3 veces consecutivas.
2. No se puede generar ningún archivo del KB.
3. Un worker crítico (`init_worker`, `synthesis_worker`) falla.
4. El usuario cancela explícitamente.
5. Se excede el presupuesto de tokens por fase.

### Fallback ante fallo

Si el discovery falla completamente, el Discovery Orchestrator puede:

- Reportar `DISCOVERY_FAILED` al Orchestrator principal.
- Usar un **discovery mínimo**: README + stack detectado por extensión de archivos, sin análisis cualitativo ni patrones.

## Integración en workers de ejecución

### `.agents/standards/context/USING_PATTERNS.md`

Guía para workers de ejecución:

1. Cómo leer `development_patterns.md`.
2. Cómo aplicar patrones al escribir o modificar código.
3. Cómo manejar excepciones documentadas.
4. Cómo tratar `confidence: low` vs `confidence: high`.
5. Cómo usar `environment.md` para elegir shell y herramientas.

### `.agents/roles/worker.md`

Incluir en el contexto del worker:

- Referencia (tag compacto) a `environment.md`.
- Referencia (tag compacto) a `development_patterns.md`.
- Instrucción de respetar los patrones descubiertos y el entorno detectado.

### `.agents/workflow/06-execute.md`

Actualizar para que:

1. El worker valide que `environment.md` y `development_patterns.md` existan antes de ejecutar.
2. El worker use el shell y herramientas recomendadas por `environment.md`.
3. El worker aplique los patrones de `development_patterns.md`.

## Archivos a modificar

1. `.agents/harness/INDEX.md` — documentar workflow 09 y H12.
2. `.agents/harness/health_check.py` — dejar de importar `project_discovery`; validar KB.
3. `.agents/standards/context/USING_PATTERNS.md` — crear.
4. `.agents/roles/worker.md` — incluir `environment.md` y `development_patterns.md` en el contexto.
5. `.agents/workflow/06-execute.md` — referenciar patrones y entorno.

## Archivos a eliminar

1. `.agents/harness/project_discovery/` — completo.
2. `.agents/harness/tests/test_project_discovery.py` — ya no aplica.
3. `plans/PLAN_ENVIRONMENT_DISCOVERY.md` — si existe.

## Análisis de costo/riesgo

### Costo del enfoque LLM vs extractor Python

| Aspecto | Extractor Python | Discovery Orchestrator LLM |
|---------|------------------|---------------------------|
| Velocidad | Rápido | Más lento |
| Costo | Bajo (CPU local) | Alto (tokens) |
| Flexibilidad | Baja | Alta |
| Mantenimiento | Alto (parsers por lenguaje) | Bajo (texto puro) |
| Escalabilidad | Baja | Alta (workers paralelos) |
| KB acumulativo | No | Sí |
| Alucinaciones | Ninguna | Posible; mitigado por H12 |

### Presupuesto de tokens estimado

| Worker | Tokens estimados | Nota |
|--------|------------------|------|
| `init_worker` | 1k - 3k | Lectura de KB previo y artefactos. |
| `environment_worker` | 1k - 3k | Comandos cortos. |
| `stack_worker` | 5k - 15k | Lectura de archivos de config. |
| `framework_worker` | 5k - 15k | Depende de `stack_worker`. |
| `patterns_worker` | 5k - 15k | Análisis de muestra de código. |
| `business_worker` | 5k - 15k | Lectura de servicios y README. |
| `synthesis_worker` | 5k - 15k | Fusión y escritura de KB. |
| **Total** | **27k - 81k** | Ajustable por config. |

## Fases de implementación

### Fase 1: H12

1. Escribir `.agents/harness/policies/H12-discovery-output.md`.
2. Definir checks de ground truth por worker.

### Fase 2: Health check

1. Actualizar `.agents/harness/health_check.py`.
2. Eliminar importaciones a `project_discovery`.

### Fase 3: Integración en workers

1. Crear `.agents/standards/context/USING_PATTERNS.md`.
2. Actualizar `.agents/roles/worker.md`.
3. Actualizar `.agents/workflow/06-execute.md`.

### Fase 4: Eliminación de legacy

1. Eliminar `.agents/harness/project_discovery/`.
2. Eliminar `.agents/harness/tests/test_project_discovery.py`.
3. Actualizar `.agents/harness/INDEX.md`.

### Fase 5: Validación

1. Probar con el proyecto `example/`.
2. Verificar que H12 rechace outputs inventados.
3. Verificar que `health_check.py` pase.
4. Verificar que los workers usen patrones y entorno.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | `.agents/harness/project_discovery/` fue eliminado. | El directorio no existe. |
| 2 | `.agents/harness/policies/H12-discovery-output.md` existe. | `ls` |
| 3 | H12 rechaza outputs inventados. | Test con `architecture.md` sin fuente. |
| 4 | `health_check.py` no importa `project_discovery`. | `grep` |
| 5 | `health_check.py` pasa. | Ejecutar el comando. |
| 6 | Los workers reciben `environment.md` y `development_patterns.md`. | Revisar `.agents/roles/worker.md` y `.agents/workflow/06-execute.md`. |
| 7 | Se definen métricas de calidad. | Leer Plan 05. |
| 8 | Se define plan de rollback. | Leer Plan 05. |
| 9 | El KB consume artefactos de sesión. | Revisar Plan 02. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| H12 es muy estricto | Calibrar umbrales; permitir `confidence: low` para afirmaciones inciertas. |
| Eliminación de legacy rompe tests | Actualizar `health_check.py` y tests. |
| Workers no adoptan patrones | Incluir referencias en payload y guía `USING_PATTERNS.md`. |
| Costo excesivo | Muestreo, cache, TTL, workers paralelos. |
| Fallo silencioso de H12 | Tests explícitos con casos de alucinación. |
| `synthesis_worker` pierde procedencia | H12 verifica que todas las entradas tengan `source_workers` y `source_files`. |
