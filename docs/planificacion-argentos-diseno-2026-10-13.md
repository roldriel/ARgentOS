# Modelo de planificación de ARgentOS — diagnóstico y diseño

**Fecha:** 2026-10-13
**Naturaleza:** Working / analysis — **no normativo**; puede ser provenance, nunca autoridad.
**Autoridad:** ninguna. Este documento **no** decide, **no** autoriza, **no** crea trabajo y **no** modifica ningún artefacto del repositorio.
**Estado de implementación:** `NOT_IMPLEMENTED` — 0 cambios estructurales. Sin Project, sin Milestone, sin issues, sin migración de `ROADMAP.md`.

**Base de evidencia:** inspección del repositorio en `dev` @ `4c5bfcb` (+30 líneas sin commitear en `docs/plans/165-…md`, declaradas abajo), `protocol/.agents/VERSION` = `12.0.1` (sin tag), tag publicado `12.0.0`, `origin/dev` = `dev` (18 commits sin push), `origin/dist` @ `1181db6`; 174 planes, 85 RFCs, 21 ADRs; la Capability & Guarantee Matrix de Etapa A (28 capacidades × 9 dimensiones); `ROADMAP.md` (107 líneas); `docs/CONVENTIONS.md` §«Contrato del ROADMAP» y §«Change Lifecycle DEV — alcance y frontera»; RFC-75 §«Dev vs Protocol» y §«Rollout incremental»; `docs/VERSIONING.md` §10.

---

## Resumen ejecutivo

**El diagnóstico no es «falta un tablero».** ARgentOS ya tiene un sistema de dirección, y es más sofisticado de lo que su `ROADMAP.md` sugiere. El problema real es que ese sistema **no separa tres ejes que se están mezclando dentro del mismo documento y del mismo campo**:

| Eje | Qué responde | Naturaleza | Cambia |
|---|---|---|---|
| **Dirección** | ¿Qué queremos que ARgentOS llegue a ser? | Intención humana | Casi nunca |
| **Capacidad** | ¿Qué debe poder hacer el PROTOCOL, y en qué estado está hoy? | Estado + evidencia | Con cada Change |
| **Trabajo** | ¿Qué hacemos ahora, bajo qué autoridad, y cuándo está terminado? | Ejecución gobernada | Constantemente |

Hoy **Dirección** y **Capacidad** viven ambos en `ROADMAP.md`, mientras que el **Trabajo** vive en `docs/plans/` (174 planes) y su estado operativo se dispersa entre `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, el header de cada plan y 27 determinaciones de `Roadmap impact` redactadas en prosa. El resultado es un mapa que hay que reescribir cuando cambia el estado —lo contrario de una hoja de ruta— y una obligación de reconciliación que **no es verificable por ningún checker**.

**Las cinco conclusiones principales:**

1. **GitHub Projects no debe ser el mecanismo operativo principal.** No por incapacidad de GitHub —un user project es posible y trackea repos de la cuenta personal— sino porque (a) este repositorio tiene una propiedad constitutiva que un Project no puede preservar: *el estado debe ser clonable, diffeable, revisable por PR y verificable por checker*; y (b) su adopción exige un **PAT clásico con scope `project`+`repo`** que hoy no se necesita, y el `GITHUB_TOKEN` de Actions es repository-scoped y **no** puede leer ni escribir Projects. La recomendación es **repo autoritativo, Project derivado cuando aporte valor de lectura** (Opción C). Detalle verificado en §G.2b.
2. **No hace falta una entidad de trabajo nueva.** «Iniciativa DEV» ya existe: **es el Plan**, con `Objetivo`, `Criterio de entrada`, `Pasos`, `Criterios de salida`, `Validation anchor` y `Checkpoint`. Crear una entidad por encima sería exactamente el tipo de maquinaria que el «Decision-Making Compass» del `AGENTS.md` manda evitar.
3. **Falta una pieza, y sólo una: estado de capacidad con estado objetivo.** El repositorio tiene **evidencia de capacidades** (la matriz de Etapa A, un snapshot de 252 celdas) pero **no tiene declaración de estado objetivo** para ninguna capacidad. Sin objetivo no hay gap; sin gap no hay priorización defendible; sin priorización, toda idea nueva compite por simpatía.
4. **`ROADMAP.md` debe sobrevivir, reducido a dirección y horizonte.** No eliminarlo: su contrato es bueno y su regla de admisión es correcta. Lo que debe salir es el *estado* (posiciones, releases, blockers con detalle), que es lo que lo obliga a cambiar en cada cierre.
5. **El milestone en ARgentOS no es una fecha ni un contenedor de issues: es un resultado del PROTOCOL verificado.** Eso lo descalifica como *Milestone de GitHub* y lo califica como entidad documental con evidencia anclada.

**Y una consecuencia incómoda pero necesaria:** la determinación de cierre `Roadmap impact` (introducida por el Plan 133, presente en 27 planes) se diseñó para un mundo donde el mapa operativo tiene un dueño verificable. Ese dueño no existe: es prosa en `ROADMAP.md`. Su síntoma es que ha generado su propia gobernanza — `PC-4`, `PC-5`, `F-3` del Plan 136, `<PLAN-137>:PC-1`, `<PLAN-138>:PC-1`, `<PLAN-140>` — gasto de gobernanza sobre una regla que no puede fallar ni pasar. Este diseño la vuelve **determinable** por primera vez.

---

## A. Estado actual

### A.1 Lo que existe hoy, y qué función cumple realmente

| Artefacto | Función **real** hoy | Función **declarada** | Veredicto |
|---|---|---|---|
| `ROADMAP.md` (107 líneas) | Dirección **+ estado actual** (posición, versión publicada, trabajo activo) **+ horizonte** (`NOW`/`NEXT`/`LATER`) **+ grafo de dependencias** **+ tabla de bloqueos estratégicos** | EntryPoint: «comunicar visualmente la dirección de evolución y el camino de alto nivel» (`docs/CONVENTIONS.md:Contrato del ROADMAP`) | **Sobrecargado.** Es el único artefacto que el propio contrato prohíbe que sea backlog, changelog o registro de capacidades — y es, de facto, las tres cosas en pequeña escala |
| `docs/plans/` (174 archivos) | **Fuente de verdad del trabajo ejecutable.** Cada Plan declara alcance, autoridad, criterio de entrada, pasos, criterios de salida, verificación, anchor y checkpoint | «la decisión materializada: cómo, dónde y en qué orden exacto se ejecuta» | **Correcto y suficiente.** Es la entidad de trabajo del sistema; no hace falta otra |
| `docs/plans/INDEX.md` | Espejo mecánico verificable por `check_plan_structure.py` (174 filas, series, header de estado) | Registro/navegación, nunca autoridad (`AU-4`) | Correcto — pero su *header* es una narración de estado de 2.000+ caracteres que duplica `ROADMAP.md` y `CHANGELOG.md` |
| `docs/rfc/` (85) + `docs/adr/` (21) | La decisión y su racional; autoridad normativa | Gobernanza | Correcto |
| `CHANGELOG.md` (214 KB) | Historial de releases y de Changes docs-only (`[Unreleased]`) | EntryPoint | Correcto; es **historia**, no planificación |
| `docs/VERSIONING.md` | Versionado, ramas, batería canónica (§4.1), estados de planes (§7), snapshot de estado (§9), DoD (§10) | Policy | Correcto. §9 es la fuente de verdad de posición de release |
| `docs/CONVENTIONS.md` | Normativa: contrato del ROADMAP, Change Lifecycle, niveles `L0–L3`, impactos de cierre | Policy | Correcto, pero aloja dos reglas cuya determinabilidad depende del modelo que este informe propone |
| `.agents/` (6 archivos) | Interfaz operacional del agente DEV: workflow, autoridad, validación/cierre, checkers, autonomía | Operational layer | Correcto |
| `docs/working/audits/ETAPA_A_…md` (584 líneas) | **Evidencia de capacidades**: 28 capacidades × 9 dimensiones, 8 niveles de madurez, 0 en «demostrado bajo condiciones reales» | Working / analysis, no normativo | **Es la mejor pieza de planificación del repositorio — y está congelada.** Nadie la actualiza: es un snapshot fechado |
| `docs/working/{audits,research,proposals}/` + sus INDEX | Familias Working pre-canónicas, con registro de status | Working | Correcto. `proposals/` ya funciona como intake informal de ideas |
| `docs/glossary/terms.md` | Registro terminológico; entrada `ROADMAP` con **términos prohibidos** («no usar roadmap para designar un backlog, un changelog, un registro de capacidades o un decision register») | Inventory descriptivo | La prohibición existe y **viola** el artefacto que describe |
| `.project/` (gitignored) | Estado de sesión efímero: deliberación de dogfood, gobernanza de change, journal del orquestador | Efímero por diseño | Correcto — y explica por qué parte de la evidencia de `C-22`/`C-23` no sobrevive |
| `MASTER_PENDING_WORK_INVENTORY.md` | **Ya no existe en disco.** Fue un inventario externo untracked; sus ítems `HD-1`…`HD-12` fueron absorbidos por los Planes 141 y 143 | — | Buen ejemplo de idea nueva **sin** hogar: entró fuera del sistema y hubo que inventariarla aparte |
| `sessions/` (gitignored) | Staging de proyectos adoptantes externos (`BeaconRBX`, `HikariClub`) | — | Fuera de alcance, y **fuente de evidencia que la matriz de Etapa A declara no haber usado** |

### A.2 La capa GitHub, medida

| Mecanismo | Estado real |
|---|---|
| **Issues** | **0** (todas las combinaciones de estado). `has_issues = true`. La última actividad de intake por issue fue la era `B-1`…`B-8` (Plan 19) |
| **Pull Requests** | **0** (histórico completo). El trabajo va directo a `dev`; no hay ramas de feature por política (`docs/VERSIONING.md` §1) |
| **Milestones** | **0** |
| **Projects** | No inspeccionables: el token de `gh` no tiene `read:project` (error: *«your authentication token is missing required scopes [read:project]»*). `has_projects = true`. No hay **ninguna** referencia a un Project en el repositorio |
| **Labels** | Sólo los 9 por defecto de GitHub (`bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`). **Ninguna** usada para planificación |
| **CI** | `.github/workflows/check-protocol.yml` (batería canónica) y `publish-dist.yml`. **No** corren los gates de lifecycle `C-1`/`C-2`/`C-3` (declarado como límite en `C-27`) |
| **Repo** | Privado, cuenta personal (`roldriel`), default branch `master`, trabajo en `dev` |

**Conclusión dura:** la capa de planificación de GitHub está **completamente vacía y nunca fue usada**. La afirmación del usuario «si tienes acceso» se responde: hay issues/PRs/milestones medidos en 0, y Projects no es inspeccionable con el scope actual. Por lo tanto **no existe un modelo actual de GitHub que preservar o migrar**, y **no hay riesgo de duplicación con un estado preexistente**: cualquier diseño parte de cero.

### A.3 La distinción PROTOCOL / DEV, tal como está hoy

El repositorio hace esta distinción **bien** a nivel de payload y **mal** a nivel de planificación.

**Lo que está bien establecido:**

- **Hard boundary** (`AGENTS.md`, `.agents/AGENTS.md`): `protocol/.agents/` + `protocol/_AGENTS.md` es **payload como datos** — se lee y se edita como contenido, nunca se obedece. El desarrollo lo gobiernan el `AGENTS.md` raíz y la capa `.agents/`.
- **Vía de autorización** (RFC-56): Clase A (modelo/contratos) exige RFC `Accepted`; Clase B (mejora documental) plan `Aprobado para ejecución`; Clase C (mecánica) commit directo.
- **Prohibición explícita** (`AGENTS.md`, RFC-75 §«Dev vs Protocol»): **no se comparten** workflows, policies, state machines, artifacts ni skills entre DEV y Protocol; **no hay herencia automática**; los principios transferibles (revalidación ante continuidad, `persistir ≠ materializar`, separación evidencia factual / autoridad normativa) **quedan como principios, no como mecanismos**.
- **Un tercer régimen, el adopter lifecycle**: `protocol/.agents/harness/lifecycle*.py` implementa un ciclo de instalación/actualización/desinstalación del payload con alcance limitado. Su CLI expone **`install`, `update`, `uninstall`, `doctor` y `recover`** — es decir, materialización, actualización, retiro y recuperación — pero **no** `validate` ni `upgrade`: la verificación de forma del payload es de `gate_validator.py`/`hook_gate.py`, y la promoción de versión es de DEV. Es una tercera cosa, distinta de DEV y del protocolo en uso.

**Lo que está roto:**

- **La matriz de Etapa A etiqueta cada capacidad con un dominio** (`DEV` / `PROTOCOL` / `BOTH` / `UNKNOWN`) — 28 filas con `C-nn` como identidad. **Ese vocabulario no está canonizado en ninguna parte**: ni en `docs/CONVENTIONS.md`, ni en el glosario. Es una convención local de un documento Working, y `ROADMAP.md` la usa (`[PROTOCOL]`, `[DEV]`, `[BOTH]`) como si fuera normativa.
- **La lista de 28 mezcla dos cosas incompatibles.** `C-08 Agent Worker`, `C-10 Delegation`, `C-15 Placement`, `C-27 CI` son *plomería de DEV*: no son comportamiento observable de un adoptante. `C-16 Discovery`, `C-18 Protocol gates`, `C-20 EARS`, `C-22 Deliberation`, `C-23 Change Governance` son *comportamiento del producto*. La matriz lo resuelve con una columna `Dominio` —información insuficiente para planificar, porque un adoptante no «adopta» `C-15 Placement`— y `BOTH` es un cajón, no una clasificación.
- **La posición de release se declara en `ROADMAP.md`.** «Protocolo publicado: 12.0.0», «En `dev`: PATCH 12.0.1 implementado y sin tag». Eso duplica `docs/VERSIONING.md` §9, que es la fuente declarada, y **ambos pueden divergir** de Git. `docs/VERSIONING.md` §9 ya reconoce la regla («una divergencia frente a Git nunca se usa para inventar una versión»): el problema es que el ROADMAP la ignora.
- **`ROADMAP.md` declara «Trabajo activo: ninguno» mientras el worktree tiene 30 líneas de diseño de implementación de `F-C` sin commitear** en `docs/plans/165-f-c-autonomy-frontier-implementation.md` (`## Diseño de implementación (Fase 1)`, con las decisiones `ID-2`, `ID-4`, `ID-6`, `ID-7`, `ID-8` resueltas). Es un caso concreto y verificable de que el mapa no puede representar el estado real.

### A.4 Vocabulario de identidades que ya existe (y que hay que respetar)

El repositorio ya tiene un sistema denso de identificadores estables. Cualquier modelo nuevo debe **encajar**, no renombrar:

| Prefijo | Significado | Dueño |
|---|---|---|
| `F-A`, `F-B`, `F-C` | Fronteras de autonomía (tramos de trabajo) | `docs/adr/19`, `docs/CONVENTIONS.md` |
| `C-01`…`C-28` | Capacidades del alcance conceptual mínimo | `docs/plans/149`, matriz de Etapa A |
| `C-02`, `C-16`, `C-17`, `C-21`, `C-26` | Condiciones / brechas dentro de esa lista | Ídem |
| `OD-1`…`OD-7` | Open decisions | Planes 160–163 |
| `PC-n` | Pending decisions (por artefacto) | Plan dueño |
| `F-n` / `C-n` | Findings / corrections (namespace por artefacto) | Plan/RFC dueño |
| `HD-n` | Human decisions (inventario externo ya absorbido) | Planes 141/143 |
| `B-n`, `I-n` | Backlog evidenciado (histórico) | Plan 19 / `docs/plans/INDEX.md` |
| `FC-n`, `DC-n`, `ID-n`, `AE-n`, `D-n`, `Q-x`, `P-n`, `PR-n` | Criterios de cierre, premisas, decisiones de implementación, decisiones de autoridad | Planes 151–165 |

**Implicación de diseño:** no hace falta inventar un namespace de identidad para planificación. Hace falta **una capacidad declarada con estado objetivo**, y eso se puede expresar reutilizando `C-nn` y los nombres de frontera.

---

## B. Problemas

Distingo **problemas reales** (evidencia en el repositorio de que ya causaron daño) de **problemas hipotéticos** (riesgos plausibles sin daño observado).

### B.1 Problemas reales

**R-1 — `ROADMAP.md` es simultáneamente dirección y estado, y por eso se reescribe constantemente.**
Evidencia: tres Changes consecutivos sobre el mismo documento en nueve días — Plan 155 (reconciliación de estado), Plan 156 (reconciliación de layout), Plan 157 («reemplaza su estructura por una representación visual»), Plan 158 («reduce `ROADMAP.md` de 367 a 99 líneas aplicando *reduce, not reorganize*»), Plan 159 (retiro del envelope como «ya implementado»), Plan 161 (retiro de Etapa A como completada), Plan 163 (retiro de una fila `LATER`, entrada de `F-C` en `NEXT`), Plan 164 (retiro del blocker de autorización). **Siete ediciones del documento de dirección en ~3 semanas.** El Plan 158 lo dice explícitamente: el problema del Plan 157 fue que «mejoró la estructura formal pero **no logró que el ROADMAP sea inmediatamente legible como hoja de ruta**». La causa que el Plan 158 **no** atacó es la mezcla de ejes: redujo el tamaño, no separó dirección de estado.

**R-2 — No existe estado objetivo declarado para ninguna capacidad.**
Evidencia: la matriz de Etapa A tiene 9 dimensiones por capacidad (qué afirma, mecanismo, tests, dogfooding, condiciones probadas, condiciones no probadas, garantía demostrada, garantía sin demostrar, limitaciones) y **ninguna dimensión «estado objetivo»**. El repositorio sabe, para `C-16 Discovery`, que está `no demostrado`; **no sabe qué tendría que ser verdad para considerarla demostrada**. Consecuencia directa: `gap` no es computable; la priorización no puede justificarse contra un objetivo; `C-16`/`C-17`/`C-21` quedaron en `LATER` con la frase «su garantía depende de una adopción real» **sin criterio de terminación**.

**R-3 — El progreso no tiene unidad, y por eso se mide actividad.**
Evidencia: `docs/VERSIONING.md` §11 declara un *schema baseline* de métricas del Change Lifecycle y dice explícitamente «sin medición operacional hasta el Incremento 4». El Incremento 4 se materializó (Plan 98) con alcance mínimo: **C-1 y C-2 únicamente**, «no automatiza findings/corrections, pending, stale detection, series ni métricas». La matriz lo confirma en `C-24`: «0 registros = `not applicable`»; «sin serie ni agregación operacional». Por lo tanto la única unidad de progreso disponible hoy es **contar planes ejecutados** — exactamente «hicimos 17 issues». El conteo sí existe: 174 planes, 85 RFCs, y `ROADMAP.md` declara «no se cataloga aquí el trabajo cerrado».

**R-4 — La determinación `Roadmap impact` produce gobernanza sobre gobernanza.**
Evidencia: 27 planes contienen una determinación `Roadmap impact`, redactada en prosa y en al menos **ocho formas tipográficas distintas** (`**Roadmap impact:**`, `Roadmap Impact:`, `- **Roadmap impact (§5.2):**`, `Roadmap impact (§5.2 de …)`…). Su semántica obligó a abrir decisiones humanas: `<PLAN-136>:PC-4` («si una determinación `Roadmap Impact: REQUIRED` autoriza materializar en `ROADMAP.md` fuera del Scope»), `<PLAN-136>:PC-5` («qué ocurre cuando una determinación de cierre no puede satisfacerse dentro del Scope autorizado»), `<PLAN-136>:F-3` (violación real de scope por leer `Roadmap impact: REQUIRED` como autorización), `<PLAN-137>:PC-1`, `<PLAN-138>:PC-1`, y la reclasificación de `<PLAN-137>` de `REQUIRED` a `DEFERRED` en el Plan 140. La regla se escribió **porque** el mapa operativo tiene un dueño; cuando el dueño es prosa, cada aplicación requiere una interpretación nueva. Y no hay checker: `docs/CONVENTIONS.md` §«Determinaciones de cierre» lo declara: «no hay checker que interprete prosa ni que decida si un documento está actualizado, y no se agrega uno».

**R-5 — El estado operativo está duplicado en cinco lugares, con divergencia real.**
Evidencia: la posición de release y el trabajo activo aparecen en (1) `ROADMAP.md` §«Posición actual», (2) `docs/VERSIONING.md` §9, (3) `CHANGELOG.md`, (4) `docs/plans/INDEX.md` (header de estado), (5) el header `**Status:**` de cada plan. Los cinco pueden divergir. Divergencias observadas: `ROADMAP.md` declara «Trabajo activo: ninguno» contra 30 líneas de diseño de `F-C` sin commitear; `ROADMAP.md` declara «Payload publicado: `origin/dist` @ `1181db6`» mientras su propia nota advierte que «la ref local `dist` está rezagada»; `protocol/.agents/VERSION` = `12.0.1` sin tag mientras `docs/VERSIONING.md` §9 está fechado 2026-10-11 con release `12.0.0`; `docs/plans/INDEX.md` tiene un header que narra en un solo párrafo los Planes 136–165.

**R-6 — No hay intake evaluado: hay intake conversacional.**
Evidencia: cada Plan declara su `Origen` como «pedido directo del mantenedor», «directiva del mantenedor», «acto del mantenedor» o «consigna de intake». Los Planes 141 y 143 existen **para vaciar un inventario externo** (`MASTER_PENDING_WORK_INVENTORY.md`) que hoy ya no está en disco. El Plan 149 admite el patrón: su roadmap se materializó por «pedido directo del mantenedor (… 2026-09-22)». Consecuencia: **una idea se convierte en Plan en el mismo movimiento en que se enuncia.** No hay paso intermedio donde pueda ser rechazada, diferida o convertida en experimento; la única forma de decir «no» es no escribir el Plan. Y no hay registro de los rechazos: `ROADMAP.md` no tiene categoría `REJECTED`, y el glosario prohíbe que la tenga si es un backlog.

**R-7 — El vocabulario de dominio `DEV`/`PROTOCOL`/`BOTH` no está canonizado y mezcla niveles.**
Evidencia: `ROADMAP.md` usa `[PROTOCOL]`, `[DEV]`, `[BOTH]`, `[BOTH] LOW`; la matriz usa «DEV», «DEV + PROTOCOL», «PROTOCOL», «BOTH»; **`docs/CONVENTIONS.md` no define el vocabulario** y `docs/glossary/terms.md` no tiene entrada. Además la lista de 28 mezcla plomería DEV (`C-15 Placement`, `C-27 CI`) con comportamiento del producto (`C-16 Discovery`, `C-20 EARS`). El resultado es que «¿es esto PROTOCOL o DEV?» —la pregunta central del usuario— no tiene respuesta normativa.

**R-8 — La asimetría no está reconocida: el repositorio no tiene una «fase de definición estratégica» para el protocolo.**
Evidencia: la evolución del protocolo está gobernada con precisión (RFC-56, RFC-75, planes, anchors), pero **qué debe llegar a ser el protocolo** sólo se declara en tres lugares: la sección «Destino» de `ROADMAP.md` (3 párrafos), `ADR-19` (frontera de autonomía) y `docs/plans/149` (roadmap A→B→C). No hay modelo de capacidades del producto con estado objetivo, y la única retrotranspectiva integral que existe (Etapa A) se hizo **una vez** y quedó congelada como evidencia.

**R-9 — La numeración de planes y series es densa y su función estratégica es nula.**
Evidencia: «Nonagésima tercera serie», «Octogésima novena serie», «Sexagésima octava serie» — el `docs/plans/INDEX.md` organiza 174 planes en series numeradas en ordinales españoles que no expresan dirección, capacidad ni horizonte. `docs/CONVENTIONS.md` §«Serie e identidad derivada» aclara que la serie es **identidad derivada** y que las «Vigésima X serie» son «la vista descriptiva de batches de planes (numeración/registro)». Es decir: es registro, no planificación — pero ocupa el lugar donde un lector buscaría la planificación.

### B.2 Problemas hipotéticos (no observados; los declaro como tales)

| # | Hipótesis | Por qué no es un problema real hoy |
|---|---|---|
| H-1 | «La acumulación de roadmap (roadmap debt) nos desviará» | El Plan 158 redujo el documento a 107 líneas y el presupuesto visual está definido. No hay evidencia de acumulación actual; sí de **reescritura** (R-1) |
| H-2 | «Perderemos ideas nuevas por no tener un backlog» | El repositorio nunca perdió una idea por falta de tracker: `HD-1`…`HD-12` y `B-1`…`B-8` se resolvieron, y las pendientes tienen dueño por `PC-1`. El riesgo real es el inverso (R-6): **entra todo** |
| H-3 | «Necesitamos GitHub porque el mantenedor trabaja solo y no ve el estado» | `ROADMAP.md` + `docs/plans/INDEX.md` son legibles en un clon. El problema de visibilidad no está demostrado; el problema demostrado es de **determinabilidad** (R-4, R-5) |
| H-4 | «La falta de milestones impide saber cuándo termina una etapa» | Cierto en el fondo y falso en la forma: no falta un contenedor, falta un **estado objetivo** (R-2). La consecuencia se ve en `C-16`/`C-17`/`C-21`, sin criterio de terminación |
| H-5 | «El proceso de gobernanza es demasiado pesado y frena» | Parcialmente evidenciado (los 174 planes son densos) pero **no medido**. `C-24` establece que no hay telemetría operacional para afirmarlo. No lo convierto en problema real sin medición |

### B.3 Confusión PROTOCOL / DEV: síntesis

| Pregunta | Estado hoy |
|---|---|
| ¿Qué debe poder hacer ARgentOS y cómo debe comportarse al ser adoptado? | Respondido **parcialmente** y disperso: «Destino» de `ROADMAP.md`, `ADR-19`, `docs/plans/149`. Sin estado objetivo por capacidad |
| ¿Qué debemos investigar, diseñar, implementar, validar o corregir para que el PROTOCOL alcance ese estado? | Respondido **con precisión excesiva**: el Plan, con alcance, autoridad y criterios. Pero **sin vínculo declarado y verificable** a una capacidad del PROTOCOL |
| ¿Un Plan DEV puede justificar qué capacidad del PROTOCOL hace avanzar? | **No de forma verificable.** El campo `work_type` existe pero su propio criterio de admisión (Plan 152) cubre «artefactos obligatorios, gates, verificación, registro, cierre» — no capacidades. `P-5` sigue `GAP` «por caso» |

---

## C. Modelo propuesto

### C.1 Principio de diseño

> **Una sola fuente de verdad por concepto, y el repositorio es la fuente de verdad del estado del proyecto.**

Tres consecuencias operativas, que son el criterio con el que juzgo cada decisión posterior:

1. **Dirección y estado no comparten artefacto.** La dirección casi no cambia; el estado cambia en cada Change. Juntarlos garantiza reescrituras (R-1).
2. **Toda afirmación de estado debe ser determinable.** Un enunciado que no puede ser verificado por un humano con evidencia ni por un checker es prosa de gobernanza, y la prosa de gobernanza genera gobernanza sobre sí misma (R-4).
3. **No se crea una entidad si ya existe una que la expresa.** El «Decision-Making Compass» del `AGENTS.md` exige preguntar primero si el modelo existente puede expresar la necesidad.

### C.2 Los tres ejes y sus entidades

```text
EJE 1 · DIRECCIÓN        (intención humana; casi inmutable; normative-lite)
  D1  Destino            qué queremos que ARgentOS llegue a ser
  D2  Invariante de dirección   la restricción que ninguna decisión puede violar
  D3  Horizonte          NOW / NEXT / LATER  — qué iniciativas y en qué orden

EJE 2 · CAPACIDAD        (estado + evidencia; evoluciona con cada Change)
  P1  Capacidad PROTOCOL  qué comportamiento debe garantizar ARgentOS al ser adoptado
  P2  Estado de capacidad (actual → objetivo, gap, criterio de terminación, evidencia)
  P3  Milestone           resultado del PROTOCOL verificado (agrupación de capacidades)

EJE 3 · TRABAJO          (ejecución gobernada; efímero + histórico)
  W1  Iniciativa DEV = el Plan existente   (alcance + autoridad + criterios + evidencia)
  W2  Change              la unidad atómica: authorize → execute → verify → close → commit
  W3  Idea nueva          propuesta pre-canónica; NO es entidad persistente
  W4  Decisión rechazada / diferida   el registro de por qué no se hizo
```

**Ninguna entidad nueva del Eje 3.** `W1` es el Plan que ya existe; `W2` es el Change que ya existe; `W4` se expresa con lo que ya existe (`PC-n` para diferido; una sección de rechazos en el artefacto de registro).

### C.3 Qué representa cada entidad

| Entidad | Representa | Propósito | Persistente / temporal | Vive en |
|---|---|---|---|---|
| **D1 Destino** | El estado futuro deseado de ARgentOS y su criterio de éxito | Impedir que una decisión técnica sustituya a la dirección | Persistente (años) | Documentación (`ROADMAP.md` §Destino) |
| **D2 Invariante de dirección** | La restricción que ninguna decisión puede violar | Criterio de rechazo objetivo | Persistente | Documentación (p. ej. `Autonomy ⊆ Scope ∩ Authority`; «ninguna feature entra por disponibilidad tecnológica») |
| **D3 Horizonte** (`NOW`/`NEXT`/`LATER`) | Posición relativa de una iniciativa en el camino | Responder «¿qué ahora? ¿qué después?» sin comprometer fechas | Cambia poco | Documentación (`ROADMAP.md`) |
| **P1 Capacidad PROTOCOL** | Un comportamiento que un **adoptante** puede experimentar y que ARgentOS se compromete a proporcionar | Traducir el Destino a propiedades verificables del producto | Persistente (años) | Documentación |
| **P2 Estado de capacidad** | `actual → objetivo`, gap, criterio de terminación, evidencia, límites | Hacer el progreso medible y la priorización justificable | Cambia con cada Change | Documentación; **evidencia** puede ser Working |
| **P3 Milestone** | Un resultado del PROTOCOL verificado end-to-end | Punto de control de progreso real | Temporal (nace y cierra) | Documentación |
| **W1 Iniciativa DEV** | El Plan: qué, por qué, bajo qué autoridad, con qué criterios | Ejecutar y gobernar un cambio | Temporal (se cierra) | Repositorio (`docs/plans/`) |
| **W2 Change** | La unidad atómica de ejecución validada | Trazabilidad de punta a punta | Temporal → histórico | Repositorio (plan + commit) |
| **W3 Idea nueva** | Una propuesta que aún no es trabajo | Permitir que exista sin comprometer nada | **Temporal por diseño**; nunca persistente como entidad | Conversación; como máximo Working (`docs/working/proposals/`) |
| **W4 Rechazo / diferimiento** | El porqué de lo que no se hace | Proteger la dirección de la re-proposición infinita | Persistente como registro | Documentación (sección del artefacto dueño) |
| **Datos de planificación en GitHub** | **Vista derivada** del repo | Lectura cómoda, no autoridad | Regenerable | GitHub; **nunca fuente de verdad** |

### C.4 Relaciones

```text
D1 Destino ──define──▶ P1 Capacidades PROTOCOL
D2 Invariante ──restringe──▶ (cualquier decisión sobre P1 y W1)
D3 Horizonte ──ordena──▶ W1 Iniciativas DEV
P1 Capacidad ──tiene───▶ P2 Estado (actual→objetivo, gap)
P3 Milestone ──agrupa──▶ P1 capacidades y declara un resultado verificable
W1 Iniciativa ──avanza──▶ P2 Estado (declara qué capacidad y qué transición)
W2 Change ──compone──▶ W1 Iniciativa
W1 Iniciativa ──produce──▶ Evidencia ──actualiza──▶ P2 Estado
W3 Idea ──se evalúa contra──▶ P1 + D2 ──▶ W4 (rechazo/diferimiento) | W1 (trabajo) | Experimento
```

**Relación clave y hoy ausente:** `W1 → P2`. Un Plan DEV debe declarar **qué capacidad PROTOCOL (o qué capacidad DEV habilitante) hace avanzar y qué transición de estado produce**. Esa es la respuesta verificable a «¿por qué estamos haciendo cada cosa?». Sin ella, la trazabilidad es narrativa (`Origen:` + `Depende de:`), no estructural.

### C.5 Qué NO debe persistir

| Candidato | Veredicto | Razón |
|---|---|---|
| Un registro global de capacidades con estado por fila | **NO** | Sería un registry y un dashboard. `docs/AGENTS.md` y `AU-4` lo prohíben expresamente; el glosario prohíbe que el ROADMAP sea «un registro de capacidades» |
| Un tracker de issues como fuente de verdad | **NO** | Rompe clonabilidad, diffabilidad, revisión por PR y verificabilidad por checker (ver §G) |
| Un documento por capacidad | **NO** | 28 documentos para 28 capacidades es burocracia pura |
| Un backlog separado | **NO** | El backlog es la unión de (horizonte + estado de capacidad). No tiene entidad propia |
| Un estado `REJECTED` dentro de `ROADMAP.md` | **NO en el ROADMAP; SÍ como registro** | `ROADMAP.md` es dirección; un rechazo es un hecho histórico de decisión y vive en el artefacto que lo decidió |
| Fechas objetivo por capacidad | **NO** | El propio contrato del ROADMAP declara que «el horizonte es conceptual; las versiones aparecen sólo como referencia secundaria». Las fechas convierten planificación en estimación |

### C.6 Dónde vive cada cosa (resumen operativo)

| Información | Fuente de verdad | Vista derivada | Nunca |
|---|---|---|---|
| Destino, invariante de dirección, horizonte | `ROADMAP.md` | GitHub Project (lectura) | Changelog, plans |
| Capacidades PROTOCOL y su estado | Documento de estado de capacidad (ver §D) | GitHub Project (lectura) | `ROADMAP.md` como inventario |
| Trabajo ejecutable y su autoridad | El Plan (`docs/plans/`) | GitHub Issue (espejo, si se adopta) | Project como autoridad |
| Posición de release | `docs/VERSIONING.md` §9 + tags Git | — | `ROADMAP.md`, INDEX |
| Registro de planes/RFCs/ADRs | Los INDEX | — | Cualquier otro documento |
| Historia de lo publicado | `CHANGELOG.md` + tags | GitHub Releases (si se adopta) | Plans |
| Decisiones y su racional | RFC / ADR | — | Project fields |
| Por qué no se hizo algo | Registro de rechazos en el artefacto dueño | — | Un Project column |
| Evidencia factual | Git + tests + checkers + anchors | — | Prosa |

---

## D. PROTOCOL

### D.1 El problema del modelo actual de capacidades

La matriz de Etapa A es **evidencia excelente** y **un mal modelo de planificación**. Lo es por tres razones concretas:

1. **No tiene estado objetivo.** Nueve dimensiones, ninguna dice «qué tendría que ser verdad para que esto esté terminado».
2. **Su nivel de abstracción mezcla implementación y producto.** `C-15 Placement` es un mecanismo DEV; un adoptante no lo «recibe». Un modelo de protocolo debe expresar **lo que el adoptante experimenta**.
3. **Es un snapshot congelado.** Fue producto de un Plan `Closed`; su valor como evidencia es histórico y su valor como estado caduca en el primer Change que lo contradiga. Sin embargo `ROADMAP.md` lo usa como si fuera estado corriente (`C-16`/`C-17`/`C-21` en `LATER` con la justificación «dependen de una adopción real»).

### D.2 Cómo debería representarse la evolución del PROTOCOL

**Dos capas, explícitas, nunca fusionadas.**

#### Capa P — Capacidades PROTOCOL (el producto)

Una capacidad PROTOCOL es **un comportamiento que un adoptante puede experimentar**. Se enuncia en el idioma del adoptante, no del repositorio. Se declara como:

```text
P-<n> <Nombre>
  Afirmación       qué puede afirmar ARgentOS que hace el sistema, en términos
                   observables por el adoptante
  Estado actual    uno de los niveles de madurez YA EXISTENTES en la matriz de
                   Etapa A (8 valores, vocabulario cerrado; no se inventa otro)
  Estado objetivo  el nivel que la dirección exige, y el criterio de terminación
  Gap              la diferencia actual→objetivo, en una frase
  Evidencia        tests/checkers/dogfoods/anchors que sostienen el estado actual
  Condición de      qué volvería a bajar el nivel (invalidación, no reapertura)
  invalidación
  Límites          lo que esta capacidad NO garantiza
```

**Sobre los once comportamientos que el usuario propuso evaluar.** Los evalúo contra la evidencia real del repositorio, y **rechazo dos como capacidades de nivel P**:

| Comportamiento propuesto | Veredicto | Fundamento |
|---|---|---|
| Comprensión y alineación de intención | **Sí, nivel P** | `H11-intent-reflection`, `INTENT_REFLECTION.md`, `INTENT_CONFIDENCE.md`, `intent-detector`, `ambiguity-detector`. Comportamiento observable del adoptante |
| Completitud de contexto | **Sí, nivel P** | `CONTEXT_ARTIFACT`, `H02`/`H03`, `completeness-checker`, discovery. Es la afirmación más fuerte del protocolo |
| Planificación autónoma | **No como P separada** | El protocolo **no** planifica por el usuario: produce un `EXECUTION_PLAN` autorizable. Llamarlo «autónoma» sobre-declara. Se expresa como **ejecución gobernada** + **plan explícito** |
| Judgment / crítica | **Sí, como propiedad transversal, no como capacidad** | `critic`, `self-review`, `adversarial-deliberation`, `tradeoff-analyzer`, `rubric-checker`. Es una **clase de garantía** (dependiente de juicio del agente, ya clasificada en el catálogo de garantías de D0), no una capacidad del producto |
| Ejecución gobernada | **Sí, nivel P** | `EXECUTION_PLAN` + `effects` + `AUTHORIZATION.md` + `PROTOCOL_BOUNDARIES.md`. Es el corazón del protocolo |
| Validación | **Sí, nivel P** | `VERIFICATION_REPORT`, `H06`, `evidence` classes (D4). Separable de auditoría |
| Auditoría independiente | **Sí, pero con una salvedad crítica** | El catálogo de garantías ya declara «Independencia de verificación: **Dependiente de actores externos** — sólo multi-agent; en single-instance se declara atestación». Es capacidad P **condicionada**: su estado objetivo máximo es «declarada», no «garantizada» |
| Memoria | **Sí, con nivel bajo** | `MEMORY_SYSTEM.md`, `runtime/memory/`. Pero es entrada `F-C` como **contexto**, y `AE-8` prohíbe que sea premisa de derivación o autoridad |
| Comprensión del proyecto | **Sí, nivel P** | Es Discovery más KB: `C-16`/`C-17`, `no demostrado`. La capacidad con el gap más grande del protocolo |
| Trazabilidad | **Sí, nivel P** | `CHANGE_GOVERNANCE.md`, `HARNESS_REPORT`, `METRICS`, `SESSION_LOG`. Ya existe y está `testeado` |
| Autonomía apropiada | **No como capacidad; sí como restricción de dirección** | `Autonomy ⊆ Scope ∩ Authority` es un **invariante** (D2), no una capacidad. Y el usuario mismo advierte «no asumir que más autonomía siempre es mejor» — convertirlo en capacidad invitaría justo a eso |

**Resultado: 8 capacidades de nivel P** (más las derivadas de la lectura del payload: distribución/sincronización y configuración declarada por flags), no 28.

#### Capa D — Capacidades habilitantes DEV (el repositorio)

Las 28 `C-nn` de la matriz **no se tiran**: se re-clasifican como **capacidades habilitantes DEV**. No son lo que el adoptante recibe; son **cómo este repositorio construye, valida y publica** lo que el adoptante recibe. Una capacidad DEV se declara con lo que ya tiene (afirmación, mecanismo, evidencia, límites) **más** una sola línea nueva: **qué capacidad P habilita**.

```text
C-01 Change Lifecycle (DEV)   ──habilita──▶  P-05 Ejecución gobernada, P-11 Trazabilidad
C-04 Validation / Closure     ──habilita──▶  P-06 Validación, P-11 Trazabilidad
C-16 Discovery                ──habilita──▶  P-09 Comprensión del proyecto, P-10 ...
```

**Por qué esta separación resuelve el problema del usuario:** responde literalmente a «¿qué debe poder hacer ARgentOS?» (capa P, decenas de líneas, estable) y a «¿qué debemos hacer para lograrlo?» (capa D, existente, ya evidenciada), sin que una invada a la otra ni obligue a mantener 28 fichas.

### D.3 Qué NO debe ser una capacidad PROTOCOL

- **Un mecanismo** (`C-15 Placement`, `C-19 enforced mode`, `C-25 Feature flags`, `C-28 dist`). Los flags y `dist` no son comportamiento del adoptante, son **canales de entrega y configuración**: se declaran como **capacidades DEV** o como **condiciones de despliegue**, no como promesas del protocolo.
- **Una técnica interna** (`C-14 Prompt Cache`). Es una optimización que depende del proveedor; su garantía no es de ARgentOS (`dependiente de una condición externa`).
- **Un componente** (`C-09 WorkerResult`, `C-10 Delegation`). Son contratos; su existencia es condición de otras capacidades.
- **Una garantía** (independencia de verificación, ausencia de alucinación). Las garantías son **clase** (`declarativa`, `verificable`, `mecánicamente enforceada`, `dependiente del juicio`, `dependiente de actores externos` — ya definidas en D0) y viven **dentro** de una capacidad, no al lado.
- **Una etapa de planificación** (`F-C`, Etapa B). Una etapa es **agrupación de trabajo** (horizonte), no capacidad. La matriz lo confirma: `F-C` está definida por capacidades y condiciones (`C-02`, `C-26`, Memory, actor real), no es una capacidad en sí.

### D.4 Cómo se mide la evolución del PROTOCOL

**La unidad de evidencia no cambia:** sigue siendo la evidencia ejecutable (tests, checkers, dogfoods anclados, validation anchors). **Lo que cambia es la unidad de progreso:** de «planes ejecutados» a **«capacidad pasó de nivel A a nivel B, con esta evidencia»**. Ver §I.

---

## E. DEV

### E.1 No hace falta una entidad «Iniciativa DEV»

Ya existe, y es mejor de lo que una entidad nueva sería. El **Plan** tiene: `Status`, `Change Level`, `RFC`, `Clase`, `Depende de`, `Origen`, `Objetivo`, `premises(D)` (`P-1`…`P-8`), `Criterio de entrada`, `Alcance` (`IN SCOPE`/`OUT OF SCOPE`), `Entregables`, `Pasos`, `Efectos declarados`, `Criterios de salida`, `Verificación`, `Validation anchor`, `Checkpoint / cierre`, `Findings`, `Correcciones`, `Pending decisions`, `Riesgos`, `Trazabilidad`.

Eso **es** una iniciativa con gobernanza, autoridad, evidencia y cierre. Reemplazarlo por una entidad «Initiative» en un Project sería sustituir un artefacto revisable por un campo de texto.

### E.2 Lo que falta en la capa DEV: una obligación de declaración

Un Plan DEV debe poder responder «¿qué capacidad hace avanzar?». Hoy no puede. La propuesta es **un campo, con una regla de admisión estricta**:

```text
**Avanza:** P-<n> [→ nivel objetivo]  |  C-<nn> [→ nivel objetivo]  |  —
```

Reglas (diseñadas para no repetir el error de `Roadmap impact`, R-4):

1. **Determinable o nada.** Debe nombrar una capacidad declarada y, si aplica, el nivel objetivo. Si el Change no avanza ninguna capacidad (limpieza, corrección histórica, tooling interno, release), se declara `—`. **`—` es una respuesta válida y frecuente**, no un fracaso.
2. **Sin consecuencia de autoridad.** Declarar `Avanza:` **no** autoriza nada, **no** amplía el `Scope` y **no** obliga a actualizar ningún otro documento. La lección de `<PLAN-136>:F-3` es directa: la determinación no es autorización.
3. **Verificable mecánicamente.** A diferencia de `Roadmap impact`, esta declaración **sí** puede tener checker: el identificador de capacidad debe existir en el documento de capacidades, y el nivel objetivo debe pertenecer al vocabulario cerrado de 8 niveles. Sin interpretación de prosa.
4. **Se registra en el header del Plan**, no en el cierre. El cierre ya tiene dos determinaciones; una tercera lo empeoraría.

### E.3 Ciclo de vida del trabajo DEV (ya existente; se conserva íntegro)

```text
Plan (Aprobado para redacción)
   ↓
Autorización humana → Plan (Aprobado para ejecución)
   ↓
Ejecución en `dev` → evidencia mientras se ejecuta
   ↓
Validación + Validation anchor (A1)
   ↓
[Finding → Corrección → Revalidación (A2)]     ← circuito de reparación
   ↓
Checkpoint + consistencia checkpoint↔anchor
   ↓
Closed (derivado) — Executed ≠ Committed ≠ Closed ≠ Released
   ↓
Commit atómico en `dev` → (si hay payload) promoción a `master` + tag → `dist`
```

**Esto no se toca.** Es correcto, está probado en 174 planes y está verificado por `C-1`/`C-2`/`C-3`.

### E.4 Qué se agrega a la capa DEV

| Agregado | Propósito | Coste |
|---|---|---|
| Campo `Avanza:` en el header del Plan | Vínculo verificable trabajo → capacidad | 1 línea por Plan; checker reutilizable |
| Una sección de **rechazos** en el artefacto de registro de dirección | Registrar por qué algo no se hizo, sin crear backlog | 1 sección; sin maquinaria |
| Un **Milestone** cuando la dirección lo exija (ver §F/§I) | Punto de control de progreso real | 1 documento por milestone; nace con la autorización de su trabajo |
| **Ningún** campo de prioridad numérica | La prioridad es **orden en el horizonte**, no un número comparable | Evita falsa precisión |

---

## F. Priorización

### F.1 El problema que hay que resolver

> «Se nos ocurrió una feature interesante» **no** debe convertirse automáticamente en «ahora debemos construirla».

La causa de que hoy ocurra (R-6) es que **no hay una etapa entre la idea y el Plan**. El Plan 149 lo expresa sin querer: «pedido directo del mantenedor → se materializa en `ROADMAP.md`». La idea y el compromiso son el mismo acto.

### F.2 Los estados de decisión: sólo cuatro, y ya existen

No invento una taxonomía nueva. La evalúo contra lo que el repositorio **ya usa**:

| Estado propuesto por el usuario | Veredicto | Cómo se expresa |
|---|---|---|
| `NOW` | **Se conserva** (ya existe en `ROADMAP.md`) | Horizonte `NOW` |
| `NEXT` | **Se conserva** (ya existe) | Horizonte `NEXT` |
| `LATER` | **Se conserva** (ya existe) | Horizonte `LATER` |
| `EXPERIMENT` | **Se conserva como atributo, no como horizonte** | Un experimento **está** en `NOW` o `NEXT`; su diferencia es que **no promete una capacidad**: promete *conocimiento*. Su criterio de terminación es «la pregunta quedó respondida», no «la capacidad subió de nivel» |
| `DEFERRED` | **Se conserva como atributo** | `LATER` **+** una `PC-n` con dueño (mecanismo `PC-1` ya existente) + la condición que lo desbloquea |
| `REJECTED` | **Se conserva, pero como registro histórico fuera del ROADMAP** | Una sección de rechazos en el artefacto que decidió, con la razón. **Nunca** una columna del mapa |

**Resultado: el vocabulario de decisión se reduce a `NOW`/`NEXT`/`LATER` (horizonte) + `EXPERIMENT` (atributo de propósito) + `DEFERRED` (atributo con dueño) + `REJECTED` (hecho histórico).** Cinco estados, de los cuales **tres ya existen** y dos son atributos con mecanismo preexistente.

### F.3 El filtro de admisión (obligatorio, previo a cualquier decisión)

Un filtro de preguntas, no un formulario. El objetivo es que **rechazar sea fácil y barato**, porque hoy es imposible.

```text
IDEA NUEVA
  │
  ├─ Q1. ¿Qué problema resuelve?          Si no hay problema observable y verificable
  │                                        → REJECT (o EXPERIMENT si la pregunta es legítima)
  │
  ├─ Q2. ¿A qué capacidad P o D pertenece? Si no pertenece a ninguna capacidad declarada:
  │                                        → o la capacidad falta (propuesta de capacidad: decisión
  │                                          HUMANA) o la idea está fuera del modelo → REJECT
  │
  ├─ Q3. ¿Acerca una capacidad a su        Si no mueve ningún estado objetivo declarado:
  │      estado objetivo?                    → REJECT (no LATER: LATER es para lo que sí mueve,
  │                                            sólo que después)
  │
  ├─ Q4. ¿Viola el invariante de dirección? Si sí → REJECT, con la razón citada
  │      (§C: p.ej. «autonomía ⊆ scope ∩ authority»,
  │       «ninguna feature entra por disponibilidad tecnológica»)
  │
  ├─ Q5. ¿Bloquea o desbloquea trabajo      Si desbloquea trabajo en curso → candidato a NOW
  │      existente?                          Si bloquea sin resolverlo → REJECT
  │
  ├─ Q6. ¿Fortalece una garantía o sólo     Sólo "más capacidad" no basta: la dirección de
  │      agrega superficie?                  ARgentOS es claridad y calidad de decisión, no
  │                                           acumulación de mecanismos (Decision-Making Compass)
  │
  ├─ Q7. ¿Es una pregunta abierta o una     Pregunta → EXPERIMENT (en NOW o NEXT, con la pregunta
  │      respuesta conocida?                  como criterio de terminación)
  │
  └─ PRIORIZACIÓN
        │
        ├─ NOW     mueve una capacidad del milestone activo o desbloquea trabajo en curso
        ├─ NEXT    mueve una capacidad objetivo, sin urgencia de secuencia
        ├─ LATER   mueve una capacidad objetivo, pero depende de otra cosa
        │           (+ PC-n con dueño si el desbloqueo no está disponible → DEFERRED)
        └─ REJECT  no mueve estado objetivo, viola el invariante, o no hay problema real
                    → se registra la razón y se cierra. NO se re-abre sin condición
                       de reapertura explícita (regla «Evidence closure / anti-rework»)
```

### F.4 Cómo una idea nueva puede alterar el plan existente

Cuatro respuestas posibles, y **ninguna es automática**:

| Efecto | Cuándo | Qué ocurre | Quién decide |
|---|---|---|---|
| **Entra inmediatamente** | Desbloquea trabajo en curso, o cierra un gap del milestone activo | Entra en `NOW`; el horizonte `NEXT` se corre. Exige re-derivación del alcance del milestone (`HD-K1`/R-4 ya vigente) | Humano |
| **Desplaza trabajo existente** | Está mejor justificada contra el estado objetivo que un ítem actual | El ítem desplazado baja de horizonte **con su razón registrada**. No se borra: el `Roadmap impact: REQUIRED` de ese Change lo reconcilia | Humano |
| **Queda pendiente** | Mueve una capacidad objetivo pero sin urgencia | `LATER`, o `NEXT` si su turno llega | Humano; el agente propone |
| **Se descarta** | No mueve estado objetivo, viola el invariante, o no hay problema real | Se registra la razón en el registro de rechazos del artefacto dueño, con la condición que lo reabriría | Humano; el agente propone y **nunca** decide solo |

### F.5 Regla operativa que evita el fallo

> **Una idea nueva no crea trabajo. Sólo una decisión humana crea trabajo.**

Y su consecuencia de diseño, que es la pieza que hoy falta:

> **Una idea nueva tampoco crea un Plan.** El Plan se crea en la autorización (paso §2 del Change Lifecycle), nunca en la enunciación. La idea vive en la conversación o, si necesita persistir, en `docs/working/proposals/` — donde ya existe un INDEX con status y donde nada es normativo.

### F.6 El rol correcto de GitHub en el intake

Hay un uso de GitHub que **sí** aporta y que no rompe nada: los issues como **buzón de captura de ideas**, no como fuente de verdad. Una idea puede llegar como issue desde el móvil; el issue **no es autoridad** ni estado. El flujo es:

```text
Issue (captura, cualquiera escribe)     ← NO autoridad, NO estado
   ↓  (evaluación humana + agente, con el filtro F.3)
Decisión: NOW / NEXT / LATER / EXPERIMENT / REJECTED
   ↓
REJECTED → razón registrada en el REPOSITORIO (no sólo issue cerrado)
           el issue se cierra con puntero al registro
ACEPTADA → el ítem entra en el horizonte del ROADMAP (si es ítem de dirección)
           o en el estado de capacidad (si mueve una capacidad)
           + Plan creado SOLO en la autorización
```

**Advertencia explícita:** un issue cerrado **no** es un registro de rechazo. GitHub no es un archivo. Si la razón del rechazo sólo vive en un issue, se pierde con el repo, con el token y con la migración de cuenta. Por eso el rechazo se registra en el repositorio.

---

## G. GitHub Projects

### G.1 Procedimiento y hallazgo previo

Evalué primero las capacidades reales de GitHub y luego el encaje. **Antes de eso, un hallazgo que cambia el marco:** la capa GitHub está **vacía** (0 issues, 0 PRs, 0 milestones; Projects no inspeccionable con el scope actual, y **ninguna referencia a un Project en el repositorio**). No hay nada que migrar, nada que preservar y ningún riesgo de duplicación con estado preexistente. Cualquier decisión es de diseño puro.

### G.2 Lo que GitHub puede y no puede hacer (relevante para este repositorio)

| Necesidad de ARgentOS | ¿GitHub puede? | Detalle |
|---|---|---|
| Estado del proyecto clonable con el repo | **No** | Issues, milestones y Project fields viven en la base de datos de GitHub. `git clone` no los trae |
| Estado diffeable y revisable por PR | **No** | No hay diff de un Project field. No hay revisión por pares del estado |
| Verificación por checker en CI | **No** | La API requiere token con `read:project`; CI no puede validar campos de proyecto contra el repo de forma barata ni determinista. Un `Project` no participa de la batería canónica |
| Trazabilidad anclada (`Validation anchor`, `Scoped Content Identity`) | **No** | Imposible expresar identidad de contenido scoped en un field |
| Vista cómoda de muchos ítems con filtros y agrupación | **Sí** | Es su fortaleza real |
| Relaciones tipadas (`blocked by`, sub-issues) | **Sí** | Sub-issues y dependencias existen (con límite de profundidad de anidamiento) |
| Automatización (auto-add, auto-archive, item cerrado) | **Sí** | Workflows integrados; requieren plan/visibilidad adecuados |
| Ser la fuente de verdad sin duplicación | **No** | El repo ya tiene la verdad en Markdown; GitHub sería un segundo lugar donde el mismo hecho puede quedar desactualizado |
| Acceso desde el móvil | **Sí** | El valor más real para un mantenedor solo |
| Independencia del proveedor | **No** | Todo el estado de planificación quedaría en un servicio externo privado |

**El criterio decisivo** no es «qué tan bueno es Projects», sino que este repositorio tiene una propiedad constitutiva: **todo su proceso de gobernanza está construido sobre la premisa de que el estado es contenido versionado y verificable** (`Scoped Content Identity`, `Validation anchor`, `checkpoint↔anchor`, checkers sobre el corpus real, RFC-46 sobre no reescribir historia). Poner el estado operativo en un Project **rompe esa premisa** y crea exactamente el problema que el repositorio pasó 174 planes resolviendo.

**Segundo criterio, específico y verificable:** el token actual de `gh` **no tiene `read:project`** y falla con `your authentication token is missing required scopes [read:project]`. Es decir: **hoy ni siquiera es posible leer un Project por API**. Adoptarlo como mecanismo operativo principal exigiría ampliar el scope del token, lo que a su vez introduce una dependencia operativa que el repositorio hoy no tiene.

### G.2b Mecánica concreta para una cuenta personal privada (verificado)

Esto condiciona el análisis para **este** repositorio concreto (privado, cuenta personal `roldriel`), no para GitHub en general.

| Hecho | Verificación | Consecuencia |
|---|---|---|
| **Los «user projects» existen** y pueden trackear issues y PRs de los repositorios de la cuenta personal | [GitHub Docs — Creating a project](https://raw.githubusercontent.com/anthonysidesapps/docs/2a0fd5d3ea1301bd6b3eca87c960856c08387bb9/content/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project.md): «User projects can track issues and pull requests from the repositories owned by your personal account» | **No hay un bloqueo de cuenta personal.** Un Project es posible |
| **No existe un Project «a nivel de repositorio»** para una cuenta personal: los proyectos son de la organización o del usuario. «Adding your project to a repository» es un **vínculo**, no un cambio de dueño | Ídem (solo hay secciones «organization project» y «user project»); [Community Discussion #193246](https://github.com/orgs/community/discussions/193246) sobre transferencia de un Project a un repositorio | `has_projects = true` en el repo **no** significa que exista un Project del repo. No existía ninguno, consistente con lo medido |
| **`gh` exige el scope `read:project`** y falla sin él | Medido: `gh project list --owner roldriel` → *«your authentication token is missing required scopes [read:project]»* | Hoy **no es posible leer** un Project por API con el token actual |
| **Un proyecto de usuario requiere un PAT clásico con scope `project`** (más `repo` si contiene ítems de repositorios privados). Los fine-grained PAT cubren proyectos **de organización** con permiso `Organization permissions → Projects: Read and write` — no hay permiso de Projects a nivel de usuario | [gh-aw — Authentication (Projects)](https://raw.githubusercontent.com/github/gh-aw/b527a7cb50f386594a8a5be5d9576fb99105953d/docs/src/content/docs/reference/auth-projects.mdx) | Automatizar implicaría un **PAT clásico con scope amplio** (`project` + `repo`), no un token de permisos finos |
| **El `GITHUB_TOKEN` de Actions es repository-scoped y no puede leer ni escribir Projects** — «any workflow step that reads project fields or writes updates must supply a token with explicit Projects permissions» | Ídem | **Cualquier automatización repo → Project requiere un secreto con un PAT de scope amplio.** Y una automatización GitHub → repo sería peor: escritura en el repositorio con un token de scope amplio |

**Esto refuerza la recomendación, con un argumento que no había considerado al inicio:** adoptar un Project no sólo añade una vista; **añade un secreto con permiso amplio** (`project` + `repo`) que hoy el repositorio no necesita, y lo necesita **precisamente** para la dirección de sincronización que el diseño debe evitar. El coste no es la configuración del tablero: es una dependencia de credenciales.

### G.3 Las tres opciones

#### Opción A — Un único Project con separación explícita PROTOCOL/DEV

```text
Project: ARgentOS
  campo Domain: PROTOCOL | DEV | BOTH
  campo Capability: C-01…C-28 | P-01…P-08
  campo Horizon: NOW | NEXT | LATER
  campo Status/Evidence
  vistas: PROTOCOL (filtro Domain = PROTOCOL), DEV, Milestone, Rejected
```

| Ventajas | Desventajas / riesgos |
|---|---|
| Una sola superficie; sin salto entre contextos | Un solo punto de duplicación con todo el repo |
| Relaciones PROTOCOL↔DEV visibles en una vista | `Domain` como campo reintroduce el vocabulario no canonizado (R-7) |
| Menos configuración que dos Projects | Riesgo alto de que el Project se vuelva el backlog que el contrato del ROADMAP prohíbe |
| — | Un Project no puede expresar `Validation anchor` ni estado objetivo por capacidad |

#### Opción B — Dos Projects (`ARgentOS Protocol` + `ARgentOS DEV`)

| Ventajas | Desventajas / riesgos |
|---|---|
| Separación física de los dos dominios | **Duplicación estructural:** el mismo trabajo aparecería en el Project DEV y su capacidad en el Project Protocol; mantener la correspondencia es trabajo manual |
| Cada Project con sus campos propios | Dos lugares donde el estado puede quedar obsoleto en vez de uno |
| Frontera visible | La distinción PROTOCOL/DEV **no requiere dos tableros**: requiere **un modelo de dos capas** (que es la §D). Dos tableros no crean la separación: la representan, y mal, porque pierden el vínculo |

**Veredicto: B es peor que A.** La separación PROTOCOL/DEV es una **relación** (capacidad P ← habilitada por capacidad D ← avanzada por Plan). Dos Projects separados **destruyen precisamente esa relación**, que es la que el usuario necesita para responder «¿por qué estamos haciendo cada cosa?».

#### Opción C — Repositorio autoritativo + Project derivado (recomendada)

```text
REPOSITORIO (fuente de verdad)                     GITHUB (vista derivada, opcional)
  ROADMAP.md            dirección + horizonte ──┐
  <estado de capacidad> capacidades y gaps    ──┤──▶  Project: vista de lectura
  docs/plans/           trabajo y autoridad   ──┘     (sincronización unidireccional
  docs/plans/INDEX.md   registro                      repo → GitHub; jamás al revés)
  Issues                buzón de captura de ideas (no autoridad)
```

| Ventajas | Desventajas / coste |
|---|---|
| **Cero duplicación de autoridad:** GitHub nunca decide | Requiere un paso de sincronización (un script o una acción) |
| El estado sigue siendo clonable, diffeable, revisable y verificable | La vista puede quedar desactualizada entre sincronizaciones — pero **eso no corrompe la verdad** |
| Se puede **no adoptar** GitHub y el sistema sigue completo | Si se adopta, hay que mantener el script |
| El Project puede descartarse sin tocar la gobernanza | — |
| El intake por issue funciona sin otorgar autoridad al issue | — |
| No exige ampliar el scope del token para el sistema funcionar | Leer el Project sí lo exige; **escribirlo** desde el repo también |

### G.4 Estructura recomendada (Opción C en detalle)

**Qué debería ser un Project:** una **vista de lectura** con dos usos concretos y nada más — (1) ver el estado de las capacidades y del horizonte en el móvil; (2) ver los ítems del milestone activo con sus dependencias. **No** es fuente de verdad, **no** es backlog, **no** es autoridad.

**Qué debería ser un Milestone de GitHub:** **nada, en el modelo recomendado.** El Milestone de GitHub es un contenedor de issues con fecha opcional y progreso calculado por conteo — exactamente las tres cosas que el Milestone de ARgentOS **no** es (§I.3). Si en algún momento se quiere la vista de progreso nativa, se **proyecta** el milestone documental como Milestone de GitHub, con dueño declarado como vista derivada.

**Qué debería ser un Issue:** **un buzón de captura de ideas**, opcional. Nunca estado, nunca autoridad, nunca registro de rechazo. Si el mantenedor prefiere no usar issues, el sistema funciona igual: las ideas entran por conversación.

**Qué debería ser un PR:** en este repositorio **no hay PRs y la política prohíbe ramas de feature** (`docs/VERSIONING.md` §1: «all work happens directly on the `dev` branch; feature branches are never created»). **Ninguna decisión de planificación debe introducir PRs.** Si GitHub se adopta, los PRs no forman parte del modelo.

**Qué debería permanecer en documentación (nunca en GitHub):**
- Destino e invariante de dirección.
- Estado actual y objetivo por capacidad, con su criterio de terminación.
- Definición de milestone, sus criterios de entrada/salida y su evidencia.
- Toda decisión y su racional (RFC/ADR).
- Alcance y autoridad de un Plan.
- Estado de release.
- **Razones de rechazo.**

**Campos personalizados necesarios (si se adopta el Project):**

| Campo | Tipo | Valores | ¿Fuente? |
|---|---|---|---|
| `Capacidad` | single select | `P-01`…`P-08`, `C-01`…`C-28` | Derivado |
| `Nivel` | single select | Los **8 niveles ya existentes** de la matriz de Etapa A | Derivado |
| `Horizonte` | single select | `NOW` / `NEXT` / `LATER` | Derivado de `ROADMAP.md` |
| `Milestone` | text o Milestone nativo | Nombre del milestone | Derivado |
| `Autoridad` | single select | `RFC Accepted` / `Plan aprobado` / `Clase C` / `— (no autorizado)` | Derivado: responde «¿puedo ejecutarlo ya?» |
| `Propósito` | single select | `Capacidad` / `Experimento` / `Evidencia` / `Mantenimiento` | Derivado |

**Ningún campo con autoridad.** Ningún campo numérico de prioridad. Ningún campo que no pueda regenerarse desde el repo.

**Vistas útiles (máximo 4, no más):**
1. **Milestone activo** — los ítems del milestone en curso, agrupados por capacidad, con sus bloqueos.
2. **Capacidades y gaps** — una fila por capacidad P/D con `Nivel` y `Horizonte`; responde «¿qué tenemos, qué falta?».
3. **Ahora** — horizonte `NOW` únicamente; la vista que se abre todos los días.
4. **Sin autoridad** — ítems en `NEXT`/`LATER` sin autorización: responde «¿qué está esperando una decisión humana?».

**Automatizaciones convenientes (todas repo → GitHub, ninguna al revés):**
- Al crear/actualizar un ítem en el repo, actualizar o crear el ítem del Project (por identificador `Plan NN` / `P-n` / `C-nn`).
- Al cerrar un Plan (`Closed`), mover el ítem a `Done` **y** registrarlo en el estado de capacidad **en el repo** en el mismo Change.
- **Nunca** una automatización que escriba en el repositorio desde GitHub. Esa dirección es la que crea fuentes de verdad dobles.

**Qué NO debería colocarse en GitHub (lista explícita):**
- Alcance, autoridad o `IN SCOPE`/`OUT OF SCOPE` de un Plan.
- `Validation anchor`, `Scoped Content Identity`, checkpoint.
- Findings (`F-n`), correcciones (`C-n`), pending decisions (`PC-n`).
- Estado de release, tags, versiones.
- Razones de rechazo.
- Cualquier cosa que un checker deba verificar.

### G.5 Recomendación y umbral de adopción

**Recomiendo la Opción C, y con una condición de entrada explícita:** adoptar el Project **sólo si** se cumple al menos una de estas dos condiciones, medidas y no supuestas:

1. **Existe fricción de lectura demostrada** — el mantenedor no puede responder «¿qué está en `NOW` y qué lo bloquea?» leyendo el repo en menos de un minuto, dos veces en un mes. (Hoy `ROADMAP.md` tiene 107 líneas y `NOW` tiene un ítem: la fricción no está demostrada.)
2. **El milestone activo supera los ~12 ítems** y su seguimiento en Markdown se vuelve incómodo.

**Coste verificado de adoptarlo (no es cero, y es mayor de lo que parece):** un Project de usuario exige un **PAT clásico con scope `project`** (más `repo` para ítems de repositorios privados), porque no existe permiso de Projects a nivel de usuario en los fine-grained tokens, y el `GITHUB_TOKEN` de Actions **no** puede leer ni escribir Projects. Es decir: adoptar el Project añade un **secreto con permiso amplio** que hoy el repositorio no necesita. Si además se quisiera la dirección GitHub → repo, ese token de scope amplio tendría permiso de escritura sobre el repositorio — la peor combinación posible. Detalle en §G.2b.

**Orden recomendado de adopción, si se adopta:** primero el modelo del repositorio (§C–§F), después el Project. **Nunca al revés.** Adoptar el Project antes de tener estado objetivo por capacidad produciría un tablero de 28 filas `C-nn` sin objetivo — un dashboard de actividad, que es exactamente lo que el usuario quiere evitar.

---

## H. `ROADMAP.md`

### H.1 Qué debería ocurrir con él

**Mantenerlo, reducido a dirección y horizonte.** No eliminarlo, no reemplazarlo, no convertirlo.

El contrato actual (`docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`) es **excelente** y no debe cambiarse: su regla de admisión («un contenido pertenece al ROADMAP **sólo si** eliminarlo impide entender hacia dónde evoluciona ARgentOS o cómo se relacionan y secuencian sus principales iniciativas») y su regla de frescura («se actualiza cuando cambia la dirección, la secuencia o las prioridades, **no** cuando se cierra una tarea») son correctas.

**El problema es que el documento no las cumple, y no puede cumplirlas mientras cargue estado.** Porque el estado cambia en cada cierre, y editar el documento en cada cierre viola su propia regla de frescura. R-1 lo demuestra: siete ediciones en tres semanas.

**Lo que debe salir de `ROADMAP.md`:**

| Bloque actual | Veredicto | Destino |
|---|---|---|
| `## 🎯 Destino` | **RETENER** (es dirección pura) | — |
| `## 🧭 Posición actual` (versión publicada, payload publicado, PATCH en `dev`, trabajo activo) | **ELIMINAR** | `docs/VERSIONING.md` §9 (versiones) + estado de capacidad (trabajo activo) |
| `## 🚦 Roadmap` `NOW`/`NEXT`/`LATER` | **RETENER**, reducido a **una línea por iniciativa**: `[Horizonte] Nombre — capacidad objetivo que persigue` | — |
| `> El envelope de autonomía ya no figura aquí…` (nota de retiro) | **ELIMINAR** | La historia vive en `CHANGELOG.md` y en el Plan que lo cerró |
| `## 🔗 Dependencias críticas` (grafo) | **RETENER** sólo si expresa **secuencia de dirección**. Hoy mezcla trabajo cerrado (`Etapa A ✅`, `Envelope ✅`) con trabajo futuro | Reescribir con **sólo** aristas entre iniciativas vivas |
| `## 🚧 Bloqueos que pueden cambiar el camino` (4 filas) | **REDUCIR** a los que bloquean **dirección**. Los bloqueos de un Plan concreto pertenecen a ese Plan | Plan dueño de cada decisión |
| `_Última actualización: … Protocolo publicado: 12.0.0_` | **ELIMINAR la versión** | `docs/VERSIONING.md` §9 |
| — | **AGREGAR** `## Registro de rechazos` (o puntero a él) | El registro donde se documenta por qué algo no se hizo |

**Presupuesto visual sugerido:** **≤ 60 líneas** (frente a las 107 actuales), con cero información de estado cambiante salvo el horizonte.

### H.2 Qué falta: el estado de capacidad

`ROADMAP.md` **no puede** alojar el estado de capacidad: su propio contrato lo prohíbe («no es un registro exhaustivo de capacidades»), el glosario lo prohíbe («no usar "roadmap" para designar … un registro de capacidades») y cargarlo ahí reintroduce R-1.

**Recomendación: un solo documento nuevo, `CAPACITIES.md`** (nombre a decidir), con:

- **Capa P** — las ~8 capacidades PROTOCOL: afirmación, estado actual (nivel de la matriz), estado objetivo, gap, criterio de terminación, evidencia, condición de invalidación, límites.
- **Capa D** — las 28 `C-nn` **en forma resumida** (nombre, dominio, nivel actual, qué capacidad P habilita), con **puntero** a la matriz de Etapa A como evidencia detallada. No se duplica la matriz.
- **El milestone activo**, con su resultado verificable y sus criterios de salida.

**Objeciones evaluadas honestamente:**

| Objeción | Respuesta |
|---|---|
| «Es un documento nuevo — ¿no es maquinaria?» | Es un documento, no un mecanismo: no crea estado de lifecycle, gate, checker, registry ni autoridad. Y **reemplaza** contenido que hoy está duplicado en cinco lugares |
| «Va a envejecer como la matriz» | **Sí, si nadie lo actualiza.** Por eso la actualización debe ser **consecuencia obligatoria de `Avanza:`** en el Plan, no una buena intención. Un documento de estado sin obligación de actualización es una mentira que envejece |
| «¿Por qué no en `ROADMAP.md`?» | Contrato, glosario y R-1 lo prohíben. La separación de ejes es **el** punto del diseño |
| «28 fichas es demasiado» | Correcto. De ahí la Capa P (~8) + Capa D resumida (una fila por `C-nn`) + puntero a la matriz. ~60–80 líneas, no 584 |
| «`docs/working/` es para lo no normativo» | El estado de capacidad **no es normativo en el sentido de crear autoridad**, pero es **estado corriente** y debe estar versionado y actualizado. Va en `docs/`, no en `docs/working/`; su clase documental hay que decidirla (§K, decisión D-3) |

### H.3 Fuente de verdad por tipo de información (matriz de resolución)

| # | Información | **Fuente de verdad** | Vistas derivadas | Prohibido |
|---|---|---|---|---|
| 1 | Dirección estratégica (destino, invariante) | `ROADMAP.md` §Destino | Project | Planes, INDEX, Changelog |
| 2 | Estado actual (posiciones, capacidades, gaps) | `CAPACITIES.md` (capa P) + matriz de Etapa A (evidencia de capa D) | Project | `ROADMAP.md` |
| 3 | Prioridades (qué ahora, qué después) | `ROADMAP.md` (horizonte) | Project | INDEX, Planes |
| 4 | Trabajo ejecutable | El Plan en `docs/plans/` | Issue/Project (espejo) | Project como autoridad |
| 5 | Decisiones | `docs/rfc/` + `docs/adr/` | — | Project, INDEX |
| 6 | Historial | `CHANGELOG.md` + tags Git + planes cerrados | GitHub Releases | `ROADMAP.md` |
| 7 | Registro/navegación de gobernanza | `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` | — | Registro como autoridad (`AU-4`) |
| 8 | Estado de release | `docs/VERSIONING.md` §9 + tags | — | `ROADMAP.md`, INDEX |
| 9 | Razones de rechazo | Registro de rechazos en el artefacto dueño | — | Un Project column; un issue cerrado |
| 10 | Evidencia de que algo está probado | Git + tests + checkers + `Validation anchor` | — | Prosa |

**Regla de coherencia:** cada fila tiene **exactamente una** fuente de verdad. Si dos documentos afirman lo mismo, uno debe degradarse a puntero en el mismo Change que lo detecte.

---

## I. Modelo de progreso

### I.1 La unidad fundamental de progreso

**Confirmo la intuición del usuario** y la hago concreta:

> **La unidad de progreso es `(capacidad, nivel actual → nivel objetivo)` con su evidencia.**
> No es «hicimos 17 issues». No es siquiera «el Plan 165 se cerró».

Un Plan cerrado es **actividad**. Una capacidad que pasó de `no demostrado` a `testeado` con una suite verde y un anchor registrado es **progreso**. La diferencia no es semántica: es que la segunda afirmación **puede ser falsada**.

### I.2 El mecanismo concreto

**Escalera de niveles:** el vocabulario cerrado de 8 niveles ya existente en la matriz de Etapa A, ordenado como orden parcial estricto:

```text
implementado  <  testeado  <  dogfoodeado  <  demostrado bajo condiciones reales
                                              ▲
                          parcialmente demostrado
                          dependiente de una condición externa
                          limitado por un boundary conocido
                          no demostrado
```

Los cuatro últimos **no** son niveles de una escalera lineal: son **estados de garantía acotada** (parcial / externa / limitada / ausente). Eso es correcto y debe preservarse: forzar un orden total sobre ellos sería inventar precisión. Por lo tanto el progreso se declara como **una transición**, no como un número:

```text
PROGRESO = (capacidad, nivel_origen, nivel_destino, evidencia, fecha, Change)
```

**Tabla de transiciones y su evidencia exigida** (esto es lo que hace la métrica falsable):

| Transición | Evidencia mínima exigida | Quién la produce |
|---|---|---|
| `implementado → testeado` | Suite automatizada que ejercita el contrato declarado, verde, con su conteo real | El Plan, en su batería |
| `testeado → dogfoodeado` | Ejercicio **sobre este repositorio** con traza verificable (dogfood anclado, corpus real, anchor) | El Plan, en su anchor |
| `dogfoodeado → demostrado bajo condiciones reales` | Evidencia de las condiciones pretendidas que el repositorio **no controla** (adoptante, proveedor real, CI completa) | **Fuera del repositorio.** Es la transición que hoy **nadie** puede acreditar — 0 de 28 |
| `parcialmente demostrado → dogfoodeado` | Cobertura del subconjunto de condiciones que faltaba | El Plan |
| `dependiente de una condición externa → testeado` | Aislar la dependencia y probar el contrato propio | El Plan |
| `no demostrado → implementado` | Mecanismo existente y estructuralmente válido, sin cobertura | El Plan que lo implementa |
| `→` limitación declarada (cualquiera) | Declaración explícita del límite, publicada y verificable | El Plan |

### I.3 La definición de Milestone (responde §6 del encargo)

**Un milestone en ARgentOS es un resultado del PROTOCOL verificado, no una fecha ni un contenedor.**

**Qué representa.** Un enunciado verificable de la forma:

> «El **ciclo de cambio gobernado** está implementado y puede operar de extremo a extremo bajo las garantías G1…Gn.»

No es una lista de tareas; es una **afirmación sobre el mundo** que puede ser verdadera o falsa, con evidencia.

**Contenido mínimo de un milestone:**

```text
M-<n> <Nombre del resultado>
  Afirmación          qué es verdad cuando el milestone está alcanzado (1 frase, verificable)
  Capacidades         qué capacidades P (y por las que habilitan, qué D) deben alcanzar
                      qué nivel, y cuáles no cambian
  Criterios de salida cada uno verificable con evidencia nombrada (no "estar listo")
  Fuera de alcance     qué NO incluye, explícitamente
  Criterios de entrada qué debe ser verdad para poder iniciarlo
  Evidencia exigida    qué artefactos/anclas/checkers prueban cada criterio
  Bloqueos            qué puede impedirlo
```

**Cuándo nace.** Cuando un **acto humano** autoriza el trabajo que lo persigue — nunca antes. Un milestone no nace de una idea ni de un documento. Nace del mismo acto que autoriza su primer Plan.

**Cuándo se considera iniciado.** Cuando su primer Plan pasa a `Aprobado para ejecución`. No cuando se escribe el milestone.

**Cuándo se considera completado.** Cuando **todos** sus criterios de salida tienen evidencia registrada y la afirmación del milestone es **verificable por un tercero** leyendo el repositorio. Condición derivada, análoga a `Closed`: `Milestone alcanzado = afirmación verdadera ∧ criterios evidenciados ∧ capacidades en el nivel objetivo`.

**Qué evidencia exige.** La misma que ya exige el Change Lifecycle: `Validation anchor` con scope declarado, command-set, identidad de contenido scoped; tests verdes con su conteo real; y — para las capacidades cuyo objetivo sea «demostrado bajo condiciones reales» — evidencia de condiciones que hoy el repositorio no puede producir. **Si esa evidencia no existe, el milestone no puede declararse alcanzado.** Ese es el punto: un milestone que el repositorio no puede probar **no se declara alcanzado**, se declara `parcial` con lo que falta nombrado.

**Qué ocurre con trabajo no terminado.** Tres respuestas, y ninguna es «desaparece»:

1. **Bloquea la declaración del milestone.** El milestone se declara `parcial` con el criterio incumplido nombrado, y **requiere decisión humana** para cambiar los criterios — que quedan registrados como cambio de alcance (`HD-K1` ya exige re-derivación por cambio de scope).
2. **Se traslada al milestone siguiente** como ítem explícitamente re-scopeado, con su razón. Nunca silenciosamente.
3. **Se cancela**, y la cancelación se registra con su razón (es un rechazo).

**Relación con PROTOCOL y DEV.** Un milestone **es** PROTOCOL (es una afirmación sobre el producto) y **se alcanza por** DEV (los Planes). Por eso no puede vivir ni sólo en la capa P ni sólo en la capa D: vive como **puente**, declarado en `CAPACITIES.md` y consumido por el horizonte `NOW`/`NEXT` de `ROADMAP.md`.

**Por qué no es un Milestone de GitHub.** El Milestone de GitHub: (a) tiene fecha de vencimiento opcional — ARgentOS no compromete fechas; (b) calcula progreso por **conteo de issues abiertos/cerrados** — «hicimos 17 issues»; (c) no tiene campos personalizados, no admite criterios de salida, no admite evidencia; (d) es un contenedor de issues, y un milestone de ARgentOS **no es un contenedor**. Los cuatro desajustes son estructurales, no de configuración.

### I.4 Qué se reporta y con qué frecuencia

**Regla de frescura:** el estado de capacidad se actualiza **cuando cambia**, y el cambio es consecuencia obligatoria de `Avanza:` en el Plan. **No hay reporte periódico.** Un reporte periódico de progreso inventa progreso cuando no lo hay y obliga a medir actividad.

**Lo que se puede afirmar en cualquier momento, con el modelo:**

| Pregunta del usuario | Respuesta | Fuente |
|---|---|---|
| ¿Qué queremos que ARgentOS llegue a ser? | §Destino | `ROADMAP.md` |
| ¿Qué capacidades debe tener el PROTOCOL? | Capa P | `CAPACITIES.md` |
| ¿Qué tenemos actualmente? | Nivel actual por capacidad + evidencia | `CAPACITIES.md` + matriz (evidencia) |
| ¿Qué falta? | Gap declarado por capacidad | `CAPACITIES.md` |
| ¿Qué estamos haciendo ahora? | Horizonte `NOW` + Planes `Aprobado para ejecución` | `ROADMAP.md` + `docs/plans/` |
| ¿Qué viene después? | Horizonte `NEXT` | `ROADMAP.md` |
| ¿Por qué estamos haciendo cada cosa? | `Avanza:` del Plan → capacidad → Destino | Header del Plan + `CAPACITIES.md` |
| ¿Una idea nueva debe entrar, cuándo y dónde? | Filtro de admisión §F.3 | `CAPACITIES.md` + registro de rechazos |
| ¿Cómo evitamos desviarnos? | Invariante de dirección + filtro Q4 + registro de rechazos | `ROADMAP.md` §Destino + §Rechazos |
| ¿Cuándo está terminada una etapa? | Criterios de salida del milestone con evidencia | Milestone |

**Ninguna de las diez respuestas depende de GitHub.**

---

## J. Ejemplo — el estado actual de ARgentOS en el modelo propuesto

**Sin implementar nada.** Muestro cómo quedaría representado lo que existe hoy.

### J.1 Dirección (`ROADMAP.md`, reducido)

```markdown
# 🗺️ Roadmap de ARgentOS

> Dirección y secuencia. El contrato vive en docs/CONVENTIONS.md.
> El estado de las capacidades vive en `CAPACITIES.md`; aquí no se registra estado.

## 🎯 Destino
Un protocolo documental y basado en estado para orquestar agentes: contratos que un
proyecto adopta materializando un payload, no una herramienta que se instala.

Que ARgentOS reciba un objetivo suficientemente amplio y lo ejecute de forma
autónoma bajo supervisión humana, sin perder sus garantías de autoridad, alcance,
contexto, evidencia, recuperación y terminación.

**Invariante de dirección:** `Autonomy ⊆ Scope ∩ Authority`. La autonomía es
**operacional, no decisional**: elimina traspasos operativos dentro de trabajo ya
autorizado; nunca elimina el control humano sobre alcance, autoridad, decisiones
normativas, protocolo y release.

## 🚦 Camino
▶️ NOW
   M-2 · Frontera de autonomía — que el host opere con un actor real bajo contención
         de autoridad y recuperación verificadas (C-02, C-26)

⏭️ NEXT
   M-3 · Comprensión del proyecto — que Discovery produzca conocimiento usado
         (C-16, C-17) — depende de una adopción real

⏳ LATER
   M-4 · Capacidad nueva — sólo desde necesidades descubiertas en M-2/M-3

## 🔗 Secuencia
M-2 ──▶ M-3 ──▶ M-4        (M-1 · Línea base de garantías: ✅ Alcanzado)

## 🚧 Bloqueos de dirección
| Bloqueo | Qué cambia |
|---|---|
| Autorización de release de `12.0.1` | cuándo se publica el payload reconciliado |
| Evidencia de adopción no disponible en el repositorio | acota el nivel máximo acreditable de `M-3` |

## 🚫 Registro de rechazos
| Idea | Fecha | Razón | Reabre si… |
|---|---|---|---|
| Caché de prompt como capacidad del protocolo | 2026-09 | Su garantía depende del proveedor, no de ARgentOS (`C-14`, `dependiente de una condición externa`) | el beneficio es medible sin proveedor |
| Retry con ciclo de vida propio | 2026-10-13 | Excede `FC-6`; añade mecanismo no pedido; la discrepancia política/código se resuelve alineando (`ID-8`) | el mantenedor amplía `F-C` |
```

Comparación: 107 → ~45 líneas, con **cero** información que cambie en un cierre.

### J.2 Estado de capacidad (`CAPACITIES.md`, nuevo)

```markdown
# Capacidades de ARgentOS — estado y objetivo

> Fuente de verdad del estado de capacidades. Evidencia detallada de la capa D:
> `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` (snapshot 2026-10-12).

## Capa P — capacidades del PROTOCOL (comportamiento del adoptante)

### P-01 · Alineación de intención
- **Afirmación:** el sistema no ejecuta una petición ambigua sin reflejar y confirmar la intención.
- **Actual:** `dogfoodeado` · **Objetivo:** `dogfoodeado` · **Gap:** ninguno
- **Terminación:** n/a (objetivo alcanzado)
- **Evidencia:** `H11-intent-reflection`, `INTENT_REFLECTION.md`, `INTENT_CONFIDENCE.md`, roles `intent_reflector`/`intent_reflection_reviewer`
- **Límites:** la confirmación es del usuario; el sistema no infiere intención no declarada

### P-05 · Ejecución gobernada                                            [MILESTONE M-2]
- **Afirmación:** ningún efecto fuera de la frontera ocurre sin autorización registrada y
  determinable, y la unidad de aceptación sigue siendo el Change.
- **Actual:** `parcialmente demostrado` · **Objetivo:** `demostrado bajo condiciones reales`
- **Gap:** la contención de autoridad frente a código que el host no controla no está demostrada;
  el actor real no está disponible; la recuperación ante fallos reales no está probada.
- **Terminación:** (1) frontera no dependiente de un actor benigno (`C-02`); (2) recuperación
  verificada con fallo real inyectado (`C-26`); (3) actor con procedencia declarada, ejecutado
  por un entorno adoptante (`FC-1`); (4) aislamiento declarado de forma verificable (`FC-2`).
- **Evidencia actual:** `AUTHORIZATION.md`, `PROTOCOL_BOUNDARIES.md`, `EXECUTION_PLAN` (efectos),
  `H01`/`H04`, `runtime/orchestrator/{worker,host,autonomy}.py`, suites de scope/efectos
- **Condición de invalidación:** si la política y el código divergen en la semántica de la frontera.
- **Límites:** `ID-3` declara que ARgentOS **no** ofrece aislamiento; la contención fuerte exigiría
  aislamiento y queda fuera del alcance vigente.
- **Avanza por:** Plan 165 (`Aprobado para ejecución`), frontera `F-C` (alcance canónico 1B)

### P-09 · Comprensión del proyecto                                        [MILESTONE M-3]
- **Actual:** `no demostrado` · **Objetivo:** `dogfoodeado`
- **Gap:** no existe corrida real de Discovery en este repositorio; `C-16`/`C-17` no demostrados.
- **Terminación:** una corrida real de Discovery sobre un proyecto adoptante, con KB producida y
  consumida, y su evidencia anclada.
- **Bloqueo:** **requiere un proyecto adoptante.** No es alcanzable desde este repositorio.
- **Límites:** el checker D01 sólo cubre el subconjunto mecánico.

(… P-02 contexto, P-03 ejecución/plan, P-06 validación, P-07 auditoría independiente
    [objetivo máximo: «declarada», por el catálogo de garantías D0], P-08 memoria,
    P-11 trazabilidad, P-12 entrega/configuración …)

## Capa D — capacidades habilitantes DEV (resumen; evidencia en la matriz de Etapa A)

| ID | Capacidad | Nivel actual | Habilita (capa P) |
|---|---|---|---|
| `C-01` | Change Lifecycle | `dogfoodeado` | P-05, P-11 |
| `C-02` | Authority | `parcialmente demostrado` | P-05 |
| `C-03` | Scope enforcement | `dogfoodeado` | P-05 |
| `C-04` | Validation / Closure | `dogfoodeado` | P-06, P-11 |
| `C-05` | C1/C2/C3 | `dogfoodeado` | P-06 |
| `C-06` | SAE | `dogfoodeado` | P-05 |
| `C-07` | Autonomous Orchestrator | `dogfoodeado` | P-05 |
| `C-08` | Agent Worker | `dependiente de una condición externa` | P-05, P-08 |
| `C-09` | WorkerResult | `dogfoodeado` | P-05, P-11 |
| `C-10` | Delegation | `dogfoodeado` | P-05 |
| `C-11` | Context engineering | `testeado` | P-02 |
| `C-12` | Context identity | `testeado` | P-02, P-11 |
| `C-13` | Materialization | `testeado` | P-02 |
| `C-14` | Prompt Cache | `dependiente de una condición externa` | (—; limitada por el proveedor) |
| `C-15` | Placement | `limitado por un boundary conocido` | (—; higiene interna) |
| `C-16` | Discovery | `no demostrado` | P-09 |
| `C-17` | Discovery KB | `no demostrado` | P-09 |
| `C-18` | Protocol gates | `testeado` | P-06 |
| `C-19` | enforced mode / hooks | `testeado` | P-05 |
| `C-20` | EARS | `dogfoodeado` | P-02 |
| `C-21` | Skills | `implementado` | P-03 |
| `C-22` | Deliberation | `dogfoodeado` | P-04 (judgment) |
| `C-23` | Change Governance | `testeado` | P-11 |
| `C-24` | Metrics / health | `parcialmente demostrado` | P-06 |
| `C-25` | Feature flags | `parcialmente demostrado` | P-12 |
| `C-26` | recovery | `parcialmente demostrado` | P-05 |
| `C-27` | CI / validation | `parcialmente demostrado` | P-06 |
| `C-28` | dist sync | `dependiente de una condición externa` | P-12 |

## Milestone M-2 — Frontera de autonomía
- **Afirmación:** el host opera con un actor real aportado por el entorno, y su frontera de
  autoridad no depende de que ese actor sea benigno; un fallo real es detectado, registrado y
  reconducido sin ampliar alcance ni autoridad.
- **Capacidades:** P-05 → `demostrado bajo condiciones reales`; P-08 → `dogfoodeado`;
  capacidades D: `C-02`, `C-08`, `C-26` → nivel superior.
- **Criterios de salida:** `FC-1`…`FC-10` (ya declarados por el Plan 163).
- **Fuera de alcance:** `C-16`, `C-17`, `C-21` (declarado por el acto del 2026-10-12).
- **Evidencia exigida:** una falsación ejecutable por garantía afirmada, verde; batería canónica
  sin regresión; `Validation anchor` + `Checkpoint` del Plan 165.
- **Bloqueos:** ninguno declarado. **Estado:** `autorizado, no iniciado`.
```

### J.3 Trabajo en curso (lo que cambia hoy)

```text
Plan 165 — Implementación de la frontera de autonomía F-C
  Status:  Aprobado para ejecución
  Avanza:  P-05 · parcialmente demostrado → demostrado bajo condiciones reales   ← NUEVO CAMPO
           (capa D: C-02, C-08, C-26)
  Scope:   runtime/orchestrator/**, tests/**, .agents/policies/**
  Diseño:  ID-2/ID-4/ID-6/ID-7/ID-8 resueltos (30 líneas sin commitear)
  Milestone: M-2
  Autoridad: acto del mantenedor del 2026-10-13 (Plan 164)
```

Y la corrección del hecho falso: `ROADMAP.md` **no** puede afirmar «Trabajo activo: ninguno» mientras el Plan 165 esté `Aprobado para ejecución` con diseño en curso. En el modelo propuesto, esa afirmación no existe: el trabajo activo se lee del `Status` de los Planes, y el horizonte `NOW` nombra el **milestone**, no una lista de tareas.

### J.4 Trabajo diferido y rechazado

```text
DIFERIDO (LATER + dueño + condición de desbloqueo)
  C-16 / C-17 / C-21  →  P-09 (Comprensión del proyecto)   [LATER]
      Razón:        su garantía depende de una adopción real, no observable aquí
      Dueño:        mantenedor
      Desbloquea:   una corrida de Discovery sobre un proyecto adoptante
      Estado:       fuera del alcance de M-2 por acto del 2026-10-12

RECHAZADO (registro permanente con condición de reapertura)
  Prompt Cache como capacidad del protocolo
      Razón: su beneficio depende del proveedor (`C-14`, dependiente de condición externa)
      Reabre si: el beneficio es medible sin proveedor
```

### J.5 Lo que este modelo hace visible y hoy no se ve

1. **`P-05` es la única capacidad del milestone activo**, y su objetivo es `demostrado bajo condiciones reales` — el nivel que **0 de 28** alcanza hoy. El modelo hace explícito que M-2 exige lo que el repositorio nunca logró.
2. **`P-09` no es alcanzable desde este repositorio.** Declararlo `LATER` sin condición de desbloqueo (como hoy) lo hace parecer un ítem de trabajo; declararlo con su bloqueo lo convierte en una **decisión pendiente de contexto externo**.
3. **`C-14`, `C-15` no habilitan ninguna capacidad P.** Son mecanismos internos. El modelo revela que mantenerlos en la lista de «capacidades» del roadmap era ruido.
4. **El registro de rechazos ya tiene dos entradas reales** (`C-14`, retry/`ID-8`), hoy dispersas en `docs/plans/165` y en la matriz. Centralizarlas evita re-proponerlas.

---

## K. Recomendación final

### K.1 Qué mantener (sin cambios)

| Artefacto | Razón |
|---|---|
| **El Plan como unidad de trabajo** (`docs/plans/`, 174 planes) | Es una iniciativa con gobernanza, autoridad, evidencia y cierre. No mejorar reemplazándolo |
| **El Change Lifecycle completo** (`authorize → execute → verify → close → commit → promote`) y sus estados derivados | Probado en 174 planes, verificado por `C-1`/`C-2`/`C-3`. `Executed ≠ Committed ≠ Closed ≠ Released` es un logro, no una complicación |
| **`Validation anchor` + `Checkpoint` + `Scoped Content Identity`** | Es lo que hace la evidencia falsable. Ningún Project puede replicarlo |
| **El contrato del ROADMAP** (`docs/CONVENTIONS.md:Contrato del ROADMAP`) | La regla de admisión y la de frescura son correctas; el documento es lo que no las cumple |
| **La separación DEV/Protocol a nivel de payload** (`AGENTS.md`, RFC-56, RFC-75 §«Dev vs Protocol») | Correcta y no negociable. **No se comparten mecanismos entre DEV y Protocol** |
| **La matriz de Etapa A** | Evidencia excelente. Se conserva **como evidencia**, no como estado |
| **`docs/VERSIONING.md` §9 como fuente de posición de release** | Ya es la fuente declarada; el error es que `ROADMAP.md` la duplique |
| **Los INDEX** (`plans`, `rfc`, `adr`, `working`) | Registro/navegación correcto y verificado mecánicamente |
| **`docs/working/proposals/`** | Ya es el hogar correcto de una idea pre-canónica con status |

### K.2 Qué cambiar (mínimo, quirúrgico)

| Cambio | Artefacto | Por qué |
|---|---|---|
| **Retirar todo el estado de `ROADMAP.md`** (posición, versiones, trabajo activo, notas de retiro, detalle de bloqueos) y reducir a ≤60 líneas | `ROADMAP.md` | R-1: es la causa raíz de las siete reescrituras |
| **Reescribir el grafo de dependencias** con sólo aristas entre iniciativas vivas | `ROADMAP.md` | Hoy mezcla trabajo cerrado (`✅`) con futuro |
| **Agregar `## Registro de rechazos`** | `ROADMAP.md` | R-6: hoy no hay forma de decir «no» que sobreviva |
| **Agregar el campo `Avanza:` al template y a los Planes nuevos** | `docs/plans/_TEMPLATE.md` + gobernanza | Responde «¿por qué hacemos esto?» de forma verificable. **Nunca retroactivo** (RFC-46) |
| **Canonizar el vocabulario de dominio** (`PROTOCOL` / `DEV` / `BOTH`) o eliminarlo | `docs/CONVENTIONS.md` | R-7: hoy se usa como si fuera normativo y no lo es |
| **Reducir `Roadmap impact` a una determinación determinable** — apoyada en el horizonte del ROADMAP y en el estado de capacidad, ambos verificables — **o retirarla** | `.agents/policies/validation-closure.md` §5.2 + `docs/CONVENTIONS.md` | R-4: 27 aplicaciones en prosa, ocho formas tipográficas, cuatro decisiones humanas derivadas, una violación real de scope |
| **Reducir el header de estado de `docs/plans/INDEX.md`** a hechos verificables | `docs/plans/INDEX.md` | Duplica `ROADMAP.md` y `CHANGELOG.md` (R-5) |

### K.3 Qué eliminar

| Eliminar | De dónde | Cuándo |
|---|---|---|
| Sección `## 🧭 Posición actual` completa (versión publicada, payload publicado, PATCH en `dev`, trabajo activo) | `ROADMAP.md` | En el Change de implementación |
| Nota de retiro del envelope de autonomía | `ROADMAP.md` | Ídem — la historia vive en `CHANGELOG.md` |
| `Protocolo publicado: 12.0.0` del pie | `ROADMAP.md` | Ídem |
| Narración de estado de 2.000+ caracteres | Header de `docs/plans/INDEX.md` | Ídem |
| Las series en ordinales españoles como criterio de agrupación | `docs/plans/INDEX.md` | **NO eliminar el registro** (es identidad derivada y está verificado por checker); dejar de usarlas como si fueran planificación |
| `MASTER_PENDING_WORK_INVENTORY.md` como patrón | Práctica | Ya no existe en disco; **no recrear inventarios externos** |

**Nada de documentación gobernanza se borra.** Lo que sale del ROADMAP ya tiene dueño declarado (Plan 158 lo demostró: 0 documentos nuevos, 0 información sin dueño).

### K.4 Qué crear

**Exactamente un artefacto nuevo, y sólo si se aprueba la decisión D-2:**

| Crear | Contenido | Tamaño estimado | Clase documental a decidir |
|---|---|---|---|
| `CAPACITIES.md` (nombre a decidir) | Capa P (~8 capacidades con estado actual→objetivo, gap, terminación, evidencia, límites) · Capa D resumida (28 filas: nivel + qué habilita, **con puntero** a la matriz de Etapa A) · El milestone activo | ~70–100 líneas | Inventory (`docs/AGENTS.md:Folder → class map`) — **decisión humana D-3** |

**Y un artefacto por milestone, cuando exista:** sección dentro de `CAPACITIES.md` mientras haya uno activo; documento propio (`docs/milestones/M-<n>-<slug>.md`) si llega a haber más de dos simultáneos o su contenido crece. **No crear la carpeta ahora.**

**Nada más.** En particular: **ningún registro global de capacidades fila-a-fila con estado mutable por Change** (sería un registry, prohibido por `docs/AGENTS.md` y `AU-4`), **ninguna entidad `Initiative`**, **ningún campo de prioridad numérica**, **ningún checker de estado de capacidad**.

### K.5 Qué implementar primero (orden recomendado, con su justificación)

El orden está diseñado para que **cada paso sea útil por sí solo** y para no construir un tablero antes de tener algo que mostrar en él.

```text
PASO 1 — Decisión humana sobre las cuatro preguntas abiertas (§K.7)
         Sin esto, nada más es implementable. Coste: una conversación.

PASO 2 — Canonizar el vocabulario y cerrar la frontera PROTOCOL/DEV
         · Definir (o suprimir) el vocabulario PROTOCOL/DEV/BOTH en docs/CONVENTIONS.md
         · Resolver la clase documental del estado de capacidad
         Change docs-only. Prerrequisito de todo lo demás: sin una frontera normativa,
         la capa P y la capa D se vuelven a mezclar en el primer Change.

PASO 3 — Crear `CAPACITIES.md` con la capa P y el milestone M-2
         · 8 capacidades P, con estado actual→objetivo y terminación
         · Capa D resumida con punteros a la matriz de Etapa A (sin duplicarla)
         · Milestone M-2 con FC-1…FC-10 como criterios de salida
         Change docs-only, L1–L2. Es el paso que hace el progreso medible.

PASO 4 — Añadir `Avanza:` al template y declararlo en el Plan 165
         Change docs-only + una línea. Conecta el trabajo real con la capacidad.
         Sustituye de facto la necesidad de `Roadmap impact` para el 90% de los casos.

PASO 5 — Reducir `ROADMAP.md` a dirección + horizonte + rechazos
         Change docs-only. Sólo tiene sentido DESPUÉS del Paso 3: si se hace antes,
         el estado que se retira no tiene dónde vivir.

PASO 6 — Reconciliar `Roadmap impact`: hacerlo determinable contra el horizonte
         y el estado de capacidad, o retirarlo
         Change docs-only sobre la política y la convención. Cierra R-4 y las
         decisiones humanas PC-4/PC-5 que generó.

PASO 7 — (CONDICIONAL) Project derivado en GitHub
         Sólo si se cumple el umbral de §G.5. Requiere ampliar el scope del token
         a `read:project`/`project`. Unidireccional repo → GitHub. Nada de esto
         es prerrequisito de los pasos 1–6.
```

**Por qué este orden y no otro:**

- **Paso 2 antes que 3:** crear `CAPACITIES.md` sin vocabulario canónico reproduce R-7 dentro del documento nuevo.
- **Paso 3 antes que 5:** reducir el ROADMAP antes de tener dónde poner el estado lo deja huérfano. El Plan 158 ya cometió la versión benigna de este error (redujo el tamaño sin crear destino para el estado, y el estado volvió).
- **Paso 4 antes que 6:** `Avanza:` es la alternativa constructiva a `Roadmap impact`; sin ella, retirar `Roadmap impact` deja un hueco.
- **Paso 7 al final y condicional:** nunca al revés. Un Project antes del modelo produce 28 filas sin objetivo.

### K.6 Qué dejar para después

| Diferir | Razón |
|---|---|
| **El Project de GitHub** | No demostrado como necesidad (§G.5). Además requiere ampliar el scope del token |
| **Issues como intake** | Sólo tiene sentido si hay fricción real de captura. Hoy la captura funciona por conversación |
| **Un checker de `Avanza:`** | El campo primero debe demostrar que se usa bien en 10–15 Planes. Un checker prematuro congela un formato antes de saber si es el correcto |
| **Fichas detalladas para las 28 capacidades DEV** | La matriz de Etapa A ya es la evidencia; duplicarla en 28 fichas es burocracia pura |
| **Medición operacional de métricas (`C-24`, Incremento 4 completo)** | El Incremento 4 se materializó con alcance mínimo deliberado (Plan 98). Ampliarlo es una decisión propia, no un prerrequisito |
| **Capa P completa para las 12 capacidades restantes** | Empezar con las ~8 que el milestone activo y la dirección exigen; el resto se declara cuando entre en horizonte |
| **Migrar los 174 planes a `Avanza:`** | **Nunca.** RFC-46: los artefactos cerrados no se reescriben. El campo aplica desde su adopción |
| **GitHub Releases / Discussions / wiki** | Ningún problema demostrado que resuelvan |

### K.7 Relación con el funcionamiento interno de ARgentOS (§10 del encargo)

El usuario pregunta si el sistema de planificación DEV/PROTOCOL **debería reflejar** la filosofía del protocolo: estado, gates, criterios de entrada/salida, evidencia, reevaluación, autoridad, trazabilidad.

**La respuesta tiene dos partes, y son opuestas — es importante no fusionarlas.**

#### Parte 1 — Como *principio de diseño*: SÍ, y ya ocurre

| Propiedad del protocolo | Equivalente DEV ya existente |
|---|---|
| `REQUEST → UNDERSTAND/ALIGN → COMPLETE CONTEXT → PLAN → JUDGE → EXECUTE → VALIDATE → COMPLETE` | `Intake → clasificación → Plan (con `premises(D)`) → autorización → ejecución → validación → cierre` |
| Gates `H00`…`H15` con criterios de entrada/salida | `Criterio de entrada` + `Criterios de salida` + batería canónica + `C-1`/`C-2`/`C-3` |
| `AUDIT → DEFECT → PLAN AGAIN` | `Finding → Corrección → Revalidación (A2)` (LC-1) |
| Evidencia con clase (`observation`/`measurement`/`attestation`) | Clases de evidencia DEV (`FACTUAL`/`NORMATIVE`/`DECISION`/`RELEASE`/`DESCRIPTIVE`) + `Validation anchor` |
| Autoridad separada de capacidad | `policies/authority.md`, ADR-16 (`AU-3`/`AU-5`/`AU-6`), RFC-56 |
| Trazabilidad | `Validation anchor` + `Checkpoint` + `Scoped Content Identity` + commits atómicos |

**El sistema de planificación ya es una instancia manual de la filosofía del protocolo.** Esa correspondencia es real y no hay que inventarla. Lo que este informe **agrega** es la pieza que faltaba en esa correspondencia: **el estado objetivo**. El protocolo tiene `TASK_SPECIFICATION` (qué debe ser verdad) antes de ejecutar; el DEV tiene `Criterios de salida` por Plan pero **ningún estado objetivo por capacidad**. Por eso el DEV puede decir «este Plan terminó» pero no «esta capacidad avanzó».

#### Parte 2 — Como *mecanismo compartido*: NO, y hay una prohibición explícita

`AGENTS.md` (raíz) es tajante:

> «**Do NOT** … Implement Change Lifecycle mechanisms (anchors, checkpoints, findings, pending decisions, series registries, lifecycle state machines) inside `protocol/.agents/`, or share lifecycle machinery between DEV and the Protocol.»

Y RFC-75 §«Dev vs Protocol» lo fundamenta:

> «No se crean workflow/policy/state machine/artifact/skill compartidos; no hay herencia automática. Principios transferibles (revalidación ante continuidad; persistir ≠ materializar; separación evidencia factual / autoridad normativa) quedan como **principios, no mecanismos**: si un principio debe volverse normativo en el Protocol, lo hará por el lifecycle propio del Protocol.»

`docs/CONVENTIONS.md` §«Change Lifecycle DEV — alcance y frontera» lo repite:

> «No se crean workflow/policy/state machine/artifact/skill compartidos entre DEV y Protocol; no hay herencia automática.»

**Consecuencia de diseño directa:** cualquier propuesta de que `CAPACITIES.md`, el milestone o el campo `Avanza:` **se conviertan en contrato del protocolo** (por ejemplo, que un adoptante tenga milestones o un registro de capacidades) **requiere RFC-56 Clase A** y **no** se deriva de este trabajo. Son cosas distintas: el DEV es el **primer consumidor** de la disciplina del protocolo, no el **origen** de sus mecanismos.

**El error que hay que evitar, y que este informe evita explícitamente:** copiar `Validation anchor`, `Checkpoint`, `Findings` o `PC-n` al payload porque «funcionan bien en DEV». La matriz de Etapa A ya demuestra que esa copia sería infundada: `C-01` Change Lifecycle es `dogfoodeado` **en DEV**, y `C-23` Change Governance (el mecanismo análogo del producto) es `testeado` con persistencia efímera y sin uso en la capa DEV. **Son dos mecanismos distintos con dos niveles de madurez distintos, y eso es correcto.**

### K.8 Circuito operativo corregido

El circuito que el usuario propuso es correcto en su forma. Le hago **tres correcciones**:

```text
ESTRATEGIA  (ROADMAP.md §Destino + invariante de dirección)
    ↓
CAPACIDADES PROTOCOL  (capa P: afirmación + estado actual → objetivo)
    ↓                                                  ▲
ESTADO ACTUAL  (nivel por capacidad, con evidencia)     │
    ↓                                                  │
GAPS  (actual → objetivo, con criterio de terminación)  │
    ↓                                                  │
INICIATIVAS DEV  (= el Plan existente, con `Avanza:`)   │
    ↓                                                  │
MILESTONE  (resultado verificado: agrupa capacidades)   │
    ↓                                                  │
PASOS DEL PLAN  (la unidad real de ejecución)           │
    ↓                                                  │
IMPLEMENTACIÓN                                          │
    ↓                                                  │
VALIDACIÓN  (batería + H13 por juicio)                  │
    ↓                                                  │
EVIDENCIA  (Validation anchor A1; A2 si revalida)       │
    ↓                                                  │
[FINDING → CORRECCIÓN → REVALIDACIÓN]  ← circuito de reparación (ya existe)
    ↓                                                  │
ACTUALIZACIÓN DEL ESTADO DE CAPACIDAD ─────────────────┘   ← LA PIEZA QUE FALTA
    ↓
DECISIÓN HUMANA: ¿el milestone está alcanzado? ¿cambia el horizonte?
```

**Corrección 1:** entre GAPS e INICIATIVAS DEV faltaba **MILESTONE** (o el orden estaba invertido). Un gap no se convierte en Plan directamente: se agrupa en un resultado verificable, y **ese** se autoriza. Sin este paso, cada gap genera un Plan suelto — que es exactamente el estado actual (174 planes sin agrupación por resultado).

**Corrección 2:** entre MILESTONE e IMPLEMENTACIÓN, `ISSUES` debe ser **`PASOS DEL PLAN`**. Este repositorio no tiene issues y no debe tenerlos: los `Pasos` del Plan son la unidad de ejecución, y están gobernados por el Plan que los autoriza. Introducir issues interpondría una capa sin autoridad entre el Plan y el trabajo.

**Corrección 3 — la importante:** el circuito **no cierra hoy**. Termina en «ACTUALIZACIÓN DEL ESTADO», y no existe estado que actualizar. La matriz de Etapa A fue un snapshot de un Plan `Closed`; nadie la actualiza. **Cerrar ese bucle es el objetivo completo de este diseño.**

```text
Circuito de una idea nueva (corregido)

IDEA NUEVA  (conversación, o issue como buzón sin autoridad)
    ↓
EVALUACIÓN  (filtro §F.3, Q1–Q7)  ← paso que hoy NO existe
    ↓
PRIORIZACIÓN  (NOW / NEXT / LATER / EXPERIMENT / REJECTED)
    ↓
¿ALTERA EL CAMINO ACTUAL?
    │
    ├─ SÍ → REEVALUAR EL PLAN: re-derivación del alcance del milestone
    │        (HD-K1/R-4 ya vigentes). No se edita un Plan aprobado:
    │        se crea un Change nuevo que re-deriva. Decisión humana.
    │
    └─ NO → LATER (con dueño y condición de desbloqueo, si aplica)
             EXPERIMENT (en NOW/NEXT, con la pregunta como terminación)
             REJECTED   (razón registrada en el REPOSITORIO + condición de reapertura)
```

**Corrección adicional:** «SÍ → REEVALUAR PLAN» no puede significar editar un Plan ya autorizado. La lección de `<PLAN-136>:F-3` es que una determinación no autoriza escritura fuera de scope. Re-planificar es **un Change nuevo** que re-deriva, porque `HD-K1` exige re-derivación ante cualquier cambio de scope — ampliación **o reducción**.

### K.9 Decisiones que requieren definición humana

Las separo con claridad. **Ninguna de las siguientes puedo resolverlas por análisis del repositorio.**

| # | Decisión | Opciones | Por qué es humana |
|---|---|---|---|
| **D-1** | ¿El vocabulario `PROTOCOL`/`DEV`/`BOTH` se canoniza, se redefine en dos capas, o se suprime? | (a) canonizar tal cual; (b) redefinir como Capa P / Capa D; (c) suprimir y usar sólo `Avanza:` | Cambia la frontera normativa entre el producto y su desarrollo. Es una decisión de modelo, no de repo |
| **D-2** | ¿Se crea el estado de capacidad como documento propio (`CAPACITIES.md`) o se admite dentro de otro artefacto? | (a) documento propio; (b) sección de `ROADMAP.md` (**viola el contrato vigente**); (c) sección de `docs/VERSIONING.md` §9; (d) sección nueva en `docs/CONVENTIONS.md`; (e) no crear — mantener sólo la matriz como evidencia | Afecta la fuente de verdad del estado actual y el contrato del ROADMAP |
| **D-3** | ¿Qué clase documental tiene el estado de capacidad? | Inventory (mutable, canonical) · Working · Policy | Determina su lifecycle, quién puede editarlo y si puede ser target normativo (`docs/AGENTS.md:Folder → class map`) |
| **D-4** | ¿Qué ocurre con `Roadmap impact`? | (a) hacerlo determinable contra horizonte + estado de capacidad; (b) mantenerlo como está; (c) retirarlo y sustituirlo por `Avanza:`; (d) reclasificarlo como `NOT_REQUIRED` por defecto | Es una regla normativa vigente **con decisiones humanas ya tomadas** (`PC-4`, `PC-5`). Cambiarla reabre esas decisiones |
| **D-5** | ¿Se adopta GitHub en algún grado? | (a) no adoptar; (b) sólo infraestructura CI; (c) Project derivado unidireccional; (d) issues como intake; (e) Project como mecanismo principal (**recomiendo no**) | Requiere ampliar el scope del token — y, si se adopta el Project, **añadir un PAT clásico con scope `project`+`repo`** (§G.2b). Decide si el estado de planificación sale del repositorio |
| **D-6** | ¿Un milestone puede declararse `parcial` y aun así habilitar el siguiente? | (a) no: bloquea hasta completarse; (b) sí, con criterios incumplidos nombrados y autorización explícita; (c) sí, con re-definición de criterios registrada como cambio de alcance | Es autoridad sobre el cierre de una etapa, reservada al mantenedor |
| **D-7** | ¿Quién puede declarar alcanzado un milestone? | (a) sólo el mantenedor; (b) el agente con evidencia + confirmación; (c) derivado si todos los criterios tienen evidencia | Análoga a la decisión sobre resolución de findings (ADR-16 `AU-3`: hoy es humana) |
| **D-8** | ¿El registro de rechazos vive en `ROADMAP.md` o en los artefactos dueños? | (a) sección en `ROADMAP.md`; (b) en el artefacto que decide; (c) ambos: sección índice + artefacto dueño | Toca el contrato del ROADMAP: un rechazo es dirección o historia, según se decida |

### K.10 Lo que puedo afirmar por análisis del repositorio (sin decisión humana)

Para que la separación quede completa, estas conclusiones **no** requieren autorización porque son determinaciones factuales:

1. **`ROADMAP.md` viola su propia regla de frescura.** Siete ediciones en tres semanas, varias de ellas para retirar trabajo cerrado — lo que el contrato prohíbe expresamente («no cataloga trabajo cerrado»).
2. **Ninguna capacidad tiene estado objetivo declarado.** Verificado: las 9 dimensiones de la matriz no incluyen objetivo; `ROADMAP.md` no lo declara para ninguna.
3. **La capa GitHub está vacía y nunca fue usada.** 0 issues, 0 PRs, 0 milestones, 9 labels por defecto sin uso de planificación, sin referencias a Projects.
4. **`Roadmap impact` no es determinable por un tercero.** 27 aplicaciones en prosa, 8 formas tipográficas, sin checker, con cuatro decisiones humanas derivadas y una violación real de scope (`<PLAN-136>:F-3`).
5. **`ROADMAP.md` contiene hoy una afirmación falsa:** «Trabajo activo: ninguno» mientras el Plan 165 está `Aprobado para ejecución` con 30 líneas de diseño sin commitear en el worktree.
6. **El circuito de planificación no cierra.** Termina en «actualización del estado» y no existe estado que actualizar; la matriz de Etapa A es un snapshot de un Plan `Closed`.
7. **El vocabulario de dominio no está canonizado.** `ROADMAP.md` y la matriz lo usan como normativo; `docs/CONVENTIONS.md` y `docs/glossary/` no lo definen.
8. **La separación de mecanismos DEV/Protocol está prohibida explícitamente** (`AGENTS.md`, RFC-75 §«Dev vs Protocol», `docs/CONVENTIONS.md` §«Change Lifecycle DEV — alcance y frontera»), y los principios transferibles se limitan a tres: revalidación ante continuidad, `persistir ≠ materializar`, y separación evidencia factual / autoridad normativa.
9. **Un Milestone de GitHub es estructuralmente incompatible** con la definición de milestone de ARgentOS: fecha de vencimiento, progreso por conteo de issues, ausencia de campos personalizados y de criterios de salida, y naturaleza de contenedor.
10. **Los dos Projects (Opción B) son peores que un solo Project**, porque la separación PROTOCOL/DEV es una **relación** (capacidad P ← habilitada por D ← avanzada por Plan) y dos tableros la destruyen.

---

## Apéndice — Trazabilidad de las afirmaciones de estado

Toda afirmación de este informe sobre el estado actual se ancla a `ruta:sección` o a un comando verificable.

| Afirmación | Evidencia |
|---|---|
| `ROADMAP.md` = 107 líneas y contiene estado | `ROADMAP.md` (medido) |
| Contrato del ROADMAP y su regla de admisión/frescura | `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` |
| Frontera DEV/Protocol y prohibición de mecanismos compartidos | `AGENTS.md`; `docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`; `docs/rfc/75-change-lifecycle.md:Dev vs Protocol` |
| Principios transferibles son principios, no mecanismos | `docs/rfc/75-change-lifecycle.md:Dev vs Protocol` |
| Plan 149 materializó el roadmap A→B→C por pedido directo | `docs/plans/149-argentos-capability-and-autonomy-roadmap.md:Origen` |
| Plan 157 reestructuró el ROADMAP; Plan 158 lo redujo de 367 a 99 líneas | `docs/plans/158-radical-simplification-roadmap.md:Objetivo` y `## Métricas de reducción` |
| Siete ediciones del ROADMAP en tres semanas | Commits `64398ba`, `d05fda8`, y los planes 155/156/157/159/161/163/164 |
| La matriz tiene 9 dimensiones y ninguna es estado objetivo | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md:1.3 Estructura y convención de celdas` |
| 0 de 28 capacidades en «demostrado bajo condiciones reales» | Ídem, `### 4.1 Hallazgo principal` |
| `C-16`/`C-17`/`C-21` fuera de `F-C` | `docs/plans/163-acto-autoridad-od1-alcance-f-c.md:Acto de autoridad registrado (2026-10-12)` |
| `FC-1`…`FC-10` como criterios de cierre de `F-C`, `Change Level ≥ L3` | Ídem, `## Criterios de cierre requeridos del Change de F-C` |
| `C-24` sin medición operacional; Incremento 4 mínimo (C-1/C-2) | `docs/working/audits/…md:### C-24`; `docs/plans/98-*.md` (header, «Naturaleza de este documento») |
| Métricas del lifecycle «sin medición operacional hasta el Incremento 4» | `docs/VERSIONING.md:11. Métricas del Change Lifecycle` |
| 27 planes con determinación `Roadmap impact` en prosa | Medido sobre `docs/plans/**` |
| `Roadmap impact` no tiene checker | `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre: impacto documental e impacto de Roadmap (regla operacional)` |
| `PC-4`/`PC-5`/`F-3` del Plan 136 derivan de `Roadmap impact` | `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/140-governance-residual-closure.md` |
| Independencia de verificación es «dependiente de actores externos» | `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D0 — Guarantee Model` (snapshot histórico; el catálogo que cita) |
| El glosario prohíbe usar «roadmap» para un registro de capacidades | `docs/glossary/terms.md:ROADMAP` |
| 0 issues / 0 PRs / 0 milestones / labels por defecto | `gh issue list --state all`; `gh pr list --state all`; `gh api repos/roldriel/ARgentOS/milestones`; `gh label list` |
| Token sin `read:project` | `gh project list --owner roldriel` → «missing required scopes [read:project]» |
| Sin ramas de feature; todo en `dev` | `docs/VERSIONING.md:1. Ramas y roles`; `AGENTS.md` («Branch policy») |
| Los gates `C-1`/`C-2`/`C-3` no corren en CI | `C-27` de la matriz; `.github/workflows/check-protocol.yml` |
| Plan 165 `Aprobado para ejecución` con diseño sin commitear | `git diff` sobre `docs/plans/165-f-c-autonomy-frontier-implementation.md` (30 inserciones) |
| `MASTER_PENDING_WORK_INVENTORY.md` ya no existe; absorbido por Planes 141/143 | `Test-Path` = False; `docs/plans/141-…md:Origen`; `docs/plans/143-empty-remaining-backlog.md` |
| `HD-K1` exige re-derivación ante cambio de scope | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K (adoptado por el Plan 151, 2026-10-07)` |
| `Roadmap impact: REQUIRED` no autoriza escritura fuera de scope | `docs/plans/136-d01-mechanical-checker.md:<PLAN-136>:F-3` |
| Resolución de findings es decisión humana (ADR-16 `AU-3`) | `.agents/workflows/change-lifecycle.md:7. Findings, corrections and revalidation` |
| Regla «Evidence closure / anti-rework» | `docs/CONVENTIONS.md:Regla transversal — Evidence closure / anti-rework` |
| Regla «target semantics vs operationalización» | `docs/CONVENTIONS.md:Regla transversal — target semantics vs operationalización` |
| El wrapper `lifecycle.py` expone `install`/`update`/`uninstall`/`doctor`/`recover` (sin `validate` ni `upgrade`) | `protocol/.agents/harness/lifecycle.py` (subparsers y handlers) |
| Los user projects existen y trackean repos de la cuenta personal; no hay Project «de repositorio» en cuenta personal | [GitHub Docs — Creating a project](https://raw.githubusercontent.com/anthonysidesapps/docs/2a0fd5d3ea1301bd6b3eca87c960856c08387bb9/content/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project.md) |
| Un proyecto de usuario exige PAT clásico con scope `project` (+`repo`); fine-grained sólo cubre proyectos de organización | [gh-aw — Authentication (Projects)](https://raw.githubusercontent.com/github/gh-aw/b527a7cb50f386594a8a5be5d9576fb99105953d/docs/src/content/docs/reference/auth-projects.mdx) |
| El `GITHUB_TOKEN` de Actions no puede leer ni escribir Projects | Ídem |
| Transferir un Project a un repositorio es un vínculo, no un cambio de dueño | [Community Discussion #193246](https://github.com/orgs/community/discussions/193246) |

---

## Apéndice 2 — Cambio concurrente durante el análisis

**Hecho observado y declarado, no una anomalía.** Entre el inicio y el fin de esta investigación, el working tree de `dev` **cambió por trabajo concurrente ajeno a este informe**. Estado al cerrar el análisis:

```text
 M .agents/policies/supervised-autonomous-execution.md      (+1)
 M docs/plans/165-f-c-autonomy-frontier-implementation.md   (+58)
 M runtime/README.md                                        (+2)
 M tests/AGENTS.md                                          (+1)
?? tests/test_fc_isolation_declaration.py                   (nuevo)
?? docs/planificacion-argentos-diseno-2026-10-13.md         (este informe)
```

Al inicio del análisis el worktree tenía **una** modificación (30 líneas en el Plan 165); al cerrarlo tenía **cuatro modificaciones y dos archivos nuevos**. Es la implementación de `F-C` en curso — exactamente el trabajo que `ROADMAP.md` declaraba inexistente («Trabajo activo: ninguno»).

**Esto no invalida el diagnóstico: lo confirma dos veces.**

1. **Confirma R-5 y el hallazgo A.3:** el mapa de dirección no puede representar el trabajo real, y la divergencia se agrava en tiempo real.
2. **Confirma R-1:** el estado operativo vive en un worktree que cambia sin que ningún artefacto de planificación lo refleje. Un Project de GitHub habría mostrado lo mismo que `ROADMAP.md` — nada — porque la causa no es la herramienta sino la ausencia de un dueño del estado.

**Nota de método:** este informe **no** modificó ninguno de esos archivos ni interfirió con ese trabajo. Sus mediciones son válidas para el estado en que se tomaron; las cifras de líneas y de diff son de ese momento.

---

_Fin del informe. Ninguna modificación estructural fue realizada. El repositorio queda en el estado en que se encontró —salvo el trabajo concurrente de `F-C` ya declarado arriba— con la única excepción de este documento._
