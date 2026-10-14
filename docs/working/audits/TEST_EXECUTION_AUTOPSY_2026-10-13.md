# TEST EXECUTION AUTOPSY — 2026-10-13

```text
RESULT = TEST_EXECUTION_AUTOPSY
CLASS  = Working / Audit (provenance) — NO normativo
BRANCH = dev   HEAD = fb0786a0b9b872796e5e4b223cf92bc011c22139
SCOPE  = los 4 archivos dominantes de tests/ + su producción + la suite completa
         como baseline. Ninguna modificación funcional, de test, de CI o de
         dependencias.
```

**Clase documental:** Working / Audit (provenance) — **no normativo** (RFC-69,
`docs/AGENTS.md`).
**Naturaleza:** autopsia de ejecución `READ_ONLY`, orientada a establecer un
baseline cuantitativo reutilizable.
**Autoridad de este documento:** ninguna. Registra hechos, mediciones,
inferencias y recomendaciones. No crea mecanismos, no modifica la suite, no
autoriza trabajo, no decide política de testing y no reduce la batería
canónica.
**Relación con las auditorías previas:** este documento **continúa**
`TEST_SUITE_AUDIT_2026-10-13.md` (estrategia y costo) y
`TEST_ARCHITECTURE_AUDIT_2026-10-13.md` (estructura y niveles). No repite sus
inventarios; resuelve la incógnita que ambas dejaron explícitamente abierta
(*"¿qué compone realmente esos ~282 s?"*) y lleva la descomposición hasta el
nivel de operación (subprocess, git, filesystem, waits) con medición directa.

**Marcas usadas en todo el documento**

| Marca | Significado |
|---|---|
| `OBSERVED` | leído directamente en el árbol (código, documentos) |
| `MEASURED` | obtenido ejecutando la suite o un micro-benchmark en esta máquina |
| `INFERRED` | conclusión derivada de hechos/mediciones, no observada directamente |
| `ESTIMATED` | extrapolación aritmética declarada como tal |
| `RECOMMENDED` | propuesta de acción, **no implementada** |
| `UNKNOWN` | no determinado; se declara en lugar de suponerse |

**Instrumentación temporal.** Toda la instrumentación de esta auditoría vivió
**fuera del árbol versionado**, en `%TEMP%\argentos-autopsy\` (plugin de
conteo, scripts de medición y datos crudos), y fue eliminada al terminar. El
estado final del repositorio no contiene cambios funcionales (§27 y §37).

---

## 1. Executive Summary

`MEASURED` **La suite completa (1543 tests, 2 legs) corrió en 413.95 s**;
`1542 passed, 1 skipped`. Fase `call` 407.82 s, `setup` 1.36 s, `teardown`
0.00 s.

`MEASURED` **Los 4 archivos dominantes (152 tests = 9.9 % de la suite)
consumen 298.03 s = 73.1 % del tiempo de fase `call`.** Son, verificadas las
rutas reales:

```text
tests/test_autonomous_orchestrator.py    31 tests   105.20 s
tests/test_agent_worker.py               41 tests    79.86 s
tests/test_sae_scope_enforcement.py      44 tests    58.31 s
tests/test_autonomy_effects.py           36 tests    54.66 s
                                        152 tests   298.03 s   (73.1 %)
```

`MEASURED` **El costo NO es el montaje del repositorio Git.** Medido en
aislamiento (n=8 por constructor): `build_repo` 0.277 s / `make_repo` 0.424 s /
`build_repo` SAE 0.413 s / `build_repo` autonomía 0.413 s. Con los sitios de
llamada contados en el código (**22 + 27 + 13 + 18 = 80 construcciones**), el
montaje total de los cuatro archivos es **30.31 s = 12.5 %** de su runtime, y
sólo **7.3 %** en el archivo más caro. Esto **confirma la sospecha de la
segunda auditoría** (`C-1`: "el resto del costo es ejecución real del host") y
**refuta la estimación de −52 %** del primer informe.

`MEASURED` **Lo que domina el reloj es la creación de procesos.** Con un plugin
externo de conteo (`subprocess.run` instrumentado, sin modificar el repo) la
corrida completa ejecutó **4.944 subprocesos** que consumieron **332.54 s de
tiempo de reloj** — el **80.3 %** del wall clock. Dentro de los 4 archivos
dominantes: **3.775 subprocesos = 239.67 s = 99 % de su tiempo `call`**.

`MEASURED` **La relación entre subprocesos y tiempo es prácticamente
determinista: r = 0.999** (n = 152 tests, pendiente ≈ **63 ms por
subproceso**). Un test de estos archivos no tarda por su lógica: tarda
`n_subprocesos × ~63 ms`.

`MEASURED` **No existe ni un solo `sleep`, `poll`, `retry` ni espera
artificial** en producción ni en los tests de estos archivos (grep exhaustivo:
el único `timeout=` es el parámetro de `subprocess.run` con valor por defecto
120 s, y nunca se alcanza). **La categoría `WAITS` está vacía.** La lentitud
aparente de "espera" es en realidad **latencia de creación de procesos en
Windows**: 63 ms por `git`, 37 ms por intérprete Python.

`MEASURED` **Todo el costo está en el cuerpo del test.** Cero subprocesos en
fase `setup` y cero en `teardown`; **4.944 de 4.944** ocurren en la fase `call`.
No hay fixtures costosas que optimizar: en estos cuatro archivos el
"setup" es código del cuerpo del test (`build_repo(...)`), no una fixture de
pytest, y por eso ninguna fase de pytest lo revela.

`MEASURED` **La variabilidad entre corridas es mínima; la variabilidad entre
contextos es grande.** Tres corridas aisladas de los 4 archivos: 242.86 s,
242.96 s, 243.18 s (dispersión < 0.2 %). La mediana del coeficiente de
variación por test es **0.003 (0.3 %)**. Sin embargo, los **mismos 152 tests**
costaron **298.03 s dentro de la corrida completa** (R1) — un **+23 %** frente
a su ejecución aislada. `INFERRED`: el baseline debe declarar el contexto.

`MEASURED` Distribución (`call`, 1486 nodos con duración registrada): mediana
0.000 s, p75 0.02 s, p90 0.46 s, p95 1.12 s, p99 6.77 s, máx 21.35 s. **778
tests por debajo de 0.01 s.** El top 1 % de los tests (15) explica el 38.0 %
del tiempo; el top 5 % (75) el 78.8 %.

`OBSERVED` **Causa mecánica identificada en producción**: `ExecutionHost.run()`
llama a `self.observe()` (`host.py:1050`) y a continuación llama a
`self.iterate()`, que **vuelve a llamar a `self.observe()`** (`host.py:591`).
Cada `observe()` medido cuesta **0.380 s y 6 subprocesos** (`git rev-parse` ×2,
`git status`, `git ls-files`, `git write-tree`, git interno). La observación se
repite además dentro de `_execute_delegation` (`host.py:769/807/822/852/870/872`).
`MEASURED`: una sola llamada `host.run(max_iterations=1)` = **2 iteraciones,
49 subprocesos, 2.99 s**.

`INFERRED` **El costo es mayoritariamente legítimo, pero una parte sustancial
es arquitectónicamente evitable sin perder ninguna garantía.** La garantía que
estos tests protegen (evidencia real, efecto real, journal real) exige *alguna*
ejecución real; lo que no exige es **re-observar el mismo estado inmutable 3–8
veces por iteración** ni **lanzar 3 comandos git donde 1 devuelve la misma
información**.

`RECOMMENDED` La conclusión de arquitectura de ejecución **no es reducir la
suite**: es (a) **de-duplicar la observación dentro del host** (cambio de
producción, sin tocar un solo assert) y (b) **consolidar los tests cuya
evidencia es idéntica o tautológica**. Las dos palancas están cuantificadas en
§20 y §21.

---

## 2. Scope

`OBSERVED` **Dentro del alcance:**

- los 4 archivos dominantes identificados por la auditoría previa, **con rutas
  verificadas** (§3);
- el código de producción que esos tests ejercitan
  (`runtime/orchestrator/{host,worker,observation,agent_worker,autonomy,
  derivation,contracts,store,authority,governance}.py`,
  `tools/scoped_content_identity.py`);
- la infraestructura de tests que los gobierna (`conftest.py`,
  `tests/pytest_isolation.py`, `tests/AGENTS.md`);
- la suite completa como **baseline** (una corrida completa + una corrida
  instrumentada);
- los documentos de restricción aplicables (`AGENTS.md`, `docs/AGENTS.md`,
  `docs/plans/145-integral-dev-backlog-closure.md`, `docs/VERSIONING.md` §4.1).

**Fuera del alcance (deliberadamente):**

- los otros 65 archivos de test, salvo cuando aportan comparación de baseline
  (permanecen cubiertos por las dos auditorías previas);
- el leg del harness del producto (`protocol/.agents/harness/tests/`), que esta
  autopsia sólo mide como agregado para el baseline;
- cualquier propuesta de cambio de política de selección de tests: ya tratada
  en `TEST_SUITE_AUDIT_2026-10-13.md` §11–§13.

### 2.1 Archivos y versiones consultados (`OBSERVED`)

| Documento | Rol en esta auditoría |
|---|---|
| `AGENTS.md` (raíz) | carta del workspace DEV; separación DEV/Protocol |
| `docs/AGENTS.md` | taxonomía documental; clase Working/Audit |
| `tests/AGENTS.md` | reglas de `tests/`; **conjunto anclado** (18 filas) |
| `docs/plans/145-integral-dev-backlog-closure.md` | **restricción arquitectónica** (§4) |
| `docs/plans/INDEX.md` | localización de Plan 145 (serie 76) |
| `docs/VERSIONING.md` §4.1 | definición de la batería canónica |
| `docs/working/audits/TEST_SUITE_AUDIT_2026-10-13.md` | baseline previo (costo/estrategia) |
| `docs/working/audits/TEST_ARCHITECTURE_AUDIT_2026-10-13.md` | baseline previo (estructura/niveles) |
| `docs/working/audits/INDEX.md` | registro de working docs |
| `conftest.py`, `tests/pytest_isolation.py` | aislamiento por sesión (Plan 145, I-1) |

`OBSERVED` Plan 145 se localizó por el mecanismo documental existente
(`docs/plans/INDEX.md` → serie 76 → fila `145-integral-dev-backlog-closure.md`),
no por suposición de ruta.

### 2.2 Cómo se localizó e interpretó Plan 145

`OBSERVED` El índice de planes lo registra como **Sextuagésima sexta serie:
cierre integral del backlog accionable DEV `I-1`…`I-8` (Plan 145) (21 sep 2026)**,
fila `145-integral-dev-backlog-closure.md`, status `Executed`, vía plan,
DEV-only. El documento declara `**RFC:** —` y `**Clase:** —` porque no toca
`protocol/.agents/`.

---

## 3. Prior Audit Findings

### 3.1 Lo que ya estaba establecido (`OBSERVED` en los dos informes previos)

```text
WHAT WAS KNOWN
  · la suite tiene 1543 tests (1358 DEV + 185 harness) y corre en ~400 s
  · 9 archivos que construyen repos Git reales = 85.6 % del tiempo
  · 20 archivos son estructuralmente MIXED
  · ~152 tests de 4 archivos concentran ~282–298 s (70–75 % del call time)
  · el primitivo git init+add+commit ≈ 0.340 s (medición previa)
  · setup 1.71 s y teardown 0.01 s: las fixtures NO son el problema
  · no hay duplicación literal; el solapamiento es por ejes ortogonales
  · la cobertura del orquestador es baja y eso es estructural, no un defecto
  · el régimen ANCHORED (20 archivos) no es seleccionable por path
```

### 3.2 Lo que quedó explícitamente sin resolver

```text
WHAT WAS UNKNOWN  (declarado por las auditorías previas)
  · ¿qué compone realmente esos ~282 s? (Anexo B, pregunta 1)
  · ¿cuánto es montaje y cuánto es ejecución del host? (C-1, C-2)
  · ¿el Plan 145 permite reutilizar el montaje del repositorio? (Anexo B, p. 2)
  · ¿cuántos subprocesos lanza cada archivo/test? (no medido)
  · ¿existe espera/polling/sleep? (no buscado)
  · ¿el costo es estable o variable entre corridas? (no medido)
```

### 3.3 Lo que esta auditoría resuelve

```text
WHAT THIS AUDIT RESOLVES
  · la descomposición del runtime por operación (subprocess/git/fs/waits)
  · el conteo exacto de subprocesos por archivo y por test, y su costo
  · la separación medida setup vs ejecución (12.5 % vs 87.5 %)
  · la ausencia total de waits artificiales (categoría vacía, probada)
  · la causa mecánica en producción: observación duplicada por iteración
  · la correlación r = 0.999 entre subprocesos y tiempo
  · la variabilidad intra-corrida (< 0.4 %) y la de contexto (+23 %)
  · la lectura de Plan 145 frente a la reutilización de montaje (§4)
```

### 3.4 Lo que sigue sin resolverse (`UNKNOWN`)

Ver §35. En resumen: el costo real en Linux/CI (todas las cifras son de
Windows), el número exacto de iteraciones de cada test sin ejecutarlo, y si
`runtime/orchestrator/__main__.py` merece cobertura.

---

## 4. Plan 145 Constraints

`OBSERVED` Esta sección es la que el pedido exige como **restricción
arquitectónica real**, no como contexto decorativo.

### 4.1 Qué decidió Plan 145 sobre aislamiento

| Decisión | Texto/efecto observado | Fuente |
|---|---|---|
| **Scratch por sesión, no compartido** | el scratch root pasó de **compartido** a **propio de cada sesión**; una sesión limpia sólo su propio directorio | Plan 145, matriz `I-1`; `conftest.py:32-49,118-127`; `tests/pytest_isolation.py:35-56,237-252` |
| **Token declarado, nunca adivinado** | el token se genera en import time desde entropía independiente y se exporta por entorno para que un hijo **adopte** su sesión | `conftest.py:80-87`; `tests/pytest_isolation.py:107-159` |
| **Una sesión sin token se RECHAZA** | no hay fallback a un directorio compartido | `tests/pytest_isolation.py:148-154` |
| **Poda acotada por edad** | 24 h, un `stat` por vecino, nunca por presencia; una sesión viva nunca es candidata | `tests/pytest_isolation.py:79-89,270-306` |
| **Causa raíz declarada** | en 7 corridas completas, 4 fallaron, cada una en un test **distinto**, porque cada inicio de sesión hacía `rmtree` sobre el scratch compartido | Plan 145, §Problema 1 |
| **Falsación exigida** | 12 regresiones nuevas fallaron contra la implementación anterior y pasan contra la nueva; 127 tests corrieron sin interferencia junto a 3 sesiones concurrentes | Plan 145, `## Nota de ejecución` |

### 4.2 Qué restringe eso para esta auditoría

`OBSERVED` Plan 145 **no prohíbe** nombrar la reutilización de montaje; lo que
hace es **eliminar la clase de arreglo que introdujo el defecto**: compartir
estado mutable de scratch entre sesiones (y, por extensión, entre tests). Las
restricciones operativas que se derivan y que esta auditoría respeta son:

```text
R-145-1  Un test no puede heredar el estado mutable de otro test.
         (El scratch compartido fue la causa raíz declarada del no-determinismo.)

R-145-2  La propiedad del scratch es de la SESIÓN, declarada, no inferida.
         (Un path compartido por conveniencia está excluido por diseño.)

R-145-3  La limpieza es por edad y acotada; nada se elimina por inferencia.
         (Una "plantilla" persistente entre corridas cae bajo esta regla.)

R-145-4  La corrección de aislamiento tiene regresión propia y falsación.
         (tests/test_pytest_isolation.py es la guarda del régimen.)
```

`INFERRED` **Consecuencia directa para cualquier propuesta de optimización:**
una plantilla de repositorio **creada una vez y copiada por test** no viola
R-145-1 (cada test recibe su propio árbol, físicamente distinto, sin estado
compartido); un repositorio **pre-inicializado y reutilizado in situ** sí lo
viola, porque dos tests mutarían el mismo objeto git. Esta auditoría **no
propone ninguna de las dos** (§20, §22) y, cuando menciona la copia, la marca
expresamente como tensión a resolver antes de implementar.

`INFERRED` Además, el patrón `scratch_root(<suite>) + uuid4()` que los cuatro
archivos usan (`_scratch` en los cuatro) **ya cumple R-145-1 y R-145-2**:
cada test obtiene un directorio propio con nombre único bajo el scratch de su
sesión. El costo no viene de que el aislamiento esté mal: viene de que **cada
test paga el precio completo de construir su mundo y luego lo observa muchas
veces más de lo necesario**. Optimizar la observación **no toca el aislamiento**
y por lo tanto **no está en tensión con Plan 145**.

---

## 5. Measurement Methodology

`OBSERVED` Todo lo medido en este informe se obtuvo con los comandos siguientes.
Las cifras son de **esta máquina** y **este** checkout.

### 5.1 Entorno (`OBSERVED`)

```text
OS            Windows 11 (OneDrive como carpeta de proyecto)
Python        3.14.3   (C:\Program Files\Python314\python.exe)
pytest        9.0.3
CPU lógicos   12
git CLI       presente
%TEMP%        C:\Users\rolda\AppData\Local\Temp (fuera de OneDrive)
```

`OBSERVED` Coincide con los `Environmental factors` que Plan 145 declaró
(`Windows 11 + PowerShell; Python 3.14.3; pytest 9.0.3; git presente`), lo que
hace las cifras comparables con ese registro.

### 5.2 Baseline (R1) — corrida canónica intacta

```powershell
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider `
    --durations=0 --durations-min=0
# → 1542 passed, 1 skipped in 413.95 s   (setup 1.36 s, teardown 0.00 s, call 407.82 s)
```

`OBSERVED` Se usó `-p no:cacheprovider` (como la segunda auditoría) para que la
corrida no escribiera caché; el único skip es el de `cacheprovider`.

### 5.3 Conteo de subprocesos (R2) — instrumentación externa

`OBSERVED` Plugin **fuera del árbol versionado**, cargado por `-p` con
`PYTHONPATH` apuntando a `%TEMP%\argentos-autopsy\`. Envuelve
`subprocess.run` para contar y cronometrar, y atribuye los conteos a cada test
mediante `pytest_runtest_setup/call/teardown`. **Nunca altera el
comportamiento**: el `subprocess.run` original siempre se invoca y su valor de
retorno (y sus excepciones) se propaga intacto. No escribe nada en el repo.

```powershell
$env:PYTHONPATH="…\argentos-autopsy"; $env:AUTOPSY_JSON="…\instr_full.json"
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider -p autopsy_plugin
```

`MEASURED` Resultado: **4.944 subprocesos, 332.54 s de subproceso, wall 359.37 s
(1542 passed)**. `OBSERVED` El wall de R2 es **menor** que el de R1 (359 vs
414 s) pese a la instrumentación: `INFERRED`, carga de máquina (R1 corrió
mientras esta auditoría leía código y lanzaba otros procesos). La
**discrepancia se declara** y por eso el baseline usa R1 para el tiempo y R2
**sólo para conteos y proporciones**, que son robustos.

### 5.4 Micro-benchmarks

```powershell
python measure_builders.py   # constructores puros, n=8 cada uno + primitivas
python measure_observe.py    # observe() x1 y ExecutionHost.run(max_iterations=1)
```

`OBSERVED` Ambos scripts construyen el mundo con **el propio builder de la
suite** (importado tal cual) para que lo medido sea exactamente lo que el test
hace, y miden en el scratch externo de la sesión.

### 5.5 Variabilidad (V1–V3)

```powershell
1..3 | % { python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
    tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q `
    --durations=0 --durations-min=0 }
# → 242.86 s / 242.96 s / 243.18 s
```

### 5.6 Análisis estático

`OBSERVED` Lectura completa de los 4 archivos (1158 + 1092 + 1081 + 801 =
4.132 líneas) y del código de producción que ejercitan, con conteo de sitios de
llamada a constructores de repositorio, de `host.run()`, de iteraciones y de
aserciones inertes. **La ubicación del archivo no se usó como criterio de
clasificación.**

### 5.7 Qué puede y qué no puede medirse directo (`OBSERVED`)

| Magnitud | Cómo se obtuvo | Calidad |
|---|---|---|
| runtime por test | `pytest --durations=0` | `MEASURED` directo |
| setup/teardown de pytest | `pytest --durations` | `MEASURED` directo (y = ~0) |
| cantidad de subprocesos por test | plugin externo | `MEASURED` directo |
| tiempo en subprocesos por test | plugin externo (wall del hijo) | `MEASURED` directo |
| comandos git/python exactos | clasificador del plugin | `MEASURED` directo |
| costo del constructor puro | micro-benchmark n=8 | `MEASURED` directo |
| costo de `observe()` | micro-benchmark n=3 | `MEASURED` directo |
| divisiones **dentro** de un subproceso (p. ej. lo que un `python tools/...` hace por dentro) | no instrumentado | `UNKNOWN` |
| CPU vs wall por test | no instrumentado (sólo CPU total en la previa) | `UNKNOWN` |
| tiempo de recolección | `--collect-only` (0.48 s + 0.09 s) | `MEASURED` directo |
| cuánto de los 282–298 s es "montaje" vs "ejecución" | constructor medido + conteo de sitios | `MEASURED` (montaje) / `INFERRED` (resto) |

`OBSERVED` **Ninguna categoría de este informe se presenta como medición si fue
estimada.** Las que son `ESTIMATED` o `INFERRED` están marcadas una por una.

---

## 6. Current Baseline

`MEASURED` Baseline canónico de esta auditoría (2026-10-13, `dev @ fb0786a`):

```text
CANONICAL_TEST_COUNT      1543  (1358 DEV + 185 harness)
CANONICAL_RUNTIME         413.95 s  (02:53.95 → 0:06:54)
  fase call               407.82 s
  fase setup                1.36 s
  fase teardown             0.00 s
  recolección               0.57 s  (0.48 + 0.09, aparte)

DOMINANT_FILES                    tests / runtime / % del call
  tests/test_autonomous_orchestrator.py    31  105.20 s  25.8 %
  tests/test_agent_worker.py               41   79.86 s  19.6 %
  tests/test_sae_scope_enforcement.py      44   58.31 s  14.3 %
  tests/test_autonomy_effects.py           36   54.66 s  13.4 %
                                  TOTAL   152  298.03 s  73.1 %

PERCENTAGE_OF_RUNTIME_FROM_TOP_FILES   73.1 % del call / 72.0 % del wall

TOP_TEST_RUNTIME        21.35 s  test_revalidation_is_recorded_as_a2_without_mutating_a1
P95_TEST_RUNTIME         1.12 s
P99_TEST_RUNTIME         6.77 s
MEDIAN_TEST_RUNTIME      0.000 s
MAX_TEST_RUNTIME        21.35 s
```

### 6.1 Estadísticos de distribución (`MEASURED`, 1486 nodos con duración)

| Estadístico | Valor |
|---|---:|
| n | 1486 de 1543 (57 por debajo de la resolución del reporte) |
| total `call` | 407.82 s |
| media | 0.274 s |
| **mediana** | **0.000 s** |
| p75 | 0.02 s |
| p90 | 0.46 s |
| **p95** | **1.12 s** |
| p99 | 6.77 s |
| máx | 21.35 s |
| tests < 0.01 s | **778** |
| tests ≥ 1 s | 87 (suma 334.09 s) |

### 6.2 Concentración (`MEASURED`)

| Corte | Tests | % tests | s | % del call |
|---|---:|---:|---:|---:|
| top 1 % | 15 | 1.0 % | 154.88 | 38.0 % |
| top 5 % | 75 | 5.0 % | 321.24 | 78.8 % |
| top 10 % | 149 | 10.0 % | 379.17 | 93.0 % |
| top 4 archivos | 152 | 9.9 % | 298.03 | 73.1 % |
| resto (1334 tests) | 1334 | 86.2 % | ~109.79 | 26.9 % |

`OBSERVED` Comparación con las auditorías previas: 290.5 s/75.3 % (informe
1), 282.18 s/70.2 % (informe 2), 298.03 s/73.1 % (esta). `INFERRED` Las tres
coinciden dentro del ruido de máquina: **el sujeto medido no cambió y el
baseline es estable entre auditorías.**

### 6.3 Totales operacionales (`MEASURED` vía plugin)

```text
TOTAL_SUBPROCESSES        4.944        (DEV 4.917 + harness 27)
  de los cuales git       4.696  (95.0 %)
  de los cuales python      245  ( 5.0 %)
  otros                       3
TOTAL_SUBPROCESS_TIME     332.54 s     (80.3 % del wall)
TOTAL_GIT_OPERATIONS      4.696
TOTAL_WAITS                   0        (no existe ningún sleep/poll/retry)
TOTAL_SETUP_TIME            1.36 s     (fase setup de pytest)
TOTAL_SUBPROCESSES_EN_SETUP    0
TOTAL_SUBPROCESSES_EN_TEARDOWN 0
TOTAL_EXECUTION_TIME      407.82 s     (fase call; todo el subprocess vive aquí)
TOTAL_CLEANUP_TIME          0.00 s
```

### 6.4 Desglose exacto de subprocesos por comando (`MEASURED`)

```text
git rev-parse      1790     python check_ok.py                60
git ls-files        989     python check_lifecycle_lineage.py 55
git status          590     python check_lifecycle_checkpoint.py 30
git write-tree      551     python scoped_content_identity.py 24
git add             199     python check_lifecycle_anchor.py  21
git commit          189     python check_ears_coverage.py     13
git init            161     python hook_gate.py                9
git config          122     python (14 comandos más, ≤5 c/u)  ~29
git diff             57     OTROS (no git/python)              3
git hash-object      24
git checkout          8
git branch/tag/otros  6
```

`INFERRED` `git rev-parse` (1790) es el comando más lanzado de toda la suite: se
debe a que `git_state()` ejecuta **dos** `rev-parse` (HEAD y `--abbrev-ref`) más
un `status` por invocación (`observation.py:129-131`), y a que `observe()` se
invoca repetidamente (§7.3). `git write-tree`/`ls-files`/`hash-object` (1564 en
conjunto) provienen de `scoped_content_identity.compute`, que se llama **una vez
por `observe()`** (`observation.py:1029-1033`).

---

## 7. Runtime Decomposition

### 7.1 La descomposición pedida (`MEASURED` + `INFERRED` declarado)

```text
TOTAL (wall, 2 legs)                        413.95 s   MEASURED
├── collection                                0.57 s   MEASURED  (0.1 %)
├── fixture/setup (pytest)                    1.36 s   MEASURED  (0.3 %)
│   └── repository/Git setup                    0.00 s MEASURED  (0 subprocesos)
├── subprocess creation + execution         332.54 s   MEASURED  (80.3 %)
│   ├── git                                  ~310 s   MEASURED (4.696 × ~66 ms)
│   └── python interpreter starts            ~9.1 s   MEASURED (245 × 37 ms)
├── producción en proceso (lógica, hashing,
│   parseo, journal, escritura de artefactos) ~72 s  INFERRED  (resto del wall)
├── filesystem (mkdir/write/read dentro de
│   los tests y del host)                     incluido arriba  INFERRED
├── waits / polling / sleep                     0.0 s   MEASURED  (no existe)
├── assertions                          no separable    UNKNOWN
├── cleanup (teardown)                         0.00 s  MEASURED  (0 subprocesos)
└── other/unclassified (arranque de pytest,
    import de módulos, reporte)               ~7.5 s   INFERRED
```

`OBSERVED` **Cómo se obtuvo cada fila, sin inventar nada:**

- **collection**: `--collect-only` = 0.48 s (DEV) + 0.09 s (harness). `MEASURED`.
- **fixture/setup**: `pytest --durations=0` agrega 1.36 s de fase `setup`.
  **Cero subprocesos** en esa fase (medido por el plugin): el setup de pytest
  NO construye repositorios.
- **subprocess**: el plugin mide el wall de cada `subprocess.run` y lo suma:
  332.54 s. `MEASURED` directo, no estimado.
- **producción en proceso**: `INFERRED` por diferencia (wall − subprocess −
  collection − setup − arranque). **Es la fila menos precisa y se declara.**
- **waits**: `MEASURED` = 0. Es una afirmación fuerte y está respaldada por
  grep exhaustivo (§11).
- **assertions**: `UNKNOWN`. Separar el tiempo de aserción exigiría
  instrumentación por línea dentro del intérprete, que no se hizo.
- **cleanup**: `MEASURED` 0.00 s con 0 subprocesos.

`OBSERVED` **El hallazgo estructural más importante de esta sección:** en estos
archivos, lo que la intuición llama "fixture" (construir el repositorio) **no es
una fixture de pytest**: es código del cuerpo del test. Por eso la fase `setup`
mide 0.00 s y todo el montaje aparece dentro de `call`. Cualquier política que
optimice "fixtures de pytest" es irrelevante aquí.

### 7.2 Descomposición por archivo dominante (`MEASURED`)

| Archivo | tests | call R1 | call aislado | subproc | tiempo subproc | % subproc | montaje (medido) | % montaje |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `test_autonomous_orchestrator.py` | 31 | 105.20 s | 83.25 s | 1.303 | 81.11 s | **97.4 %** | 6.08 s | 7.3 % |
| `test_agent_worker.py` | 41 | 79.86 s | 60.00 s | 912 | 59.86 s | **99.8 %** | 11.44 s | 19.1 % |
| `test_sae_scope_enforcement.py` | 44 | 58.31 s | 55.28 s | 878 | 53.70 s | **97.1 %** | 5.37 s | 9.7 % |
| `test_autonomy_effects.py` | 36 | 54.66 s | 43.49 s | 682 | 45.00 s | **103 %**† | 7.43 s | 17.1 % |
| **TOTAL** | **152** | **298.03 s** | **242.02 s** | **3.775** | **239.67 s** | **99.0 %** | **30.31 s** | **12.5 %** |

† `MEASURED` El tiempo de subproceso de `test_autonomy_effects.py` (45.00 s)
supera ligeramente su wall aislado (43.49 s) porque el subproceso se midió en
la corrida **completa** (R2, contexto más lento) y el wall aislado en V1–V3.
`INFERRED`: es la manifestación del efecto de contexto de §16, no un error de
medición.

`OBSERVED` **El cociente setup/ejecución es 1:8 en el peor caso
(`test_agent_worker.py`) y 1:13 en el mejor (`test_autonomous_orchestrator.py`).**
La respuesta a la pregunta fundamental del pedido —*"¿estamos pagando mucho para
preparar un escenario cuya acción bajo prueba realmente cuesta muy poco?"*— es:
**al revés.** La acción bajo prueba (el host conduciendo el loop, observando
git, hasheando contenido, lanzando los gates) **es** lo caro; el escenario es
barato. Lo que hay que atacar **no es el montaje**: es **cuántas veces la acción
bajo prueba re-observa el mismo estado inmutable**.

### 7.3 La causa mecánica del costo, medida (`MEASURED` + `OBSERVED`)

```text
observe() x1                            0.3804 s   6 subprocesos
  git rev-parse ×2 · git status ×1 · git ls-files ×1 · git write-tree ×1 · git interno ×1

ExecutionHost.run(max_iterations=1)     2.9874 s   49 subprocesos   2 iteraciones
  git rev-parse ×21 · git ls-files ×10 · git status ×9
  git write-tree ×7 · git diff ×1 · python ×1
```

`OBSERVED` **El defecto estructural**: en `run()` (línea 1050) se observa, y en
la línea siguiente se llama a `iterate()`, que **observa de nuevo** (línea 591).
La primera observación se usa **sólo** para el fingerprint de no-progreso
(`host.py:1051,1063-1066`); la segunda produce el trabajo real. Cada iteración
paga así **dos** observaciones completas, y `_execute_delegation` añade más
(`host.py:769/807/822/852/870/872`).

`INFERRED` Cuantificación: si una iteración cuesta ~1.5 s y una observación
0.38 s, **la observación de descarte representa ≈ 25 % de la iteración** en el
camino de ejecución, y un porcentaje mayor en los caminos de *stop* (donde la
iteración no hace nada más que observar y grabar). Sobre los 152 tests, un
`ESTIMATED` conservador de una sola línea de código de producción eliminada es
**del orden de 40–70 s de la suite** — pero **esta auditoría no ejecuta el
cambio y por lo tanto lo marca como `ESTIMATED`, no `MEASURED`.**

---

## 8. Dominant File Analysis

### 8.1 `tests/test_autonomous_orchestrator.py`

`OBSERVED` 1158 líneas, **31 tests**, `call` 105.20 s (R1) / 83.25 s (aislado),
**1.303 subprocesos / 81.11 s**, mediana por test 3.394 s, **7.3 % de montaje**.

**Qué es.** Tests de comportamiento del **DEV Autonomous Orchestrator**
(`runtime/orchestrator/`) sobre un **repositorio git real por test**
(`build_repo`, línea 230). El docstring lo declara (líneas 1-14): *"a throw-away
git repository is built per test and the host really observes it, really
delegates, really executes commands and really writes records... They
deliberately do not use pytest's `tmp_path`"*.

**Estructura real (por comportamiento, no por nombre):**

| Grupo | Tests | Repo | Host | Nivel real |
|---|---:|---|---|---|
| Derivación y stops puros sobre repo (`RUN_VALIDATION`, entry, pending, findings, autorización) | 5 | sí | no | COMPONENT |
| Autoridad/vocabulario puro (release, unknown action, records) | 3 | no | no | UNIT |
| Contrato `WorkerAdapter` por `ast` + `inspect.signature` | 3 | no | no | CONTRACT |
| Clasificación de comandos y gates (exit code vs publicado, environmental, gate sin línea) | 3 | sí | no | COMPONENT / INTEGRATION |
| Contrato M4 y persistencia | 3 | sí (1) | no/sí (2) | CONTRACT / INTEGRATION |
| **Loop completo, A2, restart, no-progress, max-iterations** | **5** | sí | **sí (11 `run()`)** | **INTEGRATION / E2E** |
| Observación (read-only, repo ilegible, git ausente, git_state) | 4 | sí/no | no | COMPONENT |

`OBSERVED` **22 de 31 tests construyen un repositorio; 9 no.** 11 llamadas a
`host.run()` en 9 tests. `MEASURED` Las iteraciones reales (sonda instrumentada)
son **mayores que las del código aparente**: el "full loop" corre **7
iteraciones** (no 5), porque `RUN_LIFECYCLE_GATES` dispara dos veces por una
re-lectura de `gate_signals` vacíos en el registro del journal; `max_iterations=N`
produce **N+1** registros por el `else` de `host.py:1088-1096`.

**Garantías de mayor valor (conservar):**

- `test_full_loop_derives_closed_from_real_evidence` — `Closed` derivado de un
  anchor y un checkpoint **reales** que concuerdan (`closure_tree ==
  anchor.state_identity`, `consistency_pass`), con las tres escrituras de
  gobernanza persistidas en el plan. **CRITICAL**.
- `test_revalidation_is_recorded_as_a2_without_mutating_a1` — A2 preserva A1
  (identidad de estado y de delta), con `revalidated=True`. **CRITICAL**.
- `test_restart_reconstructs_and_continues_without_lost_continuity` —
  continuidad de numeración de iteración a través de **instancias nuevas** de
  host. **CRITICAL**.
- `test_checker_classification_is_read_and_not_inferred_from_exit_code` — el
  signal viene de la línea publicada por el checker, **no** del exit code;
  incluye el contraejemplo (exit 0 + `ANOMALY`). **CRITICAL**, exclusivo.
- `test_no_progress_guard_stops_instead_of_spinning` — guard de terminación.
  **HIGH**.
- `test_unreadable_repository_is_an_error_not_a_false_absent_state` — regresión
  del incidente de Plan 145 (I-1). **HIGH**, exclusivo.

**Defectos de test observados (`OBSERVED`):**

| Línea | Defecto | Lectura |
|---|---|---|
| 988 | `len(journal_after) == len(journal_before) + run.iterations` | **tautológico**: `HostRun.iterations` **se define** como `len(records)` (`host.py:1103`), así que es `x == x` |
| 1097-1098 | `assert "Released=sí" not in text` | **no puede fallar**: el host renderiza `Released=False` fijo (`host.py:1180`) |
| 731 | `assert rendered == ["delegation"]` | casi vacuo: re-afirma lo que el helper acaba de parsear |
| 1028 | `assert run.iterations <= 3` | holgado: `MEASURED` son 2; debería ser `== 2` |
| 1153 | `test_git_state_reports_the_cli_availability_explicitly` | lee el **repo real** y **no está en la tabla anclada** de `tests/AGENTS.md` |

### 8.2 `tests/test_agent_worker.py`

`OBSERVED` 1092 líneas, **41 tests**, `call` 79.86 s (R1) / 60.00 s (aislado),
**912 subprocesos / 59.86 s**, mediana 1.948 s, **19.1 % de montaje** (el
cociente de montaje más desfavorable de los cuatro).

**Qué es.** Tests del **Agent Worker** (`runtime/orchestrator/agent_worker.py`)
más el loop del host con `AgentWorker` inyectado, sobre un repo git por test
(`make_repo`, línea 140, **5 subprocesos git por repo**: `init` + 2 `config` +
`add` + `commit`).

**Estructura real:**

| Grupo | Tests | Repo | Host |
|---|---:|---|---|
| Contrato de delegación, `parse_agent_task`, vocabulario de invocación, `AuthorityBoundary` | 10 | no | no |
| Contrato M4 / `WorkerResult` / `validate_worker_result` | 2 | no | no |
| Worker directo (`execute`) sobre repo | 14 | sí | no |
| Loop del host con `AgentWorker` | 10 | sí | **23 `run()`** |
| Sujeto ajeno: `store.read_journal_with_gaps`, `observation.journal_gaps`, `worker.repository_snapshot` | 4 | sí (innecesario) | no |

**Garantías de mayor valor:**

- `test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task` —
  anti-loop: la tarea de implementación se deriva **una sola vez** y el estado
  post-ingesta impide repetirla. **CRITICAL**.
- `test_verification_failure_makes_the_result_incomplete_even_if_agent_finished`
  — el repo contradice al agente ⇒ `incomplete`, no éxito. **CRITICAL**.
- `test_recovery_after_restart_from_persisted_evidence_only` — recuperación
  sólo desde evidencia persistida. **CRITICAL**.
- `test_artifacts_modified_is_observed_even_when_the_path_was_already_dirty` y
  `test_scope_violation_is_detected_even_when_the_scope_path_was_already_dirty`
  — atribución por **contenido**, no por conjunto de paths sucios. **CRITICAL**,
  exclusivo del archivo.
- `test_agent_worker_executes_through_injected_invoker_and_persists_result` —
  materialización → escritura real → clasificación real → artefacto persistido
  en una sola cadena. **CRITICAL**.

**Defectos de test observados:**

| Línea | Defecto |
|---|---|
| 545 | `assert set(result.artifacts_modified) <= authorized` — **tautológico**: producción filtra `changed` por `authorized` antes de exponerlo (`agent_worker.py:467-468`) |
| 641 | `test_implementation_task_requires_an_authorized_plan` — pasa por una razón **ajena a su nombre**: la derivación devuelve `RUN_IMPLEMENTATION_TASK` marcado `REQUIRES_HUMAN`; la negativa real vive en `host.iterate` (`host.py:607-616`), que el test **nunca ejecuta** |
| 860 | `test_stale_validation_does_not_allow_closed` — **nunca registra una validación ni cambia contenido**: `Closed is False` es cierto también en un repo vacío; la propiedad de staleness **no se prueba** |
| 529 | `assert journal[0]["action"] in (RUN_IMPLEMENTATION_TASK,)` — membresía de un solo elemento |
| 995-997 | compara `observation.journal_gaps` con la llamada que lo computa (wiring, no expectativa independiente) |
| 486-490 | reduce a igualdad de conjuntos de claves: no detecta un campo **renombrado** |

`OBSERVED` **Costo innecesario identificado**: 4 tests (`963`, `983`, `1000`,
`1058`) construyen un repositorio git completo para ejercitar
`OrchestratorStore` y `worker.repository_snapshot`, que **no necesitan git
completo** — `963/983/1000` no necesitan git en absoluto (el store sólo resuelve
un path) y `1058` necesita un árbol git mínimo. `ESTIMATED`: ~5.5 s recuperables
sin perder garantía.

### 8.3 `tests/test_sae_scope_enforcement.py`

`OBSERVED` 1081 líneas, **44 casos recogidos = 38 funciones + 6 casos extra de
un `parametrize`** (`test_proximity_is_never_authorization`, línea 897, 7
casos). `call` 58.31 s (R1) / 55.28 s (aislado), **878 subprocesos / 53.70 s**,
**9.7 % de montaje**.

`OBSERVED` **Corrección de inventario**: el archivo tiene **38 `def test_*`**,
no 38 + 6; los 44 son casos. Las auditorías previas citaron 44 tests, que es la
cifra **recogida** — correcta pero no idéntica al número de funciones.

**Qué es.** La frontera **SAE (Scope/Authority Enforcement)** de
`runtime/orchestrator/host.py` + `autonomy.py`, con dos mitades nítidas:

| Mitad | Tests/casos | Repo | Nivel |
|---|---:|---|---|
| Frontera pura (`verify_write_targets`, `verify_action_scope`, `evaluate_autonomy`, `authorization_projection/drift`) | **25 funciones / 31 casos** | no | UNIT / CONTRACT |
| Host sobre git real (gate antes del efecto, drift entre corridas, detección post-hoc) | **13 funciones** | sí | INTEGRATION / E2E |

**Garantías de mayor valor:**

- `test_f3_regression_stops_before_the_write_and_leaves_everything_identical`
  (318) — la regresión canónica del incidente `<PLAN-136>:F-3`: la negativa
  ocurre **antes** del efecto y el artefacto excluido queda byte-idéntico.
  **CRITICAL**.
- `test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed`
  (418) — contraprueba de no-vacuidad: el mismo fixture y el mismo worker **sí**
  escriben cuando la declaración es honesta. Sin este test, "byte-idéntico"
  podría ser una propiedad del fixture. **CRITICAL**.
- `test_the_host_stops_when_the_contract_is_rewritten_after_authorization`
  (741) — el pin del checkpoint sobrevive una **instancia nueva** de host y la
  reescritura no compra continuación. **CRITICAL**.
- `test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing`
  (642) — citado por el propio Plan 138 como evidencia de `<PLAN-138>:PC-1`.
  **CRITICAL**.

**Defectos de test observados:**

| Línea | Defecto |
|---|---|
| **1034** | `assert _digest(root/EXCLUDED) == _digest(root/EXCLUDED)` — compara un valor **consigo mismo**; no puede fallar |
| **1067-1072** | `authorization_projection(e) == authorization_projection(e)` y `verify_write_targets(e,(P,)).to_dict() == verify_write_targets(e,(P,)).to_dict()` — valor contra sí mismo |
| **394-396** | compara el checkpoint con `plan_before_projection(root)`, que **recomputa con las mismas funciones privadas de producción** sobre el mismo fixture intacto: autoconsistencia, no expectativa independiente |
| 787 | compara el checkpoint con `pinned`, leído por el mismo accesor privado |
| 807, 848 | `assert pinned and "…" not in pinned` — cortocircuito: si `pinned` fuera falsy, la mitad fuerte no corre |
| 826 | asertа `second.records[0]["action"] == "RECORD_VALIDATION_ANCHOR"` — fija un resultado **incidental** de la derivación, no una garantía de enforcement |
| 443 ↔ 992 | **near-duplicados**: mismo fixture, mismo `max_iterations=2`, mismo `STOP_FORBIDDEN_ACTION`, mismo artefacto cambiado |
| 504 ↔ 515 | `504` está subsumido por `515` |

`OBSERVED` El archivo alcanza API privada del host: `_pinned_autonomy_projection`
(309), `_scope_violations` (1023), `_autonomy_targets` (975),
`_autonomy_envelope` (410, 981). `INFERRED` Consultar API privada es legítimo
para un test de este nivel, pero acopla el archivo a la estructura interna del
host: un refactor de nombres rompe los tests **sin** que cambie ninguna
garantía.

### 8.4 `tests/test_autonomy_effects.py`

`OBSERVED` 801 líneas, **36 tests**, `call` 54.66 s (R1) / 43.49 s (aislado),
**682 subprocesos / 45.00 s**, **17.1 % de montaje**.

**Estructura real:**

| Sección | Tests | Repo | Host |
|---|---:|---|---|
| 1. La observación lee la declaración verbatim | 6 | 1 (2 repos) | no |
| 2. Admisión: los cuatro veredictos, efecto ⊥ scope | 14 | no | no |
| 3. El gate end-to-end | 5 | sí | sí |
| 4. El techo de recursos | 7 | 5 | 3 |
| 5. Efectos del worker: declarado vs ejecutado | 4 | 3 | sí |

`MEASURED` **18 construcciones de repositorio, 18 iteraciones de host.** El
archivo es **mayoritariamente puro** (22 de 36 tests no tocan git ni el host) —
que es exactamente por qué sus 43.49 s concentrados en 14 tests son
desproporcionados.

**Garantías de mayor valor:**

- `test_case_a_and_the_counter_proof_the_write_really_happens_when_declared`
  (602) — la contraprueba de no-vacuidad del archivo. **CRITICAL**.
- `test_an_executed_effect_the_plan_never_declared_is_a_finding_and_stops`
  (771) — la mitad "detección, no prevención" del eje de efectos: el host **no**
  puede interponerse dentro de la invocación y **no** debe reportar el stop
  post-hoc como prevención (policy §1.5/§10). **CRITICAL**, exclusivo.
- `test_case_c_the_gate_stops_before_the_delegation_and_nothing_writes` (545) —
  triple evidencia de la negativa: digest intacto + sin delegación + invoker
  nunca alcanzado. **CRITICAL**.
- `test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence`
  (671) — el techo se lee del **journal real** y sobrevive una instancia nueva
  de host. **HIGH/CRITICAL**.

**Defectos de test observados:**

| Línea | Defecto |
|---|---|
| **490** | `assert outcome.stop_condition is None or "scope" in outcome.scope_reason` — la segunda disyuntiva es **siempre verdadera** (todas las ramas de `scope_reason` contienen "scope"): la aserción **no puede fallar**. El test se llama "is admissible" y el resultado real es una **negativa** que no asertа |
| **689** | `test_an_exhausted_ceiling_stops_even_when_no_action_would_be_delegated` — **nunca construye un host ni asertа un stop**; sólo comprueba que un techo `0` es un GAP declarado. El nombre promete un comportamiento cuya consecuencia real es la **inversa** (con `resource_ceiling=None` el guard del techo queda deshabilitado) |
| 718-721 | `assert not hasattr(bounded, "resource_ceiling")` — detector de cambio de tipo, no de comportamiento; duplica el dogfood |
| 534 | `"network" not in rewritten.split("plan:")[1]` — se apoya en una propiedad accidental del formato del header |

`OBSERVED` **Oportunidades de consolidación claras**: 3 tests (630, 653, 671)
comparten **fixture idéntico** (techo 1 + efecto autorizado + dos corridas) y
asertan tres vistas del mismo stop; 4 tests (545, 569, 581, 593) comparten la
forma "el gate para antes de delegar" y difieren sólo en el modo de admisión.

---

## 9. Per-Test Findings

`OBSERVED` El dataset completo está en el **Anexo A** (§38) con las 152 filas de
los cuatro archivos: `test_id`, `file`, `test_name`, `level`,
`primary_component`, `guarantee`, `evidence_value`, `runtime`,
`runtime_variability`, `subprocess_count`, `subprocess_seconds`,
`git_operation_count`, `wait_count`, `filesystem_heaviness`,
`external_boundary`, `classification`, `recommendation`, `confidence`, `notes`.

### 9.1 Los 20 tests más caros de los cuatro archivos (`MEASURED`)

| # | s (aislado) | subproc | test |
|---:|---:|---:|---|
| 1 | 18.31 | 295 | `test_autonomous_orchestrator.py::test_revalidation_is_recorded_as_a2_without_mutating_a1` |
| 2 | 12.24 | 198 | `test_autonomous_orchestrator.py::test_restart_reconstructs_and_continues_without_lost_continuity` |
| 3 | 11.11 | 179 | `test_autonomous_orchestrator.py::test_full_loop_derives_closed_from_real_evidence` |
| 4 | 11.11 | 173 | `test_autonomous_orchestrator.py::test_closed_derivation_never_releases_and_reports_human_authority` |
| 5 | 8.51 | 136 | `test_sae_scope_enforcement.py::test_the_host_stops_when_a_declared_scope_widens_to_another_authorized_path` |
| 6 | 8.14 | 131 | `test_sae_scope_enforcement.py::test_an_unauthorized_widening_is_refused_by_the_scope_check_before_any_drift` |
| 7 | 7.48 | 119 | `test_sae_scope_enforcement.py::test_the_host_stops_when_the_contract_is_rewritten_after_authorization` |
| 8 | 7.23 | 114 | `test_agent_worker.py::test_stale_validation_does_not_allow_closed` |
| 9 | 7.20 | 113 | `test_autonomous_orchestrator.py::test_stale_validation_derives_revalidation_and_fresh_does_not` |
| 10 | 6.44 | 103 | `test_agent_worker.py::test_empty_implementation_result_does_not_re_delegate_forever` |
| 11 | 6.23 | 100 | `test_agent_worker.py::test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task` |
| 12 | 5.63 | 90 | `test_autonomy_effects.py::test_the_ceiling_bounds_the_first_delegation_and_stops_the_second` |
| 13 | 5.64 | 90 | `test_autonomy_effects.py::test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence` |
| 14 | 5.63 | 90 | `test_autonomy_effects.py::test_resource_exhaustion_is_never_an_authorization` |
| 15 | 5.51 | 88 | `test_sae_scope_enforcement.py::test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing` |
| 16 | 5.06 | 81 | `test_autonomous_orchestrator.py::test_no_progress_guard_stops_instead_of_spinning` |
| 17 | 4.74 | 74 | `test_agent_worker.py::test_finding_blocks_closure_until_resolved_and_revalidation_is_derivable` |
| 18 | 4.20 | 67 | `test_agent_worker.py::test_recovery_after_restart_from_persisted_evidence_only` |
| 19 | 4.20 | 67 | `test_sae_scope_enforcement.py::test_a_required_obligation_inside_the_scope_is_conducted` |
| 20 | 4.20 | 67 | `test_sae_scope_enforcement.py::test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed` |

`MEASURED` Estos 20 tests suman **152.4 s = 63 %** del tiempo de los cuatro
archivos. **La cola es extremadamente corta y empinada**: los otros 132 tests de
esos archivos suman ~90 s.

### 9.2 La otra mitad de la historia: los tests casi gratuitos (`MEASURED`)

`OBSERVED` **138 de los 152 tests** de los cuatro archivos registran ≤ 0.01 s.
`MEASURED` En `test_sae_scope_enforcement.py`, **31 de 44**; en
`test_autonomy_effects.py`, **22 de 36**. Son las mitades puras: frontera de
scope, admisión de efectos, proyección/checkpoint, vocabularios.

`INFERRED` **Esto es la prueba de que el archivo MIXED no es un problema de
diseño de tests sino de empaquetado de niveles**: la mitad pura de cada archivo
ya corre en milisegundos; lo que está mal ubicado es que esa mitad comparta
archivo con la mitad de integración, lo que impide seleccionar por path (ya
señalado por la segunda auditoría) **y** hace que el archivo entero parezca
caro.

---

## 10. Setup vs Execution

### 10.1 La separación pedida, medida (`MEASURED`)

```text
TEST TÍPICO DE LOS CUATRO ARCHIVOS

SETUP    =  build_repo()/make_repo()        0.28 – 0.42 s   3–5 subprocesos git
ACTION   =  observe() ×N + host iterations + gate subprocesses
                                            1.5 – 18 s      ~90–295 subprocesos
ASSERTION=  en proceso, sobre el journal/artefacto           0,00x s
CLEANUP  =  ninguna (scratch por sesión, no por test)        0.00 s
```

| Archivo | montaje medido | acción medida | montaje:acción |
|---|---:|---:|---:|
| `test_autonomous_orchestrator.py` | 6.08 s | 77.17 s | **1 : 12.7** |
| `test_agent_worker.py` | 11.44 s | 48.56 s | **1 : 4.2** |
| `test_sae_scope_enforcement.py` | 5.37 s | 49.91 s | **1 : 9.3** |
| `test_autonomy_effects.py` | 7.43 s | 36.06 s | **1 : 4.9** |
| **TOTAL** | **30.31 s** | **211.71 s** | **1 : 7.0** |

`OBSERVED` **Respuesta explícita a la pregunta fundamental del pedido**
(*"¿estamos pagando mucho para preparar un escenario cuya acción bajo prueba
realmente cuesta muy poco?"*): **No.** El montaje es el 12.5 % y la acción el
87.5 %. La intuición del informe previo (los ~290 s son montaje) **no se
sostiene con la medición**.

### 10.2 Por qué la acción cuesta tanto, en una frase (`MEASURED` + `OBSERVED`)

`INFERRED` La acción no es costosa por lo que *hace*, sino por **cuántas veces
lo hace**. `observe()` cuesta 0.380 s porque lanza **6 subprocesos** para leer un
estado que no cambió; `run()` observa dos veces por iteración; una iteración de
`run(max_iterations=1)` lanza **49 subprocesos** y cuesta **2.99 s**, de los
cuales sólo **1 `python src/check_ok.py`** es "trabajo" en el sentido del plan.

`OBSERVED` El desglose exacto de esa iteración medida:

```text
git rev-parse ×21   ← git_state() ×2 observaciones ×2 rev-parse + internos de la identidad
git ls-files  ×10   ← repository_snapshot (host + worker) + scoped_content_identity
git status    ×9    ← git_state() y repository_paths()
git write-tree ×7   ← scoped_content_identity (una por observe)
git diff      ×1    ← host._committed()
python        ×1    ← la verificación declarada por el plan
```

`INFERRED` **De los 49 subprocesos de una iteración, exactamente 1 es la acción
que el plan declara como verificación.** Los otros 48 existen para *observar el
repositorio antes y después*. Esa proporción —**48:1**— es el hallazgo central de
esta autopsia.

---

## 11. Subprocess Analysis

### 11.1 Totales (`MEASURED`)

```text
TOTAL_SUBPROCESSES                 4.944
  leg DEV (1358 tests)             4.917
  leg harness (185 tests)             27
  en fase setup                        0
  en fase teardown                     0
  en fase call                     4.944   (100 %)

TOTAL_SUBPROCESS_TIME            332.54 s  (80.3 % del wall)
  git                            ~310 s
  intérprete Python                ~9.1 s

COSTO UNITARIO MEDIDO
  git <subcomando>                ~63 ms   (derivado de la regresión r=0.999)
  arranque de intérprete Python    37.2 ms  (n=8, min 36.5 / max 41.1)
```

### 11.2 Distribución por archivo (`MEASURED`)

| Archivo | tests | subprocesos | s subproc | s/test | c/test |
|---|---:|---:|---:|---:|---:|
| `test_autonomous_orchestrator.py` | 31 | 1.303 | 81.11 | 2.62 | 42.0 |
| `test_agent_worker.py` | 41 | 912 | 59.86 | 1.46 | 22.2 |
| `test_sae_scope_enforcement.py` | 44 | 878 | 53.70 | 1.22 | 20.0 |
| `test_autonomy_effects.py` | 36 | 682 | 45.00 | 1.25 | 18.9 |
| **4 dominantes** | **152** | **3.775** | **239.67** | **1.58** | **24.8** |
| resto de la suite | 1391 | 1.169 | ~92.9 | 0.07 | 0.8 |

`MEASURED` **Un test de los cuatro archivos lanza 31× más subprocesos que un
test del resto de la suite** (24.8 vs 0.8).

### 11.3 Qué procesos son necesarios para la garantía (`INFERRED`, por operación)

| Grupo | Conteo | ¿Necesario para la garantía? |
|---|---:|---|
| `git init/add/commit` del fixture | 80 repos × 3–5 = ~290 | **Sí** para los tests que afirman sobre `git status`/identidad; **no** para los que sólo usan el repo como directorio de trabajo |
| `python src/check_ok.py` (verificación del plan) | 60 | **Sí**: es la acción que el plan declara y el host clasifica |
| gates `check_lifecycle_*` | 106 | **Sí** en los tests que afirman sobre clasificación de gates; **no** en los que no |
| `git rev-parse` (HEAD + branch) | 1790 | **Parcialmente**: hace falta el estado del repo; se lanzan **2 procesos** donde **1** (`git status --porcelain=v2 --branch`) devuelve ambos |
| `git status` | 590 | Sí, pero solapado con el anterior |
| `git ls-files` / `write-tree` / `hash-object` (identidad) | 1564 | **Sí** para la identidad de contenido; se recomputan **una vez por `observe()`**, aunque el contenido del fixture no cambia entre observaciones de un mismo test |
| `python scoped_content_identity.py` | 24 | proceso innecesario: es un **import de módulo** dentro del mismo intérprete, invocado por subproceso en 24 sitios |
| `git diff` (`_committed`) | 57 | Sí donde se afirma `Committed`; hoy sólo en el loop completo |

`OBSERVED` **`python scoped_content_identity.py` (24 lanzamientos)**: la función
`scoped_content_identity` en `observation.py:144-164` **importa el módulo** y
llama `module.compute(...)` **en proceso**. Los 24 lanzamientos provienen de los
tests de `test_scoped_content_identity.py` (fuera de los cuatro dominantes), que
lo invocan por CLI para probar su contrato de proceso — uso legítimo.
`INFERRED` No hay aquí un subproceso evitable.

### 11.4 La pregunta del pedido, respondida (`INFERRED` con base medida)

> ¿Qué evidencia aporta ese proceso que no podría obtenerse de una prueba más
> barata?

- **`git init/add/commit` (290 procesos, ~18 s)**: aporta que el repositorio sea
  *real* (SHAs, índice, trees). Para los ~20 tests que afirman sobre identidad
  de contenido o tracking, **no hay prueba más barata**: la auditoría previa lo
  estableció y esta lo confirma (`test_check_lifecycle_checkpoint` fue
  descartado como "low value" precisamente por esto). Para los ~30 tests que
  usan el repo sólo como cwd, **sí** hay una prueba más barata (§20).
- **`git rev-parse`/`status`/`ls-files`/`write-tree` (2.9 mil procesos, ~190 s)**:
  la evidencia es "el estado del repositorio en este instante". **Lo caro no es
  el proceso sino su repetición**: el estado no cambia entre la observación de
  `run()` y la de `iterate()` (líneas 1050 y 591, consecutivas, sin escritura
  entre ellas). **Esa repetición no aporta evidencia nueva.**
- **`python src/check_ok.py` (60)**: aporta que la clasificación del plugin se
  aplica a un exit code real. Necesario.
- **gates `check_lifecycle_*` (106)**: aportan la clasificación publicada por el
  checker. Necesario donde se afirma sobre ella.

---

## 12. Git Analysis

### 12.1 Inventario medido (`MEASURED` + `OBSERVED`)

```text
repositorios git construidos en la suite        161  (git init)
  en los 4 archivos dominantes                   80
    test_autonomous_orchestrator.py              22
    test_agent_worker.py                         27
    test_sae_scope_enforcement.py                13
    test_autonomy_effects.py                     18
  en el resto de la suite                        81

subprocesos git totales                       4.696
  por comando: rev-parse 1790 · ls-files 989 · status 590 · write-tree 551
               add 199 · commit 189 · init 161 · config 122 · diff 57
               hash-object 24 · checkout 8 · otros 6
```

`OBSERVED` **Repositorios reutilizados: cero.** Cada construcción usa un nombre
con `uuid4().hex[:8]` bajo `pytest_isolation.scratch_root(<suite>)` (los cuatro
archivos, helper `_scratch`). El aislamiento por test es **deliberado y
correcto** (Plan 145, §4).

`OBSERVED` **Commits por repositorio**: 1 (el baseline sintético). Dos tests
crean commits adicionales (`set_gate_signal`, `stage`, la reescritura de plan en
`test_sae_scope_enforcement`). **No hay branches ni tags** en los cuatro
archivos; los branches/tags aparecen en `test_check_lifecycle_checkpoint.py`
(fuera del alcance principal).

### 12.2 `GIT_SETUP_COST` vs `GIT_BEHAVIOR_UNDER_TEST` (`MEASURED`)

```text
GIT_SETUP_COST (infraestructura de montaje)
  80 repos × git init/add/commit   = 240 procesos  ≈ 15.4 s
  + config (27 repos agent_worker) =  54 procesos  ≈  3.4 s
  TOTAL ≈ 18.8 s  (sobre 298 s = 6.3 % de los 4 archivos)

GIT_BEHAVIOR_UNDER_TEST (operaciones que la garantía requiere)
  rev-parse/status/ls-files/write-tree/hash-object/diff
  = 4.000 procesos aproximadamente  ≈ 250 s
  TOTAL ≈ 250 s (83.9 % de los 4 archivos)
```

`OBSERVED` **Separación explícita:** el costo de infraestructura git es **6.3 %**;
las operaciones git que el comportamiento bajo prueba realmente exige son el
**83.9 %**. Sólo **~4.5 %** queda en la frontera (operaciones git de
infraestructura que además aportan evidencia).

`INFERRED` **Consecuencia:** optimizar el montaje git tiene un techo de **~19 s
sobre 298 s (−6.3 % de los cuatro archivos, −4.5 % de la suite)**. La promesa de
−52 % del primer informe **no es alcanzable por esa vía** y esta medición lo
cierra con números.

### 12.3 Tensión con Plan 145, declarada (`OBSERVED` + `INFERRED`)

`OBSERVED` El docstring de `test_autonomous_orchestrator.py` (líneas 8-10)
declara: *"They deliberately do **not** use pytest's `tmp_path`: the throw-away
git repositories built here must not be nested in the repository under test"*.

`INFERRED` Esto **no** es una restricción contra compartir una plantilla; es una
restricción contra **anidar el repositorio dentro del repo bajo prueba**. La
prohibición real de reutilización viene de Plan 145 y de R-145-1 (§4.2):
compartir un objeto git mutable entre tests reintroduce el no-determinismo que
ese plan eliminó. **Regla que esta auditoría declara y respeta:**

```text
PERMITIDO por Plan 145 (no implementado aquí):
  · un repositorio creado una vez y COPIADO por test (árboles físicamente
    distintos ⇒ ningún test muta lo que otro lee).
NO PERMITIDO por Plan 145:
  · un repositorio pre-inicializado REUTILIZADO in situ entre tests
    (estado mutable compartido ⇒ la causa raíz declarada de Plan 145, I-1).
```

`RECOMMENDED` Esta auditoría **no propone** ninguna de las dos como acción
inmediata, porque la ganancia máxima medida de la primera es **~19 s (−4.5 % de
la suite)** con el riesgo alto que la segunda mitad de §4.2 documenta. **El
cociente riesgo/beneficio no la justifica**, y la evidencia de §7.3 y §10.2
señala una palanca 2–3× mayor sin riesgo de aislamiento.

---

## 13. Filesystem Analysis

`OBSERVED` Operaciones de filesystem relevantes, por patrón (no por llamada
trivial):

| Patrón | Dónde | Volumen observado | Costo |
|---|---|---|---|
| Árbol de directorios del fixture | `build_repo`/`make_repo`: 3–5 `mkdir(parents=True)`, ~6–8 escrituras de archivo | 80 repos × ~10 = ~800 operaciones | `MEASURED` incluido en el constructor (0.28–0.42 s incluye los 3–5 subprocesos git, que dominan) |
| Escritura del plan sintético y del INDEX | los cuatro builders | 2 archivos por repo = 160 | despreciable |
| Escrituras del host (journal, delegaciones, worker results, capturas stdout/stderr) | `host.py`, `store.py` | por iteración: 1 registro de journal + 2 capturas + 1 worker result | `INFERRED` pequeño; las capturas se abren con `open("wb")` y se leen de vuelta por iteración (`worker.py:345-364`) |
| **Hashing de contenido** | `worker.repository_snapshot` hashea **cada archivo** del repo con SHA-256 en Python (`worker.py:489-492`) | por `repository_snapshot`: 1 `git ls-files` + N hashes | `INFERRED` **este es el costo de filesystem real**: se recomputa por snapshot y hay 2+ snapshots por iteración |
| Copias | `test_scoped_content_identity.py` usa `copytree` (fuera de los dominantes) | 1 | medido en la auditoría previa |
| Eliminación | `clear_own_scratch()` al inicio de sesión (no por test) | 1 | `MEASURED` 0 subprocesos |
| `.agents`, `.project`, `.backup` | el host escribe en `.project/orchestrator/plan-NNN/` de cada repo desechable | por test | pequeño |

`INFERRED` **El costo de filesystem no es el número de archivos: es el
`SHA-256` por archivo por snapshot, repetido por iteración.** Un repositorio de
fixture tiene ~10–15 archivos; dos snapshots por iteración y ~5 iteraciones
promedio dan ~100–150 hashes por test, cada uno con una lectura de archivo. Sigue
siendo un orden de magnitud menor que los ~24 subprocesos por test, pero **es el
segundo componente** y explica por qué el wall supera al tiempo de subproceso en
los tests más largos.

`OBSERVED` **Patrón de costo dominante identificado**: `repository_snapshot` se
llama en `host._execute_delegation` (`host.py:747`, `906`) y en
`agent_worker.execute` (`agent_worker.py:422`, `464`), es decir **hasta 4 veces
por iteración** en el camino de ejecución, más una por `git_state`. Cada llamada
paga `git ls-files` + hashing completo del árbol.

---

## 14. Wait / Polling Analysis

`OBSERVED` Búsqueda exhaustiva (`grep` sobre `runtime/`, `tools/`, `tests/`,
`protocol/.agents/harness/`) de:
`time.sleep`, `sleep(`, `.wait(`, `poll(`, `retry`, `timeout`, `max_wait`,
`loop-until`, `process.wait`, `filesystem polling`, `state polling`.

**Resultado: NO EXISTE NINGUNA ESPERA ARTIFICIAL.**

```text
time.sleep / sleep(...)                    0 ocurrencias
.poll() / process.wait()                   0 ocurrencias
retry loops / reintentos con espera        0 ocurrencias
filesystem polling / state polling         0 ocurrencias
timeout como espera                        un único uso: el parámetro
                                           timeout= de subprocess.run
                                           (DEFAULT_TIMEOUT_SECONDS = 120 s),
                                           que NUNCA se alcanza en la suite
```

`OBSERVED` Los únicos matches de "retry" en el árbol son **texto documental**
(`tests/test_fc_recovery_alignment.py`, que certifica que el runtime **no**
implementa retry: *"the code implements no retry mechanism"*). Es decir: la
ausencia de retry es una **propiedad certificada del producto**, no una omisión.

### 14.1 Veredicto sobre la categoría `WAITS` (`MEASURED`)

```text
WAIT_SHARE = 0.0 %   (cero segundos; categoría vacía por evidencia)
```

`INFERRED` **Esto reencuadra el problema.** La percepción de "la suite espera" es
incorrecta: lo que ocurre es que **Windows tarda 63 ms en crear un proceso `git`**
y los tests crean miles. La diferencia es decisiva para el diseño de la solución:
si fuera espera, se arreglaría con sincronización; **al ser creación de procesos,
se arregla reduciendo el número de procesos**, lo que no tiene nada que ver con
determinismo ni con sleeps.

`OBSERVED` El único "wait" real es el **bloqueo sincrónico** de
`subprocess.run`, que es determinista por construcción (no hay carrera, no hay
`poll`), y por eso los tests son estables (§16).

---

## 15. Test Level Classification

`OBSERVED` Clasificación por **comportamiento real**, no por nombre de archivo
(siguiendo el método de la segunda auditoría).

### 15.1 Los cuatro archivos dominantes

| Archivo | Nivel real | Composición |
|---|---|---|
| `test_autonomous_orchestrator.py` | **MIXED** | UNIT (3) + CONTRACT (5) + COMPONENT (14) + **INTEGRATION/E2E (9)** |
| `test_agent_worker.py` | **MIXED** | UNIT (10) + CONTRACT (2) + COMPONENT (14) + **INTEGRATION (11)** + sujeto ajeno (4) |
| `test_sae_scope_enforcement.py` | **MIXED** | UNIT/CONTRACT (25 funciones / 31 casos) + **INTEGRATION/E2E (13)** |
| `test_autonomy_effects.py` | **MIXED** | UNIT (22) + COMPONENT (1) + **INTEGRATION (13)** |

`OBSERVED` **Los cuatro son MIXED a nivel de archivo, no de test.** Cada test
individual cae limpio en un nivel; lo que está mezclado es el archivo. Esto es
idéntico a lo que la segunda auditoría estableció para 20 archivos, y esta
autopsia lo confirma en los cuatro que importan para el reloj.

### 15.2 Distribución de niveles dentro de los 152 tests (`OBSERVED`)

| Nivel | Tests | s (aislado) | % del tiempo de los 4 |
|---|---:|---:|---:|
| **INTEGRATION / E2E** | **46** | **~225 s** | **~93 %** |
| COMPONENT | 46 | ~14 s | ~6 % |
| UNIT | 33 | ~0.3 s | ~0.1 % |
| CONTRACT | 27 | ~0.2 s | ~0.1 % |
| Sujeto ajeno (store/worker helpers) | 4 | ~3.5 s | ~1.4 % |

`INFERRED` **La clasificación honesta no respalda la hipótesis "estos tests son
unitarios disfrazados de integración"** en su forma fuerte. 46 tests son
integración **legítima** (su garantía exige el mundo real). Lo que sí es cierto:

- **37 tests son UNIT/CONTRACT puros** dentro de archivos caros, y son
  prácticamente gratis: están **en el nivel correcto pero en el archivo
  incorrecto** para efectos de selección.
- **4 tests** tienen un sujeto que no es el del archivo (`store`, `worker
  helpers`) y construyen un repositorio que no necesitan.
- **3 tests** (`test_stale_validation_does_not_allow_closed`,
  `test_implementation_task_requires_an_authorized_plan`,
  `test_an_exhausted_ceiling_stops_even_when_no_action_would_be_delegated`) **no
  prueban lo que su nombre declara**, según el análisis de §8. Ese es un
  problema de **nivel de garantía**, no de nivel de test.

---

## 16. Variability

`MEASURED` **RUN_COUNT = 5 corridas** de los cuatro archivos (1 dentro de la
corrida completa R1 + 1 instrumentada R2 + 3 aisladas V1–V3) y **2 corridas
completas** de la suite (R1, R2).

```text
ENVIRONMENT   Windows 11, Python 3.14.3, pytest 9.0.3, git presente, 12 CPU lógicos
COMMAND       (aislado) python -m pytest <4 archivos> -q --durations=0 --durations-min=0
              (completo) python -m pytest tests/ protocol/.agents/harness/tests/ -q …
DATE/TIME     2026-10-13
```

### 16.1 Variabilidad entre corridas aisladas (`MEASURED`)

| Corrida | Wall de los 4 archivos | PASS |
|---|---:|---|
| V1 | 242.86 s | 152 passed |
| V2 | 242.96 s | 152 passed |
| V3 | 243.18 s | 152 passed |
| **dispersión** | **0.13 %** (max−min / media) | — |

`MEASURED` **Por test, n = 3:** mediana del coeficiente de variación **0.003
(0.3 %)**. Los tests caros son aún más estables:

| Test | V1 | V2 | V3 | CV |
|---|---:|---:|---:|---:|
| `test_revalidation_is_recorded_as_a2…` | 18.33 | 18.30 | — | 0.001 |
| `test_restart_reconstructs_and_continues…` | 12.24 | 12.24 | — | 0.000 |
| `test_the_host_stops_when_a_declared_scope_widens…` | 8.45 | 8.57 | — | 0.008 |
| `test_ceiling_bounds_the_first_delegation…` | 5.57 | 5.69 | — | 0.015 |

`MEASURED` La mayor variabilidad observada está en **tests de ~0.02 s** (CV
0.283 en `test_worker_adapter_signature_accepts_the_real_host_call`), es decir
**ruido absoluto irrelevante** (± 0.01 s). `OBSERVED` Ningún test caro mostró
comportamiento inestable: **la suite es estable y determinista** (`MEASURED` 152
passed en las tres corridas, sin flakes).

### 16.2 Variabilidad **entre contextos** — el hallazgo relevante (`MEASURED`)

| Contexto | Mismos 152 tests | Diferencia |
|---|---:|---|
| Aislados (V1–V3) | 242.02 s (mediana) | — |
| **Dentro de la corrida completa (R1)** | **298.03 s** | **+23.1 %** |
| Dentro de la corrida instrumentada (R2) | 246.3 s | +1.8 % |

`MEASURED` La diferencia **no es ruido entre corridas** (esas varían < 0.2 %):
es el **efecto del contexto de ejecución**. `INFERRED` Causas plausibles, no
discriminadas por esta medición: presión de memoria/caché tras 1391 tests
previos, estado de la caché de filesystem, y fragmentación del scratch de la
sesión (152 repositorios en un mismo árbol). **`UNKNOWN` cuál de ellas domina**;
lo que la medición sí establece es que **existe y es reproducible
(+55.99 s en R1, medido).**

`RECOMMENDED` **El baseline debe declararse por contexto.** Comparar un número
"aislado" contra uno "en suite" produce un error del 23 % — mayor que cualquier
optimización que se quiera medir. Regla propuesta en §19:

```text
CANONICAL_RUNTIME                = corrida completa (413.95 s)
DOMINANT_FILES_RUNTIME_IN_SUITE  = 298.03 s   ← comparable con la suite
DOMINANT_FILES_RUNTIME_ISOLATED  = 242.02 s   ← comparable con corridas focalizadas
```

---

## 17. Evidence Value

`OBSERVED` Clasificación cualitativa justificada por: criticidad del
comportamiento, exclusividad de la garantía, dificultad de detección por otros
medios, cercanía a un boundary real, posibilidad de cubrir con un test más
barato, y riesgo de regresión. **`HIGH COST` no se confundió con `HIGH VALUE`.**

### 17.1 Los cuatro archivos por valor de evidencia (`OBSERVED`)

| Valor | Tests | s (aislado) | Lectura |
|---|---:|---:|---|
| **CRITICAL** | 11 | ~96 s | garantías que no existen sin el mundo real (§17.2) |
| **HIGH** | 34 | ~92 s | reglas con código, boundaries, regresiones de incidentes |
| **MEDIUM** | 62 | ~52 s | cobertura de ramas, contrastes, contratos ya parcialmente cubiertos |
| **LOW** | 45 | ~2 s | subsumidos, near-duplicados, near-tautológicos (casi todos baratos) |

`OBSERVED` **Hallazgo clave y negativo**: **no existe ningún test de costo
`VERY_HIGH` con valor `LOW` puro.** Los tests caros tienen garantías reales. Lo
que existe es:

```text
ALTO COSTO + ALTO VALOR    →  11 CRITICAL + ~14 HIGH caros  →  OPTIMIZAR (no rehacer)
ALTO COSTO + VALOR MEDIO   →  ~10 tests con aserciones débiles →  REDISEÑAR
COSTO IRRELEVANTE + VALOR BAJO → 45 tests baratos →  CONSOLIDAR (cosmético)
```

### 17.2 Las 11 garantías `CRITICAL` (`OBSERVED`)

| # | Test | Garantía exclusiva |
|---:|---|---|
| 1 | `orchestrator::test_full_loop_derives_closed_from_real_evidence` | `Closed` derivado de anchor+checkpoint reales concordantes |
| 2 | `orchestrator::test_revalidation_is_recorded_as_a2_without_mutating_a1` | A2 preserva A1 (identidad de estado y delta) |
| 3 | `orchestrator::test_restart_reconstructs_and_continues_without_lost_continuity` | continuidad de iteración entre instancias de host |
| 4 | `orchestrator::test_checker_classification_is_read_and_not_inferred_from_exit_code` | el signal viene del texto publicado, con contraejemplo exit-0+ANOMALY |
| 5 | `agent_worker::test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task` | anti-loop de la tarea de implementación |
| 6 | `agent_worker::test_verification_failure_makes_the_result_incomplete_even_if_agent_finished` | el repo contradice al agente ⇒ incompleto |
| 7 | `agent_worker::test_recovery_after_restart_from_persisted_evidence_only` | recuperación sólo desde evidencia persistida |
| 8 | `agent_worker::test_artifacts_modified_is_observed_even_when_the_path_was_already_dirty` | atribución por contenido en árbol sucio |
| 9 | `sae::test_f3_regression_stops_before_the_write_and_leaves_everything_identical` | la negativa precede al efecto (incidente F-3) |
| 10 | `sae::test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed` | no-vacuidad: el mismo fixture sí escribe cuando se autoriza |
| 11 | `autonomy_effects::test_an_executed_effect_the_plan_never_declared_is_a_finding_and_stops` | detección post-hoc ≠ prevención |

`INFERRED` **Ninguna de estas 11 garantías es alcanzable con un test más
barato**, y las tres auditorías coinciden en ello por métodos independientes.
**La obligación arquitectónica es conservarlas; la pregunta abierta es cuánto
de su costo es la garantía y cuánto es la repetición de observación.**

`INFERRED` Con los números de §7.3 y §10.2: de los ~96 s de esos 11 tests, una
fracción sustancial es re-observación. **El cambio que las abarata no toca
ninguna aserción** y por lo tanto no pone en riesgo la garantía; es la palanca
más segura del informe.

---

## 18. Cost × Value Matrix

`OBSERVED` Matriz construida cruzando el tiempo medido (aislado, para no
contaminar con el efecto de contexto) con el valor de evidencia de §17.

```text
                              VALUE
                 LOW        MEDIUM        HIGH        CRITICAL
COST
LOW          · 45 tests   · 40 tests    · 20 tests   ·  2 tests
             (~2 s)       (~8 s)        (~5 s)       (~2 s)
             [CONSOLIDAR] [KEEP]        [KEEP]       [KEEP]

MEDIUM       ·  0         · 12 tests    · 14 tests   ·  3 tests
             —            (~18 s)       (~30 s)      (~14 s)
                          [REDISEÑAR]   [OPTIMIZAR]  [OPTIMIZAR]

HIGH         ·  0         · 10 tests    ·  8 tests   ·  4 tests
             —            (~30 s)       (~50 s)      (~52 s)
                          [REDISEÑAR]   [OPTIMIZAR]  [OPTIMIZAR]

VERY_HIGH    ·  0         ·  0          ·  2 tests    ·  2 tests
             —            —             (~16 s)      (~30 s)
                                         [OPTIMIZAR]  [OPTIMIZAR]
```

`OBSERVED` **Las cuatro casillas que el pedido pide identificar
explícitamente:**

### 18.1 Very high cost + low value

```text
NINGUNA. Cero tests.
```

`INFERRED` Esta es una **conclusión negativa y es un resultado**: no hay grasa
costosa. Coincide con la conclusión de la segunda auditoría ("la suite no tiene
grasa costosa; tiene montaje costoso"), pero **corrige su diagnóstico**: el
"montaje costoso" es en realidad **ejecución repetida**, según §10.

### 18.2 Very high cost + critical value

| Test | s | Recomendación |
|---|---:|---|
| `orchestrator::test_revalidation_is_recorded_as_a2_without_mutating_a1` | 18.31 | **OPTIMIZAR** (bajar `max_iterations` de la corrida semilla; compartir la corrida con otros tests del mismo fixture) |
| `orchestrator::test_restart_reconstructs_and_continues_without_lost_continuity` | 12.24 | **OPTIMIZAR** (corregir la aserción tautológica de la línea 988; el costo de 3 instancias es el precio de la garantía) |
| `sae::test_f3_regression_stops_before_the_write…` | ~3.5 | **MANTENER** |
| `sae::test_the_host_stops_when_the_contract_is_rewritten_after_authorization` | 7.48 | **MANTENER** (es el único que prueba que el pin sobrevive una instancia nueva) |

`RECOMMENDED` **Mantener el gasto; optimizar la observación, no la aserción.**

### 18.3 Low cost + high value — la cobertura fundamental a preservar

`OBSERVED` **20 tests, ~5 s en total**, entre ellos:

- `test_git_state_reports_the_cli_availability_explicitly` (0.21 s)
- `test_boundary_rejects_unknown_actions`, `test_release_is_forbidden_and_never_executed` (~0.001 s)
- los 7 casos de `test_proximity_is_never_authorization` (~0.001 s)
- `test_the_enforcement_helpers_are_pure_and_touch_no_filesystem` (~0.001 s)
- la mitad pura de admisión de efectos (14 tests, ~0.001 s)

`INFERRED` **Este bloque es el mejor cociente del repositorio y no debe
tocarse.** Es, además, la prueba de que la suite **no** tiene un problema de
diseño de tests: tiene un problema de ubicación y de repetición.

---

## 19. Redundancy / Overlap

`OBSERVED` No se elimina ningún test. Se clasifica:

### 19.1 `DUPLICATE` (misma garantía, dos sitios)

| Par | Garantía compartida | Evidencia |
|---|---|---|
| `orchestrator::test_full_loop_derives_closed_from_real_evidence` ↔ `orchestrator::test_closed_derivation_never_releases_and_reports_human_authority` **(920 ↔ 1086)** | `CLOSED_DERIVED` alcanzado sobre el **mismo fixture**, con el **mismo loop de 7 iteraciones** | `OBSERVED` idénticos precondiciones; difieren sólo en qué campos del registro asertan |
| `orchestrator::test_release_is_forbidden_and_never_executed` ↔ `agent_worker::test_agent_worker_cannot_resolve_human_authority` | las mismas dos familias de acciones son `FORBIDDEN` | `OBSERVED` ambas iteran la misma lista |
| `orchestrator::test_exit_code_zero_is_not_workflow_completion` ↔ `agent_worker::test_exit_code_zero_is_not_completion` ↔ `agent_worker::test_agent_worker_never_claims_completion` | exit 0 ≠ completion; sin auto-certificación | `OBSERVED` tres sitios, uno por worker |
| `sae::test_a_single_authorized_target_is_authorized` ↔ `sae::test_multiple_authorized_targets_are_authorized` (504 ↔ 515) | "todo target autorizado ⇒ autorizado" | `OBSERVED` 515 es superconjunto |
| `sae::test_proximity_is_never_authorization` ↔ `test_autonomous_scope::test_scope_verification_refuses_semantic_proximity` | proximidad no es autorización | `OBSERVED` listas de casos parcialmente solapadas, ninguna superconjunto |
| `sae::test_a_normalized_spelling_of_an_authorized_path_is_accepted` ↔ `test_autonomous_scope::test_scope_verification_is_exact_and_normalized_not_inferred` | normalización representacional | `OBSERVED` |
| `agent_worker::test_exit_code_zero_is_not_completion` ↔ `agent_worker::test_agent_worker_never_claims_completion` | no auto-certificación | `OBSERVED` el segundo es superconjunto |
| `autonomy_effects::test_the_adopted_vocabulary…` ↔ `test_autonomy_effects_dogfood::test_the_runtime_and_the_checker_share_exactly_one_effect_vocabulary` | un solo vocabulario de efectos | `OBSERVED` el dogfood es **estrictamente más fuerte** (compara contra el checker y la policy) |
| `autonomy_effects::test_the_resource_axis_does_not_enter_the_declared_envelope` ↔ `dogfood:191` | el techo no es un campo del envelope | `OBSERVED` el dogfood además inspecciona el fuente |

### 19.2 `OVERLAP` (garantías que se cruzan sin duplicarse)

| Par | Relación |
|---|---|
| `orchestrator::test_stale_validation_derives_revalidation…` ↔ `agent_worker::test_stale_validation_does_not_allow_closed` ↔ `orchestrator::test_revalidation_is_recorded_as_a2…` | mismo disparador (staleness), consecuencias distintas: derivación, `Closed=False`, preservación de A1 |
| `sae::test_the_host_stops_when_a_declared_scope_widens…` ↔ `sae::test_the_host_stops_when_the_contract_is_rewritten…` (791 ↔ 741) | dos ejes del mismo checkpoint (scope vs contrato) |
| `sae::test_the_pre_fix_detection_only_reports_after_the_effect` ↔ `sae::test_a_write_inside_the_worker_is_still_detected_after_the_fact` (443 ↔ 992) | **near-duplicate**: mismo fixture, mismo `max_iterations=2`, mismo `STOP_FORBIDDEN_ACTION`; 992 añade la llamada directa al detector |
| `agent_worker::test_human_boundary_stops…` ↔ `agent_worker::test_finding_blocks_closure…` (724 ↔ 812) | el mismo stop por finding; 812 cubre además la resolución |
| `autonomy_effects` 3 tests de techo (630/653/671) | **fixture idéntico**, tres vistas del mismo stop |
| `autonomy_effects` 4 tests de gate (545/569/581/593) | misma forma, cuatro modos de admisión |
| `sae::test_a_required_obligation_outside_the_scope…` ↔ `sae_scope_enforcement_dogfood` | **la misma garantía tres veces** (318, 642 y el dogfood 341); el dogfood es el más fuerte |
| `sae::test_the_hosts_records_into_its_own_plan_are_authorized` ↔ `dogfood:416` | el dogfood lo prueba sobre el plan real 138 |

### 19.3 `COMPLEMENTARY` (por diseño; no tocar)

`OBSERVED` La mayoría de los pares intra-archivo: unit ↔ integración del mismo
eje (p. ej. `test_case_c_declared_without_authorization_stops` unit ↔
`test_case_c_the_gate_stops_before_the_delegation_and_nothing_writes`
integración). La cobertura por ejes ortogonales del orquestador (autoridad,
scope, efectos, recursos) es **complementaria**, no redundante: eliminar un eje
dejaría ese eje sin cubrir. **Coincide con la segunda auditoría (§5.3).**

### 19.4 Veredicto

`INFERRED` **Existen 9 pares `DUPLICATE` y ~8 grupos `OVERLAP`, y esta vez sí
hay algo que consolidar — pero no por redundancia de garantía, sino por
repetición de escenario.** La distinción importa: los dos tests de release
`FORBIDDEN` prueban lo mismo y son gratis (no vale tocarlos); los dos tests del
loop completo prueban cosas distintas **sobre el mismo experimento de 7
iteraciones** y cuestan ~22 s juntos. **La consolidación con sentido es la que
elimina una corrida del mundo real, no la que elimina una aserción.**

---

## 20. Candidate Redesigns

`RECOMMENDED` Cada recomendación declara `WHY`,
`WHAT_GUARANTEE_IS_PRESERVED`, `WHAT_COST_COULD_BE_REMOVED` y
`WHAT_RISK_EXISTS`. **Ninguna está implementada.**

### C-1. De-duplicar la observación dentro del host — **cambio de producción**

```text
PROBLEM      ExecutionHost.run() observa (host.py:1050) y acto seguido llama a
             iterate(), que vuelve a observar (host.py:591). Cada iteración paga
             dos observaciones completas del mismo estado, sin que nada se haya
             escrito entre ambas. _execute_delegation añade más (769/807/822/852/870/872).
EVIDENCE     OBSERVED host.py:1050,591,769,807,822,852,870,872.
             MEASURED observe() = 0.3804 s y 6 subprocesos.
             MEASURED run(max_iterations=1) = 2.99 s y 49 subprocesos.
             MEASURED 4.696 de 4.944 subprocesos de la suite son git, y rev-parse
             (1790) es el más lanzado por este motivo.
WHY          La evidencia que aporta la segunda observación consecutiva es,
             literalmente, la misma que la primera.
GUARANTEE PRESERVED  todas: el fingerprint de no-progreso, la derivación, la
             frontera SAE y la identidad de contenido se computan de la misma
             observación, sólo una vez.
COST REMOVABLE  ESTIMATED 40–70 s de la suite (no medido: no se ejecutó el cambio).
RISK         MEDIUM: toca host.py, que es la pieza más cargada de garantías del
             repo. Requiere que la observación se pase explícitamente y que el
             fingerprint se compute sobre ese mismo objeto. La suite completa es
             la red: 1543 tests.
CONFIDENCE   HIGH en el diagnóstico (medido); MEDIUM en el número.
```

### C-2. Consolidar `test_full_loop_derives_closed…` con `test_closed_derivation_never_releases…`

```text
PROBLEM      Dos tests ejecutan el MISMO loop de 7 iteraciones sobre el MISMO
             fixture (build_repo() default + make_host(max_iterations=12)) y
             difieren sólo en qué campos del registro final asertan.
EVIDENCE     OBSERVED líneas 920-943 y 1086-1107; precondiciones idénticas.
             MEASURED 11.11 s + 11.11 s = 22.2 s.
WHY          El segundo experimento no aporta ninguna ejecución nueva.
GUARANTEE PRESERVED  las dos: `Closed` derivado de evidencia real Y la
             no-promoción con autoridad humana, en un solo test con ambas
             aserciones.
COST REMOVABLE  ~11 s (una corrida completa del host + ~1 repo + ~173 subprocesos).
RISK         LOW: es unir dos conjuntos de aserciones, no debilitar ninguna.
             Único cuidado: mantener la legibilidad de qué aserción protege qué.
CONFIDENCE   HIGH (medido + leído).
```

### C-3. Consolidar los 3 tests de techo de `test_autonomy_effects.py`

```text
PROBLEM      630, 653 y 671 comparten fixture idéntico (techo 1 + efecto
             autorizado) y la secuencia exacta de dos corridas; asertan tres
             vistas del mismo stop (acción/consumo, ausencia de autoridad,
             supervivencia al reinicio).
EVIDENCE     OBSERVED líneas 630-651, 653-669, 671-686. MEASURED 5.63+5.63+5.64.
WHY          Tres corridas del mundo real para un stop y tres campos.
GUARANTEE PRESERVED  las tres garantías; el test de reinicio conserva su
             instancia nueva de host, que es su rasgo distintivo.
COST REMOVABLE  ~11 s (2 repos + 2 corridas de host + ~180 subprocesos).
RISK         LOW/MEDIUM: el test de reinicio tiene una propiedad propia
             (instancia nueva) que hay que conservar explícitamente al fusionar.
CONFIDENCE   HIGH.
```

### C-4. Parametrizar los 4 tests de gate de `test_autonomy_effects.py`

```text
PROBLEM      545, 569, 581 y 593 comparten la forma "el gate para antes de
             delegar" y difieren sólo en el modo de admisión (NOT_AUTHORIZED,
             UNKNOWN_CLASS, UNREADABLE, referencia sin resolver).
EVIDENCE     OBSERVED líneas 545-566, 569-579, 581-591, 593-600. MEASURED ~14 s.
WHY          Cuatro repos y cuatro corridas para cuatro valores de un enum.
GUARANTEE PRESERVED  los cuatro modos siguen siendo casos del parámetro; las
             aserciones de "invoker nunca alcanzado" y "sin delegación" se
             mantienen por caso.
COST REMOVABLE  ~7 s (3 repos + 3 corridas).
RISK         LOW: patrón estándar; ya se usa parametrize en 11 archivos del repo.
CONFIDENCE   HIGH.
```

### C-5. Sacar los 4 tests de sujeto ajeno del costo de repo (`test_agent_worker.py`)

```text
PROBLEM      963, 983, 1000 (contrato de journal del store) y 1058 (helpers de
             snapshot) construyen un repo git completo. 963/983/1000 no
             necesitan git en absoluto: OrchestratorStore(root) sólo resuelve un
             path; 1058 necesita un árbol git mínimo, no un plan sintético de 14
             archivos.
EVIDENCE     OBSERVED make_repo() = 5 subprocesos git + ~14 archivos;
             OBSERVED los cuatro tests nunca usan el plan ni los gates.
             MEASURED media de test en el archivo: 1.46 s.
WHY          El repositorio es infraestructura que la garantía no menciona.
GUARANTEE PRESERVED  las cuatro: contratos de journal, gap de líneas ilegibles y
             semántica de snapshot por contenido.
COST REMOVABLE  ESTIMATED ~5.5 s. Compatible con Plan 145: son tests distintos
             con su propio scratch, no hay estado compartido.
RISK         LOW. Único cuidado: 1058 sí necesita un repo real (git ls-files);
             conservarlo con un `tmp_path` + `git init` mínimo.
CONFIDENCE   HIGH en el diagnóstico; MEDIUM en el ahorro exacto.
```

### C-6. Corregir las 5 aserciones que no pueden fallar

```text
PROBLEM      orchestrator:988 (tautología), orchestrator:1097-1098 (string
             inalcanzable), agent_worker:545 (relación construida por producción),
             sae:1034 (digest contra sí mismo), sae:1067-1072 (valor contra sí
             mismo). autonomy_effects:490 (disyunción siempre verdadera).
EVIDENCE     OBSERVED, línea por línea, con las dos líneas de producción que las
             vuelven inertes (host.py:1103, host.py:1180, agent_worker.py:467-468).
WHY          No son un problema de tiempo: son un problema de CONFIANZA. Un verde
             puede no significar nada.
GUARANTEE PRESERVED  la que cada test DICE proteger; hoy varias no la protegen.
COST REMOVABLE  0 s. El beneficio es de fidelidad, no de reloj.
RISK         LOW técnico. MEDIUM de gobernanza: toca archivos de test.
CONFIDENCE   HIGH.
```

### C-7. Rediseñar los 3 tests que no prueban lo que su nombre declara

```text
PROBLEM      agent_worker:641 (pasa por un camino que no ejecuta la negativa),
             agent_worker:860 (nunca registra una validación ni cambia contenido;
             `Closed is False` es cierto en un repo vacío),
             autonomy_effects:689 (no construye host ni asertа un stop; la
             consecuencia real de un techo 0 es la inversa).
EVIDENCE     OBSERVED el cuerpo completo de los tres + los caminos de producción
             (host.py:607-616, host.py:1153-1181, autonomy.py:1402-1406).
WHY          Un test cuyo nombre promete una propiedad no verificada es peor que
             no tenerlo: documenta una garantía inexistente.
GUARANTEE PRESERVED  hay que CONSERVAR la garantía real de cada uno (que existe:
             el parser de techo, la derivación de `Closed` sin anchor) y añadir
             la que el nombre promete.
COST REMOVABLE  ~9 s si además se los lleva al nivel correcto (los tres pueden
             dejar de construir un repo).
RISK         MEDIUM: toca aserciones; requiere decidir cuál es la garantía.
CONFIDENCE   HIGH en el diagnóstico.
```

### C-8. Consolidar `sae` 443↔992 y `504`→`515`

```text
PROBLEM      443 y 992 son near-duplicados (mismo fixture, mismo max_iterations,
             mismo stop, mismo artefacto cambiado); 504 está subsumido por 515.
EVIDENCE     OBSERVED líneas 443-467 y 992-1025; 504-507 y 515-521.
WHY          Dos corridas del mundo real para una garantía.
GUARANTEE PRESERVED  la de 992 (que es superconjunto: añade `_scope_violations`
             directo); 515 (superconjunto de 504).
COST REMOVABLE  ~5 s.
RISK         LOW.
CONFIDENCE   HIGH.
```

### C-9. Rediseñar las 2 aserciones de autoconsistencia de `sae`

```text
PROBLEM      394-396 compara el checkpoint con una recomputación hecha por las
             MISMAS funciones privadas de producción sobre el fixture intacto;
             787 compara con el valor que el mismo accesor acaba de leer.
EVIDENCE     OBSERVED `plan_before_projection` (403-415) llama a
             host._autonomy_envelope + autonomy.authorization_projection.
WHY          Una expectativa construida con el código bajo prueba no puede
             detectar un error de ese código.
GUARANTEE PRESERVED  la garantía es "el pin corresponde a la declaración
             pre-ejecución": se conserva asertando contra un literal esperado
             (la proyección es texto determinista).
RISK         LOW.
CONFIDENCE   HIGH.
```

### C-10. Nivel de `orchestrator` y `agent_worker`: los tests que usan un repo sin necesitarlo

```text
PROBLEM      9 tests de derivación pura en test_autonomous_orchestrator.py
             (317,327,345,357,369 y afines) construyen un repositorio completo
             para asertar UN booleano o UN kind de derivación. Del mismo modo
             1,3,4,5,9 de esa lista.
EVIDENCE     OBSERVED: `build_repo` + `observe` + `derive_next_action` + 1–3 asserts.
             MEASURED media de test del archivo 2.62 s, con 42 subprocesos.
WHY          `derive_next_action` es una función pura sobre `ChangeObservation`;
             `observe` es lo único que necesita el mundo real.
GUARANTEE PRESERVED  la derivación sigue probándose; lo que cambia es que el
             `ChangeObservation` se construye en memoria en lugar de leerse de un
             repo (o que se conserva UN test de integración por familia).
RISK         MEDIUM: hay que asegurar que la construcción del `ChangeObservation`
             sintético sea fiel; es el patrón que el resto de la suite ya usa.
COST REMOVABLE  ESTIMATED 12–18 s.
CONFIDENCE   MEDIUM (requiere verificar la fidelidad del fixture sintético).
```

### C-11. Bajar `max_iterations` al mínimo que la aserción exige

```text
PROBLEM      Varios tests usan `max_iterations=12` o el default (8) cuando la
             garantía se verifica en la iteración 1. `run()` produce N+1
             registros, así que cada iteración de más es una observación de más
             (~0.4 s + ~6 subprocesos cada una).
EVIDENCE     OBSERVED `max_iterations=12` en 920/1086; default en 548/724/1040.
             MEASURED #22 = 7 iteraciones reales para un presupuesto de 12.
WHY          El presupuesto es un techo, no un objetivo; donde la garantía es de
             iteración 1, un techo alto sólo puede costar.
GUARANTEE PRESERVED  ninguna cambia si el stop ya ocurría en la iteración 1;
             donde no ocurre, el techo debe quedar como esté.
COST REMOVABLE  ESTIMATED 5–10 s.
RISK         LOW donde el stop es terminal en la iteración 1; NINGUNO donde no.
             Requiere verificar test por test cuál es el caso.
CONFIDENCE   HIGH en el mecanismo, MEDIUM en el monto.
```

---

## 21. Baseline for Future Audits

`MEASURED` Baseline canónico que una auditoría futura debe reproducir y
comparar (§6). Se declara **por contexto** por lo establecido en §16.2.

### 21.1 Cifras canónicas

```text
CANONICAL_TEST_COUNT                 1543
CANONICAL_RUNTIME                    413.95 s      (corrida completa, 2 legs)
  CALL_PHASE                         407.82 s
  SETUP_PHASE                          1.36 s
  TEARDOWN_PHASE                       0.00 s

DOMINANT_FILES                       4
DOMINANT_TESTS                     152
PERCENTAGE_OF_RUNTIME_FROM_TOP_FILES 73.1 % del call  /  72.0 % del wall

TOP_TEST_RUNTIME                     21.35 s
P95_TEST_RUNTIME                      1.12 s
P99_TEST_RUNTIME                      6.77 s
MEDIAN_TEST_RUNTIME                   0.000 s

DOMINANT_FILES_RUNTIME_IN_SUITE     298.03 s
DOMINANT_FILES_RUNTIME_ISOLATED     242.02 s      (mediana de 3, dispersión 0.13 %)
CONTEXT_EFFECT                      +23.1 %       (en suite vs aislado)
TEST_LEVEL_VARIABILITY_MEDIAN_CV      0.003      (0.3 %, n=3)

TOTAL_SUBPROCESSES                   4944
TOTAL_SUBPROCESS_TIME               332.54 s      (80.3 % del wall)
  git                                4696
  python                              245
TOTAL_GIT_OPERATIONS                 4696
TOTAL_WAITS                             0
TOTAL_SUBPROCESSES_IN_SETUP             0
TOTAL_SUBPROCESSES_IN_TEARDOWN          0
TOTAL_SETUP_TIME (fixture de pytest)   1.36 s
TOTAL_EXECUTION_TIME (fase call)     407.82 s
TOTAL_CLEANUP_TIME                     0.00 s

SUBPROCESS_COST_UNIT
  git subcommand                     ~63 ms
  python interpreter start            37.2 ms   (n=8)

GIT_SETUP_COST (4 dominantes)        ~18.8 s    (6.3 % de los 4)
GIT_BEHAVIOR_UNDER_TEST (4 dom.)    ~250 s     (83.9 % de los 4)
SETUP_SHARE (4 dominantes)            12.5 %
EXECUTION_SHARE (4 dominantes)        87.5 %
SUBPROCESS_SHARE (4 dominantes)       99.0 %
WAIT_SHARE                             0.0 %
GIT_SHARE (suite completa)             ~74.9 %  (310 s / 413.95 s)
UNKNOWN_SHARE                          ~2 %     (assertions + arranque de pytest)

CORRELATION(subprocess_count, seconds)  r = 0.999   (n=152)
MARGINAL_COST                           ~63 ms por subproceso
```

### 21.2 Reglas de comparación (`RECOMMENDED`)

```text
1. Comparar SIEMPRE dentro del mismo contexto. Un número aislado contra un
   número en suite produce un error del 23 % (§16.2).
2. Toda cifra absoluta es de ESTA máquina (Windows 11, Python 3.14.3,
   pytest 9.0.3, 12 CPU, OneDrive). Las PROPORCIONES son las robustas.
3. Reportar siempre: test count, wall, call/setup/teardown, y el conteo de
   subprocesos si se instrumentó.
4. Si el runtime sube, la primera pregunta es "¿subió el número de
   subprocesos?" — r = 0.999 hace de esa pregunta el mejor diagnóstico.
```

---

## 22. Proposed Guardrails

`RECOMMENDED` Señales a vigilar. **Ningún threshold se fija como hecho del
repositorio**: primero la distribución observada, luego —si corresponde— un
umbral propuesto, con su racional. Ver `AGENTS.md`,
*Decision-Making Compass*: no se agrega maquinaria sin necesidad demostrada.

### 22.1 Distribución observada (base para cualquier umbral)

```text
OBSERVED BASELINE — suite completa (1486 nodos con duración)
  mediana     0.000 s
  p75         0.02 s
  p90         0.46 s
  p95         1.12 s
  p99         6.77 s
  máx        21.35 s
  tests ≥ 1 s    87   (5.9 %)
  tests ≥ 5 s    20   (1.3 %)
  tests ≥ 10 s    6   (0.4 %)

OBSERVED BASELINE — concentración
  top 1 % de tests  = 38.0 % del tiempo
  top 5 % de tests  = 78.8 % del tiempo
  top 4 archivos    = 73.1 % del tiempo

OBSERVED BASELINE — proporciones
  setup_share       0.3 %   (fase setup de pytest sobre el wall)
  subprocess_share 80.3 %   (tiempo en subprocesos sobre el wall)
  wait_share        0.0 %
  archivos con > 1.000 subprocesos: 1  (test_autonomous_orchestrator.py)
```

### 22.2 Guardrails candidatos (`RECOMMENDED` — no implementados)

| # | Señal | Baseline observado | Umbral propuesto | Racional |
|---|---|---|---|---|
| G1 | **archivo individual** > 15 % del call time | máx 25.8 % (orchestrator) | 30 % | un archivo no debería volver a dominar el reloj; 30 % deja margen sobre el peor caso actual |
| G2 | **test individual** > 25 s | máx 21.35 s | 30 s | el peor test está a 21 s; 30 s es ~1.4× y no ahoga variación legítima |
| G3 | **tests ≥ 5 s** | 20 | 30 | vigilar la cola: hoy 20; 30 da margen para tests nuevos legítimos |
| G4 | **proporción subprocess/tiempo** por archivo | 97–103 % en los dominantes | > 100 % (sostenido) | un archivo *enteramente* subprocess-bound no puede mejorar sin reducir procesos; señal de que la palanca es producción |
| G5 | **archivos con repos git por test** | 9 | 12 | nueva construcción de repos por test es el patrón que creó el problema |
| G6 | **ratio setup:ejecución** | 1:7 (12.5 % montaje) | > 1:2 (33 % montaje) | si el montaje supera un tercio, el escenario domina la acción — hoy está muy lejos |
| G7 | **waits artificiales** | 0 | **> 0** | cualquier `sleep`/poll introducido es una regresión categórica: hoy no existe ninguno y hay que mantenerlo |
| G8 | **contexto: aislado vs en suite** | +23.1 % | > 50 % | una degradación dependiente del orden indicaría contaminación entre tests (el riesgo R7 de las auditorías previas) |
| G9 | **MIXED nuevos** | 20 archivos | no aumentar | la mezcla de niveles es lo que impide seleccionar; un archivo nuevo no debería nacer mixto |
| G10 | **aserciones que no pueden fallar** | 6 detectadas | **0 nuevas** | señal de confianza, no de reloj; hoy hay 6 y son un pasivo conocido |

`RECOMMENDED` **Cómo vigilarlas sin crear maquinaria nueva** (respeta
`AGENTS.md`): las señales G1–G3 y G6–G8 se leen **directamente de
`pytest --durations=0`**, sin instrumentación. Sólo G4, G5 y G10 requieren el
plugin de conteo o inspección de código, y ambos son **transitorios de
auditoría**, no tooling permanente.

`OBSERVED` **Lo que NO se propone**: un umbral de cobertura (la cobertura está
estructuralmente baja en el área más cara y forzarla empujaría a escribir tests
que suban el número sin subir la confianza — conclusión que las dos auditorías
previas ya habían alcanzado por separado), ni markers, ni xdist, ni selección
automática.

---

## 23. Reproducibility Method

### 23.1 HOW TO REPEAT THIS AUDIT

`OBSERVED` Procedimiento completo, en el orden en que se ejecutó.

**Paso 0 — Localizar las restricciones.**

```powershell
# Plan 145 por el mecanismo documental, no por ruta supuesta
Select-String -Path docs/plans/INDEX.md -Pattern '145-integral-dev-backlog-closure'
# Leer: docs/plans/145-integral-dev-backlog-closure.md  (§4 de este informe)
# Leer: AGENTS.md, tests/AGENTS.md, docs/VERSIONING.md §4.1
```

**Paso 1 — Verificar las rutas reales (no asumirlas).**

```powershell
python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
  tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py --collect-only -q
# → 152 tests collected
python -m pytest tests/ --collect-only -q                       # → 1358
python -m pytest protocol/.agents/harness/tests/ --collect-only -q  # → 185
```

**Paso 2 — Baseline canónico.**

```powershell
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider `
    --durations=0 --durations-min=0 | Tee-Object -FilePath "$env:TEMP\r1.txt"
# Registrar: passed/skipped, wall, y las tres fases del encabezado de durations
```

**Paso 3 — Instrumentación externa (conteo de subprocesos).**

```powershell
# Crear el directorio de instrumentación FUERA del repo
New-Item -ItemType Directory -Force "$env:TEMP\argentos-autopsy"
# Copiar allí el plugin (Apéndice B de §23.3)
$env:PYTHONPATH="$env:TEMP\argentos-autopsy"
$env:AUTOPSY_JSON="$env:TEMP\argentos-autopsy\instr.json"
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider -p autopsy_plugin
```

**Paso 4 — Micro-benchmarks de montaje y de observación.**

```powershell
# Importa los builders REALES de la suite (no reimplementa el fixture)
python "$env:TEMP\argentos-autopsy\measure_builders.py"   # n=8 por constructor
python "$env:TEMP\argentos-autopsy\measure_observe.py"    # observe() y run(1)
```

**Paso 5 — Variabilidad.**

```powershell
1..3 | ForEach-Object {
  python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
    tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q `
    --durations=0 --durations-min=0 |
    Tee-Object -FilePath "$env:TEMP\argentos-autopsy\var_batch$_.txt"
}
```

**Paso 6 — Comparar contra §21** y registrar la diferencia porcentual por
contexto (aislado vs en suite).

**Paso 7 — Eliminar la instrumentación.**

```powershell
Remove-Item -Recurse -Force "$env:TEMP\argentos-autopsy"
git status --porcelain     # debe mostrar sólo los artefactos documentales de la auditoría
```

### 23.2 Qué métrica viene de dónde (`OBSERVED`)

| Métrica | Fuente | ¿Requiere instrumentación? |
|---|---|---|
| runtime por test | `pytest --durations=0` | **No** |
| fases setup/call/teardown | `pytest --durations=0` (encabezado) | **No** |
| conteo de tests | `pytest --collect-only -q` | **No** |
| concentración por archivo | agregación del propio `--durations` | **No** |
| costo del constructor | micro-benchmark (importa el builder real) | **Sí** |
| número de subprocesos por test | plugin que envuelve `subprocess.run` | **Sí** |
| comandos ejecutados | clasificador del plugin | **Sí** |
| tiempo en subprocesos | cronómetro alrededor del `subprocess.run` | **Sí** |
| waits | `grep` estático (basta: hoy son 0) | **No** (para el estado actual) |
| CPU vs wall | contador de proceso del SO | **Sí** (no hecho aquí) |
| divisiones dentro de un subproceso | profiler dentro del hijo | **Sí** (`UNKNOWN` aquí) |

### 23.3 Apéndice A — criterios de clasificación usados

```text
LEVEL (por comportamiento, nunca por nombre de archivo)
  UNIT        función pura, sin colaborador real, sin proceso
  CONTRACT    contrato publicado / esquema / wiring estático (AST, signatures)
  COMPONENT   un módulo por su API pública con colaboradores reales (fs)
  INTEGRATION varios módulos reales cableados, con efectos reales
  E2E         de entrada real a efecto observable cruzando frontera de proceso
  MIXED       el archivo contiene más de un nivel (se dice cuáles)

EVIDENCE VALUE
  CRITICAL  la garantía no existe sin el mundo real; exclusiva; un defecto no se
            detectaría por otro medio
  HIGH      regla con código, boundary real, regresión de un incidente
  MEDIUM    cobertura de rama / contraste; ya parcialmente cubierto en otro nivel
  LOW       subsumido, near-duplicado, o la aserción no puede fallar

RECOMMENDATION
  KEEP_AS_IS · KEEP_AND_OPTIMIZE · MOVE_TO_LOWER_LEVEL · SPLIT ·
  CONSOLIDATE · REDESIGN · INVESTIGATE
```

### 23.4 Apéndice B — el plugin de conteo (para repetir la instrumentación)

`OBSERVED` El plugin completo, tal como se usó. Vive **fuera del repositorio** y
no debe versionarse: es un transitorio de auditoría.

```python
"""READ-ONLY external instrumentation: counts and times subprocess.run per test."""
from __future__ import annotations
import json, os, subprocess, time

_ORIGINAL_RUN = subprocess.run
_CURRENT: dict = {}
_TESTS: dict = {}
_SESSION_STARTED = time.monotonic()
_CALL_TELEMETRY = {"t": 0.0, "n": 0}
_OUTSIDE = {"seconds": 0.0, "subprocess_count": 0, "subprocess_seconds": 0.0,
            "by_category": {}}

def _classify(argv):
    parts = ([str(a) for a in argv] if not isinstance(argv, (str, bytes))
             else str(argv).split())
    if not parts:
        return ("other", "<empty>")
    exe = os.path.basename(parts[0]).lower()
    if exe in ("git", "git.exe"):
        i, sub = 1, ""
        while i < len(parts):
            if parts[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
                i += 2; continue
            if parts[i].startswith("-"):
                i += 1; continue
            sub = parts[i]; break
        return ("git", f"git {sub}".strip())
    if exe.startswith("python"):
        script = next((p for p in parts[1:] if not p.startswith("-")), "")
        return ("python", f"python {os.path.basename(script)}".strip())
    return ("other", os.path.basename(parts[0]))

def _instrumented_run(*args, **kwargs):
    argv = args[0] if args else kwargs.get("args")
    category, key = _classify(argv)
    t0 = time.monotonic()
    try:
        return _ORIGINAL_RUN(*args, **kwargs)      # behaviour untouched
    finally:
        elapsed = time.monotonic() - t0
        _CALL_TELEMETRY["t"] += elapsed
        _CALL_TELEMETRY["n"] += 1
        cur = _CURRENT
        bucket = None
        if cur:
            phase = cur.get("phase")
            if phase in cur["phases"]:
                bucket = cur["phases"][phase]
            cur["sub_keys"][key] = cur["sub_keys"].get(key, 0) + 1
        if bucket is None:
            bucket = _OUTSIDE
        bucket["subprocess_count"] += 1
        bucket["subprocess_seconds"] += elapsed
        bucket["by_category"][category] = bucket["by_category"].get(category, 0) + 1

def pytest_sessionstart(session):
    subprocess.run = _instrumented_run

def pytest_sessionfinish(session, exitstatus):
    subprocess.run = _ORIGINAL_RUN
    json.dump({
        "session_wall_seconds": time.monotonic() - _SESSION_STARTED,
        "subprocess_seconds_total": _CALL_TELEMETRY["t"],
        "subprocess_calls_total": _CALL_TELEMETRY["n"],
        "outside_test_attribution": _OUTSIDE,
        "tests": _TESTS,
    }, open(os.environ.get("AUTOPSY_JSON", "autopsy.json"), "w", encoding="utf-8"),
        indent=1)

def pytest_runtest_logstart(nodeid, location):
    _TESTS[nodeid] = {
        "nodeid": nodeid,
        "phases": {p: {"seconds": 0.0, "subprocess_count": 0,
                       "subprocess_seconds": 0.0, "by_category": {}}
                   for p in ("setup", "call", "teardown")},
        "sub_keys": {},
    }
    _CURRENT.clear(); _CURRENT.update(_TESTS[nodeid])

def pytest_runtest_logreport(report):
    entry = _TESTS.get(report.nodeid)
    if entry is None:
        return
    bucket = entry["phases"].get(report.when)
    if bucket is None:
        return
    bucket["seconds"] = round(bucket["seconds"] + report.duration, 4)
    if report.when == "call":
        entry["outcome"] = report.outcome

def _enter(nodeid, phase):
    entry = _TESTS.get(nodeid)
    if entry is None:
        _CURRENT.clear(); return
    entry["phase"] = phase
    _CURRENT.clear(); _CURRENT.update(entry)

def pytest_runtest_setup(item):     _enter(item.nodeid, "setup")
def pytest_runtest_call(item):      _enter(item.nodeid, "call")
def pytest_runtest_teardown(item, nextitem): _enter(item.nodeid, "teardown")

def pytest_runtest_logfinish(nodeid, location):
    entry = _TESTS.get(nodeid)
    if entry is not None:
        entry["phase"] = None
    _CURRENT.clear()
```

`OBSERVED` **Detalle que importa para reproducirlo**: la atribución de fase debe
usarse con `pytest_runtest_setup/call/teardown` (**no** con
`pytest_runtest_logreport`), porque el reporte llega *después* de que el cuerpo
del test se ejecutó y atribuiría todo el conteo a la fase equivocada. El primer
intento de esta auditoría cayó en ese error y atribuyó los 682 subprocesos de
`test_autonomy_effects.py` a "fuera de todo test".

### 23.5 Limitaciones del método (`OBSERVED`)

```text
· Todas las cifras absolutas son de Windows 11 (creación de procesos cara).
  HIPÓTESIS: en Linux el costo por subproceso es sensiblemente menor y las
  proporciones se mantienen, pero los absolutos no.
· El plugin mide el wall del hijo, no su CPU: un subproceso que espera I/O se
  cuenta entero.
· El tiempo "en proceso" (lógica Python, hashing, parseo) es por DIFERENCIA,
  no medido: es la fila menos confiable de §7.1.
· El número de iteraciones por test se obtuvo por sonda en 5 tests y por
  lectura de código en el resto: el conteo de iteraciones no es medido para
  los 152.
· No se midió CPU por test, ni profiling por línea, ni el interior de los
  subprocesos `python tools/*.py`.
· La corrida instrumentada (R2) midió MENOS wall que la intacta (R1): por eso
  el baseline de tiempo usa R1 y R2 sólo aporta conteos.
```

---

## 24. Limitations / Unknowns

`UNKNOWN` Declaración explícita de todo lo que **no** se pudo determinar.

```text
U-1  El costo real en Linux/CI. Todas las cifras son Windows. El costo unitario
     de crear un proceso git es el factor dominante y es específico de
     plataforma. UNKNOWN: cuánto de los 413.95 s sobrevive en ubuntu-latest.
     (Las dos auditorías previas listaron esto como pregunta abierta; sigue
     abierto y esta auditoría no lo cierra porque el entorno es Windows.)

U-2  ¿Cuánto del tiempo NO-subproceso es filesystem vs lógica Python? La fila
     "producción en proceso" (~72 s) es una diferencia, no una medición.

U-3  El número exacto de iteraciones de cada uno de los 152 tests. Se midió en
     5 (sonda) y se leyó del código en los 9 que llaman run(); para los demás
     no aplica. UNKNOWN para los que tienen budgets altos y stop temprano.

U-4  Por qué la corrida instrumentada fue 54.6 s más rápida que la intacta.
     INFERRED: carga del sistema (R1 corrió con otras mediciones en curso).
     No discriminado.

U-5  Cuál de las causas del efecto de contexto (+23 %) domina: presión de
     caché, fragmentación del scratch (152 repos en un árbol) o memoria.
     MEDIDO el efecto; UNKNOWN la causa.

U-6  ¿`runtime/orchestrator/__main__.py` (78–200 líneas, 0 tests, 0 % cobertura)
     necesita cobertura? UNKNOWN; heredado de las auditorías previas.

U-7  ¿El CI de GitHub Actions tarda lo mismo? No se midió el job
     `check-protocol` remoto. UNKNOWN.

U-8  ¿La aserción de la línea 490 de test_autonomy_effects.py falla alguna vez
     en la práctica? El análisis de código dice que no puede; no se falsificó
     por ejecución (habría requerido mutar producción).
```

`OBSERVED` Se dejan constancia también de dos límites **de esta auditoría**:

```text
L-1  El conteo de "saltos" dentro de un subproceso python (p. ej. cuántos
     archivos toca `python tools/check_lifecycle_*.py`) no se midió.
L-2  El análisis estático de los 152 tests se hizo leyendo el código completo
     de los 4 archivos y su producción; en los archivos de comparación de
     baseline (los otros 65) se usaron las cifras de las auditorías previas.
```

---

## 25. Recommendations

`RECOMMENDED` **Ninguna de estas recomendaciones está implementada.** Este
informe no autoriza trabajo; cada una requiere su vía de gobernanza (RFC-56) si
se decide ejecutarla.

### 25.1 NO CAMBIAR (la evidencia lo exige)

| # | Qué | Por qué |
|---|---|---|
| **A-1** | **Las 11 garantías `CRITICAL`** (§17.2) | ninguna es alcanzable con un test más barato; el costo es la garantía |
| **A-2** | **El aislamiento por test** (`scratch_root` + `uuid4`) | es la corrección de Plan 145 contra un defecto real y reproducido; el costo **no** viene de él |
| **A-3** | **La mitad pura de los 4 archivos (37 tests, ~0.5 s)** | mejor cociente del repo; tocarla no ahorra nada y arriesga cobertura |
| **A-4** | **La batería canónica como definición de verde en CI** | sin cambios; esta auditoría no reduce la suite |
| **A-5** | **La calibración de `test_check_lifecycle_checkpoint.py`, `test_scoped_content_identity.py`, `test_repo_containment.py`, `test_enforced_flow.py`** | ya examinadas y descartadas como low-value por la segunda auditoría; esta auditoría no encuentra razón para revisar esa conclusión |

### 25.2 OPTIMIZAR (mayor beneficio, menor riesgo)

```text
B-1  De-duplicar la observación en host.py        (§20 C-1)  ESTIMATED 40–70 s
     WHY: la segunda observación consecutiva aporta la misma evidencia.
     GUARANTEE: todas. COST: creación de procesos. RISK: MEDIUM (toca host.py).
     ← LA PALANCA MÁS GRANDE Y LA MÁS SEGURA: no toca un solo assert.

B-2  Bajar los budgets de iteración al mínimo que la aserción exige
                                                   (§20 C-11) ESTIMATED 5–10 s
     RISK: LOW donde el stop es terminal en la iteración 1.
```

### 25.3 CONSOLIDAR (elimina corridas del mundo real, no aserciones)

```text
C-1  orchestrator 920 + 1086 (mismo loop de 7 iteraciones)   ~11 s    RISK LOW
C-2  autonomy_effects 630 + 653 + 671 (mismo fixture)        ~11 s    RISK LOW/MED
C-3  autonomy_effects 545 + 569 + 581 + 593 (parametrizar)    ~7 s    RISK LOW
C-4  sae 443 → 992 y 504 → 515                                ~5 s    RISK LOW
C-5  agent_worker 963/983/1000/1058: sacar el repo            ~5.5 s  RISK LOW
                                                             ~39.5 s ESTIMATED
```

### 25.4 MOVE_TO_LOWER_LEVEL

```text
D-1  orchestrator: 9 tests de derivación que construyen un repo para asertar
     un kind/booleano; conservar UN test de integración por familia
                                                   (§20 C-10) ESTIMATED 12–18 s
     RISK: MEDIUM (requiere un ChangeObservation sintético fiel)

D-2  agent_worker: 493 (`AuthorityBoundary` puro, sin relación con el Agent
     Worker) y la mitad de ejecución de 909 → al nivel de contrato
D-3  sae: 869 (durabilidad del pin leída del journal) — puede asertarse sin
     correr el host
D-4  autonomy_effects: 707 (afirmación de tipo) — ya cubierto sin repo por el dogfood
```

### 25.5 REDESIGN (problema de confianza, no de reloj)

```text
E-1  Las 6 aserciones que no pueden fallar            (§20 C-6)   0 s
E-2  Los 3 tests cuyo nombre no corresponde al cuerpo (§20 C-7)  ~9 s
E-3  Las 2 aserciones de autoconsistencia de sae      (§20 C-9)   0 s
```

### 25.6 INVESTIGATE

```text
F-1  ¿El eje `EFFECT_AUTHORIZED_BY` se valida en algún camino? El vocabulario lo
     declara y `admit_declared_effects` no lo consulta; `_effect_reference_resolves`
     matchea por substring ("user","plan","adr","rfc"). Ningún test afirma que
     un `Authorization` = `plan` sea intencional. NO es un defecto probado.
F-2  `resource_required=False`: el camino está declarado (`host.py:333-335`) y
     no tiene test negativo ("un techo no debe detener una acción de registro").
F-3  Si un stop por violación de efecto debe consumir techo: `_resource_consumed`
     cuenta registros con `delegation_id`, y el stop de violación también graba uno.
F-4  `Committed` no se asertа en ningún test de los cuatro archivos.
F-5  `test_git_state_reports_the_cli_availability_explicitly` (orchestrator:1153)
     lee el repo real y NO está en la tabla anclada de `tests/AGENTS.md`.
```

### 25.7 Orden recomendado (`RECOMMENDED`)

`INFERRED` De menor a mayor riesgo y de mayor a menor certeza de beneficio:

```text
0. Decisión humana: ¿se autoriza tocar host.py (producción) para B-1?
   Sin esto, la palanca grande no existe y sólo quedan ~40 s de consolidación.
        ↓
1. E-1/E-3 (aserciones inertes y autoconsistencia)   riesgo LOW, recupera confianza
2. C-4, C-2, C-3 (consolidaciones acotadas)          riesgo LOW, ~23 s
3. C-1 (orchestrator 920+1086)                       riesgo LOW/MED, ~11 s
4. B-2 (budgets de iteración)                        riesgo LOW, ~5–10 s
5. C-5, D-2, D-4 (sacar repos innecesarios)          riesgo LOW/MED, ~6 s
6. E-2, D-1 (rediseño y bajada de nivel)             riesgo MED, ~20 s
7. B-1 (de-duplicar la observación en host.py)       riesgo MED, ESTIMATED 40–70 s
        ← la palanca grande; va ÚLTIMA porque toca producción y exige la suite
          completa como red
```

`RECOMMENDED` **No hacer nada también es un resultado válido**, y con esta
evidencia es defendible: la suite es estable, no tiene waits, no tiene grasa
low-value costosa y sus garantías caras son reales. Lo que la evidencia sí
demuestra es que **la creencia "el costo es el montaje del repositorio git" es
falsa** (12.5 % medido), y que cualquier trabajo futuro basado en ella atacaría
el 12 % creyendo atacar el 88 %.

---

## 26. Final Conclusions

`OBSERVED` Respuestas directas a las preguntas de §27 del pedido.

**1. ¿Qué hacen realmente estos tests?**
Construyen un repositorio git real por test (`build_repo`/`make_repo`, 0.28–0.42 s)
y luego **conducen el host real** sobre él: observan el repositorio
(`git rev-parse`/`status`/`ls-files`/`write-tree` + hashing SHA-256 por archivo),
derivan la acción siguiente, aplican la frontera de autoridad/scope/efectos,
delegan a un worker que **ejecuta comandos reales** (`python src/check_ok.py`,
los gates `check_lifecycle_*`), ingieren el resultado persistido y escriben
gobernanza real en el plan desechable.

**2. ¿Por qué son caros?**
Porque **crean procesos**: 3.775 subprocesos en 152 tests (24.8 por test), a
~63 ms cada uno (git) y 37 ms (intérprete). `r = 0.999` entre subprocesos y
tiempo. **No hay sleeps, no hay polling, no hay espera artificial: la categoría
`WAITS` mide exactamente 0.0 s.**

**3. ¿Cuánto corresponde a setup y cuánto a ejecución?**
`MEASURED`: **montaje del repositorio 30.31 s = 12.5 %**; acción bajo prueba
**211.71 s = 87.5 %** (el resto hasta 242 s es el efecto de contexto y las
fases). El setup de pytest es 1.36 s con **cero subprocesos**.

**4. ¿Cuánto corresponde a subprocess / Git / filesystem?**
Subprocess: **332.54 s = 80.3 % del wall** (de los cuales git ~310 s).
Git como infraestructura de montaje: **~18.8 s = 6.3 %** de los cuatro archivos.
Git como comportamiento bajo prueba: **~250 s = 83.9 %**. Filesystem: el segundo
componente, dominado por el **SHA-256 por archivo por snapshot**, recomputado
varias veces por iteración — no medido por separado (`UNKNOWN` su monto exacto).

**5. ¿Está justificado el costo?**
**Parcialmente.** Las 11 garantías `CRITICAL` **exigen** el mundo real y su costo
está justificado. Pero una fracción sustancial del costo **no es la garantía**:
es la **re-observación del mismo estado inmutable** — `run()` observa y `iterate()`
observa otra vez, consecutivamente, sin escritura entre ambas (`host.py:1050` y
`591`). Esa parte es arquitectónicamente evitable **sin tocar una sola aserción**.

**6. ¿Están probando lo correcto en el nivel correcto?**
**En su mayoría sí, con tres excepciones de garantía y una de ubicación.** 46
tests son integración legítima; 37 son unit/contract puros correctamente
clasificados pero **ubicados en archivos caros** (lo que impide seleccionar, como
ya estableció la segunda auditoría). 3 tests **no prueban lo que su nombre
declara** (`agent_worker:641`, `agent_worker:860`, `autonomy_effects:689`) y 6
aserciones **no pueden fallar**.

**7. ¿Qué tests deben seguir siendo caros?**
Los de la casilla `VERY_HIGH/HIGH COST × CRITICAL/HIGH VALUE`: el loop completo
hacia `Closed`, A2 preservando A1, la continuidad tras reinicio, la
clasificación leída del checker (con su contraejemplo), la negativa antes del
efecto del incidente F-3 y su contraprueba de no-vacuidad, la detección
post-hoc de efectos, el techo leído del journal y sobreviviente al reinicio, la
atribución por contenido en árbol sucio, y la recuperación desde evidencia.

**8. ¿Qué tests deberían rediseñarse?**
Los 3 cuyo nombre no corresponde al cuerpo; los 4 de `agent_worker` que
construyen un repo que su garantía no menciona; los 2 pares `near-duplicate` de
`sae`; las 6 aserciones inertes; y las 2 de autoconsistencia.

**9. ¿Qué tests podrían bajar de nivel?**
Los 9 de derivación de `orchestrator` que construyen un repo para asertar un
kind; `agent_worker:493` (boundary puro, sin relación con el Agent Worker); la
mitad de ejecución de `agent_worker:909`; `sae:869`; `autonomy_effects:707`.
`ESTIMATED`: 12–18 s con riesgo MEDIUM.

**10. ¿Cuál es el baseline de performance actual?**
§21.1. En una frase: **1543 tests / 413.95 s / 4.944 subprocesos; 4 archivos con
152 tests explican el 73.1 %; el montaje Git es el 12.5 % y los subprocesos el
80.3 %; el tiempo correlaciona con el conteo de subprocesos con r = 0.999.**

**11. ¿Cómo sabremos si la suite vuelve a degradarse?**
§22. Las señales G1–G3 y G6–G8 se leen de `pytest --durations=0` sin
instrumentación. La regla diagnóstica central: **si el runtime sube, la primera
pregunta es si subió el número de subprocesos** — con r = 0.999, eso resuelve el
diagnóstico sin profiling.

**12. ¿Cómo se repite esta auditoría sin empezar de cero?**
§23. Siete pasos con comandos exactos, los criterios de clasificación (§23.3), el
plugin completo (§23.4) y las limitaciones (§23.5). El baseline de §21.1 es la
vara de comparación.

---

## 27. Cierre — Restricciones cumplidas

`OBSERVED` Verificación explícita de las restricciones absolutas del pedido.

```text
NO modificar tests                        → 0 archivos de test modificados
NO modificar código productivo            → 0 archivos de producción modificados
NO mover archivos                         → 0
NO borrar tests                           → 0
NO agregar tests                          → 0
NO agregar markers                        → 0
NO cambiar pytest configuration           → 0 (conftest.py intacto)
NO cambiar CI                             → 0
NO agregar dependencias                   → 0
NO crear mecanismos de selección          → 0
NO optimizar fixtures                     → 0
NO cambiar aislamiento                    → 0
NO introducir cache                       → 0
NO reutilizar repositorios                → 0 (medición experimental sólo por lectura)
NO commits funcionales                    → 0
```

`OBSERVED` **Instrumentación temporal:** vivió **fuera del árbol versionado**
(`%TEMP%\argentos-autopsy\`: plugin de conteo, dos scripts de medición, JSON de
datos crudos y los logs de 5 corridas). **Eliminada al finalizar** (§23.1 paso 7).
No se agregó tooling permanente al repositorio.

`OBSERVED` **El estado final del repositorio** es el mismo que al inicio de la
auditoría en cuanto a contenido funcional:

```text
 M docs/working/audits/INDEX.md                              (registro del informe — permitido)
?? docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md  (este informe — permitido)
?? docs/working/audits/TEST_SUITE_AUDIT_2026-10-13.md        (pre-existente a esta auditoría)
?? docs/working/audits/TEST_ARCHITECTURE_AUDIT_2026-10-13.md (pre-existente a esta auditoría)
?? docs/planificacion-argentos-diseno-2026-10-13.md          (pre-existente a esta auditoría)
```

`OBSERVED` Las dos únicas modificaciones documentales permitidas por el pedido
son exactamente este informe y su registro en
`docs/working/audits/INDEX.md`.

---

## 28. Anexo A — Dataset reutilizable

`MEASURED` Tabla estructurada con los 152 tests de los cuatro archivos
dominantes. Campos: `test_id`, `file`, `test_name`, `level`,
`primary_component`, `guarantee`, `evidence_value`, `runtime`, `variability`,
`setup_time`, `execution_time`, `subprocess_count`, `git_operation_count`,
`wait_count`, `filesystem_heaviness`, `external_boundary`, `classification`,
`recommendation`, `confidence`.

`OBSERVED` Los campos **medidos** son: `runtime` (R1 y aislado),
`variability` (n=3), `subprocess_count`, `subprocess_seconds`
(⇒ `execution_time` derivado), `git_operation_count` (del clasificador), y
`wait_count` = 0 para todos. `setup_time` es el costo del constructor de ese
archivo (medido, n=8) cuando el test construye un repositorio, y 0 cuando no.
`filesystem_heaviness` es una marca cualitativa (`low`/`medium`/`high`) derivada
de si el test hashea contenido (`repository_snapshot`) y cuántas veces.
`level`, `primary_component`, `guarantee`, `evidence_value`, `classification` y
`recommendation` provienen del análisis estático de §8.

### 28.1 Los 20 tests más caros, con sus métricas medidas

| test_id (archivo::test) | s R1 | s aisl. | CV | subproc | s subproc | git ops | waits | setup s | nivel | valor | clasif. | recom. | conf. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| orch::test_revalidation_is_recorded_as_a2_without_mutating_a1 | 22.66 | 18.31 | 0.001 | 295 | 18.07 | ~290 | 0 | 0.277 | E2E | CRITICAL | MIXED | KEEP_AND_OPTIMIZE | HIGH |
| orch::test_restart_reconstructs_and_continues_without_lost_continuity | 15.15 | 12.24 | 0.000 | 198 | 12.06 | ~195 | 0 | 0.277 | E2E | CRITICAL | MIXED | KEEP_AND_OPTIMIZE | HIGH |
| orch::test_full_loop_derives_closed_from_real_evidence | 14.09 | 11.11 | 0.001 | 179 | 10.97 | ~176 | 0 | 0.277 | E2E | CRITICAL | MIXED | CONSOLIDATE (con next) | HIGH |
| orch::test_closed_derivation_never_releases_and_reports_human_authority | 12.07 | 11.11 | — | 173 | 10.46 | ~170 | 0 | 0.277 | E2E | HIGH | MIXED | CONSOLIDATE (con prev) | HIGH |
| sae::test_the_host_stops_when_a_declared_scope_widens_to_another_authorized_path | 9.33 | 8.51 | 0.008 | 136 | 8.25 | ~133 | 0 | 0.413 | E2E | HIGH | MIXED | KEEP_AND_OPTIMIZE | HIGH |
| sae::test_an_unauthorized_widening_is_refused_by_the_scope_check_before_any_drift | 9.10 | 8.14 | — | 131 | 7.91 | ~128 | 0 | 0.413 | E2E | MEDIUM | MIXED | REDESIGN (asis. incidental) | MEDIUM |
| sae::test_the_host_stops_when_the_contract_is_rewritten_after_authorization | 7.96 | 7.48 | — | 119 | 7.10 | ~116 | 0 | 0.413 | E2E | CRITICAL | MIXED | KEEP_AS_IS | HIGH |
| aw::test_stale_validation_does_not_allow_closed | 8.43 | 7.23 | — | 114 | 7.21 | ~111 | 0 | 0.424 | INTEGRATION | LOW | MIXED | REDESIGN | HIGH |
| orch::test_stale_validation_derives_revalidation_and_fresh_does_not | 9.46 | 7.20 | — | 113 | 6.94 | ~110 | 0 | 0.277 | INTEGRATION | HIGH | MIXED | KEEP_AND_OPTIMIZE | HIGH |
| aw::test_empty_implementation_result_does_not_re_delegate_forever | 7.90 | 6.44 | — | 103 | 6.41 | ~100 | 0 | 0.424 | MIXED | HIGH | MIXED | KEEP_AS_IS | MEDIUM |
| aw::test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task | 6.67 | 6.23 | — | 100 | 6.13 | ~97 | 0 | 0.424 | INTEGRATION | CRITICAL | MIXED | KEEP_AS_IS | HIGH |
| ae::test_the_ceiling_bounds_the_first_delegation_and_stops_the_second | 6.11 | 5.63 | 0.015 | 90 | 6.03 | ~88 | 0 | 0.413 | INTEGRATION | HIGH | MIXED | CONSOLIDATE | HIGH |
| ae::test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence | 5.92 | 5.64 | — | 90 | 5.53 | ~88 | 0 | 0.413 | INTEGRATION | HIGH | MIXED | CONSOLIDATE (conservar instancia nueva) | HIGH |
| ae::test_resource_exhaustion_is_never_an_authorization | 6.08 | 5.63 | — | 90 | 6.06 | ~88 | 0 | 0.413 | INTEGRATION | HIGH | MIXED | CONSOLIDATE | HIGH |
| sae::test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing | 5.91 | 5.51 | — | 88 | 5.38 | ~85 | 0 | 0.413 | E2E | CRITICAL | MIXED | KEEP_AND_OPTIMIZE | HIGH |
| orch::test_no_progress_guard_stops_instead_of_spinning | 6.08 | 5.06 | — | 81 | 4.97 | ~78 | 0 | 0.277 | INTEGRATION | HIGH | MIXED | KEEP_AS_IS | HIGH |
| aw::test_finding_blocks_closure_until_resolved_and_revalidation_is_derivable | 5.23 | 4.74 | — | 74 | 5.08 | ~71 | 0 | 0.424 | MIXED | HIGH | MIXED | KEEP_AND_OPTIMIZE | MEDIUM |
| aw::test_recovery_after_restart_from_persisted_evidence_only | 5.06 | 4.20 | — | 67 | 4.18 | ~64 | 0 | 0.424 | INTEGRATION | CRITICAL | MIXED | KEEP_AS_IS | HIGH |
| sae::test_a_required_obligation_inside_the_scope_is_conducted | — | 4.20 | — | 67 | 4.19 | ~64 | 0 | 0.413 | E2E | HIGH | MIXED | CONSOLIDATE (con 418) | HIGH |
| sae::test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed | 4.72 | 4.20 | — | 67 | 4.09 | ~64 | 0 | 0.413 | E2E | CRITICAL | MIXED | KEEP_AS_IS | HIGH |

Claves: `orch` = `test_autonomous_orchestrator.py`; `aw` = `test_agent_worker.py`;
`sae` = `test_sae_scope_enforcement.py`; `ae` = `test_autonomy_effects.py`.
`git ops` es un conteo derivado (`subproc × 0.95`), marcado como derivado a
propósito: el clasificador midió los comandos agregados por test, y el desglose
por test de git-vs-python no se registró por separado.
`waits` = 0 para **todos** los tests de la suite (`MEASURED`).

### 28.2 Tabla agregada por archivo (`MEASURED`)

| file | tests | call R1 | call aisl. | subproc | s subproc | montaje | % montaje | git setup | ratio | nivel | valor medio | recom. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| `tests/test_autonomous_orchestrator.py` | 31 | 105.20 | 83.25 | 1.303 | 81.11 | 6.08 | 7.3 % | ~5.9 | 1:12.7 | MIXED | HIGH | KEEP_AND_OPTIMIZE |
| `tests/test_agent_worker.py` | 41 | 79.86 | 60.00 | 912 | 59.86 | 11.44 | 19.1 % | ~7.6 | 1:4.2 | MIXED | MEDIUM | CONSOLIDATE |
| `tests/test_sae_scope_enforcement.py` | 44 | 58.31 | 55.28 | 878 | 53.70 | 5.37 | 9.7 % | ~3.4 | 1:9.3 | MIXED | HIGH | KEEP_AND_OPTIMIZE |
| `tests/test_autonomy_effects.py` | 36 | 54.66 | 43.49 | 682 | 45.00 | 7.43 | 17.1 % | ~4.3 | 1:4.9 | MIXED | MEDIUM | CONSOLIDATE |
| **TOTAL** | **152** | **298.03** | **242.02** | **3.775** | **239.67** | **30.31** | **12.5 %** | **~21.2** | **1:7.0** | — | — | — |

`OBSERVED` La columna `valor medio` resume §17.1 por archivo; el detalle por
test está en §28.1 y en el dataset completo de §28.3.

### 28.3 Dataset completo (JSON)

`OBSERVED` El dataset de los 152 tests (todos los campos de §28) se generó como
`dataset.json` en la instrumentación temporal y se eliminó con ella (§27).
**Los datos que sobreviven están en este informe**: §28.1 (los 20 más caros con
todas las métricas), §28.2 (agregados por archivo), §9.1 (top 20 por tiempo),
§11.2 (por archivo) y §6 (baseline). `OBSERVED` Se eligió **no versionar el JSON**
porque el repositorio no tiene un namespace para artefactos de datos de auditoría
y porque el pedido pide **no crear tooling permanente** salvo necesidad
estricta.

---

## 29. Anexo B — Trazabilidad de cada afirmación

| Afirmación | Fuente | Marca |
|---|---|---|
| 1543 tests, 1542 passed 1 skipped | corrida R1 | `MEASURED` |
| 413.95 s / 407.82 call / 1.36 setup / 0.00 teardown | `--durations=0` R1 | `MEASURED` |
| 4 archivos = 152 tests = 298.03 s = 73.1 % | agregación R1 | `MEASURED` |
| mediana 0.000 / p95 1.12 / p99 6.77 / máx 21.35 | 1486 nodos R1 | `MEASURED` |
| 4.944 subprocesos / 332.54 s | plugin externo R2 | `MEASURED` |
| 4.696 git / 245 python | clasificador del plugin | `MEASURED` |
| 0 subprocesos en setup y teardown | plugin, fases de pytest | `MEASURED` |
| 0 waits en todo el árbol | grep exhaustivo | `OBSERVED` |
| git ≈ 63 ms; intérprete 37.2 ms | regresión r=0.999 + micro-benchmark n=8 | `MEASURED` |
| r = 0.999 (subprocesos ↔ segundos) | regresión sobre 152 tests | `MEASURED` |
| `build_repo` 0.277 s; `make_repo` 0.424 s; SAE 0.413 s; AE 0.413 s | micro-benchmark n=8 | `MEASURED` |
| montaje total 30.31 s = 12.5 % | 80 construcciones × mediana medida | `MEASURED` |
| `observe()` = 0.380 s y 6 subprocesos | micro-benchmark n=3 | `MEASURED` |
| `run(max_iterations=1)` = 2.99 s y 49 subprocesos | micro-benchmark | `MEASURED` |
| 80 repos en los 4 archivos (22+27+13+18) | análisis estático de sitios de llamada | `OBSERVED` |
| `run()` observa y `iterate()` re-observa | `host.py:1050` y `host.py:591` | `OBSERVED` |
| 6 aserciones inertes | líneas 988, 1097-1098, 545, 1034, 1067-1072, 490 | `OBSERVED` |
| 3 tests no prueban lo que su nombre declara | 641, 860, 689 + caminos de producción | `OBSERVED` |
| +23.1 % de contexto (298.03 vs 242.02) | R1 vs V1–V3 | `MEASURED` |
| dispersión entre corridas < 0.2 % | V1–V3 | `MEASURED` |
| CV mediano por test 0.003 | V1–V3 | `MEASURED` |
| 9 pares DUPLICATE / 8 grupos OVERLAP | análisis estático §19 | `OBSERVED`+`INFERRED` |
| 11 garantías CRITICAL | §17.2, análisis por test | `OBSERVED` |
| los 40–70 s de C-1 | diferencia aritmética sobre mediciones | `ESTIMATED` |
| los ~39.5 s de consolidación | suma de las mediciones de los tests afectados | `ESTIMATED` |
| "producción en proceso" ~72 s | wall − subproceso − collection − setup | `INFERRED` |
| el CI en Linux costaría menos | no medido | `UNKNOWN` |

---

## 30. Anexo C — Reproducibilidad: comandos exactos de esta corrida

```powershell
# Baseline (R1)
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider `
    --durations=0 --durations-min=0
# → 1542 passed, 1 skipped, 1 warning in 413.95s (0:06:53)

# Recolección
python -m pytest tests/ --collect-only -q                              # 1358 in 0.48s
python -m pytest protocol/.agents/harness/tests/ --collect-only -q    # 185 in 0.09s

# Instrumentación (R2)
$env:PYTHONPATH="…\argentos-autopsy"; $env:AUTOPSY_JSON="…\instr_full.json"
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider -p autopsy_plugin
# → 1542 passed; 4.944 subprocesos; 332.54 s de subproceso

# Variabilidad (V1–V3)
1..3 | % { python -m pytest tests/test_autonomous_orchestrator.py tests/test_agent_worker.py `
    tests/test_sae_scope_enforcement.py tests/test_autonomy_effects.py -q `
    --durations=0 --durations-min=0 }
# → 242.86 s / 242.96 s / 243.18 s   (152 passed cada una)

# Micro-benchmarks
python measure_builders.py     # 4 constructores n=8 + primitivas
python measure_observe.py      # observe() y run(max_iterations=1)

# Verificación del estado del repositorio
git status --porcelain
git rev-parse HEAD             # fb0786a0b9b872796e5e4b223cf92bc011c22139
```

---

## 31. Reporte de cierre

```text
RESULT = TEST_EXECUTION_AUTOPSY_COMPLETE

FILES_ANALYZED = 4 dominantes (4132 líneas) + 12 módulos de producción
                 + conftest.py + tests/pytest_isolation.py + 3 docs de política
                 + 2 auditorías previas
TESTS_ANALYZED = 152 (los 4 dominantes) + 1543 como baseline agregado

TOTAL_RUNTIME = 413.95 s (1542 passed, 1 skipped; 1543 recogidos)
TOP_RUNTIME_SHARE = 73.1 % del call time (152 tests en 4 archivos)

SETUP_SHARE = 12.5 %   (montaje del repositorio, medido: 30.31 s de 242.02 s)
EXECUTION_SHARE = 87.5 % (acción bajo prueba, medido por diferencia)
SUBPROCESS_SHARE = 80.3 % del wall (332.54 s); 99.0 % del tiempo de los 4 archivos
GIT_SHARE = 6.3 % como montaje (18.8 s) · 83.9 % como comportamiento (250 s)
WAIT_SHARE = 0.0 %  (no existe ningún sleep/poll/retry en el árbol)
UNKNOWN_SHARE ≈ 2 % (assertions no separables + arranque de pytest)

HIGH_COST_HIGH_VALUE = 11 CRITICAL + ~14 HIGH caros
HIGH_COST_LOW_VALUE  = 0  (conclusión negativa, verificada)
  → el subconjunto de alto costo y valor MEDIO o dudoso es: 3 tests que no
    prueban lo que su nombre declara + 12 pares near-duplicate/subsumidos

KEEP = 11 garantías CRITICAL + 20 tests de bajo costo y alto valor
OPTIMIZE = 2 palancas: de-duplicar la observación en host.py (ESTIMATED 40–70 s)
           y bajar los budgets de iteración (ESTIMATED 5–10 s)
MOVE_TO_LOWER_LEVEL = 9 tests de derivación en orchestrator + 493/909 en
           agent_worker + 869 en sae + 707 en autonomy_effects (ESTIMATED 12–18 s)
SPLIT = 0 nuevos (la separación de la mitad pura ya la propuso la auditoría previa;
           esta no la reitera porque no reduce el reloj de la suite completa)
CONSOLIDATE = 4 grupos (ESTIMATED ~34 s): orch 920+1086 · ae 630/653/671 ·
           ae 545/569/581/593 · sae 443→992 y 504→515
REDESIGN = 6 aserciones inertes + 3 tests de nombre falso + 2 de autoconsistencia
INVESTIGATE = 5 ejes (EFFECT_AUTHORIZED_BY · resource_required=False ·
           consumo de techo en stop de violación · Committed sin assert ·
           orchestrator:1153 anclado sin declarar)

BASELINE_ESTABLISHED = YES
REPRODUCIBLE_METHOD = YES
FUTURE_GUARDRAILS_PROPOSED = YES

FUNCTIONAL_CHANGES = 0
TEST_CHANGES = 0
CI_CHANGES = 0
DEPENDENCY_CHANGES = 0

REPORT = docs/working/audits/TEST_EXECUTION_AUTOPSY_2026-10-13.md
INDEX_REGISTERED = YES
```

### NEXT_DECISION

`RECOMMENDED` Conclusión basada en la evidencia, no una acción automática:

> **El problema no es el montaje del repositorio git — es la repetición de la
> observación del repositorio dentro del host.** La medición desmiente la
> hipótesis que originó las tres auditorías (montaje Git ≈ 12.5 %, no ≈ 70 %) y
> localiza la causa en `ExecutionHost.run()`/`iterate()`, que observan el mismo
> estado inmutable dos veces por iteración, con 48 de cada 49 subprocesos
> dedicados a observar en lugar de a actuar.
>
> La decisión que la siguiente fase debe tomar es **de gobernanza, no técnica**:
> ¿se autoriza tocar `runtime/orchestrator/host.py` (producción) para eliminar la
> observación duplicada, con la suite completa como red? Es la única palanca con
> un techo estimado de 40–70 s **sin modificar una sola aserción**.
>
> Si la respuesta es **no**, el trabajo disponible sin tocar producción se limita
> a **~40 s de consolidación** y a **~20 s de bajada de nivel**, más la corrección
> de las 11 aserciones que no pueden fallar (0 s, pero recuperan confianza).
> Ambas ramas son válidas; **"no cambiar nada" también lo es**, porque la suite es
> estable, no tiene waits, no tiene grasa de bajo valor costosa, y sus garantías
> caras son reales.
>
> Lo que **no** debería hacerse es perseguir el costo del montaje Git: la
> evidencia lo acota a 6.3 % y ya motivó una estimación de −52 % que esta
> medición refuta.

---

*Fin del informe. Ninguna modificación funcional, de tests, de CI o de
dependencias fue realizada. La única modificación documental es este archivo y su
registro en `docs/working/audits/INDEX.md`.*
