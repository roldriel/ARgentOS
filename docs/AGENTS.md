# docs/ — Carta documental del repositorio

La taxonomía documental de ARgentOS separa cinco dimensiones que no deben
confundirse: **identidad** (qué es), **naturaleza** (qué rol normativo
cumple), **lifecycle** (en qué estado está), **ubicación física** (dónde
vive) y **semántica de referencia** (qué relación expresa una cita). Esta
carta define las cuatro primeras y las reglas de la quinta; la normativa de
gobernanza vive en `docs/CONVENTIONS.md`; los INDEX son registro y
navegación, nunca fuente de normativa.

## Rules

### Naturaleza documental

Las naturalezas documentales son **EntryPoint**, **Policy**, **Governance**,
**Inventory** y **Working**. La clase expresa el rol normativo del documento,
no su carpeta; la carpeta es una convención física (ver mapa folder → clase).

| Naturaleza | Qué es | Ejemplos reales |
|---|---|---|
| **EntryPoint** | Visibilidad de un vistazo; vive en la raíz | `AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE` |
| **Policy** | Reglas vigentes del repo | `docs/AGENTS.md` (esta carta), `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `docs/source-layout.md` |
| **Governance** | Artefactos con ciclo de status propio | RFC (modelo y propuesta de cambio), ADR (decisión), Plan (ejecución) |
| **Inventory** | Registros vivos y verificables: canonical + mutable + verified | `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` (P#, CG#, RC#); `docs/plans/analisis-explicitud.md` (catálogo de gaps, Inventory-like) |
| **Working** | Transitorios, pre-canónicos; nunca targets normativos; pueden ser provenance | Audit, Research, Proposal bajo `docs/working/` |

**Product** y **Tooling** no son naturalezas documentales: son capas físicas
del repositorio con data y código. Product = `protocol/.agents/` +
`protocol/_AGENTS.md`; Tooling = `tools/`, `runtime/`, `tests/`. No se fuerza
clasificación documental sobre artefactos de otras capas.

**Operational** tampoco es una naturaleza documental: `.agents/` en la raíz
es la capa operacional del agente DEV (interfaz de operación del Change
Lifecycle; instrucciones, no autoridad normativa). `docs/` es
autoridad/historia/documentación; `tools/` es verificación determinista.

**Historical** no es una naturaleza: es un lifecycle aplicable a cualquier
clase (un Policy archivado, un Working archivado, un Governance superseded).

**Canonical ≠ immutable.** *Canonical* = referente normativo para
verificación y derivación; puede ser mutable (el Inventory se edita, las
Policy se enmiendan). *Immutable* = traza congelada (archivados, tags, trazas
RFC-46). Un Inventory puede ser canonical + mutable + verified.

### Lifecycle

Estados con transiciones permitidas — **no una cadena lineal**:

- **active**: vigente.
- **archived**: congelado con banner; sigue siendo significado histórico; no
  se borra.
- **superseded**: reemplazado por otro artefacto de la misma clase.
- **deprecated**: fuera de uso sin reemplazo; se declara antes de eliminar.

Los estados pueden coexistir: `superseded ∧ archived` (una RFC superseded se
archiva). No se elimina un documento sin una transición de deprecación o la
regla explícita correspondiente.

### Identity

`RFC-N`, `ADR-N`, `plan NN`, `D#`, `P#`, `CG#`, `RC#` son **identidades
estables** cuando corresponden a artefactos de gobernanza o inventario.
**Identidad ≠ path**: `RFC-69` es identidad; `docs/rfc/69-documentation-taxonomy-and-layout.md`
es ubicación. Mover un archivo no cambia la identidad ni el significado de una
cita: cambia su resolución (path nuevo o mapping histórico). No existe
registry global de IDs: los INDEX cumplen el rol de mapa ID → path → status.

Una **serie** (p. ej. la serie «Change Lifecycle») no es un artifact ni un
registry: en el modelo objetivo es una identidad derivada de declaraciones en
headers + relaciones verificables entre artifacts, y los INDEX la reflejan como
vista descriptiva, nunca autoritativa. No existe entidad ni registry de Series
(`docs/rfc/75-change-lifecycle.md:Mecanismo 11 — Series / Continuity`); la regla
operacional de declaración y verificación está vigente desde el Incremento 1
(plan 96): la membresía se deriva de la declaración `Serie:` del header y de
relaciones verificables RFC↔Plan. El detalle normativo vive en
`docs/CONVENTIONS.md:Change Lifecycle — Serie e identidad derivada (regla
operacional; Incremento 1)`, no en esta carta.

### Folder → class map

| Carpeta | Clase |
|---|---|
| `docs/rfc/` | Governance / RFC |
| `docs/adr/` | Governance / ADR |
| `docs/plans/` | Governance / Plan (+ support docs) |
| `docs/architecture/` | Inventory / Architecture models |
| `docs/working/` | Working (`audits/`, `research/`, `proposals/`) |
| `docs/glossary/` | Inventory / Terminology registry (DESCRIPTIVE; no normativo) |

La clase se deriva de esta carta; la carpeta es convención física, no fuente
de verdad. Support docs clasificados explícitamente:
`docs/plans/analisis-explicitud.md` → Inventory-like;
`docs/plans/skills-mechanism.md` → Governance/support;
`docs/plans/ec-pipeline-vision.md` → Historical (banner de cierre).

Excepciones que no son documentación fuente normal: `sessions/` (staging),
`.project/` (efímero), `tests/fixtures/` (fixtures), `protocol/.agents/`
(Product), `.agents/` (capa operacional DEV; raíz del repo fuente).

### Glosario y semántica de archivos AGENTS / INDEX / ENTRYPOINT

`docs/glossary/INDEX.md` + `docs/glossary/terms.md` forman el **registro
descriptivo de terminología** de ARgentOS (clase: Inventory/registro). No es
fuente normativa: cada entrada enruta a su `Authority Reference`
(`ruta:sección`) y no duplica definiciones. Las reglas normativas de
terminología viven en
`docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones
D1–D5, 2026-09-05)`.

Semántica de nombres de archivo (decisión D3, 2026-09-05; no se renombra nada):

- `AGENTS.md` = **instrucciones de agente** por capa: `AGENTS.md` raíz (DEV),
  `.agents/AGENTS.md` (capa operacional DEV), `AGENTS.md` del adoptante
  (publicado desde `protocol/_AGENTS.md`).
- `protocol/.agents/INDEX.md` = **bootstrap + navegación** del Protocol (rol
  dual; no es un mero registro).
- Los `INDEX.md` de `docs/` e internos = **registro/navegación**; nunca
  autoridad (AU-4).
- `orchestrators/discovery/contracts/ENTRYPOINT.md` = **contrato de discovery**
  de la KB entry `entrypoint.md`; no es una convención de capa (no se crea
  `.agents/ENTRYPOINT.md`).

### References

Cinco clases de referencia:

1. **Normative** — dependencia de gobernanza (plan↔RFC, ADR↔RFC, registro en
   INDEX, par changelog). Dura: rompe CI si no resuelve.
2. **Documentary** — documentación necesaria para interpretar otra. Dura:
   rompe CI si no resuelve.
3. **Provenance / Evidence** — origen o fundamento de una decisión o modelo.
   Puede apuntar a Working; debe resolver contra una copia
   versionada/archivada.
4. **Historical** — relación preservada de una migración o de un documento
   histórico. Se preserva mediante mapping; no se reescribe.
5. **Informational** — mención orientativa; nunca rompe CI.

**Provenance vs Historical:** la distinción depende del documento que
**emite** la referencia, no del target: una referencia emitida por un
documento vivo hacia evidencia working es **Provenance**; una referencia
contenida en un documento histórico/pre-migración es **Historical**.

**Mapping** es un mecanismo de resolución histórica/migratoria, no una nueva
clase de referencia. Las referencias nuevas no usan paths legacy.

### INDEX y CONVENTIONS

**INDEX = registro/navegación** (ID → path → status → relaciones).
**CONVENTIONS = normativa.** No se duplican responsabilidades. Los INDEX de
gobernanza (`docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`)
registran todos los artefactos (mirror mecánico
verificado por `tools/check_plan_structure.py`); las carpetas de working
llevan INDEX livianos de navegación/status.

### ADR

`docs/adr/` aloja ADRs individuales (identidad estable `ADR-N`) y
`docs/adr/INDEX.md` como matriz `D# ↔ ADR ↔ RFC ↔ plan` (many-to-many, sin
relaciones 1:1 inventadas). El backfill de las decisiones D0–D13 del
`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` se ejecutó en el plan 83
(RFC-69, Plan B); `D#` se preserva como identidad histórica y el modelo permanece
como registro del análisis que originó las decisiones. Los ADRs nuevos nacen de
`docs/adr/_TEMPLATE.md` y se registran en el INDEX en el mismo commit.

### Idiomas y citas

Inglés en el protocolo, el código y los commits (Conventional Commits);
español en `docs/`, `docs/plans/` y `docs/rfc/`; `README.md` en inglés. Las
afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). Los documentos de esta carta son
canónicos; el resto del repo referencia, nunca duplica (`docs/CONVENTIONS.md:Convenciones`).

La capa operacional `.agents/` de la raíz (DEV) se escribe en inglés, igual que
el `AGENTS.md` raíz de desarrollo: es lo que leen los agentes.
