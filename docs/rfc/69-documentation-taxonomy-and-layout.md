# RFC-69 — Taxonomía documental del repo fuente: clases, identidad, referencias y layout

**Status:** Accepted (Plan A, 2026-08-27)
**Fecha:** 2026-08-27
**Serie:** Repositorio fuente: taxonomía documental y layout (27 ago 2026)
**Origen:** Diseño con el mantenedor (2026-08-27) y auditoría adversarial de la
primera versión (2026-08-27). Evidencia: `docs/AGENTS.md:Rules`,
`docs/AUDITORIA_DOCUMENTACION.md:Deuda técnica`,
`docs/VERSIONING.md:4.1 Batería canónica de verificación`,
`docs/CONVENTIONS.md:Convenciones`.
**Pregunta:** ¿Cómo se organiza la documentación del repo fuente para que la
raíz quede limpia, la navegación escale con RFC + ADR + plan, y la semántica
documental (clase, lifecycle, identidad, referencia) no se confunda con la
ubicación física ni acople la verificación a documentos transitorios?
**Afectados:** — (ninguna ruta de `protocol/.agents/`)

## Problema

1. **La raíz se ensucia.** Hoy conviven en la raíz los entry points
   (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`) con
   documentos sin hogar clasificado: `ARCHITECTURAL_PROBLEM_MODEL.md`,
   `ARCHITECTURAL_DECISION_MODEL.md`, `WORKFLOW_PROPOSAL.md`,
   `AUDITORIA_SISTEMA.md`, `AUDITORIA_SISTEMA_2026-08-16.md`,
   `AUDITORIA_REUTILIZACION_2026-08-25.md` e
   `INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`. La regla vigente reserva
   la raíz a lo que debe verse de un vistazo (`docs/AGENTS.md:Rules`).
2. **La navegación no escala.** La historia de diseño concentraba 161
   documentos `.md` committeados (91 en `plans/` + 70 en `plans/rfc/`); el
   working tree llegaba a 162 con el draft de esta RFC. El registro de RFCs
   vive ahora en `docs/rfc/INDEX.md` y las tablas por serie en
   `docs/plans/INDEX.md`. El INDEX anterior acumulaba roles mezclados
   (series, RFC, roadmap, backlog, convenciones, archivo, visión); la deuda
   ya fue declarada (`docs/AUDITORIA_DOCUMENTACION.md:Deuda técnica`).
3. **La anidación `plans/rfc/` no admite un tercer artefacto.** El flujo del
   proyecto incorpora ADR (decisión). Mantener `plans/rfc/` y agregar
   `plans/adr/` anidaría clases que no son sub-planes: RFC (modelo/propuesta),
   ADR (decisión), plan (ejecución).
4. **La semántica se confundía con la ubicación.** La clase de un documento se
   infería de su carpeta, su identidad de su path, y toda referencia era
   `ruta:sección` sin distinguir qué clase de relación expresa.
5. **La verificación acoplaba documentos transitorios.** `check_plan_citations.py`
   (batería canónica y CI) verifica toda cita producida bajo la historia de
   diseño y en los docs canónicos: planes 58–74 citaban auditorías, planes
   76–82 y RFCs 62–68 citaban los modelos arquitectónicos, y RFC-68 cita
   `WORKFLOW_PROPOSAL.md` e `INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`
   como evidencia (**16 ocurrencias verificadas: 11 de `WORKFLOW_PROPOSAL.md`
   y 5 de `INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`**).
6. **El estado publicado ya estaba comprometido.** RFC-68 (Accepted, publicado
   en 9.1.0) y el plan 82 citaban `WORKFLOW_PROPOSAL.md` e
   `INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`, que estaban **untracked**:
   un clone fresco de `master` fallaba `check_plan_citations`.
   `AUDITORIA_REUTILIZACION_2026-08-25.md` también estaba untracked, pero solo
   era citada por documentos untracked. **Los tres se contienen y versionan en
   esta implementación** (invariante de contención).
7. **Rol preciso de los checkers.** `check_plan_citations.py` y
   `check_plan_structure.py` pertenecen a la batería canónica
   (`docs/VERSIONING.md:4.1 Batería canónica de verificación`) y a CI.
   `check_architecture_traceability.py` es **dev-only**: no está en la batería
   ni en CI; se actualiza al layout nuevo y **permanece dev-only**.

## Objetivos

- Establecer **naturaleza documental** y **lifecycle** como dimensiones
  separadas.
- Separar **identidad, clase, lifecycle, path y semántica de referencia**.
- Definir clases de referencia con comportamiento de verificación diferenciado.
- Permitir que los working documents sean evidencia/provenance sin ser targets
  de dependencia normativa permanente.
- Dejar la raíz en entry points y dar hogar clasificado a todo documento.
- Hacer navegables planes/RFCs/ADRs con INDEX-registro y reglas normativas en
  CONVENTIONS.

## No-objetivos

- No es un sistema de gestión documental: no hay registry global de IDs, front
  matter obligatorio, UUIDs, generador obligatorio de INDEX, base de datos, ni
  servicio de documentación.
- No rediseña `protocol/.agents/` ni `dist`.
- No backfillea ADRs (plan separado de gobernanza ADR).
- No decide si `check_architecture_traceability.py` entra a CI (decisión
  explícita futura, no automática).
- No agrupa físicamente las RFCs.
- No automatiza la promoción working → canonical.

## Modelo

### Taxonomía (naturaleza documental)

La clase expresa qué es un documento por su rol normativo, no por dónde vive.
Las carpetas son convención física; la clase se deriva de `docs/AGENTS.md`.

| Naturaleza | Artefactos reales | Rol |
|---|---|---|
| **EntryPoint** | `AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE` | Visibilidad de un vistazo |
| **Policy** | `docs/AGENTS.md` (carta), `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `docs/source-layout.md` | Reglas vigentes del repo |
| **Governance** | RFC (modelo y propuesta de cambio; rol dual declarado), ADR (decisión individual), Plan (ejecución) | Ciclos de status propios |
| **Inventory** | `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` (P#, CG#, RC#); `docs/plans/analisis-explicitud.md` (Inventory-like) | Registros vivos y verificables |
| **Working** | Audit (`AUDITORIA_*`), Research (`INVESTIGACION_*`), Proposal (`WORKFLOW_PROPOSAL.md`) | Transitorios, pre-canónicos |

**Product** y **Tooling** no son naturalezas documentales: son capas físicas
con data y código, y se declaran como tales en la carta. **Historical** no es
una naturaleza: es un lifecycle aplicable a cualquier clase.

**Canonical ≠ immutable.** *Canonical* = referente normativo para
verificación y derivación; puede ser mutable (el Inventory se edita, las
Policy se enmiendan). *Immutable* = traza congelada (archivados, tags, trazas
RFC-46). El Problem Inventory es **canonical + mutable + verified**: cada
problema exige evidencia resoluble (AEW-002).

Support docs clasificados explícitamente: `docs/plans/analisis-explicitud.md`
→ Inventory-like; `docs/plans/skills-mechanism.md` → Governance/support;
`docs/plans/ec-pipeline-vision.md` → Historical (banner de cierre).

### Lifecycle

Estados con transiciones permitidas, **no una cadena lineal**:
`active`, `archived`, `superseded`, `deprecated`.

- **active**: referente vigente.
- **archived**: congelado con banner; sigue siendo significado histórico;
  nunca se borra.
- **superseded**: reemplazado por otro artefacto de la misma clase.
- **deprecated**: fuera de uso sin reemplazo; se declara antes de eliminar.

Los estados pueden coexistir: `superseded ∧ archived` (una RFC superseded se
archiva). No existe borrado sin deprecación o regla explícita.

### Identidad documental

`RFC-N`, `ADR-N`, `plan NN`, `D#`, `P#`, `CG#`, `RC#` son **identidades
estables** cuando corresponden a artefactos de gobernanza o inventario. El path
es ubicación física.

- `RFC-69` es identidad; `docs/rfc/69-documentation-taxonomy-and-layout.md` es
  ubicación.
- **Mover un archivo ≠ cambiar su identidad.** Una referencia a RFC-69 sigue
  refiriendo a RFC-69 aunque el archivo se mueva.
- Consecuencia: cuando un documento cambia de ubicación, el **significado** de
  una cita no cambia; cambia su **resolución** (path nuevo o mapping
  histórico). Las referencias vivas se actualizan; las históricas se mapean.
- No se diseña un registry global de IDs: los INDEX por carpeta cumplen el rol
  de mapa ID → path → status.

### Semántica de referencias

| Clase | ¿Se verifica? | ¿Puede romper CI? | ¿Puede apuntar a working? | ¿Requiere archivo? | ¿Requiere sección? | ¿Resolución por mapping? |
|---|---|---|---|---|---|---|
| **Normative** (dependencia de gobernanza: plan↔RFC, ADR↔RFC, registro en INDEX, par changelog) | Sí | Sí | No | No | No (vínculo por ID/registro) | Solo histórico |
| **Documentary** (documentación necesaria para interpretar) | Sí | Sí | No | No | Sí (`ruta:sección`) | Solo histórico |
| **Provenance / Evidence** (origen o fundamento: RFC-68 → `WORKFLOW_PROPOSAL.md`; P# → evidencia) | Sí | Sí, si la evidencia se borra sin archivar | Sí | Sí (versionado/archivado al citar) | Sí | Sí (histórico) |
| **Historical** (relación preservada de una migración) | No contra la taxonomía actual | No, una vez mapeada | Sí (lo que existía) | No | Se conserva tal cual fue escrita | Sí, exclusivo |
| **Informational** (mención orientativa, URL, backtick sin sección) | No | No | Sí | No | No | No |

Reglas derivadas: Normative + Documentary son **duras**; Provenance es dura
contra la copia archivada/versionada (borrar evidencia citada sin deprecación
rompe CI a propósito); Historical nunca se reescribe y se absorbe por mapping;
Informational nunca rompe CI.

**Provenance vs Historical:** la distinción depende del documento que
**emite** la referencia, no del target: emitida por un documento vivo hacia
evidencia working = Provenance; contenida en un documento histórico/pre-migración
= Historical.

### Layout físico

```text
docs/
├── AGENTS.md            carta: clases, lifecycle, identidad, referencias
├── CONVENTIONS.md       reglas normativas del repo
├── VERSIONING.md, ADOPTION.md, MIGRATION.md, source-layout.md
├── rfc/                 plano (criterio de no-agrupación declarado)
│   ├── INDEX.md         registro: RFC → path → status → planes
│   └── RFC-*.md
├── adr/                 (se materializa en el plan de gobernanza ADR)
│   └── INDEX.md         matriz futura D# ↔ ADR ↔ RFC ↔ plan
├── plans/               plano; navegación por series en su INDEX
│   ├── INDEX.md         registro de planes + series
│   └── NN-*.md
├── architecture/
│   ├── ARCHITECTURAL_PROBLEM_MODEL.md       (Inventory)
│   └── ARCHITECTURAL_DECISION_MODEL.md      (pendiente de conversión ADR, Plan B)
└── working/
    ├── audits/          + INDEX.md (archivo, fecha, status)
    ├── research/        + INDEX.md
    └── proposals/       + INDEX.md
```

Nombres de carpeta en inglés; los nombres de archivo se conservan (son
contenido y traza). La clase no la define la carpeta: `docs/working/audits/`
es convención física de la clase Working/Audit, declarada en la carta.

**RFCs físicamente planas.** Criterio explícito: agrupar físicamente solo
donde existe un eje temático estable ya documentado — `plans/` lo tiene en las
series del INDEX; las RFCs no tienen eje de serie y su numeración es identidad
secuencial. El descubrimiento lo cubre `docs/rfc/INDEX.md`; la agrupación a
escala queda como Future Evolution.

### Semántica de INDEX

- **INDEX = registro y navegación** (ID → path → status → relaciones).
- **CONVENTIONS = normativa** (`docs/CONVENTIONS.md`).
- `docs/plans/INDEX.md` no carga convenciones; `docs/rfc/INDEX.md` espeja las
  RFCs; `docs/adr/INDEX.md` llega con el plan ADR; las carpetas de working
  llevan INDEX livianos sin verificación mecánica.
- Referencias históricas a la sección Convenciones del antiguo `plans/INDEX.md`
  se resuelven por mapping y anclas de navegación; el criterio de remoción de
  un ancla es cero referencias vivas y referencias históricas resueltas.

### Modelo ADR

- **ADR = registro individual** de una decisión (contexto, alternativas,
  decisión, consecuencias, status).
- **ADR INDEX = vista agregada**: matriz `D# ↔ ADR ↔ RFC ↔ plan`,
  **many-to-many** (ejemplo real: D11 → RFC-62 y RFC-66). No se imponen
  relaciones 1:1.
- Migración D0–D13: cada decisión del modelo actual (que ya tiene estructura
  ADR completa) se convierte en una ADR individual en un **plan separado**;
  `D#` se preserva como identidad histórica. El
  `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` permanece como modelo
  pendiente de conversión (Plan B) y no se convierte en esta tarea.
- No se inventan relaciones inexistentes: solo D0–D13, con mapeo documentado a
  RFCs 62–68.

### Working / Provenance

Regla: **un working document no puede ser target de una dependencia normativa
permanente, pero puede ser evidencia o provenance de una decisión, RFC,
inventario o auditoría.**

Caso real preservado: `WORKFLOW_PROPOSAL.md` e
`INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md` → RFC-68. La relación es
válida (provenance) y RFC-68 no se invalida; los documentos pasan a
`docs/working/` versionados y sus citas se conservan.

Comportamiento por estado del working document:

1. **Activo**: puede citarse como provenance; debe estar versionado.
2. **Archivado**: la cita resuelve contra la copia archivada (banner); no se
   duplica contenido.
3. **Promovido a conocimiento canónico**: la conclusión se incorpora al
   documento canónico; el working se archiva como evidencia; la referencia se
   conserva como provenance/histórica. Promover no significa "convertir el
   archivo".
4. **Eliminado**: solo tras archivado o tras enmendar/remover la cita; borrar
   evidencia citada sin deprecación rompe CI (intencional).

La promoción no se automatiza en esta RFC.

### Migración legacy

Invariantes del mapping (implementado en `tools/legacy_paths.py`):

```text
legacy path → un único target canónico
ninguna referencia nueva a paths legacy (el checker la detecta)
mapping es migration-only
mapping debe ser removible
```

Orden de resolución obligatorio: `plans/rfc/` → `docs/rfc/` antes que
`plans/` → `docs/plans/`; los bare paths de modelos, auditorías,
investigaciones y propuestas mapean a su hogar canónico. El formato concreto de
la tabla pertenece a la implementación; la RFC fija las invariantes.

### Tooling boundary

**Normativo (qué verifica el tooling):** referencias duras
(normative/documentary/provenance); documentos canonical registrados en los
INDEX; qué constituye una referencia rota; mappings válidos (un target, sin
referencias nuevas); working docs como evidencia permitida; invariantes de
INDEX (mirror por carpeta de gobernanza).

**Implementación abierta (cómo):** cantidad de scripts, estructura interna,
parser, CLI, formato interno del mapping, generación, optimización. No se
diseña un framework de checkers.

- `check_plan_citations.py` y `check_plan_structure.py` (batería + CI) operan
  sobre `docs/plans/` y `docs/rfc/` y excluyen working como targets
  normativos.
- `check_architecture_traceability.py` se actualiza a las rutas nuevas y
  **permanece dev-only**; su incorporación a CI es una decisión explícita
  futura.

### Versionado

Regla inequívoca para un plan que modifica solo documentación/estructura fuente
(sin `protocol/.agents/`, sin payload):

```text
cambio docs-only → ítem en CHANGELOG [Unreleased] con (plan, RFC-69)
                 → sin versión de payload, sin VERSION bump, sin tag
```

Se descarta "repository governance release" (tag sin VERSION) porque violaría
la invariante versión ↔ changelog ↔ tag (`docs/VERSIONING.md:2. Invariantes`).
`docs/VERSIONING.md` se enmienda para declarar esta regla.

### Invariante de contención (untracked)

**Un documento referenciado por un artefacto versionado no puede depender de
existir únicamente en el working tree.** Es una invariante arquitectónica; la
acción de migración (versionar los tres working docs) pertenece a esta
implementación.

## Alternativas consideradas

1. **Mover solo los documentos sueltos y dejar `plans/` en la raíz.**
   Descartada: no resuelve la navegación de 161+ documentos ni da hogar al ADR;
   el costo marginal de la mudanza completa es acotado si se hace ahora.
2. **Mantener `plans/rfc/` y agregar `plans/adr/`.** Descartada: mezcla clases
   distintas (modelo, decisión, ejecución) bajo "planes".
3. **RFCs planas vs agrupadas.** Se acepta **plana** con criterio explícito
   (eje de serie documentado solo para planes; `docs/rfc/INDEX.md` cubre el
   descubrimiento). Agrupación a escala = Future Evolution.
4. **INDEX sobrecargado vs INDEX + CONVENTIONS.** Se acepta la separación.
5. **canonical/working binario.** Descartado: confunde naturaleza con
   lifecycle y no admite el Problem Inventory (canonical + mutable).
6. **Identidad por path.** Descartada como modelo: se adopta identidad estable
   mínima, sin registry global.
7. **Exclusión total de working de la verificación.** Descartada: invalida la
   relación provenance real de RFC-68; se adopta no-target-normativo con
   provenance permitida.
8. **Release de gobernanza con tag.** Descartada: viola la invariante
   versión ↔ changelog ↔ tag.

## Alcance

**Incluido:** taxonomía (naturaleza), lifecycle, identidad, semántica de
referencias, layout físico, INDEX/CONVENTIONS, modelo ADR (nivel conceptual),
working/provenance, invariantes de migración legacy, contención (untracked) y
versionado docs-only.

**Requerido para migración:** movimientos `git mv`, actualización de rutas en
documentos vivos, mappings, INDEX por carpeta, actualización de checkers y
tests, contención y commit de los working docs, enmienda de
`docs/VERSIONING.md`.

**Fuera de alcance:** backfill completo de ADR, rediseño del protocolo,
cambios en `dist`, metadata/front matter, automatizaciones, agrupación física
de RFCs, registry global de IDs, ingreso de `check_architecture_traceability.py`
a CI.

## Criterios de aceptación

Cada criterio es verificable PASS/FAIL.

- **Layout.** La raíz contiene solo entry points y capas de desarrollo; la
  estructura `docs/` refleja el Modelo; los tres working docs están contenidos
  y versionados.
- **Identity.** Los IDs (`RFC-N`, `plan NN`, `D#`, `P#`, `CG#`, `RC#`) son
  únicos y estables; mover un archivo no cambia su identidad; las referencias
  vivas apuntan a los paths nuevos.
- **Classification.** Todo artefacto real mapea a una clase de naturaleza y un
  lifecycle declarados en `docs/AGENTS.md`; el Problem Inventory está
  clasificado como inventory.
- **Lifecycle.** Working docs con lifecycle declarado; archivado con banner;
  ningún borrado sin deprecación.
- **References.** Normative/Documentary resuelven y rompen CI si no;
  Informational no se verifica; Provenance resuelve contra copia
  versionada/archivada; ninguna referencia nueva usa paths legacy.
- **Provenance.** RFC-68 y plan 82 verifican en un clone fresco; la invariante
  de contención se cumple.
- **Legacy mappings.** Un target canónico por path legacy; cero referencias
  nuevas; migration-only; removible.
- **INDEX.** `docs/plans/INDEX.md` sin normativa; `docs/rfc/INDEX.md` espeja
  las RFCs; convenciones en `docs/CONVENTIONS.md`.
- **Tooling.** Checkers actualizados y verdes; `check_architecture_traceability.py`
  dev-only.
- **Versioning.** El plan docs-only tiene ítem en `[Unreleased]`, sin VERSION
  bump ni tag; `docs/VERSIONING.md` declara la regla.
- **Repository integrity.** Batería canónica verde; `protocol/.agents/` y
  `dist` sin cambios.

## Riesgos

- Los mappings legacy pueden acumularse y devenir segunda taxonomía; mitigado
  por las invariantes (un target, sin refs nuevas, removible).
- Las referencias por path persisten: futuros movimientos siguen costando; el
  INDEX debe mantenerse al día.
- Clase por carpeta puede derivar si un documento cambia de carpeta; la carta
  es la fuente y el folder→class map la hace interpretable.
- "Un plan = una versión" (VERSIONING §3) es una restricción adyacente que no
  se resuelve aquí y que a 100+ planes se vuelve ruido.
- El backfill ADR (plan separado) puede racionalizar retrospectivamente; se
  declararán "alternativas no documentadas" donde corresponda.

## Future Evolution

Registradas como evolución, **no** como requisitos de esta RFC: front matter /
metadata para clase y status; registry global de IDs; generador/verificador de
INDEX; agrupación física de RFCs a escala; fragmentación del Problem Inventory
(umbral sugerido: >50 P#/CG# o >2 dominios); ingreso de
`check_architecture_traceability.py` a CI; backfill de decisiones no D0–D13;
automatización de la promoción working → canonical.

## Amendment Log

- 2026-08-27 — Creación (v1).
- 2026-08-27 — Reescritura integral tras auditoría arquitectónica (MAJOR
  REVISION): naturaleza × lifecycle; clases de referencia; identidad vs path;
  INDEX/CONVENTIONS; Problem Inventory; invariante de contención; versionado
  docs-only; rol dev-only de `check_architecture_traceability.py`.
- 2026-08-27 — Correcciones factuales: conteo de `plans/` (161 committeados /
  162 con el draft); referencias de RFC-68 a working docs (16: 11 + 5);
  atribución de untracked (dos citados por versionados; el tercero solo por
  untracked); layout incluye `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md`
  pendiente de conversión; clasificación de support docs. Aceptada con
  autorización del mantenedor para ejecutar el Plan A.
- 2026-08-27 — Plan B ejecutado (plan 83): `docs/adr/` materializado con 14 ADRs
  individuales (ADR-01…ADR-14 ↔ D0–D13 preservadas como identidad histórica),
  matriz many-to-many en `docs/adr/INDEX.md`, template `_TEMPLATE.md`, ciclo de
  status ADR en `docs/CONVENTIONS.md` y cobertura de `docs/adr/` en
  `tools/check_plan_structure.py` y `tools/check_plan_citations.py`. El modelo
  ADR de esta RFC no cambia.
- 2026-09-21 — Determinación registrada por el Plan 141 (`HD-8`). El ingreso de
  `check_architecture_traceability.py` a CI que esta RFC dejó en su evolución
  futura **no se adopta**: la decisión sigue siendo explícita y futura, no
  automática, y el checker permanece una ayuda de navegación DEV fuera de la
  batería canónica. La determinación cierra la continuidad de esa evolución sin
  modificar el checker, CI ni el modelo de esta RFC.
