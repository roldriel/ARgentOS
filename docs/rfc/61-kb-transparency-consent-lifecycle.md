# RFC-61 — Consentimiento y visibilidad del discovery
**Status:** Accepted (2026-08-24, autorización explícita del usuario)
**Fecha:** 2026-08-23
**Serie:** —
**Origen:** Discusión de diseño con el mantenedor (2026-08-23): el discovery se ejecuta sin consentimiento ni visibilidad para el usuario.
**Pregunta:** ¿Cómo hace ARgentOS que el discovery — trabajo no pedido explícitamente — sea consentido y visible para el usuario?
**Afectados:** `.agents/orchestrators/core/roles/orchestrator.md` (§4.3), `.agents/features.toml`, `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`, `.agents/orchestrators/discovery/roles/discovery_orchestrator.md`, `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` (o el artefacto de cierre de tarea), `.agents/skills/INDEX.md` + nueva skill, `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `.agents/standards/runtime/PROTOCOL_METRICS.md` + contrato `METRICS.md`.
**Alcance:** este RFC cubre consentimiento (gate), visibilidad (reporte de cierre) e invocación manual (skill `/discovery`). La persistencia de conocimiento verificado durante la ejecución (volcado task-derived a la KB de discovery, frescura) queda fuera de alcance y se trata en el RFC-62.
## Problema
Cuando `.project/knowledge/discovery/` no existe (caso típico: proyecto en desarrollo que adopta el protocolo), el core Orchestrator invoca un discovery `full` automáticamente antes de la primera tarea (`.agents/orchestrators/core/roles/orchestrator.md` §4.3, condición 1). Lo mismo ocurre ante TTL vencido, cambio de hash o inconsistencia reportada. El usuario nunca es consultado ni notificado activamente: se entera solo si observa los tool calls o lee `SESSION_LOG.md`. Una tarea de "creá un endpoint" puede demorar decenas de minutos sin que el usuario sepa por qué.
La consecuencia práctica: ARgentOS ejecuta trabajo que el usuario no pidió, sin avisar. Esto contradice el principio de transparencia del protocolo y el espíritu de No-Assumption Enforcement: ante una decisión con costo relevante y alternativas legítimas (scope, o directamente no correr discovery), el protocolo consulta — excepto aquí.
## Principio rector
Ningún trabajo no pedido se ejecuta sin consentimiento explícito del usuario. El consentimiento no es una configuración global implícita: es una decisión por evento, con opciones concretas y costos visibles. Ante ausencia de respuesta clara, el protocolo pide clarificación — nunca asume un scope por defecto.
## Decisión propuesta
Tres ejes:
### Eje 1 — Gate de consentimiento en discovery
**Detección.** El core Orchestrator mantiene las condiciones de detección actuales de §4.3 (KB inexistente, TTL vencido, hash cambiado, inconsistencia reportada). Lo que cambia es la acción: al detectar una condición, **no invoca** al Discovery Orchestrator; presenta al usuario una consulta con el formato de clarificación existente (No-Assumption Enforcement: al menos dos opciones concretas + opción libre):
1. Qué condición disparó la necesidad (KB inexistente / TTL vencido / hash cambiado / inconsistencia), con el detalle disponible (qué TTL, qué hash, qué inconsistencia).
2. Opciones concretas con costo relativo explícito:
   - `full` — discovery completo (todas las entradas; el más costoso).
   - `lite` — scope nuevo (ver Eje 3): entorno, lenguaje, stack y arquitectura, sin análisis cualitativo profundo.
   - **Sin discovery** — continuar sin KB, con la degradación documentada (equivalente al "minimal discovery" que hoy es fallback de fallo: las delegaciones operan sin contexto KB).
3. Opción libre ("otra respuesta").
**Ante silencio o respuesta vaga** ("dale, seguí", respuestas ambiguas): el Orchestrator **no ejecuta ningún scope**; pide clarificación de nuevo, como en cualquier otra ambigüedad. No hay default de ejecución.
**Sesión no interactiva o canal de consulta degradado** (no hay usuario disponible para responder): no se ejecuta discovery; se continúa sin KB y se registra en `SESSION_LOG.md` la condición detectada y la razón del bypass. Esto es coherente con el principio rector: sin posibilidad de consentimiento, no hay trabajo no pedido.
**Flag.** Un único flag nuevo en `.agents/features.toml`:
- `discovery_require_consent = true` (default). Declarativo, registrado en `SESSION_LOG.md` como el resto de los flags activos. Con `false` se restaura íntegramente el comportamiento automático actual (invocación directa según la tabla de scopes de §4.3, sin consulta).
**Registro.** Cada evento de gate se registra en `SESSION_LOG.md`: condición disparada, opciones presentadas, decisión del usuario (scope elegido, rechazo, o bypass por sesión no interactiva), y timestamp. Nuevo evento de métricas en el contrato `METRICS.md` (ej. `discovery_consent`) con esos campos; las métricas siguen siendo advisory (no gatean nada).
### Eje 2 — "Qué aprendimos" en el cierre de la tarea
Al finalizar la tarea, el feedback de cierre incluye una sección breve **"Qué aprendimos"** con el resumen del conocimiento persistido durante la sesión (en el alcance de este RFC: entradas de `.project/knowledge/entries/`; cuando exista el RFC-62, también el volcado task-derived a `knowledge/discovery/`).
Reglas explícitas:
- **La curación es del agente.** El agente decide por su cuenta qué aprendizajes merecen persistirse, aplicando el filtro existente de `KNOWLEDGE_CURATION.md`. El usuario no elige entrada por entrada ni aprueba la persistencia.
- **La sección es informativa, no transaccional.** Reporta lo que ya quedó persistido ("Persistí en `entries/...`: ..."). No requiere acción del usuario. Si el usuario detecta un error, puede pedir la corrección como en cualquier otra salida del protocolo; si no dice nada, no pasa nada.
- **Condicional.** Si la tarea no produjo aprendizajes que pasen el filtro, la sección no aparece (no se reporta el vacío).
- **Responsable:** el core Orchestrator, como paso del feedback de cierre posterior a la transición `VERIFYING → COMPLETED` (gated por H06/H07). El contenido se obtiene de lo efectivamente persistido durante la sesión; el verifier no cambia de responsabilidades y `VERIFICATION_REPORT.md` no se modifica.
### Eje 3 — Skill `/discovery` (user-invoked)
Nueva skill invocable por el usuario:
- `/discovery` — sin argumentos, ejecuta scope `full`.
- `/discovery full` — igual que sin argumentos.
- `/discovery lite` — ejecuta scope `lite`.
Reglas explícitas:
- **Sin gate de consentimiento:** la invocación explícita del usuario *es* el consentimiento.
- Sigue el precedente de `suggest-commits`: skill user-invoked, registrada en `skills/INDEX.md` con la nota correspondiente, **fuera de la activation table por diseño** (no es parte del workflow de tareas).
- Invoca al Discovery Orchestrator con el scope indicado y reporta el resultado al usuario al terminar (entradas escritas/actualizadas, stale marcados, duración).
- **Scope `lite` (nuevo, se define también en `DISCOVERY_STATE_MACHINE.md`):** `init_worker` + `environment_worker` + `stack_worker` + `framework_worker` + `synthesis_worker`. Respeta el grafo de dependencias existente (`DISCOVERY_FRAMEWORK` depende de `DISCOVERY_STACK`; `DISCOVERY_MERGE` — synthesis — cierra todo run). Equivale al scope `stack` actual más `environment_worker`: entorno, lenguaje, stack y arquitectura, sin el análisis cualitativo profundo de `patterns`/`business`.
## Alternativas consideradas
- **Default `lite` ante silencio o respuesta vaga**: descartado. Ejecutar cualquier scope sin respuesta clara es ejecutar trabajo no consentido — contradice el principio rector. Ante vaguedad se pide clarificación, como en todo el protocolo.
- **Consultar solo el primer discovery y dejar los refrescos por TTL automáticos**: descartado como comportamiento por defecto; la consulta aplica a toda condición de detección. El usuario que prefiera el comportamiento automático completo tiene `discovery_require_consent = false`.
- **Que el usuario elija/apruebe qué conocimiento se persiste en el cierre**: descartado; le delega al usuario trabajo de curación que corresponde al agente, y no escala.
- **Notificación pasiva sin consulta** (avisar "voy a correr discovery" y seguir): descartado; un aviso que no espera respuesta no es consentimiento, y la tarea igual se demora sin que el usuario pudiera evitarlo.
## Impacto en el protocolo
| Archivo | Cambio |
|---|---|
| `.agents/orchestrators/core/roles/orchestrator.md` §4.3 | La detección pasa a producir una consulta al usuario (formato No-Assumption); la respuesta determina scope (`full`/`lite`), rechazo, o re-clarificación. Bypass documentado en sesión no interactiva. Paso de cierre con sección "Qué aprendimos". |
| `features.toml` | Flag nuevo `discovery_require_consent` (default `true`). |
| `DISCOVERY_STATE_MACHINE.md` | Scope nuevo `lite` en la tabla de scopes. |
| `discovery_orchestrator.md` + workers | Tabla de scopes con `lite` (sin cambios en la lógica de workers: el subconjunto respeta el grafo existente). |
| Cierre de tarea (orchestrator) | Sección condicional "Qué aprendimos" en el feedback post `VERIFYING → COMPLETED`. |
| `skills/discovery/SKILL.md` + `skills/INDEX.md` | Skill user-invoked nueva, fuera de la activation table. |
| `PROTOCOL_TAXONOMY.md`, `PROTOCOL_METRICS.md` + `METRICS.md` | Evento nuevo de consentimiento de discovery (condición, opciones, decisión, timestamp). |
## Criterios de aceptación
- [ ] Con `discovery_require_consent = true`, el core Orchestrator nunca invoca discovery sin una decisión explícita del usuario en esa sesión, y registra condición + decisión en `SESSION_LOG.md`.
- [ ] Ante silencio o respuesta vaga, el Orchestrator pide clarificación; no ejecuta ningún scope por defecto.
- [ ] En sesión no interactiva no se ejecuta discovery; el bypass queda registrado con su razón.
- [ ] Con `discovery_require_consent = false` el comportamiento es idéntico al actual (invocación automática según §4.3).
- [ ] El cierre de tarea incluye "Qué aprendimos" solo cuando hay aprendizajes persistidos que reportar, y la sección no requiere acción del usuario.
- [ ] `/discovery` sin argumentos ejecuta `full`; `/discovery lite` ejecuta el scope `lite` definido; `/discovery full` equivale a sin argumentos.
- [ ] El scope `lite` figura en `DISCOVERY_STATE_MACHINE.md` y respeta el grafo de dependencias del pipeline.
- [ ] El evento de consentimiento está en el catálogo del contrato `METRICS.md` y referenciado en la taxonomía.
- [ ] La batería de verificación del repo corre en verde.
## Amendment Log
| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-23 | Creación (Proposal) | Discusión de diseño con el mantenedor |
| 2026-08-24 | Reescritura tras revisión crítica: el RFC se divide. Este documento conserva consentimiento (Eje 1), visibilidad (Eje 2) y skill `/discovery` (Eje 3). El volcado de conocimiento task-derived y la frescura de la KB pasan al RFC-62. Se elimina el default `lite` ante silencio (ahora: pedir clarificación), el flag separado de TTL y el framing de "spam de consultas"; se fijan explícitamente nombre de flag, responsable del reporte de cierre y comportamiento en sesión no interactiva. | Revisión crítica con el mantenedor |
| 2026-08-24 | Accepted (autorización explícita del usuario); citas de `orchestrator.md` corregidas a la ruta completa del payload (`.agents/orchestrators/core/roles/orchestrator.md`). | Revisión previa a la redacción del plan |
