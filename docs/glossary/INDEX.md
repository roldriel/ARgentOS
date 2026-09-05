# Glossary — Registro terminológico de ARgentOS (DEV)

> Clase documental: **Inventory / registro descriptivo** (no normativo).
> Reglas normativas: `docs/CONVENTIONS.md:Convenciones de terminología y > nomenclatura (decisiones D1–D5, 2026-09-05)`.
> Taxonomía documental: `docs/AGENTS.md:Folder → class map`.

## Qué es y qué no es

**Es:** el puente descriptivo entre los vocabularios de **DEV** y
**Protocol**. Registra, por término: `Scope`, `Status`, `Authority Reference`
(fuente normativa), abreviaturas/expansiones, alias, términos prohibidos,
regla de calificación y relaciones. No define conceptos: enruta a quien los
define.

**No es:** fuente normativa, segunda autoridad, definición canónica ni
ontología. No prevalece sobre RFC/ADR/estándar del payload ni sobre la
gobernanza DEV. El payload del Protocol **no referencia** `docs/glossary/`
(boundary DEV/Protocol; `docs/CONVENTIONS.md:Frontera documental (Producto)`).

## Uso por agentes

1. Para saber **dónde** se define un término: buscar la entrada en
   `docs/glossary/terms.md:<Term>` y seguir su `Authority Reference`.
2. Para **escribir** texto normativo nuevo: aplicar las reglas de
   `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)` (calificación obligatoria de términos
   overloaded en contexto cross-layer; regla SCI).
3. Si el dominio no puede inferirse con seguridad, **no asumir semántica**:
   marcar la ambigüedad (BOUNDARY / NEEDS_CLARIFICATION) antes de usarla en
   una decisión.

## Campos de una entrada

Mínimos (REQUIRED): `Term`, `Scope` (`DEV | Protocol | Cross-cutting`),
`Status`, `Authority Reference` (`ruta:sección` resoluble).

Opcionales (solo cuando aplican): `Abbreviation / Expansion`, `Aliases`,
`Forbidden Terms`, `Qualification Rule`, `Related Terms`, `Historical Note`,
`Migration Reference` y un `Gloss` no normativo de una línea, marcado
explícitamente como resumen (nunca como definición).

**Prohibido:** duplicar definiciones normativas (single-source;
`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`). Si una fuente define, el glosario cita.

## Status de un término

- `current` — vigente.
- `historical` — traza preservada (RFC-46; no se reescribe ni reinterpreta).
- `deprecated` — fuera de uso con declaración; se elimina solo tras
  deprecación explícita.
- `superseded` — reemplazado por otro término de la misma clase.
- `forbidden` — prohibido en texto nuevo (p. ej. `SCI` desnudo en texto
  cross-layer; uso histórico permitido como traza).

## Registro inicial de términos

| Term | Scope | Status | Authority Reference |
|---|---|---|---|
| AGENTS.md | Cross-cutting | current | `docs/AGENTS.md:Naturaleza documental` |
| Anchor | Cross-cutting | current | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)` |
| Artifact | Cross-cutting | current | `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule` |
| Change Lifecycle | DEV | current | `docs/rfc/75-change-lifecycle.md:Terminología` |
| Checkpoint | DEV | current | `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)` |
| Context | Protocol | current | `protocol/.agents/standards/context/CONTEXT.md:Context segments, identity, scope and isolation` |
| Correction | Cross-cutting | current | `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` |
| DEV | Cross-cutting | current | `AGENTS.md:Repository layout` |
| ENTRYPOINT.md | Protocol | current | `protocol/.agents/orchestrators/discovery/contracts/ENTRYPOINT.md:Purpose` |
| EntryPoint | DEV | current | `docs/AGENTS.md:Naturaleza documental` |
| Execution | Protocol | current | `docs/rfc/64-execution-record-model.md:Terminology` |
| EXECUTION_PLAN artifact | Protocol | current | `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Purpose` |
| Finding | Cross-cutting | current | `docs/rfc/75-change-lifecycle.md:Terminología` |
| Glossary | DEV | current | `docs/AGENTS.md:Folder → class map` |
| INDEX | Cross-cutting | current | `docs/AGENTS.md:INDEX y CONVENTIONS` |
| Payload | Cross-cutting | current | `AGENTS.md:Repository layout` |
| Plan | Cross-cutting | current | `docs/VERSIONING.md:7. Estados de planes y RFCs` |
| Profile | Protocol | current | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:profile` |
| Protocol | Cross-cutting | current | `protocol/_AGENTS.md:Active roles` |
| SCI | Cross-cutting | current (restricted) | `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)` |
| Scoped Content Identity | DEV | current | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)` |
| SemanticContextIdentity | Protocol | current | `protocol/.agents/standards/context/CONTEXT.md:Identity` |
| Session | Protocol | current | `docs/rfc/64-execution-record-model.md:Terminology` |
| State | Cross-cutting | current | `docs/rfc/63-state-and-artifact-lifecycle-model.md:Terminology` |
| Status | Cross-cutting | current | `docs/VERSIONING.md:7. Estados de planes y RFCs` |
| Validation | Cross-cutting | current | `docs/rfc/65-evidence-and-verification-model.md:Terminology` |
| Validation Anchor | DEV | current | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)` |
| Verification | Cross-cutting | current | `docs/rfc/65-evidence-and-verification-model.md:Terminology` |

## Regla SCI (resumen)

- `Scoped Content Identity` — **DEV** (Validation Anchors del Change
  Lifecycle).
- `SemanticContextIdentity` — **Protocol** (identidad del contexto semántico
  compuesto; RFC-71).
- `SCI` desnudo **no es aceptable** en texto cross-layer nuevo; la primera
  aparición debe expandir la abreviatura y la calificación de capa es
  obligatoria ante ambigüedad (`SCI (DEV)` / `SCI (Protocol)`). No se renombra
  ninguna identidad; los históricos no se reescriben (RFC-46).

## Semántica AGENTS / INDEX / ENTRYPOINT (resumen)

| Archivo | Función |
|---|---|
| `AGENTS.md` (raíz DEV; `.agents/AGENTS.md`; `AGENTS.md` del adoptante) | **Instrucciones de agente** por capa |
| `protocol/.agents/INDEX.md` | **Bootstrap + navegación** del Protocol (rol dual; no se renombra) |
| `docs/*/INDEX.md` e INDEX internos | **Registro/navegación** (nunca autoridad; AU-4) |
| `orchestrators/discovery/contracts/ENTRYPOINT.md` | **Contrato de discovery** (`entrypoint.md` KB; no es convención de capa) |

No se introduce `.agents/ENTRYPOINT.md` ni `BOOTSTRAP.md` como convención de
capa (D3).

## Vínculos

- Reglas normativas: `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`.
- Taxonomía documental y semántica de archivos: `docs/AGENTS.md:Glosario y semántica de archivos AGENTS / INDEX / ENTRYPOINT`.
- Origen: `docs/plans/105-terminology-architecture-materialization.md`.
