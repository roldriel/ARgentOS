# Plan 137 — EARS Structural Validator (auditoría de cobertura EARS y guarda de paridad)

**Status:** Aprobado para redacción
**Fecha:** 2026-09-15
**RFC:** — (vía plan; DEV-only: `tools/` + `tests/` + `docs/`, sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L1 (coordinación 1 agente; scope `tools/` + `tests/` + `docs/`, un artefacto nuevo; impacto arquitectónico: ninguno; sin impacto de release; duración <1 sesión)
**Depende de:** plan 66 + RFC-57 (validador estructural del harness — entregado), plan 33 + RFC-34 (forma canónica EARS — entregado), plan 136 (D01 Mechanical Checker — convenciones DEV reutilizables), plan 135 (SAE, habilita la ejecución autónoma)
**Origen:** `ROADMAP.md:Trabajo activo / dogfood` — «EARS structural validator» (`B-2` derivado, **Media / Próximo dogfood**); reconstrucción de intake de este Plan (§«Reconstrucción»), que **corrige la premisa de esa entrada**

## Reconstrucción: qué es hoy la validación EARS

Reconstruido contra el repositorio en `c9cec35`, no inferido del diseño histórico. **El hallazgo principal es que lo que el roadmap describe como trabajo futuro ya existe en el payload.**

**Qué es EARS en ARgentOS.** Un estándar de redacción de criterios de aceptación: `protocol/.agents/standards/requirements/EARS.md`, con **cinco patrones** de oración y cinco reglas de redacción (un criterio por bullet; usar `shall`; evitar negaciones; ser específico; ser verificable).

**Forma canónica (decidida y materializada).** `RFC-34` (`Accepted`, 2026-08-12) y el plan 33 resolvieron que **los bullets Markdown son la forma canónica** de `## Acceptance Criteria`, un bullet por criterio EARS, atómico y verificable; el bloque TOML `acceptance_criteria` es una representación machine-readable **opcional y derivada** que no reemplaza a los bullets. El contrato lo declara textualmente (`protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`): «The canonical form is one Markdown bullet per criterion», y «an artifact whose criteria appear only in the TOML block does not satisfy the canonical form».

**El validador estructural ya existe y ya cubre EARS.** `protocol/.agents/harness/gate_validator.py` (entregado por el plan 66 bajo RFC-57) implementa el subconjunto `[gate]` de las policies, y **incluye el chequeo EARS de H01**: el spec de `TRIGGERS["H01"]` activa `"ears": True` y el bloque de validación correspondiente lee `## Acceptance Criteria`, extrae los bullets (`-`/`*`) y falla si alguno no casa `EARS_RE` — una regex que implementa los cinco patrones. Está **cubierto por tests** (`protocol/.agents/harness/tests/test_gate_validator.py`: `test_valid_h01_passes`, `test_non_ears_bullet_fails`) y **corre en CI** (job `check-protocol` de `.github/workflows/check-protocol.yml`, líneas 32–33). Verificado por ejecución en esta investigación: un bullet `- The API should handle errors gracefully.` produce `ears FAIL — 1 bullets do not match EARS` y `decision: FAIL`.

**Qué significa eso para B-2.** El ítem histórico `B-2` tenía dos partes: `F-01` (desalineación contrato ↔ validador EARS: el contrato mostraba el array TOML como forma canónica mientras el validador leía bullets) y `F-02` (árbol de recovery sin rama de retry de formato, cubierto por el plan 29). **`F-01` está resuelto**: el contrato declara los bullets como canónicos, el validador los lee, y ambos están alineados y verificados. La entrada del roadmap describe `EARS structural validator` como una **extensión futura inexistente** (mismo patrón que la entrada de D01), pero a diferencia de D01 —donde el contrato declaraba explícitamente que la validación mecánica no existía— acá el mecanismo **sí existe**, en el payload, entregado por RFC-57.

**Decisión de coherencia que el roadmap describe al revés.** El propio repositorio declara que la validación EARS es **mixta**, no puramente mecánica: la policy H01 marca el patrón EARS como `[gate]` (ítem 11) y la no-compoundidad como `[agent]` (ítem 12), «declared judgment», con la regla de que un criterio es compuesto cuando «and»/«or» separan acciones o condiciones independientes pero **no** cuando enumeran valores del mismo dominio — una distinción que exige interpretación. Las cinco reglas de redacción restantes (¿es específico?, ¿es verificable?, ¿evita negaciones?, ¿es apropiado para el dominio?) son `[agent]`.

**Decisiones ya tomadas (no se reinterpretan).** Los bullets son la forma canónica (RFC-34/plan 33). El validador estructural es **opcional, fail-open, y su salida es evidencia, nunca gate**: el juicio del Orchestrator sigue siendo el árbitro (RFC-57, `harness/INDEX.md`). El validador **no** cubre los ítems `[agent]` (RFC-57 §Reglas de borde). D01 y S00 quedan fuera de su alcance por diseño.

**Boundary registrado, no resuelto.** El roadmap (`ROADMAP.md:Trabajo activo / dogfood`) aún presenta esta entrada como trabajo futuro con estado **Próximo dogfood**, lo que la evidencia contradice. **`ROADMAP.md` está fuera del `Scope` de este Plan** y la lección de `F-3` del Plan 136 es vinculante: una determinación de impacto **no** autoriza escribir un artefacto excluido del scope. La corrección del roadmap se registra como pending decision (`<PLAN-137>:PC-1`) para decisión humana; este Plan **no** la ejecuta.

## Objetivo

Producir la **verificación reproducible de que la validación EARS está efectivamente implementada, es determinista y coincide con lo que el contrato y el estándar declaran** — y dejar registrada, con evidencia, la frontera entre su subconjunto mecánico y el juicio que permanece humano.

El objetivo **no** es implementar un validador EARS: ya existe en el payload. El objetivo es **auditar la cobertura EARS y convertirla en una guarda de paridad DEV** que falle si el contrato, el conjunto mecánico declarado y el validador del payload dejan de coincidir. Eso es trabajo real, acotado y no duplicativo: no reimplementa la validación, la **verifica desde afuera** y protege la coherencia que `F-01` rompió una vez.

**Este Plan se aprueba sólo para redacción.** Su `**Status:**` es `Aprobado para redacción`: **no** está autorizado para ejecución. La autorización de ejecución es una decisión humana posterior (§«Criterio de entrada»).

## Problema

`F-01` documenta el costo real de que el contrato y el validador EARS se desalineen: un gate FAIL, una fase `RECOVERY` completa y re-trabajo del writer. La alineación se corrigió (plan 33 + plan 66), pero **nada la protege**: no existe una verificación que falle si el contrato vuelve a declarar otra forma canónica, si el validador deja de chequear EARS, o si el subconjunto declarado como mecánico diverge de lo que el validador realmente hace. La paridad vive hoy sólo en la prosa de dos documentos y en un test del payload que no conoce el contrato.

El riesgo es concreto: una divergencia futura entre `EARS.md`, `TASK_SPECIFICATION.md` y `gate_validator.py` reintroduce exactamente el fallo que `F-01` describió, y se detectaría en producción (una sesión de adopción) en lugar de en este repositorio.

## Naturaleza mecánica: qué subset está justificado

**A. Mecánicamente verificable (entra en esta auditoría/guarda).** Sólo lo que se decide leyendo texto y comparando, con fuente normativa explícita:

| # | Regla | Fuente normativa | Criterio determinista |
|---|---|---|---|
| R1 | `## Acceptance Criteria` contiene **al menos un bullet** (`-` o `*`) | `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md:Gate Checklist` ítem 3; `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria` | ¿existe ≥1 línea que tras `lstrip` empiece por `-`/`*` en la sección? |
| R2 | Cada bullet casa **uno de los cinco patrones EARS** | `protocol/.agents/standards/requirements/EARS.md:Patterns`; `H01` ítem 11 (`[gate]`) | ¿la oración casa el patrón correspondiente? |
| R3 | Criterios presentes **sólo** en el bloque TOML `acceptance_criteria` constituyen violación de forma | `H01:Gate Checklist` ítem 3; `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria` | ¿la sección tiene bullets **y** el TOML no los reemplaza? |
| R4 | El validador del payload **realmente** chequea EARS para H01 | `gate_validator.py` (spec `TRIGGERS["H01"]["ears"] = True`) | ¿la ejecución produce una entrada `ears` con PASS/FAIL? |
| R5 | **Paridad** entre el conjunto mecánico declarado y el implementado | `RFC-57:Alcance`; `H01` | ¿el conjunto de patrones que la guarda conoce == el que el validador acepta/rechaza? |

**B. NO mecánicamente verificable — permanece juicio.** No se convertirá en regla:

| Ítem | Por qué exige interpretación | Clasificación existente |
|---|---|---|
| ¿el criterio es **específico**? | juzgar si los inputs/outputs son concretos | `H01` ítem 10 `[agent]` |
| ¿el criterio es **verificable**? | juzgar si un test podría confirmarlo | `H01` ítem 10 `[agent]` |
| ¿el criterio es **compound**? | distinguir «crear X y enviar Y» de «HTTP 200 o 201» | `H01` ítem 12 `[agent]` |
| ¿evita **negaciones**? | `protocol/.agents/standards/requirements/EARS.md:Writing rules` 3 es una regla de redacción, no un patrón | no clasificada por el payload |
| ¿evita **`should`/`must`/`will`/`may`**? | idem: regla de redacción sin marca `[gate]` | no clasificada por el payload |
| ¿es **apropiado para el dominio**? | conocimiento del dominio | `H01` ítem 10 `[agent]` |
| ¿deriva de una **assumption no confirmada**? | requiere cruzar con `Assumptions` y su confirmación | `H01` ítem 16 `[agent]` |

**Frontera declarada importante.** `protocol/.agents/standards/requirements/EARS.md:Writing rules` 2 y 3 (usar `shall`; evitar negaciones) **no** están marcadas `[gate]` por H01 y su enunciado es léxico, no estructural: «evitá `should`» y «evitá negaciones» no definen de forma cerrada qué cuenta como negación ni cubren los cinco patrones. **No se implementan como reglas mecánicas** en este Plan. Se registran como posible extensión futura (`<PLAN-137>:PC-2`), porque incorporarlas al conjunto mecánico sería **ampliar el contrato del payload** y requiere autorización por RFC-56.

## Subset excluido

Todo el bloque B de la sección anterior queda **explícitamente fuera**: la guarda **no** juzga especificidad, verificabilidad, no-compoundidad, negaciones, vocabulario modal, adecuación al dominio ni derivación desde assumptions. Un test de frontera demuestra que la guarda **no** se pronuncia sobre ellos (silencio declarado, no aprobación silenciosa).

## Contrato del validator (guarda de paridad)

**Naturaleza.** Herramienta **DEV**, de sólo lectura, que audita la cobertura EARS comparando tres fuentes: el estándar (`EARS.md`), el contrato (`TASK_SPECIFICATION.md`) y la implementación del payload (`gate_validator.py`). **No** reimplementa la validación EARS: la **invoca** sobre un corpus y verifica la paridad del conjunto mecánico.

1. **Entrada exacta.**
   - `--payload PATH` (default `protocol/.agents`): raíz del payload, para localizar `standards/requirements/EARS.md`, el contrato de `TASK_SPECIFICATION.md` y `harness/gate_validator.py`.
   - `--root PATH` (default `.`): raíz del proyecto, para resolver un corpus opcional.
   - `--corpus PATH` (opcional, repetible): archivo(s) `TASK_SPECIFICATION.md` (o fragmentos con `## Acceptance Criteria`) a auditar.
   - Sin `--corpus`: la guarda corre sólo las verificaciones de **paridad** (R4, R5) y de **coherencia documental** (R3 contra el contrato), y declara la ausencia de corpus como `N/A` explícito.
2. **Fuente de verdad del formato EARS.** Triple, y **ninguna propia de la herramienta**: `protocol/.agents/standards/requirements/EARS.md:Patterns` (los cinco patrones), `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria` (la forma canónica: bullets) y `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md:Gate Checklist` (qué ítem es `[gate]`). La herramienta **no** mantiene su propia lista de patrones: **deriva** el conjunto del estándar y lo contrasta con el validador.
3. **Reglas incluidas.** R1–R5 de §«Naturaleza mecánica».
4. **Reglas excluidas.** Todo el bloque B, por nombre.
5. **Resultado de cada regla.** `VALID` / `GAP` / `ANOMALY` / `BOUNDARY` / `N/A`, con la razón y la cita `ruta:sección` de la fuente que la exige.
6. **Exit codes (contrato existente del repositorio).** `0` sin `ANOMALY` (**`GAP` es advisory y nunca cambia el exit code**); `1` ante al menos un `ANOMALY`; `2` ante error de lectura irrecuperable.
7. **Formato de salida.** Reporte de texto (una línea por artefacto con señal y razón, más `Summary:`) y `--json` opcional, en la forma de los checkers existentes. **No se inventa formato.**
8. **Determinismo esperado.** Salida byte-idéntica para el mismo input; orden de corpus y de evaluaciones determinista (ordenado, no dependiente del filesystem). Sin reloj, sin red, sin estado.
9. **Comportamiento frente a datos incompletos.** Una sección `## Acceptance Criteria` ausente o vacía es `GAP`/`N/A` declarado, nunca `VALID` por vacío. Un corpus que no existe es `N/A` explícito.
10. **Comportamiento frente a referencias no resolubles.** Una cita del contrato o del estándar que no resuelve es `ANOMALY` (evidencia presente pero contradictoria); una fuente ausente es `GAP` (evidencia faltante).
11. **Distinción GAP / ANOMALY / FAIL / N/A.** `GAP` = evidencia faltante o no obtenible (advisory); `ANOMALY` = contradicción verificable; `N/A` = ausencia declarada legítima; `BOUNDARY` = ambigüedad estructural que requiere revisión humana. `FAIL` es vocabulario del **validador del payload** (su decisión PASS/FAIL); la guarda lo **reporta** como evidencia, no lo produce como clasificación propia. La distinción se documenta explícitamente para no confundir los dos vocabularios.
12. **Política de read-only.** La guarda no escribe, no repara y no archiva nada: ni en el payload, ni en el corpus, ni en el proyecto. Verificado por test (snapshot antes/después).

## Inputs y Outputs

**Inputs.** El payload (tres fuentes de verdad, sólo lectura) y, opcionalmente, un corpus de artefactos con criterios de aceptación. Fuera del payload no hay corpus de sesión versionado en este repositorio (§«Dogfood»).

**Outputs.** Reporte de cobertura EARS por regla y por artefacto, con evidencia; la lista del **subconjunto mecánico establecido** con su fuente; y la lista explícita de lo excluido. La salida es **evidencia factual**, nunca autoridad normativa (ADR-16).

## Reutilización

| Mecanismo existente | Se reutiliza | Por qué |
|---|---|---|
| `protocol/.agents/harness/gate_validator.py` | **Se invoca, no se duplica** | Es la implementación vigente de la validación EARS; reimplementarla crearía una segunda fuente de verdad para el mismo contrato |
| Estructura del checker DEV de D01 (`tools/check_discovery_output.py`) | **Sí** | Compatibilidad de contrato verificada: mismo patrón (`argparse` con `--root`/`--payload`, stdlib pura, señales `VALID`/`GAP`/`ANOMALY`/`BOUNDARY`/`N/A`, exit `0`/`1`/`2`, texto + `--json`, sólo lectura). Es una **convención compartida**, no un acoplamiento: la guarda EARS no comparte código con D01, comparte contrato |
| `tests/testsupport.py` — función `assert_tool_imports_only_stdlib` | **Sí** | Helper existente para el contrato «stdlib pura» |
| `tests/pytest_isolation.py` | **Sí** | Único mecanismo de temporales fuera del repo (`tests/AGENTS.md`) |
| Patrón de **módulo anclado al repo real** (`tests/test_discovery_output_dogfood.py`, `tests/test_autonomous_scope_dogfood.py`) | **Sí** | Precedente documentado en `tests/AGENTS.md` para leer el payload real a propósito |
| Gates C-1/C-2/C-3, batería canónica, SAE | **Sí** | Sin cambios; este Plan los usa como están |

**No se reutiliza** nada de D01 más allá de la convención: la guarda EARS no lee contratos de discovery, no comparte módulos y no depende de `check_discovery_output.py`. El único acoplamiento compartido legítimo es el contrato de herramienta DEV, y se declara como tal.

## Tests

**Positivos.** Un corpus mínimo armado **desde la forma canónica documentada** (`protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`) que pasa: cada uno de los **cinco** patrones representado por su ejemplo del estándar (`protocol/.agents/standards/requirements/EARS.md:Patterns` ejemplos 1–5), y los tres aceptables de `protocol/.agents/standards/requirements/EARS.md:Examples for this project` ⇒ R1/R2 `VALID` y paridad R5 `VALID`.

**Negativos (falsación; cada uno debe fallar de forma explícita y reproducible).**

| Escenario | Señal esperada |
|---|---|
| Sección `## Acceptance Criteria` sin bullets | `GAP`/`N/A` declarado, exit 0 |
| Criterios **sólo** en el bloque TOML `acceptance_criteria` | `ANOMALY` (violación de forma canónica, R3) |
| Bullet que no casa **ningún** patrón (p. ej. `- The API should handle errors gracefully.`, no-aceptable de `EARS.md`) | `ANOMALY` (R2) |
| Bullet que casa un patrón pero es **compound** (`- The API shall validate input and return errors.`, no-aceptable de `EARS.md`) | **Sin hallazgo de la guarda** — frontera: es juicio `[agent]`; el test lo demuestra explícitamente |
| Bullet con negación (`- Users can't create accounts with bad data.`) | **Sin hallazgo** — frontera declarada (`protocol/.agents/standards/requirements/EARS.md:Writing rules` 3 no es `[gate]`) |
| Bullet que usa `should`/`must`/`will`/`may` | **Sin hallazgo** — frontera declarada (no es patrón) |
| Cita del contrato o del estándar que no resuelve | `ANOMALY` |
| Fuente de verdad ausente (p. ej. `EARS.md` no encontrado) | `GAP`, nunca `VALID` |
| El validador del payload deja de chequear EARS (spec H01 sin `ears`) | `ANOMALY` (R4: regresión de paridad) |
| El validador acepta un patrón que el estándar no declara, o rechaza uno que sí | `ANOMALY` (R5: **falso positivo / falso negativo** de la guarda y del validador) |

**Falsificación.** Los casos están diseñados para intentar **refutar** a la guarda, no para confirmarla: se incluye un caso que la guarda **debe dejar pasar aunque sea malo** (compound / negación / `should`) y uno que **debe fallar aunque parezca bueno** (sección con bullets que no casan patrón). Además se falsifica el **validador del payload**: si su regex y el estándar divergen, la guarda debe reportar `ANOMALY` en lugar de asumir que el payload tiene razón.

**Determinismo.** Dos corridas sobre el mismo input dan salida byte-idéntica; orden estable.

**Sólo lectura.** Snapshot del payload y del corpus antes/después de correr la guarda: idénticos. La guarda **no** invoca el validador con capacidad de escritura.

**Contrato de herramienta.** `assert_tool_imports_only_stdlib`; sin imports de módulos de `tools/` (o declarados y justificados).

## Dogfood

**Corpus real: limitación declarada.** La validación EARS aplica a `TASK_SPECIFICATION.md`, un artefacto de **sesión** en `.project/<session-uuid>/<iteration>/`, y `.project/` es efímero y no versionado (convención del repositorio, `AGENTS.md`). **No existe en el repositorio un corpus versionado de `TASK_SPECIFICATION.md`** — verificado: la búsqueda de artefactos de sesión fuera del payload no devuelve ninguno, y la única sesión presente en `.project/` no contiene especificaciones de tarea. **No se fabrican artefactos de producción para crear corpus.**

Por lo tanto el dogfood consiste en:

1. **Dogfood de payload real (obligatorio).** La guarda audita el payload **real**: verifica que `EARS.md` declara los cinco patrones, que el contrato declara los bullets como forma canónica, y que `gate_validator.py` realmente chequea EARS para H01 (R4) y que su conjunto aceptado coincide con el estándar (R5). Esta parte **sí** tiene evidencia real y es la que protege contra la regresión de `F-01`.
2. **Ejercicio del validador real sobre corpus construido con procedencia.** Para R1/R2/R3 se construyen especímenes **citando su origen normativo** (los ejemplos aceptables y no aceptables de `protocol/.agents/standards/requirements/EARS.md:Examples for this project`, y la violación de forma canónica descripta en `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`), y se ejecuta el **validador real del payload** sobre ellos. No son casos inventados: son los casos que el propio estándar y el propio contrato declaran.
3. **Declaración explícita de la limitación.** El Plan exige que la nota de ejecución registre que **no hubo** corpus real de `TASK_SPECIFICATION.md` y que, en consecuencia, la cobertura de R1/R2 sobre datos de producción **no** queda demostrada — sólo la paridad y la coherencia documental. Un `GAP` de corpus **no** se convierte en `PASS`.
4. **Caso de frontera real del validador.** Se documenta el comportamiento observado del validador ante un bullet no EARS real (`- The API should handle errors gracefully.` ⇒ `ears FAIL`), como evidencia de que el mecanismo opera.

Si el mantenedor puede aportar un `TASK_SPECIFICATION.md` real (de una sesión de adopción), el Plan indica incorporarlo como `--corpus` **sin copiarlo al repositorio** (se pasa por ruta) — decisión operativa del ejecutor, no requisito.

## Verificación

```bash
python tools/check_ears_coverage.py --payload protocol/.agents
python tools/check_ears_coverage.py --payload protocol/.agents --corpus <specimen> --json
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

Criterios objetivos y reproducibles:

1. La guarda reporta el **conjunto mecánico establecido** con la fuente de cada regla, y la lista explícita de lo excluido.
2. R4 y R5 (`VALID`) sobre el payload real: el validador chequea EARS y su conjunto coincide con `EARS.md`.
3. Los casos negativos fallan de forma explícita y reproducible, con la señal nombrada en §«Tests».
4. Los casos de frontera (compound, negación, `should`) **no** producen hallazgo, y el test lo demuestra.
5. `assert_tool_imports_only_stdlib` pasa; la guarda es de sólo lectura (snapshot antes/después idéntico).
6. Determinismo: dos corridas byte-idénticas.
7. `python -m pytest tests/` y `python -m pytest protocol/.agents/harness/tests/ -q` en verde, con el conteo exacto registrado.
8. Seis checkers canónicos en verde; `C-1`, `C-2`, `C-3` `VALID` con `ANOMALY=0`.
9. **`protocol/`, `runtime/` y `.agents/`: 0 diff** (el payload no se toca; se lee).
10. Documentation Impact y Roadmap Impact determinados (§ abajo), cada uno con su evidencia.
11. La nota de ejecución registra la **limitación de corpus** (§«Dogfood» 3) y no la convierte en `PASS`.

## Documentation Impact

```text
Documentation Impact: REQUIRED
```

Determinado para que la ejecución lo reconcilie; **no** se anticipa ninguna edición.

- **Contractual:** `tools/check_ears_coverage.py` y sus suites son artefactos nuevos; `docs/plans/137-ears-structural-validator.md` registra anchor, checkpoint, nota de ejecución y findings.
- **Operativa:** ninguno de `.agents/` cambia. La guarda **no** es un gate de lifecycle ni un paso obligatorio del workflow DEV: no se agrega a `docs/VERSIONING.md` §4.1 (igual que el Plan 136 — agregar un checker a la batería canónica crea una obligación de gobernanza sobre todo Change futuro y este Plan **no** la autoriza; si la ejecución concluyera que corresponde, **STOP** y escalar). `runtime/README.md` no se toca: la guarda no vive en `runtime/`.
- **Registro:** `docs/plans/INDEX.md` (fila y serie del Plan 137) y `CHANGELOG.md` (ítem `[Unreleased]` `(plan 137, RFC-—)`; docs-only/DEV-only, sin `VERSION` bump ni tag).
- **Normativa: `NOT_REQUIRED` y explícitamente NO autorizada.** `RFC-57`, `RFC-34`, `EARS.md`, `TASK_SPECIFICATION.md` y la policy H01 **no** se modifican: son la fuente de verdad que la guarda audita, y tocarlas requeriría RFC-56. Si la ejecución concluyera que un cambio de payload es necesario para que la paridad se sostenga, **STOP** y escalar (`<PLAN-137>:PC-2`).
- **Histórica: no se toca** (RFC-46): en particular el plan 33, el plan 66, el anexo de fricciones del plan 19 y las entradas históricas de `B-2`.

## Roadmap Impact

```text
Roadmap Impact: DEFERRED
```

*Reclasificación (Plan 140, 2026-09-20).* El Plan 137 declaró `REQUIRED` —la
obligación de reconciliar `ROADMAP.md`— y delegó su continuidad en
`<PLAN-137>:PC-1`, con `ROADMAP.md` explícitamente fuera del `Scope`. La regla
vigente (`.agents/policies/validation-closure.md` §5.2) fija que una determinación de
impacto es una **obligación de estado y nunca una autorización de escritura**, y que
cuando el artefacto que posee el estado está fuera del `Scope` la clasificación
correcta es `DEFERRED` con la pending decision **existente** que la gobierna. Este
Plan no escribió `ROADMAP.md` en ningún momento, de modo que la determinación se
reclasifica a `DEFERRED` sin cambiar ningún hecho: la obligación queda gobernada por
`<PLAN-137>:PC-1` (owner: mantenedor), que conserva la decisión futura y no requiere
acción del agente en el estado actual. El texto original de esta determinación, con
su contenido y su evidencia, se conserva íntegro en el historial de Git (RFC-46).

Determinado para que la ejecución lo reconcilie; **no** se ejecuta ahora y **no** se usa para escribir `ROADMAP.md`.

- **Artefacto a reconciliar: `ROADMAP.md`** (`## Trabajo activo / dogfood`). La entrada `EARS structural validator` (`B-2` derivado, `Media`, **Próximo dogfood**) describe como trabajo futuro una capacidad que **ya existe** en el payload (plan 66, RFC-57) y está cubierta por tests y CI. Al completarse este Plan, esa entrada queda **obsoleta** igual que quedó la de D01 tras el plan 136.
- **Por qué `REQUIRED`:** la entrada declara un estado (`Próximo dogfood`) que la evidencia contradice; el mapa operativo deja de representar el estado real, y ninguna otra categoría lo absorbe.
- **Boundary declarado — no se resuelve por inferencia.** `ROADMAP.md` **no** figura en el `Scope` de este Plan. La decisión humana de `F-3` (`<PLAN-136>:PC-4`) estableció que `Roadmap Impact: REQUIRED` **no** amplía el `Scope` autorizado: una determinación de impacto no es una autorización de escritura. Por lo tanto esta obligación de reconciliación **queda pendiente** y su continuidad vive en `<PLAN-137>:PC-1`, que es una pending decision **existente** del propio Plan (mecanismo PC-1, sin crear mecanismo nuevo). La ejecución **no** debe editar `ROADMAP.md` por su propia cuenta: si el mantenedor quiere la reconciliación, lo autoriza ampliando el scope o ejecutándola él.
- **Trabajo nuevo creado:** **ninguno** más allá de esta guarda. No se reclasifica ningún ítem histórico ni se eleva la prioridad de EARS: el estado del mapa (`Media`) es **input** de este Plan, no objeto de reinterpretación. `B-3` sigue candidato futuro; `F-14`/`F-16`/`F-17` siguen en la sección de pendientes que requieren autorización.

## Artefactos afectados

| Ruta | Acción | Contenido |
|---|---|---|
| `tools/check_ears_coverage.py` | crear | Guarda DEV de cobertura y paridad EARS: sólo lectura, stdlib pura |
| `tests/test_check_ears_coverage.py` | crear | Comportamiento, reglas R1–R5, clasificación, exit codes, determinismo, sólo lectura, stdlib-only, CLI |
| `tests/test_check_ears_coverage_falsification.py` | crear | Falsación del subset mecánico y de las fronteras (bloque B) |
| `tests/test_check_ears_coverage_dogfood.py` | crear | Módulo anclado al payload real, sólo lectura: R4/R5 y coherencia documental |
| `docs/plans/137-ears-structural-validator.md` | modificar | Este Plan: anchor, checkpoint, nota de ejecución y findings al ejecutarse |
| `docs/plans/INDEX.md` | modificar | Registro del Plan 137 y su serie |
| `CHANGELOG.md` | modificar | Ítem `[Unreleased]` `(plan 137, RFC-—)` |

`protocol/`, `runtime/`, `.agents/` y `ROADMAP.md`: **0 diff**.

## Delegación agentiva

- **Task:** Implementar `tools/check_ears_coverage.py`, la guarda DEV de sólo lectura que audita la cobertura EARS del payload y protege la paridad entre el estándar (`EARS.md`), el contrato (`TASK_SPECIFICATION.md`) y el validador del payload (`gate_validator.py`), siguiendo las reglas R1–R5 y **sin reimplementar** la validación EARS: la **invoca** y reporta con el vocabulario de señales y el contrato de exit codes existentes. Implementar las tres suites (comportamiento, falsación, dogfood anclado al payload real). Registrar el Plan en `docs/plans/INDEX.md` y `CHANGELOG.md`. **No** modificar `protocol/`, **no** modificar el validador del payload, **no** agregar la guarda a la batería canónica, **no** tocar `ROADMAP.md`, **no** convertir en reglas mecánicas los ítems del bloque B.
- **Scope:** `tools/check_ears_coverage.py`, `tests/test_check_ears_coverage.py`, `tests/test_check_ears_coverage_falsification.py`, `tests/test_check_ears_coverage_dogfood.py`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera de las siete rutas (incluye `ROADMAP.md`: ver §«Roadmap Impact» y `<PLAN-137>:PC-1`).
  - **`STOP_FORBIDDEN_AUTONOMY`** — tocar `protocol/`, `runtime/` o `.agents/`, en particular el validador del payload, `EARS.md`, el contrato de `TASK_SPECIFICATION.md` y la policy H01; release, promotion, tag.
  - **`STOP_AUTHORITY_REQUIRED`** — incorporar al conjunto mecánico cualquiera de los ítems del bloque B (negaciones, vocabulario modal, no-compoundidad), lo que **amplía el contrato del payload** y exige RFC-56; agregar la guarda a `docs/VERSIONING.md` §4.1; cambiar el `**Status:**` de este Plan fuera de los statuses del lifecycle.
  - **`STOP_AUTHORITY_REQUIRED`** — conflicto entre `EARS.md`, el contrato y el validador que **no** pueda resolverse determinísticamente: es una contradicción normativa de payload, se registra y se escala, no se resuelve reinterpretando una de las fuentes.
  - **`STOP_AUTHORITY_REQUIRED`** — evidencia insuficiente para alguna regla: se reporta `GAP`, no se inventa la regla.
- **Autoridad:** este Plan aprobado para ejecución, y ninguna otra. La guarda **no** sustituye el juicio del Orchestrator (RFC-57: el validador es soporte, el juicio es el árbitro) ni convierte su propia salida en autoridad normativa (ADR-16).
- **Stop conditions:** las de la policy SAE (`.agents/policies/supervised-autonomous-execution.md` §5) más las de arriba.

## SAE execution boundary

Diseñado para ejecutarse bajo `--sae` sin handoffs operacionales. **Pre-autorizado** dentro de Scope + Authority: observar el repositorio; derivar el diseño final de las cinco reglas; implementar la guarda y sus suites; correr tests y checkers; detectar findings; corregir defectos deterministas **dentro de las siete rutas**; revalidar; actualizar `INDEX.md` y `CHANGELOG.md`; continuar; cerrar cuando las condiciones se cumplan.

**Requiere STOP:** cambio de scope; decisión normativa; payload change; RFC/ADR; cambio de authority; cambio de Protocol; **interpretación semántica presentada como validación mecánica**; arquitectura nueva; evidencia insuficiente; contradicción normativa; cualquier escritura fuera de Scope (en particular `ROADMAP.md`); release/promotion/tag. No se diseñan mecanismos nuevos de SAE. La observabilidad existente (`authorized_steps`, `autonomous_steps`, `human_operational_interventions`, `human_authority_decisions`, `findings_detected`, `findings_autonomously_corrected`, `findings_escalated`, `recoveries`, `stop_conditions`) se registra con los mecanismos actuales, sin sistema nuevo de métricas.

## Human authority boundary

Reservado al humano: autorizar la ejecución de este Plan; cambiar su scope; decidir la reconciliación de `ROADMAP.md` (`<PLAN-137>:PC-1`); autorizar cualquier cambio de payload, RFC-56, RFC o ADR; autorizar la incorporación de reglas del bloque B al conjunto mecánico (`<PLAN-137>:PC-2`); resolver un conflicto normativo entre las tres fuentes; resolver findings; release y promotion. El ejecutor **no** puede convertir un `STOP` en un `CONTINUE` por inferencia.

## Stop conditions

Además de las de la policy SAE §5: las cinco de §«Delegación agentiva» (scope, forbidden autonomy, authority required ×3). Detienen y escalan sin excepción.

## Findings esperados

Findings **esperables** durante la ejecución (se registran con refs `<PLAN-137>:F-<n>` cuando ocurran, no se fabrican):

- **Posible `ANOMALY` de paridad:** que el conjunto de patrones aceptado por `EARS_RE` diverja del declarado en `protocol/.agents/standards/requirements/EARS.md:Patterns` (p. ej. por un patrón agregado a un lado y no al otro). Es el escenario que motiva la guarda; si no ocurre, se registra la ausencia como resultado `VALID`, no como finding.
- **Posible `GAP` de corpus:** ausencia de corpus real de `TASK_SPECIFICATION.md` (ya establecida en §«Dogfood»), que limita la cobertura de R1/R2 sobre datos de producción.
- **Posible `BOUNDARY`:** que la forma canónica del contrato y el bloque TOML opcional vuelvan a leerse como contradictorios por un lector nuevo (`F-01` textual). Se registra, no se resuelve: el payload no se toca.

## Pending decisions

- `<PLAN-137>:PC-1`: decisión: si corresponde reconciliar `ROADMAP.md` retirando la entrada `EARS structural validator` de `## Trabajo activo / dogfood`, dado que la capacidad ya existe en el payload (plan 66, RFC-57) y la entrada declara un estado que la evidencia contradice; blocking: **sí** para la reconciliación, **no** para ejecutar este Plan (la guarda no depende del roadmap); owner: mantenedor; escalación: `ROADMAP.md` **no** está en el `Scope` de este Plan y, por la decisión humana de `F-3` (`<PLAN-136>:PC-4`), `Roadmap Impact: REQUIRED` **no** amplía el scope autorizado; el agente no la resuelve por inferencia; resolución: **deferred** (clasificación materializada por el Plan 140 el 2026-09-20): la decisión sigue siendo del mantenedor y **no** está tomada; el Plan 140 la clasifica como **no accionable actualmente** —`ROADMAP.md` está fuera del `Scope` autorizado y no se ejecutó ninguna escritura— y su continuidad permanece en esta misma pending decision, sin acción pendiente del agente; evidencia: `ROADMAP.md:Trabajo activo / dogfood`, `protocol/.agents/harness/gate_validator.py` (spec H01 con `ears: True`), `protocol/.agents/harness/tests/test_gate_validator.py` (`test_non_ears_bullet_fails`), `.github/workflows/check-protocol.yml` job `check-protocol` líneas 32–33, `docs/rfc/57-harness-structural-validator.md:Alcance`, `docs/plans/66-harness-structural-validator.md`; efecto downstream: el mapa operativo sigue declarando como futuro un trabajo ya realizado; el Plan 137 se ejecuta igual; ADR-worthiness: no aplica.
- `<PLAN-137>:PC-2`: decisión: si el conjunto mecánico de EARS debe **ampliarse** para cubrir las reglas de redacción de `protocol/.agents/standards/requirements/EARS.md:Writing rules` 1–3 (un criterio por bullet —ya cubierto estructuralmente por R1—, usar `shall`, evitar negaciones) y la no-compoundidad (hoy `[agent]`); blocking: **no** para este Plan; owner: mantenedor; escalación: ampliar el conjunto mecánico **cambia el contrato del payload** (`EARS.md`, la policy H01 y su clasificación `[gate]`/`[agent]`) y por lo tanto requiere la vía RFC-56 (RFC + plan); el Plan 137 lo registra como frontera y **no** lo implementa; resolución: pendiente; evidencia: `protocol/.agents/standards/requirements/EARS.md:Writing rules`, `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md:Checklist` ítems 10/11/12; efecto downstream: sin esta decisión, la guarda documenta esas reglas como juicio y no las chequea, lo que es el comportamiento correcto y autorizado; ADR-worthiness: no evaluado — requiere decisión humana.
- `<PLAN-137>:PC-3`: decisión: si corresponde agregar `tools/check_ears_coverage.py` a la batería canónica (`docs/VERSIONING.md` §4.1); blocking: **no**; owner: mantenedor; escalación: incorporar un checker a la batería crea una obligación de gobernanza sobre todo Change futuro y este Plan no la autoriza; resolución: pendiente; evidencia: `docs/plans/136-d01-mechanical-checker.md` (precedente: D01 no se agregó); efecto downstream: la guarda se valida por su propia suite y por el dogfood; ADR-worthiness: no aplica.

## Criterio de entrada

- [ ] `**Status:**` de este Plan es `Aprobado para ejecución` (hoy es `Aprobado para redacción`).
- [ ] `## Delegación agentiva` presente, con `Task` y `Scope` no vacíos y el `Scope` con las siete rutas exactas.
- [ ] `## Verificación` presente, con el command-set exacto.
- [ ] Autoridad válida: la del propio Plan; sin autoridad implícita, sin RFC/ADR requerido, sin cambio de payload involucrado.
- [ ] Baseline del repositorio identificable: SHA y tree registrados al inicio de la ejecución.
- [ ] **Precondición de coherencia:** `protocol/.agents/harness/gate_validator.py`, `EARS.md` y el contrato de `TASK_SPECIFICATION.md` presentes y legibles; si alguno falta, la ejecución arranca con un `GAP` declarado y evalúa si el Plan sigue siendo ejecutable.
- [ ] Sin pending decision bloqueante para la ejecución (`PC-1`, `PC-2` y `PC-3` no bloquean).
- [ ] Dependencias conocidas: planes 33/RFC-34 y 66/RFC-57 cerrados; plan 136 cerrado; batería canónica verde.

## Criterios de salida

- [ ] `tools/check_ears_coverage.py` existe, es stdlib pura, de sólo lectura, e implementa R1–R5 **sin reimplementar** la validación EARS.
- [ ] El conjunto mecánico se **deriva** de las fuentes del payload; la guarda no mantiene una lista propia de patrones.
- [ ] Las tres suites en verde, cubriendo positivos, negativos, falsación, fronteras del bloque B, determinismo, sólo lectura, stdlib-only y CLI.
- [ ] R4/R5 `VALID` sobre el payload real; los casos de frontera **no** producen hallazgo.
- [ ] Batería canónica en verde; `pytest tests/` y `pytest protocol/.agents/harness/tests/ -q` en verde; C-1/C-2/C-3 `VALID` con `ANOMALY=0`.
- [ ] La limitación de corpus queda declarada en la nota de ejecución y **no** se reporta como `PASS`.
- [ ] `protocol/`, `runtime/`, `.agents/` y `ROADMAP.md`: 0 diff.
- [ ] Determinaciones de impacto registradas; commit atómico en `dev`.

## Criterio de cierre

Los estados se determinan así, sin reinterpretarlos (`.agents/policies/validation-closure.md` §6):

```text
Verified   = ∃ validation(PASS, anchor A1 registrado en este Plan)
Executed   = Plan status "Executed" (implementación + validación)
Committed  = estado del repositorio: el commit atómico en dev (no es un status de Plan)
Closed     = Executed ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor
             ∧ evidencia PASS para el estado de cierre
Promoted   = merge dev → master (acción del mantenedor)
Released   = tag anotado en master (acción del mantenedor)
```

`Committed ≠ Closed ≠ Promoted ≠ Released`. El cierre es **del Plan 137** (la guarda DEV), no de EARS ni del validador del payload: **`EARS.md`, la policy H01 y `gate_validator.py` no cambian de estado**. `Promoted` y `Released` no son objetivos de este Plan y quedan fuera de la autoridad del host (SAE los reporta `FORBIDDEN`).

## Riesgos

- **Duplicar la validación EARS (segunda fuente de verdad).** Mitigación: la guarda **invoca** el validador del payload y verifica **paridad**; no reimplementa los patrones, los deriva. Los criterios de salida lo exigen.
- **Convertir juicio en regla mecánica.** Mitigación: el bloque B está enumerado por nombre con su clasificación `[agent]`; un test de frontera demuestra el silencio deliberado; la stop condition de authority lo prohíbe.
- **Ampliar el contrato del payload de facto.** Mitigación: `PC-2` registra la ampliación como decisión de payload con vía RFC-56; la ejecución no la toma.
- **Escribir `ROADMAP.md` por inferencia (recaída de `F-3`).** Mitigación: `ROADMAP.md` está **explícitamente fuera del Scope**, la obligación queda en `PC-1` y la stop condition de scope la bloquea.
- **Reportar cobertura de producción sin corpus.** Mitigación: §«Dogfood» 3 obliga a declarar la limitación; un `GAP` de corpus no se convierte en `PASS`.

## Trazabilidad

`ROADMAP.md` (B-2 derivado, `Media` / Próximo dogfood) → `docs/plans/INDEX.md` §Backlog evidenciado - plan 19 (`B-2` = `F-01` + `F-02`, prioridad `Alta` **del ítem histórico**) → plan 29 (`F-02`: rama `RETRY_WORKER`) → plan 33 + RFC-34 (`F-01`: bullets como forma canónica) → plan 66 + RFC-57 (validador estructural del payload, con el chequeo EARS de H01) → plan 136 (convenciones DEV de checker y precedente de no agregar a la batería) → **Plan 137 (este Plan)** → `tools/check_ears_coverage.py` → ejecución autónoma bajo SAE. Continuidad de la frontera de roadmap: `<PLAN-137>:PC-1`. Continuidad de la frontera de contrato: `<PLAN-137>:PC-2`.

## Nota de redacción

Este Plan se redactó **sin implementar nada**: no existe `tools/check_ears_coverage.py` ni ninguna suite nueva, y `protocol/`, `runtime/`, `.agents/` y `ROADMAP.md` tienen 0 diff. Su hallazgo central —que el validador estructural EARS ya existe en el payload (plan 66, RFC-57) y que la entrada del roadmap lo describe como trabajo futuro— se registra como evidencia y se convierte en la pending decision `<PLAN-137>:PC-1`, **sin** resolverla por inferencia ni editar `ROADMAP.md`.

## Determinaciones del Plan 140 (B-2 y Roadmap Impact)

*Registro posterior a la redacción, agregado por el Plan 140 (2026-09-20). **No**
modifica el `## Objetivo`, el `## Contrato del validator`, el `## Scope`, la
Delegación agentiva, los `## Artefactos afectados`, la `## Documentación Impact`, el
`## Human authority boundary`, las `## Stop conditions` ni la `## Nota de redacción` de
este Plan: registra la determinación de estado de `B-2` y la reconciliación de su
determinación de `Roadmap Impact`.*

**1. `B-2` está satisfecho y no deja residual de trabajo.** El ítem histórico `B-2`
tenía dos partes —`F-01` (desalineación contrato ↔ validador EARS) y `F-02` (rama de
retry de formato)— y ambas están resueltas: `F-01` por el plan 33/RFC-34, que declaró
los bullets Markdown como forma canónica de `## Acceptance Criteria`, alineada con el
validador, y `F-02` por el plan 29. El **mecanismo responsable** existe en el payload y
opera: `protocol/.agents/harness/gate_validator.py` activa el chequeo EARS para H01
(`TRIGGERS["H01"]["ears"] = True`), implementa los cinco patrones del estándar en
`EARS_RE` y produce la señal `ears` PASS/FAIL. Cobertura y ejecución: la suite
`protocol/.agents/harness/tests/test_gate_validator.py` (incluye el caso de bullet no
EARS) y el job `check-protocol` de `.github/workflows/check-protocol.yml`. Evidencia
adicional obtenida por el Plan 140 con el validador real, de forma read-only y sobre
especímenes con procedencia: un bullet EARS produce `ears` PASS con
`decision: PASS`; el bullet no aceptable del estándar
(`- The API should handle errors gracefully.`) produce
`ears FAIL — 1 bullets do not match EARS` con `decision: FAIL`. **No se implementó
nada nuevo** para llegar a esta determinación.

**2. Lo que este Plan proponía no es un residual de `B-2`.** La guarda DEV de paridad
(`tools/check_ears_coverage.py` y sus suites) es trabajo **nuevo** de aseguramiento,
no una parte pendiente de `B-2`. Su ejecución no está autorizada: el `**Status:**` de
este Plan es `Aprobado para redacción` y su propio `## Criterio de entrada` exige
`Aprobado para ejecución`. `Superseded` **no** es una salida disponible, porque el
ciclo de status de planes exige indicar el plan reemplazante y no existe ninguno
(`docs/CONVENTIONS.md:Convenciones`; precedente del plan 87 ante la misma situación).
En consecuencia **no se cambia el status de este Plan** y la disposición de su guarda
—ejecutarla o retirarla— sigue siendo una decisión humana ya declarada en el
`## Criterio de entrada` y el `## Human authority boundary` de este mismo Plan.

**3. `Roadmap Impact` reclasificado a `DEFERRED`.** Ver `## Roadmap Impact`: la
obligación de reconciliar `ROADMAP.md` queda gobernada por la pending decision
existente `<PLAN-137>:PC-1` (owner: mantenedor), clasificada como no accionable
actualmente. `ROADMAP.md` permanece con **0 diff** en todo momento.

**4. No-acciones explícitas.** El Plan 140 **no** implementa la guarda, **no** modifica
`protocol/`, `tools/`, `tests/`, `runtime/`, `.agents/` ni `ROADMAP.md`, **no** cambia
el status de este Plan y **no** resuelve `<PLAN-137>:PC-2` ni `<PLAN-137>:PC-3`.
