# Análisis: Extracción de herramientas, metodologías y mecánicas de `example/` para `.agents/`

> **Alcance:** Este documento compara la carpeta `example/` contra el protocolo `.agents/` actual y propone extracciones concretas que pueden mejorar la calidad, la gobernanza y la operativa de ARgentOS. No modifica `.agents/`; presenta opciones para decisión del usuario.

---

## 1. Resumen ejecutivo

La carpeta `example/` contiene una **plantilla completa de gobernanza de agentes para un proyecto Flask de pagos**. Sus componentes más valiosos y portables son:

1. **Contrato operativo supremo** (`OPERATIONAL_RULES.md`) + **checklist pre-vuelo** (`PREFLIGHT_CHECKLIST.md`).
2. **Contrato arquitectónico de capas duras** (`ARCHITECTURE_*.md`) con reglas de dependencia, naming y auto-verificación.
3. **Estructura modular de roles** (`ROLE.md` + `PROMPT.md` + `MUST_READ.md` + módulos `_common/`).
4. **Guía de orquestación** con 7 preguntas de decisión, checklist de delegación y glosario de capas.
5. **Context engineering** con tags de compresión para prompts densos.
6. **Reglas de output mínimo** (`OUTPUT_EFFICIENCY.md`, `COMMUNICATION_RULES.md`).
7. **Roles especializados** (QA Engineer, Tech Writer, Functional Writer, Integration Specialist, DB Architect).
8. **Artefactos de contexto** (`project-map.md`, `technical-analysis.md`).

A continuación se detalla qué existe en `example/`, qué ya cubre `.agents/`, y qué se recomienda incorporar, con prioridad y ubicación sugerida.

---

## 2. Mapeo comparativo

| Área | Estado en `.agents/` | Estado en `example/` | Brecha / Oportunidad |
|------|----------------------|----------------------|----------------------|
| **Contrato operativo** | Fragmentado en `NO_ASSUMPTIONS.md`, `ANTI_CIRCUMVENTION.md`, `PROTOCOL_BOUNDARIES.md` y `orchestrator.md`. | Documento único y detallado (`OPERATIONAL_RULES.md`) + checklist de 20 secciones (`PREFLIGHT_CHECKLIST.md`). | Consolidar en un estándar operativo supremo con checklist ejecutable. |
| **Arquitectura de capas** | Estándares individuales: `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, etc. Sin contrato único de dependencias. | Contrato único `ARCHITECTURE.md` con 6 capas, dependencias duras, naming suffixes, file identity. | Crear un contrato arquitectónico consolidado aplicable a proyectos gobernados. |
| **Estructura de roles** | Roles genéricos: `orchestrator.md`, `worker.md`, `reviewer.md`, `verifier.md`. `profiles/` solo para intent reflection. | Roles especializados con `ROLE.md`/`PROMPT.md`/`MUST_READ.md` + módulos `_common/` por tema. | Crear perfiles de worker especializados reutilizables. |
| **Delegación** | `WORKER_DELEGATION_CONTRACT.md` genérico. | Plantillas específicas por rol con contexto aislado, lecturas obligatorias y output efficiency. | Enriquecer el contrato de delegación con plantillas por perfil. |
| **Orquestación** | Cubierta en `orchestrator.md` y workflow. | `ORCHESTRATION_GUIDE.md` con 7 preguntas, checklist pre-delegación, glosario de capas. | Integrar guía de orquestación práctica. |
| **Contexto / KB** | `CONTEXT.md`, `KB_DISCOVERY_REPORT.md`, project discovery. | `CONTEXT_ENGINEER.md` con tags compactos y técnicas de compresión. | Añadir context engineering con tags. |
| **Comunicación** | `CAVEMAN.md` (español argentino). | `OUTPUT_EFFICIENCY.md` + `COMMUNICATION_RULES.md` neutros, técnicos, universales. | Complementar CAVEMAN con reglas de output mínimo universales. |
| **Testing** | `TDD.md`, `RUBRICS.md`. | Rol `qa_engineer/` con `TESTING_RULES.md`, alcance, mocks, cobertura. | Crear perfil QA Engineer y reglas de testing específicas. |
| **Documentación funcional/técnica** | Plantillas genéricas de contratos. | Roles `tech_writer/` y `func_writer/` con `DOMAIN_CHEATSHEET.md`. | Añadir perfiles de documentación y plantillas de dominio. |
| **Artefactos de contexto** | `CONTEXT_ARTIFACT.md`, `KB_DISCOVERY_REPORT.md`. | `project-map.md`, `technical-analysis.md` del proyecto real. | Crear contratos para mapa de proyecto y análisis técnico. |
| **Configuración de IDE** | No existe. | `.claude/settings.local.json` con permisos y herramientas permitidas. | Proveer plantilla de configuración para Claude / otros IDEs. |

---

## 3. Extracciones recomendadas (con prioridad)

### 3.1 Alta prioridad — Fundamentos operativos y arquitectónicos

#### A. Contrato operativo supremo + Pre-Flight Checklist

**Qué extraer:**
- `example/.agents/roles/_common/OPERATIONAL_RULES.md`
- `example/.agents/roles/_common/PREFLIGHT_CHECKLIST.md`

**Dónde integrar:**
- `.agents/standards/conduct/OPERATIONAL_RULES.md`
- `.agents/standards/quality/PREFLIGHT_CHECKLIST.md`

**Qué aporta:**
- Una sola fuente de verdad para: autoridad/precedencia, límites de tooling, control de scope, ambigüedad, context awareness, error handling, external interaction safety, determinismo, criterios de completitud, output constraints y estilo de comunicación.
- Un checklist de 20 secciones que el worker debe evaluar antes de cualquier respuesta o cambio de código.
- Se alinea con `NO_ASSUMPTIONS.md` y `ANTI_CIRCUMVENTION.md` ya existentes, pero los consolida y hace ejecutables.

**Notas de adaptación:**
- Eliminar referencias específicas a `pay_back`, Flask, Windows 10 y `.venv`; parametrizarlas o moverlas a plantilla de proyecto.
- El punto de que las reglas prevalecen sobre instrucciones de usuario ya está implícito en `ANTI_CIRCUMVENTION.md`; aquí se expresa de forma explícita y contractual.

---

#### B. Contrato arquitectónico de capas duras

**Qué extraer:**
- `example/.claude/rules/ARCHITECTURE.md` (versión consolidada)
- `example/.agents/roles/_common/ARCHITECTURE_LAYERS.md`
- `example/.agents/roles/_common/ARCHITECTURE_NAMING.md`
- `example/.agents/roles/_common/ARCHITECTURE_PROHIBITIONS.md`

**Dónde integrar:**
- `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`
- O `.agents/standards/development/design/LAYERED_ARCHITECTURE_CONTRACT.md`

**Qué aporta:**
- Definición explícita de 6 capas: Views, Validators, Schemas, Services, Models, Providers.
- Reglas de dependencia duras (qué capa puede depender de cuál).
- Prohibiciones de bypass y mezcla de patrones.
- Naming suffixes obligatorios (`View`, `Validator`, `Schema`, `Service`, `Provider`, `Error`/`Exception`).
- File identity: línea 1 con ruta absoluta desde root, imports absolutos.
- Auto-verificación arquitectónica obligatoria antes de generar código.

**Notas de adaptación:**
- .agents ya tiene `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `SCREAMING_ARCHITECTURE.md`, `DDD_TACTICAL.md`, etc. Se recomienda **no duplicar**, sino crear un contrato operativo que las consuma y las convierta en reglas aplicables por el worker.
- El contrato debe ser opcional: solo se aplica cuando el proyecto gobernado lo declara (feature flag o declaración en `TASK_SPECIFICATION.md`).

---

#### C. Output Efficiency + Communication Rules

**Qué extraer:**
- `example/.agents/roles/_common/OUTPUT_EFFICIENCY.md`
- `example/.agents/roles/_common/COMMUNICATION_RULES.md`

**Dónde integrar:**
- `.agents/standards/communication/OUTPUT_EFFICIENCY.md`
- Actualizar `.agents/standards/communication/CAVEMAN.md` para referenciarlo.

**Qué aporta:**
- Reglas universales de salida mínima: sin saludos, resúmenes, disclaimers, justificaciones, emojis, cortesías.
- Principio del "robot frío": precisión > amabilidad, densidad > claridad conversacional.
- Complementa a CAVEMAN sin reemplazarlo: CAVEMAN es el registro local argentino; Output Efficiency es el estándar universal.

**Notas de adaptación:**
- Mantener CAVEMAN como feature flag opcional; Output Efficiency como base.
- Aclarar que el estilo no justifica ambigüedad (ya está en CAVEMAN, reforzar aquí).

---

### 3.2 Media prioridad — Roles, delegación y orquestación

#### D. Perfiles de worker especializados

**Qué extraer:**
- Estructura `example/.agents/roles/<rol>/` con `ROLE.md` + `PROMPT.md` + `MUST_READ.md`.
- Roles: `backend_python`, `database_mysql`, `integration_specialist`, `qa_engineer`, `tech_writer`, `func_writer`.

**Dónde integrar:**
- `.agents/roles/profiles/<perfil>.md`
- Crear también `.agents/roles/profiles/README.md` con índice.

**Qué aporta:**
- Workers que adoptan un perfil técnico específico en lugar de un worker genérico.
- Cada perfil define lecturas obligatorias, restricciones y plantilla de delegación.
- Reduce la carga del prompt del orquestador al tener contratos predefinidos.

**Notas de adaptación:**
- Los perfiles deben ser **opcionales**: el orquestador puede seguir usando el worker genérico o elegir un perfil según la fase.
- Reutilizar los `_common/` de example como módulos de contexto temático dentro de `.agents/standards/development/` o `.agents/roles/profiles/common/`.

---

#### E. Guía de orquestación práctica

**Qué extraer:**
- `example/.agents/roles/coordinator/ORCHESTRATION_GUIDE.md`

**Dónde integrar:**
- `.agents/standards/runtime/ORCHESTRATION_GUIDE.md`
- O extender `.agents/roles/orchestrator.md` con un anexo.

**Qué aporta:**
- **Anexo A:** 7 preguntas rápidas para decidir qué roles involucrar.
- **Anexo B:** checklist antes de delegar.
- **Anexo C:** glosario de capas con sufijos y reglas de oro.
- Regla clave: nunca reenviar el prompt original; reescribir con template del rol.

**Notas de adaptación:**
- Alinear con el workflow existente de .agents (fases 00–08) para que las 7 preguntas se apliquen dentro del contexto del state machine.
- Incluir referencias a los feature flags (`rubrics`, `knowledge_base`, `decision_trees`).

---

#### F. Context Engineering con tags de compresión

**Qué extraer:**
- `example/.agents/roles/coordinator/CONTEXT_ENGINEER.md`

**Dónde integrar:**
- `.agents/standards/context/CONTEXT_ENGINEERING.md`

**Qué aporta:**
- Técnicas de compresión de prompt: cherry-picking de módulos, tags compactos (`[AUTHORITY:...]`, `[LAYER:...]`, `[DEPENDENCY:...]`, `[NAMING:...]`, `[MONETARY:...]`, etc.), inline vs referencia, one-shot examples, regla del 50%, descomposición multi-turn.
- Mejora la eficiencia de tokens en la delegación entre orquestador y workers.

**Notas de adaptación:**
- Generalizar los ejemplos que hoy son de pagos (`MONETARY` → `BUSINESS_CRITICAL`, etc.).
- Asegurar que no contradiga `CONTEXT.md` ni los budgets de KB definidos.

---

### 3.3 Baja prioridad — Especializaciones y artefactos de contexto

#### G. Rol QA Engineer con reglas de testing

**Qué extraer:**
- `example/.agents/roles/qa_engineer/ROLE.md`
- `example/.agents/roles/qa_engineer/TESTING_RULES.md`
- `example/.agents/roles/qa_engineer/PROMPT.md`

**Dónde integrar:**
- `.agents/roles/profiles/qa_engineer.md`
- `.agents/standards/testing/TESTING_RULES.md`

**Qué aporta:**
- Definición de alcance de tests (unitario, integración, regresión).
- Patrones de mock y cobertura mínima.
- Prohibición de ejecutar `pytest` sin instrucción explícita.

**Notas de adaptación:**
- Complementa `TDD.md` y `RUBRICS.md`; no duplicar.
- Hacerlo opcional bajo feature flag o elección del orquestador.

---

#### H. Perfiles de documentación (Tech Writer / Functional Writer)

**Qué extraer:**
- `example/.agents/roles/tech_writer/`
- `example/.agents/roles/func_writer/` + `DOMAIN_CHEATSHEET.md`

**Dónde integrar:**
- `.agents/roles/profiles/tech_writer.md`
- `.agents/roles/profiles/functional_writer.md`
- `.agents/contracts/DOMAIN_CHEATSHEET_TEMPLATE.md`

**Qué aporta:**
- Separación clara entre documentación técnica (para devs/agentes) y funcional (para negocio).
- Plantilla de cheatsheet de dominio para proyectos complejos.

---

#### I. Artefactos de contexto: project-map y technical-analysis

**Qué extraer:**
- `example/project-map.md`
- `example/technical-analysis.md`

**Dónde integrar:**
- `.agents/contracts/PROJECT_MAP.md`
- `.agents/contracts/TECHNICAL_ANALYSIS.md`

**Qué aporta:**
- Estandarizar cómo el `context_gatherer` documenta el proyecto real.
- `project-map.md`: mapa rápido de carpetas, endpoints, modelos, flujos, riesgos.
- `technical-analysis.md`: análisis profundo de stack, arquitectura, integraciones, riesgos.

---

#### J. Configuración de IDE

**Qué extraer:**
- `example/.claude/settings.local.json`

**Dónde integrar:**
- `.agents/templates/claude-settings.json`
- O documentar en `.agents/standards/runtime/IDE_CONFIGURATION.md`

**Qué aporta:**
- Plantilla de permisos de ejecución y herramientas habilitadas para Claude.
- Acelera la adopción del protocolo en nuevos proyectos.

**Notas de adaptación:**
- No incluir en `.agents/` archivos que sean específicos del IDE del usuario; mejor como plantilla.

---

## 4. Propuesta de integración ordenada

Para no romper el protocolo existente ni duplicar reglas, se sugiere el siguiente orden:

1. **Fundamentos operativos:**
   - Crear `.agents/standards/conduct/OPERATIONAL_RULES.md`.
   - Crear `.agents/standards/quality/PREFLIGHT_CHECKLIST.md`.
   - Actualizar `.agents/standards/INDEX.md` para referenciar ambos.

2. **Comunicación:**
   - Crear `.agents/standards/communication/OUTPUT_EFFICIENCY.md`.
   - Actualizar `CAVEMAN.md` para que lo referencie.

3. **Arquitectura:**
   - Crear `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` (o extender `LAYERED_ARCHITECTURE.md`).
   - Asegurar que sea un estándar **aplicable** (con evidencia y checklist), no solo teórico.

4. **Orquestación:**
   - Crear `.agents/standards/runtime/ORCHESTRATION_GUIDE.md`.
   - Extender `orchestrator.md` para que lo use.

5. **Context engineering:**
   - Crear `.agents/standards/context/CONTEXT_ENGINEERING.md`.

6. **Perfiles de worker:**
   - Crear `.agents/roles/profiles/<perfil>.md` iniciales: `backend_engineer`, `database_engineer`, `integration_engineer`, `qa_engineer`, `tech_writer`, `functional_writer`.
   - Actualizar `WORKER_DELEGATION_CONTRACT.md` para soportar `profile` en el payload.

7. **Artefactos de contexto:**
   - Crear `.agents/contracts/PROJECT_MAP.md`.
   - Crear `.agents/contracts/TECHNICAL_ANALYSIS.md`.

8. **Plantillas de proyecto:**
   - Crear `.agents/templates/claude-settings.json`.
   - Crear `.agents/templates/domain-overview-template.md` y `domain-cheatsheet-template.md`.

---

## 5. Riesgos y consideraciones

| Riesgo | Mitigación |
|--------|------------|
| Duplicación con estándares existentes (`CAVEMAN.md`, `NO_ASSUMPTIONS.md`, `RUBRICS.md`, `TDD.md`). | Extraer como **complemento** o **consolidación**, no como reemplazo. Mantener single-source of truth. |
| Sobrecarga de contexto para workers. | Los módulos `_common/` y los perfiles permiten cherry-picking; cada worker lee solo lo que su `MUST_READ` indica. |
| Rigidez excesiva del contrato arquitectónico. | Hacer el contrato arquitectónico **opt-in** por proyecto o tarea; no imponerlo a todos los proyectos gobernados. |
| Conflicto con "documentos prevalecen sobre instrucciones de usuario". | Dejar claro que el contrato operativo prevalece **solo sobre instrucciones que violen el protocolo**, no sobre el objetivo legítimo del usuario. |
| Mantenimiento de plantillas por IDE. | Mantener templates fuera del core del protocolo, en `.agents/templates/`. |

---

## 6. Conclusión

`example/` aporta mecánicas maduras de **gobernanza operativa, arquitectónica y de delegación** que `.agents/` aún no tiene de forma consolidada. Las extracciones de **alta prioridad** (contrato operativo supremo, checklist pre-vuelo, contrato arquitectónico de capas duras y output efficiency) pueden elevar la calidad del protocolo sin aumentar significativamente la complejidad. Las de **media/baja prioridad** (perfiles de worker, guía de orquestación, context engineering, artefactos de contexto) lo hacen más escalable y especializable.

**Recomendación:** Comenzar por los fundamentos operativos y arquitectónicos, validar su funcionamiento en tareas reales, y luego incorporar perfiles especializados de a uno por vez.
