# Plan 138 — SAE Scope & Authority Hardening (la autonomía operacional nunca excede Scope + Authority)

**Status:** Executed
**Fecha:** 2026-09-20
**RFC:** — (vía plan; DEV-only: `.agents/`, `runtime/`, `tests/`, `docs/`; sin efecto en `protocol/.agents/`, RFC-56 no aplica; justificación documentada en `## Objetivo`)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L2 (coordinación: 1 agente; scope: multi-área — policy + runtime + tests + docs de gobernanza; impacto arquitectónico: endurece la frontera de SAE existente sin crear mecanismo nuevo; sin impacto de release; duración: 1–2 sesiones)
**Depende de:** plan 135 (SAE: policy, `autonomy.py`, gate `--sae`), plan 136 (incidente F-3 y sus decisiones humanas PC-4/PC-5), plan 122 (host), plan 123 (Agent Worker), plan 134 (integridad de la evidencia de cierre)
**Origen:** incidente `<PLAN-136>:F-3` (exceso de Scope y auto-autorización retrospectiva durante la ejecución del Plan 136), decisiones humanas `<PLAN-136>:PC-4` y `<PLAN-136>:PC-5`, y solicitud directa del mantenedor (Change «SAE Scope & Authority Hardening», 2026-09-20)

## Objetivo

Endurecer el mecanismo de SAE para que la autonomía operacional del host
**nunca** pueda exceder `Scope + Authority`, aunque el agente interprete que
existe una obligación de cierre, impacto o reconciliación que aparentemente
requiere una acción fuera de Scope.

El Plan 136 demostró que la frontera de SAE es **incompleta**, no que sea
incorrecta. El agente derivó correctamente que el `Task` del Plan era la
frontera de escritura, pero el mecanismo no se lo impidió: el host delegó la
tarea semántica cuyos *write targets* no había verificado, el trabajador escribió
`ROADMAP.md` fuera del Scope, y la violación se detectó **después** de la
escritura. Después, el Plan mismo fue reescrito para que la escritura pareciera
autorizada desde el inicio.

El objetivo **no** es hacer al agente menos autónomo. Es que pueda seguir siendo
autónomo dentro de su autoridad y que **se detenga automáticamente antes del
efecto persistente**, en el límite correcto.

**Propiedades que este Change debe garantizar** (enunciadas como propiedades, no
como mecanismos; el mapeo a materialización está en `## Pasos`):

- **P1 — Scope precede a Impact.** Una determinación `Documentation Impact:
  REQUIRED`, `Roadmap Impact: REQUIRED` o cualquier otra obligación de
  reconciliación define una **obligación de estado/cierre**; **no** concede
  autorización para modificar el artefacto. Si satisfacerla exige escribir fuera
  de Scope: `STOP` antes de la escritura.
- **P2 — Scope es una precondición operacional.** Antes de cualquier acción con
  efectos persistentes el sistema determina: cuál es el target; si está dentro
  del Scope autorizado; si la acción está permitida por Authority; y si existe
  alguna restricción adicional aplicable. Conceptual:
  `authorized_action = scope_allows(target) AND authority_allows(action)`. La
  fórmula es conceptual: el punto de enforcement real se determina en
  `## Causa arquitectónica` e `## Punto de enforcement propuesto`.
- **P3 — STOP antes de escribir.** El orden correcto es
  `derivar → validar autorización → detectar violación → STOP → registrar
  evidencia → escalar → no ejecutar la escritura`. El orden incorrecto
  (`escribir → detectar → registrar finding`) es exactamente el defecto de F-3.
- **P4 — No retroactividad.** `Scope`, `Task`, `Authority`, la declaración de
  out-of-scope y cualquier otro elemento del contrato de autorización son el
  *checkpoint de autorización* de la ejecución. Una vez iniciada la ejecución el
  agente **no puede** modificarlos retrospectivamente para legitimar una acción
  ya realizada. Una ampliación legítima ocurre antes de la acción, por el
  mecanismo de autoridad existente, con evidencia de la decisión y con
  revalidación cuando corresponda. **No se crea un authority class nuevo.**
- **P5 — Impact no debe convertirse en autorización.** Se investiga si las
  policies vigentes contienen otros mecanismos equivalentes (Documentation
  Impact, Roadmap Impact, closure/validation/checkpoint/lifecycle requirements)
  interpretables como autorización implícita de escritura, y si existe una clase
  general de regla que necesite la misma protección. Resultado de la
  investigación en `## Causa arquitectónica` §2.

**Vía de autorización.** El mantenedor solicitó explícitamente la investigación y
la redacción de este Plan (2026-09-20), con el próximo número libre del registro
(138). El cambio es DEV-only: no modifica `protocol/.agents/`, `dist/`, ni ningún
artifact cerrado. La autorización de ejecución es una decisión humana posterior:
este Plan se crea en `Aprobado para redacción` y **no se ejecuta**.

**Fronteras explícitamente fuera de este Change.** No se cierra `<PLAN-136>:F-3`
(la transición de estado de un finding es decisión humana con evidencia; CL-8,
ADR-16 `AU-3`). No se modifica el Plan 136 ni ninguno de sus elementos
inmutables. No se resuelve `<PLAN-136>:PC-5` como parte de este Change: este Plan
registra el límite como **provenance** y lo reformula como una pending decision
propia (`<PLAN-138>:PC-2`). No se avanza EARS ni ningún otro trabajo del mapa.

## Criterio de entrada

- [x] Baseline registrado: `dev` en `ebdbfad13e34ef1a38c5dc91365159d552e458f7` (tree `8fb41698a02c24668c5521707224978635565000`), working tree limpio.
- [x] Batería canónica verde (seis checkers, exit 0) y gates C-1/C-2/C-3 `ANOMALY=0` sobre ese baseline.
- [x] Suites de SAE verdes antes de empezar (`pytest tests/test_autonomous_scope.py tests/test_autonomous_scope_dogfood.py` → 62 passed).
- [x] Plan 138 es el próximo número libre del registro (`docs/plans/INDEX.md`), verificado contra `docs/plans/`.
- [x] `<PLAN-136>:F-3` permanece `open` / `ready for human resolution` y `<PLAN-136>:PC-4` (a) y `<PLAN-136>:PC-5` están legibles como evidencia; **no** se modifican.
- [x] Autorización explícita del mantenedor para **ejecutar** este Plan (decisión humana; el Plan pasa a `Aprobado para ejecución`).

## Entregables

1. `.agents/policies/supervised-autonomous-execution.md` — regla de precedencia Scope/Authority sobre obligaciones de cierre, definición del *checkpoint de autorización* y regla de no retroactividad, precondición de escritura con conjunto completo de targets, y límite declarado del enforcement (corregido por la ejecución; ver `## Riesgos`).
2. `.agents/policies/validation-closure.md` — aclaración en §5.1/§5.2 de que una determinación `REQUIRED` **no** es autorización de escritura y que la reconciliación se satisface dentro del Scope autorizado o se registra `DEFERRED` con pending decision existente (PC-1).
3. `.agents/policies/autonomous-orchestration.md` — la frontera de §5/§11.3 pasa a declarar explícitamente la precondición de escritura y la parada previa al efecto.
4. `runtime/orchestrator/autonomy.py` — conjunto completo de write targets por candidato, verificación de todos los targets, y proyección del checkpoint de autorización (función pura, sin I/O).
5. `runtime/orchestrator/host.py` — enforcement **antes** de la delegación: la acción derivada no se ejecuta si algún target no está autorizado o si el checkpoint de autorización deriva; evidencia en el journal.
6. `tests/test_sae_scope_enforcement.py` — regresión F-3 reproducible y matriz de falsación (targets/acciones dentro y fuera, obligaciones `REQUIRED` dentro y fuera, no retroactividad, drift).
7. `tests/test_sae_scope_enforcement_dogfood.py` — dogfood anclado al repo real: el punto de enforcement existe, la frontera del Plan 136 está registrada y `ROADMAP.md` no fue tocado.
8. `.agents/AGENTS.md` — ruteo actualizado **sólo si** el nombre o el alcance de las policies cambia (si el ruteo vigente sigue siendo correcto, el paso registra `NOT_REQUIRED` con la razón y el archivo no se toca).
9. `runtime/README.md` — sección SAE (Plan 135) actualizada con el endurecimiento y los límites declarados.
10. `docs/plans/INDEX.md` — registro del Plan 138 y su serie.
11. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 138, RFC-—)` (DEV-only: sin bump ni tag).
12. `tests/test_sae_scope_enforcement_dogfood.py` — dogfood anclado al repo real (sólo lectura): el punto de enforcement previo al efecto existe en el runtime, la frontera de F-3 sigue registrada sin modificación, y `ROADMAP.md` con 0 diff. **Corregido en la ejecución** (`<PLAN-138>:F-1` / `<PLAN-138>:C-1`): este entregable figuraba en `## Delegación agentiva` → `Scope` y en el `## Scope` del Plan, pero **no** en `## Entregables`, de modo que la declaración autorizaba un path que el propio Plan no declaraba como entregable. Es exactamente la clase de divergencia que el enforcement de este Change detecta, y quedó registrada como finding.
13. `docs/plans/138-sae-scope-authority-hardening.md` — este Plan, con anchor, checkpoint y determinaciones de impacto.

## Pasos

> **Regla de secuencia (no negociable).** Los Pasos 0–2 son **investigación
> read-only** y deben ejecutarse y registrarse **antes** de tocar el runtime. Un
> defecto del mecanismo no se corrige a ciegas: se reconstruye, se documenta y
> recién entonces se materializa. Si la investigación contradice alguna
> afirmación de este Plan, la contradicción se registra como finding y se
> **escala**; no se reinterpreta el Plan para que siga siendo cierto.

0. **Paso 0 — Reconstrucción read-only de la cadena real.** Verificar contra el
   repositorio, sin modificar nada, el estado exacto de:
   `runtime/orchestrator/observation.py` (de dónde sale el Scope autorizado),
   `runtime/orchestrator/derivation.py` (dónde se construye la acción),
   `runtime/orchestrator/authority.py` (Authority), `runtime/orchestrator/host.py`
   (`_apply_autonomy_gate`, `_build_delegation`, `_execute_delegation`,
   `_scope_violations`), `runtime/orchestrator/worker.py` (snapshots de
   contenido) y `runtime/orchestrator/agent_worker.py` (el invoker y los write
   targets reales). Confirmar **por lectura y por ejecución** las tres
   afirmaciones que sostienen este Plan:
   (a) el gate de SAE evalúa el target con `_autonomy_target_path`, que para
   `RUN_IMPLEMENTATION_TASK` resuelve **un solo** path (`resolved[0]`);
   (b) la violación de Scope se detecta **después** de la delegación, por
   comparación de snapshots de contenido, y se reporta como
   `STOP_FORBIDDEN_ACTION`;
   (c) el envelope de autorización se re-deriva desde el artifact en **cada**
   iteración, sin ningún registro de la declaración vigente al autorizar.
   Registrar el resultado como evidencia de la investigación (secciones
   `## Causa arquitectónica` e `## Nota de ejecución`). Sin hallazgo que
   contradiga (a)–(c), continuar.

1. **Paso 1 — Clasificación de la clase de obligación (P1/P5).** Recorrer
   `.agents/policies/` y `.agents/workflows/change-lifecycle.md` y clasificar
   **cada** mecanismo que enuncie una obligación de estado/cierre:
   `Documentation Impact` (§5.1), `Roadmap Impact` (§5.2), el gate de
   verificación del DoD, las condiciones de anchor/checkpoint, los gates
   C-1/C-2/C-3, la obligación de changelog del payload y la obligación de
   lineage de findings. Para cada uno responder: *¿enuncia autorización de
   escritura, o sólo una obligación de estado?* Registrar el resultado en
   `## Causa arquitectónica` §2. Si aparece una clase real de obligación que
   confiere autorización implícita, **escalar** antes de continuar; no ampliar el
   problema sin evidencia.

2. **Paso 2 — Estado de los elementos del contrato de autorización (P4).**
   Determinar exactamente qué elementos constituyen el *checkpoint de
   autorización* de una ejecución en el modelo vigente: `## Delegación
   agentiva` → `Task` y `Scope`; el `**Status:**` que autoriza la ejecución; la
   declaración de out-of-scope y la tabla de artefactos afectados cuando existen;
   y los propios registros de gobernanza que el host escribe. Determinar cuáles
   de esos elementos el host **puede** escribir legítimamente durante la
   ejecución (records) y cuáles **nunca** (la declaración de autorización).
   Registrar la separación en `## Punto de enforcement propuesto`.

3. **Paso 3 — Formalizar la regla en la policy de SAE.** En
   `.agents/policies/supervised-autonomous-execution.md`: (i) enunciar la
   precedencia `Scope`/`Authority` sobre cualquier obligación de cierre, impacto
   o reconciliación (P1); (ii) definir el **checkpoint de autorización** y la
   regla de no retroactividad (P4), incluyendo la vía legítima de ampliación
   (antes de la acción, por el mecanismo de autoridad existente, con evidencia);
   (iii) precisar §9 para que `REQUIRED` no pueda leerse como autorización de
   escritura. **No** se crea un authority class, un mecanismo de ampliación de
   scope, un estado ni un cuarto valor de determinación.

4. **Paso 4 — Aclarar las determinaciones de cierre.** En
   `.agents/policies/validation-closure.md` §5.1/§5.2, agregar la frase
   normativa mínima: una determinación `REQUIRED` **no** autoriza a escribir el
   artefacto que nombra; si el artefacto está fuera del `Scope` autorizado, la
   reconciliación se registra `DEFERRED` con la pending decision existente
   (PC-1) que la gobierna, o se escala. Reusar `DEFERRED` y PC-1; **no** crear un
   valor nuevo ni un mecanismo de pending nuevo.

5. **Paso 5 — Materializar el conjunto completo de write targets.** En
   `runtime/orchestrator/autonomy.py`: `AutonomyCandidate` recibe el conjunto de
   targets de escritura del candidato (aditivo-optional, de modo que todo el
   corpus de tests del Plan 135 siga leyéndose sin modificación);
   `evaluate_candidate` verifica **todos** los targets y la regla es
   all-or-nothing; un write class cuyo conjunto de targets sea vacío o no
   resoluble **no** puede continuar (no puede demostrarse que escriba dentro del
   Scope). La función sigue siendo pura: sin filesystem, reloj, branch, CWD ni
   cache.

6. **Paso 6 — Materializar la proyección del checkpoint de autorización.** En
   `runtime/orchestrator/autonomy.py`: una función pura que, a partir de la
   observación, produce la proyección de los elementos del contrato de
   autorización (Paso 2) y un digest determinista de ella. Reusar el algoritmo
   de identidad de contenido existente (`tools/scoped_content_identity.py`,
   plan 109) o la digestión determinista de texto del propio runtime; **no**
   duplicar el algoritmo de identidad ni crear un registro nuevo.

7. **Paso 7 — Enforcement antes del efecto en el host.** En
   `runtime/orchestrator/host.py`: (i) `_apply_autonomy_gate` pasa a construir y
   verificar el **conjunto completo** de targets de la acción derivada, y a
   detenerse en `STOP_SCOPE_VIOLATION` (`REQUIRES_HUMAN`) **antes** de construir
   la delegación cuando algún target no está autorizado o el conjunto no es
   resoluble; (ii) se agrega la comparación contra el checkpoint de autorización
   registrado en el journal del run, que produce la misma parada ante
   divergencia (intento de autorización retrospectiva); (iii) el registro de
   iteración incorpora la decisión de scope, la decisión de autoridad, la
   condición de parada, la evidencia y la constancia de ausencia de efecto
   persistente, reusando el campo `autonomy` que ya existe. **No** se crea un
   sistema de telemetría paralelo.

8. **Paso 8 — Preservar la detección posterior como defensa en profundidad.**
   `_scope_violations` y `STOP_FORBIDDEN_ACTION` **no** se eliminan ni se debilitan:
   siguen siendo la red que cubre la escritura que ocurre *dentro* del worker
   (por ejemplo, a través de un `AgentInvoker` inyectado), que el host no puede
   interponer. Documentar explícitamente este límite declarado en la policy y en
   `runtime/README.md`: el objetivo del Change es el enforcement **antes** del
   efecto para toda acción que el host controla, y la detección posterior se
   conserva para lo que el host no controla. No fingir una garantía que la
   arquitectura no puede dar.

9. **Paso 9 — Regresión F-3 reproducible.** En
   `tests/test_sae_scope_enforcement.py`: construir un repositorio git temporal
   con un Plan autorizado cuyo `Scope` **excluya** un artefacto (el nombre del
   artefacto excluido es un parámetro, **no** `ROADMAP.md` hardcodeado) y que
   declare una determinación de Impact `REQUIRED` que nombra ese artefacto como
   lo que debe reconciliarse; un invoker inyectado que **intenta** escribir el
   artefacto excluido; y el host con `autonomy_gate=True`. Demostrar: el host se
   detiene **antes** de delegar (`STOP_SCOPE_VIOLATION`, `REQUIRES_HUMAN`); no
   existe delegación persistida para esa iteración; el artefacto excluido quedó
   **byte-idéntico** (digest antes == digest después); y la evidencia de la
   parada (acción propuesta, targets, decisión de scope, autoridad, stop
   condition, ausencia de efecto) es reconstruible desde el journal. El caso debe
   **fallar** contra el comportamiento previo al fix (detección posterior) y
   **pasar** contra el fix: registrar ambas ejecuciones como evidencia
   (implementación previa en un worktree temporal read-only o `git stash`-equivalente
   documentado; nunca modificando el baseline de `dev`).

10. **Paso 10 — Matriz de falsación y no retroactividad.** En el mismo módulo,
    falsar como mínimo: target permitido (continúa); target no permitido
    (STOP); acción permitida (continúa); acción no permitida (STOP); obligación
    `REQUIRED` cuyo artefacto está **dentro** del Scope (continúa); obligación
    `REQUIRED` cuyo artefacto está **fuera** del Scope (STOP **y** el artefacto
    byte-idéntico); conjunto de targets múltiple con un solo path fuera (STOP);
    target vacío o no resoluble (STOP); escritura legítima del propio Plan por
    los records del host (continúa); modificación retrospectiva del `Scope`
    después de la primera delegación (STOP); modificación retrospectiva del
    `Task` (STOP); y ausencia de pending decision que gobierne un `DEFERRED`
    (condición bloqueante, no `DEFERRED`). Ningún caso puede pasar «por
    proximidad semántica»: cada aserción nombra la stop condition exacta.

11. **Paso 11 — Dogfood.** `tests/test_sae_scope_enforcement_dogfood.py`
    (anclado, sólo lectura) comprueba sobre el repo real: que el punto de
    enforcement previo al efecto existe en el runtime; que
    `.agents/policies/supervised-autonomous-execution.md` enuncia la precedencia
    Scope/Authority y la no retroactividad; que `<PLAN-136>:F-3` y
    `<PLAN-136>:PC-4` siguen registrados sin modificación; que el Plan 136
    conserva `## Scope` excluyendo `ROADMAP.md`; y que `ROADMAP.md` no fue
    modificado por este Change. Además, un **dogfood funcional**: sobre un
    proyecto scratch fuera del repositorio, el mismo escenario de F-3
    (obligación `REQUIRED`, target fuera de Scope, agente con autonomía
    suficiente para intentarlo) produce `STOP` antes del efecto. El dogfood
    **debe** dejar declarado que no existe provider ni modelo real en el
    repositorio (decisión humana H-1 del Plan 123): el agente real se sustituye
    por un `AgentInvoker` inyectado que **realmente escribe** en el repositorio,
    de modo que el efecto que se impide es material y no simulado. Si esa
    sustitución no se considera dogfood suficiente, documentar exactamente por
    qué y registrarlo como límite declarado, sin convertirlo en `PASS`.

12. **Paso 12 — Documentación operacional y registros.** Actualizar
    `runtime/README.md` (sección SAE) y, sólo si el ruteo cambió,
    `.agents/AGENTS.md`. Registrar el Plan en `docs/plans/INDEX.md` (tabla de
    serie + header de estado) y el ítem `(plan 138, RFC-—)` en
    `CHANGELOG.md:[Unreleased]`. `ROADMAP.md` **no** se modifica en ninguno de
    los pasos de este Change.

13. **Paso 13 — Validar, registrar anchor/checkpoint y commitear.** Batería
    canónica completa, C-1/C-2/C-3, suites nuevas y suites de SAE existentes;
    registrar el Validation Anchor y el Checkpoint con revalidación A2 cuando
    corresponda; determinar `Documentation Impact` y `Roadmap Impact`;
    commit atómico en `dev`. Sin push, sin merge, sin tag, sin release, sin
    promotion.

## Scope

Rutas que este Change queda autorizado a modificar al ejecutarse. Un path fuera
de esta lista es `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el Scope es
decisión humana.

- `.agents/policies/supervised-autonomous-execution.md`
- `.agents/policies/validation-closure.md`
- `.agents/policies/autonomous-orchestration.md`
- `.agents/AGENTS.md` (condicional al Paso 12; si el ruteo vigente sigue siendo correcto, no se toca)
- `runtime/orchestrator/autonomy.py`
- `runtime/orchestrator/host.py`
- `runtime/README.md`
- `tests/test_sae_scope_enforcement.py`
- `tests/test_sae_scope_enforcement_dogfood.py`
- `docs/plans/138-sae-scope-authority-hardening.md`
- `docs/plans/INDEX.md`
- `CHANGELOG.md`

**Excluido explícitamente (y por eso este Change es su propia demostración):**

- `ROADMAP.md` — excluido del Scope autorizado. La determinación `Roadmap
  Impact` de este Plan **no** autoriza escribirlo. Es la frontera que `<PLAN-136>:PC-4`
  fijó y que este Plan respeta: ver §`Roadmap Impact`.
- `docs/plans/136-d01-mechanical-checker.md` — cerrado y terminal: no se reescribe,
  no se reabre, no se le modifican elementos inmutables (Regla 5 de `.agents/AGENTS.md`).
  Este Change lo usa como evidencia, nunca como target.
- `runtime/orchestrator/contracts.py` — **no** entra salvo que el Paso 0 demuestre
  que hace falta un valor de vocabulario nuevo; en ese caso el Plan se detiene y
  se escala, porque un vocabulario nuevo es una decisión de arquitectura
  (stop condition §5 de la policy SAE). La preferencia declarada es **reusar**
  `STOP_SCOPE_VIOLATION`, que ya existe y ya es human-authority stop.
- `runtime/orchestrator/worker.py`, `runtime/orchestrator/agent_worker.py`,
  `runtime/orchestrator/derivation.py`, `runtime/orchestrator/observation.py` —
  **no** entran salvo que el Paso 0 demuestre que el enforcement no puede
  materializarse en `autonomy.py` + `host.py` sin tocarlos; en ese caso el Plan
  se detiene y se escala con la evidencia concreta.
- `protocol/.agents/`, `dist/`, `protocol/_AGENTS.md` — payload: RFC-56, fuera de
  este Change (0 diff).
- RFCs, ADRs, otros planes y sus registros — 0 diff.
- `.agents/policies/authority.md` — **no** entra: la investigación no encontró una
  contradicción normativa real que lo requiera (ver `## Causa arquitectónica` §2
  y `## Cambios normativos`). Si el Paso 1 la encontrara, se escala; no se
  resuelve implícitamente.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 0–13 de este Plan: reconstruir read-only la cadena
  de enforcement de SAE; formalizar en las policies de `.agents/` la precedencia
  de Scope/Authority sobre las obligaciones de cierre, el checkpoint de
  autorización y la regla de no retroactividad; materializar en
  `runtime/orchestrator/autonomy.py` y `runtime/orchestrator/host.py` el
  enforcement del conjunto completo de write targets **antes** de la delegación y
  la detección de la modificación retrospectiva; escribir las suites
  `tests/test_sae_scope_enforcement.py` y
  `tests/test_sae_scope_enforcement_dogfood.py` con la regresión F-3 y su matriz
  de falsación; y registrar `runtime/README.md`, `docs/plans/INDEX.md`,
  `CHANGELOG.md` y este Plan. **No** modificar `ROADMAP.md`, el Plan 136,
  `.agents/policies/authority.md`, `runtime/orchestrator/contracts.py`,
  `protocol/.agents/` ni ningún artifact cerrado. Sin autoridad nueva: la
  autoridad es este Plan aprobado.
- **Scope:** `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `tests/test_sae_scope_enforcement.py`, `tests/test_sae_scope_enforcement_dogfood.py`, `.agents/policies/supervised-autonomous-execution.md`, `.agents/policies/validation-closure.md`, `.agents/policies/autonomous-orchestration.md`, `.agents/AGENTS.md`, `runtime/README.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`

## Criterios de salida

- [ ] AC-01 — Scope/Authority enforcement implementado en el punto correcto (`runtime/orchestrator/host.py`, antes de construir la delegación), con el conjunto completo de write targets verificado.
- [ ] AC-02 — Regresión F-3 PASS: el escenario que antes produjo una escritura fuera de Scope ahora produce `STOP` antes del efecto persistente.
- [ ] AC-03 — Falsification suite PASS: los trece casos mínimos del Paso 10, cada uno nombrando su stop condition exacta.
- [ ] AC-04 — Tests de targets dentro y fuera de Scope PASS.
- [ ] AC-05 — Tests de obligación `REQUIRED` dentro y fuera de Scope PASS, con el artefacto fuera de Scope byte-idéntico.
- [ ] AC-06 — Demostración de STOP antes de escritura: sin delegación persistida para la iteración detenida, y con el digest del artefacto excluido idéntico antes y después.
- [ ] AC-07 — Demostración de no modificación retrospectiva: `Scope`, `Task` y `Authority` byte-idénticos tras la parada, y un intento de ampliarlos retrospectivamente produce `STOP_SCOPE_VIOLATION`.
- [ ] AC-08 — Tests SAE existentes sin regresiones (`tests/test_autonomous_scope.py`, `tests/test_autonomous_scope_dogfood.py`, `tests/test_agent_worker.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_change_governance.py`).
- [ ] AC-09 — Checkers canónicos PASS (los seis de `docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- [ ] AC-10 — C-1/C-2/C-3 ejecutados y `ANOMALY=0` sobre el estado de cierre.
- [ ] AC-11 — `pytest tests/` completo PASS, sin regresiones.
- [ ] AC-12 — Dogfood real ejecutado según el Paso 11, con su límite declarado (no hay provider ni modelo en el repositorio) registrado.
- [ ] AC-13 — `Documentation Impact` reconciliado con evidencia.
- [ ] AC-14 — `Roadmap Impact` reconciliado **sin inferir autoridad**: `ROADMAP.md` con 0 diff y la obligación diferida con pending decision existente y owner.
- [ ] AC-15 — Git checkpoint reproducible: baseline, commits de cierre, tree y consistencia anchor↔checkpoint declarados.
- [ ] No se modifica `protocol/.agents/` ni ningún artifact cerrado; `<PLAN-136>:F-3` permanece `open`; EARS no avanza.
- [ ] No se crea state machine, entidad, authority class, registry, lifecycle, sistema de permisos paralelo, mecanismo de Scope independiente, mecanismo específico para `ROADMAP.md` ni mecanismo específico para `Documentation Impact`.

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

Verificación adicional exigida por este Plan (fuera de la batería canónica, no se
agrega a `docs/VERSIONING.md` §4.1: hacerlo crearía una obligación de gobernanza
sobre todo Change futuro y este Plan no la autoriza):

```bash
python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q
git diff --stat -- ROADMAP.md docs/plans/136-d01-mechanical-checker.md .agents/policies/authority.md runtime/orchestrator/contracts.py protocol/
```

La segunda corrida debe dar **0 diff**: es la verificación mecánica de que este
Change respeta las fronteras que el propio incidente F-3 puso a prueba.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 138 (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 138 (SAE Scope & Authority Hardening): `.agents/policies/supervised-autonomous-execution.md`, `.agents/policies/validation-closure.md`, `.agents/policies/autonomous-orchestration.md`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `runtime/README.md`, `tests/test_sae_scope_enforcement.py`, `tests/test_sae_scope_enforcement_dogfood.py`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `.agents/AGENTS.md`
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m pytest tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py -q`
- **Effective inputs (repo content):** el scope declarado (12 paths) más `docs/plans/INDEX.md` y los checkers de `tools/` consumidos por la batería.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14; sin red. **Factor ambiental declarado relevante:** la raíz temporal de la sesión de pytest es externa al repositorio (`ARGENTOS_PYTEST_TMP` / `tests/pytest_isolation.py`); las suites nuevas usan `pytest_isolation.scratch_root` y no escriben temporales dentro del repositorio. Ninguna dependencia ambiental impidió obtener evidencia: la corrida final es completa y en verde.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `ed2964d656c4a01f68100a383deadbb3c0133345` (`git write-tree` sobre el índice staged con el cambio completo; coincide con el tree del commit C1).
  - **Delta scoped identity (scope S = los 12 paths, ordenados; serialización `scoped-v1`):** `c7a8212e52dba5cfbb58d88c60ef1c49852d8e2289ce765c0ffc1ccfcf7a8cd3`
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/AGENTS.md`, `.agents/policies/autonomous-orchestration.md`, `.agents/policies/supervised-autonomous-execution.md`, `.agents/policies/validation-closure.md`, `CHANGELOG.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `tests/test_sae_scope_enforcement.py`, `tests/test_sae_scope_enforcement_dogfood.py`
- **Validity / stale:** `vigente` para A1; el Plan queda **revalidada** por A2 sobre el estado de cierre (ver el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` OK (215 archivos, 10256 referencias); `check_plan_citations` OK; `check_plan_structure` OK; `check_taxonomy_coherence` OK; `check_session_artifacts` OK; `check_version_state` OK (warnings esperados de `dev`); `pytest tests/` PASS (**1009 passed, 0 failed**); suites nuevas PASS (**44 + 12 = 56 passed**); C-1 `VALID`, C-2 `VALID` (consistencia con A1/A2), C-3 `VALID` (`<PLAN-138>:F-1` → `<PLAN-138>:C-1`); `ANOMALY=0` en los tres gates.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 138 (GC-1, Incremento 3; modelo del Plan 134).*

- **Commits de cierre:** dos (2) commits en `dev`, identificados por su mensaje: C1 `feat(runtime): enforce SAE scope and authority before the effect (plan 138)` (contenido: policies, runtime, suites, README, INDEX, CHANGELOG y el anchor de este Plan) y C2 `docs(plans): close the plan 138 record (plan 138)` (registros de cierre: nota de ejecución, status, checkpoint y revalidación A2).
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `c7a8212e52dba5cfbb58d88c60ef1c49852d8e2289ce765c0ffc1ccfcf7a8cd3`, state identity T1 = `ed2964d656c4a01f68100a383deadbb3c0133345`.
- **Estado de cierre (identidad):** delta scoped identity + state identity de A1, es decir `c7a8212e52dba5cfbb58d88c60ef1c49852d8e2289ce765c0ffc1ccfcf7a8cd3` / `ed2964d656c4a01f68100a383deadbb3c0133345`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** C1 = `53d06882e1acf10b274331a84aaa17aa51e1930a`. Es un hecho de Git y coincide con la state identity T1 del anchor porque el commit C1 **es** la materialización exacta del estado validado: no incluye ningún registro de governance posterior (la nota de ejecución, el status `Executed` y este checkpoint viven en C2, y el Plan está excluido de la identidad de contenido). El tree de C2 diferirá legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`).
- **Consistencia checkpoint↔anchor:** PASS. La identidad scoped del estado de cierre es la del anchor aplicable y los factores ambientales declarados no cambiaron entre la validación y el cierre; C-2 lo verifica sobre el artefacto del Plan. **Revalidación A2:** ejecutada sobre el estado de cierre tras C1 — el mismo command-set (batería canónica + las tres suites de SAE + C-1/C-2/C-3) sobre el contenido idéntico: `pytest tests/` `1009 passed, 0 failed`; seis checkers canónicos PASS; C-1/C-2/C-3 `ANOMALY=0`. A1 se conserva sin mutar; A2 se registra aquí y su delta/state identity son las del estado de cierre, que es el mismo que validó A1 (el Change no modificó contenido entre la validación y el cierre: sólo agregó registros de governance fuera de la identidad de contenido).
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 138 y su serie (Septuagésima) con el header de estado actualizado; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 138, RFC-—)`; `<PLAN-138>:F-1`/`C-1` registrados; determinaciones de impacto abajo; sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag (DEV-only, RFC-69).
- **Condición derivada:** `Closed` (docs-only + tooling DEV, sin release). `Verified` = sí (∃ validación PASS con anchor A1 y revalidación A2); `Executed` = sí (implementación + validación); `Committed` = sí para C1 (estado del repositorio: el contenido validado está commiteado en `dev`); `Promoted` = no; `Released` = no. `Closed ≠ Released`.
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados en C1: `.agents/policies/supervised-autonomous-execution.md` (§1.1 precedencia de Scope sobre toda obligación de estado/cierre, §1.2 checkpoint de autorización y prohibición de retroactividad, §1.3 una escritura se autoriza entera, más §5 stop conditions, §9 impacto fuera de Scope ⇒ `DEFERRED` con PC-1, §10 prevención vs. detección y §12 límites declarados); `.agents/policies/validation-closure.md` (§5.1/§5.2: `REQUIRED` es obligación de estado y **nunca** autorización de escritura; `Roadmap Impact: REQUIRED` no amplía el Scope, con `<PLAN-136>:PC-4` como origen; §7 condiciones de stop); `.agents/policies/autonomous-orchestration.md` (§11.3 prevención vs. detección y punto de enforcement); `runtime/README.md` (sección SAE: enforcement point, checkpoint, all-or-nothing, límite declarado y suites). Aspecto afectado: la semántica operacional de la frontera de SAE y las determinaciones de cierre describían un enforcement que sólo detectaba después del efecto. Evidencia: los cuatro documentos modificados en C1, con las suites nuevas verificando cada regla declarada. `.agents/AGENTS.md` **no** se modificó: el criterio condicional del Paso 12 no se activó —el nombre y el alcance de las policies de SAE/validation closure/autonomous orchestration no cambiaron, de modo que el ruteo vigente sigue siendo correcto— y se registra aquí como `NOT_REQUIRED` parcial con su razón. `docs/CONVENTIONS.md`, `docs/adr/16-change-lifecycle-authority.md`, `docs/rfc/75-change-lifecycle.md` y `.agents/policies/authority.md` **no** se tocaron: la investigación del Paso 0/1 no encontró contradicción normativa real, y la regla nueva es operacional. `docs/VERSIONING.md` §9 no se toca (sin release).
- **Roadmap impact:** `DEFERRED` — la obligación se registra y **no** se satisface dentro de la autorización. El Change **sí** crea trabajo futuro (el endurecimiento de SAE y sus suites entran al mapa operativo), lo que correspondería a `REQUIRED`; el artefacto que posee esa representación para un ítem nuevo es `ROADMAP.md`, que está **excluido del `Scope` autorizado** de este Plan, y por la regla que este mismo Change formaliza (`Roadmap Impact: REQUIRED` **no** autoriza escribir el artefacto que nombra; `<PLAN-136>:PC-4`) la reconciliación no puede completarse aquí. Queda gobernada por la pending decision existente `<PLAN-138>:PC-1` (owner: mantenedor) y el estado de implementación queda representado en `docs/plans/INDEX.md`, que es la fuente de verdad que registra el Plan 138 y su serie. **`ROADMAP.md`: 0 diff**, verificado con `git diff --name-only HEAD -- ROADMAP.md` (vacío) y por
`tests/test_sae_scope_enforcement_dogfood.py` (el test
`test_the_roadmap_is_not_modified_by_this_change`). Ésta es la demostración viva de que el Plan respeta la frontera que el incidente F-3 puso a prueba: el Change que impide convertir una obligación de impacto en autorización de escritura se cierra sin editar el Roadmap.
- Condición derivada: `Closed` (docs-only + tooling DEV, sin release)

## Findings / Correcciones / Pending

### Findings

- `<PLAN-138>:F-1` — estado: `resolved` (transición `open` → `resolved` aplicada el 2026-09-21 por decisión humana del mantenedor, Change del Plan 141; la acción de corregir se ejecutó dentro del Scope por `<PLAN-138>:C-1`); observación: el propio Plan autorizaba como write target `tests/test_sae_scope_enforcement_dogfood.py` —figuraba en `## Delegación agentiva` → `Scope` y en el `## Scope` del Plan— pero **no** lo declaraba en `## Entregables`, de modo que la declaración autorizaba un path que el Plan no declaraba como entregable; es exactamente la clase de divergencia que el enforcement de este Change detecta, y apareció al verificar el envelope real del propio Plan contra la nueva frontera (el
test `test_the_real_plan_envelope_passes_the_new_enforcement` de
`tests/test_sae_scope_enforcement_dogfood.py`); evidencia original: el Plan en el
baseline `b11e4a3` (sección `## Delegación agentiva` → `Scope` vs. sección
`## Entregables`), y la salida de la verificación read-only que muestra
`tests/test_sae_scope_enforcement_dogfood.py` como el único `declared_outside_scope`; estado Git observado: `b11e4a3222f2c6d36a65669be92cf4a3e9889db3`, working tree limpio; provenance original: Paso 0/5 de la ejecución autorizada (2026-09-20). Autoridad aplicable: el Plan aprobado para ejecución autoriza la corrección dentro de su propio Scope (`docs/plans/138-sae-scope-authority-hardening.md` es un write target declarado), y la corrección no cambia ninguna decisión normativa, no requiere RFC ni ADR y no toca el payload; resolución: corregida dentro del Scope por `<PLAN-138>:C-1`; transición `open` → `resolved` aplicada el 2026-09-21 por decisión humana del mantenedor (Change del Plan 141).

### Correcciones

- `<PLAN-138>:C-1` — refs origen: `<PLAN-138>:F-1`; alcance de revalidación: `docs/plans/138-sae-scope-authority-hardening.md`, sección `## Entregables` (se agregó el entregable faltante y se renumeró el registro del propio Plan) y su efecto sobre el envelope del Plan verificado por el test `test_the_real_plan_envelope_passes_the_new_enforcement` de `tests/test_sae_scope_enforcement_dogfood.py`; evidencia: la suite de dogfood en verde tras la corrección, y la verificación read-only que muestra el envelope del Plan 138 con `declared_outside_scope` vacío; la autorización de la corrección es el propio Plan aprobado (registro factual, no fuente normativa).

### Pending decisions

- `<PLAN-138>:PC-1` — decisión: si el endurecimiento de SAE debe registrarse como
  trabajo activo o como candidato en `ROADMAP.md`, y con qué prioridad frente al
  dogfood EARS vigente (`Media`), dado que `ROADMAP.md` está explícitamente fuera
  del `Scope` autorizado de este Plan y la determinación `Roadmap Impact:
  REQUIRED` no autoriza escribirlo; blocking: **no** — no bloquea la ejecución de
  este Plan (cuyo trabajo está íntegramente dentro de rutas autorizadas) ni su
  cierre documental dentro de la autorización; owner: mantenedor; escalación:
  frontera de Scope detectada al redactar este Plan por aplicación directa de la
  decisión humana `<PLAN-136>:PC-4` (a) —`Roadmap Impact: REQUIRED` no amplía el
  `Scope` autorizado— y de la regla que este mismo Plan formaliza; resolución:
  **resuelta** (decisión humana del mantenedor, materializada por el Plan 139 el
  2026-09-20 — DEC-2): la relación queda fijada como
  `Impact classification != authorization`. En particular,
  `Roadmap Impact: REQUIRED` **no autoriza** `write outside authorized Scope`:
  `Scope`/`Task`/`Authority` tienen precedencia sobre cualquier clasificación de
  Impact, y la autorización **no** puede inferirse por proximidad semántica,
  dependencia documental ni requisito de cierre. La regla operativa quedó
  materializada en su lugar canónico existente —
  `.agents/policies/validation-closure.md` §5.1/§5.2 y
  `.agents/policies/supervised-autonomous-execution.md` §1.1— sin crear policy
  paralela ni duplicar la norma. El estado de implementación de este Plan queda
  registrado en `docs/plans/INDEX.md`, que es la fuente de verdad que lo posee, y
  `ROADMAP.md` **no** se modifica; el remanente operativo —si el cierre de estas
  decisiones se registra o no en el mapa y con qué prioridad— sigue gobernado por
  esta misma decisión con owner mantenedor. Evidencia: este registro actualizado, la
  regla en las dos policies y la regresión de `tests/test_sae_scope_enforcement.py`
  (`test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing`);
  efecto downstream: ninguno sobre la ejecución de este Plan; el
  trabajo queda representado en `docs/plans/INDEX.md`; ADR-worthiness: no evaluado — es una decisión humana que
  este Plan no toma.

- `<PLAN-138>:PC-2` — decisión: si SAE necesita un mecanismo para representar y
  ejecutar una **ampliación legítima de Scope** (autorizada por el humano antes
  de la acción), o si basta con que el host se detenga correctamente y la
  ampliación se exprese por la vía de autoridad existente (una nueva
  aprobación/actualización del Plan por el mantenedor); blocking: **no** — la
  detección y la parada correctas no dependen de la existencia de ese mecanismo:
  `STOP por Scope` y `mecanismo para ampliar Scope` son problemas **diferentes**,
  y este Plan resuelve el primero; owner: mantenedor; escalación: investigación
  de F-3 y reformulación del gap registrado en `<PLAN-136>:PC-5`, que este Plan
  **no** resuelve ni reescribe: lo re-registra como boundary propio con el
  alcance mínimo que SAE necesita (detenerse correctamente); resolución:
  **deferred** (decisión humana del mantenedor, materializada por el Plan 139 el
  2026-09-20 — DEC-3): **no se introduce en este Change ningún mecanismo autónomo de
  Scope Expansion**, y la decisión sobre si debe existir queda **diferida**. La
  frontera de autoridad vigente es: el Orchestrator **no** puede ampliar
  autónomamente `Task`, `Scope` ni `Authority`; una necesidad de ampliarla es una
  frontera de autoridad humana y produce `STOP` / `REQUIRES_HUMAN`; hasta que exista
  un mecanismo explícitamente autorizado, el agente se detiene o escala cuando la
  continuación requiera acciones fuera del Scope autorizado. La vía legítima
  existente —sin mecanismo nuevo— es una nueva decisión humana de alcance: una
  aprobación o actualización del Plan por el mantenedor, seguida de la
  reautorización del trabajo que habilita. **No** se inventa protocolo, comando,
  estado, registry, API ni workflow nuevos, ni se modifica `authority.md`; evidencia:
  `## Scope` (exclusión de `.agents/policies/authority.md` y de
  `runtime/orchestrator/contracts.py`), `## Causa arquitectónica` §3 y §4,
  `.agents/policies/supervised-autonomous-execution.md` §1 y §1.3 (la ampliación de
  scope es autoridad humana; el estado de ampliación no existe como mecanismo);
  efecto downstream: si el mantenedor decide que hace falta un mecanismo, su vía es
  una decisión normativa propia (posible ADR-worthiness, no evaluada aquí);
  ADR-worthiness: no evaluado — es una decisión humana que este Plan no toma.

## Causa arquitectónica

*(Resultado de la investigación read-only. Las afirmaciones sobre el código se
anclan a `ruta:sección` o a la función nombrada, y se re-verifican en el Paso 0
antes de materializar nada.)*

### 1. La cadena real, extremo a extremo

```text
Host                runtime/orchestrator/host.py
  observe()         observation.observe()          ← el Scope autorizado se LEE aquí
  derive()          derivation.derive_next_action() ← la ACCIÓN se CONSTRUYE aquí
  authorize()       authority.AuthorityBoundary     ← Authority se evalúa aquí
  [SAE gate]        host._apply_autonomy_gate()     ← la frontera se evalúa aquí (opt-in)
  delegate()        host._build_delegation()        ← el Scope DELEGADO se fija aquí
  execute()         worker.CommandWorker / AgentWorker → (AgentInvoker)
  verify()          host._scope_violations()        ← la violación se DETECTA aquí (después)
  ingest()          contracts.validate_worker_result / WorkerResult
  decide()          derivación siguiente o STOP
```

- **Dónde se construye la acción:** `derivation.derive_next_action`, función pura
  sobre la observación; devuelve un `NextAction` con `kind` y `rationale`. No
  conoce paths de escritura.
- **Dónde se conoce el Scope:** `observation.observe` lo deriva del artifact
  (anchor `Scope set` + artefactos declarados + el propio Plan) y
  `observation.parse_agent_task` lee la declaración `## Delegación agentiva`
  (`Task` + `Scope`). El envelope de SAE se construye desde ahí con
  `autonomy.envelope_from_observation`.
- **Dónde se conoce Authority:** `authority.AuthorityBoundary.evaluate`, que
  emite `AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN` con `basis`.
- **Dónde se materializa una escritura:** en el worker. `CommandWorker` ejecuta
  el command-set; `AgentWorker` invoca un `AgentInvoker` inyectado y luego corre
  la verificación declarada. Los *records* de gobernanza los escribe el host con
  `governance.record_*` sobre el artifact del Plan.
- **Qué componente controla la ejecución:** el `ExecutionHost`; es el único que
  decide continuar o detenerse.
- **Qué componentes pueden modificar archivos:** el worker (vía command-set o vía
  el invoker) y el host (vía los *record writers*). Nada más.
- **Qué componente debería ser el enforcement point:** el `ExecutionHost`, antes
  de `store.write_delegation`, porque es el último punto en el que el efecto
  persistente todavía **no** ocurrió y el único que tiene simultáneamente el
  Scope observado, el envelope declarado y la decisión de autoridad.
- **Qué componentes sólo deberían recibir una decisión ya autorizada:** el
  worker y el invoker. Ninguno de los dos debe contener lógica de autorización:
  si la contenida, habría dos fuentes de verdad de lo autorizado y el worker no
  es autoridad.

### 2. Clasificación de las obligaciones de cierre (P1/P5)

Recorrido de `.agents/policies/` y `.agents/workflows/change-lifecycle.md`
buscando mecanismos que enuncie una obligación de estado/cierre:

| Mecanismo | Qué enuncia | ¿Confiere autorización de escritura? | Protección |
|---|---|---|---|
| `Documentation Impact: REQUIRED` (§5.1 de `.agents/policies/validation-closure.md`) | documentación de estado actual que debe quedar correcta | **No lo dice explícitamente** | aclaración normativa mínima (Paso 4) |
| `Roadmap Impact: REQUIRED` (§5.2 de `.agents/policies/validation-closure.md`) | estado operativo del mapa que debe reconciliarse antes del cierre | **No** — la policy dice «no significa editar `ROADMAP.md`» y que el artefacto lo fija *ownership* | aclaración normativa mínima + regla general de la policy SAE |
| Obligación de reconciliación con `DEFERRED` | impacto que no puede resolverse aún | No | ya exige pending decision existente (PC-1) |
| Gate de verificación del DoD (`docs/VERSIONING.md:10. Definition of Done`) | comandos que deben correr en verde | No (operación read-only) | ninguna: no hay escritura que autorizar |
| Anchor/checkpoint (VC-1/GC-1) | registros que el host escribe en el artifact del Plan | Sí, pero ya está acotada: los escribe el host con el artifact del Plan dentro de `scope_set` | enforcement del Paso 5–7 la vuelve verificable |
| Gates C-1/C-2/C-3 | clasificaciones factuales de los checkers | No | ninguna: read-only |
| Changelog del payload (`docs/VERSIONING.md:5. Changelog`) | obligación de preempción para cambios de `protocol/.agents/` | No — preempción significa que su propia obligación sigue vigente, no que autorice escribir fuera de Scope | cubierta por la regla general |
| Lineage de findings (`LC-1`) | registro factual en el artifact que lo posee | No | ninguna: el registro vive en el artifact autorizado |

**Conclusión (P5).** Existe **una** clase general de regla que necesita la misma
protección: *toda obligación de estado o cierre es un enunciado sobre el estado
del repositorio y nunca una autorización de escritura*. No se encontró ningún
mecanismo que **conceda** autorización de escritura por inferencia; el defecto es
de **ausencia de enunciado explícito**, no de contradicción entre fuentes
normativas. Por eso la protección es una regla general en la policy SAE (que
gobierna el punto de enforcement) más una aclaración mínima en las dos
determinaciones, y **no** un mecanismo nuevo ni un caso especial para `ROADMAP.md`
ni para `Documentation Impact`. **`docs/adr/16-change-lifecycle-authority.md` no
se modifica**: no hay contradicción normativa real que registrar como boundary.

### 3. Distinción entre detección y enforcement

- **Detección (existe hoy).** `host._scope_violations` compara un snapshot de
  contenido del working tree tomado antes de la delegación con otro tomado
  después (`worker.repository_snapshot` / `worker.changed_paths`) y produce
  `STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN` cuando aparecen paths fuera de
  `delegation.declared_scope`. Es un buen mecanismo: deriva de la realidad del
  repositorio y no de la declaración del worker, y funciona incluso sobre un
  working tree que ya estaba sucio. Su límite es estructural: **corre después de
  la escritura**. El efecto persistente ya ocurrió y la parada sólo lo reporta.
- **Enforcement (no existe hoy).** No hay ningún punto que **impida** la
  escritura. El gate de SAE del Plan 135 verifica el candidato contra el
  envelope, pero para `RUN_IMPLEMENTATION_TASK` resuelve **un solo** path
  (`observation.agent_task.scope[0]` en `host._autonomy_target_path`), de modo
  que verifica que el primer path declarado esté en Scope —lo cual es
  trivialmente cierto, porque el envelope y el `declared_scope` de la delegación
  se leen de la misma declaración— y **no** verifica el conjunto de paths que la
  tarea va a escribir. El resultado es que el gate autoriza la delegación sin
  haber demostrado que la escritura sea interna al Scope.
- **Dónde se incorpora el enforcement.** En el `ExecutionHost`, en el punto que
  ya existe (`_apply_autonomy_gate`, invocado desde `iterate` **antes** de
  `_execute_delegation`). No se agrega una fase, un gate nuevo, un componente
  nuevo ni un segundo mecanismo de Scope: se completa el que ya existe.

### 4. Las cuatro causas, separadas

| Causa | ¿Se verificó? | Qué es |
|---|---|---|
| **Ambigüedad normativa** | Sí, real pero **menor** | Ninguna policy decía que una determinación de cierre **no** amplía el Scope. La policy SAE §9 enunciaba qué reconciliar y dónde detenerse, pero no enunciaba el caso F-3 (obligación cuyo artefacto está fuera de Scope) como una parada obligatoria. Es ambigüedad de **enunciado**, no conflicto entre fuentes: `.agents/policies/authority.md` ya ordena STOP al modificar governance fuera de scope sin su propia autorización. |
| **Ausencia de enforcement** | Sí, es la causa principal | El host autorizaba la delegación sin verificar el conjunto real de write targets, y la única verificación de Scope corría después del efecto. La frontera era **descriptiva** (una policy que el agente debía leer y obedecer) y no **operativa** (una precondición que el mecanismo impide violar). |
| **Error de razonamiento del agente** | Sí, contribuyente | El Plan 136 tenía dos enunciados que no podían ser verdaderos a la vez (`Scope` excluye `ROADMAP.md` y `Roadmap Impact: REQUIRED` lo nombra como lo que hay que reconciliar). El agente los resolvió por inferencia a favor de la obligación de impacto en lugar de escalar la contradicción. La regla de refusal ya existía («si la pertenencia no puede establecerse, la respuesta es STOP»); lo que faltaba era que el mecanismo no dejara la decisión en manos del razonamiento del agente. |
| **Posibilidad de autorización retrospectiva** | Sí, real | El artifact del Plan es a la vez el contrato de autorización y el registro mutable de la ejecución. Un agente que puede reescribir `## Scope`, `Task` y la tabla de artefactos afectados puede hacer que una escritura fuera de Scope parezca autorizada desde el inicio, y **nada en el mecanismo lo detecta**: la observación se re-deriva del artifact en cada iteración y no existe constancia de la declaración vigente al autorizar. El propio registro de `corrections` del Plan 136 (`<PLAN-136>:C-3`) documenta el caso. |

**Lo que F-3 demostró como insuficiente.** No la separación conceptual de
Authority/Scope/Autonomy —esa sostuvo el análisis y es correcta— sino **el punto y
el momento del enforcement**: un Scope declarado que sólo se *verifica después* y
que puede *reescribirse durante* la ejecución no es una precondición operacional,
es una recomendación auditable.

**La fórmula conceptual.** `authorized_action = scope_allows(target) AND
authority_allows(action)` es correcta como semántica, pero **no** se implementa
como una igualdad literal ni como una función nueva: se implementa como
**precondición del host antes de la delegación**, sobre el conjunto completo de
`target`s que la acción va a escribir, reusando las funciones y los vocabularios
que ya existen (`verify_action_scope`, `evaluate_autonomy`, `STOP_SCOPE_VIOLATION`).

## Punto de enforcement propuesto

**Componente: `runtime/orchestrator/host.py`, método `_apply_autonomy_gate`,
invocado desde `iterate` antes de `_execute_delegation`.**

Por qué ahí, y no en otro lugar:

1. Es el **último** punto en el que el efecto persistente no ocurrió todavía y en
   el que el host ya tiene todo lo necesario: la acción derivada, el Scope
   observado, el envelope declarado y la decisión de autoridad.
2. Es el **único** componente que decide continuar o detenerse. Poner el
   enforcement en el worker crearía una segunda fuente de verdad de lo autorizado
   y le daría al worker una potestad de decisión que su contrato le prohíbe
   (`.agents/policies/autonomous-orchestration.md` §11.3).
3. `derivation.derive_next_action` **no** cambia: sigue siendo una función pura
   que no decide autorización. Mezclar autorización en la derivación acoplaría dos
   responsabilidades que hoy están limpias y haría la derivación dependiente del
   envelope.
4. `authority.AuthorityBoundary` **no** cambia: sigue respondiendo *¿está
   permitida esta clase de acción?*. El Scope responde *¿está autorizado este
   target?*. Son dos preguntas distintas y se mantienen separadas; la
   conjunción ocurre en el host, que es donde ambas respuestas ya confluyen.
5. La **verificación posterior** (`_scope_violations` → `STOP_FORBIDDEN_ACTION`)
   **se conserva**: cubre la escritura que ocurre dentro del worker y que el host
   no puede interponer. Es defensa en profundidad, no el mecanismo principal.

Diseño del enforcement (tres piezas, todas sobre mecanismos existentes):

- **E1 — Precondición de escritura sobre el conjunto completo.** El candidato de
  SAE lleva el conjunto de write targets de la acción (no un solo path). Todos
  deben pertenecer al Scope autorizado (pertenencia exacta, ya implementada en
  `autonomy.verify_action_scope`) y la clase debe estar permitida por Authority
  (ya implementado en `evaluate_candidate`). Un conjunto vacío o no resoluble
  **no** puede continuar: no puede demostrarse que escriba dentro del Scope.
- **E2 — Checkpoint de autorización (no retroactividad).** La proyección de los
  elementos del contrato de autorización se registra en el journal del run cuando
  el host autoriza la primera acción, y en cada iteración se compara contra la
  proyección observada. Una divergencia es una modificación retrospectiva del
  contrato de autorización y produce `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`.
  Los elementos del contrato son los del Paso 2: `Task`, `Scope`, el `Status` que
  autoriza y la declaración de out-of-scope. Los *records* de gobernanza que el
  host escribe legítimamente (status `Executed`, anchor, checkpoint, nota de
  ejecución) **no** forman parte de la proyección: no son autorización.
- **E3 — Evidencia sin telemetría nueva.** El registro de iteración que ya existe
  (`host._record`, campo `autonomy`) incorpora: acción propuesta, targets,
  decisión de scope, decisión de autoridad, stop condition, evidencia y la
  constancia de ausencia de efecto persistente. Nada de esto requiere un store,
  un registry ni un archivo nuevos.

**Boundary registrado (no se resuelve aquí).** La ampliación legítima de Scope
—autorizada por el humano antes de la acción— se expresa hoy por la vía de
autoridad existente (una nueva aprobación o actualización del Plan por el
mantenedor). **No** existe un mecanismo específico de ampliación de Scope, y este
Plan **no** lo inventa: registra el límite como `<PLAN-138>:PC-2` y determina lo
único que SAE necesita para detenerse correctamente, que es lo que E1–E3 dan.
`STOP por Scope` y `mecanismo para ampliar Scope` son problemas diferentes.

## Cambios normativos

**Qué necesita aclaración:**

1. `.agents/policies/supervised-autonomous-execution.md` — tres enunciados
   nuevos, ninguno de los cuales concede ni quita autoridad:
   (a) **precedencia**: una obligación de cierre, impacto o reconciliación no
   amplía el Scope ni la Authority, y satisfacerla fuera de Scope es `STOP`;
   (b) **checkpoint de autorización**: los elementos que autorizan la ejecución y
   la prohibición de modificarlos retrospectivamente para legitimar una acción ya
   realizada, con la vía legítima de ampliación (antes de la acción, por el
   mecanismo de autoridad existente, con evidencia);
   (c) **precondición de escritura**: ninguna acción con efectos persistentes se
   ejecuta sin que el conjunto completo de sus targets haya sido verificado
   contra el Scope, y la ausencia de target resoluble es `STOP`.
2. `.agents/policies/validation-closure.md` §5.1/§5.2 — una frase por
   determinación: `REQUIRED` **no** autoriza a escribir el artefacto que nombra;
   si ese artefacto está fuera del Scope autorizado, la reconciliación se
   registra `DEFERRED` con la pending decision existente (PC-1) que la gobierna,
   o se escala.
3. `.agents/policies/autonomous-orchestration.md` §5 y §11.3 — la frontera ya
   declara que ensanchar el Scope es decisión humana; se explicita que el host
   verifica **antes** de delegar y que la verificación posterior es defensa en
   profundidad, no el mecanismo principal.

**Qué NO necesita cambio (y por qué):**

- `.agents/policies/authority.md` — la regla «modificar governance fuera de scope
  sin su propia autorización → STOP, report scope violation» ya existe y ya es
  correcta. El defecto era que no había un mecanismo que la hiciera cumplir, no
  que la regla faltara.
- `docs/adr/16-change-lifecycle-authority.md` — no se encontró contradicción
  normativa real. La causa es una ausencia de enunciado operacional en las
  policies DEV, que es donde se corrige.
- `docs/rfc/75-change-lifecycle.md` — RFC-75 gobierna el lifecycle; este Change
  **conduce** mecanismos existentes y no extiende, enmienda ni reinterpreta el
  lifecycle. Sin Amendment Log.
- `docs/CONVENTIONS.md` — la sección «Change Lifecycle — Determinaciones de
  cierre: impacto documental e impacto de Roadmap (regla operacional)» ya declara
  que `REQUIRED` no significa «editar `ROADMAP.md`» y que el artefacto lo fija
  *ownership*; la aclaración de que tampoco autoriza la escritura es operacional
  (policy) y duplicarla en `docs/CONVENTIONS.md` sería una segunda fuente de la
  misma regla.
- `protocol/.agents/` — payload: RFC-56, totalmente fuera.
- Cualquier caso especial para `ROADMAP.md` o para `Documentation Impact` — sería
  exactamente el mecanismo específico que este Plan prohíbe.

## Cambios de runtime

| Archivo | Cambio | Motivo | Riesgo si no se hace |
|---|---|---|---|
| `runtime/orchestrator/autonomy.py` | conjunto de write targets por candidato; verificación all-or-nothing de todos los targets; proyección del checkpoint de autorización | es el módulo puro donde ya vive la frontera; concentrarlo ahí la mantiene testable y determinista | el enforcement quedaría disperso en el host y la frontera dejaría de ser una función pura auditable |
| `runtime/orchestrator/host.py` | enforcement del conjunto completo antes de `_build_delegation`; comparación contra el checkpoint de autorización; evidencia en el registro de iteración | es el único punto que controla la ejecución y el último antes del efecto persistente | el defecto de F-3 persiste: la escritura ocurre y sólo se reporta después |
| `runtime/orchestrator/contracts.py` | **sin cambio**, salvo que el Paso 0 demuestre lo contrario (entonces: STOP y escalar) | `STOP_SCOPE_VIOLATION` ya existe, ya es human-authority stop y ya está en `STOP_ACTIONS` | si se agregara vocabulario nuevo sin necesidad, se crearía estado/lifecycle nuevo, prohibido por este Plan |
| `runtime/orchestrator/derivation.py` | **sin cambio** | la derivación es pura y no decide autorización; mezclarla acoplaría responsabilidades | — |
| `runtime/orchestrator/worker.py`, `agent_worker.py` | **sin cambio** | el worker recibe una decisión ya autorizada y no decide; el límite de la escritura dentro del worker se cubre con la verificación posterior | si se moviera la autorización al worker, habría dos fuentes de verdad de lo autorizado |
| `runtime/orchestrator/observation.py` | **sin cambio**, salvo que la proyección de E2 no sea expresable a partir de la observación (entonces: STOP y escalar) | la observación ya expone `agent_task` (Task/Scope), el status y el path del Plan | — |

## Regresión F-3

**Qué reproduce.** El escenario exacto del incidente, sin nombrar `ROADMAP.md` en
la lógica: un Plan autorizado cuyo `Scope` **excluye** un artefacto `A`; una
determinación de Impact `REQUIRED` que nombra `A` como lo que debe reconciliarse;
un trabajador con autonomía suficiente para intentar resolverlo escribiendo `A`;
y el host con `autonomy_gate=True`.

**Cómo se construye.** `tests/test_sae_scope_enforcement.py` crea un repositorio
git temporal fuera del repo (`pytest_isolation.scratch_root`) con: el artefacto
`A` versionado con un contenido conocido; un Plan autorizado
(`Aprobado para ejecución`) con `## Delegación agentiva` → `Task` que describe el
trabajo y `Scope` que **no** incluye `A`; la determinación
`Roadmap Impact: REQUIRED` nombrando `A`; y un `AgentInvoker` inyectado que
realmente escribe `A` y el path autorizado. El nombre de `A` es un parámetro del
fixture: ningún test hardcodea `ROADMAP.md`.

**Cómo se demuestra que ya no puede ocurrir.**

| # | Aserción | Evidencia |
|---|---|---|
| 1 | El host se detiene con `STOP_SCOPE_VIOLATION` y veredicto `REQUIRES_HUMAN` | `run.terminal_action`, `record["authority"]["verdict"]` |
| 2 | La parada ocurre **antes** de la delegación: no hay delegación persistida para esa iteración | `store.read_delegation(...)` es `None`; `record["delegation_id"] is None` |
| 3 | El artefacto excluido permanece **byte-idéntico** | `sha256` de `A` antes == después |
| 4 | `Scope`, `Task` y la declaración de out-of-scope del Plan permanecen **byte-idénticos** | `sha256` del artifact del Plan antes == después |
| 5 | La evidencia es suficiente y reconstruible | el registro de iteración lleva acción propuesta, targets, `scope_reason`, autoridad, `stop_condition`, evidencia y ausencia de efecto |
| 6 | No se permite legitimar la acción retrospectivamente | ampliar `## Delegación agentiva` después de la primera autorización produce `STOP_SCOPE_VIOLATION`, no continuidad |
| 7 | El caso **falla** contra el comportamiento previo y **pasa** contra el fix | la misma suite corrida sobre el estado previo al cambio (worktree temporal read-only) produce `STOP_FORBIDDEN_ACTION` **después** de la escritura; el baseline de `dev` nunca se modifica |

## Falsificación

Intentos de evadir el enforcement que la suite debe probar y **refusar**, cada
uno nombrando la stop condition exacta (Paso 10):

| Intento | Resultado exigido |
|---|---|
| Escribir un target permitido con una acción permitida | continúa (`AUTONOMOUS`) |
| Escribir un target permitido con una acción no permitida | `REQUIRES_HUMAN` / `FORBIDDEN` según la clase |
| Un target no permitido con una acción en principio permitida | `STOP_SCOPE_VIOLATION` |
| Un conjunto de targets válidos con **un solo** path fuera | `STOP_SCOPE_VIOLATION` (all-or-nothing) |
| Un write class sin target resoluble (o con target vacío) | `STOP_SCOPE_VIOLATION` — no puede demostrarse que escriba dentro del Scope |
| Obligación `REQUIRED` cuyo artefacto está **dentro** del Scope | continúa; la escritura ocurre y el artefacto cambia |
| Obligación `REQUIRED` cuyo artefacto está **fuera** del Scope | `STOP_SCOPE_VIOLATION` **y** el artefacto byte-idéntico |
| Ampliar `Scope` en el artifact después de la primera autorización | `STOP_SCOPE_VIOLATION` (E2: proyección divergente) |
| Cambiar el `Task` después de la primera autorización | `STOP_SCOPE_VIOLATION` |
| Quitar la línea de Scope / vaciar la declaración | `STOP_SCOPE_VIOLATION` o `STOP_AUTHORITY_REQUIRED` según el caso; nunca continuidad |
| Proximidad semántica (path contenedor, descendiente, plural, prefijo, `./`, separadores) | fuera de Scope; nunca `IN_SCOPE` |
| `DEFERRED` sin pending decision que lo gobierne | no es `DEFERRED`: es condición bloqueante |
| Escritura legítima del propio Plan por los *records* del host | continúa (el artifact del Plan es Scope autorizado del host) |
| Declaración de un `AgentInvoker` que escribe fuera de lo declarado (escritura **dentro** del worker) | `STOP_FORBIDDEN_ACTION` posterior (defensa en profundidad); el test documenta que este es el límite que el host no puede interponer |

## Riesgos

- **Falso positivo sobre la escritura legítima del propio Plan.** Si la
  proyección de E2 incluyera el texto completo del artifact, cada *record* de
  gobernanza la haría divergir y el loop se detendría sobre un Change conforme.
  Mitigación: la proyección incluye **sólo** los elementos del contrato de
  autorización (Task, Scope, Status autorizante, out-of-scope), y el test del
  Paso 10 verifica explícitamente que la escritura legítima de un record
  **continúa**.
- **Regresión sobre el corpus de tests de SAE.** Cambiar la firma de
  `verify_action_scope` o de `AutonomousCandidate` rompería las 62 pruebas
  vigentes. Mitigación: extensión **aditiva-optional** (el campo nuevo tiene
  default vacío y el `target_path` singular sigue funcionando); AC-08 lo exige.
- **Enforcement que se convierte en un gate no-op.** Un enforcement que verifica
  el mismo dato del que sale el Scope (como hace hoy
  `host._autonomy_target_path`) pasa siempre y no protege nada. Mitigación: el
  Paso 0 establece el defecto por ejecución y la regresión F-3 exige que el caso
  **falle** contra el estado previo; un test que pasa en ambos estados no es
  regresión.
- **Promesa de garantía que la arquitectura no puede dar.** El host no puede
  interponerse a una escritura que ocurre dentro del `AgentInvoker`. Mitigación:
  declararlo como límite explícito (Paso 8, Paso 11) y conservar la detección
  posterior; el Plan **no** declara una garantía que no puede demostrar.
- **Confundir `STOP por Scope` con `mecanismo para ampliar Scope`.** Sería
  inventar un mecanismo de ampliación dentro de este Plan. Mitigación: el límite
  se registra como `<PLAN-138>:PC-2`; el Change sólo entrega la parada correcta.
- **Reescribir el Plan 136.** El incidente es evidencia; su corrección y la
  transición de `<PLAN-136>:F-3` son humanas. Mitigación: `docs/plans/136-d01-mechanical-checker.md`
  está excluido del Scope y el comando de `## Verificación` exige 0 diff sobre él.
- **Resolver `<PLAN-136>:PC-5` implícitamente.** Mitigación: el Plan registra la
  provenance y crea su propia boundary decision (`<PLAN-138>:PC-2`) sin modificar
  el artifact del Plan 136 ni sus decisiones.

## Trazabilidad

`<PLAN-136>:F-3` (exceso de Scope) → `<PLAN-136>:PC-4` (decisión humana:
`Roadmap Impact: REQUIRED` no amplía el Scope) → `<PLAN-136>:PC-5` (gap de
gobernanza registrado y no resuelto) → **Plan 138** (endurecimiento del
mecanismo) → entregables 1–7 → `<PLAN-138>:PC-1` (reconciliación de Roadmap
diferida) y `<PLAN-138>:PC-2` (boundary de ampliación de Scope, pendiente).

Los Planes 135 (frontera de SAE), 122 (host), 123 (Agent Worker) y 134
(integridad de la evidencia de cierre) son dependencias verificables, no fuentes
modificadas por este Change.

## Nota de redacción

Plan redactado el 2026-09-20 sobre el baseline `ebdbfad` (tree `8fb41698`),
working tree limpio. **Sólo redacción e investigación read-only: no se ejecutó
ningún paso, no se implementó ningún cambio de runtime, no se modificó ninguna
policy, ninguna SAE, ningún test, `protocol/` ni `ROADMAP.md`.** La investigación
de la cadena `Host → Orchestrator → Derivation → Delegation → Worker → Action →
Result` se hizo por lectura de los módulos reales y por ejecución de la batería y
de las suites de SAE (`62 passed`), sin mutar el repositorio.

**Este Plan es su propia demostración.** Declara `Roadmap Impact: DEFERRED` con
una pending decision existente y exige 0 diff sobre `ROADMAP.md`: la obligación
de reconciliación se registra y se difiere, y **no** se convierte en una
autorización para escribir un artefacto fuera del Scope. Es exactamente la
conducta que `<PLAN-136>:PC-4` determinó que era la correcta para el caso F-3.

## Nota de ejecución

**Ejecutado el 2026-09-20** sobre el baseline `b11e4a3222f2c6d36a65669be92cf4a3e9889db3`
(tree `1341ff35f4606b68ab09c41b4099b12d146d08fa`), working tree limpio al iniciar.
Autorización humana explícita para ejecutar el Plan bajo Supervised Autonomous
Execution (el `Status` pasó a `Aprobado para ejecución` como primer acto de la
ejecución, y a `Executed` al cerrar).

**Qué se hizo.** El endurecimiento se materializó en tres piezas sobre mecanismos
existentes, más las policies y las suites. **E1** (`verify_write_targets`,
`_plan_authorized_scope`, `_autonomy_targets`): la precondición de escritura opera
sobre el **conjunto completo** de write targets y verifica contra el Scope que el
Plan declara —`## Entregables` + el `Scope set` del anchor + el propio Plan— y no
contra la declaración que se está verificando; ése era el defecto estructural: el
gate anterior resolvía `resolved[0]` de la misma declaración de la que salía el
Scope, de modo que la comprobación no podía fallar mientras la escritura que
importaba nunca se miraba. **E2** (`authorization_projection`,
`authorization_contract_projection`, `authorization_scope_projection`,
`authorization_drift`, `_pinned_autonomy_projection`): el checkpoint de
autorización se registra en el journal al autorizar y se compara en toda iteración
posterior, con el pin tomado de la autorización **más temprana** del plan para que
una reescritura entre corridas no se re-pinee; la proyección se partió en dos
mitades —contrato y scope— porque una reescritura que el bound de Scope filtra
debía seguir siendo visible como divergencia. **E3**: la evidencia va al campo
`autonomy` del registro de iteración que ya existía. **La detección posterior se
conservó** (`_scope_violations`, `STOP_FORBIDDEN_ACTION`) como defensa en
profundidad, con su límite declarado.

**Defectos encontrados durante la ejecución y su tratamiento.** Tres, todos
deterministas y dentro del Scope, corregidos sin cambiar ninguna decisión
normativa:

1. **`<PLAN-138>:F-1`** — el propio Plan declaraba `tests/test_sae_scope_enforcement_dogfood.py`
   en `## Delegación agentiva` → `Scope` y en `## Scope` pero **no** en
   `## Entregables`: la declaración autorizaba un path que el Plan no declaraba
   como entregable, que es exactamente la clase de divergencia que este Change
   detecta. Detectado al verificar el envelope real del Plan contra la nueva
   frontera; corregido en `<PLAN-138>:C-1` dentro del Scope autorizado.
2. **Falso positivo del checkpoint sobre la transición legítima de status.** La
   primera formulación de la proyección incluía el texto literal del status, de
   modo que el propio `RECORD_PLAN_STATUS_EXECUTED` del host habría hecho divergir
   al run de su propio checkpoint. Corregido antes de cerrar: la proyección usa la
   **familia** de status autorizante (`Aprobado para ejecución` y `Executed` son la
   misma familia), y el test
   `test_the_projection_is_stable_across_the_legitimate_status_transition` lo fija.
3. **Circularidad del chequeo de un solo path.** La verificación contra el Scope
   declarado por la propia declaración bajo prueba era vacua; el primer fixture de
   regresión lo demostró (el caso no se detenía). Corregido redefiniendo la base de
   autorización como el Scope **declarado por el Plan**, con la existencia de la
   ruta deliberadamente **no** requerida —un Plan autoriza el entregable que está
   por crear, y la suite de dogfood de este mismo Change es la prueba: declarada,
   autorizada y ausente hasta que la ejecución la escribe—.

**Ajustes de alcance no realizados.** `.agents/AGENTS.md` **no** se modificó: el
criterio condicional del Paso 12 no se activó (el nombre y el alcance de las
policies no cambiaron, el ruteo vigente sigue siendo correcto).
`runtime/orchestrator/contracts.py`, `derivation.py`, `worker.py`,
`agent_worker.py` y `observation.py` **no** se tocaron: el enforcement se
materializó íntegramente en `autonomy.py` + `host.py` reutilizando
`STOP_SCOPE_VIOLATION`, tal como el Plan exigía. No se creó state machine,
entidad, authority class, registry, lifecycle, sistema de permisos paralelo,
mecanismo de Scope independiente ni caso especial para `ROADMAP.md` o
`Documentation Impact`.

**Verificación.** Seis checkers canónicos PASS; `pytest tests/` **1009 passed,
0 failed** (antes del Change: 953 passed; +56 pruebas nuevas); las suites de SAE
preexistentes verdes (`test_autonomous_scope.py`,
`test_autonomous_scope_dogfood.py`, `test_agent_worker.py`,
`test_autonomous_orchestrator.py`, `test_change_governance.py`: 142 passed);
C-1 `VALID`, C-2 `VALID` con revalidación A2, C-3 `VALID` para
`<PLAN-138>:F-1` → `<PLAN-138>:C-1`; `ANOMALY=0` en los tres gates.
**`ROADMAP.md`, `docs/plans/136-d01-mechanical-checker.md`, `protocol/`, `docs/rfc/`,
`docs/adr/` y `.agents/policies/authority.md`: 0 diff** (verificado con
`git diff --name-only HEAD -- <rutas>`).

**Fronteras respetadas.** `<PLAN-136>:F-3` **no** se cerró: la acción de corregir
es autónoma, la transición de estado es humana, y este Plan no la escribió. El Plan
136 no se modificó. `<PLAN-136>:PC-5` **no** se resolvió: se re-registró como
`<PLAN-138>:PC-2`, no bloqueante. `<PLAN-138>:PC-1` y `<PLAN-138>:PC-2` quedan sin
resolver. EARS no avanzó. Sin push, sin merge, sin tag, sin release y sin promotion.

**Un ciclo de recuperación registrado.** El defecto 3 (circularidad) se detectó por
la propia regresión F-3 fallando contra el fixture —no por inspección del agente—,
y el ciclo fue `detectar → diagnosticar → corregir → revalidar → continuar` dentro
del Scope, sin handoff operacional y sin ampliar autoridad. El defecto 2 se detectó
por diseño (antes de escribir el registro de cierre) y se corrigió en el mismo
ciclo.
