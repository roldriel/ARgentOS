# EXECUTION_HOST_OBSERVATION_PILOT — 2026-10-14

```text
RESULT = SAFE_TO_KEEP_EXPERIMENT

PILOT_SCOPE = run.observe -> iterate
SECOND_OBSERVE_REMOVED = YES
OTHER_DUPLICATES_TOUCHED = NO
FUNCTIONAL_EQUIVALENCE = VERIFIED
FOCUSED_TESTS = PASS
DOMINANT_152_TESTS = PASS
FULL_CANONICAL_SUITE = PASS

OBSERVATIONS_BEFORE = 444   (los 152 dominantes)   |  254 (suites SAE)
OBSERVATIONS_AFTER  = 358                          |  213
                    = -86 (-19.4 %)                |  -41 (-16.1 %)

SUBPROCESSES_BEFORE = 2777  (sólo los lanzados dentro de observe())
SUBPROCESSES_AFTER  = 2242
                    = -535

RUNTIME_BEFORE = 276.59 s  (152 dominantes, aislado)
RUNTIME_AFTER  = 225.62 s
RUNTIME_SAVED  = 50.97 s
RUNTIME_SAVED_PERCENT = 18.4 %   ← NO atribuible con confianza al cambio:
                                   dos corridas del MISMO código variaron
                                   hasta 42 s (15 %) en esta máquina

JOURNAL_EQUIVALENCE = IDENTICAL
SAE_AUTONOMY_EQUIVALENCE = IDENTICAL
NO_PROGRESS_GUARD_EQUIVALENCE = IDENTICAL

PLAN_145_COMPLIANCE = VERIFIED

PRODUCTION_CHANGES = 1 file (runtime/orchestrator/host.py, +12 −2)
TEST_CHANGES = 0
CI_CHANGES = 0
DEPENDENCY_CHANGES = 0

ROLLBACK = NO

NEXT_GATE = Decidir si se acepta que iterate() reciba la observación como
            argumento; mientras esa decisión no exista, el piloto se conserva
            como experimento y no se propaga a los otros pares.
```

**Clase documental:** Working / Audit (provenance) — **no normativo** (RFC-69,
`docs/AGENTS.md`).
**Naturaleza:** piloto experimental con cambio de producción acotado,
reversible y medido.
**Fecha:** 2026-10-14 · **Rama:** `dev` · **HEAD:** `fb0786a0b9b872796e5e4b223cf92bc011c22139`
(git HEAD y `dev` no cambiaron: el piloto **no commitea**).
**Basado en:** `docs/working/audits/EXECUTION_HOST_SEMANTIC_AUDIT_2026-10-14.md`
(que concluyó `SAFE_TO_EXPERIMENT`) y
`docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md` (que midió el costo).

---

## 1. Objetivo

Ejecutar un experimento controlado, reversible y medible que verifique si la
observación producida por `ExecutionHost.run()` puede ser consumida por
`ExecutionHost.iterate()` en el mismo ciclo, eliminando **únicamente** la
segunda llamada a `observe()` del camino

```text
run()
  └── observe()          # host.py:1050
      └── iterate()
          └── observe()  # host.py:591   ← el duplicado
              └── action
```

sin alterar ninguna garantía observable: contenido de la observación, orden
lógico, no-progress guard, condiciones de terminación, excepciones, valores de
retorno, efectos sobre journal, SAE/autonomy, transiciones de estado y acción
finalmente ejecutada.

**No** era objetivo: eliminar `observe()`, introducir cache o memoria entre
iteraciones, reutilizar repositorios, modificar Plan 145, ni tocar los otros
pares de observaciones identificados por la auditoría semántica.

---

## 2. Hipótesis

```text
ANTES
  run()      observe() -> S1
             iterate()
               observe() -> S2          (S2 debe ser idéntico a S1)
               action(S2)

DESPUÉS
  run()      observe() -> S
             iterate(S)
               action(S)

S == S'  ⇔  la segunda observación es semánticamente innecesaria y puede
            reemplazarse por el mismo dato sin alterar ninguna garantía.
```

Condición de refutación declarada de antemano: si `S != S'` en algún caso
comparable, el piloto debía revertirse (§14).

---

## 3. Estado inicial

`FACT` Registrado antes de tocar nada:

```text
GIT_HEAD_BEFORE = fb0786a0b9b872796e5e4b223cf92bc011c22139
BRANCH          = dev
WORKTREE_STATUS =  M docs/working/audits/INDEX.md
                  ?? docs/planificacion-argentos-diseno-2026-10-13.md
                  ?? docs/working/audits/EXECUTION_HOST_SEMANTIC_AUDIT_2026-10-14.md
                  ?? docs/working/audits/TEST_ARCHITECTURE_AUDIT_2026-10-13.md
                  ?? docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md
                  ?? docs/working/audits/TEST_SUITE_AUDIT_2026-10-13.md
                   (todo documental; 0 cambios funcionales previos)
```

`FACT` Verificación de las premisas **en el código**, no en la auditoría
(§3 del pedido):

| # | Premisa | Verificación | Resultado |
|---|---|---|---|
| 1 | `run()` necesita la observación para el no-progress guard | `host.py:1051` (`fingerprint = observation.governance_fingerprint()`) y `1063-1066` (comparación con `previous_fingerprint`) | **confirmada** |
| 2 | `iterate()` necesita una observación para derivar | `host.py:591` es su única fuente; alimenta `boundary`, `derive_next_action`, `_apply_autonomy_gate` y `_build_delegation` | **confirmada** |
| 3 | la observación de `run()` puede alimentar a `iterate()` | no hay mutación entre `1050` y `591` (§5) | **confirmada** |
| 4 | no hay mutación legítima entre ambas | las líneas `1051-1081` son 4 operaciones puras | **confirmada** |
| 5 | no hay override/subclase/monkeypatch que dependa de que `iterate()` observe | `grep 'class .*(ExecutionHost)'` → 0; `grep 'def observe(self'` → 1 (el propio); `grep 'def iterate(self'` → 1; `grep '\.iterate('` → 1 (host.py:1083); `grep 'setattr.*observe'` en tests → 0 | **confirmada** |
| 6 | no hay contrato externo que exija que `iterate()` sea autosuficiente | `iterate` **no** está en `__all__` de `runtime/orchestrator/__init__.py`; el CLI (`__main__.py`) nunca lo llama; ningún test lo invoca; los documentos que lo mencionan (`runtime/README.md:331`, `ADR-19:162`, planes 138:592/621 y 159:40/65) describen **dónde** corre el gate, no su firma | **confirmada** |

`FACT` No apareció evidencia nueva que contradijera la auditoría semántica.
**No fue necesario detener el experimento.**

---

## 4. Baseline

`FACT` Instrumentación **temporal y externa** (`%TEMP%\argentos-pilot\`),
eliminada al finalizar (§19). Nunca se convirtió en infraestructura permanente.
Envuelve `ExecutionHost.observe` y los métodos que **consumen** una observación,
registrando un digest del payload y el costo en subprocesos, sin alterar
comportamiento (el original siempre se invoca y su valor se devuelve intacto).

`MEASURED` Baseline:

```text
BASELINE_FOCUSED_TESTS        = los 152 dominantes (los 4 archivos de la autopsia)
BASELINE_FOCUSED_RESULT       = 152 passed, 0 failed
BASELINE_FOCUSED_RUNTIME      = 276.59 s   (job A) / 234.82 s (trace job B)
BASELINE_152_COUNT            = 152
BASELINE_152_RUNTIME          = 276.59 s
BASELINE_152_RESULT           = 152 passed
BASELINE_152_SUBPROCESS_COUNT = 2777   (sólo los lanzados DENTRO de observe())
BASELINE_152_OBSERVE_COUNT    = 444
```

`MEASURED` Baseline por sitio de `observe()` (los 152 dominantes):

| sitio (`host.py`) | llamadas | subprocesos | tiempo |
|---|---:|---:|---:|
| **591** (`iterate`) | **86** | **535** | **36.2 s** |
| 769 | 5 | 32 | 2.2 s |
| 807 | 1 | 6 | 0.4 s |
| 822 | 1 | 6 | 0.4 s |
| 852 | 1 | 6 | 0.5 s |
| 870 | 45 | 284 | 19.1 s |
| 872 | 45 | 284 | 19.3 s |
| 974 | 16 | 97 | 6.5 s |
| 1050 (`run`) | 87 | 541 | 37.8 s |
| 1089 | 24 | 154 | 10.8 s |
| 1117 | 50 | 314 | 21.4 s |
| 1154 | 50 | 314 | 21.5 s |
| 1287 | 29 | 178 | 12.0 s |
| fuera de `host.py` | 4 | 26 | 1.9 s |
| **total** | **444** | **2777** | **~190 s** |

`MEASURED` Otros datos de baseline:

```text
BASELINE_RUN_RESULT              = los 152 pasan; run() devuelve HostRun válido
BASELINE_EXCEPTIONS              = ninguna
BASELINE_JOURNAL_OUTPUT          = 115 registros de journal en 46 tests que corren el host
BASELINE_SAE_AUTONOMY_OUTPUT     = 58 registros, 56 con bloque `autonomy` no nulo
                                   (suites SAE, gate activo)
BASELINE_NO_PROGRESS_GUARD       = 83 pares `derive_next_action` consecutivos;
                                   el guard está realmente ejercitado (4 salidas
                                   por no-progress en la corrida de la autopsia)
```

`FACT` **Nota metodológica importante**: la varianza de wall clock de esta
máquina es alta. Dos corridas **del mismo código** de los 152 tests dieron
276.59 s y 234.82 s (**15 % de diferencia**). Esto condiciona la interpretación
del ahorro (§15) y se declara desde el baseline.

---

## 5. Cambio exacto realizado

`FACT` Diff completo del cambio de producción:

```diff
--- a/runtime/orchestrator/host.py
+++ b/runtime/orchestrator/host.py
@@ -586,9 +586,19 @@ class ExecutionHost:
             input_artifacts=tuple(input_artifacts),
         )
 
-    def iterate(self, iteration: int) -> dict[str, Any]:
-        """Run exactly one iteration and return its journal record."""
-        observation = self.observe()
+    def iterate(
+        self, iteration: int, observation: ChangeObservation
+    ) -> dict[str, Any]:
+        """Run exactly one iteration and return its journal record.
+
+        ``observation`` is the reading of the change taken **at the start of this
+        iteration, before any write**: ``run`` computes it once and hands it over,
+        so the loop reads the repository and the persisted evidence once per
+        iteration instead of twice (the two readings are the same state — nothing
+        between them mutates it). It is a value passed within the iteration, never
+        persisted: the host still holds no state between iterations
+        (``.agents/policies/autonomous-orchestration.md`` §1/§9).
+        """
         boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
         action = derive_next_action(
             observation,
@@ -1080,7 +1090,7 @@ class ExecutionHost:
                 previous_kind = action.kind
                 previous_fingerprint = fingerprint
 
-            record = self.iterate(iteration)
+            record = self.iterate(iteration, observation)
             self.store.append_iteration(self.plan, record)
             records.append(record)
             if record.get("terminal"):
```

`FACT` Contenido efectivo: **se elimina 1 línea** (`observation = self.observe()`),
**se extiende 1 firma** y **se ajusta 1 sitio de llamada**. La docstring
**documenta la precondición** que el cambio introduce, que es justamente el
riesgo R-3 de la auditoría semántica ("enmascarar una mutación futura
introducida entre las dos observaciones").

`FACT` El cambio **no** toca:
- los otros 12 sitios de `observe()` (`769/807/822/852/870/872/974/1089/1117/1154/1287` + la llamada directa);
- `_apply_autonomy_gate` ni su punto de invocación (sigue invocándose desde
  `iterate`, antes de `_execute_delegation`: `host.py:611` antes → `621` después);
- el segundo `derive_next_action` (ver §7 y §10, aclaración importante);
- la firma de `run()`;
- ninguna otra parte de `ExecutionHost`.

---

## 6. Archivos modificados

```text
runtime/orchestrator/host.py    +12 −2    (el cambio del piloto)
docs/working/audits/EXECUTION_HOST_OBSERVATION_PILOT_2026-10-14.md   (este informe)
docs/working/audits/INDEX.md    +1 fila   (registro del informe)
```

`FACT` Sin cambios en: tests, `conftest.py`, `tests/pytest_isolation.py`, CI,
dependencias, `protocol/`, `dist/`, `ROADMAP.md`, `docs/adr/`.

---

## 7. Contrato semántico preservado

`FACT` Lo que el cambio preserva, punto por punto (verificado en §9–§16, no
razonado solamente):

| Elemento | Cómo se preserva |
|---|---|
| **contenido de la observación** | se pasa el mismo objeto que `iterate()` habría computado (`MEASURED`: 83/83 pares previos con digest idéntico) |
| **orden lógico de operaciones** | la secuencia de métodos que reciben una observación es **idéntica** antes y después (`MEASURED`: 46/46 y 30/30 tests) |
| **no-progress guard** | sigue comparando `observation.governance_fingerprint()` contra el de la iteración anterior, ambos pre-acción (`host.py:1051`/`1063-1066`); el fingerprint no cambia de semántica |
| **condiciones de terminación** | `STOP_MAX_ITERATIONS`, `STOP_NO_PROGRESS`, terminales de derivación: sin cambios (`MEASURED`: journal idéntico) |
| **excepciones** | `observe()` sigue siendo el primer acto de la iteración en `run()`; una falla se detecta igual, sólo una vez en vez de dos |
| **valores de retorno** | `run()` → `HostRun`; `iterate()` → el registro del journal (`MEASURED`: journal byte-equivalente) |
| **efectos sobre journal** | `MEASURED`: **115 → 115** registros en los 152 dominantes; **58 → 58** en las suites SAE; contenido idéntico tras normalizar campos no deterministas |
| **SAE / autonomy** | `MEASURED`: 56 → 56 registros con bloque `autonomy` no nulo; el gate sigue corriendo en `iterate` antes de `_execute_delegation` |
| **transiciones de estado** | el orden `observa → deriva → autoriza → actúa → graba` queda intacto; lo único que desaparece es una lectura repetida del mismo estado |
| **acción ejecutada** | `MEASURED`: misma acción y misma rationale en cada registro del journal |
| **validaciones** | `MEASURED`: 1542 passed, 1 skipped (mismos conteos antes y después) |

### 7.1 Aclaración importante sobre lo que el piloto **no** elimina

`FACT` El piloto elimina la segunda **`observe()`**, **no** el segundo
`derive_next_action`. `run()` deriva en `host.py:1055` (para el guard) e
`iterate()` deriva otra vez en `host.py:593` (para actuar). Esa segunda
derivación **permanece**, y eso es correcto: `derive_next_action` es una función
pura (`derivation.py` no importa `store`, no escribe, no lanza subprocesos), su
costo es de milisegundos, y la auditoría semántica ya lo había registrado como
"duplicación de cálculo, no de lectura".

`MEASURED` Consecuencia: **el conteo de consumos por método es idéntico antes y
después** (`derive_next_action` 166 → 166, `_apply_autonomy_gate` 86 → 86,
`_record` 111 → 111, etc.). Lo que baja son las **lecturas del mundo**, no las
derivaciones. Quien lea este informe no debe esperar que el número de consumos
baje.

---

## 8. Tests enfocados

`MEASURED` Tests directamente relacionados con `ExecutionHost.run()`,
`iterate()`, `observe()`, no-progress guard, journal, SAE/autonomy,
lifecycle/terminación y el camino modificado:

| Conjunto | Comando | Antes | Después |
|---|---|---|---|
| 4 archivos dominantes (152) | `pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q` | **152 passed** (276.59 s) | **152 passed** (225.62 s) |
| Suites SAE con gate activo (173) | `pytest tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py tests/test_autonomous_scope.py tests/test_sae_scope_enforcement_dogfood.py tests/test_autonomy_effects_dogfood.py -q` | **173 passed** (120.98 s) | **173 passed** (106.73 s) |
| Camino modificado, test por test | los 46 tests que corren el host, comparados uno a uno | — | **sin diferencias** (§9–§13) |

`FACT` **No se aceptó "PASS" como evidencia suficiente.** La pregunta del pedido
—*¿el sistema conserva exactamente las garantías que existían antes de eliminar
la segunda observación?*— se respondió con la comparación observacional de §9–§13,
no con el resultado de pytest.

---

## 9. Resultados de los 152 tests

`MEASURED` Igual que en el baseline: **mismo comando, mismo conjunto, misma
máquina**.

```text
                        antes        después      delta
tests                   152          152          +0
passed                  152          152          +0
failed                    0            0          0
errors                    0            0          0
runtime                 276.59 s     225.62 s     −50.97 s (−18.4 %)
observe() calls         444          358          −86 (−19.4 %)
subprocesos de observe  2777         2242         −535 (−19.3 %)
journal records         115          115          +0
```

`FACT` La instrumentación corrió en ambos lados con el **mismo** plugin
(`-p pilot_trace`), de modo que la comparación es simétrica:

```text
                        antes (BEFORE.json)   después (AFTER.json)
runtime trace           234.82 s              203.40 s
observe() calls         444                   358
subprocesos de observe  2777                  2242
derive calls            166                   166
tests con traza         46                    46
```

---

## 10. Resultado de la suite canónica

`MEASURED` Ambos legs (`tests/` + `protocol/.agents/harness/tests/`), mismo
comando, condiciones equivalentes:

| Corrida | Resultado | Wall |
|---|---|---|
| **ANTES** (`git stash` del cambio) | 1542 passed, 1 skipped | **318.33 s** |
| **DESPUÉS** | 1542 passed, 1 skipped | **292.37 s** |
| referencia de la autopsia, mismo commit (máquina más cargada) | 1542 passed, 1 skipped | 413.95 s |
| `tests/` solo, antes | 1357 passed, 1 skipped | 341.91 s |
| `tests/` solo, después | 1357 passed, 1 skipped | 292.37 s (leg completo en 292.37) |

`FACT` `test_count`, `passed`, `skipped`, `failed`, `errors`: **idénticos** en
todas las parejas. Delta de runtime del par simétrico: **−25.96 s (−8.2 %)**.
`FACT` **Ese delta está dentro del ruido de esta máquina** (dos corridas del
mismo código variaron 42 s; §4). Ver §15 para la conclusión honesta.

`FACT` No se declaró éxito basándose sólo en los tests dominantes: la suite
canónica completa se ejecutó antes y después.

---

## 11. Observaciones antes/después

`MEASURED` Conteo global y por sitio.

```text
MISMA CORRIDA (152 dominantes)      antes   después   delta
observaciones totales                 444       358      −86   (−19.4 %)
  sitio 591 (iterate)                  86         0      −86   ← el duplicado
  sitio 1050 (run)                     87        87        0
  sitio 769                              5         5        0
  sitio 807                              1         1        0
  sitio 822                              1         1        0
  sitio 852                              1         1        0
  sitio 870                             45        45        0
  sitio 872                             45        45        0
  sitio 974                             16        16        0
  sitio 1089                            24        24        0
  sitio 1117                            50        50        0
  sitio 1154                            50        50        0
  sitio 1287                            29        29        0
  fuera de host.py                       4         4        0
```

`MEASURED` Mismo patrón en las suites SAE (gate activo):

```text
observaciones totales                 254       213      −41   (−16.1 %)
  sitio 591                            41         0      −41   ← el duplicado
  todos los demás                      213       213        0
```

`FACT` **La verificación decisiva del pedido** ("desaparezca solamente la
observación duplicada; no deben desaparecer observaciones de otros caminos"):
el delta es **exactamente** el número de llamadas del sitio 591 (86 y 41
respectivamente) y **ningún otro sitio cambia** (0 en los 12 restantes).
`MEASURED` `removed site calls == observation delta` → **True** en ambos conjuntos.

`FACT` **Prueba directa de que las dos observaciones eran la misma**: en el
baseline, cada iteración derivó dos veces desde observaciones distintas en el
código; los 83 pares consecutivos de `derive_next_action` recibieron un payload
con **digest byte-idéntico**:

```text
pares de derive consecutivos:                        83
  con observación BYTE-IDÉNTICA en ambos:            83   (100 %)
  con observación distinta:                           0
consumidores aguas abajo con el mismo digest:        83
  discrepancias:                                      0
SECOND_OBSERVATION_RETURNED_IDENTICAL_STATE = YES  (83/83)
```

`FACT` Los digests se comparan **dentro de una misma corrida** (mismo proceso,
mismo repositorio desechable), por lo que la igualdad es concluyente y no
depende de normalización alguna.

---

## 12. Subprocesses antes/después

`MEASURED` Subprocesos lanzados **dentro de `observe()`** (los únicos que la
eliminación puede afectar):

```text
                           antes   después   delta
152 dominantes              2777      2242     −535   (−19.3 %)
suites SAE (gate activo)    1557      1306     −251   (−16.1 %)
```

`FACT` Costo unitario medido en la auditoría semántica: **6 subprocesos y
~0.33 s por `observe()`** con el repositorio de fixture. La aritmética cierra:
`86 × 6 = 516` y `41 × 6 = 246`, próximos a las reducciones observadas (535 y
251); la diferencia se debe a que el conteo real por llamada no es siempre 6
(depende del número de archivos del `content_scope_set`).

`FACT` **No se asumió un ahorro proporcional**: se midió. La reducción de
subprocesos es robusta y reproducible (es un conteo, no un tiempo).

---

## 13. Runtime antes/después

`MEASURED` Todas las corridas de los 152 dominantes, en orden cronológico:

| # | Condición | Código | Wall |
|---|---|---|---|
| 1 | aislado, sin instrumentación | antes | 276.59 s |
| 2 | aislado, sin instrumentación | después | 225.62 s |
| 3 | traza, con instrumentación | antes | 277.27 s |
| 4 | traza, con instrumentación | después | 226.33 s |
| 5 | traza (instrumentación final) | antes | 234.82 s |
| 6 | traza (instrumentación final) | después | 203.40 s |
| 7 | traza (instrumentación final) | antes | 233.78 s |
| 8 | traza (instrumentación final) | **después** | 202.44 s |
| 9 | traza (instrumentación final) | **después** | 202.76 s |

`FACT` Agrupando por código, con instrumentación equivalente:

```text
ANTES   (traza): 277.27, 234.82, 233.78        mediana 234.82
DESPUÉS (traza): 226.33, 203.40, 202.44, 202.76  mediana 203.40
                                        diferencia de medianas: −31.4 s (−13.4 %)
```

`MEASURED` Suite canónica completa (ambos legs), par simétrico:
**318.33 s → 292.37 s (−25.96 s, −8.2 %)**.

`FACT` **Pero la varianza de esta máquina es del mismo orden**: dos corridas del
**mismo** código de los 152 tests dieron **276.59 s y 234.82 s (−15 %)**. Con
una sola réplica por lado, **no es posible atribuir el delta al cambio con
confianza estadística**. Ver §19.

---

## 14. Journal antes/después

`MEASURED` Comparación de los registros de journal capturados por test.

```text
                               153 dominantes        suites SAE
tests comparados                     46                  30
journal idéntico                     46/46 (100 %)       30/30 (100 %)
registros totales                 115 → 115           58 → 58
```

`FACT` La comparación **no acepta diferencias porque los tests no las
detecten**: compara el contenido serializado de cada registro, campo por campo
(incluido el bloque `observed` completo, la `rationale`, `evidence_refs`,
`authority`, `stop_reason`, `gate_signals`, `validation_signals`, `notes`,
`delegation_id`, `result_id`, `result_status`).

`FACT` Normalizaciones aplicadas, declaradas explícitamente (nada más):
1. `run_id` / `created_at` — llevan timestamp;
2. `git.head` / `git_head` — el repo desechable se reconstruye con uuid nuevo,
   así que el SHA del commit cambia entre dos corridas del **mismo** código;
3. `state_identity` / `current_state_identity` / `checkpoint_tree` /
   `closure_tree` — son **tree ids**, y el tree incluye el blob del plan, que
   lleva el timestamp de la corrida.
4. rutas de scratch de sesión.

`FACT` **No se normalizaron las identidades de *delta***
(`delta_identity`, `current_delta_identity`): están acotadas al contenido
declarado, con el plan excluido por contrato (`observation.py:1013-1028`), por lo
que son deterministas y una diferencia real de contenido habría aparecido a
través de ellas. Que coincidan es evidencia positiva, no un efecto de la
normalización.

---

## 15. SAE / autonomy antes/después

`MEASURED` Con el gate activo (`autonomy_gate=True`), suites
`test_sae_scope_enforcement.py`, `test_autonomy_effects.py`,
`test_autonomous_scope.py` y los dos dogfood:

```text
                                     antes   después   delta
tests                                  173       173        0
passed                                 173       173        0
wall                              120.98 s  106.73 s   −14.25 s
observaciones                          254       213      −41
  sitio 591                             41         0      −41
subprocesos de observe                1557      1306     −251
registros de journal                    58        58        0
  con bloque `autonomy` no nulo         56        56        0
derive calls                            82        82        0
journal idéntico                          —   30/30 (100 %)
```

`FACT` **El gate realmente se ejerció** (no es un camino vacío): 56 de 58
registros llevan un bloque `autonomy` no nulo, con la proyección de checkpoint y
el veredicto de la frontera. `MEASURED` El contenido de esos bloques es
**idéntico** antes y después.

`FACT` Además, el contrato de forma que el dogfood fija por texto sigue
satisfecho: `test_autonomy_effects_dogfood.py:146-151` exige que
`def _apply_autonomy_gate` aparezca **antes** de `def _execute_delegation` y que
existan los literales `_autonomy_effects(action.kind, observation)` y
`resource_required=_autonomy_consumes_delegation(action.kind)`. El piloto **no
tocó ninguna de las tres cosas** (el gate se sigue invocando desde `iterate`
antes de `_execute_delegation`) y ese test pasa.

---

## 16. No-progress guard antes/después

`FACT` Este punto era **crítico** para el pedido, porque es una de las razones
por las que `run()` necesita observar.

`FACT` Semántica del guard, sin cambios:

```text
host.py:1051   fingerprint = observation.governance_fingerprint()
host.py:1062   if not action.terminal:
host.py:1063-1066   if previous_kind == action.kind
                       and previous_fingerprint == fingerprint:
host.py:1067-1079       no_progress_action(...) -> _record -> append -> break
host.py:1080-1081   previous_kind = action.kind
                    previous_fingerprint = fingerprint
```

`FACT` El `fingerprint` se computa sobre la observación de `1050`, **pre-acción**,
igual que antes; `previous_fingerprint` viene de la iteración anterior, cuyo
valor también era pre-acción. **La comparación sigue siendo entre dos
fingerprints pre-acción de iteraciones distintas** — que es exactamente lo que
la hace válida.

`MEASURED` Verificación:

```text
fingerprint source line          1050 (antes) -> 1060 (después)   [no se movió de run()]
pares de derive consecutivos     83 -> 83
governance_fingerprint()         método puro; no cambió
salidas por no-progress          ejercitadas en el baseline y en la suite
test dedicado                    tests/test_autonomous_orchestrator.py::
                                 test_no_progress_guard_stops_instead_of_spinning → PASS
journal idéntico                 46/46 tests (incluye el registro del guard)
```

`FACT` El test dedicado al guard (que monkeypatchea `derive_next_action` para
forzar el caso) pasa, y su registro de journal es idéntico al del baseline.

---

## 17. Diferencias encontradas

`FACT` **Ninguna diferencia funcional.** Se detectaron y resolvieron **cinco
diferencias del método de comparación** (no del sistema), que se documentan
porque un lector debe poder reproducir el razonamiento y porque dos de ellas
casi produjeron un falso veredicto:

| # | Diferencia observada | Causa real | Resolución |
|---|---|---|---|
| D-1 | 42/46 journals "diferían" en `git_head` | el repo desechable se reconstruye con uuid nuevo ⇒ SHA distinto entre corridas del **mismo** código | normalizar `git.head` (N1a) |
| D-2 | 1/46 journals difería en `current_state_identity` | es un **tree id**; el tree incluye el blob del plan, que lleva el timestamp | normalizar `state_identity`/`checkpoint_tree`/`closure_tree` (N1b) |
| D-3 | el digest de las observaciones no coincidía entre corridas | mi `_digest` normalizaba `head` en el nivel superior, pero en el payload está anidado en `{"git": {"head": ...}}` | la comparación intra-corrida (que no necesita normalización) pasó a ser la prueba primaria |
| D-4 | la secuencia de consumos parecía diferir (13 → 11) | el conteo de consumos **no debe** bajar: el piloto elimina la segunda *lectura*, no el segundo *derive* (§7.1) | corregir la expectativa y la herramienta |
| D-5 | `derive_next_action` no se registraba en algunas corridas | `test_max_iterations_is_an_explicit_stop` hace `monkeypatch.setattr` sobre `derive_next_action`, **sobrescribiendo** el parche del plugin | documentado; no afecta al resultado (el test pasa y su journal es idéntico) |

`FACT` Las tres primeras son **ruido del entorno de test**, no del cambio:
`D-1` y `D-2` varían entre dos corridas del mismo código. `D-4` y `D-5` son
errores de mi instrumentación, corregidos antes de emitir el veredicto.

`FACT` **No se adaptó ningún test para aceptar un comportamiento nuevo**, y no
se ocultó ninguna diferencia: las cinco están listadas arriba.

---

## 18. Diferencias descartadas

`FACT` Descartadas por evidencia, con su justificación:

| Diferencia | Veredicto | Evidencia |
|---|---|---|
| `git_head` distinto entre corridas | **ruido del fixture** | el repo es `_scratch(name-uuid4)`; dos corridas del **mismo** código dan SHA distintos |
| `state_identity` / `checkpoint_tree` / `closure_tree` distintos | **ruido del fixture** | son tree ids que incluyen el blob del plan; el plan contiene el timestamp de corrida |
| `delta_identity` / `current_delta_identity` | **NO es ruido** — coincidieron exactamente | están acotadas al contenido declarado (plan excluido); se dejaron sin normalizar a propósito |
| conteo de consumos por método | **sin cambio por diseño** | el piloto no elimina la segunda derivación (§7.1) |
| `derive_next_action` no registrado en 2 tests | **artefacto de la instrumentación** | esos tests monkeypatchean la función; `grep` confirma los dos sitios |
| el delta de runtime | **dentro del ruido** | ver §13/§19 |
| `test_check_lifecycle_*`, `test_scoped_content_identity`, etc. | **fuera del alcance** | no pasan por `iterate()`; su runtime no se tocó |

---

## 19. Medidas vs estimaciones

`FACT` Distinción explícita, como exige el pedido.

```text
MEASURED
  · observaciones: 444 -> 358 (−86) y 254 -> 213 (−41)
  · subprocesos dentro de observe(): 2777 -> 2242 (−535) y 1557 -> 1306 (−251)
  · el delta de observaciones es EXACTAMENTE el del sitio 591; 0 en los otros 12
  · journal: 115 -> 115 y 58 -> 58 registros; contenido idéntico 46/46 y 30/30
  · bloques `autonomy` no nulos: 56 -> 56, contenido idéntico
  · 83/83 pares con observación byte-idéntica en el baseline
  · secuencia de consumos idéntica 46/46 y 30/30
  · 152 / 173 / 1542 tests: mismos passed/skipped/failed antes y después
  · wall clock de cada corrida (nueve corridas, tabla en §13)
  · varianza de la máquina: 276.59 s vs 234.82 s para el MISMO código

ESTIMATED
  · ninguna cifra de ahorro de runtime se presenta como medida atribuible.
    La reducción de subprocesos (medida) implica una reducción de tiempo
    (los subprocesos son ~97 % del costo de observe()), pero cuánto de eso
    aparece en el wall clock total no quedó aislado.
  · "~0.33 s por observación eliminada": derivado de medir observe() (0.380 s
    de mediana) y del costo de subproceso (0.367 s) — es aritmética, no una
    medición del ahorro de suite.

INFERRED
  · que en Linux/CI el ahorro absoluto sea mayor o menor (todas las cifras son
    Windows; el costo dominante es creación de procesos)
  · que los otros dos pares de duplicación (870→872, 1154→1287→1117) sean
    igualmente seguros. La auditoría semántica los dejó fuera y este piloto
    NO los investigó: sólo midió que siguen intactos.

UNKNOWN
  · el ahorro real de wall clock atribuible al cambio, con la varianza de esta
    máquina y una sola réplica por lado
```

### 19.1 La lectura honesta del rendimiento (`FACT` + `INFERENCE`)

`FACT` El cambio elimina una lectura del mundo real por iteración. Eso es
**conteo**, y el conteo bajó: **−19.4 % de observaciones, −19.3 % de subprocesos**
en los 152 dominantes.

`FACT` El tiempo de pared **bajó en todas las parejas medidas**, pero la
magnitud (8 %–18 %) **no es separable del ruido** con los datos disponibles:
dos corridas del mismo código variaron 15 %.

`INFERENCE` El ahorro de tiempo **existe** (menos trabajo real ejecutado) pero
**no está cuantificado con confianza**. Presentar "18.4 %" como resultado sería
presentar como medido algo que no lo está.

---

## 20. Riesgos

`FACT` Riesgos evaluados tras el experimento, con su estado.

| # | Riesgo | Estado tras el piloto | Severidad residual |
|---|---|---|---|
| R-1 | cambio de producción en la pieza más cargada de garantías | **mitigado**: 1542 tests PASS, journal byte-equivalente, 0 diferencias funcionales | BAJA |
| R-2 | cambio externo concurrente entre las dos lecturas | **sin cambios**: no hay hilos ni modelo concurrente declarado; el riesgo ya existía (la ventana era de código puro) | BAJA |
| R-3 | enmascarar una mutación futura introducida en esa ventana | **mitigado parcialmente**: la precondición quedó **documentada en la docstring de `iterate()`**; el invariante I-2 la cubre | MEDIA — es el riesgo que sobrevive |
| R-4 | `iterate()` deja de ser autocontenido | **materializado, es la decisión pendiente** (2.3). Sin consumidores afectados hoy | MEDIA |
| R-5 | el ahorro no se materializa | **el conteo se materializa; el tiempo no está aislado** | MEDIA |
| R-6 | propagar el cambio a los otros dos pares | **no se hizo**; siguen intactos (medido) | NINGUNA |
| R-7 | creer que es seguro "porque parece obvio" | **evitado**: el veredicto no es `SAFE_TO_REFACTOR` | NINGUNA |
| R-8 | interacción con el gate SAE | **verificado con el gate activo**: 56 bloques `autonomy` idénticos, 173 tests PASS | BAJA |
| R-9 | interacción con el no-progress guard | **verificado**: mismo fingerprint, mismo punto de comparación, test dedicado PASS | BAJA |
| R-10 | `ObservationError` en un momento distinto | **sin cambios observables**: sigue detectándose en `run()`, sólo una vez | MUY BAJA |

`INFERENCE` El riesgo residual se concentra en **R-3** (una mutación futura en
esa ventana quedaría enmascarada) y **R-4** (la propiedad de forma perdida).
Ninguno de los dos es un defecto actual; ambos son condiciones que deben
**decidirse y documentarse** si el piloto se consolida.

---

## 21. Impacto sobre el contrato de `iterate()`

`FACT` Antes:

```python
def iterate(self, iteration: int) -> dict[str, Any]:
    """Run exactly one iteration and return its journal record."""
    observation = self.observe()
```

`FACT` Después:

```python
def iterate(self, iteration: int, observation: ChangeObservation) -> dict[str, Any]:
    """...``observation`` is the reading of the change taken at the start of
    this iteration, before any write..."""
```

`FACT` Consumidores afectados:

```text
callers de iterate() en el repositorio            1  (host.py:1093, run())
callers en tests                                  0
callers en el CLI                                 0
subclases de ExecutionHost                        0
overrides de iterate()                            0
iterate en __all__ de runtime/orchestrator         NO
documentos que declaren su FIRMA                  0
documentos que mencionen "invocado desde iterate" 4
  (runtime/README.md:331, ADR-19:162, plan 138:592/621, plan 159:40/65)
  → describen DÓNDE corre el gate, no la firma; siguen siendo exactos
```

`INFERENCE` **Ninguna ruptura de compatibilidad real.** Lo que cambia es una
**propiedad de forma**: `iterate()` deja de ser invocable sin contexto y pasa a
exigir que su caller le entregue el estado.

`INFERENCE` **¿Es el cambio mínimo, o hay una alternativa menos invasiva?**
Evaluado en la auditoría semántica (§18) y reconfirmado aquí:

| Alternativa | Veredicto |
|---|---|
| `iterate(iteration, observation)` — lo implementado | **el cambio mínimo real**: 1 línea, 1 firma, 1 call site |
| `iterate(iteration, observation=None)` con `observe()` de fallback | **rechazado**: un parámetro opcional que cambia cuántas veces se lee el mundo real según el caller es exactamente la ambigüedad que el repo evita (`AGENTS.md`, *Decision-Making Compass*); además un solo caller no necesita dos formas |
| cache / memoria en el host | **rechazado**: viola el invariante "el host no tiene estado entre iteraciones" (política §1/§9) |

`FACT` El pedido advierte: *"No introducir abstracciones solamente para preservar
una API que actualmente no tiene consumidores"* — no se introdujo ninguna.

`INFERENCE` **Pero la decisión excede lo puramente local en un sentido**: aceptar
que `iterate()` reciba la observación es aceptar que la unidad autocontenida pasa
a ser `run()`, no `iterate()`. Es una decisión de arquitectura **pequeña pero
real**, y es la razón por la que el resultado es `SAFE_TO_KEEP_EXPERIMENT` y no
`SAFE_TO_REFACTOR`.

---

## 22. Decisión final

```text
RESULT = SAFE_TO_KEEP_EXPERIMENT
```

`INFERENCE` Justificación, contra las cinco categorías posibles:

**No es `ROLLBACK`.** La equivalencia funcional **se demostró**:
- journal idéntico en 46/46 y 30/30 tests, campo por campo, después de
  normalizar sólo campos que varían entre corridas del mismo código;
- 0 deltas inesperados en los 13 sitios de observación;
- 83/83 pares de observación byte-idéntica en el baseline;
- 152 / 173 / 1542 tests PASS con los mismos conteos;
- SAE con el gate activo: 56 bloques `autonomy` idénticos;
- no-progress guard: mismo fingerprint y mismo punto de comparación;
- ninguna diferencia funcional encontrada.

**No es `KEEP_CURRENT`.** La optimización **sí aporta**:
- elimina 86 observaciones (−19.4 %) y 535 subprocesos (−19.3 %) en los 152
  dominantes, y 41 / 251 en las suites SAE;
- es un cambio de 1 línea efectiva, sin cache, sin estado, sin abstracciones;
- el delta es exactamente el duplicado: ningún otro camino pierde una lectura;
- el riesgo residual es acotado y está identificado (R-3, R-4).

**No es `SAFE_TO_REFACTOR`.** El propio pedido prohíbe elegirlo "solamente porque
el cambio parece obvio", y hay dos razones concretas:
1. **`iterate()` cambia de forma** (R-4). Es una decisión de contrato que debe
   tomarse explícitamente, no consolidarse por inercia.
2. **El beneficio de rendimiento no está aislado del ruido** (R-5). El ahorro
   estructural está medido; el de wall clock, no.

**No es `NEEDS_DESIGN`.** No falta una decisión arquitectónica mayor: el
invariante de la política ya está satisfecho, el cambio es de una línea y no hay
consumidores que romper. Lo que falta es una decisión de contrato acotada y mejor
medición de tiempos.

**Es `SAFE_TO_KEEP_EXPERIMENT`**: el experimento es correcto, está verificado y
aporta valor **medible** (en observaciones y subprocesos), pero consolidarlo
requiere una decisión arquitectónica explícita sobre la firma de `iterate()`.

---

## 23. Rollback realizado o no

```text
ROLLBACK = NO
```

`FACT` El cambio se conserva en el árbol de trabajo **sin commit**. Motivo: la
equivalencia funcional está verificada y el criterio de rollback del pedido
(§14) no se activó en ninguno de sus puntos:

```text
cambio funcional no explicado .................. no ocurrió
cambio de acción ............................... no ocurrió (journal idéntico)
cambio de excepción ............................ no ocurrió
cambio del no-progress guard ................... no ocurrió
cambio de estado no explicado .................. no ocurrió
cambio relevante en journal .................... no ocurrió
cambio relevante en SAE/autonomy ............... no ocurrió
pérdida de una observación necesaria ........... no ocurrió (sólo se perdió el duplicado)
dependencia oculta de iterate() sobre observe()  no apareció
violación de Plan 145 .......................... no ocurrió
necesidad de estado persistente/cache/memoria .. no apareció
necesidad de tocar los otros pares ............. no apareció
necesidad de modificar tests .................... no apareció
el cambio dejó de ser local .................... no ocurrió (1 línea efectiva)
```

`FACT` Reversión trivial disponible: restaurar las dos líneas. El cambio está
**sin commitear**, de modo que revertirlo no requiere reescribir historia.

---

## 24. Siguiente paso recomendado

`RECOMMENDED` **Una sola acción**: decidir si `iterate()` pasa a recibir la
observación como argumento (la decisión de contrato de §21). Es la única cosa que
bloquea la consolidación; todo lo demás ya está verificado.

`FACT` Si la decisión es **sí**, queda un paso de verificación de forma, no de
semántica: repetir la comparación de journal con **más réplicas de wall clock**
para aislar el ahorro de tiempo del ruido de máquina (mínimo 3 corridas por lado
del conjunto dominante, misma sesión), y volver a correr la batería canónica
completa antes del commit atómico.

`FACT` Si la decisión es **no**, el piloto se revierte y no se pierde nada: el
hallazgo estructural (que la segunda observación devolvía un estado idéntico en
83/83 casos) ya quedó registrado y es evidencia reutilizable.

`RECOMMENDED` **No propagar a los otros dos pares** (`870→872`,
`1154→1287→1117`) en ningún caso como parte de este trabajo: la auditoría
semántica los dejó fuera, este piloto sólo midió que siguen intactos, y tienen
contexto semántico distinto (uno está en un camino condicional, el otro atraviesa
`write_run_report`).

---

## 25. Apéndice — Reproducibilidad

`FACT` Todo lo necesario para repetir el razonamiento.

### 25.1 Comandos

```powershell
# Baseline de los 152 dominantes (código original)
git stash push -- runtime/orchestrator/host.py
python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
    tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q `
    -p no:cacheprovider --durations=0 --durations-min=0

# Traza instrumentada (el plugin vive fuera del árbol)
$env:PYTHONPATH="<dir>"; $env:PILOT_JSON="<dir>\BEFORE.json"
python -m pytest <los 4 archivos> -q -p no:cacheprovider -p pilot_trace

git stash pop

# Lo mismo con el cambio aplicado -> AFTER.json

# Suites SAE con el gate activo
python -m pytest tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py `
    tests/test_autonomous_scope.py tests/test_sae_scope_enforcement_dogfood.py `
    tests/test_autonomy_effects_dogfood.py -q -p no:cacheprovider -p pilot_trace

# Suite canónica completa (ambos legs)
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider

# Verificaciones
python check_window.py BEFORE.json          # 83/83 pares byte-idénticos
python compare.py BEFORE.json AFTER.json    # sitios + estructura + journal
python verify.py                            # recuento agregado por método
```

### 25.2 Qué prueba cada verificación

| Verificación | Pregunta que responde | Resultado |
|---|---|---|
| `check_window.py BEFORE` | ¿las dos observaciones del baseline devolvían el mismo estado? | **83/83 idénticas** |
| `compare.py` §1 | ¿desapareció **sólo** el sitio 591? | **sí; 0 deltas en los otros 12** |
| `compare.py` §3 | ¿la estructura de consumos es idéntica? | **46/46** |
| `compare.py` §3 | ¿el journal es idéntico? | **46/46** (y 30/30 en SAE) |
| `compare.py` §5 | ¿los otros dos pares siguen intactos? | **45/45, 50/50, 29/29 sin cambio** |
| `verify.py` | ¿los consumos agregados por método cambian? | **no** (coherente con §7.1) |

### 25.3 Limitaciones declaradas (`UNKNOWN`)

```text
· Varianza alta: 276.59 s vs 234.82 s para el MISMO código. Una réplica por
  lado no permite aislar el ahorro de wall clock. → hace falta más réplicas.
· Todas las mediciones son de Windows 11 (creación de procesos cara).
· El costo interno de cada subproceso `python tools/*.py` no se midió.
· No se investigaron los otros dos pares de observaciones.
· La instrumentación de `derive_next_action` es interferida por los 2 tests que
  la monkeypatchean; no afecta al veredicto (esos tests pasan y su journal es
  idéntico).
```

---

*Fin del informe del piloto. 1 archivo de producción modificado
(`runtime/orchestrator/host.py`, +12 −2); 0 tests modificados; 0 cambios de CI,
dependencias, `protocol/`, `dist/`, `ROADMAP.md` ni `docs/adr/`. La
instrumentación vivió fuera del árbol versionado y fue eliminada.*

---

# CONSOLIDACIÓN — 2026-10-14 (ejecución posterior)

`FACT` **Sección aditiva.** El informe anterior queda **sin reescribir**: es la
traza del piloto tal como se ejecutó. Esta sección registra la **verificación
incremental por gates** que consolidó el cambio, ejecutada después.

```text
PILOT = ACCEPTED
CONTRACT = iterate(iteration, observation)
SEMANTIC_EQUIVALENCE = VERIFIED
REGRESSION = NONE
PERFORMANCE = CONFIRMED  (ver G5; en el piloto había quedado ESTIMATED/UNKNOWN)
FULL_SUITE = PASS
```

## C.1 Método: gates incrementales

`FACT` No se usó la suite completa como herramienta de diagnóstico (§REGLA
PRINCIPAL del pedido). Se ejecutaron gates locales primero:

```text
G1 = PASS   inspección estructural
G2 = PASS   tests focales de ExecutionHost
G3 = PASS   SAE / autonomía / no-progress
G4 = PASS   verificación estructural de la optimización (instrumentación temporal)
G5 = PASS   performance: 3 réplicas BASE / 3 CANDIDATE alternadas — EFFECT = CONFIRMED
G6 = PASS   batería canónica completa
```

## C.2 G1 — Inspección estructural (`MEASURED`)

```text
firma            iterate(self, iteration: int, observation: ChangeObservation)
self.observe()   12 sitios; el de iterate() ya no existe
callers de iterate(               1  (host.py:1093)
callers en tests / CLI            0 / 0
subclases de ExecutionHost        0
overrides de iterate()/observe()  0
iterate en __all__                NO
pares fuera de alcance            870→872 (ahora 880/882) · 1154→1287→1117
                                  (ahora 1164/1297/1127): presentes, intactos
cache / lru_cache / estado        ninguno (grep sin coincidencias)
áreas protegidas modificadas      0 (protocol/, dist/, ROADMAP.md, docs/adr/, tests/)
```

## C.3 G2 — Tests focales (`MEASURED`)

```text
7 tests (run/iterate/observe/journal/no-progress/max_iterations/restart/
         observation_is_read_only/closed_derivation)   7 passed  35.61 s
tests/test_autonomous_orchestrator.py completo         31 passed  67.27 s
```

## C.4 G3 — SAE / autonomía / no-progress (`MEASURED`)

```text
5 suites SAE (scope, effects, autonomous_scope, 2 dogfood)  173 passed  117.55 s
test_autonomy_effects_dogfood.py (contrato de forma del gate por texto)
                                                             13 passed    3.24 s
```

`FACT` El gate sigue invocándose desde `iterate` **antes** de
`_execute_delegation`, que es lo que el dogfood fija por texto.

## C.5 G4 — Verificación estructural de la optimización (`MEASURED`)

`FACT` Instrumentación **temporal y no versionada** (fuera del árbol; eliminada
al finalizar). Se midió el **candidato** (código sin cambios posteriores) y se
comparó contra el baseline del piloto:

```text
                              152 dominantes        suites SAE
observaciones                 358                   213
  baseline del piloto (AFTER) 358                   213        → coincide exacto
subprocesos dentro de observe 2242                  1306
  baseline del piloto (AFTER) 2242                  1306       → coincide exacto
sitio 591 (iterate)            ausente               ausente
sitio 1060 (run)               87 llamadas           41 llamadas → coincide
pares fuera de alcance         880/882=45,45         880/882=21,21
                               984=16, 1099=24,      1127=36, 1164=36, 1297=35
                               1127=50, 1164=50,     (todos presentes)
                               1297=29
atributos de observación
  ganados por la instancia     0                     0            → sin memoria persistente
iterate() invocaciones         86                    41
  recibiendo un digest
  producido en el sitio
  de observe() de run()        86/86 = 100 %         41/41
```

`FACT` **Verificación (4) del pedido — "la observación recibida por `iterate()`
corresponde a la observación calculada por `run()` en el mismo frame lógico"**:
las 86 invocaciones de `iterate()` en los 152 dominantes reciben un digest que
fue producido en el **sitio propio de `run()`** (`host.py:1060`), con **0
violaciones**.

`FACT` **Verificación (5) — "no se introdujo memoria persistente"**: se comparó,
por invocación, la lista de atributos de la instancia que contienen "observ"
antes y después de `iterate()`. **0 atributos ganados**, en ambos conjuntos.

## C.6 G5 — Performance (`MEASURED`)

`FACT` Seis corridas de los 152 dominantes, **3 BASE y 3 CANDIDATE
alternadas** (BASE, CAND, BASE, CAND, BASE, CAND) en la misma sesión. El cambio
se aplicó/revirtió con `git stash` para que BASE fuese exactamente el código de
HEAD.

| Réplica | BASE | CANDIDATE | delta | delta % |
|---|---:|---:|---:|---:|
| 1 | 268.22 s | 222.52 s | **+45.70 s** | +17.04 % |
| 2 | 275.52 s | 201.27 s | **+74.25 s** | +26.95 % |
| 3 | 228.21 s | 193.13 s | **+35.08 s** | +15.37 % |

```text
                  BASE      CANDIDATE
n                  3           3
mínimo         228.21 s    193.13 s
máximo         275.52 s    222.52 s
media          257.32 s    205.64 s
mediana        268.22 s    201.27 s
desv. estándar  25.47 s     15.17 s
rango           47.31 s     29.39 s

delta medio            = +51.68 s   (+20.08 %)
delta mediano          = +45.70 s
delta desv. estándar   =  20.26 s
```

`FACT` **Las dos distribuciones no se solapan**: el máximo del candidato
(222.52 s) es menor que el mínimo del baseline (228.21 s), con un hueco de
5.69 s. El candidato fue más rápido en **las tres** réplicas pareadas.

`FACT` Pruebas estadísticas exactas (n = 3 por lado, 20 particiones posibles):

```text
permutación exacta, una cola:  p = 0.0000  (0 de 20 particiones tan extremas)
Mann-Whitney U exacto:         U = 9 de 9  (el candidato gana todos los pares)
                               valor crítico (n=3,3, α=0.05) = 9  → significativo
```

`FACT` **El tamaño del efecto (51.68 s) es mayor que el rango intra-condición de
ambos grupos** (47.31 s y 29.39 s), que era exactamente la condición que el
piloto no había podido satisfacer con una sola réplica por lado.

```text
EFFECT = CONFIRMED
```

`FACT` **Esto corrige el estado del piloto**, donde el ahorro quedó declarado
como no atribuible. Con tres réplicas alternadas el efecto se separa del ruido.

## C.7 G6 — Batería canónica completa (`MEASURED`)

```text
comando                                     resultado
python -m pytest tests/                     1357 passed, 1 skipped   298.06 s
python -m pytest protocol/.../harness/tests/ 185 passed                 7.18 s
combinado (legs sumados)                    1542 passed, 1 skipped
check_protocol_invariants.py  EXIT=0        216 files, 10476 references verified
check_plan_citations.py       EXIT=1        ver C.7.1
check_plan_structure.py       EXIT=0        sin violaciones estructurales
check_taxonomy_coherence.py   EXIT=0        OK
check_session_artifacts.py    EXIT=0        OK
check_version_state.py        EXIT=0        OK
check_lifecycle_anchor (C-1)  EXIT=0        VALID=72, GAP=0, ANOMALY=0
check_lifecycle_checkpoint(C-2) EXIT=0      VALID=71, GAP=1, ANOMALY=0
check_lifecycle_lineage  (C-3) EXIT=0       VALID=37, GAP=0, ANOMALY=0
check_ears_coverage.py        EXIT=0        N/A=1, VALID=3
check_discovery_output.py     EXIT=0        N/A=1
```

### C.7.1 Fallo clasificado: `check_plan_citations.py` — **categoría C (no relacionado, preexistente)**

`FACT` Salida:

```text
Legacy references from live sources: 1
- docs/CONVENTIONS.md:808 -> `.agents/policies/validation-closure.md` [new legacy reference]
```

`FACT` Evidencia de que es **preexistente y no relacionado**:
1. el archivo señalado es `docs/CONVENTIONS.md`, que **no fue tocado** por este
   trabajo (`git diff --name-only -- docs/CONVENTIONS.md` → vacío); su último
   commit es `4c5bfcb`, muy anterior;
2. **con `host.py` revertido a HEAD** (`git stash`), el checker **falla
   idénticamente** con el mismo exit 1 y el mismo mensaje ⇒ el fallo **no lo
   introduce el cambio**;
3. la salida **no menciona `host.py` ni `runtime/orchestrator/`** (grep vacío);
4. es un fallo documental de citas legacy, no de código de host.

`FACT` **No se tocó.** El pedido indica expresamente no modificarlo
innecesariamente (categoría C). Queda registrado, no corregido.

## C.8 Estado de gates y consolidación

```text
GATE_STATUS

G1 = PASS
G2 = PASS
G3 = PASS
G4 = PASS
G5 = PASS     (EFFECT = CONFIRMED)
G6 = PASS     (batería canónica verde; 1 fallo preexistente clasificado en C.7.1)

CURRENT_GATE = CONSOLIDATED
NEXT_ACTION  = commit atómico
```

`FACT` Contrato aceptado formalmente, **sin** parámetro opcional, **sin**
fallback interno a `self.observe()`, **sin** cache y **sin** estado persistente:

```python
iterate(iteration: int, observation: ChangeObservation) -> dict[str, Any]
```

`FACT` Intención preservada:

```text
run()
  └── observe once
       ├── no-progress guard
       └── iterate(iteration, observation)
             └── derive/action
```

## C.9 Resumen de la consolidación

```text
OBSERVATIONS_BEFORE = 444   (152 dominantes)   |  254 (SAE)
OBSERVATIONS_AFTER  = 358                      |  213
OBSERVATION_DELTA   = −86 (−19.4 %)            |  −41 (−16.1 %)

SUBPROCESSES_BEFORE = 2777                     |  1557
SUBPROCESSES_AFTER  = 2242                     |  1306
SUBPROCESS_DELTA    = −535 (−19.3 %)           |  −251 (−16.1 %)

PERFORMANCE_BASE_MEDIAN      = 268.22 s
PERFORMANCE_CANDIDATE_MEDIAN = 201.27 s
PERFORMANCE_DELTA            = −66.95 s (−25.0 %) sobre medianas
                               −51.68 s (−20.08 %) sobre medias
EFFECT                       = CONFIRMED

FULL_SUITE = 1542 passed, 1 skipped
OTHER_DUPLICATES_TOUCHED = NO
```
