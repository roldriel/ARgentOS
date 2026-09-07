# Plan 101 — Capa operacional `.agents/` de ARgentOS DEV (materialización del workflow operativo del Change Lifecycle)

> **Naturaleza de este documento.** Este es un Implementation Plan **posterior
> al cierre de la serie A–D** del Change Lifecycle DEV (planes 94–100,
> RFC-75). No es una unidad del roadmap A–D y no inventa un "Incremento 5":
> materializa una capacidad operacional nueva del repo fuente, la **capa
> `.agents/` DEV** como interfaz operacional permanente que un agente LLM lee
> para ejecutar el Change Lifecycle, reutilizando los mecanismos existentes
> (RFC-75, ADR-15/16, C1/C2/C3, templates y convenciones) **sin crear**
> autoridad normativa nueva, sin copiar el dominio Protocol y sin duplicar
> governance.
>
> **La presente iteración es solo de creación/registro del plan**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; **no materializa**
> `.agents/`, no copia `sessions/agents-dev-layer/agents/` a la raíz, no
> modifica `AGENTS.md`, `docs/AGENTS.md` ni `docs/CONVENTIONS.md`, no modifica
> `protocol/`, `runtime/`, `tools/` ni `tests/`, no ejecuta commits y no
> modifica RFC-75, ADR-15, ADR-16 ni los Planes 94–100. Estado esperado al
> cierre de esta iteración:
>
> ```text
> Plan 101 = Aprobado para ejecución (PLANNED / OPEN)
> Materialización .agents/ = NOT STARTED
> Planned = YES
> Executed = NO
> Committed = NO (sin commit en esta iteración; registro en el working tree)
> Verified = NO
> Closed = NO (condición derivada)
> Released = NO
> ```

**Status:** Executed (2026-09-03; capa `.agents/` DEV materializada e integrada
en la raíz del repo fuente; condición derivada `Closed` docs-only registrada en
`## Checkpoint / cierre`)
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio DEV-only del repo fuente,
principalmente documental/instruccional; sin `VERSION` bump ni tag; RFC-56 no
aplica; RFC-69)
**Change Level:** L2 (clasificación prospectiva declarada al crear el plan;
ver §11)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/75-change-lifecycle.md`); ADR-15
`Accepted` (`docs/adr/15-change-lifecycle-continuity.md`); ADR-16 `Accepted`
(`docs/adr/16-change-lifecycle-authority.md`); RFC-46 `Accepted`; RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed`; Plan 95 `Executed`; Plan 96
`Executed` + condición derivada `Closed` (docs-only); Plan 97 `Executed` +
condición derivada `Closed` (docs-only); Plan 98 `Executed` + condición
derivada `Closed` (docs-only); Plan 99 `Executed` + condición derivada
`Closed` (docs-only, corrección post-close de F-1); Plan 100 `Executed` +
condición derivada `Closed` (docs-only); Decisión B (`fc52c88`, semántica
A1/A2/closure PASS); estado factual del repositorio al 2026-09-02 (HEAD
`d93d234`, branch `dev`, working tree limpio, pytest `428 passed`, C1/C2/C3
`GAP=0, ANOMALY=0`; §3).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): crear y registrar
el Plan 101 formal para autorizar **posteriormente** la materialización de la
capa operacional `.agents/` de ARgentOS DEV en la raíz del repositorio, **sin
implementarla en esta iteración**. Fuente de diseño: staging temporal
`sessions/agents-dev-layer/` (ver §6), deliberadamente separado de la
ubicación canónica final.

---

## Convención de evidencia

Este documento distingue, en cada conclusión importante, las marcas usadas por
los planes de la serie y compatibles con la convención del repositorio
(`docs/CONVENTIONS.md:Convenciones`):

| Marca | Significado |
|---|---|
| `OBSERVED` | Verificado en el repositorio (git, archivos, checkers, pytest). |
| `NORMATIVE` | Impuesto por RFC `Accepted`, ADR `Accepted`, plan aprobado o convención vigente. |
| `DERIVED` | Deducción necesaria a partir de evidencia citada. |
| `PROPOSED` | Especificación de la ejecución futura de este plan; no es normativa hasta ejecutarse. |
| `OPEN` | Decisión pendiente que no impide crear/registrar el plan; requiere decisión humana posterior. |
| `BLOCKER` | Contradicción que impide redactar o ejecutar (no se detectó ninguna; ver §30). |

Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). El staging
`sessions/agents-dev-layer/` es **provenance de diseño de sesión, no un
artifact versionado ni fuente normativa** (ADR-16 AU-4): se cita por ruta como
insumo, no como autoridad.

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Header / metadata e identidad | Header de este archivo |
| Naturaleza / esta iteración no materializa | Banner de apertura |
| Resumen ejecutivo | §1 |
| Contexto histórico | §2 |
| Baseline factual del repositorio | §3 |
| Declaración del problema | §4 |
| Objetivo | §5 |
| Fuente de diseño (staging) | §6 |
| Ubicación canónica y transición staging → `.agents/` | §7 |
| Base normativa | §8 |
| Alcance exacto | §9 |
| Fuera de alcance | §10 |
| Clasificación del cambio | §11 |
| Contenido de la capa `.agents/` (spec futura) | §12 |
| Integración mínima (root AGENTS, docs/AGENTS, CONVENTIONS) | §13 |
| Frontera DEV/Protocol | §14 |
| Modelo de autoridad | §15 |
| Semántica de validación/cierre (A1/A2/GC-1) | §16 |
| Integración de checkers C1/C2/C3 | §17 |
| Criterios de aceptación | §18 |
| Gates de ejecución | §19 |
| Dogfooding | §20 |
| Estrategia de commits | §21 |
| Recovery / Stop Conditions | §22 |
| Estrategia de validación | §23 |
| Estrategia de anchor | §24 |
| Estrategia de checkpoint | §25 |
| Restricciones de governance | §26 |
| Change Lifecycle del propio Plan 101 | §27 |
| Riesgos | §28 |
| Dependencias | §29 |
| Pending / Open Questions | §30 |
| Veredicto final | §31 |
| Traceability Matrix | §32 |

---

## 1. Resumen ejecutivo

**[DERIVED + NORMATIVE]** El Change Lifecycle de ARgentOS DEV está definido
(RFC-75 `Accepted`), sus mecanismos están materializados (anchors/checkpoint
por planes 96–100; C1/C2/C3 operativos) y su gobernanza vive en el `AGENTS.md`
raíz, `docs/CONVENTIONS.md`, `docs/VERSIONING.md` y `docs/AGENTS.md`
(`docs/plans/94-change-lifecycle-master-action-plan.md:2.2 Estado del repositorio`).
Sin embargo, el repo fuente **no tiene** una capa `.agents/` propia: no existe
una interfaz operacional permanente que un agente LLM lea para descubrir y
ejecutar el workflow sin que un humano le explique el procedimiento.

**[PROPOSED]** Este Plan 101 autorizará, en una ejecución futura separada, la
materialización de esa interfaz en la **ubicación canónica** `/.agents/` de la
raíz del repositorio, con cinco archivos (entry point + workflow + tres
policies), una integración mínima de descubrimiento/taxonomía/frontera en
`AGENTS.md`, `docs/AGENTS.md` y `docs/CONVENTIONS.md`, y la eliminación del
staging temporal para evitar dos fuentes operacionales.

**[OBSERVED]** Esta iteración **solo crea y registra el Plan 101**. No ejecuta
la materialización; el Plan queda `Aprobado para ejecución` con condición
`Planned: YES` (vocabulario del repo: `docs/CONVENTIONS.md:Convenciones`); la
autorización de ejecución y de commits es humana y queda abierta (§30).

## 2. Historical Context

**[OBSERVED]** El Master Action Plan 94 declaró que el repo fuente no tenía
`.agents/` propio y que la gobernanza DEV vivía en el `AGENTS.md` raíz,
`docs/CONVENTIONS.md`, `docs/VERSIONING.md` y `docs/AGENTS.md`
(`docs/plans/94-change-lifecycle-master-action-plan.md:2.2 Estado del repositorio`).
Las unidades A–D (planes 95–100) materializaron semántica, anchors,
checkpoints, findings/correcciones y los checkers C1/C2/C3, sin crear la capa
operacional del agente.

**[OBSERVED]** Entre el cierre del Plan 100 (HEAD `d93d234`, 2026-09-02) y la
creación de este Plan se estudió el diseño de la capa `.agents/` DEV y se
staged su contenido completo bajo `sessions/agents-dev-layer/` (directorio
gitignored por `/sessions/*` en `.gitignore`; ver §6). Ese diseño no se
reinventa: este Plan lo formaliza como alcance de ejecución futura.

## 3. Current Repository Baseline

**[OBSERVED]** Verificado con git y checkers al 2026-09-02:

| Dato | Valor observado |
|---|---|
| Branch | `dev` (sync con `origin/dev`) |
| HEAD | `d93d2340b74faf4c3ae9c27b39f3db3180f54177` |
| Working tree | limpio (sin cambios versionados) |
| pytest | `428 passed, 0 failed` (basetemp local `.pytest_cache/basetemp` por ACL del sandbox) |
| Checkers documentales | PASS (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`) |
| C1/C2/C3 | `GAP=0, ANOMALY=0` sobre `docs/plans/` |
| Planes 96–100 | `Executed` + condición derivada `Closed` (docs-only, sin release) |
| RFC-75 / ADR-15 / ADR-16 | `Accepted` |
| `protocol/.agents/` | intacto (dominio Protocol; no es regla DEV) |
| `.agents/` en la raíz | **no existe** |
| Staging | `sessions/agents-dev-layer/` presente (gitignored; no versionado) |

## 4. Problem Statement

**[OBSERVED + DERIVED]** El lifecycle DEV está verificado por maquinaria (C1/
C2/C3) y documentado en `docs/`, pero el agente que entra al repo no tiene una
**interfaz operacional** que responda: ¿soy un Change? ¿qué leo primero? ¿qué
hago antes de modificar? ¿cuándo planifico, ejecuto, valido, corrijo,
revalido, checkpointo y cierro? El conocimiento está disperso en fuentes
normativas e históricas; sin la capa operacional, el agente depende del humano
para reconstruir el procedimiento (problema de "bus humano" documentado por
RFC-75) o lee contexto innecesario.

## 5. Objective

**[PROPOSED]** En la ejecución futura autorizada por este Plan, crear en la
raíz del repositorio la capa operacional permanente `.agents/` de ARgentOS
DEV:

```text
.agents/
├── AGENTS.md
├── workflows/
│   └── change-lifecycle.md
└── policies/
    ├── authority.md
    ├── validation-closure.md
    └── lifecycle-checkers.md
```

La capa convierte contratos y decisiones existentes en instrucción operacional
consumible por un LLM. **No crea autoridad normativa nueva**, no es una fuente
superior de verdad, no copia governance y no es una copia del Producto.

## 6. Fuente de diseño (staging)

**[OBSERVED]** El diseño ya estudiado vive como staging temporal bajo:

```text
sessions/agents-dev-layer/
├── PLAN-101-draft.md
├── README.md
└── agents/
    ├── AGENTS.md
    ├── workflows/change-lifecycle.md
    └── policies/
        ├── authority.md
        ├── validation-closure.md
        └── lifecycle-checkers.md
```

`sessions/` es staging gitignored (`.gitignore`), nunca versionado, nunca
operacional. El contenido de `sessions/agents-dev-layer/agents/` es la fuente
de diseño para la ejecución futura; **no es la ubicación final** y no debe
quedar como interfaz permanente mantenida manualmente en paralelo con
`/.agents/`.

## 7. Ubicación canónica y transición staging → `.agents/`

**[PROPOSED]** La ubicación canónica y permanente de la capa operacional DEV
es `/.agents/` en la raíz del repositorio. La transición autorizada por este
Plan es:

```text
sessions/agents-dev-layer/agents/
                ↓
    materialización autorizada (ejecución del Plan 101)
                ↓
            .agents/  (raíz; canónico y permanente)
```

La ejecución futura deberá:

1. Materializar los cinco archivos en `.agents/` a partir del staging (contenido
   ya diseñado; sin rediseñarlo salvo corrección factual documentada).
2. Verificar que no existe divergencia no resuelta entre staging y lo
   materializado (AC-101-09).
3. **Eliminar el staging** `sessions/agents-dev-layer/` **después** de una
   materialización verificada y anclada con éxito, como parte de la ejecución
   del Plan (mecanismo: `git` no lo versiona; es staging efímero conforme a
   `docs/AGENTS.md`). No se inventa una política de archivado: el staging no es
   un artifact documental y nunca debe convertirse en copia operacional.

## 8. Base normativa

**[NORMATIVE]** Fuentes que la ejecución futura reutiliza (sin redefinirlas ni
duplicarlas):

- RFC-75 — Change Lifecycle DEV (modelo, mecanismos 1–15, rollout)
  (`docs/rfc/75-change-lifecycle.md`).
- ADR-15 — Continuity & Git Checkpoint Semantics (CL-1..CL-10)
  (`docs/adr/15-change-lifecycle-continuity.md:Invariantes`).
- ADR-16 — Authority & Decision Model (AU-1..AU-7)
  (`docs/adr/16-change-lifecycle-authority.md:Decisión`).
- RFC-56 — clases de autorización de payload; RFC-69 — versionado docs-only;
  RFC-46 — trazas inmutables.
- Reglas operacionales de los Incrementos 1+3 y 2 en
  `docs/CONVENTIONS.md:Convenciones` (anchor v1, checkpoint GC-1, refs
  calificadas LC-1, pending PC-1).
- Template de Plan (`docs/plans/_TEMPLATE.md`) y batería canónica
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- Checkers C1/C2/C3 (`tools/`) como evidencia factual determinista.

## 9. Alcance exacto

### 9.1 Esta iteración de planificación (incluido ahora)

1. Crear este artifact: `docs/plans/101-change-lifecycle-agents-operational-layer.md`.
2. Registrarlo en `docs/plans/INDEX.md` (Trigésima tercera serie).
3. Verificación documental de creación (estructura, citas, C1/C2/C3 neutros).
4. Sin commits (decisión del mantenedor; práctica del repo, precedente planes
   99/100 en su fase de creación).

### 9.2 Ejecución futura del plan (incluido entonces; NO se ejecuta ahora)

1. **Creación** en la raíz:
   - `.agents/AGENTS.md`
   - `.agents/workflows/change-lifecycle.md`
   - `.agents/policies/authority.md`
   - `.agents/policies/validation-closure.md`
   - `.agents/policies/lifecycle-checkers.md`
2. **Integración mínima**:
   - `AGENTS.md` raíz: hacer descubrible `.agents/` y establecer
     `.agents/AGENTS.md` como entry point operacional DEV (puntero corto, sin
     duplicar contenido).
   - `docs/AGENTS.md`: registrar la taxonomía de la capa (`.agents/` =
     operación DEV; `docs/` = autoridad/historia/documentación; `tools/` =
     verificación determinista) sin convertirla en un segundo workflow.
   - `docs/CONVENTIONS.md`: formalizar la frontera documental
     Product/Protocol vs DEV y el rol de `.agents/` como interfaz operacional
     DEV, sin modificar convenciones no relacionadas.
3. **Eliminación del staging** tras materialización exitosa (§7).
4. Registro de cierre: anchor propio, checkpoint, espejo del INDEX, ítem en
   `CHANGELOG.md:[Unreleased]` `(plan 101)`.

### 9.3 Excluido incluso en la ejecución futura

- `protocol/`, `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/`.
- Nuevos checkers (C4/C5/…); modificación de C1/C2/C3 **salvo** necesidad
  factual estrictamente imprescindible descubierta en la ejecución y autorizada
  por el propio alcance (no se asume ahora).
- F-3 y F-2/F-4…F-9; nuevos RFCs/ADRs; modificación de RFC-75/ADR-15/ADR-16;
  Planes 94–100.
- State machines nuevas, registry global, tracker global, base de datos,
  orchestrator runtime, integración LLM runtime, CI/CD, `VERSION` bump,
  release, tag, push.

## 10. Out of Scope

Excluido explícitamente (lista exhaustiva del encargo y del diseño): todo lo
de §9.3, más: no se crea una segunda fuente de verdad para estado; no se
introduce estado mutable en `.agents/` (`.agents/state.json`, registries);
no se copian workflows/policies/state machines/skills/mecanismos de
`protocol/.agents/` a `.agents/`; no se audita de nuevo el Change Lifecycle; no
se hace roadmap assessment; no se crea el Plan 102.

## 11. Clasificación del cambio

### 11.1 Clase RFC-56

**[NORMATIVE + DERIVED]** El cambio no toca `protocol/.agents/` ni el layout
del payload fuente: la clase RFC-56 no aplica (`docs/rfc/56-governance-fast-track.md`).
Es un cambio DEV-only, principalmente documental/instruccional, docs-only sin
versión de protocolo (RFC-69; `docs/VERSIONING.md:3. Versionado`), cuya vía de
autorización es un Plan `Aprobado para ejecución` con justificación
documentada (práctica de los Planes 95–100).

### 11.2 Change Level

**[DERIVED]** `Level = max(coordination, scope, architectural impact, release
impact, duration/complexity)` (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`):

| Dimensión | Valor | Justificación |
|---|---|---|
| coordination | 1 | 1 agente, 1 sesión por etapa |
| scope | 2 | multi-área: `AGENTS.md` raíz + `docs/AGENTS.md` + `docs/CONVENTIONS.md` + árbol `.agents/` nuevo |
| architectural impact | 2 | nueva capa/seam operacional del agente DEV (aditiva, reversible, sin cambio de contratos) |
| release impact | 0 | sin versión de protocolo; docs-only |
| duration/complexity | 1 | 1 sesión por etapa |

**Change Level: L2** (clasificación prospectiva; no es status y no autoriza
payload — RFC-56).

## 12. Contenido de la capa `.agents/` (spec de ejecución futura)

**[PROPOSED]** La ejecución futura materializa los cinco archivos con el
contenido ya diseñado en `sessions/agents-dev-layer/agents/` (referencia
informacional; no se re-escribe el diseño salvo corrección factual
documentada). Requisitos invariantes por archivo:

### 12.1 `.agents/AGENTS.md` — entry point operacional DEV

Debe permitir que un agente, con lectura mínima: sepa que opera sobre
ARgentOS DEV; descubra el workflow; conozca las reglas fundamentales de
autoridad; conozca las stop conditions; sepa cuándo leer cada policy/workflow;
entienda que `docs/` contiene autoridad e historia; entienda que `tools/`
contiene mecanismos deterministas; y entienda la frontera con
`protocol/.agents/` (data, no reglas). **No** debe ser un índice gigante ni
duplicar governance.

### 12.2 `.agents/workflows/change-lifecycle.md` — workflow operativo

Debe materializar, como mínimo: intake → estado Git → detección del cambio →
clasificación → autorización → Plan → ejecución → evidencia → validación →
findings/corrections/revalidation → checkpoint → `Closed` → post-close.
Reutiliza RFC-75/ADR-15/16 **sin** crear state machine global, registry
global de Changes, base de datos ni tracker global.

### 12.3 `.agents/policies/authority.md`

Debe operar con las clases FACTUAL / NORMATIVE / DECISION / RELEASE /
DESCRIPTIVE y el patrón `detect → classify → escalate → human decision →
correct artifact → revalidate`. Prohibiciones explícitas: convertir inferencia
propia en decisión humana; usar INDEX como autoridad normativa; resolver
conflictos normativos por inferencia; modificar silenciosamente una decisión
humana.

### 12.4 `.agents/policies/validation-closure.md`

Debe operar sobre A1, A2, revalidation, validation anchor, closure state,
checkpoint, `Executed`, `Committed`, `Verified`, `Closed`, `Released`, GAP,
ANOMALY y stop conditions; preservar `Committed != Closed` y
`Closed != Released`; y preservar la semántica GC-1 **corregida por F-1 en
C-2**: `closure state → validation whose validated state corresponds to
closure → corresponding anchor`. Prohibido: `latest A2 wins`, generic tree
membership, selección arbitraria de un anchor. A1 inmutable; A2 nueva
validación con lineage hacia A1; A2 no reemplaza A1.

### 12.5 `.agents/policies/lifecycle-checkers.md`

Debe integrar operacionalmente C1 (`tools/check_lifecycle_anchor.py`), C2
(`tools/check_lifecycle_checkpoint.py`) y C3
(`tools/check_lifecycle_lineage.py`): cuándo ejecutarlos; qué input usan;
significado de `VALID`, `GAP`, `ANOMALY`; acción del agente; carácter
determinista; carácter no normativo. **No** copia algoritmos; no crea checkers
nuevos; no modifica C1/C2/C3.

## 13. Integración mínima (spec de ejecución futura)

**[PROPOSED]** La integración se limita a descubribilidad, entry point,
taxonomía y frontera:

1. **`AGENTS.md` raíz:** una adición mínima que establezca la ruta
   `AGENTS.md → .agents/AGENTS.md → workflow/policies según necesidad`, sin
   duplicar el contenido del entry point operacional.
2. **`docs/AGENTS.md`:** ajuste taxonómico mínimo que distinga `.agents/`
   (operación DEV), `docs/` (autoridad/historia/documentación) y `tools/`
   (verificación determinista), coherente con el mapa Folder → class y las
   reglas de referencia existentes; no se convierte en un segundo workflow.
3. **`docs/CONVENTIONS.md`:** actualización acotada para formalizar la
   frontera documental Product vs DEV y establecer `.agents/` como interfaz
   operacional DEV, preservando que `docs/` sigue siendo autoridad/historia y
   que `.agents/` no es fuente normativa superior.

## 14. Frontera DEV/Protocol

**[NORMATIVE]** Prohibiciones expresas (vigentes ya y reforzadas por la capa):

- `protocol/`, `protocol/.agents/` y `dist/` no se modifican en ninguna etapa.
- `.agents/` DEV es exclusivamente DEV; no copia workflows, policies, state
  machines, skills ni mecanismos de `protocol/.agents/`.
- `protocol/.agents/` sigue perteneciendo a otro dominio (Product); su
  contenido es data para DEV, no reglas (`docs/source-layout.md`).
- No hay herencia automática ni mecanismos compartidos DEV/Protocol
  (`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`).

## 15. Modelo de autoridad (spec)

**[NORMATIVE + PROPOSED]** La policy `authority.md` de la capa materializa el
modelo de ADR-16: cinco clases de autoridad sin jerarquía total y el protocolo
de conflicto detect → classify → escalate → human decision → correct artifact
→ revalidate (`docs/adr/16-change-lifecycle-authority.md:Decisión`). Los
checkers son evidencia factual; `anchor missing` = GAP, no invalidación
(RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

## 16. Semántica de validación/cierre (spec)

**[NORMATIVE + PROPOSED]** La policy `validation-closure.md` preserva:

- `Verified = ∃ validation(PASS, anchor)`; `Executed = implementación +
  validación` (legal sin commit); `Committed` = estado del repo, no status de
  Plan; `Closed` = condición derivada; `Released` = tag inmutable en `master`
  (ADR-15 `docs/adr/15-change-lifecycle-continuity.md:Invariantes`;
  `docs/VERSIONING.md:7. Estados de planes y RFCs`).
- A1 inmutable; A2 = revalidación del mismo contrato sobre estado nuevo con
  anchor propio y ref a A1; A2 no reemplaza A1
  (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`).
- GC-1 con selección del anchor por **correspondencia del estado validado con
  el estado de cierre** (semántica corregida por F-1 en C-2, Plan 99): nunca
  recencia (`latest A2 wins`), nunca generic tree membership, nunca selección
  arbitraria (`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).

## 17. Integración de checkers C1/C2/C3 (spec)

**[PROPOSED]** La policy `lifecycle-checkers.md` define, sin copiar código:

| Checker | Cuándo | Input | VALID | GAP | ANOMALY | Acción del agente |
|---|---|---|---|---|---|---|
| C-1 `check_lifecycle_anchor.py` | tras registrar una validación/anchor | `--root` opcional (default: raíz) | anchor presente y consistente | campo faltante / no verificable (advisory) | contradicción | VALID → citar como evidencia; GAP → completar o registrar; ANOMALY → STOP + finding/corrección |
| C-2 `check_lifecycle_checkpoint.py` | antes de derivar `Closed` | `--root` opcional; git read-only local | checkpoint consistente con el anchor aplicable (GC-1, correspondencia de estado) | evidencia insuficiente | contradicción (mismatch de tree identity, A2 sin lineage A1, FAIL con Closed) | VALID → derivar `Closed`; GAP → completar; ANOMALY → no cerrar, corregir y revalidar |
| C-3 `check_lifecycle_lineage.py` | cuando existen registros F/C, antes del cierre | `--root` opcional | registros completos y consistentes (LC-1) | información faltante/ambigua (incluye `reopened`, duplicados) | contradicción verificable | VALID → seguir al checkpoint; GAP → completar o escalar (sin tie-break inventado); ANOMALY → STOP |

Exit codes: `0` salvo ≥1 ANOMALY (`1`); C-3 usa `2` solo ante errores de
lectura irrecuperables. Todos: deterministas, read-only (C-2 con git local
read-only), advisory, sin autoridad normativa.

## 18. Acceptance Criteria

Checklist verificable PASS/FAIL. Esta iteración de creación satisface
AC-101-18 (registro) y deja el resto para la ejecución futura:

- [ ] **AC-101-01** — `.agents/` existe en la raíz con los cinco archivos de §12.
- [ ] **AC-101-02** — `.agents/AGENTS.md` es el entry point operacional DEV (§12.1).
- [ ] **AC-101-03** — El `AGENTS.md` raíz apunta a `.agents/AGENTS.md` (§13).
- [ ] **AC-101-04** — El workflow existe bajo `.agents/workflows/` (§12.2).
- [ ] **AC-101-05** — Las policies existen bajo `.agents/policies/` (§12.3–§12.5).
- [ ] **AC-101-06** — La capa reutiliza RFC-75/ADR-15/ADR-16 sin redefinirlos (§8/§12).
- [ ] **AC-101-07** — La capa no crea autoridad normativa nueva (§15).
- [ ] **AC-101-08** — El `.agents/` DEV permanece separado de `protocol/.agents/` (§14).
- [ ] **AC-101-09** — No existe duplicación operacional permanente entre `.agents/` y `sessions/` (§7).
- [ ] **AC-101-10** — `docs/` continúa siendo autoridad/historia documental (§13).
- [ ] **AC-101-11** — `tools/` continúa siendo la fuente de mecanismos deterministas (§17).
- [ ] **AC-101-12** — C1/C2/C3 son gates, no autoridad (§17).
- [ ] **AC-101-13** — Existen stop conditions claras (§22).
- [ ] **AC-101-14** — El entry point permite comenzar una operación sin cargar todo `docs/` (§12.1).
- [ ] **AC-101-15** — La materialización puede validarse, anclarse, checkpointarse y cerrarse mediante el lifecycle existente (§23–§25).
- [ ] **AC-101-16** — `.agents/` no introduce registry, estado mutable, database ni segunda fuente de verdad (§10).
- [ ] **AC-101-17** — La integración no modifica convenciones no relacionadas (§13).
- [ ] **AC-101-18** — El Plan 101 existe en `docs/plans/101-change-lifecycle-agents-operational-layer.md` y está registrado en `docs/plans/INDEX.md` (Trigésima tercera serie; Status `Aprobado para ejecución`; `Planned: YES; Executed: NO; Committed: NO; Verified: NO; Closed: NO; Released: NO`; sin placeholders).

## 19. Execution Gates

**[PROPOSED — Future Implementation]** La ejecución futura no omite ningún
gate:

| Gate | Entrada | Acciones | Evidencia | PASS | STOP |
|---|---|---|---|---|---|
| G0 Baseline | Branch `dev`; HEAD conocido; árbol limpio salvo cambios del plan | Capturar estado §3; batería/pytest baseline | `git status`, pytest, checkers | Estado sostenido o desviación aceptada (plan 94 §24.1) | Estado distinto sin autorización |
| G1 Materialización | G0 PASS | Crear los cinco archivos `.agents/` desde el staging (§12) | Diff limitado al árbol `.agents/` | Archivos presentes con contenido del diseño | Scope leakage; rediseño sin necesidad |
| G2 Discovery | G1 PASS | Aplicar puntero `AGENTS.md` raíz → `.agents/AGENTS.md` | Diff de `AGENTS.md` | Ruta de descubrimiento verificable | Entry point ausente o duplicación del contenido |
| G3 Boundary | G2 PASS | Verificar independencia respecto de `protocol/.agents/` | Inspección del árbol + git diff | Sin referencias ni copias al dominio Protocol | Contaminación DEV/Protocol |
| G4 Documentation coherence | G3 PASS | Ajustes mínimos en `docs/AGENTS.md` y `docs/CONVENTIONS.md` (§13) | Checkers documentales; diff acotado | Taxonomía y frontera coherentes; sin cambios no relacionados | Incoherencia o scope creep |
| G5 Existing validation | G4 PASS | Batería canónica + C1/C2/C3 sobre el corpus | Salida de checkers + pytest | Batería verde o desviación aceptada; GAP/ANOMALY según corresponda | Fallo sin desviación aceptada |
| G6 Dogfood | G5 PASS | Ejecutar el caso operacional de §20 | Traza del caso | El agente navega AGENTS.md → `.agents/AGENTS.md` → workflow sin leer todo `docs/` | Descubrimiento roto o instrucción ambigua |
| G7 Anchor / checkpoint / closure | G6 PASS | Registrar Validation Anchor y Checkpoint propios; eliminar staging; espejo INDEX; ítem changelog | Anchor V1; checkpoint con consistencia GC-1 | Condición derivada `Closed` (docs-only) | Inconsistencia checkpoint↔anchor o AC FAIL |

## 20. Dogfooding

**[PROPOSED]** Caso operacional de la ejecución futura (y verificable después
de la materialización por cualquier agente):

```text
usuario solicita cambio
    ↓
AGENTS.md (raíz; siempre cargado)
    ↓
.agents/AGENTS.md (entry point; siempre cargado para operar)
    ↓
workflows/change-lifecycle.md (intake → clasificación → autorización)
    ↓
policies/authority.md (si hay duda de autoridad)
    ↓
Plan (crear/consultar según el gate de autorización)
    ↓
ejecución
    ↓
C1/C2/C3 (gates deterministas según §17)
    ↓
validation (anchor A1; A2 si revalidación)
    ↓
checkpoint (consistencia GC-1)
    ↓
Closed (condición derivada)
```

Demuestra que el agente comienza una operación leyendo `AGENTS.md` +
`.agents/AGENTS.md` y carga el resto on-demand; no necesita leer todo `docs/`.
El propio Plan 101 es el primer dogfood del ciclo de creación (clasificado,
registrado, sin ejecutar; su cierre usará el lifecycle en la ejecución futura).

## 21. Commit Strategy

**[PROPOSED — Future Implementation]** Patrón real de Planes 96–100 (commit de
contenido C1 + commit de registro/cierre C2; sin push/tag/release):

- **C1 (materialización/integración):** árbol `.agents/` + puntero en
  `AGENTS.md` raíz + ajustes mínimos de `docs/AGENTS.md` y
  `docs/CONVENTIONS.md`; mensaje propuesto:
  `feat(agents): materialize dev operational layer (plan 101, RFC-75)`.
- **C2 (documentación/registro):** Validation Anchor, Checkpoint, espejo del
  INDEX, eliminación del staging, ítem `(plan 101)` en
  `CHANGELOG.md:[Unreleased]`; mensaje propuesto:
  `docs(plans): record plan 101 validation anchor and checkpoint (plan 101, RFC-75)`.
- Sin push, sin tag, sin `VERSION` bump, sin release; working tree limpio al
  cierre; el registro de cierre no embebe su propio SHA/tree
  (auto-referencia excluida).

## 22. Recovery / Stop Conditions

**[PROPOSED]** La ejecución futura usa **Git como mecanismo factual de
recuperación** (sin mecanismos especiales) y se detiene/escala (AU-3) ante:

| Incidencia | Detección | Acción de recovery |
|---|---|---|
| Materialización parcial | `git status` / árbol incompleto | Completar los archivos faltantes según §12 antes de continuar; nunca cerrar parcial |
| Archivos incorrectamente ubicados | Paths fuera de `.agents/` | Mover al path canónico antes de C2; verificar diff |
| Divergencia staging/`.agents/` | Comparación de contenido | Resolver contra el diseño staged; documentar cualquier corrección factual |
| Modificación accidental de `protocol/.agents/` | `git status`/diff | STOP; revertir solo el cambio accidental (`git restore` sobre paths verificados) y escalar; nunca mezclarlo |
| Root `AGENTS.md` incorrecto | Revisión del puntero | Corregir el puntero mínimo; sin duplicar contenido |
| Documentación incoherente | Checkers documentales | Corregir la sección afectada de `docs/AGENTS.md`/`docs/CONVENTIONS.md` dentro del alcance §13 |
| Validación fallida | pytest/checkers | Corregir la causa dentro del scope o registrar desviación aceptada por el mantenedor; no reportar PASS |
| Rollback antes del cierre | Decisión del ejecutor/mantenedor | Revertir commits/working tree del plan (cambio aditivo y reversible); los registros parciales se tratan como legacy si se revierte |

Stop conditions bloqueantes: autoridad normativa inexistente; decisión humana
requerida; conflicto normativo; cambio fuera de scope; evidencia insuficiente
para decisión obligatoria; ANOMALY de C1/C2/C3; intento de modificar historial
cerrado o `protocol/.agents/`; resolución de decisión humana por inferencia.
Deuda no bloqueante se registra, no congela la ejecución.

## 23. Validation Strategy (ejecución futura)

**[PROPOSED]** La validación del contenido corre **antes** de agregar los
registros de cierre (anti-circularidad; precedente Planes 96–100):

- Validation command-set: batería canónica
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`), C1/C2/C3,
  `git diff --check` y el caso de dogfooding de §20.
- Declared scope / effective inputs / observed dependencies / environmental
  factors / Scoped Content Identity (state identity + delta v1): se registran
  en `## Validation anchor` al ejecutar.
- Política de "batería verde" del plan 94 §24.1: PASS real o desviación
  documentada aceptada por el mantenedor.

## 24. Anchor Strategy (ejecución futura)

**[PROPOSED]** Al ejecutar, este artifact registrará su propio Validation
Anchor en la sección `## Validation anchor` (no se fabrica en esta iteración):
V1 sobre el contenido del commit C1 (estado validado = tree id de C1), delta
scoped identity sobre el scope del cambio (los cinco archivos `.agents/` + los
tres documentos de integración), según formato v1
(`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`).
No reutiliza anchors de Planes 96–100.

## 25. Checkpoint Strategy (ejecución futura)

**[PROPOSED]** Al ejecutar, este artifact registrará su Checkpoint en la
sección `## Checkpoint / cierre`: commits C1/C2, estado validado (ref al
anchor), estado de cierre (tree id del commit final; auto-referencia
excluida), consistencia checkpoint↔anchor (revalidación V2 sobre el estado
final antes de `Closed` si difiere), governance aplicada y condición derivada
`Closed` (docs-only, sin release), conforme a GC-1
(`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).

## 26. Governance Constraints

**[NORMATIVE]** RFC-75, ADR-15, ADR-16, RFC-46/56/69 y Planes 94–100
permanecen intactos en todas las etapas. El espejo del INDEX se actualiza en el
mismo commit de registro; el INDEX es descriptivo, nunca autoridad (ADR-16
AU-4). Cierre docs-only sin `VERSION` bump ni tag (RFC-69). Sin commits en
esta iteración (decisión del mantenedor, práctica del repo).

## 27. Change Lifecycle for Plan 101

**[PROPOSED]** Estado del propio Plan 101:

```text
Plan 101 = Aprobado para ejecución (PLANNED / OPEN)   ← esta iteración
Planned = YES
Executed = NO
Committed = NO
Verified = NO
Closed = NO
Released = NO
```

La ejecución futura sigue la cadena: baseline → materialización → integración
→ validación V1 + anchor propio → findings/corrections/revalidación si surgen
→ checkpoint con consistencia → `Closed` (docs-only). `Planned`/`OPEN` es
condición descriptiva de la fase de creación; el status mecánico del repo es
`Aprobado para ejecución` (vocabulario vigente de planes en
`docs/CONVENTIONS.md:Convenciones`).

## 28. Riesgos

| Riesgo | Mitigación |
|---|---|
| `.agents/` como autoridad normativa superior | Regla explícita §15/AC-101-07: conversión de contratos en operación; `docs/` sigue siendo autoridad |
| Colisión con la regla «Frontera documental» de `docs/CONVENTIONS.md` | El ajuste §13.3 acota el scope de esa regla a Producto vs DEV sin reinterpretar el Producto |
| Dos fuentes operacionales (staging + `.agents/`) | Transición §7 con eliminación del staging tras materialización verificada (AC-101-09) |
| Checkers escaneando el árbol `.agents/` nuevo | Verificación en G5; si un checker existente reporta el dominio como ajeno, registrar finding y escalar (sin modificar C1/C2/C3 de entrada) |
| Scope creep (workflows/policies del Producto) | Out of scope §9.3/§10; frontera §14 |
| Burocracia en la operación | Entry point mínimo; carga on-demand; sin state machines ni registries |

## 29. Dependencies

**[NORMATIVE + OBSERVED]** RFC-75 `Accepted`; ADR-15/16 `Accepted`; RFC-46/56/69
`Accepted`; Planes 94–100 cerrados (históricos); C1/C2/C3 presentes; staging
`sessions/agents-dev-layer/` presente como fuente de diseño; batería canónica
verde al cierre de cada etapa.

## 30. Pending / Open Questions

- **OQ-1** — Autorización humana de la ejecución futura y de los commits C1/C2
  (owner: mantenedor; escalación: humana; blocking: no para la creación;
  resolución: pendiente). Se registra formalmente como pending en la ejecución
  si corresponde (PC-1).
- **OQ-2** — Aceptación de la batería al cierre de la ejecución futura
  (owner: mantenedor; se resuelve con evidencia al ejecutar).
- **OQ-3** — Si la ejecución descubre interacción de los checkers existentes
  con el árbol `.agents/` nuevo: registrar finding y escalar; no se asume
  ninguna modificación de C1/C2/C3.

## 31. Veredicto final

**`GO — CREATION ONLY`** para esta iteración: el Plan 101 queda creado y
registrado (Status `Aprobado para ejecución`; `Planned: YES`; sin ejecución).
**`GO WITH CONDITIONS`** para la ejecución futura: condiciones C1–C4 —
(C1) autorización explícita del mantenedor; (C2) criterios de entrada y batería
verde o desviación aceptada; (C3) sin scope creep fuera de §9/§10; (C4) cierre
docs-only con anchor/checkpoint propios. No se detectaron BLOCKERs.

## 32. Traceability Matrix

**[DERIVED]**

| Requisito / decisión | Fuente | Sección del plan | Evidencia futura |
|---|---|---|---|
| Lifecycle DEV operativo consumible por agentes | RFC-75 `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`; Plan 94 §18 | §5/§12 | `.agents/` materializado; dogfooding §20 |
| Clases de autoridad y protocolo de conflicto | ADR-16 `docs/adr/16-change-lifecycle-authority.md:Decisión` | §15 | `policies/authority.md` |
| Continuidad/checkpoint (CL-1..CL-10) | ADR-15 `docs/adr/15-change-lifecycle-continuity.md:Invariantes` | §16/§25 | `policies/validation-closure.md`; checkpoint C2 |
| GC-1 corregido (correspondencia de estado, sin latest A2 wins) | Decisión B `fc52c88`; Plan 99 (F-1); C-2 | §16/§17 | Política de cierre + gate C-2 |
| Checker factual ≠ autoridad; GAP ≠ ANOMALY | ADR-16 AU-1/AU-4; RFC-75 Mec. 14 | §15/§17 | `policies/lifecycle-checkers.md` |
| Frontera DEV/Protocol sin mecanismos compartidos | RFC-75 `docs/rfc/75-change-lifecycle.md:Dev vs Protocol`; RFC-55 | §14 | Independencia verificada (G3; AC-101-08) |
| Versionado docs-only sin release | RFC-69; `docs/VERSIONING.md:3. Versionado` | §9/§21/§26 | `Closed` docs-only; sin tag |
| Taxonomy/estructura del repo | `docs/AGENTS.md:Folder → class map` | §13 | Ajuste taxonómico mínimo |
| Batería canónica | `docs/VERSIONING.md:4.1 Batería canónica de verificación` | §19/§23 | G0/G5/G7 PASS |

---

## Validation anchor

Registrado al ejecutar el Plan 101 (2026-09-03). La validación **V1** corrió
sobre el contenido de materialización (commit de contenido C1) **antes** de
agregar los registros de cierre de esta sección (anti-circularidad, §23/§25;
precedente Planes 96–100).

- Declared scope: materialización de la capa `.agents/` DEV en la raíz del
  repo fuente (`.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md`,
  `.agents/policies/authority.md`, `.agents/policies/validation-closure.md`,
  `.agents/policies/lifecycle-checkers.md`) + integración mínima de
  descubrimiento/taxonomía/frontera (`AGENTS.md`, `docs/AGENTS.md`,
  `docs/CONVENTIONS.md`) + batería canónica del repo + C1/C2/C3.
- Validation command-set:
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp`
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python tools/check_lifecycle_anchor.py`
  - `python tools/check_lifecycle_checkpoint.py`
  - `python tools/check_lifecycle_lineage.py`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/` y la
  raíz; pytest consume `tests/` + `tools/`); representado por el State
  identity (tree id). El working tree validado incluía además los registros de
  creación del Plan 101 (`docs/plans/INDEX.md` modificado + este artifact sin
  trackear, pendientes de C2), ajenos al contenido de C1 inspeccionado por la
  validación V1.
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta ejecución); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de
  verificación`).
- Environmental factors: OS Windows; Python 3.14; git 2.55; pytest 9.0.3;
  `protocol/.agents/VERSION` = 10.3.0; pytest ejecutado con basetemp local
  `.pytest_cache\basetemp` por ACL del basetemp `pytest-of-rolda` (ruido
  ambiental documentado en planes 96–100); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `74f96b14fb853c1410b9feadca0061bea704b3c6` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 8 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `47c95eee4ad496bd321ba932c69571236b2daebc5625d8d9e60cd2eb81727be2`.
    Pares path → blob (C1):
    `.agents/AGENTS.md` → `6f9dcd901cf7771c77115737d24631cd6bfa42f8`;
    `.agents/policies/authority.md` → `720cb07d20472dc5c00875a323124c48608def68`;
    `.agents/policies/lifecycle-checkers.md` →
    `338dd2dd515ac790bd13292620779348a9d5e938`;
    `.agents/policies/validation-closure.md` →
    `474edc1af9ab2493b604f55e843232a3c4055374`;
    `.agents/workflows/change-lifecycle.md` →
    `206c61fea2ab78bb2cef601accfa5326d6792a67`;
    `AGENTS.md` → `029e49b4c277e576ba6a70ef26196251086114bc`;
    `docs/AGENTS.md` → `f77551f5efbecede6a61001d3d0c39264619f369`;
    `docs/CONVENTIONS.md` → `97e6072c15e4b25eec412bbc35b84084ec61c6d6`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería completa +
  pytest + dogfooding C1/C2/C3 sobre el estado final de la ejecución, incluidos
  los registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7; §25 de este
plan). Se registra en el commit de registro C2, posterior al commit de
contenido C1.

- Commits de cierre:
  - C1 `37065700c95ee14a4ef07375fc320a67742fc0a8` —
    `feat(agents): materialize dev operational layer (plan 101, RFC-75)`
    (contenido de la capa `.agents/` + integración, validado por V1).
  - C2 — este commit de registro
    (`docs(plans): record plan 101 validation anchor and checkpoint (plan 101,
    RFC-75)`); su SHA se identifica por el mensaje y el árbol no embebe su
    propia identidad (auto-referencia excluida, §21).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `74f96b14fb853c1410b9feadca0061bea704b3c6`; Delta scoped identity =
  `47c95eee4ad496bd321ba932c69571236b2daebc5625d8d9e60cd2eb81727be2`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`74f96b14…`) → **PASS**.
  - Estado final (C2): difiere de C1 en los registros de cierre (anchor/
    checkpoint de este plan, contenedor de findings/pending, INDEX y
    changelog); **revalidación V2** (batería canónica completa + pytest +
    dogfooding C1/C2/C3 sobre el contenido final de la ejecución, ejecutada
    antes del commit) → PASS. GC-1 queda satisfecho por revalidación antes de
    `Closed` (la consistencia del estado de cierre se evalúa contra A2/V2;
    correspondencia por estado, nunca por recencia, nunca por generic tree
    membership).
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 101, RFC-75)` en `CHANGELOG.md:[Unreleased]`; capa DEV-only
  docs-only, sin `VERSION` bump ni tag.
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a
artifacts nuevos; la ausencia de registros no es invalidez):

### Findings

- `No findings detected / N/A` (no se fabrican findings sintéticos).

### Correcciones

- `N/A` (ninguna corrección en esta iteración).

### Pending decisions

Pendings **no-bloqueantes** (PC-1), owner: mantenedor, escalación: humana
(AU-3); condiciones reales del Plan (§30) resueltas al ejecutar:

- `<PLAN-101>` — decisión: OQ-1 autorización de ejecución y commits; blocking:
  no; owner: mantenedor; escalación: humana; resolución: autorización explícita
  otorgada por el mantenedor (Execution Prompt 2026-09-03); ejecución y commits
  C1/C2 realizados en `dev`; resuelto.
- `<PLAN-101>` — decisión: OQ-2 aceptación de la batería al cierre; blocking:
  no; owner: mantenedor; escalación: humana; resolución: batería aceptada al
  cierre (pytest `428 passed, 0 failed`; checkers canónicos PASS; dogfooding
  C1/C2/C3 GAP=0, ANOMALY=0); resuelto.

## Trazabilidad

Origen → solicitud del mantenedor (2026-09-02) + diseño staged
`sessions/agents-dev-layer/` → RFC-75 `Accepted` + ADR-15/16 (Accepted) +
Planes 94–100 (históricos) → este Plan 101 (creación y registro) → ejecución
futura autorizada (materialización `.agents/` + integración mínima) →
validación V1 → checkpoint con revalidación V2 → cierre docs-only. Este Plan no
autoriza cambios de payload (RFC-56); la autorización de la ejecución es humana
(OQ-1).

## Nota de ejecución

- 2026-09-03 — **Ejecución del Plan 101** (autorización explícita del
  mantenedor; Execution Prompt). Gates G0–G7 superados: baseline G0 (branch
  `dev`, HEAD `d93d234`, working tree con los registros de creación del plan,
  pytest `428 passed`, checkers canónicos PASS, C1/C2/C3 GAP=0/ANOMALY=0,
  `.agents/` ausente, staging presente, `protocol/.agents/` intacto);
  materialización G1 (cinco archivos en `.agents/` desde el diseño staged,
  1:1 verificado por hash, con ajuste mínimo de coherencia del ejemplo de
  dogfooding del workflow); integración G2–G4 (puntero en `AGENTS.md` raíz;
  taxonomía en `docs/AGENTS.md`; frontera documental Producto vs DEV en
  `docs/CONVENTIONS.md`); aislamiento G5 (sin cambios en `protocol/`,
  `runtime/`, `tools/`, `tests/`, `dist/`); validación G6 (pytest `428
  passed, 0 failed`; checkers canónicos PASS; `git diff --check` limpio);
  dogfooding G7 (cadena `AGENTS.md` → `.agents/AGENTS.md` → workflow →
  policies verificada; sin cambios adicionales); staging eliminado tras la
  materialización verificada (sin segunda copia operacional); Validation
  Anchor V1 y Checkpoint con revalidación V2 registrados arriba; commit C1
  `3706570` (contenido) y commit C2 (registro) en `dev`; sin push, sin tag,
  sin `VERSION` bump, sin release. Estado final: `Planned: YES; Executed: YES;
  Committed: YES; Verified: YES; Closed: YES; Released: NO`. Sin findings ni
  corrections reales (`N/A`); sin recovery necesario; sin F-3/F-2…F-9; RFC-75,
  ADR-15/16 y Planes 94–100 intactos.
