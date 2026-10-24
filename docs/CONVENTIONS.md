# Convenciones — Repositorio ARgentOS

> Normativa de gobernanza del repo, migrada desde la sección Convenciones de
> `docs/plans/INDEX.md` (RFC-69, Plan A). Los INDEX son
> registro/navegación; esta carta es normativa. La taxonomía documental
> (naturaleza, lifecycle, identidad, referencias) vive en `docs/AGENTS.md`.

## Convenciones

- **Verificación**: la batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de verificación`
  (`python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
  `python tools/check_taxonomy_coherence.py`, `python tools/check_session_artifacts.py`,
  `python tools/check_version_state.py`, `python -m pytest tests/`, H13 por
  juicio). `python tools/check_dist_sync.py`
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
- **Inmutabilidad y clasificación de cambios del payload (RFC-56)**: `protocol/.agents/`
  solo se modifica por la vía que corresponde a la **clase RFC-56 del payload delta**
  (`docs/rfc/56-governance-fast-track.md:Modelo vigente (enmienda 2026-10-23)`).
  La clasificación pertenece al **payload delta**, no al Change, al Plan ni al documento
  que lo describe; un Change puede contener **cero, uno o varios** payload deltas con
  clases distintas.
  - **Clase A** (modelo conceptual, contratos, breaking): RFC `Accepted` + Plan
    `Aprobado para ejecución`; una RFC en `Proposal` NO habilita tocar el payload.
  - **Clase B** (mejora documental compatible **del payload**, sin cambio de
    significado): Plan `Aprobado para ejecución` con justificación documentada +
    batería en verde.
  - **Clase C** (transformación mecánica del payload que **preserva la semántica
    normativa y los contratos del payload**): commit directo en `dev` con la batería
    en verde, registrado en el changelog de la próxima versión, cuando la ruta directa
    es aplicable.
  - **Ruta efectiva**: la fija la **clase más estricta presente**, `A > B > C > N/A`.
    No existe una clase `AB`; un delta C puede viajar en el mismo Plan que deltas A/B;
    no se divide artificialmente el Change para evitar la composición.
  - **RFC-56 N/A**: un Change sin efecto sobre `protocol/.agents/` no tiene clase
    A/B/C; su governance es el lifecycle DEV y el Change Level. Clase B **no** es
    sinónimo de «cambio documental» en general.
  - **Reglas de borde**: ante la duda se elige la clase más estricta; el checker es
    **evidencia factual, no autoridad** (un checker que no cambia no demuestra por sí
    solo que el cambio sea C, y uno que cambia no lo vuelve A/B por sí solo); la clase
    se declara en el Plan (`**RFC-56 Class:**`) o en el commit y es revisable; la
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
  `Accepted` no habilita cambios de payload (la vía la fija la clase RFC-56 del
  payload delta: A exige RFC `Accepted` + plan; B, plan; C, commit directo cuando
  la ruta directa aplica).
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
  de sesión (`.project/`), no los documentos de diseño. `plans/archive/`
  (hoy `docs/plans/archive/`) fue
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
  (`protocol/.agents/` + `protocol/_AGENTS.md`); la rama `dist` contiene el
  payload en su propia raíz (`.agents/` + `AGENTS.md`). El layout adoptado
  materializa el payload bajo `.argentos/.agents/` y deja en la raíz del
  proyecto solo el adapter `AGENTS.md` que apunta a
  `.argentos/.agents/INDEX.md`. Los docs del payload usan rutas ancladas al
  payload (`.agents/...`); los links a `AGENTS.md` rotos en fuente son
  intencionales y se documentan en `docs/source-layout.md`.

### Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)

Decisiones humanas del mantenedor aprobadas el 2026-09-05 (D1–D5 del
«Terminology Architecture Decision Report»; ejecutadas por el Plan 105). Esta
subsección es la regla operacional; el registro descriptivo vive en
`docs/glossary/`.

- **Vocabularios DEV/Protocol separados + puente descriptivo (D1).** DEV y
  Protocol mantienen vocabularios propios con sus definiciones normativas
  vigentes; no existe vocabulario global normativo. `docs/glossary/` es el
  puente **descriptivo** entre ambos: registra término → scope → status →
  autoridad; no redefine conceptos y no es fuente normativa. El payload del
  Protocol no referencia `docs/glossary/` (boundary DEV/Protocol).
- **Glosario descriptivo (D2).** `docs/glossary/INDEX.md` +
  `docs/glossary/terms.md` son registro/inventario descriptivo (clase
  Inventory/registro; `docs/AGENTS.md:Folder → class map`). Prohibido
  duplicar definiciones normativas; cada entrada exige `Authority Reference`
  (`ruta:sección`) resoluble. El glosario nunca prevalece sobre una
  RFC/ADR/estándar.
- **Convención AGENTS/INDEX/ENTRYPOINT (D3).** Se preserva la arquitectura
  actual: `AGENTS.md` = instrucciones de agente por capa; el INDEX del
  Protocol (`protocol/.agents/INDEX.md`) = bootstrap + navegación (no se
  renombra); los INDEX de `docs/` e internos = registro/navegación (nunca
  autoridad, AU-4); `ENTRYPOINT.md` = contrato de discovery existente (no
  convención de capa). No se introduce `.agents/ENTRYPOINT.md` ni
  `BOOTSTRAP.md` sin nueva decisión.
- **Regla SCI (D4).** Nombres completos preferentes en todo texto nuevo:
  `Scoped Content Identity` (DEV) y `SemanticContextIdentity` (Protocol).
  `SCI` desnudo prohibido en texto cross-layer nuevo; primera aparición
  expandida; calificación de capa obligatoria ante ambigüedad
  (`SCI (DEV)` / `SCI (Protocol)`). No se renombra ninguna identidad; los
  históricos no se reescriben (RFC-46).
- **Calificación de términos overloaded (D5).** En contexto cross-layer o
  ambiguo, el término debe calificarse. Formas canónicas: `DEV Plan` /
  `EXECUTION_PLAN artifact`; `Validation Anchor` / `composition anchor`;
  `product payload` / `delegation payload` / `materialization payload`;
  `execution (iteration)` / `capability execution` / `EXECUTING state`;
  `lifecycle finding` / `architecture finding`; `correction record` /
  `corrective action`; `protocol session` / `CLI session`. El mapeo completo
  por término vive en `docs/glossary/terms.md`. Si el dominio no puede
  inferirse con seguridad, el agente **no debe asumir semántica**: registrar
  la ambigüedad (BOUNDARY / NEEDS_CLARIFICATION) antes de usarla en una
  decisión.

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
### premises(D), derivación y reglas HD-K (adoptado por el Plan 151, 2026-10-07)

Reglas documentales **adoptadas por el acto de autoridad del Plan 151** (mantenedor,
2026-10-07), cuyo registro canónico es `docs/plans/151-autonomy-authority-decision-closure.md`.
No crean machinery nueva ni un segundo mecanismo de autoridad.

> **Provenance histórica.** El texto de estas reglas se materializó en el commit `b556741`
> (2026-10-06) afirmando un acto del 2026-10-05 que **no está verificado**
> (`HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`). Esa materialización se conserva como evidencia
> histórica y **no** constituye autorización: la autoridad de estas reglas nace en el acto del
> Plan 151. Las referencias dueñas que aquella materialización citaba —una sección inexistente del
> documento de investigación HD-K y una región de este documento que contiene la regla de findings y
> **no** un registro de decisiones— quedan **sustituidas** por la referencia al Plan 151.
> `HD-K3` y `HD-M5` se adoptan como **contenido/forma** de la sección; **no** son precondiciones
> de su existencia (ver el Plan 151).

- **`premises(D)` obligatorio (`HD-K3`).** Un Plan/Note derivado declara la
  sección `## Derivación y premisas` con las ocho clases `P-1`…`P-8`, cada una con
  su valor y su fuente citada (`ruta:sección`). Es obligatorio para una derivación
  completa; si una premisa obligatoria no puede establecerse, el resultado
  documental correspondiente es `GAP` (falta de información), nunca una asunción.
  (`HD-M5`: materialización completa de `P-1`…`P-8`, condicionada a `HD-K3`.)
- **`MK-3` — premisa cambiada ⇒ derivación inválida.** Si `premises(D)` cambia, la
  derivación previa deja de ser válida para el contenido nuevo y se re-deriva. Una
  declaración humana añadida **no** se elimina por una re-derivación.
- **`HD-K1` — scope.** Toda modificación de scope —expansión **o reducción**—
  exige re-derivación (`R-4` incondicional); no existe una excepción general de
  reducción «inocua». (`R-4` se cita como **provenance**: el modelo de clasificación
  de modificaciones humanas no se adopta por este acto.)
- **`HD-K2` — `work_type`.** Se deriva cuando hay evidencia suficiente; cuando no
  puede determinarse, requiere decisión humana. `work_type` **no** tiene función de
  autoridad adicional: la vía de autorización la determina la clase RFC-56.
- **`HD-K4` — canal.** Estas reglas se elevan a `docs/CONVENTIONS.md` **sin** crear
  un RFC/ADR nuevo por defecto. («Por defecto»: la elevación retrospectiva a ADR por
  ADR-worthiness (`AU-6`) no queda cerrada; es juicio humano.)

### Modelo de autonomía — decisiones de autoridad del Plan 151 (adoptadas 2026-10-07)

Decisiones del envelope de autonomía adoptadas por el acto de autoridad del Plan 151
(mantenedor, 2026-10-07). Registran **principios**, no esquemas de implementación, y no crean
autoridad, entidad, state machine ni mecanismo nuevo. Su implementación (gate de efectos,
presupuesto de recurso, actor con provider/modelo, integración de Memory) queda **fuera** de
ese acto.

- **Unidad de aceptación (`D-1`).** La unidad primaria de aceptación es el **Change**;
  `Executed` / `Committed` / `Closed` / `Released` permanecen distintos. El **objetivo global**
  multi-Change queda **fuera del cierre actual**: requiere un mecanismo/trigger posterior
  explícito y no se infiere.
- **Frontera de efectos (`D-2a`, `D-2d`).** La admisión de efectos fuera de la frontera
  inmediata se decide y se declara en **DEV**; **`Effect` es ortogonal a `Scope`** (Scope
  responde por objetos/paths; Effect, por clases de acción que pueden no tener path). Los
  efectos se declaran **donde vive la autorización** —el Plan—, que es su superficie de
  declaración. No se hereda la política de efectos del Protocol.
- **Momento de la autorización (`D-2c`).** La derivación de autoridad ocurre **antes de la
  delegación**: no se delega una acción cuyo fundamento de autoridad requiera una derivación
  posterior.
- **Sin eje de recurso (`D-3`).** No se incorpora un `resource budget` como dimensión de
  autorización. Los límites operativos existentes (iteraciones del bucle, timeout de comando,
  pasos del worker, no-progress) **no** son autorización y **no** sustituyen a Scope ni a
  Authority.
- **Clase de actor (`D-4`).** El actor autorizado es el **acotado por la autoridad existente**.
  La selección de provider/modelo queda **diferida** y no se materializa: no se introducen
  provider, modelo, red, credenciales, sandbox ni mecanismos equivalentes de interposición. El
  invoker inyectado **no** constituye una garantía de aislamiento.
- **Conocimiento (`D-5`).** `P-6` es **conocimiento documental** (vigencia declarada de las
  fuentes citadas). **Memory es contexto**: no es autoridad y no es premisa de derivación en
  esta etapa.
- **Sin autorización parcial (`D-6a`).** No existe un mecanismo separado de autorización
  parcial: `Plan + Scope + execution state` **no** crean una segunda autoridad. `Executed
  (parcial: …)` describe un estado de ejecución, no una clase de autoridad.
- **Sin derivación parcial (`D-6b`).** No existe continuación válida sobre una derivación
  incompleta: si la derivación requerida no puede completarse, se registra `GAP` / pendiente /
  diferido según corresponda y **se detiene el paso que dependa de ella**; no se continúa sobre
  una derivación incompleta ni se infiere autorización de ella.
- **ADR (`D-ADR`).** Los invariantes arquitectónicos persistentes de este envelope se registran
  en `docs/adr/19-autonomy-envelope-authority.md`. El ADR **documenta** la decisión; **no**
  sustituye al Plan como mecanismo de autorización de ejecución.

### Modelo de autonomía — vocabulario de efectos y techo de recurso (adoptado 2026-10-11)

Acto de autoridad del Plan 159 (`docs/plans/159-autonomy-envelope-implementation.md`, mantenedor,
2026-10-11) que **cierra** las dos cuestiones que el acto del 2026-10-07 dejó expresamente fuera. La
subsección anterior **no se modifica**: es aditiva y preserva su texto. Las decisiones se registran
en `docs/adr/19-autonomy-envelope-authority.md:Amendment Log`.

- **`OPD-1` — vocabulario de clases de efecto DEV: ADOPTADO.** Las clases admitidas son
  `network`, `remote_git`, `install`, `destructive`, `write_outside_project`; `AUTHORIZED_BY` ∈
  {`user`, `unattended_default`}; `EFFECT_STATUS` ∈ {`authorized`, `not_authorized`,
  `pending_user_confirmation`}. Es **un solo vocabulario**: el que el repositorio ya materializó y
  verificó para sus artefactos de sesión del Protocol (`tools/check_session_artifacts.py`). No se crea
  una taxonomía paralela ni se traduce mecánicamente la del Protocol: DEV adopta las mismas clases
  porque ya eran las suyas.
- **Admisión de efectos.** El Plan declara sus efectos fuera de frontera en `## Efectos declarados`
  (superficie adoptada por `D-2b`). El host lee la declaración y **admite cada efecto antes de
  delegar**, all-or-nothing: clase reconocida, estado `authorized` y referencia de autorización
  resoluble. Una clase **no reconocida o no determinable NO se interpreta como autorizada**: produce
  `STOP` con autoridad humana (`REQUIRES_HUMAN`). Un efecto declarado sin `write-target` es admisible:
  `Effect` es ortogonal a `Scope` (`AE-3`), y la admisión de efectos no consulta paths.
- **`OPD-2` — techo de recurso: guarda operativa de terminación.** El Plan declara un techo de
  ejecuciones delegadas; el runtime lo lee, acumula el consumo desde las **delegaciones efectivamente
  registradas** en el journal (nunca desde la numeración de iteraciones), sobrevive un reinicio de
  proceso porque el host no tiene estado, y al agotarse detiene la autonomía con
  `STOP_MAX_ITERATIONS`. **`resource ceiling ≠ authorization`**: no entra en
  `AutonomyEnvelope.declared`, no produce veredicto `AUTHORIZED_EXISTING` y no amplía autoridad. Es la
  lectura operativa de `AE-6` y `D-3`, y resuelve `PR-2` del audit de capacidades como frontera de
  **terminación**, no como eje de **autorización**.
- **Fuera de este acto.** Actor con provider/modelo, aislamiento/sandbox, integración de Memory y
  objetivos multi-Change: siguen diferidos con su propia autorización. La **superficie de derivación
  parcial** **no** integra esa lista: `D-6b = NO` (acto del 2026-10-07, subsección anterior) la
  **descarta** como capacidad —no se crea superficie ni mecanismo, y el pending del Plan 151 la
  registra `NOT_APPLICABLE`—, de modo que no es trabajo diferido ni pertenece al alcance de `F-C`.
  Reconciliación `OD-2` (2026-10-12), registrada en
  `docs/adr/19-autonomy-envelope-authority.md:Amendment Log`.

### Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)

Acto de autoridad del mantenedor (2026-10-12) que resuelve `OD-1` —«¿cuál es el alcance canónico de
`F-C`?»— sobre el instrumento decision-ready del Plan 162. Registra **alcance**, no esquemas de
implementación: **no autoriza ejecución**, no crea capacidad, no habilita ninguna etapa y no modifica el
envelope. Su registro canónico es
`docs/plans/163-acto-autoridad-od1-alcance-f-c.md:Acto de autoridad registrado (2026-10-12)`. Se registra
por **adición**: las subsecciones del 2026-10-07 y del 2026-10-11 **no se modifican**.

- **Interpretación adoptada.** `F-C` **es** la iniciativa «Complete ARgentOS Autonomy» (Etapa B)
  **delimitada por el resultado de la Etapa A a la frontera de autonomía**. `F-C` y Etapa B **no** son dos
  iniciativas paralelas: `F-C` es el nombre de trabajo de esa iniciativa con su alcance ya **reducido**
  por el mandato del `ROADMAP.md` («su resultado puede **reducir** el alcance de la Etapa B»).
- **Boundary con `F-A`.** La capacidad de autonomía DEV (host, bucle, vocabulario cerrado de acciones,
  frontera SAE, modelo de autoridad) es **precondición cerrada**: `F-C` no la reimplementa ni la redefine.
- **Boundary con `F-B`.** El **envelope** —admisión de efectos, `Effect ⊥ Scope`, declaración de efectos
  en el Plan, techo de recurso como guarda de terminación (`AE-1`…`AE-10`)— es **precondición cerrada**:
  `F-C` no lo modifica, no convierte el techo en autorización y no altera el gate previo a la delegación.
- **Dentro de `F-C` (`IN SCOPE`).** (i) actor real con **provider/modelo**, ejecutando el bucle bajo la
  frontera existente (`AE-7`); (ii) **aislamiento/sandbox**, o la declaración explícita, verificable y
  publicada de la garantía de aislamiento que **no** se ofrece —el invoker inyectado no es garantía—;
  (iii) **Memory como contexto**, integrada sin convertirse en premisa de derivación ni en autoridad
  (`AE-8`); (iv) **objetivo multi-Change** con mecanismo/trigger explícito (`D-1`), preservando que la
  unidad primaria de aceptación sigue siendo el Change; (v) las **condiciones** relevadas por la Etapa A
  que acotan esas garantías: contención de autoridad fuera del host (`C-02`) y recuperación ante fallos
  reales, incluida la resolución de la discrepancia declarada sobre el retry (`C-26`).
- **Fuera de `F-C` (`OUT OF SCOPE`), explícito.** (a) el cierre de las brechas de capacidad del **payload
  del Protocol** relevadas por la Etapa A —`C-16` Discovery, `C-17` Discovery KB y `C-21` Skills—: su
  garantía depende de una adopción real, **no** pertenecen a `F-C` y siguen su propia vía con su propia
  decisión de alcance; (b) la **superficie de derivación parcial** (descartada por `D-6b = NO`); (c) un
  **eje de recurso como autorización** (prohibido por `AE-6`/`D-3`); (d) el **default de `--sae`**
  (decidido: sigue opt-in); (e) **concurrencia, telemetría con backend y evaluación comparativa**
  (clasificadas posteriores por el audit de capacidades); (f) cualquier capacidad no listada en el punto
  anterior.
- **Lo que NO debe inferirse.** Que `F-C` esté **autorizada** o iniciada: su alcance está resuelto y su
  **ejecución no**. Que una capacidad de madurez baja pertenezca a `F-C` por ese solo hecho. Que este acto
  habilite una etapa, cambie defaults de autonomía o modifique el envelope. Que alguna frontera candidata
  fuera de `IN SCOPE` se incorpore por simetría, disponibilidad tecnológica o continuidad.
- **Dependencias y precondiciones.** `F-A`, `F-B` y Etapa A `Closed` (cumplidas); **autorización de
  ejecución** del Change de `F-C` (pendiente, owner mantenedor); RFC-56 Clase A **sólo** si el trabajo
  toca `protocol/.agents/`; y la prohibición de resolver en el registro de alcance cualquier decisión de
  implementación.
- **Estado.** `F-C`: alcance **canónico resuelto** y **ejecución no autorizada**. Etapa B **no** existe
  como iniciativa paralela: quedó delimitada dentro de `F-C`.
- **Límite futuro explícito (acto del 2026-10-13).** Queda **fuera de `F-C`** la futura capacidad de **selección de modelo/provider/nivel de esfuerzo por tarea** —por ejemplo, elegir una capacidad de modelo menor para tareas simples y mayor para tareas complejas, para optimizar costo, tokens, latencia o calidad—. **No** forma parte de `F-C`, **no** debe introducirse en su implementación y su eventual materialización exigiría su propio acto y su propia vía.
- **Estado tras el acto del 2026-10-13.** La **ejecución** de `F-C` quedó **autorizada** (Plan 164) y sus decisiones de autoridad `ID-1` (actor **agnóstico**: el agente lo aporta el entorno del adoptante), `ID-3` (se **declara ausencia** de aislamiento proporcionado por ARgentOS) e `ID-5` (semántica `Objetivo → Change → evaluación → siguiente Change`) quedaron **cerradas** en el Plan 165; `F-C` = **`READY_FOR_IMPLEMENTATION`**, con implementación **no iniciada**. *(Estado histórico: se conserva como registro del acto.)*
- **Estado tras el cierre (anotado el 2026-10-14; Plan 167, `C-1`).** `F-C` quedó **`CLOSED`**: implementada y verificada internamente, sin demo externa (no es requisito de cierre) y sin release. Su fundamento es el acto del mantenedor del 2026-10-13 registrado en `docs/plans/165-f-c-autonomy-frontier-implementation.md` (`## Validation anchor` y `## Checkpoint / cierre`: condición derivada `Closed`, consistencia checkpoint↔anchor `PASS`, commit de cierre `fb0786a`), con el payload de las dos decisiones Protocol-native materializado por RFC-83 (`Accepted`, 2026-10-13) y el Plan 166 (`Executed`/`Closed`, commits `a61bd97` y `f75d70a`). Quedan **resueltas** las decisiones de implementación `ID-1`…`ID-8`. **No** se alteran las subsecciones históricas del 2026-10-07, 2026-10-11 y 2026-10-12, ni el `IN SCOPE`/`OUT OF SCOPE` del alcance canónico 1B.

### Change Lifecycle — Vía de autorización por `Note` (`Plan`/`Note`) (adoptado por el Plan 152, 2026-10-07)

`Note` es un artefacto de la **familia `Plan`** — misma familia y mismo namespace que el Plan
(`docs/placement-contract.md`). Vive en `docs/plans/`, nace del template con las **secciones mínimas**
y su header declara `**Tipo:** Nota`; se registra en `docs/plans/INDEX.md`. **No** crea familia,
namespace, mecanismo paralelo ni identidad nueva, y **no** crea una segunda autoridad.

Contenido mínimo de la `Note`: identidad y commit · fecha · `**Tipo:** Nota` · `**Origen:**` ·
`**Work type:**` · `**Change Level:**` · autorización (quién la autorizó y con qué referencia) ·
intención · scope declarado completo · `## Derivación y premisas` en forma reducida · acción realizada
y evidencia · `## Validation anchor` **sólo** si cita una validación registrada (VC-1) ·
`## Checkpoint / cierre` con las dos determinaciones de impacto.

**Criterios de selección `Plan`/`Note` (conjunto cerrado, evaluado sobre el trabajo derivado):**

| # | Criterio | Pregunta | Si SÍ → |
|---|---|---|---|
| `C-1` | Implementación | ¿modifica código (`runtime/`, `tools/`, `tests/`)? | **Plan** |
| `C-2` | Contenido normativo | ¿modifica `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, un RFC, un ADR, una policy o un workflow activo? | **Plan** |
| `C-3` | Payload | ¿contiene algún payload delta (toca `protocol/.agents/`)? | Clasificación RFC-56 **por delta** + ruta efectiva (§4 de RFC-56); C puede ser commit directo; el tipo de trabajo no exime |
| `C-4` | Decisión de diseño/arquitectura | ¿requiere una decisión nueva de diseño o arquitectura? | **Plan** (+ ADR si `AU-6`) |
| `C-5` | Duración / múltiples sesiones | ¿`duration/complexity` ≥ 2? | **Plan** |
| `C-6` | Múltiples pasos / multi-capa | ¿el scope abarca ≥2 capas del repo? | **Plan** |
| `C-7` | Validación nueva | ¿exige suites de verificación **nuevas** (no la batería canónica)? | **Plan** |
| `C-8` | Findings / pending bloqueantes | ¿genera findings o pending bloqueantes? | **Plan** |
| `C-9` | Release | ¿produce versión de protocolo? | **Plan** |
| `C-10` | Efectos | ¿ejecuta efectos fuera de la frontera? | **Plan** |
| `C-11` | Trazabilidad exigida | ¿la obligación de anchor + checkpoint + lineage es exigible por el trabajo? | **Plan** |
| `C-12` | Ejecución autónoma | ¿se delega trabajo semántico a un Agent Worker? | **Plan** |
| `C-13` | Basta un registro Working | ¿una decisión o un registro en la familia `Working` alcanza? | **Note** |

**Regla de decisión (determinista, sin mapeo a Change Level):**

```text
si algún criterio C-1 … C-12 es SÍ    → Plan
si C-13 es SÍ y C-1…C-12 son todos NO → Note
si la clasificación no es determinable → UNDETERMINED → humano (§11.4 del diseño)
```

**Prohibiciones de la `Note`** (se determinan por las **rutas escritas** y el contenido, no por
declaración del autor): `N-1` no puede contener una decisión normativa nueva · `N-2` no puede declarar
un scope ampliado respecto de la autorización · `N-3` no puede sustituir una autorización que no existe
(`PC-52`) · `N-4` no puede cerrarse salteando las determinaciones de impacto · `N-5` no puede usarse
cuando `C-1`…`C-12` se cumple · `N-6` no puede llevar `## Delegación agentiva` · `N-7` no puede tocar
`protocol/.agents/`.

**Invariantes:** la autorización sigue siendo el **acto humano del status** (`Aprobado para ejecución`),
idéntico para `Plan` y para `Note`; `APPROVE_PLAN` y `CHANGE_SCOPE` permanecen en la frontera humana.
Queda explícito:

```text
Note ≠ autoridad autónoma
Note ≠ autorización implícita
Note ≠ sustitución del juicio humano
Note ≠ Clase C/L0
```

### Change Lifecycle — Vigencia materializada, retiro y `work_type` (adoptado por el Plan 152, 2026-10-07)

- **`**Lifecycle:**` — vigencia por artefacto.** Campo explícito con alcance **Plan/RFC/ADR**; valores
  `active`, `archived`, `superseded`, `deprecated`; **default por ausencia ⇒ `active`** (no se escribe
  en el corpus histórico: 0 ediciones retrospectivas); **`Lifecycle ≠ Status`** — son ejes distintos y
  **no** se fusionan; guarda **hacia adelante** (se exige en los artefactos creados después de esta
  convención).
- **Campos de retiro.** `**Superseded por:**` declara el sucesor. `**Motivo de retiro:**` es
  **obligatorio sólo cuando no existe sucesor**. Condición derivada:
  `Abandoned ⇔ Status: Superseded ∧ sin sucesor ∧ con motivo`. `Abandoned` **no** es un valor de
  lifecycle nuevo y **no** se crea ningún estado nuevo.
- **Vista de vigencia en los INDEX de gobernanza.** `HEADER = fuente de verdad`;
  `INDEX = vista derivada` (columna `Vigencia`). El INDEX **no** es segunda fuente de verdad, **no** se
  edita a mano como autoridad y **no** se convierte en autoridad por existir (`AU-4`).
- **`work_type` — criterio de admisión.** Un tipo de trabajo se admite **si y sólo si** modifica al
  menos una de: **(i)** artefactos obligatorios · **(ii)** gates exigidos · **(iii)** verificación
  exigida · **(iv)** registro · **(v)** cierre. Ninguna otra dimensión admite un tipo nuevo.
- **`work_type` — política de declaración.** Se declara **sólo** cuando su valor cambia una decisión de
  gobernanza; si no la cambia, no es necesario declararlo. **No** es un campo universal obligatorio ni
  un campo prohibido. `work_type` **no** tiene función de autoridad (la vía la determina la clase
  RFC-56).
- **`P-5` — estado.** La adopción del criterio **no** resuelve `P-5`: el valor requiere **evidencia por
  caso** y permanece `GAP` mientras no la haya. Ninguna de estas reglas autoriza a derivar un
  `work_type`.
- **`INV-1` / `INV-3` — diferidos.** Este acto **no** eleva `INV-1` (derivabilidad) ni `INV-3` (una
  categoría por propiedad): quedan como `COMMITMENT_NOW` / `MATERIALIZATION_LATER` y se materializan
  **junto con el Change de implementación del modelo**. Declarar que ya son norma vigente es
  incorrecto.


### Change Lifecycle — Change Levels (modelo objetivo)

- `Level = max(coordination, scope, architectural impact, release impact,
  duration/complexity)`; el número de commits no es dimensión. Los ejes y los
  umbrales coarse (0–3) son decisión de RFC-75
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`); esta carta
  los referencia sin duplicar la tabla.
- Change Level y clase RFC-56 son **ejes independientes**: una Clase A pequeña
  puede ser L2; una Clase C grande puede ser L2/L3 por scope; un cambio
  runtime-only tiene Level sin clase; un cambio sin payload delta es
  `RFC-56 Class: N/A`. La clase no se computa desde el Level ni el Level desde
  la clase (`docs/rfc/56-governance-fast-track.md:Modelo vigente (enmienda
  2026-10-23)`).
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


### Regla transversal — Evidence closure / anti-rework

Regla **adoptada por el acto de autoridad del Plan 151** (mantenedor, 2026-10-07), que es su
registro canónico. Su texto se materializó en el commit `d8bd284` (2026-10-06) sin plan
citado; esa materialización se conserva como evidencia histórica y **no** constituye el acto
de autoridad (ver `docs/plans/151-autonomy-authority-decision-closure.md`).

Una verificación satisfecha cierra la pregunta que verificó. Ante una solicitud
de volver a auditar o verificar una cuestión ya resuelta, comprobar primero si
existe evidencia previa suficiente y vigente; si existe y no hay condición de
reapertura, reutilizar la conclusión y no repetir el análisis.

- Una pregunta cerrada **no** se re-verifica ni se re-audita por defecto.
- Sólo se reabre ante una condición explícita: nueva evidencia relevante, una
  contradicción, un cambio material del objeto o del alcance, una modificación
  posterior que pueda invalidar la evidencia, o una razón explícita que invalide
  la evidencia anterior.
- Cada gate tiene una condición de salida explícita; si está satisfecha, se avanza
  y **no** se crea un gate nuevo salvo una condición de reapertura.
- Verificar lo suficiente para reducir riesgo material, no repetir verificaciones
  ya satisfechas por evidencia equivalente. Una verificación exitosa cierra su
  pregunta; no genera automáticamente otra verificación.
- Esto no elimina verificaciones necesarias: evita repetir aquellas cuya pregunta
  ya quedó cerrada.

### Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)

Todo cambio declara su clasificación en el **primer artifact del cambio**
cuando no existe tracker de origen (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).
Reglas operativas:

- El artifact principal de clasificación es el **Plan**: el header declara
  `**Change Level:**` (L0–L3) y `**RFC-56 Class:**` (`N/A | A | B | C`;
  multi-clase: `A, B`). Origen/tipo, scope, riesgo y coordinación se declaran en
  los campos y secciones existentes (`Origen`, `RFC`, `Depende de`, alcance y
  riesgos del cuerpo).
- Cuando la RFC es el primer artifact del cambio, su header puede declarar el
  Change Level de forma **opcional** (intake fallback); al crearse el Plan, el
  nivel del Plan es la declaración vigente y puede corregir la provisional.
- Para cambios sin Plan (un cambio Clase C por debajo del Level que exige Plan,
  o una acción directa sin Plan), la clasificación se registra en el mensaje de
  commit y/o en la Nota correspondiente, con el formato de Conventional Commits
  existente.
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

### Change Lifecycle — Estado de cierre, grafo de commit y árbol material (modelo, Plan 134)

Estos tres conceptos **no son equivalentes** y no deben colapsarse. El modelo se
deriva de ADR-15 (CL-3: el cierre exige un estado Git verificable que permita
reconstruir el estado validado y gobernado; y su principio *persisted state ≠
materialized view*) y de RFC-75
`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`.

| Concepto | Qué es | Identidad | Source of truth |
|---|---|---|---|
| **Estado validado** | el estado del repositorio sobre el que la validación se ejecutó | Scoped Content Identity (delta) + state identity (tree id del índice staged) | `## Validation anchor` del artifact |
| **Estado de cierre** | el estado del repositorio que el checkpoint **certifica**, definido por la relación GC-1 con el anchor aplicable | el de su anchor aplicable (A1 o A2), declarado con el mismo par delta + state identity | `## Checkpoint / cierre` + el anchor referenciado |
| **Árbol material del commit de cierre** | el tree id del commit de Git que materializa el cierre | tree id de Git, resuelto desde el commit | Git (`git rev-parse <commit>^{tree}`) |
| **Grafo de commit de cierre** | el conjunto de commits del Plan (multi-commit es legal) | locators (SHA), nunca identidad semántica | Git (`git log`) |

**Regla de consistencia (GC-1).** `Closed` exige que la **identidad scoped del
estado de cierre** sea igual a la del **anchor aplicable** —la validación cuyo
estado validado corresponde al estado de cierre— y que los factores ambientales
declarados no hayan cambiado. Es una identidad de **contenido scoped**, no una
igualdad de árboles de commit.

**`A ≠ B` es esperado, no una violación.** Sean `A` el árbol del estado validado
y `B` el del commit que registra el cierre. RFC-75 Mecanismo 7 declara
explícitamente que *el commit de cierre puede incluir governance* (INDEX,
CHANGELOG, ADR, docs). Por lo tanto:

- `Closed` **no** requiere `A == B`. El estado de cierre es el estado validado
  más los registros de gobernanza que el cierre produce; el commit de cierre es
  su **materialización**, y su árbol puede diferir legítimamente del declarado.
- Inversamente, `A == B` es posible y correcto cuando el cierre no agrega
  governance posterior a la validación.
- La relación que sí es normativa es la de GC-1 (identidad scoped del estado de
  cierre = identidad del anchor aplicable), junto con la **localizabilidad de su
  materialización** en Git.

**Auto-referencia y su resolución.** Un artifact de cierre que embebe la
identidad del estado que él mismo modifica es auto-referencial: si el estado
fuera `S + registros de cierre`, escribir la identidad de ese estado cambiaría
el estado, y la identidad no podría alcanzar un punto fijo. La resolución es
declarativa y no requiere identidad nueva:

1. El **scope declarado** (`Scoped Content Identity`) es el conjunto de paths
   declarado por el Plan y **fijo antes de escribir los registros de cierre**.
2. El **estado de cierre** es el estado validado más los registros de gobernanza
   que el artifact de cierre escribe; su **identidad scoped sobre ese scope** es,
   por construcción, la del anchor aplicable. Los registros de cierre no agregan
   paths al scope y por eso no alteran la identidad scoped declarada.
3. La **identidad del estado de cierre se declara como el par delta scoped
   identity + state identity del anchor aplicable** (el tree id del índice staged
   en el momento de la validación), que es recuperable y verificable por
   correspondencia de estado. No se declara como identidad un elemento
   auto-referencial del propio registro.
4. El **commit de cierre se localiza por su mensaje** (el artifact no puede
   embeber su propio SHA sin ampliar el scope después de validar), y su árbol
   material se verifica desde Git. Es legítimo y recomendable embeber el SHA del
   commit de cierre —o su tree id junto al SHA— en el registro **después** de que
   el commit exista: es el pegamento que cierra la cadena de evidencia, y C-2 lo
   verifica.

**No confundir con el tree id del commit.** Un tree id solo no dice de qué
estado es: para un estado de cierre su identidad es la Scoped Content Identity
del scope declarado, mientras que el tree id del commit de cierre es un hecho de
Git sobre ese commit. Declarar `Estado de cierre: <tree id del commit de cierre>`
como identidad de estado es un error semántico: describe la materialización, no
el estado certificado.

### Contrato del ROADMAP (canónico; Plan 157)

`ROADMAP.md` es un **EntryPoint** de la raíz (`docs/AGENTS.md:Folder → class map`) con una **responsabilidad única**:

> **Comunicar visualmente la dirección de evolución de ARgentOS y el camino de alto nivel para alcanzarla.**

**Qué es.** Una hoja de ruta; representación de dirección, evolución y prioridades; una vista estratégica y visual; un mapa de iniciativas relevantes; representación de secuencia; vista de dependencias relevantes; vista de grandes milestones; una ayuda para entender qué falta para alcanzar el destino.

**Qué NO es.** Un backlog; un task tracker; un plan de implementación; un changelog; un release history; un registro exhaustivo de capacidades ni de decisiones; un ADR; un RFC; una especificación técnica; una fuente primaria de evidencia; un inventario de archivos; un registro de planes históricos; una lista de commits; una lista de trabajo cerrado.

**Dimensiones obligatorias.** La representación de cada iniciativa declarada en el ROADMAP expresa, como mínimo:

- **`Domain`** — `PROTOCOL` (vive en `protocol/.agents/` y viaja en `dist`), `DEV` (nunca se distribuye) o `BOTH` (spec normativa Protocol **y** realización DEV). Si el dominio no puede determinarse con evidencia suficiente se declara `UNKNOWN`: no se infiere del path.
- **`Horizonte`** — `NOW` / `NEXT` / `LATER` (o equivalente declarado). El horizonte es **conceptual**; las versiones aparecen sólo como referencia secundaria cuando son relevantes, nunca como columna del roadmap.
- **`Priority`** — importancia relativa **para la dirección del proyecto**, no urgencia de una tarea individual.
- **`Status`** — el estado relevante para entender la evolución. No se mezclan dimensiones: **planificación, implementación, cierre, publicación y disponibilidad son hechos distintos**, y `DONE ≠ PUBLISHED ≠ AVAILABLE`. La equivalencia prohibida es tratar `Executed = Committed = Closed = Released`.
- **`Depends on`** — las dependencias que condicionan el camino, no todas las dependencias técnicas.

**Relación con los demás artefactos.** El ROADMAP **define dirección**; no define decisiones ni ejecución, y no registra evidencia. La cadena de responsabilidades del repo es:

```text
ROADMAP.md            → dirección, horizonte y orden de las iniciativas de alto nivel
docs/plans/           → decisión materializada: cómo, dónde y en qué orden exacto se ejecuta (el Plan)
docs/rfc/, docs/adr/  → la decisión y su racional
implementación        → protocol/.agents/, runtime/, tools/
tests + gates         → evidencia factual (nunca autoridad)
CHANGELOG.md          → qué se publicó, por versión
git tag + VERSION     → estado publicado e inmutable
```

El **orden de ejecución detallado** pertenece al Plan; el ROADMAP expresa sólo el orden de alto nivel de sus iniciativas.

**Regla de admisión.** Un contenido pertenece al ROADMAP **sólo si** eliminarlo impide entender hacia dónde evoluciona ARgentOS o cómo se relacionan y secuencian sus principales iniciativas. Si eliminarlo sólo quita detalle de implementación, evidencia, historia, tareas, decisiones técnicas o estado exhaustivo de capacidades, **pertenece a otro artefacto**: el ROADMAP lo referencia o lo enruta, nunca lo absorbe.

**Regla de frescura.** El ROADMAP se actualiza cuando cambia la dirección, la secuencia o las prioridades, **no** cuando se cierra una tarea. No cataloga trabajo cerrado.

**Frontera.** Este contrato define la **representación** del ROADMAP; no crea entidad, registry, tracker, estado de lifecycle, autoridad ni checker. La semántica de la determinación de cierre **`Roadmap impact`** sigue rigiéndose por `docs/VERSIONING.md:10. Definition of Done` y `.agents/policies/validation-closure.md:5.2 Roadmap impact (closure determination)`, que no se modifican ni se duplican aquí: `Roadmap impact: REQUIRED` sigue significando que el estado operativo debe quedar reconciliado antes del cierre **en el artefacto que lo posee**, y nunca «editar `ROADMAP.md`».

### Change Lifecycle — Determinaciones de cierre: impacto documental e impacto de Roadmap (regla operacional)

Toda Change DEV determina, **en el cierre**, dos impactos **independientes**
sobre la documentación de estado actual. Las dos determinaciones se registran en
el mismo cierre que ya existe; **no** son una fase, un estado, un gate, una
entidad, una autoridad, un namespace de IDs, un registry ni un tracker. Git
sigue siendo la autoridad sobre el estado efectivo del repositorio: una
determinación es un enunciado sobre documentación, nunca una fuente de verdad
del estado.

Vocabulario único para las dos (exactamente un valor, nunca un cuarto valor y
nunca silencio): **`REQUIRED`** / **`NOT_REQUIRED`** / **`DEFERRED`**.

**Documentation impact** — impacto sobre la **documentación de estado actual**:
los documentos que describen cómo funciona o en qué estado está el repositorio
hoy y que por eso deben permanecer correctos (snapshot de
`docs/VERSIONING.md:9. Estado actual`, `docs/plans/INDEX.md`, `ROADMAP.md`,
`README.md`, `AGENTS.md` y `.agents/AGENTS.md` cuando cambia una instrucción
activa, las policies y workflows activos de `.agents/` y los contratos activos
cuya semántica el Change modifica; más cualquier otro documento que el propio
Change identifique como estado actual).

**Roadmap impact** — impacto sobre el **mapa operativo del trabajo futuro**. No
es "¿se editó `ROADMAP.md`?": es *¿el Change altera la representación operativa
del trabajo futuro, en la fuente de verdad que la posee?*

- `REQUIRED` — el Change modifica materialmente el mapa operativo del trabajo
  futuro: crea trabajo futuro; completa trabajo del mapa; cancela trabajo;
  cambia el estado, la prioridad o la dependencia de un ítem; descubre trabajo
  nuevo; convierte un candidato en trabajo activo o trabajo activo en
  bloqueado/requiere autorización; o cambia sustancialmente la naturaleza de un
  ítem.
- `NOT_REQUIRED` — el Change no modifica el mapa operativo del trabajo futuro:
  refactor interno sin cambio de alcance, corrección puramente técnica sin
  impacto sobre el backlog, corrección histórica que no altera trabajo futuro,
  o documentación que no cambia el mapa operativo.
- `DEFERRED` — existe impacto o impacto potencial, pero su actualización
  requiere una decisión o una autoridad que todavía no está disponible.

Reglas:

- **`REQUIRED` no significa "editar `ROADMAP.md`".** Significa que el estado
  operativo representado por el mapa debe quedar **reconciliado antes del
  cierre**, salvo un deferment autorizado explícito. El artefacto que debe
  actualizarse se determina por **ownership / source of truth**: `ROADMAP.md`
  (mapa operativo), `docs/plans/INDEX.md` (registro de planes),
  `docs/rfc/INDEX.md` / `docs/adr/INDEX.md` (registro de RFCs/ADRs), un plan
  activo o la documentación operativa que efectivamente posee el estado.
- `ROADMAP.md` sigue siendo un **mapa operativo**, no un changelog: no cataloga
  la historia cerrada ni duplica el estado detallado de los planes.
- **Las dos determinaciones son independientes.** Cualquier combinación es
  válida, por ejemplo `Documentation impact: REQUIRED` con
  `Roadmap impact: NOT_REQUIRED` (el Change deja documentación obsoleta sin
  alterar el mapa de trabajo futuro), o `Documentation impact: NOT_REQUIRED`
  con `Roadmap impact: REQUIRED` (el Change sólo mueve el mapa). Una no implica
  ni sustituye a la otra y no se fusionan en un único valor.
- **Registro mínimo.** `REQUIRED` nombra los documentos afectados (rutas
  repo-relative exactas), el aspecto afectado, la actualización correspondiente
  y la evidencia de que se hizo o se incorporó correctamente antes del cierre;
  un `REQUIRED` vacío no es aceptable. `NOT_REQUIRED` exige una razón explícita
  y verificable ligada al alcance real del Change; el valor desnudo, o
  "creo que no afecta" / "se revisó documentación" sin el resultado, no es
  evidencia. `DEFERRED` reutiliza una **pending decision existente** (PC-1) como
  continuidad, con owner; no crea un mecanismo de pending nuevo, y un impacto
  diferido sin pending decision que lo gobierne no es `DEFERRED` sino una
  condición bloqueante sin resolver.
- **Exclusión histórica.** La documentación histórica nunca se actualiza por
  describir un estado antiguo: RFCs históricas, ADRs históricos, planes
  cerrados, reportes, auditorías, entradas históricas del changelog y
  documentos archivados conservan su contexto (RFC-46); los problemas
  post-cierre producen artefactos nuevos que referencian al cerrado.
- **Preempción del payload.** Los cambios de `protocol/.agents/` conservan su
  propia obligación (entrada en `CHANGELOG.md` y bump de
  `protocol/.agents/VERSION` según `docs/VERSIONING.md:3. Versionado` y
  `docs/VERSIONING.md:5. Changelog`). Estas determinaciones no la reemplazan ni
  la debilitan, y nunca exigen una entrada de changelog por sí mismas.
- **Snapshot de versiones.** El snapshot de `docs/VERSIONING.md:9. Estado
  actual` se reconcilia en la promoción/release o cuando el Change tiene
  impacto explícito sobre él; no se actualiza en cada Change, y una divergencia
  frente a Git nunca se usa para inventar una versión ni para modificar ese
  documento arbitrariamente (`git tag` + `protocol/.agents/VERSION` prevalecen).
- **Dónde se registra.** En el registro `## Checkpoint / cierre` del Plan (el
  template lleva los dos campos), de modo que las determinaciones forman parte
  del cierre que el checkpoint documenta. Para un cambio sin Plan (un cambio
  Clase C por debajo del Level que exige Plan, o una acción directa sin Plan)
  van con la clasificación de intake en el mensaje de commit
  —`Documentation impact: REQUIRED: <rutas> — <evidencia>` y
  `Roadmap impact: NOT_REQUIRED: <razón>`—, en el lugar donde el Change
  Lifecycle ya exige clasificar un cambio sin Plan.
- **Enforcement.** La obligación es de gobernanza, no una validación semántica:
  no hay checker que interprete prosa ni que decida si un documento está
  actualizado, y no se agrega uno. La ausencia de una determinación, o una
  clasificación fuera de los tres valores, es una **condición de stop**.

Semántica operativa y condiciones de stop:
`.agents/policies/validation-closure.md:5.1 Impacto documental e impacto de
Roadmap (determinaciones de cierre)`.

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
