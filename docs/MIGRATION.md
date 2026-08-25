# Política de migración — Protocolo ARgentOS

Cómo migrar un proyecto que adoptó el protocolo ARgentOS (`.agents/` + `AGENTS.md`)
de una versión a otra. Este archivo vive **fuera de `.agents/`** a propósito
(origen: `plans/20-release-adoption.md` §A): una migración no debe modificar su
propia política.

La versión vigente está declarada en `.agents/VERSION` (una línea semver). El
historial de cambios está en [`CHANGELOG.md`](CHANGELOG.md). La guía de adopción
inicial está en [`ADOPTION.md`](ADOPTION.md).

---

## 1. Esquema de versión

Semver conceptual (`plans/20-release-adoption.md` §A):

| Componente | Cuándo sube | Ejemplo |
|---|---|---|
| **MAJOR** | Cambios del modelo conceptual o contratos incompatibles: un contrato de artefacto cambia campos obligatorios, una fase del workflow se renombra o elimina, una policy cambia su criterio de PASS de forma incompatible. | Un `TASK_SPECIFICATION.md` válido en 1.x deja de serlo en 2.0. |
| **MINOR** | Adiciones compatibles: policies nuevas, contratos nuevos que no rompen los existentes, skills nuevas, secciones opcionales. | Aparece una nueva policy H21; los artefactos 1.x siguen siendo válidos. |
| **PATCH** | Fixes documentales: redacción, ejemplos, enlaces, typos; sin cambio de comportamiento. | Se corrige un ejemplo en un contrato. |

## 2. Procedimiento de migración

Para pasar un proyecto adoptante de la versión `X` a la versión `Y`:

1. **Leer el changelog** entre `X` e `Y` en `CHANGELOG.md`. Cada ítem referencia
   la policy, plan o RFC que lo originó; esas son las fuentes de detalle.
2. **Revisar contratos modificados** (`.agents/contracts/`,
   `.agents/orchestrators/*/contracts/`): para cada contrato listado en el
   changelog, comparar campos obligatorios (front matter `artifact`, `phase`,
   `produced_by`, `schema_version`) y secciones requeridas contra los
   artefactos que el proyecto ya produce. `schema_version` es semver: un salto
   **MAJOR** (campos obligatorios incompatibles) exige actualizar las
   plantillas o los artefactos vivos del proyecto; **MINOR** (adiciones
   compatibles) y **PATCH** (fixes documentales) no rompen los artefactos
   válidos existentes.
3. **Revisar artifacts renombrados o eliminados**: todo rename/removal aparece en
   la sección **Removed** del changelog. Actualizar referencias en roles, workflow
   y artefactos propios del proyecto.
4. **Adoptar policies nuevas**: revisar `.agents/harness/policies/` y
   `.agents/orchestrators/*/harness/policies/`. Las policies nuevas (MINOR)
   empiezan a validar en cuanto se copian; verificar que los artefactos del
   proyecto las cumplen antes de habilitar el trigger correspondiente.
5. **Revisar flags**: comparar `.agents/features.toml` contra la versión nueva;
   los flags nuevos llegan con default seguro (deshabilitado salvo indicación del
   changelog).
6. **Sincronizar el directorio**: reemplazar `.agents/` y `AGENTS.md` por los de
   la versión `Y`. `.agents/` es autocontenido: no referencia `plans/` ni RFCs, así
   que no hace falta copiar nada más del repo de origen.
7. **Validar**: la checklist documental de
   `.agents/standards/runtime/PROTOCOL_HEALTH.md` (la aplica el system agent en
   el bootstrap) debe terminar en `PASS`. Si el proyecto opera en modo
   enforced, ejecutar además la sonda de almacenamiento de estado
   (`python .agents/harness/health_check.py` → PASS). La suite de tests
   (`python -m pytest .agents/harness/tests/`) es solo para desarrollo del
   protocolo, no un requisito del adoptante.
8. **Actualizar la versión adoptada**: registrar en el proyecto qué versión de
   `.agents/VERSION` quedó adoptada.

## 3. Cambios de modelo y contratos — planes 28-30 (2026-08-11)

Implementación autorizada explícitamente por el usuario (RFC-29…31 `Accepted`,
planes 28–30 `Executed`). Puntos que un adoptante debe revisar al adoptar esta
versión:

- **`VERIFICATION_REPORT.md` — Scope Compliance con dos ramas**: los reportes
  existentes que cumplen la Rama A (sin extra, `unplanned_changes = []`,
  `user_authorized_extra_work = false`) siguen siendo válidos. La Rama B
  (`user_authorized_extra_work = true` con cambios fuera del plan) solo pasa H07
  con autorización escrita del usuario citada en el reporte (`SESSION_LOG.md` o
  artefacto de sesión). `scope_respected = false` es fallo en ambas ramas.
- **`RECOVERY_REPORT.md` — `ABORT` en la recomendación**: el enum de
  `corrective_action.recommended_next_state` ahora admite `ABORT`, válido solo
  como abort fundado (causa registrada en `SESSION_LOG.md`, per `DECISIONS.md`
  D5).
- **Máquina de estados — aristas de recovery a fases tempranas**:
  `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION | GATHERING_CONTEXT |
  VALIDATING_CONTEXT` son transiciones legales para corregir artefactos de fases
  tempranas; `RETRY_WORKER` sobre la fase actual es una acción correctiva sin
  transición de estado. H01 incorpora una rama de retry acotado
  (`retry_count == 0`) para fallos de formato.
- **Modo enforced — cierre terminal**: `runner_state.py` registra estados
  terminales (`python .agents/harness/runner_state.py --session <uuid> --state
  ABORT|COMPLETED terminal`); el hook deja cerrar la sesión por `Stop` cuando
  `state.json.status` es `ABORT`/`COMPLETED`, además de las condiciones
  anteriores (H06 PASS o `NEEDS_CLARIFICATION` registrado).

Este cambio se publica como versión `3.0.0` (2026-08-11); esta sección es la
guía de migración del cambio.

## 3.1 Cambios de forma y nomenclatura — planes 31-33 (2026-08-11)

Release 3.0.1 (PATCH): correcciones documentales sin cambios de modelo.

- **`TASK_SPECIFICATION.md` — criterios de aceptación**: la forma canónica de
  `## Acceptance Criteria` son los bullets Markdown EARS. Las specs históricas
  con criterios solo en el bloque TOML `acceptance_criteria` deben migrar los
  criterios a bullets; el bloque TOML queda como representación opcional y
  derivada (no reemplaza los bullets).
- **`EXECUTION_SUMMARY.md` — lista de pasos**: el nombre canónico de la lista es
  `[[steps_executed]]`. Los resúmenes históricos con `[[steps]]` son no
  conformes y deben migrar la clave a `[[steps_executed]]`.
- **Fase 02 — rol**: la tabla de activación y la guía de orquestación usan el
  rol de fase `task_specification_writer`; `functional_writer` queda limitado a
  la documentación funcional de la fase 06.

Este cambio se publica como versión `3.0.1` (2026-08-11); esta sección es la
guía de migración del cambio.

## 3.2 Namespacing de artefactos de discovery — plan 40 (2026-08-12)

Desde `3.3.0`, los artefactos de sesión del dominio discovery usan prefijo
`D<order>-` (p. ej. `D01-KB_DISCOVERY_REPORT.md`) y los intermedios de workers
viven en `.project/<session-uuid>/discovery/` sin `<order>`. No requiere
acción en proyectos adoptantes: las iteraciones previas quedan como traza
histórica (no se renombran); la regla aplica a ejecuciones futuras.

## 4. Qué NO migra

- **Artefactos de sesión** (`.project/`): son efímeros y específicos del proyecto;
  no se migran ni se versionan con el protocolo.
- **Knowledge base** (`.project/knowledge/`): se conserva; si un contrato de KB
  cambió (sección del changelog), regenerar o re-curar las entradas afectadas.
- **Skills propias del proyecto** (`.project/skills/` o las del usuario): se
  conservan; revalidarlas contra el estándar de skills si la sección
  correspondiente del changelog indica cambios estructurales.

## 5. Soporte de versiones

Se soporta una sola línea de versión: la vigente. No hay ramas de mantenimiento
de versiones anteriores (fuera de alcance declarado en
`plans/20-release-adoption.md` §Fuera de alcance).

## 6. Modelo de garantías y fronteras de enforcement — 4.0.0 (plan 76, RFC-62)

Cambio **MAJOR** del modelo conceptual: cambia el significado declarado de
"verificado" y agrega obligaciones de registro.

- **Nueva semántica de "verificado".** Un claim puede llamarse "verificado"
  solo cuando cita evidencia de clase distinta de atestación. Sin evidencia
  citable, el término permitido es "atestado". El detalle de las clases de
  evidencia se define en el modelo de evidencia posterior.
- **Obligaciones nuevas.** Todo claim emitido por el protocolo es
  evidencia-citado o está marcado explícitamente como atestación/inferencia
  (regla de claims). Los gate checks de `HARNESS_REPORT.md` y los criterios y
  resultados de `VERIFICATION_REPORT.md` distinguen `verified` de
  `attested`/`inference`; los timestamps mecánicos usan reloj UTC y los
  agentes sin reloj confiable marcan `clock: agent_clock`; `SESSION_LOG.md`
  puede citar `Evidence` por decisión.
- **Campos nuevos opcionales.** `claim_class` (HARNESS_REPORT y
  VERIFICATION_REPORT), `clock` (HARNESS_REPORT y METRICS) y `Evidence`
  (SESSION_LOG) son adiciones compatibles: los artefactos válidos previos
  siguen siendo válidos (schema 1.1.0).
- **Trazas históricas.** Las sesiones previas a 4.0.0 son registros inmutables
  bajo la semántica vieja (RFC-46): no se reescriben ni se re-reportan. Los
  checkers de desarrollo no las reportan.
- **Adopción.** Leer `.agents/harness/INDEX.md`, secciones "Guarantee
  catalog" y "Enforcement boundaries", para la matriz completa por capa y el
  comportamiento en modo declarativo vs. enforced. No se requiere ninguna
  acción de migración sobre artefactos existentes; los reportes nuevos deben
  cumplir la regla de claims.
