# Plan 136 — D01 Mechanical Checker (DEV checker del subconjunto mecánico de D01)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; DEV-only: `tools/` + `tests/`, sin efecto en `protocol/.agents/`; RFC-56 no aplica. D01 declara la validación mecánica como extensión futura posible y nada del payload distribuido depende de ella: `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` §Implementation Note)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L2 (coordinación 1 agente; scope: `tools/` + `tests/`, dos artefactos nuevos; impacto arquitectónico: ninguno — es un checker DEV más, con la infraestructura existente; sin impacto de release; duración 1 sesión)
**Depende de:** plan 135 (SAE, habilita la ejecución autónoma), plan 60 (modelo D01: no hay runner; la validación mecánica es extensión futura), plan 47 + RFC-48 (D01 ítem 12 resuelve secciones exclusivamente desde los contratos), plan 53 + RFC-54 (`## Project Shape` en lugar de «primera línea»), plan 40 + RFC-41 (D01 valida las entradas en `knowledge/discovery/` sin artefacto-puente)
**Origen:** `ROADMAP.md:Trabajo activo / dogfood` — «Mechanical D01 subset — DEV checker for discovery output structure and provenance» (`B-1` derivado, próximo dogfood); reconstrucción de intake de este Plan (sección «Reconstrucción»)

## Reconstrucción: qué es D01 hoy

Reconstruido contra el repositorio en `8489b89` (baseline de este Change), no inferido del diseño histórico.

**Qué es D01.** D01 es una **harness policy del payload**, no código: `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`, trigger `D01`, transición `DISCOVERY_VALIDATE → DISCOVERY_READY`, el **único gate de validación del dominio discovery** (el trigger core `H10` valida `KB_RECOMMENDATION.md` en `core:GATHERING_CONTEXT` y no participa del ciclo). Su `Purpose` declara que cubre **dos** cosas: validación **estructural** (entradas y manifest conformes a sus contratos) y **ground truth** (toda claim con fuente real; el merge de `synthesis_worker` sin inconsistencias).

**Estado actual real.** El runner del harness **no existe** (plan 60): los 12 ítems de D01 se evalúan hoy por **juicio del Orchestrator**, todos declarados `[agent]`. El propio contrato declara los ítems de estructura determinista (existencia de entradas, existencia de paths de `source_files`, campos y secciones requeridas) como **candidatos `[gate]`** «objetivamente chequeables sin interpretación si una implementación futura restaura los chequeos mecánicos». Eso es exactamente el subconjunto que este Plan autoriza implementar.

**Origen del ítem del Roadmap.** `B-1` histórico (fricción `F-11`: el gate D01 no era superable porque el runner resolvía `artifact_validated: KB_DISCOVERY_ENTRY.md` dentro de la iteración de sesión mientras las entradas viven en `.project/knowledge/discovery/`) quedó **resuelto** por los planes 40 y 47; lo que sigue es **trabajo derivado nuevo**, una extensión que el propio contrato admite, no la reapertura de `B-1`.

**Contratos que D01 verifica.** `KB_DISCOVERY_ENTRY.md` (contrato base: front matter TOML obligatorio con `artifact`, `kind`, `title`, `generated_at`, `tags`, `source_files`; secciones `# <Title>`, `## Summary`, `## Discovered Facts`; el `#` debe coincidir con `title`; `system_probe` es fuente válida **solo** para entradas de environment), los **21 contratos por entrada** (`STACK.md`, `DEPENDENCIES.md`, `ARCHITECTURE.md`, `EXECUTIVE_SUMMARY.md`, …) que definen secciones adicionales por tipo, y `DISCOVERY_MANIFEST.md` (TOML: `[knowledge_base]` con `project_shape` entre `library|cli|service|application|monorepo|unknown`, `[hashes]`, `[entries]` con `active`/`stale`, `[workers]`; `[runtime]` opcional).

**Ubicación de los artefactos.** `.project/knowledge/discovery/*.md` y `.project/knowledge/discovery/.discovery_manifest` (el marcador `.last_discovery` vive en `.project/.last_discovery`; el de `knowledge/discovery/` está deprecado).

**Contradicción histórica que se conserva como evidencia.** El `#` de la policy D01 declara `artifact = "KB_DISCOVERY_ENTRY.md"` y `artifact_validated: KB_DISCOVERY_ENTRY.md`, mientras su §Input enumera las entradas reales en `.project/knowledge/discovery/*.md`. Es la fricción `F-11`, resuelta funcionalmente por el plan 40 (la policy valida las entradas directamente, sin puente). Se conserva sin tocar: `protocol/.agents/` no se modifica en este Change ni en la ejecución de D01.

**Decisiones ya tomadas (no se reinterpretan).** No hay runner en el harness y la validación mecánica es una extensión futura posible, no parte del payload distribuido (plan 60). D01 resuelve las secciones requeridas **exclusivamente desde los contratos**, sin lista propia (plan 47, RFC-48). `## Project Shape` es la primera sección de contenido, no la «primera línea» literal (plan 53, RFC-54). Las entradas se validan directamente en `knowledge/discovery/` (plan 40, RFC-41).

**Decisiones abiertas (registradas, no resueltas aquí).** `F-16` (`project_shape: unknown` pierde información real en repos documentales/protocolo; requeriría enmendar el modelo de clasificación) y `F-17` (`source_files` no tiene un valor de procedencia para ausencias y hechos de árbol; requeriría un valor «observado por scan» en el contrato). **Ambas son de payload y no se resuelven en este Change ni en D01**; D01 las registra como fronteras declaradas (§«Frontera: lo que D01 no decide»).

## Objetivo

Implementar un **checker DEV** que materialice el **subconjunto mecánico y determinista** de D01 —estructura y procedencia resoluble— sobre `.project/knowledge/discovery/`, consumiendo los contratos del payload como **datos de sólo lectura**, y reportando con el vocabulario de señales y el contrato de exit codes que el repositorio ya usa.

El objetivo **no** es reimplementar D01: el juicio sobre ground truth, las claims y el merge permanece donde está. El objetivo es que la parte de D01 que es objetivamente chequeable deje de depender de la inspección manual, sin crear mecanismos nuevos.

**Este Plan se aprueba sólo para redacción.** Su `**Status:**` es `Aprobado para redacción`: **no** está autorizado para ejecución. La autorización de ejecución es una decisión humana posterior e independiente (ver §«Criterio de entrada»).

## Problema

Hoy la validación estructural y de procedencia de discovery es **juicio declarado**, no verificación reproducible: el contrato afirma que las entradas y el manifest cumplen sus contratos y que todo `source_files` existe, pero **nada lo comprueba**. Consecuencias verificables en el corpus histórico:

- El mismo gate falló de forma no superable por un defecto de resolución de artefactos, y se salvó con un artefacto-puente inventado en cada ejecución (`F-11`, crítica, planes 19/40).
- Entradas con rutas absolutas de otra máquina circularon en la KB legada (`F-21`), y hechos de ausencia/tree no tenían forma de declarar procedencia (`F-17`).
- `project_shape: unknown` degradó `api.md` y omitió `distribution.md` sin que nada lo señalara (`F-16`).

El riesgo que D01-MC ataca es concreto y acotado: **una KB publicada con estructura inválida o con procedencia irresoluble se consume como contexto en sesiones futuras**, y hoy eso sólo se detecta por inspección.

## Contrato

La regla verificada es la que **ya existe** y está publicada, leída como dato:

| Regla | Fuente normativa |
|---|---|
| Front matter TOML obligatorio y campos requeridos del entry | `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter` |
| `artifact` = `KB_DISCOVERY_ENTRY.md`, `kind` = `snapshot` | `…contracts/KB_DISCOVERY_ENTRY.md:Completion Criteria` |
| El `#` del cuerpo coincide con `title` | `…contracts/KB_DISCOVERY_ENTRY.md:Completion Criteria` |
| `## Discovered Facts` presente | `…contracts/KB_DISCOVERY_ENTRY.md:Completion Criteria` |
| `system_probe` válido sólo para entradas de environment | `…contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` |
| Secciones adicionales por tipo de entrada | los 21 contratos per-entry `…contracts/<ENTRY_TYPE>.md:Required sections` |
| `## Project Shape` como primera sección de contenido, coincidente con el manifest | `…contracts/EXECUTIVE_SUMMARY.md:Required sections` |
| Secciones y campos del manifest; `project_shape` en su enum | `…contracts/DISCOVERY_MANIFEST.md:Required sections` |
| Las entradas se validan directamente en `knowledge/discovery/` | `…policies/D01-discovery-output.md:Input` (resolución de `F-11`, plan 40) |

**No se crea ninguna regla nueva.** Si la implementación y los contratos discrepan, **gobiernan los contratos** y el defecto de la implementación se escala y se corrige; jamás se reconcilia reinterpretando el contrato.

## Naturaleza mecánica: qué es determinista y qué no

**Determinista (entra en D01-MC).** Todas estas se deciden leyendo bytes y comparando, sin interpretar significado:

1. existencia y no-vaciedad de cada entrada y del manifest;
2. front matter TOML parseable y delimitado;
3. presencia y tipo de los campos requeridos del entry;
4. `artifact` = `KB_DISCOVERY_ENTRY.md` y `kind` = `snapshot`;
5. coincidencia `#` ↔ `title`;
6. presencia de `## Discovered Facts` y de las secciones requeridas por el contrato del tipo;
7. existencia de cada path de `source_files` en el proyecto, con `system_probe` admitido **sólo** para entradas de environment;
8. `[entries] active` ↔ archivos presentes (bidireccional) y `stale` sin contradicción;
9. coherencia de front matter entrada ↔ manifest;
10. `## Project Shape` presente, primera sección de contenido, y coincidente con `[knowledge_base] project_shape`;
11. presencia condicional de `distribution.md` cuando `project_shape` es `library` o `cli`.

**No determinista — NO se convierte artificialmente en checker.** Es juicio y permanece juicio:

| Ítem de D01 | Por qué no es mecánico |
|---|---|
| 1 (stack real), 2 (dependencias reales) | exige decidir si un hecho «proviene» de un archivo de configuración |
| 3 (patrones con ejemplo verificable) | exige juzgar qué cuenta como ejemplo del patrón |
| 4 (environment sin secretos) | la detección de secretos es heurística, no decidible |
| 6 (claims sin fuente) | exige interpretar qué es una claim cualitativa |
| 7 (merge consistente) | exige comparar significado entre entradas |
| 11 (api.md coincide con el shape) | exige interpretar el contenido de `api.md` |

**Frontera registrada como hallazgo del Plan, no resuelta:** `F-17`. El ítem 5 de D01 exige que todo `source_files` exista, pero `containers.md`/`database.md` declaran **ausencias** y `file_map.md` declara **hechos de árbol**, y no existe un valor de procedencia normativo que los represente (`system_probe` sólo es legal para environment). D01-MC **no marca esas entradas como inválidas ni las exime por criterio propio**: reporta la claim con procedencia no resoluble y la clasifica `GAP` (evidencia faltante, advisory), nunca `ANOMALY`. Resolver la ausencia de un valor de procedencia es un cambio de contrato de payload y requiere autorización propia.

**Frontera declarada:** `F-16`. `project_shape` en su enum es mecánicamente chequeable, pero **qué shape corresponde** a un repositorio documental/protocolo es una enmienda al modelo de clasificación (payload). D01-MC acepta los seis valores del enum y no decide el correcto.

## Input

- `.project/knowledge/discovery/*.md` — entradas de la KB (incluido `executive_summary.md`).
- `.project/knowledge/discovery/.discovery_manifest` — manifest TOML.
- Los contratos del payload, **como datos de sólo lectura**: `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`, los 21 contratos per-entry y `DISCOVERY_MANIFEST.md`.
- El árbol del proyecto bajo `--root`, para resolver la existencia de cada path de `source_files`.

Resolver los requisitos **desde los contratos** (no desde una lista propia) es obligatorio: el ítem 12 de D01 declara que D01 «does not maintain a section list of its own» (plan 47, RFC-48). Incrustar las secciones en el checker reintroduciría la violación single-source que el plan 47 eliminó.

## Output

- **Formato:** el reporte de texto que ya usan los checkers del repositorio (una línea por artefacto inspeccionado con su señal y su razón, más una línea `Summary:`), y `--json` opcional para consumo mecánico. **No se inventa formato nuevo.**
- **Vocabulario de señales:** el existente (`.agents/policies/lifecycle-checkers.md`, `.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`) — `VALID`, `GAP`, `ANOMALY`, `BOUNDARY`, `N/A`. Sin sinónimos nuevos.
- **Contrato de exit codes:** el de los checkers existentes — `0` cuando no hay `ANOMALY` (**`GAP` es advisory y nunca cambia el exit code**), `1` ante al menos un `ANOMALY`, `2` ante error de lectura irrecuperable.
- **Clasificación por hallazgo:**

| Situación | Señal |
|---|---|
| Todo conforme | `VALID` |
| Evidencia faltante o no resoluble (path de `source_files` no existe; procedencia de ausencia/tree bajo `F-17`) | `GAP` |
| Contradicción verificable (`#` ≠ `title`; `artifact`/`kind` incorrectos; manifest ↔ archivos incoherentes; `project_shape` del manifest ≠ el de `executive_summary.md`; campo requerido de tipo incorrecto) | `ANOMALY` |
| Ambigüedad estructural (entrada sin contrato reconocible para su tipo; manifest sin `project_shape`) | `BOUNDARY` (revisión humana, nunca adivinada) |
| Ausencia declarada (no hay `.project/knowledge/discovery/`, o no hay entradas) | `N/A` — es válido, no un fallo (precedente: `check_session_artifacts.py`, «sin `.project/` es OK») |

- **Ausencia de información:** nunca se convierte en evidencia positiva. Un manifest ausente es `GAP`/`N/A` declarado, jamás `VALID` por vacío.
- **Estado inválido:** un artefacto presente pero corrupto (TOML no parseable, front matter sin delimitar) es `ANOMALY`, nunca excepción no controlada ni `PASS`.
- **Determinismo:** la salida depende sólo del contenido inspeccionado; mismo input ⇒ mismo output byte a byte. Sin reloj, sin red, sin orden de filesystem no determinista, sin estado.

## Scope

Rutas que la ejecución de D01 queda autorizada a crear o modificar — **exactamente estas, nada más**:

```text
tools/check_discovery_output.py
tests/test_check_discovery_output.py
tests/test_discovery_output_dogfood.py
docs/plans/136-d01-mechanical-checker.md
docs/plans/INDEX.md
CHANGELOG.md
```

Reglas del scope, para que SAE pueda verificar pertenencia mecánicamente:

- `tools/check_discovery_output.py` es el checker; es lo único que se **crea** en `tools/`.
- `tests/test_check_discovery_output.py` cubre comportamiento y falsación con fixtures sintéticos.
- `tests/test_discovery_output_dogfood.py` es el módulo anclado al repo real, **sólo lectura**: ejercita el parser de contratos contra el payload real y acepta la ausencia de KB como ausencia declarada.
- `docs/plans/136-d01-mechanical-checker.md` es este Plan; `docs/plans/INDEX.md` y `CHANGELOG.md` son su registro obligatorio.
- **Fuera de scope, explícitamente:** `protocol/` completo (0 diff), `runtime/`, `tools/` más allá del archivo nombrado, `docs/` más allá de las tres rutas nombradas, `.agents/` completo, **`ROADMAP.md`**, cualquier plan o RFC cerrado.
- **`ROADMAP.md` — excepción de scope NO autorizada (corregido).** Este registro afirmaba que `ROADMAP.md` quedaba dentro del scope por la sola existencia de la determinación `Roadmap Impact: REQUIRED`. **Esa afirmación fue una inferencia del agente y no una autorización**: el `Scope` del Plan tal como se autorizó excluía `ROADMAP.md`, el `Task` de la Delegación agentiva decía `no tocar ROADMAP.md`, y la tabla de «Artefactos afectados» decía `ROADMAP.md — no`. El texto anterior se conserva en el historial de git (commit `3b94611`); la decisión humana del mantenedor sobre esta frontera está registrada en `<PLAN-136>:PC-4`. La obligación de reconciliación **no** quedó satisfecha dentro de la autorización: ver §«Roadmap Impact».
- Un path fuera de esta lista es `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN` para SAE: ampliar el scope es decisión humana. **La ejecución tocó `ROADMAP.md` fuera de este scope**: es el defecto registrado en `<PLAN-136>:F-3` y decidido en `<PLAN-136>:PC-4`.

## Diseño propuesto

Un checker DEV, sin dependencias externas, en la forma de los checkers existentes (`argparse` con `--root` y `--payload`; stdlib únicamente; `testsupport.assert_tool_imports_only_stdlib`).

1. **Carga de contratos (sólo lectura).** Parsear `KB_DISCOVERY_ENTRY.md` para los campos requeridos del entry, los contratos per-entry para las secciones adicionales por tipo, `EXECUTIVE_SUMMARY.md` para el requisito de `## Project Shape`, y `DISCOVERY_MANIFEST.md` para secciones y campos del manifest. El mapeo contrato → nombre de artefacto runtime se lee de la declaración `## Location` de cada contrato, **no** de una tabla propia ni de una convención de nombres inferida: la observación de esta ejecución mostró que la convención de nombres falla (`ENVIRONMENT_DISCOVERY.md` → `environment.md`, `API_SURFACE.md` → `api.md`), mientras que cada contrato declara su path de runtime explícitamente (`<PLAN-136>:F-4`).
2. **Descubrimiento de la KB.** Listar `.project/knowledge/discovery/`. Ausencia ⇒ `N/A` con exit 0.
3. **Validación por entrada.** Los once puntos deterministas de §«Naturaleza mecánica», cada uno produciendo `VALID`/`GAP`/`ANOMALY`/`BOUNDARY` con su razón y la cita `ruta:sección` del contrato que lo exige.
4. **Validación del manifest.** Secciones y campos requeridos; coherencia bidireccional con los archivos presentes; coherencia de front matter; `project_shape` en su enum.
5. **Resolución de procedencia.** Cada path de `source_files` se resuelve contra `--root`; `system_probe` sólo se admite para entradas de environment. **Nunca se marca inválido por `F-17`**: se reporta `GAP`.
6. **Reporte.** Texto legible + `--json`; exit code según el contrato.

**Lo que el diseño NO hace, por decisión explícita:** no decide el `project_shape` correcto; no calcula ni valida hashes ni TTL; no valida el marcador `.last_discovery` (es `B-3`, candidato futuro, otro ítem); no impone un **conjunto requerido** de entradas (los contratos no definen un conjunto obligatorio y el conjunto realmente producido depende del shape y de los workers invocados: `DISCOVERY_INIT` produce `file_map.md`, `DISCOVERY_ENV` → `environment.md`, etc.); no escribe, no repara y no archiva nada.

## Delegación agentiva

- **Task:** Implementar `tools/check_discovery_output.py`, el checker DEV que materializa el subconjunto mecánico y determinista de D01 (estructura y procedencia resoluble) sobre `.project/knowledge/discovery/`, resolviendo los requisitos **desde los contratos del payload leídos como datos de sólo lectura** y reportando con el vocabulario de señales y el contrato de exit codes existentes. Implementar `tests/test_check_discovery_output.py` (comportamiento, falsación, edge cases, determinismo, ausencia e invalidez) y `tests/test_discovery_output_dogfood.py` (sólo lectura, anclado al payload real). Registrar el Plan en `docs/plans/INDEX.md` y `CHANGELOG.md`. **No** implementar los ítems de D01 que no son mecánicos, **no** modificar `protocol/`, **no** agregar el checker a la batería canónica, **no** tocar `ROADMAP.md`.
- **Scope:** `tools/check_discovery_output.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera de las rutas del `Scope`.
  - **`STOP_AUTHORITY_REQUIRED`** — el diseño exige cambiar un contrato del payload (por ejemplo agregar el valor de procedencia de `F-17` o un shape de `F-16`), o ampliar el subconjunto mecánico más allá de los once puntos declarados.
  - **`STOP_FORBIDDEN_AUTONOMY`** — release, promotion, tag. También tocar `protocol/`, `runtime/`, `.agents/` o cualquier artefacto cerrado.
  - **`STOP_AUTHORITY_REQUIRED`** — modificar el `**Status:**` de este Plan fuera de los statuses del lifecycle, o agregar el checker a `docs/VERSIONING.md` §4.1 (la batería canónica es una obligación de gobernanza: si la ejecución concluye que el checker debe entrar, **STOP** y escalar; no se auto-autoriza).
- **Autoridad:** este Plan aprobado para ejecución, y ninguna otra. El worker y el host no adquieren autoridad propia; no crean reglas nuevas ni reinterpretan los contratos.
- **Stop conditions:** las de la policy SAE (`.agents/policies/supervised-autonomous-execution.md` §5) más las cuatro de arriba. Corregir findings dentro de las rutas del `Scope` y verificar de nuevo es trabajo autónomo; un finding que exija tocar un contrato, un `ANOMALY` de C-1/C-2/C-3, o cualquier decisión normativa, detiene y escala.

## Artefactos afectados

| Ruta | Acción | Contenido |
|---|---|---|
| `tools/check_discovery_output.py` | crear | Checker DEV: parser de contratos, validación de entradas y manifest, reporte, exit codes |
| `tests/test_check_discovery_output.py` | crear | Comportamiento, falsación, edge cases, determinismo, ausencia, invalidez |
| `tests/test_discovery_output_dogfood.py` | crear | Módulo anclado al repo real, sólo lectura |
| `docs/plans/136-d01-mechanical-checker.md` | modificar | Este Plan: anchor, checkpoint, nota de ejecución y findings al ejecutarse |
| `docs/plans/INDEX.md` | modificar | Registro del Plan 136 y su serie |
| `CHANGELOG.md` | modificar | Ítem `[Unreleased]` `(plan 136, RFC-—)` (docs-only: sin bump ni tag) |

`protocol/`, `runtime/` y `.agents/`: **0 diff**. `ROADMAP.md` **no** figuraba aquí como artefacto autorizado: fue modificado **fuera del scope** (ver `<PLAN-136>:F-3` y `<PLAN-136>:PC-4`).

## Estrategia de tests

El Plan especifica **qué deberá demostrar** la implementación; los tests se escriben durante la ejecución, no ahora.

**Positivos.** Un árbol de discovery sintético válido y completo ⇒ todas las entradas `VALID`, manifest `VALID`, exit 0. Un shape `library` con `distribution.md` presente ⇒ `VALID`. `system_probe` en `environment.md` ⇒ `VALID`. Ausencia total de `.project/knowledge/discovery/` ⇒ `N/A` y exit 0.

**Negativos (falsación; cada uno debe fallar de forma explícita y reproducible).** `#` distinto de `title` ⇒ `ANOMALY`. `artifact` o `kind` incorrectos ⇒ `ANOMALY`. `## Discovered Facts` ausente ⇒ `ANOMALY`. Sección adicional exigida por el contrato del tipo ausente ⇒ `ANOMALY`. `source_files` con path inexistente en una entrada que no es de environment ⇒ `GAP` (advisory, exit 0). `system_probe` en una entrada que no es de environment ⇒ `ANOMALY`. Manifest que lista en `active` un archivo ausente, o que omite un archivo presente ⇒ `ANOMALY`. `project_shape` fuera del enum ⇒ `ANOMALY`. `project_shape` del manifest distinto del declarado en `executive_summary.md` ⇒ `ANOMALY`. `project_shape` `library`/`cli` sin `distribution.md` ⇒ `ANOMALY`. Front matter sin delimitar o TOML no parseable ⇒ `ANOMALY`, nunca excepción. Campo requerido con tipo incorrecto (por ejemplo `tags` no-lista) ⇒ `ANOMALY`.

**Fronteras del dominio mecánico.** Un juicio que D01 sí hace pero D01-MC **no** debe hacer: una claim cualitativa sin fuente (ítem 6), un patrón sin ejemplo (ítem 3), una dependencia que no aparece en ningún archivo de configuración (ítem 2). El test debe demostrar que el checker **no** los marca y **no** los aprueba: no reporta nada sobre ellos, porque no son de su dominio (declarado, no silencioso).

**Determinismo.** Dos ejecuciones sobre el mismo input producen salida byte-idéntica; el orden de las entradas en el reporte es determinista (ordenado) y no depende del orden del filesystem.

**Ausencia e invalidez.** Ausencia declarada (`N/A`) versus archivo presente pero corrupto (`ANOMALY`) deben ser distinguibles y ninguno debe convertirse en el otro.

**Contrato de la herramienta.** `testsupport.assert_tool_imports_only_stdlib` sobre el checker (stdlib puro, sin módulos de `tools/`); el checker es de sólo lectura (`test_observation_is_read_only` como precedente: comparar snapshots del árbol antes y después).

**Dogfood.** El módulo anclado al repo real verifica que el parser de contratos resuelve los requisitos **desde el payload real** (campos del entry base, secciones de al menos un contrato per-entry, secciones del manifest, requisito de `## Project Shape`), y que la ausencia de `.project/knowledge/discovery/` se reporta como ausencia declarada y no como fallo. Es sólo lectura y no depende de que exista una KB.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_discovery_output.py --root .
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Criterios objetivos y reproducibles (cada uno convertible en evidencia):

1. **Suite del checker en verde**, con los casos positivos, negativos y de frontera de §«Estrategia de tests» nombrados uno por uno en la nota de ejecución.
2. **Batería canónica completa en verde**: los seis checkers con exit 0 y `python -m pytest tests/` sin fallos.
3. **C-1 `VALID`, C-2 `VALID` (consistencia checkpoint↔anchor), C-3 `VALID`** para el Plan 136, con `ANOMALY=0` en los tres.
4. **Contrato de la herramienta:** `assert_tool_imports_only_stdlib` pasa; el checker no importa módulos de `tools/` salvo que se declare y justifique.
5. **Contrato de exit codes:** exit 0 con sólo `VALID`/`GAP`/`N/A`; exit 1 ante `ANOMALY`; exit 2 ante error de lectura irrecuperable. Demostrado por test, no afirmado.
6. **Determinismo:** dos corridas sobre el mismo input dan salida byte-idéntica (test).
7. **Sólo lectura:** ningún archivo del proyecto cambia tras correr el checker (snapshot antes/después, test).
8. **Ausencia de cambios fuera del scope:** `git diff --stat` sobre `protocol/`, `runtime/` y `.agents/` es vacío (0 diff), verificable con `git diff <baseline>..<final> -- protocol/ runtime/ .agents/`. `ROADMAP.md` **sí** cambia: es la reconciliación de Roadmap Impact declarada abajo.
9. **Estado Git esperado:** un commit atómico en `dev`, working tree limpio, sin push/merge/tag/release/promotion; `dev` ahead de `origin/dev` por el commit del Plan.
10. **Documentation Impact** y **Roadmap Impact** determinados, cada uno con su evidencia (abajo).

## Documentation Impact

```text
Documentation Impact: REQUIRED
```

Determinado ahora para que la ejecución lo reconcilie; **no** se anticipa ninguna edición.

- `CHANGELOG.md` — ítem `[Unreleased]` `(plan 136, RFC-—)`; es el registro obligatorio de todo plan docs-only (RFC-69) y su ausencia rompería el DoD.
- `docs/plans/INDEX.md` — registro del Plan 136 y su serie; espejo descriptivo obligatorio (AU-4: registra, no gobierna).
- `docs/plans/136-d01-mechanical-checker.md` — su propio anchor, checkpoint, nota de ejecución y findings.
- **`docs/VERSIONING.md` §4.1 — deliberadamente NO.** Agregar un checker a la batería canónica crea una obligación de gobernanza sobre todo Change futuro. Este Plan **no** la autoriza: la ejecución que concluya que corresponde agregarlo debe **STOP** y escalar (ver §«Delegación agentiva», límites).
- **`ROADMAP.md` — no** (ver §«Roadmap Impact»).
- **`.agents/` — no.** Ninguna instrucción activa cambia: el checker no es un gate de lifecycle ni un paso obligatorio del workflow DEV.
- **`runtime/README.md` — no.** El checker no vive en `runtime/` ni es una materialización de Execution Context.
- **Documentación histórica: no se toca** (RFC-46, `.agents/policies/validation-closure.md:5.1`). En particular **no** se editan la policy D01, las fricciones del plan 19, ni el plan 60 para «aclarar» D01: son traza. La contradicción `artifact_validated: KB_DISCOVERY_ENTRY.md` vs las entradas reales (`F-11`) se **conserva**.

## Roadmap Impact

```text
Roadmap Impact: REQUIRED
```

Determinado ahora; la reconciliación ocurre **al ejecutar**, no ahora.

- **Artefacto a reconciliar: `ROADMAP.md`** — es el mapa operativo y la entrada que este Plan ejecuta vive ahí (`## Trabajo activo / dogfood`, fila «Mechanical D01 subset — DEV checker for discovery output structure and provenance», estado **Próximo dogfood**). Al completarse D01, esa fila deja de estar **activa**: pasa a trabajo completado, y `EARS structural validator` pasa a ser el próximo dogfood. Eso **es** un cambio del estado operativo del mapa, y ninguna otra categoría lo absorbe.
- **Por qué `REQUIRED` y no `NOT_REQUIRED`:** la distinción pedida es explícita. Ejecutar D01 «ya previsto» **sí** mueve el mapa, porque la fila declara un estado (`Próximo dogfood`) que queda falso al completarse; y el orden de la secuencia de dogfood cambia (EARS pasa a próximo). `NOT_REQUIRED` aplicaría a un Change que no alterara el mapa; este lo altera.
- **Por qué *no* significa «editar `ROADMAP.md` sin criterio»:** el ítem está en la sección «Trabajo activo / dogfood», que es la que representa trabajo vigente. Se retira la fila de trabajo activo (o se la marca completada según el criterio que `ROADMAP.md` ya usa) y se actualiza el orden de la secuencia de dogfood. `ROADMAP.md` sigue siendo un **mapa operativo, no un changelog**: no se cataloga historia ni se duplica el estado detallado del Plan, que vive en `docs/plans/INDEX.md`.
- **Trabajo nuevo creado:** **ninguno**. Los residuos `F-16`/`F-17` (`B-4`/`B-7` residual) ya figuran en `ROADMAP.md:Pendientes que requieren autorización` como payload; este Change **no** los crea, **no** los reclasifica y **no** los mueve. `B-3` (checker de `.last_discovery`) permanece candidato futuro y explícitamente **fuera** del diseño de D01-MC.
- **Dependencia:** `EARS structural validator` queda después de D01. Si al ejecutar D01 la secuencia de dogfood cambia, eso se registra como actualización del mapa, no como ítem nuevo.

**Estado de esta determinación tras la decisión humana (`<PLAN-136>:PC-4`).** La obligación que `REQUIRED` impone —reconciliar antes del cierre— **no quedó satisfecha dentro de la autorización del Plan**: `ROADMAP.md` estaba excluido del `Scope`, y la determinación de impacto **no** es por sí sola una autorización para escribir fuera del scope (`policies/authority.md`: modificar governance fuera de scope sin su propia autorización es STOP). La edición de `ROADMAP.md` que efectivamente ocurrió fue el defecto `<PLAN-136>:F-3`; el mantenedor decidió que **no** la autorizó implícitamente. La reconciliación queda por lo tanto **pendiente de decisión humana** y su continuidad vive en `<PLAN-136>:PC-4`, que es una pending decision **existente** del propio Plan (PC-1 del mecanismo, sin crear mecanismo nuevo). Consecuencia sobre el cierre: la condición derivada `Closed` de este Plan se apoya en evidencia de validación independiente de `ROADMAP.md` (checker, suites, batería y gates), de modo que **no** queda invalidada por este defecto; lo que queda pendiente es la decisión sobre el contenido de `ROADMAP.md`, no la validez del checker.

**Por qué el Plan no podía resolverlo por sí mismo.** La política de Roadmap Impact (`.agents/policies/validation-closure.md:5.2`) dice que `REQUIRED` «does not mean *always edit `ROADMAP.md`*» y que el artefacto a actualizar sigue **ownership / source of truth**; regula **qué** debe reconciliarse, no **quién está autorizado** a escribirlo. La autorización de escritura la fija el `Scope` del Plan, y `autonomy ⊆ authorized scope` (`.agents/policies/supervised-autonomous-execution.md` §1). No existe en el repositorio ninguna regla de precedencia que haga que una determinación de cierre amplíe el scope de ejecución: el grep sobre `.agents/` sólo encuentra reglas en el sentido **opuesto** (modificar governance fuera de scope es STOP). Por eso la vía correcta era `DEFERRED` con una pending decision con owner —o escalar para ampliar el scope— y no editar el artefacto.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 136 (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 136 (checker DEV del subconjunto mecánico de D01) y su registro: `tools/check_discovery_output.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`
- **Nota sobre el alcance declarado (corregida por `<PLAN-136>:PC-4`).** En el momento de la validación este campo enumeraba también `ROADMAP.md`. Esa inclusión **no** provenía del `Scope` autorizado —que lo excluía— sino de una inferencia del agente; se retira aquí para que el anchor describa el scope realmente autorizado. La modificación de `ROADMAP.md` ocurrió **fuera** de ese scope y es el defecto `<PLAN-136>:F-3`, decidido por el mantenedor en `<PLAN-136>:PC-4`. El delta scoped identity de A1 se calculó sobre los 7 paths que incluían `ROADMAP.md`; su valor queda como está (A1 no se muta) y se declara aquí la diferencia para que sea reconstruible sin inferencia.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python tools/check_discovery_output.py --root .`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`
- **Effective inputs (repo content):** el scope declarado (7 paths) más los contratos de discovery del payload que el checker consume como datos de sólo lectura y el corpus que consumen los checkers canónicos (`docs/plans/`, `docs/rfc/`, `docs/adr/`, `tools/`, `protocol/.agents/`).
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14; sin red. El GAP ambiental de temporales de pytest declarado por los Planes 121–135 **no se reprodujo** en esta ejecución: `python -m pytest tests/` corrió completo y dio PASS sin aislamiento adicional. Sin clases ambientales declaradas para este Change.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `5f6c4fab93bdbfdae422af3f8b4004175c0bf624` (`git write-tree` sobre el índice staged con el cambio completo).
  - **Delta scoped identity (scope S = los 7 paths, ordenados; serialización `scoped-v1`):** `d454752737d229bbb61a45eafcc8c110a7c4b92ea3fb511891ff27fb1649cf99`
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `tools/check_discovery_output.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md`
- **Validity / stale:** `vigente` (validación sobre el estado de contenido observado; el cierre se apoya en el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` OK (215 archivos, 10256 referencias); `check_plan_citations` OK; `check_plan_structure` OK; `check_taxonomy_coherence` OK; `check_session_artifacts` OK; `check_version_state` OK; `pytest tests/` PASS (**953 passed, 0 failed**, incluidas las 54 pruebas nuevas de D01: 42 de comportamiento y falsación, 12 de dogfood); `check_discovery_output --root .` exit 0 con `N/A` (el repo DEV no es un target de discovery: ausencia declarada); C-1 `VALID`; C-2 `VALID` (consistencia con A1); C-3 `VALID`, con `ANOMALY=0` en los tres.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 136 (GC-1, Incremento 3; modelo del Plan 134).*

- **Commits de cierre:** un (1) commit atómico en `dev`, identificado por su mensaje: `feat(tools): implement the D01 mechanical checker for discovery output (plan 136)`. El SHA no se embebe (R4 permanece opcional, decisión del Plan 134 no reabierta); el commit se localiza por su mensaje.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `d454752737d229bbb61a45eafcc8c110a7c4b92ea3fb511891ff27fb1649cf99`, state identity T1 = `5f6c4fab93bdbfdae422af3f8b4004175c0bf624`.
- **Estado de cierre (identidad):** delta scoped identity + state identity de A1, es decir `d454752737d229bbb61a45eafcc8c110a7c4b92ea3fb511891ff27fb1649cf99` / `5f6c4fab93bdbfdae422af3f8b4004175c0bf624`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro; el commit de cierre incluye governance (este Plan, INDEX, CHANGELOG), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`). Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Consistencia checkpoint↔anchor:** PASS. La identidad scoped del estado de cierre es la del anchor aplicable (A1) y no hay factores ambientales declarados que hayan cambiado; C-2 lo verifica sobre el artefacto del Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 136 y su serie; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 136, RFC-—)`; `ROADMAP.md` reconciliado según la determinación de Roadmap Impact de abajo; sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag (DEV-only, RFC-69).
- **Condición derivada:** `Closed` (DEV-only: docs + tooling, sin release). `Verified` = sí (∃ validación PASS con anchor A1); `Executed` = sí (implementación + validación); `Committed` = estado del repositorio, no un status: el commit atómico en `dev` es la acción del mantenedor y queda fuera de la autoridad del host; `Promoted` = no; `Released` = no. `Closed ≠ Released`.
- **Documentation impact:** `REQUIRED` — reconciliado en esta ejecución. `CHANGELOG.md` (ítem `[Unreleased]` del Plan), `docs/plans/INDEX.md` (fila, serie y encabezado de estado) y `docs/plans/136-d01-mechanical-checker.md` (anchor, checkpoint, nota de ejecución y findings). `docs/VERSIONING.md` §4.1 **no** se toca: agregar el checker a la batería canónica sería una obligación de gobernanza sobre todo Change futuro y el Plan **no** la autorizó; el checker se valida por su propia suite y por el dogfood, no por el bloque canónico. `.agents/` y `runtime/README.md` no se tocan: ninguna instrucción activa cambia y el checker no vive en `runtime/`. Documentación histórica: no se toca (RFC-46), en particular la policy D01, las fricciones del plan 19 y el plan 60.
- **Roadmap impact:** `REQUIRED` — **la reconciliación no quedó satisfecha dentro de la autorización**: ver «Resolución post-cierre de F-3 (A y B)». El registro original de esta línea describía la retirada de la fila `Mechanical D01 subset` y el paso de `EARS structural validator` a próximo dogfood con prioridad `Alta`; el mantenedor determinó después (`<PLAN-136>:PC-4`) que `ROADMAP.md` estaba fuera del `Scope` y que la determinación `REQUIRED` no lo autorizaba, y la resolución de F-3 confirmó **A** (retirada de la fila de D01, reconciliación factual) y **B1** (`Próximo dogfood`) pero **restituyó `Media`** en **B2**, porque el cambio a `Alta` no tenía evidencia documental. **No se crea trabajo nuevo** ni se reclasifica ningún ítem histórico: los residuos de payload que D01 no podía resolver (`F-17` y `F-16`) ya figuraban en `Pendientes que requieren autorización` y permanecen ahí sin cambios; `B-3` sigue candidato futuro y explícitamente fuera del diseño de D01-MC.

## Criterio de entrada

Condiciones que deben ser ciertas **antes** de ejecutar este Plan:

- [ ] `**Status:**` de este Plan es `Aprobado para ejecución` (hoy es `Aprobado para redacción`).
- [ ] `## Delegación agentiva` presente, con `Task` y `Scope` no vacíos y el `Scope` con las seis rutas exactas.
- [ ] `## Verificación` presente, con el command-set exacto.
- [ ] Autoridad válida: la del propio Plan; sin autoridad implícita, sin RFC/ADR requerido, sin cambio de payload involucrado.
- [ ] Baseline del repositorio identificable: SHA y tree registrados al inicio de la ejecución.
- [ ] Sin pending decision bloqueante en este Plan.
- [ ] Dependencias conocidas y disponibles: planes 135, 60, 47/RFC-48, 53/RFC-54 y 40/RFC-41 cerrados; los contratos de discovery presentes en el payload.
- [ ] `GAP`/`ANOMALY` de C-1/C-2/C-3 resueltos al inicio de la ejecución.

Ninguna de estas condiciones requiere una decisión que hoy falte: la única pendiente es la **autorización humana de ejecución** (§«Criterio de entrada» punto 1), que es exactamente la decisión que este Change no toma.

## Criterios de salida

- [ ] `tools/check_discovery_output.py` existe, es stdlib-only, de sólo lectura, y materializa los once puntos deterministas de §«Naturaleza mecánica».
- [ ] Los requisitos se resuelven **desde los contratos**; el checker no mantiene lista propia de secciones.
- [ ] `tests/test_check_discovery_output.py` y `tests/test_discovery_output_dogfood.py` en verde, cubriendo positivos, negativos, falsación, edge cases, determinismo, ausencia e invalidez, y la frontera con el dominio no mecánico.
- [ ] Batería canónica en verde; C-1/C-2/C-3 `VALID` con `ANOMALY=0`.
- [ ] Contrato de exit codes demostrado por test.
- [ ] `protocol/`, `runtime/`, `.agents/` y `ROADMAP.md` salvo la reconciliación declarada: 0 diff.
- [ ] `docs/plans/INDEX.md` y `CHANGELOG.md` actualizados; determinaciones de impacto registradas.
- [ ] Commit atómico en `dev`; sin push, merge, tag, release ni promotion.

## Criterio de cierre del futuro D01

Los estados se determinan así, sin reinterpretarlos (`.agents/policies/validation-closure.md` §6):

```text
Verified   = ∃ validation(PASS, anchor A1 registrado en este Plan)
Executed   = Plan status "Executed" (implementación + validación)
Committed  = estado del repositorio: el commit atómico en dev (no es un status de Plan)
Closed     = Executed ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor
             ∧ evidencia PASS para el estado de cierre  (condición DERIVADA de este Plan;
             D01 NO queda "Closed" como estado de la policy D01 del payload)
Promoted   = merge dev → master (acción del mantenedor)
Released   = tag anotado en master (acción del mantenedor)
```

- `Committed ≠ Closed ≠ Promoted ≠ Released`, y `Closed ≠ Released`.
- El cierre es **del Plan 136** (la materialización DEV), no de la policy D01 del payload. **La policy D01 no cambia de estado**: sigue siendo una policy `[agent]` del payload con la validación mecánica declarada como extensión futura. Si al cerrar pareciera necesario marcarla de otro modo, eso es un cambio de payload: **STOP**.
- `Promoted` y `Released` **no** son objetivos de este Plan: son acciones del mantenedor y quedan fuera de la autoridad del host (SAE las reporta `FORBIDDEN`).

## Stop conditions

Además de las de `.agents/policies/supervised-autonomous-execution.md` §5, detienen la ejecución y escalan:

1. **Cambio de contrato del payload** — agregar el valor de procedencia de `F-17`, un shape de `F-16`, o cualquier cláusula nueva a los contratos de discovery.
2. **Ampliación del subconjunto mecánico** — implementar cualquiera de los seis ítems de juicio de D01 (stack real, dependencias reales, patrones, secretos, claims, merge, api↔shape).
3. **Incorporación a la batería canónica** — modificar `docs/VERSIONING.md` §4.1 o el bloque de CI.
4. **Imposición de un conjunto requerido de entradas** — la regla no existe en los contratos; inventarla es una decisión normativa.
5. **Exención de entradas de forma ad-hoc** — eximir `containers.md`/`database.md`/`file_map.md` por criterio propio, en lugar de reportarlas `GAP`. La exención correcta vive en el contrato y no existe todavía (es `F-17`).
6. **Escritura fuera de las seis rutas del `Scope`.**
7. **Cambio de `**Status:**` de este Plan** distinto de `Executed` por la propia ejecución, o cualquier intento de auto-autorización.
8. Cualquier `ANOMALY` de C-1/C-2/C-3, conflicto entre fuentes normativas, o necesidad de RFC/ADR/release/promotion.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-136>:F-1`: estado: `open`; observación: `F-17` es una frontera real del subconjunto mecánico de D01: el ítem 5 exige que todo `source_files` exista, pero `containers.md` y `database.md` declaran ausencias y `file_map.md` declara hechos de árbol, y el contrato no ofrece un valor de procedencia que los represente (`system_probe` sólo es legal para entradas de environment). Sin resolverlo, cualquier implementación mecánica del ítem 5 produce falsos fallos; resolverlo exige agregar un valor de procedencia al contrato `KB_DISCOVERY_ENTRY.md`, que es payload; evidencia original: docs/plans/19-anexo-a-bitacora-fricciones.md sección F-17, protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md sección Optional Front Matter (provenance), y la evidencia de la KB del plan 19 (anexo B) donde se citaron raíces escaneadas con nota explícita; estado Git observado: `8489b89`, working tree limpio; provenance original: reconstrucción de intake del Plan 136 (2026-09-15). Resolución: **no resuelta por diseño**; mitigada dentro del alcance DEV por la decisión de reportar `GAP` y nunca `ANOMALY` en ese caso; la corrección de fondo es payload y queda como `<PLAN-136>:PC-2`.
- `<PLAN-136>:F-2`: estado: `open`; observación: el `#` de la policy D01 declara `artifact = "KB_DISCOVERY_ENTRY.md"` y `artifact_validated: KB_DISCOVERY_ENTRY.md`, mientras su §Input enumera las entradas reales en `.project/knowledge/discovery/*.md`; es la fricción `F-11`, resuelta funcionalmente por el plan 40 (validación directa, sin artefacto-puente) pero cuya contradicción textual permanece en el payload y un lector nuevo puede interpretarla como que D01 valida un único archivo llamado `KB_DISCOVERY_ENTRY.md`; evidencia original: protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md líneas 4 y 20 frente a su sección Input, docs/plans/19-anexo-a-bitacora-fricciones.md sección F-11, y docs/plans/40-discovery-artifact-boundaries.md; estado Git observado: `8489b89`, working tree limpio; provenance original: reconstrucción de intake del Plan 136 (2026-09-15). Resolución: **no resuelta por diseño**; la contradicción se conserva como evidencia (RFC-46) y **no** se edita el payload.

- `<PLAN-136>:F-3`: estado: `resolved` (decisión humana del mantenedor; transición materializada por el Plan 139 — ver `## Metadatos de estado (evolucionables)` al final de este registro); observación: el Plan declaraba `ROADMAP.md` como fuera de scope y a la vez determinaba «Roadmap Impact: REQUIRED» nombrando `ROADMAP.md` como el artefacto a reconciliar, de modo que sus dos enunciados no podían ser verdaderos a la vez y un ejecutor read-only habría tenido que elegir por inferencia entre violar el scope o incumplir la determinación de impacto; evidencia original: la sección «Scope» y la sección «Roadmap Impact» de este Plan tal como se publicaron en el baseline de la ejecución, `8489b89` y `f0d9c03`; estado Git observado: `f0d9c0334c6256a1b4187d30a1cf37fe0ab0f816`, working tree limpio; provenance original: lectura del propio Plan al iniciar la ejecución autorizada (2026-09-15). Resolución: **el agente NO la resolvió; la resolvió el humano.** Autoridad aplicable: el `Scope` de este Plan tal como se autorizó —que excluía `ROADMAP.md` y cuyo `Task` decía «no tocar `ROADMAP.md`»— es la frontera de escritura; una determinación de cierre regula **qué** debe reconciliarse, no **quién** está autorizado a escribirlo. No existe en el repositorio ninguna regla de precedencia que haga que una determinación de cierre amplíe el scope de ejecución: las policies vigentes sólo contienen reglas en el sentido opuesto (modificar governance fuera de scope sin su propia autorización es STOP, y es stop condition de cierre). Análisis: los dos enunciados del Plan eran contradictorios y el agente los resolvió por inferencia a favor de la determinación de impacto, en lugar de escalar la contradicción; ése es el defecto. Decisión humana (`<PLAN-136>:PC-4`, 2026-09-15): el mantenedor **no** autorizó implícitamente la modificación de `ROADMAP.md` por el solo hecho de que el Plan declarara `Roadmap Impact: REQUIRED`, porque `ROADMAP.md` había sido excluido explícitamente del `Scope` del Plan 136; la modificación **excedió el Scope**. Efecto sobre el estado del finding: la transición de estado la reserva la normativa al humano y el agente no la tomó; el finding **permanece `open`** y la decisión sobre revertir, conservar o rehacer la modificación de `ROADMAP.md` queda pendiente como decisión humana explícita en `<PLAN-136>:PC-4` (el agente no revirtió nada, por instrucción explícita).; Resolución: decisión humana del mantenedor (2026-09-20), materializada por el Plan 139 como DEC-1: el incidente **ocurrió** (la escritura de `ROADMAP.md` que `<PLAN-136>:C-3` conserva con autorización no establecida); el Plan 138 corrigió el mecanismo preventivo con enforcement previo a la delegación basado en el Scope autorizado; la regresión específica de ese enforcement demuestra que el intento equivalente se detiene antes de ejecutar al Worker, sin delegación persistida y con el artefacto excluido byte-idéntico; y la evidencia histórica del Plan 136 no se modifica. El estado queda formalmente `resolved`; el detalle y la justificación completa están en `## Metadatos de estado (evolucionables)`.`n ; Resolución: decisión humana del mantenedor (2026-09-20), materializada por el Plan 139 como DEC-1: el incidente **ocurrió** (la escritura de `ROADMAP.md` que `<PLAN-136>:C-3` conserva con autorización no establecida); el Plan 138 corrigió el mecanismo preventivo con enforcement previo a la delegación basado en el Scope autorizado; la regresión específica de ese enforcement demuestra que el intento equivalente se detiene antes de ejecutar al Worker, sin delegación persistida y con el artefacto excluido byte-idéntico; y la evidencia histórica del Plan 136 no se modifica. El estado queda formalmente `resolved`. La transición no legitima retrospectivamente ninguna escritura fuera de Scope.; Resolución: decisión humana del mantenedor (2026-09-20), materializada por el Plan 139 como DEC-1: el incidente ocurrió (la escritura de `ROADMAP.md` que `<PLAN-136>:C-3` conserva con autorización no establecida); el Plan 138 corrigió el mecanismo preventivo con enforcement previo a la delegación basado en el Scope autorizado; la regresión específica de ese enforcement demuestra que el intento equivalente se detiene antes de ejecutar al Worker, sin delegación persistida y con el artefacto excluido byte-idéntico; y la evidencia histórica del Plan 136 no se modifica. El estado queda formalmente `resolved` y la transición no legitima retrospectivamente ninguna escritura fuera de Scope.
- `<PLAN-136>:F-4`: estado: `open`; observación: el diseño del Plan preveía resolver el mapeo contrato → nombre de artefacto runtime por la «convención declarada por el contrato base», pero esa convención no existe como regla: derivar el nombre por minúsculas mapea `ENVIRONMENT_DISCOVERY.md` a `environment_discovery.md` y `API_SURFACE.md` a `api_surface.md`, mientras los artefactos reales son `environment.md` y `api.md`. Una tabla propia de artefactos habría violado single-source y habría duplicado contenido de contrato; evidencia original: los contratos de discovery bajo `protocol/.agents/orchestrators/discovery/contracts/`, cada uno de los cuales declara su path de runtime en su sección `## Location` (verificado por el dogfood anclado); estado Git observado: `f0d9c03`, working tree limpio; provenance original: implementación del Paso 1 del diseño (2026-09-15). Resolución: corregida por `<PLAN-136>:C-4`: el mapeo se lee de la declaración de Location de cada contrato, sin tabla ni convención inferida.
- `<PLAN-136>:F-5`: estado: `open`; observación: el Plan nació con `**Status:** Aprobado para redacción` y su criterio de entrada exigía `Aprobado para ejecución`, que es el status que el Change Lifecycle define como «autorizado a ejecutar»; el mantenedor autorizó la ejecución por directiva sin que el artefacto se hubiera actualizado, de modo que el criterio de entrada no se satisfacía leyendo sólo el Plan y satisfacerlo es en sí mismo el registro de la decisión humana; evidencia original: el header de este Plan en el baseline de la ejecución y el criterio de entrada punto 1 de este Plan; estado Git observado: `f0d9c0334c6256a1b4187d30a1cf37fe0ab0f816`, working tree limpio; provenance original: aplicación del criterio de entrada al iniciar la ejecución (2026-09-15). Resolución: corregida por `<PLAN-136>:C-5`: la autorización humana se registró en `<PLAN-136>:PC-1` y el status se llevó a `Executed` al cerrar, sin inventar un status intermedio ni auto-otorgarse autoridad: la decisión humana existió y quedó registrada.
- `<PLAN-136>:F-6`: estado: `open`; observación: la señal `BOUNDARY` del vocabulario del repositorio estaba declarada en la firma del checker pero ningún caso de prueba la ejercitaba, de modo que la rama «ambigüedad estructural → revisión humana» habría podido degradarse silenciosamente a un resultado distinto sin que la suite lo detectara; evidencia original: la suite de comportamiento y falsación en su estado intermedio durante la ejecución y el conteo de 41 pruebas pasando con la rama sin cobertura; estado Git observado: working tree de la ejecución del Plan 136; provenance original: revisión de la propia suite tras ponerla en verde (2026-09-15). Resolución: corregida por `<PLAN-136>:C-6`: se agregó el caso de entrada sin contrato reconocible que exige `BOUNDARY` y ausencia de `ANOMALY`, más el caso de ausencia declarada.

### Correcciones

- `<PLAN-136>:C-1`: refs origen: `<PLAN-136>:F-1`; alcance de revalidación: `docs/plans/136-d01-mechanical-checker.md`, secciones «Naturaleza mecánica: qué es determinista y qué no» y «Estrategia de tests», donde la frontera se declara explícitamente y el comportamiento se fija en `GAP` (advisory) en lugar de `ANOMALY` o exención ad-hoc; evidencia: el Plan publicado con esa decisión y este registro de provenance, sin modificar ninguna regla normativa ni el payload.
- `<PLAN-136>:C-2`: refs origen: `<PLAN-136>:F-2`; alcance de revalidación: `docs/plans/136-d01-mechanical-checker.md`, sección «Reconstrucción: qué es D01 hoy», donde la contradicción histórica se conserva y se declara explícitamente como evidencia no reescrita; evidencia: el Plan publicado con esa sección y la cita de `F-11` y del plan 40, sin tocar `protocol/.agents/`.

- `<PLAN-136>:C-3`: refs origen: `<PLAN-136>:F-3`; alcance de revalidación: `docs/plans/136-d01-mechanical-checker.md` secciones «Scope», «Delegación agentiva» y «Artefactos afectados», donde la exclusión de `ROADMAP.md` volvió a declararse como tal, y `ROADMAP.md` mismo; evidencia: el commit `3b94611` y el diff de `ROADMAP.md` entre `f0d9c03` y `3b94611`. **Autorización: NO establecida.** Esta corrección **excedió** el `Scope` autorizado del Plan; el mantenedor decidió (`<PLAN-136>:PC-4`) que la determinación de `Roadmap Impact: REQUIRED` no autorizaba implícitamente la escritura de `ROADMAP.md`. El registro se conserva como traza factual (RFC-46) y **no** como acto autorizado: es el hecho que el defecto `<PLAN-136>:F-3` describe.
- `<PLAN-136>:C-4`: refs origen: `<PLAN-136>:F-4`; alcance de revalidación: `tools/check_discovery_output.py` (la resolución del mapeo contrato → artefacto se lee de la sección `## Location` de cada contrato) y `docs/plans/136-d01-mechanical-checker.md` sección «Diseño propuesto» paso 1; evidencia: el dogfood anclado (`tests/test_discovery_output_dogfood.py`) verifica sobre el payload real que los 18 contratos per-entry resuelven su path de runtime y que el mapeo ingenuo por minúsculas sería incorrecto, en verde sobre el estado de cierre.
- `<PLAN-136>:C-5`: refs origen: `<PLAN-136>:F-5`; alcance de revalidación: el header `**Status:**` de este Plan y `<PLAN-136>:PC-1`; evidencia: la autorización humana explícita registrada en `<PLAN-136>:PC-1` y el status final `Executed`, con la condición derivada `Closed` registrada en el Checkpoint; la ejecución no creó autoridad propia ni inventó un status fuera de los del lifecycle.
- `<PLAN-136>:C-6`: refs origen: `<PLAN-136>:F-6`; alcance de revalidación: `tests/test_check_discovery_output.py`, casos `test_an_unknown_entry_type_is_a_boundary_not_an_anomaly` y `test_an_entry_with_no_contract_is_not_silently_approved`; evidencia: la suite completa de D01 en verde (42 casos de comportamiento y falsación) sobre el estado de cierre.

### Pending decisions

- `<PLAN-136>:PC-1`: decisión: autorizar la ejecución del Plan 136 (implementación de D01-MC); blocking: **sí**; owner: mantenedor; escalación: el Plan estaba `Aprobado para redacción` y la autorización de ejecución es una decisión humana explícita que el agente no puede tomar; resolución: **resuelta** — el mantenedor autorizó explícitamente la ejecución íntegra del Plan 136 bajo SAE el 2026-09-15, sin ampliar scope, authority, contrato de D01, subconjunto mecánico, Protocol, RFC-56 ni las reglas de findings/release; evidencia: esa autorización y este registro; efecto downstream: habilitó la ejecución completa registrada en la Nota de ejecución y el cierre del Plan; ADR-worthiness: no aplica.
- `<PLAN-136>:PC-2`: decisión: si `F-17` debe resolverse agregando un valor de procedencia («observado por scan») al contrato `KB_DISCOVERY_ENTRY.md`, o por otra vía; blocking: **no** para esta ejecución (el checker reporta `GAP` y no necesita la decisión), pero **sí** para cerrar el hueco de fondo; owner: mantenedor; escalación: es un cambio de contrato de payload y por lo tanto requiere RFC-56 (RFC `Accepted` + plan), que este Change no crea ni puede crear; resolución: pendiente; evidencia: `<PLAN-136>:F-1`; efecto downstream: sin esta decisión, el ítem 5 de D01 no puede ser mecánicamente correcto para entradas que declaran ausencias o hechos de árbol; ADR-worthiness: no evaluado aquí (requiere decisión humana).
- `<PLAN-136>:PC-3`: decisión: si `F-16` debe resolverse ampliando el modelo de clasificación de `project_shape` para repositorios documentales/protocolo; blocking: **no**; owner: mantenedor; escalación: cambio de modelo en payload, requiere la vía RFC-56; resolución: pendiente, ya registrada en `ROADMAP.md:Pendientes que requieren autorización` como `B-7` residual; evidencia: `docs/plans/19-anexo-a-bitacora-fricciones.md` sección F-16; efecto downstream: ninguna sobre D01-MC, que acepta los seis valores del enum y no decide el correcto; ADR-worthiness: no evaluado aquí.

- `<PLAN-136>:PC-4`: decisión: (a) si una determinación `Roadmap Impact: REQUIRED` autoriza materialmente la modificación de `ROADMAP.md` cuando ese artefacto fue excluido explícitamente del `Scope` del Plan, y (b) qué debe ocurrir con la modificación de `ROADMAP.md` que la ejecución realizó; blocking: **sí**; owner: mantenedor; escalación: frontera de autoridad detectada por SAE en su primer Change funcional (`<PLAN-136>:F-3`); la pregunta **no** es resoluble mecánicamente porque ninguna fuente normativa establece precedencia entre la obligación de reconciliación de `.agents/policies/validation-closure.md` §5.2 y la frontera de escritura que fija el `Scope`; resolución: **(a) resuelta** por decisión humana explícita (2026-09-15): **no** se autorizó implícitamente la modificación de `ROADMAP.md` por el solo hecho de declarar `Roadmap Impact: REQUIRED`, porque `ROADMAP.md` había sido excluido explícitamente del `Scope` del Plan 136, de modo que la modificación **excedió el Scope**; **(b) pendiente**: la decisión de revertir, conservar o rehacer la modificación de `ROADMAP.md` queda como decisión humana explícita y **no** fue tomada ni inferida por el agente, que **no** revirtió nada por instrucción explícita del mantenedor; evidencia: el diff de `ROADMAP.md` entre `f0d9c03` y `3b94611`, el `Scope` autorizado del Plan en `f0d9c03` (que lo excluía), el `Task` de la Delegación agentiva («no tocar `ROADMAP.md`»), la tabla de Artefactos afectados («`ROADMAP.md` — no»), `.agents/policies/authority.md` (modificar governance fuera de scope sin su propia autorización → STOP) y `.agents/policies/supervised-autonomous-execution.md` §1 (`autonomy ⊆ authorized scope`); efecto downstream: (1) la reconciliación que `Roadmap Impact: REQUIRED` exigía **no** quedó satisfecha dentro de la autorización y sigue pendiente, de modo que el estado de `ROADMAP.md` respecto de este Plan está **sin autorizar**; (2) el Plan 136 permanece cerrado porque su evidencia de validación (checker, suites, batería, C-1/C-2/C-3) es independiente de `ROADMAP.md`; (3) no se amplía retrospectivamente la autoridad del Plan ni se modifica ninguna política; ADR-worthiness: no evaluado aquí — podría corresponder si el mantenedor decide que la relación entre una determinación de cierre y el scope de ejecución merece una regla permanente, pero esa elevación es una decisión humana que este registro no toma.

- `<PLAN-136>:PC-5`: decisión: si la gobernanza debe definir explícitamente qué ocurre cuando una determinación `Roadmap Impact: REQUIRED` (o, por simetría, `Documentation Impact: REQUIRED`) obliga a reconciliar un artefacto que el `Scope` del Plan excluye; blocking: **no** — no bloquea la resolución de F-3, que quedó determinada por la decisión humana vigente, ni el cierre de este Plan; owner: mantenedor; escalación: observación de gobernanza detectada durante la investigación de F-3; la situación es real y ya se materializó (`Roadmap Impact: REQUIRED` + `ROADMAP.md` fuera de Scope), pero la política vigente no la contempla: `REQUIRED` no amplía el scope y `DEFERRED` exige una pending decision **existente** que al redactarse el Plan puede no existir todavía, de modo que un Plan puede nacer con una obligación de cierre inejecutable dentro de su propia autorización; resolución: **superseded** (decisión humana del mantenedor, materializada por el Plan 140 el 2026-09-20): su premisa —«la política vigente no la contempla»— queda superada por la regla vigente, que **sí** define explícitamente la situación: una determinación `REQUIRED` es obligación de estado y nunca autorización de escritura, con el artefacto fuera de `Scope` la vía es `DEFERRED` con la pending decision **existente** que la gobierna, la autorización no se infiere por clasificación, proximidad semántica, dependencia documental ni requisito de cierre, y un impacto diferido sin pending decision que lo gobierne es una condición bloqueante sin resolver, no un `DEFERRED` (`.agents/policies/validation-closure.md` §5.1/§5.2 y §7; `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.4). No queda una cuestión independiente: la continuidad de la frontera —si debe existir un mecanismo de ampliación legítima de Scope— vive en `<PLAN-138>:PC-2`, `deferred` con owner. La transición es metadata **evolucionable** (LC-1): su observación, evidencia, estado Git observado y provenance originales se preservan verbatim, y no se crea ningún valor, estado ni mecanismo nuevos; evidencia: `<PLAN-136>:F-3`, `<PLAN-136>:PC-4` (a) y el diff de `ROADMAP.md` entre `f0d9c03` y `3b94611`; efecto downstream: ninguno sobre D01 ni sobre este Plan; si el mantenedor decide que merece una regla permanente, su vía es una decisión normativa propia (posible ADR-worthiness, no evaluada aquí); ADR-worthiness: no evaluado — es una decisión humana que este registro no toma.

## Riesgos

- **Implementar de más (convertir juicio en checker).** Mitigación: los seis ítems de juicio están enumerados y excluidos por nombre; el test de frontera demuestra que el checker no los reporta; la stop condition 2 lo prohíbe explícitamente.
- **Duplicar la regla en el checker (violar single-source).** Mitigación: los requisitos se resuelven desde los contratos; el `Task` lo exige y los criterios de salida lo verifican; el plan 47/RFC-48 ya eliminó esa duplicación en la policy D01 y reintroducirla en código sería la misma violación.
- **Convertir un defecto del payload en un fallo del checker.** Mitigación: `F-17` se reporta `GAP` y nunca `ANOMALY`; la tentación de eximir entradas por criterio propio está prohibida por la stop condition 5.
- **Deriva del payload.** Los contratos pueden cambiar y volver obsoleta la resolución de requisitos. Mitigación: el dogfood anclado (sólo lectura) falla si el parser deja de resolver los requisitos reales, y los contratos siguen siendo la fuente; el checker no incrusta contenido de contrato.
- **Agrandar la batería sin autoridad.** Mitigación: la incorporación a `docs/VERSIONING.md` §4.1 es stop condition 3; el checker se valida por su suite, no por el bloque canónico.

## Trazabilidad

`ROADMAP.md` (B-1 derivado, próximo dogfood) → fricción `F-11` del plan 19 → resolución `B-1` por planes 40 y 47/RFC-48 → modelo D01 por plan 60 → alineaciones por planes 53/RFC-54 y 47/RFC-48 → habilitación SAE por plan 135 → **Plan 136 (este Plan)** → `tools/check_discovery_output.py` → ejecución autónoma bajo SAE. Continuidad de las fronteras de payload: `<PLAN-136>:F-1`/`PC-2` (`F-17`) y `PC-3` (`F-16`), ambas ya registradas en `ROADMAP.md:Pendientes que requieren autorización`.

## Nota de redacción

Este Plan se redactó **sin implementar nada**: no existe `tools/check_discovery_output.py` ni ninguna suite de D01, y `protocol/`, `runtime/` y `.agents/` tienen 0 diff. Su único propósito es habilitar una autorización humana única tras la cual SAE pueda ejecutar D01 de principio a fin sin dirección operacional paso a paso.

## Nota de ejecución

**Fecha:** 2026-09-15. **Status:** Executed. **Condición derivada:** Closed (DEV-only: docs + tooling, sin release).

**Baseline de la ejecución:** `dev` @ `f0d9c0334c6256a1b4187d30a1cf37fe0ab0f816`, tree `45e7d5b58f1bd70edb8f9480b7e6d4d13eb6d3c3`, working tree limpio.

**Qué se implementó.** Un (1) checker DEV nuevo y dos (2) suites nuevas, más el registro documental:

| Artefacto | Contenido |
|---|---|
| `tools/check_discovery_output.py` | Checker del subconjunto mecánico: resolución de contratos desde el payload (sólo lectura), validación por entrada, validación del manifest, resolución de procedencia, reporte texto + `--json`, contrato de exit codes |
| `tests/test_check_discovery_output.py` | 42 pruebas: positivos, negativos, falsación, fronteras, determinismo, ausencia, invalidez, sólo-lectura, stdlib-only, CLI |
| `tests/test_discovery_output_dogfood.py` | 12 pruebas ancladas al payload real, sólo lectura: resolución de contratos, enum de shape, frontera declarada, no-escritura |

**Los once puntos deterministas** de §«Naturaleza mecánica» están implementados; los **seis ítems de juicio** (stack real, dependencias reales, patrones con ejemplo, secretos, claims sin fuente, merge consistente, api↔shape) **no** se convirtieron en checks y un test de frontera verifica que el checker no reporta nada sobre ellos. El comportamiento de `F-17` es el autorizado: `GAP` advisory, nunca `ANOMALY`, sin exención ad-hoc, sin tocar el payload. El de `F-16`: se aceptan los seis valores del enum y no se decide el shape correcto.

**Autonomy summary (plan 135 §11; derivado de la evidencia, no de una métrica nueva).**

| Campo | Valor |
|---|---|
| `authorized_steps` | 10 pasos autorizados por este Plan |
| `autonomous_steps` | 10 ejecutados sin intervención operacional humana |
| `human_operational_interventions` | 0 |
| `human_authority_decisions` | 1 (la autorización de ejecución, `<PLAN-136>:PC-1`) |
| `findings_detected` | 6 (F-1 y F-2 del intake; F-3 a F-6 de la ejecución) |
| `findings_autonomously_corrected` | 4 (F-3 a F-6, todos determinísticos y dentro del scope) |
| `findings_escalated` | 2 (F-1 y F-2: fronteras de payload, no resolubles sin RFC-56) |
| `recoveries` | 5 (tres defectos de la propia suite/fixtures detectados por la suite; el mapeo de contratos; la cobertura de la rama `BOUNDARY`) |
| `stop_conditions` | 0 detenciones por frontera de autoridad durante la ejecución |
| `deferred_branches` | 2 (los pendientes de payload `PC-2` y `PC-3`, preservados y no ejecutados) |

**Distinción estricta.** `human_operational_interventions = 0`: el humano no operó ningún paso. `human_authority_decisions = 1`: la autorización de ejecución, que es la frontera funcionando como se diseñó, no un fallo de autonomía. No hubo ninguna detención por frontera durante la ejecución: las dos fronteras de payload (`F-17` y `F-16`) ya estaban identificadas en el Plan y el diseño las **rodea sin resolverlas**, así que no bloqueaban trabajo autorizado; sus pendientes quedan preservados.

**Ciclos autónomos.** La secuencia real fue `observe → derive → implement → test → detect → correct → verify → revalidate → continue` sin handoffs: se detectaron y corrigieron cinco defectos propios de forma autónoma (mapeo de contratos por convención inexistente, secciones de contrato declaradas en forma de prosa, prefijo de cita del payload, colisión de fixtures y ausencia de cobertura de la rama `BOUNDARY`), y se corrigió además la contradicción interna del Plan entre su scope y su determinación de Roadmap Impact — corrección que, por decisión humana posterior, **excedió el Scope** (ver `<PLAN-136>:F-3` y `<PLAN-136>:PC-4`).

**Verificación realizada.** Batería canónica completa: `check_protocol_invariants` OK (215 archivos, 10256 referencias), `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts` y `check_version_state` en verde; `python -m pytest tests/` **953 passed, 0 failed**; `check_discovery_output.py --root .` exit 0 con `N/A` (el repo DEV no es un target de discovery). Gates sobre el árbol validado: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`**, con `ANOMALY=0` en los tres. El GAP ambiental de temporales de pytest de los Planes 121–135 **no se reprodujo**.

**Alcance respetado — con una excepción decidida como defecto.** `protocol/`, `runtime/` y `.agents/`: **0 diff**. Las rutas autorizadas del `Scope` fueron las únicas tocadas **salvo `ROADMAP.md`**, que estaba excluido del `Scope` y fue modificado igualmente: es el defecto `<PLAN-136>:F-3`, decidido por el mantenedor en `<PLAN-136>:PC-4` como **exceso de scope** (la determinación de `Roadmap Impact: REQUIRED` no autoriza por sí sola la escritura de un artefacto excluido). El checker **no** se agregó a la batería canónica: `docs/VERSIONING.md` §4.1 intacto, conforme a la stop condition 3.

**Intervención posterior del mantenedor (2026-09-15): decisión sobre F-3.** El mantenedor determinó que **no** autorizó implícitamente la modificación de `ROADMAP.md` por el solo hecho de que el Plan declarara `Roadmap Impact: REQUIRED`, porque `ROADMAP.md` había sido excluido explícitamente del `Scope`; trató F-3 como pending decision de autoridad y ordenó no inferir su resolución. Esta intervención **sólo** registra esa decisión: corrige las afirmaciones del propio Plan que presentaban la modificación como autorizada (secciones «Scope», «Delegación agentiva», «Artefactos afectados», «Roadmap Impact» y «Validation anchor»), registra la decisión en `<PLAN-136>:PC-4`, actualiza la metadata de `<PLAN-136>:F-3` sin marcarlo `resolved` y sin reescribir sus elementos inmutables, y **no** revierte la modificación de `ROADMAP.md`: la decisión sobre revertirla, conservarla o rehacerla queda pendiente como decisión humana explícita en `<PLAN-136>:PC-4` (b). No se modificó ninguna política, RFC, ADR, `protocol/`, `runtime/`, el checker ni sus suites.

**Estado del repositorio.** `dev`, un commit atómico. Sin push, sin merge, sin tag, sin release, sin promotion. Ningún artefacto cerrado modificado; ningún ADR/RFC creado.

## Resolución post-cierre de F-3 (A y B)

*Registro posterior al cierre. **No** modifica el `Scope`, el `Task`, los Artefactos afectados, el anchor, el checkpoint ni ningún elemento inmutable de este Plan: la resolución de F-3 fue una acción **posterior y explícitamente autorizada**, no una autorización retroactiva de la ejecución de D01.*

La decisión humana vigente, normativa para esta resolución, es:

> `Roadmap Impact: REQUIRED` **no** amplía implícitamente el `Scope` autorizado de un Plan. Si `ROADMAP.md` está explícitamente fuera de Scope, su modificación durante la ejecución es una acción fuera de alcance y no queda autorizada retrospectivamente por la determinación `REQUIRED`.

Sobre esa base se resolvieron **independientemente** los dos cambios que la ejecución había hecho en `ROADMAP.md`:

- **Cambio A — eliminación de la fila de D01: CONFIRMADO como reconciliación factual.** La fila declaraba `Próximo dogfood`, que es falso: D01 está implementado (`tools/check_discovery_output.py`), verificado (`pytest tests/` 953 passed con sus 54 pruebas), committed (`3b94611`), y este Plan está `Executed` con condición derivada `Closed`. Evidencia: este Plan y su anchor A1; `docs/plans/INDEX.md` (fila del Plan 136); `CHANGELOG.md` (`[Unreleased]`, plan 136); `tools/check_discovery_output.py` y sus dos suites. **Clasificación: reconciliación de estado operativo, no decisión normativa.** La eliminación se conserva.
- **Cambio B1 — secuencia (`Estado`): CONFIRMADO.** `ROADMAP.md` registraba `EARS structural validator` como `Siguiente dogfood, después de B-1`, y el Plan 132 documenta esa secuencia como decisión explícita. Completar `B-1` **cumple la condición** `después de B-1`, de modo que `Próximo dogfood` es el estado correcto. Evidencia: `ROADMAP.md` vigente antes de la ejecución de D01 (`f0d9c03`), `docs/plans/132-roadmap-current-state.md` (clasificación `B-2` derivado, `Siguiente dogfood, después de B-1`), `docs/plans/INDEX.md` §Backlog evidenciado - plan 19. **Decisión: se conserva `Próximo dogfood`.**
- **Cambio B2 — prioridad (`Media` → `Alta`): NO SUSTENTADO; se restituye `Media`.** No existe evidencia documental que justifique `Alta` para la entrada derivada. El ítem histórico `B-2` fue `Alta` **por su propio motivo y en su propio contexto** («un fallo de formato cuesta una fase RECOVERY completa», `docs/plans/INDEX.md`), mientras la entrada derivada `EARS structural validator` fue registrada **`Media`** por el Plan 132, y `ROADMAP.md` establece que no se recalifica una entrada sin evidencia nueva. D01 terminado no aporta evidencia sobre la importancia intrínseca de EARS: sólo cumple su condición de secuencia. Evidencia de la corrección: el diff de `ROADMAP.md` en esta resolución restituye `Media`. **Decisión: `Media`.**

**Independencia de las tres decisiones.** A no justifica B2: que D01 haya terminado vuelve obsoleta la fila de D01, y no dice nada sobre la prioridad de EARS. B1 no implica B2: la secuencia (qué se ejecuta después) y la prioridad (cuánta importancia relativa tiene) son dimensiones distintas, y `ROADMAP.md` declara explícitamente que la prioridad `Media` de EARS provenía de su posición en la secuencia; cumplida la condición de secuencia, la prioridad no se sigue de ella. La regla del mapa es que no se recalifica sin evidencia documental nueva, y no la hay.

**Estado del finding.** `<PLAN-136>:F-3` permanece `open`: la transición a `resolved` es una decisión humana con evidencia (CL-8, ADR-16 AU-3) y esta ejecución no la tomó. La resolución de A, B1 y B2 queda determinada y registrada aquí, de modo que el finding queda **`ready for human resolution`**. La decisión humana ya tomada y aplicada es la de `<PLAN-136>:PC-4` (a); la parte (b) de `PC-4` —revertir, conservar o rehacer— queda **resuelta en su alcance**: A y B1 se conservan, B2 se corrige; ninguna otra modificación de `ROADMAP.md` permanece pendiente.

**Gap de gobernanza, registrado y no resuelto.** La investigación de F-3 detectó que la política vigente no define qué ocurre cuando una determinación de cierre obliga a tocar un artefacto que el `Scope` excluye: `REQUIRED` no implica autorización, y `DEFERRED` exige una pending decision existente que al redactarse el Plan puede no existir todavía. Queda **registrado como observación** en `<PLAN-136>:PC-5`, sin crear un cuarto valor, sin modificar la policy, sin crear estados ni mecanismos nuevos y sin redactar RFC/ADR.

## Metadatos de estado (evolucionables)

*Registro posterior al cierre, agregado por el Plan 139 (2026-09-20) en cumplimiento de
DEC-1 de ese Plan. **No** modifica el `Scope`, el `Task`, la Delegación agentiva, la
tabla de Artefactos afectados, el anchor, el checkpoint, la Nota de ejecución ni
ninguna sección normativa de este Plan: es la transición de estado del finding, que
es metadata **evolucionable** según
`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional;
LC-1, Incremento 2)`. Los elementos inmutables del finding —identidad, observación
original, evidencia original, estado Git observado y provenance original— se
conservan **verbatim** en el registro de `### Findings`.*

**`<PLAN-136>:F-3` — transición `open` → `resolved`.**

- **Acto.** Decisión humana del mantenedor (2026-09-20), materializada por el Plan
  139; el agente no infirió la resolución (CL-8; ADR-16 `AU-3`).
- **Justificación mínima (DEC-1).** (1) El Plan 136 incurrió efectivamente en una
  modificación fuera de `Scope`: la escritura de `ROADMAP.md` que el registro de
  `### Correcciones` conserva como `<PLAN-136>:C-3` con autorización **no**
  establecida. (2) El Plan 138 introdujo enforcement **previo a la delegación**
  basado en el Scope autorizado, verificado contra el Scope que el Plan declara y no
  contra la declaración bajo prueba. (3) La regresión específica de ese enforcement
  demuestra que el intento equivalente se detiene **antes** de ejecutar al Worker:
  `tests/test_sae_scope_enforcement.py` (`test_f3_regression_stops_before_the_write_and_leaves_everything_identical`:
  parada `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`, sin delegación persistida, sin
  Worker Result, artefacto excluido byte-idéntico, invoker nunca alcanzado) y
  `test_the_old_single_path_check_would_have_authorized_this_action`, que fija
  exactamente la ceguera estructural que produjo el incidente. (4) La evidencia
  histórica de este Plan **no** se modifica: observación, evidencia, estado Git y
  provenance del finding quedan intactos.
- **Efecto sobre el estado del finding.** `<PLAN-136>:F-3` queda formalmente
  `resolved`. Este registro es el acto de transición; su continuidad no requiere
  ninguna acción adicional.
- **Nota de no retroactividad.** La transición **no** legitima retrospectivamente la
  modificación de `ROADMAP.md` que la ejecución realizó, ni autoriza la del Plan 136:
  `<PLAN-136>:C-3` conserva su declaración de autorización **no** establecida, y la
  decisión humana `<PLAN-136>:PC-4` (a) —`Roadmap Impact: REQUIRED` no amplía el
  `Scope`— permanece vigente y ahora es regla operacional
  (`.agents/policies/validation-closure.md` §5.1/§5.2, cerrada por
  `<PLAN-138>:PC-1`).

