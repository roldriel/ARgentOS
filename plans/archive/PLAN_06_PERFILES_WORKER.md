# Plan de Implementación 06 — Perfiles de Worker (actualizado)

> **Origen:** Punto 6 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Crear perfiles de worker especializados reutilizables en `.agents/roles/profiles/` y alinear el contrato de delegación con el campo `profile` que ya usa la guía de orquestación.
> **Estado de referencia:** `orchestrator.md` y `ORCHESTRATION_GUIDE.md` ya contemplan el campo `profile`. El contrato de delegación no lo tiene todavía. Los perfiles no existen.

---

## 1. Decisiones de diseño fijas (no negociables en esta implementación)

Para evitar ambigüedad durante la ejecución, este plan asume las siguientes decisiones:

1. **Un único archivo por perfil.** Cada perfil es un archivo Markdown en `.agents/roles/profiles/<nombre>.md` con secciones fijas. No se usa la estructura `ROLE.md + PROMPT.md + MUST_READ.md` del ejemplo, porque el orchestrator leerá el archivo completo y extraerá las secciones que necesite.
2. **Perfiles genéricos.** Ningún perfil puede referirse a `pay_back`, Flask, SQLAlchemy, MySQL, estados de pago, dominios específicos ni tecnologías de ejemplo. Los perfiles son contratos de comportamiento para cualquier proyecto que use este protocolo.
3. **El contrato de delegación real está en `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.** No existe en `.agents/contracts/`. Todos los cambios al contrato deben hacerse en esa ruta.
4. **El worker genérico (`worker.md`) no se modifica salvo que sea estrictamente necesario** para reconocer el campo `profile`. En este plan no se elimina ni reemplaza.
5. **Los perfiles son opcionales.** Si el payload no incluye `profile` o su valor es `null`, el worker actúa como worker genérico.

---

## 2. Objetivo del plan

Crear seis perfiles de worker especializados en `.agents/roles/profiles/`:

1. `backend_engineer.md`
2. `database_engineer.md`
3. `integration_engineer.md`
4. `qa_engineer.md`
5. `tech_writer.md`
6. `functional_writer.md`

Además:

- Crear `.agents/roles/profiles/README.md` con el catálogo y guía de uso.
- Actualizar `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` para que el payload incluya `profile` y el return report incluya `profile_executed`.
- Asegurar que `orchestrator.md` y `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` sean consistentes con el contrato actualizado.
- Actualizar `.agents/standards/INDEX.md` para indexar los perfiles bajo la sección de orquestación.
- No modificar el worker genérico (`worker.md`) salvo una referencia opcional al catálogo de perfiles.

---

## 3. Alcance

### Incluido
- Creación de 6 perfiles en `.agents/roles/profiles/` con estructura fija y contenido genérico.
- Creación de `.agents/roles/profiles/README.md`.
- Actualización de `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
- Verificación de consistencia de `orchestrator.md` y `ORCHESTRATION_GUIDE.md`.
- Actualización de `.agents/standards/INDEX.md`.

### Excluido
- No modificar `orchestrator.md` salvo para corregir inconsistencias con el contrato.
- No modificar `ORCHESTRATION_GUIDE.md` salvo para corregir inconsistencias con el contrato.
- No eliminar el worker genérico (`worker.md`).
- No crear perfiles adicionales.
- No mover archivos de `example/.agents/roles/_common/` a `.agents/`. El contenido específico de `pay_back` no se reutiliza.
- No implementar selección automática de perfiles: la selección sigue siendo manual basada en las 7 preguntas de `ORCHESTRATION_GUIDE.md`.

---

## 4. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/roles/profiles/README.md` | Índice y guía de uso del catálogo. |
| `.agents/roles/profiles/backend_engineer.md` | Perfil de ingeniero backend. |
| `.agents/roles/profiles/database_engineer.md` | Perfil de ingeniero de base de datos. |
| `.agents/roles/profiles/integration_engineer.md` | Perfil de especialista en integraciones. |
| `.agents/roles/profiles/qa_engineer.md` | Perfil de QA. |
| `.agents/roles/profiles/tech_writer.md` | Perfil de documentación técnica. |
| `.agents/roles/profiles/functional_writer.md` | Perfil de documentación funcional. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` | Añadir campo `profile` al payload y `profile_executed` al return report. Actualizar ejemplos. |
| `.agents/standards/INDEX.md` | Indexar perfiles bajo la sección de orquestación. |
| `.agents/roles/worker.md` | Opcional: añadir nota de que el worker debe leer el perfil indicado en `profile` si no es null. |

### Archivos a verificar (posibles correcciones menores)
| Ruta | Verificación |
|------|--------------|
| `.agents/roles/orchestrator.md` | Confirmar que la sección 5.1 referencia `.agents/roles/profiles/README.md` y el campo `profile`. Corregir si hay inconsistencia. |
| `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` | Confirmar que la plantilla de payload usa `profile` y que el mapeo de perfiles coincide con los 6 perfiles de este plan. |

### Archivos de referencia (solo lectura, no se tocan)
| Ruta | Uso |
|------|-----|
| `example/.agents/roles/backend_python/` | Inspiración para el perfil `backend_engineer`. |
| `example/.agents/roles/database_mysql/` | Inspiración para el perfil `database_engineer`. |
| `example/.agents/roles/integration_specialist/` | Inspiración para el perfil `integration_engineer`. |
| `example/.agents/roles/qa_engineer/` | Inspiración para el perfil `qa_engineer`. |
| `example/.agents/roles/tech_writer/` | Inspiración para el perfil `tech_writer`. |
| `example/.agents/roles/func_writer/` | Inspiración para el perfil `functional_writer`. |
| `example/.agents/roles/_common/` | Consulta para extraer reglas genéricas; su contenido específico de `pay_back` se descarta. |

---

## 5. Pasos de implementación

### Paso 1 — Análisis de fuentes (solo lectura)

1. Leer cada directorio de rol en `example/.agents/roles/`.
2. Leer `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
3. Leer `.agents/roles/orchestrator.md` y `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.
4. Identificar, para cada rol de ejemplo, qué reglas son genéricas y cuáles son específicas de `pay_back`:
   - Genéricas: separación de capas, no lógica de negocio en providers, no ejecutar tests sin instrucción, output efficiency, etc.
   - Específicas de `pay_back`: `Preorder`, `PreorderStatus`, `Flask`, `SQLAlchemy`, `MySQL`, paths como `C:\Users\rroldan\Desktop\NET Pagos\Proyectos\pay_back`, dominios como `preorder`, `payment`, `callback`.
5. Las reglas específicas de `pay_back` no se trasladan a los perfiles. Las genéricas se adaptan a lenguaje neutral.

### Paso 2 — Diseño de la estructura de cada perfil

Cada perfil será un único archivo Markdown con las siguientes secciones exactas, en este orden:

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

Reglas para redactar cada sección:

- **## 1. Propósito**: una oración que defina qué hace el perfil. Sin jerga ni dominios específicos.
- **## 2. Cuándo usar**: lista de condiciones concretas que activan el perfil. Debe coincidir con las 7 preguntas de `ORCHESTRATION_GUIDE.md`.
- **## 3. Lecturas obligatorias (MUST_READ)**: lista de rutas exactas en `.agents/standards/`. Si una lectura depende de un feature flag, indicarlo explícitamente con el formato: `(solo si <flag> está activo)`.
- **## 4. Restricciones**: lista de prohibiciones y comportamientos obligatorios. Deben ser verificables.
- **## 5. Herramientas permitidas**: lista de herramientas del agente (Read, Edit, Write, Grep, Glob, Bash, etc.). Si una herramienta requiere autorización explícita (ej. `curl`, ejecución de tests), indicarlo.
- **## 6. Criterios de aceptación**: checklist para que el worker verifique su propio output.
- **## 7. Output esperado**: formato concreto del entregable (archivos, secciones, naming).
- **## 8. Relación con otros perfiles**: qué perfiles no deben usarse para esta tarea y cuándo convocar a otro perfil en secuencia.
- **## 9. Plantilla de prompt**: plantilla de Markdown que el orchestrator usará para reescribir el objetivo. Debe incluir placeholders concretos entre `<` y `>`.

### Paso 3 — Redacción de perfiles

#### 3.1 `backend_engineer.md`

```markdown
# Backend Engineer

## 1. Propósito
Implementar lógica de negocio, endpoints, servicios y otras piezas de la capa de aplicación respetando la arquitectura del proyecto.

## 2. Cuándo usar
- La tarea implementa lógica de negocio, endpoints o servicios.
- La tarea modifica código en la capa de aplicación (services, views, validators, schemas, commands, etc.).
- No modifica esquemas de base de datos ni integraciones externas.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Solo si el feature flag `architecture_contract` está activo |
| `.agents/standards/testing/TDD.md` | Solo si el feature flag `tdd` está activo |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |

## 4. Restricciones
- No mezclar responsabilidades entre capas (ej. lógica de negocio en Views o Providers).
- No ejecutar tests sin instrucción explícita del usuario o del orchestrator.
- No modificar esquemas de base de datos; si se detecta que la tarea lo requiere, detenerse y reportar que corresponde a `database_engineer`.
- No realizar llamadas a sistemas externos; si se detecta que la tarea lo requiere, detenerse y reportar que corresponde a `integration_engineer`.
- Respetar los sufijos de naming y las reglas de imports definidos en `ARCHITECTURE_CONTRACT.md` (si aplica).

## 5. Herramientas permitidas
- Read, Edit, Write, Grep, Glob, Bash (solo para comandos del proyecto; no `curl` ni requests externos).

## 6. Criterios de aceptación
- [ ] El código respeta la separación de capas del proyecto.
- [ ] No se introducen dependencias prohibidas.
- [ ] Los criterios de aceptación de `TASK_SPECIFICATION.md` están cubiertos.
- [ ] Si `tdd` está activo, existe evidencia de red-green-refactor.

## 7. Output esperado
- Archivos de código de la capa correspondiente.
- Si aplica, actualización de tests de acuerdo con `TDD.md`.
- Un return report que indique el perfil ejecutado y los archivos modificados.

## 8. Relación con otros perfiles
- No usar para cambios de esquema de base de datos (`database_engineer`).
- No usar para integraciones externas (`integration_engineer`).
- No usar para definir tests como tarea principal (`qa_engineer`).
- Si una tarea requiere backend + documentación técnica, dividir en subtareas: primero `backend_engineer`, luego `tech_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como Backend Engineer para implementar la siguiente tarea.

# Tarea específica
<Objetivo atómico y medible>

# Capa arquitectónica
<CAPA> (ej: Service, View, Validator, Schema, Command)

# Entradas
- Archivo actual: <ruta>
- Fragmento relevante:
```
<código>
```

# Criterios de aceptación
- <CA-1>
- <CA-2>

# Restricciones
- No mezclar responsabilidades entre capas.
- No ejecutar tests sin instrucción.
- Respetar los contratos arquitectónicos del proyecto.

# Output esperado
<Código o descripción del entregable>
```
```

#### 3.2 `database_engineer.md`

```markdown
# Database Engineer

## 1. Propósito
Diseñar y modificar esquemas, migraciones, queries, índices y modelos de persistencia sin introducir lógica de negocio.

## 2. Cuándo usar
- La tarea modifica esquemas, tablas, migraciones, queries, índices o modelos de persistencia.
- La tarea requiere justificar un índice nuevo o una restricción de integridad.
- No implementa endpoints ni lógica de negocio.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Solo si el feature flag `architecture_contract` está activo (sección Models/Providers) |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |

## 4. Restricciones
- Los modelos de persistencia no deben contener lógica de negocio, llamadas HTTP ni orquestación.
- No borrar datos existentes sin instrucción explícita y un plan de rollback.
- No ejecutar migraciones en producción ni sin backup.
- Justificar cada índice, clave foránea o constraint nuevo.
- Preservar la integridad de los datos existentes en cualquier modificación de esquema.

## 5. Herramientas permitidas
- Read, Edit, Write, Grep, Bash (solo para scripts de migración si se instruye explícitamente).

## 6. Criterios de aceptación
- [ ] El esquema o modelo está correctamente definido.
- [ ] La migración es reversible (rollback plano o script de reversión).
- [ ] No se introduce lógica de negocio en la capa de persistencia.
- [ ] Los datos existentes están protegidos.

## 7. Output esperado
- Archivo de modelo o esquema actualizado.
- Si aplica, script de migración con rollback.
- Justificación de índices y constraints nuevos.

## 8. Relación con otros perfiles
- No usar para implementar endpoints o servicios (`backend_engineer`).
- No usar para providers externos (`integration_engineer`).
- Si la tarea también requiere documentación funcional, dividir: primero `database_engineer`, luego `functional_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como Database Engineer para modificar el esquema de persistencia.

# Tarea específica
<Descripción del cambio en el esquema o modelo>

# Entidades impactadas
<lista>

# Relaciones afectadas
<lista>

# Criterios de aceptación
- <CA-1>
- <CA-2>

# Restricciones
- No introducir lógica de negocio en modelos.
- Justificar cada índice o constraint nuevo.
- Proporcionar plan de rollback.

# Output esperado
<Modelo actualizado y/o script de migración>
```
```

#### 3.3 `integration_engineer.md`

```markdown
# Integration Engineer

## 1. Propósito
Integrar sistemas externos, APIs, providers y servicios de terceros traduciendo errores externos al dominio del proyecto.

## 2. Cuándo usar
- La tarea consume o expone una API externa.
- La tarea implementa o modifica un provider, adaptador o cliente HTTP.
- La tarea maneja autenticación, retries, timeouts o mapeo de errores externos.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Solo si el feature flag `architecture_contract` está activo (sección Providers) |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |

## 4. Restricciones
- No decidir flujos de negocio; solo transportar, adaptar y traducir.
- No realizar requests reales a sistemas externos sin autorización explícita del usuario.
- No exponer credenciales, tokens ni secretos en el código ni en los artefactos.
- Manejar timeouts, retries y errores de forma explícita.
- Traducir todos los errores externos a excepciones o modelos del dominio del proyecto.

## 5. Herramientas permitidas
- Read, Edit, Write, Grep, Bash (sin `curl` ni requests reales salvo autorización explícita).

## 6. Criterios de aceptación
- [ ] El provider o adaptador está aislado de la lógica de negocio.
- [ ] Los errores externos se traducen al dominio del proyecto.
- [ ] No se exponen credenciales.
- [ ] Se incluyen mocks o stubs para tests.

## 7. Output esperado
- Código del provider/adaptador.
- Actualización de excepciones de dominio si es necesario.
- Documentación del contrato con el sistema externo (request/response esperados).

## 8. Relación con otros perfiles
- No usar para lógica de negocio (`backend_engineer`).
- No usar para esquemas de base de datos (`database_engineer`).
- Si requiere documentación funcional del flujo, dividir: primero `integration_engineer`, luego `functional_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como Integration Engineer para integrar un sistema externo.

# Sistema externo
<Nombre y descripción>

# Contrato técnico
- Base URL: <URL>
- Método HTTP: <GET|POST|...>
- Auth: <tipo>
- Request esperado: <ejemplo>
- Response esperado (éxito): <ejemplo>
- Response esperado (error): <ejemplo>

# Criterios de aceptación
- <CA-1>
- <CA-2>

# Restricciones
- No realizar requests reales sin autorización.
- No exponer credenciales.
- Manejar timeouts, retries y errores explícitamente.
- Traducir errores al dominio del proyecto.

# Output esperado
<Código del provider/adaptador>
```
```

#### 3.4 `qa_engineer.md`

```markdown
# QA Engineer

## 1. Propósito
Definir el alcance de tests, diseñar casos de prueba, aplicar mocks y verificar cobertura sin modificar código funcional.

## 2. Cuándo usar
- La tarea consiste en diseñar, escribir o revisar tests.
- La tarea audita cobertura de código tras cambios.
- La tarea verifica que los cambios no rompan tests existentes.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/testing/TDD.md` | Solo si el feature flag `tdd` está activo |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |
| `.agents/standards/quality/RUBRICS.md` | Solo si el feature flag `rubrics` está activo |

## 4. Restricciones
- No ejecutar `pytest`, `jest`, `mocha` ni ningún runner de tests sin instrucción explícita.
- No modificar código funcional de producción sin autorización.
- No acceder a APIs reales en tests; usar mocks o stubs.
- Asegurar que los tests fallen si se viola una regla de negocio.
- Documentar el escenario que cubre cada test.

## 5. Herramientas permitidas
- Read, Grep, Bash (solo lectura; no ejecución de tests salvo instrucción).

## 6. Criterios de aceptación
- [ ] Los tests cubren los criterios de aceptación de la tarea.
- [ ] Las dependencias están aisladas con mocks.
- [ ] No se modificó código funcional.
- [ ] La cobertura mínima del proyecto se respeta (si está definida).

## 7. Output esperado
- Archivos de test con naming consistente con el proyecto.
- Lista de mocks utilizados.
- Métrica o estimación de cobertura si aplica.

## 8. Relación con otros perfiles
- No usar para implementar código funcional (`backend_engineer`).
- No usar para esquemas (`database_engineer`) ni integraciones (`integration_engineer`) como tarea principal.
- Si se requiere documentación técnica de los tests, dividir: primero `qa_engineer`, luego `tech_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como QA Engineer para diseñar y escribir tests.

# Alcance
<Unitario | Integración | Regresión>

# Archivo objetivo
- Producción: <ruta>
- Tests existentes (si los hay): <ruta>

# Criterios de aceptación a cubrir
- <CA-1>
- <CA-2>

# Restricciones
- No ejecutar tests sin instrucción explícita.
- No modificar código funcional.
- Usar mocks para aislar dependencias.
- No acceder a APIs reales.

# Output esperado
<Archivos de test con escenarios y mocks>
```
```

#### 3.5 `tech_writer.md`

```markdown
# Technical Writer

## 1. Propósito
Producir y mantener documentación técnica para desarrolladores y agentes: READMEs, guías de arquitectura, docstrings y contratos.

## 2. Cuándo usar
- La tarea produce documentación técnica para desarrolladores o agentes.
- La tarea actualiza `README.md`, `AGENTS.md` o documentos de `.agents/`.
- La tarea revisa docstrings o decisiones técnicas.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` | Solo si el feature flag `architecture_contract` está activo |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |

## 4. Restricciones
- No inventar funcionalidades no presentes en el código.
- Mantener ejemplos actualizados y ejecutables.
- Escribir docstrings técnicas en inglés y documentación de negocio en el idioma del proyecto.
- No asumir conocimiento previo del lector; definir acrónimos y términos clave.

## 5. Herramientas permitidas
- Read, Edit, Write, Grep.

## 6. Criterios de aceptación
- [ ] La documentación refleja el estado actual del código.
- [ ] Los ejemplos son correctos y actualizados.
- [ ] No se inventan funcionalidades.
- [ ] La audiencia y el formato están definidos.

## 7. Output esperado
- Archivo markdown actualizado o nuevo.
- Secciones obligatorias cubiertas.
- Ejemplos concretos.

## 8. Relación con otros perfiles
- No usar para documentación de negocio (`functional_writer`).
- No usar para implementar código (`backend_engineer`).
- Si la tarea requiere documentar un flujo de negocio, usar `functional_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como Technical Writer para documentar un cambio técnico.

# Audiencia
<Desarrolladores | Agentes IA | Operaciones>

# Tarea específica
<Documentar el cambio X / Actualizar el archivo Y>

# Fuentes de información
- <ruta_archivo_1>
- <ruta_archivo_2>

# Restricciones
- No inventar funcionalidades.
- Mantener ejemplos actualizados.
- Definir acrónimos y términos clave.

# Output esperado
<Contenido markdown listo para insertar/reemplazar>
```
```

#### 3.6 `functional_writer.md`

```markdown
# Functional Writer

## 1. Propósito
Producir documentación orientada a negocio: flujos de estados, manuales de operación, reglas de negocio y comunicación con stakeholders no técnicos.

## 2. Cuándo usar
- La tarea describe flujos de negocio, estados, transiciones o reglas de negocio.
- La tarea produce manuales de operación para soporte o producto.
- La audiencia son stakeholders no técnicos.

## 3. Lecturas obligatorias (MUST_READ)
| Archivo | Condición |
|---------|-----------|
| `.agents/standards/conduct/OPERATIONAL_RULES.md` | Siempre |
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Siempre |
| `.agents/standards/requirements/EARS.md` | Siempre |
| `.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | Siempre |

## 4. Restricciones
- No usar jerga técnica sin explicarla.
- Enfocarse en el "qué" y el "por qué", no en el "cómo".
- Validar la información contra el código; no asumir comportamientos.
- Incluir ejemplos concretos (estados, actores, montos, transiciones).

## 5. Herramientas permitidas
- Read, Edit, Write, Grep.

## 6. Criterios de aceptación
- [ ] El documento es comprensible para un lector no técnico.
- [ ] Las reglas de negocio están validadas contra el código.
- [ ] Los ejemplos son concretos y actualizados.
- [ ] Se incluye glosario si hay términos técnicos inevitables.

## 7. Output esperado
- Documento markdown en `docs/` o sección en `README.md`.
- Glosario de términos.
- Ejemplos de flujo.

## 8. Relación con otros perfiles
- No usar para documentación técnica de desarrolladores (`tech_writer`).
- No usar para implementar código (`backend_engineer`).
- Si se requiere documentar la integración técnica en lenguaje de negocio, dividir: primero `integration_engineer`, luego `functional_writer`.

## 9. Plantilla de prompt
```markdown
# Rol
Actúas como Functional Writer para documentar un flujo de negocio.

# Proceso de negocio
<Descripción>

# Actores
<lista>

# Reglas de negocio
<lista>

# Excepciones
<lista>

# Criterios de aceptación
- <CA-1>
- <CA-2>

# Restricciones
- No usar jerga técnica sin explicar.
- Enfocarse en el "qué" y el "por qué".
- Validar contra el código.

# Output esperado
<Documento markdown con ejemplos y glosario>
```
```

### Paso 4 — Creación del `README.md` de perfiles

Crear `.agents/roles/profiles/README.md` con el siguiente contenido mínimo:

```markdown
# Perfiles de Worker

## Qué son
Los perfiles son especializaciones del worker genérico para tareas técnicas específicas. Son opcionales; si ninguno aplica, se usa el worker genérico (`profile: null`).

## Lista de perfiles

| Perfil | Cuándo usar |
|--------|-------------|
| `backend_engineer` | Implementar lógica de negocio, endpoints o servicios. |
| `database_engineer` | Modificar esquemas, migraciones, queries o modelos de persistencia. |
| `integration_engineer` | Integrar APIs o sistemas externos; providers y adaptadores. |
| `qa_engineer` | Diseñar, escribir o revisar tests y cobertura. |
| `tech_writer` | Documentación técnica para desarrolladores o agentes. |
| `functional_writer` | Documentación funcional para negocio o stakeholders no técnicos. |

## Cómo elegir un perfil
El orchestrator debe seguir las 7 preguntas de decisión en `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.

## Perfil por defecto
Si ninguna de las 7 preguntas aplica, el orchestrator debe usar el worker genérico con `profile: null`.

## Cómo añadir un nuevo perfil
1. Crear `<nuevo_perfil>.md` en este directorio siguiendo la estructura de 9 secciones.
2. Actualizar esta tabla.
3. Actualizar `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` si el perfil requiere una nueva pregunta de decisión.
4. Actualizar `.agents/standards/INDEX.md`.
```

### Paso 5 — Actualización del contrato de delegación

Editar `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`:

1. En la sección `Required Invocation Payload`, añadir después de `role_to_adopt`:
   ```text
   profile: "<backend_engineer|database_engineer|integration_engineer|qa_engineer|tech_writer|functional_writer|null>"
   ```
2. Añadir una subsección explicando `profile`:
   ```markdown
   ### `profile`

   - **Opcional.**
   - Si es `null` o se omite, el worker actúa como worker genérico.
   - Si contiene un nombre de perfil, el worker debe leer `.agents/roles/profiles/<profile>.md` antes de ejecutar la fase y aplicar sus restricciones, lecturas obligatorias y plantilla de prompt.
   - El valor debe coincidir exactamente con el nombre del archivo sin extensión.
   ```
3. En la sección `Worker Execution`, añadir un paso:
   ```markdown
   1. (Opcional) Si el payload incluye `profile`, leer `.agents/roles/profiles/<profile>.md` y aplicar sus reglas.
   ```
4. En el `Worker Return Report`, añadir:
   ```text
   profile_executed: "<profile o null>"
   ```
5. Actualizar el ejemplo JSON del payload para incluir `profile: null` y `profile_executed` en el ejemplo de return report.

### Paso 6 — Verificación del orchestrator

1. Leer `.agents/roles/orchestrator.md` sección 5.1.
2. Verificar que:
   - Referencie `.agents/roles/profiles/README.md`.
   - Indique que el campo se registra como `profile` en el payload.
   - Diga que si no aplica, `profile` es `null`.
3. Si hay inconsistencia con `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, corregir el texto de `orchestrator.md` para que sea coherente.

### Paso 7 — Verificación de la guía de orquestación

1. Leer `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.
2. Verificar que:
   - Las 7 preguntas mapeen exactamente a los 6 perfiles de este plan.
   - La plantilla de payload incluya `profile: "<perfil o null>"`.
   - El ejemplo de payload genérico use `profile: null`.
3. Si hay inconsistencia, corregir.

### Paso 8 — Actualización del índice de estándares

1. Abrir `.agents/standards/INDEX.md`.
2. Bajo la sección `## Orchestration`, agregar:
   ```markdown
   ### Worker profiles
   - `.agents/roles/profiles/README.md` — catalog of specialized worker profiles.
   - `.agents/roles/profiles/backend_engineer.md`
   - `.agents/roles/profiles/database_engineer.md`
   - `.agents/roles/profiles/integration_engineer.md`
   - `.agents/roles/profiles/qa_engineer.md`
   - `.agents/roles/profiles/tech_writer.md`
   - `.agents/roles/profiles/functional_writer.md`
   ```
3. Si no existe sección `## Orchestration`, crearla antes de `## Runtime`.

### Paso 9 — Actualización opcional del worker genérico

1. Abrir `.agents/roles/worker.md`.
2. En la sección de input del orchestrator o en ejecución, añadir una nota:
   ```markdown
   If the delegation payload includes a non-null `profile` field, the Worker must read `.agents/roles/profiles/<profile>.md` before executing the phase and apply its rules.
   ```
3. No modificar el ciclo de vida ni las restricciones del worker.

### Paso 10 — Revisión final

Verificar:
1. Los 6 perfiles existen en `.agents/roles/profiles/`.
2. Cada perfil tiene las 9 secciones definidas.
3. `README.md` de perfiles existe y tiene la tabla completa.
4. `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` tiene `profile` y `profile_executed`.
5. `orchestrator.md` y `ORCHESTRATION_GUIDE.md` son consistentes con el contrato.
6. `.agents/standards/INDEX.md` indexa los perfiles.
7. El worker genérico sigue siendo la opción por defecto (`profile: null`).
8. No se elimina ni modifica `worker.md` más allá de la nota opcional.
9. No hay referencias a `pay_back`, Flask, SQLAlchemy, MySQL, estados de pago ni dominios específicos en ningún perfil.

---

## 6. Criterios de aceptación

- [ ] Existen 6 perfiles iniciales en `.agents/roles/profiles/`.
- [ ] Cada perfil cubre las 9 secciones definidas y usa lenguaje genérico.
- [ ] Existe `.agents/roles/profiles/README.md` con índice, guía de uso e instrucciones para añadir perfiles.
- [ ] `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` soporta el campo `profile` y el return report incluye `profile_executed`.
- [ ] `orchestrator.md` referencia el catálogo de perfiles y es consistente con el contrato.
- [ ] `ORCHESTRATION_GUIDE.md` es consistente con los 6 perfiles y el contrato.
- [ ] `.agents/standards/INDEX.md` indexa los perfiles bajo la sección de orquestación.
- [ ] El worker genérico sigue siendo la opción por defecto (`profile: null` o ausente).
- [ ] No se elimina ni modifica `worker.md` salvo la nota opcional.
- [ ] No hay referencias a `pay_back`, Flask, SQLAlchemy, MySQL, estados de pago ni dominios específicos en los perfiles.
- [ ] Ningún perfil duplica estándares transversales; solo los referencia condicionalmente por feature flags.

---

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Sobrecarga de contexto por perfiles. | Cada perfil debe tener menos de 2000 tokens aproximadamente; el resto de reglas se referencia vía feature flags. |
| Duplicación con roles genéricos o estándares. | Los perfiles solo contienen reglas específicas del rol. Todo lo transversal vive en `.agents/standards/`. |
| Confusión sobre cuándo usar cada perfil. | El `README.md` y `ORCHESTRATION_GUIDE.md` incluyen ejemplos concretos de decisión. |
| Mantenimiento de muchos perfiles. | Se empieza con 6 perfiles. Añadir uno nuevo requiere actualizar `README.md`, `ORCHESTRATION_GUIDE.md` e `INDEX.md`. |
| Inconsistencia entre contrato y guía de orquestación. | Verificar que la plantilla de payload de `ORCHESTRATION_GUIDE.md` use exactamente los mismos nombres y semántica que el contrato. |

---

## 8. Dependencias

- `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` debe existir (ya existe).
- `.agents/roles/orchestrator.md` debe existir (ya existe).
- `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` debe existir (ya existe).
- `.agents/standards/INDEX.md` debe existir (ya existe).
- Acceso a los roles de ejemplo en `example/.agents/roles/` solo como referencia de inspiración.

No es necesario esperar a otros planes de implementación para ejecutar este plan, salvo que esos planes definan artefactos que un perfil deba referenciar (ej. `DOMAIN_CHEATSHEET_TEMPLATE.md`). En ese caso, la referencia se añade al perfil una vez que el artefacto exista.

---

## 9. Orden relativo de ejecución

Ejecutar cuando se esté listo para poblar `.agents/roles/profiles/`. El `ORCHESTRATION_GUIDE.md` ya depende de la existencia de estos perfiles, por lo que este plan no debe postergarse.

Si los perfiles referencian artefactos que aún no existen (como `DOMAIN_CHEATSHEET_TEMPLATE.md`), dejar esas referencias condicionales o comentarlas hasta que el artefacto esté disponible.

---

## 10. Notas adicionales

- No se requiere ejecutar código en este plan.
- No se debe crear `.agents/roles/profiles/common/` a menos que aparezca contenido genuinamente compartido entre perfiles que no sea ya un estándar.
- Cualquier regla transversal que aparezca en más de un perfil debe migrarse a `.agents/standards/`, no duplicarse.

---

## 11. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| Cada `<perfil>.md` | Definir las reglas, lecturas y restricciones de un rol técnico específico. | Reglas generales del protocolo (están en `OPERATIONAL_RULES.md` y `standards/`); reglas de otros roles; contenido específico de `pay_back`. |
| `WORKER_DELEGATION_CONTRACT.md` | Especificar el formato de delegación de trabajo. | Lógica interna de cada perfil; solo habilita el campo `profile`. |
| `README.md` de perfiles | Índice y guía de uso del catálogo. | Contenido normativo de perfiles. |
| `orchestrator.md` / `worker.md` | Roles genéricos. | No asumen responsabilidades de los perfiles; los referencian. |
| `ORCHESTRATION_GUIDE.md` | Decidir cuándo y a quién delegar. | No define las reglas internas de cada perfil. |

**Principio aplicado:** cada perfil tiene una única razón de cambio: cambiar las reglas de ese rol técnico específico. El contrato de delegación no crece con lógica de perfiles; solo los habilita mediante un campo opcional. La guía de orquestación no define las reglas de los perfiles; solo decide cuándo aplicarlos.