# ADR-17 — Repository Structure: Lifetime Model and Composite Placement

**Status:** Accepted
**Fecha:** 2026-09-15
**Decisión original:** — (decisión nueva de arquitectura de repositorio DEV; no deriva del modelo D#)
**RFC:** — (decisión de estructura del repo fuente; no requiere RFC mientras no toque `protocol/.agents/`; ver Estado de implementación)
**Plan:** plan 125 (`docs/plans/125-repository-architecture-decisions.md`)
**Clase de cambio:** — (docs-only; no toca `protocol/.agents/`; ver RFC-56)
**Problemas que resuelve:** — (ambigüedad de lifetime/persistencia y ausencia de criterio estructural; ver Contexto)

## Contexto

Una revisión integral read-only de la estructura del repositorio (`dev` @ `4cd11ed`)
determinó que ARgentOS ya tiene una arquitectura coherente de **dos ejes**:

1. **capa/dominio** — `protocol/` (payload distribuido), `runtime/` + `tools/` +
   `tests/` (ejecución y verificación DEV), `docs/` + `.agents/` (autoridad y
   operación DEV);
2. **lifetime/autoridad** — normativo vivo, traza normativa congelada,
   derivado/navegación, estado de ejecución efímero, externo desechable.

La revisión identificó además que el eje de lifetime se expresa hoy por
**convención** y no por carpetas, y que dos artefactos de gobernanza declaran
cosas distintas sobre la persistencia:

- `docs/AGENTS.md:Naturaleza documental` declara que *«Historical no es una
  naturaleza: es un lifecycle aplicable a cualquier clase»*: lifetime ya es una
  dimensión independiente de la clase documental.
- `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Purpose` declara el
  Change Governance Artifact como una categoría *«durable, per-project»* que
  *«survives»*, materializada en `.project/changes/<change_identity>.md`, **sin
  mencionar Git** en su semántica de persistencia.
- El bloque `# Generated session artifacts` de `.gitignore` ignora la totalidad
  de `.project/`, de modo que en este repositorio la categoría
  durable es efímera en la práctica.
- `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project
  state` ya distingue conceptualmente estado durable de estado de sesión **dentro
  del mismo padre**, sin exigir separación física.
- `docs/rfc/69-documentation-taxonomy-and-layout.md:Layout físico` fija la
  planitud de `docs/rfc/` y `docs/adr/`, y RFC-46 prohíbe reescribir citas
  históricas.

La arquitectura estructural no estaba decidida: no existía una decisión
registrada sobre si lifetime debe ser una dimensión física del árbol ni sobre si
el repositorio debe adoptar una única estructura física global. Este ADR registra
esas dos decisiones, tomadas por el mantenedor el 2026-09-15.

## Alternativas consideradas

### A — Lifetime como dimensión física general

Separar lifetime en namespaces físicos (`durable/`, `ephemeral/`, `history/` o
equivalentes), haciéndolo visible y mecánicamente verificable en todo el árbol.

*Pros:* la distinción se vuelve evidente; un checker de placement puede
verificarla; la mezcla accidental se detecta.

*Contras:* introduce un tercer eje de organización sobre un árbol que ya expresa
dos; degrada la estabilidad de las citas `ruta:sección` de los 232 documentos de
gobernanza versionados; entra en tensión directa con la regla de no relocalizar
historia congelada (RFC-46); requiere un inventario permanente de mapeo legacy.

### B — Lifetime como propiedad semántica, con separación física local admitida

Lifetime permanece como propiedad declarada del artefacto; las carpetas no lo
codifican de forma general. La separación física se admite únicamente donde la
persistencia ya es contractual y está en discusión (`.project/`).

*Pros:* no mueve nada; preserva la estabilidad de citas y la planitud fijada por
RFC-69; mantiene clase y lifetime como dos ejes independientes, coherente con
`docs/AGENTS.md:Naturaleza documental`; no crea maquinaria nueva.

*Contras:* lifetime no es visible sin leer declaraciones; exige que el contrato
de placement lo registre explícitamente para no perderse.

### C — Única estructura física global obligatoria

Adoptar una organización estructural uniforme para todos los namespaces.

*Pros:* uniformidad conceptual.

*Contras:* ignora que los namespaces tienen naturalezas, owners, lifecycles y
boundaries distintos; fuerza reestructuración de `tests/`, `tools/` y `runtime/`
sin razón semántica; contradice la conclusión de la revisión de que el layout
actual es fundamentalmente sólido y que los defectos son locales.

### D — Sin decisión (statu quo no declarado)

Mantener el estado actual sin registrar el criterio estructural.

*Contras:* deja el eje de lifetime como convención tácita y deja la ambigüedad
de persistencia de `.project/` sin resolver para todo cambio futuro.

## Decisión

Se adoptan **B** (lifetime semántico con separación física local admitida) y el
criterio de **arquitectura estructural compuesta**.

**1. Modelo de lifetime.** Lifetime es una **propiedad semántica** del artefacto,
**independiente** de su naturaleza/clase documental. En `docs/`, lifetime no se
convierte en una dimensión física del árbol: `docs/` no se reorganiza para hacer
visible lifetime y **no se crean namespaces globales** `durable/`, `ephemeral/`,
`history/` ni equivalentes. **No existe una regla global `lifetime → folder`.**

**2. Separación física local.** Dentro de `.project/` se admite una separación
física específica entre estado **project-durable** y estado
**session-ephemeral**, si y sólo si una decisión posterior sobre persistencia la
requiere. Esta admisión no la ejecuta ni la presume: no se mueve
`.project/changes/`, no se modifica `.gitignore` y no se modifican runtime
resolvers como consecuencia de este ADR.

**3. Estructura compuesta.** No existe una única estrategia estructural global
obligatoria. La estructura se decide **por namespace/dominio** cuando exista una
razón semántica para hacerlo, según naturaleza, owner, authority, lifecycle,
persistence y boundary. `docs/` conserva su organización actual sin reagrupación
clean-slate; el Protocol payload resuelve su propia frontera; `tests/`, `tools/`,
`runtime/` y los demás namespaces DEV no se reestructuran para satisfacer una
teoría global de carpetas.

**4. Persistencia de `.project/`.** `.project/changes/` **conserva su path**. La
arquitectura distingue explícitamente **project-durable state** de
**session-ephemeral state**, y **«durable» no debe interpretarse automáticamente
como «Git committed»** en el contrato Protocol. El contrato Protocol debe
expresar explícitamente su semántica de lifetime/persistence; cualquier decisión
futura de Git persistence pertenece al dominio y a la autoridad correspondientes.

**Límite de autorización.** Esta decisión **no autoriza migración alguna**. No
habilita cambios de payload, no resuelve ninguna decisión de placement pendiente
y no sustituye la vía de autorización RFC-56.

## Consecuencias

- Lifetime y clase documental permanecen como **dos ejes independientes**.
- No existe una regla global `lifetime → folder`; el placement podrá variar por
  namespace con razón semántica.
- `docs/` conserva su organización; ninguna reagrupación clean-slate queda
  habilitada por este ADR.
- `.project/changes/` conserva su ubicación; la distinción durable/ephemeral se
  expresa semánticamente y su explicitación contractual queda pendiente con vía
  RFC-56.
- «Durable» no implica Git-committed por defecto.
- El Repository/Artifact Placement Contract queda **downstream** de este ADR y
  **no** debe convertirse en la fuente de verdad de la arquitectura.
- Las decisiones de placement pendientes (distribución de tests del payload,
  self-containment del payload, boundary checker, vocabulario `tags.kind`,
  clasificación documental DEV, estructura interna del harness, navegación y
  `protocol/.project/`) **permanecen abiertas** y no se derivan de este ADR.

## Invariantes

- **RS-1**: Lifetime es una propiedad semántica independiente de la
  naturaleza/clase del artefacto; ninguna carpeta del árbol implica por sí sola un
  lifetime.
- **RS-2**: No existe una regla global que mapee lifetime a una ubicación física;
  toda correspondencia lifetime↔ubicación es local a un namespace y explícita.
- **RS-3**: Ninguna reestructuración de un namespace DEV puede justificarse
  únicamente por uniformidad estructural.
- **RS-4**: `docs/` no se reorganiza para hacer visible lifetime; su planitud y
  sus citas se preservan.
- **RS-5**: «Project-durable» no implica «Git-committed»; ambas propiedades se
  declaran por separado.
- **RS-6**: El Placement Contract es downstream de la decisión arquitectónica y
  no es fuente de autoridad arquitectónica.
- **RS-7**: Este ADR no autoriza migración, cambio de payload ni resolución de
  decisiones de placement abiertas.

## Relaciones

- Depende de: — (decisión nueva; no deriva de D0–D13). Consume, sin modificarlos,
  ADR-15 y ADR-16 (lifecycle y autoridad de cambios DEV).
- Formalizada en: plan 125
  (`docs/plans/125-repository-architecture-decisions.md`), que registra además las
  decisiones humanas A3/B4/F1/L1 y las decisiones abiertas.

## Estado de implementación

Registro de la decisión: **completo** (este ADR + plan 125, docs-only, sin
`VERSION` bump ni tag; RFC-69).

Implementación derivada: **pendiente**, y compuesta por Changes separados:

- Explicitación de la semántica de lifetime/persistence en el contrato Protocol
  (consecuencia de F1) → **efecto payload**, requiere vía RFC-56; no ejecutado ni
  autorizado aquí.
- Cualquier separación física dentro de `.project/` → decisión/Change posterior;
  no iniciada.
- Repository/Artifact Placement Contract → **no diseñado**; downstream de este
  ADR.

Las decisiones de placement abiertas no quedan habilitadas ni resueltas por el
status `Accepted` de este ADR; el status del ADR refleja la decisión registrada,
no el estado de formalización de la implementación.
