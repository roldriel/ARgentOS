# Plan de Implementación 03 — Arquitectura

> **Origen:** Punto 3 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Crear un contrato arquitectónico consolidado, aplicable y opt-in, que convierta los estándares existentes de arquitectura en reglas ejecutables por el worker.

---

## 1. Objetivo del plan

Crear `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` como estándar del protocolo ARgentOS que operativiza las reglas arquitectónicas para los proyectos gobernados. El documento contendrá:

- Definición explícita de capas arquitectónicas.
- Reglas de dependencia duras entre capas.
- Prohibiciones de bypass y mezcla de patrones.
- Naming suffixes obligatorios.
- File identity: línea 1 de cada archivo con su ruta desde la raíz del proyecto (p. ej. `# apps/payments/services/payment_service.py`), no como ruta del sistema de archivos.
- Imports absolutos desde la raíz del proyecto; imports relativos prohibidos.
- Mecanismo de auto-verificación arquitectónica antes de generar código.
- Naturaleza opt-in: el contrato solo se aplica a un proyecto cuando éste lo declara explícitamente (ver punto 2).

El contrato no duplicará `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `SCREAMING_ARCHITECTURE.md`, `DDD_TACTICAL.md`, etc.; los consumirá y los convertirá en reglas ejecutables por el worker.

> **Restricción de gobernanza:** Este plan modifica archivos dentro de `.agents/`. Según `PROTOCOL_BOUNDARIES.md`, cualquier cambio en `.agents/` requiere acuerdo explícito del usuario y debe quedar documentado.

---

## 2. Alcance

### Incluido
- Extracción de:
  - `example/.claude/rules/ARCHITECTURE.md`
  - `example/.agents/roles/_common/ARCHITECTURE_LAYERS.md`
  - `example/.agents/roles/_common/ARCHITECTURE_NAMING.md`
  - `example/.agents/roles/_common/ARCHITECTURE_PROHIBITIONS.md`
- Consolidación de las fuentes anteriores en `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
- Definición del mecanismo de activación opt-in:
  - Feature flag `architecture_contract` en `.agents/features.toml` (default `false`).
  - Declaración explícita en `TASK_SPECIFICATION.md`.
- Actualización de `.agents/standards/INDEX.md` para indexar el nuevo contrato y el feature flag.
- Adición de una **nota final de referencia** (sin modificar el cuerpo principal) en:
  - `.agents/standards/development/design/LAYERED_ARCHITECTURE.md`
  - `.agents/standards/development/design/CLEAN_ARCHITECTURE.md`
  - `.agents/standards/development/design/DDD_TACTICAL.md`
  - `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md`

### Excluido
- No modificar el cuerpo principal de los estándares arquitectónicos existentes.
- No imponer el contrato a todos los proyectos gobernados; su aplicación es opt-in.
- No crear código de verificación automatizada en este plan.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Contrato arquitectónico operativo. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/features.toml` | Añadir el feature flag `architecture_contract = false`. |
| `.agents/standards/INDEX.md` | Indexar el nuevo contrato bajo design y el feature flag correspondiente. |
| `.agents/standards/development/design/LAYERED_ARCHITECTURE.md` | Añadir nota final que referencie el contrato como aplicación operativa. |
| `.agents/standards/development/design/CLEAN_ARCHITECTURE.md` | Añadir nota final que referencie el contrato como aplicación operativa. |
| `.agents/standards/development/design/DDD_TACTICAL.md` | Añadir nota final que referencie el contrato como aplicación operativa. |
| `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md` | Añadir nota final que referencie el contrato como aplicación operativa. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.claude/rules/ARCHITECTURE.md` | Fuente consolidada. |
| `example/.agents/roles/_common/ARCHITECTURE_LAYERS.md` | Fuente de capas. |
| `example/.agents/roles/_common/ARCHITECTURE_NAMING.md` | Fuente de naming. |
| `example/.agents/roles/_common/ARCHITECTURE_PROHIBITIONS.md` | Fuente de prohibiciones. |
| `.agents/standards/development/design/LAYERED_ARCHITECTURE.md` | Evitar contradicciones con capas horizontales. |
| `.agents/standards/development/design/CLEAN_ARCHITECTURE.md` | Evitar contradicciones con dependencias hacia adentro. |
| `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md` | Alinear organización por dominio. |
| `.agents/standards/development/design/DDD_TACTICAL.md` | Alinear entidades, value objects y agregados. |
| `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` | Reglas de gobernanza para modificar `.agents/`. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer los cuatro archivos de arquitectura de `example/`.
2. Leer los estándares existentes de `.agents/standards/development/design/`.
3. Leer `.agents/features.toml` para comprender el formato y ubicación de los feature flags.
4. Leer `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` para confirmar las restricciones de modificación en `.agents/`.
5. Identificar:
   - Cuántas capas se definen.
   - Qué dependencias se permiten.
   - Qué naming suffixes se exigen.
   - Qué prohibiciones existen.
   - Cómo se verifica la arquitectura.

### Paso 2 — Diseño del contrato
Estructura propuesta:

```markdown
# ARCHITECTURE_CONTRACT.md

## 1. Propósito y alcance
## 2. Activación
## 3. Capas arquitectónicas
## 4. Reglas de dependencia
## 5. Naming suffixes
## 6. File identity
## 7. Prohibiciones
## 8. Auto-verificación
## 9. Relación con otros estándares
## 10. Ejemplos
```

### Paso 3 — Redacción del contenido

#### Sección 1 — Propósito y alcance
- Este documento es un contrato operativo que aplica los principios de arquitectura definidos en otros estándares.
- Es opt-in: el proyecto gobernado debe declarar que lo adopta.
- Aplica a todo código generado o modificado por workers mientras el contrato esté activo.

#### Sección 2 — Activación
Definir al menos una de estas formas:
- Feature flag `architecture_contract` habilitado en `.agents/features.toml` o vía variable de entorno `AGENTS_FEATURE_ARCHITECTURE_CONTRACT=true`.
- Declaración explícita en `TASK_SPECIFICATION.md`:
  ```markdown
  ## Arquitectura
  Este proyecto adopta `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
  ```

#### Sección 3 — Capas arquitectónicas
Definir capas de ejemplo basadas en `example/`:

| Capa | Responsabilidad | Sufijos |
|------|-----------------|---------|
| Views | Interfaz de entrada | `View` |
| Validators | Validación de entrada | `Validator` |
| Schemas | Serialización/deserialización | `Schema` |
| Services | Lógica de negocio | `Service` |
| Models | Entidades y persistencia | `Model` |
| Providers | Adaptadores externos | `Provider` |
| Domain Errors | Excepciones de dominio | `Error`, `Exception` |

Nota: el proyecto puede adaptar las capas al activar el contrato, pero debe documentar la equivalencia de responsabilidades, sufijos y reglas de dependencia. No puede reducir la lista mínima de sufijos ni eliminar reglas duras.

#### Sección 4 — Reglas de dependencia
- Las dependencias permitidas son:
  ```text
  Views → Validators → Schemas
  Views → Services → Models
  Services → Providers → External APIs
  ```
- Las dependencias prohibidas son:
  - Views → Models
  - Views → Providers
  - Validators → Services
  - Validators → Providers
  - Schemas → Validators o Services
  - Providers → Models
  - Models → cualquier capa superior
- Los providers actúan como adaptadores: no contienen lógica de negocio ni acceden directamente a modelos.
- La lógica de negocio no puede depender de frameworks de infraestructura.

Incluir un diagrama ASCII o tabla que visualice la matriz de dependencias permitidas y prohibidas.

#### Sección 5 — Naming suffixes
- Cada archivo/clase debe tener un sufijo que indique su capa.
- Lista mínima: `View`, `Validator`, `Schema`, `Service`, `Provider`, `Error`/`Exception`.
- El proyecto puede extender la lista, pero no reducirla.

#### Sección 6 — File identity
- Línea 1 de cada archivo: comentario con la ruta del archivo desde la raíz del proyecto.
  ```python
  # apps/payments/services/payment_service.py
  ```
- Imports absolutos obligatorios desde la raíz del proyecto; imports relativos prohibidos.
- Un archivo = una responsabilidad principal.

#### Sección 7 — Prohibiciones
- No mezclar lógica de capas en un mismo archivo.
- No importar infraestructura desde dominio/servicios.
- No usar nombres genéricos sin sufijo (`Manager`, `Helper`, `Utils` como clase principal).
- No bypassear validadores desde views.
- No acceder a modelos directamente desde views.
- No realizar refactors arquitectónicos implícitos.
- No mezclar patrones arquitectónicos dentro de una misma tarea.

#### Sección 8 — Auto-verificación
Antes de generar o modificar código, el worker debe:
1. Identificar la capa del archivo.
2. Verificar que sus dependencias solo apuntan a capas permitidas.
3. Confirmar que el nombre cumple el sufijo.
4. Confirmar que la línea 1 tiene file identity.
5. Revisar que no viole prohibiciones.

Incluir un checklist mínimo de auto-verificación.

#### Sección 9 — Relación con otros estándares
- `LAYERED_ARCHITECTURE.md`: principios teóricos de capas.
- `CLEAN_ARCHITECTURE.md`: principios de independencia de frameworks.
- `SCREAMING_ARCHITECTURE.md`: naming que refleje dominio.
- `DDD_TACTICAL.md`: entidades, value objects, agregados.
- Este contrato las une en reglas aplicables.
- En caso de conflicto, prevalece el estándar canónico correspondiente.

#### Sección 10 — Ejemplos
Incluir al menos:
- Un ejemplo de archivo bien estructurado.
- Un ejemplo de dependencia permitida.
- Un ejemplo de violación y cómo corregirla.

### Paso 4 — Actualización del feature flag
1. Abrir `.agents/features.toml`.
2. Añadir `architecture_contract = false` bajo `[features]`.
3. Verificar que el flag pueda ser sobreescrito vía `AGENTS_FEATURE_ARCHITECTURE_CONTRACT`.

### Paso 5 — Actualización de estándares existentes
1. En cada uno de estos estándares, añadir una nota final sin modificar su cuerpo principal:
   - `.agents/standards/development/design/LAYERED_ARCHITECTURE.md`
   - `.agents/standards/development/design/CLEAN_ARCHITECTURE.md`
   - `.agents/standards/development/design/DDD_TACTICAL.md`
   - `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md`
2. La nota será:
   ```markdown
   > Para la aplicación operativa de estos principios, ver `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
   ```

### Paso 6 — Actualización del índice
1. Abrir `.agents/standards/INDEX.md`.
2. Añadir `ARCHITECTURE_CONTRACT.md` bajo la sección de design.
3. Añadir el feature flag `architecture_contract` en la tabla de feature flags.

### Paso 7 — Revisión final
1. Verificar que el contrato no contradiga estándares existentes.
2. Confirmar que es opt-in.
3. Validar que el checklist de auto-verificación sea aplicable.
4. Asegurar que no haya referencias a proyecto específico.
5. Confirmar que se cuenta con acuerdo explícito del usuario para modificar archivos dentro de `.agents/`.
6. Verificar que `.agents/features.toml` incluye `architecture_contract = false`.

---

## 5. Criterios de aceptación

- [ ] `ARCHITECTURE_CONTRACT.md` existe y cubre las 10 secciones definidas.
- [ ] El documento define claramente el mecanismo de activación opt-in.
- [ ] Incluye las 6 capas principales (Views, Validators, Schemas, Services, Models, Providers) y la capa de Domain Errors, con responsabilidades y sufijos.
- [ ] Incluye matriz de dependencias permitidas/prohibidas de forma explícita.
- [ ] Define file identity con ruta desde la raíz del proyecto e imports absolutos obligatorios (imports relativos prohibidos).
- [ ] Incluye checklist de auto-verificación.
- [ ] Incluye una cláusula que establezca que, en caso de conflicto, prevalece el estándar canónico correspondiente.
- [ ] `.agents/features.toml` incluye `architecture_contract = false`.
- [ ] `.agents/standards/INDEX.md` indexa el contrato bajo design y el feature flag correspondiente.
- [ ] `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `DDD_TACTICAL.md` y `SCREAMING_ARCHITECTURE.md` añaden la nota final de referencia al contrato.
- [ ] No se modifican los cuerpos principales de los estándares arquitectónicos existentes.
- [ ] No hay referencias a `pay_back`, Flask ni dominio específico.
- [ ] Se cuenta con acuerdo explícito del usuario para modificar archivos dentro de `.agents/`.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con `LAYERED_ARCHITECTURE.md` y otros. | Posicionar el contrato como aplicación operativa, no como teoría. |
| Rigidez excesiva. | Hacerlo opt-in. Permitir adaptación de capas solo si se documenta la equivalencia de responsabilidades, sufijos y reglas de dependencia, sin reducir la lista mínima ni eliminar reglas duras. |
| Resistencia de proyectos legacy. | El opt-in permite adoptarlo solo en nuevos módulos o refactorizaciones. |
| Verificación manual pesada. | Incluir checklist breve y enfocado. |
| Modificación no autorizada de archivos dentro de `.agents/`. | Obtener acuerdo explícito del usuario antes de editar cualquier archivo bajo `.agents/` y documentarlo. |
| Conflicto entre el contrato y estándares canónicos existentes. | Dejar explícito en el contrato que, en caso de discrepancia, prevalece el estándar canónico correspondiente. |

---

## 7. Dependencias

- Plan 01 completado (el contrato operativo debe existir para que el contrato arquitectónico se alinee).
- Acceso a todos los archivos de arquitectura de `example/`.
- Acceso a `.agents/standards/development/design/`.
- Acceso a `.agents/features.toml`.
- Acceso a `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`.
- Acuerdo explícito del usuario para modificar archivos dentro de `.agents/`.

---

## 8. Orden relativo de ejecución

Ejecutar **después del Plan 01 y 02**, y **antes del Plan 04 (Orquestación)**, ya que la guía de orquestación puede necesitar referirse a las capas, sufijos y contrato arquitectónico definidos aquí.

---

## 9. Notas adicionales

- Considerar en el futuro una herramienta de linting arquitectónico (por ejemplo, un script que verifique imports).
- El feature flag `architecture_contract` es opt-in por proyecto; su default `false` garantiza que no se imponga a proyectos existentes.
- No se requiere ejecutar código en este plan.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `ARCHITECTURE_CONTRACT.md` | Operativizar las reglas arquitectónicas: capas, dependencias, naming, auto-verificación. | Teoría arquitectónica general, que permanece en `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `SCREAMING_ARCHITECTURE.md`, `DDD_TACTICAL.md`, etc. |
| `LAYERED_ARCHITECTURE.md` / `CLEAN_ARCHITECTURE.md` / `SCREAMING_ARCHITECTURE.md` / `DDD_TACTICAL.md` / etc. | Definir principios teóricos de cada escuela arquitectónica. | Reglas operativas de aplicación; solo referencian el contrato. |
| `INDEX.md` | Descubribilidad. | Contenido normativo. |

**Principio aplicado:** el contrato arquitectónico no compite con los estándares teóricos. Su única razón de cambio es "cambiar cómo se aplican operativamente las reglas arquitectónicas a los proyectos gobernados".
