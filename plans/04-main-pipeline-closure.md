# Plan — Nivel 1: Cierre del Pipeline Principal

**Status:** Plan aprobado para redacción de RFCs

**Depends on:** — (ninguno; es la base de los Niveles 2–4)

**Referencia:** `feature.md` (Execution Context Pipeline), `plans/rfc/04-context-candidate-prioritization-model.md` (RFC-00YB), `plans/rfc/05-context-resolution-model.md` (RFC-00YC)

---

# Objetivo

Completar la definición conceptual de cada etapa del pipeline principal (Stages 1–9 del protocolo; Stages 10–11 pertenecen al runtime según `feature.md` §Stage 10) y dejar el feature doc consistente con el estado real de los RFCs.

---

# Alcance

## A. Context Composition Model (RFC-00YD) — el único ⏳ del Nivel 1

Redactar `plans/rfc/06-context-composition-model.md` siguiendo la estructura de RFC-00YC:

- **Pregunta que responde:** ¿Cómo se transforma un Resolved Candidate Set en un Execution Context?
- **Contenido mínimo:**
  - Abstract que encadene la serie (…00YC introdujo Resolution; falta la transformación final).
  - Goals / Non Goals (sin algoritmos, sin representación, sin materialización).
  - Definición del invariante de composición: Composition opera **exclusivamente** sobre un Resolved Candidate Set; no decide prioridades, conflictos ni restricciones (ya afirmado en `feature.md` Stage 8 y en RFC-00YC).
  - Relación con Context Budget: el Budget **restringe** la composición (como ya anticipa el diagrama de RFC-00YC: `Context Composition ◄──── constrains ──── Context Budget`).
  - Tabla "Relationship with Previous RFCs": la tabla vive en cada RFC de la serie (la de RFC-00YC está en su sección homónima). RFC-00YD incluye su **propia copia** de la tabla, replicando las filas 00XY–00YC y agregando la fila propia: `RFC-00YD | ¿Cómo se construye el Execution Context a partir del conjunto resuelto?`. No se edita RFC-00YC para esto.
  - Future Extensions: Context Compression Model y Context Optimization Model (Nivel 3), que extienden Composition.
  - Compatibility / Documentation Impact: actualizar RFC-00XZ (Assembly Process) y `feature.md`.
- **Criterio de aceptación (compuesto; reformulado el 2 ago 2026 — el original, "RFC-00YD marcado ✔ en feature.md", era circular):** el archivo `plans/rfc/06-*.md` existe, tiene `Status: Accepted` y autor asignado, y entonces se marca ✔ en `feature.md` → Planned Evolution → Nivel 1.

## B. Actualizar RFC-00XZ (pendiente de las enmiendas 00YB/00YC)

(Sección vigente; antes "B'". La sección B original —"Regularizar los RFCs ausentes"— quedó sin efecto y se preserva en §Historial.)

RFC-00XZ quedó desactualizado respecto de 00YB/00YC y su propio *Documentation Impact* lo exige:

1. **Responsibilities:** incorporar Context Candidate Prioritization y Context Resolution como responsabilidades conceptuales del Assembly Process, anteriores a Composition (hoy declara solo cinco y `orchestrator.md` ya describe siete).
2. **Future Extensions:** corregir las descripciones stale — hoy dicen que Resolution y Prioritization operan "*durante* Context Composition", lo que RFC-00YC enmendó explícitamente (ambas son anteriores a Composition).
3. **Conceptual Model:** actualizar el diagrama para reflejar Prioritization → Resolution → Composition con Budget como restricción lateral de Resolution y Composition.

## C. Fixes de consistencia en `feature.md`

1. **Diagrama del pipeline:** incorporar Context Budget como input lateral de Prioritization, Resolution y Composition (no como etapa en línea). Nota: los diagramas de 00YB/00YC solo muestran Budget → Resolution y Budget → Composition; la arista Budget → Prioritization es una extensión nueva y debe presentarse como tal.
2. **Línea divisoria de frontera del protocolo** entre Stage 9 (Execution Context) y Stage 10 (Prompt Rendering): marcar visualmente dónde termina el protocolo y empieza el runtime.
3. **Índice de RFCs:** sección nueva en `feature.md` con tabla RFC → archivo (SIN columna de status — el status vive únicamente en `plans/INDEX.md`, single-source; duplicarlo violaría esa regla), incluyendo RFC-00XX (Skill Capability Model), que antecede a la serie de contexto.
4. **Stages 2–4:** declarar que Discovery/Collection/Organization son las responsabilidades ya establecidas por RFC-00XZ (Accepted) y que ninguna RFC del roadmap las redefine.
5. **Stage 4 (Organization):** reemplazar las categorías del ejemplo (Knowledge, Skills, Standards, Runtime Metadata, User Intent) por las categorías canónicas de RFC-00XY: Identity Context, Task Context, Knowledge Context, Capability Context, Execution Metadata. Hoy `feature.md` contradice un RFC aprobado y a `.agents/`.
6. **Context Candidate:** declarar que Organization *produce* candidates (o definir explícitamente qué responsabilidad lo hace), cerrando el encadenamiento hacia Prioritization. Ningún RFC existente define quién transforma información organizada en Context Candidates; si el fix conceptual pertenece a 00XZ/00YB, registrarlo como enmienda.
7. **Context Delivery:** el pipeline de `feature.md` omite Context Delivery, la responsabilidad de transporte del Execution Context vía Delegation Payload definida en RFC-00XZ (corregido el 2 ago 2026: el texto citaba "la 5ª responsabilidad", ordinal prohibido por `plans/INDEX.md` §Convenciones → Citas verificables — queda stale al ampliarse la lista). Incorporarlo al modelo del feature doc y dejar su relación con Prompt Rendering/Materialization como input del Nivel 4.

## D. Regularización de status

- RFC-00YB y RFC-00YC figuran `Status: Proposal` / `Author: TBD` pese a estar marcados ✔ en `feature.md` y ya aplicados en `.agents/`. Actualizar a Approved/Accepted y asignar autor, en coherencia con el resto de la serie.

  Nota (2 ago 2026): ya regularizado fuera de este plan — los headers de ambas RFCs figuran `Status: Accepted` / `Author: Rodrigo Roldán` (ver `plans/rfc/04-*.md` y `plans/rfc/05-*.md`). Esta sección queda sin efecto.

---

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC-00YD Context Composition Model | `plans/rfc/06-context-composition-model.md` |
| 2 | RFC-00XZ actualizado (enmiendas 00YB/00YC) | `plans/rfc/02-execution-context-assembly-process.md` |
| 3 | Status regularizado de 00YB/00YC | `plans/rfc/04-context-candidate-prioritization-model.md`, `plans/rfc/05-context-resolution-model.md` |
| 4 | `feature.md` corregido | `feature.md` |

# Fuera de alcance

- Conflict Classification, Tie-Breaking, Merge, Deduplication (→ Nivel 2).
- Compression, Optimization (→ Nivel 3).
- Cualquier modelo de materialización (→ Nivel 4).
- Cambios de runtime, contratos, harness o state machine (todos los RFCs son de Impact: Conceptual).

---

# Historial

## (Supersedida) Regularizar los RFCs ausentes (00XY, 00XZ, 00YA) — RESUELTO

Sección B original del plan, sin efecto — reemplazada por la sección B vigente (antes "B'"). Se preserva como traza histórica.

Texto original: "Los RFCs 00XX/00XY/00XZ/00YA existen en `plans/` con status Approved/Accepted, y las referencias desde `.agents/` (`orchestrator.md:196`, `worker.md:78`, `SKILLS.md:12,39`) ya resuelven. Esta sección queda sin efecto."

Nota (2 ago 2026): la formulación original era incorrecta en dos puntos — (1) citaba números de línea absolutos sobre archivos mutables (prohibido por `plans/INDEX.md` §Convenciones → Citas verificables); (2) hablaba de "referencias desde `.agents/`" que nunca existieron: grep confirma 0 referencias a `plans/` en `.agents/`. La formulación correcta es: los conceptos ya están definidos inline en `.agents/` (orchestrator.md §5, worker.md §Input from Orchestrator y §Constraints, SKILLS.md §Skill vs. profile y §Validation), conforme a la frontera documental (`plans/INDEX.md` §Convenciones).
