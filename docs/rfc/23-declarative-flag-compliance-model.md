# RFC-23 — Declarative-Flag Compliance Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define el **modelo conceptual de cumplimiento de los feature flags declarativos**: qué significa que un flag `[declarative]` esté *enabled*, qué obligación genera sobre los agentes que lo consumen, qué clase de fallo es ignorarlo y qué evidencia mínima debe quedar registrada para que su cumplimiento sea auditable a posteriori. Cierra el gap 7 de `plans/analisis-explicitud.md`.

Hoy `.agents/features.toml` (§"Consumption") anota honestamente qué flags lee el harness (`[code]`) y cuáles consumen agentes (`[declarative]`), y `standards/INDEX.md` (§"Feature flags") obliga al Orchestrator a consultarlos y registrarlos en `SESSION_LOG.md`. Pero ningún modelo define la obligación que un flag declarativo genera ni vincula el registro de flags activos (`.agents/contracts/SESSION_LOG.md`, §"Required content": "Feature flags active") con ninguna verificación: una sesión puede ignorar `caveman`, `llm_discovery` o `discovery_orchestrator` sin que nada lo detecte.

El modelo clasifica el incumplimiento de un flag declarativo en la taxonomía de fallos de RFC-18 (`plans/rfc/18-failure-recovery-taxonomy.md`), sin introducir clases nuevas, y declara la validación mecánica de la evidencia como Future Extension.

---

# Motivation

- Un flag `[code]` tiene cumplimiento mecánico: el harness lo lee y gatea (`.agents/features.toml`, §"Consumption"). Un flag `[declarative]` solo puede cumplirse *leyéndolo y actuando en consecuencia* — y nada define qué significa eso: ni lectura obligatoria, ni punto del flujo donde se consume, ni consecuencia de ignorarlo.
- El inventario real es más rico que "flags booleanos": hay settings declarativos no booleanos (`discovery_sample_size`, TTLs) y flags **duales** de technical practices que el harness lee *y* los workers consumen declarativamente (`.agents/features.toml`, §"Technical practices"). Sin categorías conceptuales, no se puede decir qué obligación tiene cada uno.
- El contrato de `SESSION_LOG.md` (§"Required content", §"Initial entry template") ya obliga a registrar los flags activos al inicio de sesión, pero ese registro no está vinculado a verificación alguna: es evidencia huérfana. Ningún documento define qué más debe quedar registrado para auditar que un flag enabled fue efectivamente respetado.
- Ignorar un flag declarativo no tiene clase de fallo asignada: no es un harness FAIL (nadie lo gatea), no es un blocker (la fase completa igual), y sin clasificación tampoco tiene destino conceptual (RFC-18).

---

# Goals

- Definir la **distinción formal** entre las tres categorías de flags que `features.toml` ya anota: `[code]`, `[declarative]` y dual.
- Definir la **obligación declarativa**: lectura obligatoria, punto del flujo de consumo y clase de fallo de ignorarlo.
- Definir la **evidencia de cumplimiento**: la entrada mínima que hace auditable a posteriori el cumplimiento de un flag declarativo, construida sobre la obligación ya existente del contrato de `SESSION_LOG.md`.
- Aplicar el modelo como **inventario de instancias** a los flags booleanos declarativos, a los settings declarativos de discovery y al consumo declarativo de los flags duales de technical practices.
- Dejar la distinción conceptual aplicada inline en `.agents/` (frontera documental): sección "Feature flags" de `standards/INDEX.md` y nota de consumo de `features.toml`.

---

# Non Goals

Esta RFC no propone:

- convertir flags declarativos en `[code]` (decisión de runtime, fuera del alcance conceptual);
- crear flags nuevos ni cambiar valores de los existentes;
- validación mecánica de la evidencia por el harness runner (Future Extension);
- modificar el contrato de `SESSION_LOG.md`: el modelo se construye sobre su obligación ya vigente (§"Required content"), no la reformula;
- mecanismos de override por sesión más allá de los ya existentes (variables de entorno `AGENTS_FEATURE_`, `standards/INDEX.md` §"Feature flags").

---

# Definitions

## Categorías de flag

Un feature flag se clasifica según **quién lo consume**, no según su tipo de dato:

- **Flag `[code]`:** lo consume el harness (código Python: `feature_flags.py`, `health_check.py`, runner). Su cumplimiento es **mecánico**: si el flag está enabled, el comportamiento gateado ocurre o el health-check/la policy falla. No requiere evidencia declarativa: la traza de ejecución del harness es la evidencia.
- **Flag `[declarative]`:** lo consumen agentes leyendo `features.toml` (directamente o vía `runner.py features`). El harness solo lo resuelve y expone. Su cumplimiento es **por conducta**: un agente debe leerlo y actuar en consecuencia en el punto del flujo que le corresponde.
- **Flag dual:** `[code]` + declarativo. El harness lo lee (presencia de estándares en health-check, validadores semánticos) *y* los workers lo consumen declarativamente durante la ejecución (los flags de technical practices: `tdd`, `srp`, …). Tiene dos obligaciones independientes: la mecánica (cubierta por el harness) y la declarativa (sujeta a este modelo).

La categoría es una propiedad del flag, no del consumidor: un mismo agente puede consumir flags de las tres categorías.

## Obligación declarativa

Un flag declarativo **enabled** genera una obligación con tres componentes:

1. **Lectura obligatoria:** el agente que consume el flag debe conocer su valor antes del punto del flujo donde el flag condiciona conducta. El mecanismo de resolución ya existe (`runner.py features` / `feature_flags.all_flags()`); la obligación es consumirlo, no solo poder hacerlo.
2. **Punto de consumo:** cada flag declarativo tiene un punto del flujo donde se aplica (p. ej. `caveman` en toda comunicación de protocolo; `discovery_orchestrator` en la decisión de mantener la KB de discovery, orchestrator.md §"4.3 Discovery Orchestrator Invocation"). Fuera de ese punto el flag no obliga; dentro, obliga siempre que esté enabled.
3. **Clase de fallo:** ignorar un flag declarativo enabled — no leerlo, o leerlo y no actuar — es una **deviation (F2)** de la taxonomía de RFC-18: diferencia entre lo especificado (el flag habilita una conducta estándar) y lo ejecutado. Su destino conceptual es warning loggeado; si la omisión es material para los criterios de aceptación o el scope (p. ej. ignorar `tdd` en una tarea cuya especificación exige TDD), se reclasifica como F1 (recovery) o F3 (clarificación) según la regla de reclasificación de F2. Deshabilitar el flag *no* es una desviación: el usuario puede apagarlo vía `AGENTS_FEATURE_` y la obligación desaparece con el flag.

## Evidencia de cumplimiento

La evidencia mínima que hace auditable el cumplimiento de un flag declarativo se construye en dos piezas:

1. **Registro de flags activos** (ya obligatorio): la entrada inicial de `SESSION_LOG.md` con "Feature flags active" (`.agents/contracts/SESSION_LOG.md`, §"Required content" y §"Initial entry template"). Es la *declaración de obligaciones vigentes* de la sesión: todo flag declarativo listado ahí genera la obligación del punto 2.
2. **Declaración de consumo:** cuando un flag declarativo condiciona la conducta de un agente, esa condición queda declarada en el artefacto que el agente produce o en la entrada de `SESSION_LOG.md` del evento correspondiente. La declaración nombra el flag y el efecto aplicado (p. ej. una delegación que declara el nivel `caveman`; una invocación del Discovery Orchestrator registrada como evento). Para los flags duales de technical practices, la declaración de consumo ya existe en forma de evidencia de práctica (p. ej. la evidencia red-green-refactor de TDD en `EXECUTION_SUMMARY.md`).

**Auditabilidad a posteriori:** la auditoría conceptual es un *join* entre las dos piezas: cada flag declarativo listado como activo (pieza 1) debe tener al menos una declaración de consumo coherente en los artefactos de la sesión (pieza 2), o una desviación F2 explícita que explique su no-aplicación. Un flag activo sin declaración de consumo ni desviación registrada es **cumplimiento no evidenciado**: no prueba incumplimiento, pero es exactamente el agujero que este modelo cierra — y su detección mecánica queda declarada como Future Extension.

La evidencia nunca se reescribe retroactivamente (integridad de los artefactos de sesión, RFC-22): una omisión descubierta tarde se registra como desviación F2, no se parcha el log.

---

# Inventory

Aplicación del modelo a las instancias vigentes (fuente: `.agents/features.toml`; catálogo: `.agents/standards/INDEX.md`, §"Feature flags").

## Flags booleanos `[declarative]`

| Flag | Punto de consumo | Conducta obligada cuando enabled |
|---|---|---|
| `caveman` | Toda comunicación de protocolo; la delegación declara el nivel (orchestrator.md, §"5. Worker Delegation"); la entrada inicial del propio `SESSION_LOG.md` (orchestrator.md, §"4. Feature Flag Awareness") | Aplicar `.agents/standards/communication/CAVEMAN.md` a los artefactos y mensajes. |
| `llm_discovery` | Fase de context gathering / dominio discovery | Usar el discovery basado en LLM en lugar del fallback. |
| `discovery_orchestrator` | Decisión del Orchestrator de mantener la KB de discovery (orchestrator.md, §"4.3 Discovery Orchestrator Invocation") | Invocar al Discovery Orchestrator del dominio `discovery` ante los disparadores de detección. |

## Settings declarativos de discovery

Los settings no booleanos (`discovery_sample_size`, `discovery_environment_ttl_hours`, `discovery_project_ttl_hours`) son flags declarativos *valorados*: la obligación no es "aplicar/no aplicar" sino **acotar la conducta al valor resuelto** — el muestreo de los workers de discovery (`.agents/orchestrators/discovery/roles/discovery_orchestrator.md`, §"Sampling") y la evaluación de staleness de la KB por TTL (mismo archivo, detección de necesidad de KB). La declaración de consumo es el propio valor usado, observable en los artefactos de discovery (payloads con `sample_size`, entradas de KB con TTL). Incumplirlos (muestrear sin cota, ignorar TTL) es deviation F2.

## Flags duales de technical practices

`tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`, `screaming_architecture`, `clean_architecture`, `dry`, `layered_architecture`, `grasp`, `ddd_tactical`, `ddd_strategic`, `architecture_contract`:

- **Obligación mecánica** (categoría `[code]`): presencia de estándares en health-check y validadores semánticos H01/H05 (`.agents/features.toml`, §"Technical practices"). Fuera del alcance de este modelo.
- **Obligación declarativa:** el worker que ejecuta aplica el estándar habilitado; el Orchestrator incluye `technical_approach` en la delegación cuando alguno está enabled (orchestrator.md, §"5. Worker Delegation"). La evidencia de cumplimiento es la evidencia de práctica en los artefactos de ejecución (p. ej. evidencia TDD en `EXECUTION_SUMMARY.md`) o una desviación F2 justificada.

---

# Consequences

- "Flag habilitado" deja de ser un dato sin consecuencia: cada flag declarativo activo en `SESSION_LOG.md` es una obligación auditable, con clase de fallo (F2) y destino conceptual definidos.
- El registro de flags activos del contrato de `SESSION_LOG.md` queda vinculado a verificación conceptual: es la pieza 1 del join de auditoría. El gap entre "flag activo" y "flag respetado" pasa de invisible a detectable (conceptualmente hoy; mecánicamente como Future Extension).
- La distinción de categorías ordena futuras mecanizaciones (serie 15+): un flag `[declarative]` solo puede convertirse en `[code]` si su punto de consumo es gateable; los duales muestran que ambas obligaciones pueden coexistir.
- Ningún archivo de `.agents/` referencia esta RFC: la distinción y la obligación se definen inline en `standards/INDEX.md` (§"Feature flags") y en la nota de consumo de `features.toml` (frontera documental).

---

# Compatibility

Cambio conceptual y documental. No se modifican valores de flags, ni el runner, ni validadores, ni contratos: la obligación declarativa y la evidencia se apoyan en mecanismos ya vigentes (registro inicial de `SESSION_LOG.md`, resolución por `runner.py features`, campos de delegación existentes). Las adiciones en `standards/INDEX.md` y `features.toml` son prosa autocontenida.

---

# Relationship with Previous RFCs

- **RFC-18 — Failure & Recovery Taxonomy** (`plans/rfc/18-failure-recovery-taxonomy.md`, Accepted): dependencia directa. El incumplimiento de un flag declarativo se clasifica como deviation F2 con su regla de reclasificación; esta RFC no introduce clases nuevas. La audiencia de evaluación machine/agent de RFC-18 es el mismo eje conceptual que la distinción `[code]`/`[declarative]`, aplicado a policies en vez de a flags.
- **RFC-22 — Session & Iteration Lifecycle Model** (`plans/rfc/22-session-iteration-lifecycle-model.md`, Accepted): la evidencia de cumplimiento hereda la integridad de los artefactos de sesión (conformidad y fidelidad del log): la evidencia no se reescribe retroactivamente; las omisiones se registran como desviaciones.

---

# Rationale

Se eligió definir la obligación por **categoría de consumidor** (quién lee el flag) y no por tipo de dato o subsistema, porque el gap es exactamente ese: el mismo archivo de configuración mezcla flags que la máquina fuerza y flags que solo la conducta honra, y sin nombrar la diferencia no hay forma de exigir evidencia. La evidencia se construye **sobre el registro ya obligatorio** de `SESSION_LOG.md` en lugar de crear un artefacto nuevo porque el contrato ya resolvió la mitad del problema (declarar obligaciones vigentes) y lo que faltaba era la segunda pieza (declaración de consumo) y el join conceptual entre ambas. Clasificar el incumplimiento como F2 (y no como clase nueva) sigue el precedente de RFC-22: las condiciones anómalas del protocolo ya tienen taxonomía; lo que faltaba era decir que ignorar un flag es una instancia de ella.

---

# Future Extensions

- **Validación mecánica de la evidencia:** una policy de harness que verifique el join de auditoría (flags declarativos activos vs. declaraciones de consumo en artefactos de sesión). Requiere definir primero cómo se declara el consumo de forma parseable; queda fuera de esta RFC por ser mecanización, no concepto.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Accepted). Categorías de flag (`[code]`/`[declarative]`/dual), obligación declarativa (lectura, punto de consumo, F2), evidencia de cumplimiento en dos piezas, inventario de instancias. | Plan `plans/14-declarative-flag-compliance.md` (gap 7 de `plans/analisis-explicitud.md`) |
