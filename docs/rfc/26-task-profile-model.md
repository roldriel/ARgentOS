# RFC-26 — Task Profile Model

**Status:** Accepted

**Aceptación retroactiva:** 2026-08-11 — regularización de auditoría 2.0.1 (RFC-42, plan 41). El modelo ya estaba implementado por el plan 25 (`plans/25-task-profile-model.md`, `Executed`); el status `Proposal` era un desfase documental. Evidencia: plan 25 y `CHANGELOG.md` (2.0.0).

**Author:** Rodrigo Roldán

**Impact:** Structural

**Breaking Changes:** The intake phase assigns a task profile; policies branch on it.

---

# Abstract

Esta RFC define el **modelo de perfiles de tarea**: toda tarea se clasifica en el intake como `trivial`, `standard` o `complex`, y el ciclo de artefactos, gates y delegaciones se ajusta al perfil. Hoy el protocolo aplica el ciclo completo a toda tarea: la única sesión de dogfooding registrada generó ~23 archivos, 10 gates de harness y ~52 minutos de reloj para una sola tarea, pasando por 2 NEEDS_CLARIFICATION y 1 RECOVERY. Para tareas pequeñas, el protocolo cuesta más que la tarea.

El modelo usa mecanismos ya existentes (decision trees TOML que el runner parsea, clasificación en la fase de análisis) y solo agrega la política de bifurcación que falta.

---

# Motivation

- El overhead es uniforme e independiente del tamaño de la tarea: 12 artefactos de iteración + 4 de sesión + JSONs de workers, sin importar si la tarea es "renombrar una variable" o "diseñar un subsistema".
- El dogfooding confirma fricción incluso en el caso de uso feliz del propio autor.
- Sin perfiles, la adopción seria es inviable en el día a día: el usuario elige entre seguir el protocolo entero o saltárselo — y saltárselo es exactamente lo que el protocolo quiere prevenir.
- El runner ya ejecuta decision trees TOML (`H00_FAIL.toml`…`H15_FAIL.toml`): la bifurcación por perfil es una extensión de un mecanismo vigente, no un subsistema nuevo.

---

# Goals

- Definir tres perfiles de tarea con **criterios objetivos** de asignación en la fase 01-task-analysis.
- Definir el conjunto de artefactos, gates y delegaciones obligatorios por perfil.
- Hacer que las policies de harness validen el conjunto *del perfil asignado*, no el ciclo completo.
- Garantizar que el perfil `trivial` cumpla: ≤ 5 archivos generados, ≤ 3 gates, sin fase de discovery.
- Registrar el perfil asignado y su justificación en `TASK_ANALYSIS.md` (auditable).

---

# Non Goals

Esta RFC no propone:

- eliminar el ciclo completo: `standard` es el ciclo vigente sin cambios;
- clasificación automática por heurísticas de código (el perfil lo asigna el task_analyst con criterios, con validación de la policy H00);
- perfiles por tipo de tarea (bugfix/refactor/feature) — la dimensión es el *peso*, no la naturaleza;
- saltear gates de verificación en ningún perfil: toda tarea termina con VERIFICATION_REPORT.

---

# Definitions

## Perfiles

| Perfil | Criterio de asignación | Artefactos obligatorios | Gates |
|---|---|---|---|
| `trivial` | Cambio acotado: ≤ 3 archivos, sin decisiones de diseño, sin ambigüedad de requisitos, sin impacto en interfaces públicas | TASK_ANALYSIS, EXECUTION_PLAN, VERIFICATION_REPORT | H00, H04, H06 |
| `standard` | El default. Cualquier tarea que no cumpla trivial ni complex | Ciclo vigente completo (01–11) | H00–H15 según transiciones |
| `complex` | Múltiples subsistemas, decisiones de arquitectura, o riesgo alto declarado | Ciclo completo + REVIEW_REPORT + discovery si aplica | Ciclo completo + gate de revisión |

## Reglas del modelo

1. **El perfil se asigna una vez**, en la fase 01, y queda registrado en `TASK_ANALYSIS.md` con justificación. La policy H00 valida la presencia del perfil y la coherencia básica de la justificación.
2. **Solo se escala hacia arriba:** si durante la ejecución la tarea revela complejidad no vista (ambigüedad, scope creep), el Orchestrator reclasifica hacia `standard` o `complex` y completa los artefactos faltantes. Nunca se reclasifica hacia abajo.
3. **Los gates omitidos por perfil quedan registrados** en `HARNESS_REPORT.md` como `skipped: profile`, no como ausencia — la omisión es decisión del sistema, no descuido.
4. NEEDS_CLARIFICATION y RECOVERY aplican a todos los perfiles: una tarea trivial ambigua se reclasifica, no se fuerza.

---

# Consequences

- El coste operativo deja de ser uniforme: tareas triviales pasan de ~23 archivos a ≤ 5.
- El protocolo se vuelve usable en el día a día sin sacrificar rigor donde importa: `standard` y `complex` conservan el ciclo completo.
- La reclasificación solo ascendente evita el gaming (declarar trivial para saltear gates) sin introducir mecanismos punitivos.
- La política H00 y los decision trees ganan una dimensión de validación nueva (perfil), extensión de mecanismos existentes.

---

# Compatibility

Breaking change moderado: `TASK_ANALYSIS.md` gana un campo obligatorio (perfil + justificación), y las policies validan conjuntos por perfil. Las sesiones anteriores se leen como `standard`. No se tocan contratos de artefactos salvo el campo nuevo de TASK_ANALYSIS, ni la máquina de estados (las transiciones son las mismas; el perfil determina qué subconjunto es obligatorio).

---

# Relationship with Previous RFCs

- **RFC-18 — Failure & Recovery Taxonomy**: NEEDS_CLARIFICATION/RECOVERY se preservan en todos los perfiles; la reclasificación usa los mismos caminos.
- **RFC-24 — Skill Lifecycle Model**: el perfil `trivial` reduce también las skills aplicables por fase; el cableado de skills se define por fase, y el perfil determina qué fases existen.
- **RFC-22 — Session & Iteration Lifecycle Model**: los artefactos de sesión (SESSION_BRIEF, SESSION_LOG, HARNESS_REPORT, METRICS) se mantienen en todos los perfiles.

---

# Rationale

Se eligió peso de tarea (y no tipo) como dimensión de perfil porque el problema medido es el overhead, no la variedad funcional. Se eligió asignación por el task_analyst con validación de policy sobre clasificación automática porque los criterios (n° de archivos, ambigüedad, impacto en interfaces) requieren juicio sobre el contexto del proyecto que una heurística de código no tiene. La regla de escalado solo ascendente sigue el principio del protocolo de no-asunción: ante la duda, más rigor, nunca menos.

---

# Future Extensions

- **Calibración con métricas:** tras N sesiones con `METRICS.md` (tokens, minutos, gates por perfil), ajustar los umbrales de asignación con datos reales.
- **Perfil sugerido por heurística:** el runner puede *proponer* un perfil (conteo de archivos tocados, keywords) que el task_analyst confirma — reduce el juicio sin automatizarlo.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Proposal). Tres perfiles, criterios objetivos, regla de escalado ascendente, registro de gates omitidos como `skipped: profile`. | Análisis crítico de adopción (2026-08-05): ~23 archivos / ~52 min por tarea en dogfooding |
| 2026-08-05 | Corrección de numeración de gates del perfil trivial: `H00, H05, H10` → `H00, H04, H06` (H04 = execution-plan, H06 = verification-report; H05 es execution-completed y H10 es el gate opcional de KB). El conjunto anterior saltearía la validación del plan y exigiría un gate opcional. | Detectado al ejecutar el plan 26 (hook enforcement requiere H04 PASS para escribir deliverables) |
| 2026-08-11 | Aceptación retroactiva (`Proposal` → `Accepted`): regularización del desfase de gobernanza; el plan 25 ya ejecutó el modelo. | Regularización de auditoría 2.0.1 (decisión del usuario, 2026-08-11) |
| 2026-08-14 | Enmienda (plan 59): el perfil `trivial` usa la arista explícita `ANALYZING_TASK → PLANNING` y un conjunto reducido de inputs (`TASK_ANALYSIS.md` como referencia de tarea; sin artefactos de contexto). Corrige la afirmación de Compatibility ("las transiciones son las mismas"): el camino trivial sí requiere una arista nueva, condicionada al perfil, validada por H00 y documentada en la taxonomía. | Decisión del usuario (2026-08-14): opción 1 — legalizar el camino trivial (`AUDITORIA_SISTEMA.md` Nivel 3.1) |
