# Plan 157 — ROADMAP canónico visual y estratégico

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-11
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L2 (`max(coordination=0, scope=2, architectural impact=1, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, un dominio (documentación DEV de raíz + gobernanza de estado actual). *scope*: área acotada pero multi-documento —`ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/glossary/`, referencias cruzadas en `docs/AGENTS.md` / `README.md`. *architectural impact*: **documental y acotado** — no crea entidad, registry, checker, taxonomía, autoridad, lifecycle ni estado nuevo; **reemplaza la estructura de representación** de un documento canónico y nombra su contrato, que es una decisión de representación, no de arquitectura. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: acotada a una sesión.
**Depende de:** — (no depende de un plan previo; los planes 132, 133, 149 y 155/156 son el punto de partida que este Change no reabre)
**Origen:** Directiva del mantenedor (2026-10-11) que ordena implementar el modelo canónico visual y estratégico de `ROADMAP.md`, apoyada en la auditoría conceptual `ROADMAP AUDIT & REDESIGN — INFORME COMPLETO` (emitida en la sesión de intake), cuyo veredicto fue `REPLACE_ROADMAP_STRUCTURE`.

## Objetivo

Reemplazar la estructura de `ROADMAP.md` por una representación **estratégica, visual, orientada al futuro y explícitamente delimitada**, y establecer el contrato documental de qué es y qué no es el ROADMAP de ARgentOS.

Hoy el documento es estructuralmente incapaz de cumplir su función, no meramente mejorable: su propio encabezado declara un *«mapa operativo actual»* que *«no cataloga la historia ya cerrada»* (`ROADMAP.md`), y sin embargo **tres de sus cinco secciones operativas contienen exactamente eso** — trabajo cerrado bajo `## Trabajo activo / dogfood`, trabajo resuelto bajo `## Pendientes que requieren autorización` (que declaraba «Ninguno» y aun así listaba cinco ítems resueltos), y la totalidad de `## Trazabilidad histórica`. Ningún ítem tenía estado, no existía una sección para decisiones pendientes, no había punteros de verificación por afirmación, y la separación Protocol/DEV se enunciaba dos veces sin aplicarse nunca por capacidad. El plan 132 ya vació esas secciones y **se rellenaron de historia en veinte planes**: el defecto se reproduce por construcción, porque el esqueleto invita a la historia dentro del área operativa.

El Change **reemplaza el esqueleto y la representación por ítem**, y preserva el contenido real en los artefactos que lo poseen. No implementa ninguna capacidad, no resuelve ninguna decisión pendiente, no toca `protocol/` ni el runtime.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-11): implementar el modelo canónico visual/estratégico de `ROADMAP.md`; `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna enumera la estructura objetivo (§7), el modelo visual (§6), el horizonte NOW/NEXT/LATER (§9), la prioridad (§10), los dominios (§8), las dependencias (§12), los blockers (§13), el caso Autonomy (§14), la migración (§15), el glosario (§17), el informe final (§27) y el criterio de éxito (§28) | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `AGENTS.md`; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/authority.md`; `.agents/policies/validation-closure.md`; `docs/AGENTS.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/glossary/INDEX.md`; `docs/glossary/terms.md`; `docs/placement-contract.md`; `docs/plans/_TEMPLATE.md`; `docs/plans/INDEX.md`; `docs/rfc/56-governance-fast-track.md`; `ROADMAP.md`; `README.md`; `runtime/README.md`; `docs/adr/17`, `docs/adr/18`, `docs/adr/19`; `docs/plans/132`, `docs/plans/149`, `docs/plans/155`, `docs/plans/156`; `docs/working/audits/architecture-capability-review.md`; `docs/behavior-patterns.md` | agente | lista de `ruta:sección` de este registro |
| `P-4` Derivabilidad | **Derivable con `GAP` declarado.** `GAP-1`: la consigna cita como input `Texto pegado.txt`, que **no existe en el repositorio** (verificado: `Test-Path` → `False`, sin archivos `.txt` en la raíz y sin referencia en ningún artefacto). Se sustituye por la auditoría emitida en la propia sesión de intake, cuyo contenido es el mismo informe; el `GAP` se registra como `<PLAN-157>:F-1` y **no** bloquea: la autoridad de la directiva es el pedido explícito del mantenedor, no el archivo. Sin señal bloqueante en el resto | agente | este registro; verificación de filesystem |
| `P-5` `work_type` | `GAP` — el criterio de admisión de `work_type` sigue pendiente (`docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`, `docs/plans/152-authority-decisions-gov-1-10.md:Pending decisions`); no se inventa un valor | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` |
| `P-6` Conocimiento vigente | `active` para `AGENTS.md`, `.agents/**`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/glossary/**`, `ROADMAP.md`, `README.md`; `Executed`/`Closed` (historical, RFC-46) para los planes 132/149/155/156 y los ADR-17/18/19; `archived` para `docs/architecture/**` | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (clasificación; sin efecto payload ⇒ Clase B), RFC-75 (Change Levels SS2, checkpoints SS7, findings SS8, pending SS15), RFC-69 (plan docs-only cierra sin release), RFC-46 (exclusión histórica), ADR-15/ADR-16 (condiciones derivadas y autoridad), `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre`, `docs/placement-contract.md`. `NOT_APPLICABLE`: RFC-56 Clase A (sin `protocol/.agents/`), preempción de payload de `validation-closure.md` SS5.1 | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad requerida: **decisión del mantenedor** (aprobación de este Plan). Conjunto declarado de rutas: el `## Scope` de este registro | **humano** | declaración del humano (consigna de intake) |

## Criterio de entrada

- [x] `dev` limpio en `a09364e2f687d334e52bff9a13170245b7f20a6b` (verificado con `git status --porcelain=v1` y `git rev-parse HEAD`); rama `dev`; `master` = `78ca512`; divergencia `0 / 2`.
- [x] `protocol/.agents/VERSION` = `12.0.1` (commiteado, sin tag); último tag = `12.0.0`; `dist` local rezagado (`11.7.1`) respecto de `origin/dist` (`12.0.0`) — hecho registrado, fuera del scope.
- [x] `ROADMAP.md` leído completo (379 líneas) y su contenido clasificado bloque por bloque.
- [x] No existe plan ni RFC previo para este Change: el próximo número libre es **157** (último registrado: Plan 156); búsqueda de `roadmap visual` / `ROADMAP_REDESIGN` / `nuevo modelo canónico de ROADMAP` en `docs/plans/` → 0 coincidencias.
- [x] `docs/glossary/terms.md` **no tiene** entrada `ROADMAP` (verificado); el glosario es `Inventory` descriptivo y **no define**: enruta a su `Authority Reference` (`docs/glossary/INDEX.md:Qué es y qué no es`).
- [x] Fuentes de verdad de estado confirmadas: `docs/plans/INDEX.md` (registro de planes), `docs/runtime/README.md` (capacidades del runtime DEV), secciones `Estado de implementación` de los ADR, `.agents/policies/*`.
- [x] Referencia comparativa `roldriel/eones@master:ROADMAP.md` obtenida y evaluada como **patrón, no autoridad** (ver `## Pasos`, paso 1).
- [ ] **Gate de autorización:** este Plan no se ejecuta hasta que el mantenedor lo apruebe (`.agents/workflows/change-lifecycle.md` §2: *«new Plan required; STOP and propose the plan (never create it silently, never execute it)»*).

## Scope

Rutas que este Change queda autorizado a modificar (conjunto declarado, ordenado):

```text
AGENTS.md
CHANGELOG.md
README.md
ROADMAP.md
docs/AGENTS.md
docs/CONVENTIONS.md
docs/glossary/INDEX.md
docs/glossary/terms.md
docs/plans/157-canonical-visual-roadmap.md
docs/plans/INDEX.md
```

`AGENTS.md` entra en el scope por el paso 6 (reconciliación de referencias cruzadas): su línea de cierre describía el ROADMAP como *«project priorities»*, que contradice el contrato nuevo. Quedan **fuera** del scope, explícitamente: `protocol/` (incluido `protocol/.agents/` y `VERSION`); `dist/`; `runtime/`; `tools/`; `tests/`; `.agents/`; `.github/`; `docs/VERSIONING.md`; `docs/placement-contract.md`; `docs/behavior-patterns.md`; `docs/rfc/**`; `docs/adr/**`; `docs/working/**`; y todo plan cerrado (RFC-46).

## Entregables

1. `ROADMAP.md` — estructura reemplazada conforme al contrato nuevo: header, visión/destino, posición actual, ROADMAP at a Glance (NOW / NEXT / LATER con cards por iniciativa), dependencias estratégicas, blockers/decisiones, caso Autonomy, relación con otros artefactos, y definición explícita *es / no es*.
2. `docs/CONVENTIONS.md` — subsección nueva que establece el contrato canónico del ROADMAP (responsabilidad única; *es / no es*; relación con el resto de los artefactos), sin duplicar la semántica de `Roadmap impact` ya vigente en `docs/VERSIONING.md:10` y `.agents/policies/validation-closure.md:5.2`.
3. `docs/glossary/terms.md` — entrada `ROADMAP` con `Scope`, `Status`, `Authority Reference` (que enruta a `docs/CONVENTIONS.md`) y `Related Terms`; **sin** duplicar la definición (regla single-source del propio glosario).
4. `docs/glossary/INDEX.md` — alta de `ROADMAP` en el registro inicial de términos y actualización del conteo si corresponde.
5. `docs/AGENTS.md` — **verificado y sin cambio**: su fila de clase documental (`EntryPoint`, línea 21) ya describía correctamente el rol de `ROADMAP.md` y no contradecía el contrato nuevo. Se declara el resultado de la reconciliación (paso 6) en lugar de inventar una edición.
6. `README.md` — corrección de la frase que describe el ROADMAP como *«project priorities»* si contradice el contrato (o `NOT_REQUIRED` justificado).
7. `docs/plans/157-canonical-visual-roadmap.md` — este registro.
8. `docs/plans/INDEX.md` — fila + serie + encabezado de estado.
9. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 157), conforme a la regla de changelog para planes docs-only (RFC-69).

## Pasos

1. **Evaluar la referencia comparativa (sin copiarla).** Leer `roldriel/eones@master:ROADMAP.md` y extraer **sólo patrones** de representación: destino al frente, secciones cortas y escaneables, uso de emojis como marcas de sección, cards de milestone con `Prioridad`/`Estado`, y pie con `Última actualización`/`Versión actual`. **Descartar explícitamente** sus antipatrones: listas extensas de versiones ya completadas dentro del roadmap, y el índice de funcionalidades completas como contenido del documento. Registrar el veredicto.
2. **Fijar el contrato.** Redactar en `docs/CONVENTIONS.md` la subsección del contrato del ROADMAP: responsabilidad única (*comunicar visualmente la dirección de evolución y el camino de alto nivel*), la lista *es* / *no es*, y la cadena de relación con los demás artefactos usando la terminología real del repositorio (`ROADMAP` → dirección; `Plan`/`RFC`/`ADR` → decisión y ejecución; implementación; `Validation`/gates; `CHANGELOG`/release). **No** redefinir `Roadmap impact` ni la semántica de cierre.
3. **Escribir el ROADMAP nuevo.** Reemplazar `ROADMAP.md` con la estructura del §7 de la consigna, adaptada a la evidencia:
   - **Header**: nombre, propósito, definición breve, `Última actualización`, estado/versión relevante. Sin ficha histórica.
   - **Visión / Destino**: qué quiere llegar a ser ARgentOS y qué significa éxito, en pocas líneas. Sin documentación arquitectónica.
   - **Posición actual**: baseline publicado (`12.0.0`, tag sobre `78ca512`), PATCH `12.0.1` en `dev` sin promocionar, payload publicado = `origin/dist` @ `1181db6` (**no** la ref local, que está rezagada), y las capacidades ya disponibles en una lista corta con marca de dominio. **Sin** matriz exhaustiva de capabilities.
   - **ROADMAP at a Glance**: sección principal y más visual, con lanes `NOW` → `NEXT` → `LATER` y una card por iniciativa estratégica (no por tarea): `Objective`, `Domain`, `Priority`, `Status`, `Depends on`.
   - **Dependencias estratégicas**: diagrama Mermaid con las aristas que condicionan el camino.
   - **Blockers / decisiones**: tabla corta `Decision / Blocker | Impact | Affects | Status`, sólo con lo que puede cambiar prioridad, secuencia, alcance, viabilidad o siguiente paso; con referencia al artefacto dueño. **No** es un decision register.
   - **Caso Autonomy**: representación que distingue *host autonomy*, *SAE*, *authority model*, *envelope*, *Complete ARgentOS Autonomy*, *Stage A* y *Stage B*, sin un único párrafo y sin matriz exhaustiva.
   - **Relación con otros artefactos**: tabla *«Necesito saber… → Consulto…»* con nombres reales del repositorio.
   - ***Es / no es***: la definición explícita, en el propio documento.
   - Toda afirmación de estado con puntero verificable (`ruta:sección`) o referencia al artefacto dueño.
4. **Migrar el contenido clasificado.** Aplicar la tabla de migración de `## Migración del contenido actual`: conservar en el ROADMAP destino, posición, iniciativas, secuencia, prioridades, dependencias y blockers; reubicar el detalle en el artefacto responsable. **No borrar nada sin destino registrado.**
5. **Alta en el glosario.** Agregar la entrada `ROADMAP` a `docs/glossary/terms.md` (que enruta, no define) y registrarla en `docs/glossary/INDEX.md`.
6. **Reconciliar referencias cruzadas.** Buscar menciones de la función del ROADMAP en `AGENTS.md`, `.agents/`, `docs/`, `README.md`, glosario y conventions; corregir **sólo** las que contradigan el contrato nuevo. Sin limpieza documental indiscriminada.
7. **Validación visual.** Aplicar el checklist de 12 puntos de `## Verificación` como usuario nuevo, ignorando el detalle técnico.
8. **Registrar el Change**: este Plan, `docs/plans/INDEX.md` y `CHANGELOG.md`.
9. **Verificar**: batería canónica, gates C-1/C-2/C-3 y verificación factual del ROADMAP.
10. **Cerrar**: Validation Anchor, `## Checkpoint / cierre` con las dos determinaciones de impacto, `## Nota de ejecución` y condición derivada.

## Migración del contenido actual

Clasificación de cada bloque del `ROADMAP.md` vigente. **`MOVE_TO_CAPABILITY_STATUS` no se usa**: no existe —ni este Plan crea— un capability registry separado; el estado de capacidad vive en `docs/plans/INDEX.md` (estado de plan), `runtime/README.md` (runtime DEV), las secciones `Estado de implementación` de los ADR y `.agents/policies/*`, y el ROADMAP **enruta** a ellos.

| Bloque actual (líneas) | Clasificación | Destino / tratamiento |
|---|---|---|
| Encabezado `:1-16` | `KEEP_IN_ROADMAP` (reescrito) | Header nuevo: propósito, definición, frescura, `Es/No es` |
| Intro estratégica `:18-32` | `KEEP_IN_ROADMAP` (condensado) | Visión / Destino |
| Diagrama A→B→C + regla de dependencia `:34-48` | `KEEP_IN_ROADMAP` | Dependencias estratégicas (Mermaid) |
| `### Etapa A` `:50-103` | `MOVE_TO_PLAN_INDEX` + `KEEP_IN_ROADMAP` (1 card) | Doctrina → plan 149; la iniciativa queda como card `NEXT` |
| `### Etapa B` `:105-176` | `KEEP_IN_ROADMAP` (cards) | Fronteras candidatas → initiatives `LATER`; `Autonomy ⊆ Scope ∩ Authority` → caso Autonomy |
| `### Etapa C` `:178-195` | `KEEP_IN_ROADMAP` (4 líneas) | Regla de admisión, en la lane `LATER` |
| `### Qué no es una entrada` `:197-213` | `MOVE_TO_CONVENTIONS` | Política, no mapa → contrato nuevo en `docs/CONVENTIONS.md` |
| `### Estado` — versión/dist `:215-231` | `KEEP_IN_ROADMAP` (tabla) | Posición actual, con `origin/dist` vs ref local |
| `### Estado` — párrafo de autonomía `:232-245` | `KEEP_IN_ROADMAP` (estructurado) | Caso Autonomy, en cards diferenciadas |
| `### Estado` — lista histórica `:246-252` | `REMOVE_AS_REDUNDANT` | Ya declarada «no se reabre»; sin valor de camino |
| `## Trabajo activo / dogfood` `:254-272` | `KEEP_IN_ROADMAP` (lanes) / `MOVE_TO_PLAN_INDEX` | El estado vacío → lanes; lifecycle y Memory → `CHANGELOG`/planes |
| Bloque EARS plan 137 `:274-281` | `MOVE_TO_PLAN_INDEX` | Registro de cierre; el ROADMAP no cataloga historia |
| Bloque D01 plan 136 `:283-290` | `MOVE_TO_PLAN_INDEX` | Ídem |
| Criterio de prioridad `:292-299` | `MOVE_TO_CONVENTIONS` | Regla de gobernanza |
| `## Pendientes que requieren autorización` `:301-337` | `MOVE_TO_OTHER_DOCUMENT` + `KEEP_IN_ROADMAP` (tabla corta) | El detalle vive en el artefacto dueño de cada PC (PC-1); el ROADMAP conserva **sólo** los blockers que cambian el camino |
| `## Candidatos futuros` `:339-348` | `KEEP_IN_ROADMAP` (card `LATER`) | Un candidato es un estado, no una sección |
| `## Trazabilidad histórica` `:350-360` | `MOVE_TO_PLAN_INDEX` | 11 líneas para decir «resuelto, ver INDEX» |
| `## Proceso` 1-3 `:362-373` | `MOVE_TO_CONVENTIONS` | Duplica gobernanza vigente |
| `## Proceso` 4 `:374-379` | `KEEP_IN_ROADMAP` | Regla de admisión de Etapa C |

**Hallazgo de la migración que se registra y NO se corrige aquí** (`REVIEW_REQUIRED`): las decisiones abiertas de los planes 122, 123, 125, 126, 131, 137, 138, 151, 152, 155 y 156 **no están registradas en el ROADMAP** (su sección «Pendientes» declara «Ninguno»). Este Plan **no** las resuelve ni crea un registro de decisiones: el ROADMAP mostrará únicamente las que condicionan el camino estratégico, y la ausencia de registro agregado queda como finding.

## Criterios de salida

- [ ] `ROADMAP.md` responde las nueve preguntas de la consigna por escaneo visual, sin leer prosa técnica extensa.
- [ ] `ROADMAP.md` declara explícitamente su responsabilidad única y su lista *es / no es*.
- [ ] `NOW` → `NEXT` → `LATER` es inequívoco, con al menos una card por lane.
- [ ] Cada card declara `Objective`, `Domain` (`PROTOCOL`/`DEV`/`BOTH`), `Priority`, `Status` y `Depends on`.
- [ ] La separación Protocol / DEV es visible por card, no sólo enunciada.
- [ ] Las dependencias estratégicas están representadas (Mermaid) y coinciden con las aristas declaradas en las cards.
- [ ] Los blockers/decisiones que pueden cambiar el camino aparecen en una tabla corta con referencia al artefacto dueño.
- [ ] El caso Autonomy distingue host autonomy, SAE, authority model, envelope, Complete Autonomy, Stage A y Stage B, y responde *qué existe / qué falta / qué depende de qué / qué es DEV / cuál es el siguiente paso*.
- [ ] `ROADMAP.md` **no** contiene: changelog, backlog, matriz exhaustiva de capabilities, especificación técnica, inventario de archivos, ni listas de commits.
- [ ] `ROADMAP.md` **no** mezcla implementación con publicación (`Executed` ≠ `Committed` ≠ `Closed` ≠ `Released`).
- [ ] Ninguna información relevante se perdió: cada bloque migrado tiene destino registrado en `## Migración del contenido actual`.
- [ ] `docs/CONVENTIONS.md` establece el contrato del ROADMAP; `docs/glossary/terms.md` tiene la entrada `ROADMAP` que **enruta** sin duplicar la definición.
- [ ] `README.md` y `docs/AGENTS.md` son consistentes con el contrato nuevo.
- [ ] `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, RFCs, ADRs, `docs/VERSIONING.md`, `docs/placement-contract.md` y los planes cerrados: **0 diff**.
- [ ] Batería canónica y gates C-1/C-2/C-3 registrados con evidencia; determinaciones de impacto declaradas.

## Verificación

```text
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Más la **validación visual** sobre el estado final (checklist de 12 puntos, leído como usuario nuevo):

```text
 1. La estructura visual muestra un camino
 2. NOW → NEXT → LATER inequívoco
 3. Protocol / DEV visible
 4. Blockers / dependencias principales visibles
 5. Autonomy se entiende sin documentación adicional
 6. No parece un CHANGELOG
 7. No parece un backlog
 8. No parece una capability matrix gigante
 9. No parece una especificación técnica
10. Responde las 9 preguntas de la consigna por escaneo
11. Toda afirmación de estado tiene puntero verificable
12. Mantenible sin degradarse en registro histórico
```

Y la verificación factual de scope: `git diff --name-only HEAD` ⊆ el conjunto declarado en `## Scope`.

## Riesgos

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Perder información al reemplazar la estructura | alta | Tabla de migración bloque por bloque; ningún borrado sin destino; `docs/plans/INDEX.md` y el changelog conservan la traza |
| Convertir el ROADMAP en un decision register | alta | La tabla de blockers se limita a lo que cambia prioridad/secuencia/alcance/viabilidad/siguiente paso, con puntero al artefacto dueño |
| Convertir el ROADMAP en capability matrix | alta | Sin matriz: cards de iniciativa y una lista corta de capacidades disponibles; el detalle vive en `docs/plans/INDEX.md` y `runtime/README.md` |
| Afirmar que Complete Autonomy está completa | máxima | El caso Autonomy separa explícitamente lo implementado (host, SAE, authority model) de lo planificado (envelope, Stage B), con puntero a `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación` |
| Duplicar definiciones normativas en el glosario | media | La entrada sólo enruta: `Authority Reference` a `docs/CONVENTIONS.md`; prohibición single-source del propio glosario |
| Reabrir o reescribir artefactos cerrados | alta | Exclusión histórica (RFC-46): los planes 132/149/155/156 y los ADR se citan, nunca se editan |
| Ampliar el alcance hacia gobernanza no pedida | media | `docs/VERSIONING.md` y `docs/placement-contract.md` quedan fuera de scope; la semántica de `Roadmap impact` no se redefine en este Plan |
| Duplicar el contrato en ROADMAP y CONVENTIONS | media | El ROADMAP declara el contrato en forma operativa breve y `docs/CONVENTIONS.md` es la definición normativa; el ROADMAP referencia, no define |
| Copiar el ROADMAP de Eones | media | El Paso 1 extrae patrones y **descarta explícitamente** sus antipatrones (listas de versiones completadas, índice de funcionalidades completas) |

## Hallazgos de la auditoría que este Plan registra y NO ejecuta

Separados deliberadamente del scope, para no agrupar Changes distintos (precedente `<PLAN-132>:PC-1`):

1. **Semántica de `Roadmap impact` sin valor correctivo.** El plan 155 editó `ROADMAP.md` con cuarenta y seis inserciones de afirmaciones factuales y determinó `Roadmap impact: NOT_REQUIRED` (`docs/plans/155-documentation-refresh-behavior-patterns.md:Checkpoint / cierre`). Bajo los tres valores vigentes la clasificación queda acoplada al juicio. Requiere un Change propio sobre `.agents/policies/validation-closure.md:5.2 Roadmap impact (closure determination)` y `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre: impacto documental e impacto de Roadmap (regla operacional)`.
2. **Decisiones abiertas sin registro agregado.** Tres listas agregadas se contradicen y una es factualmente falsa: `docs/plans/146-release-promotion-11-6-1.md` declara abierta `<PLAN-137>:PC-3`, que está `resuelta` en `docs/plans/137-ears-structural-validator.md:Pending decisions`. El ROADMAP nuevo no crea registro: mostrará sólo los blockers estratégicos.
3. **Ref local `dist` rezagada** (`11.7.1` vs `origin/dist` `12.0.0`). Se documenta en la Posición actual; no se «corrige» la ref.
4. **`ROADMAP.md` no puede ser la fuente de verdad del estado de features** sin convertirse en registro. La Posición actual enruta a `docs/plans/INDEX.md` y `runtime/README.md` en lugar de duplicarlos.

## Trazabilidad

Auditoría conceptual `ROADMAP AUDIT & REDESIGN — INFORME COMPLETO` (veredicto `REPLACE_ROADMAP_STRUCTURE`) + directiva del mantenedor (2026-10-11) → **este Plan** → `ROADMAP.md` reestructurado + contrato en `docs/CONVENTIONS.md` + entrada en `docs/glossary/` → registro en `docs/plans/INDEX.md` y `CHANGELOG.md`.

Punto de partida no reabierto: planes 132 (mapa operativo actual), 133 (Roadmap impact), 149 (roadmap estratégico A→B→C), 155/156 (refresh documental y reconciliación de payload), RFC-75, ADR-15/16/17/18/19.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las ocho rutas de **contenido** que la identidad de contenido mide — `AGENTS.md`, `CHANGELOG.md`, `README.md`, `ROADMAP.md`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`, `docs/glossary/INDEX.md`, `docs/glossary/terms.md`. Quedan fuera del scope **medido** la governance del Change (este artefacto de Plan y su fila/serie en `docs/plans/INDEX.md`), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–149). El `## Scope` autorizado del Change tiene diez rutas: las ocho medidas más `docs/plans/157-canonical-visual-roadmap.md` y `docs/plans/INDEX.md`.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la validación visual de doce puntos y la verificación factual de scope (`git diff --name-only HEAD`).
- **Effective inputs (repo content):** el scope declarado; `docs/VERSIONING.md` (batería, política de changelog, estados y snapshot); `docs/CONVENTIONS.md`; `docs/glossary/INDEX.md` y `docs/glossary/terms.md` (reglas del glosario); `docs/AGENTS.md` (taxonomía y mapa folder→clase); `docs/placement-contract.md` (familias y estado de distribución); `.agents/policies/validation-closure.md` y `.agents/policies/authority.md`; `docs/rfc/56-governance-fast-track.md`; el corpus completo de `docs/plans/` y `docs/rfc/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` disponible para las identidades de contenido y la resolución de objetos (`check_plan_citations` y C-2 resuelven árboles con `git rev-parse`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.x; git 2.55.0.windows.5; repositorio bajo OneDrive. **Clase ambiental declarada (GAP preexistente, no defecto del Change):** `python tools/check_plan_citations.py` está **rojo en el baseline** `a09364e` con 27 citas rotas preexistentes; el Change **no aumenta** el conteo (27 antes y 27 después) y **reduce** una cita al conservar `### Estado del que parte este roadmap` en `ROADMAP.md`. Queda registrado como `<PLAN-157>:F-2` con continuidad en `<PLAN-157>:PC-1`. `check_dist_sync.py` **no** aplica: es local-only y se espera verde sólo en `master`, y este Change no promueve.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `5f645f316b5dd29f9d52161c70c624171e233ec7` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado sobre las ocho rutas declaradas ya staged.
  - **Delta scoped identity (scope S = las ocho rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `320040e3ed1d3ba915629a1c12cfdb5cf92197e9a9bf6b4ceefb57de51b1f9c5`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto y `docs/plans/INDEX.md`); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `AGENTS.md`, `CHANGELOG.md`, `README.md`, `ROADMAP.md`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`, `docs/glossary/INDEX.md`, `docs/glossary/terms.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (exit 0, 216 files / 10457 references); verification-02 (`check_plan_citations`): **FAIL preexistente** (exit 1, 27 citas rotas, idénticas en número al baseline `a09364e`; el Change no introduce ninguna y reduce una); verification-03 (`check_plan_structure`): **PASS** (exit 0); verification-04 (`check_taxonomy_coherence`): **PASS** (exit 0); verification-05 (`check_session_artifacts`): **PASS** (exit 0); verification-06 (`check_version_state`): **PASS** (exit 0, con los warnings de tags esperados en `dev`); verification-07 (`python -m pytest tests/`): **PASS** (exit 0, **1267 passed** en 238.89 s); verification-08 (C-1 `check_lifecycle_anchor`): `ANOMALY=0`, `GAP=0`, `VALID=62`; verification-09 (C-2 `check_lifecycle_checkpoint`): `ANOMALY=0`, `VALID=61`, `GAP=1` (el GAP histórico del Plan 116, preexistente e intacto); verification-10 (C-3 `check_lifecycle_lineage`): `ANOMALY=0`, `GAP=0`, `VALID=31`. Validación visual de doce puntos: **las doce cumplidas**. Verificación factual de scope: `git diff --name-only HEAD` ⊆ el `## Scope` declarado.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(roadmap): replace the roadmap structure with the canonical visual map (plan 157)`. Se identifica por su mensaje (convención anti-circularidad: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `5f645f316b5dd29f9d52161c70c624171e233ec7`, delta scoped identity `320040e3ed1d3ba915629a1c12cfdb5cf92197e9a9bf6b4ceefb57de51b1f9c5`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `320040e3ed1d3ba915629a1c12cfdb5cf92197e9a9bf6b4ceefb57de51b1f9c5` / `5f645f316b5dd29f9d52161c70c624171e233ec7`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto y `docs/plans/INDEX.md`), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7) y el árbol material queda verificable con `git log -1 --format=%T`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); verificado con C-2, que clasificó este artefacto sin `ANOMALY`. El `GAP=1` del corpus C-2 es el histórico del Plan 116, declarado y no tocado.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 157 (serie Octogésima sexta + fila + encabezado de estado); `CHANGELOG.md` `[Unreleased]` registra el par (plan 157); `ROADMAP.md` reestructurado; `docs/CONVENTIONS.md` establece el contrato del ROADMAP; `docs/glossary/terms.md` y `docs/glossary/INDEX.md` registran el término; `AGENTS.md`, `README.md` y `docs/AGENTS.md` reconciliados; findings `<PLAN-157>:F-1` (`resolved`) y `<PLAN-157>:F-2` (`open`), corrección `<PLAN-157>:C-1` y pending `<PLAN-157>:PC-1` registrados; `**Status:** Executed`.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `ROADMAP.md` (aspecto: presentaba un «mapa operativo actual» que catalogaba historia cerrada, sin estado por ítem, sin sección de decisiones pendientes y sin punteros de verificación; actualización: estructura reemplazada por el mapa estratégico visual con `NOW`/`NEXT`/`LATER`, dominio y estado por iniciativa, dependencias, blockers y caso Autonomy; evidencia: el documento en el estado validado, con la validación visual de doce puntos cumplida). `docs/CONVENTIONS.md` (aspecto: no existía contrato canónico del ROADMAP; actualización: subsección `### Contrato del ROADMAP (canónico; Plan 157)`). `docs/glossary/terms.md` y `docs/glossary/INDEX.md` (aspecto: el término `ROADMAP` no estaba registrado; actualización: entrada que enruta al contrato sin duplicarlo). `AGENTS.md` y `README.md` (aspecto: describían la función del ROADMAP como «project priorities», contradeciendo el contrato nuevo; actualización: descripción alineada con la dirección estratégica). `docs/AGENTS.md` **examinado y sin cambio**: su fila de clase documental ya era correcta (razón verificable, no omisión). `docs/plans/INDEX.md` y `CHANGELOG.md` por el registro del Change. `docs/VERSIONING.md` **no** se toca: sin release, su snapshot §9 no cambia, y la semántica de `Roadmap impact` de §10 no se modifica. No se actualiza ningún documento histórico (RFC-46).
- **Roadmap impact:** `REQUIRED` — el propio Change **es** la reconciliación del mapa estratégico: reemplaza la representación del trabajo futuro, reordena sus iniciativas en horizontes, hace explícito el estado de AUTONOMY en cuatro planos y expone los bloqueos que condicionan el camino. El artefacto que lo posee es `ROADMAP.md`, con el contrato normativo en `docs/CONVENTIONS.md` y el registro descriptivo en `docs/plans/INDEX.md`. **No** crea trabajo ejecutable: ninguna etapa queda autorizada por este documento.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-10-11. Ejecutado en `dev` @ `a09364e2f687d334e52bff9a13170245b7f20a6b`, árbol de trabajo limpio al inicio.*

**Gate de autorización.** No existía plan aprobado para este Change; conforme a `.agents/workflows/change-lifecycle.md` §2 se creó este Plan y se detuvo la ejecución en el gate. El mantenedor aprobó la ejecución el 2026-10-11, junto con la decisión de usar como fuente la auditoría emitida en la sesión de intake ante la ausencia del archivo `Texto pegado.txt` citado por la consigna (`<PLAN-157>:F-1`).

**Verificación realizada.** Batería canónica: `check_protocol_invariants` PASS (216 archivos, 10457 referencias); `check_plan_structure` PASS; `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` PASS con los warnings de tags esperados en `dev`; `python -m pytest tests/` → **1267 passed** (238,89 s). Gates de lifecycle: C-1 `ANOMALY=0 / GAP=0` (62 `VALID`), C-2 `ANOMALY=0 / VALID=61 / GAP=1` (el histórico del Plan 116), C-3 `ANOMALY=0 / GAP=0`. `check_dist_sync.py` no se ejecutó: es local-only y sólo se espera verde en `master`.

**Baseline medido, no asumido.** `python tools/check_plan_citations.py` está **rojo en `a09364e`** con **27** citas rotas preexistentes, mayormente citas de fuentes históricas (`docs/plans/`, `docs/rfc/`, `docs/plans/INDEX.md`, `CHANGELOG.md`) a secciones del ROADMAP anterior, más una referencia legacy en `docs/CONVENTIONS.md`. Se midió el baseline **antes** de tocar el ROADMAP, intercambiando temporalmente el archivo por su versión de `HEAD`, para poder comparar. Resultado: **27 antes y 27 después** — el Change no introduce ninguna cita rota y **reduce una** (la de `CHANGELOG.md` a `### Estado del que parte este roadmap`) al conservar ese encabezado en el ROADMAP nuevo, porque el destino de esa cita es un documento vivo. Las citas desde fuentes históricas a `## Trabajo activo / dogfood` y `## Pendientes que requieren autorización` no se reparan: reescribir documentos cerrados violaría la exclusión histórica (RFC-46) y forzar esos encabezados en el ROADMAP reintroduciría la mezcla que el Change elimina. Queda como `<PLAN-157>:PC-1`.

**Qué se materializó.** `ROADMAP.md` reemplaza su estructura: header con propósito, definición y frescura; `## 🎯 Visión / Destino`; `## 📍 Posición actual` (tabla de baseline con `12.0.0` sobre `78ca512`, `origin/dist` @ `1181db6`, el PATCH `12.0.1` sin tag, trabajo activo ninguno; capacidades disponibles separadas por dominio; `### Estado del que parte este roadmap`); `## 🚦 Roadmap at a Glance` con lanes `NOW`/`NEXT`/`LATER` y una card por iniciativa con `Objetivo`, `Domain`, `Priority`, `Status` y `Depends on`; `## 🔗 Dependencias estratégicas` (Mermaid); `## 🚧 Blockers y decisiones que condicionan el camino` más `### ⏸️ Pendientes que requieren autorización y trabajo diferido`; `## 🧭 Autonomy — mapa del caso` con tres tablas y dos diagramas que separan host autonomy, SAE y authority model (existentes) del envelope (decidido, no implementado) y de las Etapas A/B (futuras); `## 🗂️ Dónde consultar qué`; y `## 📐 Qué es y qué NO es este documento` con responsabilidad única, regla de admisión y regla de frescura. `docs/CONVENTIONS.md` gana `### Contrato del ROADMAP (canónico; Plan 157)`, que además resuelve una sobreafirmación: el orden de ejecución **detallado** pertenece al Plan, y el ROADMAP expresa sólo el orden de alto nivel de sus iniciativas. `docs/glossary/terms.md` y `docs/glossary/INDEX.md` registran `ROADMAP` **enrutando** al contrato, sin duplicar la definición.

**Corrección registrada.** Durante la edición se perdieron líneas preexistentes del `[Unreleased]` del changelog y la viñeta de resumen del Plan 146 en el encabezado del INDEX. Ambas se restauraron antes de la validación: `git diff --stat HEAD -- CHANGELOG.md` es **adición pura** (36 inserciones, 0 borrados) y la descripción del Plan 146 permanece. Registrado como `<PLAN-157>:C-1`.

**Alcance.** Diez rutas: `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/glossary/terms.md`, `docs/glossary/INDEX.md`, `docs/AGENTS.md`, `README.md`, `AGENTS.md`, `docs/plans/157-canonical-visual-roadmap.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`. Ningún artefacto movido, renombrado ni eliminado; sin carpetas nuevas.

**No realizado (por diseño).** No se implementó ninguna capacidad; no se completó Autonomy ni el envelope; no se resolvió ninguna decisión pendiente; no se creó capability registry ni decision register; no se implementó documentación automática; no se alteró governance del Protocol ni arquitectura del runtime; `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`, `docs/VERSIONING.md`, `docs/placement-contract.md`, RFCs, ADRs y planes cerrados con **0 diff**; sin `VERSION` bump, sin tag, sin promoción.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```
