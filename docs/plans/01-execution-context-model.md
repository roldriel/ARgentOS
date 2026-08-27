# Implementation Plan — RFC-00XY Execution Context Model

**Status:** Executed

**Related RFC:** RFC-00XY — Execution Context Model (`plans/rfc/01-execution-context-model.md`)

**Impact:** Documental únicamente. Sin cambios de comportamiento.

**Breaking Changes:** None

---

# Scope

Implementar los ajustes documentales declarados en la sección *Documentation Impact* de la RFC:

- `.agents/orchestrators/core/roles/orchestrator.md`
- `.agents/roles/worker.md`
- `.agents/standards/orchestration/SKILLS.md`

Explícitamente fuera de alcance:

- `PROTOCOL_TAXONOMY.md`
- contratos (`.agents/contracts/`, `.agents/orchestrators/core/contracts/`)
- `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md`
- workflow, harness, máquina de estados, `AGENTS.md`
- cualquier cambio de comportamiento del runtime

**Nota sobre inmutabilidad:** `.agents/` es inmutable sin acuerdo explícito y documentado (`PROTOCOL_BOUNDARIES.md`). La RFC aceptada constituye ese acuerdo; cada cambio debe referenciarla para dejar trazabilidad.

---

# Phase 0 — Cierre de la RFC

1. Resolver el nit pendiente de la review: en *Context Categories*, quitar "Workflow State" de **Task Context** (ya cubierto por "Current State" en **Execution Metadata**) o unificar el nombre en ambas categorías.
2. Guardar la RFC como `plans/rfc/01-execution-context-model.md` (misma convención que `plans/rfc/00-skill-capability-model.md`).
3. Cambiar `Status: Proposal` → `Accepted`; asignar número definitivo y autor.

   Nota (2 ago 2026): aclaración — no existe "número definitivo" que asignar: los IDs conceptuales (RFC-00XY…) se mantienen por convención y el número de archivo es solo orden físico (`plans/INDEX.md` §Convenciones → Numeración de archivos). El autor quedó asignado el 2 ago 2026 (Rodrigo Roldán, ver header de la RFC).

**Criterio de salida:** la RFC existe en `plans/`, está aprobada y sin observaciones abiertas.

---

# Phase 1 — `orchestrator.md`: Context Assembly como responsabilidad

Archivo: `.agents/orchestrators/core/roles/orchestrator.md`, sección **5. Worker Delegation** (líneas 194–208).

Cambios:

1. Agregar un párrafo introductorio a la sección 5 indicando que, antes de cada delegación, el Orchestrator realiza el **Context Assembly**: reúne y organiza las cinco categorías del Execution Context (Identity, Task, Knowledge, Capability, Execution Metadata) y lo entrega mediante el Delegation Payload. Referenciar `plans/rfc/01-execution-context-model.md`.

   Nota (2 ago 2026): la referencia a la RFC NO se insertó — la frontera documental (`plans/INDEX.md` §Convenciones) prohíbe referencias `.agents/` → `plans/`; la ejecución real definió el concepto inline, de forma autocontenida. Esta desviación queda registrada.
2. La lista de campos de la invocación (líneas 197–206) **no se modifica** — ya constituye el assembly. Opcionalmente anotar cada bullet con su categoría (ej. `Session UUID` *(Execution Metadata)*, `skills: [...]` *(Capability Context)*), reforzando la propiedad *Traceable* del Design Intent.
3. No tocar las secciones 5.1 (Profile Selection) ni 5.2 (Skill Selection); ya son consistentes con el modelo.

**Criterio de salida:** la sección 5 nombra explícitamente Context Assembly y Execution Context, sin alterar ningún MUST existente.

---

# Phase 2 — `worker.md`: el Worker recibe un Execution Context

Archivo: `.agents/roles/worker.md`.

Cambios:

1. En **Input from Orchestrator** (líneas 76–89): agregar una oración introductoria: el conjunto de información preparada por el Orchestrator y entregada vía delegation payload constituye el **Execution Context** del Worker; el Worker lo consume y nunca lo construye. Referenciar la RFC.

   Nota (2 ago 2026): la referencia a la RFC NO se insertó — la frontera documental (`plans/INDEX.md` §Convenciones) prohíbe referencias `.agents/` → `plans/`; la ejecución real definió el concepto inline, de forma autocontenida. Esta desviación queda registrada.
2. En **Constraints** (líneas 139–147): agregar una línea: "A Worker MUST NOT construct its own context; it executes using the Execution Context received from the Orchestrator."
3. No modificar **Skill Consumption** (líneas 99–108): la carga diferida de referencias ya quedó cubierta por el Design Intent de la RFC (las referencias forman parte del Execution Context; su resolución posterior no lo modifica).

**Criterio de salida:** el rol Worker declara explícitamente que recibe un Execution Context construido por el Orchestrator, sin cambios en sus obligaciones operativas.

---

# Phase 3 — `SKILLS.md`: Skills como Capability Context

Archivo: `.agents/standards/orchestration/SKILLS.md`.

Cambios:

1. En **Skill vs. profile** (líneas 7–12): agregar una línea ubicando profiles en *Identity Context* y skills en *Capability Context* del Execution Context.
2. En la nota de exclusión de la taxonomy (línea 39): agregar referencia cruzada a la RFC como modelo conceptual que agrupa skill + profile + knowledge bajo un mismo Execution Context.

   Nota (2 ago 2026): la referencia a la RFC NO se insertó — la frontera documental (`plans/INDEX.md` §Convenciones) prohíbe referencias `.agents/` → `plans/`; la ejecución real definió el concepto inline, de forma autocontenida. Esta desviación queda registrada.
3. No tocar **Activation** ni **Authority hierarchy**: ya son consistentes con la RFC.

**Criterio de salida:** las Skills quedan referenciadas como una categoría del Execution Context y no como contexto aislado.

---

# Phase 4 — Verificación

1. Health check del protocolo:

   ```bash
   python .agents/harness/runner.py health-check
   ```

2. Tests estructurales del harness (validan referencias cruzadas entre documentos):

   ```bash
   python -m pytest .agents/harness/tests/test_protocol_taxonomy.py .agents/harness/tests/test_protocol_skills.py
   ```

3. Consistencia terminológica (reformulado el 2 ago 2026 — el criterio original, "que `Execution Context` y `Context Assembly` aparecen únicamente en las secciones previstas", era inverificable: no existía lista de secciones previstas). Lista explícita de dónde quedaron definidos los conceptos (verificada el 2 ago 2026):
   - **Execution Context**: `.agents/orchestrators/core/roles/orchestrator.md` §5 (Worker Delegation); `.agents/roles/worker.md` §Input from Orchestrator y §Constraints; `.agents/standards/orchestration/SKILLS.md` §Skill vs. profile y §Validation.
   - **Context Assembly** (como concepto agregado): `.agents/orchestrators/core/roles/orchestrator.md` §5.

   Comando concreto:

   ```bash
   grep -rn "Execution Context\|Context Assembly" .agents/
   ```

   Criterio: todas las ocurrencias deben estar en las secciones listadas arriba, y ninguna sección modificada debe usar "context" de forma ambigua entre Project Context y Execution Context.

**Criterio de salida:** health check y tests en verde; terminología consistente.

---

# Risks

- **Riesgo funcional:** ninguno; todos los cambios son documentales.
- **Riesgo de redacción ambigua** (confundir Project Context con Execution Context en las secciones tocadas): mitigado en Phase 4, paso 3.
- **Riesgo de deriva terminológica futura:** declarado en la propia RFC — al no incorporarse a `PROTOCOL_TAXONOMY.md`, la consistencia de estos términos depende de revisión documental, no del harness.

# Effort estimate

Tres ediciones documentales pequeñas, un archivo nuevo en `plans/` y una corrida de verificación.
