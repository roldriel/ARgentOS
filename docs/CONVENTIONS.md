# Convenciones — Repositorio ARgentOS

> Normativa de gobernanza del repo, migrada desde
> `plans/INDEX.md` (sección Convenciones) (RFC-69, Plan A). Los INDEX son
> registro/navegación; esta carta es normativa. La taxonomía documental
> (naturaleza, lifecycle, identidad, referencias) vive en `docs/AGENTS.md`.

## Convenciones

- **Verificación**: la batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de verificación`
  (`python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
  `python -m pytest tests/`, H13 por juicio). `python tools/check_dist_sync.py`
  es local-only y se espera verde solo en `master` (CI no la fetchea);
  `python protocol/.agents/harness/health_check.py` es la sonda del producto
  (adoptantes, modo enforced), no parte de la batería del repo. Los tests del
  harness (`protocol/.agents/harness/tests/`) no corren en la batería del repo:
  son tests del producto, se ejecutan en proyectos adoptantes.
- **Idioma**: inglés en el protocolo (`protocol/.agents/`), en su entry file
  (`protocol/_AGENTS.md`) y en el `AGENTS.md` raíz de desarrollo (es lo que
  leen los agentes), en el código y en los commits (Conventional Commits en
  inglés); español en la documentación de adopción (`docs/ADOPTION.md`,
  `docs/MIGRATION.md`, `CHANGELOG.md`), en `docs/plans/`, `docs/rfc/` y en la
  documentación del tooling (`tools/`, `runtime/`, `docs/` — el código en
  inglés); `README.md` en inglés (público). Los documentos nuevos siguen esta
  regla; los existentes se alinean de forma incremental.
- **Inmutabilidad y clases de cambio (RFC-56)**: `protocol/.agents/` solo se
  modifica por la vía que corresponde a la clase del cambio. **Clase A**
  (modelo conceptual, contratos, breaking): requiere RFC `Accepted`; una RFC
  en `Proposal` NO habilita tocar el payload. **Clase B** (mejora documental
  compatible, sin cambio de significado): plan `Aprobado para ejecución` con
  justificación documentada + batería en verde. **Clase C** (corrección
  mecánica: typos, formato, links; cero cambio de significado): commit directo
  en `dev` con la batería en verde, registrado en el changelog de la próxima
  versión. Reglas de borde: ante la duda se elige la clase más estricta; la
  clase se declara en el plan (A/B) o en el commit (C) y es revisable; la
  batería de verificación corre en las tres clases.
- **Ciclo de status (RFCs)**: `Proposal` (borrador) → `Accepted` (aprobada) →
  `Superseded` (reemplazada; el header indica por cuál RFC). No existe
  `Approved`: los documentos que lo usaban se normalizaron a `Accepted`
  (2 ago 2026).
- **Ciclo de status (planes)**: `Aprobado para redacción` (entregables
  documentales: RFCs, estándares), `Aprobado para ejecución` (entregables de
  implementación o cambios en el repo), `Executed` (todos los criterios de
  salida verificados; si alguno quedó incumplido:
  `Executed (parcial: <qué falta>)`), `Superseded` (reemplazado; indicar por
  qué plan). Todo plan con dependencias abiertas declara su **criterio de
  entrada verificable** (qué archivos/estados deben existir antes de
  ejecutarlo).
- **Ciclo de status (ADRs)**: `Proposal` (decisión en consideración) →
  `Accepted` (decisión adoptada y registrada) → `Superseded` (reemplazada; el
  header indica por cuál ADR). El status del ADR refleja la **decisión
  registrada**, no el estado de formalización de su RFC: la matriz de
  `docs/adr/INDEX.md` muestra cada artefacto con su propio status, y un ADR
  `Accepted` no habilita cambios de payload (la vía sigue siendo RFC `Accepted`
  + plan, RFC-56).
- **Trazas históricas (RFC-46)**: los artefactos de sesión son registros
  inmutables de la versión del protocolo vigente al momento de la sesión; no
  se reescriben ni se "reproducen" con una versión nueva. Las entradas de
  gates previas a 2.0.0 fueron evaluadas por runner (checks machine); las
  posteriores, por juicio del agente contra checklists en prosa. Los contratos
  de sesión declaran `protocol_version` desde 3.4.1.
- **Citas verificables**: toda afirmación sobre el estado actual del repo
  ("hoy X") se ancla a `ruta:sección` (encabezado Markdown) existente al
  momento de la redacción. Prohibidos: rangos aproximados (p. ej. "H01–H13"),
  ordinales ("5ª responsabilidad"), números de línea absolutos sobre archivos
  mutables, y referencias a documentos inexistentes. Criterio de aceptación de
  todo documento nuevo en `docs/plans/` y `docs/rfc/`: cada referencia
  resuelve contra el repo.
- **Plantillas**: todo plan nuevo nace de `docs/plans/_TEMPLATE.md`, toda RFC
  nueva de `docs/rfc/_TEMPLATE.md` y todo ADR nuevo de `docs/adr/_TEMPLATE.md`
  (estructura completa; las secciones marcadas como opcionales pueden omitirse).
  Los templates no se numeran ni se registran en los INDEX; el resto de los
  documentos referencia la estructura, no la duplica. El cumplimiento estructural
  (nombre de archivo, status dentro del ciclo vigente, ausencia de placeholders,
  Amendment Log en RFCs, registro en el INDEX correspondiente) se verifica
  mecánicamente con
  `python tools/check_plan_structure.py`.
- **Amendment log**: toda RFC lleva una sección `## Amendment Log` (fecha →
  qué cambió → origen). Cuando una RFC posterior desfasa a una anterior, la
  anterior recibe además un banner bajo el header:
  `> ⚠ Enmienda pendiente: <qué cambió y dónde está el modelo vigente>`. Este
  log es el único registro de "qué decía antes" para documentos sin historia
  previa.
- **Verificación contra el repo**: los INDEX son registros descriptivos, no
  fuentes de verdad. Todo plan nuevo verifica sus premisas contra `.agents/` y
  git como paso 0, nunca contra los INDEX.
- **Catálogo de gaps**: los "gaps de explicitud" referenciados por los planes
  08–14 están definidos en `docs/plans/analisis-explicitud.md`. Se cita el
  catálogo por ruta; ningún documento referencia IDs de gap que no existan
  allí.
- **Numeración de archivos**: hay tres secuencias independientes y cada una es
  única dentro de su espacio:
  - `docs/rfc/`: solo RFCs, numeración incremental (`00`–`15` existentes — los
    `07`–`15` reservados por el roadmap EC ya fueron asignados a
    RFC-00YE…00YM; los RFCs fuera del roadmap EC numeran a partir de `16`). Un
    implementation plan nunca vive aquí.
  - `docs/plans/` (raíz): solo planes de ejecución, numerados por **orden
    cronológico de ejecución** — esa es la prioridad ante cualquier conflicto.
    `01`–`03` son los implementation plans de los RFCs base (ejecutados 25–26
    jul); `04`–`07` primera serie (Execution Context); `08`–`14` segunda serie
    (explicitud de decisiones); `15`–`20` tercera serie (protocolo operativo),
    mapeada el 28 jul.
  - `docs/adr/`: solo ADRs, numeración incremental (`01`–`14` existentes); la
    identidad estable es `ADR-N` y el archivo es `NN-slug.md`. Un plan o una RFC
    nunca vive aquí.
  - Los identificadores internos de la serie (RFC-00XX … RFC-00YM) se
    mantienen como IDs conceptuales dentro de los documentos; el número de
    archivo es solo orden físico.
- **Versionado**: `docs/plans/` y `docs/rfc/` completos están versionados en
  git (política adoptada el 2 ago 2026; antes figuraba como ignorado pese a
  estar trackeado de facto, y hubo una pérdida y restauración). Los planes
  ejecutados se conservan como traza histórica: no se borran; si quedan
  desfasados se marcan `Superseded`. Lo efímero del proyecto son los artefactos
  de sesión (`.project/`), no los documentos de diseño. `plans/archive/` fue
  eliminado del working tree; su contenido sigue disponible en la historia de
  git.
- **Política de versionado, changelog, tags y estados**: definida en
  `docs/VERSIONING.md`. Resumen: trabajo e integración en `dev` con detalle
  por plan; releases estables solo en `master` vía tags; modelo por plan (cada
  plan ejecutado que toca el payload produce una versión, atada a su RFC);
  invariante versión ↔ changelog ↔ tag; los estados de planes y RFCs cambian
  en el commit del plan y se reflejan en los INDEX.
- **Frontera documental**: `.agents/` (versionado, permanente) no referencia
  `docs/plans/`, `docs/rfc/` ni ADRs. Los conceptos que `.agents/` necesita se
  definen inline, de forma autocontenida. Ningún plan debe instruir referencias
  `.agents/` → `docs/plans/`; la instrucción correcta es siempre "definir el
  concepto inline, sin mencionar la RFC".
- **Layout fuente (RFC-55)**: el payload del producto vive en `protocol/`
  (`protocol/.agents/` + `protocol/_AGENTS.md`); el layout adoptado (`dist`)
  mantiene `.agents/` + `AGENTS.md` en la raíz. Los docs del payload describen
  el layout adoptado; los links a `AGENTS.md` rotos en fuente son intencionales
  y se documentan en `docs/source-layout.md`.

### Change Lifecycle DEV — alcance y frontera

El Change Lifecycle (RFC-75) gobierna la evolución de **ARgentOS DEV**: el
`AGENTS.md` raíz, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, los templates y
los checkers dev. No gobierna automáticamente la evolución del Protocol
(`protocol/.agents/`): un cambio con efecto payload sigue la vía de RFC-56
(clases A/B/C y autorización).

- No se crean workflow/policy/state machine/artifact/skill compartidos entre
  DEV y Protocol; no hay herencia automática.
- Principios potencialmente transferibles (revalidación ante continuidad;
  persistir ≠ materializar; separación entre evidencia factual y autoridad
  normativa) quedan como principios, no como mecanismos
  (`docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).

### Change Lifecycle — Change Levels (modelo objetivo)

- `Level = max(coordination, scope, architectural impact, release impact,
  duration/complexity)`; el número de commits no es dimensión. Los ejes y los
  umbrales coarse (0–3) son decisión de RFC-75
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`); esta carta
  los referencia sin duplicar la tabla.
- Change Level y clase RFC-56 son **ejes independientes**: una Clase A pequeña
  puede ser L2; una Clase C grande puede ser L2/L3 por scope; un cambio
  runtime-only tiene Level sin clase.
- **L0** es el nivel mínimo (1 agente, 1 sesión, superficie de 1 archivo, sin
  cambio estructural, sin versión, <1 sesión) y es **provisional**: al
  activarse un trigger (finding, revalidación requerida, decisión ADR-worthy,
  múltiples RFCs, impacto release-critical o arquitectónico), el Level se
  recomputa antes de continuar
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).
- La maquinaria del lifecycle escala con el Level (CL-10); la matriz operacional
  L0–L3 y el reparto de decisiones viven en el Master Action Plan
  (`docs/plans/94-change-lifecycle-master-action-plan.md:9. Economía de Change Levels`),
  no se duplican aquí.
- La clasificación operacional (registro del Level en el primer artifact del
  cambio / intake fallback) se materializa en el Incremento 1; en esta etapa
  (Incremento 0) queda fijado el modelo, sin exigencia operacional (regla
  transversal, sección siguiente).

### Regla transversal — target semantics vs operationalización

Una regla definida por RFC-75 puede formar parte del modelo normativo objetivo
antes de que exista su mecanismo de enforcement; una regla del lifecycle se
vuelve operacionalmente exigible solo después de que el incremento que
materializa su mecanismo es aceptado
(`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`,
`docs/rfc/75-change-lifecycle.md:Rollout incremental`).

- Mapa de aplicabilidad: VC-1 (toda validación registrada con anchor) →
  Incremento 1; GC-1 (checkpoint para `Closed`) → Incremento 3; LC-1/PC-1
  (lineage de findings / pending decisions) → Incremento 2.
- Ningún incremento anterior invalida artifacts legacy ni impone requisitos sin
  mecanismo; la ausencia de campos nuevos indica legacy, no invalidez
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- El output de un checker es evidencia factual, no autoridad normativa;
  "anchor missing" es un GAP, no una invalidación
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).
