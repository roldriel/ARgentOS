# RFC-21 — Skill Activation Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define el **modelo conceptual de activación de skills**: qué hace a una skill **candidata** a activarse para una tarea, qué debe contener la `description` de una skill para ser **activable** (suficiencia de descripción) y qué es un **override justificado** de la tabla de activación. Es el análogo, para las skills, de lo que RFC-20 (`plans/rfc/20-profile-selection-model.md`) definió para los perfiles: candidatura y selección como conceptos, sin algoritmos.

Hoy existen dos vías de activación (`.agents/standards/orchestration/SKILLS.md`, §"Activation"): la tabla de activación de `.agents/skills/INDEX.md` (§"Activation table"), con eje de clasificación fase+perfil, y el "judgment override" loggeado. Lo que no existe es el modelo: ninguna define qué hace a una skill candidata fuera de la tabla, ni qué convierte una `description` en suficiente para activar por juicio, ni qué estatuto conceptual tiene el override (gap 3 de `plans/analisis-explicitud.md`).

Este modelo produce una activación; la **validez** de la activación resultante (resolubilidad de cada skill, condición V2) está definida por RFC-19 (`plans/rfc/19-delegation-validity-model.md`) y no se redefine aquí.

---

# Motivation

- El override por juicio es hoy la vía dominante de activación (la mayoría de las skills del inventario se declaran "Activated by judgment"; `.agents/skills/INDEX.md`, §"Skill inventory"), pero "the skill's `description` justifies it" (SKILLS.md, §"Activation") es un criterio sin límites: nada dice qué debe contener una descripción para justificar una activación, así que cualquier activación — o ninguna — es defendible.
- La tabla de activación tiene eje definido (fase + perfil) pero su suficiencia como modelo nunca fue evaluada: no se declara si basta para expresar candidatura, ni dónde viven los conceptos que el eje no expresa (exclusión entre skills, override).
- El override existe como práctica loggeada sin concepto: no se distingue entre activación fuera de tabla, no-activación dentro de tabla, y activación contraria a la descripción.
- RFC-19 define qué hace *válida* una activación ya hecha (V2), pero declara fuera de alcance cómo se elige (§Non Goals). Este modelo es ese complemento.

---

# Goals

- Definir el concepto de **candidatura de skill** en sus dos vías: candidatura de tabla y candidatura por juicio.
- Definir la **suficiencia de descripción**: qué debe contener la `description` de una skill para ser activable.
- Definir el **override justificado** como concepto, con sus formas y su obligación de registro.
- Evaluar y decidir la suficiencia de la estructura existente de la tabla de activación (eje fase+perfil).
- Declarar la relación con el Skill Capability Model (RFC-00XX): la activación opera sobre la capacidad conceptual, no sobre el mecanismo.

---

# Non Goals

Esta RFC no propone:

- algoritmos de matching, scoring o clasificación de skills;
- entradas concretas de la tabla de activación (se llenan por skill, caso por caso);
- redefinir la validez de la activación (condición V2 de RFC-19);
- cambios en el formato `SKILL.md` (`.agents/skills/README.md`) ni en la membresía del catálogo de skills (RFC-16, `plans/rfc/16-core-skills-catalog-model.md`);
- validación por harness de las activaciones (hook declarado como Future Extension en RFC-19, plan 15).

---

# Definitions

## Skill Candidacy

Propiedad conceptual entre una skill y una tarea: la skill es **candidata** a activarse cuando la tarea cae dentro de las condiciones de uso que la skill declara. Existen dos vías de candidatura, disjuntas en su origen y equivalentes en su resultado:

1. **Candidatura de tabla:** la combinación (fase del workflow + perfil seleccionado) de la tarea coincide con una fila de la tabla de activación que lista la skill. La candidatura es *declarativa*: alguien evaluó por adelantado que esa combinación requiere esa capacidad.
2. **Candidatura por juicio:** la `description` de la skill declara condiciones de uso que la tarea satisface, sin que exista fila de tabla aplicable. La candidatura es *evaluada en el momento* por el Orchestrator, sobre la descripción.

Ambas vías producen candidatos; la **activación** es la selección del subconjunto de candidatos que viaja en el campo `skills` del Delegation Payload.

## Suficiencia de descripción

Una `description` es **suficiente para activar** cuando contiene, de forma reconocible:

1. **Capacidad:** qué hace la skill (el procedimiento o resultado que aporta).
2. **Condiciones de uso:** cuándo aplica — los disparadores o situaciones de la tarea que la hacen candidata ("Use when…").

Una descripción que solo declara capacidad sin condiciones de uso no es suficiente para candidatura por juicio: el Orchestrator no tiene contra qué evaluar la tarea, y toda activación sería juicio sin límites — exactamente el gap que esta RFC cierra. La suficiencia es un requisito conceptual sobre las skills del protocolo; el test estructural existente (`.agents/harness/tests/test_protocol_skills.py`) valida la *presencia* de `description`, no su suficiencia, que se evalúa al incorporar cada skill al catálogo.

## Override justificado

Un **override** es toda activación que se aparta de la candidatura de tabla. Tiene dos formas:

- **Override de activación:** activar una skill sin fila de tabla aplicable, por candidatura por juicio (descripción suficiente satisfecha por la tarea).
- **Override de omisión:** no activar una skill que la tabla lista para la combinación fase+perfil, cuando las condiciones de la tarea concreta hacen que la capacidad no aplique.

Todo override es **justificado**: la razón — qué condición de la descripción (o de la tarea) lo motiva — se registra en `SESSION_LOG.md`, conforme a la obligación ya normativa de SKILLS.md (§"Activation"). Un override sin justificación registrada es conceptualmente una **deviation** (clase F2 de RFC-18, `plans/rfc/18-failure-recovery-taxonomy.md`): la activación no es inválida (V2 solo exige resolubilidad), pero el proceso quedó fuera del modelo y el desvío queda loggeado.

## Exclusión entre skills

A diferencia de los perfiles, las skills **no son mutuamente excluyentes**: un worker puede portar un perfil y cero o más skills, que son ortogonales y nunca compiten (SKILLS.md, §"Skill vs. profile"). Por tanto el modelo no necesita concepto de empate ni de división para skills: la selección es un subconjunto, no una elección única. La única frontera conceptual es la de autoridad (una skill nunca habilita lo que el protocolo prohíbe; SKILLS.md, §"Authority hierarchy"), que ya está definida y no es un caso de exclusión entre candidatos.

## Candidatura sobre la capacidad, no sobre el mecanismo

Conforme al Skill Capability Model (RFC-00XX, `plans/rfc/00-skill-capability-model.md`), una skill es una capacidad reutilizable independiente de cómo el runtime la incorpore. La candidatura y la activación se evalúan sobre esa capacidad conceptual — lo que la `description` declara — no sobre el mecanismo de entrega (inyección de contexto en el runtime prompt). Un runtime distinto con el mismo catálogo aplicaría el mismo modelo de activación.

---

# The Activation Process (conceptual)

```text
tarea + fase + perfil seleccionado
        │
        ├─ candidatura de tabla (fila fase+perfil lista la skill)
        │        └─ ¿las condiciones de la tarea la hacen no aplicable?
        │             ├─ no ──► activación
        │             └─ sí ──► override de omisión (justificado, loggeado)
        │
        └─ candidatura por juicio (description suficiente satisfecha)
                 └─► override de activación (justificado, loggeado)
```

Reglas conceptuales:

1. Toda skill activada es candidata por alguna de las dos vías; no existe activación sin candidatura.
2. La tabla no acota el universo de candidatas: delimita la candidatura *declarativa*. El juicio opera sobre las descripciones suficientes del inventario completo.
3. El resultado de la activación alimenta el campo `skills` del payload y queda sujeto a la condición de validez V2 (resolubilidad) de RFC-19; una activación conceptualmente correcta de una skill inexistente o malformed es una deviation reportada por el Worker, no una violación de este modelo.

---

# Decision on the Table Structure

La estructura existente de la tabla (`.agents/skills/INDEX.md`, §"Activation table": `Workflow phase | Profile | Skills`) se declara **suficiente** para el modelo:

- El eje fase+perfil expresa exactamente la candidatura declarativa: reusa dos decisiones que el Orchestrator ya toma (la fase corriente y la selección de perfil de RFC-20), sin taxonomía paralela.
- Los conceptos que el eje no expresa — suficiencia de descripción, override, exclusión — no son *columnas faltantes*: son propiedades del proceso de activación (definidas en §Definitions) o no aplican (la exclusión, por la ortogonalidad de las skills). Añadir campos a la tabla para ellos duplicaría en cada fila lo que es una regla del modelo.
- Las entradas concretas siguen fuera de alcance: se llenan por skill, caso por caso, al incorporar skills al catálogo (criterios de RFC-16).

---

# Relationship with Existing Concepts

## Delegation Validity (RFC-19)

RFC-19 define qué hace *válida* una activación (V2: cada entrada de `skills` resuelve bajo `.project/skills/` o `.agents/skills/`, con la precedencia del proyecto). Esta RFC define cómo se *produce* esa activación. La frontera es exacta: candidatura → activación → gate de validez. Ninguna condición V1–V5 se modifica.

## Profile Selection (RFC-20)

La candidatura de tabla consume el resultado de la selección de perfil: sin perfil seleccionado no hay fila aplicable. La activación de skills es posterior y ortogonal a la selección de perfil (perfil = quién es el worker; skills = qué capacidades ejecuta).

## Skill Capability (RFC-00XX) y Core Skills Catalog (RFC-16)

RFC-00XX define qué es una skill; RFC-16 define cuáles skills construir y por qué. Esta RFC define cuándo se activan las skills que existen. La suficiencia de descripción se evalúa al incorporar una skill (responsabilidad del proceso de catálogo) y se consume al activar (responsabilidad del Orchestrator).

## Taxonomía de fallos (RFC-18)

El único fallo nuevo que este modelo reconoce — override sin justificación registrada — se clasifica en la clase existente F2 (deviation). No se introduce ninguna clase nueva.

---

# Alternatives Considered

## Extender la tabla con columnas de criterio y override

Se descartó: los criterios de candidatura por juicio viven en las descripciones de las skills (donde el worker también los lee), y el override es un evento del proceso, no un dato por fila. Columnas nuevas congelarían en la tabla lo que es dinámico o ya está declarado en otro lugar.

## Prohibir el override y hacer la tabla exhaustiva

Se descartó: la tabla es declarativa y se llena caso por caso; prohibir el override dejaría sin activación a toda skill aún no tabulada, y la mayoría del inventario actual se activa por juicio (`.agents/skills/INDEX.md`, §"Skill inventory"). El override justificado convierte esa realidad en modelo en lugar de prohibirla.

## Eje de clasificación por tipo de tarea

Se descartó por la misma razón que en RFC-20: una taxonomía de tareas paralela a fase+perfil exige mantener dos clasificaciones sincronizadas. El eje actual reusa decisiones ya tomadas.

---

# Compatibility

Esta RFC no modifica:

- runtime;
- workflow ni state machine;
- policies de harness ni runner;
- el formato `SKILL.md` ni el inventario de skills;
- la estructura de la tabla de activación (confirmada como suficiente);
- el contrato de delegación ni las condiciones V1–V5.

---

# Documentation Impact

- **`.agents/standards/orchestration/SKILLS.md`** (§"Activation"): se reescribe como modelo conceptual autocontenido (candidatura de tabla y por juicio, suficiencia de descripción, override justificado y sus formas), sin referenciar RFCs (frontera documental).
- **`.agents/skills/INDEX.md`** (§"Activation table"): se añade una nota declarativa que confirma la suficiencia del eje fase+perfil y remite los conceptos de candidatura y override a `SKILLS.md`; las entradas concretas siguen fuera de alcance.
- **`.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`**: nota transversal mínima que conecta la selección de perfil con la activación de skills, sin referenciar RFCs.
- No se requieren cambios en `PROTOCOL_TAXONOMY.md`: la activación de skills es un concepto del modelo, no una entidad estructural del flujo (mismo criterio que RFC-19, §Documentation Impact).

---

# Rationale

La activación de skills era, junto con la selección de perfil, el último mecanismo de delegación gobernado por juicio sin modelo. El aporte mínimo es nombrar las dos vías de candidatura, ponerle límites al juicio (una descripción sin condiciones de uso no habilita candidatura por juicio) y darle estatuto al override (dos formas, justificación obligatoria, deviation si falta). La tabla se confirma suficiente sin tocarla: lo que le "faltaba" no eran columnas sino el modelo que la enmarca.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación: modelo de activación de skills (candidatura de tabla y por juicio, suficiencia de descripción, override justificado, suficiencia del eje fase+perfil). | Plan 12 (`plans/12-selection-models.md`) |
