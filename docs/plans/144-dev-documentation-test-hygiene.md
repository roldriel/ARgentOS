# Plan 144 — Higiene documental y de tests del backlog DEV residual (DEV Documentation and Test Hygiene)

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-21
**RFC:** — (vía plan; DEV-only sobre `tests/` y `docs/`, sin efecto en `protocol/.agents/`, por lo que RFC-56 no aplica)
**Clase:** — (sin efecto de payload; ningún archivo de `protocol/.agents/` se toca)
**Change Level:** L1 (`max(coordination=1, scope=1, architectural=0, release=0, duration=1)`: un solo Change coherente bajo una única autorización, con superficie dispersa pero mecánica —un documento de tests, dos suites y tres espejos documentales—, sin decisión arquitectónica, sin release y sin cambio semántico en ningún checker ni contrato)
**Depende de:** plan 124 (`tests/AGENTS.md` y el bootstrap de importación), plan 143 (estado del backlog posterior)
**Origen:** pedido directo del mantenedor (Change «Plan — Resolve DEV Documentation and Test Hygiene Backlog», 2026-09-21), que enumera los tres residuales accionables que dejó abiertos el inventario read-only posterior al Plan 143 —`AW-1`, `AW-2` y `AW-3`— y autoriza su resolución final como un único Change DEV

## Objetivo

Eliminar los tres únicos residuales accionables que el inventario posterior al Plan 143
identificó en el repositorio, de modo que ninguno siga representando trabajo pendiente:

1. **`AW-1`** — el conjunto anclado declarado en `tests/AGENTS.md` no representa el corpus
   real: la tabla enumera ocho módulos y cinco módulos anclados más existen y no figuran en
   ella, tres de los cuales citan esa misma tabla como su contrato.
2. **`AW-2`** — dos suites repiten una manipulación de `sys.path` para `tools/` que el
   bootstrap único de la sesión (`conftest.py`) ya realiza, duplicación que
   `tests/AGENTS.md:Rules` declara y que `<PLAN-124>:C-1` registró como falsada.
3. **`AW-3`** — tres espejos documentales describen un estado que sus propias fuentes
   contradicen: la fila de RFC-75 en `docs/rfc/INDEX.md`, el registro de investigaciones y
   el registro de auditorías.

**El objetivo no es reclasificar ni limpiar el repositorio.** El Change corrige sólo lo que
el inventario identificó como accionable y **no** amplía su alcance a otras inconsistencias
que descubra: las clasifica y las reporta.

**Qué no cambia.** Este Change **no** toca `protocol/.agents/`, no crea ni modifica
mecanismos, policies, checkers, estados, registries, authority classes, taxonomías ni
workflows, **no** reabre el Plan 124, el Plan 143, RFC-56, RFC-79, RFC-75 ni ningún
artefacto cerrado, **no** modifica la semántica de ningún test ni de ningún checker, **no**
cambia `dist/`, **no** promueve, taggea, publica ni empuja, y **no** modifica el inventario
externo `MASTER_PENDING_WORK_INVENTORY.md`.

**Qué sí cambia.** La tabla del conjunto anclado de `tests/AGENTS.md`, la eliminación de
dos `sys.path.insert` redundantes en dos suites, y tres filas de espejo documental. Nada
más.

## Frontera de autoridad

Este Change es un mantenimiento **DEV-only** de documentación y tooling de tests. Su
autoridad es el pedido del mantenedor que lo origina, y cubre exactamente:

1. la corrección del conjunto anclado de `tests/AGENTS.md`;
2. la eliminación de las dos manipulaciones de `sys.path` redundantes;
3. la corrección de los tres espejos documentales identificados;
4. los tests y la verificación necesarios para demostrar esas correcciones.

**No** se requiere ni se concede autoridad de payload: `protocol/.agents/` queda con
**0 diff**. Una necesidad de cambio de payload detiene la ejecución (`STOP_AUTHORITY_REQUIRED`).

**Una determinación de impacto no autoriza una escritura.** Si al verificar aparece un
residual cuyo artefacto dueño está fuera del `Scope` de este Plan, se registra —no se
escribe— y se detiene en la frontera (`.agents/policies/validation-closure.md` §5.1/§5.2;
`<PLAN-136>:PC-4`(a); regla formalizada por el Plan 139 `DEC-2`).

## Criterio de entrada

- [x] Baseline del repositorio identificable: `dev` @ `6a433d14abf24c406a7342a1e11cd7ef3bd6bcec`, working tree limpio salvo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md`.
- [x] Los tres residuales son legibles y se re-verificaron contra el repositorio, no contra el resumen del inventario: el conjunto anclado declara 8 módulos y 5 anclados existen fuera de la tabla; los dos `sys.path.insert` de `tools/` existen; los tres espejos describen estado superado.
- [x] Ningún Change posterior al inventario los resolvió: `git log` desde el Plan 143 (`5484763`, `6a433d1`) no toca `tests/AGENTS.md`, las dos suites de discovery ni los tres espejos.
- [x] La autoridad existe y está vigente: el pedido del mantenedor, más `.agents/policies/validation-closure.md` §4/§5, `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (LC-1)` y `docs/VERSIONING.md:4.1 Batería canónica de verificación`.
- [x] Plan 144 es el próximo número libre, verificado contra `docs/plans/` (último: `143-empty-remaining-backlog.md`) y `docs/plans/INDEX.md`.
- [x] El bootstrap de importación de la sesión de test existe y pone `tools/` en `sys.path`: la raíz `conftest.py`, en su bloque de importación.
- [x] Batería canónica verde sobre el estado de partida (registrada en `## Nota de ejecución`).

## Matriz de investigación (resultado real, no supuesto)

| Residuo | Premisa registrada | Evidencia observada en el repositorio | Acción |
|---|---|---|---|
| `AW-1` | la tabla del conjunto anclado enumera 8 módulos y omite los anclados posteriores | `tests/AGENTS.md` §«The anchored set» enumera 8 filas; existen además `test_placement_dogfood.py`, `test_autonomous_scope_dogfood.py`, `test_sae_scope_enforcement_dogfood.py`, `test_discovery_output_dogfood.py` y `test_check_ears_coverage_dogfood.py`, los cinco anclados y de sólo lectura, y **los cinco citan la tabla como su propio contrato** («This module is in the “tests anchored to the real repository” set of `tests/AGENTS.md`» / «in the sense of `tests/AGENTS.md`»); los tres módulos que se declaran **isolated** (`test_check_discovery_output.py`, `test_check_ears_coverage.py`, `test_check_ears_coverage_falsification.py`) ya no figuran en la tabla y no deben figurar | **Corregir** (§1): completar la tabla con los cinco módulos que el contrato ya define como anclados |
| `AW-2` | dos suites repiten la manipulación de `sys.path` para `tools/` | `tests/test_check_discovery_output.py` y `tests/test_discovery_output_dogfood.py` hacen `sys.path.insert(0, ... / "tools")` en su encabezado; el bootstrap único de la sesión (la raíz `conftest.py`, en su bloque de importación) ya inserta `tools/` (y `tests/`) una sola vez, y `tests/AGENTS.md:Rules` declara que «a per-file `sys.path.insert` is duplication»; `<PLAN-124>:C-1` registró la falsación «0 coincidencias» justo sobre este patrón | **Eliminar** (§2): quitar sólo esas dos sentencias |
| `AW-3(a)` | la fila de RFC-75 en `docs/rfc/INDEX.md` declara implementación pendiente | la columna `Status` de esa fila decía `implementación pendiente`; el header de `docs/rfc/75-change-lifecycle.md` declara `implementación materializada por los Incrementos 0–4 — planes 95–101 … con el Incremento 5 fuera de alcance por decisión de la propia RFC`; el Plan 141 corrigió el header del documento, no el espejo | **Corregir** (§3) |
| `AW-3(b)` | el registro de investigaciones no lista un documento versionado | `docs/working/research/INDEX.md` listaba sólo `INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`; `git ls-files docs/working/research` muestra además `PROMPT_CACHE_PHASE_1_REPORT.md`, versionado desde `a5fa23e` y declarado como `Origen` por `docs/rfc/78-provider-bound-stable-prefix-materialization.md` | **Corregir** (§3) |
| `AW-3(c)` | el registro de auditorías marca la auditoría de sistema como activa | `docs/working/audits/INDEX.md` decía `vigente` / `active (tracker vivo de remediación)`; `docs/working/audits/AUDITORIA_SISTEMA.md` declara en su header `**Status:** All original findings and remediation items resolved (2026-08-14)` y su propio texto aclara que lo restante son «optional future RFCs … not open audit items» | **Corregir** (§3) |

## Determinaciones

### 1. `AW-1` — el conjunto anclado se completa, no se redefine

**Qué define «anclado».** El contrato vigente de `tests/AGENTS.md` §«Two kinds of test, by
repository dependency» ya lo define y **no se cambia**: un test anclado lee el working tree
vivo **a propósito**, es **estrictamente read-only**, y su contrato de estabilidad es que
puede nombrar paths canónicos, números de artefacto y estados del repositorio real, de modo
que se actualiza cuando ese estado canónico cambia de forma legítima. La corrección aplica
esa definición al corpus; no la reinterpreta ni crea categorías.

**Cómo se determinó el conjunto real.** Por lectura de los módulos, no por heurística de
nombres: los trece módulos de la tabla leen el repositorio real (corrida del checker sobre
`REPO_ROOT`, `git ls-files` sobre el árbol, barrido del payload real, snapshots del working
tree) o afirman algo sobre el estado canónico del propio repositorio. Los módulos que
construyen su propio repositorio, payload o fixture y no leen el árbol real quedan fuera; en
particular los tres que se declaran `isolated` en su propio docstring.

**Qué se conserva de la tabla.** Las ocho filas existentes **no se retiran ni se
reescriben**: su entrada, su nombre de test y su descripción de protección se preservan. Se
agregan cinco filas, una por módulo, en el mismo formato (`Test` / `Protects`) y con la
referencia al plan que materializó cada protección. Se conserva tal cual la nota final sobre
`tests/fixtures/skills/`.

**Resultado.** La tabla pasa de **8** a **13** filas. Los cinco módulos que citan la tabla
como su contrato quedan representados en ella, y ningún módulo que se declara `isolated`
aparece en la tabla.

### 2. `AW-2` — se elimina sólo la duplicación de `tools/`, no la manipulación legítima de `runtime/`

**Qué es duplicación y qué no.** El bootstrap único de la sesión (la raíz `conftest.py`, en
su bloque de importación) pone `tests/` y `tools/` en `sys.path` **una sola vez**, y su
propio comentario declara el propósito. Por lo tanto una inserción por archivo que agregue
exactamente `tools/` es duplicación —las dos identificadas—, mientras que una inserción que
agregue la raíz del repositorio **no lo es**: las suites que importan `runtime.toolcalls.*` o
`runtime.orchestrator.*` lo necesitan, porque `conftest.py` no agrega la raíz a `sys.path`.

**Alcance de la corrección.** Se eliminan exactamente dos sentencias y se ajustan sus
imports para que queden al nivel de módulo, sin `noqa: E402`: la de
`tests/test_check_discovery_output.py` y la de `tests/test_discovery_output_dogfood.py`. En
el primer módulo, `sys` se vuelve innecesario y se retira; `Path` **se conserva** porque se
usa como anotación en el resto del archivo. En el segundo, `sys` se conserva (`sys.executable`)
y `Path` se conserva.

**Lo que se deja como está, y por qué.** Las nueve sentencias restantes insertan la raíz del
repositorio para importar `runtime/`; se verificó módulo por módulo que cada una es
**necesaria**, de modo que no son duplicación y **no** entran en el alcance de este Change.
El Change no hace un refactor generalizado de importaciones.

### 3. `AW-3` — tres espejos se reconcilian contra su fuente autoritativa

**Regla aplicada.** Un INDEX es registro/navegación y **nunca** autoridad
(`docs/AGENTS.md`; AU-4). Se corrige el espejo para que describa el estado que su fuente
declara; la fuente **no** se toca.

- **`AW-3(a)`** — la fila de RFC-75 se corrige para reflejar el estado autoritativo que
  declara el header de `docs/rfc/75-change-lifecycle.md`: implementación materializada por los
  Incrementos 0–4 (planes 95–101), Incremento 5 fuera de alcance por decisión de la propia
  RFC. RFC-75 **no** se modifica, su `Status` no cambia y su alcance de implementación no se
  altera. El espejo no se convierte en bitácora: recoge el estado corriente de la RFC, que
  es lo que la columna `Status` del registro expresa.
- **`AW-3(b)`** — se agrega la fila del documento versionado que faltaba, con el formato de
  la tabla (`Archivo` / `Fecha` / `Status`) y sin inventar metadata: la fecha y el status se
  leen de la cabecera del propio informe (`**Fase:** 1 …`, cierre
  `PHASE_1_READY_FOR_HUMAN_DECISIONS`) y de su rol declarado como `Origen` de RFC-78
  (`docs/rfc/78-provider-bound-stable-prefix-materialization.md:7`). RFC-78 **no** se
  modifica y el informe **no** se reclasifica: sigue siendo Working/no normativo.
- **`AW-3(c)`** — la fila de la auditoría de sistema se reconcilia con el estado que la
  propia auditoría declara (`AUDITORIA_SISTEMA.md:3`: todos los hallazgos y la remediación
  resueltos el 2026-08-14; lo restante son RFCs futuros opcionales, no ítems abiertos). Se
  usa el mismo formato de la fila hermana ya archivada
  (`AUDITORIA_SISTEMA_2026-08-16.md`). La auditoría **no** se reescribe para coincidir con el
  índice: se preserva íntegra.

## Entregables

1. `docs/plans/144-dev-documentation-test-hygiene.md` — este Plan, con la matriz, las tres determinaciones, el anchor, el checkpoint y los registros de lineage.
2. `tests/AGENTS.md` — tabla del conjunto anclado completada (8 → 13 filas) y frase de precisión en la regla del bootstrap de importación (el bootstrap no pone la raíz del repositorio en `sys.path`, de modo que la inserción que las suites hacen para importar `runtime.*` no es la duplicación que la regla prohíbe). No cambia la definición de «anclado» ni ninguna otra instrucción.
3. `tests/test_check_discovery_output.py` — eliminación del `sys.path.insert` de `tools/` y del import `sys` que queda sin uso.
4. `tests/test_discovery_output_dogfood.py` — eliminación del `sys.path.insert` de `tools/`.
5. `docs/rfc/INDEX.md` — sólo el `Status` de la fila de RFC-75.
6. `docs/working/research/INDEX.md` — la fila faltante del informe de Phase 1.
7. `docs/working/audits/INDEX.md` — sólo la fila de `AUDITORIA_SISTEMA.md`.
8. `docs/plans/INDEX.md` — registro del Plan 144, su serie y el header de estado.
9. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 144, RFC-—)`.

## Pasos

1. **Observar el estado real (read-only).** Verificar los tres residuales en sus artefactos, el bootstrap de importación de la sesión y el estado Git; construir la matriz sin anticipar resultados.
2. **Correr la batería del estado de partida** y registrar su resultado real.
3. **`AW-1` — determinar el conjunto anclado** por lectura de los módulos y completar la tabla de `tests/AGENTS.md` sin cambiar la definición ni retirar entradas.
4. **`AW-2` — eliminar** las dos sentencias de `sys.path` redundantes y ajustar los imports que quedan sin uso; verificar que ninguna otra inserción de `tools/` sobrevive y que las nueve restantes (raíz del repositorio, para `runtime/`) son necesarias y quedan intactas.
5. **`AW-3` — reconciliar** los tres espejos contra su fuente autoritativa, sin modificar la fuente.
6. **Verificar** las suites afectadas, las trece entradas de la tabla anclada y sus tests nombrados, la batería canónica completa, el harness del payload y los gates C-1/C-2/C-3; registrar anchor y checkpoint; commit atómico en `dev`. Sin push, sin merge, sin tag, sin release y sin promotion.
7. **Barrido final de consistencia** de los tres residuales y clasificación de lo que aparezca fuera de alcance, sin incorporarlo.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el `Scope` es decisión humana.

- `docs/plans/144-dev-documentation-test-hygiene.md` (este Plan)
- `tests/AGENTS.md`
- `tests/test_check_discovery_output.py`
- `tests/test_discovery_output_dogfood.py`
- `docs/rfc/INDEX.md` (sólo el `Status` de la fila de RFC-75)
- `docs/working/research/INDEX.md` (sólo la fila faltante)
- `docs/working/audits/INDEX.md` (sólo la fila de `AUDITORIA_SISTEMA.md`)
- `docs/plans/INDEX.md`
- `CHANGELOG.md`

**Excluido explícitamente:**

- `protocol/.agents/` completo — **0 diff**. Ningún archivo del payload se toca y no se requiere RFC-56.
- `runtime/` — **0 diff**.
- `docs/rfc/75-change-lifecycle.md`, `docs/rfc/78-provider-bound-stable-prefix-materialization.md`, `docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` y `docs/working/audits/AUDITORIA_SISTEMA.md` — **0 diff**: son las fuentes autoritativas que los espejos describen y no se reescriben (RFC-46).
- `docs/adr/` — **0 diff**.
- `docs/VERSIONING.md` — **0 diff**: su snapshot §9 se reconcilia en la promoción/release, no en cada Change (§5.1). El Plan 143 ya tocó §4.1 y no se reabre.
- `ROADMAP.md` — **0 diff**: el mapa operativo ya está en «Sin trabajo activo / Ninguno», y este Change no crea, completa, cancela ni reclasifica trabajo futuro.
- Las nueve sentencias de `sys.path` restantes y los demás módulos de `tests/` — **0 diff**: no son duplicación y quedan fuera del alcance.
- `dist/`, el plan 124, el plan 143, el plan 116 y el inventario externo `MASTER_PENDING_WORK_INVENTORY.md` — **0 diff**.
- Cualquier otra inconsistencia que aparezca — se clasifica en el informe y **no** se incorpora al alcance.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–7 de este Plan: observar read-only los tres residuales; completar la tabla del conjunto anclado de `tests/AGENTS.md` con los cinco módulos que el contrato ya define como anclados (8 → 13 filas) sin cambiar la definición, retirar entradas ni tocar las instrucciones; eliminar exactamente los dos `sys.path.insert` redundantes de `tools/` en `tests/test_check_discovery_output.py` y `tests/test_discovery_output_dogfood.py` con el ajuste de imports que corresponda, dejando intactas las nueve inserciones legítimas de la raíz del repositorio; reconciliar los tres espejos (`docs/rfc/INDEX.md` fila RFC-75, `docs/working/research/INDEX.md` fila faltante, `docs/working/audits/INDEX.md` fila de `AUDITORIA_SISTEMA.md`) contra la fuente autoritativa sin modificar la fuente; registrar el Plan y su serie en `docs/plans/INDEX.md` y el ítem en `CHANGELOG.md`; verificar las suites afectadas, los tests nombrados de la tabla anclada, la batería canónica, el harness del payload y los gates C-1/C-2/C-3; registrar anchor y checkpoint; commit atómico en `dev`. **No** crear mecanismo, policy, checker, estado, registry, authority class ni workflow nuevos; **no** modificar `protocol/.agents/`, `runtime/`, `docs/adr/`, `dist/`, `ROADMAP.md`, `docs/VERSIONING.md`, RFC-75, RFC-78, el informe de Phase 1, la auditoría de sistema, el plan 124 ni el plan 143; **no** hacer un refactor generalizado de importaciones ni una limpieza documental general; **no** promover, taggear, publicar, empujar ni inventar evidencia.
- **Scope:** las rutas enumeradas en `## Scope`.
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera del `Scope`.
  - **`STOP_FORBIDDEN_AUTONOMY`** — release, promotion, tag, push, `dist/`, reescritura de un artefacto cerrado o de una fuente autoritativa.
  - **`STOP_AUTHORITY_REQUIRED`** — cualquier cambio de `protocol/.agents/`: es frontera de payload y sigue su propia vía RFC-56. Si la corrección revelara una necesidad de payload, se registra como finding con su pending decision y se detiene; **no** se escribe el payload.
  - **`STOP_AUTHORITY_REQUIRED`** — convertir la inferencia del agente en decisión humana: la definición de «anclado» se lee del contrato vigente; no se inventa una categoría nueva.
  - **`STOP` (`ANOMALY`)** — cualquier `ANOMALY` de la batería o de C-1/C-2/C-3 que la ejecución no pueda resolver dentro del `Scope`.
- **Autoridad:** este Plan y el pedido del mantenedor que lo origina. Ninguna otra.

## Stop conditions

Además de las de `.agents/policies/supervised-autonomous-execution.md` §5, este Change se
detiene y escala —sin resolver por inferencia— si:

1. completar el conjunto anclado exigiera modificar un módulo de test más allá de las dos
   sentencias de `sys.path` identificadas, o cambiara la definición de «anclado» en lugar de
   aplicarla;
2. reconciliar un espejo exigiera reescribir su fuente autoritativa en lugar de describirla;
3. apareciera un residual accionable cuyo artefacto dueño esté fuera del `Scope`: se registra
   con su continuidad y **no** se escribe.

## Criterios de salida

- [ ] La tabla del conjunto anclado de `tests/AGENTS.md` representa el corpus real (13 módulos), sin retirar ninguna entrada previa, sin cambiar la definición de «anclado» y sin alterar las demás instrucciones del archivo.
- [ ] Los cinco módulos que citan la tabla como su contrato están representados en ella; ningún módulo declarado `isolated` figura en la tabla.
- [ ] Las dos sentencias `sys.path.insert` de `tools/` fueron eliminadas y ninguna otra manipulación de `tools/` sobrevive en `tests/`.
- [ ] Las dos suites afectadas pasan, y la suite completa no registra regresiones.
- [ ] Los tres espejos describen el estado que declara su fuente; ninguna fuente autoritativa cambió.
- [ ] Batería canónica en verde; harness del payload en verde; C-1/C-2/C-3 con `ANOMALY=0`, `BOUNDARY=0` y sin `GAP` nuevo (el `GAP` de C-2 sobre el plan 116 sigue emitiéndose como comportamiento contractual histórico).
- [ ] Determinaciones de Documentation impact y Roadmap impact registradas de forma independiente y con evidencia.
- [ ] `protocol/`, `runtime/`, `docs/adr/`, `dist/`, `ROADMAP.md` y `docs/VERSIONING.md`: **0 diff**.
- [ ] Anchor, checkpoint y nota de ejecución registrados; commit atómico en `dev`.

## Verificación

```bash
python -m pytest tests/ -q
python -m pytest protocol/.agents/harness/tests/ -q
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación específica de este Change:

```bash
python -m pytest tests/test_check_discovery_output.py tests/test_discovery_output_dogfood.py -q
python -m pytest tests/test_placement_dogfood.py tests/test_autonomous_scope_dogfood.py tests/test_sae_scope_enforcement_dogfood.py tests/test_check_ears_coverage_dogfood.py tests/test_prompt_cache_dogfood.py tests/test_repo_containment.py tests/test_pytest_isolation.py -q
python -m pytest tests/test_check_lifecycle_anchor.py::test_real_repo_expected_classifications tests/test_check_lifecycle_checkpoint.py::test_real_repo_expected_classifications tests/test_check_lifecycle_lineage.py::test_t27_real_repo_dogfooding tests/test_check_plan_structure.py::test_real_repo_has_no_violations tests/test_check_protocol_invariants.py::test_source_layout_documents_intentionally_broken_links -q
git diff HEAD --name-only -- protocol/ runtime/ docs/adr/ dist/ ROADMAP.md docs/VERSIONING.md docs/rfc/75-change-lifecycle.md docs/rfc/78-provider-bound-stable-prefix-materialization.md docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md docs/working/audits/AUDITORIA_SISTEMA.md
git diff HEAD --stat
```

La cuarta corrida debe dar **0 diff**; la quinta debe mostrar **sólo** las rutas del
`## Scope`.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 144 (VC-1).*

- **Declared scope:** las rutas del `## Scope` (nueve archivos: `CHANGELOG.md`, `docs/plans/144-dev-documentation-test-hygiene.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/working/audits/INDEX.md`, `docs/working/research/INDEX.md`, `tests/AGENTS.md`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`).
- **Validation command-set:** el de `## Verificación` (batería canónica completa, suite `tests/`, harness del payload, gates C-1/C-2/C-3 y las corridas específicas de este Change).
- **Effective inputs (repo content):** el scope declarado, `conftest.py` (el bootstrap de importación), la suite `tests/` completa, el payload que consume el harness, el corpus de `docs/plans/` y `docs/rfc/` y el árbol de `docs/working/`.
- **Observed dependencies:** `git` (identidad de contenido y estado de sólo lectura), `python` (intérprete de los checkers y de las suites); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14.3; git 2.55.0.windows.5; sin red.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `fe2f28a08c968ab8541661aaab9e2d0683d79213` (`git write-tree` sobre el índice staged con el Change completo).
  - **Delta scoped identity (scope S = las nueve rutas del `## Scope`, ordenadas; serialización `scoped-v1`):** `c05924d6d226e7309d9b099196d0bee3e5c3fc618e9e765f4669a6816dd71297`.
  - **Límite declarado:** el delta se mide sobre el índice staged **antes** de transcribir los literales de identidad de este registro y del `Checkpoint`; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140/141/142/143).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/plans/144-dev-documentation-test-hygiene.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/working/audits/INDEX.md`, `docs/working/research/INDEX.md`, `tests/AGENTS.md`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`.
- **Validity / stale:** vigente.

*Resultado real de la ejecución:* **estado de partida** — `check_protocol_invariants` PASS (215 archivos, 10334 referencias); `check_plan_citations` PASS; `check_plan_structure` PASS; `check_taxonomy_coherence` PASS (`exit 0` sobre el corpus real); `check_session_artifacts` PASS; `check_version_state` OK (warnings de secciones sin tag, esperados en `dev`); `python -m pytest tests/` **1120 passed, 0 failed**; `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; C-1 `VALID=49, GAP=0, ANOMALY=0`, C-2 `VALID=48, GAP=1, ANOMALY=0` y C-3 `VALID=27, GAP=0, ANOMALY=0`. **Estado de cierre** — `check_protocol_invariants` PASS (215 archivos, 10334 referencias); `check_plan_citations` PASS; `check_plan_structure` PASS; `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` OK; `python -m pytest tests/` **1120 passed, 0 failed** (sin regresiones: el recuento es idéntico al del estado de partida, porque este Change no agrega ni retira casos de test y las dos suites afectadas conservan sus 62 casos, 62 passed); `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; C-1 `VALID=50, GAP=0, ANOMALY=0`, C-2 `VALID=49, GAP=1, ANOMALY=0` y C-3 `VALID=28, GAP=0, ANOMALY=0` (el `GAP` de C-2 es el preexistente del Plan 116, que sigue emitiéndose por contrato y no se reabre; los `VALID` suben en uno porque el Plan 144 entra al régimen).

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 144 (GC-1).*

- **Commits de cierre:** uno (1) commit en `dev`, identificado por su mensaje: `docs(dev): resolve the DEV documentation and test hygiene backlog (plan 144)`. Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `c05924d6d226e7309d9b099196d0bee3e5c3fc618e9e765f4669a6816dd71297` / `fe2f28a08c968ab8541661aaab9e2d0683d79213`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado como identidad; el commit de cierre incluye governance (este Plan, `docs/plans/INDEX.md`, `CHANGELOG.md`), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`).
- **Consistencia checkpoint↔anchor:** PASS — la identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron; C-2 lo verifica sobre el artefacto de este Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 144 y su serie (Septuagésima quinta) con el estado corriente; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 144, RFC-—)`; los tres espejos documentales reconciliados; la tabla del conjunto anclado de `tests/AGENTS.md` completa. Sin RFC, sin ADR, sin payload, sin `VERSION` bump, sin tag.
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados: `tests/AGENTS.md` (el conjunto anclado declarado no representaba el corpus real: 8 filas frente a 13 módulos anclados, con tres de los omitidos citando la tabla como su propio contrato), `docs/rfc/INDEX.md` (el `Status` de la fila de RFC-75 declaraba implementación pendiente contra el header corregido de la RFC), `docs/working/research/INDEX.md` (faltaba un documento versionado que es `Origen` de RFC-78) y `docs/working/audits/INDEX.md` (la fila de la auditoría de sistema la declaraba viva contra su propio banner de cierre). `docs/plans/INDEX.md` y `CHANGELOG.md` se actualizan como registro del Change. Aspecto afectado: espejos documentales que describían un estado superado por su propia fuente. `docs/VERSIONING.md` **no** se modifica: su snapshot §9 se reconcilia en la promoción/release y este Change no tiene impacto explícito sobre él. Las fuentes autoritativas (`docs/rfc/75-…`, `docs/rfc/78-…`, el informe de Phase 1 y `AUDITORIA_SISTEMA.md`) **no** se modifican.
- **Roadmap impact:** `NOT_REQUIRED` — razón explícita ligada al alcance real: este Change no crea, completa, cancela, reclasifica ni re-prioriza trabajo futuro. Los tres residuales que corrige son higiene documental y de tests; el mapa operativo ya declaraba «Sin trabajo activo» y «Pendientes que requieren autorización: Ninguno» desde los Planes 141–143, y ninguna entrada del mapa cambia de estado. El artefacto que se actualiza es el registro de planes (`docs/plans/INDEX.md`), que es su fuente de verdad, no `ROADMAP.md`.
- Condición derivada: **`Closed` (docs-only + tooling DEV, sin release)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released`: requieren autorización separada del mantenedor.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A. Las dos observaciones que la ejecución produjo y que quedan
**fuera** del alcance —el bucket `Future Extensions sin nivel asignado` de
`docs/plans/INDEX.md` y el borrador escalado que vive en el staging ignorado— se clasifican en
la Nota de ejecución y **no** se incorporan al Change: no son residuales introducidos por él
y su corrección no está autorizada por este Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia: la ejecución no detectó ningún defecto
propio dentro del `Scope` que exigiera una corrección posterior a la verificación.

### Pending decisions

No se registran pending decisions nuevas. Este Change no abre ninguna decisión: la
definición de «anclado» se lee del contrato vigente y su aplicación al corpus no requiere
autoridad adicional; los tres espejos se reconcilian contra una fuente que ya declara el
estado.

## Riesgos

- **Ampliar la tabla con módulos que no son anclados.** Mitigación: el conjunto se determinó por lectura de los módulos (lectura del árbol real, corridas sobre `REPO_ROOT`, `git ls-files`, barridos del payload), no por nombre; los tres módulos que se declaran `isolated` se verificaron y quedan fuera.
- **Retirar una entrada para evitar documentarla.** Mitigación: las ocho filas previas se preservan sin cambios; sólo se agregan cinco.
- **Eliminar una inserción de `sys.path` que sí era necesaria.** Mitigación: se verificó módulo por módulo que las nueve restantes insertan la raíz del repositorio para importar `runtime/`, que `conftest.py` no agrega; sólo se retiran las dos que agregan `tools/`.
- **Convertir la corrección de espejos en una reescritura de la fuente.** Mitigación: `docs/rfc/75-…`, `docs/rfc/78-…`, el informe de Phase 1 y la auditoría de sistema quedan con **0 diff** y la verificación lo comprueba.
- **Ampliar el alcance a otras inconsistencias.** Mitigación: el barrido final clasifica lo que aparezca y **no** lo incorpora; una necesidad fuera del `Scope` detiene la ejecución.

## Trazabilidad

Inventario read-only posterior al Plan 143 (`AW-1`, `AW-2`, `AW-3`; artefacto externo,
untracked, no autoridad) → **Plan 144 (este Plan)**. `AW-1` → `tests/AGENTS.md:Two kinds of
test, by repository dependency` + los cinco módulos anclados que citan la tabla + el
precedente del plan 124 (`<PLAN-124>:F-2`). `AW-2` → `conftest.py` (bootstrap de importación)
+ `tests/AGENTS.md:Rules` + `<PLAN-124>:C-1`. `AW-3(a)` → `docs/rfc/75-change-lifecycle.md`
(header corregido por el Plan 141) → `docs/rfc/INDEX.md`. `AW-3(b)` →
`docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` → el `Origen` de
`docs/rfc/78-provider-bound-stable-prefix-materialization.md`.
`AW-3(c)` → el `Status` de `docs/working/audits/AUDITORIA_SISTEMA.md` → `docs/working/audits/INDEX.md`.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `6a433d14abf24c406a7342a1e11cd7ef3bd6bcec`,
working tree limpio salvo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md`.

**Qué se hizo.** Los tres residuales, uno por uno. `AW-1`: el conjunto anclado se determinó
por lectura de los módulos —no por heurística de nombres— y la tabla de `tests/AGENTS.md`
pasó de 8 a 13 filas; las ocho entradas previas se preservaron sin cambios, los cinco
módulos anclados que citan la tabla como su contrato quedaron representados, y los tres
módulos que se declaran `isolated` se verificaron y quedaron fuera. `AW-2`: se eliminaron
las dos sentencias `sys.path.insert` de `tools/` y se ajustaron los imports (`sys` dejó de
importarse en `tests/test_check_discovery_output.py`, donde quedó sin uso; `Path` se
conservó en los dos módulos porque se usa como anotación y como `sys.executable`
respectivamente); las nueve inserciones restantes se verificaron **necesarias** —agregan la
raíz del repositorio para importar `runtime.toolcalls.*` y `runtime.orchestrator.*`, que el
bootstrap de la sesión no agrega— y quedaron intactas. `AW-3`: los tres espejos se
reconciliaron contra su fuente autoritativa, que quedó con **0 diff**.

**Observación registrada durante `AW-2` y resuelta como precisión dentro del archivo ya en
alcance.** La regla del bootstrap de `tests/AGENTS.md` describía que el `conftest.py` raíz
pone `tests/` y `tools/` en `sys.path`; la verificación de las nueve inserciones restantes
mostró que la regla era correcta pero **incompleta**: el bootstrap no agrega la raíz del
repositorio, de modo que una inserción que la agregue para importar `runtime.*` no es la
duplicación que la regla prohíbe. Se agregó esa frase de precisión al mismo punto, sin
cambiar la regla ni la definición de «anclado». La corrección es documental y no altera el
comportamiento de ningún test.

**Observaciones clasificadas y NO incorporadas al alcance.** (a) `docs/plans/INDEX.md`
conserva el bucket `Future Extensions sin nivel asignado` con cuatro modelos de RFC-00YA/00YB
que el mapa operativo nunca recogió: los propios RFC declaran esas extensiones como futuras,
de modo que se clasifican **EXPLICITLY DEFERRED** (sin trabajo accionable) más una
inconsistencia de responsabilidad entre registro y mapa, ajena a los tres residuales de este
Change. (b) `sessions/drafts/PROMPT_CACHE_PHASE_2_INTAKE_AND_CLASSIFICATION.md` — un
borrador escalado en el staging ignorado con baseline `dev @ 4314d5e` / `VERSION` 11.4.0,
superado por la RFC-78 y el Plan 121: se clasifica **HISTORICAL / NON-ACTIONABLE**. Ninguna
de las dos se corrige: no son residuales de este Change y su corrección no está autorizada
por este Plan.

**Verificación.** Seis checkers canónicos PASS (`check_protocol_invariants` 215 archivos /
10334 referencias, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
`check_session_artifacts`, `check_version_state` con los warnings de tags esperados en `dev`);
`python -m pytest tests/` **1120 passed, 0 failed**; `python -m pytest
protocol/.agents/harness/tests/ -q` **109 passed**; las dos suites afectadas **62 passed**;
los siete módulos anclados de cuerpo completo **73 passed**; los cinco tests nombrados de la
tabla anclada **5 passed**; C-1 `VALID=50, GAP=0, ANOMALY=0`, C-2 `VALID=49, GAP=1,
ANOMALY=0` y C-3 `VALID=28, GAP=0, ANOMALY=0`. Durante la construcción del registro, la
corrida intermedia mostró `ANOMALY=1` en C-1 y `GAP=2` en C-2: eran los marcadores de
identidad y de checkpoint todavía sin transcribir en este Plan, y desaparecieron al
completarlos. El `GAP` de C-2 sobre el plan 116 es el histórico, sigue emitiéndose por
contrato y no se reabre.

**Fronteras respetadas.** No se creó ningún mecanismo, policy, checker, estado, registry,
authority class, taxonomy ni workflow nuevos; `protocol/.agents/`, `runtime/`, `docs/adr/`,
`dist/`, `ROADMAP.md` y `docs/VERSIONING.md` quedan con **0 diff**; las fuentes autoritativas
que los espejos describen (`docs/rfc/75-…`, `docs/rfc/78-…`, el informe de Phase 1 y
`AUDITORIA_SISTEMA.md`) quedan con **0 diff**; no se tocó ningún artefacto cerrado ni el
inventario externo `MASTER_PENDING_WORK_INVENTORY.md`; no se promovió, taggeó, publicó ni
empujó; no se hizo ningún refactor generalizado de importaciones ni ninguna limpieza
documental general.
