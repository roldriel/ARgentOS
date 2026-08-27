# Implementation Plan — RFC-00XZ Execution Context Assembly Process

**Status:** Executed

**Related RFC:** RFC-00XZ — Execution Context Assembly Process (`plans/rfc/02-execution-context-assembly-process.md`)

**Impact:** Documental únicamente. Sin cambios de comportamiento.

**Breaking Changes:** None

**Nota (2 ago 2026):** parcialmente superseded por RFC-00YB/00YC: el criterio de salida de Phase 2 exigía cinco responsabilidades en orchestrator.md §5, pero hoy describe siete (ver `plans/04-main-pipeline-closure.md` §B).

---

# Scope

Implementar los ajustes documentales declarados en la sección *Documentation Impact* de la RFC:

- `plans/rfc/01-execution-context-model.md` (RFC-00XY, secciones *Context Assembly* y *Responsibilities → Orchestrator*)
- `.agents/orchestrators/core/roles/orchestrator.md` (sección 5, Worker Delegation)

Explícitamente fuera de alcance:

- `PROTOCOL_TAXONOMY.md` (exclusión justificada en *Alternatives Considered* de la RFC)
- contratos (`.agents/contracts/`, `.agents/orchestrators/core/contracts/`)
- Delegation Payload, workflow, harness, máquina de estados, `AGENTS.md`
- `.agents/roles/worker.md` y `.agents/standards/orchestration/SKILLS.md` (ya actualizados por RFC-00XY; esta RFC no los modifica)
- cualquier cambio de comportamiento del runtime

**Nota sobre inmutabilidad:** `.agents/` es inmutable sin acuerdo explícito y documentado (`PROTOCOL_BOUNDARIES.md`). La RFC aceptada constituye ese acuerdo; cada cambio debe referenciarla para dejar trazabilidad.

---

# Phase 0 — Cierre de la RFC

1. Cambiar `Status: Proposal` → `Accepted` en `plans/rfc/02-execution-context-assembly-process.md`; asignar número definitivo y autor.
2. Confirmar que la RFC-00XY queda como definición canónica de Execution Context y sus categorías (esta RFC no toca esas secciones).

**Criterio de salida:** la RFC existe en `plans/`, está aprobada y sin observaciones abiertas.

---

# Phase 1 — RFC-00XY: referenciar el proceso refinado

Archivo: `plans/rfc/01-execution-context-model.md`.

Cambios:

1. En la sección **Context Assembly** (líneas 275–300):
   - Mantener el diagrama de categorías → Context Assembly → Execution Context → Worker como representación agregada válida.
   - Agregar una nota posterior indicando que RFC-00XZ descompone Context Assembly en cinco responsabilidades conceptuales (Source Discovery, Context Collection, Context Organization, Context Composition, Context Delivery) y que el modelo detallado del proceso se define allí. Referenciar `plans/rfc/02-execution-context-assembly-process.md`.
   - No eliminar la afirmación "la presente RFC no define cómo el Orchestrator realiza esta construcción" — reformularla como "la descomposición interna del proceso es definida por RFC-00XZ".
2. En **Responsibilities → Orchestrator** (líneas 304–313): agregar una línea de referencia cruzada a RFC-00XZ como la descomposición conceptual de estas cuatro actividades (reunir ≈ Discovery + Collection; organizar = Organization; preparar = Composition; entregar = Delivery). No eliminar los bullets existentes.
3. No tocar: *Context Categories*, *Responsibilities → Worker*, *Design Intent*, contratos ni ninguna otra sección.

**Criterio de salida:** RFC-00XY sigue siendo la definición canónica del resultado (Execution Context y categorías) y referencia explícitamente a RFC-00XZ como la definición del proceso.

---

# Phase 2 — `orchestrator.md`: las cinco responsabilidades

Archivo: `.agents/orchestrators/core/roles/orchestrator.md`, sección **5. Worker Delegation** (línea 196).

Cambios:

1. Reescribir el párrafo introductorio de Context Assembly (agregado por RFC-00XY) para presentar el **Execution Context Assembly Process** con sus cinco responsabilidades:
   - **Source Discovery**: determinar qué fuentes participan (role, profile, project context, skills, standards, policies).
   - **Context Collection**: obtener la información de esas fuentes.
   - **Context Organization**: clasificarla en las categorías del Execution Context (Identity, Task, Knowledge, Capability, Execution Metadata).
   - **Context Composition**: construir el Execution Context final.
   - **Context Delivery**: entregarlo mediante el delegation payload.
2. Mantener la aclaración de que se trata de una descomposición conceptual, no de una nueva etapa del workflow, y que la lista de campos de la invocación ya constituye el proceso.
3. La sección 5 de orchestrator.md NO debe referenciar RFCs (frontera documental, `plans/INDEX.md` §Convenciones); solo se actualiza la descripción inline de las responsabilidades.

   Nota (2 ago 2026): la premisa original de este ítem era falsa — pedía actualizar "la referencia" de `plans/rfc/01-execution-context-model.md` a dos archivos con nombres inexistentes (`rfc-execution-context-model.md`, `rfc-execution-context-assembly-process.md`), pero nunca existió tal referencia (grep confirma 0 referencias a `plans/` en `.agents/`). Queda registrada.
4. No modificar la lista de campos de la invocación (líneas 198 en adelante) ni las secciones 5.1 y 5.2.

**Criterio de salida:** la sección 5 nombra las cinco responsabilidades del Execution Context Assembly Process, sin alterar ningún MUST existente ni la lista de campos del payload.

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

3. Consistencia terminológica: grep para confirmar que:
   - `Execution Context Assembly Process`, `Source Discovery`, `Context Collection`, `Context Organization`, `Context Composition` y `Context Delivery` aparecen únicamente en las secciones previstas.
   - Ninguna sección modificada usa "Context Assembly" (a secas) para referirse a una responsabilidad individual — ese término queda reservado al concepto agregado de RFC-00XY y al nombre del proceso.
   - "Project Context" se usa como fuente (Knowledge Context), no como sinónimo de Execution Context.

**Criterio de salida:** health check y tests en verde; terminología consistente.

---

# Risks

- **Riesgo funcional:** ninguno; todos los cambios son documentales.
- **Riesgo de colisión terminológica** (confundir "Context Assembly" el concepto agregado con "Context Composition" la responsabilidad #4): mitigado en Phase 3, paso 3.
- **Riesgo de contradicción entre RFC-00XY y RFC-00XZ** (dos descripciones del mismo proceso): mitigado en Phase 1 manteniendo 00XY como descripción agregada con referencia explícita a 00XZ como descripción detallada.
- **Riesgo de deriva terminológica futura:** declarado en la propia RFC — al no incorporarse a `PROTOCOL_TAXONOMY.md`, la consistencia de estos términos depende de revisión documental, no del harness.

# Effort estimate

Dos ediciones documentales pequeñas, cierre de la RFC en `plans/` y una corrida de verificación.
