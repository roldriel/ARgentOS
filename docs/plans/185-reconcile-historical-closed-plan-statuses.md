# Plan 185 — Reconcile Historical Closed Plan Statuses

**Status:** Aprobado para ejecución
**Fecha:** 2026-11-03
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L1
**Depende de:** Plan 184
**Origen:** failure of the Plan 184 closeout battery on the repository-level structural checker; four already-closed historical plans use the derived `Closed — ...` annotation while the checker only accepts canonical plan status values.
**Work type:** GAP
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Reconcile the historical representation `Status: Closed — <outcome>` used by Plans 180–183 with the current convention that `Closed` is a derived lifecycle condition rather than a plan status, without reopening or rewriting those closed artifacts. The correction must make the structural checker backward-compatible with the historical records while keeping new plans on the canonical status cycle.

This is a DEV-only governance/tooling correction. It does not modify `protocol/.agents/`, `dist/`, runtime behavior, or the historical plan documents.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Corregir el bloqueo real de cierre de Plan 184 sin reescribir planes cerrados. | humano | instrucción del mantenedor de continuar y ejecutar la corrección |
| `P-2` Confianza de intención | HIGH | agente | failure observado en `tests/test_check_plan_structure.py::test_real_repo_has_no_violations` |
| `P-3` Conjunto de contexto | conventions, checker, tests y Plans 180–184 | agente | `docs/CONVENTIONS.md:Convenciones`, `tools/check_plan_structure.py`, `tests/test_check_plan_structure.py`, `docs/plans/180-comparative-architecture-refactor-study.md` … `184-new-agent-adoption-conformance-test.md` |
| `P-4` Derivabilidad | El bloqueo es una incompatibilidad entre checker vigente y representación histórica cerrada; la evidencia no justifica editar los planes cerrados. | agente | failure report + `AGENTS.md:Task lifecycle` |
| `P-5` `work_type` | GAP | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` |
| `P-6` Conocimiento vigente | Plans 180–183 están cerrados y deben conservar su registro histórico. | documento | `docs/plans/INDEX.md` y headers de los planes |
| `P-7` Reglas aplicables | Closed is derived; closed artifacts are terminal; checker is evidence, not authority. | agente | `AGENTS.md:Task lifecycle` y `docs/CONVENTIONS.md:Convenciones` |
| `P-8` Autoridad y scope | DEV-only: `tools/check_plan_structure.py`, su suite de tests, Plan 185 e INDEX; sin payload/runtime/dist y sin editar Plans 180–183. | humano | instrucción directa del mantenedor |

## Integration continuity

### Integration obligations

| Obligation | Declaration |
|---|---|
| **Expected consumer(s)** | `tests/test_check_plan_structure.py` and the Plan 184 closeout battery |
| **Contract / lifecycle extended** | Structural checking of historical DEV plan status representation; no protocol contract changes |
| **Intentional isolation** | Historical plan documents remain immutable; compatibility is implemented in the DEV checker/test layer |

### Integration result vocabulary

`INTEGRATED` requires the checker and its regression tests to recognize the historical representation while preserving rejection of malformed/non-closed uses.

## Criterio de entrada

- [x] Plan 184 execution evidence exists and its final verifier passed.
- [x] The blocking structural failure is reproducible from the repository evidence.
- [x] Plans 180–183 are closed historical artifacts and must not be rewritten.
- [x] No Protocol payload change is required.

## Entregables

1. `docs/plans/185-reconcile-historical-closed-plan-statuses.md`
2. `tools/check_plan_structure.py` compatibility rule for historical `Closed — <outcome>` headers with `Lifecycle: closed`.
3. `tests/test_check_plan_structure.py` regression coverage for accepted and rejected legacy representations.
4. `docs/plans/INDEX.md` registration and Plan 184 closeout record.

## Pasos

1. Register this Plan as `Aprobado para ejecución` in `docs/plans/INDEX.md`.
2. Extend `check_plan_structure.py` so `Closed — <outcome>` is accepted only as a historical plan representation when `**Lifecycle:** closed` is present; normalize it to `Executed` for status/index comparison. Do not add `Closed` to the canonical status cycle.
3. Add focused unit tests for the compatibility rule, lifecycle guard, and status/index normalization.
4. Re-run the structural checker and the focused test suite.
5. Re-run the Plan 184 canonical closeout battery, including pytest.
6. If green, record Plan 184 as `Executed`/closed-derived in its INDEX and add its closeout evidence without modifying the historical Plans 180–183.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno fuera del DEV repository; no payload/runtime/dist mutation | Plan 185 / maintainer instruction | authorized |

## Criterios de salida

- [ ] `check_plan_structure.py` accepts Plans 180–183 without changing their files.
- [ ] A `Closed — ...` plan without `Lifecycle: closed` remains a structural violation.
- [ ] Canonical new plan statuses remain unchanged.
- [ ] The structural checker and focused tests pass.
- [ ] Plan 184 closeout battery passes after the correction.
- [ ] Plans 180–183 remain byte-for-byte untouched.

## Verificación

- `python tools/check_plan_structure.py --root .`
- `python -m pytest tests/test_check_plan_structure.py`
- Full Plan 184 closeout battery from `CLOSE_PLAN184_FIXED_v3.ps1` or an equivalent corrected command set, including `python -m pytest tests/`.
- Git diff inspection confirming no edits to Plans 180–183 and no changes under `protocol/.agents/`, `runtime/`, or `dist/`.

## Validation anchor

- **Declared scope:** Plan 185, `docs/plans/INDEX.md`, `tools/check_plan_structure.py`, `tests/test_check_plan_structure.py`; Plan 184 closeout evidence.
- **Validation command-set:** structural checker, focused checker tests, Plan 184 canonical gates, full pytest.
- **Effective inputs (repo content):** refactor HEAD `4dab99818d585cbebff13d93068ad9a0f7f81eb7`; Plans 180–184; checker/tests listed above.
- **Observed dependencies:** Plan 184 closeout was blocked only by the four historical status violations.
- **Environmental factors:** Windows/PowerShell closeout runner; Python/pytest versions recorded by the closeout run.
- **Scoped Content Identity:** populated at validation.
- **Validity / stale:** populated at validation.

## Checkpoint / cierre

Populated only after validation and commit.

## Findings / Correcciones / Pending

### Findings

N/A — no lineage finding is registered before execution; the blocking condition is recorded in the plan origin and validation anchor.

### Correcciones

N/A — no correction is considered validated until the focused tests and Plan 184 closeout battery pass.

### Pending decisions

- No pending decisions at plan creation.

## Riesgos

- Accepting `Closed — ...` without a lifecycle guard would silently expand the canonical status vocabulary. The test must prevent that.
- Normalizing historical headers to `Executed` would destroy historical evidence and violate the closed-artifact rule; this plan explicitly avoids that repair.

## Nota de ejecución

Populated after execution.