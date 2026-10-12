# Layout del payload fuente y links rotos intencionales

El payload del producto vive en `protocol/` (`protocol/.agents/` +
`protocol/_AGENTS.md`). La rama `dist` lo publica como `.agents/` + `AGENTS.md`
en la raíz del proyecto adoptante.

## Regla general

Los links relativos dentro de `protocol/.agents/` que apuntan a `AGENTS.md`
están **rotos a propósito** en el árbol fuente y **correctos en `dist`**.
**No arreglarlos**: modificarlos altera el payload inmutable (requiere RFC/plan)
y rompería el layout publicado. El checker mapea estas referencias al entry
file fuente (`protocol/_AGENTS.md`) y las considera válidas.

## Inventario exacto

| Archivo (fuente) | Link | Por qué roto en dev/master | Por qué correcto en dist |
| --- | --- | --- | --- |
| `protocol/.agents/standards/conduct/OPERATIONAL_RULES.md` | `[AGENTS.md](../../../AGENTS.md)` | Resuelve a `protocol/AGENTS.md`, que no existe (es `_AGENTS.md`) | Desde `.agents/standards/conduct/` resuelve a la raíz del adoptante, donde `AGENTS.md` existe |
| `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md` | `[AGENTS.md](../../../AGENTS.md)` | Ídem | Ídem |

## Prosa que describe el layout adoptado

Estos textos describen el producto tal como se adopta (`dist`), no el layout
fuente; en fuente, "AGENTS.md" es ambiguo (el de la raíz es el dev).

**Estado tras la release `12.0.0` (reconciliado por RFC-82, plan 156).** La
premisa de esta lista era que el layout adoptado tenía su entrada normativa en
`AGENTS.md` en la raíz, porque `dist` publicaba `AGENTS.md` como entry. Con el
layout canónico de RFC-81 esa premisa dejó de valer: el bootstrap normativo es
`.argentos/.agents/INDEX.md` y el `AGENTS.md` de la raíz es un **adapter no
normativo**. Las dos entradas que afirmaban lo contrario se **corrigieron en el
payload** (autorización: RFC-82 `Accepted`); esta lista registra el estado
vigente y ya no las protege.

Lo que sigue siendo correcto y **no se toca**:

- `protocol/.agents/roles/profiles/tech_writer.md` — mención de `AGENTS.md` sin
  patología: no afirma cuál es la entrada normativa.
- Los links rotos intencionales del inventario de arriba: siguen rotos a
  propósito en fuente y correctos en `dist`.
- Las citas históricas de `docs/plans/` (sección siguiente): son traza
  (RFC-46) y no se reescriben.

La **guarda** de la sección final sigue vigente sin cambios: los links de path al
entry file permanecen restringidos a la allowlist de los dos archivos del
inventario, las menciones en prosa (sin separador de path) están permitidas, y
cualquier excepción futura debe documentarse acá, sumarse a la allowlist y
cubrirse con test antes de mergear.

## Citas históricas de `docs/plans/`

Los planes y RFCs existentes citan `.agents/...` y `AGENTS.md` con rutas del
layout viejo, y `feature.md` (documento de visión que vivió en la raíz hasta
el 12 ago 2026). `check_plan_citations.py` las resuelve con un mapeo legacy
(`.agents/...` → `protocol/.agents/...`, `AGENTS.md` → `protocol/_AGENTS.md`,
`feature.md` → `docs/plans/ec-pipeline-vision.md`).
**No reescribir planes históricos**: son traza.

## Guarda

Si aparece un link nuevo roto en fuente que no apunte al entry file, el checker
lo reporta como violación. Además, los links de path al entry file
(`[AGENTS.md](../../../AGENTS.md)`) están restringidos mecánicamente a la
allowlist de los dos archivos del inventario (`_ENTRY_LINK_ALLOWLIST` en
`tools/check_protocol_invariants.py`): un tercer archivo con ese link es
violación BOUNDARY. Las menciones en prosa (sin separador de path) están
permitidas — son la prosa que describe el layout adoptado. Si un cambio futuro
agrega una excepción, hay que documentarla acá, sumarla a la allowlist y
cubrirla con test antes de mergear.
