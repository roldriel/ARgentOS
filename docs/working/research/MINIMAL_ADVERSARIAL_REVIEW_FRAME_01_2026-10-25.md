# FRAME-01 — Caso MAR-VALID-01 (CONGELADO)

> **Estado:** `FROZEN` — congelado por el Lead antes de ejecutar cualquier pasada del experimento de validación.
> **Naturaleza:** Working / no normativo. No autoriza nada, no modifica `protocol/`, `.agents/` ni ningún artefacto cerrado.
> **Uso:** es el objeto único que reciben BASELINE, DEFENSE, PROSECUTION y la revisión mínima. Se publica verbatim en el informe de validación.

## Metadata

- **ID de caso:** `MAR-VALID-01`
- **Versión:** `v2` — corrección pre-freeze del 2026-10-25 (revisión independiente `PRE-F04`/`PRE-F05`/`PRE-F19`; ver el registro de corrección en `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:14. Registro de corrección pre-freeze`). La v2 corrige el techo de contaminación, la lista de material prohibido, el anclaje de `behavior-patterns` y la relación HEAD-congelado / HEAD-de-ejecución. Nada se ejecutó antes de la v2.
- **Fecha de congelamiento (v2):** 2026-10-25 (America/Buenos_Aires)
- **Repositorio:** ARgentOS DEV, rama `dev`
- **HEAD de evidencia congelado:** `ac7f68074edbb9d67a1f231fac99c9e543a301aa`
- **HEAD de ejecución:** el commit del Change que materializa este FRAME (Commit 1). La evidencia se verifica contra `ac7f680` con `git show ac7f680:<path>` o comprobando que los archivos ancla no cambiaron en el árbol de ejecución; esa verificación es un ítem de la auditoría de integridad.
- **Working tree al congelar la v1:** sólo los dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`); ningún artefacto de este experimento es tracked.
- **Congelado por:** Lead del Change experimental (plan 179).
- **Evidencia base:** verificada por el Lead a HEAD `ac7f680` con `read`/`git grep` el 2026-10-25 (ver `## EVIDENCE STATE`); re-verificada por la revisión pre-ejecución contra el mismo HEAD. Las líneas pueden desplazarse; la verificación se hizo en el HEAD declarado.
- **Forma versionada:** este archivo es el **objeto congelado Git-verificable** en Commit 1; la copia operativa en `sessions/minimal-adversarial-review/FRAME-01.md` es idéntica byte a byte. Su sha256 se registra en el ledger y en el informe de validación; si una copia discrepa, **gobierna este archivo**.
- **Caso de selección:** `MAR-CAND-01` (documento de selección en staging gitignored, no citable como provenance versionada).

## QUESTION

¿La condición derivada `Closed` que alcanza el DEV Autonomous Orchestrator (`CLOSED_DERIVED`), y el registro `## Checkpoint / cierre` que el host escribe, deben exigir como precondición las dos determinaciones de impacto de cierre (`Documentation impact` §5.1 y `Roadmap impact` §5.2) que `.agents/policies/validation-closure.md` §7 declara **stop bloqueante**, o está esa obligación fuera del alcance de la derivación autónoma y basta con declarar la diferencia como límite?

## CANDIDATE

**Proposición a deliberar (C-MAR-01):**

> «El cierre derivado por el host queda sujeto a las determinaciones de impacto: la derivación no debe alcanzar `CLOSED_DERIVED` —ni escribir un checkpoint con `Condición derivada: Closed`— cuando falte alguna de las dos determinaciones, y el repositorio debe materializar esa precondición de forma derivable.»

Direcciones materialmente distintas que la revisión debe considerar:

- **A — Proceed (hacer efectiva la precondición).** Añadir a `derive_next_action` una comprobación/stop previo a `CLOSED_DERIVED` cuando las determinaciones no estén presentes y con clasificación válida; definir de dónde se leen (campos estructurados en el Plan, o el registro de cierre ya escrito). Consecuencia: el host deja de cerrar autónomamente un Change cuyo cierre está incompleto; exige decidir representación derivable y probablemente tocar `docs/plans/_TEMPLATE.md`.
- **B — Revise (acotar la norma).** Declarar en §5.1/§5.2/§7 que las determinaciones son obligaciones del **acto de cierre** (registro que afirma/cierra), no de la **condición derivada** que el host lee y nunca escribe como status; documentar por qué la derivación queda fuera y qué evidencia conserva. Consecuencia: no se toca el runtime; se evita introducir interpretación de prosa en el ejecutor.
- **C — Reject (no cambiar y registrar el límite).** Mantener el comportamiento actual y registrar la diferencia como límite aceptado / pending decision con owner, sin declararla resuelta. Consecuencia: el `Closed` derivado sigue siendo alcanzable sin determinaciones; el límite queda explícito y verificable.

## CRITERIA (obligatorios, evaluables)

1. **Consistencia normativa (correctness).** ¿Puede el mismo repositorio afirmar a la vez «cierre sin determinaciones = STOP» (§7) y derivar `Closed` sin ellas? ¿Qué lectura es la correcta?
2. **Autoridad.** ¿Quién puede declarar un Change cerrado? El host «nunca escribe `Closed` como status» (`runtime/orchestrator/host.py`, docstring) pero escribe el registro de cierre con `Condición derivada: Closed`; ¿es eso un acto de cierre o una lectura?
3. **Integración con el Change Lifecycle.** ¿La condición derivada y el acto de cierre son la misma cosa? ¿C-1/C-2/C-3 (los gates que la derivación sí consulta) cubren o no la obligación de impacto?
4. **Coste y viabilidad.** A exige representación derivable (campos estructurados) y amplía los stops; B exige una enmienda de policy (DEV, no payload); C no tiene coste de implementación pero mantiene el límite.
5. **Mantenibilidad / verificabilidad.** §5.1/§5.2 declaran «Enforcement: governance, not a semantic validation; no checker interprets prose». ¿A contradice ese diseño? ¿B lo preserva? ¿Qué evidencia quedaría verificable?
6. **Reversibilidad y evidencia.** ¿Alguna opción exige tocar artefactos cerrados o reescribir historia? ¿El cierre derivado de corridas ya ejecutadas (planes 122/123) se vuelve inválido? ¿Cómo se registra la decisión sin reabrir cierres?

## EVIDENCE BASE (verificable a HEAD)

- `.agents/policies/validation-closure.md:5.1 Documentation impact (closure determination)` — obligación de determinar el impacto documental al cierre; tres clasificaciones excluyentes; se registra en `## Checkpoint / cierre`; «Enforcement. The obligation is governance, not a semantic validation. No checker interprets prose».
- `.agents/policies/validation-closure.md:5.2 Roadmap impact (closure determination)` — determinación independiente de §5.1; misma disciplina de enforcement.
- `.agents/policies/validation-closure.md:7. Stop conditions (validation/closure)` — bullet bloqueante: «Closure without an explicit Documentation impact determination (5.1) or without an explicit Roadmap impact determination (5.2), or with a classification outside `REQUIRED` / `NOT_REQUIRED` / `DEFERRED` in either».
- `runtime/orchestrator/derivation.py:derive_next_action` — pasos 11–14: `CLOSED_DERIVED` se emite tras status `Executed`, anchor, checkpoint (`closure_tree == current_state_identity`) y gates C-1/C-2/C-3 re-leídos; `closure_gate_problems` sólo consulta C-1/C-2/C-3.
- `runtime/orchestrator/host.py` — docstring: «There is no state machine … `Closed` is a derived condition, never a status the host writes»; rama `RECORD_CHECKPOINT` de `_write_record` escribe `build_checkpoint_body(..., condition="**`Closed`** (con release pendiente) — …")`; `_governance_facts` devuelve sólo cuatro hechos (INDEX registra el Plan, anchor, `Status: Executed`, `Nota de ejecución`).
- `runtime/orchestrator/governance.py:build_checkpoint_body` — cuerpo del registro de cierre GC-1; no hay campo de impacto.
- `tests/test_autonomous_orchestrator.py` — fixture `plan_text(..., closed=True)` con `Condición derivada: Closed` y sin determinaciones de impacto; `test_full_loop_derives_closed_from_real_evidence` exige `run.terminal_action == "CLOSED_DERIVED"`.
- `docs/plans/122-dev-autonomous-orchestrator-mvp.md` y `docs/plans/123-dev-agent-worker-mvp.md` — corridas reales del host que terminaron en `CLOSED_DERIVED` con las condiciones derivadas registradas; historia que no se reescribe.
- `docs/behavior-patterns.md:2.2 Condiciones que se derivan` (aprox. L129–L135) — `Closed` se deriva, nunca se escribe; la condición derivada alcanzada es cierre derivado; release es autoridad humana.
- `docs/VERSIONING.md:10. Definition of Done` — las dos determinaciones de impacto son condición de cierre del Change (RFC-56 N/A para planes docs-only).
- **Provenance Working (versionada, no normativa):** `docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md:3.6` hallazgo `c` — registra la tensión como `CONTRADICTION`. **Declaración de techo:** el mismo documento Working contiene además una inclinación previa hacia hacer que el ejecutor consulte las obligaciones ya escritas (`:9.1 FACT 3`; `:9.3 DESIGN_OPTION` propuesta (2); `:HD-OPS-G`), es decir, hacia una dirección compatible con la opción A. No hay decisión registrada, pero el caso **no** es neutral: la revisión se hace sobre un baseline informado por ese análisis y por esa inclinación.
- **Ausencia de parsers:** `git grep -n -i "Documentation impact\|Roadmap impact" -- runtime/ tools/` no encuentra código de cierre que las lea (verificación del Lead a HEAD; el patrón no matchea `runtime/README.md` porque éste no contiene esas cadenas en HEAD).

## EVIDENCE STATE (hechos verificados a HEAD, no interpretación)

1. La policy vigente declara obligatorias y bloqueantes las dos determinaciones de impacto en el cierre, y declara que su enforcement es gobernanza (sin checker de prosa).
2. La derivación del host no lee ninguna de las dos determinaciones ni tiene código que las parsee; su precondición de `CLOSED_DERIVED` es status/anchor/checkpoint/gates C-1/C-2/C-3.
3. El host **escribe** el registro `## Checkpoint / cierre` del Plan con `Condición derivada: Closed` cuando deriva el cierre; ese cuerpo no incluye las determinaciones.
4. Corridas reales versionadas (planes 122/123) alcanzaron `CLOSED_DERIVED` y sus registros de cierre derivado existen en planes cerrados.
5. Ningún artefacto versionado resuelve la tensión entre 1 y 2/3; el hallazgo está registrado sólo como `CONTRADICTION` en un documento Working de 2026-09-22, que no resuelve la decisión pero **sí registra una inclinación** hacia que el ejecutor consulte las obligaciones ya escritas (ver `## CONTAMINATION CEILING`).
6. La policy y la documentación del host son coherentes en el otro sentido: el host no escribe `Closed` como status ni release; el desacuerdo es sobre si la **condición derivada** y el **registro de cierre** quedan alcanzados por §5.1/§5.2/§7.

## EVIDENCE RULES / CONSTRAINTS

- Toda afirmación debe anclarse con `ruta:sección` verificable en el HEAD de evidencia congelado (`ac7f680`), con `git show ac7f680:<path>` cuando el árbol de ejecución haya avanzado, o con un comando reproducible declarado.
- No se cita `PRIORITY.md` ni ningún insumo local no versionado (contención RFC-69 I2; precedente `<PLAN-178>:F-2`).
- No se modifica ni se reescribe ningún artefacto cerrado (planes 122/123, RFCs, ADRs); la decisión se registra en artefactos vivos de DEV o en un artefacto nuevo que los referencia.
- Las rutas `runtime/`, `.agents/policies/`, `docs/plans/_TEMPLATE.md` y la documentación viva son **superficies hipotéticas** de una materialización futura que exigiría su propio Change autorizado; la review **no escribe ninguna de ellas** y este FRAME **no autoriza nada**. Ninguna opción exige `protocol/.agents/` (sería RFC-56 Clase A).
- `Closed` es una **condición derivada**, nunca un status que el host escriba; el FRAME no lo presenta como status.
- Cada pasada declara el material que recibió (`material_received`) y el que se le retuvo (`withheld_material`); ninguna pasada puede leer las conclusiones de otra antes de comprometer la propia.

## MATERIAL PROHIBIDO Y EXPOSICIÓN (v2)

Para que la comparación no se contamine con el experimento mismo, **ningún ejecutor de BASELINE, FULL o MAR** lee:

- `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md` (diseño/preregistro: contiene hipótesis, regla de decisión y el caso), `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_VALIDATION_2026-10-25.md` o `docs/plans/179-minimal-adversarial-review.md`;
- `docs/working/research/ADVERSARIAL_DELIBERATION_*` (campaña previa: contiene resultados y el mecanismo evaluado);
- cualquier contenido de `sessions/` (FRAME operativo, ledger, revisiones, salidas de otras condiciones) salvo el propio FRAME y el archivo de salida asignado;
- los insumos locales no versionados del mantenedor.

Puede leer el repositorio y su evidencia normal (incluido el documento Working que registra la tensión del caso: es parte del baseline informado y su efecto se declara). Cada ejecutor reporta la lista de material leído; la evaluación y la integridad auditan la exposición. Los ejecutores de **EVALUACIÓN/ADJUDICACIÓN/INTEGRIDAD** conocen la identidad de las condiciones y el caso, pero no reciben las hipótesis del Lead ni el diseño; reciben las definiciones congeladas verbatim.

## TRIGGER DECLARADO (antes de ejecutar)

Señales declaradas por el invocador para `MAR-VALID-01`: `materiality_potential=HIGH`, `ambiguity=HIGH`, `risk=MEDIUM`, `impact=HIGH`, `uncertainty=MEDIUM`, `irreversibility=MEDIUM`, `error_cost=HIGH`. Recomendación esperada de la regla congelada: **`REVIEW_TWO_PASS`**. La invocación es una **decisión declarada del Change** (plan 179) con motivo registrado: validar el mecanismo MAR, no decidir el caso. La review no decide sobre el caso.

## RECEPCIÓN DE MATERIAL (declarada, simétrica entre FULL y MAR salvo el conjunto de operaciones)

| Condición / pasada | Recibe |
|---|---|
| BASELINE | FRAME |
| FULL DEFENSE / PROSECUTION | FRAME (sin conclusión de la otra pasada) |
| FULL SYNTHESIS | FRAME + BASELINE cerrado + DEFENSE + PROSECUTION |
| FULL REBUTTAL (solo si la síntesis identifica un desacuerdo material) | FRAME + BASELINE + DEFENSE + PROSECUTION + SYNTHESIS + la objeción identificada |
| MAR PASS 1 / PASS 2 | FRAME (sin conclusión de la otra pasada) |
| MAR SYNTHESIS | FRAME + BASELINE cerrado + PASS 1 + PASS 2 |
| EVALUACIÓN | FRAME + todas las condiciones cerradas + costes |
| ADJUDICACIÓN | FRAME + evaluación + hallazgos disputados |
| INTEGRIDAD | FRAME + ledger + todos los artefactos crudos + declaraciones de material |


## CONTAMINATION CEILING (declarado, v2)

El **hecho** está pre-diagnosticado en un documento Working versionado (`INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md:3.6 c`, `CONTRADICTION`), y la fila del INDEX sigue `active`; la **decisión** no está resuelta en ningún plan, ADR, RFC ni policy. **Además, ese mismo Working contiene una inclinación previa hacia que el ejecutor consulte las obligaciones ya escritas (`:9.1 FACT 3`; `:9.3 DESIGN_OPTION` propuesta (2); `:HD-OPS-G`), compatible con la opción A y no neutral.** Por lo tanto el valor que se mida es **valor sobre un baseline informado**, no sobre un baseline ingenuo; la dirección de la inclinación se declara para que no se lea como descubrimiento independiente. La *forma* del hallazgo (regla declarada sin realización en el ejecutor) se parece a la de T2/AE-8 y a la observación `I-6` del Working: el caso es independiente **en objeto y decisión**, pero no se presenta como independiente en forma. Los ejecutores tienen acceso normal al repositorio (incluido el Working); la exposición se audita en la evaluación e integridad.

## LIMITS

- `n=1`, mismo modelo/proveedor en todas las pasadas: separación **procedural**, no independencia epistémica.
- El baseline es un agente instruido, no el proceso normal vivo; recibe un FRAME formal que el proceso normal podría no tener.
- Theoretical Execution no participa; no se modifica su policy.

## BASELINE (definido, no ejecutado a la fecha de congelamiento)

El baseline responde la QUESTION con CANDIDATE y CRITERIA mediante análisis normal (sin instrucción adversarial), produce decisión/recomendación con plan y evidencia, y se congela (hash) antes de que empiece cualquier pasada del tratamiento. La comparación de retención se hace contra el tratamiento completo ejecutado sobre este mismo FRAME.
