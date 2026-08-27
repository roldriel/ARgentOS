# RFC-22 — Session & Iteration Lifecycle Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define el **modelo conceptual del ciclo de vida de una sesión y de sus iteraciones**: qué es una sesión, qué es una iteración, cuándo empieza y termina cada una, qué regla conceptual gobierna la secuencia `<order>` de artefactos dentro de una iteración, qué hace íntegros a los artefactos de sesión (`SESSION_LOG.md`, `SESSION_BRIEF.md`) y qué es una **desviación retroactiva**. Cierra el gap 4 de `plans/analisis-explicitud.md`.

Hoy esas reglas existen pero están distribuidas y sin modelo que las justifique: la regla MUST de carpetas de iteración y la convención `<order>-ARTIFACT_NAME.md` viven en `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (§"Artifact Safety Rule"); la prohibición de artefactos retroactivos vive en la No-Skip Rule de `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`; la prohibición de reescribir el log vive en `.agents/contracts/SESSION_LOG.md` (§"Constraints"); y la mecánica de sesión vive en `.agents/orchestrators/core/roles/orchestrator.md` (§"1. Session Management"). Ninguna define los conceptos — sesión, iteración, reanudación, iteración parcial — sobre los que esas reglas operan.

El modelo clasifica la violación de integridad de los artefactos de sesión en la taxonomía de fallos de RFC-18 (`plans/rfc/18-failure-recovery-taxonomy.md`), sin introducir clases nuevas.

---

# Motivation

- La apertura de una iteración nueva vs. continuar en la actual es una regla MUST sin criterio para casos borde: ¿qué pasa cuando el runtime reanuda una sesión (p. ej. el comando de resume del CLI actual)? ¿Cuándo una iteración queda *parcial* y qué significa retomarla? Sin modelo, cada respuesta es una decisión ad hoc.
- `<order>` está definido como "generation/reading sequence" (BOUNDARIES, §"Artifact Safety Rule") sin regla conceptual: no se dice qué propiedad del flujo refleja ni qué lo viola.
- `SESSION_LOG.md` y `SESSION_BRIEF.md` tienen contrato pero ningún trigger los valida: nada declara qué los hace íntegros ni qué clase de fallo es su violación.
- La desviación retroactiva está prohibida en dos lugares (state machine, No-Skip Rule; contrato de SESSION_LOG, §"Constraints") sin concepto único: cada archivo la describe a su manera y ninguno la clasifica.
- Las cuatro fuentes normativas pueden derivar: sin modelo conceptual común, una edición en una de ellas no obliga a revisar las otras.

---

# Goals

- Definir **sesión** y sus límites: inicio, terminación y reanudación.
- Definir **iteración** y sus límites: cuándo el trabajo abre `.project/<session-uuid>/<iteration>/` nuevo vs. continúa en el actual, incluidos los casos borde (reanudación, iteración parcial).
- Definir la regla conceptual de **`<order>`** como secuencia de artefactos dentro de una iteración.
- Definir la **integridad de los artefactos de sesión** y clasificar su violación.
- Definir la **desviación retroactiva** como concepto único.
- Consolidar el marco conceptual de las reglas distribuidas, dejando la regla canónica inline en cada archivo de `.agents/` (frontera documental).

---

# Non Goals

Esta RFC no propone:

- políticas de retención, limpieza o archivado de sesiones;
- cambios al layout de `.project/` ni a la convención de nombres;
- nuevas policies o triggers de harness (la validación por harness de integridad de sesión queda declarada como Future Extension);
- mecanismos técnicos de persistencia o reanudación del runtime;
- cambios a la state machine (estados, transiciones, triggers): el modelo opera sobre el flujo ya definido.

---

# Definitions

## Sesión

Una **sesión** es la unidad de continuidad del protocolo: todo el trabajo realizado bajo un mismo identificador de sesión (`.project/<session-uuid>/`). Una sesión agrega una o más iteraciones y los artefactos de sesión (`SESSION_LOG.md`, `SESSION_BRIEF.md`, `HARNESS_REPORT.md`) que las describen.

- **Inicio:** una sesión comienza cuando el Orchestrator acepta una tarea del usuario y genera el identificador de sesión con su `SESSION_LOG.md` inicial (orchestrator.md, §"1. Session Management"). El inicio queda registrado en la primera entrada del log.
- **Terminación:** una sesión termina cuando el runtime cierra el contexto de ejecución — normalmente tras un estado terminal (`COMPLETED` o `ABORT`), pero la terminación es un hecho del runtime, no un estado del protocolo: una sesión puede terminar en cualquier punto si el runtime se cierra.
- **Reanudación:** el runtime puede reanudar una sesión terminada (p. ej. el comando de resume del CLI actual). La reanudación es **continuidad vía estado persistido**: la sesión reanudada conserva su identificador, su log y sus iteraciones; el log y el brief son el estado desde el cual el protocolo reconstruye dónde quedó el trabajo. La reanudación no crea una sesión nueva ni reescribe la historia: el log continúa appendando entradas.

## Iteración

Una **iteración** es la unidad de trabajo del protocolo dentro de una sesión: una pasada completa del workflow para una petición del usuario, con su propio conjunto de artefactos bajo `.project/<session-uuid>/<iteration>/`.

- **Apertura:** cada petición del usuario — o pasada completa del workflow — abre una iteración nueva, numerada secuencialmente (`00/`, `01/`, …). La iteración es el contenedor de la traza de esa pasada: dos peticiones no comparten iteración aunque la segunda dependa de la primera.
- **Continuación dentro de la iteración actual:** los loops internos de una misma pasada no abren iteración nueva. Son loops internos: el ciclo `NEEDS_CLARIFICATION` (la clarificación alimenta la pasada que la pidió), el loop de recovery (`RECOVERY → PLANNING` o `→ NEEDS_CLARIFICATION`), y los retries acotados del reviewer o del harness. El criterio conceptual es el de *petición*: una iteración sirve a una petición; lo que sirve a la misma petición continúa en su iteración.
- **Iteración parcial:** una iteración que no alcanzó un estado terminal (`COMPLETED`/`ABORT`) antes de que la sesión terminara. Es una condición observable, no un fallo en sí misma. Al reanudar la sesión: si el usuario retoma la misma petición, el trabajo continúa en la iteración parcial, retomando desde el último artefacto íntegro según el log; si el usuario hace una petición nueva, se abre una iteración nueva y la parcial queda como traza histórica. Lo que una iteración parcial nunca hace es reescribirse: los artefactos ya producidos no se regeneran retroactivamente (ver §Desviación retroactiva).

## Secuencia de artefactos (`<order>`)

`<order>` es la **secuencia de generación** de los artefactos dentro de una iteración: un ordinal que refleja el orden en que el flujo produjo cada artefacto. Reglas conceptuales:

1. `<order>` es monótono con el flujo: un artefacto producido después lleva un ordinal mayor.
2. `<order>` es una propiedad de la traza, no un parámetro libre: el ordinal asignado a un artefacto declara cuándo fue producido, y esa declaración es auditable contra el `SESSION_LOG.md`.
3. La secuencia permite leer una iteración como historia: cualquier lector reconstruye el orden de ejecución a partir de los nombres de archivo (BOUNDARIES, §"Artifact Safety Rule").

Un `<order>` que no refleja el orden real de generación es una violación de integridad de la traza (§Integridad), no un error de estilo.

## Integridad de los artefactos de sesión

`SESSION_LOG.md` y `SESSION_BRIEF.md` son los artefactos de sesión con contrato (`.agents/contracts/`). Un artefacto de sesión es **íntegro** cuando cumple dos condiciones:

1. **Conformidad:** cumple su contrato (estructura, contenido requerido, ubicación).
2. **Fidelidad:** lo que declara corresponde a lo que ocurrió. Para el log: cada evento significativo tiene su entrada, ninguna entrada fue reescrita para ocultar fases salteadas o transiciones fallidas, y las entradas son append-only. Para el brief: su contenido refleja las decisiones efectivamente confirmadas por el usuario, no las que el agente habría preferido.

La conformidad es verificable mecánicamente; la fidelidad es auditable (el log contra los artefactos de las iteraciones, el brief contra los `INTENT_REFLECTION.md` y clarificaciones). Hoy ningún trigger valida ninguna de las dos; la validación por harness es Future Extension (§Future Extensions).

**Clasificación del fallo:** una violación de integridad de los artefactos de sesión es una **deviation (F2)** de la taxonomía de RFC-18: el trabajo pudo ser válido, pero la traza ya no describe fielmente el proceso. Si la falta de fidelidad es material para los criterios de aceptación o el scope, se reclasifica según la regla general de F2 (recovery F1, o clarificación F3 si requiere decisión del usuario). No se introduce ninguna clase de fallo nueva.

## Desviación retroactiva

Una **desviación retroactiva** es la creación de un artefacto fuera de su fase: producir después de la ejecución un artefacto que debió producirse durante ella, para "rellenar un hueco" de la traza. Es el caso particular de violación de `<order>` (el ordinal declara una posición que no corresponde a la generación real) y de fidelidad del log (el evento no fue registrado cuando ocurrió).

El concepto ya está prohibido en dos lugares normativos — la No-Skip Rule de la state machine y los Constraints del contrato de `SESSION_LOG.md` —; este modelo lo unifica:

1. Un artefacto retroactivo es una **deviation (F2)**, no una forma válida de completar una iteración.
2. Cuando una recovery lo justifica (no la conveniencia), el artefacto se marca explícitamente como retroactivo en el propio artefacto y en el log, con referencia a la decisión de recovery que lo autoriza.
3. Un artefacto retroactivo no marcado es además una violación de fidelidad: dos desviaciones, la de producción y la de ocultamiento.

---

# The Lifecycle (conceptual)

```text
runtime abre contexto
        │
        ▼
SESIÓN comienza ── Orchestrator genera <session-uuid> + SESSION_LOG.md inicial
        │
        ├─ petición del usuario ──► ITERACIÓN <nn> se abre
        │        │
        │        ├─ loops internos (clarificación, recovery, retries)
        │        │      └─► continúan en la misma iteración
        │        │
        │        ├─ artefactos producidos en secuencia <order> monótona
        │        │
        │        └─► estado terminal (COMPLETED/ABORT) o iteración parcial
        │
        ├─ nueva petición ──► ITERACIÓN <nn+1> se abre
        │
        ▼
runtime cierra contexto ── SESIÓN termina (en cualquier punto)
        │
        ▼
reanudación: misma sesión, estado reconstruido desde log + brief
        ├─ misma petición ──► continúa la iteración parcial
        └─ nueva petición ──► abre iteración nueva
```

---

# Consolidation of Distributed Rules

Las reglas hoy distribuidas quedan ancladas al modelo, cada una como regla canónica inline en su archivo (frontera documental: `.agents/` no referencia RFCs):

| Regla | Ubicación canónica | Concepto del modelo que la enmarca |
|---|---|---|
| Carpetas de iteración y `<order>-ARTIFACT_NAME.md` | `PROTOCOL_BOUNDARIES.md`, §"Artifact Safety Rule" | Iteración; Secuencia de artefactos |
| Prohibición de artefactos retroactivos | `AGENT_STATE_MACHINE.md`, No-Skip Rule | Desviación retroactiva |
| Log append-only, desviaciones explícitas | `SESSION_LOG.md` (contrato), §"Constraints" | Integridad (fidelidad) |
| Mecánica de sesión (UUID, log inicial, entradas) | `orchestrator.md`, §"1. Session Management" | Sesión (inicio, registro) |

La consolidación no mueve las reglas: las dota de un vocabulario común. Una edición futura en cualquiera de ellas se evalúa contra el modelo de esta RFC.

---

# Alternatives Considered

## Crear un archivo nuevo en `.agents/` con el modelo de ciclo de vida

Se descartó: el modelo es conceptual y las reglas ya tienen ubicaciones canónicas correctas (BOUNDARIES para filesystem, state machine para flujo, contratos para artefactos, rol para mecánica). Un archivo nuevo duplicaría o competiría con esas ubicaciones, violando la single-source policy (BOUNDARIES, §"Single-source documentation policy"). La RFC documenta el modelo; los archivos de `.agents/` se reescriben autocontenidos.

## Mover todas las reglas de sesión a un solo archivo canónico

Se descartó por la misma razón: las reglas pertenecen a dominios distintos (filesystem, flujo, contrato, rol) y la single-source policy ya asigna cada una a su dominio. El gap no era de ubicación sino de modelo.

## Modelar la reanudación como sesión nueva vinculada

Se descartó: rompería la append-only del log (la sesión "nueva" heredaría historia de la anterior) y contradice la práctica del runtime (el resume del CLI continúa el contexto, no lo clona). La continuidad vía estado persistido sobre el mismo identificador es más simple y fiel.

---

# Compatibility

Esta RFC no modifica:

- el layout de `.project/` ni la convención de nombres;
- la state machine (estados, transiciones, triggers);
- los contratos de `SESSION_LOG.md` / `SESSION_BRIEF.md` en su estructura;
- policies de harness ni runner;
- el runtime.

Los cambios documentales en `.agents/` son aclaraciones autocontenidas que conectan las reglas existentes con el vocabulario del modelo (§Documentation Impact).

---

# Documentation Impact

- **`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`** (§"Artifact Safety Rule"): se añade la regla conceptual de `<order>` (monotonía con el flujo, ordinal como declaración auditable) y el criterio de iteración parcial/continuación, inline y autocontenido.
- **`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`** (No-Skip Rule): el párrafo de artefacto retroactivo se reescribe con el vocabulario del modelo (desviación retroactiva: creación fuera de fase, marcado obligatorio, justificación por recovery), sin referenciar RFCs.
- **`.agents/orchestrators/core/roles/orchestrator.md`** (§"1. Session Management"): se añaden los criterios conceptuales de sesión (inicio, terminación, reanudación por continuidad de estado persistido) e iteración (apertura por petición, loops internos, iteración parcial), inline.
- **`plans/INDEX.md`**: fila de RFC-22 en la serie de RFCs; status del plan 13 a `Executed`.
- **`plans/analisis-explicitud.md`**: gap 4 marcado cerrado.

---

# Future Extensions

- **Validación por harness de integridad de sesión:** un trigger (o extensión de health-check) que verifique la conformidad de `SESSION_LOG.md` y `SESSION_BRIEF.md` contra sus contratos y la coherencia del log con las iteraciones presentes (fidelidad mecánica: entradas append-only, `<order>` monótono, una iteración por petición). Fuera de alcance de esta RFC; queda declarada para un plan futuro de la serie operativa.

---

# Rationale

El ciclo de vida de sesión e iteración era el último conjunto de reglas normativas del protocolo sin modelo conceptual: cuatro archivos normaban correctamente pero sin vocabulario común ni criterios para los casos borde (reanudación, iteración parcial, retroactividad). El aporte mínimo es nombrar los conceptos — sesión, iteración, `<order>` como secuencia auditable, integridad como conformidad + fidelidad, desviación retroactiva — y clasificar sus violaciones en la taxonomía existente, sin mover ninguna regla de su ubicación canónica ni añadir mecanismos.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación: modelo de ciclo de vida de sesión e iteración (límites de sesión, límites de iteración, `<order>`, integridad de artefactos de sesión, desviación retroactiva). | Plan 13 (`plans/13-session-iteration-lifecycle.md`); gap 4 de `plans/analisis-explicitud.md` |
