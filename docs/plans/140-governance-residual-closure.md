# Plan 140 — Governance Residual Closure (F-1, PC-5, B-2, Roadmap Impact, C-2 GAP)

**Status:** Executed
**Fecha:** 2026-09-20
**RFC:** — (vía plan; DEV-only: `docs/plans/` + `CHANGELOG.md` + un test anclado; sin efecto en `protocol/.agents/`, RFC-56 no aplica; justificación documentada en `## Objetivo`)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L1 (coordinación: 1 agente; scope: registros de gobernanza en `docs/plans/` + `CHANGELOG.md` + un test anclado; impacto arquitectónico: ninguno — no crea mecanismos, estados ni registries; sin impacto de release; duración: 1 sesión)
**Depende de:** plan 116, plan 136, plan 137, plan 138 y plan 139 (los cinco artefactos que poseen los pendientes que este Change reconcilia)
**Origen:** solicitud directa del mantenedor (Change «Plan140 — Governance Residual Closure», 2026-09-20), que enumera los cinco pendientes objetivo y fija el principio de cierre de este Plan

## Objetivo

Dejar el inventario de gobernanza **sin pendientes accionables** ejecutando, en un
único Change, la revisión, resolución y cierre de los pendientes ya conocidos:

1. `<PLAN-139>:F-1` / `<PLAN-136>:PC-5`
2. plan 137 / `B-2` — EARS
3. plan 137 — `Roadmap Impact`
4. `<PLAN-138>:PC-2` — Scope Expansion
5. plan 116 — `C-2 GAP`

El objetivo **no** es crear gobernanza nueva: es terminar de limpiar la deuda
existente **reutilizando los mecanismos ya construidos**, para que el trabajo
siguiente vuelva a ser evolución funcional de ARgentOS.

**Qué no cambia.** Este Change **no** crea ni modifica mecanismos: no introduce
Scope Expansion, ni autoridad nueva, ni estados de lifecycle, ni registries, ni
checkers, ni workflows; **no** modifica `protocol/`, `runtime/`, `tools/`, `.agents/`,
`ROADMAP.md`, ninguna RFC, ningún ADR ni `docs/CONVENTIONS.md`; y **no** reabre el
contrato de C-2, la discusión de CI, el Plan 121, R4 ni el modelo de estado de cierre
(`docs/CONVENTIONS.md:Change Lifecycle — Estado de cierre, grafo de commit y árbol
material (modelo, Plan 134)`).

**Frontera de autoridad.** Los pendientes 1–5 están enumerados en el pedido y este
Plan queda autorizado a investigarlos, reconciliarlos y cerrarlos **con la evidencia
disponible**. Donde la evidencia no alcanza para un cierre legítimo, el elemento
permanece `DEFERRED` con su owner: no se convierte `DEFERRED` en `RESOLVED` ni se
declara `non-actionable` nada que todavía requiera trabajo.

**Vía de autorización.** El mantenedor solicitó explícitamente este Change y enumeró
en él los pendientes objetivo y el principio de cierre («eliminar los pendientes
accionables, no falsificar estados»). El cambio es DEV-only.

## Criterio de entrada

- [x] Baseline registrado: `dev` en `8727b60b2361ca03bc389fc6328d1b1788cc6911` (tree `2bc144d76ffe2c17432638d1c1208525bc97f3f5`), working tree limpio.
- [x] Los cinco pendientes son legibles en sus artefactos: `<PLAN-139>:F-1` (`open`), `<PLAN-136>:PC-5` (`resolución: pendiente`), `<PLAN-137>` (`Aprobado para redacción`, con `Roadmap Impact: REQUIRED` y `<PLAN-137>:PC-1` pendiente), `<PLAN-138>:PC-2` (`deferred`), plan 116 (`C-2 GAP` declarado como residuo no bloqueante).
- [x] Las reglas que se aplican ya existen y están vigentes: `.agents/policies/validation-closure.md` §5.1/§5.2 y §7, y `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.4.
- [x] Plan 140 es el próximo número libre del registro, verificado contra `docs/plans/` y `docs/plans/INDEX.md`.
- [x] Batería canónica ejecutada sobre el baseline: los seis checkers en verde y `pytest tests/` con **1 failed, 1009 passed** — el fallo es el defecto `<PLAN-140>:F-1`, registrado y corregido en este Change (no se declara verde un baseline que no lo está).

## Matriz de investigación (resultado real, no supuesto)

| Pendiente | Premisa registrada | Evidencia observada en el repositorio | Estado real | Acción posible / ejecutada |
|---|---|---|---|---|
| `<PLAN-136>:PC-5` / `<PLAN-139>:F-1` | «la política vigente no contempla qué ocurre cuando una determinación de cierre obliga a reconciliar un artefacto que el `Scope` excluye», y `DEFERRED` exige una pending decision existente que al redactar el Plan puede no existir | `.agents/policies/validation-closure.md` §5.1/§5.2 (una determinación `REQUIRED` es obligación de estado y **nunca** autorización; con el artefacto fuera de Scope la vía es `DEFERRED` + PC existente) y §7 («un impacto diferido sin pending decision que lo gobierne no es `DEFERRED` sino una condición bloqueante sin resolver»); `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.4; regresión `tests/test_sae_scope_enforcement.py` | **Premisa superada**: la situación **sí** está contemplada y su desenlace está definido (obligación registrada `DEFERRED` con PC existente, o condición bloqueante). Sin pregunta independiente residual | Registrar `<PLAN-136>:PC-5` como `superseded` (metadata evolucionable) y `<PLAN-139>:F-1` como `resolved` |
| plan 137 / `B-2` — EARS | `B-2` (= `F-01` + `F-02`) describe trabajo futuro: un validador EARS estructural | `protocol/.agents/harness/gate_validator.py` con `TRIGGERS["H01"]["ears"] = True`, `EARS_RE` con los cinco patrones y el chequeo `ears` PASS/FAIL; `protocol/.agents/harness/tests/test_gate_validator.py`; job `check-protocol` de `.github/workflows/check-protocol.yml`; `F-01` resuelta por plan 33/RFC-34 (bullets canónicos) y `F-02` por plan 29; dogfood read-only ejecutado en este Change (`PASS` con bullets EARS, `FAIL` con `- The API should handle errors gracefully.`) | **`B-2` satisfecho**: mecanismo responsable existente, verificado y con cobertura. **Cero residual de `B-2`** | Registrar la determinación; **no** implementar nada nuevo; el plan 137 no fue autorizado para ejecución (`Aprobado para redacción`) y `Superseded` exige un plan reemplazante que no existe — queda clasificado, no forzado |
| plan 137 — `Roadmap Impact` | determinación `REQUIRED` con `ROADMAP.md` (su entry `EARS structural validator`) como artefacto a reconciliar, y continuidad en `<PLAN-137>:PC-1` | `.agents/policies/validation-closure.md` §5.2: `REQUIRED` **no** autoriza escribir el artefacto que nombra; con el artefacto fuera de Scope la clasificación correcta es `DEFERRED` con la pending decision **existente** que la gobierna; `ROADMAP.md` no figura en el `Scope` del plan 137 | **Determinación reconciliable**: la obligación queda satisfecha por el mecanismo vigente (`DEFERRED` + `<PLAN-137>:PC-1`), sin ninguna escritura | Reclasificar la determinación a `DEFERRED`, preservar el texto original, registrar la continuidad en `<PLAN-137>:PC-1` y **no** tocar `ROADMAP.md` |
| `<PLAN-138>:PC-2` | si SAE necesita un mecanismo autónomo de ampliación de Scope | `<PLAN-138>:PC-2` está `deferred` con owner (materializado por el plan 139, DEC-3) y `.agents/policies/supervised-autonomous-execution.md` §1.4 declara que no existe ni se introduce; `blocking: no` | **`DEFERRED` y no accionable actualmente**: no hay necesidad actual de Scope Expansion y no existe una taxonomía canónica de «non-actionable» que introducir | Registrar la clasificación en el inventario de este Plan; **no** alterar su contenido, su estado ni la policy; **no** crear taxonomía nueva |
| plan 116 — `C-2 GAP` | `C-2` reporta `GAP` por el commit único de cierre (auto-referencia) | ``python tools/check_lifecycle_checkpoint.py`` sobre el corpus real: `116-adversarial-deliberation-mvp-closure.md: GAP — multiple declared revalidations could correspond to the closure state; ambiguity, evidence insufficient`; `GAP` es advisory y no cambia el exit code (`exit 0`, `ANOMALY=0`); la causa es la ambigüedad `Tier 2` del registro del plan 116, artefacto **cerrado** | **Limitación histórica/documental no accionable**: no es una violación, no bloquea ningún lifecycle y no se resuelve sin modificar el artefacto cerrado o el contrato de C-2, ambos prohibidos | Registrar la clasificación y la razón; **no** reabrir C-2/CI, Plan 121, R4, closure identity ni el plan 116 |

## Determinaciones

### 1. `<PLAN-136>:PC-5` → `superseded` y `<PLAN-139>:F-1` → `resolved`

`PC-5` preguntaba si la gobernanza debe **definir explícitamente** qué ocurre cuando
una determinación `REQUIRED` obliga a reconciliar un artefacto que el `Scope` excluye.
Desde el plan 138 —y generalizado por el plan 139 (DEC-2)— la respuesta está escrita
en el lugar canónico: la determinación es una **obligación de estado** y nunca una
autorización de escritura; con el artefacto fuera de Scope la vía es `DEFERRED` con la
pending decision **existente** que la gobierna; la autorización no se infiere por
clasificación, proximidad semántica, dependencia documental ni requisito de cierre; y
si no existe pending decision que gobierne el diferimiento, la situación no es
`DEFERRED` sino una **condición bloqueante sin resolver** (§7 de la policy).

Esa segunda mitad es la que `PC-5` señalaba como no contemplada, y también está
contemplada: el desenlace está definido (condición bloqueante ⇒ no se cierra, se
escala), y la continuidad del caso —que exista o no un mecanismo de ampliación
legítima de Scope— vive en `<PLAN-138>:PC-2`, `deferred` con owner. `PC-5` **no**
contiene por lo tanto una cuestión independiente que requiera una decisión nueva:
su premisa quedó superada por la regla vigente. La transición de estado de `PC-5` es
metadata **evolucionable** de una pending decision, no una reescritura de su
observación, su evidencia ni su provenance, que se preservan verbatim.

### 2. `B-2` (EARS) satisfecho — sin residual

El mecanismo responsable existe en el payload y opera: el validador estructural del
harness (plan 66/RFC-57) chequea EARS para H01, con los cinco patrones del estándar,
cobertura en `protocol/.agents/harness/tests/`, ejecución en CI y la forma canónica de
criterios ya alineada al contrato por el plan 33/RFC-34. El dogfood read-only de este
Change lo confirma sobre especímenes con procedencia (un bullet EARS produce `ears`
PASS y `decision: PASS`; un bullet no EARS produce `ears FAIL — 1 bullets do not match
EARS` y `decision: FAIL`). **No hay trabajo residual de `B-2`.**

Lo que el plan 137 proponía —una guarda DEV de paridad `tools/check_ears_coverage.py`—
**no** es un residual de `B-2`: es trabajo nuevo de aseguramiento, y su ejecución no
está autorizada (el plan está `Aprobado para redacción`, y su propio `## Criterio de
entrada` exige `Aprobado para ejecución`). `Superseded` no es una salida legítima
porque exige indicar el plan reemplazante y no existe ninguno
(`docs/CONVENTIONS.md:Convenciones`, ciclo de status de planes; precedente del plan
87 ante la misma situación). El plan 137 queda, por lo tanto, **clasificado**: sin
residual de `B-2`, con su propuesta de guarda pendiente de una decisión humana de
ejecución que ya está declarada en su propio `## Criterio de entrada` y en su
`## Human authority boundary`.

### 3. plan 137 — `Roadmap Impact` reconciliado

La obligación concreta era retirar de `ROADMAP.md` la entry `EARS structural
validator`, que declara como trabajo futuro una capacidad que ya existe. La regla
vigente (§5.2) no permite satisfacerla escribiendo un artefacto fuera del `Scope`
autorizado del plan 137, y la clasificación correcta para «existe impacto, pero su
actualización requiere una autoridad que todavía no está disponible» es **`DEFERRED`**
con la pending decision **existente** que la gobierna: `<PLAN-137>:PC-1`, owner
mantenedor. Con eso la obligación queda gobernada por el mecanismo existente,
`ROADMAP.md` queda con **0 diff** y no se inventa ninguna excepción. `<PLAN-137>:PC-1`
permanece como la decisión humana que conserva la continuidad; se registra que **no**
requiere acción del agente en el estado actual.

### 4. `<PLAN-138>:PC-2` — `DEFERRED` y no accionable actualmente

La decisión ya está tomada y materializada: no existe ni se introduce un mecanismo
autónomo de Scope Expansion, ampliar `Task`/`Scope`/`Authority` es frontera de
autoridad humana y produce `STOP` / `REQUIRES_HUMAN`, y la vía legítima es una nueva
decisión humana de alcance. No hay ninguna necesidad actual de Scope Expansion en el
repositorio, de modo que la decisión **no es accionable ahora** y no requiere ninguna
acción adicional. Se preserva íntegra para el futuro. **No existe una taxonomía
canónica de «non-actionable»** para pending decisions (el vocabulario canónico es
`pendiente`/`resuelta`/`deferred` y la metadata `blocking`), así que **no se inventa
ninguna**: la marca explícita de no-accionabilidad es el registro de este Plan, y el
contenido, el estado y la policy no se alteran.

### 5. plan 116 — `C-2 GAP` es una limitación histórica/documental no accionable

Determinación sobre las cinco preguntas exigidas:

1. **¿Representa una violación actual?** No. `GAP` es evidencia faltante o ambigua
   —advisory— y nunca una contradicción: `C-2` sale con `exit 0` y `ANOMALY=0` sobre
   el corpus real, y el propio contrato del checker declara que un `GAP` no cambia el
   exit code ni invalida la evidencia registrada.
2. **¿Requiere una acción actualmente autorizada?** No. La ambigüedad `Tier 2` es una
   propiedad del registro del plan 116 (dos segmentos de su `## Validation anchor`
   declaran una revalidación que referencia el estado de cierre, bajo la convención
   anti-auto-referencia del corpus). Resolverla exigiría reescribir el anchor de un
   plan **cerrado** (prohibido: el artefacto cerrado no se reabre) o cambiar el
   contrato de `C-2` (prohibido por este Plan y por el modelo del plan 134).
3. **¿Bloquea algún lifecycle actual?** No. `C-2` es advisory para el corpus; el plan
   116 está `Executed` con condición derivada `Closed` derivada sobre la
   correspondencia con su anchor aplicable, y ningún cierre actual depende de esa
   clasificación.
4. **¿Puede resolverse con las reglas actuales sin modificar el contrato de C-2?** No
   para el artefacto existente: la única vía lícita es registrar el hecho en un
   artefacto nuevo que referencie al cerrado, que es lo que este Plan hace.
5. **¿Es una limitación histórica/documental no accionable?** Sí: se clasifica
   **HISTORICAL / NON-ACTIONABLE**, con la razón y la evidencia registradas, sin
   modificar el contrato de `C-2`, el plan 116 ni la discusión de CI.

## Entregables

1. `docs/plans/140-governance-residual-closure.md` — este Plan, con la matriz, las cinco determinaciones, el inventario final, el anchor, el checkpoint y los registros de lineage.
2. `docs/plans/136-d01-mechanical-checker.md` — `<PLAN-136>:PC-5` con su `resolución` de estado actualizada a `superseded`, preservando el resto del registro.
3. `docs/plans/139-sae-governance-boundary-closure.md` — `<PLAN-139>:F-1` con su estado actualizado a `resolved` y el bloque append-only que documenta la transición.
4. `docs/plans/137-ears-structural-validator.md` — determinación de `B-2` y del `Roadmap Impact`, con la reclasificación a `DEFERRED` y el estado de `<PLAN-137>:PC-1`.
5. `tests/test_sae_scope_enforcement_dogfood.py` — corrección del test anclado roto (`<PLAN-140>:F-1`), preservando y endureciendo la protección histórica del plan 136.
6. `docs/plans/INDEX.md` — registro del Plan 140, su serie y el header de estado.
7. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 140, RFC-—)`.

## Pasos

1. **Observar el estado real (read-only).** Verificar los cinco pendientes en sus artefactos, las policies vigentes y la evidencia Git, y construir la matriz de investigación sin anticipar resultados.
2. **Correr la batería del baseline** y registrar su resultado real, incluido cualquier fallo (se detectó el defecto `<PLAN-140>:F-1`).
3. **A — cerrar `PC-5`/`F-1`.** Registrar `PC-5` como `superseded` (sólo su campo de resolución) y `F-1` como `resolved` con el bloque append-only de metadatos, preservando los elementos inmutables.
4. **B — determinar `B-2`.** Registrar la determinación con el mecanismo responsable y su evidencia; no implementar nada nuevo.
5. **C — reconciliar el `Roadmap Impact`** del plan 137: reclasificar a `DEFERRED`, preservar el texto original, registrar la continuidad en `<PLAN-137>:PC-1` y no escribir `ROADMAP.md`.
6. **D/E — clasificar** `<PLAN-138>:PC-2` y el `C-2 GAP` del plan 116 en el inventario final, sin alterar sus artefactos.
7. **Corregir el defecto detectado** (`<PLAN-140>:F-1`) y registrar la corrección y su revalidación.
8. **Registrar el Plan 140** en `docs/plans/INDEX.md` (serie + header) y en `CHANGELOG.md`.
9. **Verificar** la batería completa, los gates C-1/C-2/C-3 y la ausencia de diff en los artefactos protegidos.
10. **Registrar anchor y checkpoint**, y commitear atómicamente en `dev`. Sin push, sin merge, sin tag, sin release, sin promotion.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el Scope es decisión humana.

- `docs/plans/140-governance-residual-closure.md` (este Plan)
- `docs/plans/136-d01-mechanical-checker.md` (sólo el campo `resolución` de `<PLAN-136>:PC-5`)
- `docs/plans/139-sae-governance-boundary-closure.md` (sólo el estado de `<PLAN-139>:F-1` y el bloque append-only de metadatos)
- `docs/plans/137-ears-structural-validator.md` (determinaciones de `B-2` y de `Roadmap Impact`, y estado de `<PLAN-137>:PC-1`)
- `tests/test_sae_scope_enforcement_dogfood.py` (sólo el test anclado roto en `HEAD`, ver `<PLAN-140>:F-1`)
- `docs/plans/INDEX.md`
- `CHANGELOG.md`

**Excluido explícitamente:**

- `ROADMAP.md` — no se modifica. `Roadmap Impact: REQUIRED` **no** autoriza
  escribirlo; es la regla que este mismo Plan aplica (ver `## Determinaciones` §3).
- `docs/plans/138-sae-scope-authority-hardening.md` y
  `docs/plans/116-adversarial-deliberation-mvp-closure.md` — **0 diff**: sus
  pendientes se clasifican en el inventario de este Plan; no se altera su contenido.
- `protocol/`, `runtime/`, `tools/`, `.agents/` — **0 diff**. No se crea policy,
  checker, mecanismo, estado, registry ni authority class. La batería se ejecuta
  como está.
- `docs/CONVENTIONS.md`, RFCs y ADRs — la regla que se aplica ya existe; no se crea
  ni se modifica la fuente normativa.
- `.github/workflows/` — CI no se toca.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–10 de este Plan: observar read-only el estado real de los cinco pendientes, de las policies y de la evidencia Git; registrar `<PLAN-136>:PC-5` como `superseded` y `<PLAN-139>:F-1` como `resolved` preservando los elementos inmutables; registrar la determinación de `B-2` sin implementar nada nuevo; reconciliar el `Roadmap Impact` del plan 137 a `DEFERRED` con `<PLAN-137>:PC-1` como continuidad; clasificar `<PLAN-138>:PC-2` y el `C-2 GAP` del plan 116 en el inventario final; corregir el test anclado roto preservando su protección histórica; registrar el Plan 140, su anchor y su checkpoint; verificar la batería completa, los gates C-1/C-2/C-3 y el 0 diff de los artefactos protegidos. **No** crear ningún mecanismo, policy, checker, estado, registry, authority class ni workflow nuevos; **no** modificar `ROADMAP.md`, `protocol/`, `runtime/`, `tools/`, `.agents/`, RFCs, ADRs ni los planes 116 y 138. Sin autoridad nueva: la autoridad es este Plan y el pedido del mantenedor que lo origina.
- **Scope:** `docs/plans/140-governance-residual-closure.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/137-ears-structural-validator.md`, `tests/test_sae_scope_enforcement_dogfood.py`, `docs/plans/INDEX.md`, `CHANGELOG.md`

## Criterios de salida

- [ ] `<PLAN-136>:PC-5` está formalmente `superseded` y `<PLAN-139>:F-1` formalmente `resolved`, con sus elementos inmutables intactos.
- [ ] `B-2` (EARS) queda registrado como satisfecho, con el mecanismo responsable y su evidencia, y sin residual.
- [ ] El `Roadmap Impact` del plan 137 queda reconciliado como `DEFERRED` con `<PLAN-137>:PC-1` como continuidad, y `ROADMAP.md` con **0 diff**.
- [ ] `<PLAN-138>:PC-2` queda clasificado `DEFERRED` / no accionable actualmente, sin introducir Scope Expansion ni taxonomía nueva.
- [ ] El `C-2 GAP` del plan 116 queda clasificado histórico/no accionable, sin reabrir C-2/CI, Plan 121, R4, closure identity ni el plan 116.
- [ ] El inventario final declara `OPEN / ACTIONABLE = 0` y enumera `DEFERRED` y `HISTORICAL / NON-ACTIONABLE` con evidencia.
- [ ] Los seis checkers canónicos PASS; `pytest tests/` PASS; C-1/C-2/C-3 sin `ANOMALY`.
- [ ] `Documentation Impact` y `Roadmap Impact` determinados de forma independiente y con evidencia.
- [ ] No existe ningún finding abierto que impida el cierre.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/ -q
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación específica de este Change (reutiliza lo existente; no agrega tests ni
checkers, y no incorpora nada a `docs/VERSIONING.md` §4.1):

```bash
python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q
git diff HEAD --name-only -- ROADMAP.md protocol/ runtime/ tools/ .agents/ docs/CONVENTIONS.md docs/rfc/ docs/adr/ docs/plans/116-adversarial-deliberation-mvp-closure.md docs/plans/138-sae-scope-authority-hardening.md
git diff HEAD --stat -- docs/plans/136-d01-mechanical-checker.md docs/plans/139-sae-governance-boundary-closure.md docs/plans/137-ears-structural-validator.md
git rev-parse HEAD^{tree}
```

La segunda corrida debe dar **0 diff**; la tercera debe mostrar **sólo** metadata de
estado y bloques append-only, nunca una sección normativa reescrita. La verificación
del mecanismo EARS es read-only y no vive en una suite nueva:

```bash
python protocol/.agents/harness/gate_validator.py --trigger H01 --artifact <specimen>
```

## Findings / Correcciones / Pending

### Findings

- `<PLAN-140>:F-1` — estado: `resolved` (corregido dentro del Scope por `<PLAN-140>:C-1`); observación: el estado comprometido de `dev` deja la suite canónica en rojo: el test `test_the_closed_plan_of_the_incident_keeps_its_history` de `tests/test_sae_scope_enforcement_dogfood.py` afirma que el plan cerrado del incidente **debe** mostrar cambios contra `HEAD` (`assert changed, "the F-3 closure must be visible as a change"`), invariante que sólo es verdadera mientras el cambio del plan 139 está sin commitear; sobre el estado comprometido el diff es vacío y la aserción falla, de modo que la suite queda roja de forma permanente y CI con ella (el flujo `check-protocol` corre `python -m pytest tests/ -q`); evidencia original: `python -m pytest tests/ -q` sobre el baseline `8727b60` con working tree limpio → `1 failed, 1009 passed in 183.93s`, con la traza `AssertionError: the F-3 closure must be visible as a change` / `assert []` en `tests/test_sae_scope_enforcement_dogfood.py`; estado Git observado: `8727b60b2361ca03bc389fc6328d1b1788cc6911` (tree `2bc144d76ffe2c17432638d1c1208525bc97f3f5`), working tree limpio; provenance original: Paso 2 (batería del baseline) de la ejecución del Plan 140 (2026-09-20); resolución: corregido por `<PLAN-140>:C-1` con una invariante independiente del estado de Git —el contenido normativo del plan cerrado se fija por digest normalizado (se excluye el bloque append-only de metadatos y se canonicalizan los valores de estado y resolución, que LC-1 declara evolucionables)—, lo que **endurece** la protección: cualquier cambio fuera de esa metadata cambia el digest y falla el test.

- `<PLAN-140>:F-2` — estado: `resolved` (corregido por registro en artefacto nuevo, `<PLAN-140>:C-2`); observación: el `## Checkpoint / cierre` del Plan 139 declara como «árbol material del commit de cierre (tree id)» el valor `e284f98d8915f8c3e917f40218420caf604328b2` y afirma que **coincide** con la state identity T1 del anchor «porque el commit atómico **es** la materialización exacta del estado validado», pero Git contradice esa igualdad: el árbol del commit de cierre es `2bc144d76ffe2c17432638d1c1208525bc97f3f5`, y el árbol declarado difiere de él exactamente en `docs/plans/139-sae-governance-boundary-closure.md`, es decir en el propio registro de gobernanza que el cierre publicó; evidencia original: `git rev-parse 8727b60^{tree}` → `2bc144d76ffe…`, `git cat-file -t e284f98d8915f8c3e917f40218420caf604328b2` → `tree`, y `git diff --name-status e284f98d8915f8c3e917f40218420caf604328b2 2bc144d76ffe2c17432638d1c1208525bc97f3f5` → `M docs/plans/139-sae-governance-boundary-closure.md` (única diferencia); estado Git observado: `8727b60b2361ca03bc389fc6328d1b1788cc6911`, working tree limpio; provenance original: Paso 9 (verificación de los planes 136–139) de la ejecución del Plan 140 (2026-09-20); resolución: corregido por `<PLAN-140>:C-2` mediante un artefacto nuevo que registra el hecho de Git, sin modificar el plan cerrado (RFC-46; el artefacto cerrado no se reabre) y sin alterar ninguna condición derivada: la identidad del **estado de cierre** del Plan 139 es la del anchor aplicable y su correspondencia con `C-2` R2 no se ve afectada —lo inexacto es la declaración del árbol **material**, que el modelo del plan 134 define como un hecho de Git y cuya divergencia con el estado de cierre es esperada y exige atribución.

- `<PLAN-140>:F-3` — estado: `deferred` (owner: mantenedor); observación: el plan 136 conserva findings con state metadata sin transición y pending decisions abiertas que **no** forman parte de los cinco pendientes autorizados por este Change: `<PLAN-136>:F-1`, `<PLAN-136>:F-2`, `<PLAN-136>:F-4`, `<PLAN-136>:F-5` y `<PLAN-136>:F-6` figuran como `open`, y `<PLAN-136>:PC-2` y `<PLAN-136>:PC-3` como `pendiente` (ambas son fronteras de payload con vía RFC-56, ya representadas en `ROADMAP.md:Pendientes que requieren autorización` como residuos `B-4` y `B-7`); `F-4`, `F-5` y `F-6` fueron corregidos durante la ejecución del plan 136 por `<PLAN-136>:C-1`..`C-4`, de modo que lo que falta es la transición de estado, que CL-8 reserva al humano; evidencia original: el registro `### Findings` y `### Pending decisions` de `docs/plans/136-d01-mechanical-checker.md`, y `ROADMAP.md:Pendientes que requieren autorización`; estado Git observado: `8727b60b2361ca03bc389fc6328d1b1788cc6911`, working tree limpio; provenance original: Paso 1 (observación read-only) de la ejecución del Plan 140 (2026-09-20); destino: el inventario `DEFERRED` de este Plan, con owner mantenedor; la resolución de esos estados es una decisión humana y este Change no la toma porque no está autorizado por él.

### Correcciones

- `<PLAN-140>:C-1` — refs origen: `<PLAN-140>:F-1`; alcance de revalidación: `tests/test_sae_scope_enforcement_dogfood.py` (`test_the_closed_plan_of_the_incident_keeps_its_history`), sobre `docs/plans/136-d01-mechanical-checker.md` como sujeto anclado, más la suite completa `python -m pytest tests/ -q` y la suite de SAE/Scope; evidencia: la corrida del baseline (`1 failed, 1009 passed`), la corrida posterior a la corrección y la revalidación del estado de cierre registradas en el `## Validation anchor`; carácter: FACTUAL / TRACEABILITY (no normativo); autorización: este Plan y el pedido del mantenedor que lo origina (corrección determinista dentro del Scope, preautorizada por el principio de autocorrección del Change); qué se corrigió: la forma del test anclado —una aserción dependiente del diff sin commitear se reemplaza por aserciones de contenido y por un digest normalizado del contenido normativo del plan cerrado— conforme al contrato de estabilidad de tests anclados de `tests/AGENTS.md`; no se relajó ninguna invariante: la protección pasa a ser independiente del estado de Git y cubre también los elementos inmutables de los registros del plan cerrado.

- `<PLAN-140>:C-2` — refs origen: `<PLAN-140>:F-2`; alcance de revalidación: `docs/plans/139-sae-governance-boundary-closure.md` como sujeto observado (no modificado) y `docs/plans/140-governance-residual-closure.md` como artefacto de registro, más los gates C-1/C-2/C-3 sobre el corpus real; evidencia: las salidas de Git registradas en `<PLAN-140>:F-2` (`git rev-parse`, `git cat-file -t` y el `git diff` cuyo único nombre es el propio plan 139) y la clasificación `VALID` que C-2 mantiene para el plan 139 (R2 se evalúa sobre la identidad del estado de cierre, no sobre el árbol material); carácter: FACTUAL / TRACEABILITY (no normativo); autorización: este Plan (registro post-close en artefacto nuevo; el plan cerrado no se reabre); qué se corrigió: el registro factual —el árbol material del commit de cierre del plan 139 queda establecido como un hecho de Git y su divergencia con el estado de cierre queda atribuida a los registros de gobernanza del cierre (RFC-75 Mecanismo 7)—, sin tocar el artefacto cerrado ni ninguna condición derivada.

### Pending decisions

No se registran pending decisions nuevas. Los asuntos que requieren una decisión
humana conservan su continuidad en las pending decisions **existentes**:
`<PLAN-137>:PC-1` (reconciliación de `ROADMAP.md`; clasificada `deferred`), el
`## Criterio de entrada` y el `## Human authority boundary` del plan 137 (autorización
de ejecución de la guarda de paridad EARS), `<PLAN-138>:PC-2` (`deferred`; mecanismo
de ampliación de Scope), `<PLAN-136>:PC-2` y `<PLAN-136>:PC-3` (fronteras de payload
con vía RFC-56) y `<PLAN-140>:F-3` (transiciones de estado pendientes en el plan 136).
Ninguna de ellas es accionable por el agente en el estado actual: todas requieren
autoridad humana o la vía RFC-56.

## Inventario final

### 1. `OPEN / ACTIONABLE`

**Ninguno.** No queda ningún asunto de gobernanza que este Change pueda ejecutar
legítimamente con la autoridad y el Scope vigentes.

### 2. `DEFERRED`

| Elemento | Por qué no es accionable ahora | Continuidad / owner |
|---|---|---|
| `<PLAN-137>:PC-1` — reconciliar `ROADMAP.md` retirando la entry `EARS structural validator` | `ROADMAP.md` está fuera del Scope; la escritura requiere autorización del mantenedor | la propia `<PLAN-137>:PC-1` (owner: mantenedor) |
| plan 137 — ejecutar o retirar la guarda de paridad EARS (`tools/check_ears_coverage.py`) | el plan está `Aprobado para redacción`; ejecutar requiere `Aprobado para ejecución` y `Superseded` exige un plan reemplazante inexistente | `## Criterio de entrada` y `## Human authority boundary` del plan 137 (owner: mantenedor) |
| `<PLAN-138>:PC-2` — ¿existe un mecanismo de ampliación legítima de Scope? | no hay necesidad actual; no existe ni se introduce mecanismo; toda ampliación es frontera de autoridad humana | la propia `<PLAN-138>:PC-2` (owner: mantenedor) |
| `<PLAN-136>:PC-2` (`F-17`) y `<PLAN-136>:PC-3` (`F-16`) — fronteras de payload | tocan contratos de `protocol/.agents/`; requieren RFC-56 | `ROADMAP.md:Pendientes que requieren autorización` (residuos `B-4` y `B-7`) |
| `B-8` residual — session risk de single-instance sin slot en `METRICS.md` | deuda de payload de baja prioridad; requiere cambio de payload | `ROADMAP.md:Pendientes que requieren autorización` |
| `<PLAN-136>:F-1`, `F-2`, `F-4`, `F-5`, `F-6` — state metadata sin transición | la resolución de un finding es decisión humana (CL-8); `F-4`/`F-5`/`F-6` ya fueron corregidos por `<PLAN-136>:C-1`..`C-4` | `<PLAN-140>:F-3` (owner: mantenedor) |
| `<PLAN-114>:F-1`/`F-2` (reconocimiento formal) y `<PLAN-114>:F-3` | actos humanos de reconocimiento posteriores al cierre del plan 114; no reabren el artefacto cerrado | registros del plan 116 y `<PLAN-114>` (owner: mantenedor) |
| release de `11.1.0`/`11.2.0` y de `11.3.0`–`11.5.0` | `Promoted`/`Released` son acciones humanas; el agente las reporta `FORBIDDEN` | `docs/VERSIONING.md` §9 y el mantenedor |

### 3. `HISTORICAL / NON-ACTIONABLE`

| Elemento | Clasificación y razón |
|---|---|
| plan 116 — `C-2 GAP` (`multiple declared revalidations could correspond to the closure state; ambiguity, evidence insufficient`) | `GAP` advisory del corpus real (`exit 0`, `ANOMALY=0`); propiedad del registro de un plan cerrado (ambigüedad `Tier 2` de su anchor bajo la convención anti-auto-referencia); resolverla exigiría reescribir un artefacto cerrado o cambiar el contrato de `C-2`, ambos prohibidos; no bloquea ningún lifecycle |
| `<PLAN-136>:C-3` — corrección con autorización **no** establecida | traza factual preservada (RFC-46); el defecto que la originó (`<PLAN-136>:F-3`) está `resolved` y la regla que lo gobierna es operacional; no se legitima retrospectivamente ni requiere acción |
| `<PLAN-137>` — entrada `EARS structural validator` de `ROADMAP.md` como «Próximo dogfood» | hecho documental obsoleto respecto del payload real (el validador existe desde el plan 66/RFC-57); la corrección del mapa es `DEFERRED`, no un trabajo abierto |
| observaciones de gobernanza de los planes 136 y 139 sobre la frontera Impact↔autorización | ya materializadas como regla operacional; los registros históricos conservan su contexto y no se actualizan |

## Riesgos

- **Forzar el cierre para vaciar la lista.** Mitigación: cada clasificación de `DEFERRED`/`HISTORICAL` nombra su razón, su evidencia y su continuidad; la matriz de investigación se construyó sobre el repositorio, no sobre la descripción resumida de los pendientes.
- **Modificar de más la evidencia histórica.** Mitigación: sólo se toca metadata de estado (elemento evolucionable por LC-1) y bloques append-only, con los elementos inmutables preservados; `git diff` restringido en `## Verificación`.
- **Convertir `DEFERRED` en mecanismo.** Mitigación: `ROADMAP.md`, `.agents/`, `runtime/` y `tools/` quedan con 0 diff y no se crea taxonomía, estado ni registry nuevos.
- **Corregir un test relajándolo.** Mitigación: la corrección reemplaza una invariante dependiente del estado de Git por un digest del contenido normativo; la protección se amplía a los elementos inmutables de los registros y no se elimina ninguna aserción de contenido.

## Trazabilidad

`<PLAN-136>:PC-5` (gap de gobernanza) → plan 138 (`<PLAN-136>:PC-5` re-registrada como `<PLAN-138>:PC-2`; regla `REQUIRED` ≠ autorización) → plan 139 (generalización normativa; `<PLAN-139>:F-1` registra la supersesión sin resolver) → **Plan 140** (cierre formal de `PC-5` y `F-1`). `B-2` → plan 29 + plan 33/RFC-34 + plan 66/RFC-57 → plan 137 (auditoría: el validador ya existe) → **Plan 140** (determinación de `B-2` satisfecho y reconciliación del `Roadmap Impact`). `<PLAN-138>:PC-2` → plan 139 (DEC-3) → **Plan 140** (clasificación). plan 116 (`C-2 GAP`) → plan 134 (modelo de estado de cierre y contrato de C-2) → **Plan 140** (clasificación histórica).

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 140 (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 140 (Governance Residual Closure): `docs/plans/140-governance-residual-closure.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/137-ears-structural-validator.md`, `tests/test_sae_scope_enforcement_dogfood.py`, `docs/plans/INDEX.md`, `CHANGELOG.md`
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python -m pytest protocol/.agents/harness/tests/ -q`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q`
- **Effective inputs (repo content):** el scope declarado (7 paths) más los checkers de `tools/`, la suite `tests/` y el corpus de `docs/plans/` que consume la batería.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14.3; git 2.55.0.windows.5; sin red. La suite completa se ejecutó de forma reproducible y verde sobre el estado de cierre.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `9f8b84af39240db2ebf68eff03113e2497d2b431` (`git write-tree` sobre el índice staged con el cambio completo).
  - **Delta scoped identity (scope S = los 7 paths, ordenados; serialización `scoped-v1`):** `bc1feb6bb682704cada4312ab767ff0b255bfd4a7044535e38f39b7ca0317510`
  - **Límite declarado:** T1 y el delta se midieron con `git write-tree` y `tools/scoped_content_identity.py` sobre el índice staged del Change **antes** de transcribir los cuatro literales de identidad de este registro; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre, de modo que el árbol material del commit de cierre **no** se transcribe como identidad (convención anti-auto-referencia, precedente Planes 114/116/134).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/140-governance-residual-closure.md`, `docs/plans/INDEX.md`, `tests/test_sae_scope_enforcement_dogfood.py`
- **Validity / stale:** el Plan queda **revalidado** por A2 sobre el estado de cierre (ver el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` OK (215 archivos, 10256 referencias); `check_plan_citations` OK; `check_plan_structure` OK; `check_taxonomy_coherence` OK; `check_session_artifacts` OK; `check_version_state` OK (warnings esperados de `dev`: secciones sin tag); `pytest tests/` **1010 passed, 0 failed** (baseline: `1 failed, 1009 passed` — el fallo era el defecto `<PLAN-140>:F-1`, corregido por `<PLAN-140>:C-1`, sin agregar tests nuevos); `pytest protocol/.agents/harness/tests/ -q` **109 passed**; suites de SAE/Scope (`tests/test_sae_scope_enforcement.py` + `tests/test_sae_scope_enforcement_dogfood.py`) **57 passed**; C-1 `VALID` (`ANOMALY=0`), C-2 `VALID` (`ANOMALY=0`, con el `GAP` preexistente del plan 116 sin cambios) y C-3 `VALID` (`ANOMALY=0`, con los cinco registros de lineage del Plan 140 consistentes y el plan 136 íntegro).

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 140 (GC-1, Incremento 3; modelo del Plan 134).*

- **Commits de cierre:** un (1) commit atómico en `dev`, identificado por su mensaje: `docs(governance): close the governance residual inventory (plan 140)`. Su SHA se identifica por el mensaje y su árbol material se resuelve con Git; no se embebe por auto-referencia.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1), es decir `bc1feb6bb682704cada4312ab767ff0b255bfd4a7044535e38f39b7ca0317510` / `9f8b84af39240db2ebf68eff03113e2497d2b431`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado como identidad en este registro; el commit de cierre incluye governance (este Plan, `INDEX.md`, `CHANGELOG.md`), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`). Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Consistencia checkpoint↔anchor:** PASS. La identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron entre la validación y el cierre; C-2 lo verifica sobre el artefacto del Plan. **Revalidación A2:** ejecutada sobre el estado de cierre con el mismo command-set (batería canónica + suite de SAE/Scope + gates C-1/C-2/C-3) y registrada en la nota de ejecución.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 140 y su serie (Septuagésima segunda) con el header de estado actualizado; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 140, RFC-—)`; estados de `<PLAN-136>:PC-5` y `<PLAN-139>:F-1` actualizados; determinación de `B-2` y reclasificación del `Roadmap Impact` del plan 137 registradas; sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag (DEV-only, RFC-69).
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados: `docs/plans/136-d01-mechanical-checker.md` (campo `resolución` de `<PLAN-136>:PC-5`), `docs/plans/139-sae-governance-boundary-closure.md` (estado de `<PLAN-139>:F-1` y bloque append-only de metadatos), `docs/plans/137-ears-structural-validator.md` (determinaciones de `B-2` y de `Roadmap Impact`, y estado de `<PLAN-137>:PC-1`), `docs/plans/INDEX.md` y `CHANGELOG.md`. Aspecto afectado: el registro de gobernanza declaraba pendientes cuya premisa ya había sido superada por decisiones posteriores o cuya resolución no está autorizada en el estado actual. `ROADMAP.md`, `docs/CONVENTIONS.md` y las policies `.agents/` **no** se modifican: la regla aplicable ya existe y su lugar canónico no cambia. Sin release.
- **Roadmap impact:** `DEFERRED` — el Change **no** crea trabajo nuevo ni completa, cancela o re-prioriza ítems del mapa por sí mismo (clasificación estricta `NOT_REQUIRED`), pero existe una obligación de estado identificada que este Plan tiene **prohibido** satisfacer: la entry `EARS structural validator` de `ROADMAP.md` declara como futuro trabajo ya realizado, y `ROADMAP.md` está fuera del Scope autorizado. La obligación queda `DEFERRED` con la pending decision existente que la gobierna, `<PLAN-137>:PC-1` (owner: mantenedor). **`ROADMAP.md`: 0 diff.**
- Condición derivada: **`Closed` (docs-only, sin release)** — `Executed` (status) ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor (A1) ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released` (docs-only, RFC-69).

## Nota de ejecución

**Ejecutado el 2026-09-20** sobre el baseline `8727b60b2361ca03bc389fc6328d1b1788cc6911`
(tree `2bc144d76ffe2c17432638d1c1208525bc97f3f5`), working tree limpio al iniciar.

**Qué se hizo.** Se ejecutaron las cinco determinaciones y las dos correcciones, con
observación read-only previa del repositorio y sin crear gobernanza nueva. **A**:
`<PLAN-136>:PC-5` pasó a `superseded` (sólo su campo `resolución`, que es metadata
evolucionable) y `<PLAN-139>:F-1` a `resolved`, con un bloque
`## Metadatos de estado (evolucionables)` append-only en el Plan 139; ambos registros
conservan verbatim su observación, evidencia, estado Git observado y provenance.
**B**: `B-2` quedó determinado como satisfecho sin residual, con el validador EARS del
payload como mecanismo responsable, su cobertura de tests y CI, y dogfood read-only
ejecutado en esta misma sesión; no se implementó nada nuevo y el Plan 137 no cambió de
status. **C**: el `Roadmap Impact` del Plan 137 se reclasificó de `REQUIRED` a
`DEFERRED` con `<PLAN-137>:PC-1` como pending decision existente que lo gobierna, y
`ROADMAP.md` quedó con 0 diff. **D**: `<PLAN-138>:PC-2` quedó clasificada `DEFERRED` y
no accionable actualmente, sin alterar su contenido ni la policy. **E**: el `C-2 GAP`
del Plan 116 quedó clasificado histórico/no accionable con su razón y su evidencia, sin
reabrir C-2/CI, Plan 121, R4 ni closure identity.

**Correcciones autónomas dentro del Scope.** Dos, ambas detectadas por la verificación
y no por inspección casual. `<PLAN-140>:F-1` / `<PLAN-140>:C-1`: el estado comprometido
de `dev` dejaba la suite en rojo —el test anclado que el Plan 139 agregó afirmaba un
diff contra `HEAD` que sólo existe mientras el cambio está sin commitear—, y la
corrección reemplaza esa aserción por aserciones de contenido, por la regla de que el
bloque de metadatos es la última región del artefacto y por un digest normalizado del
contenido normativo del plan cerrado: la protección **se endurece** (cualquier edición
de una observación, una evidencia, un elemento inmutable o una sección normativa cambia
el digest y falla) y deja de depender del estado de Git. `<PLAN-140>:F-2` /
`<PLAN-140>:C-2`: el checkpoint del Plan 139 declaraba como árbol material del commit
de cierre un tree id distinto del real; el hecho de Git se registra en este artefacto
nuevo, sin modificar el plan cerrado y sin afectar la correspondencia R2 del estado de
cierre.

**Verificación.** Seis checkers canónicos PASS; `pytest tests/` **1010 passed, 0 failed**
(antes del Change: `1 failed, 1009 passed`); `pytest protocol/.agents/harness/tests/ -q`
**109 passed**; suites de SAE/Scope **57 passed**; C-1/C-2/C-3 sin `ANOMALY`. El
mecanismo EARS se verificó de forma read-only con el validador del payload sobre
especímenes con procedencia. **`ROADMAP.md`, `protocol/`, `runtime/`, `tools/`,
`.agents/`, RFCs, ADRs y los planes 116 y 138: 0 diff.**

**Fronteras respetadas.** No se creó ningún mecanismo, policy, checker, estado,
registry, authority class ni workflow; no se modificó `ROADMAP.md` ni ningún artefacto
protegido; no se reabrieron C-2/CI, Plan 121, R4, closure identity, los planes 116 y
138 ni el modelo de estado de cierre; no se convirtió ningún `DEFERRED` en `RESOLVED` y
no se inventó taxonomía para los asuntos no accionables. Sin push, sin merge, sin tag,
sin release y sin promotion.

## Nota de redacción

Plan redactado y ejecutado el 2026-09-20 sobre el baseline
`8727b60b2361ca03bc389fc6328d1b1788cc6911` (tree
`2bc144d76ffe2c17432638d1c1208525bc97f3f5`), working tree limpio. Este Plan **no**
crea mecanismos, estados, registries, checkers, workflows ni autoridad: reconcilia y
clasifica pendientes ya registrados reutilizando las reglas vigentes, y no modifica
`ROADMAP.md`, `protocol/`, `runtime/`, `tools/`, `.agents/`, RFCs, ADRs ni los planes
116 y 138.
