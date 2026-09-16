# Plan 127 — Diseño del Repository/Artifact Placement Contract (cierre de diseño)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=1, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única. *scope*: un dominio y un archivo de gobernanza DEV. *architectural impact*: registra un diseño derivado de arquitectura ya aceptada; no introduce arquitectura nueva. *release impact*: ninguno. *duration/complexity*: acotada. (L1 y no L0 porque lo que se registra es un diseño arquitectónico consumido repo-wide, aunque su materialización esté pendiente.)
**Depende de:** ADR-17 (`docs/adr/17-repository-lifetime-and-composite-structure.md`) y ADR-18 (`docs/adr/18-payload-boundary-provenance-and-classification.md`), que son la arquitectura upstream. Consume, sin modificarlas: RFC-46 (inmutabilidad histórica), RFC-56 (clases de cambio), RFC-75 (lifecycle DEV), ADR-15 y ADR-16 (continuidad y autoridad).
**Origen:** Directiva del mantenedor (2026-09-15) que ordena cerrar formalmente Plan 127 como trabajo de DISEÑO, sin materializar el Placement Contract, tras la corrección final read-only sobre `derived` / `generated`.

## Objetivo

Registrar formalmente el cierre de diseño de Plan 127 y persistir, como traza reproducible en el repositorio, el resultado del diseño del **Repository/Artifact Placement Contract** — incluido el modelo semántico corregido, el algoritmo de resolución, el modelo de STOP, el modelo de excepciones y las decisiones que quedan **explícitamente abiertas**.

Este plan **no** materializa el Placement Contract, **no** crea registry, checker, schema, namespace ni ADR, **no** autoriza migración alguna y **no** modifica la arquitectura aceptada.

**Hallazgo de registro.** El diseño de Plan 127 y su correction report fueron producidos como análisis read-only y **no existían como artefacto versionado** (`git status` limpio en `50771b6`; sin archivo de diseño ni de Placement Contract en el árbol; sin referencias a `127` en los INDEX). Este plan es, por tanto, el registro persistente mínimo que hace el diseño reproducible desde el repositorio, sin crear el contrato.

## Criterio de entrada

- [x] `dev` limpio en `50771b6cd7828b1fd4b3dafdf8f4b7997d664278` (verificado con `git status --short` y `git rev-parse HEAD`).
- [x] ADR-17 y ADR-18 presentes y `Accepted` como arquitectura upstream.
- [x] Diseño de Plan 127 completado y corregido (correction report `CANONICALITY — DERIVED vs GENERATED`) verificado sobre el mismo baseline.
- [x] Confirmado que no existe Placement Contract, ni registro de Plan 127, ni migración en curso.
- [x] Autorización humana explícita para registrar el cierre (directiva del mantenedor de esta sesión).

## Entregables

1. `docs/plans/127-repository-artifact-placement-contract-design.md` (**este archivo**) — registro del diseño y de su cierre.
2. `docs/plans/INDEX.md` — registro de este plan (tabla + serie + encabezado de estado).
3. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 127).

## Pasos

1. Verificar baseline (HEAD, branch, working tree) y ausencia de artefactos previos de Plan 127.
2. Persistir el diseño: tesis central, modelo semántico, inventario de familias, modelo de canonicalidad, algoritmo, STOP, excepciones, moves, distribución/lifetime, contrato de agente, verificabilidad, integración con el Orchestrator, mapeo current→target y alternativas.
3. Registrar las correcciones aplicadas durante el diseño (C1–C9) con su relación BEFORE/AFTER/REASON.
4. Registrar las cuatro decisiones que permanecen **ABIERTAS** sin inferir respuesta.
5. Clasificar el estado final del Plan 127.
6. Ejecutar la batería canónica y los gates de lifecycle; registrar anchor y checkpoint.

## Criterios de salida

- [ ] El diseño queda persistido y es reproducible desde el repositorio, sin haber creado el Placement Contract.
- [ ] La regla central queda registrada literalmente: canonicality **cualifica** placement, no lo determina; placement requiere regla explícita; sin regla → STOP.
- [ ] `generated` y `derived` quedan registrados sin las sobre-generalizaciones prohibidas.
- [ ] Las cuatro decisiones pendientes (`OQ-2`, `OQ-3`, `OQ-4`, `PC-1`) permanecen abiertas y sin resolver.
- [ ] Sin Placement Contract, sin registry, sin checker, sin schema, sin namespace nuevo, sin state machine, sin clase de autoridad, sin ADR adicional, sin migración.
- [ ] `protocol/`, `runtime/`, `tools/`, `tests/` sin cambios; DEV ≠ Protocol intacto.
- [ ] Batería canónica y gates de lifecycle registrados con resultado real.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --name-status
```

---

## 1. Tesis central del diseño

```text
DISCRIMINADORES      domain/owner  →  kind/family
                         ↓
REGLA DE FAMILIA     canonical namespace  (tabla domain-scoped)
                         ↓
CUALIFICADOR         canonicality status  (cómo se interpreta la ubicación)
                         ↓
CONSTRAINTS          domain boundary · historical status · distribution ·
                     dependency direction · discovery · mutation authority
                         ↓
                     PLACE  |  STOP
```

**Propiedad de seguridad:** *no unique canonical placement → no guessing → STOP.*

**Qué NO debe ser el contrato:** no taxonomía global de carpetas (ADR-17 `RS-2`/`RS-3`); no registry; no ID space; no subsistema runtime; no fuente de autoridad; no autorización de migración (`RS-7`); no enum cerrado de kinds (`RS-11`); no segunda fuente de verdad para la semántica de frontera ya fijada por ADR-18.

## 2. Modelo semántico

### Discriminadores (necesarios y suficientes para seleccionar namespace)

| Dimensión | Rol | Evidencia |
|---|---|---|
| **Domain / owner** | Discriminador primario; la tabla de reglas está *domain-scoped* | **[FACT]** Protocol: 7 namespaces bajo `protocol/.agents/`. DEV: `.agents/{policies,workflows}`, `docs/`, `runtime/`, `tools/`, `tests/` |
| **Artifact kind / family** | Discriminador secundario; dentro del dominio selecciona la regla de familia | **[FACT]** `RFC→docs/rfc/`, `ADR→docs/adr/`, `contract→protocol/.agents/contracts/` |

**`kind` NO es un enum global cerrado del repositorio.** **[FACT]** ADR-18 `RS-11`; `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md:Protocol Taxonomy`. Consecuencia normativa: `Protocol + contract → protocol/.agents/contracts/`; **`DEV + contract → STOP (NEW FAMILY)`** — nunca `.agents/contracts/` por simetría. **[INFERENCE]**

### Cualificador (interpreta; nunca selecciona)

**Canonicality status** — `source-of-truth` · `derived` · `generated` · `historical` · `fixture` · `scratch`. Nunca selecciona y **nunca crea** una namespace.

### Constraints (pueden prohibir o señalar; no pueden elegir)

Dominio (frontera), estatus histórico, distribución (derivada de domain+namespace), dirección de dependencia (la única regla dura: el payload no depende de DEV), discovery (INDEX opcional; una familia puede exigirlo), autoridad de mutación (¿puede escribir *este* Change?).

### Metadata (se registra, no coloca)

**Authority class**, **lifetime/persistence**, productor, consumidor, scope. Lifetime se registra por familia y **no** crea topología; la única prohibición que implica (session-ephemeral fuera de durable y viceversa) ya la declara el Protocol y el contrato la **referencia**, no la repite.

### Ortogonal

**Identidad** (`RFC-N`, `ADR-N`, `plan NN`), versión/release, Change Level.

## 3. Modelo de canonicalidad (corregido)

**Tres ejes ortogonales, nunca colapsados:**

```text
MECANISMO DE PRODUCCIÓN   ESTATUS DE CANONICALITY        PLACEMENT
cómo se produce            cómo se relaciona con su      dónde vive
                           fuente y con el repositorio
──────────────────         ────────────────────────       ──────────────────
hand-authored        ─┐    source-of-truth          ─┐
generated (tool/CI)  ─┴─   derived                   │
                           generated                 ├─→  SIEMPRE de una
                           historical                │    REGLA EXPLÍCITA
                           fixture                   │    (familia · generador ·
                           scratch                   ┘     mecanismo que lo produce)
                                                                  │
                                                          ¿sin regla? → STOP
```

**Regla universal única:** *canonicality status no selecciona placement y no crea namespace.*

| Estatus | Qué describe | De dónde viene la ubicación | ¿Crea namespace? |
|---|---|---|---|
| **source-of-truth** | contenido autorado y editado aquí | la namespace de authoring de la regla de familia | No |
| **derived** | representación regenerable de otra fuente | la namespace de representación designada por la regla de familia; **si no hay ninguna designada, comparte la namespace de familia** | **No** |
| **generated** | contenido producido automáticamente por herramienta, proceso o CI | la ubicación **explícitamente designada** por su regla de familia, su generador o el mecanismo que lo gobierna; **sin default; ausencia de designación → STOP** | **No** |
| **historical** | congelado tras el cierre | conserva su ubicación existente | No |
| **fixture** | sustituto sintético del test subsystem | la namespace de fixtures designada por el test subsystem | No |
| **scratch** | desechable, no canónico | el mecanismo/ubicación desechable designado | No |

**Dos desambiguaciones explícitas:**

```text
generated ≠ non-canonical
    (cierto de dist, __pycache__ y .project/orchestrator/ — y no coloca a ninguno)

derived ≠ same namespace
    (cierto de docs/*/INDEX.md — y la colocalización es una elección de familia,
     no una consecuencia de derivar)
```

**Falsificación empírica que sostiene la corrección.** Cuatro artefactos generados o derivados, cuatro ubicaciones canónicas distintas, ninguna deducible del hecho de ser generado/derivado: **[FACT]**
- `dist` → **branch** generado por CI, fuera del working tree (`publish-dist.yml`, `.gitignore`);
- `__pycache__/` (2 en el payload) → en el árbol, **ignorado**, 0 archivos trackeados;
- `.project/orchestrator/**` (367 archivos) → en el árbol, ignorado, área de evidencia del host;
- `docs/{plans,rfc,adr}/INDEX.md` → **derivados, versionados y visibles**, junto a su familia.

## 4. Inventario de familias

**15 familias canónicas** (con lookup domain-scoped y namespace), **3 reglas root-anchored** (la ubicación la dicta un constraint externo, no un lookup de familia) y **2 no-familias registradas** (fuera del contrato).

### Familias canónicas

| # | Familia | Dominio | Namespace canónica | ¿Se distribuye? |
|---|---|---|---|---|
| **F1** | Política normativa DEV | DEV | `docs/*.md` (raíz) | No |
| **F2** | Instrucción operacional DEV | DEV | `.agents/{AGENTS.md,policies/,workflows/}` | **No** |
| **F3** | RFC | DEV | `docs/rfc/` (plana) | No |
| **F4** | ADR | DEV | `docs/adr/` (plana) | No |
| **F5** | Plan | DEV | `docs/plans/` (plana) | No |
| **F6** | Working analysis | DEV | `docs/working/{audits,research,proposals}/` | No |
| **F7** | Inventory / registro descriptivo | DEV | `docs/glossary/` | No |
| **F8** | Navegación / INDEX | DEV **y** Protocol (por instancia) | junto a su familia, cuando esa familia lo exige | INDEX del payload sí; de DEV no |
| **F9** | Ejecutable de verificación DEV | DEV | `tools/` (plana) | **No** |
| **F10** | Runtime de referencia DEV | DEV | `runtime/<package>/` | **No** |
| **F11** | Test subsystem DEV | DEV | `tests/` (+ `fixtures/`) | **No** |
| **F12** | Payload Protocol — spec y capacidad | Protocol | `protocol/.agents/{contracts,delegation,standards,orchestrators,roles,skills}/` | **Sí** |
| **F13** | Harness ejecutable Protocol | Protocol | `protocol/.agents/harness/` | **Sí** |
| **F14** | Estado de ejecución de sesión | Protocol runtime | `.project/<uuid>/<iter>/`; `.project/orchestrator/` | No (ignorado) |
| **F15** | Estado project-durable | Protocol runtime | `.project/changes/`, `.project/knowledge/` | No (ignorado en DEV) |

### Reglas root-anchored (no son familias)

| # | Artefacto | Por qué no es familia | Ubicación |
|---|---|---|---|
| **R1** | EntryPoint (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`) | sin lookup de kind: la ubicación la dicta la convención de visibilidad, y su clase documental la deriva la carta | raíz del repositorio |
| **R2** | `conftest.py` raíz | infraestructura de sesión de test; la ubicación la dicta el requisito de colección de pytest | raíz del repositorio |
| **R3** | Configuración de CI | configuración; la ubicación la dicta el path fijo de la plataforma | `.github/workflows/` |

### No-familias registradas (fuera del contrato)

**N1** `dist` — **branch** generado y publicado por CI, nunca editado a mano, ausente del working tree. **N2** `sessions/` — área externa desechable, untracked. También excluidos: `protocol/.project/` (efecto de probe, ADR-18 `RS-15`) y los directorios generados ignorados (`__pycache__`, `.mypy_cache`, `.pytest_cache`).

**Defectos del inventario original ya corregidos y registrados aquí:** el encabezado decía «catorce familias» con una tabla de veinte entradas; las veinte no eran veinte familias (EntryPoint, `conftest.py` y CI config no tienen lookup de kind; `dist` y `sessions/` no tienen owner ni regla). **Ubicaciones actuales que NO deben generalizarse:** los 3 documentos no-Plan en `docs/plans/` (excepciones declaradas); `docs/AUDITORIA_DOCUMENTACION.md` en la raíz de `docs/` (Working/Audit clasificado en el lugar, `RS-12`); `docs/architecture/` (nombre legacy, clase Historical); `runtime/` es **una** familia con dos paquetes; `tests/` es **una** familia con dos formas de contenido (suites y fixtures), distinguidas por el cualificador.

## 5. Algoritmo de resolución de placement

```text
PASO 1 — IDENTIFICACIÓN SEMÁNTICA
         Describir el artefacto y producir un *candidato* de kind (no una clave aún).
         Sin kind nombrable                                  → STOP (UNKNOWN KIND)

PASO 2 — DOMAIN / OWNER                        [DISCRIMINADOR 1 — único]
         Resolver por precedencia:
           a. quién tiene la autoridad para cambiarlo (Protocol → RFC-56; DEV → Change DEV)
           b. si los adoptantes lo reciben
           c. qué familia de namespace lo posee en la tabla
         0 candidatos                                        → STOP (NO DOMAIN)
         >1 candidato                                        → STOP (CROSS-DOMAIN AMBIGUITY)
         REGLA: estar *sobre* el Protocol ≠ ser *poseído* por el Protocol.

PASO 3 — KIND / FAMILY                         [DISCRIMINADOR 2]
         Buscar el kind en la tabla DOMAIN-SCOPED.
           ninguna regla en este dominio                     → STOP (NEW FAMILY)
           >1 regla en este dominio                          → STOP (AMBIGUOUS KIND)
         REGLA: no resolver una regla DEV ausente por simetría con Protocol.

PASO 4 — CANONICAL NAMESPACE
         La regla de familia produce la namespace canónica.
           ninguna                                           → STOP (UNDEFINED PLACEMENT)
           más de una                                        → STOP (TWO VALID LOCATIONS)

PASO 5 — CANONICALITY QUALIFICATION       [CUALIFICADOR — no selecciona,
                                           no crea namespace]
         Clasificar el artefacto y tomar la ubicación de una REGLA EXPLÍCITA.
         Ninguna rama de este paso puede derivar una ubicación del estatus mismo.

         source-of-truth → la namespace del PASO 4.
         derived         → la namespace de representación designada por la regla
                           de familia; si no hay ninguna, la del PASO 4.
                           NUNCA inventar una namespace de representación.
         generated       → la ubicación designada explícitamente por su regla de
                           familia, su generador o el mecanismo que lo gobierna.
                           NO hay default. Sin designación explícita
                           → STOP (UNDEFINED PLACEMENT).
         historical      → conserva su ubicación existente.
         fixture         → la namespace de fixtures del test subsystem.
         scratch         → el mecanismo/ubicación desechable designado.

         INVARIANTE: canonicality status NUNCA crea una namespace. Si el estatus
         no resuelve ubicación por una regla EXISTENTE → STOP, nunca inferencia.

PASO 6 — AUTHORITY Y LIFETIME                  [METADATA — no seleccionan]
         Declarar autoridad y lifetime con independencia de la ubicación.
           autoridad desconocida o en disputa                 → STOP (AUTHORITY UNRESOLVED)
         Si es project-durable, registrar `git_committed` por separado;
         el contrato NO lo decide.                             [RS-5; PC-1 ABIERTO]

PASO 7 — VALIDACIÓN DE CONSTRAINTS             [no re-selecciona]
         a. ¿frontera de dominio respetada?
         b. ¿artefacto nuevo (permitido) o relocalización de uno congelado (no autorizada aquí)?
         c. ¿cambiaría lo que reciben los adoptantes? (si sí → cuestión RFC-56, no placement)
         d. ¿haría que el payload dependa de DEV? (si sí → rechazar; citar RS-10)
         e. ¿la regla de ESTA familia exige un INDEX? (nunca universal)
         f. ¿el Change actual está autorizado a escribir aquí?
         Cualquier violación                                  → STOP (CONSTRAINT VIOLATION)

PASO 8 — COLOCAR Y REGISTRAR
         Registrar: dominio, kind/familia, namespace canónica, estatus de
         canonicality, autoridad, lifetime y referencia de excepción si la hay.
         Placement NO confiere autoridad.
```

## 6. STOP semantics

| Trigger | Paso | Clase | Escala a |
|---|---|---|---|
| UNKNOWN KIND | 1 | regla ausente | humano |
| NO DOMAIN | 2 | ownership ausente | humano |
| CROSS-DOMAIN AMBIGUITY | 2 | ownership contradictorio | humano |
| NEW FAMILY | 3 | regla ausente | humano + governance (enmienda de la tabla) |
| AMBIGUOUS KIND | 3 | regla contradictoria | humano |
| UNDEFINED PLACEMENT | 4 y 5 | regla ausente | humano |
| TWO VALID LOCATIONS | 4 | regla contradictoria | humano |
| AUTHORITY UNRESOLVED | 6 | autoridad contradictoria | humano (ADR-16 AU-3) |
| CONSTRAINT VIOLATION | 7 | constraint violado | humano o el artefacto que autoriza el Change |

**Mapeo al modelo existente — sin mecanismo nuevo:** regla ausente ≈ **GAP**; regla contradictoria ≈ **ANOMALY**; constraint violado → **`REQUIRES_HUMAN`**. No se crea clase de autoridad, estado de lifecycle ni estado de state machine. **[INFERENCE]** conforme a `.agents/policies/authority.md:Stop conditions (authority)`.

## 7. Modelo de excepciones

| Estatus | Autorizado por | Registrado en | ¿Se vuelve regla? |
|---|---|---|---|
| Canónica | n/a | el contrato | es la regla |
| Excepción autorizada | humano, en el artefacto que posee la decisión | **en el artefacto poseedor** — no en un registry | **No** |
| Ubicación histórica | ya congelada (RFC-46) | banner del artefacto + su INDEX | **No** — no es precedente |
| Temporal / scratch | no requiere | en ningún lado | No |
| Generada | herramienta/CI | `.gitignore`, el branch o el mecanismo designado | No |

Propiedades: acotada; por artefacto o por familia, **nunca por namespace** (espeja el rechazo de `RS-9` a excepciones por prefijo); una segunda instancia requiere su propia autorización; una excepción es permanente **como registro**, nunca como regla; **la recurrencia de excepciones es evidencia de que la regla está mal** y la respuesta es enmendarla por governance. Instancias vivas: 3 documentos no-Plan en `docs/plans/`; `docs/AUDITORIA_DOCUMENTACION.md`; 2 citas de provenance del payload; `conftest.py` raíz.

## 8. Move / rename

Colocar un artefacto nuevo (regla de familia) **≠** migrar uno existente (Change Lifecycle + política histórica + `RS-7`). **Una regla de placement nunca autoriza un movimiento.** Requisitos antes de relocalizar: Change autorizado; justificación de que la nueva ubicación *es* canónica bajo la tabla; para payload, RFC-56 y consecuencia de distribución declarada; resolución de citas preservada (las históricas no se reescriben, RFC-46; el mapping legacy es el mecanismo); consistencia anchor/checkpoint si es artefacto de gobernanza; sin cruzar la frontera DEV/Protocol sin la vía de autorización del dominio correspondiente. Nunca se relocaliza historia congelada por prolijidad. **Un rename que cambia la identidad no es un rename, es un artefacto nuevo.**

## 9. Distribución y lifetime

**Distribución (corregida a domain+namespace-scoped).** `protocol/.agents/` — incluidos `harness/` y `harness/tests/` — **se distribuye**; el `.agents/` de DEV (`AGENTS.md`, `policies/`, `workflows/`) **no se distribuye nunca**; `runtime/`, `tools/`, `tests/`, `docs/` tampoco. **[FACT]** `.github/workflows/publish-dist.yml` (paso de publicación) copia sólo `protocol/.agents`, y ningún workflow copia el `.agents/` raíz. El token desnudo `.agents/` **no** es determinante de distribución y no debe usarse como tal. La distribución es **constraint** (paso 7c), nunca selector; un placement que cambiaría lo que recibe el adoptante es una cuestión RFC-56. No se propone ni se necesita cambio alguno en `publish-dist.yml`.

**Lifetime.** Semantic, declarado por familia, nunca topología: el contrato registra `lifetime` y `git_committed` por separado (`RS-5`) y no decide el segundo. Prohibido: `all project-durable → .project/durable/` (`RS-2`, `RS-3`).

## 10. Contrato del agente autónomo

| Caso | Determina solo | Debe verificar | STOP | Autoridad |
|---|---|---|---|---|
| **A. Artefacto nuevo** | dominio, kind/familia, namespace (pasos 2–4) | canonicality, autoridad, lifetime, constraints, autoridad de mutación | si algún paso da 0 o >1; si no hay regla; si el target está en el otro dominio | sólo la que ya le otorga el Change |
| **B. Artefacto existente, ubicación dudosa** | si el path actual es la namespace canónica de su familia | si la discrepancia es excepción autorizada, ubicación histórica o *drift* | sí, si es *drift*: **reporta, no mueve** | mover requiere un Change |
| **C. Ubicación no canónica pedida** | la namespace canónica; la declara | si existe excepción autorizada | sí, salvo que quien pide tenga la autoridad del dominio → **registrar la excepción y luego colocar**; una petición no es una autorización | humana |
| **D. Familia nueva** | que ninguna regla domain-scoped coincide | familias más cercanas y por qué no alcanzan | **siempre**; no crea namespace ni inventa regla | humana + governance |
| **E. Artefacto cross-domain** | que el paso 2 dio dos candidatos | ambas lecturas de ownership, qué se compartiría, por qué está prohibido | **siempre** (el STOP más importante) | humana; resolución típica: **dividir** en dos artefactos, o relación de **conformance/reference** (permitida) en vez de ownership compartido (prohibido) |

**Desambiguación:** un artefacto **DEV que referencia el Protocol** no es cross-domain (DEV puede leer el payload). Un artefacto **Protocol que referencia DEV** sí es cuestión de frontera, ya gobernada por la allowlist (`RS-9`/`RS-10`). **Precedencia cuando ambas lecturas sobreviven:** gana el dominio cuya autoridad debe autorizar el cambio; si no, STOP. El agente no puede elegir el dominio más barato.

## 11. Machine-verifiability

| Regla | Clase | Base |
|---|---|---|
| El path pertenece a la namespace permitida de la familia | Verificable mecánicamente | chequeo de path |
| El artefacto declara metadata `kind` | Parcialmente verificable | presencia sí; **valor no**, porque `tags.kind` es no exhaustivo (`RS-11`) |
| Frontera de dominio (payload → DEV) | **Verificable y ya aplicada** | ADR-18 `RS-10`; `tools/check_protocol_invariants.py` |
| Frontera de dominio (DEV → payload) | Verificable como chequeo de path | no aplicada hoy; este diseño no propone cambiarlo |
| **`generated` como característica de producción** | **Verificable mecánicamente** | detectable (marca del generador, `.gitignore`, el branch, el contrato del generador) |
| **A qué ubicación pertenece un `generated`** | **Verificable sólo si** la regla de familia/generador **designa explícitamente** la ubicación | no hay default; sin designación → STOP |
| Estatus distribuido / no distribuido | Verificable | derivado de (dominio, namespace); `publish-dist.yml` es la autoridad |
| Presencia de INDEX | Condicionalmente verificable | sólo para familias cuya regla lo exija; nunca universal (`RS-14`) |
| Declaración de lifetime | No automatizable de forma significativa | valores semánticos; sin mapeo global (`RS-2`) |
| Fuente canónica vs copia derivada | Parcialmente verificable | una marca «derived» es chequeable; la afirmación es juicio |
| Presencia de excepción | Depende de `OQ-2` | verificable **si** las excepciones se vuelven localizables de forma convencional |
| «Este artefacto pertenece a esta familia» | Juicio semántico/humano | el núcleo irreducible |
| «Esta relocalización está justificada» | Juicio humano | `RS-3`, `RS-7` |

**No se afirma** que `generated → outside repository`, ni `→ ignored`, ni `→ branch`, ni `→ non-canonical` como regla universal. No se crea checker.

## 12. Integración con el Orchestrator

El host DEV ya lee el plan autorizado, observa snapshots de contenido, verifica el scope declarado y deriva la próxima acción. **[FACT]** `runtime/README.md:DEV Autonomous Orchestrator (Plan 122)`. Puntos de consulta, del más temprano al más tardío: (1) **antes de la delegación al Worker** (preflight de placement contra los artefactos declarados en el plan) — preferido, porque un conflicto se detecta antes de cualquier escritura; (2) **después de la ejecución del Worker**, extendiendo la verificación de scope/path que ya existe; (3) **durante la verificación/cierre**, como evidencia dentro de los registros de validación existentes. **No se crea** gate, estado, transición, registry ni lifecycle de placement. Un conflicto de placement se expresa con el vocabulario existente (GAP / ANOMALY / `REQUIRES_HUMAN`).

## 13. Current → Target

**No se propone ni se autoriza migración alguna.** La columna «canonicality» (estatus) y «placement actual» (ubicación) son **distintas** por diseño.

| Familia / regla | Canonicality status | Placement canónico | Estado de la ubicación actual |
|---|---|---|---|
| F1 Política DEV | source-of-truth | `docs/` raíz | **canonical** |
| F2 Operacional DEV | source-of-truth | `.agents/{AGENTS.md,policies,workflows}` | **canonical** |
| F3 RFC | source-of-truth → historical al congelarse | `docs/rfc/` plana | **canonical** |
| F4 ADR | source-of-truth | `docs/adr/` plana | **canonical** |
| F5 Plan | source-of-truth → historical | `docs/plans/` plana | **canonical** |
| F5 support docs | source-of-truth | no generalizable | **exception** (3 declaradas) |
| F6 Working | source-of-truth / historical | `docs/working/<bucket>/` | **canonical** |
| F6 `AUDITORIA_DOCUMENTACION.md` | historical | hogar Working es `docs/working/audits/` | **exception** (clasificada en el lugar, `RS-12`) |
| F7 Inventory | source-of-truth (descriptivo) | `docs/glossary/` | **canonical** |
| `docs/architecture/*` | **historical** | ninguna para artefactos nuevos | **historical** (nombre legacy) |
| F8 Navegación | **derived** | junto a su familia cuando ésta lo exige | **canonical**; opcional en el resto |
| F9 tools | source-of-truth | `tools/` plana | **canonical** |
| F10 runtime | source-of-truth | `runtime/<package>/` | **canonical** (una familia, dos paquetes) |
| F11 tests + fixtures | source-of-truth; fixtures = **fixture** | `tests/` (+ `fixtures/`) | **canonical** |
| F12 Payload spec | source-of-truth | `protocol/.agents/<familia>/` | **canonical** |
| F13 Payload harness | source-of-truth | `protocol/.agents/harness/` | **canonical** |
| excepción | — | n/a | **exception** (2 citas de provenance, allowlisted) |
| F14 Sesión | **generated** | `.project/<uuid>/<iter>/` | **canonical, disposable** |
| F15 Project-durable | source-of-truth; `project_segment.json` **derived** | `.project/changes/`, `.project/knowledge/` | **canonical** (path fijado por ADR-17 §4); Git persistence **`PC-1` ABIERTO** |
| R1 EntryPoint | source-of-truth | raíz | **canonical** |
| R2 `conftest.py` | source-of-truth (infra) | raíz (constraint de pytest) | **canonical, constrained** |
| R3 CI config | source-of-truth (config) | `.github/workflows/` | **canonical** |
| **N1 `dist`** | **generated — branch / salida de distribución** | el branch `dist` | **no es artefacto del working tree** |
| N2 `sessions/` | **scratch** | mecanismo desechable externo | **external / disposable** |
| `protocol/.project/` | no es artefacto | — | **excluido** (`RS-15`) |

## 14. Alternativas evaluadas y recomendación

| Criterio | **A. Minimal semantic** | **B. Structured placement** | **C. Machine-oriented** | **D. Reference-only** |
|---|---|---|---|---|
| Contenido | ~8 invariantes, sin tabla | vocabulario + tabla **domain-scoped** + constraints + excepciones + algoritmo | schema estructurado para chequeo automático | citas a reglas existentes + STOP + algoritmo, sin tabla |
| Determinismo | medio: sigue infiriendo familias no listadas | **alto: cada paso termina en namespace o STOP** | alto para paths, **bajo para el núcleo semántico** | STOP-heavy: no responde placement |
| Mantenimiento | muy bajo | moderado: ~15 líneas de regla | **alto**: versionado de schema y deriva prosa↔schema | muy bajo |
| Riesgo de sobrerregulación | bajo | moderado, acotado por STOP | **alto** | ninguno |
| Compatibilidad con la gobernanza | buena | **buena** — mismo idioma documental que `docs/source-layout.md` y `docs/CONVENTIONS.md` | pobre: se vuelve segunda autoridad y registry de facto | buena pero inerte |
| Riesgo de registry | ninguno | **bajo** si las excepciones viven en el artefacto poseedor | **alto** | ninguno |

**Recomendación (no es decisión humana): B — Structured Placement Contract**, DEV-owned, acotado. **Reevaluada tras las correcciones:** la corrección de `generated`/`derived` **refuerza** B, porque el modelo queda con exactamente dos claves de lookup (dominio, kind) y la canonicality deja de tentar como tercer eje; y el inventario corregido (15 familias + 3 reglas root-anchored) hace que la tabla sea un artefacto genuinamente acotado. Ninguna corrección debilita B. Su núcleo verificable es pequeño y estable (ownership, path, frontera, registro de excepciones), lo que coincide con la asimetría de verificabilidad en lugar de pelearla.

## 15. Correcciones aplicadas durante el diseño

Se registran con su relación BEFORE / AFTER / REASON. La arquitectura aceptada (ADR-17/ADR-18) no fue reabierta en ninguna.

| # | BEFORE | AFTER | REASON |
|---|---|---|---|
| **C1** | «Everything under `.agents/` ships as-is» — afirmación sin cualificar, luego en contradicción con tratar el `.agents/` de DEV como no distribuido | Distribución declarada para **`protocol/.agents/`** (se distribuye) y para el **`.agents/` de DEV** (nunca) como dos hechos distintos | **[FACT]** `.github/workflows/publish-dist.yml` (paso de publicación) copia sólo `protocol/.agents`; ningún workflow copia el `.agents/` raíz. El token desnudo designaba dos namespaces distintos |
| **C2** | §4 decía «catorce familias» con una tabla de F1–F20 | **15 familias canónicas + 3 reglas root-anchored + 2 no-familias** | El 14 era un error; pero 20 tampoco eran 20 familias: EntryPoint, `conftest.py` y CI config no tienen lookup domain-scoped, y `dist`/`sessions` no tienen owner ni regla |
| **C3** | Tres «placement determinants» (dominio, kind, **canonicality**), aunque el algoritmo mostraba que canonicality heredaba la namespace de su familia | **Dos discriminadores** (dominio/owner, kind/family) + **un cualificador** (canonicality) + constraints | Una propiedad que nunca selecciona namespace no es un determinante |
| **C4** | Domain-first argumentado en prosa; `kind` nunca declarado explícitamente no-enum global | **`kind` no es enum global cerrado**; tabla **domain-scoped**; `DEV + contract → STOP (NEW FAMILY)` como ejemplo | Alinea con ADR-18 `RS-11`; evita inventar `.agents/contracts/` por simetría |
| **C5** | Modelo de excepciones definido | Igual en sustancia; re-marcado como **preferencia, no decisión irrevocable** | La revisión humana confirmó el modelo; la localizabilidad machine-readable queda abierta |
| **C6** | §18 listaba la ubicación del contrato como decisión humana, pero la prosa de recomendación insinuaba `docs/` raíz | Queda **HUMAN DECISION REQUIRED** con comparación ampliada de seis propiedades; ninguna opción seleccionada | La directiva prohíbe decidirla |
| **C7** | Implicaba que materializar la decisión podría requerir ADR nuevo | Relación `ADR-17/ADR-18 → Placement Contract` explícita; **ADR nuevo sólo si la materialización introduce arquitectura/invariante no cubierto** | Evita asumir que toda materialización genera un ADR |
| **C8** | `.project/changes/` sin resolver, pero anotado dentro de una lista genérica | Elevado a **`OPEN / DEFERRED — PC-1`** con el límite exacto de lo que el contrato puede afirmar | La directiva prohíbe resolverlo |
| **C9** | §7 STEP 5: `generated / scratch → outside canonical state`; §5 trataba `derived` como casi equivalente a colocalización | `generated` y `derived` **cualifican**; la ubicación viene **siempre de una regla explícita**; sin designación → **STOP (UNDEFINED PLACEMENT)**. `scratch` conserva su semántica desechable. `historical` y `fixture` sin cambios | **Sobre-generalización**: el mecanismo de producción no es un estatus de canonicality ni un placement. Falsificado por las cuatro ubicaciones divergentes de `dist`, `__pycache__`, `.project/orchestrator/` y `docs/*/INDEX.md`. No se añadió STOP nuevo: se reutiliza `UNDEFINED PLACEMENT` |

## 16. Decisiones explícitamente pendientes

No se infiere respuesta para ninguna. No se convierten en decisiones del Plan 127.

| ID | Pregunta | Estado |
|---|---|---|
| **OQ-2** | ¿Las excepciones de placement deben ser machine-locatable? Preferencia arquitectónica actual: registradas en el artefacto que ya posee la decisión; **no irrevocable**. No se crea JSON/YAML/SQLite registry, base de excepciones ni índice global de placement | **`OPEN`** |
| **OQ-3** | ¿Dónde debe vivir canónicamente el Placement Contract? Opciones: (A) documento independiente bajo `docs/`, junto a las seis Policy de raíz y con `docs/source-layout.md` como precedente directo; (B) sección/apéndice de `docs/AGENTS.md`, máxima localidad con el modelo documental pero acoplamiento fuerte y riesgo de leer placement como instrucciones de agente | **`OPEN — HUMAN DECISION REQUIRED`** |
| **OQ-4** | ¿La materialización requiere un ADR nuevo? Relación: ADR-17 + ADR-18 → Placement Contract, que es **downstream** y no fuente de autoridad arquitectónica (`RS-6`). ADR nuevo **sólo** si la materialización introduce una arquitectura o invariante no cubierto | **`OPEN — HUMAN DECISION REQUIRED`** |
| **PC-1** | Persistencia Git de `.project/changes/` (`project-durable ≠ git-committed`, `RS-5`) | **`OPEN / DEFERRED`** |
| OQ-5 | Renombrar `docs/architecture/` | `CLOSED for this design` (`RS-12` lo mantiene en su lugar) |

**No se registró ningún `DECISION REQUIRED`.** Ninguna corrección requirió cambio de ownership, de frontera DEV/Protocol, de autoridad, de lifecycle, de state machine, de persistencia, de distribución, de identidad, de entidad ni de mecanismo de registry.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-127>:F-1` — estado: `open`; observación: el diseño de Plan 127 y su correction report se produjeron como análisis read-only y no existían como artefacto versionado en el repositorio, de modo que el resultado del diseño no era reproducible desde el árbol ni auditable sin la sesión que lo produjo; evidencia original: `git status` limpio en `50771b6`, ausencia de archivo de diseño y de Placement Contract en el árbol, y ausencia de referencias a `127` en `docs/plans/INDEX.md`, `docs/adr/INDEX.md` y `CHANGELOG.md`; estado Git observado: `dev` @ `50771b6`, working tree limpio; provenance original: cierre formal de Plan 127 ordenado por el mantenedor (2026-09-15); resolución: este plan persiste el diseño y su corrección como traza versionada, sin materializar el contrato.

### Correcciones

- `<PLAN-127>:C-1` — refs origen: `<PLAN-127>:F-1`; alcance de revalidación: `docs/plans/127-repository-artifact-placement-contract-design.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`; evidencia (Git/commit/estado): el diseño queda versionado y la batería canónica pasa; commit atómico de cierre.

### Pending decisions

- `<PLAN-127>:PC-1` — decisión: persistencia Git de `.project/changes/`; blocking: no; owner: mantenedor; escalación: vía RFC-56 si se autoriza el cambio de semántica de persistencia del contrato Protocol; resolución: pendiente; evidencia: ADR-17 `RS-5` separa project-durable de git-committed; `git ls-files .project` = 0 y `.gitignore` ignora `.project/`.
- `<PLAN-127>:PC-2` — decisión: `OQ-3`, ubicación canónica del Placement Contract; blocking: sí para la materialización futura, no para este cierre; owner: mantenedor; escalación: decisión humana directa; resolución: pendiente; evidencia: comparación de seis propiedades registrada en `## 16`.
- `<PLAN-127>:PC-3` — decisión: `OQ-4`, ADR-worthiness de la materialización; blocking: no; owner: mantenedor; escalación: decisión humana directa; resolución: pendiente; evidencia: `.agents/policies/authority.md:ADR-worthiness` y ADR-17 `RS-6`.
- `<PLAN-127>:PC-4` — decisión: `OQ-2`, localizabilidad machine-readable de las excepciones; blocking: no; owner: mantenedor; escalación: decisión humana directa; resolución: pendiente; evidencia: `## 7` y `## 11`.

## Riesgos

- **Tomar el cierre de diseño por autorización de materialización.** Mitigación: la clasificación de estado final distingue `Design: CLOSED` de `Placement Contract: NOT CREATED` y `Release: NOT AUTHORIZED`.
- **Convertir el registro del diseño en una segunda fuente de autoridad arquitectónica.** Mitigación: este plan **referencia** ADR-17/ADR-18 y no los reinterpreta ni los enmienda; `RS-6` se cita explícitamente.
- **Derivar decisiones abiertas por comodidad.** Mitigación: `OQ-2`/`OQ-3`/`OQ-4`/`PC-1` se registran como pendientes con su vía de escalación y sin respuesta.

## Trazabilidad

Revisión de arquitectura read-only (`4cd11ed`) → decisiones A/B/F/L (plan 125, ADR-17) → decisiones C–K (plan 126, ADR-18) → diseño del Repository/Artifact Placement Contract (plan 127, este registro) → **decisión humana pendiente** (`OQ-2`/`OQ-3`/`OQ-4`, `PC-1`) → materialización del contrato (no autorizada) → migración (no autorizada).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** el registro del cierre de diseño: `CHANGELOG.md`, `docs/plans/127-repository-artifact-placement-contract-design.md`, `docs/plans/INDEX.md`. Total 3 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`.
- **Effective inputs (repo content):** el scope declarado (3 paths) más `docs/plans/`, `docs/rfc/`, `docs/adr/` y `protocol/.agents/` consumidos por los checkers canónicos.
- **Observed dependencies:** `git` (identidad de contenido y estado; el checker de citas resuelve contra el árbol de trabajo); `python` (intérprete de los checkers); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; sin red. **La pierna de tests no se ejecutó y no se declara como validación de este plan:** el cambio es exclusivamente documental (un plan, su registro en el INDEX y el changelog), no modifica código, checkers, runtime ni payload, y la suite DEV ya arrastra la clase ambiental conocida de temporales de pytest (`PermissionError [WinError 5]`) declarada por los Planes 121–126. No se ejecuta `python -m pytest tests/` porque no hay superficie de producto que validar; la verificación exigible de este plan es la batería de checkers, que corre completa. No se reabre el aislamiento de pytest ni se modifica CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `95bee05472ebecf817161b3eb96ff5d4b37e1e65`.
  - **Delta scoped identity (scope S = los 3 paths del cambio, ordenados; serialización `scoped-v1`):** `a737fa3a23a12839bb4346e1cb286ae110229eaa14a789f2f00af43e49e46a8a`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `95bee05472ebecf817161b3eb96ff5d4b37e1e65`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`95bee05472ebecf817161b3eb96ff5d4b37e1e65`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/plans/127-repository-artifact-placement-contract-design.md`, `docs/plans/INDEX.md`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0, 215 files checked); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`). Gates de lifecycle sobre el árbol final: C-1 `VALID`, C-2 `VALID`, C-3 `VALID` para el Plan 127.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(plans): close plan 127 repository artifact placement contract design`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `a737fa3a23a12839bb4346e1cb286ae110229eaa14a789f2f00af43e49e46a8a`, tree `95bee05472ebecf817161b3eb96ff5d4b37e1e65`.
- **Estado de cierre (tree id):** `95bee05472ebecf817161b3eb96ff5d4b37e1e65` — el árbol del índice que la validación A1 consumió, con el scope declarado (3 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–126) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 127 (tabla + serie, Quincuagésima novena) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 127); `## Validation anchor` y `## Checkpoint / cierre` registrados; finding `F-1`, corrección `C-1` y pendientes `PC-1`..`PC-4` registrados; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — documentos afectados: `docs/plans/INDEX.md` (aspecto: el diseño de Plan 127 no estaba registrado; actualización: serie + tabla + encabezado de estado; evidencia: `check_plan_structure` PASS) y `CHANGELOG.md` (aspecto: par del plan; actualización: ítem `[Unreleased]`; evidencia: `check_version_state` PASS). Este plan **es** el documento de estado actual del diseño y su propio registro. No se modifica `docs/AGENTS.md` (la carta documental no cambia: el diseño no introduce naturaleza, clase ni lifecycle nuevos), ni `docs/source-layout.md`, ni ningún documento histórico (RFC-46). No se requiere `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. **Clasificación de estado final de Plan 127:** `Design: CLOSED` · `Implementation: NOT STARTED` · `Placement Contract: NOT CREATED` · `Migration: NOT STARTED` · `Release: NOT AUTHORIZED`. `Committed` es estado del repositorio. Cerrar el **diseño** no es materializar el **contrato** ni autorizar **release**. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `50771b6`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: seis checkers PASS (`check_protocol_invariants` 215 files checked; `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0). Gates de lifecycle sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`**; corpus C-2 con único GAP preexistente `116-adversarial-deliberation-mvp-closure.md`, no modificado. Incidencia corregida durante la ejecución: dos citas a `.github/workflows/publish-dist.yml` escritas con nombre desnudo y número de línea, reportadas por `check_plan_citations` (`file not found`), sustituidas por path completo.

**Alcance.** 3 archivos, todos documentales. Ningún artefacto movido, renombrado ni eliminado. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/` y `.gitignore` sin cambios. Ningún documento histórico reescrito. Sin Placement Contract, registry, checker, schema, namespace nuevo, state machine, clase de autoridad, ADR adicional ni migración.

**No realizado (por diseño).** El Repository/Artifact Placement Contract **no fue materializado**; no se creó ADR; no se resolvió ninguna de las cuatro decisiones pendientes (`OQ-2`, `OQ-3`, `OQ-4`, `PC-1`); no se ejecutó ni autorizó migración; no se anticipó la etapa de materialización.
