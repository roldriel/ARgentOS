# Plan de Implementación 05 — Context Engineering (actualizado)

> **Origen:** Punto 5 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Incorporar técnicas de compresión de contexto al estándar existente `.agents/standards/context/CONTEXT.md`, usando solo tags y conceptos que ya existan en el protocolo ARgentOS.
> **Regla de oro:** no se crea un nuevo documento de context engineering; se refactoriza el estándar vigente.

---

## 1. Objetivo del plan

Refactorizar `.agents/standards/context/CONTEXT.md` para que integre, de forma medible y sin ambigüedad, las técnicas de compresión de prompt extraídas de `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`.

El documento resultante debe:

- Definir **tags compactos** derivados del vocabulario del protocolo.
- Establecer reglas explícitas de **inline vs referencia** con un umbral medible.
- Documentar el uso de **one-shot examples**.
- Reemplazar la vaga "regla del 50 %" por una **regla de compresión por presupuesto**.
- Describir **descomposición multi-turn** con un criterio de activación claro.
- Mantenerse alineado con `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` y `.agents/standards/conduct/OPERATIONAL_RULES.md`.

No se crea `.agents/standards/context/CONTEXT_ENGINEERING.md`. Ese nombre duplicaría la responsabilidad de `CONTEXT.md` y generaría confusión de autoridad.

---

## 2. Alcance

### Incluido

- Extracción de las técnicas válidas de `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`.
- Generalización de ejemplos de dominio (reemplazar nombres de pagos por placeholders genéricos como `<DOMAIN>` o `<ENTITY>`).
- Definición de tags compactos **basados en documentos del protocolo existentes**.
- Reglas de cuándo usar **inline** y cuándo **referencia**.
- Integración con el workflow de orquestación a través de `CONTEXT.md`.
- Actualización de `.agents/standards/conduct/OPERATIONAL_RULES.md` para que referencie `CONTEXT.md` en la sección de Context Awareness.
- Actualización de `.agents/standards/INDEX.md` si la descripción de `CONTEXT.md` cambia.

### Excluido

- No crear un documento nuevo llamado `CONTEXT_ENGINEERING.md`.
- No modificar los presupuestos de KB definidos en `CONTEXT.md` (8000 y 4000 caracteres).
- No implementar compresión automática en runtime.
- No crear glosarios separados de tags; los tags se definen dentro de `CONTEXT.md`.
- No depender de archivos que no existan.

---

## 3. Archivos afectados

### Archivos a modificar

| Ruta | Cambio |
|------|--------|
| `.agents/standards/context/CONTEXT.md` | Añadir secciones de compresión, tags, inline vs referencia, one-shot, regla de compresión, multi-turn, anti-patrones y ejemplos. |
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | En la sección 5 "Context Awareness", referenciar `.agents/standards/context/CONTEXT.md` como el estándar de interpretación de contexto comprimido. |
| `.agents/standards/INDEX.md` | Actualizar la descripción de `CONTEXT.md` si la responsabilidad del documento se amplía. |

### Archivos a leer (solo lectura)

| Ruta | Uso |
|------|-----|
| `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md` | Fuente original de técnicas de compresión. |
| `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` | Verificar que ya consume `CONTEXT.md` en la checklist y en la sección 6. No requiere modificación salvo que la referencia esté ausente. |
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Sección 5, donde se añadirá la referencia a `CONTEXT.md`. |
| `.agents/standards/requirements/NO_ASSUMPTIONS.md` | Origen del tag `[NO_ASSUME]`. |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Origen del tag `[OUTPUT:<modo>]`. |
| `.agents/standards/communication/CAVEMAN.md` | Origen de modos de comunicación comprimida. |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Origen de tags de capa, dependencia y naming. |
| `.agents/states/AGENT_STATE_MACHINE.md` | Origen del tag `[STATE:<estado>]`. |

### Archivos que no se leerán

- `.agents/standards/context/KB_DISCOVERY_REPORT.md` — **no existe** en el repositorio. No se puede depender de él.

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuente

1. Leer `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md` completo.
2. Leer `.agents/standards/context/CONTEXT.md` completo.
3. Leer las secciones 4, 6, 8, 9 y 10 de `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` para confirmar que ya consume `CONTEXT.md`.
4. Leer la sección 5 de `.agents/standards/conduct/OPERATIONAL_RULES.md`.
5. Leer los documentos de origen de los tags: `NO_ASSUMPTIONS.md`, `OUTPUT_EFFICIENCY.md`, `CAVEMAN.md`, `ARCHITECTURE_CONTRACT.md`, `AGENT_STATE_MACHINE.md`.
6. Listar los tags de `CONTEXT_ENGINEER.md` y descartar los que dependan de dominio de pagos o que no tengan origen en el protocolo.
7. Reemplazar en los ejemplos: `PaymentService`, `Payment`, `AmountVO`, `MONETARY`, `pay_back`, `click.echo` y similares por placeholders genéricos (`<ENTITY>`, `<DOMAIN>`, `<VALUE_OBJECT>`, `<FRAMEWORK>`).

### Paso 2 — Diseño de la estructura de `CONTEXT.md`

Estructura final propuesta para `CONTEXT.md` (se mantienen las secciones existentes y se añaden nuevas):

```markdown
# Context Engineering Standard

## 1. Propósito
## 2. Prioridad de información
## 3. Reglas de omisión
## 4. Presupuestos de contexto de Knowledge Base
## 5. Distribución de presupuesto
## 6. Criterios de selección de entradas de KB
## 7. Session Brief
## 8. Session Log
## 9. Técnicas de compresión de contexto
### 9.1 Tags compactos
#### 9.1.1 Tags de autoridad y alcance
#### 9.1.2 Tags arquitectónicos
#### 9.1.3 Tags de acción y estado
### 9.2 Inline vs referencia
### 9.3 One-shot examples
### 9.4 Regla de compresión por presupuesto
### 9.5 Descomposición multi-turn
## 10. Anti-patrones
## 11. Ejemplos
```

### Paso 3 — Definición de tags compactos

Cada tag debe tener tres columnas: **Tag**, **Significado** y **Origen en el protocolo**.

Tags a definir, todos derivados de documentos existentes:

| Tag | Significado | Origen en el protocolo |
|-----|-------------|------------------------|
| `[AUTHORITY:<source>]` | Fuente normativa que prevalece en caso de conflicto. | `OPERATIONAL_RULES.md` §1.3 (canonical sources). |
| `[SCOPE:<scope>]` | Alcance permitido de la tarea. | `OPERATIONAL_RULES.md` §2.1. |
| `[LAYER:<layer>]` | Capa arquitectónica afectada. | `ARCHITECTURE_CONTRACT.md` y `ORCHESTRATION_GUIDE.md` §5. |
| `[DEPENDENCY:<rule>]` | Regla de dirección de dependencia permitida. | `ARCHITECTURE_CONTRACT.md`. |
| `[NAMING:<convention>]` | Convención de nombres obligatoria. | `ARCHITECTURE_CONTRACT.md`. |
| `[NO_ASSUME]` | Requiere clarificación ante información faltante. | `NO_ASSUMPTIONS.md`. |
| `[OUTPUT:<mode>]` | Modo de salida esperado (`minimal`, `structured`, `verbose`). | `OUTPUT_EFFICIENCY.md` y `CAVEMAN.md`. |
| `[STATE:<state>]` | Estado actual del protocolo. | `AGENT_STATE_MACHINE.md`. |

Reglas para los tags:

- No se permiten tags fuera de esta lista inicial sin una propuesta de cambio documentada.
- Cada tag debe ser descomprimible por el worker leyendo el documento de origen citado.
- No se usan tags con nombres de dominio de negocio.
- El tag `[OUTPUT:<mode>]` solo acepta modos definidos en `OUTPUT_EFFICIENCY.md` o `CAVEMAN.md`.

### Paso 4 — Reglas de inline vs referencia

Criterios explícitos:

**Usar inline cuando el contenido sea:**

- Específico de la tarea actual (no reutilizable).
- Un fragmento de código que debe modificarse.
- Una regla de dominio no obvia (ejemplo: "`<STATUS>` no bloquea el procesamiento de `<EVENT>`").
- Un mensaje de error, contrato o valor exacto.
- Una instrucción que no está documentada en la KB.

**Usar referencia cuando el contenido sea:**

- Un estándar ya documentado en `.agents/standards/` o en la KB.
- Una convención de nombres o arquitectura.
- Un `project-map.md`, `technical-analysis.md` o similar.
- Estable y reutilizable entre tareas.

**Umbral de decisión:**

- Si el contenido excede el 10 % del presupuesto de KB de la fase actual, usar referencia.
- El presupuesto de KB se toma de `CONTEXT.md` §4: 8000 caracteres para análisis y contexto; 4000 para planificación, ejecución y verificación.
- Ejemplo: en fase de ejecución, el umbral es 400 caracteres (10 % de 4000). Si el contenido supera esa cifra, referenciar.

### Paso 5 — One-shot examples

Incluir un ejemplo compacto de input/output cuando:

- El formato de salida es estricto.
- La tarea tiene un patrón repetitivo.
- Se quiere reducir explicaciones verbales.

Reglas:

- El ejemplo debe ocupar como máximo 5 líneas de prompt.
- Debe ser genérico: sin nombres de clases del dominio de pagos.
- Debe incluir una nota que explique por qué el patrón aplica.

### Paso 6 — Regla de compresión por presupuesto

Reemplazar la "regla del 50 %" por el siguiente procedimiento:

1. Medir el tamaño en caracteres del contexto de KB que el orchestrator va a incluir en el payload.
2. Comparar contra el presupuesto de la fase (8000 o 4000 caracteres).
3. Si el tamaño excede el presupuesto, aplicar compresión en este orden:
   1. **Omitir** entradas de KB con menor relevancia.
   2. **Resumir** entradas manteniendo los criterios de aceptación y restricciones.
   3. **Referenciar** en lugar de incluir inline.
   4. **Dividir** la tarea en sub-tareas (multi-turn).
4. Verificar que el payload final conserva:
   - Autoridad (fuentes normativas aplicables).
   - Criterios de aceptación de `TASK_SPECIFICATION.md`.
   - Restricciones críticas (seguridad, dependencias, capas).
   - Estado actual del protocolo.

No se acepta compresión que elimine cualquiera de los cuatro elementos anteriores.

### Paso 7 — Descomposición multi-turn

Activar solo cuando, después de aplicar la regla de compresión por presupuesto, el contexto de KB siga excediendo el presupuesto.

Procedimiento:

1. Dividir la tarea en sub-tareas secuenciales.
2. Cada sub-tarea debe producir un artifact parcial en `.project/<session-uuid>/<iteration>/`.
3. El orchestrator referencia los artifacts parciales en los turnos posteriores, en lugar de repetir todo el contexto.
4. Cada sub-tarea debe tener su propio `TASK_SPECIFICATION.md` o sección de criterios de aceptación.

### Paso 8 — Actualización de `OPERATIONAL_RULES.md`

En la sección 5 "Context Awareness", añadir al final:

```markdown
### 5.3 Contexto comprimido

Cuando el orchestrator entregue contexto comprimido usando tags compactos, el worker debe interpretar cada tag según `.agents/standards/context/CONTEXT.md`. Si un tag no está definido allí, el worker debe reportarlo como ambigüedad y no asumir su significado.
```

### Paso 9 — Actualización de `INDEX.md`

Si la sección "Context" de `INDEX.md` describe `CONTEXT.md` solo como "context engineering and knowledge-base budgets", actualizar la descripción para incluir:

```markdown
- `context/CONTEXT.md` — context engineering, knowledge-base budgets, técnicas de compresión de contexto y tags compactos.
```

### Paso 10 — Verificación final

1. Confirmar que `CONTEXT.md` contiene las secciones 9, 10 y 11.
2. Confirmar que cada tag tiene un documento de origen en el protocolo.
3. Confirmar que no queda ninguna referencia a `pay_back`, `MONETARY`, `PaymentService`, `AmountVO`, `Payment` ni términos del dominio de pagos.
4. Confirmar que `OPERATIONAL_RULES.md` §5 referencia `CONTEXT.md`.
5. Confirmar que `ORCHESTRATION_GUIDE.md` ya referencia `CONTEXT.md` (ya lo hace en checklist y sección 6).
6. Confirmar que no se creó `CONTEXT_ENGINEERING.md`.
7. Confirmar que los presupuestos de KB no cambiaron.

---

## 5. Criterios de aceptación

- [ ] `CONTEXT.md` incluye una sección "Técnicas de compresión de contexto" con subsecciones de tags, inline vs referencia, one-shot, regla de compresión y multi-turn.
- [ ] Define tags compactos derivados de documentos del protocolo, con significado, origen y ejemplo.
- [ ] No define tags inventados o sin origen en el protocolo.
- [ ] Incluye reglas de inline vs referencia con un umbral medible (10 % del presupuesto de KB).
- [ ] Incluye la regla de compresión por presupuesto, con procedimiento ordenado y elementos no negociables.
- [ ] Incluye procedimiento de descomposición multi-turn con criterio de activación.
- [ ] Incluye al menos 3 ejemplos de prompts antes/después de compresión.
- [ ] `OPERATIONAL_RULES.md` referencia `CONTEXT.md` en la sección de Context Awareness.
- [ ] `ORCHESTRATION_GUIDE.md` mantiene su referencia existente a `CONTEXT.md`.
- [ ] `.agents/standards/INDEX.md` refleja la descripción actualizada de `CONTEXT.md`.
- [ ] No se crea `CONTEXT_ENGINEERING.md`.
- [ ] No se modifican los presupuestos de KB (8000 y 4000 caracteres).
- [ ] No quedan referencias al dominio de pagos.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Workers no interpreten correctamente los tags. | Cada tag debe citar un documento de origen del protocolo. El worker puede leer ese documento para descomprimir el significado. |
| Exceso de tags crea un lenguaje opaco. | Límite inicial de 8 tags. Nuevo tag requiere propuesta de cambio y aprobación. |
| Pérdida de información crítica por compresión. | Aplicar checklist de no negociables: autoridad, criterios de aceptación, restricciones críticas, estado actual. |
| Conflicto con `ORCHESTRATION_GUIDE.md`. | `CONTEXT.md` es el estándar técnico; `ORCHESTRATION_GUIDE.md` es el consumidor. No se duplican procedimientos. |
| Referencias a dominio de pagos quedan en ejemplos. | Verificar con búsqueda de términos antes de dar el plan por terminado. |

---

## 7. Dependencias

- Acceso a `.agents/standards/context/CONTEXT.md`.
- Acceso a `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.
- Acceso a `.agents/standards/conduct/OPERATIONAL_RULES.md`.
- Acceso a `.agents/standards/requirements/NO_ASSUMPTIONS.md`.
- Acceso a `.agents/standards/communication/OUTPUT_EFFICIENCY.md`.
- Acceso a `.agents/standards/communication/CAVEMAN.md`.
- Acceso a `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
- Acceso a `.agents/states/AGENT_STATE_MACHINE.md`.
- Acceso a la fuente `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`.

**No se depende de:**

- `.agents/standards/context/KB_DISCOVERY_REPORT.md` — no existe.
- Plan 01 o Plan 04 como entidades abstractas; solo se depende de los archivos concretos `OPERATIONAL_RULES.md` y `ORCHESTRATION_GUIDE.md`, que ya existen en sus rutas correctas.

---

## 8. Orden relativo de ejecución

- Ejecutar después de que existan `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` y `.agents/standards/conduct/OPERATIONAL_RULES.md`.
- Ejecutar antes de cualquier plan que genere perfiles de worker que vayan a consumir tags compactos, para que `CONTEXT.md` sea la fuente de verdad.
- No bloquearse por planes anteriores si los archivos reales de dependencia ya están disponibles.

---

## 9. Notas adicionales

- No se requiere ejecutar código en este plan.
- No se crea glosario separado. Los tags se definen dentro de `CONTEXT.md`.
- Toda referencia a feature flags debe coincidir con los definidos en `.agents/features.toml`.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `CONTEXT.md` | Estándar de contexto, KB, presupuestos y técnicas de compresión. | Procedimientos de selección de worker; eso es responsabilidad de `ORCHESTRATION_GUIDE.md`. |
| `ORCHESTRATION_GUIDE.md` | Decidir a qué perfil delegar y cómo construir el payload. | Definir tags ni técnicas de compresión; las consume desde `CONTEXT.md`. |
| `OPERATIONAL_RULES.md` | Conducta operativa del worker. | Técnicas de compresión; referencia `CONTEXT.md` para su interpretación. |

**Principio aplicado:** `CONTEXT.md` responde a "cómo comprimir el contexto y qué presupuestos aplicar". `ORCHESTRATION_GUIDE.md` responde a "cómo y a quién delegar". `OPERATIONAL_RULES.md` responde a "cómo debe comportarse el worker". Ningún documento absorbe responsabilidad de otro.
