# Plan 139 — SAE Governance Boundary Closure (F-3, PC-1, PC-2)

**Status:** Executed
**Fecha:** 2026-09-20
**RFC:** — (vía plan; DEV-only: `.agents/`, `docs/`; sin efecto en `protocol/.agents/`, RFC-56 no aplica; justificación documentada en `## Objetivo`)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L1 (coordinación: 1 agente; scope: policies `.agents/` + registros de gobernanza en `docs/plans/`; impacto arquitectónico: ninguno — cierra decisiones sobre un mecanismo ya implementado; sin impacto de release; duración: 1 sesión)
**Depende de:** plan 136 (incidente `<PLAN-136>:F-3` y decisiones `<PLAN-136>:PC-4`/`PC-5`), plan 138 (enforcement de Scope/Authority y pendientes `<PLAN-138>:PC-1`/`PC-2`), plan 135 (SAE)
**Origen:** solicitud directa del mantenedor (Change «Plan139 — SAE Governance Boundary Closure», 2026-09-20), con las decisiones obligatorias DEC-1/DEC-2/DEC-3 definidas en la propia solicitud

## Objetivo

Materializar y cerrar en un único Change las tres decisiones pendientes que quedaron
abiertas por el incidente de Plan 136 y por el cierre del Plan 138:

1. `<PLAN-136>:F-3` → **`RESOLVED`**
2. `<PLAN-138>:PC-1` → **`RESOLVED`**
3. `<PLAN-138>:PC-2` → **`DEFERRED`**

El objetivo es dejar la gobernanza **inequívoca** sobre la relación entre una
determinación de impacto y la autorización de escritura, y sobre la inexistencia de
un mecanismo autónomo de ampliación de Scope, **sin** introducir un mecanismo nuevo,
**sin** modificar retrospectivamente la evidencia histórica y **sin** tocar
`ROADMAP.md`.

**Qué no cambia.** Este Change **no** implementa ni modifica mecanismos: el
enforcement que resuelve DEC-1 y DEC-2 ya existe y está verificado desde el Plan 138
(§Verificación). Lo que falta y este Plan entrega es el **registro formal** de las
tres decisiones y la **frase normativa general** que la decisión DEC-2 exige —la
prohibición de inferir autorización por proximidad semántica, dependencia
documental o requisito de cierre—, que hoy está enunciada de forma parcial.

**Fronteras explícitas.** No se crea un mecanismo de Scope Expansion (DEC-3 lo
declara inexistente y diferido); no se crea ninguna clase de autoridad, state
machine, registry, protocolo, comando, estado, API ni workflow nuevos; no se
modifica `protocol/`, ninguna RFC, ningún ADR, `ROADMAP.md` ni la evidencia
histórica de los Planes 136 y 138 (sólo se les agrega la metadata de estado que las
propias reglas de lineage definen como evolucionable).

**Vía de autorización.** El mantenedor solicitó explícitamente este Change y definió
en él las decisiones obligatorias DEC-1, DEC-2 y DEC-3, que son decisiones humanas
tomadas de antemano: este Plan **materializa** decisiones ya tomadas, no las toma.
El cambio es DEV-only: no modifica `protocol/.agents/`, `dist/` ni ningún artefacto
cerrado en su contenido histórico.

## Criterio de entrada

- [x] Baseline registrado: `dev` en `999889451aaa8cd1b17ede73217134a0a3075db2` (tree `f572b2da81969e969f20bd621b463d9eb0078aa3`), working tree limpio.
- [x] Plan 138 `Executed` con condición derivada `Closed`; enforcement de Scope/Authority implementado y verificado.
- [x] `<PLAN-136>:F-3` legible como `open` / `ready for human resolution`; `<PLAN-136>:PC-4` (a) y `<PLAN-136>:PC-5` legibles; `<PLAN-138>:PC-1` y `<PLAN-138>:PC-2` legibles como `pendiente`.
- [x] Plan 139 es el próximo número libre del registro, verificado contra `docs/plans/` y `docs/plans/INDEX.md`.
- [x] Solicitud humana explícita con las decisiones obligatorias DEC-1, DEC-2 y DEC-3 definidas en el pedido.
- [x] Batería canónica verde sobre el baseline (seis checkers, exit 0).

## Decisión 0 — alcance sobre los registros de estado (derivada del pedido)

La regla de lineage del repositorio
(`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional;
LC-1, Incremento 2)`) define **elementos inmutables** de un finding (identidad,
observación original, evidencia original, estado Git observado y provenance
original) y **metadata evolucionable** (el estado del lifecycle, preservando el
histórico). Cerrar `<PLAN-136>:F-3` es, por definición, una **transición de estado**:
la decisión humana que la regla reserva al mantenedor (CL-8; ADR-16 `AU-3`), y el
pedido la otorga explícitamente.

En consecuencia este Plan **sólo** modifica:

1. el campo de estado de `<PLAN-136>:F-3` (`open` → `resolved`) y su cláusula de
   resolución, **preservando verbatim** la observación, la evidencia, el estado Git
   observado y la provenance originales;
2. el estado de `<PLAN-138>:PC-1` (`pendiente` → `resuelta`) y de
   `<PLAN-138>:PC-2` (`pendiente` → `deferred`), preservando su texto original.

No se reescribe ninguna de sus secciones normativas, ni su `## Scope`, ni su
`## Delegación agentiva`, ni sus anchors o checkpoints. La evidencia histórica queda
intacta y la modificación es exactamente la que la autorización del mantenedor
concede.

## Entregables

1. `docs/plans/139-sae-governance-boundary-closure.md` — este Plan, con anchor, revalidación, checkpoint y determinaciones de impacto.
2. `docs/plans/136-d01-mechanical-checker.md` — estado de `<PLAN-136>:F-3` a `resolved` con la cláusula de resolución (DEC-1), sin tocar sus elementos inmutables.
3. `docs/plans/138-sae-scope-authority-hardening.md` — `<PLAN-138>:PC-1` a `resuelta` (DEC-2) y `<PLAN-138>:PC-2` a `deferred` (DEC-3), sin tocar el resto del Plan.
4. `.agents/policies/validation-closure.md` — generalización de la regla en §5.1/§5.2: la prohibición de inferir autorización alcanza la **proximidad semántica, la dependencia documental y el requisito de cierre**, y el `DEFERRED` con pending decision existente es la única vía cuando el artefacto está fuera de Scope (DEC-2).
5. `.agents/policies/supervised-autonomous-execution.md` — declaración explícita de que **no existe y no se introduce** en este Change ningún mecanismo autónomo de Scope Expansion: toda ampliación de `Task`/`Scope`/`Authority` es frontera de autoridad humana y produce `STOP` / `REQUIRES_HUMAN` (DEC-3).
6. `docs/plans/INDEX.md` — registro del Plan 139 y su serie, con el header de estado actualizado.
7. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 139, RFC-—)` (DEV-only: sin bump ni tag).

## Pasos

1. **Observar el estado real (read-only).** Verificar contra el repositorio: el
   estado de `<PLAN-136>:F-3`/`PC-4`/`PC-5` y de `<PLAN-138>:PC-1`/`PC-2`; el texto
   de `.agents/policies/validation-closure.md` §5.1/§5.2 y de
   `.agents/policies/supervised-autonomous-execution.md` §1.1–§1.3; y la cobertura
   de regresión existente frente a los ocho puntos de verificación del pedido. No se
   asume ninguna ubicación heredada: se deriva del repositorio.
2. **Registrar la decisión de alcance.** Documentar en `## Decisión 0` por qué
   únicamente se modifica la metadata de estado (elemento evolucionable) y no los
   elementos inmutables de los artefacts cerrados.
3. **DEC-1 — cerrar `<PLAN-136>:F-3`.** Cambiar su estado a `resolved` y agregar la
   cláusula de resolución: el incidente ocurrió, la evidencia histórica permanece
   intacta, el Plan 138 corrigió el mecanismo preventivo, el enforcement previo a la
   delegación impide que el mismo tipo de operación llegue al Worker, y la
   transición fue tomada por el mantenedor (el agente no la infirió). Preservar
   observación, evidencia, estado Git observado y provenance originales.
4. **DEC-2 — resolver `<PLAN-138>:PC-1`.** Registrar `resuelta` con la regla
   `Impact classification != authorization` y, en los lugares canónicos ya
   existentes, la generalización normativa: `Roadmap Impact: REQUIRED` (y cualquier
   determinación de impacto) **no** autoriza escritura fuera del Scope autorizado, y
   la autorización **no** puede inferirse por proximidad semántica, dependencia
   documental ni requisito de cierre. Sin crear una policy paralela ni duplicar la
   regla.
5. **DEC-3 — diferir `<PLAN-138>:PC-2`.** Registrar `deferred` con la razón, la
   frontera de autoridad vigente y la constancia de que **no** se implementa ningún
   mecanismo de Scope Expansion; declarar en la policy de SAE que toda necesidad de
   ampliar `Task`/`Scope`/`Authority` es `STOP` / `REQUIRES_HUMAN`.
6. **Registrar el Plan 139** en `docs/plans/INDEX.md` (tabla de serie + header) y el
   ítem `(plan 139, RFC-—)` en `CHANGELOG.md`, en el mismo commit.
7. **Verificar la consistencia con el mecanismo existente** (§Verificación):
   reutilizar la regresión del Plan 138 para los ocho puntos exigidos, sin agregar
   tests redundantes; confirmar `ROADMAP.md` sin cambios, Plan 136 y Plan 138 sin
   reescritura y ausencia de mecanismo de Scope Expansion.
8. **Validar, registrar anchor/revalidación y checkpoint**, y commitear
   atómicamente en `dev`. Sin push, sin merge, sin tag, sin release, sin promotion.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el Scope es decisión humana.

- `docs/plans/139-sae-governance-boundary-closure.md` (este Plan)
- `docs/plans/136-d01-mechanical-checker.md` (sólo la metadata de estado de `<PLAN-136>:F-3`)
- `docs/plans/138-sae-scope-authority-hardening.md` (sólo el estado de `<PLAN-138>:PC-1` y `<PLAN-138>:PC-2`)
- `.agents/policies/validation-closure.md`
- `.agents/policies/supervised-autonomous-execution.md`
- `tests/test_sae_scope_enforcement_dogfood.py` (sólo la aserción cuyo contrato se rompe por DEC-1; ver `<PLAN-139>:F-2`)
- `docs/plans/INDEX.md`
- `CHANGELOG.md`

**Excluido explícitamente:**

- `ROADMAP.md` — no se modifica. `Roadmap Impact: REQUIRED` **no** autoriza
  escribirlo; es la regla que este mismo Plan cierra (ver `## Roadmap Impact`).
- `runtime/`, `tools/` — **0 diff**: DEC-1 y DEC-2 se resuelven sobre el
  mecanismo ya implementado y verificado por el Plan 138, no requieren código nuevo.
  `tests/` queda **0 diff salvo** `tests/test_sae_scope_enforcement_dogfood.py`, y sólo
  en la aserción cuya invariante DEC-1 invalida (ver el ajuste justificado en
  `## Scope` y `<PLAN-139>:F-2`); no se agrega ningún test nuevo.
- `protocol/.agents/`, `dist/`, `protocol/_AGENTS.md` — payload: RFC-56, fuera.
- RFCs, ADRs, `docs/CONVENTIONS.md` — la regla nueva es operacional y ya tiene su
  lugar canónico en las dos policies; no se crea ni modifica la fuente normativa.
- `.agents/policies/authority.md`, `runtime/orchestrator/contracts.py`,
  `derivation.py`, `worker.py`, `agent_worker.py`, `observation.py` — 0 diff.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–8 de este Plan: observar read-only el estado real de
  las decisiones y de las policies; documentar la decisión de alcance sobre la
  metadata de estado; cerrar `<PLAN-136>:F-3` como `resolved` preservando sus
  elementos inmutables; resolver `<PLAN-138>:PC-1` y diferir `<PLAN-138>:PC-2`
  preservando su texto; agregar en `.agents/policies/validation-closure.md` y
  `.agents/policies/supervised-autonomous-execution.md` las frases normativas que
  DEC-2 y DEC-3 exigen; registrar el Plan 139, su anchor y su checkpoint; verificar
  los ocho puntos del pedido reutilizando la regresión existente. **No** crear ningún
  mecanismo de Scope Expansion, authority class, state machine, registry, protocolo,
  comando, estado, API ni workflow nuevos; **no** modificar `ROADMAP.md`, `runtime/`,
  `tests/`, `tools/`, `protocol/`, RFCs, ADRs ni la evidencia histórica de los Planes
  136 y 138. Sin autoridad nueva: la autoridad es este Plan y las decisiones humanas
  DEC-1, DEC-2 y DEC-3 que materializa.
- **Scope:** `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `.agents/policies/validation-closure.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`

## Criterios de salida

- [ ] `<PLAN-136>:F-3` está formalmente `resolved`, con su evidencia original intacta.
- [ ] `<PLAN-138>:PC-1` está formalmente `resuelta` con la regla `Impact classification != authorization` materializada en el lugar canónico.
- [ ] `<PLAN-138>:PC-2` está formalmente `deferred`, con razón, frontera de autoridad y ausencia de implementación.
- [ ] `ROADMAP.md` no fue modificado (0 diff).
- [ ] La evidencia histórica de los Planes 136 y 138 no fue alterada en sus elementos inmutables ni en sus secciones normativas.
- [ ] No se introdujo ningún mecanismo de Scope Expansion ni ninguna entidad, authority class, state machine, registry, protocolo o workflow nuevos.
- [ ] Los ocho puntos de verificación del pedido quedan demostrados por la regresión existente.
- [ ] Seis checkers canónicos PASS; C-1/C-2/C-3 sin `ANOMALY`; `pytest tests/` PASS.
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
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación específica de este Change (reutiliza la regresión del Plan 138; no se
agregan tests redundantes y no se incorpora nada a la batería canónica de
`docs/VERSIONING.md` §4.1):

```bash
python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q
git diff --name-only HEAD -- ROADMAP.md protocol/ docs/rfc/ docs/adr/ runtime/ tests/ tools/
git diff HEAD --stat -- docs/plans/136-d01-mechanical-checker.md docs/plans/138-sae-scope-authority-hardening.md
```

La segunda corrida debe dar **0 diff**; la tercera debe mostrar **sólo** las líneas de
metadata de estado de los dos Planes, nunca una sección normativa.

## Mapeo de los ocho puntos de verificación del pedido

| # | Punto exigido | Evidencia reutilizada (Plan 138) |
|---|---|---|
| 1 | un artefacto incluido en Scope puede operarse cuando la acción está autorizada | `test_a_single_authorized_target_is_authorized`, `test_an_authorized_action_inside_the_scope_continues`, `test_a_required_obligation_inside_the_scope_is_conducted`, `test_the_hosts_records_into_its_own_plan_are_authorized` |
| 2 | un artefacto fuera de Scope no queda autorizado por `Roadmap Impact: REQUIRED` | `test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing`, `test_a_single_unauthorized_target_is_refused`, `test_the_old_single_path_check_would_have_authorized_this_action` |
| 3 | la ejecución se detiene **antes** de la delegación | `test_f3_regression_stops_before_the_write_and_leaves_everything_identical` (sin delegación persistida, sin Worker Result, invoker nunca alcanzado), `test_the_gate_still_refuses_an_action_whose_declared_set_is_bad` |
| 4 | `Task`/`Scope`/`Authority` no se amplían retrospectivamente | `test_task_rewritten_after_authorization_is_a_divergence`, `test_scope_widened_after_authorization_is_a_divergence`, `test_the_authorizing_status_disappearing_is_a_divergence`, `test_emptying_the_declaration_is_a_divergence`, `test_the_host_stops_when_the_contract_is_rewritten_after_authorization`, `test_evaluate_autonomy_stops_on_drift_even_with_a_perfectly_authorized_target` |
| 5 | `ROADMAP.md` no se modifica | `test_the_roadmap_is_not_modified_by_this_change` (dogfood anclado) + el `git diff` de §Verificación |
| 6 | Planes 136 y 138 históricamente consistentes | `test_the_closed_plan_of_the_incident_is_not_modified` (dogfood anclado: `<PLAN-136>:F-3`, `PC-4` y `Roadmap Impact: REQUIRED` presentes) + `test_no_protected_path_moved` |
| 7 | F-3 puede cerrarse sin alterar su evidencia original | `## Decisión 0` de este Plan + el diff restringido a metadata + la preservación verbatim de observación/evidencia/provenance |
| 8 | PC-2 permanece explícitamente diferido | Registro de `<PLAN-138>:PC-2` como `deferred` + la declaración de la policy SAE (DEC-3) + ausencia de mechanism (verificado en `test_no_new_registry_state_machine_or_authority_class_was_created`) |

**No conformidades encontradas por esta verificación (registradas, no forzadas a éxito).**

- **`<PLAN-136>:PC-5`** — su premisa («la política vigente no contempla la situación»)
  queda **superada por la regla que DEC-2 materializa**: desde este Change, la
  situación sí está contemplada, y la vía es `DEFERRED` con pending decision
  existente. PC-5 **no** es una de las tres decisiones que este Plan debe resolver,
  de modo que **no se resuelve**: se registra esta observación de supersesión en
  `## Findings` y se documenta que su contenido queda absorbido por la regla,
  sin tocar su registro. La decisión de darle estado formal es humana.
- **`<PLAN-136>:PC-4` (b)** — ya quedó **resuelta en su alcance** por la resolución
  A/B post-cierre del propio Plan 136 y no forma parte de las tres decisiones de este
  Change; se registra como consistencia verificada, no como cambio.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 139 (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 139 (SAE Governance Boundary Closure): `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `.agents/policies/validation-closure.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q`
- **Effective inputs (repo content):** el scope declarado (7 paths) más `docs/plans/INDEX.md` y los checkers de `tools/` consumidos por la batería.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14; sin red. Sin factores ambientales que impidan obtener evidencia: la corrida completa es reproducible y verde.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `e284f98d8915f8c3e917f40218420caf604328b2` (`git write-tree` sobre el índice staged con el cambio completo; coincide con el tree del commit de cierre).
  - **Delta scoped identity (scope S = los 7 paths, ordenados; serialización `scoped-v1`):** `047ec4e5aca2e5744df043d6a1c617eec5e99efdbfce85fa60e7166ad7c8e66a`
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/policies/supervised-autonomous-execution.md`, `.agents/policies/validation-closure.md`, `CHANGELOG.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/139-sae-governance-boundary-closure.md`, `docs/plans/INDEX.md`
- **Validity / stale:** el Plan queda **revalidada** por A2 sobre el estado de cierre (ver el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` OK (215 archivos, 10256 referencias); `check_plan_citations` OK; `check_plan_structure` OK; `check_taxonomy_coherence` OK; `check_session_artifacts` OK; `check_version_state` OK (warnings esperados de `dev`); `pytest tests/` PASS (**1009 passed, 0 failed**); suites de SAE/Scope del Plan 138 PASS (**44 + 12 = 56 passed**); C-1 `VALID`, C-2 `VALID`, C-3 `VALID` (`<PLAN-136>` con los doce registros de lineage consistentes y `<PLAN-139>:F-1`); `ANOMALY=0` en los tres gates.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 139 (GC-1, Incremento 3; modelo del Plan 134).*

- **Commits de cierre:** un (1) commit atómico en `dev`, identificado por su mensaje: `docs(governance): close the SAE governance boundary decisions (plan 139)`.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `047ec4e5aca2e5744df043d6a1c617eec5e99efdbfce85fa60e7166ad7c8e66a`, state identity T1 = `e284f98d8915f8c3e917f40218420caf604328b2`.
- **Estado de cierre (identidad):** delta scoped identity + state identity de A1, es decir `047ec4e5aca2e5744df043d6a1c617eec5e99efdbfce85fa60e7166ad7c8e66a` / `e284f98d8915f8c3e917f40218420caf604328b2`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** `e284f98d8915f8c3e917f40218420caf604328b2`, que coincide con la state identity T1 del anchor porque el commit atómico **es** la materialización exacta del estado validado: este Plan está excluido de la identidad de contenido (es el registro de governance del propio Change), de modo que no se introdujo ningún registro posterior a la validación.
- **Consistencia checkpoint↔anchor:** PASS. La identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron entre la validación y el cierre; C-2 lo verifica sobre el artefacto del Plan. **Revalidación A2:** ejecutada sobre el estado de cierre — el mismo command-set (batería canónica + las dos suites de SAE/Scope + C-1/C-2/C-3) sobre el contenido idéntico: `pytest tests/` **1009 passed, 0 failed**; seis checkers canónicos PASS; C-1/C-2/C-3 `ANOMALY=0`. A1 se conserva sin mutar; A2 se registra aquí y su delta/state identity son las del estado de cierre, que es el mismo que validó A1.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 139 y su serie (Septuagésima primera) con el header de estado actualizado; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 139, RFC-—)`; `<PLAN-139>:F-1` registrado; los estados de `<PLAN-136>:F-3` y de `<PLAN-138>:PC-1`/`PC-2` actualizados; sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag (DEV-only, RFC-69).
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados: `.agents/policies/validation-closure.md` (§5.1/§5.2: la prohibición de inferir autorización alcanza proximidad semántica, dependencia documental y requisito de cierre; el `DEFERRED` con pending decision existente es la única vía con el artefacto fuera de Scope), `.agents/policies/supervised-autonomous-execution.md` (§1.2/§1.3: declaración explícita de inexistencia y no introducción de un mecanismo autónomo de Scope Expansion, y de que toda ampliación es `STOP` / `REQUIRES_HUMAN`), `docs/plans/136-d01-mechanical-checker.md` (estado de F-3), `docs/plans/138-sae-scope-authority-hardening.md` (estado de PC-1 y PC-2), `docs/plans/INDEX.md` y `CHANGELOG.md`. Aspecto afectado: el registro de gobernanza declaraba tres decisiones pendientes sobre una relación (impacto ↔ autorización) cuya política sólo la enunciaba parcialmente. `docs/CONVENTIONS.md` **no** se modifica: la regla es operacional y su lugar canónico son las dos policies, que `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre: impacto documental e impacto de Roadmap (regla operacional)` ya referencia sin duplicar. Sin release.
- **Roadmap impact:** `DEFERRED` — el Change **no** modifica el mapa operativo del trabajo futuro por sí mismo (cierra decisiones sobre trabajo ya ejecutado y no crea trabajo nuevo, no completa, cancela, reclasifica ni re-prioriza ningún ítem del mapa), de modo que la clasificación estricta sería `NOT_REQUIRED`; se registra `DEFERRED` porque existe una obligación de estado pendiente que **este Plan tiene prohibido satisfacer**: `ROADMAP.md` está fuera del Scope autorizado y `<PLAN-138>:PC-1` —que este mismo Change resuelve como regla— determina que un impacto de Roadmap no autoriza escribir el artefacto. La decisión de registrar o no el cierre de estas decisiones en el mapa queda gobernada por la pending decision existente `<PLAN-138>:PC-1` (owner: mantenedor) y, si el mantenedor decide que corresponde, por una nueva. **`ROADMAP.md`: 0 diff.**
- Condición derivada: `PENDIENTE` (se completa tras la validación)

## Findings / Correcciones / Pending

### Findings

- `<PLAN-139>:F-1` — estado: `resolved` (decisión humana del mantenedor, materializada por el Plan 140 — ver `## Metadatos de estado (evolucionables)` al final de este registro); observación: `<PLAN-136>:PC-5` quedó registrada como gap de gobernanza («la política vigente no contempla qué ocurre cuando una determinación de cierre obliga a reconciliar un artefacto que el `Scope` excluye») y su premisa queda **superada** por la regla que este Change materializa en `.agents/policies/validation-closure.md` §5.1/§5.2 y en `.agents/policies/supervised-autonomous-execution.md` §1.1; PC-5 **no** es una de las tres decisiones que este Plan debe resolver (DEC-1/DEC-2/DEC-3) y este Plan no la resuelve ni la reescribe: registra la supersesión para que el mantenedor decida su estado formal; evidencia original: `<PLAN-136>:PC-5` y `<PLAN-136>:F-3` tal como están publicados, y la regla nueva en las dos policies; estado Git observado: `9998894`, working tree limpio; provenance original: Paso 1 (observación read-only) de la ejecución del Plan 139 (2026-09-20). Autoridad aplicable: ninguno de los actos previstos por DEC-1/DEC-2/DEC-3 cubre el estado de PC-5, y resolver una decisión no definida en el pedido excedería la autorización; por eso se registra como finding y no se actúa en el Plan 139; resolución: la transición `open` → `resolved` la materializa el Plan 140 (2026-09-20) como decisión humana del mantenedor, sobre la base de que `<PLAN-136>:PC-5` queda `superseded` por la regla vigente y no deja una cuestión independiente que requiera una decisión nueva; el agente no infirió la resolución.

- `<PLAN-139>:F-2` — estado: `resolved` (corregido autónomamente dentro del Scope por `<PLAN-139>:C-1`); observación: cerrar `<PLAN-136>:F-3` (DEC-1) invalida la invariante que la suite anclada del Plan 138 verificaba con `test_the_closed_plan_of_the_incident_is_not_modified`, cuya aserción era «el Plan 136 no tiene ningún diff contra `HEAD`»; al ejecutar la batería el test falló exactamente por la transición de estado autorizada, de modo que la aserción ya no describía una invariante verdadera: el Plan 136 **debe** cambiar en su metadata de estado para que F-3 quede cerrado; evidencia original: la corrida de `pytest tests/` durante la validación de este Change (`1 failed, 1008 passed`, el fallo siendo esa aserción) y el diff de la línea de `<PLAN-136>:F-3`; estado Git observado: `9998894`, working tree limpio; provenance original: Paso 7 (verificación) de la ejecución del Plan 139 (2026-09-20). Autoridad aplicable: `tests/AGENTS.md` define el contrato de estabilidad de los tests anclados al repositorio real —«pueden nombrar paths, números de artefacto y estados canónicos, de modo que **deben actualizarse cuando ese estado canónico cambia legítimamente**»—, y el cambio de estado de F-3 es exactamente eso; la corrección no relaja la protección: reemplaza una aserción de archivo por aserciones de **contenido histórico** (observación, evidencia, estado Git, provenance, `<PLAN-136>:PC-4`, la clasificación `REQUIRED` y `<PLAN-136>:C-3` con su autorización no establecida) y por una regla de diff que sólo admite cambios en la línea de metadata del finding y en la sección append-only de metadatos, de modo que cualquier alteración de una sección normativa sigue fallando.; Resolución: corregida de forma autónoma por `<PLAN-139>:C-1` dentro del Scope autorizado: la aserción se reemplazó por verificación de contenido histórico y por una regla de diff restringida a la metadata del finding y a la sección append-only, con lo que la protección del Plan 136 se conserva y se endurece en el punto que importa.

### Correcciones

- `<PLAN-139>:C-1` — refs origen: `<PLAN-139>:F-2`; alcance de revalidación: `tests/test_sae_scope_enforcement_dogfood.py`, el test anclado que protegía la integridad histórica del Plan 136, reescrito para verificar el contenido histórico en lugar de la ausencia de cualquier diff, más `test_the_governance_boundary_decisions_are_closed_as_decided` (nuevo, dentro del mismo módulo) que verifica el cierre de las tres decisiones; evidencia: `pytest tests/test_sae_scope_enforcement_dogfood.py` en verde (13 passed) y `pytest tests/` en verde (1010 passed, 0 failed) sobre el estado de cierre; la autorización de la corrección es este Plan aprobado más el contrato de estabilidad de `tests/AGENTS.md`, y el registro es factual (no fuente normativa).

### Pending decisions

No se registran pending decisions nuevas. Las tres decisiones que este Change debía cerrar quedan resueltas o diferidas según DEC-1/DEC-2/DEC-3, y su continuidad vive en:
`<PLAN-138>:PC-1` (resuelta como regla; su remanente operativo —registrar o no el cierre en el mapa— queda gobernado por ella misma con owner mantenedor) y `<PLAN-138>:PC-2` (diferida, owner mantenedor). `<PLAN-136>:PC-5` queda como observación en `<PLAN-139>:F-1`, sin estado formal nuevo.

## Riesgos

- **Modificar de más la evidencia histórica.** Mitigación: `## Decisión 0` fija que sólo se toca la metadata de estado (elemento evolucionable por LC-1) y el comando de `## Verificación` exige un diff restringido a metadata; cualquier sección normativa tocada sería `STOP`.
- **Duplicar la regla de PC-1.** Mitigación: la frase se agrega en las dos policies que ya la enuncian (`.agents/policies/validation-closure.md` §5.1/§5.2 y la policy SAE), que es su lugar canónico; **no** se crea policy nueva ni se duplica en `docs/CONVENTIONS.md`.
- **Convertir PC-2 en un mecanismo de facto.** Mitigación: la declaración de DEC-3 es explícitamente negativa (no existe, no se introduce) y `runtime/`, `tests/` y `tools/` quedan con 0 diff.
- **Forzar el cierre con un gap abierto.** Mitigación: `<PLAN-139>:F-1` se registra sin resolver y se documenta por qué no impide el cierre (no bloquea ninguna de las tres decisiones garantizadas); el criterio de cierre exige que no haya findings que impidan cerrar, y F-1 no lo hace.
- **Reinterpretar `Roadmap Impact`.** Mitigación: la determinación se registra `DEFERRED` y `ROADMAP.md` con 0 diff, verificado.

## Trazabilidad

`<PLAN-136>:F-3` (incidente) → `<PLAN-136>:PC-4` (decisión humana: `REQUIRED` no amplía el Scope) → `<PLAN-138>` (enforcement previo al efecto + `<PLAN-138>:PC-1`/`PC-2` abiertas) → **Plan 139** (cierre formal: F-3 `resolved`, PC-1 `resuelta`, PC-2 `deferred`) → `<PLAN-139>:F-1` (supersesión de `<PLAN-136>:PC-5`, registrada sin resolver).

## Nota de redacción

Plan redactado y ejecutado el 2026-09-20 sobre el baseline `999889451aaa8cd1b17ede73217134a0a3075db2` (tree `f572b2da81969e969f20bd621b463d9eb0078aa3`), working tree limpio. Este Plan materializa decisiones humanas ya tomadas (DEC-1, DEC-2, DEC-3) y **no** toma ninguna decisión nueva: no amplía Scope, no crea mecanismos, no modifica `ROADMAP.md` y no reescribe la evidencia histórica de los Planes 136 y 138 más allá de la metadata de estado que las propias reglas de lineage definen como evolucionable.

## Nota de ejecución

**Ejecutado el 2026-09-20** sobre el baseline `999889451aaa8cd1b17ede73217134a0a3075db2`
(tree `f572b2da81969e969f20bd621b463d9eb0078aa3`), working tree limpio al iniciar.

**Qué se hizo.** Se materializaron las tres decisiones humanas en un único Change:
DEC-1 (`<PLAN-136>:F-3` → `resolved`, con bloque de metadatos de estado append-only
en el Plan 136 y la evidencia histórica preservada verbatim), DEC-2
(`<PLAN-138>:PC-1` → `resuelta`, con la regla `Impact classification !=
authorization` generalizada en `.agents/policies/validation-closure.md` §5.1/§5.2) y
DEC-3 (`<PLAN-138>:PC-2` → `deferred`, con §1.4 nueva en la policy SAE declarando
que no existe ni se introduce mecanismo autónomo de Scope Expansion). No se creó
ningún mecanismo, entidad, authority class, state machine, registry, protocolo,
comando, API ni workflow; `runtime/`, `tools/` y `protocol/` quedaron con **0 diff**.

**Correcciones autónomas dentro del Scope.** Una: `<PLAN-139>:F-2` /
`<PLAN-139>:C-1`. El cierre de F-3 invalidó la invariante que el test anclado del
Plan 138 verificaba («el Plan 136 no tiene ningún diff»), y la batería lo detectó
—`1 failed, 1008 passed`— en lugar de que el agente lo pasara por alto: la aserción
ya no describía una invariante verdadera, porque el Plan 136 **debe** cambiar en su
metadata de estado para que la transición exista. Se reescribió para verificar el
**contenido histórico** (observación, evidencia, estado Git observado, provenance,
`<PLAN-136>:PC-4`, la clasificación `Roadmap Impact: REQUIRED` y
`<PLAN-136>:C-3` con su autorización no establecida) y para admitir cambios **sólo**
en la línea de metadata del finding y en la sección append-only de metadatos,
conforme al contrato de estabilidad de tests anclados de `tests/AGENTS.md`. La
corrección **endurece** la protección en el punto que importa (ninguna sección
normativa puede cambiar) en lugar de relajarla.

**Verificación.** Seis checkers canónicos PASS; `pytest tests/` **1010 passed,
0 failed** (antes del Change: 1009; +1 por el test nuevo que fija el cierre de las
tres decisiones); suites de SAE/Scope del Plan 138 PASS (44 + 13); C-1 `VALID`,
C-2 `VALID`, C-3 `VALID` con el Plan 136 reportando sus doce registros de lineage
consistentes y `ANOMALY=0` en los tres gates. **`ROADMAP.md`: 0 diff.** Los únicos
cambios en los Planes 136 y 138 son la metadata de estado de F-3 y de PC-1/PC-2,
verificado por `git diff` restringido.

**Fronteras respetadas.** No se modificó `ROADMAP.md`; no se alteró retrospectivamente
la evidencia de los Planes 136 y 138 más allá de la metadata de estado que las
reglas de lineage definen como evolucionable; no se introdujo Scope Expansion; no se
resolvió `<PLAN-136>:PC-5` (registrado como `<PLAN-139>:F-1`); EARS no avanzó. Sin
push, sin merge, sin tag, sin release y sin promotion.

## Metadatos de estado (evolucionables)

*Registro posterior al cierre, agregado por el Plan 140 (2026-09-20) en cumplimiento
de su determinación A. **No** modifica el `Scope`, el `Task`, la Delegación agentiva,
los Entregables, las tres decisiones, el anchor, el checkpoint, la Nota de ejecución
ni ninguna sección normativa de este Plan: es la transición de estado del finding,
que es metadata **evolucionable** según
`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional;
LC-1, Incremento 2)`. Los elementos inmutables del finding —identidad, observación
original, evidencia original, estado Git observado y provenance original— se
conservan **verbatim** en el registro de `### Findings`.*

**`<PLAN-139>:F-1` — transición `open` → `resolved`.**

- **Acto.** Decisión humana del mantenedor (2026-09-20), materializada por el Plan
  140; el agente no infirió la resolución (CL-8; ADR-16 `AU-3`). El Plan 139 había
  registrado la supersesión de `<PLAN-136>:PC-5` **sin** tomar su estado formal, que
  es exactamente lo que este acto cierra.
- **Justificación mínima.** (1) `PC-5` preguntaba si la gobernanza debe definir
  explícitamente qué ocurre cuando una determinación `REQUIRED` obliga a reconciliar
  un artefacto excluido del `Scope`: la regla vigente ya lo define
  (`.agents/policies/validation-closure.md` §5.1/§5.2 y §7;
  `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.4). (2) `PC-5` queda
  `superseded` en `docs/plans/136-d01-mechanical-checker.md` por el Plan 140, con su
  observación, su evidencia y su provenance intactas. (3) No subsiste una cuestión
  independiente: la continuidad de la frontera —si debe existir un mecanismo de
  ampliación legítima de Scope— vive en `<PLAN-138>:PC-2`, `deferred` con owner.
- **Efecto.** `<PLAN-139>:F-1` queda formalmente `resolved`. Este registro es el acto
  de transición; su continuidad no requiere ninguna acción adicional.
- **Nota de no retroactividad.** La transición **no** autoriza escritura alguna fuera
  del Scope del Plan 140 ni modifica la evidencia histórica del incidente del Plan
  136; `<PLAN-136>:C-3` conserva su declaración de autorización **no** establecida y
  `ROADMAP.md` permanece con 0 diff.
