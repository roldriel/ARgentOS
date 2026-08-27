# Implementation Plan — RFC-00YA Context Budget Model

**Status:** Executed

**Related RFC:** RFC-00YA — Context Budget Model (`plans/rfc/03-context-budget-model.md`)

**Impact:** Documental únicamente. Sin cambios de comportamiento.

**Breaking Changes:** None

---

# Scope

Implementar los ajustes documentales declarados en la sección *Documentation Impact* de la RFC:

- `plans/rfc/02-execution-context-assembly-process.md` (RFC-00XZ)
- `.agents/orchestrators/core/roles/orchestrator.md`

Explícitamente fuera de alcance:

- `PROTOCOL_TAXONOMY.md` (exclusión deliberada, justificada en la RFC)
- contratos (`.agents/contracts/`, `.agents/orchestrators/core/contracts/`)
- workflow, harness, máquina de estados, Workers, Skills, Delegation Payload
- cualquier cambio de comportamiento del runtime

**Nota sobre inmutabilidad:** `.agents/` es inmutable sin acuerdo explícito y documentado (`PROTOCOL_BOUNDARIES.md`). La RFC aceptada constituye ese acuerdo; cada cambio debe referenciarla para dejar trazabilidad.

---

# Phase 0 — Cierre de la RFC

1. La RFC ya está guardada como `plans/rfc/03-context-budget-model.md` con el diagrama corregido (la restricción apunta a Context Composition, no al proceso completo).
2. Cambiar `Status: Proposal` → `Accepted`; asignar autor (hoy `TBD`).

**Criterio de salida:** la RFC existe en `plans/`, está aprobada y sin observaciones abiertas.

---

# Phase 1 — RFC-00XZ: Context Budget como restricción de Context Composition

Archivo: `plans/rfc/02-execution-context-assembly-process.md`.

Cambios:

1. En **Responsibilities**, en la definición de **Context Composition**: agregar una oración indicando que la composición opera bajo un **Context Budget** — una restricción conceptual finita, consumible y exhaustible sobre la cantidad de información que puede formar parte del resultado — referenciando `plans/rfc/03-context-budget-model.md`. No agregar algoritmos, unidades ni políticas.
2. En **Conceptual Model** (líneas 251–274): actualizar el diagrama ASCII para reflejar el Budget como restricción lateral sobre Context Composition, usando la misma forma que la RFC-00YA:

   ```text
   Context Composition ◄──── constrains ──── Context Budget
   ```

   El Budget **no** se agrega como nodo del pipeline (no es una etapa ni una responsabilidad nueva; las cinco responsabilidades de RFC-00XZ no cambian).
3. En **Relationship with Existing Concepts** o en una nota junto al diagrama: una línea de trazabilidad a RFC-00YA como origen del concepto.
4. No tocar las secciones *Goals*, *Non Goals*, *Compatibility* ni *Design Intent* de RFC-00XZ: el Budget no altera sus responsabilidades.

**Criterio de salida:** RFC-00XZ declara que Context Composition opera bajo un Context Budget y su diagrama lo muestra como restricción, sin modificar las cinco responsabilidades ni agregar etapas.

---

# Phase 2 — `orchestrator.md`: mención del Context Budget

Archivo: `.agents/orchestrators/core/roles/orchestrator.md`, sección **5. Worker Delegation** (línea 196).

Cambios:

1. En el párrafo que describe el Execution Context Assembly Process, extender la descripción inline de **Context Composition**: indicar que construye el Execution Context final bajo un **Context Budget** (restricción conceptual, sin definir tamaño, unidad ni administración), sin agregar referencias a `plans/`; la trazabilidad a RFC-00YA vive solo en las RFCs y en este plan.

   Nota (2 ago 2026): la premisa original de este ítem ("agregar la referencia a `plans/rfc/03-context-budget-model.md` junto a las dos referencias existentes") era falsa — nunca existieron tales referencias en `.agents/` y la frontera documental (`plans/INDEX.md` §Convenciones) las prohíbe. Queda registrada.
2. No agregar ningún MUST nuevo: la RFC es explícitamente no normativa en comportamiento. No tocar la lista de campos de la invocación ni las secciones 5.1 y 5.2.
3. Regla cerrada (reformulada el 2 ago 2026 — el criterio original, "verificar si otra sección requiere la mención", era vago e inverificable): no agregar Context Budget fuera de orchestrator.md §5. Ninguna otra sección del archivo (p. ej. *Constraints*) recibe la mención.

**Criterio de salida:** la sección 5 menciona Context Budget como restricción conceptual de Context Composition, sin referencias a `plans/` (la trazabilidad vive en las RFCs y en este plan) y sin alterar obligaciones existentes.

---

# Phase 3 — Verificación

1. Health check del protocolo:

   ```bash
   python .agents/harness/runner.py health-check
   ```

2. Tests estructurales del harness (validan referencias cruzadas entre documentos):

   ```bash
   python -m pytest .agents/harness/tests/test_protocol_taxonomy.py .agents/harness/tests/test_protocol_skills.py
   ```

3. Consistencia terminológica: grep para confirmar que `Context Budget` aparece únicamente en los puntos previstos (RFC-00YA, RFC-00XZ Context Composition + diagrama, `orchestrator.md` sección 5), y que no se introdujo ninguna unidad concreta (tokens, bytes, etc.) como definición del Budget fuera de los ejemplos de la sección Runtime.

**Criterio de salida:** health check y tests en verde; terminología consistente.

---

# Risks

- **Riesgo funcional:** ninguno; todos los cambios son documentales.
- **Riesgo de sobre-especificación:** que al editar RFC-00XZ u `orchestrator.md` se cuele una unidad o política concreta (ej. "tokens"), contradiciendo los invariantes *Resource-independent* y *Representation-independent*. Mitigado en Phase 3, paso 3.
- **Riesgo de deriva terminológica futura:** declarado en la propia RFC — al no incorporarse a `PROTOCOL_TAXONOMY.md`, la consistencia del término depende de revisión documental, no del harness.

# Effort estimate

Dos ediciones documentales pequeñas y una corrida de verificación. La RFC ya está guardada (Phase 0 parcialmente completa).
