# Plan de Implementación 07 — Artefactos de Contexto

> **Origen:** Punto 7 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Estandarizar los artefactos `project-map.md` y `technical-analysis.md` como contratos del context gatherer.

---

## 1. Objetivo del plan

Crear dos contratos en `.agents/contracts/`:

1. `.agents/contracts/PROJECT_MAP.md` — estándar para el documento `project-map.md` de cada proyecto gobernado.
2. `.agents/contracts/TECHNICAL_ANALYSIS.md` — estándar para el documento `technical-analysis.md` de cada proyecto gobernado.

Estos contratos definirán:

- Estructura obligatoria y opcional.
- Audiencia.
- Cómo se generan y actualizan.
- Relación con `CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md` existentes.
- Cómo los workers deben usarlos.

---

## 2. Alcance

### Incluido
- Extracción de `example/project-map.md`.
- Extracción de `example/technical-analysis.md`.
- Definición de contratos en `.agents/contracts/`.
- Alineación con `CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md`.
- Actualización de `.agents/standards/INDEX.md`.

### Excluido
- No generar los artefactos reales del proyecto actual (eso ocurre en fase de discovery).
- No modificar `CONTEXT_ARTIFACT.md` salvo referencias.
- No modificar `KB_DISCOVERY_REPORT.md` salvo referencias.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/contracts/PROJECT_MAP.md` | Contrato del project-map. |
| `.agents/contracts/TECHNICAL_ANALYSIS.md` | Contrato del technical-analysis. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/INDEX.md` | Indexar contratos bajo contracts. |
| `.agents/contracts/CONTEXT_ARTIFACT.md` | Referenciar los nuevos contratos. |
| `.agents/contracts/KB_DISCOVERY_REPORT.md` | Referenciar los nuevos contratos. |
| `.agents/standards/conduct/OPERATIONAL_RULES.md` (Plan 01) | Referenciar project-map y technical-analysis en context awareness. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/project-map.md` | Fuente original. |
| `example/technical-analysis.md` | Fuente original. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer `example/project-map.md` completo.
2. Leer `example/technical-analysis.md` completo.
3. Leer `.agents/contracts/CONTEXT_ARTIFACT.md`.
4. Leer `.agents/contracts/KB_DISCOVERY_REPORT.md`.
5. Identificar:
   - Secciones comunes.
   - Información estructurada vs libre.
   - Dependencias entre ambos artefactos.
   - Cómo se actualizan.

### Paso 2 — Diseño de `PROJECT_MAP.md`
Estructura propuesta:

```markdown
# PROJECT_MAP.md

## 1. Propósito
## 2. Ubicación
## 3. Audiencia
## 4. Secciones obligatorias
### 4.1 Resumen del proyecto
### 4.2 Estructura de carpetas
### 4.3 Endpoints / puntos de entrada
### 4.4 Modelos / entidades principales
### 4.5 Flujos de negocio clave
### 4.6 Dependencias externas
### 4.7 Riesgos y supuestos
## 5. Secciones opcionales
## 6. Formato y mantenimiento
## 7. Cómo usar este artefacto
## 8. Relación con technical-analysis.md
```

### Paso 3 — Redacción de `PROJECT_MAP.md`

#### Sección 1 — Propósito
- Proveer una vista rápida y navegable del proyecto para workers y orchestrators.
- Servir como lectura obligatoria inicial (`MUST_READ`) en fase de discovery.

#### Sección 2 — Ubicación
- Ubicación sugerida: `<project-root>/project-map.md`.
- En proyectos con módulos grandes, puede existir uno por módulo.

#### Sección 3 — Audiencia
- Workers del protocolo.
- Orchestrator.
- Agentes de contexto.

#### Sección 4 — Secciones obligatorias

**4.1 Resumen del proyecto**
- Una a tres líneas describiendo qué hace el proyecto.

**4.2 Estructura de carpetas**
- Mapa de directorios relevantes con una línea de descripción por carpeta.

**4.3 Endpoints / puntos de entrada**
- Lista de endpoints, comandos o interfaces principales.

**4.4 Modelos / entidades principales**
- Entidades clave y sus relaciones breves.

**4.5 Flujos de negocio clave**
- Pasos principales de los flujos más importantes.

**4.6 Dependencias externas**
- Bases de datos, APIs, servicios, librerías críticas.

**4.7 Riesgos y supuestos**
- Lo que puede romperse y qué se asume.

#### Sección 5 — Secciones opcionales
- Diagramas.
- Glosario de términos.
- Decisiones arquitectónicas.
- Enlaces a documentación externa.

#### Sección 6 — Formato y mantenimiento
- Usar Markdown.
- Mantener actualizado cuando cambien estructura, endpoints o modelos.
- El context gatherer lo genera; cualquier worker lo actualiza si descubre inconsistencias.

#### Sección 7 — Cómo usar este artefacto
- Leer antes de planificar implementación.
- Consultar para entender impacto de cambios.
- Actualizar si se descubre información nueva.

#### Sección 8 — Relación con `technical-analysis.md`
- `project-map.md` es la vista rápida.
- `technical-analysis.md` es el análisis profundo.

### Paso 4 — Diseño de `TECHNICAL_ANALYSIS.md`
Estructura propuesta:

```markdown
# TECHNICAL_ANALYSIS.md

## 1. Propósito
## 2. Ubicación
## 3. Audiencia
## 4. Secciones obligatorias
### 4.1 Stack tecnológico
### 4.2 Arquitectura y patrones
### 4.3 Capas y dependencias
### 4.4 Integraciones externas
### 4.5 Seguridad
### 4.6 Testing
### 4.7 Riesgos técnicos
### 4.8 Deuda técnica
## 5. Secciones opcionales
## 6. Formato y mantenimiento
## 7. Cómo usar este artefacto
## 8. Relación con project-map.md
```

### Paso 5 — Redacción de `TECHNICAL_ANALYSIS.md`

#### Sección 1 — Propósito
- Proveer análisis profundo del stack, arquitectura, integraciones y riesgos técnicos.
- Servir como referencia para decisiones de diseño e implementación.

#### Sección 2 — Ubicación
- Ubicación sugerida: `<project-root>/technical-analysis.md`.

#### Sección 3 — Audiencia
- Workers de perfil técnico.
- Orchestrator en fases de design y planning.
- Perfiles de arquitectura.

#### Sección 4 — Secciones obligatorias

**4.1 Stack tecnológico**
- Lenguajes, frameworks, bases de datos, librerías principales, versiones.

**4.2 Arquitectura y patrones**
- Patrón arquitectónico adoptado (layered, clean, hexagonal, etc.).
- Decisiones clave.

**4.3 Capas y dependencias**
- Detalle de capas y cómo se relacionan.
- Puede referenciar `ARCHITECTURE_CONTRACT.md`.

**4.4 Integraciones externas**
- APIs, servicios, colas, eventos.
- Contratos y manejo de fallos.

**4.5 Seguridad**
- Autenticación, autorización, manejo de secretos, validaciones.

**4.6 Testing**
- Estrategia de testing, frameworks, cobertura esperada.

**4.7 Riesgos técnicos**
- Puntos de fragilidad, dependencias críticas, escenarios de fallo.

**4.8 Deuda técnica**
- Áreas conocidas que necesitan refactorización.

#### Sección 5 — Secciones opcionales
- Diagramas de arquitectura.
- Decisiones registradas (ADRs).
- Benchmarks.
- Plan de migración.

#### Sección 6 — Formato y mantenimiento
- Markdown, tablas para datos estructurados.
- Actualizar cuando cambie el stack o se identifiquen nuevos riesgos.

#### Sección 7 — Cómo usar este artefacto
- Consultar antes de diseñar cambios significativos.
- Usar como entrada para el contrato arquitectónico.
- Actualizar al detectar nuevos riesgos o deuda.

#### Sección 8 — Relación con `project-map.md`
- `technical-analysis.md` profundiza lo que `project-map.md` resume.

### Paso 6 — Actualización de contratos existentes
1. En `CONTEXT_ARTIFACT.md`, añadir nota sobre project-map y technical-analysis como artefactos de contexto de proyecto.
2. En `KB_DISCOVERY_REPORT.md`, añadir nota sobre cómo estos artefactos se alimentan del descubrimiento de KB.

### Paso 7 — Actualización del índice
1. Añadir `PROJECT_MAP.md` y `TECHNICAL_ANALYSIS.md` en `.agents/standards/INDEX.md`.

### Paso 8 — Referencia cruzada
1. En `OPERATIONAL_RULES.md` (Plan 01), en context awareness, listar project-map.md y technical-analysis.md como lecturas recomendadas.

### Paso 9 — Revisión final
1. Verificar que ambos contratos sean coherentes.
2. Confirmar que no se confundan con los artefactos reales del proyecto.
3. Validar que las secciones sean aplicables a cualquier tipo de proyecto.
4. Asegurar que no haya referencias a `pay_back`, Flask ni dominio específico.

---

## 5. Criterios de aceptación

- [ ] `PROJECT_MAP.md` existe y cubre las 8 secciones definidas.
- [ ] `TECHNICAL_ANALYSIS.md` existe y cubre las 8 secciones definidas.
- [ ] Ambos documentos definen ubicación sugerida, audiencia y formato.
- [ ] `CONTEXT_ARTIFACT.md` referencia ambos contratos.
- [ ] `KB_DISCOVERY_REPORT.md` referencia ambos contratos.
- [ ] `.agents/standards/INDEX.md` indexa ambos contratos.
- [ ] `OPERATIONAL_RULES.md` referencia ambos artefactos.
- [ ] No se generan los artefactos reales del proyecto en este plan.
- [ ] No hay referencias a dominio de pagos.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con `CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md`. | Posicionar los nuevos contratos como estándares de artefactos de proyecto, no como reemplazo. |
| Sobrecarga de secciones obligatorias. | Permitir secciones opcionales y adaptación al tamaño del proyecto. |
| Desactualización de los artefactos reales. | Establecer que cualquier worker debe actualizarlos al detectar cambios. |
| Confusión entre contrato y artefacto real. | Usar nombres claros: `PROJECT_MAP.md` es el contrato; `project-map.md` es el artefacto del proyecto. |

---

## 7. Dependencias

- Plan 01 completado.
- Plan 03 completado (technical-analysis puede referenciar `ARCHITECTURE_CONTRACT.md`).
- Acceso a `example/project-map.md` y `example/technical-analysis.md`.
- Acceso a `.agents/contracts/CONTEXT_ARTIFACT.md` y `KB_DISCOVERY_REPORT.md`.

---

## 8. Orden relativo de ejecución

Ejecutar **después del Plan 06 (Perfiles de Worker)** y **antes del Plan 08 (Plantillas de Proyecto)**, ya que las plantillas de proyecto pueden incluir ejemplos de project-map y technical-analysis.

---

## 9. Notas adicionales

- Considerar crear plantillas rellenables en `.agents/templates/` como parte del Plan 08.
- No se requiere ejecutar código en este plan.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `PROJECT_MAP.md` | Especificar el contrato del mapa rápido de proyecto. | Análisis técnico profundo; eso es responsabilidad de `TECHNICAL_ANALYSIS.md`. |
| `TECHNICAL_ANALYSIS.md` | Especificar el contrato del análisis técnico profundo. | Mapa rápido de navegación; eso es responsabilidad de `PROJECT_MAP.md`. |
| `CONTEXT_ARTIFACT.md` / `KB_DISCOVERY_REPORT.md` | Mantener sus responsabilidades originales de artifact de contexto y reporte de KB. | Solo referencian los nuevos contratos. |

**Principio aplicado:** los dos artefactos son complementarios. `PROJECT_MAP.md` responde a "¿dónde estoy y qué hay?"; `TECHNICAL_ANALYSIS.md` responde a "¿cómo funciona y qué riesgos tiene?". No solapan contenido.
