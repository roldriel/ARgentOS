# Plan 174 — Materialización y cierre del modelo RFC-56 / A-B-C

**Status:** Executed
**Fecha:** 2026-10-23
**Tipo:** Plan
**Lifecycle:** active
**RFC:** RFC-56 (`docs/rfc/56-governance-fast-track.md`; enmienda del modelo de clasificación del payload)
**RFC-56 Class:** N/A (sin payload delta: el Change solo modifica documentación DEV; `protocol/.agents/` no se toca)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 2 — multi-área DEV (`docs/`, `.agents/` y el `AGENTS.md` raíz). *architectural impact*: 2 — precisa el modelo de gobernanza en la frontera RFC-56 × RFC-75, de forma aditiva y reversible por una enmienda posterior; no cambia ningún contrato del payload. *release impact*: 0 — docs-only, sin versión ni tag (RFC-69). *duration/complexity*: 2 — auditoría global, TE pre/post y batería completa.
**Depende de:** RFC-56 `Accepted`; RFC-75 `Accepted`; RFC-46 `Accepted`; RFC-69 `Accepted`; Planes 171/172/173 (registro histórico reciente)
**Origen:** instrucción directa del mantenedor (2026-10-23) — «PRIORITY 3 — MATERIALIZACIÓN Y CIERRE DEL MODELO RFC-56 / A-B-C» — y el documento de prioridades del mantenedor (`PRIORITY.md`, no versionado), §3 «Revisión de RFC 56 y del modelo documental A/B/C». El análisis conceptual ya fue resuelto por auditoría y Theoretical Execution; este Plan lo materializa, lo audita y lo cierra.
**Work type:** `GAP`
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Materializar en la documentación vigente el modelo conceptual ya resuelto de RFC-56 y del
modelo A/B/C, eliminar las formulaciones que hoy permiten dos rutas razonables para el mismo
caso, verificar el resultado con Theoretical Execution (pre y post materialización) y cerrar
Priority 3 si las gates del lifecycle quedan satisfechas.

El modelo a materializar, tomado como hipótesis de trabajo y confirmado por TE durante este
Plan, es:

```text
Change
│
├── sin efecto sobre protocol/.agents/  → RFC-56 = N/A
│
└── uno o más payload deltas
      ├── Class A → RFC Accepted + Plan
      ├── Class B → Plan
      └── Class C → Direct (si la ruta directa es aplicable)

Ruta efectiva del Change = clase más estricta presente:  A > B > C > N/A
```

**Este Plan no** crea una entidad `Change` ni `Payload Delta`, no agrega una clase `AB`, no
crea un registry, no implementa TE como feature del protocolo, no modifica DEV Memory, no
altera el modelo de autonomía ni RFC-75, no toca `protocol/`, `runtime/`, `tools/`, `tests/`
ni `dist/`, y no reescribe planes, RFCs o ADRs cerrados.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Materializar el modelo A/B/C ya resuelto (payload delta, multi-clase, ruta efectiva, N/A, semántica de C, checker como evidencia, clase más estricta) y cerrar Priority 3 en una ejecución, con TE y validación completas | humano | instrucción directa del mantenedor de esta sesión; el documento de prioridades del mantenedor (`PRIORITY.md`, no versionado), §3 «Revisión de RFC 56 y del modelo documental A/B/C» |
| `P-2` Confianza de intención | `HIGH` — el pedido fija el modelo, el alcance, las gates y los negativos; no introduce una decisión nueva | agente | instrucción del mantenedor (secciones 1–24) |
| `P-3` Conjunto de contexto | RFC-56; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/plans/_TEMPLATE.md`; `AGENTS.md`; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/validation-closure.md`; RFC-46; RFC-75; `docs/placement-contract.md`; Plan 94 §9.2; planes 171/172/173; auditoría global de usos | agente | las rutas citadas |
| `P-4` Derivabilidad | `DERIVABLE` — la normativa vigente (RFC-56 `Accepted`, RFC-75, RFC-46) más TE determinan el modelo; no hay una decisión de autoridad pendiente. La única puerta es la autorización de ejecución del mantenedor | agente | este Plan; `## Theoretical execution (pre-materialización)` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type (adoptado por el Plan 152, 2026-10-07)` |
| `P-6` Conocimiento vigente | RFC-56, RFC-46, RFC-69 y RFC-75 `Accepted`; `docs/CONVENTIONS.md` y `docs/VERSIONING.md` activos; Plan 94 `Executed` (matriz operacional referenciada); planes 171/172/173 `Executed`/`Closed` (traza histórica) | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (lifecycle), RFC-69 (cierre docs-only), RFC-46 (no reescribir historia), VC-1, GC-1, LC-1, PC-1, `docs/VERSIONING.md:4.1 Batería canónica de verificación`. `NOT_APPLICABLE`: RFC-56 (no hay payload delta: el Change es RFC-56 N/A), release (docs-only). | agente | `docs/CONVENTIONS.md:Convenciones`; `docs/VERSIONING.md` |
| `P-8` Autoridad y scope | Autoridad: mantenedor, por instrucción directa que autoriza la ejecución de este Plan. Scope declarado: las once rutas de `## Entregables` (ampliado antes de ejecutar por `HD-K1` al detectar, en la auditoría, la cita de `docs/placement-contract.md` a la sección superada de RFC-56). No se amplía por inferencia | humano | este Plan |

## Criterio de entrada

- [x] RFC-56, RFC-75, RFC-46 y RFC-69 están `Accepted`; `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` y `.agents/` existen en el baseline `66d132b`.
- [x] Worktree sin cambios preexistentes tracked; los dos untracked del mantenedor (`PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md`) permanecen intactos y fuera del scope.
- [x] Plan registrado en `docs/plans/INDEX.md` con el mismo `Status` del header (mismo commit).
- [x] **Autorización de ejecución:** instrucción directa del mantenedor de esta sesión (2026-10-23), que autoriza materializar, verificar y cerrar Priority 3:

```text
PLAN_ID                   = 174
AUTHORIZATION             = MAINTAINER_AUTHORIZED_FOR_EXECUTION (Priority 3)
AUTHORITY_CLASS           = DEV_PLAN (RFC-56 Class: N/A — sin payload delta)
EXECUTION_AUTHORIZED      = YES
RFC_REQUIRED              = NO
PROTOCOL_AUTHORITY        = UNCHANGED (0 diff en protocol/, dist/ y VERSION)
```

  Aplica solo al scope de este Plan. **Satisfecha.**
- [x] Ninguna pending decision bloqueante sin resolución/escalación. **Satisfecha.**

## Entregables

1. `docs/rfc/56-governance-fast-track.md` — banner de enmienda, texto original conservado como registro histórico, sección `## Modelo vigente (enmienda 2026-10-23)` y entrada de `## Amendment Log`.
2. `docs/CONVENTIONS.md` — bullet «Inmutabilidad y clasificación de cambios del payload (RFC-56)», criterio `C-3`, campo de intake y ortogonalidad con Change Level.
3. `docs/plans/_TEMPLATE.md` — campo canónico `**RFC-56 Class:**` con `N/A`, composición multi-clase y separación explícita de `**Change Level:**`.
4. `docs/VERSIONING.md` — §4 (playbook de autorización) alineado con las clases por payload delta y con RFC-56 N/A.
5. `AGENTS.md` (raíz) — `Do NOT` y `Task lifecycle`.
6. `.agents/AGENTS.md` — reglas operativas 1 y 2.
7. `.agents/workflows/change-lifecycle.md` — §1 (clasificación), §2 (gate de autorización), §3 (header del Plan) y §11 (ejemplo dogfood).
8. `.agents/policies/validation-closure.md` — §5.1/§5.2 (registro de impacto para un cambio sin Plan).
9. `docs/plans/INDEX.md` — nueva serie y fila del Plan 174; actualización del estado del registro.
10. `CHANGELOG.md` — entrada en `[Unreleased]` con `(plan 174)`.
11. `docs/placement-contract.md` — cita de la autoridad del dominio Protocol actualizada a la sección vigente de RFC-56 (dejaba de apuntar a la formulación superada).

El Plan mismo (este archivo) queda **fuera** del `Scoped Content Identity` declarado (anti-auto-referencia).

## Pasos

### Paso 0 — Preflight y baseline

- **Archivo:** ninguno (lectura).
- **Modificación:** ninguna.
- **Motivo:** fijar el estado del que parte la ejecución y verificar que no hay cambios ajenos.
- **Resultado esperado:** `git status` solo con los dos untracked del mantenedor; HEAD `/` branch registrados; batería baseline en verde.
- **Evidencia:** `git status --porcelain=v2 --branch`; `git rev-parse HEAD`; batería completa.
- **Validación posterior:** si aparece un cambio tracked ajeno, `STOP`.

### Paso 1 — Enmendar RFC-56

- **Archivo:** `docs/rfc/56-governance-fast-track.md`.
- **Modificación:** (a) banner bajo el header que declara la enmienda vigente y remite a la nueva sección; (b) marcar `## Decisión propuesta` como superada, conservando su texto íntegro (RFC-46); (c) agregar `## Modelo vigente (enmienda 2026-10-23)` con payload delta, clases A/B/C, definición semántica de C, checker como evidencia, multi-clase, ruta efectiva, RFC-56 N/A, ortogonalidad con Change Level y ruta directa aplicable; (d) entrada en `## Amendment Log` con la autoridad del Plan 174.
- **Motivo:** `docs/rfc/56-governance-fast-track.md:Decisión propuesta` es la fuente normativa de la clasificación y hoy no distingue payload delta de Change, no contempla multi-clase ni N/A, y ata Class C al resultado de un checker.
- **Precondición:** Paso 0.
- **Resultado esperado:** una única formulación operativa vigente y el registro histórico intacto.
- **Evidencia:** `git diff -- docs/rfc/56-governance-fast-track.md`; `python tools/check_plan_citations.py`.
- **Validación posterior:** TE post-materialización, escenarios T1–T15.

### Paso 2 — Alinear `docs/CONVENTIONS.md`

- **Archivo:** `docs/CONVENTIONS.md`.
- **Modificación:** reescribir el bullet de clases; corregir `C-3` (payload delta → clasificación por delta, no «Plan + RFC-56» automático); renombrar el campo de intake a `**RFC-56 Class:**`; precisar la independencia respecto de Change Level.
- **Motivo:** elimina la formulación «todo payload touch → Plan + RFC-56», que contradice Class C, y el registro de un campo que ya no existe.
- **Precondición:** Paso 1.
- **Resultado esperado:** CONVENTIONS y RFC-56 no se contradicen.
- **Evidencia:** `git diff -- docs/CONVENTIONS.md`.

### Paso 3 — Corregir el template de Plan

- **Archivo:** `docs/plans/_TEMPLATE.md`.
- **Modificación:** reemplazar `**Clase:** A | B` por `**RFC-56 Class:** N/A | A | B | C` (multi-clase `A, B`), con comentario que separa la clase del Change Level y aclara que `A | B` no es una clase combinada.
- **Motivo:** el campo actual (a) ofrece `A | B` como si fuera una enumeración de una única dimensión y (b) fuerza un valor incluso sin efecto payload; once planes vigentes escribieron `Clase: B` sin payload effect.
- **Precondición:** Paso 2.
- **Resultado esperado:** un Plan nuevo no puede inducir una clase combinada ni una clase para un cambio DEV-only.
- **Evidencia:** `git diff -- docs/plans/_TEMPLATE.md`; `python -m pytest tests/test_autonomy_effects_dogfood.py -q`.

### Paso 4 — Alinear `docs/VERSIONING.md`, `AGENTS.md` y `.agents/`

- **Archivos:** `docs/VERSIONING.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md`, `.agents/policies/validation-closure.md`.
- **Modificación:** reemplazar las formulaciones que asocian «todo cambio del payload» a una única vía por la clasificación del payload delta y la ruta efectiva; declarar `RFC-56 N/A` para cambios sin efecto payload; actualizar el registro de impacto de un cambio sin Plan (Clase C o acción directa, no «Class C = sin Plan»).
- **Motivo:** son instrucciones activas de operación: una formulación ambigua induce una ruta incorrecta antes de llegar a RFC-56.
- **Precondición:** Paso 2.
- **Resultado esperado:** las instrucciones operativas derivan la ruta de la clase, no del mero contacto con `protocol/`.
- **Evidencia:** `git diff -- <rutas>`.

### Paso 5 — Registrar el Change

- **Archivos:** `docs/plans/INDEX.md`, `CHANGELOG.md`.
- **Modificación:** nueva serie `Centésima primera serie` con la fila del Plan 174 (`Executed`), actualización del párrafo de estado del INDEX y entrada `### Changed` en `[Unreleased]`.
- **Motivo:** registro derivado del Change y changelog de la próxima versión (RFC-69: docs-only, sin `VERSION` ni tag).
- **Precondición:** Pasos 1–4.
- **Resultado esperado:** INDEX espejo del header; changelog con trazabilidad `(plan 174)`.
- **Evidencia:** `python tools/check_plan_structure.py`; `python tools/check_version_state.py`.

### Paso 6 — Validación y anchor

- **Archivo:** este Plan (`## Validation anchor`).
- **Modificación:** ejecutar la batería canónica, los gates C-1/C-2/C-3 y la suite completa; computar el `Scoped Content Identity` del scope declarado con `tools/scoped_content_identity.py`; registrar el anchor A1.
- **Motivo:** VC-1; la validación es evidencia factual, no autoridad.
- **Precondición:** Pasos 1–5.
- **Resultado esperado:** batería en verde y anchor completo.
- **Evidencia:** salida de los comandos en `## Nota de ejecución`.

### Paso 7 — TE post-materialización y cierre

- **Archivo:** este Plan (`## Nota de ejecución`, `## Checkpoint / cierre`, `## Findings / Correcciones / Pending`).
- **Modificación:** re-ejecutar TE sobre el texto materializado (T1–T15), registrar findings/correcciones, las dos determinaciones de impacto, el checkpoint y la condición derivada.
- **Motivo:** demostrar que el repositorio ya no deja dos rutas razonables para el mismo caso.
- **Precondición:** Paso 6.
- **Resultado esperado:** `Closed` derivado, o el motivo exacto por el que no se cierra.
- **Evidencia:** `## Nota de ejecución`; C-1/C-2/C-3.

### Paso 8 — Commit atómico en `dev`

- **Archivo:** todos los anteriores.
- **Modificación:** un commit atómico en `dev` con Conventional Commit en inglés que declare la vía (`plan 174`) y la condición derivada.
- **Motivo:** `Committed` es estado del repositorio; `Released` no aplica (docs-only, RFC-69).
- **Precondición:** Paso 7.
- **Resultado esperado:** `dev` con el Change materializado; sin tag, sin promoción, sin `dist`.
- **Evidencia:** `git log -1`, `git status`.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change solo escribe documentación DEV; no hay red, git remoto, instalación, operación destructiva ni escritura fuera del proyecto | instrucción del mantenedor (2026-10-23) + este Plan | authorized |

## Theoretical execution (pre-materialización)

TE es el mecanismo de razonamiento de esta decisión, no un artifact por escenario. Para cada
caso: `payload effect?` · `RFC-56 class?` · `Change Level?` · `ruta efectiva?` · `Plan?` ·
`RFC?` · `Direct?` · `decisión humana?`.

| # | Caso | Payload | Clase | Nivel | Ruta efectiva | Plan | RFC | Direct | Humano |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Change C-only | sí | C | propio del Level (L0/L1 en el caso) | Direct | no | no | sí | no |
| T2 | Change B-only | sí | B | propio | Plan | sí | no | no | sí (aprobación del Plan) |
| T3 | Change A-only | sí | A | propio | RFC + Plan | sí | sí (`Accepted`) | no | sí (aceptación de la RFC) |
| T4 | Change A+B | sí | A | propio | RFC + Plan | sí | sí | no | sí |
| T5 | Change B+C | sí | B | propio | Plan | sí | no | no | sí |
| T6 | Change A+C | sí | A | propio | RFC + Plan | sí | sí | no | sí |
| T7 | Change A+B+C | sí | A | propio | RFC + Plan | sí | sí | no | sí |
| T8 | Change sin payload effect | no | N/A | propio (p. ej. L2) | lifecycle + Level | según Level | no | solo si el Level no exige Plan | según la vía del Level |
| T9 | payload + tooling | sí (delta de payload) + tooling DEV | la del delta | propio | la del payload delta | según clase | según clase | según clase | según clase |
| T10 | C + L3 | sí | C | L3 | Plan (el Level exige maquinaria completa; sin RFC) | sí | no | no (el Level no lo permite) | sí (aprobación del Plan) |
| T11 | A + L0 | sí | A | el que permitan las cinco dimensiones del Level | RFC + Plan | sí | sí | no | sí |
| T12 | documentación de payload con cambio semántico | sí | A | propio | RFC + Plan | sí | sí | no | sí |
| T13 | documentación de payload sin cambio semántico | sí | B (o C si es mecánico) | propio | Plan (o Direct si C y aplica) | según clase | no | según clase | según clase |
| T14 | checker sin cambio, semántica potencialmente modificada | sí | no puede ser C por el checker: A o B según la semántica | propio | la de la clase semántica | sí | según clase | no | sí |
| T15 | checker cambiado, semántica preservada | sí | C posible si se demuestra preservación semántica | propio | Direct si aplica; si no, Plan | según Level | no | según Level | según Level |

Decisiones resueltas por TE (sin escalamiento): la composición multi-clase y la ruta por la
clase más estricta (T4–T7); la inexistencia de una clase `AB`; `RFC-56 N/A` (T8, T9); la
independencia Class ↔ Change Level (T10, T11); la semántica de C y el checker como evidencia
(T12–T15). Ningún caso quedó con dos interpretaciones normativas válidas.

## Auditoría de usos existentes

Búsqueda global de `RFC-56`, `Class A/B/C`, `Clase A/B/C`, `payload`, `Change Level`, `Direct`,
`Plan required`. Clasificación de los resultados (no se reescribe historia, RFC-46):

| Clase | Artefactos | Tratamiento |
|---|---|---|
| `CURRENT-NORMATIVE` | `docs/rfc/56-governance-fast-track.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `AGENTS.md`; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/validation-closure.md`; `docs/plans/_TEMPLATE.md`; `docs/placement-contract.md` (cita de autoridad del dominio Protocol) | Alineados en este Change |
| `CURRENT-NORMATIVE` sin cambio | `.agents/policies/authority.md` («RFC `Accepted` (authorization gate, RFC-56)»); `docs/AGENTS.md` (sin detalle de clases); `docs/rfc/INDEX.md` (fila de RFC-56: status sin cambio) | Verificados: la formulación sigue siendo correcta bajo el modelo (el payload se rige por RFC-56; la clase fija el artefacto). Sin edición |
| `CURRENT-DESCRIPTIVE` | `docs/plans/INDEX.md`; `CHANGELOG.md` | Actualizados en este Change |
| `HISTORICAL` | Planes 58–173 con `**Clase:**`; RFCs 32–84; ADRs 01–21; entradas históricas de `CHANGELOG.md`; `docs/architecture/*`; `docs/working/*`; `docs/AUDITORIA_DOCUMENTACION.md` | Preservados. La traza se interpreta por su fecha; no se reescribe |
| `LEGACY` | Planes con `**Clase:** —` (94–99 y otros) | Preservados. La ausencia del campo nuevo es legacy, no invalidez (RFC-75 Mecanismo 15) |
| `INCONSISTENT` (histórico, no reescrito) | Plan 112, 118, 119, 133, 134, 147, 153, 155, 171, 172, 173: declaran `Clase: B` sin payload effect | Registrado como `<PLAN-174>:F-3`; la guarda es hacia adelante (template + CONVENTIONS). No se editan los planes |

## Criterios de salida

- [ ] RFC-56 expresa inequívocamente payload delta, A/B/C, multi-clase, ruta efectiva, RFC-56 N/A, definición semántica de C, checker como evidencia y regla de la clase más estricta.
- [ ] `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md`, `docs/VERSIONING.md`, `AGENTS.md`, `.agents/AGENTS.md`, el workflow y la policy de cierre no contradicen RFC-56.
- [ ] La auditoría global está clasificada y los artefactos históricos quedan preservados.
- [ ] TE pre y post materialización ejecutadas; T1–T15 sin contradicciones ni casos irresueltos.
- [ ] Batería canónica, C-1, C-2 y C-3 en verde (los `GAP` declarados del corpus se preservan).
- [ ] Determinaciones de impacto documental y de Roadmap registradas (independientes).
- [ ] Sin ADR y sin pending decision bloqueante que exista solo por una ambigüedad resuelta aquí.
- [ ] Anchor A1 y checkpoint GC-1 registrados; condición derivada evaluada.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python tools/check_enforcement_declarations.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python tools/scoped_content_identity.py <scope>
```

## Riesgos

- **Ampliar el scope a un rediseño documental.** Mitigación: solo las once rutas de los entregables; no se crean entidades, registries ni clases.
- **Convertir una inferencia en autoridad.** Mitigación: cada regla materializada se deriva de RFC-56 `Accepted`, RFC-75, RFC-46 o TE; lo no derivable se habría escalado (no ocurrió).
- **Reescribir historia.** Mitigación: el texto original de RFC-56 se conserva; los planes cerrados no se editan.

## Trazabilidad

```text
documento de prioridades del mantenedor, §3 (Revisión de RFC-56 y del modelo A/B/C)
        ↓
auditoría + TE conceptual previa
        ↓
Plan 174 (materialización) → RFC-56 (enmienda) + CONVENTIONS + TEMPLATE + instrucciones DEV
        ↓
TE post-materialización → batería + C-1/C-2/C-3 → anchor + checkpoint
        ↓
Closed (dev) · Released = NO (docs-only, RFC-69)
```

## Validation anchor

**Validation anchor (VC-1).**

- **Declared scope:** las once rutas de la materialización: `.agents/AGENTS.md`, `.agents/policies/validation-closure.md`, `.agents/workflows/change-lifecycle.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md` y `docs/rfc/56-governance-fast-track.md`. Este Plan queda **fuera** del scope medido (anti-auto-referencia).
- **Validation command-set:** los ocho checkers de `docs/VERSIONING.md:4.1 Batería canónica de verificación`; los tres gates de lifecycle C-1/C-2/C-3; `python -m pytest tests/`; `git diff --check`; y la recomputación del Scoped Content Identity con `tools/scoped_content_identity.py`.
- **Effective inputs (repo content):** las once rutas del scope en el estado validado (commit de implementación `03d4001`, tree `cc1d81f703fb250d9ae83a08388fe1c15feffb91`); el corpus completo que consumen los checkers y la suite; el Plan 174 fuera del scope.
- **Observed dependencies:** intérprete Python con biblioteca estándar (`tools/`, `tests/`), `pytest`, CLI `git`. Sin red, sin servicios externos, sin instalación de componentes del payload.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.1.1; `git` 2.55; `core.autocrlf = true`; `check_dist_sync.py` no aplica (local-only; rojo en `dev`); `check_plan_structure.py` reporta los 2 `GAP` declarados (157/158); C-1 reporta el `GAP` del propio anchor y C-2 el del propio checkpoint en el estado validado (se escriben después de la validación, por diseño); C-3 reporta los cuatro `GAP` legacy declarados (155/158/168/169); `check_version_state.py` emite los 9 warnings históricos de versiones sin tag.
- **Scoped Content Identity:**
  - **State identity (estado validado):** `cc1d81f703fb250d9ae83a08388fe1c15feffb91` (tree del índice staged del estado validado; tree del commit de implementación `03d4001`).
  - **Delta scoped identity:** `4eedde4da0833d331c7487a540ca8407c939e10cf493542a7d7f60edfa7503b0` (scope = las once rutas declaradas; serialización `scoped-v1`, orden canónico).
  - **Scope set (repo-relative paths, ordenados):** las once rutas del scope declarado.
- **Validity / stale:** `vigente`. El commit de cierre agrega únicamente este Plan, excluido del scope medido; el delta recomputado sobre el estado de cierre es idéntico al declarado y el estado validado es el del commit de implementación.
- **Battery result (estado validado S0):** 8 checkers: 7 PASS + `check_plan_structure` PASS con 2 `GAP` declarados; C-1 `VALID=79 GAP=1 ANOMALY=0` (el `GAP` es el anchor de este Plan, escrito después); C-2 `VALID=78 GAP=2 ANOMALY=0` (116 y el checkpoint de este Plan); C-3 `VALID=38 GAP=4 ANOMALY=0`; `pytest tests/` **1435 passed**; `git diff --check` limpio; recomputación de identidad PASS.
- **Re-ejecución sobre el estado de cierre (S1):** mismos checkers y gates sobre el estado que incorpora este anchor y este checkpoint — 8 checkers PASS; C-1 `VALID=80 GAP=0 ANOMALY=0`; C-2 `VALID=79 GAP=1` (Plan 116) `ANOMALY=0`; C-3 `VALID=38 GAP=4 ANOMALY=0`; delta recomputado idéntico. Es una nota de la misma validación, no una A2: el Plan está fuera del scope declarado y ningún path del scope cambió (CL-2).

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** `03d4001` (commit de implementación: las once rutas del scope y este Plan; tree `cc1d81f703fb250d9ae83a08388fe1c15feffb91`) y el commit de cierre en `dev`, que incorpora este Validation Anchor, este Checkpoint y la `## Nota de ejecución`. El commit de cierre se localiza por su mensaje. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** State identity `cc1d81f703fb250d9ae83a08388fe1c15feffb91`; Delta scoped identity `4eedde4da0833d331c7487a540ca8407c939e10cf493542a7d7f60edfa7503b0`.
- **Estado de cierre (identidad):** State identity `cc1d81f703fb250d9ae83a08388fe1c15feffb91`; Delta scoped identity `4eedde4da0833d331c7487a540ca8407c939e10cf493542a7d7f60edfa7503b0` (el mismo estado validado, por correspondencia con el anchor aplicable).
- **Árbol material del commit de cierre:** no declarado; el commit de cierre aún no existe al escribir este checkpoint y agrega únicamente este Plan (excluido del scope). `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió; el delta recomputado sobre el estado de cierre coincide con el declarado.
- **Governance aplicada:** RFC-56 (enmienda; el Change es **RFC-56 Class: N/A** porque no tiene payload deltas); RFC-46 (texto original de RFC-56 conservado; planes cerrados no editados); RFC-69 (docs-only, sin release ni tag); RFC-75 (Mecanismo 7, checkpoint); ADR-16 (autoridad y evidencia); VC-1/GC-1/LC-1/PC-1; `docs/VERSIONING.md:4.1 Batería canónica de verificación`.
- **Documentation impact:** `REQUIRED` — actualizados en este Change: `docs/rfc/56-governance-fast-track.md` (modelo vigente, banner y Amendment Log), `docs/CONVENTIONS.md` (clases, `C-3`, intake, Change Levels, ciclo ADR y determinaciones de impacto), `docs/VERSIONING.md` (§4 y §7), `AGENTS.md` (`Do NOT` y `Task lifecycle`), `.agents/AGENTS.md` (frontera DEV/Protocol y reglas 1–2), `.agents/workflows/change-lifecycle.md` (§1–§3 y §11), `.agents/policies/validation-closure.md` (§5.1/§5.2), `docs/plans/_TEMPLATE.md` (campo canónico), `docs/placement-contract.md` (cita de autoridad del dominio Protocol), `docs/plans/INDEX.md` (serie y fila) y `CHANGELOG.md` (`[Unreleased]`). Evidencia: `git show --stat 03d4001` y la batería registrada en el anchor.
- **Roadmap impact:** `NOT_REQUIRED` — la materialización no crea, completa, cancela, reclasifica ni re-prioriza una iniciativa del mapa operativo de `ROADMAP.md` (no existe allí un ítem de RFC-56/A-B-C); el documento de prioridades del mantenedor no es el mapa operativo del repositorio ni su fuente de verdad.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance aplicada + checkpoint + consistencia + PASS). `Committed` es estado del repositorio; `Released` es `NO` (docs-only, RFC-69).

## Findings / Correcciones / Pending

### Findings

- `<PLAN-174>:F-1` — estado: `resolved` (corregido por `<PLAN-174>:C-1`); observación: la formulación original de RFC-56 ataba la declaración de Class C al resultado de un checker —«La clase C solo puede declararse si ningún checker cambia de resultado semántico (mismas secciones, mismas referencias)»—, lo que convierte la evidencia factual en condición de autoridad y deja sin definir la propiedad semántica que debe preservarse; un cambio de significado que no altere el resultado de ningún checker podía leerse como C; evidencia original: `docs/rfc/56-governance-fast-track.md:Decisión propuesta` (bullets de Clase C y de reglas de borde) en el baseline `66d132b`, y `.agents/AGENTS.md:Fundamental operating rules` regla 3 («A checker result is factual evidence, never normative authority»), que ya establecía la regla correcta; estado git observado: `dev` @ `66d132b89c0815deb7a84a23c38df997a8be9a16`, worktree sin cambios tracked y dos untracked del mantenedor; provenance original: auditoría de Priority 3 (2026-10-23), Paso 1 — lectura de RFC-56 contra el estado real del repositorio; resolución: `<PLAN-174>:C-1` define Class C por preservación de la semántica normativa y de los contratos del payload, declara el checker como evidencia y explicita que ni un checker sin cambio demuestra C ni uno cambiado obliga a A/B por sí solo; el texto original se conserva como registro histórico superado (RFC-46).

- `<PLAN-174>:F-2` — estado: `resolved` (corregido por `<PLAN-174>:C-2`); observación: la normativa vigente aplicaba las clases A/B/C a «todo cambio del payload» (el Change completo), sin distinguir el **payload delta**, sin composición multi-clase, sin ruta efectiva y sin un valor N/A para un Change sin efecto payload; en consecuencia, un Change con deltas de clases distintas no tenía una ruta única y un cambio DEV-only quedaba expuesto a recibir una clase «por defecto»; evidencia original: `docs/rfc/56-governance-fast-track.md:Decisión propuesta` («Clasificar todo cambio del payload»), `docs/CONVENTIONS.md:Convenciones` (bullet de clases), `docs/VERSIONING.md:4. Flujo por plan (playbook)` paso 1, `AGENTS.md:Task lifecycle` y `.agents/workflows/change-lifecycle.md:1. Change detection and classification`; estado git observado: `dev` @ `66d132b`; provenance original: auditoría de Priority 3 (2026-10-23), Pasos 1–2; resolución: `<PLAN-174>:C-1` y `<PLAN-174>:C-2` materializan la clasificación por payload delta, la composición multi-clase, la ruta por la clase más estricta (`A > B > C > N/A`, sin clase `AB`) y `RFC-56 N/A`, y alinean RFC-56, CONVENTIONS, VERSIONING, AGENTS raíz y la capa operativa `.agents/`.

- `<PLAN-174>:F-3` — estado: `resolved` (corregido por `<PLAN-174>:C-3`); observación: `docs/plans/_TEMPLATE.md` ofrecía `**Clase:** A | B` como una única enumeración —leíble como una clase combinada `A | B`— y forzaba un valor incluso para un Change sin efecto payload, mientras que el campo canónico de intake en CONVENTIONS seguía siendo `Clase`; el resultado es que planes DEV-only escribieron `Clase: B` sin payload effect; evidencia original: el header de `docs/plans/_TEMPLATE.md` (campo `Clase`) y `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)` en el baseline, más los headers de los planes 112, 118, 119, 133, 134, 147, 153, 155, 171, 172 y 173; estado git observado: `dev` @ `66d132b`; provenance original: auditoría de Priority 3 (2026-10-23), Pasos 3 y 12; resolución: `<PLAN-174>:C-3` reemplaza el campo por `**RFC-56 Class:** N/A | A | B | C` (multi-clase `A, B`), documenta que no existe una clase `AB` y alinea el campo de intake; la traza histórica de los planes listados se preserva y se registra en `<PLAN-174>:F-6`.

- `<PLAN-174>:F-4` — estado: `resolved` (corregido por `<PLAN-174>:C-4`); observación: `docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note (Plan/Note) (adoptado por el Plan 152, 2026-10-07)` afirmaba en el criterio `C-3` que tocar `protocol/.agents/` exige «**Plan** + vía RFC-56», y las secciones de impacto y la policy de cierre equiparaban «cambio sin Plan» con «Clase C / acción directa»; ambas formulaciones contradecían la ruta directa de Class C y la posibilidad de un Plan de clase C exigido por el Change Level; evidencia original: `docs/CONVENTIONS.md` (fila `C-3`, subsecciones de intake e impacto) y `.agents/policies/validation-closure.md:5.1 Documentation impact (closure determination)` / `:5.2 Roadmap impact (closure determination)` en el baseline; estado git observado: `dev` @ `66d132b`; provenance original: auditoría de Priority 3 (2026-10-23), Paso 2; resolución: `<PLAN-174>:C-4` corrige `C-3` (clasificación por delta + ruta efectiva) y reemplaza «Clase C / acción directa» por la descripción precisa (un cambio Clase C por debajo del Level que exige Plan, o una acción directa sin Plan).

- `<PLAN-174>:F-5` — estado: `resolved` (corregido por `<PLAN-174>:C-5`); observación: `docs/placement-contract.md` citaba la autoridad de cambio del dominio Protocol como `docs/rfc/56-governance-fast-track.md:Decisión propuesta`, una sección que la enmienda marca como superada; la cita resolvía mecánicamente pero apuntaba a la formulación histórica; evidencia original: la tabla de dominios de `docs/placement-contract.md` en el baseline; estado git observado: `dev` @ `66d132b`; provenance original: auditoría de referencias de Priority 3 (2026-10-23), Paso 4; resolución: `<PLAN-174>:C-5` actualiza la cita a `## Modelo vigente (enmienda 2026-10-23)`.

- `<PLAN-174>:F-6` — estado: `deferred`; observación: once planes vigentes declaran `Clase: B` sin payload effect (112, 118, 119, 133, 134, 147, 153, 155, 171, 172, 173); algunos lo hacen explícitamente contradictorio («mejora documental compatible; `protocol/.agents/` no se toca, por lo que RFC-56 no aplica»); son artefactos ejecutados/cerrados y su header es parte de la traza; evidencia original: headers listados en `## Auditoría de usos existentes` de este Plan, estado git `dev` @ `66d132b`; estado git observado: `dev` @ `66d132b`, sin modificaciones de esos archivos en este Change; provenance original: auditoría de Priority 3 (2026-10-23), Paso 12; owner: mantenedor; destino: traza histórica — no se reescriben (RFC-46; `.agents/AGENTS.md` regla 5); la guarda es hacia adelante y se materializa en `<PLAN-174>:C-3`.

### Correcciones

- `<PLAN-174>:C-1` — refs origen: `<PLAN-174>:F-1` y `<PLAN-174>:F-2`; alcance de revalidación: `docs/rfc/56-governance-fast-track.md` completo (banner, sección superada, `## Modelo vigente (enmienda 2026-10-23)` y `## Amendment Log`), más las citas y la batería canónica que lo consumen; evidencia: `python tools/check_plan_citations.py` → «All citations resolve», `python tools/check_protocol_invariants.py --payload protocol .` → OK, y TE post-materialización T1–T15 registrada en `## Nota de ejecución`; carácter: FACTUAL / TRACEABILITY (no normativo por sí mismo; la acción la autoriza este Plan y la instrucción del mantenedor); autorización: instrucción directa del mantenedor (2026-10-23) + este Plan `Aprobado para ejecución`; qué se corrigió: se enmienda RFC-56 con la unidad payload delta, la definición semántica de Class C, el checker como evidencia, las clases A/B/C, los Changes multi-clase y la ruta efectiva, `RFC-56 N/A`, la independencia respecto del Change Level y la regla de la clase más estricta; el texto original de `## Decisión propuesta` se conserva íntegro y marcado como superado.

- `<PLAN-174>:C-2` — refs origen: `<PLAN-174>:F-1` y `<PLAN-174>:F-2`; alcance de revalidación: `docs/CONVENTIONS.md` (bullet de clases, ciclo de ADR, `C-3`, intake, Change Levels, impacto de cierre), `docs/VERSIONING.md:4. Flujo por plan (playbook)` y `:7. Estados de planes y RFCs`, `AGENTS.md` (`Do NOT` y `Task lifecycle`), `.agents/AGENTS.md` (frontera DEV/Protocol y reglas 1–2) y `.agents/workflows/change-lifecycle.md` (§1, §2, §3 y §11); evidencia: los `git diff` de esas rutas y la batería canónica; carácter: FACTUAL / TRACEABILITY; autorización: instrucción directa del mantenedor (2026-10-23) + este Plan; qué se corrigió: se reemplazan las formulaciones que derivaban la ruta del mero contacto con el payload por la clasificación del payload delta y la ruta efectiva, y se declara `RFC-56 N/A` para un Change sin efecto payload.

- `<PLAN-174>:C-3` — refs origen: `<PLAN-174>:F-3` y `<PLAN-174>:F-6`; alcance de revalidación: `docs/plans/_TEMPLATE.md` (header y comentario del campo), `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)` y la suite anclada `tests/test_autonomy_effects_dogfood.py` (que lee el template real); evidencia: `python -m pytest tests/test_autonomy_effects_dogfood.py -q` → verde (exit 0) y `python tools/check_plan_structure.py` → sin violaciones; carácter: FACTUAL / TRACEABILITY; autorización: instrucción directa del mantenedor (2026-10-23) + este Plan; qué se corrigió: el campo canónico pasa a `**RFC-56 Class:** N/A | A | B | C` con composición `A, B`, separado de `**Change Level:**`, y la representación ya no admite leer `A | B` como clase combinada ni obliga a clasificar un cambio DEV-only.

- `<PLAN-174>:C-4` — refs origen: `<PLAN-174>:F-4`; alcance de revalidación: `docs/CONVENTIONS.md` (fila `C-3`, intake, determinaciones de impacto) y `.agents/policies/validation-closure.md` (§5.1 y §5.2); evidencia: `git diff` de ambas rutas y la batería canónica; carácter: FACTUAL / TRACEABILITY; autorización: instrucción directa del mantenedor (2026-10-23) + este Plan; qué se corrigió: se elimina «todo payload touch → Plan + RFC-56» y la equivalencia «sin Plan = Clase C», sustituyéndolas por la clasificación por delta y por la ruta directa de C condicionada al Change Level.

- `<PLAN-174>:C-5` — refs origen: `<PLAN-174>:F-5`; alcance de revalidación: `docs/placement-contract.md` (`PC-3`) y la resolución de citas; evidencia: `python tools/check_plan_citations.py` → «All citations resolve»; carácter: FACTUAL / TRACEABILITY; autorización: instrucción directa del mantenedor (2026-10-23) + este Plan; qué se corrigió: la cita de autoridad del dominio Protocol apunta a `## Modelo vigente (enmienda 2026-10-23)` en lugar de a la sección superada.

### Pending decisions

N/A — no hay pending decisions; todas las ambigüedades se resolvieron por normativa vigente + TE y no queda una decisión que requiera autoridad no disponible.

## Nota de ejecución

**Ejecutado el 2026-10-23.** Change DEV con **RFC-56 Class: N/A** (sin payload delta), conducido en `dev` bajo la instrucción directa del mantenedor.

```text
PLAN_ID                   = 174
AUTHORIZATION             = MAINTAINER_AUTHORIZED_FOR_EXECUTION (Priority 3)
AUTHORITY_CLASS           = DEV_PLAN (RFC-56 Class: N/A)
EXECUTION_AUTHORIZED      = YES
RFC_REQUIRED              = NO
PROTOCOL_AUTHORITY        = UNCHANGED (0 diff en protocol/, dist/, VERSION)
EXECUTION_BASELINE_HEAD   = 66d132b
IMPLEMENTATION_COMMIT     = 03d4001 (tree cc1d81f703fb250d9ae83a08388fe1c15feffb91)
SCOPE_PATHS               = 11
CONCEPTUAL_DECISIONS_REMAINING = NONE
```

### TE post-materialización

TE re-ejecutada sobre el texto materializado, no sobre el diseño. Para cada caso: `input → classification → authority route → artifact required → execution permission → validation expectation`. La regla citada es la que un agente encuentra hoy en el repositorio, no la que este Plan quiso escribir.

| # | Caso | Regla materializada (dónde) | Ruta única | Resultado |
|---|---|---|---|---|
| T1 | Change C-only | RFC-56, modelo vigente §2 (C) y §4 (fila C); CONVENTIONS, bullet C | Direct, si el Level no exige Plan | una sola ruta; sin Plan/RFC |
| T2 | Change B-only | RFC-56 §2 (B) y §4 (fila B) | Plan con justificación + batería | una sola ruta; sin RFC |
| T3 | Change A-only | RFC-56 §2 (A) y §4 (fila A) | RFC `Accepted` + Plan | una sola ruta |
| T4 | Change A+B | RFC-56 §4 (fila A+B; sin clase `AB`) | RFC `Accepted` + Plan | una sola ruta |
| T5 | Change B+C | RFC-56 §4 (fila B+C) | Plan (el delta C viaja en el mismo Plan) | una sola ruta |
| T6 | Change A+C | RFC-56 §4 (fila A+C) | RFC `Accepted` + Plan | una sola ruta |
| T7 | Change A+B+C | RFC-56 §4 (fila A+B+C) | RFC `Accepted` + Plan | una sola ruta |
| T8 | Change sin payload effect | RFC-56 §5 (`RFC-56 N/A`); CONVENTIONS, bullet N/A | lifecycle DEV + Change Level; sin A/B/C | una sola ruta |
| T9 | payload + tooling | RFC-56 §1 (la clase es del delta) y §4 | la del payload delta; el tooling DEV no tiene clase | una sola ruta |
| T10 | C + L3 | RFC-56 §5 (ruta directa aplicable solo si el Level no exige Plan) + matriz L0–L3 | Plan de clase C, sin RFC | una sola ruta; el Level agrega maquinaria, no rebaja la clase |
| T11 | A + L0 | RFC-56 §5 (ortogonalidad; el Level se computa de sus cinco dimensiones) | RFC `Accepted` + Plan; el Level solo es L0 si sus dimensiones lo permiten | una sola ruta de autorización |
| T12 | documentación de payload con cambio semántico | RFC-56 §2 (A) y §3 (no es C si cambia interpretación o contrato) | RFC `Accepted` + Plan | una sola ruta |
| T13 | documentación de payload sin cambio semántico | RFC-56 §2 (B) y §3 (C solo si es mecánico) | Plan, o Direct si es C y aplica | una sola ruta |
| T14 | checker sin cambio, semántica modificada | RFC-56 §3 (el checker es evidencia, no autoridad) | A o B según la semántica; nunca C por el checker | una sola ruta |
| T15 | checker cambiado, semántica preservada | RFC-56 §3 (C posible si se demuestra preservación) | C/Direct si aplica; si no, Plan | una sola ruta |

**Casos irresueltos: 0. Escalamientos: 0.** La TE pre-materialización (sección `## Theoretical execution (pre-materialización)`) y la post-materialización coinciden en la ruta de cada escenario. Las dos precisiones que la materialización hizo explícitas son: (a) T10/T11 — el Level agrega maquinaria y nunca rebaja el mínimo de la clase, y la clase no se computa desde el Level; (b) T14/T15 — el resultado de un checker no determina la clase en ninguna dirección.

### Resultados

| Comando | Resultado |
|---|---|
| `check_protocol_invariants` | PASS — 217 archivos, 10.541 referencias |
| `check_plan_citations` | PASS — todas las citas resuelven |
| `check_plan_structure` | PASS — 0 violaciones; 2 `GAP` declarados (157/158) |
| `check_taxonomy_coherence` | PASS |
| `check_session_artifacts` | PASS |
| `check_version_state` | PASS; 9 warnings históricos |
| `check_invariants_equivalence` | PASS — `IDENTICAL: YES`; `ENFORCED=7/15` |
| `check_enforcement_declarations` | PASS — ENF-001…ENF-003 |
| C-1 | `VALID=80 GAP=0 ANOMALY=0` sobre el estado de cierre |
| C-2 | `VALID=79 GAP=1` (Plan 116) `ANOMALY=0` |
| C-3 | `VALID=38 GAP=4` (155/158/168/169) `ANOMALY=0` |
| `pytest tests/` | **1435 passed** |
| `git diff --check` | limpio |
| Recomputación de identidad | PASS — `DECLARED_DELTA == recomputado(S1) == recomputado(S0)`; `ANCHOR_STATE == CHECKPOINT_STATE == tree(03d4001)` |

**Archivos del Change:** las once rutas del `## Validation anchor` más este Plan. `VERSION`, `PROTOCOL_VERSION`, `protocol/`, `runtime/`, `tools/`, `tests/` y `dist` sin cambios. **`Released = NO`** (docs-only, RFC-69).

### ADR y Pending decisions

**ADR: NO.** El criterio de ADR-worthiness (`.agents/policies/authority.md:ADR-worthiness (when a decision must leave the RFC/Plan)`) no se cumple: la decisión (a) no se consume fuera de RFC-56 —todas las referencias enrutan a RFC-56—, (b) no supersede ni modifica ningún ADR, y (c) no es un invariante arquitectónico persistente independiente de RFC-56; si RFC-56 fuera superseded, el modelo se movería con ella. Elevarla a ADR duplicaría la autoridad sin cambiar ningún gate.

**Pending decisions: ninguna.** Las seis observaciones de la auditoría se dispusieron con normativa vigente + TE (cinco corregidas y una diferida a traza histórica con owner y destino); no queda una decisión que requiera autoridad no disponible.
