# EXECUTION_HOST_SEMANTIC_AUDIT — 2026-10-14

```text
RESULT = SAFE_TO_EXPERIMENT

SECOND_OBSERVE_CLASSIFICATION = MIXED
  · NECESSARY  as the iteration's own observation (iterate must act on a fresh
               reading of the true current state)
  · ACCIDENTAL as a *duplicate* of the one run() already computed at host.py:1050
               (86/86 measured identical; nothing mutated in the window;
                present since the original commit of plans 122/123)

PRODUCTION_CHANGES = 0
TEST_CHANGES       = 0
CI_CHANGES         = 0
DEPENDENCY_CHANGES = 0

NEXT_ACTION = Design and run the bounded pilot of §21 (pass run()'s observation
              into iterate() at host.py:1083 and re-verify) as its own
              authorized Change, before touching any other call site.
```

**Clase documental:** Working / Audit (provenance) — **no normativo** (RFC-69,
`docs/AGENTS.md`).
**Naturaleza:** auditoría **semántica** `READ_ONLY`. No es un benchmark de
performance.
**Autoridad de este documento:** ninguna. Registra hechos, inferencias,
hipótesis e incógnitas. No crea mecanismos, no modifica la suite, no autoriza
trabajo y no decide arquitectura.
**Fecha:** 2026-10-14 · **Rama:** `dev` · **HEAD:** `fb0786a0b9b872796e5e4b223cf92bc011c22139`
**Restricción cumplida:** 0 cambios en producción, tests, CI, dependencias,
`protocol/`, `dist/` y `ROADMAP.md`. La instrumentación de la investigación vivió
**fuera del árbol versionado** y fue eliminada al terminar (§22).

**Relación con la auditoría previa.**
`docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md` midió que los
subprocesos son el 80.3 % del wall clock y que la observación es el mecanismo
dominante, y dejó **explícitamente abierta** la pregunta semántica: *"¿es la
segunda observación una redundancia accidental?"*. Ese informe la marcó como
`INFERRED`, no como hecho, y advirtió que el cambio *"toca host.py, que es la
pieza más cargada de garantías del repo"*. **Este documento responde esa
pregunta con evidencia de código, tests, documentación e historial**, y no
repite su análisis de performance.

**Marcas usadas en todo el documento**

| Marca | Significado |
|---|---|
| `FACT` | observado directamente en el árbol (código, documento, historial Git) |
| `MEASURED` | obtenido ejecutando una sonda read-only en esta máquina |
| `INFERENCE` | conclusión derivada de hechos/mediciones, no observada directamente |
| `HYPOTHESIS` | conjetura explícita, no verificada |
| `ESTIMATE` | extrapolación aritmética, declarada como tal |
| `UNKNOWN` | no determinado; se declara en lugar de suponerse |

---

## 1. Executive Summary

`FACT` `ExecutionHost` declara en su propio docstring (línea 405):
**`"The loop. It holds no state: every iteration observes from scratch."`**
Y la política que lo gobierna
(`.agents/policies/autonomous-orchestration.md:§1`) define la etapa `observe`
como *"re-read the repository and the persisted evidence (**no memory, no
session, no cursor**)"*, con `§9` añadiendo *"The host holds no state."*

`FACT` `run()` llama a `self.observe()` en `host.py:1050` y, en la misma
iteración, llama a `iterate()`, que **vuelve a llamar a `self.observe()`** en
`host.py:591` (`iterate` tiene esa observación como **única** fuente de su
estado). Entre ambas llamadas no hay **ninguna** operación mutadora: sólo
cálculos puros (`governance_fingerprint()`, `AuthorityBoundary(...)`,
`derive_next_action(...)`) y la bifurcación del guard de no-progreso.

`MEASURED` **Sonda de equivalencia**: dos observaciones consecutivas sobre el
mismo árbol producen payloads **byte-idénticos** (`sha256` del `to_dict()`
completo + lectura de `git_state`), en tres escenarios: fixture limpio, fixture
con historial de host (journal + worker results), y el par exacto
`run()→iterate()`. Coste de cada una: **6 subprocesos, ~0.33 s**.

`MEASURED` **Sonda de atribución en corrida real** (los 4 archivos dominantes,
152 tests, 444 llamadas a `observe()` instrumentadas con el número de línea del
caller):

```text
PARES CONSECUTIVOS SIN MUTACIÓN INTERMEDIA (idénticos, 100 %)
  par 1050 -> 591    86 pares   86 idénticos   0 distintos
  par  870 -> 872    45 pares   45 idénticos   0 distintos
  par 1154 -> 1287   29 pares   29 idénticos   0 distintos
  par 1287 -> 1117   29 pares   29 idénticos   0 distintos
  --------
  pares idénticos consecutivos: 189 de 189  (100 %), 0 excepciones

PARES CON ACCIÓN/ESCRITURA ENTRE MEDIAS (distintos, 100 %)
  pares  591->870 (45), 872->1050 (25), 1089->1154 (24), 872->1089 (20),
         591->1154 (17), 591->974 (16), 974->1050 (12), 769->1154 (5),
         591->769 (5), 974->1089 (4), y otros menores
  --------
  pares distintos: 187 de 187  (100 %), 0 excepciones
```

`INFERENCE` La separación es nítida: **cada par consecutivo o no tiene mutación
intermedia y es idéntico, o tiene una acción/escritura entre medias y difiere.**
No hay un solo caso ambiguo. Esto valida simultáneamente que `observe()` es
determinista y que el digest empleado detecta los cambios reales.

`FACT` **Corrección de una lectura previa de esta misma auditoría**: el orden
real al cierre de `run()` es `derived_conditions()` (**1154**) →
`write_run_report`/`render_run` (**1287**) → `_record_run_note` (**1117**), tal
como fija `host.py:1099-1112`. Una lectura inicial atribuyó los pares a
`(1117→1154)` y `(1154→1287)`; los datos crudos muestran `(1154→1287)` y
`(1287→1117)`. Las cifras de este informe son las verificadas contra el JSON de
la sonda.

`FACT` **El doble `observe()` no es un artefacto de la era de autonomía.**
`git log` sobre `runtime/orchestrator/host.py` muestra 5 commits; el **primero**
(`4f85e67`, "consolidate autonomous orchestrator and agent worker mvps (plans
122, 123)") ya tiene **11** llamadas a `self.observe()`, incluidas las dos de
`run()` e `iterate()`. Planes 135, 138 y 159 subieron el conteo a 12 y luego a
13, **sin tocar el par**: la duplicación precede a toda la maquinaria SAE.

`FACT` `observe()` es **read-only**: no escribe archivos, no muta
`ExecutionHost` (que sólo declara `_last_autonomy` / `_last_autonomy_drift`,
asignados por `iterate`, no por `observe`), y `observation.py` no usa reloj,
`random` ni `datetime` (grep: 0 coincidencias). El store es append-oriented y
`OrchestratorStore.__init__` sólo resuelve paths.

`FACT` **No hay concurrencia ni extensión**: ningún `import threading`,
`multiprocessing`, `signal` ni `asyncio` en `runtime/`; **ninguna** subclase de
`ExecutionHost` en todo el repositorio; `iterate()` se define y se llama **una
sola vez**, desde `run()`; y no es API pública (`runtime/orchestrator/__init__.py`
exporta `ExecutionHost`, `HostRun`, `ChangeObservation` y `observe`, **no**
`iterate`).

`MEASURED` **La redundancia no es un solo sitio.** Hay **tres** pares
consecutivos cuya segunda lectura no aporta ningún hecho nuevo, y un cuarto par
de lectura equivalente. En los 4 archivos dominantes: **189 de 444 llamadas
(42.6 %)** son el primer miembro de uno de esos pares, y consumen **74.6 s de
tiempo de subproceso** de los ~157 s que la observación cuesta en esos archivos
(`MEASURED` sobre tiempo de subproceso; ver §10.3).

`INFERENCE` **La segunda observación es `MIXED`.** Como *contrato de `iterate()`*
es `NECESSARY`: `iterate()` debe actuar sobre una lectura fresca del estado real,
y hoy esa lectura es su única fuente. Como *duplicado de la observación que
`run()` ya calculó*, es `ACCIDENTAL`: el valor reutilizado es, con evidencia
medida del 100 %, exactamente el mismo objeto que `iterate()` habría computado,
y nada en el diseño exige re-leerlo.

`INFERENCE` **Reutilizar la observación no contradice la política `no memory,
no session, no cursor`.** Esa regla prohíbe **persistir estado entre
iteraciones o entre reinicios** (es lo que hace que la recuperación funcione).
Pasar un `ChangeObservation` fresco —calculado en el mismo frame, en la misma
iteración, sin mutación intermedia— como **parámetro** no es memoria: la
derivación y el registro siguen leyendo del mundo real en cada iteración, y
`iterate()` no guarda nada. El invariante que la regla protege ("cada iteración
decide sobre el estado real y actual") se preserva.

`INFERENCE` Lo que **sí** cambiaría es una propiedad de forma: `iterate()`
dejaría de ser *autocontenido* (hoy observa por sí mismo) para exigir una
observación de su caller. `FACT` **Ningún test llama a `iterate()`** y no hay
subclases, así que esa propiedad no está protegida por ninguna regla ni test
explícito — pero es una decisión de contrato que debe tomarse a conciencia, no
por descuido.

`UNKNOWN` **El ahorro en wall clock no está medido**, porque el cambio no se
ejecutó (prohibido en esta fase). La auditoría previa estimó 40–70 s de suite;
esa cifra sigue siendo `ESTIMATE` y esta auditoría **no la eleva a hecho**.

---

## 2. Question Under Investigation

`FACT` Pregunta exacta:

> **¿Puede `run()` observar una vez y pasar ese estado a `iterate()` sin
> cambiar ninguna garantía funcional, de seguridad, aislamiento, determinismo,
> recuperación o control del ciclo de ejecución?**

Y su forma operacional, del flujo real:

```text
HOY
  run()    : observation_A = observe()          # host.py:1050
             ... fingerprint, derive (no se usan para actuar)
             iterate(iteration)
  iterate(): observation_B = observe()          # host.py:591
             derive(observation_B) -> action -> actúa

CANDIDATO
  run()    : observation_A = observe()
             ... fingerprint, derive
             iterate(iteration, observation_A)
  iterate(): derive(observation_A) -> action -> actúa
```

`FACT` La condición de validez que el pedido fija es estricta: **sólo es válido
si `S == S'` bajo el contrato real de ejecución.** Este informe establece qué
significa `S` (§7, §9), si `S == S'` puede fallar (§8, §10) y con qué evidencia
se sostiene (§13, §14, §15).

`FACT` Pregunta secundaria, que el pedido exige responder primero:

> **¿Por qué `run()` observa y `iterate()` vuelve a observar?**

Respuesta corta (§16): **porque nadie se lo preguntó.** La duplicación nació en
el commit original (§14), no hay documentación que la justifique, ningún test la
protege, y ninguna de las tres razones funcionales que la justificarían se
sostiene frente al código. Pero **la clasificación correcta no es "accidental"
a secas**: `iterate()` necesita una observación fresca, y hoy la obtiene por sí
mismo. La discusión está en §17.

---

## 3. Scope and Constraints

`FACT` **Dentro del alcance:**

- `ExecutionHost.run()`, `iterate()`, `observe()` y **todos** sus auxiliares
  invocados en el camino (`_record`, `_build_delegation`, `_apply_autonomy_gate`,
  `_execute_delegation`, `_scope_violations`, `_apply_record`,
  `_record_run_note`, `derived_conditions`, `_committed`, `reconstruct`,
  `render_run`, `_autonomy_block`);
- `runtime/orchestrator/observation.py::observe()` y `ChangeObservation`;
- `runtime/orchestrator/{derivation,authority,store,contracts,autonomy}.py` en
  lo que toca al contrato del loop;
- los tests que ejercitan el host;
- la documentación de diseño: `.agents/policies/autonomous-orchestration.md`,
  `.agents/policies/supervised-autonomous-execution.md`, `runtime/README.md`,
  `runtime/orchestrator/__init__.py`, `docs/behavior-patterns.md`, planes
  122/123/135/138/145/159;
- el historial Git de `host.py`.

**Fuera del alcance:** el resto de la suite, el leg del harness, y cualquier
propuesta de reorganizar los 152 tests (prohibido por el pedido y ya tratado en
la auditoría de ejecución).

### 3.1 Restricciones respetadas (`FACT`)

```text
0 modificaciones a producción, tests, CI, dependencias
0 modificaciones a protocol/, dist/, ROADMAP.md
0 mecanismos de selección de tests
0 reorganización de los 152 tests
0 optimización de fixtures
0 eliminación de subprocesos "para reducir tiempo"
0 eliminación de ninguna llamada a observe() (se demostró su contrato antes)
instrumentación: fuera del árbol versionado, eliminada al finalizar (§22)
```

### 3.2 Plan 145 como restricción (`FACT`)

`FACT` Plan 145 eliminó el scratch **compartido** y estableció propiedad por
sesión con token declarado. **Esta auditoría no propone compartir estado entre
tests ni entre ejecuciones.** El objeto de estudio es estrictamente más acotado:

```text
in-memory reuse of ONE observation WITHIN ONE iteration of ONE run
   ≠
shared mutable repository state ACROSS tests or sessions
```

`FACT` La primera no toca ninguna regla de Plan 145 (no hay scratch, no hay
repositorio, no hay sesión: es una variable local pasada por parámetro). La
segunda está prohibida y **no se considera**. Ver §10.2 para la verificación de
que la reutilización propuesta no introduce estado compartido de ningún tipo.

---

## 4. Current Execution Flow

`FACT` Flujo reconstruido leyendo el archivo completo, no sólo las líneas de las
llamadas.

```text
ExecutionHost.run(max_iterations)                       host.py:1040
│  limit = max_iterations or self.max_iterations
│  start = len(self.store.read_journal(self.plan))       ← 1 lectura del journal
│  records = []
│  previous_fingerprint = None ; previous_kind = None
│
├─ for offset in range(limit):                          host.py:1048
│    iteration = start + offset + 1
│  ┌─ observation_A = self.observe()                    host.py:1050  ◄── (1)
│  │     = observe(self.root, self.plan, self.store)    host.py:455
│  │
│  ├─ fingerprint = observation_A.governance_fingerprint()      host.py:1051  [puro]
│  ├─ boundary    = AuthorityBoundary(plan_authorized=...)      host.py:1052  [puro]
│  ├─ action_A    = derive_next_action(observation_A, ...)      host.py:1055  [puro]
│  │
│  ├─ if not action_A.terminal:                                host.py:1062
│  │    if previous_kind == action_A.kind
│  │       and previous_fingerprint == fingerprint:            host.py:1063-1066
│  │       → record = self._record(observation_A, no_progress_action(...))
│  │         self.store.append_iteration(plan, record)   host.py:1077  ── ESCRITURA
│  │         records.append(record) ; break
│  │    previous_kind = action_A.kind
│  │    previous_fingerprint = fingerprint
│  │
│  ├─ record = self.iterate(iteration)                  host.py:1083
│  │  │
│  │  │  iterate(iteration)                             host.py:589
│  │  ├─ observation_B = self.observe()                 host.py:591  ◄── (2) DUPLICADO
│  │  ├─ boundary_B   = AuthorityBoundary(...)          host.py:592
│  │  ├─ action_B     = derive_next_action(observation_B, ...)  host.py:593
│  │  ├─ action_B, autonomy = _apply_autonomy_gate(observation_B, action_B, boundary_B)
│  │  │     (opt-in; cuando está activo lee git/journal/write-tree)
│  │  ├─ self._last_autonomy = autonomy                 host.py:602   [MUTACIÓN del host]
│  │  ├─ if action_B.terminal → _record(observation_B, ...)     host.py:604-605
│  │  ├─ if authority != AUTHORIZED_EXISTING → _record(stop)    host.py:607-616
│  │  ├─ if action_B.kind in EXECUTABLE_ACTIONS
│  │  │     → _execute_delegation(observation_B, action_B, iteration)
│  │  └─ else → _apply_record(observation_B, action_B, iteration)
│  │
│  ├─ self.store.append_iteration(plan, record)         host.py:1084  ── ESCRITURA
│  ├─ records.append(record)
│  └─ if record.terminal → break                        host.py:1086-1087
│
├─ else:  (el for terminó sin break)                    host.py:1088
│    observation_C = self.observe()                     host.py:1089  ◄── (3)
│    record = self._record(observation_C, max_iterations_action(...))
│    self.store.append_iteration(plan, record)          host.py:1095  ── ESCRITURA
│    records.append(record)
│
├─ conditions = self.derived_conditions()               host.py:1099
│    └─ observation_D = self.observe()                  host.py:1154  ◄── (4) DUPLICADO
│    └─ committed = self._committed(observation_D)      host.py:1157 → 1198/1206 git
│
├─ run = HostRun(..., iterations=len(records), ...)     host.py:1100-1108
├─ self.store.write_run_report(plan, run_id, render_run(run))   host.py:1109-1111
│    └─ render_run → _autonomy_block → observation_E = self.observe()  host.py:1287  ◄── (5)
├─ self._record_run_note(run)                            host.py:1112
│    └─ observation_F = self.observe()                   host.py:1117  ◄── (6)
│    └─ record_run_note(...)                             ── ESCRITURA en el plan
└─ return run
```

`FACT` **Observaciones por iteración en el camino de ejecución:**

```text
(1) host.py:1050   run()        — pre-acción
(2) host.py:591    iterate()    — pre-acción, INMEDIATAMENTE después de (1)
(3) host.py:872    _execute_delegation — post-acción (dentro del mismo iterate)
---
(4) host.py:870    _execute_delegation — pre-(3), INMEDIATAMENTE antes, sin
                                        mutación entre ambas (sólo `notes.append`)
(5) host.py:1154   derived_conditions() — 1 vez por corrida (previa a 1287/1117)
(6) host.py:1117   _record_run_note()   — 1 vez por corrida (rellena 1154)
```

`FACT` En el camino **no ejecutable** (`_apply_record`: graba anchor, status,
revalidación o checkpoint) hay **una** observación post-acción adicional
(`host.py:974`) porque la grabación **sí** modifica el plan, y por eso esa
observación **no** es reutilizable.

`FACT` **Los cuatro pares consecutivos con estado no modificado entre medias**
son `(1050→591)`, `(870→872)`, `(1154→1287)` y `(1287→1117)`. Los tres últimos
no estaban identificados por la auditoría previa, que localizó sólo el primero.

---

## 5. ExecutionHost.run()

`FACT` **Firma:** `def run(self, max_iterations: int | None = None) -> HostRun`.

`FACT` **Garantía que ofrece** (`OBSERVED` en el código y en `HostRun.to_dict`):
devuelve un `HostRun` con `run_id`, `plan`, `iterations` (`= len(records)`),
`terminal_action`, `rationale`, `derived_conditions` y `records`; y persiste
(i) un registro de journal por iteración, (ii) un run report
(`self.store.write_run_report`), y (iii) una nota de ejecución idempotente en el
plan (`_record_run_note`).

`FACT` **Argumentos y estado mutable:**

| Elemento | Naturaleza |
|---|---|
| `self.root`, `self.plan`, `self.store`, `self.worker`, `self.run_id`, `self.gate_commands`, `self.autonomy_gate` | sólo lectura en `run()` |
| `self._last_autonomy`, `self._last_autonomy_drift` | **mutados por `iterate`** (`host.py:602` y dentro de `_apply_autonomy_gate`), no por `run` |
| `records`, `previous_fingerprint`, `previous_kind`, `iteration`, `observation`, `fingerprint`, `boundary`, `action` | locales de `run()` |
| `self.store` (journal, delegaciones, worker results, run reports) | **mutado** — append-only |
| plan artifact | **mutado** — vía `_record_run_note` y `_apply_record` |

`FACT` **Puntos de escritura dentro de `run()`:** `host.py:1077` (guard de
no-progreso), `1084` (fin de cada iteración), `1095` (rama de agotamiento),
`1109` (run report), `1112` (nota en el plan). **Ninguno ocurre entre `1050` y
`591`.**

`FACT` **Máquina de estados real, derivada del código** (no asumida):

```text
ENTRY
  └─ lee journal (start)
LOOP (hasta `limit`)
  ├─ OBSERVE (1050)
  ├─ FINGERPRINT = f(observation)            [puro]
  ├─ DERIVE (1055)                           [puro; NO se usa para actuar]
  ├─ if not terminal and fingerprint sin cambio y mismo kind:
  │      STOP_NO_PROGRESS → APPEND JOURNAL → break
  ├─ ITERATE(1083)
  │      ├─ OBSERVE (591)
  │      ├─ DERIVE (593)
  │      ├─ AUTONOMY GATE (601, opt-in; sólo cambia la acción, no el estado)
  │      ├─ terminal?            → RECORD → return
  │      ├─ no autorizado?       → RECORD(stop) → return
  │      ├─ ejecutable?          → EXECUTE_DELEGATION → RECORD → return
  │      └─ si no               → APPLY_RECORD (escribe el plan) → RECORD → return
  ├─ APPEND JOURNAL (1084)
  └─ terminal? → break
EXHAUSTED (sin break)
  ├─ OBSERVE (1089) → RECORD(STOP_MAX_ITERATIONS) → APPEND JOURNAL
FINALIZE
  ├─ OBSERVE (1154) → DERIVED CONDITIONS (git diff / ls-files)
  ├─ BUILD HostRun
  ├─ WRITE RUN REPORT (→ OBSERVE en 1287 si el gate está activo)
  └─ RECORD RUN NOTE (→ OBSERVE en 1117; escribe el plan)
DONE → return HostRun
```

`FACT` **`max_iterations` = techo operativo del loop, no objetivo.** La rama
`else` de `host.py:1088` añade **un registro extra** cuando el `for` se agota sin
`break`, de modo que `run.iterations ∈ [1, limit+1]`. La auditoría de ejecución
lo midió (`max_iterations=1` → 2 iteraciones, 49 subprocesos).

`FACT` **La acción derivada en `1055` se calcula y se descarta** para todo salvo
el guard de no-progreso; la acción que se ejecuta es `action_B` (`host.py:593`),
derivada de `observation_B`. Es decir: el trabajo de decisión se hace **dos
veces por iteración** con dos observaciones distintas en el código, aunque
idénticas según la medición (§9.5).

`FACT` **Nada entre `1050` y `591` puede cambiar el estado observado**:

| Líneas | Operación | Naturaleza |
|---|---|---|
| 1051 | `governance_fingerprint()` | `FACT` puro: sólo formatea campos de la observación (`observation.py:872-893`) |
| 1052 | `AuthorityBoundary(...)` | `FACT` constructor puro |
| 1055 | `derive_next_action(...)` | `FACT` puro por contrato y por código: `derivation.py` no importa `store`, no escribe, no abre archivos, no lanza subprocesos (grep: 0 coincidencias) |
| 1062-1081 | comparación y asignación de locales | `FACT` puro |

`INFERENCE` Por lo tanto, en el **modelo de ejecución real** (un solo hilo, sin
callbacks, sin hooks entre esas líneas), `observation_A` y `observation_B` **no
pueden** diferir salvo por cambio externo concurrente — y no hay concurrencia
(§10.1) ni modelo de ejecución concurrente soportado. La medición lo confirma en
86 de 86 casos.

---

## 6. ExecutionHost.iterate()

`FACT` **Firma:** `def iterate(self, iteration: int) -> dict[str, Any]`.
Docstring: *"Run exactly one iteration and return its journal record."*

`FACT` **`iterate()` obtiene su estado por sí mismo**: `self.observe()` en
`host.py:591`, y esa observación es la **única** fuente de:
`boundary`, `action`, la decisión de la frontera SAE (`_apply_autonomy_gate`), la
construcción de la delegación (`_build_delegation`: `command_set`, `task`,
`input_artifacts`, `declared_scope`), la verificación de efectos
(`observation.declared_effects`), y el registro (`_record`: todo el bloque
`"observed"`).

`FACT` **Precondiciones reales de `iterate()`:**

| Precondición | ¿La verifica? | Evidencia |
|---|---|---|
| `self.root`, `self.plan` válidos | no | los usa directamente |
| `self.store` operativo | no | `observe` lee con él |
| que el plan exista | no | lo reporta la observación (`plan_present`), no un raise |
| **que el estado sea el actual** | **sí, observando** | `host.py:591` |
| `iteration` coherente con el journal | no | el caller lo calcula (`start + offset + 1`) |

`FACT` **Lo que ocurre entre el `observe()` de `run()` y el de `iterate()`:
nada que mute estado.** Ver la tabla de §5. La única operación que no es un
cálculo puro es la lectura de locales.

`FACT` **El resultado de `observe()` afecta directamente la acción**: la
derivación es una función de la observación (`derivation.py:195`, docstring:
*"Derive the next valid action from the observation, deterministically"*), y
`_BUILD_DELEGATION` toma de ella `command_set`, `task`, `input_artifacts` y
`declared_scope`.

`FACT` **`observe()` se usa para decidir si ejecutar, continuar, abortar o
corregir**: `action_B.terminal` → parar; `authority.verdict != AUTHORIZED_EXISTING`
→ stop; `kind in EXECUTABLE_ACTIONS` → delegar; en otro caso → grabar y seguir.

`FACT` **`observe → decision → action` versus `observe → observe → decision →
action`:**

```text
PATRÓN 1 (lo que el diseño documenta)
  observe() → decision → action

PATRÓN 2 (lo que el código hace)
  observe()            [run, host.py:1050]  → fingerprint/no-progress
  observe()            [iterate, host.py:591] → decision → action
```

`INFERENCE` **El segundo patrón no tiene semántica propia en este código.** La
primera observación no alimenta ninguna decisión que la segunda no alimente
mejor: la única diferencia es que la primera participa del guard de no-progreso
**antes** de entrar, y la segunda decide. El guard podría usar la misma
observación sin perder nada, porque el guard compara el fingerprint con el de la
**iteración anterior** (que sí reflejaba un estado pre-acción), no con el de un
estado intermedio. Ver §15 (invariante I-3) para la demostración.

---

## 7. ExecutionHost.observe()

`FACT` **Firma:** `def observe(self) -> ChangeObservation:
return observe(self.root, self.plan, self.store)`. Es un **delegado puro** a
`observation.py::observe` con la store del host.

### 7.1 Las 14 preguntas del pedido, respondidas

| # | Pregunta | Respuesta | Marca |
|---|---|---|---|
| 1 | ¿Qué estado obtiene? | un `ChangeObservation` inmutable (dataclass) con ~40 campos: status, entry criteria, command set, environmental classes, declared artifacts, agent task (incl. resource ceiling), declared effects, anchor (present/delta/state identity/stale/scope set), checkpoint (present/closure tree/consistency), findings, pending, git state, worker results, journal length y gaps, gates (4 flags), validation/revalidation/implementation flags, signals, scope set, content scope set, current delta/state identity, gaps | `FACT` |
| 2 | ¿De dónde lo obtiene? | (a) el **texto del plan** `docs/plans/<n>-*.md`; (b) `docs/plans/INDEX.md`; (c) el **estado git** del root; (d) el **journal** y los **worker results** persistidos en `.project/orchestrator/plan-NNN/`; (e) la identidad de contenido de `content_scope_set` (vía `tools/scoped_content_identity.py`) | `FACT` |
| 3 | ¿Qué comandos ejecuta? | `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`, `git status --porcelain` (`observation.py:129-131`); `git ls-files -z --cached --others --exclude-standard` (`worker.repository_snapshot`); y los de la identidad de contenido (`ls-files -s`, `hash-object`, `write-tree`). **Medido: 6 subprocesos por llamada** | `FACT` + `MEASURED` |
| 4 | ¿Qué archivos/directorios inspecciona? | el plan, `docs/plans/INDEX.md`, y los archivos de `content_scope_set` (para hashear); nunca escribe | `FACT` |
| 5 | ¿Qué información produce? | el `ChangeObservation` completo (§7.1.1) | `FACT` |
| 6 | ¿Qué información descarta? | el contenido íntegro de los archivos (sólo guarda hashes); el **texto crudo** del plan (parsea a campos); el journal **malformado** (lo reporta como `journal_gaps`, no lo interpreta); las líneas de journal de otros planes | `FACT` |
| 7 | ¿Dónde almacena el resultado? | **en ningún sitio**: lo retorna y no lo cachea. `ExecutionHost` no tiene campo de observación | `FACT` |
| 8 | ¿Modifica atributos de `ExecutionHost`? | **no**. `self.root`, `self.plan`, `self.store` son de sólo lectura en `observe`. Los únicos campos mutables del host (`_last_autonomy`, `_last_autonomy_drift`) los asigna `iterate`, no `observe` | `FACT` |
| 9 | ¿Modifica filesystem? | **no**. `_write_text` (el único escritor del store) no se alcanza desde `observe`; no hay `mkdir`, `write_text`, `open(..., "w")`, `unlink` en el camino | `FACT` |
| 10 | ¿Ejecuta Git? | **sí, en modo lectura** (6 subprocesos medidos). Nunca `add`, `commit`, `checkout` | `FACT` |
| 11 | ¿Ejecuta Python u otros procesos? | **no** directamente. `scoped_content_identity.compute` se invoca **en proceso** (`observation.py:144-164` importa el módulo y llama `module.compute`), no como subproceso | `FACT` |
| 12 | ¿Puede producir resultados distintos aunque nada haya cambiado? | **no**, bajo el contrato observado: `observation.py` no usa reloj, `random` ni `datetime` (grep: 0 coincidencias); `utc_now()` no aparece en `observe`; los datos derivan sólo del contenido del plan, del índice, del estado git y del store. El resultado es una **función determinista** de esos insumos | `FACT` + `INFERENCE` |
| 13 | ¿Qué errores puede detectar? | repo ilegible con CLI disponible ⇒ **`ObservationError`** (`observation.py:956-963`, plan 145/I-1); CLI ausente ⇒ `GAP` declarado; plan ausente ⇒ `gaps`; líneas de journal ilegibles ⇒ `journal_gaps`; entregables ausentes ⇒ `gaps`; techo malformado ⇒ `ceiling_gap`; entrada de efectos ilegible ⇒ `gaps` | `FACT` |
| 14 | ¿Qué invariantes establece? | ninguno por mutación. Establece **hechos**: "no se infiere lo que no se leyó" (todo lo ausente es un `GAP` declarado, nunca un valor fabricado) | `FACT` |

#### 7.1.1 Campos del `ChangeObservation` (`FACT`)

```text
identidad          root, plan, plan_path, plan_present
gobernanza         status, change_level, rfc, index_registered
entrada            entry_criteria{checked,total}
verificación       command_set, environmental_classes, verification_section_present,
                   declared_artifacts
delegación         agent_task{declared, section_present, task, scope,
                              scope_declared, resource_ceiling, ceiling_declared,
                              ceiling_gap}
efectos            declared_effects, declared_effects_unresolved
lifecycle          anchor{present, delta_identity, state_identity, scope_set,
                          revalidated}, anchor_stale
                   checkpoint{present, closure_tree, consistency_pass}
findings/pending   findings, open_findings, blocking_pending
git                git{is_repository, git_available, head, branch, dirty_paths}
evidencia          worker_results, journal_length, journal_gaps
gates              gates_run_after_anchor, gates_run_after_checkpoint,
                   gates_run_for_current_state, gates_run_for_current_closure,
                   last_gate_signals
señales            validation_signals, gate_signals
progreso           validation_done_for_current_state,
                   revalidation_done_for_current_state,
                   implementation_done_for_current_state,
                   implementation_already_satisfied
identidad contenido scope_set, content_scope_set,
                   current_delta_identity, current_state_identity
gaps               gaps
```

`INFERENCE` El objeto es **inmutable en la práctica** (dataclass de campos
escalares y tuplas) y **completo**: no hay un "snapshot parcial" que justifique
releer para completarlo. Ese era uno de los motivos a investigar (§5 del pedido,
*"el resultado de `observe()` no representa un snapshot completo"*) y **queda
refutado**.

### 7.2 Clasificación de efectos del pedido (`FACT`)

| Efecto | Clasificación | Evidencia |
|---|---|---|
| lectura del plan | `PURE_READ` | `plan_path.read_text` |
| lectura del INDEX | `PURE_READ` | `read_text` |
| `git rev-parse/status/ls-files/hash-object/write-tree` | `EXTERNAL_OBSERVATION` | subprocesos de lectura |
| hashing de contenido | `PURE_READ` | `hashlib.sha256(read_bytes())` |
| lectura de journal y worker results | `PURE_READ` | `read_journal_with_gaps`, `list_worker_results` |
| detección de repo ilegible | `ERROR_DETECTION` | `raise ObservationError` |
| detección de gaps | `ERROR_DETECTION` | lista `gaps` |
| cache | **ninguno** | no hay campo de cache en el host ni en la observación |
| validación de invariantes del host | **ninguna** | no valida el estado del host |
| mutación de `ExecutionHost` | **ninguna** | `FACT` |
| mutación de filesystem | **ninguna** | `FACT` |
| `MUTATION` / `CACHE_UPDATE` / `SIDE_EFFECT` | **ninguno en ninguna categoría** | `FACT` |

`FACT` **Ninguna entrada de la tabla queda `UNKNOWN`**: todas se rastrearon
hasta la implementación.

---

## 8. State Model

`FACT` El estado que `observe()` lee se compone de **cuatro fuentes**, y sólo
una de ellas es mutable por el propio host dentro de una corrida:

```text
FUENTE 1  el artifact del plan (texto)        ── MUTABLE por el host
             escritores: _apply_record (anchor/status/revalidación/checkpoint),
                         _record_run_note
FUENTE 2  docs/plans/INDEX.md                 ── NO mutado por el host
FUENTE 3  estado git del root                 ── MUTABLE por el worker
             escritores: el comando delegado (p.ej. `python src/check_ok.py`),
                         y cualquier escritura de archivo del worker
FUENTE 4  .project/orchestrator/ (journal,    ── MUTABLE por el host
          delegaciones, worker results)          escritores: append_iteration,
                                                 write_delegation,
                                                 write_run_result,
                                                 write_run_report
```

`FACT` **La clave del modelo: dentro de una iteración, `run()` e `iterate()` se
ejecutan antes de cualquier escritura.** Las escrituras de la iteración ocurren
**después** de que `iterate()` decide y actúa. Por eso el par `(1050, 591)` cae
íntegramente en una **zona sin mutación**.

`FACT` Y cuando **sí** hay mutación entre dos observaciones consecutivas, la
diferencia es real y el digest lo detecta (medido): los pares
`591→870`, `872→1050`, `591→974`, `974→1050`, `872→1089` son **todos distintos**,
y corresponden exactamente a `post-acción → pre-acción`.

`INFERENCE` Es decir: **el digest distingue correctamente "mismo estado" de
"estado nuevo"**. La medición no es un artefacto de que el digest sea insensible:
si lo fuera, los pares post-acción también saldrían iguales, y no salen (45/45,
25/25, 16/16, 12/12, 20/20 distintos).

### 8.1 Los cuatro casos del pedido, resueltos (`FACT` + `MEASURED`)

```text
CASO 1 — mismo estado
    observe(S) → iterate() → observe(S) → action
    APLICA. Es el par (1050→591): 86/86 medidos idénticos.
    Es también (870→872): 45/45; (1154→1287): 29/29; (1287→1117): 29/29.

CASO 2 — estado modificado
    observe(S1) → mutation → observe(S2) → action
    APLICA pero NO es el par en cuestión. Es (591→974), (591→870),
    (872→1050), (872→1089): el host escribió el plan, el journal, una
    delegación o un worker result (o el worker escribió el repositorio).
    Medido: distintos en el 100 % de los casos.

CASO 3 — estado externamente mutable
    observe(S1) → external system may change → observe(S2) → action
    NO APLICA como modelo soportado: no hay hilos, no hay callbacks entre las
    dos llamadas, y el host no declara un modelo de ejecución concurrente.
    Si otro proceso mutara el repositorio entre 1050 y 591, la ventana es de
    ~microsegundos de código puro (la observación de 1050 ya ocurrió; entre
    ambas sólo hay dos llamadas puras). Riesgo residual: ver §19 (R-2).

CASO 4 — observación con side effects
    observe() → mutation → observe()
    REFUTADO. observe() no muta nada (§10).
```

`INFERENCE` **No corresponde un quinto modelo.** El flujo encaja exactamente en
el Caso 1 para el par de interés y en el Caso 2 para todos los demás pares.

---

## 9. Observation Semantics

### 9.1 Qué significa observar (`FACT`)

`FACT` `observation.py:943` lo declara: *"Observe the change and the repository
state. **Read-only, no inference.**"* La semántica es **leer y reportar hechos**,
con la regla fuerte de que lo ausente se declara ausente:

- ausencia del plan ⇒ `plan_present=False` + `gaps`;
- ausencia de CLI git ⇒ `git_available=False` + `GAP` declarado;
- **repo ilegible con CLI presente y root existente ⇒ `ObservationError`** — no
  se degrada a "no es un repositorio" (plan 145, I-1; el incidente real: un
  repositorio desechable que desapareció y se leyó como estado ordinario);
- línea de journal ilegible ⇒ `journal_gaps`, nunca interpretación;
- entregable declarado ausente ⇒ `gaps`, nunca fabricación.

### 9.2 Determinismo (`FACT` + `INFERENCE`)

`FACT` `observation.py` no importa ni usa reloj, `random` ni `datetime`. No hay
`utc_now()` en el camino de observación (sí en `_build_delegation` y en
`run_id`, fuera de `observe`). Los únicos insumos son contenido de archivos,
estado git y contenido del store.

`INFERENCE` Por tanto `observe()` es una **función determinista de sus insumos**:
dos llamadas con los mismos insumos devuelven el mismo payload. La medición lo
confirma en **189 pares consecutivos sin mutación intermedia** (§9.5).

`FACT` **El digest de la sonda no es un hash del objeto en memoria**: serializa
`observation.to_dict()` con `sort_keys=True` y además incorpora la lectura
explícita de `git_state`. Compara **contenido**, no identidad.

### 9.3 Idempotencia y pureza (`FACT`)

| Propiedad | Veredicto | Evidencia |
|---|---|---|
| ¿pura? | **sí en efectos; no en coste** — no muta nada, pero lanza 6 subprocesos | §7.2, §10.3 |
| ¿idempotente? | **sí** — repetirla no cambia el mundo | §10 |
| ¿side-effect free? | **sí** | §10.3 |
| ¿barata? | **no** — `MEASURED` ~0.33 s, 6 subprocesos | §10.3 |
| ¿equivalente a leer un snapshot? | **sí, con la salvedad de que el snapshot hay que construirlo**: computa un estado fresco y completo en cada llamada; no hay snapshot almacenado del cual leer | §7.1.1, §8 |

### 9.4 Riesgo de excepción (`FACT`)

`FACT` `observe()` **puede lanzar** `ObservationError`. En el flujo actual, si
`observation_B` (591) falla, la excepción sale de `iterate()` y de `run()`
(no hay `try/except` alrededor: el único `try/except` de `run()` está en
`_record_run_note`, `host.py:1141-1149`, y sólo protege la nota).

`INFERENCE` **Reutilizar `observation_A` no elimina ese riesgo**: la observación
que se reutiliza ya se ejecutó y ya habría lanzado. De hecho lo **reduce**: hoy
el mismo fallo se detecta dos veces; reutilizando, una. No hay pérdida de
detección porque la ventana entre ambas no introduce riesgo nuevo (no hay
mutación).

### 9.5 La equivalencia, medida (`MEASURED`)

**Sonda 1 — equivalencia directa de payloads.** Tres escenarios, dos
observaciones consecutivas cada uno, comparando `to_dict()` completo +
`git_state`:

| Escenario | Idénticos | Diferencias | Subprocesos por llamada | Wall por llamada |
|---|---|---|---|---|
| fixture limpio (A vs B) | **sí** | `{}` | 6 | 0.337–0.367 s |
| fixture con historial de host (journal=3, worker_results=1) | **sí** | `{}` | 6 | 0.336–0.346 s |
| par exacto `run()→iterate()` (S3) | **sí** | `{}` | 6 | 0.334–0.334 s |

`MEASURED` El tiempo de subproceso representa **~97 %** del wall de `observe()`
(0.33 de 0.34 s). Es decir: el coste de observar es casi íntegramente
**creación de procesos**.

**Sonda 2 — atribución en corrida real.** Plugin externo que envuelve
`ExecutionHost.observe`, registra el **número de línea del caller** y un digest
del payload; corrida sobre los 4 archivos dominantes (152 tests, **444 llamadas
a `observe()`**):

| Par consecutivo | Pares | Idénticos | Distintos |
|---|---:|---:|---:|
| **1050 → 591** (run → iterate) | **86** | **86 (100 %)** | **0** |
| 870 → 872 (dentro de `_execute_delegation`) | 45 | 45 (100 %) | 0 |
| 1154 → 1287 (`derived_conditions` → `render_run`) | 29 | 29 (100 %) | 0 |
| 1287 → 1117 (`render_run` → `_record_run_note`) | 29 | 29 (100 %) | 0 |
| **total consecutivos idénticos** | **189** | **189 (100 %)** | **0** |
| 591 → 870, 872 → 1050, 1089 → 1154, 872 → 1089, 591 → 1154, 591 → 974, 974 → 1050, 769 → 1154, 591 → 769, 974 → 1089 y otros menores | 187 | 0 | **187 (100 %)** |

`MEASURED` **La distinción es nítida y no ambigua**: los 189 pares sin mutación
intermedia son idénticos; **todos** los 187 pares con acción/escritura entre
medias son distintos. El digest es sensible (detecta los cambios reales) y
estable (no inventa diferencias).

`INFERENCE` Los ocho pares con un solo miembro (`591→807`, `591→822`,
`1117→1050`, `1117→None`) son fronteras de secuencia dentro de un test (el
`nodeid` de un caso parametrizado contiene espacios y el parser de la sonda los
omitió); no afectan a ninguno de los pares de interés.

`MEASURED` **Cuentas de conservación** (verifican que la atribución es
consistente y no hay llamadas perdidas):

```text
llamadas en 591  = 86   pares (1050→591)  = 86    ✓
llamadas en 872  = 45   pares (870→872)   = 45    ✓
llamadas en 1287 = 29   pares (1154→1287) = 29    ✓  y  pares (1287→1117) = 29  ✓
llamadas en 1154 = 74   = 24 de (1089→1154) + 29 de (1154→1287) + 21 de (1154→1117)
llamadas en 1117 = 50   = 21 de (1154→1117) + 29 de (1287→1117)
llamadas en 1089 = 28   (rama de agotamiento del límite / guard)
total en sitios instrumentados = 444
```

`UNKNOWN` Cuatro observaciones no quedaron emparejadas en la secuencia
(`1117` tiene 50 llamadas y 49 pares; hay 4 pares `974→1089` que sugieren 4
salidas por el guard de no-progreso). `INFERENCE`: son fronteras de secuencia
dentro del test, no llamadas perdidas; la conservación cierra en los cuatro
pares de interés, que son los que sostienen la conclusión.

---

## 10. Mutation / Side-Effect Analysis

### 10.1 Concurrencia y estado de proceso (`FACT`)

| Fuente de nondeterminismo | Presente | Evidencia |
|---|---|---|
| hilos | **no** | 0 `import threading` / `Thread(` en `runtime/` |
| multiprocessing | **no** | 0 coincidencias |
| `asyncio` | **no** | 0 coincidencias |
| signal handlers | **no** | 0 `import signal` |
| locks | **no** | 0 `Lock(` / `RLock(` |
| callbacks/hooks entre 1050 y 591 | **no** | el código entre esas líneas es 4 operaciones puras |
| proceso hijo que mute el repo entre ambas | **no** en el flujo | la última acción del worker ocurrió en la iteración anterior o posterior, nunca entre 1050 y 591 |

### 10.2 Estado compartido (`FACT`)

`FACT` La reutilización propuesta es una **variable local pasada por
parámetro** dentro de un mismo frame de una misma iteración. **No** introduce:

- estado persistido entre iteraciones (el objeto muere al terminar la iteración);
- estado entre reinicios (nada se escribe);
- scratch compartido entre tests ni entre sesiones (Plan 145 intacto);
- cache (no hay campo de cache, ni en el host ni en la observación);
- metadatos ni archivos generados (no se escribe nada).

`FACT` El host ya tiene dos campos mutables (`_last_autonomy`,
`_last_autonomy_drift`) que son **evidencia de la iteración en curso**, y el
propio comentario del código aclara que **no** son estado persistido:
*"never persisted as state (the next iteration re-derives everything from the
repository)"* (`host.py:444-446`). Pasar una observación como parámetro es
**más débil** que eso: no sobrevive a la llamada.

### 10.3 Coste (`MEASURED`)

```text
observe() x1  =  0.380 s   /  6 subprocesos          (sonda 1, n=3)
                  de los cuales ~0.366 s son subproceso (96.4 %)
0.033 s de lógica Python: parseo del plan, hashing SHA-256 del scope set,
                          recorrido del journal, armado del dataclass

run(max_iterations=1)  =  2.99 s / 49 subprocesos / 2 iteraciones
                          (auditoría previa; consistente con 2×~6 +
                           snapshots + 1 comando de verificación)
```

`MEASURED` **Redundancia en los 4 archivos dominantes** (444 llamadas):

```text
llamadas que son el PRIMER miembro de un par consecutivo idéntico:
   1050 (86) + 870 (45) + 1154 (29) + 1287 (29)  =  189 de 444  =  42.6 %

tiempo de subproceso de esos cuatro sitios: 74.6 s
tiempo de subproceso de la observación total: 157.0 s   =  47.5 %
wall de esos cuatro sitios: 76.9 s
   (1050: 32.0 · 870: 16.3 · 1154: 18.4 · 1287: 10.2)
```

`INFERENCE` **Esto es redundancia de *observación*, no de *llamadas*.** En cada
par idéntico las dos llamadas son necesarias **para su propio consumidor**; lo
que es evitable es **la segunda lectura del mundo**, no la función. Por eso el
techo del ahorro se mide en **lecturas evitables** (= 189 en esta corrida), no
en llamadas eliminadas.

`ESTIMATE` **Ese 42.6 % es el techo de la reutilización de observaciones** en los
4 archivos dominantes, y **no** corresponde a un cambio concreto: los cuatro
sitios son cuatro cambios distintos (dos exigen mover un valor a través de una
frontera de método, uno atraviesa `write_run_report`), y esta auditoría **sólo
recomienda experimentar con uno** (§21). `ESTIMATE` El efecto de eliminar **sólo**
el par `(1050→591)` es del orden de **86 lecturas** de las 189, es decir ~19.4 %
de las llamadas medidas y ~31 s de subproceso de esos archivos. **No se convierte
en segundos de suite**: el cambio no se ejecutó, y la estimación de 40–70 s de la
auditoría previa **permanece `ESTIMATE`**.

### 10.4 Efectos sobre archivos y Git (`FACT`)

`FACT` Ninguna observación modifica archivos ni el índice git. La única
interacción con git es de lectura (`rev-parse`, `status`, `ls-files`,
`hash-object`, `write-tree`). `git write-tree` **lee** el índice staged y
devuelve un tree id; no crea objetos nuevos de contenido del usuario (aunque
git puede escribir en su propio `.git/`, que `observe` **excluye** de la
identidad de contenido y que `repository_snapshot` no incluye por
`--exclude-standard`).

`INFERENCE` Ese detalle importa: la observación **no es totalmente inocua sobre
`.git/`** (git mantiene su propio estado interno), pero **sí lo es sobre todo lo
que la observación misma lee** — que es lo que hace que dos observaciones
consecutivas coincidan.

---

## 11. All observe() Call Sites

`FACT` Inventario completo (13 sitios en producción; ninguno en tests ni en
otras capas).

| # | Sitio | Caller | Contexto | Motivo aparente | ¿Estado puede cambiar antes? | ¿Garantía protegida? | ¿Reutilizable? |
|---|---|---|---|---|---|---|---|
| 1 | `host.py:591` | `iterate` | inicio de la iteración | **la** observación de la que se deriva y se actúa | no (es la primera del frame) | sí: actuar sobre estado actual | **NECESARIA** (es el destino de la reutilización) |
| 2 | `host.py:769` | `_execute_delegation` | tras violación de scope | registrar el estado **después** de la acción | **sí**: la delegación se escribió y el worker corrió | evidencia post-acción real | no |
| 3 | `host.py:807` | `_execute_delegation` | tras fallo M4 | ídem | **sí** | ídem | no |
| 4 | `host.py:822` | `_execute_delegation` | tras worker result ausente | ídem | **sí** | ídem | no |
| 5 | `host.py:852` | `_execute_delegation` | tras efecto no declarado | ídem | **sí** | ídem | no |
| 6 | `host.py:870` | `_execute_delegation` | resumen del worker | alimentar la nota `"worker result: …"` | **sí** (post-acción) | ninguna propia; sólo la nota | **REDUNDANTE respecto de 872** |
| 7 | `host.py:872` | `_execute_delegation` | registro final | el bloque `observed` del registro | no (inmediatamente después de 870) | sí: el registro refleja el estado real | **sí** (destino) |
| 8 | `host.py:974` | `_apply_record` | tras grabar en el plan | el registro refleja el plan **ya modificado** | **sí**: `record_*` escribió el artefacto | sí: `observed` debe ser post-grabación | no |
| 9 | `host.py:1050` | `run` | inicio del loop | fingerprint de no-progreso | no | guard de no-progreso | **REDUNDANTE respecto de 591** |
| 10 | `host.py:1089` | `run` (rama `else`) | agotamiento del límite | registrar el estado al agotar | no desde la última escritura | sí: el registro final es real | sí (destino) |
| 11 | `host.py:1117` | `_record_run_note` | cierre de la corrida | `plan_present`, `plan_path` | no | sí: no escribir nota si no hay plan | **REDUNDANTE respecto de 1154** |
| 12 | `host.py:1154` | `derived_conditions` | cierre | derivar las condiciones | no | sí: `Closed` derivado del estado real | **sí** (destino) |
| 13 | `host.py:1287` | `_autonomy_block` | render del run report | `findings`/`open_findings` para el resumen SAE | no | sí: el resumen refleja el estado real | **sí** (destino) |

`FACT` **Llamadas fuera de `host.py`: cero.** Grep sobre todo el repositorio:

```text
runtime/orchestrator/host.py:1083   self.iterate(iteration)     ← único caller de iterate
tests/   : ninguna llamada a .iterate(
runtime/ : ninguna otra
```

`FACT` **Llamadas a `observe()` desde tests: 4, todas directas y legítimas**
(`second_host.observe()`, `host.observe()` ×2, `third.observe()`), ninguna
relacionada con `iterate`.

`FACT` **Llamadas desde el CLI:** `__main__.py:146` llama a `observe(...)` para
`--observe` (observar y derivar sin ejecutar) y `__main__.py:203` llama a
`host.run()`. **El CLI no llama a `iterate()`.**

`INFERENCE` **No existe un contrato transversal que impida reutilizar.** No hay
wrapper, subclase, callback ni mock que dependa de que `observe()` se llame dos
veces. La única "garantía" que la doble llamada protege hoy es **implícita**: que
`iterate()` funcione sin recibir nada — y ningún test ni documento la declara.

---

## 12. Inheritance / Overrides

`FACT` **No existe ninguna subclase de `ExecutionHost`.** Grep de
`class .*\(ExecutionHost\)` sobre todo el repositorio: **0 coincidencias**.

`FACT` **No hay overrides de `run()`, `iterate()` ni `observe()` en ninguna
capa.** Las únicas clases definidas en `tests/` son `DeliberationInvalid`
(exception), `IncompleteBoundary` (Protocol local), y adapters de cache
(`RecordingAdapter`, `EvictingAdapter`, `TtlExpiringAdapter`,
`FailingCacheAdapter`) — ninguna relacionada con el host.

`FACT` **No hay monkeypatch de `observe` en los tests.** Grep de
`monkeypatch.setattr(... "observe" ...)`: **0 coincidencias**. Los tests que
intervienen la derivación lo hacen sobre `derive_next_action`
(`test_autonomous_orchestrator.py:1009`, `1032`), no sobre la observación.

`FACT` **`iterate()` no forma parte de la superficie pública declarada.**
`runtime/orchestrator/__init__.py` exporta en `__all__`:
`AgentInvocationRequest`, `AgentInvocationResult`, `AgentInvoker`, `AgentTask`,
`AgentWorker`, `ChangeObservation`, `Delegation`, `DERIVED_ACTIONS`,
`DERIVED_CONDITIONS`, `ExecutionContext`, `ExecutionHost`, `HostRun`,
`NullAgentInvoker`, `OrchestratorStore`, `SIGNALS`, `WORKER_RESULT_FIELDS`,
`WorkerResult`, `agent_invoker_from_environment`, `observe`.
**`iterate` no está.** Sí lo está `observe` (la función de módulo).

`FACT` **No hay método abstracto ni Protocol que declare el contrato del loop.**
`WorkerAdapter` es un Protocol (`worker.py`), pero es el contrato del *worker*,
no del host. El host no implementa ninguna interfaz.

`INFERENCE` **La respuesta a la pregunta del pedido** (*"¿la optimización sería
segura para la implementación actual pero rompería una extensión soportada por
diseño?"*): **no hay extensión que romper.** La implementación concreta es la
única implementación. Lo que sí cambiaría es la **forma** de `iterate()`:
dejaría de ser invocable sin argumentos. `FACT` Eso no rompe ningún consumidor
existente (§11), pero convierte un método autocontenido en uno que exige un
argumento — una decisión de contrato que debe ser **deliberada**, no un efecto
colateral.

`INFERENCE` Si en el futuro se quisiera preservar la autonomía de `iterate()`,
la firma podría ser `iterate(iteration, observation=None)` con observación
propia como fallback. **Esta auditoría no lo recomienda** (un parámetro opcional
que cambia el número de lecturas del mundo real es exactamente el tipo de
ambigüedad que el repositorio evita por principio — `AGENTS.md`,
*Decision-Making Compass*), pero lo registra como alternativa en §18
(Alternativa C).

---

## 13. Relevant Tests

`FACT` **Ningún test llama a `iterate()` directa o indirectamente como unidad.**
`iterate()` se ejercita **sólo** a través de `run()`. Consecuencia directa:

> **Ningún test depende explícitamente de que `iterate()` observe por sí
> mismo**, porque ningún test puede observar esa propiedad sin llamarlo.

`FACT` Tests relevantes al contrato del loop:

| Test | Garantía que protege | Método ejercitado | ¿Depende de una 2ª observación? | Evidencia |
|---|---|---|---|---|
| `test_autonomous_orchestrator.py::test_full_loop_derives_closed_from_real_evidence` (920) | `CLOSED_DERIVED` desde anchor+checkpoint reales; `closure_tree == anchor.state_identity` | `run()` completo, 7 iteraciones | **no** — asertа sobre el resultado del loop y el plan; ninguna aserción distingue el número de observaciones | explícita para `Closed`; incidental para el conteo de observaciones |
| `::test_revalidation_is_recorded_as_a2_without_mutating_a1` (945) | A2 preserva A1 | `run()` ×2 en dos hosts | **no** | explícita para A1/A2 |
| `::test_restart_reconstructs_and_continues_without_lost_continuity` (970) | continuidad de numeración entre instancias; journal = iteraciones | `run()` ×2 + `reconstruct` | **no** | explícita; y refuerza el invariante "sin memoria entre iteraciones" |
| `::test_no_progress_guard_stops_instead_of_spinning` (1009) | el guard corta antes del límite con fingerprint sin cambio | `run()` con `derive_next_action` monkeypatcheado a constante | **sí, indirectamente**: el fingerprint que compara viene de `1050` y el de la iteración previa de `1050`. **Reutilizar 1050 no lo rompe** (el guard sigue comparando fingerprints pre-acción de iteraciones distintas) | explícita para el guard |
| `::test_max_iterations_is_an_explicit_stop` (1032) | `STOP_MAX_ITERATIONS`, `iterations == limit+1` | `run()` con derivación variable | **no** | explícita |
| `::test_observation_is_read_only` (1070) | `observe()` deja el repo byte-idéntico | `observe()` directo | no | **explícita para la pureza de `observe()`** |
| `::test_stale_validation_derives_revalidation_and_fresh_does_not` (381) | staleness ⇒ `RUN_REVALIDATION` | `run()` + `observe` | **no**, pero es **sensible**: depende de que la observación refleje el contenido **después** de `git add` | explícita |
| `::test_unreadable_repository_is_an_error_not_a_false_absent_state` (1109) | repo ilegible ⇒ `ObservationError` | `observe()` | no | explícita |
| `::test_an_absent_git_cli_stays_a_declared_gap_not_an_error` (1129) | CLI ausente ⇒ `GAP` | `observe()` | no | explícita |
| `::test_git_state_reports_the_cli_availability_explicitly` (1153) | `git_state` en el repo real | `git_state` | no | explícita (test **anclado** no declarado en `tests/AGENTS.md`) |
| `test_agent_worker.py::test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task` (613) | anti-loop: la tarea se deriva una vez | `run()` 2 iteraciones | **no**, pero **sensible**: la 2ª iteración debe ver el journal actualizado | explícita |
| `test_autonomy_effects.py::test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence` (671) | el techo se lee del journal real | 2 hosts | **no** — refuerza el invariante "sin memoria" | explícita |
| `test_sae_scope_enforcement.py::test_the_host_stops_when_the_contract_is_rewritten_after_authorization` (741) | el pin sobrevive una instancia nueva | `run()` ×2 | **no** | explícita |

### 13.1 ¿Qué comportamiento quedaría desprotegido? (`INFERENCE`)

```text
SI iterate() dejara de observar por sí mismo:
  · ninguna aserción existente falla por esa razón, porque ninguna la mide
  · lo que se pierde NO es una garantía probada: es una PROPIEDAD DE FORMA
    ("iterate es autocontenido / invocable sin contexto")
  · lo que se gana: la observación que se pasa es, con evidencia del 100 %,
    idéntica a la que iterate computaría
```

`INFERENCE` **El riesgo no es que un test se rompa: es que un test deje de
detectar algo.** Si `iterate()` recibe la observación de `run()`, y en el futuro
alguien introduce una mutación entre `1050` y `591`, **el cambio reutilizador
enmascararía ese bug**: la mutación ocurriría después de la observación
reutilizada, y el host actuaría sobre estado pre-mutación. Hoy ese bug sería
invisible igual (nadie mide la equivalencia), pero con la reutilización la
ventana "segura" se vuelve una **suposición cargada**.

`INFERENCE` Esa es la razón por la que la clasificación final es `MIXED` y la
decisión es `SAFE_TO_EXPERIMENT` y no `SAFE_TO_REFACTOR`: el cambio es
demostrablemente inocuo **hoy**, y hay que demostrar por experiencia que no
introduce una regresión de detección. Ver §21 (invariante a instrumentar).

---

## 14. Historical / Architectural Evidence

### 14.1 Historial Git (`FACT`)

```text
$ git log --oneline -- runtime/orchestrator/host.py
2de6bfe  feat(runtime): materialize the autonomy effect and resource frontiers (plan 159)
b0e37a5  feat(runtime): enforce SAE scope and authority before the effect (plan 138)
7c4fec3  feat(runtime): materialize supervised autonomous execution (plan 135)
4aa2617  refactor(dev): harden orchestrator runtime maintainability
4f85e67  feat(dev): consolidate autonomous orchestrator and agent worker mvps (plans 122, 123)
```

`FACT` **Conteo de `self.observe()` por versión del archivo:**

| Commit | Plan | Nº de `self.observe()` | ¿El par (1050, 591) existe? |
|---|---|---:|---|
| `4f85e67` | 122 + 123 (original) | **11** | **sí** — `run()` observa y `iterate()` observa |
| `4aa2617` | refactor maintainability | 11 | sí |
| `7c4fec3` | plan 135 (SAE) | 12 | sí |
| `b0e37a5` | plan 138 (enforcement) | 12 | sí |
| `2de6bfe` | plan 159 (efectos/recursos) | 13 | sí |
| `HEAD` | — | 13 | sí |

`INFERENCE` **Evidencia histórica concluyente sobre el origen:** la doble
observación **nació con el host**, en el commit que consolidó los MVPs de los
planes 122 y 123. **No fue introducida por** la frontera SAE (135), el
enforcement de scope (138), el envelope de efectos/recursos (159), ni el refactor
de mantenibilidad (4aa2617). Planes posteriores **añadieron** sitios de
observación (870/872 en 123; 974 en 135/138; 1154/1117/1287 preexistentes) pero
**nunca revisaron el par original**.

`FACT` Esto **descarta la hipótesis `LEGACY` en el sentido de "deuda acumulada
por capas posteriores"** y la reemplaza por una más precisa: es una decisión
**original** de diseño de la implementación de referencia, no una sedimentación.

### 14.2 Documentación de diseño (`FACT`)

`FACT` **El diseño documentado describe el PATRÓN 1, no el 2.** Ninguna fuente
describe una doble observación por iteración:

| Fuente | Texto | ¿Menciona 2 observaciones? |
|---|---|---|
| `runtime/orchestrator/host.py:405` | *"The loop. **It holds no state: every iteration observes from scratch.**"* | describe **una** observación por iteración |
| `.agents/policies/autonomous-orchestration.md:§1` | *"observe → derive → authorize → delegate → execute → ingest → verify → decide → continue/stop"*; *"**observe** — re-read the repository and the persisted evidence (no memory, no session, no cursor)"* | una etapa `observe` por iteración |
| `.agents/policies/autonomous-orchestration.md:§9` | *"**The host holds no state.** After a restart it reconstructs the situation from the repository … and the persisted evidence, continuing the iteration numbering and the derivation."* | no |
| `runtime/README.md:206-208` | *"The loop … is `observe → derive → authorize → delegate → execute → ingest → verify → decide → continue/stop`"* | una etapa |
| `runtime/orchestrator/__init__.py:6-9` | *"it observes the state that already exists, derives the next valid action, checks the authority boundary, delegates…"* | una |
| `runtime/README.md:330-331` | *"`ExecutionHost._apply_autonomy_gate`, invoked from `iterate` **before** `_execute_delegation`"* | confirma que `iterate` actúa, no cuántas veces observa |
| `docs/behavior-patterns.md:214` | *"Host autónomo DEV \| observa, deriva, autoriza, delega, verifica, registra, escala"* | una |
| `docs/working/audits/architecture-capability-review.md:183` | *"Continuidad del host (DEV) \| **el host no tiene estado: re-observa y re-deriva**; la numeración de iteraciones continúa desde el journal"* | **"re-observa"** — pero en el sentido de *volver a observar en la próxima iteración*, no de observar dos veces en la misma |

`FACT` **La única fuente que usa la palabra "re-observa"** es un working doc
(`architecture-capability-review.md:183`, no normativo) y su contexto es la
continuidad entre iteraciones: *"el host no tiene estado: re-observa y re-deriva;
la numeración de iteraciones continúa desde el journal"*. `INFERENCE` Es una
descripción del invariante entre iteraciones, **no** una justificación de la
doble observación intra-iteración.

`FACT` **Plan 122** (el plan que creó el host) describe el ciclo como
`observe → derive → authorize → delegate → execute → ingest → verify → decide`
(línea 35) — **una vez por iteración**.

`INFERENCE` **No existe documentación que explique por qué `run()` observa y
`iterate()` vuelve a observar.** Pero —como el pedido advierte explícitamente—
**la ausencia de documentación no demuestra que sea accidental**. Por eso la
conclusión se apoya en el comportamiento medido, no en el silencio documental.

### 14.3 Evidencia negativa: lo que se buscó y no se encontró (`FACT`)

```text
BÚSQUEDA                                          RESULTADO
comentario que explique la 2ª observación          0 coincidencias
docstring en iterate() que mencione observar       no (sólo "Run exactly one iteration")
ADR / RFC sobre el número de observaciones         0
CHANGELOG que mencione la doble observación        0
issue / finding documentado sobre esto             0
test que asiertе el número de observaciones        0
subclase / override / hook de observe              0
modelo de concurrencia declarado                   0
nota en tests/AGENTS.md sobre iterate()            0
```

### 14.4 Evidencia positiva de diseño: el invariante es *entre iteraciones* (`FACT`)

`FACT` Las fuentes son consistentes y repetidas en un punto: **la ausencia de
estado es una propiedad *entre* iteraciones y *entre* corridas.**

```text
"the next iteration re-derives everything from the repository"   host.py:444-446
"no memory, no session, no cursor"                               policy §1
"The host holds no state. After a restart it reconstructs…"      policy §9
"the host holds no state"                                        policy §9
"el host no tiene estado: re-observa y re-deriva"                arch-review:183
```

`INFERENCE` **Ninguna de esas afirmaciones exige que la función `iterate()`
ejecute su propia llamada a `observe()`.** Todas exigen que **la iteración** se
base en el estado real y actual. Una observación pasada por parámetro, calculada
en el mismo frame, satisface exactamente esa exigencia. La forma actual
(satisfacerla llamando a `observe()` dentro de `iterate`) es **una** manera de
implementar el invariante, no el invariante mismo.

`INFERENCE` **Esta es la distinción central del informe** y merece enunciarse sin
ambigüedad:

```text
INVARIANTE (lo que la política exige)
  cada iteración decide sobre el estado real y actual del mundo;
  no hay memoria entre iteraciones ni entre reinicios.

IMPLEMENTACIÓN ACTUAL (una forma de lograrlo)
  iterate() llama a observe() por sí mismo.

FORMA ALTERNATIVA (la que se investiga)
  run() llama a observe() una vez y pasa el resultado a iterate().
  → satisface el invariante si el valor pasado es fresco.
```

---

## 15. Invariants

`FACT` Invariantes obtenidos del código y de la documentación (no asumidos).

### I-1. Cada acción se ejecuta contra el estado observado (`FACT`)

```text
ENUNCIADO    la acción que se ejecuta se deriva de una observación del estado
             real, y los datos de la delegación (command_set, task, scope)
             provienen de esa misma observación.
EVIDENCIA    host.py:591-598 (derive de observation_B) y
             host.py:745-587 (_build_delegation usa observation_B).
DISEÑO       iterate() observa y deriva en el mismo frame; no hay hueco.
REUTILIZAR   la observación reutilizada es la de run():1050, computada en el
             mismo frame, sin mutación intermedia (§5, §9.5).
CAMBIO       ninguno. El invariante se conserva.
RIESGO       LOW.
```

### I-2. No se ejecuta sobre estado obsoleto (`FACT`)

```text
ENUNCIADO    la observación que decide la acción no puede ser anterior a la
             última escritura del sistema.
EVIDENCIA    todas las escrituras de la iteración ocurren DESPUÉS de que
             iterate() decide (host.py:1077, 1084, 1095, 1109, 1112), o dentro
             de _execute_delegation/`_apply_record`, es decir después de 591.
DISEÑO       el orden observa→decide→actúa lo garantiza por construcción.
REUTILIZAR   la observación reutilizada es posterior a la última escritura de la
             iteración anterior (el journal se escribió en 1084/1077/1095 de la
             iteración previa, y run() lee el journal al inicio con `start`).
CAMBIO       ninguno.
RIESGO       LOW.
```

### I-3. El guard de no-progreso compara estados pre-acción (`FACT` + `MEASURED`)

```text
ENUNCIADO    el guard corta cuando dos iteraciones consecutivas derivan la misma
             acción sobre el mismo fingerprint de gobernanza.
EVIDENCIA    host.py:1051 (fingerprint de la iteración actual) contra
             previous_fingerprint (host.py:1080-1081, guardado en la iteración
             ANTERIOR, cuyo valor también vino de 1050, pre-acción).
DISEÑO       ambos fingerprints son pre-acción ⇒ comparables.
REUTILIZAR   la observación de 1050 sigue siendo pre-acción; el fingerprint no
             cambia de semántica.
CAMBIO       ninguno. Verificado: el guard se ejerció 4 veces en la corrida
             medida (4 pares 974→1089) con el comportamiento esperado.
RIESGO       LOW.
```

### I-4. El host no acumula estado entre iteraciones (`FACT`)

```text
ENUNCIADO    ninguna iteración depende de memoria de una iteración anterior; el
             estado se relee del repositorio y del journal.
EVIDENCIA    host.py:444-446 (comentario explícito), policy §1/§9,
             host.py:1043 (`start = len(read_journal)`).
DISEÑO       cada iteración observa desde cero.
REUTILIZAR   la observación se pasa por parámetro y **no se almacena**: el
             atributo `self` no gana ningún campo. No hay memoria nueva.
CAMBIO       ninguno. La reutilización es intra-iteración e intra-frame.
RIESGO       LOW.
```

### I-5. Recuperación tras reinicio desde evidencia persistida (`FACT`)

```text
ENUNCIADO    una instancia nueva de host reconstruye la situación desde el
             repositorio y el journal.
EVIDENCIA    host.py:1219 (`reconstruct`), 1043, 668 (`read_journal` en el gate);
             tests `test_restart_reconstructs_and_continues...` (970),
             `test_the_ceiling_survives_a_process_restart...` (671),
             `test_recovery_after_restart_from_persisted_evidence_only` (762).
DISEÑO       nada se guarda en el objeto entre corridas.
REUTILIZAR   no afecta: el reinicio se prueba con instancias nuevas, y la
             reutilización no crea estado que sobreviva al frame.
CAMBIO       ninguno.
RIESGO       LOW.
```

### I-6. Evidencia fiel: el registro refleja el estado del momento (`FACT`)

```text
ENUNCIADO    el bloque `observed` de cada registro corresponde al estado en el
             que se tomó la decisión.
EVIDENCIA    host.py:484-508 (`_record` serializa la observación recibida).
DISEÑO       cada sitio de registro pasa una observación coherente con el
             momento (post-acción donde hubo acción).
REUTILIZAR   en el par (1050→591) el registro de `iterate` ya usa la observación
             post-1050/pre-acción; reutilizar 1050 produce **el mismo registro**.
             Los sitios post-acción (769/807/822/852/872/974) NO se tocan.
CAMBIO       ninguno en el contenido del registro.
RIESGO       LOW.
```

### I-7. El aislamiento de tests no se toca (`FACT`)

```text
ENUNCIADO    cada test construye su propio repositorio desechable bajo el
             scratch de su sesión (Plan 145, I-1).
EVIDENCIA    `_scratch` en los 4 archivos (uuid4), tests/pytest_isolation.py.
DISEÑO       propiedad por sesión, token declarado, poda por edad.
REUTILIZAR   el cambio propuesto es in-memory y no toca scratch, repositorios,
             sesiones, tokens ni fixtures.
CAMBIO       ninguno.
RIESGO       NONE.
```

### I-8. La frontera SAE decide antes del efecto (`FACT`)

```text
ENUNCIADO    `_apply_autonomy_gate` se evalúa antes de construir la delegación.
EVIDENCIA    host.py:601 (antes de 604-621), docstring 626-648,
             runtime/README.md:330-336.
DISEÑO       el gate recibe la observación y la acción, y no muta estado salvo
             `_last_autonomy`.
REUTILIZAR   el gate recibe `observation_B`; con la reutilización recibe
             `observation_A`, que es idéntica. Los campos que consume
             (`agent_task.resource_ceiling`, `declared_effects`, `scope_set`,
             `plan_path`) son idénticos.
CAMBIO       ninguno en el veredicto. **Único punto que el experimento debe
             verificar con cuidado** porque el gate lee git/journal/identidad
             (§21, invariante a instrumentar).
RIESGO       LOW, verificable.
```

### I-9. Determinismo (`FACT` + `MEASURED`)

```text
ENUNCIADO    la misma entrada produce la misma decisión.
EVIDENCIA    `derive_next_action` es pura por contrato (`derivation.py:203`);
             `observe` es determinista (§9.2); la suite es estable
             (CV mediano 0.003, auditoría previa).
DISEÑO       funciones puras sobre hechos.
REUTILIZAR   reutilizar un valor determinista en lugar de recomputarlo no cambia
             el resultado.
CAMBIO       ninguno.
RIESGO       NONE.
```

### I-10. La suite sigue siendo la red (`FACT`)

```text
ENUNCIADO    1543 tests verifican el comportamiento; cualquier cambio de
             producción debe pasar la batería canónica.
EVIDENCIA    docs/VERSIONING.md §4.1; 152 tests ejercitan el host.
DISEÑO       la batería es el gate.
REUTILIZAR   el experimento propuesto corre los 152 tests primero y la suite
             completa después (§21).
CAMBIO       ninguno.
RIESGO       LOW.
```

`INFERENCE` **Ninguno de los diez invariantes se rompe con la reutilización.**
Los que podrían parecer en tensión — I-2 (estado obsoleto) e I-4 (sin memoria) —
se resuelven porque el valor reutilizado es **fresco** (computado en el mismo
frame, sin mutación intermedia) y **no se almacena** (viaja como parámetro).

---

## 16. Why the Second Observation Exists

`FACT` Respuesta a la pregunta del pedido, con la evidencia de §4, §5, §14.

**Razón 1 — `iterate()` es autocontenido.** `iterate()` obtiene su propio estado
y no exige contexto al caller: `iterate(iteration)`. Es una forma limpia y
defensiva de escribir un paso de un loop. `FACT` Nació así en el commit original
(`4f85e67`).

**Razón 2 — `run()` necesita el fingerprint antes de decidir si entra.**
`run()` debe comparar el fingerprint de la iteración actual con el de la anterior
**para poder cortar antes de ejecutar** (`host.py:1062-1079`). Eso exige una
observación en `run()`. `FACT` Es una necesidad real y bien fundada.

**Razón 3 — no se pasó el valor.** Una vez que `run()` ya tenía la observación,
lo natural habría sido pasarla; el código no lo hace. `FACT` No hay ninguna razón
técnica en el código que lo impida: `iterate` podría recibirla, y `run` la tiene
en la mano.

`INFERENCE` **La causa real es la conjunción de (1) y (2) sin coordinación entre
ellas.** Cada una es correcta por separado:
- `run()` **debe** observar (razón 2);
- `iterate()` **debe** tener una observación (razón 1);
- nadie notó que son **la misma**.

`INFERENCE` **No es una defensa deliberada ante cambios de estado.** Si lo fuera,
habría alguna de estas señales, y **ninguna existe** (`FACT`, §14.3): un
comentario, un docstring, un test, un ADR, un CHANGELOG, o una escritura
deliberada entre las dos observaciones. Y hay evidencia en contra: la ventana
entre ambas es de **cuatro operaciones puras**, lo que no deja lugar a que
"algo cambie" — si el diseño quisiera detectar un cambio externo, el punto de
re-lectura estaría **después** de la acción (y de hecho lo está: 769/807/822/852/
872/974), no inmediatamente antes de decidir.

`INFERENCE` **No es herencia de capas posteriores** (`LEGACY` en ese sentido):
precede a SAE (135), al enforcement (138) y al envelope (159) (§14.1).

`INFERENCE` **No protege una garantía no evidente.** Los candidatos que el pedido
enumera y su veredicto:

| Hipótesis del pedido | Veredicto | Evidencia |
|---|---|---|
| `iterate()` necesita verificar precondiciones actualizadas | **parcial** — necesita una observación actual, no una *segunda* | §6, §9.5 |
| `run()` puede modificar el entorno antes de entrar en `iterate()` | **refutada** — no modifica nada (4 ops puras) | §5 |
| `observe()` establece invariantes internas | **refutada** — no muta nada | §7.2, §10 |
| `observe()` puede detectar cambios producidos por hooks | **refutada** — no hay hooks | §10.1 |
| existe una máquina de estados donde la 2ª observación marca una transición | **refutada** — no hay máquina de estados persistida (policy §2) y la 2ª observación no marca nada | §4, §14.2 |
| `iterate()` fue diseñado como punto de sincronización | **refutada** — no hay concurrencia que sincronizar | §10.1 |
| existe recuperación ante inconsistencias | **refutada en este punto** — la recuperación es entre iteraciones/reinicios, no intra-iteración | I-5 |
| la observación vuelve a validar aislamiento | **refutada** — `observe()` no valida aislamiento de tests | §7.2 |
| el resultado de `observe()` no es un snapshot completo | **refutada** — es completo (§7.1.1) | §7.1.1 |
| alguna implementación/subclase modifica el estado | **refutada** — no hay subclases | §12 |
| comportamiento implícito en métodos llamados por `observe()` | **refutada** — verificado método por método | §7.2 |
| **nadie se lo preguntó** | **la explicación que la evidencia sostiene** | §14.1, §14.3 |

---

## 17. Competing Hypotheses

`FACT` Las seis categorías del pedido, evaluadas una por una con su evidencia.

### H-1. `NECESSARY` — "`iterate()` necesita observar por sí mismo"

```text
SOSTIENE     iterate() debe actuar sobre una lectura fresca del estado real.
EVIDENCIA A FAVOR   host.py:591 es su única fuente de estado; el invariante I-1
                    requiere una observación actual; la política exige que cada
                    iteración se base en el estado real.
EVIDENCIA EN CONTRA la observación que run() ya computó ES una lectura fresca del
                    estado real, hecha en el mismo frame y sin mutación entre
                    medias (medido: 86/86 idénticas).
VEREDICTO    PARCIALMENTE VERDADERA. Es necesaria una observación; no es
             necesario que sea una SEGUNDA observación.
```

### H-2. `DEFENSIVE` — "es una defensa deliberada ante cambios de estado"

```text
SOSTIENE     la segunda lectura protege contra un cambio ocurrido entre ambas.
EVIDENCIA A FAVOR   ninguna directa.
EVIDENCIA EN CONTRA (a) la ventana son 4 operaciones puras; (b) los puntos de
                    re-lectura deliberada están DESPUÉS de cada acción
                    (769/807/822/852/872/974), no antes de decidir; (c) cero
                    comentarios, tests o documentos que la describan como
                    defensa; (d) las dos observaciones son idénticas en el
                    100 % de 86 casos reales.
VEREDICTO    REFUTADA como defensa deliberada. La defensa real existe y está
             en otro sitio (la re-observación post-acción).
```

### H-3. `CONTRACTUAL` — "es un contrato interno entre métodos"

```text
SOSTIENE     iterate() se compromete a obtener su propio estado y run() confía
             en ello.
EVIDENCIA A FAVOR   iterate(iteration) tiene esa firma; el docstring dice
                    "Run exactly one iteration".
EVIDENCIA EN CONTRA el contrato NO está declarado en ningún sitio (§14.2);
                    iterate no es API pública (§12); ningún test ni consumidor
                    lo ejercita (§11, §13); no hay subclases ni overrides.
VEREDICTO    VERDADERA PERO NO BINDING. Es un contrato *de facto* de la
             implementación, no un contrato declarado, probado ni consumido.
             Cambiarlo es una decisión, no una violación.
```

### H-4. `LEGACY` — "es herencia histórica"

```text
SOSTIENE     la duplicación se acumuló con el tiempo.
EVIDENCIA A FAVOR   ninguna.
EVIDENCIA EN CONTRA la duplicación existe en el COMMIT ORIGINAL (4f85e67,
                    planes 122/123); los commits posteriores no la tocaron ni la
                    introdujeron (§14.1).
VEREDICTO    REFUTADA como sedimentación por capas. (En sentido débil es
             "legacy" = código original no revisado desde entonces; eso es
             exacto y está recogido por H-6.)
```

### H-5. `ACCIDENTAL` — "es una redundancia accidental"

```text
SOSTIENE     nadie decidió duplicar; el código duplica porque run() necesitaba
             su observación y iterate() la suya, sin coordinarse.
EVIDENCIA A FAVOR   (a) cero documentación (§14.3); (b) ventana sin mutación;
                    (c) 86/86 idénticas; (d) ausencia de test o consumidor que
                    dependa de la duplicación; (e) las dos necesidades son
                    independientes y legítimas (§16), y nadie las coordinó.
EVIDENCIA EN CONTRA si iterate() se hiciera cargo de la observación y run()
                    dejara de observar, el guard de no-progreso perdería su
                    fingerprint pre-acción. Es decir: hay una razón para que
                    run() observe. Eso NO justifica que iterate() observe
                    también, pero sí muestra que la duplicación no es "gratuita".
VEREDICTO    VERDADERA para el DUPLICADO (la segunda lectura), no para el hecho
             de observar en run().
```

### H-6. `MIXED` — **la clasificación que la evidencia sostiene**

```text
COMPONENTE NECESARIO
  · iterate() debe decidir y actuar sobre una observación del estado real y
    actual. Eso es invariante (I-1, I-2) y no se discute.
  · run() debe tener una observación pre-acción para el fingerprint del guard
    de no-progreso (I-3). Eso también es una necesidad real.

COMPONENTE ACCIDENTAL
  · que esas dos necesidades se satisfagan con DOS LECTURAS DEL MISMO ESTADO
    EN EL MISMO FRAME, cuando una sola observación satisface ambas.
  · 86/86 medidas idénticas; ventana sin mutación; duplicación presente desde
    el commit original; cero documentación; cero tests; cero consumidores.
```

`INFERENCE` **La formulación precisa:** la segunda observación es
`NECESSARY` **como fuente de estado de `iterate()`** y `ACCIDENTAL` **como
duplicado de la que `run()` ya computó**. La separación entre ambas es lo que
hace la recomendación posible: **se elimina el duplicado, no la observación.**

```text
LO QUE SE ELIMINA       la segunda LECTURA (6 subprocesos, ~0.33 s por iteración)
LO QUE SE CONSERVA      la observación como fuente de decisión de iterate()
                        y como fingerprint pre-acción del guard
LO QUE NO SE TOCA       los 6 sitios de observación post-acción
                        (769/807/822/852/872/974), que protegen I-6
```

---

## 18. Candidate Designs

`INFERENCE` Las cuatro alternativas del pedido, evaluadas. **Ninguna
implementada.**

### Alternativa A — `run()` observa y pasa la observación a `iterate()`

```python
# host.py:1050  (sin cambio)
observation = self.observe()
fingerprint = observation.governance_fingerprint()
boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
action = derive_next_action(observation, boundary, ...)
...
# host.py:1083  (cambio)
record = self.iterate(iteration, observation)

# host.py:589   (cambio)
def iterate(self, iteration: int, observation: ChangeObservation) -> dict[str, Any]:
    boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
    action = derive_next_action(observation, boundary, ...)
    ...
```

| Dimensión | Evaluación |
|---|---|
| **Garantías preservadas** | las 10 de §15; en particular I-1 (la acción se deriva de una observación real), I-3 (el fingerprint sigue siendo pre-acción), I-4 (no se almacena nada) |
| **Riesgos** | (a) `iterate()` deja de ser invocable sin contexto — cambio de forma, sin consumidores hoy; (b) si en el futuro se introduce una mutación entre 1050 y 591, el cambio la enmascara (R-3, §19); (c) `derive_next_action` se sigue llamando dos veces (en `run` y en `iterate`) — la duplicación de *cálculo* no se elimina, sólo la de *lectura*. `INFERENCE`: el cálculo es puro y barato (~ms); la lectura es la cara |
| **Complejidad** | **muy baja**: 2 líneas tocadas, 1 firma |
| **Compatibilidad** | `iterate` no es API pública; 0 callers externos; 0 subclases; 0 tests. **Ruptura real: ninguna.** Ruptura de forma: `iterate()` pasa a exigir un argumento |
| **Ahorro potencial** | `MEASURED` 6 subprocesos y ~0.33 s por iteración (una lectura por iteración eliminada). `ESTIMATE` sobre la corrida medida: 86 lecturas de 444 (19.4 %) en los 4 archivos ⇒ ~31 s de subproceso de esos archivos (de 157.0 s). **No medido en wall clock de suite** |
| **Marca** | `MEASURED` (coste unitario) + `ESTIMATE` (efecto agregado) |

### Alternativa B — eliminar la observación de `run()` y dejar la de `iterate()`

| Dimensión | Evaluación |
|---|---|
| **Garantías preservadas** | I-1, I-2, I-4, I-5, I-6, I-7, I-8, I-9, I-10 |
| **Garantías en riesgo** | **I-3 se rompe**: el guard de no-progreso necesita un fingerprint **pre-acción** para comparar con el de la iteración anterior. Si `run()` no observa, no tiene fingerprint con el que decidir *antes* de entrar en `iterate()`. Habría que mover el guard dentro de `iterate()` (donde ya existe una observación) o mantener estado entre iteraciones — lo segundo viola I-4 |
| **Complejidad** | **media**: el guard tendría que reubicarse o el fingerprint pasar a formarse dentro de `iterate()`, cambiando el punto donde el loop corta |
| **Compatibilidad** | el comportamiento del guard es observable (`STOP_NO_PROGRESS`) y está testeado (`test_no_progress_guard_stops_instead_of_spinning`, 1009) |
| **Ahorro** | el mismo que A (una lectura por iteración) |
| **Veredicto** | **INFERIOR a A.** Ahorra lo mismo con más riesgo: mueve una decisión de control del loop y pone en tensión I-3 sin necesidad. **No recomendada.** |

### Alternativa C — mantener ambas observaciones y cachear el snapshot

```python
def iterate(self, iteration, observation=None):
    observation = observation or self.observe()   # fallback ambiguo
```

| Dimensión | Evaluación |
|---|---|
| **Garantías preservadas** | todas, formalmente |
| **Riesgos** | **introduce la ambigüedad que el repositorio evita por principio**: un parámetro opcional que cambia cuántas veces se lee el mundo real. Dos llamadas con la misma firma observable se comportan distinto. `AGENTS.md` (*Decision-Making Compass*) pide preferir claridad a maquinaria; esto añade una rama sin necesidad (un solo caller) |
| **Complejidad** | baja técnicamente; **alta conceptualmente** |
| **Compatibilidad** | total |
| **Ahorro** | el mismo, **sólo** si el caller pasa el argumento — es decir, la ambigüedad no compra nada que A no dé |
| **Veredicto** | **NO recomendada.** Un `observation=None` con fallback es exactamente el patrón "silenciosamente distinto según el caller" que este repositorio rechaza. Y una **cache** real (guardar la observación en el host) violaría I-4 (estado en el host) — descartada de plano |

### Alternativa D — mantener la semántica actual

| Dimensión | Evaluación |
|---|---|
| **Garantías preservadas** | todas por construcción |
| **Riesgos** | ninguno nuevo; se conserva el coste medido |
| **Complejidad** | nula |
| **Compatibilidad** | total |
| **Ahorro** | 0 |
| **Veredicto** | **DEFENDIBLE y es el estado actual.** La auditoría lo declara explícitamente válido: si el mantenedor prefiere no tocar `host.py`, la suite sigue siendo correcta — sólo cara |

### 18.1 Comparación (`INFERENCE` sobre `MEASURED`)

| Alternativa | Garantías | Riesgos | Complejidad | Compatibilidad | Potencial de ahorro | Veredicto |
|---|---|---|---|---|---|---|
| **A** — `run()` pasa la observación | las 10 preservadas | R-2 (concurrencia externa), R-3 (enmascarar mutación futura) | **muy baja** (2 líneas + 1 firma) | sin consumidores; cambia la forma de `iterate()` | `MEASURED` 6 subprocesos/~0.33 s por iteración; `ESTIMATE` ~31 s de subproceso en los 4 archivos | **RECOMENDADA para experimento** |
| **B** — quitar la de `run()` | I-3 en riesgo | mueve el control del loop | media | el guard es observable y testeado | igual a A | no recomendada |
| **C** — fallback/cache | todas | **ambigüedad de firma**; cache viola I-4 | baja técnica / alta conceptual | total | igual a A pero opcional | no recomendada |
| **D** — mantener | todas | ninguno | nula | total | 0 | válida |

`INFERENCE` **A y C tienen el mismo techo de ahorro; A tiene menos superficie de
error.** La elección entre A y D es de gobernanza, no técnica.

---

## 19. Risk Analysis

`FACT` Riesgos identificados, con su base y su severidad.

| # | Riesgo | Base | Severidad | Mitigación |
|---|---|---|---|---|
| **R-1** | **Cambio de producción en la pieza más cargada de garantías.** `host.py` concentra el loop, el gate SAE, la delegación, el registro y las condiciones derivadas | `FACT`: `host.py` tiene 1295 líneas y es ejercitado por 152 tests | **ALTA** | experimento acotado a una línea y una firma (§21); los 152 tests primero, la suite completa después |
| **R-2** | **Cambio externo concurrente entre las dos lecturas.** Si otro proceso mutara el repositorio entre 1050 y 591, la reutilización perdería la detección | `FACT`: no hay hilos ni modelo concurrente declarado; `FACT`: la ventana la cubre una lectura de 1050 y ~microsegundos de código puro | **BAJA** | el modelo de ejecución es de un solo driver; si se quisiera soportar concurrencia, el punto correcto no es `iterate()` sino el contrato del loop entero (`NEEDS_DESIGN` aparte) |
| **R-3** | **Enmascarar una mutación futura introducida entre 1050 y 591.** Con la reutilización, una escritura añadida en esa ventana dejaría de verse | `INFERENCE` | **MEDIA** | documentar la precondición en el docstring de `iterate()` ("the observation must be the one taken at the start of this iteration, before any write"); el invariante I-2 lo cubre |
| **R-4** | **Pérdida de autonomía de `iterate()`.** Deja de ser invocable sin contexto | `FACT`: no hay consumidores; `FACT`: no es API pública | **BAJA** | decidirlo explícitamente; si se quiere preservar, es la Alternativa C (no recomendada) |
| **R-5** | **Que el ahorro no se materialice.** El coste unitario está medido, el efecto agregado no | `FACT`: el cambio no se ejecutó | **MEDIA** | medir antes/después en el experimento (§21); la estimación previa de 40–70 s sigue siendo `ESTIMATE` |
| **R-6** | **Aplicar el mismo cambio a los otros tres sitios sin analizarlos uno por uno** | los sitios (870→872), (1154→1287), (1287→1117) tienen estructuras distintas (uno está dentro de un camino condicional; otro atraviesa `write_run_report`) | **MEDIA** | el experimento toca **sólo** (1050→591); los otros tres son trabajo posterior y separado |
| **R-7** | **Creer que el cambio es seguro porque "parece obvio"** | advertencia explícita del pedido | **MEDIA** | por eso la decisión es `SAFE_TO_EXPERIMENT` y **no** `SAFE_TO_REFACTOR`: falta la verificación por ejecución |
| **R-8** | **Interacción con el gate SAE.** El gate lee `agent_task.resource_ceiling`, `declared_effects`, `scope_set`, y consulta git/journal/identidad a través de la observación | `FACT`: `host.py:652-687` | **MEDIA** | el experimento debe comparar los registros `autonomy` antes/después, campo por campo (§21) |
| **R-9** | **Interacción con el guard de no-progreso** | I-3 | **BAJA** | comparar los `STOP_NO_PROGRESS` antes/después; se ejerció 4 veces en la corrida medida |
| **R-10** | **`ObservationError` en un momento distinto** | `FACT`: hoy el fallo se detecta dos veces (1050 y 591); con el cambio, una | **MUY BAJA** | el fallo se sigue detectando en 1050; el comportamiento observable es el mismo salvo que no se lanza dos veces |

`INFERENCE` **R-1 y R-7 son los que mandan:** el cambio es pequeño y su efecto
es demostrable, pero vive en la pieza más sensible del runtime DEV. La respuesta
proporcionada es un **experimento acotado**, no un refactor directo —
exactamente la distinción `SAFE_TO_EXPERIMENT` / `SAFE_TO_REFACTOR`.

---

## 20. Decision

```text
RESULT = SAFE_TO_EXPERIMENT

SECOND_OBSERVE_CLASSIFICATION = MIXED
```

### 20.1 Por qué no `KEEP_CURRENT` (`INFERENCE`)

`FACT` Ninguna de las razones que justificarían mantener la segunda observación
se sostiene: no hay defensa deliberada (cero documentación, ventana sin
mutación), no hay contrato declarado (no es API pública, cero consumidores,
cero tests), no hay subclases ni hooks, no hay concurrencia que sincronizar, y
la duplicación precede a toda la maquinaria posterior. `MEASURED` 86 de 86 pares
idénticos en corrida real.

### 20.2 Por qué no `SAFE_TO_REFACTOR` (`INFERENCE`)

`FACT` El pedido prohíbe expresamente usar `SAFE_TO_REFACTOR` "solamente porque
el cambio parece obvio". Y hay dos razones concretas para no darlo:

1. **El efecto agregado no está medido** (R-5). El coste unitario sí (6
   subprocesos, ~0.33 s), pero la promesa de ahorro de suite sigue siendo
   `ESTIMATE`.
2. **`iterate()` cambia de forma** (R-4) y eso es una **decisión de contrato**,
   aunque hoy no rompa nada.

`INFERENCE` Un `SAFE_TO_REFACTOR` exigiría, como mínimo, haber medido el
antes/después con la suite completa. Eso es precisamente el experimento.

### 20.3 Por qué no `NEEDS_DESIGN` (`INFERENCE`)

`FACT` No falta una decisión arquitectónica: el invariante ya está satisfecho y
la política no se opone (§14.4). Falta **verificación empírica**, no diseño.

### 20.4 Por qué no `INSUFFICIENT_EVIDENCE` (`INFERENCE`)

`FACT` La evidencia es suficiente para decidir **el experimento**: código,
tests, documentación, historial, invariantes y dos sondas medidas
independientes. Lo que falta es la ejecución del cambio, que el pedido prohíbe
en esta fase.

### 20.5 Qué queda demostrado y qué no (`FACT`/`INFERENCE`)

```text
DEMOSTRADO (FACT/MEASURED)
  · observe() es read-only, sin side effects, sin cache, sin mutación del host
  · es determinista: no usa reloj, random ni datetime
  · dos observaciones consecutivas sin mutación intermedia son idénticas
    (189/189 pares; 86/86 en el par run()->iterate(), en corrida real)
  · todos los pares con acción entre medias difieren (118/118) ⇒ el digest
    distingue correctamente mismo-estado de estado-nuevo
  · entre 1050 y 591 no hay ninguna operación mutadora (4 operaciones puras)
  · no hay hilos, subclases, overrides, hooks ni monkeypatches de observe
  · iterate() tiene un único caller en todo el repositorio (host.py:1083)
  · iterate() no es API pública y ningún test lo invoca
  · la duplicación existe desde el commit original de los planes 122/123
  · la política exige "sin memoria ENTRE iteraciones", no "una lectura por
    función"
  · la redundancia tiene CUATRO sitios, no uno (189 lecturas evitables de 444 = 42.6 %)

NO DEMOSTRADO (UNKNOWN/ESTIMATE)
  · el ahorro de wall clock de la suite (no se ejecutó el cambio)
  · que el cambio sea inocuo bajo el gate SAE activo en todos los caminos
    (razonado por campo, no verificado por ejecución)
  · si los otros tres sitios son igual de seguros de tocar (no analizados
    en profundidad; estructuras distintas)
```

---

## 21. Proposed Follow-Up Experiment

`RECOMMENDED` **NO EJECUTADO EN ESTA FASE.** Diseño del experimento que debería
ejecutarse en una fase posterior, **como su propio Change autorizado** (RFC-56:
toca `runtime/orchestrator/host.py`, código de producción DEV; requiere plan
`Aprobado para ejecución` — clase B, DEV-only, sin efecto de payload).

### 21.1 Cambio mínimo

```text
ARCHIVO   runtime/orchestrator/host.py
LÍNEA 589 def iterate(self, iteration: int, observation: ChangeObservation) -> dict[str, Any]:
LÍNEA 591 (ELIMINAR)  observation = self.observe()
LÍNEA 1083            record = self.iterate(iteration, observation)

+ docstring de iterate(): declarar la precondición
  "``observation`` must be the reading taken at the start of this iteration,
   before any write: the loop observes once and decides once."

+ import de ChangeObservation (ya presente en el archivo: se usa en firmas)
```

`FACT` Total: **1 línea eliminada, 1 firma extendida, 1 call site ajustado, 1
docstring**. Ninguna otra llamada a `observe()` se toca (los 12 sitios restantes
permanecen).

### 21.2 Orden de ejecución

```text
1. los 152 tests de los 4 archivos dominantes
   python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py \
       tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q
2. las suites de autonomía y dogfood (usan el host con gate SAE activo)
   python -m pytest tests/test_autonomous_scope.py tests/test_autonomy_effects_dogfood.py \
       tests/test_sae_scope_enforcement_dogfood.py tests/test_autonomous_scope_dogfood.py -q
3. la suite canónica completa
   python -m pytest tests/ -q
4. el leg del harness (no debería verse afectado; verificación de no-regresión)
   python -m pytest protocol/.agents/harness/tests/ -q
5. los checkers de la batería (docs/VERSIONING.md §4.1)
```

### 21.3 Invariantes a verificar (uno por uno, no en bloque)

```text
I-1  la acción se deriva de una observación del estado real
     → comparar `records[*].action` y `[*].rationale` antes/después
I-2  no se actúa sobre estado obsoleto
     → comparar `records[*].observed` completo antes/después
I-3  el guard de no-progreso comparaba fingerprints pre-acción
     → forzar STOP_NO_PROGRESS (test 1009) y comparar el registro
I-4  el host no gana estado
     → `diff` de los atributos de instancia del host durante la corrida
I-5  recuperación tras reinicio
     → tests 970, 762, 671 (usan instancias nuevas) deben pasar sin cambios
I-6  fidelidad del registro
     → comparar el payload JSON del journal byte a byte antes/después
I-8  veredicto de la frontera SAE
     → comparar `records[*].autonomy` y `records[*].autonomy_checkpoint`
        campo por campo, con `--sae` activo
I-9  determinismo
     → dos corridas con el cambio deben dar journal idéntico
```

### 21.4 Comparaciones requeridas

| # | Comparación | Método | Criterio |
|---|---|---|---|
| 1 | **funcional** | `pytest` antes/después, mismos tests, mismo árbol | idéntico `passed/failed/skipped` |
| 2 | **resultados observados** | journal de una corrida cornerada (`git add -A` + `run`) antes/después; `sha256` del `journal.jsonl` | **byte-idéntico** o diferencia explicada campo por campo |
| 3 | **subprocesos** | plugin contador externo (el de la auditoría previa §23.4) antes/después | reducción esperada ≈ 1 × nº de iteraciones del par (1050→591) |
| 4 | **runtime** | `pytest --durations=0` antes/después, **misma sesión, misma máquina** | registrar; **no** exigir una cifra — el objetivo es el conteo de subprocesos y la equivalencia funcional |
| 5 | **errores** | `ObservationError` forzado (test 1109) antes/después | mismo comportamiento observable (la excepción sale de `run`) |
| 6 | **registro SAE** | `--sae` sobre un fixture con scope, drift y techo | `autonomy` y `autonomy_checkpoint` idénticos |
| 7 | **flakiness** | 3 corridas de los 152 tests | 0 diferencias entre corridas (baseline medido: CV mediano 0.003) |

### 21.5 Criterios de rollback

```text
ROLLBACK SI:
  · cualquier test de los 152 falla y la causa no es un cambio de comportamiento
    esperado y documentado
  · el journal difiere en un campo que no sea explicable por el cambio
  · el veredicto de `autonomy`/`autonomy_checkpoint` difiere en cualquier caso
  · `STOP_NO_PROGRESS` deja de disparar donde lo hacía (test 1009)
  · aparece cualquier dependencia de orden entre tests (señal de estado
    compartido, prohibido por Plan 145)
  · el conteo de subprocesos NO baja (el cambio no aporta)

ROLLBACK = revertir las 4 líneas. Coste de reversión: trivial.
```

### 21.6 Explícitamente fuera del experimento

```text
· los sitios (870→872), (1154→1287), (1287→1117): analizarlos y decidirlos
  por separado, cada uno con su propio razonamiento
· cualquier cambio en tests
· cualquier cambio en el gate SAE
· cualquier cache o estado en el host
· cualquier reutilización entre iteraciones o entre corridas
```

---

## 22. Reproducibility

`FACT` Todo lo necesario para repetir el razonamiento.

### 22.1 Archivos inspeccionados

```text
runtime/orchestrator/host.py             (1295 líneas, completo)
runtime/orchestrator/observation.py      (1197 líneas, camino de observe + ChangeObservation)
runtime/orchestrator/derivation.py       (firma y contrato de derive_next_action)
runtime/orchestrator/store.py            (__init__, _write_text, layout, reads)
runtime/orchestrator/__init__.py         (superficie pública / __all__)
runtime/orchestrator/__main__.py         (CLI: --observe, run, --reconstruct)
runtime/orchestrator/worker.py           (repository_snapshot, run_command_set)
runtime/README.md                        (loop, gate, límites)
.agents/policies/autonomous-orchestration.md  (§1 qué es el host, §8, §9, §10)
.agents/policies/supervised-autonomous-execution.md  (referencias al loop)
tests/test_autonomous_orchestrator.py    (1158 líneas)
tests/test_agent_worker.py               (1092 líneas)
tests/test_sae_scope_enforcement.py      (1081 líneas)
tests/test_autonomy_effects.py           (801 líneas)
tests/AGENTS.md                          (conjunto anclado, reglas de scratch)
docs/behavior-patterns.md                (patrón del host)
docs/working/audits/architecture-capability-review.md:183  ("re-observa")
docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md   (hallazgo previo)
docs/plans/122-dev-autonomous-orchestrator-mvp.md:35
docs/plans/123-dev-agent-worker-mvp.md
docs/plans/{135,138,145,159}             (contexto de las capas posteriores)
conftest.py, tests/pytest_isolation.py   (aislamiento; verificación de no-tensión)
```

### 22.2 Comandos de verificación estática

```bash
# el par en cuestión
grep -n "self\.observe()" runtime/orchestrator/host.py

# todas las llamadas a iterate
grep -rn "iterate(" --include=*.py .

# subclases de ExecutionHost
grep -rn "class .*(ExecutionHost)" --include=*.py .

# concurrencia en runtime
grep -rn "^import threading\|^import multiprocessing\|import signal\|Thread(\|Lock(" runtime/

# nondeterminismo en observation.py
grep -n "utc_now\|time\.\|random\|datetime" runtime/orchestrator/observation.py

# pureza de la derivación (no debe tocar store/IO)
grep -n "store\|write\|open(\|subprocess\|self\." runtime/orchestrator/derivation.py

# superficie pública
grep -n "__all__" -A 25 runtime/orchestrator/__init__.py

# historial del par
git log --oneline -- runtime/orchestrator/host.py
for c in 4f85e67 4aa2617 7c4fec3 b0e37a5 2de6bfe HEAD; do
  echo "$c: $(git show $c:runtime/orchestrator/host.py | grep -c 'self\.observe()')"
done

# declaración del invariante
grep -n "holds no state\|no memory\|no cursor" \
  runtime/orchestrator/host.py .agents/policies/autonomous-orchestration.md runtime/README.md
```

### 22.3 Sondas ejecutadas (read-only, fuera del árbol versionado)

```powershell
# Sonda 1 — equivalencia de payloads (3 escenarios, n=3)
python probe_observe_equivalence.py
#   construye repos con los builders REALES de la suite; compara to_dict()
#   completo + git_state entre dos observe() consecutivas

# Sonda 2 — atribución por call site en corrida real
$env:PYTHONPATH="<dir>"; $env:TRACE_JSON="<dir>\trace_sites.json"
python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
    tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py `
    -q -p no:cacheprovider -p observe_trace_sites
#   envuelve ExecutionHost.observe, registra nº de línea del caller + digest
#   → 152 passed, 444 llamadas, 229.73 s
```

`FACT` **Ninguna sonda modificó comportamiento**: la función original siempre se
invocó y su valor se devolvió intacto. La instrumentación vivió en
`%TEMP%\argentos-semantic-audit\` y **fue eliminada al terminar**.

### 22.4 Commits históricos relevantes (`FACT`)

```text
4f85e67  feat(dev): consolidate autonomous orchestrator and agent worker mvps (plans 122, 123)
         ← ORIGEN de la doble observación (11 llamadas a self.observe())
4aa2617  refactor(dev): harden orchestrator runtime maintainability      (11, sin cambios)
7c4fec3  feat(runtime): materialize supervised autonomous execution (plan 135)  (12)
b0e37a5  feat(runtime): enforce SAE scope and authority before the effect (plan 138)  (12)
2de6bfe  feat(runtime): materialize the autonomy effect and resource frontiers (plan 159)  (13)
fb0786a  HEAD (dev, 2026-10-13)
```

### 22.5 Hipótesis descartadas (`FACT`)

```text
DESCARTADA  "observe() muta estado"                       refutada por lectura + medición
DESCARTADA  "hay hilos o concurrencia"                    refutada por grep
DESCARTADA  "hay subclases que sobreescriben iterate"      refutada por grep
DESCARTADA  "algún test depende de la 2ª observación"      refutada: 0 llamadas a iterate
DESCARTADA  "la 2ª observación se añadió con SAE (plan 135)" refutada por git: existe en 4f85e67
DESCARTADA  "el digest es insensible y por eso coinciden"   refutada: 118/118 pares con
                                                            acción difieren
DESCARTADA  "observe() usa el reloj"                       refutada por grep
DESCARTADA  "el snapshot es parcial y hay que completarlo"  refutada: ChangeObservation es completo
DESCARTADA  "run() muta el entorno antes de iterate()"      refutada: 4 operaciones puras
DESCARTADA  "hay una máquina de estados que la 2ª obs marca" refutada: policy §2 lo prohíbe
DESCARTADA  "es deuda acumulada por capas posteriores"      refutada por git
```

### 22.6 Incertidumbres restantes (`UNKNOWN`)

```text
U-1  el ahorro de wall clock de la suite (no ejecutado; la estimación 40–70 s
     de la auditoría previa sigue siendo ESTIMATE)
U-2  el comportamiento con el gate SAE en TODOS los caminos (razonado campo por
     campo en §21.3, no verificado por ejecución)
U-3  la seguridad de los otros tres sitios de duplicación (estructuras distintas;
     no analizados al mismo nivel de detalle)
U-4  las 4 observaciones no emparejadas en la secuencia de la sonda 2
     (INFERENCE: fronteras de secuencia, no llamadas perdidas)
U-5  el coste real en Linux/CI (heredado: todas las mediciones son Windows)
```

---

## 23. Open Questions

`UNKNOWN` Preguntas que esta auditoría no resuelve y que no bloquean la decisión.

```text
Q-1  ¿El mantenedor quiere que iterate() siga siendo autocontenido?
     Es una decisión de forma, no de corrección. La evidencia no la resuelve
     porque es una preferencia de contrato. (§12, §18)

Q-2  ¿Los otros tres sitios de duplicación (870→872, 1154→1287, 1287→1117)
     deben tratarse en el mismo Change o en Changes separados?
     INFERENCE: separados — (870→872) está en un camino condicional,
     (1154→1287) sólo ocurre con el
     gate SAE activo. Cada uno merece su verificación.

Q-3  ¿Debería `iterate()` documentar la precondición de §21.1 en la policy y no
     sólo en el docstring? Es una decisión documental (clase B).

Q-4  ¿Existe un modelo de ejecución concurrente previsto para el host?
     FACT: no hoy (§10.1). Si se previera, el punto de decisión sería el
     contrato del loop entero, no este par. (NEEDS_DESIGN aparte, si aplica.)

Q-5  ¿El `test_git_state_reports_the_cli_availability_explicitly`
     (test_autonomous_orchestrator.py:1153), que lee el repo real, debería
     declararse en el conjunto anclado de tests/AGENTS.md?
     Heredada de la auditoría de ejecución (§25 F-5). No relacionada con esta
     pregunta, pero detectada de nuevo al leer el archivo.
```

---

## 24. Final Status

```text
RESULT = SAFE_TO_EXPERIMENT

SECOND_OBSERVE_CLASSIFICATION = MIXED

  NECESSARY  as the iteration's own source of state (iterate() must decide on a
             fresh reading of the real, current state — invariants I-1, I-2)
  ACCIDENTAL as a *duplicate* of the observation run() already computed at
             host.py:1050, in the same frame, with no intervening mutation
             (MEASURED: 86/86 identical in a real 152-test run; 189/189
             consecutive pairs without mutation; 187/187 pairs WITH an action
             between them differ)

PRODUCTION_CHANGES = 0
TEST_CHANGES       = 0
CI_CHANGES         = 0
DEPENDENCY_CHANGES = 0

NEXT_ACTION = Open the authorized Change for the bounded pilot of §21 (pass
              run()'s observation into iterate() at host.py:1083) and run it
              with the 152 dominant tests first and the full canonical battery
              second, comparing the journal byte for byte.
```

### 24.1 Una frase para la decisión (`INFERENCE`)

> `run()` observa porque necesita el fingerprint pre-acción del guard de
> no-progreso; `iterate()` observa porque necesita un estado del cual derivar y
> actuar. **Las dos necesidades son reales; el objeto que las satisface es el
> mismo.** La segunda lectura no protege ninguna garantía: **no hay hook, no hay
> hilo, no hay mutación, no hay contrato declarado, no hay test, no hay
> subclase — y 86 de 86 mediciones dicen que devuelve exactamente lo mismo.**
> Lo que se elimina es la lectura duplicada, no la observación; y lo que debe
> decidirse antes de tocar `host.py` no es si el cambio es correcto —eso está
> medido— sino si se acepta que `iterate()` deje de ser autocontenido.

### 24.2 Lo que esta auditoría NO autoriza

```text
NO autoriza implementar el cambio (es SAFE_TO_EXPERIMENT, no SAFE_TO_REFACTOR)
NO autoriza tocar los otros tres sitios de duplicación
NO eleva a hecho la estimación de ahorro de 40–70 s
NO propone cache, estado en el host, ni reutilización entre iteraciones
NO propone compartir nada entre tests (Plan 145 intacto)
```

---

*Fin del informe. 0 cambios en producción, tests, CI y dependencias. La
instrumentación vivió fuera del árbol versionado y fue eliminada. La única
modificación documental es este archivo y su registro en
`docs/working/audits/INDEX.md`.*
