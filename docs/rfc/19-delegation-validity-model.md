# RFC-19 — Delegation Validity Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define qué hace **válida** una delegación del Orchestrator a un Worker más allá del schema del payload, y qué hace válido un **return report**. Introduce el concepto de **Delegation Validity**: el conjunto de condiciones conceptuales que una delegación debe cumplir para ser ejecutable, y el **gate conceptual** que las evalúa en tres puntos del flujo (pre-delegation, pre-execution, post-return).

Hoy el contrato de delegación (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Required Invocation Payload") define únicamente la *forma* del payload. Ninguna condición conceptual tiene gate: el valor de `profile` debe resolver en `.agents/roles/profiles/`, cada entrada de `skills` debe resolver bajo `.project/skills/` o `.agents/skills/`, los `input_artifacts` deben existir en la sesión, y el campo `context_budget` figura como literal `4000` sin significado definido (el "huérfano del 4000"; gap 2 de `plans/analisis-explicitud.md`). Esta RFC resuelve el huérfano declarando `context_budget` como la **materialización del Context Budget** (RFC-00YA, `plans/rfc/03-context-budget-model.md`) que el runtime corriente aplica a una delegación concreta.

El modelo reutiliza la taxonomía de fallos de RFC-18 (`plans/rfc/18-failure-recovery-taxonomy.md`): cada violación de validez se clasifica en una clase de fallo existente; no se introduce ninguna clase nueva.

---

# Motivation

- El schema del payload define forma, no ejecutabilidad: un payload bien formado puede referenciar un perfil inexistente, una skill inexistente o artefactos de entrada inexistentes, y ningún documento declara qué ocurre entonces de manera uniforme.
- El campo `context_budget: 4000` del contrato es un literal huérfano: RFC-00YA define el Context Budget sin unidades ni límites, y nada conecta ese número con el modelo conceptual. El protocolo no puede decir si `4000` es una policy, una materialización del runtime o un ejemplo.
- El contrato ya resuelve parcialmente la irresolubilidad de skills (§"`skills`": el Worker la reporta como deviation) y la invalidez del output (§"Retry Rules": una re-invocación y luego `RECOVERY`), pero esas reglas son casos aislados sin un modelo que diga en qué punto del flujo se evalúa cada condición y qué clase de fallo genera cada violación.
- Sin gate conceptual, la futura policy de harness que valide delegaciones no tiene modelo que instanciar.

---

# Goals

- Definir las condiciones conceptuales de validez de un Delegation Payload y de un return report.
- Definir el gate conceptual de validez: los puntos del flujo donde se evalúa y la clase de fallo de cada violación.
- Resolver el huérfano `context_budget: 4000` declarando su relación con el Context Budget.
- Declarar la futura policy de harness de validación de delegaciones como Future Extension, sin implementarla.

---

# Non Goals

Esta RFC no propone:

- implementar policies de harness ni modificar el runner (la policy de validación de delegaciones es una Future Extension, asignada al plan 15 como H15);
- modelos de selección de perfil o skill (cómo el Orchestrator *elige* un perfil o una skill): este modelo define qué hace *válida* una selección ya hecha, no cómo se elige;
- unidades, límites ni representación interna del Context Budget (explícitamente fuera de alcance de RFC-00YA, §Non Goals);
- nuevas clases de fallo ni cambios de máquina de estados;
- modificar el schema del return report.

---

# Definitions

## Delegation Validity

Propiedad conceptual de una delegación: el payload no solo está bien formado según el schema, sino que todas sus referencias son resolubles y coherentes con el modelo conceptual del protocolo. Un payload bien formado pero inválido no es ejecutable.

## Punto de evaluación (gate conceptual)

Uno de tres momentos del flujo de delegación en que se evalúa la validez:

- **Pre-delegation:** el Orchestrator, antes de invocar al Worker.
- **Pre-execution:** el Worker, al recibir el payload y antes de ejecutar la fase.
- **Post-return:** el Orchestrator, al recibir el return report y antes de aplicar el trigger de harness de la transición.

---

# Validity Conditions

Una delegación es válida cuando cumple las cinco condiciones siguientes. Cada condición declara su punto de evaluación primario y la clase de fallo (RFC-18) que genera su violación.

## V1 — Resolubilidad de perfil

Si `profile` está presente y no es `null`, su valor debe resolver exactamente a un archivo bajo `.agents/roles/profiles/` (sin la extensión `.md`), conforme a la regla ya normativa del contrato (§"`profile`": "The value MUST match a file name under `.agents/roles/profiles/` exactly").

- **Punto de evaluación:** pre-delegation (el Orchestrator verifica antes de invocar); el Worker la re-verifica pre-execution.
- **Violación:** clase **F1 — Blocker**. Un perfil irresoluble impide ejecutar la fase con las reglas especializadas requeridas; el destino conceptual es recovery (el Orchestrator corrige la selección y re-delega).

## V2 — Resolubilidad de skills

Cada entrada de `skills` debe resolver bajo `.project/skills/` (nivel proyecto, gana en colisión de nombres) o `.agents/skills/` (nivel protocolo), según la precedencia ya definida en `.agents/standards/orchestration/SKILLS.md`.

- **Punto de evaluación:** pre-execution (el Worker verifica al cargar cada `SKILL.md`).
- **Violación:** clase **F2 — Deviation**, conforme a la regla ya normativa del contrato (§"`skills`": el Worker reporta la skill inexistente o malformed como deviation y no inventa su contenido). La condición V2 es la única cuya violación no bloquea: la fase continúa sin esa capacidad y el reporte queda loggeado.

## V3 — Coherencia de Budget

El campo `context_budget` expresa la **materialización del Context Budget** (RFC-00YA) que el runtime corriente aplica a esa delegación concreta: la porción del Budget disponible para poblar el payload (en particular, los extractos de `knowledge_entries`). Es coherente cuando su valor es una restricción finita y positiva del recurso que el runtime usa para representar el Budget.

- **Punto de evaluación:** pre-delegation.
- **Violación:** clase **F1 — Blocker** si el valor no es una restricción finita (ausencia de límite donde el modelo exige finitud, por el invariante *Finite* de RFC-00YA, §Budget Invariants); clase **F2 — Deviation** si el valor es finito pero el Orchestrator no puede justificar su coherencia con el Budget de la sesión.
- **Resolución del huérfano del 4000:** el literal `4000` del contrato era una materialización *no declarada* del Budget por el runtime basado en prompts. La decisión conceptual es: el contrato **no fija el valor**; declara el concepto (materialización del Context Budget por el runtime) y deja el número al runtime. Las unidades y los límites concretos pertenecen al runtime, no al contrato, en la misma línea que el invariante *Representation-independent* de RFC-00YA. La materialización concreta para el runtime prompt (unidades, estimación y límites) es una Future Extension asignada al plan 15 junto con la policy H15.

## V4 — Existencia de artefactos de entrada

Cada ruta de `input_artifacts` debe existir dentro de la sesión (`.project/<session-uuid>/<iteration>/`) al momento de la delegación.

- **Punto de evaluación:** pre-delegation (el Orchestrator solo referencia artefactos que la sesión ya produjo); el Worker la re-verifica pre-execution al leer los artefactos.
- **Violación:** clase **F1 — Blocker**. Sin los artefactos de entrada la fase no puede ejecutarse; el destino conceptual es recovery (la delegación se refiere a un estado de sesión que aún no existe o fue mal citado).

## V5 — Validez del return report

El return report es válido cuando cumple el schema del contrato (§"Worker Return Report") **y** cada entrada de `blockers` y `deviations` declara su clase de fallo conforme a §"Failure classes in `blockers` and `deviations`" del mismo contrato (`blockers`: solo clase `blocker`; `deviations`: cada entrada prefijada con `deviation`, `ambiguity` o `inconsistency`).

- **Punto de evaluación:** post-return.
- **Violación:** output incompleto o inválido según las reglas ya normativas del contrato (§"Retry Rules"): el Orchestrator puede re-invocar al Worker una vez con instrucciones correctivas; si el segundo intento falla, transición a `RECOVERY`. Conceptualmente es una condición **F1 — Blocker** sobre la transición protegida (la fase no puede darse por completada con un reporte inválido), no una clase de fallo nueva.

---

# The Conceptual Gate

```text
Orchestrator                      Worker                      Orchestrator
     │                               │                             │
  pre-delegation                 pre-execution                 post-return
  V1 perfil ────────► payload ──► V2 skills (deviation) ──► ejecución ──► V5 report
  V3 budget                        V1 re-check (blocker)                    │
  V4 artefactos                    V4 re-check (blocker)                    ▼
                                                          harness trigger de la transición
```

Reglas del gate:

1. Toda condición se evalúa en su punto primario; las re-verificaciones del Worker (V1, V4) existen porque el Worker no puede asumir que el Orchestrator verificó.
2. Toda violación se reporta con la clase de fallo declarada en §Validity Conditions — el mismo hook determinista de la taxonomía de RFC-18, sin doble forma del entregable.
3. El gate es **conceptual**: hoy lo aplica el agente (Orchestrator y Worker) como parte de sus responsabilidades. Su materialización como policy de harness machine-evaluated es una Future Extension (§Future Extensions).

---

# Relationship with Existing Concepts

## Context Budget (RFC-00YA)

RFC-00YA define el Budget como restricción conceptual de Context Composition, sin unidades ni representación. Esta RFC no extiende esa definición: declara que `context_budget` es el punto donde el Budget conceptual toca el contrato de delegación, como materialización runtime-específica. La construcción del Execution Context sigue restringida por el Budget conceptual; el payload transporta la porción materializada que el runtime asigna a la delegación.

## Taxonomía de fallos (RFC-18)

Todas las violaciones de validez se clasifican en F1 (blocker) o F2 (deviation); ninguna requiere clase nueva. La clasificación por origen y destino conceptuales se preserva: V1/V3/V4/V5 tienen origen en la delegación misma y destino recovery; V2 tiene destino warning loggeado (el reporte del Worker).

## Selección de perfil y skills

Este modelo asume la selección ya hecha. Cómo el Orchestrator elige candidatos (la tabla de activación de `.agents/skills/INDEX.md`, §"Activation table", y las preguntas de `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`) es un modelo separado, fuera de alcance.

---

# Future Extensions

- **Delegation Validation Policy (H15):** policy de harness que materializa el gate conceptual como checks ejecutables (resolubilidad de perfil y skills, existencia de artefactos, coherencia declarada del budget). Asignada al plan 15. La numeración de policies omite H14 (sin asignar); la omisión se documentará en `.agents/harness/INDEX.md` junto a las de H08 y H12 al crearse H15.
- **Materialización del Budget para el runtime prompt:** unidades, estimación y límites del `context_budget` para el runtime basado en prompts. Asignada al plan 15 junto con H15. Relacionada con las extensiones *Budget Resource Model* y *Budget Estimation Model* anunciadas por RFC-00YA (§Future Extensions).

---

# Alternatives Considered

## Fijar `4000` como policy del protocolo

Se descartó: convertiría una decisión del runtime prompt (tokens u otra unidad) en norma del protocolo, contradiciendo los principios *Runtime-independent* y *Resource-independent* de RFC-00YA (§Design Principles).

## Eliminar `context_budget` del payload

Se descartó: el campo ya es consumido (opcional, poblado con `knowledge_entries`; contrato §"Required Invocation Payload") y expresa una restricción real del modelo (invariante *Finite*). Eliminarlo dejaría la delegación sin representación del Budget.

## Evaluar toda la validez post-return

Se descartó: detectar un perfil o artefacto irresoluble después de ejecutar la fase convierte errores prevenibles en retrabajo. Los tres puntos de evaluación reflejan dónde está la información necesaria para cada condición.

## Introducir una clase de fallo "invalid delegation"

Se descartó: la taxonomía de RFC-18 ya cubre los orígenes y destinos involucrados (F1 con destino recovery; F2 con destino warning). Una clase nueva duplicaría conceptos sin añadir destino.

---

# Compatibility

Esta RFC no modifica:

- runtime;
- workflow;
- state machine;
- policies de harness ni runner;
- el schema del payload ni del return report (la enmienda del contrato reemplaza el literal `4000` por la referencia conceptual, sin alterar la opcionalidad ni la posición del campo);
- la taxonomía de fallos.

---

# Documentation Impact

- **`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`** (§"Required Invocation Payload"): el literal `context_budget: 4000` se reemplaza por un placeholder y una nota que define el concepto inline (materialización del Context Budget por el runtime corriente), conforme a la frontera documental (`.agents/` no referencia RFCs).
- **`.agents/harness/INDEX.md`**: sin cambios en esta RFC; la omisión de H14 se documentará al crearse H15 (ver §Future Extensions).
- No se requieren modificaciones en `PROTOCOL_TAXONOMY.md`: Delegation Validity es un concepto del modelo conceptual, no una entidad estructural (mismo criterio que RFC-00YA, §Documentation Impact).

---

# Rationale

El contrato de delegación definía forma sin ejecutabilidad, y el único número del payload carecía de modelo. Esta RFC cierra ambos flancos con dos decisiones mínimas: la validez son cinco condiciones con punto de evaluación y clase de fallo declarados, y `context_budget` es la materialización del Context Budget que cada runtime declara. Ninguna regla operativa nueva se impone al agente más allá de lo que el contrato ya normaba parcialmente (resolubilidad de skills como deviation, retry ante output inválido); el aporte es el modelo que las unifica y el punto de extensión (H15) para su materialización.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación: modelo de validez de delegación (V1–V5), gate conceptual en tres puntos, resolución del huérfano `context_budget: 4000` como materialización del Context Budget, H15 declarada Future Extension. | Plan 11 (`plans/11-delegation-validity-model.md`) |
