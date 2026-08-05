# RFC-20 — Profile Selection Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define el **modelo conceptual de selección de perfil**: qué hace a una tarea **candidata** a un perfil especializado, cómo se **selecciona** un perfil entre candidatos, qué significa la **exclusión mutua** entre perfiles y cómo se resuelve un **empate** entre perfiles mediante los conceptos de **divisibilidad** y **frontera de subtarea**. Es el análogo, para la selección de perfil, de lo que la serie de Execution Context (RFC-00YB Prioritization, RFC-00YC Resolution, RFC-00YF Tie-Breaking) definió para los candidates del contexto: candidatura, selección, exclusión y empate como conceptos, sin algoritmos.

Hoy la selección de perfil existe solo como un procedimiento: 7 preguntas keyword-based en `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` (§"3. The 7 decision questions"), con fallback a worker genérico, una tabla de perfiles prohibidos (§"Alternative profiles that must not be used") y la regla "split it into sequential subtasks" ante múltiples coincidencias — donde la decisión de división (orden, fronteras) es juicio sin concepto (gap 3 de `plans/analisis-explicitud.md`).

Este modelo produce una selección; la **validez** de esa selección (resolubilidad del perfil elegido, condición V1) está definida por RFC-19 (`plans/rfc/19-delegation-validity-model.md`) y no se redefine aquí.

---

# Motivation

- Las 7 preguntas de la guía son criterios de clasificación sin modelo: ninguna define qué las hace suficientes, qué ocurre cuando varias aplican, ni por qué la pregunta 7 (worker genérico) es un fallback y no un perfil más.
- La regla de división en subtareas secuenciales introduce dos decisiones — en qué **fronteras** cortar la tarea y en qué **orden** ejecutar los fragmentos — que hoy se toman por juicio, sin conceptos que las acoten.
- La tabla de perfiles prohibidos es una regla explícita aislada: sin el concepto de exclusión no queda claro si es una lista cerrada, una heurística o una consecuencia de algo más general.
- RFC-19 define qué hace *válida* una selección ya hecha, pero declara explícitamente fuera de alcance cómo se elige (§Non Goals, §"Relationship with Existing Concepts"). Este modelo es ese complemento.

---

# Goals

- Definir el concepto de **candidatura de perfil**: qué convierte a una tarea en candidata a un perfil especializado.
- Definir los conceptos de **exclusión mutua** entre perfiles y de **empate entre perfiles**, incluyendo su resolución conceptual.
- Definir los conceptos de **divisibilidad** y **frontera de subtarea** que gobiernan la división en subtareas secuenciales.
- Ubicar la tabla de perfiles prohibidos como instancia del concepto de exclusión.
- Definir el estatuto conceptual del worker genérico como fallback.

---

# Non Goals

Esta RFC no propone:

- algoritmos de matching, scoring o clasificación de tareas;
- cambios en el catálogo de perfiles (`.agents/roles/profiles/`) ni en las 7 preguntas como procedimiento operativo;
- redefinir la validez de la selección (condición V1 de RFC-19): este modelo termina donde empieza el gate de validez;
- modelos de activación de skills (definidos en RFC-21, `plans/rfc/21-skill-activation-model.md`);
- validación por harness de las selecciones (hook declarado como Future Extension en RFC-19, plan 15).

---

# Definitions

## Profile Candidacy

Propiedad conceptual entre una tarea y un perfil: la tarea es **candidata** a un perfil cuando su contenido cae dentro del dominio de acción que define ese perfil. En el estado actual del protocolo, cada una de las 6 primeras preguntas de la guía (`ORCHESTRATION_GUIDE.md`, §"3. The 7 decision questions") **es** el criterio de candidatura de un perfil: una respuesta afirmativa declara la candidatura. El criterio de candidatura de un perfil es parte de la definición conceptual del perfil, no una taxonomía paralela de tareas: clasificar la tarea es reconocer en ella el dominio del perfil.

Una tarea puede ser candidata a cero, uno o varios perfiles.

## Selección

La selección es la decisión que toma el conjunto de candidatos y produce el valor de `profile` del Delegation Payload: un único perfil, o `null` (worker genérico). La selección consume candidaturas; no las crea.

## Fallback (worker genérico)

El worker genérico (`profile: null`) **no es un perfil candidato**: es el resultado conceptual de una selección con conjunto de candidatos vacío. La pregunta 7 de la guía ("Does none of the above apply...?") no compite con las demás: se evalúa solo cuando ninguna candidatura especializada existe. Conceptualmente: *sin candidatura especializada, no hay selección de perfil*.

## Exclusión mutua

Dos perfiles son **mutuamente excluyentes** para una tarea cuando delegar la tarea completa a uno de ellos viola el dominio del otro: cada perfil ejecutaría trabajo que la definición del otro declara propio. La exclusión mutua es una propiedad de la *tarea candidata a varios perfiles*, no de los perfiles en abstracto.

La tabla de perfiles prohibidos de la guía (§"Alternative profiles that must not be used") es una **instancia** de este concepto: enumera, para cada dominio, los perfiles cuya selección está excluida aunque la tarea pueda parecerles candidata. No es una lista independiente: es la forma materializada de la exclusión para los pares de dominios donde el error es frecuente.

## Empate entre perfiles

Hay **empate** cuando una tarea es candidata a dos o más perfiles mutuamente excluyentes y ningún criterio de candidatura la declara más propia de uno que de otro. El empate no se resuelve eligiendo: se resuelve **dividiendo**.

## Divisibilidad

Una tarea en empate es **divisible** cuando puede descomponerse en subtareas tales que cada subtarea es candidata a exactamente uno de los perfiles en empate (o al worker genérico) y la unión de las subtareas cubre la tarea original. La división es la resolución conceptual del empate: el empate señala que la unidad de delegación estaba mal cortada, no que falte un criterio de elección.

## Frontera de subtarea

La **frontera** entre dos subtareas es el corte de la tarea original. Una frontera es conceptualmente válida cuando:

1. **Cobertura:** ningún fragmento de la tarea queda fuera de todas las subtareas.
2. **Pertenencia:** cada subtarea cae entera dentro del dominio de un único perfil (la candidatura deja de ser múltiple por construcción).
3. **Orden por dependencia:** si una subtarea consume el resultado de otra, se delega después (el caso canónico: la subtarea de documentación consume el `EXECUTION_SUMMARY.md` de la subtarea técnica — `ORCHESTRATION_GUIDE.md`, §"Example 4 — Multiple sequential profiles"). Sin dependencia, el orden es libre.

Una tarea en empate **no divisible** (ninguna frontera cumple las tres condiciones) es una **ambigüedad de alcance**, no un problema de selección: su destino conceptual es `NEEDS_CLARIFICATION`, conforme a la frontera ya definida entre clarificación y recovery (`.agents/standards/orchestration/DECISIONS.md`).

---

# The Selection Process (conceptual)

```text
tarea ──► candidatura (¿a qué perfiles es candidata?)
             │
             ├─ 0 candidatos ──────────► worker genérico (fallback)
             ├─ 1 candidato ───────────► selección directa
             └─ 2+ candidatos ──► ¿exclusión mutua?
                     ├─ no ──► selección del candidato cuyo dominio
                     │         cubre la acción principal de la tarea
                     └─ sí ──► empate ──► división en subtareas
                               secuenciales (fronteras válidas)
                               o NEEDS_CLARIFICATION si no divisible
```

Reglas conceptuales:

1. Toda selección pasa por candidatura: ningún perfil se elige sin que la tarea le sea candidata.
2. La exclusión mutua prohibe delegar la tarea entera a uno solo de los perfiles en empate; la tabla de prohibidos materializa los casos conocidos.
3. La división produce subtareas cada una con su propio proceso de selección (cada subtarea reingresa al diagrama).
4. El resultado de la selección alimenta el campo `profile` del payload y queda sujeto a la condición de validez V1 (resolubilidad) de RFC-19; la selección conceptualmente correcta de un perfil inexistente es inválida igualmente (el gate la rechaza pre-delegation).

---

# Relationship with Existing Concepts

## Delegation Validity (RFC-19)

RFC-19 define qué hace *válida* una selección (V1: el valor de `profile` resuelve a un archivo bajo `.agents/roles/profiles/`). Esta RFC define cómo se *produce* esa selección. La frontera es exacta: candidatura → selección → gate de validez. Ninguna condición V1–V5 se modifica.

## Decisiones del Orchestrator (RFC-17)

La selección de perfil es una decisión del Orchestrator ya catalogada como parte del catálogo conceptual de `.agents/standards/orchestration/DECISIONS.md`. Este modelo no añade un punto de decisión nuevo: da estructura conceptual (candidatura, exclusión, empate, división) a una decisión que el catálogo ya reconocía.

## Candidates del Execution Context (RFC-00YB/00YC/00YF)

La analogía es estructural, no de identidad: los perfiles no son context candidates. Se reutilizan los *patrones conceptuales* (candidatura como propiedad previa a la selección; empate como situación con resolución declarada) sin importar los mecanismos del pipeline de contexto.

## Fixed profiles

Los perfiles de fase fija (`intent_reflector` en fase 01) no participan de este modelo: no hay selección donde el perfil está fijado por la fase. El modelo aplica únicamente donde la guía aplica (`ORCHESTRATION_GUIDE.md`, §"2. When to use this guide").

---

# Alternatives Considered

## Taxonomía de tareas independiente de los perfiles

Se descartó: clasificar tareas en categorías propias y luego mapear categorías a perfiles introduce una taxonomía paralela que hay que mantener sincronizada con el catálogo de perfiles. La candidatura como "reconocer el dominio del perfil en la tarea" reusa las decisiones que el Orchestrator ya toma, el mismo criterio que el eje fase+perfil de la tabla de activación de skills (`.agents/skills/INDEX.md`, §"Activation table").

## Resolver el empate por precedencia de perfiles

Se descartó: un orden de precedencia entre perfiles (p. ej. "database gana a backend") convertiría el empate en elección arbitraria y delegaría trabajo fuera del dominio del perfil ganador. La división respeta los dominios; la precedencia los viola.

## Tratar el worker genérico como un perfil más

Se descartó: el genérico no tiene dominio propio ni `MUST_READ` especializado (`ORCHESTRATION_GUIDE.md`, §"3. The 7 decision questions", fila 7). Modelarlo como perfil candidato lo haría competir con los especializados; modelarlo como fallback expresa exactamente su estatuto: resultado de la ausencia de candidatura.

---

# Compatibility

Esta RFC no modifica:

- runtime;
- workflow ni state machine;
- policies de harness ni runner;
- el catálogo de perfiles ni las 7 preguntas como procedimiento;
- el contrato de delegación ni las condiciones V1–V5.

---

# Documentation Impact

- **`.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`**: se añade una sección conceptual autocontenida (candidatura, exclusión mutua, empate, divisibilidad, frontera de subtarea, fallback) que enmarca las 7 preguntas y la tabla de prohibidos, sin referenciar RFCs (frontera documental).
- No se requieren cambios en `PROTOCOL_TAXONOMY.md`: la selección de perfil es un concepto del modelo, no una entidad estructural del flujo (mismo criterio que RFC-19, §Documentation Impact).

---

# Rationale

La selección de perfil era el último mecanismo de delegación gobernado por "juicio del Orchestrator" sin modelo. El aporte mínimo es nombrar las cuatro situaciones que el procedimiento ya enfrenta — candidatura, selección, exclusión, empate — y declarar la resolución conceptual del empate: dividir en subtareas con fronteras válidas (cobertura, pertenencia, orden por dependencia), con `NEEDS_CLARIFICATION` como destino del caso no divisible. Nada operativo cambia: las 7 preguntas, la tabla de prohibidos y el ejemplo 4 de la guía ya eran este modelo en forma de procedimiento.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación: modelo de selección de perfil (candidatura, selección, exclusión mutua, empate, divisibilidad, frontera de subtarea, fallback genérico). | Plan 12 (`plans/12-selection-models.md`) |
