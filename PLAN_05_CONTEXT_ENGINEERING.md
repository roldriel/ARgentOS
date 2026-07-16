# Plan de Implementación 05 — Context Engineering

> **Origen:** Punto 5 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Añadir técnicas de compresión de contexto mediante tags compactos y estrategias de selección de módulos.

---

## 1. Objetivo del plan

Crear `.agents/standards/context/CONTEXT_ENGINEERING.md` a partir de `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`, con:

- Técnicas de compresión de prompt.
- Tags compactos (`[AUTHORITY:...]`, `[LAYER:...]`, `[DEPENDENCY:...]`, `[NAMING:...]`, `[BUSINESS_CRITICAL:...]`, etc.).
- Estrategias de cherry-picking de módulos.
- Diferencia entre inline vs referencia.
- Uso de one-shot examples.
- Regla del 50%: reducir el contexto a la mitad manteniendo precisión.
- Descomposición multi-turn.
- Alineación con `CONTEXT.md` y los budgets de KB existentes.

---

## 2. Alcance

### Incluido
- Extracción de `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`.
- Generalización de ejemplos (`MONETARY` → `BUSINESS_CRITICAL`).
- Definición de tags estándar de ARgentOS.
- Reglas de cuándo usar inline vs referencia.
- Integración con el workflow de orquestación.
- Actualización de `.agents/standards/INDEX.md`.

### Excluido
- No modificar `CONTEXT.md` salvo referencias cruzadas.
- No implementar compresión automática.
- No cambiar los límites de KB existentes.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/context/CONTEXT_ENGINEERING.md` | Estándar de context engineering. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/INDEX.md` | Indexar el documento bajo context. |
| `.agents/standards/context/CONTEXT.md` | Referenciar CONTEXT_ENGINEERING.md. |
| `.agents/standards/runtime/ORCHESTRATION_GUIDE.md` (Plan 04) | Referenciar técnicas de compresión. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md` | Fuente original. |
| `.agents/standards/context/CONTEXT.md` | Estándar existente. |
| `.agents/standards/context/KB_DISCOVERY_REPORT.md` | Reporte de KB. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuente
1. Leer `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md` completo.
2. Leer `.agents/standards/context/CONTEXT.md`.
3. Leer `.agents/standards/context/KB_DISCOVERY_REPORT.md`.
4. Identificar todos los tags y técnicas de compresión usados.
5. Listar ejemplos específicos de dominio de pagos que deban generalizarse.

### Paso 2 — Diseño del documento
Estructura propuesta:

```markdown
# CONTEXT_ENGINEERING.md

## 1. Propósito
## 2. Principios
## 3. Tags compactos
### 3.1 Tags de autoridad y precedencia
### 3.2 Tags arquitectónicos
### 3.3 Tags de riesgo y criticidad
### 3.4 Tags de acción y estado
## 4. Cherry-picking de módulos
## 5. Inline vs referencia
## 6. One-shot examples
## 7. Regla del 50%
## 8. Descomposición multi-turn
## 9. Integración con orquestación
## 10. Anti-patrones
## 11. Ejemplos
```

### Paso 3 — Redacción del contenido

#### Sección 1 — Propósito
- Reducir el consumo de tokens en la delegación entre orchestrator y workers.
- Mantener la precisión y autoridad del contexto.
- Estandarizar la forma de comprimir reglas, estado y requisitos.

#### Sección 2 — Principios
- Todo tag debe ser descomprimible por el worker.
- La compresión nunca debe introducir ambigüedad.
- Preferir referencia cuando el contexto es grande y estable.
- Preferir inline cuando el contexto es pequeño y variable.

#### Sección 3 — Tags compactos
Definir tags estándar:

| Tag | Significado | Ejemplo |
|-----|-------------|---------|
| `[AUTHORITY:<fuente>]` | Fuente de verdad que prevalece. | `[AUTHORITY:OPERATIONAL_RULES]` |
| `[LAYER:<capa>]` | Capa arquitectónica afectada. | `[LAYER:Service]` |
| `[DEPENDENCY:<dir>]` | Dirección de dependencia permitida. | `[DEPENDENCY:Service->Provider]` |
| `[NAMING:<sufijo>]` | Sufijo obligatorio. | `[NAMING:Service]` |
| `[BUSINESS_CRITICAL]` | Acción con alto impacto de negocio. | `[BUSINESS_CRITICAL]` |
| `[NO_ASSUME]` | Requiere clarificación si falta información. | `[NO_ASSUME]` |
| `[OPT_IN:<contrato>]` | Contrato opt-in activo. | `[OPT_IN:ARCHITECTURE_CONTRACT]` |
| `[MUST_READ:<path>]` | Lectura obligatoria. | `[MUST_READ:project-map.md]` |
| `[OUTPUT:<modo>]` | Modo de output esperado. | `[OUTPUT:minimal]` |
| `[STATE:<estado>]` | Estado actual del protocolo. | `[STATE:EXECUTING]` |

#### Sección 4 — Cherry-picking de módulos
- El orchestrator no envía todo el contexto; selecciona solo los módulos relevantes.
- Criterios de selección:
  - Pertinencia con la tarea.
  - Estado actual del protocolo.
  - Perfil del worker.
  - Feature flags activos.

#### Sección 5 — Inline vs referencia
- **Inline:** para datos pequeños, variables o específicos de la tarea.
- **Referencia:** para contratos, estándares, project-map, technical-analysis.
- Regla: si ocupa más de 10 líneas o es estable, referenciar.

#### Sección 6 — One-shot examples
- Incluir un ejemplo compacto de input/output esperado cuando:
  - El formato de salida es estricto.
  - La tarea tiene patrón repetitivo.
  - Se quiere reducir explicaciones.

#### Sección 7 — Regla del 50%
- Antes de delegar, el orchestrator debe intentar reducir el contexto a la mitad sin perder:
  - Autoridad.
  - Criterios de aceptación.
  - Restricciones críticas.
  - Estado del protocolo.

#### Sección 8 — Descomposición multi-turn
- Si el contexto sigue siendo demasiado grande, dividir la tarea en sub-tareas.
- Cada turno debe entregar un artifact parcial.
- El orchestrator acumula artifacts y los referencia en turnos posteriores.

#### Sección 9 — Integración con orquestación
- La guía de orquestación (Plan 04) debe usar CONTEXT_ENGINEERING.md para construir payloads.
- El payload de delegación debe incluir tags compactos cuando sea útil.

#### Sección 10 — Anti-patrones
- No comprimir hasta el punto de perder semántica.
- No inventar tags no documentados.
- No mezclar inline y referencia para el mismo estándar sin indicar jerarquía.
- No ignorar `[NO_ASSUME]` por compresión.

#### Sección 11 — Ejemplos
- Ejemplo de payload antes y después de compresión.
- Ejemplo de uso de tags en un prompt.
- Ejemplo de descomposición multi-turn.

### Paso 4 — Actualización de CONTEXT.md
1. Añadir al final o en una sección nueva:
   ```markdown
   ## Compresión de contexto
   
   Para técnicas de compresión y tags compactos, ver `.agents/standards/context/CONTEXT_ENGINEERING.md`.
   ```

### Paso 5 — Actualización del índice
1. Añadir `CONTEXT_ENGINEERING.md` en `.agents/standards/INDEX.md` bajo context.

### Paso 6 — Referencias cruzadas
1. En `ORCHESTRATION_GUIDE.md` (Plan 04), añadir sección o nota que referencie CONTEXT_ENGINEERING.md en la construcción del payload.
2. En `OPERATIONAL_RULES.md` (Plan 01), si habla de context awareness, referenciar este documento.

### Paso 7 — Revisión final
1. Verificar que los tags sean autoexplicativos.
2. Confirmar que no se contradiga con `CONTEXT.md`.
3. Validar que los ejemplos muestren reducción real de tokens.
4. Asegurar que no haya referencias a `pay_back`, `MONETARY` ni dominio específico.

---

## 5. Criterios de aceptación

- [ ] `CONTEXT_ENGINEERING.md` existe y cubre las 11 secciones definidas.
- [ ] Define al menos 10 tags compactos con significado claro.
- [ ] Incluye reglas de inline vs referencia.
- [ ] Incluye regla del 50% con criterios.
- [ ] Incluye al menos 3 ejemplos.
- [ ] `CONTEXT.md` referencia el nuevo documento.
- [ ] `ORCHESTRATION_GUIDE.md` referencia el nuevo documento.
- [ ] `.agents/standards/INDEX.md` indexa el documento.
- [ ] No se modifican los budgets de KB existentes.
- [ ] No hay referencias a dominio de pagos.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Workers no interpreten correctamente los tags. | Documentar significado explícito y usar tags auto-descriptivos. |
| Exceso de tags crea nuevo lenguaje opaco. | Limitar el set estándar; permitir extensión documentada. |
| Pérdida de información crítica por compresión. | Aplicar regla del 50% con criterios de no negociables. |
| Conflicto con `CONTEXT.md`. | Posicionar CONTEXT.md como estándar general y CONTEXT_ENGINEERING.md como técnica operativa. |

---

## 7. Dependencias

- Plan 01 completado.
- Plan 04 completado o al menos disponible el borrador de `ORCHESTRATION_GUIDE.md`.
- Acceso a `.agents/standards/context/CONTEXT.md` y `KB_DISCOVERY_REPORT.md`.
- Acceso a la fuente de `example/`.

---

## 8. Orden relativo de ejecución

Ejecutar **después del Plan 04 (Orquestación)** y **antes del Plan 06 (Perfiles de Worker)**, ya que los perfiles pueden usar tags en sus prompts.

---

## 9. Notas adicionales

- Considerar crear un glosario de tags accesible desde `INDEX.md`.
- No se requiere ejecutar código en este plan.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `CONTEXT_ENGINEERING.md` | Definir técnicas de compresión de contexto y tags compactos. | El contenido semántico del contexto (qué reglas, qué arquitectura); solo comprime y referencia. |
| `CONTEXT.md` | Estándar general de contexto y KB. | Técnicas de compresión; las referencia. |
| `ORCHESTRATION_GUIDE.md` (Plan 04) | Procedimiento de delegación. | Técnicas de compresión; las consume. |

**Principio aplicado:** este documento responde a "cómo comprimir el contexto", no a "qué contexto enviar". La selección de contenido sigue siendo responsabilidad del orchestrator y de la guía de orquestación.
