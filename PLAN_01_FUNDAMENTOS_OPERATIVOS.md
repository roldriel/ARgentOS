# Plan de Implementación 01 — Fundamentos Operativos

> **Origen:** Punto 1 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Crear un contrato operativo del worker y un checklist pre-vuelo ejecutable, referenciando las fuentes canónicas del protocolo sin duplicarlas.

---

## 1. Objetivo del plan

Crear dos artefactos complementarios bajo `.agents/standards/` que consolidan la operativa del worker **sin duplicar** las reglas canónicas ya definidas en otros estándares:

1. `.agents/standards/conduct/OPERATIONAL_RULES.md` — contrato operativo del worker que:
   - Organiza la operativa del worker en los siguientes temas: autoridad, precedencia, límites de tooling, control de scope, manejo de ambigüedad, context awareness, error handling, seguridad de interacciones externas, determinismo, criterios de completitud, restricciones de output y estilo de comunicación.
   - Referencia explícitamente las fuentes canónicas existentes: `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` y `PROTOCOL_BOUNDARIES.md`.
   - No repite el contenido normativo de esos documentos; en caso de conflicto, prevalece el estándar canónico correspondiente.

2. `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` — checklist ejecutable que el worker evalúa antes de actuar, derivado del contrato operativo y de los estándares de conducta existentes.

Además, actualizar `.agents/standards/INDEX.md` para incluir ambos documentos bajo sus categorías correspondientes, facilitando su descubrimiento.

> **Restricción de gobernanza:** Este plan modifica archivos dentro de `.agents/`. Según `PROTOCOL_BOUNDARIES.md`, cualquier cambio en `.agents/` requiere acuerdo explícito del usuario y debe quedar documentado.

---

## 2. Alcance

Este plan produce exactamente dos archivos nuevos bajo `.agents/standards/`, modifica uno existente en el mismo directorio, y no altera ningún otro archivo del protocolo.

### 2.1 Archivos a crear

#### 2.1.1 `.agents/standards/conduct/OPERATIONAL_RULES.md`

**Formato:**
- Archivo Markdown.
- Encabezado principal: `# Operational Rules`.
- Secciones numeradas con encabezados `## N. Título`.
- Sección final obligatoria: `## 12. Relationship to other standards`.
- Sin metadatos de proyecto específico.

**Estructura y contenido mínimo:**

| Sección | Origen | Contenido esperado | Referencia a estándar canónico |
|---|---|---|---|
| `## 1. Authority and Precedence` | Adaptado del punto 1 del fuente | Este documento aplica a todo worker. No prevalece sobre instrucciones legítimas del usuario que no violen el protocolo. En caso de conflicto con reglas de `.agents/`, prevalece el estándar canónico correspondiente. | `AGENTS.md` (punto de entrada), `PROTOCOL_BOUNDARIES.md` (límites), `ANTI_CIRCUMVENTION.md` (prohibición de evasión). |
| `## 2. Scope and Boundaries` | Adaptado del punto 4 del fuente y de `PROTOCOL_BOUNDARIES.md` | El worker ejecuta solo la tarea asignada; no expande scope, no refactoriza código no solicitado, no modifica archivos fuera del working directory, reporta bloqueos en lugar de asumirlos. | `PROTOCOL_BOUNDARIES.md` para reglas de límites de archivo y artefactos. |
| `## 3. Tooling and Execution Restrictions` | Adaptado del punto 3 del fuente | Lista de herramientas/operaciones prohibidas por defecto (instalar paquetes, modificar configuración de entorno, ejecutar linters/tests sin instrucción explícita). | Ninguna duplicación: si el proyecto necesita una lista técnica específica, se deja como plantilla fuera de `.agents/`. |
| `## 4. Handling Missing or Ambiguous Information` | Referencia al estándar existente | No definir nuevas reglas de ambigüedad. Incluir únicamente: "ante ambigüedad, ver `NO_ASSUMPTIONS.md`". | `NO_ASSUMPTIONS.md`. |
| `## 5. Context Awareness` | Adaptado del punto 6 del fuente | Antes de actuar, el worker debe leer `AGENTS.md`, `README.md` y los artefactos de contexto relevantes. No introducir abstracciones paralelas ni arquitecturas alternativas. | `AGENTS.md` (reglas de lectura por directorio). |
| `## 6. Error Handling` | Adaptado del punto 7 del fuente | No ocultar excepciones, no usar `except:` sin tipo, reportar errores de forma visible según el contexto de ejecución. | Ninguna; contenido propio. |
| `## 7. External Interaction Safety` | Adaptado del punto 8 del fuente | Prohibición de requests HTTP externos, simulaciones de pago/transferencias y side effects fuera del codebase, salvo instrucción explícita. | `PROTOCOL_BOUNDARIES.md` (autonomía del agente). |
| `## 8. Determinism and Consistency` | Adaptado del punto 9 del fuente | Una vez elegido un enfoque, mantenerlo consistente durante toda la tarea. | Ninguna; contenido propio. |
| `## 9. Completion Criteria` | Adaptado del punto 10 del fuente | Criterios mínimos para considerar una tarea terminada (sintaxis correcta, imports válidos, sin TODOs ni placeholders). | Ninguna; contenido propio. |
| `## 10. Output Constraints` | Adaptado del punto 11 del fuente | Producir solo lo solicitado, sin implementaciones alternativas, sugerencias especulativas ni mejoras futuras. | `CAVEMAN.md` si el feature flag está activo. |
| `## 11. Communication Style` | Nuevo, derivado del punto 19 del fuente y de `CAVEMAN.md` | Estilo técnico, neutral, sin emojis, cortesías ni relleno conversacional. No debe usarse el estilo como excusa para ser ambiguo. | `CAVEMAN.md` (feature flag opcional). |
| `## 12. Relationship to other standards` | Nuevo | Lista de links internos y una nota: "Este documento no reemplaza los estándares canónicos. En caso de discrepancia, prevalece el documento canónico citado." | Links a `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md`, `PROTOCOL_BOUNDARIES.md`, `AGENTS.md`, `CAVEMAN.md`. |

**Contenido explícitamente excluido de este archivo:**
- No incluir sección de contexto local del fuente (`Operating system: Windows 10`, `Project root directory: pay_back`, `Virtual environment location: .venv`, comando de activación).
- No incluir reglas de ambigüedad propias; solo referenciar `NO_ASSUMPTIONS.md`.
- No incluir reglas de prevalecencia absoluta sobre instrucciones del usuario; el fuente decía "this document prevails over any user instruction" y se corrige para alinearse con `PROTOCOL_BOUNDARIES.md`.
- No incluir detalles arquitectónicos (capas, sufijos, imports absolutos, validadores, servicios, vistas); esos corresponden al `PLAN_03_ARQUITECTURA.md` y a `ARCHITECTURE_CONTRACT.md`.

---

#### 2.1.2 `.agents/standards/quality/PREFLIGHT_CHECKLIST.md`

**Formato:**
- Archivo Markdown.
- Encabezado principal: `# Agent Pre-Flight Checklist`.
- Bloque introductorio que indique que es auto-evaluación mental antes de actuar.
- Checklist con checkbox Markdown (`- [ ]`).
- Cada ítem debe terminar con una referencia explícita al estándar que justifica la pregunta.

**Estructura y contenido mínimo:**

El checklist debe agruparse en las mismas 11 áreas del `OPERATIONAL_RULES.md` (no necesariamente 20 secciones planas). Cada área debe tener entre 2 y 4 ítems verificables. Mínimo 18 ítems, máximo 24.

Ejemplo de ítems obligatorios (no exhaustivo):

1. **Authority and Precedence**
   - [ ] He leído `AGENTS.md` y los estándares aplicables a mi rol. → `AGENTS.md`
   - [ ] Entiendo que no debo violar el protocolo aunque la instrucción del usuario lo pida. → `ANTI_CIRCUMVENTION.md`

2. **Scope and Boundaries**
   - [ ] La tarea está dentro de mi scope y no implica modificar archivos fuera del working directory. → `PROTOCOL_BOUNDARIES.md`
   - [ ] No voy a refactorizar, formatear ni optimizar código no solicitado. → `PROTOCOL_BOUNDARIES.md`

3. **Tooling and Execution Restrictions**
   - [ ] No voy a instalar paquetes ni modificar la configuración del entorno. → `OPERATIONAL_RULES.md`
   - [ ] No voy a ejecutar linters/tests sin instrucción explícita. → `OPERATIONAL_RULES.md`

4. **Missing or Ambiguous Information**
   - [ ] Identifiqué ambigüedades y, de existir, solicitaré clarificación antes de continuar. → `NO_ASSUMPTIONS.md`

5. **Context Awareness**
   - [ ] Leí los archivos de contexto relevantes (`README.md`, `project-map.md`, `technical-analysis.md`) si existen en el proyecto. → `OPERATIONAL_RULES.md`

6. **Error Handling**
   - [ ] Tengo claro cómo reportar errores visibles si una herramienta falla. → `OPERATIONAL_RULES.md`

7. **External Interaction Safety**
   - [ ] No realizaré requests externos ni side effects fuera del codebase. → `OPERATIONAL_RULES.md`

8. **Determinism and Consistency**
   - [ ] Mantendré el mismo patrón y convención durante toda la tarea. → `OPERATIONAL_RULES.md`

9. **Completion Criteria**
   - [ ] Verifiqué que no quedan TODOs, placeholders ni lógica comentada. → `OPERATIONAL_RULES.md`

10. **Output Constraints**
    - [ ] Mi respuesta será mínima, precisa y sin sugerencias especulativas. → `OPERATIONAL_RULES.md`

11. **Communication Style**
    - [ ] Mi estilo será técnico y neutral, sin emojis ni cortesías innecesarias. → `CAVEMAN.md` / `OPERATIONAL_RULES.md`

**Contenido explícitamente excluido de este archivo:**
- No copiar las 20 secciones originales del fuente con sus sub-ítems específicos de Flask (`click.echo`, `current_app.logger`, capas de arquitectura, sufijos de naming, imports absolutos, docstrings Google-style).
- No incluir ítems que dependan de `ARCHITECTURE_CONTRACT.md` (ese contrato aún no existe).
- No exigir que el checklist se escriba como artefacto de sesión; es auto-evaluación mental.

---

### 2.2 Archivos a modificar

#### 2.2.1 `.agents/standards/INDEX.md`

**Cambios exactos:**
- Añadir bajo la sección `## Conduct` (después de `ANTI_CIRCUMVENTION.md`):
  ```markdown
  - `conduct/OPERATIONAL_RULES.md` — operational contract for workers, referencing canonical conduct standards.
  ```
- Añadir bajo la sección `## Quality` (después de `RUBRICS.md`):
  ```markdown
  - `quality/PREFLIGHT_CHECKLIST.md` — pre-flight self-checklist for workers.
  ```

**Restricciones:**
- No reordenar las secciones existentes.
- No añadir descripciones largas; una línea por documento.
- No modificar el resto del índice.

---

### 2.3 Archivos explícitamente NO modificados

- `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`
- `.agents/standards/requirements/NO_ASSUMPTIONS.md`
- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
- `.agents/roles/orchestrator.md`
- `.agents/roles/worker.md`
- `.agents/roles/profiles/*.md`
- `.agents/workflow/*.md`
- `.agents/states/AGENT_STATE_MACHINE.md`
- `.agents/contracts/*.md`

**Nota:** Si en una futura iteración el orchestrator necesita incluir `OPERATIONAL_RULES.md` en el `MUST_READ` del payload de delegación, eso se tratará en `PLAN_04_ORQUESTACION.md`, no aquí.

---

### 2.4 Contenido del proyecto `example/` (solo lectura)

- `example/.agents/roles/_common/OPERATIONAL_RULES.md` — fuente original.
- `example/.agents/roles/_common/PREFLIGHT_CHECKLIST.md` — fuente original.

Estos archivos no se modifican. Se usan como referencia para extraer contenido portable, descartando toda referencia a:
- `pay_back`
- `Windows 10`
- `.venv`
- Comandos de activación de entorno virtual
- Cualquier convención específica de Flask (clicks, loggers, capas, sufijos, imports absolutos, docstrings)

---

## 3. Archivos afectados

Este punto resume el inventario de archivos derivado del alcance definido en la sección 2. No añade ni quita información respecto a lo establecido allí.

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Contrato operativo del worker. No es fuente única de verdad ni prevalece sobre los estándares canónicos; referencia `AGENTS.md`, `PROTOCOL_BOUNDARIES.md`, `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` y `CAVEMAN.md`. Ver sección 2.1.1 para formato y contenido mínimo. |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Checklist de auto-evaluación mental previa a actuar, agrupado en 11 áreas, con 18–24 ítems y referencia explícita al estándar que justifica cada ítem. Ver sección 2.1.2 para formato y contenido mínimo. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/INDEX.md` | Añadir una entrada en la sección `## Conduct` (debajo de `ANTI_CIRCUMVENTION.md`) y otra en la sección `## Quality` (debajo de `RUBRICS.md`). Usar rutas relativas desde `.agents/standards/` y descripciones de una sola línea. |

### Archivos explícitamente no modificados
- `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`
- `.agents/standards/requirements/NO_ASSUMPTIONS.md`
- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
- `.agents/roles/orchestrator.md`
- `.agents/roles/worker.md`
- `.agents/roles/profiles/*.md`
- `.agents/workflow/*.md`
- `.agents/states/AGENT_STATE_MACHINE.md`
- `.agents/contracts/*.md`

> **Restricción de gobernanza:** Toda modificación en `.agents/` —incluida `INDEX.md`— requiere acuerdo explícito del usuario según `PROTOCOL_BOUNDARIES.md`.

---

## 4. Pasos de implementación

### Paso 1 — Análisis de la fuente
1. Leer `example/.agents/roles/_common/OPERATIONAL_RULES.md`.
2. Leer `example/.agents/roles/_common/PREFLIGHT_CHECKLIST.md`.
3. Verificar que el mapeo de secciones del fuente al diseño de la sección 2.1.1 sea correcto.

### Paso 2 — Redacción de `OPERATIONAL_RULES.md`
1. Crear `.agents/standards/conduct/OPERATIONAL_RULES.md`.
2. Escribir las 12 secciones definidas en la sección 2.1.1, usando los títulos en inglés allí especificados.
3. Asegurar que las secciones que corresponden a estándares canónicos (`Handling Missing or Ambiguous Information`, `Scope and Boundaries`, `External Interaction Safety`, `Output Constraints`, `Communication Style`) referencien esos estándares en lugar de redefinir sus reglas.
4. Incluir la sección `## 12. Relationship to other standards` con links a `AGENTS.md`, `PROTOCOL_BOUNDARIES.md`, `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` y `CAVEMAN.md`.

### Paso 3 — Redacción de `PREFLIGHT_CHECKLIST.md`
1. Crear `.agents/standards/quality/PREFLIGHT_CHECKLIST.md`.
2. Escribir el checklist siguiendo la estructura de 11 áreas definida en la sección 2.1.2.
3. Garantizar entre 18 y 24 ítems, cada uno con checkbox Markdown (`- [ ]`) y referencia explícita al estándar que lo justifica.
4. No incluir ítems que dependan de `ARCHITECTURE_CONTRACT.md` ni convenciones específicas de Flask.

### Paso 4 — Actualización del índice
1. Editar `.agents/standards/INDEX.md`.
2. Añadir la entrada de `OPERATIONAL_RULES.md` bajo `## Conduct`, después de `ANTI_CIRCUMVENTION.md`.
3. Añadir la entrada de `PREFLIGHT_CHECKLIST.md` bajo `## Quality`, después de `RUBRICS.md`.
4. Usar rutas relativas desde `.agents/standards/` y descripciones de una sola línea.

### Paso 5 — Validación
1. Releer ambos documentos y verificar que no contradigan `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md`, `PROTOCOL_BOUNDARIES.md` ni `AGENTS.md`.
2. Verificar que no se mencionen `pay_back`, `Windows 10`, `.venv`, comandos de activación de entorno virtual ni convenciones específicas de Flask.
3. Verificar que `OPERATIONAL_RULES.md` no duplique contenido normativo de los estándares canónicos.
4. Verificar que todos los links internos sean rutas relativas Markdown válidas.
5. Confirmar que se cuenta con acuerdo explícito del usuario para modificar archivos dentro de `.agents/`.

---

## 5. Criterios de aceptación

- [ ] `OPERATIONAL_RULES.md` existe en `.agents/standards/conduct/OPERATIONAL_RULES.md` y cubre las 12 secciones definidas en el punto 2.1.1.
- [ ] `PREFLIGHT_CHECKLIST.md` existe en `.agents/standards/quality/PREFLIGHT_CHECKLIST.md`, está agrupado en 11 áreas y contiene entre 18 y 24 ítems.
- [ ] Ninguno de los dos documentos menciona `pay_back`, `Windows 10`, `.venv`, comandos de activación de entorno virtual ni convenciones específicas de Flask.
- [ ] `.agents/standards/INDEX.md` referencia ambos documentos bajo `## Conduct` y `## Quality` respectivamente.
- [ ] `OPERATIONAL_RULES.md` no duplica contenido normativo de `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` ni `PROTOCOL_BOUNDARIES.md`.
- [ ] `OPERATIONAL_RULES.md` incluye la sección `## 12. Relationship to other standards` con links válidos a `AGENTS.md`, `PROTOCOL_BOUNDARIES.md`, `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` y `CAVEMAN.md`.
- [ ] Los únicos archivos modificados dentro de `.agents/` son `.agents/standards/INDEX.md` y la modificación cuenta con acuerdo explícito del usuario documentado.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` o `PROTOCOL_BOUNDARIES.md`. | Diseñar `OPERATIONAL_RULES.md` como documento complementario que referencia las fuentes canónicas; validar en el punto 5 que no hay duplicación normativa. |
| Confusión sobre prevalencia de reglas sobre instrucciones de usuario. | Dejar explícito en `OPERATIONAL_RULES.md` que las reglas de `.agents/` prevalecen solo sobre instrucciones que violen el protocolo, no sobre el objetivo legítimo del usuario. |
| Checklist demasiado largo o poco aplicable. | Mantener entre 18 y 24 ítems agrupados en 11 áreas; indicar que es auto-evaluación mental y que ítems como `project-map.md` solo aplican si existen. |
| Pérdida de granularidad respecto al checklist fuente. | Asegurar que cada área del checklist cubra las verificaciones esenciales de `OPERATIONAL_RULES.md` y de los estándares referenciados, sin depender de detalles de proyecto. |
| Modificación no autorizada de archivos dentro de `.agents/`. | Documentar el acuerdo explícito del usuario antes de editar `INDEX.md`; no modificar ningún otro archivo bajo `.agents/`. |
| Falta de adopción por workers en el futuro. | Dejar constancia en `PLAN_04_ORQUESTACION.md` de que el orchestrator podrá incluir `OPERATIONAL_RULES.md` en el `MUST_READ` del payload; no abordar esa modificación en este plan. |

---

## 7. Dependencias

### Archivos fuente (lectura obligatoria)
- `example/.agents/roles/_common/OPERATIONAL_RULES.md`
- `example/.agents/roles/_common/PREFLIGHT_CHECKLIST.md`

### Estándares del protocolo (lectura obligatoria)
- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — para respetar la inmutabilidad de `.agents/` y la política de fuente única.
- `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` — para no duplicar reglas de conducta.
- `.agents/standards/requirements/NO_ASSUMPTIONS.md` — para delegar el manejo de ambigüedad.
- `.agents/standards/communication/CAVEMAN.md` — para alinear Output Constraints y Communication Style.
- `AGENTS.md` (raíz del proyecto) — para entender la entrada del protocolo y la precedencia de reglas.

### Archivo a modificar
- `.agents/standards/INDEX.md` — agregar entradas de los dos documentos nuevos.

---

## 8. Orden relativo de ejecución

Este plan debe ejecutarse **primero** dentro de la propuesta de integración ordenada, ya que los planes posteriores de **arquitectura** y **orquestación** pueden referenciar o asumir la existencia de `OPERATIONAL_RULES.md` y `PREFLIGHT_CHECKLIST.md`.

La modificación de `.agents/standards/INDEX.md` requiere acuerdo explícito del usuario según `PROTOCOL_BOUNDARIES.md`; una vez resuelta, los documentos creados por este plan están disponibles para los planes siguientes.

---

## 9. Notas adicionales

- No se requiere ejecutar código ni tests para este plan.
- El resultado es puramente documental y de gobernanza.
- La automatización del checklist queda fuera del alcance de este plan; si en el futuro se decide automatizarlo, deberá hacerse mediante un artefacto de sesión bajo `.project/<session-uuid>/<iteration>/`.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `OPERATIONAL_RULES.md` | Organizar el contrato operativo del worker, referenciando las reglas canónicas del protocolo sin duplicarlas. | Reglas canónicas ya definidas en `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md` o `PROTOCOL_BOUNDARIES.md`; detalles de compresión de contexto, arquitectura de capas o perfiles técnicos. |
| `PREFLIGHT_CHECKLIST.md` | Proveer el procedimiento de auto-verificación previa a actuar. | Reglas operativas (solo las referencia y verifica). |
| `INDEX.md` | Descubribilidad de estándares. | Contenido normativo. |
| `ANTI_CIRCUMVENTION.md` / `NO_ASSUMPTIONS.md` / `PROTOCOL_BOUNDARIES.md` | Mantener su propia responsabilidad como estándares canónicos; no se modifican en este plan. | No asumen nuevas responsabilidades. |

**Principio aplicado:** el contrato operativo y el checklist son complementarios pero separados. Si cambia una regla operativa propia del worker, se edita `OPERATIONAL_RULES.md`; si cambia una regla canónica del protocolo, se edita el estándar canónico correspondiente; si cambia el procedimiento de verificación, se edita `PREFLIGHT_CHECKLIST.md`.
