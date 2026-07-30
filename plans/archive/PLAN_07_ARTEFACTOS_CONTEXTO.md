# Plan de Implementación 07 — Artefactos de Contexto

> **Origen:** Punto 7 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Estandarizar los artefactos `project-map.md` y `technical-analysis.md` como documentos de contexto de proyecto, y su relación con los contratos de protocolo existentes.

---

## 1. Objetivo del plan

Crear el estándar `.agents/standards/context/PROJECT_ARTIFACTS.md` que defina:

1. Estructura de `project-map.md`.
2. Estructura de `technical-analysis.md`.
3. Ubicación exacta de los artefactos reales en un proyecto.
4. Audiencia de cada artefacto.
5. Cómo se generan y actualizan.
6. Relación con `CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md`.
7. Cómo los workers deben usarlos.

**Este plan no crea los artefactos reales del proyecto.** Solo define el contrato/estándar que los gobierna.

**Decisión de arquitectura:** los artefactos `project-map.md` y `technical-analysis.md` son entregables del proyecto, no outputs del protocolo. Por eso su especificación vive en `.agents/standards/context/` y no en `.agents/contracts/`, que está reservado para artefactos que el protocolo genera (`CONTEXT_ARTIFACT.md`, `KB_DISCOVERY_REPORT.md`, etc.).

---

## 2. Alcance

### Incluido
- Resolución de la inconsistencia entre el ejemplo del README (ABM de usuarios) y los artefactos actuales de `example/` (PayBack Microservice).
- Definición del estándar `.agents/standards/context/PROJECT_ARTIFACTS.md`.
- Definición de secciones base obligatorias y secciones opcionales condicionales.
- Definición de triggers de actualización de los artefactos reales.
- Alineación con `CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md`.
- Verificación de que `OPERATIONAL_RULES.md` ya referencia ambos artefactos.

### Excluido
- No generar los artefactos reales del proyecto actual (eso ocurre en fase de discovery o en el Plan 08 de plantillas).
- No modificar `CONTEXT_ARTIFACT.md` salvo referencias explícitas si son necesarias.
- No modificar `KB_DISCOVERY_REPORT.md` (no es un índice de artefactos de proyecto).
- No crear plantillas de proyecto dentro de `.agents/`.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/context/PROJECT_ARTIFACTS.md` | Estándar que define `project-map.md` y `technical-analysis.md`. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/INDEX.md` | Añadir `PROJECT_ARTIFACTS.md` bajo la sección `## Context`. |
| `.agents/standards/context/CONTEXT.md` | Referenciar `PROJECT_ARTIFACTS.md` como fuente de artefactos de proyecto. |
| `.agents/contracts/CONTEXT_ARTIFACT.md` | Referenciar `PROJECT_ARTIFACTS.md` si es relevante para el contexto de proyecto. |
| `example/project-map.md` | Mover a `example/<nombre-del-ejemplo>/project-map.md` o eliminar si es inconsistente con el README. |
| `example/technical-analysis.md` | Mover a `example/<nombre-del-ejemplo>/technical-analysis.md` o eliminar si es inconsistente con el README. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/project-map.md` | Fuente observada para identificar secciones recurrentes. |
| `example/technical-analysis.md` | Fuente observada para identificar secciones recurrentes. |
| `.agents/contracts/CONTEXT_ARTIFACT.md` | Contrato de artefacto temporal por tarea. |
| `.agents/contracts/KB_DISCOVERY_REPORT.md` | Contrato de reporte de KB por tarea. |
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Verificar que ya referencia `project-map.md` y `technical-analysis.md`. |

---

## 4. Pasos de implementación

### Paso 1 — Resolución de la inconsistencia del ejemplo
1. Leer `README.md` y confirmar qué ejemplo es el canónico: ABM de usuarios o PayBack Microservice.
2. Decidir una de estas dos opciones y documentarla en el plan de ejecución:
   - **Opción A:** Conservar solo el ejemplo de ABM de usuarios y eliminar/mover los artefactos de PayBack.
   - **Opción B:** Conservar ambos ejemplos en subdirectorios separados: `example/flask-abm-users/` y `example/payback-microservice/`.
3. Ejecutar la opción elegida antes de continuar con el Paso 2.

### Paso 2 — Análisis de fuentes
1. Leer el `project-map.md` del ejemplo canónico.
2. Leer el `technical-analysis.md` del ejemplo canónico.
3. Leer `.agents/contracts/CONTEXT_ARTIFACT.md`.
4. Leer `.agents/contracts/KB_DISCOVERY_REPORT.md`.
5. Leer `.agents/standards/conduct/OPERATIONAL_RULES.md` (sección 5.1).
6. Identificar:
   - Secciones que son recurrentes en cualquier proyecto (independientes del dominio).
   - Información estructurada vs libre.
   - Dependencias entre `project-map.md` y `technical-analysis.md`.
   - Solapamientos a eliminar.

### Paso 3 — Diseño de `PROJECT_ARTIFACTS.md`
Estructura del estándar:

```markdown
# PROJECT_ARTIFACTS.md

## 1. Propósito
## 2. Artefactos cubiertos
### 2.1 project-map.md
### 2.2 technical-analysis.md
## 3. Ubicación de los artefactos reales
## 4. Audiencia
## 5. project-map.md
### 5.1 Secciones obligatorias (base)
### 5.2 Secciones opcionales (condicionales)
### 5.3 Cómo usarlo
## 6. technical-analysis.md
### 6.1 Secciones obligatorias (base)
### 6.2 Secciones opcionales (condicionales)
### 6.3 Cómo usarlo
## 7. Formato y mantenimiento
### 7.1 Formato
### 7.2 Triggers de actualización
### 7.3 Responsable de actualización
## 8. Relación con otros contratos
### 8.1 CONTEXT_ARTIFACT.md
### 8.2 KB_DISCOVERY_REPORT.md
## 9. Plantillas de ejemplo
```

### Paso 4 — Redacción de `PROJECT_ARTIFACTS.md`

#### 5.1 `project-map.md` — secciones obligatorias (base)

1. **Resumen del proyecto**
   - Una a tres líneas describiendo qué hace el proyecto.

2. **Estructura de carpetas**
   - Mapa de directorios relevantes con una línea de descripción por carpeta.

3. **Puntos de entrada**
   - Lista de endpoints, comandos o interfaces principales.
   - Formato tabla: nombre, ubicación/URL, descripción.

4. **Componentes principales**
   - Entidades, modelos, servicios o módulos clave.
   - Relación breve entre componentes.

#### 5.2 `project-map.md` — secciones opcionales (condicionales)

- **Diagramas** (si el proyecto tiene más de dos capas).
- **Glosario de términos** (si el dominio usa vocabulario no trivial).
- **Decisiones arquitectónicas** (si difieren de los estándares por defecto).
- **Enlaces a documentación externa** (si existe documentación fuera del repo).

#### 6.1 `technical-analysis.md` — secciones obligatorias (base)

1. **Stack tecnológico**
   - Lenguajes, frameworks, bases de datos, librerías principales, versiones.

2. **Arquitectura y patrones**
   - Patrón arquitectónico adoptado (layered, clean, hexagonal, etc.).
   - Decisiones clave.

3. **Integraciones externas**
   - APIs, servicios, colas, eventos.
   - Contratos y manejo de fallos básico.

4. **Riesgos técnicos y deuda técnica**
   - Puntos de fragilidad, dependencias críticas, escenarios de fallo.
   - Áreas conocidas que necesitan refactorización.

#### 6.2 `technical-analysis.md` — secciones opcionales (condicionales)

- **Seguridad** (si el proyecto maneja autenticación, autorización o secretos).
- **Testing** (si existe una estrategia de testing definida).
- **Diagramas de arquitectura** (si aportan claridad).
- **ADRs** (si existen decisiones registradas formalmente).
- **Benchmarks** (si hay mediciones de performance relevantes).
- **Plan de migración** (si hay migraciones en curso o planificadas).

#### 7. Formato y mantenimiento

- **Formato:** Markdown. Tablas para datos estructurados.
- **Ubicación:** `<project-root>/project-map.md` y `<project-root>/technical-analysis.md`.
- **Triggers de actualización obligatorios:**
  1. Un worker modifica la estructura de carpetas del proyecto.
  2. Un worker agrega, elimina o cambia endpoints, comandos o interfaces principales.
  3. Un worker agrega, elimina o renombra modelos, entidades o servicios principales.
  4. Un worker cambia el stack tecnológico, arquitectura o integraciones externas.
  5. Un worker identifica un nuevo riesgo técnico o deuda técnica.
- **Responsable de actualización:** el worker que realiza el cambio. Si no es seguro, el worker debe reportarlo como parte de la entrega.
- **Validación:** en la fase de review, verificar que los cambios en código estén reflejados en los artefactos si corresponde.

#### 8. Relación con otros contratos

- **`CONTEXT_ARTIFACT.md`:** es el artefacto temporal que un context gatherer produce para una tarea específica. Puede citar `project-map.md` y `technical-analysis.md` como fuentes, pero no los reemplaza.
- **`KB_DISCOVERY_REPORT.md`:** es el reporte de entradas de KB recomendadas para la tarea actual. No referencia artefactos de proyecto de forma permanente.

#### 9. Plantillas de ejemplo

El estándar incluirá bloques de template mínimo para `project-map.md` y `technical-analysis.md`. Estos templates no contienen nombres de dominio.

### Paso 5 — Actualización de `.agents/standards/INDEX.md`
1. Añadir entrada en la sección `## Context`:
   - `context/PROJECT_ARTIFACTS.md` — estándar para los artefactos de proyecto `project-map.md` y `technical-analysis.md`.

### Paso 6 — Referencia en `.agents/standards/context/CONTEXT.md`
1. Añadir una nota que cite `PROJECT_ARTIFACTS.md` como el estándar que gobierna los artefactos de contexto persistente del proyecto.

### Paso 7 — Verificación de `OPERATIONAL_RULES.md`
1. Confirmar que la sección 5.1 de `OPERATIONAL_RULES.md` ya menciona `project-map.md` y `technical-analysis.md` como archivos de contexto a leer.
2. Si no los menciona, añadir la referencia.
3. Si ya los menciona, no realizar cambios.

### Paso 8 — Referencia en `CONTEXT_ARTIFACT.md` (solo si aplica)
1. Añadir una nota en `CONTEXT_ARTIFACT.md` indicando que el contexto de proyecto puede provenir de `project-map.md` y `technical-analysis.md`, gobernados por `PROJECT_ARTIFACTS.md`.
2. No modificar la estructura de `CONTEXT_ARTIFACT.md`.

### Paso 9 — Reubicación de los ejemplos
1. Mover los ejemplos actuales a una estructura coherente:
   - Si se elige la Opción A: eliminar `example/project-map.md` y `example/technical-analysis.md` si no corresponden al ejemplo canónico.
   - Si se elige la Opción B: moverlos a `example/payback-microservice/project-map.md` y `example/payback-microservice/technical-analysis.md`.

### Paso 10 — Revisión final
1. Verificar que `PROJECT_ARTIFACTS.md` no contenga nombres propios de dominio (como "PayBack", "preorder", "payment", "CPE", etc.).
2. Verificar que las secciones base sean aplicables a un proyecto mínimo (ej: ABM de usuarios Flask).
3. Verificar que no existan solapamientos entre `project-map.md` y `technical-analysis.md`.
4. Verificar que los triggers de actualización sean accionables.
5. Verificar que `PROJECT_ARTIFACTS.md` no viva en `.agents/contracts/`.

---

## 5. Criterios de aceptación

- [ ] `PROJECT_ARTIFACTS.md` existe en `.agents/standards/context/`.
- [ ] `PROJECT_ARTIFACTS.md` define ubicación exacta: `<project-root>/project-map.md` y `<project-root>/technical-analysis.md`.
- [ ] `PROJECT_ARTIFACTS.md` define exactamente 4 secciones obligatorias para `project-map.md`.
- [ ] `PROJECT_ARTIFACTS.md` define exactamente 4 secciones obligatorias para `technical-analysis.md`.
- [ ] `PROJECT_ARTIFACTS.md` lista secciones opcionales con condiciones de activación.
- [ ] `PROJECT_ARTIFACTS.md` define al menos 5 triggers de actualización concretos.
- [ ] `PROJECT_ARTIFACTS.md` define responsable de actualización: el worker que realiza el cambio.
- [ ] `.agents/standards/INDEX.md` indexa `PROJECT_ARTIFACTS.md` bajo `## Context`.
- [ ] `.agents/standards/context/CONTEXT.md` referencia `PROJECT_ARTIFACTS.md`.
- [ ] `.agents/contracts/CONTEXT_ARTIFACT.md` referencia `PROJECT_ARTIFACTS.md` solo si aplica.
- [ ] `OPERATIONAL_RULES.md` referencia `project-map.md` y `technical-analysis.md` (ya lo hace; verificar que siga vigente).
- [ ] No se generan los artefactos reales del proyecto en este plan.
- [ ] `PROJECT_ARTIFACTS.md` no contiene nombres propios de dominio de pagos.
- [ ] Los ejemplos de `example/` se reubican según la Opción A o B del Paso 1.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con `README.md`. | `project-map.md` se enfoca en navegación técnica; `README.md` se enfoca en instalación y uso inicial. Si hay duplicación, el README debe apuntar a `project-map.md`. |
| Duplicación con `CONTEXT_ARTIFACT.md`. | `CONTEXT_ARTIFACT.md` es temporal por tarea; `project-map.md` es persistente por proyecto. Mantener separados sus ciclos de vida. |
| Sobrecarga de secciones obligatorias. | Usar 4 secciones base obligatorias y el resto opcional condicional. Probar con un proyecto mínimo antes de aprobar. |
| Desactualización de los artefactos reales. | Establecer triggers de actualización vinculados a cambios concretos de código, y verificar en review. |
| Confusión entre contrato y artefacto real. | El estándar se llama `PROJECT_ARTIFACTS.md`; los artefactos reales se llaman `project-map.md` y `technical-analysis.md`. Nunca se llaman igual. |
| Ejemplo inconsistente con el README. | Resolver en el Paso 1 antes de continuar. |

---

## 7. Dependencias

- Acceso a `example/project-map.md` y `example/technical-analysis.md`.
- Acceso a `.agents/contracts/CONTEXT_ARTIFACT.md`.
- Acceso a `.agents/contracts/KB_DISCOVERY_REPORT.md` (solo lectura; no se modifica).
- Acceso a `.agents/standards/INDEX.md`.
- Acceso a `.agents/standards/context/CONTEXT.md`.
- Acceso a `.agents/standards/conduct/OPERATIONAL_RULES.md`.

**No depende de Plan 01 ni Plan 03**, salvo que se requiera una referencia explícita a `ARCHITECTURE_CONTRACT.md`. Si dicha referencia es necesaria, agregar `Plan 03 completado` como dependencia en el momento de la ejecución.

---

## 8. Orden relativo de ejecución

- Ejecutar **después de que el Plan 06 (Perfiles de Worker)** haya definido qué perfiles consumen estos artefactos.
- Ejecutar **en paralelo con el Plan 08 (Plantillas de Proyecto)**, con un hito de sincronización:
  - Plan 07 debe entregar el template mínimo de `project-map.md` y `technical-analysis.md` antes de que Plan 08 genere plantillas de proyecto completas.
- No es un prerrequisito estricto de Plan 08; es un acoplamiento de contenido.

---

## 9. Notas adicionales

- Las plantillas rellenables de proyecto deben vivir en `templates/project-map.template.md` y `templates/technical-analysis.template.md` dentro del proyecto concreto, o en `example/<nombre-del-ejemplo>/templates/` para los ejemplos. **No deben vivir en `.agents/templates/`** porque son específicas del proyecto.
- No se requiere ejecutar código en este plan.
- El estándar debe ser validado contra al menos un proyecto mínimo (ABM de usuarios Flask) y un proyecto mediano antes de considerarse estable.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `PROJECT_ARTIFACTS.md` | Especificar el formato, contenido y mantenimiento de `project-map.md` y `technical-analysis.md`. | Contenido de dominio de proyectos específicos. |
| `project-map.md` | Responder "¿qué componentes existen y dónde están?". | Análisis profundo de riesgos, deuda técnica o decisiones arquitectónicas; eso va en `technical-analysis.md`. |
| `technical-analysis.md` | Responder "¿cómo funciona y qué riesgos técnicos tiene?". | Mapa de navegación de carpetas o lista de endpoints sin análisis; eso va en `project-map.md`. |
| `CONTEXT_ARTIFACT.md` | Mantener la responsabilidad de artefacto temporal de contexto por tarea. | Solo referencia `PROJECT_ARTIFACTS.md` si es necesario. |
| `KB_DISCOVERY_REPORT.md` | Mantener la responsabilidad de reporte de recomendaciones de KB por tarea. | No referencia artefactos de proyecto de forma permanente. |

**Principio aplicado:** los dos artefactos son complementarios. `project-map.md` responde a "¿dónde estoy y qué hay?"; `technical-analysis.md` responde a "¿cómo funciona y qué riesgos tiene?". `PROJECT_ARTIFACTS.md` es el estándar que define ambos. No solapan contenido.
