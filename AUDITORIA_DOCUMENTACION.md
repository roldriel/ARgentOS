# Auditoría de documentación e instrucciones — ARgentOS

**Fecha:** 2026-08-12

**Alcance:** revisión del repositorio fuente tras la reestructuración
`protocol/` (plan 54, RFC-55), con foco en qué instrucciones y documentación
necesita el workspace para desarrollo sostenido asistido por un agente LLM.

**Método:** inventario de archivos, lectura de la documentación raíz, `dev/`,
`plans/` y `protocol/`, ejecución de los checkers y la suite de tests,
auditoría de links Markdown en la documentación de desarrollo y revisión de
git/CI/versiones.

---

## Veredicto

La reestructuración quedó **sólida y consistente**: la separación
`protocol/` (payload, data) vs. workspace de desarrollo (AGENTS.md raíz) está
bien ejecutada, verificada mecánicamente y publicada. No hay defectos
bloqueantes. Los hallazgos son de **mejora de la operación de desarrollo
asistida por LLM**: cerrar huecos de verificación, concentrar la guía
operativa en el entry point de sesión y actualizar documentos que quedaron
desfasados respecto del estado actual de planes/RFCs.

---

## Estado verificado (evidencia)

| Verificación | Resultado |
| --- | --- |
| `python dev/tools/check_protocol_invariants.py --payload protocol .` | OK — 186 archivos, 7.268 referencias |
| `python dev/tools/check_plan_citations.py` | OK — sin citas `ruta:sección` rotas |
| `python -m pytest protocol/.agents/harness/tests/ dev/runtime/tests/ dev/tools/tests/ -q` | 105 passed |
| Working tree | limpio, en `dev` |
| Versión | `protocol/.agents/VERSION` = 3.0.5; sección en `CHANGELOG.md`; tag `3.0.5` en `master` |
| `dist` | regenerada desde `master` (workflow `publish-dist`) |
| Links Markdown en docs raíz y `dev/` | sin roturas; las únicas referencias "rotas" son las dos intencionales de `protocol/.agents/` documentadas en `dev/source-layout.md` |
| CI (`check-protocol.yml`) | corre invariantes + pytest en push/PR de `protocol/**` y `dev/**` |

---

## Documentación existente (inventario)

| Área | Documentos | Rol |
| --- | --- | --- |
| Instrucciones dev | `AGENTS.md` (raíz) | Entry point de toda sesión de desarrollo; layout, "protocol es data", workflow, verificación |
| Producto | `protocol/.agents/` + `protocol/_AGENTS.md` | Payload distribuible; data, no instrucciones |
| Dev tooling | `dev/README.md`, `dev/ROADMAP.md`, `dev/source-layout.md`, `dev/runtime/README.md` | Mapa del workspace dev, pendientes, layout fuente y links intencionales |
| Gobernanza | `plans/INDEX.md` (55 RFCs + 54 planes), `plans/rfc/`, `feature.md` | Historia de diseño, convenciones, estados, visión del Execution Context Pipeline |
| Release / adopción | `README.md`, `ADOPTION.md`, `MIGRATION.md`, `VERSIONING.md`, `CHANGELOG.md` | Visibilidad pública, onboarding, migración y política de versionado |
| CI | `.github/workflows/check-protocol.yml`, `publish-dist.yml` | Verificación en push/PR y publicación de `dist` |

---

## Hallazgos priorizados

### Alta — afectan directamente la calidad de las sesiones del agente LLM

1. **AGENTS.md raíz declarativo, no operativo.** Contiene el layout y las
   reglas de fondo, pero no el flujo concreto de trabajo: RFC → plan →
   ejecución → changelog → versión, el Definition of Done de una tarea, las
   convenciones de commit/idioma ni una sección de "qué NO hacer" (no tocar
   `protocol/.agents/` sin vía, no arreglar los links intencionales, no
   commitear `.project/`, no editar `dist` a mano). Hoy esa información está
   dispersa entre `plans/INDEX.md` §Convenciones, `VERSIONING.md` §4 y
   `dev/README.md`. Un agente que entra al repo debe leer tres documentos
   para armar el mapa operativo; conviene concentrarlo en el entry point.

   > ✅ **Resuelto (2026-08-12):** `AGENTS.md` raíz incorpora "Task lifecycle"
   > (pipeline autorizar → ejecutar → verificar → cerrar → commit → promover),
   > DoD resumido, sección "Do NOT" y convenciones de idioma/commits, con
   > punteros a `VERSIONING.md` §4/§10 y `plans/INDEX.md` §Convenciones como
   > fuentes de verdad.

2. **CI incompleto: no valida citas de planes ni docs raíz.**
   `check-protocol.yml` corre `check_protocol_invariants.py` y pytest, pero
   **no ejecuta `check_plan_citations.py`** y sus paths de trigger no
   incluyen `plans/**`. Un PR que rompa citas de planes pasa CI sin
   detección. Acción: agregar el paso al workflow y sumar `plans/**` a los
   paths.

   > ✅ **Resuelto (2026-08-12, superado):** CI corre la batería completa
   > (invariantes + `check_plan_citations.py` + `check_plan_structure.py` +
   > pytest) y se **eliminaron los path filters**: el workflow corre en todo
   > push/PR, con lo que la clase de problema "path no declarado" desaparece.

3. **Sin verificación mecánica de links en la documentación raíz y `dev/`.**
   Los checkers cubren solo `protocol/.agents/` y `plans/`. README,
   ADOPTION, MIGRATION, VERSIONING, CHANGELOG y los docs de `dev/` pueden
   acumular links rotos sin que nada lo detecte (hoy están sanos, pero sin
   protección). Acción: checker liviano (p. ej. `dev/tools/check_root_docs.py`)
   + paso en CI.

   > 🟡 **Resuelto parcial (2026-08-12):** en lugar de un checker nuevo,
   > `check_plan_citations.py` se extendió para escanear como fuentes los docs
   > raíz canónicos (AGENTS, README, ROADMAP, VERSIONING, CHANGELOG, MIGRATION,
   > ADOPTION) más `runtime/README.md` y `docs/source-layout.md`, y corre en
   > CI. Las **citas `ruta:sección`** quedan verificadas; los **links Markdown
   > genéricos** (`[x](foo.md)`) en esos docs siguen sin verificación — se
   > evalúa debajo si amerita checker propio.

### Media — reducen fricción y evitan trabajo duplicado

4. **`dev/ROADMAP.md` desactualizado.** La tabla de pendientes (B-1…B-8) no
   refleja que casi todos los ítems ya tienen su par RFC + plan redactado
   (B-1 → planes 40/47, B-2 → planes 29/33, B-3 → plan 50, B-4 → planes
   37-43/53, B-5 → plan 44, B-6 → plan 46, B-7 → planes 29/43/52, B-8 → plan
   49). Un agente puede re-planificar trabajo ya planificado. Acción: columna
   "Cubierto por" con links y estados.

   > ✅ **Resuelto (2026-08-12):** `ROADMAP.md` (movido a la raíz) tiene la
   > columna "Cubierto por" con el mapeo a planes, referenciando estados en
   > `plans/INDEX.md` sin duplicarlos.

5. **Faltan plantillas formales de plan y RFC.** La estructura es consistente
   de facto (planes: Status / RFC / Criterio de entrada / Objetivo /
   Entregables / Verificación / Nota de ejecución; RFCs: Pregunta / Problema /
   Modelo / Alcance / Amendment Log). Un `plans/_TEMPLATE.md` y
   `plans/rfc/_TEMPLATE.md` haría que los documentos nuevos nazcan conformes,
   respetando la convención single-source (el resto linkea, no duplica).

   > ✅ **Resuelto (2026-08-12, superado):** creados ambos templates
   > (estructura completa, guías en comentarios HTML, notas anti-implícito de
   > numeración/nombre/espejo en INDEX), más el checker
   > `tools/check_plan_structure.py` que hace cumplir mecánicamente la
   > estructura (status, placeholders, Amendment Log, espejo en INDEX) sobre
   > los 110 documentos numerados, con 29 tests y corrida en CI.

6. **`plans/INDEX.md` con snapshot desfasado.** Dice "Estado al 2026-08-11" y
   describe la sexta serie como trabajo activo; el estado real al cierre es:
   RFC-55 Accepted, RFC-32…54 redactadas en `Proposal` (planes en `Aprobado
   para redacción`/`Executed` según el caso) y el siguiente paso es la
   aceptación de RFCs y ejecución. También queda pendiente la referencia de
   RFC-42 en `protocol/.agents/standards/conduct/ANTI_CIRCUMVENTION.md`
   (verificada: el archivo no contiene la referencia de gobernanza).

   > 🟡 **Parcial (2026-08-12):** snapshot del encabezado de `plans/INDEX.md`
   > actualizado al estado real del 12 ago 2026 (serie de remediación cerrada
   > en redacción, RFC-55 ejecutada, remediación documental completada).
   > **Queda** la referencia de RFC-42 en
   > `protocol/.agents/standards/conduct/ANTI_CIRCUMVENTION.md`: toca el
   > payload y requiere vía (RFC Accepted o plan aprobado).

7. **Sin verificación local de `dist`.** No hay forma documentada de
   comprobar localmente que `dist` está sincronizada con `protocol/`; hoy
   depende del workflow `publish-dist`. Acción: script
   `dev/tools/check_dist_sync.py` o sección con el comando de comparación en
   `dev/README.md`.

   > ✅ **Resuelto (2026-08-12):** `tools/check_dist_sync.py` compara el
   > payload commiteado (blobs de `HEAD`, inmune a CRLF/autocrlf) contra la
   > rama `dist` local: layout, contenido byte a byte y archivos extra. 7
   > tests; cableado a la batería local (no a CI: el checkout no fetchea
   > `dist`).

### Baja — higiene y cierre de cabos

8. **Carpetas vacías `docs/` y `tests/` en la raíz.** No están trackeadas por
   git y confunden (parecen destinos oficiales). Los tests viven en
   `dev/**/tests/` y `protocol/.agents/harness/tests/`. Acción: borrarlas o
   darles propósito y documentarlas en el layout de `AGENTS.md`.

   > ✅ **Resuelto (2026-08-12, por la vía de darles propósito):** `tests/`
   > centraliza las suites de `tools/` y `runtime/` (con `tests/AGENTS.md`
   > propio) y `docs/` aloja `source-layout.md`. Ambas documentadas en el
   > layout del AGENTS.md raíz.

9. **Rama local stale `feature/orchestrators-domain-restructure`.** Puede
   confundir a un agente que la tome como trabajo activo. Acción: borrarla o
   marcarla como obsoleta.

   > ✅ **Resuelto (2026-08-12):** rama local eliminada con autorización del
   > usuario (estaba solo en local; último commit `fce4a83`).

10. **Faltan `LICENSE` y sección `[Unreleased]` en `CHANGELOG.md`.** La
    sección Unreleased está prevista por `VERSIONING.md` §8 para ejecución en
    paralelo; crearla evita fricción cuando haya varios planes en vuelo.

    > ✅ **Resuelto (2026-08-12):** `[Unreleased]` creada en `CHANGELOG.md` y
    > `LICENSE` MIT agregada (decisión del usuario), con sección License en
    > `README.md`.

11. **Nota de ejecución del plan 54 desfasada.** Dice "promoción a `master` +
    tags + `publish-dist` pendientes", pero `VERSIONING.md` §9 registra que la
    promoción, los tags 3.0.2–3.0.5 y la regeneración de `dist` se ejecutaron
    el 12 ago 2026. Los planes son traza histórica (no se reescriben), pero
    una línea de cierre evitaría lecturas ambiguas.

    > ✅ **Resuelto (2026-08-12):** línea de cierre agregada a la Nota de
    > ejecución del plan 54 (promoción, tags y `dist` registrados en
    > `VERSIONING.md` §9), sin reescribir la traza original.

---

## Qué haría más fácil el trabajo del agente LLM

1. **AGENTS.md raíz operativo** (flujo de contribución, DoD, convenciones,
   anti-reglas): es lo primero que lee cada sesión; concentrar la guía reduce
   contexto consumido y errores de procedimiento.
2. **CI que valide la cadena completa**: citas de planes + invariantes +
   tests + links de docs raíz. Convierte la documentación en algo verificable
   y evita que un agente introduzca regresiones silenciosas.
3. **Plantillas de plan/RFC**: documentos nuevos conformes sin adivinar
   estructura ni status.
4. **Roadmap vivo** (columna "Cubierto por" + estados): evita re-planificar
   lo ya planificado.
5. **Chequeo local de `dist`**: detecta drift del artefacto publicado sin
   depender del CI.

---

## Próximos pasos sugeridos

1. Extender `check-protocol.yml`: correr `check_plan_citations.py` y agregar
   `plans/**` a los paths.
2. Crear `dev/tools/check_root_docs.py` (links de docs raíz + `dev/`) e
   integrarlo al CI.
3. Reescribir/ampliar `AGENTS.md` raíz con el flujo operativo completo.
4. Actualizar `dev/ROADMAP.md` y el encabezado/estado de `plans/INDEX.md`.
5. Agregar plantillas de plan y RFC en `plans/`.
6. Higiene: borrar `docs/` y `tests/` vacías (o darles propósito), borrar la
   rama stale, agregar `LICENSE` y `[Unreleased]` en el changelog.

---

**Nota:** este documento es un informe de auditoría, no un plan de ejecución.
Los cambios que toquen `protocol/.agents/` requieren su vía de autorización
habitual (RFC Accepted o plan aprobado); las mejoras documentales de la raíz
y `dev/` no requieren RFC.

---

## Estado de remediación (2026-08-12, actualización posterior a la auditoría)

Resueltos: **1, 2, 4, 5, 7, 8, 9, 10, 11** (el 2 y el 5 superados: CI sin path
filters con batería completa; templates + enforcement mecánico). Parcial:
**3** (citas de docs raíz verificadas; links Markdown genéricos sin checker).
Pendiente: **6** (snapshot del INDEX + referencia RFC-42 en el payload, que
requiere vía).

Trabajo adicional de la misma tanda, fuera del alcance original: consolidación
de tests en `tests/` (con `tests/AGENTS.md`), disolución de `dev/` (`tools/`,
`runtime/`, `docs/` en raíz), eliminación de path filters de CI, extensión del
checker de citas a docs raíz y componentes, y guarda mecánica de los links
intencionales (`_ENTRY_LINK_ALLOWLIST`).

### Análisis de los pendientes

- **4 (ROADMAP "Cubierto por")** — Valor alto, esfuerzo bajo: es una columna
  con mapeo ya enumerado en este mismo informe. Riesgo: duplicar estados que
  viven en `plans/INDEX.md`; conviene referenciar, no copiar.
- **6 (snapshot del INDEX + referencia RFC-42)** — Dos mitades: el snapshot
  del INDEX es documental y trivial; la referencia en `ANTI_CIRCUMVENTION.md`
  toca el payload y **requiere vía** (plan aprobado). Conviene separarlas.
- **7 (verificación local de dist)** — Valor medio, esfuerzo medio: script
  `tools/check_dist_sync.py` que compare `dist` contra `protocol/` (layout +
  entry file + VERSION). Simple porque `dist` es derivada.
- **9 (rama stale)** — Trivial pero destructiva; requiere decisión del
  usuario. Existe solo localmente.
- **10 (LICENSE + Unreleased)** — `[Unreleased]` es trivial; LICENSE es
  decisión de licenciamiento del usuario, no documental.
- **11 (nota plan 54)** — Trivial: una línea de cierre sin reescribir la
  traza.
- **3 residual (links genéricos en docs raíz)** — Evaluar si el riesgo lo
  justifica: los docs raíz tienen pocos links Markdown y cambian poco. Si se
  implementa, es un checker liviano en `tools/` reutilizando la extracción de
  `check_protocol_invariants.py`.
