# Plan 114 — MVP de deliberación adversarial (convención DEV + primer dogfooding)

<!-- Promoción: este artifact nació como borrador en sessions/drafts/ (staging
ignorado por git) y fue promovido a docs/plans/ con el GO del mantenedor
registrado como H1 en ## Creación. -->

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-07 (borrador)
**RFC:** — (vía plan; sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (sin efecto en payload)
**Change Level:** L1 (docs-only; un área documental; sin impacto de release; sin impacto arquitectónico)
**Depende de:** — (el primer Trial consume la decisión pendiente registrada en el Plan 105, que está `Closed`; ver Step 3)
**Origen:** análisis de diseño D1 / D1-Review / D2 / D2-Review-Closure / D3 (no persistidos en el repositorio; ver `## Trazabilidad`) + decisión pendiente `<PLAN-105>` (elevación ADR de la arquitectura terminológica, diferida, no bloqueante) + `docs/plans/INDEX.md` (siguiente número libre: 114)

## Status

`Aprobado para ejecución` (GO del mantenedor: H1 = GO, 2026-09-09). Condición operacional de autorización:

- **`Status: Aprobado para redacción`** — habilita la redacción y la promoción del Plan (moverlo a `docs/plans/`, registrarlo en el INDEX). **No** habilita la ejecución de los Steps 1–12.
- **`Status: Aprobado para ejecución`** — es el **único** estado que habilita ejecutar los Steps 1–12. **Estado vigente.**
- Si existe GO del mantenedor (H1) pero el `Status` vigente no es exactamente `Aprobado para ejecución`: **STOP** (ver `## Stop Conditions`).

No se auto-asigna autorización (`.agents/AGENTS.md`: "Do not invent authorization") y no se inventan estados nuevos.

## Creación

2026-09-09 — **H1 = GO** otorgado explícitamente por el mantenedor, que autoriza exclusivamente la ejecución del experimento definido por este Plan. Alcance de la autorización: **no** aprueba la feature arquitectónicamente de forma definitiva, **no** implica promoción a gobernanza, obligatoriedad, integración con Change Lifecycle ni integración con Protocol.

Promoción ejecutada: el artifact, creado originalmente como borrador en `sessions/drafts/114-adversarial-deliberation-mvp.md` (staging ignorado por git), fue movido a `docs/plans/114-adversarial-deliberation-mvp.md` con `**Status:** Aprobado para ejecución` y registrado en `docs/plans/INDEX.md` en el mismo commit (Cuadragésima sexta serie). Número verificado contra el INDEX: siguiente libre = 114 (último plan registrado: 113).

## Objetivo

Introducir en ARgentOS DEV la capacidad de **deliberación adversarial** de decisiones candidatas mediante el mínimo suficiente: **una convención no normativa** y un **registro embebido en el artefacto dueño de la decisión**, sin código, sin tool, sin skill, sin checker, sin artefacto nuevo de gobernanza y sin máquina de estados.

El Plan no busca demostrar que se puede escribir una convención: busca responder, con evidencia real, si la deliberación adversarial **produce evidencia adicional útil para una decisión real de DEV** frente al baseline existente. El resultado puede ser valor demostrado, parcialmente demostrado, no demostrado, o que la feature sea innecesaria; **todos son resultados válidos** y ninguno habilita por sí mismo promover la convención a gobernanza.

## Alcance

**Dentro del alcance:** la convención de deliberación adversarial (documento *Working*), su registro en el INDEX de propuestas, la ejecución de **un** Trial real sobre una decisión pendiente real de DEV, el registro de ese Trial, su validación y la captura de evidencia de valor.

**Punto de integración (cerrado en D3):** `docs/working/proposals/*` (clase *Working*: no normativa, pre-canónica, persistente, registrada en su INDEX) + registro embebido en el artefacto dueño de la decisión. **HD-1 resuelto por el mantenedor.**

**Queda fuera de este Plan** (lista completa en `## Out of Scope`): promoción a gobernanza, obligatoriedad, tooling/checkers, plantillas, `.agents/`, `protocol/`, `runtime/`, `tools/`, `tests/`, integración con Change Lifecycle, orquestación de N candidatas, votación, aislamiento técnico y cualquier entidad/registry/state machine.

## Authority / Decision Basis

- **D1 / D1-Review** (modelo conceptual cerrado): la unidad es `Problema × Solución candidata`; `Trial` es un acto/concepto de evaluación, **sin** entidad global, **sin** registry y **sin** ID global; su registro pertenece al artefacto dueño; `Problem` es una **referencia**; `Verdict ≠ Recommendation ≠ Decision`; `NOT_VIABLE` no descarta; los criterios son obligatorios en viabilidad y en comparación; el desacuerdo se preserva.
- **D2 / D2-Review-Closure** (arquitectura de ejecución cerrada): marco declarado → pasadas atribuidas → confrontación opcional → síntesis → veredicto con base → recomendación opcional → registro → autoridad existente. **Independencia = condición de procedencia, relacional y direccional**: ejecutores distintos es condición **necesaria y no suficiente**; DEV no garantiza independencia epistemológica. **Síntesis**: puede resumir, reorganizar, derivar relaciones, identificar contradicciones/convergencias/dependencias/condiciones, derivar consecuencias y discrepar; **no** puede introducir hechos externos no soportados, evidencia nueva ni argumentos materiales no fundados; un argumento material nuevo implica una **nueva pasada de evaluación**; no suprime ni reescribe conclusiones; **convergencia ≠ evidencia**. **Mecanismo mínimo** (marco + ≥1 evaluación + veredicto con base + registro) **≠ demostración adversarial** (≥2 posturas opuestas, compromiso antes de revelación, síntesis, desacuerdo preservado). **Conducción**: responsabilidad operacional, no actor/rol/componente. **Una síntesis** en el camino canónico, sin prohibición arquitectónica de síntesis futuras.
- **D3** (implementación cerrada): alternativa E — híbrido mínimo (convención + registro embebido + uso **opcional** de herramientas existentes como métodos). Sin código, sin tool, sin skill, sin checker, sin artefacto nuevo, sin cambio de plantillas, sin cambio de gobernanza, sin `.agents/`, sin `protocol/`, sin integración obligatoria con Change Lifecycle. Change surface: 2 archivos + contenedores estándar.
- **Autoridad DEV vigente aplicable:** `.agents/policies/authority.md` (clases FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE; "el agente nunca convierte su inferencia en decisión humana"; stop conditions); `.agents/AGENTS.md` (reglas operativas; prohibición de registry/estado global/base de datos/state machine en `.agents/`); `.agents/workflows/change-lifecycle.md` (§10 GAP/ANOMALY/BOUNDARY; disciplina de afirmaciones; borradores en `sessions/`); `.agents/policies/validation-closure.md` (historia no reescribible; resolución de findings = humana); `docs/CONVENTIONS.md` (findings y pendientes en el artefacto dueño); `docs/VERSIONING.md` §4.1 (batería canónica), §7 (estados de planes), §10 (DoD); `docs/plans/_TEMPLATE.md` (estructura del Plan).
- **Herramientas del producto usables como herramientas (no como reglas):** `AGENTS.md` raíz declara que las skills inyectadas desde `protocol/.agents/skills/` "may be used as tools during development, but they are never rules for this workspace". Este Plan las cita, si acaso, como **métodos sugeridos** y nunca como normas ni como arquitectura.

## Criterio de entrada

**Autorización (condición previa absoluta):**

- [ ] GO del mantenedor registrado en este Plan como H1.
- [ ] `**Status:**` fijado por el mantenedor en exactamente **`Aprobado para ejecución`**. `Aprobado para redacción` **no** habilita la ejecución de los Steps 1–12.
- [ ] Si existe GO pero el `Status` no es `Aprobado para ejecución`: **STOP** (ver `## Stop Conditions`).

**Estado del Plan y del repositorio:**

- [ ] Plan registrado en `docs/plans/INDEX.md` (fila + serie) en el mismo commit de creación.
- [ ] `sessions/drafts/114-adversarial-deliberation-mvp.md` movido a `docs/plans/114-adversarial-deliberation-mvp.md`.
- [ ] Repositorio en `dev`, working tree limpio (excepto staging ignorado), HEAD confirmado (`git status --short --branch`; `git rev-parse HEAD`).
- [ ] `docs/working/proposals/` existe y contiene `INDEX.md` (verificado).
- [ ] `docs/plans/105-terminology-architecture-materialization.md` existe, está registrado como `Executed` con condición derivada `Closed`, y su registro `<PLAN-105>` de decisión pendiente está vigente y sin resolver.
- [ ] Siguiente número libre confirmado en `docs/plans/INDEX.md` (114).
- [ ] Confirmado que **ninguna** superficie `Out of Scope` requiere cambios para ejecutar este Plan.

Si cualquier criterio de entrada falla: **STOP** (ver `## Stop Conditions`).

## Entregables

1. `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` — la convención (nueva, clase *Working*, no normativa).
2. `docs/working/proposals/INDEX.md` — una entrada nueva registrando la convención (sin modificar otras entradas).
3. Sección de registro del **primer Trial real** dentro de este Plan (`docs/plans/114-adversarial-deliberation-mvp.md`), referenciando la decisión pendiente `<PLAN-105>` (el Plan 105 está `Closed` y no se modifica).
4. `docs/plans/114-adversarial-deliberation-mvp.md` — este Plan, registrado y con su `## Nota de ejecución`.
5. `docs/plans/INDEX.md` — fila del Plan 114.
6. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 114, —)` al cierre (docs-only, sin `VERSION` bump ni tag).
7. `## Validation anchor` y `## Checkpoint / cierre` completados en este Plan.

## Pasos

Secuencia operativa: Steps 1–12 abajo. Cada paso referencia rutas y secciones exactas (`ruta:sección`), nunca números de línea.

## Step 1 — Create Convention

Crear `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` con, como mínimo, estas secciones y contenidos. El documento debe ser **autocontenido** (no puede depender de los análisis D1–D3, que no están persistidos) y llevar un **banner de clase** en la cabecera: *Working · no normativa · pre-canónica · sin autoridad · no crea gates, obligaciones ni reglas de gobernanza*.

**Declaración de naturaleza de sus reglas (obligatoria dentro de la convención).** Además del banner, la convención debe declarar explícitamente que:

- sus reglas (`MUST`, `PROHIBITED`, "debe", "no puede", "argumento material nuevo ⇒ nueva pasada", "preservar el desacuerdo", etc.) son **condiciones y convenios de ejecución del experimento/MVP**;
- son **instrucciones para quienes decidan utilizar esta Working Convention**, no para el workspace;
- **no** son obligaciones generales de ARgentOS DEV;
- **no** crean gates;
- **no** crean lifecycle states;
- **no** crean governance;
- **no** modifican la autoridad existente (el mecanismo sigue sin decidir, autorizar, aprobar ni descartar);
- **no** son requisitos para trabajos DEV que no utilicen esta convención;
- su carácter normativo podrá evaluarse posteriormente mediante evidencia, pero esa promoción queda **fuera del Plan 114**.

El objetivo es que el uso interno de `MUST`/`PROHIBITED` sea inequívocamente **interno al experimento** y no se lea como regulación del repositorio. Esta declaración **aclara el alcance** de las restricciones; **no** las debilita: las condiciones de procedencia, el compromiso antes de revelación, la síntesis sin invención, la preservación del desacuerdo y la authority boundary se mantienen íntegras.

1. **Purpose** — qué problema resuelve (obtener evidencia adversarial trazable sobre una decisión candidata); declaración explícita de que **no** es gobernanza ni un paso obligatorio.
2. **Scope** — decisiones apropiadas (con ≥2 direcciones materiales posibles, o viabilidad en duda real) y decisiones inapropiadas (cambios mecánicos; decisiones reversibles de bajo impacto; casos cuyo bloqueo real es **falta de evidencia**, donde la acción es obtener evidencia; casos cuyo criterio ya está fijado por gobernanza).
3. **Invocation** — quién puede invocarla (agente DEV y/o humano), por qué, cuándo tiene sentido y cuándo no; registro del motivo de invocación; **sin** clasificador automático; la invocación no cambia ningún estado.
4. **Declared Frame** — referencia al problema/cuestión; candidata(s) con etiqueta local y descripción; **criterios declarados**; modo (`viability` | `comparative`); límites de ejecución declarados.
5. **Evaluation Pass** — por evaluación: etiqueta local; postura/instrucción; ejecutor; material recibido; material compartido; relación con conclusiones previas; condición de compromiso antes de revelación; conclusión; razones **por criterio**; premisas; citas (`ruta:sección`); supuestos; incertidumbres.
6. **Independence / Provenance** — la formulación cerrada: condición **de procedencia, relacional y direccional**; ejecutores distintos = necesaria, no suficiente; DEV no afirma independencia epistemológica; distinguir evaluación independiente / re-evaluación / contexto compartido / visibilidad de conclusiones previas.
7. **Optional Confrontation** — opcional, acotada, con propósito declarado; un intercambio que no puede cambiar la base ni introducir un contraargumento material la termina; **sin** infraestructura de rondas generalizada.
8. **Synthesis** — *Allowed*: resumir, reorganizar, derivar relaciones, identificar contradicciones, convergencias, dependencias y condiciones, derivar consecuencias, discrepar. *Prohibited*: hechos externos no soportados, evidencia nueva, argumentos materiales no fundados. Un argumento material nuevo ⇒ **nueva pasada de evaluación**, no síntesis. No suprime ni reescribe conclusiones. Preserva el desacuerdo. Cada relación derivada identifica su origen. Convergencia ≠ evidencia.
9. **Verdict** — viabilidad (`VIABLE` | `NOT_VIABLE` | `UNDETERMINED`) y comparación (`PREFERRED(A)` | `PREFERRED(B)` | `TIE` | `UNDETERMINED`); debe contener **base declarada**, razones, desacuerdo, relación con cada evaluación, limitaciones declaradas y razón de terminación.
10. **Recommendation** — opcional, advisory, nunca autorización ni decisión; separada del veredicto.
11. **Termination** — razón registrada: `VERDICT` | `UNDETERMINED` | `LIMIT` | `NO_VALUE` | `FAILURE`; **sin** estados de lifecycle. Terminar por `NO_VALUE` exige fundamento registrado.
12. **Authority Boundary** — *CAN*: evaluar, atacar, defender, sintetizar, emitir veredicto, emitir recomendación, revelar material para findings. *CANNOT*: decidir, autorizar, aprobar, descartar, resolver findings, cambiar lifecycle, crear gobernanza, ser gate, reemplazar validación, reemplazar verificación.
13. **Canonical MVP Path** — `candidata → perspectiva A → perspectiva B → compromiso → revelación → síntesis → veredicto → recomendación → decisión humana`; la segunda perspectiva no recibe la conclusión de la primera antes de comprometer la propia; **no** convertir el camino en una state machine.
14. **Degradation** — qué ocurre si solo hay una perspectiva (la ausencia de segunda perspectiva debe quedar **explícita**; **no** simular independencia), si una perspectiva falla, si la evidencia es insuficiente, si hay desacuerdo, si la síntesis no puede resolver, y si se alcanza el límite.

Reglas de contenido adicionales: incluir obligatoriamente la **Declaración de naturaleza de sus reglas** de arriba (reglas internas del experimento, no gobernanza del workspace); no nombrar estados de gobernanza nuevos; no declarar obligaciones generales de ARgentOS DEV; no prometer garantías de independencia; usar `ruta:sección` en las citas. El uso interno de `MUST`/`PROHIBITED` es correcto y esperado: son reglas del experimento.

## Step 2 — Register Convention

Modificar **únicamente** `docs/working/proposals/INDEX.md`: leerlo primero, respetar exactamente su formato vigente y añadir una entrada para `ADVERSARIAL_DELIBERATION_CONVENTION.md` con su clase (*Working* / no normativa). No modificar otras entradas. No tocar ningún otro INDEX.

## Step 3 — Select Real Dogfooding Case

**Caso seleccionado (real, no inventado):** la decisión pendiente registrada por el Plan 105.

- **Registro de origen:** `docs/plans/105-terminology-architecture-materialization.md:## Findings / Correcciones / Pending` → `### Pending decisions` → `<PLAN-105>`: *evaluar la elevación de la arquitectura terminológica (D1–D5) a ADR cuando se satisfaga el criterio de ADR-worthiness (`docs/adr/16-change-lifecycle-authority.md`, punto 3): consumo fuera de `docs/`, supersession de esta convención, o invariante arquitectónico con cambio futuro auditable de forma independiente*; `blocking: no`; `owner: mantenedor`; `resolución: pendiente (sin plazo)`; `ADR-worthiness: candidata futura (no bloqueante)`.
- **Criterio de ADR-worthiness aplicable:** `docs/adr/16-change-lifecycle-authority.md` (`ADR-worthiness`).
- **Por qué este caso:** decisión **real y registrada**; **DEV-only**; con **dos opciones materialmente distintas**; **no bloqueante** (riesgo bajo para un primer uso); con **dueño claro** (el mantenedor) y **resolución pendiente**.
- **Marco del Trial:**
  - **Problema/cuestión (referencia):** la decisión pendiente `<PLAN-105>`.
  - **Candidata (etiqueta local `C-1`):** *elevar ahora la arquitectura terminológica (D1–D5) a ADR*.
  - **Criterios declarados (`K-1..K-4`):** (K-1) los tres disparadores de ADR-worthiness de `docs/adr/16`; (K-2) costo de gobernanza de un ADR prematuro; (K-3) valor de fijar el invariante antes de que aparezca un consumidor; (K-4) reversibilidad de elevar después.
  - **Modo:** `viability`.
  - **Límites declarados:** máximo de pasadas de evaluación = 2; sin confrontación; una síntesis.
- **Registro (dónde vive el Trial):** el Plan 105 está `Closed` (condición derivada docs-only) y **no se modifica**: conforme a la regla DEV, lo posterior al cierre son artefactos nuevos que lo referencian. El Trial se registra por tanto **en este Plan 114**, con referencia explícita a `<PLAN-105>`. La **decisión** sigue siendo del mantenedor.
- **Si el caso no resultara adecuado al ejecutar (p. ej. la decisión ya se resolvió):** **STOP**. No inventar otro caso; escalar y pedir la designación de un caso real.

## Step 4 — Execute Perspective A

Producir la **perspectiva A** (postura: sostener la viabilidad de `C-1`) conforme a `ADVERSARIAL_DELIBERATION_CONVENTION.md` (§Evaluation Pass) y registrar, con `ruta:sección`, material recibido (registro `<PLAN-105>`; `docs/adr/16-change-lifecycle-authority.md`; `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura`; `docs/glossary/INDEX.md`), material compartido (encuadre, criterios `K-1..K-4`, evidencia disponible), ejecutor declarado, condición de compromiso, conclusión, razones **por criterio**, premisas citadas, supuestos e incertidumbres.

**Compromiso:** la conclusión de A se registra **antes** de que B conozca conclusión alguna.

## Step 5 — Execute Perspective B

Producir la **perspectiva B** (postura: atacar `C-1`) con el mismo rigor: debilidades, supuestos inválidos, omisiones, consecuencias negativas, evidencia faltante. Registrar material recibido (no incluye la conclusión de A), material compartido, ejecutor, condición de compromiso, conclusión, razones por criterio, premisas, supuestos e incertidumbres.

**Compromiso:** la conclusión de B se registra **antes** de revelar la de A en la fase de síntesis.

**Declaración de procedencia obligatoria:** si ambas perspectivas las produce el **mismo ejecutor**, la base del veredicto lo declara y **no** se afirma independencia; si el humano ejecuta una de las dos, se declara `ejecutores: distinto` (condición necesaria, **no suficiente**), junto con el material compartido.

## Step 6 — Synthesis

Conforme a §Synthesis de la convención: reunir ambas evaluaciones; preservar **ambas** conclusiones; identificar convergencias y contradicciones; identificar argumentos materiales; derivar solo relaciones permitidas; **registrar el origen** de cada relación derivada; identificar el desacuerdo; producir la síntesis.

**Prohibido:** introducir hechos externos no soportados, evidencia nueva o argumentos materiales no fundados. **Si aparece un argumento material nuevo:** registrarlo como **nueva pasada de evaluación** (con su postura y ejecutor) o **STOP**; **nunca** ocultarlo dentro de la síntesis. La síntesis no suprime ni reescribe conclusiones y **puede discrepar**, registrando la divergencia.

## Step 7 — Verdict

Emitir el veredicto de viabilidad con: **valor** (`VIABLE` | `NOT_VIABLE` | `UNDETERMINED`); **base declarada** (¿hubo ataque? sí; `ejecutores: mismo|distinto`; material compartido; criterios declarados; qué quedó sin hacer); **razones** (por criterio); **desacuerdo** registrado; **relación con cada evaluación** (coincide / diverge); **limitaciones declaradas**; **razón de terminación** (`VERDICT` | `UNDETERMINED` | `LIMIT` | `NO_VALUE` | `FAILURE`).

**Prohibido:** emitir una decisión; descartar automáticamente la candidata; presentar convergencia como evidencia; afirmar independencia epistemológica.

## Step 8 — Recommendation

Si corresponde, emitir una **recomendación advisory**, claramente separada del veredicto y de la decisión. Si no corresponde, registrarlo como ausencia deliberada. La recomendación **nunca** autoriza.

## Step 9 — Human Decision

La decisión sobre `<PLAN-105>` la toma **el mantenedor**, fuera del mecanismo. Registrarla como acto humano separado, con: fecha, actor, opción elegida y fundamento, y con la declaración explícita `Trial Verdict ≠ Recommendation ≠ Human Decision`. **No** escribir la decisión como si el Trial la hubiera producido.

Si al ejecutar **no hay decisión humana disponible**: registrar el veredicto y dejar la decisión como **pendiente escalada** (con owner: mantenedor) en la sección `### Pending decisions` de este Plan. **No** improvisar una decisión ni cerrar el Plan como si estuviera resuelta.

## Step 10 — Validation

Ejecutar, desde la raíz del repositorio:

```
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Juicios manuales obligatorios:

- [ ] La convención lleva el banner de clase *Working* / no normativa **y** la **Declaración de naturaleza de sus reglas** (reglas internas del experimento; sin gates, sin lifecycle states, sin gobernanza y sin obligaciones generales del workspace).
- [ ] La declaración es explícita respecto de `MUST`/`PROHIBITED`: se leen como reglas del experimento, no como regulación del repositorio; y las restricciones experimentales (procedencia, compromiso, síntesis, desacuerdo, authority boundary) siguen íntegras.
- [ ] `docs/working/proposals/INDEX.md` registra la convención y **ninguna otra entrada** fue modificada.
- [ ] Todas las citas `ruta:sección` del registro del Trial resuelven (las valida `check_plan_citations.py`).
- [ ] La sección de registro **no** usa encabezados que los checkers de lifecycle interpretan como contenedores (`## Findings`, `### Findings`, `### Correcciones`).
- [ ] `git diff --name-only` está contenido en el change surface autorizado.
- [ ] Working tree limpio al finalizar (excepto staging ignorado).
- [ ] Revisión manual del primer Trial: dos perspectivas atribuidas, compromiso antes de revelación, procedencia registrada, síntesis con desacuerdo preservado, veredicto con base, recomendación separada, decisión fuera del mecanismo.

**No** crear checkers nuevos ni tests de código inexistente. `tools/check_dist_sync.py` es local y solo se espera verde en `master`: en `dev` es rojo por diseño (no cuenta como fallo de este Plan).

## Step 11 — Evidence of Value

Registrar la evidencia del dogfooding comparando **baseline** (qué habría producido el proceso normal sin deliberación: la práctica actual de alternativas con razón de descarte en prosa) contra **Trial** (qué produjo la deliberación adicional). Responder, una por una:

1. ¿La segunda perspectiva encontró algo material?
2. ¿Encontró un contraargumento que el baseline no habría producido?
3. ¿Detectó un supuesto inválido?
4. ¿Detectó evidencia mal interpretada?
5. ¿Cambió el veredicto?
6. ¿Cambió la decisión humana?
7. ¿El desacuerdo quedó mejor preservado?
8. ¿La base del veredicto permitió reconstruir el razonamiento?
9. ¿Cuál fue el coste incremental (pasadas, tiempo, contexto duplicado)?
10. ¿La deliberación fue innecesaria?

**"No aportó valor" es un resultado válido.** No manipular la evidencia para justificar la feature. Registrar también lo que no se puede concluir con un solo caso (no generalizar valor desde N=1).

## Step 12 — Closure

Cerrar solo si se cumplen los 16 criterios de `## Criterios de salida`. Al cerrar: añadir `## Nota de ejecución` (fecha, verificación realizada, resultado); ítem `[Unreleased]` `(plan 114, —)` en `CHANGELOG.md` (docs-only: sin `VERSION` bump, sin tag); fila del Plan 114 en `docs/plans/INDEX.md` ya registrada en la creación (actualizar status/descripción si corresponde); completar `## Validation anchor` y `## Checkpoint / cierre`; registrar en `### Pending decisions` toda decisión que siga abierta; y emitir la conclusión final del Plan en `## Resultado final del Plan`.

**No** promover la convención a gobernanza, **no** hacerla obligatoria, **no** crear tooling, **no** integrarla con Change Lifecycle ni con Protocol dentro de este Plan.

## Registro del primer Trial — `<PLAN-105>` (Steps 3–9)

> **Este registro es contenido experimental del Plan 114.** No crea gobernanza, no
> modifica la decisión pendiente `<PLAN-105>` y no posee autoridad: la decisión
> sigue siendo del mantenedor. Conforme a la regla DEV, el Plan 105 está `Closed`
> y **no** se modifica; este Plan es el artefacto nuevo que lo referencia.

### Marco declarado

| Elemento | Valor |
|---|---|
| Problema / cuestión (referencia) | Decisión pendiente `<PLAN-105>`: *elevar la arquitectura terminológica (D1–D5) a ADR cuando se satisfaga el criterio de ADR-worthiness* |
| Candidata | `C-1` — *elevar **ahora** la arquitectura terminológica (D1–D5) a ADR* |
| Modo | `viability` |
| Criterios | `K-1` disparadores de ADR-worthiness de `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3 — ADR-worthiness) · `K-2` costo de gobernanza de un ADR prematuro · `K-3` valor de fijar el invariante antes de que aparezca un consumidor · `K-4` reversibilidad de elevar después |
| Límites declarados | máximo 2 pasadas de evaluación; sin confrontación; una síntesis |
| Motivo de invocación | El Plan 114 requiere un caso real de dogfooding; `<PLAN-105>` es una decisión registrada, DEV-only, con dos opciones materialmente distintas, no bloqueante y con resolución pendiente |

### Perspectiva A — postura: sostener la viabilidad de `C-1`

- **Etiqueta local:** `E-A`.
- **Ejecutor:** agente DEV (sesión de ejecución del Plan 114).
- **Material recibido:** registro `<PLAN-105>` (`docs/plans/105-terminology-architecture-materialization.md:## Findings / Correcciones / Pending` → `### Pending decisions`); `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3 — ADR-worthiness); `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`; `docs/glossary/INDEX.md:Qué es y qué no es`; `docs/AGENTS.md:INDEX y CONVENTIONS`.
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (primera pasada del Trial).
- **Condición de compromiso:** conclusión registrada antes de que `E-B` conociera conclusión alguna.
- **Conclusión:** **VIABLE** (la elevación inmediata es viable).
- **Razones por criterio:**
  - `K-1(a)` *consumo fuera del artefacto de origen*: **parcialmente a favor**. La convención vive en `docs/CONVENTIONS.md` y la consumen piezas que no son esa subsección — el `AGENTS.md` raíz y `.agents/AGENTS.md` referencian la convención de terminología, y todo texto nuevo aplica las reglas de calificación y la regla SCI.
  - `K-1(c)` *invariante arquitectónico persistente con cambio auditable de forma independiente*: **a favor**. La decisión D3 declara "no se introduce `.agents/ENTRYPOINT.md` ni `BOOTSTRAP.md` sin nueva decisión": es un invariante cuya modificación futura exige decisión propia. Un ADR lo haría auditable por sí mismo, independientemente del texto de CONVENTIONS.
  - `K-2` *costo*: **bajo**. Un ADR es un documento + registro en `docs/adr/INDEX.md`; el ciclo `Proposal → Accepted → Superseded` ya existe y está normalizado.
  - `K-3` *valor de fijar antes del primer consumidor*: **a favor**. La regla SCI y la calificación de términos ya se aplican en texto nuevo; un ADR las haría visibles para quien lee el registro de decisiones y no el cuerpo de CONVENTIONS.
  - `K-4` *reversibilidad*: **a favor**. La elevación es reversible por supersession; elevar ahora no introduce un compromiso irreversible.
- **Premisas:** (P1) el ADR no autoriza cambios: su función es de registro/auditoría y no de habilitación (`docs/adr/16-change-lifecycle-authority.md:Decisión` puntos 1–2); (P2) la elevación puede ser retrospectiva (`:Decisión`, punto 3 — ADR-worthiness); (P3) la carga de mantenimiento de un ADR es acotada.
- **Supuestos:** que el contenido D1–D5 no cambiará en el corto plazo; que la visibilidad adicional en el registro de decisiones tiene valor para el mantenedor y para agentes que no leen CONVENTIONS completo.
- **Incertidumbres:** si `K-1(c)` basta por sí solo cuando el ADR **no** autoriza nada; si "invariante arquitectónico" alcanza a convenciones de terminología; si `K-1(a)` aplica sin una RFC de origen.

### Perspectiva B — postura: atacar `C-1`

- **Etiqueta local:** `E-B`.
- **Ejecutor:** **el mismo** agente DEV (misma sesión) → `ejecutores: mismo`.
- **Material recibido:** registro `<PLAN-105>`; `docs/adr/16-change-lifecycle-authority.md` (`ADR-worthiness`, `Decisión` puntos 1–5, `Invariantes`, `Consecuencias`); `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`; `docs/glossary/INDEX.md:Qué es y qué no es`; `docs/AGENTS.md:INDEX y CONVENTIONS`. **No** recibió la conclusión de `E-A`.
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (no conocía `E-A`).
- **Condición de compromiso:** conclusión registrada antes de la revelación de `E-A`.
- **Conclusión:** **NOT_VIABLE** (elevar ahora no es viable).
- **Razones por criterio:**
  - `K-1(a)`: **no se satisface**. El criterio presupone un artefacto de origen del que la decisión se desprende; aquí no hay RFC ni plan de origen que la contenga: la decisión nació como decisión humana directa materializada en `docs/CONVENTIONS.md` y reflejada en `docs/AGENTS.md`. Afirmar que "todo el texto nuevo la consume" extiende el criterio: el criterio habla de **consumo desde otro artefacto de decisión**, no de que el repositorio aplique una convención vigente.
  - `K-1(b)`: **no se satisface**. Elevar no supersede ni modifica un ADR existente; sería un ADR nuevo sobre materia no cubierta por ADR-01…16.
  - `K-1(c)`: **débil, y potencialmente autoinvalidante**. La fuerza del invariante D3 ("sin nueva decisión") **ya existe** en la regla operacional vigente; y como el ADR **no autoriza** (`docs/adr/16-change-lifecycle-authority.md:Invariantes` AU-2), convertirlo en ADR **no agrega fuerza ejecutable**: la autorización seguiría viniendo del lifecycle. El beneficio sería de visibilidad, no de auditabilidad.
  - `K-2`: **costo real y no trivial**. Un ADR es un artefacto permanente con ciclo propio, registro en INDEX, relaciones, estado de implementación y Amendment Log. Un ADR cuyo contenido **espeje** la subsección de `docs/CONVENTIONS.md` crea **dos textos sobre la misma materia**, que es lo que la gobernanza documental DEV prohíbe: `docs/AGENTS.md:INDEX y CONVENTIONS` ("no se duplican responsabilidades"; el INDEX registra, no regula) y `docs/glossary/INDEX.md:Qué es y qué no es` ("Prohibido: duplicar definiciones normativas"). El ADR quedaría obligado a mantener sincronía con CONVENTIONS sin ser su fuente.
  - `K-3` (invertido): fijar "antes del primer consumidor" es **prematuro** cuando no hay consumidor que lo requiera. El propio criterio es **condicional a evidencia** y trae guardas explícitas: "No toda decisión arquitectónica necesita ADR; no se crea un ADR por cada RFC" (`docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3 — ADR-worthiness)).
  - `K-4` (invertido): la reversibilidad **corta en ambos sentidos**. Elevar es reversible, pero deshacer un ADR improcedente deja traza de gobernanza (supersession + Amendment Log) y consume mantenimiento; **esperar cuesta cero** mientras la convención opera.
  - **Debilidades de `E-A` detectadas:** (i) trata "todo el texto nuevo consume la convención" como si fuera el criterio `(a)`, cuando el texto nuevo consume un artefacto **ya normativo** (`docs/CONVENTIONS.md`) y por tanto no hay carencia de autoridad; (ii) supone que elevar "gana estabilidad" cuando el ADR no cambia la autorización — P1 es cierta pero **juega contra** `E-A`; (iii) no verifica si existe un consumidor que demande cita independiente.
- **Evidencia faltante (declarada):** no existe ningún caso registrado de conflicto entre la convención D1–D5 y otra autoridad DEV; no existe consumidor cross-artefacto que requiera citarla por identidad independiente; no se localizó ningún pedido del mantenedor de elevar.
- **Omisiones detectadas:** `E-A` no evaluó el riesgo de duplicación de fuente ni la asimetría de costo (mantener un ADR frente a mantener una subsección ya existente).
- **Consecuencias negativas:** un artefacto de gobernanza más que mantener; riesgo de divergencia CONVENTIONS↔ADR; precedente de elevar convenciones operativas a ADR por anticipación.
- **Supuestos:** que un ADR aporta visibilidad neta.
- **Incertidumbres:** si el criterio ADR-worthiness admite una lectura amplia de `(c)` que B no comparte; si esa visibilidad tiene valor material para quien ya lee `docs/CONVENTIONS.md`.

### Síntesis

**Entradas consideradas:** `E-A` y `E-B` (ambas comprometidas antes de la revelación). **Ninguna conclusión fue suprimida ni reescrita.**

**Convergencias (derivadas, con origen):**

- `S-1` — *elevar no cambia la autorización*: deriva de `docs/adr/16-change-lifecycle-authority.md:Decisión` punto 1 (un ADR es registro de decisión y no autoriza payload) y `:Invariantes` AU-2. Ambas evaluaciones la asumen; `E-B` la usa **contra** `C-1` y `E-A` no la pondera.
- `S-2` — *la elevación es reversible por supersession*: deriva de `docs/adr/16-change-lifecycle-authority.md:Decisión` punto 5 y `:Invariantes` AU-7.
- `S-3` — *la convención D1–D5 está vigente y operando*: deriva de `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)` (regla operacional) y del registro `<PLAN-105>` (`resolución: pendiente`).

**Contradicciones identificadas (no adjudicadas):**

- `X-1` — **`K-1(c)`**: `E-A` sostiene que el invariante D3 satisface el criterio y que un ADR lo haría auditable independientemente; `E-B` sostiene que la auditabilidad ya existe en la regla operacional y que, al no autorizar el ADR, no hay ganancia funcional.
- `X-2` — **costo de duplicación**: `E-A` lo estima "bajo" (documento + registro); `E-B` lo estima **riesgo estructural** (dos textos sobre la misma materia, contra la gobernanza documental DEV). Depende de si el ADR sería fuente o espejo.

**Dependencias y condiciones (derivadas):**

- `D-1` — el valor de elevar depende de que exista un **consumidor que requiera cita independiente** (condición no satisfecha hoy).
- `C-2` — si apareciera un conflicto real entre la convención y otra autoridad, o un consumidor cross-artefacto, `K-1(a)`/`K-1(b)` podrían satisfacerse y la conclusión podría invertirse (el criterio admite elevación retrospectiva: `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3 — ADR-worthiness)).

**Desacuerdo preservado (explícito, sin adjudicar):** la divergencia se concentra en `K-1(c)` y en el costo de duplicación; **no se resuelve por mayoría, por conteo ni por preferencia del sintetizador**.

**Sin contenido nuevo:** la síntesis no introdujo hechos externos, evidencia nueva ni argumentos materiales no fundados. No fue necesaria ninguna pasada adicional: no surgió ningún argumento material nuevo que exigiera registrarse como nueva evaluación.

### Veredicto

| Campo | Valor |
|---|---|
| **Valor** | `NOT_VIABLE` — *no es viable elevar **ahora*** `C-1` (la candidata evaluada es la elevación inmediata) |
| **¿Hubo ataque?** | Sí (`E-B`) |
| **Ejecutores** | `mismo` — dos pasadas del **mismo** ejecutor (agente DEV de esta sesión) |
| **Material compartido** | encuadre, criterios `K-1..K-4`, registro `<PLAN-105>`, `docs/adr/16`, subsección de terminología de `docs/CONVENTIONS.md`, `docs/glossary/INDEX.md`, `docs/AGENTS.md` |
| **Criterios** | declarados: `K-1..K-4` |
| **Qué quedó sin hacer** | sin confrontación (declarada opcional y no usada); sin participación humana como ejecutor; sin verificación externa de las premisas más allá de los artefactos leídos; límite de 2 pasadas respetado |
| **Razones por criterio** | `K-1(a)` no satisfecho · `K-1(b)` no satisfecho · `K-1(c)` **en disputa** (`X-1`) · `K-2` costo/riesgo de duplicación alegado y no refutado (`X-2`) · `K-3` prematuro sin consumidor · `K-4` reversible en ambos sentidos |
| **Desacuerdo** | `X-1` y `X-2`, preservados sin adjudicar |
| **Relación con cada evaluación** | **coincide con `E-B`** (valor `NOT_VIABLE`); **diverge de `E-A`** (que concluyó `VIABLE`); la divergencia queda registrada con sus razones |
| **Limitaciones** | veredicto **relativo a la evidencia disponible** y **criterio-dependiente** (una lectura amplia de `K-1(c)` lo invertiría); **no** es evidencia de independencia (mismo ejecutor); **no** descarta `C-1` (el criterio admite elevación retrospectiva) |
| **Razón de terminación** | `VERDICT` |

### Recomendación (advisory)

**Se emite,** separada del veredicto y de la decisión:

> **No elevar ahora.** Mantener `<PLAN-105>` abierto y **re-evaluar cuando aparezca un disparador verificable**: consumo cross-artefacto que requiera citar la decisión por identidad independiente, o un conflicto real entre la convención D1–D5 y otra autoridad DEV. Si lo que se busca es **descubribilidad** y no auditabilidad independiente, la vía de menor costo es una **referencia desde el registro existente** hacia la regla operacional, no un ADR que espeje su contenido.

Esta recomendación es **advisory**: **no** autoriza, **no** aprueba, **no** decide y **no** modifica gobernanza.

### Decisión humana — fuera del mecanismo

**No tomada durante esta ejecución.** No hubo decisión del mantenedor disponible al ejecutar el Trial.

`Trial Verdict ≠ Recommendation ≠ Human Decision`

Registro: `<PLAN-105>` **permanece pendiente y escalada** al mantenedor (owner: mantenedor), sin resolución improvisada. Este Plan **no** resolvió la decisión ni la declara resuelta. La decisión, cuando se tome, deberá registrarse como **acto humano separado** (fecha, actor, opción elegida, fundamento) — fuera de este mecanismo.

### Evidencia de valor (baseline vs Trial)

**Baseline (proceso normal sin deliberación adversarial):** la práctica vigente registraría la cuestión como decisión pendiente y, llegado el caso, una **nota en prosa** con la recomendación del agente (`docs/rfc/_TEMPLATE.md:Alternativas consideradas` aplicado a mano). No habría segunda postura obligada a atacar, ni base declarada, ni desacuerdo tipado por criterio.

**Trial (segunda perspectiva + síntesis):**

| # | Pregunta | Respuesta observada |
|---|---|---|
| 1 | ¿La segunda perspectiva encontró algo material? | **Sí.** `E-B` aportó dos argumentos que `E-A` no había considerado: (i) el ADR **no autoriza**, luego elevar no agrega fuerza funcional; (ii) el **riesgo de duplicación de fuente** CONVENTIONS↔ADR, contra la gobernanza documental DEV |
| 2 | ¿Contraargumento que el baseline probablemente no habría producido? | **Probablemente sí**, con reserva: el baseline habría registrado "elevar / no elevar" y el criterio; la conexión *no-autorización ⇒ no-ganancia* y el conflicto con la regla de no-duplicación requieren postura adversarial dirigida. **No demostrable contrafactualmente** |
| 3 | ¿Detectó un supuesto inválido? | **Sí.** `E-A` trataba "todo el texto nuevo consume la convención" como si satisfaciera `K-1(a)`, cuando ese texto consume un artefacto **ya normativo** |
| 4 | ¿Detectó evidencia mal interpretada? | **No como cita errónea.** Sí detectó una **inferencia no sostenida**: que `K-1(c)` basta cuando el ADR no agrega fuerza |
| 5 | ¿Cambió el veredicto? | **Sí — hallazgo principal.** Sin `E-B`, la conclusión de una sola pasada habría sido `VIABLE` (apoyada en `K-1(c)`, costo bajo y reversibilidad). Con `E-B`, el veredicto es `NOT_VIABLE` |
| 6 | ¿Cambió la decisión humana? | **No observable** — no hubo decisión durante la ejecución |
| 7 | ¿El desacuerdo quedó mejor preservado? | **Sí.** Quedó tipado por criterio (`X-1`, `X-2`) en lugar de un "sí/no" plano |
| 8 | ¿La base permitió reconstruir el razonamiento? | **Sí.** Base declarada + razones por criterio + premisas citadas + divergencia registrada |
| 9 | ¿Cuál fue el coste incremental? | Una pasada de evaluación adicional + una síntesis; **mismo ejecutor y mismo contexto**, sin lecturas externas duplicadas; **coste humano adicional nulo**; sin medición de tiempo ni de tokens (no instrumentado) |
| 10 | ¿La deliberación fue innecesaria? | **No en este caso**: cambió el resultado respecto de la conclusión de una sola pasada (5). Con la reserva de ser **un** caso |

**Qué NO pudo demostrarse (registro obligatorio):**

- **La independencia no se demostró:** ambas perspectivas las produjo el **mismo ejecutor**; la divergencia observada es un **re-encuadre adversarial interno a un mismo razonador**, no divergencia entre evaluadores independientes. Lo demostrado es el valor de la **disciplina adversarial con procedencia declarada**, no el de perspectivas independientes.
- **N=1:** un solo caso no permite generalizar valor, ni estimar frecuencia de utilidad, ni costo medio.
- **El baseline es una reconstrucción**, no una ejecución observada y comparable.
- **No hay medición** de tokens, tiempo ni contexto consumido.
- **Caso en que la segunda perspectiva solo confirmó lo ya disponible:** no ocurrió aquí; **no se registra ninguno**.
- **Coincidencia ≠ evidencia de valor:** `S-1..S-3` se registraron como convergencias **derivadas**, no como evidencia de corrección del veredicto.

## Criterios de salida

- [ ] 1. La convención existe en `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`.
- [ ] 2. Está registrada en `docs/working/proposals/INDEX.md` sin alterar otras entradas.
- [ ] 3. No es normativa: lleva banner de clase *Working* **y** la **Declaración de naturaleza de sus reglas** (reglas internas del experimento; sin gates, sin lifecycle states, sin gobernanza y sin obligaciones generales del workspace).
- [ ] 4. El primer Trial real fue ejecutado sobre la decisión pendiente `<PLAN-105>`.
- [ ] 5. Existen dos perspectivas **atribuidas** (postura + ejecutor).
- [ ] 6. Se respetó el **compromiso antes de revelación**.
- [ ] 7. Se registró **procedencia** (material recibido, material compartido, ejecutor, relación con conclusiones previas).
- [ ] 8. Se produjo **síntesis** con origen declarado de las relaciones derivadas.
- [ ] 9. Se preservó el **desacuerdo** (sin promediar, sin mayoría).
- [ ] 10. Se produjo **veredicto con base** declarada.
- [ ] 11. La **recomendación** está separada del veredicto (o su ausencia es deliberada y registrada).
- [ ] 12. La decisión quedó en **autoridad humana**, registrada como acto separado.
- [ ] 13. No hubo cambios fuera del change surface autorizado.
- [ ] 14. Las validaciones aplicables pasan (batería + juicios manuales).
- [ ] 15. La **evidencia de dogfooding** quedó registrada (Step 11).
- [ ] 16. Se registró explícitamente si la feature **NO** aportó valor.

## Verificación

Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (comandos exactos en Step 10) + los juicios manuales de Step 10 + `git status --short --branch` limpio (excepto staging ignorado) + `git diff --name-only` contenido en el change surface. `tools/check_dist_sync.py` es local y se espera rojo en `dev` por diseño.

## Validation anchor

<!-- Se completa al validar (VC-1, docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity).

- Declared scope: ...
- Validation command-set: ...
- Effective inputs (repo content): ...
- Observed dependencies: ... | no instrumentado
- Environmental factors: ...
- Scoped Content Identity: delta (path → blob) y state identity (git write-tree / tree id)
- Validity / stale: vigente | stale (motivo) | revalidada -->

## Checkpoint / Closure

<!-- Se completa al cerrar (GC-1, docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git).

- Commits de cierre: ...
- Estado validado (ref al Validation anchor): ...
- Estado de cierre (tree id): ...
- Consistencia checkpoint↔anchor: PASS/FAIL + evidencia
- Governance aplicada: plan `Executed` + INDEX + CHANGELOG `[Unreleased]`; sin VERSION bump ni tag (RFC-69)
- Condición derivada: Closed (docs-only) | no cerrado (motivo) -->

## Out of Scope

**No tocar:** `protocol/**`; `runtime/**`; `tools/**`; `tests/**`; `.agents/**`; plantillas (`docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`, `docs/plans/_TEMPLATE.md`); `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/glossary/**`; `master`; tags; `dist/`; `VERSION`.

**No implementar ni diseñar:** Change Lifecycle como workflow obligatorio; integración con Protocol; infraestructura multi-agente; infraestructura de skills; votación de jurado; voto por mayoría; ranking; orquestación de N candidatas; número configurable de jurados; rondas generalizadas; clasificador automático; aislamiento técnico; ACL; sandbox; autoridad autónoma; registry nuevo; base de datos; state machine; entidad global.

**No hacer dentro de este Plan:** promover la convención a gobernanza; hacerla obligatoria; crear tooling o checkers; crear RFC/ADR; modificar el Plan 105 (está `Closed`); generalizar conclusiones de valor con N=1.

## Stop Conditions

Detenerse inmediatamente, registrando la condición, la evidencia, por qué bloquea y la decisión requerida — **sin improvisar, sin ampliar alcance y sin crear un Plan adicional** — si:

- no existe una **decisión real** disponible para el dogfooding (incluido el caso de que `<PLAN-105>` ya esté resuelto);
- se necesita una nueva **entidad**;
- se necesita **registry**;
- se necesita **state machine**;
- se necesita un nuevo **actor**;
- se necesita **Worker**;
- se necesita **Skill**;
- se necesita **Tool**;
- se necesita una nueva **regla de gobernanza**;
- se necesita modificar **Protocol**;
- se necesita integrar **obligatoriamente** el Change Lifecycle;
- se necesita modificar una **plantilla**;
- se necesita resolver una **contradicción de D1/D2**;
- se necesita afirmar **independencia epistemológica**;
- la síntesis necesita introducir **evidencia nueva**;
- el registro **no puede preservar el desacuerdo**;
- no se puede mantener la **authority boundary**;
- el change surface excede el autorizado;
- el GO del mantenedor (H1) no está registrado;
- el `Status` vigente no es exactamente `Aprobado para ejecución` (incluido `Aprobado para redacción`, que **no** habilita la ejecución de los Steps 1–12).

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Que la convención se lea como normativa, o que `MUST`/`PROHIBITED` se lean como regulación del repositorio | Banner de clase *Working*/no normativa **+ Declaración de naturaleza de sus reglas** (reglas internas del experimento; sin gates, lifecycle states, gobernanza ni obligaciones generales del workspace); ubicación en `docs/working/` (HD-1); verificación explícita en Step 10 y criterio de salida 3 |
| Que el primer Trial sea débil y no permita concluir nada | Registrar la limitación explícitamente (N=1); el resultado "valor no demostrado" es válido y no habilita promoción |
| Sesgo de confirmación al evaluar la propia feature | El caso elegido **no** es la feature (es la elevación ADR de terminología); perspectiva B obligada a atacar; baseline declarado antes de deliberar |
| Conclusión de la perspectiva B contaminada por A | Compromiso antes de revelación; la convención lo exige y el registro lo declara |
| Registro que colisiona con checkers de lifecycle | Evitar encabezados contenedores (`## Findings`, `### Findings`, `### Correcciones`) en la sección de registro |
| Deriva de alcance (tooling, gobernanza, plantillas) | `## Out of Scope` + `## Stop Conditions` + verificación de `git diff --name-only` |
| Que el Plan se ejecute sin GO | El Status de creación es acto del mantenedor; este borrador no se auto-aprueba |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-114>:F-01` — estado: `partially-resolved` (corrección `C-01` aplicada y revalidada; la **resolución formal es decisión del mantenedor**: `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); **observación original:** 4 citas del Plan 114 referenciaban `docs/adr/16-change-lifecycle-authority.md:ADR-worthiness`, sección que **no existe** como encabezado — la materia "ADR-worthiness" es el **punto 3 de `## Decisión`** de ese ADR; detectado por `python tools/check_plan_citations.py` en la **primera** ejecución de la batería (V1 = **FAIL**: 4 broken citations) sobre el estado del commit C1 `4f6a3a4`; **evidencia original:** salida del checker listando las líneas 242, 250, 279 y 306 con `[section not found]`; **estado Git observado:** `dev` en `4f6a3a4`, working tree limpio salvo `.codegraph/` (untracked); **provenance original:** contenido producido por el agente en la ejecución del Plan 114.

### Correcciones

- `<PLAN-114>:C-01` — **refs origen:** `<PLAN-114>:F-01`; **acción:** repuntar las 4 citas a `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3 — ADR-worthiness) y la forma corta `:ADR-worthiness` a `:Decisión`; **alcance de revalidación:** batería canónica completa sobre el estado corregido (V2), en particular `check_plan_citations.py`; **evidencia:** commit `C2` y salida de V2 (ver `## Nota de ejecución`).

### Pending decisions

- `<PLAN-114>` — decisión: resolución de `<PLAN-105>` (elevación ADR de la arquitectura terminológica) a la luz del veredicto del primer Trial; blocking: no; owner: mantenedor; escalación: mantenedor; resolución: pendiente; evidencia: registro del Trial en este Plan; efecto downstream: gobernanza terminológica; ADR-worthiness: candidata futura.
- `<PLAN-114>` — decisión: promover (o no) la convención de deliberación a gobernanza y/o hacerla obligatoria; blocking: no; owner: mantenedor; resolución: pendiente (depende de la evidencia de valor); evidencia: Step 11.

## Trazabilidad

Análisis de diseño D1 → D1-Review → D2 → D2-Review-Closure → D3 (fase previa, **no persistida en el repositorio**) → **este Plan** → `ADVERSARIAL_DELIBERATION_CONVENTION.md` + `docs/working/proposals/INDEX.md` + registro del primer Trial (en este Plan) + `docs/plans/INDEX.md` + `CHANGELOG.md`.

**Limitación declarada:** los análisis D1–D3 y la decisión HD-1 provienen del diálogo con el mantenedor y **no están persistidos** como artefactos del repositorio; por eso la convención es autocontenida y este Plan no depende de ellos para ejecutarse.

Referencias verificables usadas: `docs/plans/105-terminology-architecture-materialization.md` (`### Pending decisions`, `<PLAN-105>`); `docs/adr/16-change-lifecycle-authority.md` (ADR-worthiness); `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura`; `docs/glossary/INDEX.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/authority.md`; `.agents/policies/validation-closure.md`; `docs/VERSIONING.md` §4.1/§7/§10; `docs/plans/_TEMPLATE.md`.

## Nota de ejecución

<!-- No se crea con el Plan: se agrega al ejecutar, con fecha, verificación realizada y resultado. Si quedó algo incumplido: Status `Executed (parcial: ...)`. -->

## Resultado final del Plan

<!-- Al cerrar, exactamente uno:

### `MVP IMPLEMENTED — VALUE DEMONSTRATED`
### `MVP IMPLEMENTED — VALUE PARTIALLY DEMONSTRATED`
### `MVP IMPLEMENTED — VALUE NOT DEMONSTRATED`
### `MVP NOT IMPLEMENTED — BLOCKED`

La promoción a gobernanza, la obligatoriedad, el tooling, la integración con Change Lifecycle, la integración con Protocol y cualquier evolución arquitectónica **no se deciden dentro de este Plan**: dependen de la evidencia obtenida. -->
