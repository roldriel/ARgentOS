# Plan de Implementación 04 — Orquestación

> **Origen:** Punto 4 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Integrar una guía de orquestación práctica que complemente `orchestrator.md`, el state machine y el contrato de delegación existentes.

---

## 1. Objetivo del plan

Crear `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` a partir de `example/.agents/roles/coordinator/ORCHESTRATION_GUIDE.md`, con:

- 7 preguntas rápidas para decidir qué perfil de worker convocar en la fase de ejecución.
- Checklist antes de delegar, basado en artefactos reales del protocolo.
- Referencia al catálogo de capas de `ARCHITECTURE_CONTRACT.md` (Plan 03) y al catálogo de perfiles de Plan 06.
- Regla clave: nunca reenviar el prompt original del usuario; reescribirlo usando la plantilla del perfil y el payload de `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- Mapeo explícito a los workflow phases reales (`00-analyze-task.md` a `08-recovery.md`).
- Referencias a feature flags existentes en `.agents/features.toml`: `rubrics`, `knowledge_base`, `decision_trees`.

Además, extender `.agents/roles/orchestrator.md` dentro de su sección existente "5. Worker Delegation" para que use la guía antes de delegar la fase 06.

---

## 2. Alcance

### Incluido
- Extracción de `example/.agents/roles/coordinator/ORCHESTRATION_GUIDE.md`.
- Adaptación de los anexos A, B y C al protocolo `.agents/`.
- Eliminación de referencias específicas de proyecto.
- Alineación con el state machine, los workflow phases y `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- Actualización de `.agents/roles/orchestrator.md` (sección 5 existente).
- Actualización de `.agents/standards/INDEX.md`.
- Creación de `.agents/standards/orchestration/README.md`.

### Excluido
- No modificar el state machine (`AGENT_STATE_MACHINE.md`).
- No modificar los archivos de workflow (`phase_*.md`) salvo referencias.
- No implementar código de orquestación automatizada.
- No modificar `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (la guía no añade reglas de límites de archivo).
- No modificar `.agents/standards/conduct/OPERATIONAL_RULES.md` (la guía lo consume, no al revés).
- No definir nuevos feature flags.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` | Guía práctica de orquestación. |
| `.agents/standards/orchestration/README.md` | Índice y responsabilidad de la categoría orchestration. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/roles/orchestrator.md` | Añadir subsección dentro de "5. Worker Delegation" que referencie y use la guía. |
| `.agents/standards/INDEX.md` | Añadir nueva sección `## Orchestration` con la guía. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.agents/roles/coordinator/ORCHESTRATION_GUIDE.md` | Fuente original. |
| `.agents/roles/orchestrator.md` | Contrato del orchestrator. |
| `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` | Formato obligatorio del payload de delegación. |
| `.agents/states/AGENT_STATE_MACHINE.md` | Alineación de estados. |
| `.agents/workflow/*.md` | Alineación de fases. |
| `.agents/features.toml` | Feature flags relevantes. |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` (Plan 03) | Catálogo de capas. |
| `.agents/standards/context/CONTEXT_ENGINEERING.md` (Plan 05) | Técnicas de compresión. |
| `.agents/roles/profiles/*.md` (Plan 06) | Catálogo de perfiles. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer `example/.agents/roles/coordinator/ORCHESTRATION_GUIDE.md` completo.
2. Leer `.agents/roles/orchestrator.md`.
3. Leer `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
4. Leer `.agents/states/AGENT_STATE_MACHINE.md`.
5. Leer `.agents/workflow/*.md` para entender las fases 00–08.
6. Leer `.agents/features.toml` para identificar flags existentes.
7. Leer el catálogo de perfiles de Plan 06 (`.agents/roles/profiles/README.md` y los perfiles individuales si existen; si aún no existen, usar los nombres definidos en Plan 06).

### Paso 2 — Diseño de la guía
Estructura propuesta:

```markdown
# ORCHESTRATION_GUIDE.md

## 1. Propósito
## 2. Cuándo usar esta guía
## 3. Las 7 preguntas de decisión
## 4. Checklist pre-delegación
## 5. Uso del catálogo de capas y perfiles
## 6. Regla de oro: reescribir, no reenviar
## 7. Mapeo a workflow phases
## 8. Feature flags relevantes
## 9. Plantilla de payload de delegación
## 10. Ejemplos
```

### Paso 3 — Redacción del contenido

#### Sección 1 — Propósito
- Proveer al orchestrator un manual práctico para decidir **a qué perfil** delegar una tarea de ejecución.
- Reducir carga cognitiva y tokens en el prompt del orchestrator.
- Asegurar coherencia con el state machine y con `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.

#### Sección 2 — Cuándo usar
- **Principalmente** en la transición `PLAN_READY → EXECUTING`, antes de delegar la fase `06-execute.md`.
- También en transiciones opcionales ya definidas en `orchestrator.md`:
  - `knowledge_base` activado → delegar `context_discoverer` antes del worker real.
  - `rubrics` activado → delegar `reviewer` antes de transiciones críticas.
- **No aplica** a `CONFIRMING_INTENT` (perfil fijo: `intent_reflector`) ni a fases puramente analíticas/planificación (00–05).

#### Sección 3 — Las 7 preguntas de decisión
Las preguntas son mutuamente excluyentes en su acción principal. Si una tarea activa más de una, dividirla en subtareas secuenciales.

1. ¿La tarea modifica esquemas, migraciones, queries o índices de base de datos? → `database_engineer`.
2. ¿La tarea integra o consume sistemas/APIs externos? → `integration_engineer`.
3. ¿La tarea define o ejecuta pruebas, casos de prueba o verificación de calidad? → `qa_engineer`.
4. ¿La tarea produce documentación técnica para desarrolladores/agentes? → `tech_writer`.
5. ¿La tarea produce documentación funcional o de negocio? → `functional_writer`.
6. ¿La tarea implementa lógica de negocio, endpoints o servicios? → `backend_engineer`.
7. ¿Ninguna de las anteriores aplica o la tarea es genérica (análisis, planificación, recuperación)? → `worker` genérico.

Para cada pregunta, indicar:
- Perfil convocado.
- Workflow phase donde aplica (principalmente `06-execute.md`).
- Archivos `MUST_READ` del perfil según `.agents/roles/profiles/<perfil>.md`.
- Perfiles alternativos que **no** deben usarse.

#### Sección 4 — Checklist pre-delegación
- [ ] Tengo el state actual del protocolo según `SESSION_LOG.md`.
- [ ] Tengo `TASK_SPECIFICATION.md`, `CONTEXT_VALIDATION_REPORT.md` y `EXECUTION_PLAN.md` para la fase 06.
- [ ] Apliqué las 7 preguntas e identifiqué si la tarea requiere un perfil especializado.
- [ ] Seleccioné el perfil o el worker genérico y lo registré en el payload.
- [ ] Determiné las lecturas obligatorias del perfil según `.agents/roles/profiles/<perfil>.md`.
- [ ] Reescribí el objetivo usando la plantilla del perfil, no el prompt original del usuario.
- [ ] Incluí los criterios de aceptación de `TASK_SPECIFICATION.md` en el payload.
- [ ] Verifiqué que el payload sigue el formato de `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- [ ] Apliqué compresión de contexto según `CONTEXT_ENGINEERING.md` si el contexto excede el umbral definido allí.
- [ ] Registré la decisión de delegación en `SESSION_LOG.md`.

#### Sección 5 — Uso del catálogo de capas y perfiles
La guía de orquestación **no define** capas arquitectónicas ni perfiles técnicos. Solo indica:
- Dónde encontrar el catálogo de capas: `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
- Dónde encontrar el catálogo de perfiles: `.agents/roles/profiles/README.md`.
- Cómo usarlos al decidir: una tarea que afecta una capa específica puede convocar al perfil correspondiente (por ejemplo, capa Provider → `integration_engineer`).

> **SRP:** `ORCHESTRATION_GUIDE.md` decide *cuándo y a quién delegar*; `ARCHITECTURE_CONTRACT.md` define *qué son las capas*; los perfiles definen *cómo actúa cada rol técnico*.

#### Sección 6 — Regla de oro: reescribir, no reenviar
- El orchestrator no debe reenviar el prompt crudo del usuario.
- Debe reescribirlo usando:
  - Contexto comprimido según `CONTEXT_ENGINEERING.md`.
  - La plantilla de prompt del perfil (sección `## 9. Plantilla de prompt` de `.agents/roles/profiles/<perfil>.md`).
  - Criterios de aceptación de `TASK_SPECIFICATION.md`.
  - Estado actual del protocolo.
- Si se usa el worker genérico, aplicar la plantilla mínima del payload del contrato de delegación.

#### Sección 7 — Mapeo a workflow phases
Mapear las 7 preguntas y el checklist a los workflow phases reales:

| Workflow phase | Aplica guía de orquestación | Decisión |
|---|---|---|
| `00-analyze-task.md` | No | Perfil fijo según `orchestrator.md`. |
| `01-confirm-intent.md` | No | Perfil fijo `intent_reflector`. |
| `02-build-task-specification.md` | No | Worker genérico. |
| `03-gather-context.md` | No | Worker genérico (o `context_discoverer` si `knowledge_base` está activo). |
| `04-validate-context.md` | No | Worker genérico. |
| `05-plan.md` | No | Worker genérico. |
| `06-execute.md` | **Sí** | Elegir perfil con las 7 preguntas. |
| `07-verify.md` | Parcialmente | Si `rubrics` está activo, invocar `reviewer`. |
| `08-recovery.md` | Parcialmente | Worker genérico; si `decision_trees` está activo, seguir árbol de decisión. |

#### Sección 8 — Feature flags relevantes
Solo pueden mencionarse feature flags que existan en `.agents/features.toml`:

- `rubrics`: si está activo, invocar `reviewer` antes de transiciones críticas.
- `knowledge_base`: si está activo, adjuntar entradas de KB relevantes (vía `context_discoverer`).
- `decision_trees`: si está activo, seguir árbol de decisión en recovery.
- `caveman`: si está activo, aplicar estilo de comunicación comprimido en el payload.

> **Nota:** `context_engineering` **no es un feature flag**. La compresión de contexto se aplica según `CONTEXT_ENGINEERING.md` cuando el contexto excede el umbral definido.

#### Sección 9 — Plantilla de payload de delegación
El payload debe ser una instancia concreta de `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`. Ejemplo para fase 06:

```json
{
  "session_uuid": "<uuid>",
  "current_state": "EXECUTING",
  "target_phase": "workflow/06-execute.md",
  "role_to_adopt": "worker",
  "profile": "<perfil o null>",
  "input_artifacts": [
    ".project/<uuid>/<iteration>/<order>-TASK_SPECIFICATION.md",
    ".project/<uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md",
    ".project/<uuid>/<iteration>/<order>-EXECUTION_PLAN.md"
  ],
  "harness_policy": "harness/policies/H05-execution-completed.md",
  "task_summary": "<objetivo reescrito usando plantilla del perfil>",
  "knowledge_entries": [],
  "context_budget": 4000,
  "communication_style": {"enabled": true, "level": "full"},
  "technical_approach": {"enabled": [], "notes": []}
}
```

La guía debe explicar cómo rellenar cada campo en función del perfil elegido.

#### Sección 10 — Ejemplos
Incluir al menos 4 ejemplos con:
1. Prompt original del usuario.
2. Aplicación de las 7 preguntas.
3. Perfil elegido.
4. Payload JSON completo según el contrato.
5. Justificación de por qué no se eligió otro perfil.

Ejemplos mínimos:
1. Worker genérico: "Corregir typo en README.md".
2. `backend_engineer`: "Agregar endpoint de listado de usuarios".
3. `database_engineer`: "Agregar campo `email_verified` a la tabla users".
4. Múltiples perfiles secuenciales: "Integrar API externa de pagos y documentar el flujo" → primero `integration_engineer`, luego `functional_writer`.

### Paso 4 — Extensión de `orchestrator.md`
1. Localizar la sección existente "5. Worker Delegation".
2. Añadir subsección: "5.X. Profile selection before execution".
3. Indicar que, antes de delegar `workflow/06-execute.md`, el orchestrator debe consultar `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` y aplicar las 7 preguntas.
4. Indicar que el payload debe seguir `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` y usar el campo `profile` (introducido por Plan 06) cuando aplica.
5. No modificar las demás secciones del orchestrator.

### Paso 5 — Actualización del índice
1. Añadir una nueva sección `## Orchestration` en `.agents/standards/INDEX.md`.
2. Bajo esa sección, añadir:
   ```markdown
   - `orchestration/ORCHESTRATION_GUIDE.md` — decision procedure for selecting worker profiles and delegation payloads.
   - `orchestration/README.md` — overview of orchestration standards.
   ```

### Paso 6 — Creación de `orchestration/README.md`
1. Crear `.agents/standards/orchestration/README.md`.
2. Contenido mínimo:
   - Una línea sobre la responsabilidad de la categoría.
   - Lista de archivos en la categoría.
   - Enlace a `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.

### Paso 7 — Revisión final
1. Verificar coherencia con el state machine.
2. Confirmar que las 7 preguntas cubren los 6 perfiles del Plan 06.
3. Validar que el payload de ejemplo sea compatible con `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
4. Validar que todos los feature flags mencionados existan en `.agents/features.toml`.
5. Asegurar que no haya referencias a proyecto específico.
6. Asegurar que no se hayan modificado `PROTOCOL_BOUNDARIES.md` ni `OPERATIONAL_RULES.md`.

---

## 5. Criterios de aceptación

- [ ] `ORCHESTRATION_GUIDE.md` existe en `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` y cubre las 10 secciones definidas.
- [ ] Existe `.agents/standards/orchestration/README.md` con la responsabilidad de la categoría.
- [ ] Incluye 7 preguntas de decisión mutuamente excluyentes en su acción principal y con mapeo explícito a perfiles.
- [ ] Incluye checklist pre-delegación con al menos 10 ítems verificables, sin conceptos no definidos en el protocolo.
- [ ] Incluye sección de "Uso del catálogo de capas y perfiles" que referencia `ARCHITECTURE_CONTRACT.md` y `.agents/roles/profiles/README.md`.
- [ ] Incluye plantilla de payload de delegación como instancia JSON de `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- [ ] Incluye al menos 4 ejemplos con payload JSON completo y justificación del perfil elegido.
- [ ] `orchestrator.md` referencia y usa la guía dentro de la sección "5. Worker Delegation".
- [ ] `.agents/standards/INDEX.md` indexa la guía bajo una nueva sección `## Orchestration`.
- [ ] No se modifica `AGENT_STATE_MACHINE.md`.
- [ ] No se modifica `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`.
- [ ] No se modifica `.agents/standards/conduct/OPERATIONAL_RULES.md`.
- [ ] No se inventan feature flags; todos los flags mencionados existen en `.agents/features.toml`.
- [ ] No hay referencias a `pay_back`, Flask ni dominio específico.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con `orchestrator.md`. | Integrar la guía dentro de la sección "5. Worker Delegation" existente; tratar la guía como manual práctico y el rol como contrato de comportamiento. |
| Sobrecarga de decisiones. | Las 7 preguntas son binarias y mutuamente excluyentes en su acción principal. Si una tarea activa varias, se divide en subtareas secuenciales. |
| Desalineación con fases existentes. | Mapear explícitamente cada pregunta/checklist a los workflow phases reales (`00-analyze-task.md` a `08-recovery.md`). |
| Payload incompatible con `WORKER_DELEGATION_CONTRACT.md`. | La plantilla de payload de la guía debe ser una instancia concreta del contrato, no un formato nuevo. |
| Dependencia circular con Plan 05 y Plan 06. | Plan 04 define las 7 preguntas y los perfiles esperados por nombre; Plan 05 y Plan 06 implementan los documentos referenciados sin cambiar la interfaz definida aquí. |
| Pérdida de información por compresión. | Aplicar compresión solo según `CONTEXT_ENGINEERING.md` y nunca sobre criterios de aceptación, restricciones críticas o estado del protocolo. |

---

## 7. Dependencias

- Plan 01 completado (`.agents/standards/conduct/OPERATIONAL_RULES.md` y `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` disponibles).
- Plan 03 completado o al menos disponible el borrador de `ARCHITECTURE_CONTRACT.md`.
- `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` leído y estable. Si Plan 04 necesita añadir el campo `profile`, coordinar con Plan 06.
- Catálogo de perfiles del Plan 06 conocido (nombres: `backend_engineer`, `database_engineer`, `integration_engineer`, `qa_engineer`, `tech_writer`, `functional_writer`).
- Acceso a `.agents/roles/orchestrator.md`, `.agents/states/AGENT_STATE_MACHINE.md`, `.agents/workflow/*.md`.
- Acceso a `.agents/features.toml`.

---

## 8. Orden relativo de ejecución

Ejecutar **después del Plan 03 (Arquitectura)** y **antes del Plan 05 (Context Engineering)** y **Plan 06 (Perfiles de Worker)**.

Racional:
- Plan 04 necesita saber que existe `ARCHITECTURE_CONTRACT.md` para referenciarlo.
- Plan 04 define las 7 preguntas y nombra los perfiles que Plan 06 implementará.
- Plan 04 referencia `CONTEXT_ENGINEERING.md` como técnica de compresión; Plan 05 lo implementa.
- Plan 04 no requiere el contenido final de Plan 05 ni Plan 06, solo sus interfaces y nombres.

---

## 9. Notas adicionales

- En el futuro, las 7 preguntas pueden migrarse a un árbol de decisión TOML bajo `.agents/harness/decisions/`, aprovechando el feature flag `decision_trees` ya existente.
- No se requiere ejecutar código en este plan.
- La guía no modifica el contrato de delegación salvo que Plan 06 requiera añadir el campo `profile`; en ese caso, la modificación se documenta en Plan 06.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `ORCHESTRATION_GUIDE.md` | Decidir cuándo, a quién y cómo delegar tareas. | Definición de capas arquitectónicas (responsabilidad de `ARCHITECTURE_CONTRACT.md`), técnicas de compresión (responsabilidad de `CONTEXT_ENGINEERING.md`), ni reglas internas de cada perfil (responsabilidad de `.agents/roles/profiles/<perfil>.md`). |
| `orchestrator.md` | Contrato de comportamiento del rol orchestrator. | Detalles de la guía práctica; solo la referencia dentro de Worker Delegation. |
| `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` | Formato estructurado del payload de delegación. | Lógica de selección de perfiles. |
| `.agents/roles/profiles/<perfil>.md` | Reglas, lecturas obligatorias y plantilla de un perfil técnico. | Lógica de orquestación. |
| `.agents/roles/profiles/README.md` | Catálogo y guía de uso de perfiles. | Decisiones de cuándo usar cada perfil. |
| `ARCHITECTURE_CONTRACT.md` (Plan 03) | Definición de capas. | Lógica de delegación. |
| `CONTEXT_ENGINEERING.md` (Plan 05) | Compresión de contexto. | Decisiones de orquestación. |

**Principio aplicado:** la guía de orquestación *usa* capas, perfiles, compresión y el contrato de delegación, pero no los define. Su única razón de cambio es "cambiar el procedimiento de decisión/orquestación".
