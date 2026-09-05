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
  - `docs/rfc/`: solo RFCs, numeración incremental (`00`–`75` existentes; los
    `07`–`15` reservados por el roadmap EC ya fueron asignados a
    RFC-00YE…00YM y los RFCs fuera del roadmap EC numeran desde `16`). Un
    implementation plan nunca vive aquí.
  - `docs/plans/` (raíz): solo planes de ejecución, numerados por **orden
    cronológico de ejecución** — esa es la prioridad ante cualquier conflicto.
    `01`–`03` son los implementation plans de los RFCs base (ejecutados 25–26
    jul); `04`–`07` primera serie (Execution Context); `08`–`14` segunda serie
    (explicitud de decisiones); `15`–`20` tercera serie (protocolo operativo),
    mapeada el 28 jul.
  - `docs/adr/`: solo ADRs, numeración incremental (`01`–`16` existentes;
    ADR-01…ADR-14 ↔ D0–D13 y ADR-15/16 del Change Lifecycle DEV); la identidad
    estable es `ADR-N` y el archivo es `NN-slug.md`. Un plan o una RFC nunca
    vive aquí.
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
- **Frontera documental (Producto)**: en el layout del Producto (`.agents/`
  adoptado en `dist`; `protocol/.agents/` como data en fuente), `.agents/`
  (versionado, permanente) no referencia `docs/plans/`, `docs/rfc/` ni ADRs.
  Los conceptos que `.agents/` necesita se definen inline, de forma
  autocontenida. Ningún plan debe instruir referencias `.agents/` →
  `docs/plans/`; la instrucción correcta es siempre "definir el concepto
  inline, sin mencionar la RFC".
- **Frontera operacional (DEV)**: `.agents/` en la raíz del repo fuente es la
  capa operacional del agente DEV (Plan 101): instrucciones de operación del
  Change Lifecycle que referencian la autoridad de `docs/` sin duplicarla ni
  reemplazarla. No crea autoridad normativa nueva, no es fuente superior de
  verdad y no importa mecanismos del Producto (`protocol/.agents/` es data de
  otro dominio; RFC-75 `docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).
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
- `.agents/` (raíz) es la interfaz operacional del agente DEV para ejecutar el
  Change Lifecycle: la operación vive ahí, la autoridad/historia en `docs/`
  (RFC/ADR/Plan) y la verificación determinista en `tools/`. La capa no se
  convierte en gobernanza ni en fuente superior de verdad.
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
  cambio / intake fallback) está vigente desde el Incremento 1 (plan 96): todo
  Plan nuevo declara su Change Level en el header; la regla operacional de
  intake y clasificación se define en la subsección «Change Lifecycle — Intake
  y clasificación (regla operacional; Incremento 1)» de esta misma sección.

### Regla transversal — target semantics vs operationalización

Una regla definida por RFC-75 puede formar parte del modelo normativo objetivo
antes de que exista su mecanismo de enforcement; una regla del lifecycle se
vuelve operacionalmente exigible solo después de que el incremento que
materializa su mecanismo es aceptado
(`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`,
`docs/rfc/75-change-lifecycle.md:Rollout incremental`).

- Mapa de aplicabilidad: VC-1 (toda validación registrada con anchor) y GC-1
  (checkpoint para `Closed`) quedaron materializados por el Incremento 1+3
  (Unidad B, plan 96); LC-1 (lineage de findings/corrections con refs
  calificadas) y PC-1 (persistencia de pending decisions bloqueantes) quedaron
  materializados por el Incremento 2 (Unidad C, plan 97). Los cuatro son
  operacionalmente exigibles para artifacts nuevos; los artifacts previos son
  legacy y no se reescriben.
- Ningún incremento anterior invalida artifacts legacy ni impone requisitos sin
  mecanismo; la ausencia de campos nuevos indica legacy, no invalidez
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- El output de un checker es evidencia factual, no autoridad normativa;
  "anchor missing" es un GAP, no una invalidación
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

### Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)

Todo cambio declara su clasificación en el **primer artifact del cambio**
cuando no existe tracker de origen (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).
Reglas operativas:

- El artifact principal de clasificación es el **Plan**: el header declara
  `**Change Level:**` (L0–L3). Origen/tipo, clase RFC-56, scope, riesgo y
  coordinación se declaran en los campos y secciones existentes (`Origen`,
  `Clase`, `RFC`, `Depende de`, alcance y riesgos del cuerpo).
- Cuando la RFC es el primer artifact del cambio, su header puede declarar el
  Change Level de forma **opcional** (intake fallback); al crearse el Plan, el
  nivel del Plan es la declaración vigente y puede corregir la provisional.
- Para cambios sin Plan (Clase C / acción directa), la clasificación se
  registra en el mensaje de commit y/o en la Nota correspondiente, con el
  formato de Conventional Commits existente.
- `Level = max(coordination, scope, architectural impact, release impact,
  duration/complexity)` (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`);
  el número de commits no es dimensión; Change Level y clase RFC-56 son ejes
  independientes.
- **L0 es provisional**: al activarse un trigger (finding, revalidación
  requerida, decisión ADR-worthy, múltiples RFCs, impacto release-critical o
  arquitectónico), el Level se recomputa antes de continuar; si el cambio deja
  de ser L0, pasa por la vía de Plan correspondiente.
- La clasificación es mutable: upgrade obligatorio al descubrir complejidad;
  downgrade con justificación documentada en el artifact que la posee.
- No existe entidad `Change`, ni tracker obligatorio, ni workflow de intake
  paralelo: el fallback es solo el registro en el primer artifact.

### Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)

**Validación registrada**: toda validación citada como evidencia en un artifact
de gobernanza DEV (resultado PASS/FAIL de checkers, pytest o juicio H13 en una
Nota de ejecución, en una ronda de auditoría de una RFC o en el cierre de un
Plan) debe poder anclarse a un estado reproducible (CL-1/VC-1).

El **Validation Anchor** se registra en el artifact que posee la validación:
sección `## Validation anchor` del Plan (template) o entrada del
`## Amendment Log` de una RFC. Campos (RFC-75
`docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`; formato v1
del Plan 96, `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:12. Modelo de anchor (formato v1)`):

- Declared scope (qué afirma cubrir la validación).
- Validation command-set (comandos exactos ejecutados).
- Effective inputs (repo content) (qué contenido del repo consume el
  command-set).
- Observed dependencies (cuando exista instrumentación; si no, `no
  instrumentado`).
- Environmental factors (inputs fuera del repo consumidos y declarados).
- Scoped Content Identity (identidad semántica del contenido evaluado).
- Validity / stale (aplicabilidad actual del anchor).

Distinciones obligatorias:

- Metadata (fecha/autor/sesión, ID local del artifact) no forma parte de la
  identidad semántica.
- Locator (commit SHA, path) localiza un estado u objeto; **nunca** es identidad
  semántica.
- Identidad semántica = Scoped Content Identity (algoritmo abajo).
- `anchor changed ≠ semantic validity changed` (CL-2): la validez de una
  validación es relativa al estado identificado por su anchor (V1 es vigente
  para S1). Si aparece un estado posterior S2 con cambios relevantes para el
  contrato y no existe una revalidación aplicable, V1 **no es evidencia de
  validación para S2**: se marca `stale` respecto de S2 y, antes de `Closed`,
  debe existir una revalidación PASS sobre S2. Ningún cambio del repo invalida
  automáticamente una validación: aplican los límites de aplicabilidad y de
  factores no declarados (CL-2; RFC-75 Mecanismo 6).
- Límite declarado: dependencias ambientales desconocidas nunca detectadas no
  son verificables por el lifecycle; es responsabilidad del autor de la
  validación y la revalidación es el backstop (RFC-75 Mecanismo 6).

**Revalidación (mismo contrato, estado nuevo).** Una revalidación es la
re-ejecución de un **mismo contrato de validación** sobre un nuevo estado Git
relevante (S2) cuando cambió el estado scoped del contrato (CL-2/GC-1). Es una
**validación registrada**: produce un resultado propio y un **Validation Anchor
propio (A2)** sobre S2. Propiedades:

- A2 puede referenciar A1 como origen de la cadena (lineage), pero **no
  reemplaza ni muta A1**: A1 conserva su significado histórico (valida S1) y
  nunca se reescribe ni se reinterpreta retrospectivamente. La cadena es
  histórica (`A1 → A2`), no una mutación (`A1 becomes A2`).
- **Registro mínimo de una revalidación (A2):** referencia al anchor original
  (A1), estado revalidado (locator + nueva Scoped Content Identity),
  command-set (puede referenciar el de A1 cuando es idéntico, sin duplicarlo),
  cambios relevantes de factores ambientales (con confirmación de que los
  demás permanecen sin cambio) y resultado de la revalidación. Los campos del
  contrato no modificados se heredan de A1 por referencia.
- La re-ejecución sobre el mismo estado (sin cambio scoped relevante) se
  registra como nota de la misma validación, sin crear A2; la nota no modifica
  el significado de A1.
- No existe entidad, registry ni state machine de revalidación: es una relación
  de evidencia entre validaciones del mismo contrato; el lineage formal con
  refs calificadas está operativo desde el Incremento 2 (Unidad C, plan 97;
  ver «Change Lifecycle — Findings y correcciones (regla operacional; LC-1,
  Incremento 2)» en esta sección; RFC-75
  `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`).

**Scoped Content Identity (algoritmo v1)** — identidad de contenido
determinista sobre los effective inputs repo
(`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:13. Scoped Content Identity (algoritmo v1)`):

- Primitivas Git ya usadas por los checkers: `git ls-files -s`,
  `git hash-object --path=<path> <path>`, `git write-tree`,
  `git rev-parse <commit>^{tree}` y `git ls-tree`.
- **Delta scoped identity**: para el scope set `S` (paths repo-relative
  ordenados), blob id por path (index tras `git add`, o `git hash-object`) y
  `sha256` de la serialización canónica `scoped-v1` + pares
  `path <0x00> blob <0x00>`.
- **State identity**: cuando el command-set consume el repo completo (p. ej.,
  la batería canónica), tree id de `git write-tree` sobre el estado staged; los
  tree objects de git son content-addressed: contenido idéntico → tree id
  idéntico, independiente de la historia.
- Rebase/cherry-pick/amend con contenido scoped idéntico no invalida la
  identidad; contenido distinto → evaluar aplicabilidad / revalidar (stale).
- Un cambio fuera del scope no altera el delta identity; el tree id puede
  cambiar → evaluación de aplicabilidad (CL-2), no invalidación automática.

### Change Lifecycle — Serie e identidad derivada (regla operacional; Incremento 1)

- La serie es identidad **derivada**: `Serie(RFC)` = declaración `Serie:` del
  header; `Serie(Plan)` = declaración propia si existe, ∪ series de la(s)
  RFC(s) referenciada(s) en su campo `RFC` (relación verificable RFC↔Plan).
- La coincidencia textual aislada no basta: la membresía exige la relación
  RFC↔Plan resuelta y la coherencia de los artifacts (INDEX espejo).
- Sin entidad ni registry de series; INDEX = vista descriptiva, nunca
  autoritativa (AU-4, ADR-16).
- La identidad es repo-scoped, derivada y estable: renombrado con historia;
  supersession de miembros no disuelve la serie; legacy sin declaración no es
  inválido.
- Las secciones "Vigésima X serie" del INDEX de planes son la vista descriptiva
  de batches de planes (numeración/registro), un eje distinto de la serie
  conceptual `Serie:`; ninguna es autoritativa.

### Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)

- **Checkpoint** = relación closure↔estado Git verificable (RFC-75
  `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`); no es un
  artifact, no es "tener un commit" y no es el SHA.
- Registro del checkpoint en la sección de cierre/Nota del Plan al cerrar:
  commits de cierre (lista; multi-commit), estado validado (ref al anchor),
  estado de cierre (tree id), consistencia, governance aplicada y condición
  derivada.
- **Consistencia checkpoint↔anchor (GC-1)**: `Closed` exige que la identidad
  scoped del estado de cierre sea igual a la del anchor **de la validación cuyo
  estado validado corresponde al estado de cierre** y que los factores
  ambientales declarados no hayan cambiado; si difiere cualquiera →
  **revalidación antes de `Closed`**. Si existe una revalidación A2 sobre el
  estado de cierre, la consistencia se evalúa contra A2; si el estado de cierre
  sigue siendo el estado de A1, contra A1. La existencia de A2 no elimina A1.
  Factores irrelevantes (no consumidos) y desconocidos no invalidan
  automáticamente; un factor relevante consumido pero no declarado es una
  anomalía auditable.
- `Closed` = `Executed` + governance aplicable + checkpoint + consistencia +
  evidencia de validación PASS para el estado de cierre (condición derivada, no
  status). Si el estado de cierre difiere del estado validado inicialmente, esa
  evidencia es una revalidación PASS anclada al estado de cierre (A2). `Closed`
  no deriva de `Committed` ni de "HEAD == commit esperado": el commit es
  evidencia factual, no la condición. `Committed` = estado del repositorio, no
  status de Plan. `Closed ≠ Released`; un Plan docs-only se cierra sin release
  (RFC-69).
- Multi-commit: el checkpoint lista todos los commits del Plan y la
  consistencia se evalúa sobre el estado validado (con revalidación si el
  estado de cierre difiere). Multi-RFC: la governance aplica por RFC
  (Amendment Log cuando corresponda). Multi-Plan: cada Plan cierra con su
  propio checkpoint; sin registry.
- Cambios posteriores al cierre no invalidan el checkpoint: generan artifacts
  nuevos que referencian al cerrado (RFC-46; RFC-75
  `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes`).
- Relación temporal acíclica: `state → validation → validation evidence
  (anchor) → closure/checkpoint → derivación de Closed`. El anchor describe la
  validación realizada sobre un estado Git; el checkpoint relaciona
  posteriormente el closure con ese estado; `Closed` nunca es prerrequisito de
  un anchor ni de una revalidación.

### Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)

**Finding (registro factual en su artifact).** Un finding es una relación de
lineage (origin → observation → correction → revalidation → result) registrada
en el artifact que la detecta/posee; no existe entidad arquitectónica `Finding`
(RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`).
Para artifacts nuevos:

- Formato: ref calificada `<artifact>:F-<n>`; el namespace pertenece al
  artifact del registro. No existe namespace ni registry global; el número es
  locator del registro, nunca autoridad normativa (ADR-16 AU-4/AU-5). Refs
  cross-artifact son posibles y legítimas.
- Elementos inmutables del finding: identidad (ref), observación original,
  evidencia original (ref a validación/anchor, estado Git y cita
  `ruta:sección` cuando aplique), estado Git donde fue observado y provenance
  original. No se reescriben ni se reinterpretan retrospectivamente (CL-8;
  RFC-46).
- La metadata de lifecycle (estado y resolución) puede evolucionar preservando
  el histórico de transiciones. Estados válidos: `open`,
  `partially-resolved`, `resolved`, `deferred` (con owner/destino) y
  `superseded` (sustituido/duplicado; ≠ `resolved`; nunca borrado silencioso).
  Reapertura: finding nuevo que referencia al original **o** metadata/historial
  `reopened` (ambas permitidas). El mecanismo concreto de preservación del
  histórico (metadata actual con histórico, append-only u otra representación
  compatible) es decisión de implementación del artifact, sin contradecir
  CL-8.
- Cardinalidades N:M: 1 finding → N corrections; N findings → 1 correction;
  1 correction → N revalidaciones.
- Un finding sobre un artifact cerrado se registra en un artifact nuevo con ref
  al cerrado (post-close por referencia; RFC-75
  `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes`); el
  artifact cerrado no se reabre.
- Los `F-xx` bare de bitácoras/auditorías históricas (bitácora del plan 19,
  auditorías F1–F7, backlog) son namespaces distintos y legítimos; no se
  migran ni se mezclan con el lineage lifecycle.

**Correction (registro de provenance).** La acción de corregir está autorizada
normativamente por el Plan aprobado (o por la vía RFC-56 / Clase C según
corresponda); el registro `C-<n>` documenta la corrección realizada y es
**FACTUAL / TRACEABILITY**, no una fuente normativa. Para artifacts nuevos:

- Formato: `<artifact>:C-<n>`, namespace del artifact que posee el registro;
  sin registry global; el número no otorga autoridad.
- Toda corrección preserva provenance hacia su origen/finding y declara su
  **alcance de revalidación** (CL-6); el resultado de la revalidación es
  trazable a la corrección y a su origen (CL-7).
- Cadena cuando corresponde: finding → correction → estado posterior S2 →
  revalidación V2 (anchor A2) → evidencia → resolución/elegibilidad de cierre.
  No toda corrección requiere revalidación (solo si cambia el estado scoped
  relevante; CL-2 + Decisión B) y no toda revalidación requiere finding.
- La resolución de un finding (`resolved`/`partially-resolved`/`deferred`/
  `superseded`) es decisión humana con evidencia (CL-8; ADR-16 AU-3); el
  agente detecta, registra, propone y escala, no resuelve unilateralmente.
- Corrections y findings se registran en el artifact que los posee; no existe
  entidad global de Correction ni de Finding.

### Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)

**Pending** es una decisión pendiente registrada en el **artifact que posee la
decisión** (el que requiere la resolución), con refs a los artifacts
bloqueados; no es un lifecycle state global, no es un finding ni un checker
output, y no existe entidad `Decision` (RFC-75
`docs/rfc/75-change-lifecycle.md:Mecanismo 9 — Pending Decisions`). Para
artifacts nuevos:

- Metadata requerida: `blocking/no-blocking`, `owner`, `escalación`,
  `resolución`, `evidencia`, `efecto downstream` y `ADR-worthiness`.
- **PC-1**: toda decisión pendiente **bloqueante** persiste en el artifact que
  bloquea; nunca desaparece. Las no-bloqueantes se registran con su metadata;
  no todo pending es bloqueante.
- Ownership: si el owner se supersede/elimina/cierra → transferir al sucesor o
  escalar al humano; si dos artifacts reclaman ownership → el humano decide con
  refs a todos los reclamantes (AU-3).
- La determinación de blocking/materialidad es decisión humana cuando la
  normativa la requiere (ADR-16 AU-3; Plan 94 §8); la resolución se registra
  con decisión + evidencia + artifacts afectados en el artifact dueño y en el
  registro del pendiente.
- No confundir modelos: **Pending** (decisión per-artifact) ≠ **finding open**
  (estado de metadata de un finding) ≠ **Warning** (salida informativa de
  checkers) ≠ **GAP** (evidencia faltante; no invalidación, RFC-75 Mecanismo
  14) ≠ **FAIL** (violación mecánica) ≠ **Observation** (finding no bloqueante
  registrado como observación).
- Implicación operacional (derivada de PC-1 + matriz de governance, no regla
  nueva): al intentar derivar `Closed`, los findings deben estar resueltos o
  diferidos con destino/ownership y no debe existir pending bloqueante sin
  resolución ni escalación con dueño.
