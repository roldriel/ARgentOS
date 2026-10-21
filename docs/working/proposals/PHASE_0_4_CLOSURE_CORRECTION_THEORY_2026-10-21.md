# Phase 0.4 — Corrección de la clausura: implementación teórica, ataques y estado final esperado

**Naturaleza documental:** Working / design record — **no normativo**, provenance de la corrección. Registra el ciclo PLAN → IMPLEMENTACIÓN TEÓRICA → ESTADO HIPOTÉTICO → ATAQUE → CORRECCIÓN → ESTABILIDAD que precede a la implementación real del Plan 173.
**Fecha:** 2026-10-21.
**Autoridad:** instrucción directa del mantenedor (2026-10-21). El documento no decide nada por sí mismo; la ejecución vive en `docs/plans/173-phase-0-4-closure-correction.md`.
**Baseline:** `dev` = `master` = `f77cd3f`; dos untracked del usuario. La implementación real se ejecuta en `dev`.

---

## 0. Método y criterio

```text
PLAN → TEORÍA #1 → EXPECTED_FINAL_STATE #1 → ATAQUE #1
     → TEORÍA #2 → EXPECTED_FINAL_STATE #2 → ATAQUE #2
     → TEORÍA #3 (final) → EXPECTED_FINAL_STATE #3 → ATAQUE #3
     → ESTABLE → IMPLEMENTACIÓN REAL → COMPARACIÓN → VALIDACIÓN → CIERRE
```

Un problema teórico se registra con `THEORETICAL_FINDING`, `CAUSE`, `IMPACT`, `CORRECTION`, `AFFECTED_ITEMS`, `AFFECTED_FILES`, `NEW_EXPECTED_EVIDENCE`. La estabilidad exige `NEW_PROBLEMS = 0` en una pasada completa además de los ocho contadores en cero.

**Sondas empíricas ejecutadas antes de teorizar** (read-only, sobre el estado real):

| Sonda | Resultado |
|---|---|
| INDEX→archivo con formas de fila por namespace | planes 172 filas / 0 missing; RFC 87 / 0; ADR 116 / 0 |
| INDEX→archivo con «cualquier token `.md`» (diseño ingenuo) | 15 falsos positivos (fechas `2026-08-16.md`, RFCs citadas en tablas de planes) |
| Matriz ENF contra reglas candidatas | 12 filas; regla estricta ENF-002 marcaría `Determinable authorization` (agent + human); regla acotada: 0 flags |
| C-2 con baseline `git log -S` sobre 68 planes cerrados | 25 planes con commits posteriores fuera de la región de metadatos → regla de historia **ruidosa**, descartada |
| Lifecycle: 2.º uninstall / doctor ×2 / 2.º recover | `NOOP`, `valid` determinista, `NOOP` («no operation journal present») |
| `harness/tests` en `origin/dist` | 14 archivos: la suite **sí** se distribuye → todo cambio de tests del payload es cambio de payload |

---

## 1. Implementación teórica #1 (diseño ingenuo)

| Ítem | Cambio propuesto (resumen) |
|---|---|
| A · D-0.3-12 / FM-05 / R-03 | Nuevo checker `tools/check_post_close_integrity.py`: compara el texto del plan en el working tree con `git show HEAD:<plan>` y marca **cualquier** diferencia como ANOMALY. |
| B · G-07 / FM-07 / D-0.3-13 / R-04 | `check_plan_structure.py`: recorre cada celda de cada tabla de los tres INDEX y verifica que todo token `*.md` exista. |
| C · G-08 | Los tres tests de idempotencia se agregan dentro del commit del Plan 173. |
| D · G-04 | Nuevo checker ENF estricto (`Verifiable` ⇒ herramienta externa o attestation). |
| E · FM-10 / DOC-04 | Se corrige sólo la frase `origin/dist` de `docs/VERSIONING.md` §9. |
| F · inventario | Se editan en sitio las filas de los 11 ítems en `§B`, sin provenance. |
| G · identidad de Plan 172 | Se corrigen los literales del Anchor del Plan 172 en el propio Plan 172. |
| H · cierre del Plan 173 | Un único commit; la identidad se calcula antes de la validación final y, si no cambió el valor, se reutiliza el literal. |

### EXPECTED_FINAL_STATE #1

- 11 ítems reclasificados; 22 residuales.
- `check_plan_structure` con la regla amplia.
- Un checker ENF estricto en la batería.
- Plan 172 con literales corregidos.
- Un commit de Plan 173 con la identidad declarada.

---

## 2. Ataque adversarial #1

### TF-01 — La identidad vuelve a quedar stale (el fallo que invalidó Plan 172)

- **CAUSE:** H calcula la identidad antes de la validación final y reutiliza el literal; cualquier edición posterior a un archivo del scope (p. ej. un ajuste del inventario o de un test) cambia el delta.
- **IMPACT:** `DECLARED_SCOPED_DELTA ≠ RECOMPUTED_SCOPED_DELTA`; el cierre sería inválido otra vez.
- **CORRECTION:** patrón de dos commits: A (implementación, todos los archivos del scope finales) y B (sólo el Plan, excluido del scope). La identidad se calcula al final de A y se **recomputa como gate** después de B y en `HEAD`; si difiere, el cierre se detiene.
- **AFFECTED_ITEMS:** todos. **AFFECTED_FILES:** el Plan 173 y todo el scope. **NEW_EXPECTED_EVIDENCE:** `scoped_content_identity` ejecutado dos veces (A y HEAD) con igualdad.

### TF-02 — La corrección de G edita un artefacto cerrado

- **CAUSE:** corregir los literales del Plan 172 en el propio Plan 172.
- **IMPACT:** violación de `INV-04`/RFC-46/`E1-D4`; el cierre quedaría invalidado por historia.
- **CORRECTION:** el Plan 172 no se edita. El Plan 173 registra una **corrección post-close por referencia** que declara la identidad real de f77cd3f (tree `58cee8…`, delta `c2492e83…` sobre el scope del Plan 172) y supersede los literales sin reescribirlos.
- **AFFECTED_ITEMS:** P03-D-0.3-12, P03-FM-05, P03-R-03 y el cierre de Phase 0.4. **AFFECTED_FILES:** Plan 173 (sección post-close). **NEW_EXPECTED_EVIDENCE:** `git rev-parse 'f77cd3f^{tree}'` + delta recomputado + `git diff --name-status` entre el árbol declarado por el Plan 172 y f77cd3f.

### TF-03 — Comparación de texto crudo: CRLF/encoding

- **CAUSE:** A compara el working tree (posible CRLF por `core.autocrlf=true`) con `git show` (LF).
- **IMPACT:** ANOMALY en todos los planes cerrados en Windows; el gate se vuelve inútil.
- **CORRECTION:** comparar primero **blob ids** (`git hash-object --path=<rel>` vs `git rev-parse HEAD:<rel>`) y, si difieren, usar `git diff -U0 HEAD -- <rel>` (Git normaliza).
- **AFFECTED_ITEMS:** A. **AFFECTED_FILES:** `tools/check_lifecycle_checkpoint.py`. **NEW_EXPECTED_EVIDENCE:** test con finales de línea distintos y contenido igual → sin hallazgo.

### TF-04 — Falsos positivos sobre apéndices legítimos

- **CAUSE:** A marca cualquier diferencia; el corpus apenda findings/correcciones post-close y la política recomienda embeber el SHA del commit de cierre en el bullet «Commits de cierre» después de que exista.
- **IMPACT:** falsos positivos en usos legítimos; el gate bloquearía la operación normal.
- **CORRECTION:** permitir cambios cuyas líneas caigan en las secciones `### Findings`, `### Correcciones`, `### Pending decisions`, o dentro del bullet «Commits de cierre» del `## Checkpoint / cierre`; cualquier otra línea → ANOMALY. Clasificar ambos lados del diff (líneas viejas y nuevas).
- **AFFECTED_ITEMS:** A. **AFFECTED_FILES:** C-2. **NEW_EXPECTED_EVIDENCE:** fixtures: apéndice de finding → sin hallazgo; edición del objetivo → ANOMALY; edición del bullet de commits → sin hallazgo.

### TF-05 — La regla INDEX→archivo con «cualquier token» produce 15 falsos positivos

- **CAUSE:** B escanea toda celda de toda tabla; las tablas de planes citan fechas (`2026-08-16.md`) y RFCs (`62-…md`) que no son filas de plan.
- **IMPACT:** FAIL sobre el corpus real; CI roja.
- **CORRECTION:** formas de fila por namespace: planes → primera celda `` `NN-slug.md` ``; RFC → celda `` `docs/rfc/NN-slug.md` ``; ADR → primera celda `[ADR-NN](NN-slug.md)`. Sonda: 0 missing.
- **AFFECTED_ITEMS:** B. **AFFECTED_FILES:** `tools/check_plan_structure.py`. **NEW_EXPECTED_EVIDENCE:** corpus real sin violaciones; fixtures de fila sin target.

### TF-06 — G-08 dentro del Plan 173 fuerza una versión y un tag

- **CAUSE:** C mete un cambio de `protocol/.agents/harness/tests/` en el commit del Plan 173; `docs/VERSIONING.md` §3: todo plan que toca el payload produce una versión propia, y un plan = una versión = un tag.
- **IMPACT:** release no autorizada o violación de §3; además el payload de `master` quedaría por delante de `dist`.
- **CORRECTION:** commit Clase C **separado y anterior**: tests-only, sin VERSION, sin tag, sin `dist`, registrado en `[Unreleased]`; el Plan 173 no toca el payload en su propio commit. El payload de `dev` queda pendiente de release; no se promueve.
- **AFFECTED_ITEMS:** G-08. **AFFECTED_FILES:** tests del payload + CHANGELOG. **NEW_EXPECTED_EVIDENCE:** commit Clase C con mensaje que declara clase/scope; `VERSION` sin cambios; `dist` sin cambios; suite del payload verde.

### TF-07 — El checker ENF estricto deja el corpus en rojo

- **CAUSE:** D exige herramienta o attestation para toda fila `Verifiable`; la fila `Determinable authorization … agent + human (authorization model)` no la nombra.
- **IMPACT:** CI roja; corregir el payload exigiría un cambio de protocolo + versión, fuera del scope.
- **CORRECTION:** regla acotada y declarada: ENF-001 completo (mecánico ⇒ mecanismo, no sólo agente); ENF-003 completo (declaración fail-open presente y no afirmación de control absoluto); ENF-002 estructural (toda fila `Verifiable*` declara una fuente de verificación y no es sólo humano). `LIMIT`: no decide la verdad de la clase (`INV-12`). Sin cambio de payload.
- **AFFECTED_ITEMS:** G-04. **AFFECTED_FILES:** `tools/check_enforcement_declarations.py`, tests. **NEW_EXPECTED_EVIDENCE:** matriz real 12/12 PASS; fixtures de fallo para las tres reglas.

### TF-08 — Editar el inventario sin provenance oculta la auditoría

- **CAUSE:** F cambia los estados en sitio.
- **IMPACT:** desaparece la traza de que la auditoría los había marcado `MISCLASSIFIED`; el inventario “siempre tuvo razón”.
- **CORRECTION:** sección `## Corrección Phase 0.4 (Plan 173)` con `ESTADO PREVIO → ESTADO NUEVO`, causa y evidencia; §D con los conteos finales; las filas de §B actualizadas apuntan a la corrección.
- **AFFECTED_ITEMS:** los 11. **AFFECTED_FILES:** inventario. **NEW_EXPECTED_EVIDENCE:** tabla de corrección + conteos 15/16/4/22/8.

### TF-09 — Corregir sólo una frase de §9 deja otra afirmación falsa

- **CAUSE:** E ignora que, con G-08, el payload de `dev` deja de ser idéntico a `dist`; la viñeta `dev` («no queda ningún cambio de payload sin publicar») pasa a ser falsa.
- **IMPACT:** contradicción interna de §9 (el mismo defecto que DOC-04 denuncia).
- **CORRECTION:** reconciliar §9 completo: `origin/dist` desde el tag `12.3.0` (`7f6b73f`), `master` = `12.3.0`, `dev` = `12.3.0` **con un cambio tests-only pendiente de release** (G-08), y `check_dist_sync` rojo en `dev` por diseño.
- **AFFECTED_ITEMS:** FM-10, DOC-04. **AFFECTED_FILES:** `docs/VERSIONING.md` §9. **NEW_EXPECTED_EVIDENCE:** lectura contra `origin/dist` y `git tag`; ninguna frase de §9 contradice Git.

### TF-10 — Verificación no canónica

- **CAUSE:** D añade un checker sin incorporarlo a §4.1 ni a CI.
- **IMPACT:** la verificación de ENF no corre en la batería canónica; G-04 seguiría sin verificación efectiva.
- **CORRECTION:** alta en §4.1 y en `.github/workflows/check-protocol.yml`; verificar que ningún test fija el número 7; actualizar el conteo en el reporte (8 repository checkers).
- **AFFECTED_ITEMS:** G-04. **AFFECTED_FILES:** `docs/VERSIONING.md` §4.1, CI. **NEW_EXPECTED_EVIDENCE:** el checker corre en la batería y en CI.

---

## 3. Implementación teórica #2

- A: R5 en C-2 (sin checker nuevo): blob ids + `git diff -U0`; regiones permitidas (findings/correcciones/pending) + bullet «Commits de cierre»; clasificación de ambos lados; key sobre **HEAD**; N/A si el plan no está en HEAD o Git no está disponible.
- B: `check_plan_structure` con formas por namespace.
- C: commit Clase C separado (tests-only, sin VERSION/tag/dist), release pendiente.
- D: checker ENF acotado + `LIMIT`, alta en §4.1 y CI.
- E: §9 reconciliado completo (incluye el estado pendiente del payload).
- F: inventario con sección de corrección y conteos finales.
- G: corrección post-close por referencia en el Plan 173 (Plan 172 intacto).
- H: dos commits (A/B), identidad al final de A y gate de recomputación en HEAD.
- I: el scope del Plan 173 incluye el archivo de tests del payload (ya final en el commit Clase C) y el documento de teoría.

### EXPECTED_FINAL_STATE #2 (valores verificables)

```text
INVENTORY_TOTAL = 65
RESOLVED = 15 · IMPLEMENTED = 16 · REJECTED_BY_DESIGN = 4
ACCEPTED_RESIDUAL_RISK = 22 · NON_ACTIONABLE_HISTORICAL = 8
MISCLASSIFIED = 0 · INSUFFICIENT_EVIDENCE = 0 · REAL_UNCLOSED_DEBT = 0

check_plan_citations: 25 históricas (baseline preservado)
check_plan_structure: PASS (2 GAP declarados 157/158) + 0 filas sin target
check_enforcement_declarations: PASS (12 filas)
check_invariants_equivalence: PASS (7/15 · 2/15 · 6/15)
C-1: ANOMALY=0 · C-2: ANOMALY=0 (+ R5 sin hallazgos) · C-3: ANOMALY=0
pytest tests/: baseline + tests nuevos
pytest protocol/.agents/harness/tests/: 204 + 3 = 207 passed, 1 skipped
```

---

## 4. Ataque adversarial #2

### TF-11 — La regla R5 se dispararía en el propio commit de cierre

- **CAUSE:** si R5 se evaluara contra el plan del *working tree* («declara Closed»), durante el commit B el plan ya declara Closed y difiere de HEAD (que no lo declaraba).
- **IMPACT:** ANOMALY falso en el cierre del propio Plan 173.
- **CORRECTION:** la condición «declara Closed» se evalúa sobre el **texto de HEAD**, no sobre el working tree; durante B, HEAD (commit A) no declara Closed y la regla queda inactiva. Existe fixture específico.
- **AFFECTED_ITEMS:** A. **FILES:** C-2.

### TF-12 — Clasificación de regiones incompleta

- **CAUSE:** mapear sólo las líneas nuevas deja pasar una **eliminación** de contenido gobernante.
- **IMPACT:** falso negativo (borrar el objetivo de un plan cerrado pasaría).
- **CORRECTION:** clasificar los rangos viejos (HEAD) y nuevos (working tree) de cada hunk; cualquiera fuera de las regiones permitidas → ANOMALY. Fixture de borrado.
- **AFFECTED_ITEMS:** A. **FILES:** C-2.

### TF-13 — Ruido en planes nuevos o sin Git

- **CAUSE:** R5 intenta leer `HEAD:<plan>` para planes que no están en HEAD (Plan 173 en A) o en un clon sin objetos.
- **IMPACT:** GAP/ANOMALY espurios.
- **CORRECTION:** si el plan no está en HEAD → N/A; si Git no está disponible → GAP advisory, nunca ANOMALY. Fixture.
- **AFFECTED_ITEMS:** A. **FILES:** C-2.

### TF-14 — Orden del commit Clase C y el scope

- **CAUSE:** si el commit Clase C se hiciera después de A, el archivo de tests del payload cambiaría después de calcular la identidad.
- **IMPACT:** delta stale.
- **CORRECTION:** orden fijo: Clase C → A (con el archivo ya final, incluido en el scope) → B. Gate de recomputación en HEAD.
- **AFFECTED_ITEMS:** C, G-08. **FILES:** orden de commits.

### TF-15 — Dogfood del checker ENF fuera de la tabla anclada

- **CAUSE:** el test que corre el checker sobre el payload real es un dogfood anclado; `tests/AGENTS.md` exige listarlo.
- **IMPACT:** incumplimiento de la carta de tests.
- **CORRECTION:** alta del dogfood en la tabla de `tests/AGENTS.md` y en el scope.
- **AFFECTED_ITEMS:** G-04. **FILES:** `tests/AGENTS.md`.

### TF-16 — El inventario quedaría con los ítems en §C.1

- **CAUSE:** los ítems implementados seguirían en la tabla de residuales aceptados.
- **IMPACT:** conteo incoherente (31 aceptados en §C.1 vs 22 en §D).
- **CORRECTION:** retirar de §C.1 las filas de los implementados; dejar R-06 (sin FM-10) y las filas genuinas; ajustar §D a 22.
- **AFFECTED_ITEMS:** inventario. **FILES:** inventario.

### TF-17 — La corrección post-close copiada de la auditoría

- **CAUSE:** usar los valores `58cee8…`/`c2492e83…` sin recomputarlos.
- **IMPACT:** evidencia no reproducida.
- **CORRECTION:** recomputar en la implementación con `git rev-parse 'f77cd3f^{tree}'` y `scoped_content_identity` sobre las 13 rutas del Plan 172, y registrar la salida.
- **AFFECTED_ITEMS:** G. **FILES:** Plan 173.

### TF-18 — N-9 con dos entradas en `[Unreleased]`

- **CAUSE:** dos commits agregan entradas al mismo bloque.
- **IMPACT:** riesgo de hunk fuera de `[Unreleased]`.
- **CORRECTION:** ambas entradas dentro de `[Unreleased]`; ejecutar el guard N-9 contra `HEAD` después de cada commit; secuencia de headings históricos idéntica.
- **AFFECTED_ITEMS:** C, E. **FILES:** CHANGELOG.

---

## 5. Implementación teórica #3 (final)

Idéntica a #2 con las correcciones TF-11…TF-18 incorporadas:
- R5 sobre HEAD + clasificación bidireccional + N/A/GAP.
- Clase C primero; A con el archivo del payload final; B sólo el Plan.
- Gate de recomputación de identidad en `HEAD` y contra el commit A.
- Inventario con corrección y §C.1 depurado.
- §9 completo, ENF en batería/CI, dogfood anclado, N-9 en cada commit.

### EXPECTED_FINAL_STATE #3

Además de los valores de #2:

```text
COMMIT_ORDER = [Clase C (payload tests), A (implementación), B (anchor/checkpoint)]
A_TREE = tree del commit A (estado validado)
DECLARED_STATE = A_TREE
DELTA(SCOPE_173) = recomputado en A y en HEAD (iguales)
PHASE_0_4_CLOSURE_STATE(f77cd3f) = 58cee8… ; DELTA(scope 172) = c2492e83…
PLAN_172_EDITED = NO
DIST_CHANGED = NO ; VERSION_CHANGED = NO ; TAGS_CREATED = 0
PROMOTION = NO (payload tests pendientes de release)
```

---

## 6. Ataque adversarial #3

| Vector | Comprobación | Resultado |
|---|---|---|
| Scope | ¿algún archivo fuera del scope? ¿`protocol/` fuera del commit Clase C? | 0 (el commit Clase C toca exactamente un archivo de tests; el resto es DEV) |
| Governance | ¿autoridad inventada? ¿Plan 172 editado? | 0 (instrucción + Clase B/C; Plan 172 intacto, corrección por referencia) |
| Lifecycle | ¿estados imposibles? ¿R5 se dispara en el cierre propio? | 0 (R5 key sobre HEAD; A no declara Closed) |
| Detection | ¿R5 detecta borrado y edición? ¿INDEX→archivo es bidireccional con el existente? ¿ENF detecta las tres? | Sí, con fixtures de ambos lados; LIMIT declarado |
| Idempotence | R5/ENF/INDEX→archivo son read-only; 1.ª/2.ª/3.ª ejecución idéntica | Sí (deterministas) |
| History | N-9; ningún plan/RFC/ADR cerrado editado | PASS |
| Boundary | `dist`/`VERSION`/`PROTOCOL_VERSION`/tags sin cambios; payload sólo tests Clase C | PASS |
| Regression | suites y checkers existentes | se ejecutan en la validación real |
| Closure | ¿puede repetirse el hallazgo de Plan 172? | No: identidad recomputada al final, delta estable, gate en HEAD |

**Concern residual declarado (no es un finding pendiente, es un límite del modelo):** un tree id de todo el repositorio no puede contener su propio literal. Por eso el Plan 173 sigue el modelo de tres identidades de `policies/validation-closure.md` §5: **estado validado** (tree del commit A), **estado de cierre** (el mismo par del anchor) y **árbol material del commit de cierre** (B, que sólo agrega el Plan, excluido del scope). La igualdad exigida se verifica como `ANCHOR_STATE == CHECKPOINT_STATE == tree(A)` y `DECLARED_DELTA == recomputado(A) == recomputado(HEAD)`. Declarar el tree de HEAD como estado validado sería falso: la validación consumió A.

```text
NEW_PROBLEMS = 0
UNRESOLVED_THEORETICAL_FINDINGS = 0
SCOPE_LEAKS = 0
GOVERNANCE_CONFLICTS = 0
LIFECYCLE_CONFLICTS = 0
EVIDENCE_CONFLICTS = 0
HISTORICAL_CONFLICTS = 0
ENFORCEMENT_OVERCLAIMS = 0
UNEXPECTED_REGRESSIONS = 0
THEORY_STABLE = YES
```

---

## 7. Hallazgos teóricos (resumen)

| ID | Iteración | Tema | Corrección |
|---|---|---|---|
| TF-01 | #1 | identidad stale otra vez | dos commits + gate de recomputación |
| TF-02 | #1 | editar Plan 172 | corrección post-close por referencia |
| TF-03 | #1 | CRLF/texto crudo | blob ids + `git diff` |
| TF-04 | #1 | falsos positivos post-close | regiones permitidas + bullet de commits |
| TF-05 | #1 | INDEX→archivo con cualquier token | formas por namespace |
| TF-06 | #1 | G-08 fuerza versión/tag | Clase C separada, release pendiente |
| TF-07 | #1 | ENF estricto deja el corpus rojo | regla acotada + LIMIT |
| TF-08 | #1 | inventario sin provenance | sección de corrección |
| TF-09 | #1 | §9 parcialmente corregido | reconciliación completa |
| TF-10 | #1 | verificación no canónica | §4.1 + CI |
| TF-11 | #2 | R5 en el commit propio | key sobre HEAD |
| TF-12 | #2 | borrados no clasificados | ambos lados del diff |
| TF-13 | #2 | planes nuevos/sin Git | N/A / GAP |
| TF-14 | #2 | orden Clase C/A/B | orden fijo |
| TF-15 | #2 | dogfood fuera de la tabla | alta en `tests/AGENTS.md` |
| TF-16 | #2 | §C.1 con ítems implementados | depurar §C.1 |
| TF-17 | #2 | identidad de f77cd3f copiada | recomputar |
| TF-18 | #2 | N-9 con dos entradas | guard por commit |

`THEORETICAL_FINDINGS_TOTAL = 18` · `THEORETICAL_FINDINGS_RESOLVED = 18` · `THEORETICAL_ITERATIONS = 3`.
