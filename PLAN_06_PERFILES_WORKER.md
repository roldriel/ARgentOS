# Plan de Implementación 06 — Perfiles de Worker

> **Origen:** Punto 6 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Crear perfiles de worker especializados reutilizables y actualizar el contrato de delegación para soportar `profile` en el payload.

---

## 1. Objetivo del plan

Crear un directorio `.agents/roles/profiles/` con perfiles de worker especializados basados en la estructura `ROLE.md` + `PROMPT.md` + `MUST_READ.md` de `example/.agents/roles/<rol>/`.

Perfiles iniciales:

1. `backend_engineer.md`
2. `database_engineer.md`
3. `integration_engineer.md`
4. `qa_engineer.md`
5. `tech_writer.md`
6. `functional_writer.md`

Además:

- Crear `.agents/roles/profiles/README.md` con índice.
- Actualizar `.agents/contracts/WORKER_DELEGATION_CONTRACT.md` para soportar `profile` en el payload.
- Asegurar que los perfiles sean opcionales y que el worker genérico siga funcionando.
- Reutilizar los módulos `_common/` de `example/` como contexto temático dentro de `.agents/roles/profiles/common/` o `.agents/standards/development/` según corresponda.

---

## 2. Alcance

### Incluido
- Extracción de la estructura de roles de `example/.agents/roles/<rol>/`.
- Creación de 6 perfiles iniciales.
- Creación de `README.md` de perfiles.
- Actualización del contrato de delegación.
- Actualización de `.agents/standards/INDEX.md`.

### Excluido
- No modificar `orchestrator.md` salvo referencia al catálogo de perfiles.
- No eliminar el worker genérico (`worker.md`).
- No implementar selección automática de perfiles.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/roles/profiles/README.md` | Índice y guía de uso de perfiles. |
| `.agents/roles/profiles/backend_engineer.md` | Perfil de ingeniero backend. |
| `.agents/roles/profiles/database_engineer.md` | Perfil de ingeniero de base de datos. |
| `.agents/roles/profiles/integration_engineer.md` | Perfil de especialista en integraciones. |
| `.agents/roles/profiles/qa_engineer.md` | Perfil de QA (incluye reglas de testing). |
| `.agents/roles/profiles/tech_writer.md` | Perfil de documentación técnica. |
| `.agents/roles/profiles/functional_writer.md` | Perfil de documentación funcional. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/contracts/WORKER_DELEGATION_CONTRACT.md` | Añadir campo `profile` al payload. |
| `.agents/standards/INDEX.md` | Indexar perfiles bajo roles. |
| `.agents/roles/orchestrator.md` | Referenciar catálogo de perfiles. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.agents/roles/backend_python/` | Estructura de perfil backend. |
| `example/.agents/roles/database_mysql/` | Estructura de perfil DB. |
| `example/.agents/roles/integration_specialist/` | Estructura de perfil integración. |
| `example/.agents/roles/qa_engineer/` | Estructura de perfil QA. |
| `example/.agents/roles/tech_writer/` | Estructura de perfil tech writer. |
| `example/.agents/roles/func_writer/` | Estructura de perfil func writer. |
| `example/.agents/roles/_common/` | Módulos comunes reutilizables. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer cada directorio de rol en `example/.agents/roles/`.
2. Leer `.agents/contracts/WORKER_DELEGATION_CONTRACT.md`.
3. Identificar:
   - Lecturas obligatorias por perfil.
   - Restricciones específicas.
   - Plantillas de prompt.
   - Módulos `_common/` reutilizables.

### Paso 2 — Diseño de la estructura de perfiles
Cada perfil será un único archivo Markdown con secciones:

```markdown
# <Nombre del perfil>

## 1. Propósito
## 2. Cuándo usar
## 3. Lecturas obligatorias (MUST_READ)
## 4. Restricciones
## 5. Herramientas permitidas
## 6. Criterios de aceptación
## 7. Output esperado
## 8. Relación con otros perfiles
## 9. Plantilla de prompt
```

### Paso 3 — Redacción de perfiles

#### backend_engineer.md
- Propósito: implementar lógica de negocio, endpoints, servicios.
- MUST_READ: `OPERATIONAL_RULES.md`, `OUTPUT_EFFICIENCY.md`, `ARCHITECTURE_CONTRACT.md` (si aplica), `TDD.md`.
- Restricciones: respetar capas, no mezclar responsabilidades, no ejecutar tests sin instrucción.
- Herramientas: Shell, ReadFile, WriteFile, StrReplaceFile, Grep, Glob.
- Plantilla de prompt: objetivo, capa, entradas/salidas, dependencias, tests.

#### database_engineer.md
- Propósito: diseñar esquemas, migraciones, queries, índices.
- MUST_READ: `OPERATIONAL_RULES.md`, `ARCHITECTURE_CONTRACT.md` (capa Models/Providers), reglas del proyecto sobre migraciones.
- Restricciones: no borrar datos sin backup, no ejecutar migraciones sin instrucción, no modificar esquemas en producción.
- Herramientas: Shell, ReadFile, WriteFile, Grep.
- Plantilla de prompt: entidades, relaciones, migraciones, riesgos, rollback.

#### integration_engineer.md
- Propósito: integrar sistemas externos, APIs, providers.
- MUST_READ: `OPERATIONAL_RULES.md`, reglas de seguridad de interacciones externas, `ARCHITECTURE_CONTRACT.md` (capa Providers).
- Restricciones: no llamar endpoints reales sin autorización, no exponer credenciales, usar mocks cuando sea posible.
- Herramientas: Shell, ReadFile, WriteFile, curl (solo si autorizado).
- Plantilla de prompt: sistema externo, contrato, mocks, manejo de errores, idempotencia.

#### qa_engineer.md
- Propósito: definir alcance de tests, diseñar casos, verificar cobertura.
- MUST_READ: `OPERATIONAL_RULES.md`, `TDD.md`, `RUBRICS.md`.
- Reglas propias del perfil (específicas de QA, no duplicar un estándar general futuro):
  - No ejecutar `pytest` sin instrucción explícita.
  - No modificar código funcional sin autorización.
  - Patrones de mock y cobertura mínima esperada.
- Herramientas: ReadFile, Grep, Shell (solo lectura).
- Plantilla de prompt: alcance, casos de prueba, mocks, cobertura mínima, criterios de aceptación.

> **SRP:** Si en el futuro se crea `.agents/standards/testing/TESTING_RULES.md` como estándar transversal, este perfil pasará a **referenciarlo** en lugar de contener las reglas generales. El perfil QA se reserva entonces las *adaptaciones del estándar a su rol*.

#### tech_writer.md
- Propósito: documentación técnica para devs/agentes.
- MUST_READ: `OPERATIONAL_RULES.md`, `OUTPUT_EFFICIENCY.md`, `PROJECT_MAP.md`, `TECHNICAL_ANALYSIS.md`.
- Restricciones: no asumir conocimiento del lector, mantener ejemplos actualizados.
- Herramientas: ReadFile, WriteFile.
- Plantilla de prompt: audiencia, formato, secciones obligatorias, ejemplos.

#### functional_writer.md
- Propósito: documentación funcional para negocio.
- MUST_READ: `OPERATIONAL_RULES.md`, `DOMAIN_CHEATSHEET_TEMPLATE.md` (Plan 08), `PROJECT_MAP.md`.
- Restricciones: no usar jerga técnica sin explicar, enfocarse en el "qué" y el "por qué".
- Herramientas: ReadFile, WriteFile.
- Plantilla de prompt: proceso de negocio, actores, reglas, excepciones, glosario.

### Paso 4 — Creación del README.md de perfiles
Contenido mínimo:
- Introducción: qué son los perfiles y cuándo usarlos.
- Lista de perfiles con enlace y una línea de descripción.
- Instrucciones para el orchestrator sobre cómo elegir un perfil.
- Nota de que los perfiles son opcionales.
- Guía para añadir nuevos perfiles.

### Paso 5 — Actualización del contrato de delegación
1. Abrir `.agents/contracts/WORKER_DELEGATION_CONTRACT.md`.
2. Añadir al payload:
   ```markdown
   - **profile** (opcional): nombre del perfil de worker a usar. Si no se especifica, se usa el worker genérico.
   ```
3. Añadir sección de perfiles con referencia a `.agents/roles/profiles/README.md`.
4. Especificar que el perfil determina las lecturas obligatorias y restricciones adicionales.

### Paso 6 — Actualización del orchestrator
1. En `.agents/roles/orchestrator.md`, añadir nota sobre el catálogo de perfiles.
2. Indicar que el orchestrator puede elegir un perfil basándose en la guía de orquestación.

### Paso 7 — Actualización del índice
1. Añadir entrada de perfiles en `.agents/standards/INDEX.md`.

### Paso 8 — Revisión final
1. Verificar que todos los perfiles tengan la misma estructura.
2. Confirmar que no se dupliquen reglas con `OPERATIONAL_RULES.md`.
3. Validar que el contrato de delegación siga siendo compatible con worker genérico.
4. Asegurar que no haya referencias a proyecto específico.

---

## 5. Criterios de aceptación

- [ ] Existen 6 perfiles iniciales en `.agents/roles/profiles/`.
- [ ] Cada perfil cubre las 9 secciones definidas.
- [ ] Existe `README.md` con índice e instrucciones.
- [ ] `WORKER_DELEGATION_CONTRACT.md` soporta el campo `profile`.
- [ ] `orchestrator.md` referencia el catálogo de perfiles.
- [ ] `.agents/standards/INDEX.md` indexa los perfiles.
- [ ] El worker genérico sigue siendo la opción por defecto.
- [ ] No se elimina ni modifica `worker.md`.
- [ ] No hay referencias a `pay_back`, Flask ni dominio específico.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Sobrecarga de contexto por perfiles. | Cada perfil lee solo su MUST_READ; el resto se referencia. |
| Duplicación con roles genéricos. | Los perfiles extienden al worker genérico; no lo reemplazan. |
| Confusión sobre cuándo usar cada perfil. | El README y la guía de orquestación deben ser claros. |
| Mantenimiento de muchos perfiles. | Empezar con 6 perfiles bien definidos; añadir más solo con necesidad clara. |

---

## 7. Dependencias

- Plan 01 completado.
- Plan 03 completado (perfiles backend/database/integration usan `ARCHITECTURE_CONTRACT.md`).
- Plan 04 completado (la guía de orquestación decide el perfil).
- Plan 05 completado (los prompts de perfil pueden usar tags).
- Acceso a todos los directorios de roles de `example/`.
- Acceso a `.agents/contracts/WORKER_DELEGATION_CONTRACT.md`.

---

## 8. Orden relativo de ejecución

Ejecutar **después del Plan 05 (Context Engineering)** y **antes del Plan 07 (Artefactos de Contexto)** y **Plan 08 (Plantillas de Proyecto)**, ya que algunos perfiles referencian esos artefactos.

---

## 9. Notas adicionales

- Considerar unificar partes comunes de los perfiles en `.agents/roles/profiles/common/` para evitar duplicación.
- No se requiere ejecutar código en este plan.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| Cada `<perfil>.md` | Definir las reglas, lecturas y restricciones de un rol técnico específico. | Reglas generales del protocolo (están en `OPERATIONAL_RULES.md`) ni definiciones de otros roles. |
| `WORKER_DELEGATION_CONTRACT.md` | Especificar el formato de delegación de trabajo. | Lógica interna de cada perfil; solo añade el campo `profile` al payload. |
| `README.md` de perfiles | Índice y guía de uso del catálogo. | Contenido normativo de perfiles. |
| `orchestrator.md` / `worker.md` | Roles genéricos. | No asumen responsabilidades de los perfiles; los referencian. |

**Principio aplicado:** cada perfil tiene una única razón de cambio: "cambiar las reglas de ese rol técnico específico". El contrato de delegación no crece con lógica de perfiles; solo los habilita mediante un campo opcional.
