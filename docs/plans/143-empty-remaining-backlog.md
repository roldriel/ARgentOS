# Plan 143 — Vaciar el backlog operativo residual (Empty Remaining Backlog)

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-21
**RFC:** — (vía plan; DEV-only sobre `docs/`, `tools/`, `tests/`, `ROADMAP.md` y `CHANGELOG.md`, con **una excepción de payload declarada**: el registro faltante de `PROTOCOL_TAXONOMY.md` que la H13 regla 11 exige, autorizado como `Clase B` — ver `## Frontera de payload autorizada`)
**Clase:** B — sólo para `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (registro faltante de una entidad `kind: contract` que el contrato H13 regla 11 exige; adición documental compatible, sin cambio de significado, de contrato ni de compatibilidad, con justificación documentada y batería de checkers en verde; `docs/rfc/56-governance-fast-track.md:Decisión propuesta`). El resto del Change no toca el payload: `Clase —`.
**Change Level:** L2 (`max(coordination=1, scope=2, architectural=1, release=1, duration=1)`: la superficie es un conjunto disperso de artefactos DEV —un checker de la batería, sus tests, metadata evolucionable de cuatro planes cerrados, `ROADMAP.md`, el registro de planes y el changelog— más una entidad de taxonomía que produce la versión PATCH 11.6.1; la decisión sobre la frontera de payload del residuo `F-1` es arquitectónica aunque su materialización sea una única línea de datos)
**Depende de:** plan 25, plan 26 y plan 46 (residuo `HD-10`); plan 116, plan 133 y plan 140 (residuo `C-2 GAP`); plan 136 y plan 142 (residuos `F-1`/`F-2`); plan 141 (pending decision `<PLAN-141>:PC-2`)
**Origen:** pedido directo del mantenedor (Change «Plan 143 — Empty Remaining Backlog», 2026-09-21), que enumera los cuatro residuos que permanecen en el backlog operativo actual —`HD-10`/plan 25, `<PLAN-142>:F-1`, `<PLAN-142>:F-2` y el `C-2 GAP` histórico del plan 116— y autoriza su resolución final

## Objetivo

Eliminar los cuatro residuos que quedan en el backlog operativo actual, de modo que
ninguno siga representando trabajo pendiente. La resolución admisible de cada uno es una
de estas: implementación, corrección, transición formal de estado, cierre
histórico/no accionable, o decisión explícita de que una condición externa no forma
parte de la continuidad operativa del repositorio.

**El objetivo no es reclasificar.** Ninguno de los cuatro se cierra por declararlo
`DEFERRED`, `BLOCKED` o `PENDING`: cada fila de la tabla de cierre final nombra la
condición que lo hacía aparecer como pendiente, la decisión que elimina esa condición y
la evidencia que la demuestra.

**Qué no cambia.** Este Change **no** crea ni modifica mecanismos, policies, estados,
registries, authority classes, taxonomías ni workflows; **no** reabre el plan 116, el
plan 142, RFC-56, RFC-75, ADR-15, ADR-16 ni C-2/CI; **no** altera ninguna evidencia
histórica inmutable; **no** inventa una sesión de usuario ni evidencia de ejecución que
no ocurrió; y **no** promueve, taggea, publica ni modifica `dist/`.

**Qué sí cambia.** Extiende **el checker existente** de la batería canónica
(`tools/check_taxonomy_coherence.py`) para verificar la correspondencia
metadata↔entidad que H13 regla 11 exige, con sus regresiones y falsaciones; transiciona
la metadata **evolucionable** de los findings y pending decisions cuyo destino quedó
cumplido; reconcilia el espejo descriptivo (`ROADMAP.md`, `docs/plans/INDEX.md`,
`CHANGELOG.md`, `docs/VERSIONING.md` §4.1); y registra en el diccionario maestro la
entidad contractual que la H13 regla 11 exige y que faltaba (versión PATCH 11.6.1), en
la frontera de payload declarada y autorizada más abajo.

## Frontera de payload autorizada

La implementación del residuo `<PLAN-142>:F-1` se decidió **leyendo el contrato antes de
medir el corpus**, y la medición reveló una condición que el Change no anticipaba:
`protocol/.agents/contracts/CHANGE_GOVERNANCE.md` declara `kind: contract` y no tenía
entidad `kind: contract` en `PROTOCOL_TAXONOMY.md` —sólo la entrada de la sección
`# Artifacts` (`kind: artifact`, con puntero `contract:`), tal como la registró el paso 3
del plan 115—, de modo que la H13 regla 11 estaba incumplida en el corpus y el checker
extendido —uno de los seis de la batería canónica— salía `exit 1`.

Escribir `protocol/.agents/` es una frontera de payload: `Clase B` de RFC-56 requiere plan
`Aprobado para ejecución` con justificación documentada, y `.agents/policies/
supervised-autonomous-execution.md` §5 la lista como stop condition. El agente **no**
infirió la autorización: la registró y la escaló. El mantenedor la ejerció explícitamente
el 2026-09-21 —autorizar el registro faltante bajo este Change, declarado `Clase B`, con
la justificación documentada y el `Scope` extendido de forma explícita—, y **antes** de
aplicar el efecto el `## Scope` de este Plan se amplió y la clase se declaró
(`.agents/policies/supervised-autonomous-execution.md` §1.2: un cambio de scope legítimo ocurre antes de la
acción, por el mecanismo de autoridad existente, con evidencia de esa decisión y seguido
de la autorización del trabajo que habilita).

La justificación documentada de la clase, elemento por elemento: **no cambia el
significado** del protocolo, de ningún contrato ni de ninguna máquina de estados (`B`, no
`A`); **no rompe compatibilidad** con adoptantes (agrega un registro que ya existía como
entrada de artefacto y cuyos cinco campos comparables ya coincidían con el archivo);
**no** introduce un valor, un campo, un estado ni una relación nuevos en el modelo —la
entidad se registra con los valores que el contrato y su entidad de artefacto **ya**
declaraban—; y la batería canónica queda en verde con el registro aplicado.


## Criterio de entrada

- [x] Baseline del repositorio identificable: `dev` en `3b0a3218242466d3b7397917424fde0466888849`, working tree con el cambio de los Planes 141 y 142 **staged y sin commitear** (hecho registrado en la Nota de ejecución; no bloquea la ejecución, y su commit se tramita en `## Pasos`).
- [x] Batería canónica verde sobre el estado de partida: seis checkers PASS (`check_protocol_invariants` 215 archivos / 10334 referencias), `python -m pytest tests/` **1109 passed, 0 failed**, `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; C-1 `ANOMALY=0`, C-2 `VALID=47, GAP=1, ANOMALY=0` (el `GAP` es el preexistente del plan 116) y C-3 `ANOMALY=0`.
- [x] Los cuatro residuos son legibles en sus artefactos de origen y su evidencia se reconstruyó contra el repositorio, no contra un resumen.
- [x] Plan 143 es el próximo número libre, verificado contra `docs/plans/` y `docs/plans/INDEX.md`.
- [x] Las reglas que se aplican existen y están vigentes: `.agents/policies/validation-closure.md` §4/§5/§7, `.agents/policies/supervised-autonomous-execution.md` §1.1–§1.4 y §5/§6, `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`, `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules` regla 11 y `docs/VERSIONING.md:4.1 Batería canónica de verificación`.
- [x] El contrato de H13 regla 11 y el estado real del corpus se observaron **antes** de escribir el checker (`## Matriz de investigación`), de modo que la implementación no se ajustó al resultado esperado.

## Matriz de investigación (resultado real, no supuesto)

| Residuo | Premisa registrada | Evidencia observada en el repositorio | Acción posible |
|---|---|---|---|
| `HD-10` / plan 25 | «el dogfooding medido del perfil `trivial` requiere una sesión de protocolo real con el usuario» | El perfil está **declarado e implementado**: `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles` fija para `trivial` los artefactos `TASK_ANALYSIS.md`/`EXECUTION_PLAN.md`/`VERIFICATION_REPORT.md` y los gates `H00, H04, H06`; `protocol/.agents/harness/gate_validator.py` es profile-aware (H04 omite `Context Reference`) con cobertura en `protocol/.agents/harness/tests/test_gate_validator.py`. Falta **la medición** de una tarea trivial real (≤ 5 archivos, ≤ 3 gates, tiempo contra el baseline de ~52 min) sobre `METRICS.md`, que exige una sesión real con el usuario en un proyecto adoptante sobre una versión **promovida**: `protocol/.agents/VERSION` = `11.6.0` frente a `dist` = `11.2.0`, sin `.project/METRICS.md` ni `state.json`, y con `Promoted`/`Released` reservados al mantenedor | **Determinar** (§1); el trabajo estructural ya está hecho |
| `<PLAN-142>:F-1` | el checker verifica que las referencias **resuelvan**, no que la metadata **coincida** con la entidad (H13 regla 11) | `tools/check_taxonomy_coherence.py` implementa las reglas 2/5/10; su check de contratos sólo comprueba existencia de las referencias (`CONTRACT {key} {field} references unknown state`) y la coherencia del bloque TOML. Ningún punto compara `domain`/`artifact`/`lifecycle`/`produced_by`/`consumed_by` contra la entidad. La divergencia que el Plan 142 corrigió era por eso invisible (su nota de ejecución lo registra) | **Implementar** (§2) |
| `<PLAN-142>:F-2` | el destino de `<PLAN-136>:F-1` (RFC-79 decisión 2 + Plan 142) está **cumplido** y su transición de estado es una decisión humana fuera del `Scope` del Plan 142 | `docs/rfc/79-payload-normative-residuals.md` está `Accepted`; el Plan 142 materializó la decisión 2 en `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` (`"project_scan"`), en `CONTAINERS.md`/`DATABASE.md`/`FILE_MAP.md` y en el ítem 5 de `D01-discovery-output.md`, con el checker DEV endurecido y sus suites en verde; `<PLAN-136>:F-1` sigue leyendo `estado: deferred` | **Transicionar** (§3) |
| plan 116 — `C-2 GAP` | el gate reporta `GAP` por ambigüedad de revalidaciones múltiples y se clasificó histórico/no accionable | `python tools/check_lifecycle_checkpoint.py` → `116-adversarial-deliberation-mvp-closure.md: GAP — multiple declared revalidations could correspond to the closure state; ambiguity, evidence insufficient`, con `ANOMALY=0` y exit 0; el Plan 140 lo clasificó `HISTORICAL / NON-ACTIONABLE`; `<PLAN-133>:F-1` conserva `estado: deferred` y su pending decision en `<PLAN-133>` ya lee `resuelta` | **Formalizar** (§4); el plan 116 no se modifica |

## Determinaciones

### 1. `HD-10` / plan 25 — el requisito sigue siendo normativo y necesariamente externo

**El problema exacto.** El entregable 4 del plan 25 («Tests + dogfooding trivial medido»)
incluye una verificación empírica: una tarea trivial real medida con `METRICS.md`, con
criterio de éxito «≤ 5 archivos, ≤ 3 gates, tiempo notablemente menor al baseline de ~52
min». Nunca se ejecutó.

**La condición que lo hacía aparecer como pendiente.** Tres registros lo declaraban
trabajo pendiente: el `# Status de ejecución` del propio plan 25 («Pendiente: el
dogfooding medido…»), la sección `## Pendientes que requieren autorización` de
`ROADMAP.md` («Dogfood diferido (no payload)») y la pending decision `<PLAN-141>:PC-2`
(`resolución: pendiente`), que además fijaba la acción mínima que remueve el blocker.

**La decisión que elimina esa condición.** La verificación que falta **no es una
capacidad implementable del repositorio**: exige un evento externo que el lifecycle
autónomo no contiene —una versión **promovida** a `master` con `dist` regenerado y una
sesión de protocolo real con un usuario en un proyecto adoptante—. `Promoted` y
`Released` son actos del mantenedor; el host los reporta `FORBIDDEN`, y este Change los
tiene explícitamente excluidos. Por lo tanto la condición se resuelve **reclasificándola**:
la medición del perfil `trivial` es una **actividad de adopción/operación externa**, no
backlog de implementación ni de gobernanza del repositorio.

**Por qué la sesión real sigue siendo un requisito normativo.** El plan 25 no se declara
obsoleto ni su requisito se deroga: nada en la evidencia demuestra que la medición haya
dejado de aportar la garantía que buscaba, y el repositorio no tiene sustituto legítimo
para ella (no hay `METRICS.md` de una sesión trivial, no hay checkout de trabajo de
`dist` y `dist` no contiene el payload evaluado). Lo que cambia es su **clase**: sigue
vigente como condición de adopción/operación, y deja de ser un elemento del backlog
operativo porque no es ejecutable por el agente ni por el lifecycle.

**Evidencia de la resolución.** El plan 25 queda cerrado desde el punto de vista del
backlog en este Plan (§ `## Checkpoint / cierre` y `## Inventario final de residuales`);
`<PLAN-141>:PC-2` pasa a `resuelta` conservando su observación, su evidencia y su
provenance; `ROADMAP.md` deja de declararlo trabajo pendiente y lo registra como
actividad externa de adopción; y el espejo `docs/plans/INDEX.md` se corrige (su fila del
plan 25 declaraba «dogfooding verificado», hecho que el plan 46 ejecutó para el **modo
enforced** del plan 26, no para la medición del perfil `trivial`).

**Trabajo futuro que queda fuera del backlog, y por qué no es residual de este Change.**
La promoción de la versión y la sesión real de perfil `trivial` siguen pendientes como
**actividad externa**, documentadas con su criterio de éxito y su procedimiento. No
constituyen un residual abierto porque no son trabajo del repositorio: requieren la
decisión RELEASE del mantenedor y un usuario real, y su resultado no modifica ningún
artefacto de gobernanza.

**Nunca.** No se declara que la sesión real se ejecutó; no se fabrica usuario, sesión,
`dist` promovido, `METRICS.md`, `state.json`, evidencia de runtime ni resultado de
dogfood.

### 2. `<PLAN-142>:F-1` — implementar la verificación de la H13 regla 11 en el checker existente

**Qué igualdad debe comprobarse, leída del contrato.**
`protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules` regla 11 establece:
«Every contract file on disk must have a `kind: contract` entity whose `domain`,
`artifact`, `lifecycle`, `produced_by` and `consumed_by` match the file's metadata block,
and vice versa.» Los cinco campos son exactamente los comparados; la dirección es
bidireccional (archivo→entidad y entidad→archivo); el conjunto de «contract file» lo fija
el `## Input` de la propia policy (`.agents/contracts/*.md` y
`.agents/orchestrators/*/contracts/*.md`); y el «metadata block» es el bloque YAML de
taxonomía que sigue al bloque TOML (`protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Metadata block placement`).

**Cómo se materializa.** Se extiende `tools/check_taxonomy_coherence.py` —no se crea un
segundo checker— con un punto de verificación que, para cada archivo de contrato del
`## Input`, resuelve su entidad `kind: contract` (por el campo `file` o por el nombre
declarado en `artifact`), compara los cinco campos y reporta la carencia de entidad; y en
la dirección inversa verifica que cada entidad `kind: contract` tenga su archivo. La
comparación es exacta salvo la normalización **declarada** en el propio checker
(representación de listas en línea o en bloque, y `null` frente a la ausencia del campo
como el mismo valor YAML), que es representacional y no semántica.

**Evidencia requerida.** Casos sintéticos de: contrato válido; metadata divergente en el
archivo; entidad divergente; referencia inexistente; múltiples referencias; campos
opcionales; y la normalización declarada. Falsación de que una divergencia pase en
silencio. Corrida del checker sobre el corpus real. `metadata mismatch → deterministic
failure` y `matching metadata → valid`.

**Resultado real sobre el corpus.** La corrida sobre el payload real, con el checker
extendido y **antes** de cualquier corrección del corpus, devuelve `exit 1` y exactamente
una violación:

```text
- CONTRACT .agents/contracts/CHANGE_GOVERNANCE.md has no kind: contract taxonomy entity (H13 rule 11)
```

Es una condición **preexistente** y no introducida por el checker: el paso 3 del plan 115
registró `CHANGE_GOVERNANCE.md` como `kind: artifact` en la sección `# Artifacts` (con
puntero `contract:`) y nunca como `kind: contract`, de modo que el archivo declara
`kind: contract` sin entidad contractual que lo respalde. Su corrección es una escritura
de payload y se resolvió por el acto del mantenedor registrado en `## Frontera de payload
autorizada`: la entidad `contract:CHANGE_GOVERNANCE.md` se registra con los cinco valores
que el contrato y su entidad de artefacto **ya** declaraban, y el checker pasa a `exit 0`
sobre el corpus real. El resultado del checker sin la corrección se conserva como la
evidencia de la medición; el resultado final se registra en la Nota de ejecución.

### 3. `<PLAN-142>:F-2` / `<PLAN-136>:F-1` — transición CL-8 del finding cuyo destino se cumplió

`<PLAN-136>:F-1` describía la frontera `F-17`: el subconjunto mecánico de D01 exigía que
todo `source_files` existiera, mientras `containers.md` y `database.md` declaran ausencias
y `file_map.md` declara hechos de árbol, sin un valor de procedencia que los represente.
Su `resolución` registraba `deferred` con destino «RFC-79 decisión 2 + Plan 142», y
`<PLAN-142>:F-2` verificó que ese destino quedó **cumplido**.

La decisión de resolver el finding existe y está autorizada: el mantenedor autorizó en
este Change «ejecutar las transiciones CL-8 explícitamente autorizadas», y esta es una de
ellas. El defecto material que el finding describe **ya no existe**: el contrato admite el
valor reservado `"project_scan"` para ausencias y hechos de árbol
(`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front
Matter (provenance)`), los tres contratos de ausencia/árbol lo fijan, el ítem 5 de
`protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist` quedó ampliado y `tools/check_discovery_output.py`
reporta `ANOMALY` —no `GAP`— para un `source_files` no resoluble y no reservado, con
falsación en `tests/test_check_discovery_output.py`.

La transición `deferred → resolved` se aplica **sólo** al campo de estado y a la
`resolución` de `<PLAN-136>:F-1`; su identidad, su observación original, su evidencia
original, su estado Git observado y su provenance original se preservan **verbatim**
(CL-8). `docs/plans/136-d01-mechanical-checker.md` es un artefacto cerrado: no se reabre,
no se reescribe ninguna sección normativa y la transición se documenta además en su
bloque append-only `## Metadatos de estado (evolucionables)`.

Como consecuencia, `<PLAN-142>:F-2` —que registró el destino cumplido y dejó la transición
al humano— pasa también a `resolved`.

### 4. plan 116 — `C-2 GAP`: histórico, no accionable y resuelto como residual de backlog

**1. Qué contrato producía originalmente el GAP.** `C-2` verifica, entre otras relaciones,
que el estado de cierre declarado por un checkpoint corresponda a una validación
registrada, y señala como `GAP` —evidencia ambigua, advisory— el caso en que más de una
revalidación declarada podría corresponder a ese estado. El registro del plan 116 declara
más de una revalidación bajo la convención anti-auto-referencia del corpus, de modo que la
selección del anchor aplicable por correspondencia no queda unívocamente determinada.

**2. Por qué el GAP no constituye hoy un defecto operativo.** `GAP` es evidencia faltante
o ambigua, nunca contradicción: `python tools/check_lifecycle_checkpoint.py` sale con
`exit 0` y `ANOMALY=0` sobre el corpus real (142 planes inspeccionados, `VALID=47`,
`GAP=1`), el contrato del checker declara que un `GAP` no cambia el exit code, y ningún
lifecycle actual depende de esa clasificación: el plan 116 está `Executed` con condición
derivada `Closed` sobre la correspondencia con su anchor aplicable.

**3. Qué cambio de modelo/contrato posterior lo dejó históricamente no accionable.** El
Plan 134 fijó el modelo que separa el **estado validado**, el **estado de cierre** y el
**árbol material del commit de cierre**, y con él el contrato de `C-2` (relaciones R1–R4):
la selección del anchor es por correspondencia, nunca por recencia, y la ambigüedad que el
`GAP` reporta es una propiedad del **registro** del plan 116, no del contrato vigente. El
Plan 140 lo clasificó formalmente `HISTORICAL / NON-ACTIONABLE`.

**4. Por qué corregirlo exigiría reabrir o alterar evidencia histórica.** Las dos únicas
vías que harían desaparecer el `GAP` son reescribir el `## Validation anchor` del plan 116
—artefacto cerrado, prohibido: `Closed` es terminal y RFC-46 preserva la traza— o cambiar
el contrato de `C-2` para desambiguar el caso —prohibido por el modelo del Plan 134 y por
el `Scope` de este Change—.

**5. Por qué esa acción no es necesaria para el estado actual del sistema.** No bloquea
ningún cierre, no invalida ninguna evidencia registrada y no impide ninguna operación: el
`GAP` continúa apareciendo en la salida de `C-2` porque ese es el comportamiento
contractual vigente, y el residual de backlog no es el `GAP` sino el **registro de estado
que se lo atribuía como deuda accionable**, `<PLAN-133>:F-1`, que sigue leyendo `estado:
deferred`.

**Materialización.** `<PLAN-133>:F-1` transiciona `deferred → resolved`, con su
observación, su evidencia, su estado Git observado y su provenance preservados verbatim y
un bloque append-only en `docs/plans/133-roadmap-impact-and-documentary-sweep.md`; su
pending decision homónima ya lee `resuelta`. El resultado se registra en este Plan como
`Plan 116 C-2 GAP = HISTORICAL / NON-ACTIONABLE / RESOLVED`, donde `resolved` se refiere a
la resolución del **residual de backlog** y no afirma que el plan 116 nunca produjo el
`GAP` ni que el `GAP` dejó de emitirse. **El plan 116 no se modifica: 0 diff.**

## Entregables

1. `docs/plans/143-empty-remaining-backlog.md` — este Plan, con la matriz, las cuatro determinaciones, la tabla de cierre, el anchor, el checkpoint y los registros de lineage.
2. `tools/check_taxonomy_coherence.py` — verificación de la H13 regla 11 (metadata↔entidad contractual, bidireccional) en el checker existente.
3. `tests/test_check_taxonomy_coherence.py` — regresiones y falsaciones de la verificación nueva.
4. `docs/plans/136-d01-mechanical-checker.md` — sólo el campo `estado` y `resolución` de `<PLAN-136>:F-1`, más el bloque append-only.
5. `docs/plans/133-roadmap-impact-and-documentary-sweep.md` — sólo el campo `estado` y `resolución` de `<PLAN-133>:F-1`, más el bloque append-only.
6. `docs/plans/142-payload-normative-residuals.md` — sólo el estado de `<PLAN-142>:F-1` y `<PLAN-142>:F-2`, más el bloque append-only.
7. `docs/plans/141-human-decision-backlog-resolution.md` — sólo el campo `resolución` de `<PLAN-141>:PC-2`.
8. `ROADMAP.md` — el residuo del plan 25 deja de declararse trabajo pendiente y pasa a actividad externa de adopción.
9. `docs/plans/INDEX.md` — registro del Plan 143 y su serie, y corrección del espejo del plan 25.
10. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 143, RFC-—)` y sección `[11.6.1]` del PATCH de payload.
11. `docs/VERSIONING.md` — §4.1: la enumeración de las reglas de H13 que el checker restaura mecánicamente.
12. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — la entidad `contract:CHANGE_GOVERNANCE.md` que la H13 regla 11 exige (`Clase B`, autorizada explícitamente).
13. `protocol/.agents/VERSION` — `11.6.1` (PATCH del plan).
14. `runtime/toolcalls/canonical.py` — sólo el literal `PROTOCOL_VERSION` = `11.6.1`, alineado con `VERSION` por `tools/check_version_state.py`.

## Pasos

1. **Observar el estado real (read-only).** Reconstruir los cuatro residuos en sus artefactos, leer el contrato de H13 regla 11 y medir el estado del corpus **antes** de escribir código; construir la matriz de investigación sin anticipar resultados.
2. **Correr la batería del estado de partida** y registrar su resultado real, incluidos el `GAP` preexistente del plan 116 y los `EXCLUDED` legacy.
3. **Committer el trabajo pendiente de los Planes 141 y 142** en `dev`, atómico por Change, antes de mezclarlo con la superficie de este Plan; registrar el hecho y su razón en la Nota de ejecución.
4. **`F-1` — implementar** la verificación de la H13 regla 11 en `tools/check_taxonomy_coherence.py` y sus casos en `tests/test_check_taxonomy_coherence.py`.
5. **`F-1` — medir sobre el corpus real** y registrar el resultado observado, sin ajustar el checker al resultado y sin declarar verde lo que no lo esté. La medición revela el registro faltante de `CHANGE_GOVERNANCE.md`: se registra como finding, se escala y **no** se escribe el payload hasta que el mantenedor autorice la ruta.
6. **`F-1` — aplicar la entidad autorizada.** Con la autorización del mantenedor registrada y el `## Scope` y la `Clase` ya declarados (`.agents/policies/supervised-autonomous-execution.md` §1.2), registrar `contract:CHANGE_GOVERNANCE.md` en `PROTOCOL_TAXONOMY.md`, subir `VERSION` a `11.6.1`, alinear el ancla `PROTOCOL_VERSION` del runtime y agregar la sección `[11.6.1]` del changelog.
7. **`F-2` — transicionar** `<PLAN-136>:F-1` y `<PLAN-142>:F-2` a `resolved`, preservando los elementos inmutables y escribiendo los bloques append-only.
8. **`C-2 GAP` — formalizar** la resolución del residual: `<PLAN-133>:F-1` a `resolved` con la clasificación `HISTORICAL / NON-ACTIONABLE` del Plan 140 como fundamento; el plan 116 no se toca.
9. **`HD-10` / plan 25 — determinar** la reclasificación como actividad externa de adopción, transicionar `<PLAN-141>:PC-2` y reconciliar el espejo.
10. **Reconciliar** `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y `docs/VERSIONING.md` §4.1, y buscar transversalmente las referencias de `## Cross-item consistency`.
11. **Verificar** la batería canónica completa, `protocol/.agents/harness/tests/`, la guarda EARS, los gates C-1/C-2/C-3 y los tests nuevos; registrar anchor y checkpoint; commit atómico en `dev`. Sin push, sin merge, sin tag, sin release y sin promotion.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el `Scope` es decisión humana.

- `docs/plans/143-empty-remaining-backlog.md` (este Plan)
- `tools/check_taxonomy_coherence.py`
- `tests/test_check_taxonomy_coherence.py`
- `tests/test_sae_scope_enforcement_dogfood.py` (sólo la constante del digest normativo del plan cerrado 136 y el docstring del test anclado) — **incluido explícitamente**: la transición CL-8 autorizada sobre un plan cerrado cambia el contenido canónico que ese test ancla, y el contrato de estabilidad de tests anclados de `tests/AGENTS.md` exige recomputar el pin cuando el estado canónico cambia de forma legítima; ninguna aserción se relaja (la lógica de canonicalización y todas las aserciones de contenido se conservan). Está cubierto por la autorización del mantenedor («crear tests y verificaciones necesarias», artefactos asociados «tests»), no por inferencia de la determinación de impacto.
- `docs/plans/136-d01-mechanical-checker.md` (sólo el estado de `<PLAN-136>:F-1` y el bloque append-only)
- `docs/plans/133-roadmap-impact-and-documentary-sweep.md` (sólo el estado de `<PLAN-133>:F-1` y el bloque append-only)
- `docs/plans/142-payload-normative-residuals.md` (sólo el estado de `<PLAN-142>:F-1`/`F-2` y el bloque append-only)
- `docs/plans/141-human-decision-backlog-resolution.md` (sólo el campo `resolución` de `<PLAN-141>:PC-2`)
- `ROADMAP.md` — incluido **explícitamente** porque su reconciliación es una obligación de estado de este Change (`.agents/policies/validation-closure.md` §5.2) y es el artefacto que posee el mapa operativo; la autorización es el pedido del mantenedor, que incluye «actualizar la documentación, índices y metadata evolutiva necesaria», **no** la determinación de impacto. Ninguna otra sección del mapa se toca.
- `docs/plans/INDEX.md`
- `CHANGELOG.md`
- `docs/VERSIONING.md` (sólo la nota de §4.1 sobre las reglas de H13 que el checker restaura)
- `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (sólo la entidad `contract:CHANGE_GOVERNANCE.md` que la H13 regla 11 exige) — **incluido explícitamente en el `Scope` por el acto del mantenedor** del 2026-09-21, con la justificación de clase documentada en `## Frontera de payload autorizada`; la autorización **no** se infiere de la clasificación de impacto ni del requisito de cierre.
- `protocol/.agents/VERSION` y `runtime/toolcalls/canonical.py` (sólo el literal `PROTOCOL_VERSION`) — **cambio asociado exigido por el contrato de versionado**: `docs/VERSIONING.md` §3 («un plan = una versión») y `tools/check_version_state.py`, que exige que el ancla semántica del runtime coincida con `protocol/.agents/VERSION`; el PATCH 11.6.1 es la versión de este Plan.

**Excluido explícitamente:**

- El resto de `protocol/.agents/` — **0 diff**: ningún otro archivo del payload se toca, y el contrato `CHANGE_GOVERNANCE.md` en sí **no** se modifica.
- `docs/plans/116-adversarial-deliberation-mvp-closure.md` — **0 diff**: su `C-2 GAP` se clasifica, no se corrige, y el artefacto cerrado no se reabre.
- `docs/plans/25-task-profile-model.md`, `docs/plans/26-hook-enforcement.md` y `docs/plans/46-enforced-mode-dogfooding.md` — **0 diff**: son artefactos cerrados y su prosa histórica se conserva (RFC-46); la determinación corriente se registra en este Plan y en el espejo del `INDEX.md`.
- `docs/rfc/`, `docs/adr/`, `.agents/`, el resto de `runtime/`, `dist/` y `MASTER_PENDING_WORK_INVENTORY.md` — **0 diff**.
- La batería canónica fuera de `tools/check_taxonomy_coherence.py` — los demás checkers se ejecutan **como están**.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–11 de este Plan: observar read-only el estado real de los cuatro residuos, del contrato de H13 regla 11 y del corpus; commitear el trabajo pendiente de los Planes 141/142 antes de empezar la superficie propia; implementar en `tools/check_taxonomy_coherence.py` —el checker existente, sin crear un segundo— la verificación bidireccional de la H13 regla 11 con sus casos y falsaciones en `tests/test_check_taxonomy_coherence.py`; medir el corpus real y registrar el resultado **observado**; registrar la entidad `contract:CHANGE_GOVERNANCE.md` que la regla exige, con el PATCH `11.6.1`, el ancla `PROTOCOL_VERSION` alineada y la sección de changelog, **sólo** bajo la autorización del mantenedor registrada en `## Frontera de payload autorizada`; transicionar la metadata evolucionable de `<PLAN-136>:F-1`, `<PLAN-133>:F-1`, `<PLAN-142>:F-1`, `<PLAN-142>:F-2` y `<PLAN-141>:PC-2` con bloques append-only y elementos inmutables preservados verbatim; registrar la determinación de `HD-10`/plan 25 como actividad externa de adopción; reconciliar `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y `docs/VERSIONING.md` §4.1; verificar la batería completa, los gates C-1/C-2/C-3 y el 0 diff de los artefactos protegidos; registrar anchor y checkpoint; commit atómico en `dev`. **No** crear ningún mecanismo, policy, checker, estado, registry, authority class, taxonomía ni workflow nuevos; **no** modificar `protocol/.agents/` fuera de la entidad declarada, `docs/plans/116-…`, los planes 25/26/46, RFCs, ADRs, `.agents/`, el resto de `runtime/`, `dist/` ni el inventario externo; **no** promover, taggear, publicar ni inventar evidencia.
- **Scope:** las rutas enumeradas en `## Scope`.
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera del `Scope`.
  - **`STOP_FORBIDDEN_AUTONOMY`** — release, promotion, tag, push, `dist/`, reescritura de un artefacto cerrado fuera de su metadata evolucionable.
  - **`STOP_AUTHORITY_REQUIRED`** — cualquier cambio de `protocol/.agents/`: es frontera de payload y sigue su propia vía RFC-56. Si la implementación de `F-1` revela una condición de payload, se registra como finding con su pending decision y se detiene en la frontera; **no** se escribe el payload.
  - **`STOP_AUTHORITY_REQUIRED`** — convertir la inferencia del agente en decisión humana: las transiciones de estado se registran como decisiones del mantenedor ejercidas por la autorización de este Change.
  - **`STOP` (`ANOMALY`)** — cualquier `ANOMALY` de la batería o de C-1/C-2/C-3 que la ejecución no pueda resolver dentro del `Scope`.
- **Autoridad:** este Plan y el pedido del mantenedor que lo origina. Ninguna otra.

## Stop conditions

Además de las de `.agents/policies/supervised-autonomous-execution.md` §5, este Change se
detiene y escala —sin resolver por inferencia— si:

1. la verificación de la H13 regla 11 exige escribir `protocol/.agents/` **fuera** de la
   entidad declarada en el `## Scope` y autorizada por el mantenedor: la frontera es de
   payload y no se amplía por inferencia (una ruta distinta de
   `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, o cualquier otro archivo
   del payload, detiene la ejecución);
2. una transición de estado exigiría modificar un elemento inmutable de un finding, o
   reabrir un artefacto cerrado;
3. resolver el residuo del plan 25 exigiera declarar ejecutada una sesión real, un `dist`
   promovido o cualquier evidencia de runtime que no existe.

## Criterios de salida

- [ ] `HD-10` / plan 25 tiene resolución final autoritativa: `RESUELTO` como residual de backlog, con la sesión real documentada como actividad externa de adopción **no ejecutada**.
- [ ] La verificación de la H13 regla 11 está implementada en `tools/check_taxonomy_coherence.py` y verificada por sus casos y falsaciones; `metadata mismatch → deterministic failure` y `matching metadata → valid`; el checker sale `exit 0` sobre el corpus real.
- [ ] La entidad `contract:CHANGE_GOVERNANCE.md` que la regla exige está registrada (única escritura de payload, autorizada), con el PATCH `11.6.1` consistente entre `VERSION`, el changelog y el ancla `PROTOCOL_VERSION`.
- [ ] `<PLAN-136>:F-1` y `<PLAN-142>:F-2` transicionados por CL-8, con observación, evidencia, estado Git observado y provenance preservados verbatim.
- [ ] El `C-2 GAP` del plan 116 queda `HISTORICAL / NON-ACTIONABLE / RESOLVED` como residual de backlog, con el plan 116 en **0 diff**.
- [ ] No existe ningún `ANOMALY` nuevo, y ningún `GAP` nuevo salvo el comportamiento histórico de `C-2` sobre el plan 116.
- [ ] Ninguna evidencia fue falsificada y ningún artefacto histórico fue reescrito fuera de su metadata evolucionable.
- [ ] Batería canónica en verde; `python -m pytest tests/` y `python -m pytest protocol/.agents/harness/tests/ -q` en verde con el conteo exacto registrado; C-1/C-2/C-3 con `ANOMALY=0`.
- [ ] `runtime/` (salvo el literal `PROTOCOL_VERSION`), `.agents/`, `docs/adr/`, `dist/` y el plan 116: **0 diff**; la tabla de cierre del backlog tiene las cuatro filas con evidencia concreta.
- [ ] Determinaciones de Documentation impact y Roadmap impact registradas de forma independiente y con evidencia.
- [ ] Anchor, checkpoint y nota de ejecución registrados; commit atómico en `dev`.

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

Verificación específica de este Change:

```bash
python -m pytest tests/test_check_taxonomy_coherence.py -q
python tools/check_lifecycle_lineage.py
git diff HEAD --name-only -- .agents/ docs/adr/ docs/rfc/ docs/plans/116-adversarial-deliberation-mvp-closure.md docs/plans/25-task-profile-model.md docs/plans/26-hook-enforcement.md docs/plans/46-enforced-mode-dogfooding.md protocol/.agents/contracts/CHANGE_GOVERNANCE.md
git diff HEAD -- runtime/
git diff HEAD --stat -- protocol/
git diff HEAD --stat -- docs/plans/133-roadmap-impact-and-documentary-sweep.md docs/plans/136-d01-mechanical-checker.md docs/plans/142-payload-normative-residuals.md docs/plans/141-human-decision-backlog-resolution.md
```

La tercera corrida debe dar **0 diff**; la cuarta debe mostrar **sólo** el literal
`PROTOCOL_VERSION` de `runtime/toolcalls/canonical.py`; la quinta debe mostrar **sólo**
`protocol/.agents/VERSION` y `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (la
entidad registrada); la sexta debe mostrar **sólo** metadata de estado y bloques
append-only, nunca una sección normativa reescrita.

## Cross-item consistency

Barrido de las referencias del conjunto, cada una clasificada en una de las cinco clases
del cambio. La historia no se modifica para obtener consistencia textual: lo que se
reconcilia es el **espejo descriptivo y la metadata evolucionable**, y lo que se conserva
es la evidencia histórica (RFC-46).

| Referencia | Dónde aparece | Clase |
|---|---|---|
| `HD-10`, `CON-8`, `CON-21` | `MASTER_PENDING_WORK_INVENTORY.md` (artefacto **externo**, untracked, no autoridad) | Provenance de investigación: se lee y no se modifica |
| `HD-10` (matriz, §7, inventario, nota de ejecución) y el bloqueo del plan 25 | `docs/plans/141-human-decision-backlog-resolution.md` | Evidencia histórica (artefacto cerrado; se conserva verbatim) |
| `HD-10`: el dogfood del plan 26 satisfecho y el del plan 25 con blocker externo | `CHANGELOG.md`, `docs/plans/INDEX.md` §Septuagésima tercera serie | Espejo resuelto: se reconcilia con el estado corriente |
| `Pendiente: el dogfooding medido de una tarea trivial…` | `docs/plans/25-task-profile-model.md:Status de ejecución` | Evidencia histórica: se conserva; la determinación corriente vive en este Plan |
| `Pendiente: dogfooding enforced real` | `docs/plans/26-hook-enforcement.md` | Evidencia histórica **satisfecha**: `docs/rfc/47-enforced-mode-dogfooding.md:Decisión propuesta` admitía la simulación y el plan 46 la ejecutó |
| `dogfooding verificado 12 ago 2026, plan 46` en la fila del **plan 25** | `docs/plans/INDEX.md` §Backlog evidenciado | Espejo resuelto: declaraba verificado el perfil `trivial` con la simulación del modo enforced; se corrige |
| `Dogfood diferido (no payload)` | `ROADMAP.md:Pendientes que requieren autorización` | Mapa operativo (current state): se reconcilia como actividad externa de adopción |
| `<PLAN-141>:PC-2` (`resolución: pendiente`) | `docs/plans/141-human-decision-backlog-resolution.md` | Espejo resuelto: metadata evolucionable → `resuelta` |
| `Plan 116 C-2 GAP` y su clasificación `HISTORICAL / NON-ACTIONABLE` | `docs/plans/140-governance-residual-closure.md:Determinaciones` y su inventario final | Normativo corriente (la clasificación vigente) + evidencia histórica |
| `<PLAN-133>:F-1` (`estado: deferred`) | `docs/plans/133-roadmap-impact-and-documentary-sweep.md:Findings` | Espejo resuelto: metadata evolucionable → `resolved` |
| `<PLAN-133>` pending decision (`resuelta`) | `docs/plans/133-roadmap-impact-and-documentary-sweep.md:Pending decisions` | Normativo corriente: ya transicionada por el Plan 141 |
| `<PLAN-136>:F-1` (`estado: deferred`, destino RFC-79 decisión 2 + Plan 142) | `docs/plans/136-d01-mechanical-checker.md:Findings` | Espejo resuelto: metadata evolucionable → `resolved` |
| `<PLAN-142>:F-1` (`estado: deferred`, destino un Change DEV propio) y `<PLAN-142>:F-2` | `docs/plans/142-payload-normative-residuals.md:Findings` | Espejo resuelto: metadata evolucionable → `resolved`; este Plan **es** el Change de destino |
| `F-17`, `project_scan`, ítem 5 de D01 | `docs/rfc/79-payload-normative-residuals.md`, `protocol/.agents/orchestrators/discovery/…` | Normativo corriente materializado por el Plan 142; evidencia de la resolución de `F-2` |
| H13 regla 11 (enunciado) | `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules` | Normativo corriente: es la fuente que el checker implementa |
| `# Artifacts` → `CHANGE_GOVERNANCE.md` (`kind: artifact`, puntero `contract:`) | `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (sección `# Artifacts` del bloque `entities`) | Normativo corriente: se **conserva**; se agrega la entidad `kind: contract` que faltaba |
| `taxonomy metadata` de los dos contratos de discovery | `docs/rfc/79-…`, `docs/plans/142-…`, `docs/plans/126-…` | Evidencia histórica de la decisión 7 y de `<PLAN-126>:PC-1` |
| `session/user dogfood` verificado del modo enforced | `docs/ADOPTION.md:6.2. Comportamiento verificado del flujo enforced` | Evidencia histórica (12 ago 2026), vigente para el plan 26 |
| `external blocker` (promoción + sesión real) | `ROADMAP.md`, `<PLAN-141>:PC-2`, `docs/plans/141-…` | Reclasificado: actividad externa de adopción, **no** backlog de implementación |
| `historical GAP` | `docs/plans/140-governance-residual-closure.md` y el inventario externo `MASTER_PENDING_WORK_INVENTORY.md` (secciones 3 y 4; artefacto no versionado, se cita sin crear un objetivo de cita trackeado) | Clasificación normativa corriente + provenance externa |
| `(H13 rules 2/5/10)` | `docs/VERSIONING.md:4.1 Batería canónica de verificación` | Normativo corriente **desactualizado**: se corrige a `2/5/10/11` |

## Tabla de cierre del backlog

| Residual | Condición original | Resolución | Evidencia | Estado final |
|---|---|---|---|---|
| `HD-10` / plan 25 | El entregable 4 del plan 25 dejaba «Pendiente» la medición de una tarea trivial real (≤ 5 archivos, ≤ 3 gates, tiempo contra el baseline de ~52 min), registrada además por `ROADMAP.md` y por `<PLAN-141>:PC-2` como trabajo pendiente | La verificación exigida **no es una capacidad implementable del repositorio**: requiere una versión promovida y una sesión real con el usuario, actos externos al lifecycle autónomo. Se **reclasifica** como actividad de adopción/operación externa; `<PLAN-141>:PC-2` → `resuelta`; `ROADMAP.md` deja de declararla trabajo pendiente; el espejo del `INDEX.md` se corrige | `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles` (gates `H00, H04, H06` y artefactos del perfil declarados) + `protocol/.agents/harness/gate_validator.py` y `protocol/.agents/harness/tests/test_gate_validator.py` (comportamiento profile-aware verificado) + `protocol/.agents/VERSION` = `11.6.1` frente a `dist` = `11.2.0` + ausencia de `METRICS.md`/`state.json` en `.project/` + `git tag --list '11.*'` sin `11.3.0`–`11.6.1` | **RESUELTO** (la sesión real queda documentada como **actividad externa no ejecutada**) |
| `<PLAN-142>:F-1` | `tools/check_taxonomy_coherence.py` verificaba que las referencias de la metadata de un contrato **resolvieran**, no que la metadata **coincidiera** con su entidad `kind: contract` (H13 regla 11), de modo que una divergencia de esa clase era invisible para la batería | Se **implementa** la verificación bidireccional de la regla 11 en el checker existente —sin crear un segundo— con sus casos y falsaciones; la corrida sobre el corpus real revela una condición de payload preexistente (registro faltante de `CHANGE_GOVERNANCE.md`), que se registra, se escala y se resuelve con la autorización explícita del mantenedor | `tools/check_taxonomy_coherence.py` (check 9) + `tests/test_check_taxonomy_coherence.py` (28 passed, incluidos los cinco campos, la referencia inexistente, las referencias múltiples, los campos opcionales y las dos normalizaciones declaradas) + `python tools/check_taxonomy_coherence.py` → `Taxonomy coherence OK` (`exit 0`) sobre el corpus real + `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (entidad `contract:CHANGE_GOVERNANCE.md`) + PATCH `11.6.1` | **RESUELTO** |
| `<PLAN-142>:F-2` (destino de `<PLAN-136>:F-1`) | `<PLAN-136>:F-1` describía la frontera `F-17` y quedó `estado: deferred` con destino «RFC-79 decisión 2 + Plan 142»; la transición de estado es una decisión humana (CL-8) que el Plan 142 no tenía autorizada | Se ejecuta la **transición CL-8 autorizada**: `<PLAN-136>:F-1` → `resolved` (el defecto material ya no existe) y `<PLAN-142>:F-2` → `resolved` (el hecho que registraba quedó consumado), con sus elementos inmutables preservados verbatim y bloque append-only | `docs/rfc/79-payload-normative-residuals.md` `Accepted` + `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` (`"project_scan"`) + `CONTAINERS.md`/`DATABASE.md`/`FILE_MAP.md` + `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist` ítem 5 + `tools/check_discovery_output.py` con `ANOMALY` para un `source_files` no resoluble + `tests/test_check_discovery_output.py` + `python tools/check_lifecycle_lineage.py` `VALID`, `GAP=0`, `ANOMALY=0` | **RESUELTO** |
| plan 116 — `C-2 GAP` | El gate `C-2` reporta `GAP` sobre `docs/plans/116-adversarial-deliberation-mvp-closure.md` (más de una revalidación declarada podría corresponder al estado de cierre), y `<PLAN-133>:F-1` lo conservaba como `estado: deferred` con destino «decisión humana» | Se **formaliza** la clasificación del Plan 140 (`HISTORICAL / NON-ACTIONABLE`) y se resuelve el residual de backlog: `<PLAN-133>:F-1` → `resolved`. El `GAP` **sigue emitiéndose** —es el comportamiento contractual vigente de `C-2`— y el plan 116 no se modifica | `python tools/check_lifecycle_checkpoint.py` → `Summary: 142 plans inspected; EXCLUDED=94, BOUNDARY=0, N/A=0, VALID=47, GAP=1, ANOMALY=0` con `exit 0` y la línea `116-…: GAP — multiple declared revalidations…` + `docs/plans/140-governance-residual-closure.md:Determinaciones` §5 + `docs/plans/134-closure-evidence-integrity.md` (modelo de estado de cierre y contrato de C-2) + `git diff` del plan 116 vacío | **RESUELTO** (`HISTORICAL / NON-ACTIONABLE / RESOLVED` como residual de backlog) |

Ninguna fila se cierra por `deferred`, `fuera de alcance` ni `ya no importante`: cada una
nombra la condición que la hacía aparecer como pendiente, la decisión que elimina esa
condición y la evidencia que la demuestra.

## Inventario final de residuales

### 1. Backlog resuelto

Los cuatro elementos de la tabla anterior: `HD-10`/plan 25, `<PLAN-142>:F-1`,
`<PLAN-142>:F-2`/`<PLAN-136>:F-1` y el `C-2 GAP` del plan 116. No queda ninguno de ellos
como trabajo pendiente del backlog operativo.

### 2. Evidencia histórica preservada

La prosa de los planes 25, 26, 46, 116, 133, 136, 141 y 142; los `GAP`/`BOUNDARY`/
`EXCLUDED` de los gates de lifecycle; el registro del plan 116 y su `C-2 GAP`; y el
inventario externo `MASTER_PENDING_WORK_INVENTORY.md`. Nada de esto se reescribe: los
artefactos cerrados conservan su contexto (RFC-46) y las únicas escrituras sobre ellos son
metadata evolucionable de estado y bloques append-only.

### 3. Actividad externa que deja de ser backlog

La **promoción** de la versión en curso y la **sesión real de protocolo** de perfil
`trivial` sobre un proyecto adoptante, con su criterio de éxito y su procedimiento. Queda
documentada como actividad de adopción/operación **no ejecutada**: requiere la decisión
RELEASE del mantenedor y un usuario real, no produce trabajo del repositorio y su
resultado no modifica ningún artefacto de gobernanza. **No se fabricó ninguna evidencia de
esa sesión.**

### 4. Residual nuevo descubierto durante la ejecución

La implementación de `<PLAN-142>:F-1` reveló **una** condición de payload preexistente y
genuina: `CHANGE_GOVERNANCE.md` declaraba `kind: contract` sin entidad `kind: contract` en
el diccionario maestro (H13 regla 11). No es un residuo abierto de este Change: se
resolvió dentro de él con la autorización explícita del mantenedor, quedó declarado en el
`## Scope` y en la `Clase` **antes** del efecto, y su corrección es una única entidad de
datos sin cambio de significado. Lo que **sí** se conserva es la observación de que la
batería era verde con la regla 11 incumplida: esa es exactamente la cobertura que este
Change agrega.



- **Ajustar el checker al corpus en lugar de medirlo.** Mitigación: el contrato se leyó y el corpus se midió **antes** de escribir la verificación, y el resultado real de la corrida se registra tal como sale, incluida cualquier divergencia que aparezca.
- **Cerrar por reclasificación en lugar de por resolución.** Mitigación: cada una de las cuatro filas de la tabla de cierre nombra la condición que lo hacía aparecer pendiente, la decisión que la elimina y su evidencia; ninguna se cierra por `deferred`/`fuera de alcance`.
- **Modificar de más la evidencia histórica.** Mitigación: sólo metadata evolucionable y bloques append-only, con los elementos inmutables verbatim y un `git diff` restringido en `## Verificación`.
- **Atribuir a este Change el trabajo pendiente de los Planes 141/142.** Mitigación: su commit se hace **antes** de empezar la superficie propia y se registra con su mensaje y su razón.
- **Convertir una actividad externa en evidencia.** Mitigación: la sesión real del plan 25 queda explícitamente declarada como **no ejecutada**; no se crea `METRICS.md`, `state.json` ni ningún resultado de dogfood.

## Riesgos

- **Ajustar el checker al corpus en lugar de medirlo.** Mitigación: el contrato se leyó y el corpus se midió **antes** de escribir la verificación, y el resultado real de la corrida se registra tal como sale, incluida la condición preexistente que apareció.
- **Cerrar por reclasificación en lugar de por resolución.** Mitigación: cada una de las cuatro filas de la tabla de cierre nombra la condición que lo hacía aparecer pendiente, la decisión que la elimina y su evidencia; ninguna se cierra por `deferred`/`fuera de alcance`.
- **Modificar de más la evidencia histórica.** Mitigación: sólo metadata evolucionable y bloques append-only, con los elementos inmutables verbatim y un `git diff` restringido en `## Verificación`.
- **Convertir la frontera de payload en una autorización inferida.** Mitigación: la única escritura de payload está declarada en el `## Scope` y en la `Clase` y respaldada por el acto explícito del mantenedor, registrado **antes** del efecto (`.agents/policies/supervised-autonomous-execution.md` §1.2); la `## Stop conditions` detiene cualquier otra ruta del payload.
- **Atribuir a este Change el trabajo pendiente de los Planes 141/142.** Mitigación: su commit se hace **antes** de empezar la superficie propia y se registra con su mensaje y su razón.
- **Convertir una actividad externa en evidencia.** Mitigación: la sesión real del plan 25 queda explícitamente declarada como **no ejecutada**; no se crea `METRICS.md`, `state.json` ni ningún resultado de dogfood.

## Trazabilidad

`MASTER_PENDING_WORK_INVENTORY.md` (`HD-10`, `CON-8`, `CON-21`) → planes 141/142 (estado
corriente) → **Plan 143 (este Plan)**. `HD-10` → `docs/rfc/47-enforced-mode-dogfooding.md`
+ plan 46 (modo enforced, satisfecho) + `docs/plans/25-task-profile-model.md:Status de
ejecución` + `ROADMAP.md:Pendientes que requieren autorización` + `<PLAN-141>:PC-2`.
`F-1` → plan 142 (`deferred`) → `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules`
regla 11 → `tools/check_taxonomy_coherence.py` + `tests/test_check_taxonomy_coherence.py`.
`F-2` → `<PLAN-136>:F-1` → RFC-79 decisión 2 → plan 142 → `D01-discovery-output.md` +
`KB_DISCOVERY_ENTRY.md` + `tools/check_discovery_output.py`. `C-2 GAP` → plan 116 → plan
134 (modelo de estado de cierre y contrato de C-2) → plan 140 (clasificación
`HISTORICAL / NON-ACTIONABLE`) → `<PLAN-133>:F-1`.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 143 (VC-1).*

- **Declared scope:** las rutas del `## Scope` (quince archivos: `CHANGELOG.md`, `ROADMAP.md`, `docs/VERSIONING.md`, `docs/plans/133-…`, `docs/plans/136-…`, `docs/plans/141-…`, `docs/plans/142-…`, `docs/plans/143-…`, `docs/plans/INDEX.md`, `protocol/.agents/VERSION`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `runtime/toolcalls/canonical.py`, `tests/test_check_taxonomy_coherence.py`, `tests/test_sae_scope_enforcement_dogfood.py` y `tools/check_taxonomy_coherence.py`).
- **Validation command-set:** el de `## Verificación` (batería canónica completa, suites del payload, la guarda EARS, los gates C-1/C-2/C-3 y las suites específicas de este Change).
- **Effective inputs (repo content):** el scope declarado, los checkers de `tools/`, la suite `tests/`, el payload completo que consume la batería y el corpus de `docs/plans/` y `docs/rfc/`.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de las suites); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14.3; git 2.55.0.windows.5; sin red.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `03f51f6cc5a4968530fe3e6f5f733aba05c45f06` (`git write-tree` sobre el índice staged con el Change completo y su metadata de cierre).
  - **Delta scoped identity (scope S = las quince rutas del `## Scope`, ordenadas; serialización `scoped-v1`):** `70aba36d32b3d6bceb57d1bc9e4edfd0c5edb00d90417e769d1ebaa85b27bcb0`.
  - **Límite declarado:** el delta se midió sobre el índice staged **antes** de transcribir los dos literales de identidad de este registro y del `Checkpoint`; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140/141/142).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/VERSIONING.md`, `docs/plans/133-roadmap-impact-and-documentary-sweep.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/141-human-decision-backlog-resolution.md`, `docs/plans/142-payload-normative-residuals.md`, `docs/plans/143-empty-remaining-backlog.md`, `docs/plans/INDEX.md`, `protocol/.agents/VERSION`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `runtime/toolcalls/canonical.py`, `tests/test_check_taxonomy_coherence.py`, `tests/test_sae_scope_enforcement_dogfood.py`, `tools/check_taxonomy_coherence.py`.
- **Validity / stale:** vigente; revalidado por A2 sobre el estado de cierre (ver el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` PASS (215 archivos, 10334 referencias); `check_plan_citations` PASS; `check_plan_structure` PASS; `check_taxonomy_coherence` PASS (`exit 0` sobre el corpus real, con la verificación de la H13 regla 11 activa); `check_session_artifacts` PASS; `check_version_state` OK (warnings de secciones sin tag, esperados en `dev`); `python -m pytest tests/` **1120 passed, 0 failed** (el estado de partida daba 1109 passed; +14 son los casos nuevos de la H13 regla 11 y −3 son los conteos preexistentes del corpus, no regresiones); `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; guarda EARS `N/A=1, VALID=3`; C-1 `VALID=49, GAP=0, ANOMALY=0`, C-2 `VALID=48, GAP=1, ANOMALY=0` y C-3 `VALID=27, GAP=0, ANOMALY=0` (el `GAP` de C-2 es el preexistente del Plan 116, que sigue emitiéndose por contrato y no se reabre).

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 143 (GC-1).*

- **Commits de cierre:** el commit atómico del Change, identificado por su mensaje: `fix(protocol): empty the remaining operational backlog (plan 143)`. Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `70aba36d32b3d6bceb57d1bc9e4edfd0c5edb00d90417e769d1ebaa85b27bcb0` / `03f51f6cc5a4968530fe3e6f5f733aba05c45f06`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado como identidad; el commit de cierre incluye governance (este Plan, `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md`), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`).
- **Consistencia checkpoint↔anchor:** PASS — la identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron; C-2 lo verifica sobre el artefacto de este Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 143 y su serie (Septuagésima cuarta) con el estado corriente; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 143, RFC-—)` y la sección `[11.6.1]` del PATCH de payload; `protocol/.agents/VERSION` → `11.6.1` con el ancla `PROTOCOL_VERSION` alineada; entidad `contract:CHANGE_GOVERNANCE.md` registrada en el diccionario maestro; estados de `<PLAN-136>:F-1`, `<PLAN-133>:F-1`, `<PLAN-142>:F-1`, `<PLAN-142>:F-2` y `<PLAN-141>:PC-2` transicionados con bloques append-only; `ROADMAP.md` y `docs/VERSIONING.md` §4.1 reconciliados. Sin RFC ni ADR nuevos, sin tag.
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados: `docs/VERSIONING.md` §4.1 (la enumeración de las reglas de H13 que el checker restaura pasa a `2/5/10/11`), `docs/plans/INDEX.md` (registro del Plan 143, serie y corrección del espejo del plan 25, que declaraba verificado el perfil `trivial`), `ROADMAP.md` (el residuo del plan 25 sale del trabajo pendiente), `CHANGELOG.md` (ítem de gobernanza y sección de la versión) y los bloques de metadata evolucionable de los planes 133/136/141/142. Aspecto afectado: el registro corriente declaraba pendientes cuya condición ya estaba resuelta o mal clasificada, y la nota de la batería describía una cobertura incompleta. `docs/CONVENTIONS.md` y las policies `.agents/` **no** se modifican: la regla aplicable ya existe.
- **Roadmap impact:** `REQUIRED` — reconciliado en la ejecución. El mapa operativo declaraba como pendiente no-payload el dogfood medido del perfil `trivial` (plan 25); este Change determina que es una actividad externa de adopción y la retira del trabajo pendiente, dejando la constancia con su criterio de éxito y su procedimiento. Artefacto que posee el mapa: `ROADMAP.md`. La escritura está autorizada por el `## Scope` de este Plan —declarado, con el pedido del mantenedor como base— y **no** por la determinación de impacto (`.agents/policies/validation-closure.md` §5.2). Ninguna otra entrada del mapa cambia.
- Condición derivada: **`Closed` (payload con release pendiente)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released`: requieren autorización separada del mantenedor.


## Findings / Correcciones / Pending

### Findings

- `<PLAN-143>:F-1` — estado: `resolved` (corregido dentro del `Scope` autorizado por `<PLAN-143>:C-1`, con autorización explícita del mantenedor); observación: la implementación de la H13 regla 11 en el checker de la batería revela una condición **preexistente y genuina** del payload: `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` declara `kind: contract` y **no** tiene entidad `kind: contract` en `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` —sólo la entrada de la sección `# Artifacts` (`kind: artifact`, con puntero `contract:`), tal como la registró el paso 3 del plan 115—, de modo que el diccionario maestro y el archivo no coinciden en la dirección archivo→entidad que la regla exige; el hueco era invisible para la batería porque ninguna verificación mecánica cubría la regla 11, que es exactamente el hueco que `<PLAN-142>:F-1` describía; evidencia original: `python tools/check_taxonomy_coherence.py` con el check 9 recién implementado → `Taxonomy coherence violations: 1` / `- CONTRACT .agents/contracts/CHANGE_GOVERNANCE.md has no kind: contract taxonomy entity (H13 rule 11)` / `exit 1`, frente a `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules` regla 11 y a las líneas 13-18 de `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` (los cuatro campos comparables ya coincidían con la entidad de artefacto, de modo que lo faltante era el registro, no un valor); estado Git observado: `dev` @ `3b0a3218242466d3b7397917424fde0466888849` más los cambios de los Planes 141/142 y el checker extendido, sin commitear; provenance original: Paso 5 (medición del corpus real) de la ejecución del Plan 143 (2026-09-21); resolución: corregido por `<PLAN-143>:C-1` —la entidad `contract:CHANGE_GOVERNANCE.md` se registra con los cinco valores que el contrato y su entidad de artefacto ya declaraban—, previa autorización explícita del mantenedor y con el `## Scope` y la `Clase` declarados **antes** del efecto (`.agents/policies/supervised-autonomous-execution.md` §1.2); el checker pasa a `exit 0` sobre el corpus real. **Frontera respetada:** el agente **no** escribió el payload por inferencia; registró la condición, la escaló y detuvo la escritura hasta la decisión humana.

- `<PLAN-143>:F-2` — estado: `resolved` (corregido por `<PLAN-143>:C-2`); observación: la transición CL-8 legítima de `<PLAN-136>:F-1` sobre un plan **cerrado** —evolucionar el campo `estado` y la `resolución`, que LC-1 declara evolucionables— cambia el digest normativo que `tests/test_sae_scope_enforcement_dogfood.py` fija sobre `docs/plans/136-d01-mechanical-checker.md`: la normalización del test canonicaliza los valores de `estado` y de la `resolución` sólo cuando ésta cierra con `; evidencia:`, y la `resolución` de F-1 queda fuera de esa forma, de modo que el pin deja de coincidir; es el caso que el propio contrato del test declara («recompute it only when a legitimate lifecycle transition changes the canonical content», `tests/AGENTS.md`) y no una edición del contenido histórico; evidencia original: `python -m pytest tests/ -q` → `3 failed, 1117 passed`, con `AssertionError: the closed plan changed outside its evolvable lifecycle metadata` y los digests `380ac29a457dfc615cddbdb8cfac8c43e07ca4d72c7bf38a5d11f2edd384f7f0` (real, recalculado con la propia función del test) frente a `5ef36941f6445d82fb5b4501ca88259a4c8e641677bedc7c37e83a7aa346a40f` (pineado); estado Git observado: `dev` @ `923c32f` (commit del Plan 142) más los cambios del Plan 143 sin commitear; provenance original: Paso 10 (verificación de la batería) de la ejecución del Plan 143 (2026-09-21); resolución: corregido por `<PLAN-143>:C-2`, que actualiza el digest al contenido canónico nuevo y documenta en el docstring del test la tercera transición —sin tocar la lógica de canonicalización, de modo que la protección no se debilita: cualquier edición de una observación, una evidencia, un elemento inmutable o una sección normativa sigue cambiando el digest y fallando—, junto con las tres suites ancladas que la verificación detectó: `test_sae_scope_enforcement_dogfood.py`, `test_repo_containment.py` y `test_check_lifecycle_lineage.py`.

### Correcciones

- `<PLAN-143>:C-1` — refs origen: `<PLAN-143>:F-1`; alcance de revalidación: `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (la entidad registrada), `tools/check_taxonomy_coherence.py` (check 9) y `tests/test_check_taxonomy_coherence.py`, más el corpus completo que consume el checker, la batería canónica y los gates C-1/C-2/C-3; evidencia: `python tools/check_taxonomy_coherence.py` → `Taxonomy coherence OK` (`exit 0`) sobre el corpus real, `python tools/check_protocol_invariants.py --payload protocol .` → `215 files checked, 10334 references verified`, `python tools/check_version_state.py` → `Version state OK` con `VERSION` = `11.6.1`, y `python -m pytest tests/test_check_taxonomy_coherence.py -q` → `28 passed`; carácter: FACTUAL / TRACEABILITY (no normativo; la acción la autoriza este Plan); autorización: `Clase B` de RFC-56 (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`) con plan `Aprobado para ejecución`, justificación documentada y acto explícito del mantenedor registrado en `## Frontera de payload autorizada`; qué se corrigió: el registro faltante —se agrega la entidad `contract:CHANGE_GOVERNANCE.md` con `domain`, `artifact`, `lifecycle`, `produced_by`, `consumed_by` y `file` idénticos a los que el contrato y su entidad de artefacto ya declaraban—, sin cambiar el significado del protocolo, ningún contrato, ninguna máquina de estados ni la compatibilidad con adoptantes.

- `<PLAN-143>:C-2` — refs origen: `<PLAN-143>:F-2` y la verificación de este Change; alcance de revalidación: `tests/test_sae_scope_enforcement_dogfood.py` (constante `CLOSED_PLAN_NORMATIVE_SHA256` y docstring del test anclado), `tests/test_repo_containment.py` y `tests/test_check_lifecycle_lineage.py`, sobre `docs/plans/136-d01-mechanical-checker.md` como sujeto anclado, más la suite completa `python -m pytest tests/ -q`; evidencia: la corrida que detectó los tres fallos (`3 failed, 1117 passed`) y la corrida de cierre registrada en el `## Validation anchor`; carácter: FACTUAL / TRACEABILITY (no normativo); autorización: este Plan (mantenimiento obligatorio de un test anclado cuando el estado canónico del repositorio cambia de forma legítima, `tests/AGENTS.md`); qué se corrigió: la constante del digest —recalculada con la propia función del test sobre el contenido canónico nuevo— y la documentación de la tercera transición de estado en el docstring; la lógica de canonicalización y todas las aserciones de contenido se conservan, de modo que ninguna invariante se relaja. La segunda parte del hallazgo —los objetivos de cita sin trackear— no era un defecto del repositorio sino del orden de ejecución: el registro del Plan 143 se estageó antes de la verificación final y `tests/test_repo_containment.py` volvió a verde sin cambios en el test.

### Pending decisions

- No se registran pending decisions nuevas. Los asuntos que requieren decisión humana conservan su continuidad en las pending decisions **existentes**: `<PLAN-125>:PC-1`/`PC-2`, `<PLAN-137>:PC-2`, `<PLAN-131>:PC-1`/`PC-2` y `<PLAN-138>:PC-2`, todas con owner mantenedor y sin trigger disparado. El residuo de payload que este Change **no** podía escribir por sí mismo no queda como pendiente: se resolvió con la autorización explícita del mantenedor y se registra en `<PLAN-143>:F-1`/`C-1`.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `3b0a3218242466d3b7397917424fde0466888849`,
working tree con el cambio de los Planes 141 y 142 **staged y sin commitear**.

**Estado de partida y su tramitación.** Los Planes 141 y 142 estaban `Executed` con
condición derivada `Closed`, con su trabajo en el índice y **sin** el commit atómico que
sus dos checkpoints declaran. Antes de empezar la superficie propia se commitearon en
`dev`, atómicos por Change y con los mensajes declarados: `73eed8c`
(`docs(governance): resolve the human decision backlog HD-1..HD-12 (plan 141)`) y `923c32f`
(`feat(protocol): materialize the payload normative residuals (plan 142, RFC-79)`). Los
documentos de gobernanza que **ambos** Changes escribieron —`CHANGELOG.md`, `ROADMAP.md`,
`docs/plans/INDEX.md`, `docs/rfc/79-…`, `docs/rfc/INDEX.md` y el campo `PC-1` del Plan
141— se commitearon con el Plan 142, cuya publicación de payload domina su contenido
final, y las dos notas de commit lo declaran: la alternativa habría sido reconstruir un
estado intermedio que ninguna validación respalda.

**Qué se hizo.** Los cuatro residuos, uno por uno. `HD-10`/plan 25: el entregable que
faltaba no es implementable en el repositorio, de modo que se reclasifica como actividad
externa de adopción y sale del backlog; `<PLAN-141>:PC-2` pasa a `resuelta`, el mapa
operativo deja de declararlo pendiente y el espejo del INDEX corrige la fila que
declaraba verificado el perfil `trivial`. `<PLAN-142>:F-1`: la verificación de la H13
regla 11 se implementa en el checker existente con sus casos y falsaciones, y la corrida
sobre el corpus real revela el registro faltante que se resuelve con autorización
explícita del mantenedor. `<PLAN-142>:F-2`/`<PLAN-136>:F-1`: la transición CL-8
autorizada se ejecuta sobre el destino cumplido, con los elementos inmutables verbatim.
`C-2 GAP` del plan 116: la clasificación del Plan 140 se formaliza y el residual de
backlog se resuelve sin tocar el plan 116.

**Frontera de payload, en el orden en que ocurrió.** El contrato de H13 regla 11 se leyó
y el corpus se midió **antes** de escribir el checker, y la medición produjo la condición
preexistente que este Change no anticipaba
(`CONTRACT .agents/contracts/CHANGE_GOVERNANCE.md has no kind: contract taxonomy entity`,
`exit 1`). La escritura de `protocol/.agents/` es una frontera RFC-56 y una stop condition
de SAE: el agente **no** la infirió —registró el hecho, lo escaló y detuvo la escritura—.
El mantenedor la autorizó explícitamente el 2026-09-21 bajo este Change, declarado
`Clase B` con justificación documentada y `## Scope` ampliado. Para que la declaración
**precediera** al efecto (`.agents/policies/supervised-autonomous-execution.md` §1.2), la
entidad se aplicó primero sólo para medir el efecto, se revirtió, se registraron el
`## Scope`, la `Clase` y la justificación, y se volvió a aplicar: el orden final de los
hechos es el que la regla exige, y esta nota declara la secuencia sin ocultarla. La
entidad registrada repite los cinco valores que el contrato y su entidad de artefacto
**ya** declaraban; ningún otro archivo del payload se toca.

**Correcciones detectadas por la verificación.** Cuatro, todas dentro del `Scope` o de la
redacción de este Plan. (a) `<PLAN-143>:F-2`/`C-2`: el digest que
`tests/test_sae_scope_enforcement_dogfood.py` fija sobre el plan cerrado 136 dejó de
coincidir por la transición CL-8 legítima de `<PLAN-136>:F-1` —el contrato del propio
test exige recomputarlo en ese caso—, y se actualizó la constante **sin** tocar la lógica
de canonicalización ni ninguna aserción: la protección no se relaja. (b) Tres citas
introducidas al redactar este Plan (`ruta:sección` con nombre de archivo suelto y una
referencia a líneas con la forma de ancla) fueron detectadas por `check_plan_citations` y
corregidas a rutas repo-relative completas o a prosa. (c) La cita del inventario externo
`MASTER_PENDING_WORK_INVENTORY.md` creaba un objetivo de cita que existe **sólo** como
archivo no versionado, que `tests/test_repo_containment.py` prohíbe (RFC-69 I2): se
conserva la referencia al artefacto externo sin crear el objetivo de cita. (d) El orden de
estageo: el registro del Plan 143 se trackeó antes de la corrida de contención, de modo que
el fallo de esa suite durante la ejecución fue de orden y no de contenido.

**Verificación.** Seis checkers canónicos PASS (`check_protocol_invariants` 215 archivos /
10334 referencias, `check_plan_citations`, `check_plan_structure`,
`check_taxonomy_coherence` —`exit 0` sobre el corpus real con la verificación de la H13
regla 11 activa—, `check_session_artifacts`, `check_version_state` con los warnings de tags
esperados en `dev`); `python -m pytest tests/` **1120 passed, 0 failed**;
`python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; guarda EARS
`N/A=1, VALID=3` (R3/R4/R5 sobre el payload real); `python -m pytest
tests/test_check_taxonomy_coherence.py -q` **28 passed**; C-1 `VALID=49, GAP=0,
ANOMALY=0`, C-2 `VALID=48, GAP=1, ANOMALY=0` (el `GAP` es el preexistente del Plan 116,
que sigue emitiéndose por contrato y no se reabre) y C-3 `VALID=27, GAP=0, ANOMALY=0`.
Corrida previa a la transcripción de la identidad de este registro: C-1 `VALID=48, GAP=1`
y C-2 `VALID=47, GAP=2`, donde el `GAP` extra era la metadata de cierre de este Plan
todavía vacía.

**Fronteras respetadas.** No se creó ningún mecanismo, policy, checker adicional, estado,
registry, authority class ni workflow; no se reabrieron el plan 116, el plan 142, RFC-56,
RFC-75, ADR-15/16 ni C-2/CI; ningún artefacto histórico fue reescrito fuera de su metadata
evolucionable; el plan 116, los planes 25/26/46, `docs/rfc/`, `docs/adr/`, `.agents/`, el
resto de `runtime/` y `dist/` quedan con **0 diff**; no se fabricó ninguna sesión de
usuario, `METRICS.md`, `state.json` ni evidencia de runtime; sin promoción, tag, release ni
push.


