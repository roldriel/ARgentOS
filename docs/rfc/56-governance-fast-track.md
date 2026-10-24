# RFC-56 — Clasificación de cambios del payload y vía rápida de gobernanza

**Status:** Accepted (2026-08-12, autorización explícita del usuario, incluida la Clase C; la serie Proposal se revisa una por una)
**Fecha:** 2026-08-12
**Serie:** Gobernanza
**Origen:** `docs/AUDITORIA_DOCUMENTACION.md` §Feedback crítico (la gobernanza escala peor que el protocolo; regularizaciones retroactivas repetidas; 23 RFCs en `Proposal`).
**Pregunta:** ¿Qué cambios del payload requieren RFC y cuáles pueden ejecutarse por vía plan con verificación mecánica?
**Afectados:** `plans/INDEX.md` §Convenciones (bullets Inmutabilidad y ciclo de status), `docs/VERSIONING.md` §7, `AGENTS.md` raíz (Task lifecycle). No toca `protocol/.agents/` por sí misma.

> **Enmienda vigente (2026-10-23, Plan 174).** El modelo de clasificación fue
> precisado por instrucción directa del mantenedor: la clasificación A/B/C
> pertenece al **payload delta** (no al Change, al Plan ni al documento que lo
> describen); un Change puede contener varios deltas con clases distintas y su
> ruta efectiva la fija la **clase más estricta presente**; un Change sin efecto
> sobre el payload es **RFC-56 N/A**. La sección `## Decisión propuesta`
> conserva el texto original como registro histórico y está **superada** por
> `## Modelo vigente (enmienda 2026-10-23)`, que es la formulación operativa que
> debe aplicarse. Ver `## Amendment Log`.

## Problema

La regla vigente (`plans/INDEX.md` §Convenciones, Inmutabilidad) exige RFC `Accepted` o plan `Aprobado para ejecución` para todo cambio de `.agents/`, sin distinguir la naturaleza del cambio. La evidencia acumulada muestra que la ceremonia completa no escala:

- RFC-24…28 se regularizaron retroactivamente (11 ago 2026, plan 41).
- Los planes 31–36 se ejecutaron por vía plan con las RFC-35…37 aún en `Proposal`, regularización pendiente.
- Los planes 55–56 (12 ago 2026) volvieron a usar la vía plan porque el cambio era claramente menor.
- 23 RFCs (32…54) llevan redactadas en `Proposal` sin ejecutar: diseño aprobado en papel que no avanza.

El resultado es deuda de gobernanza recurrente: el estado documental se desfasa de la realidad y hay que regularizar a posteriori cada pocas semanas.

## Decisión propuesta

> **Superada por `## Modelo vigente (enmienda 2026-10-23)`.** Se conserva como
> registro histórico de la decisión original (RFC-46). No aplicar como texto
> vigente sus definiciones de clase, su regla de borde ligada al resultado de un
> checker ni su alcance «todo cambio del payload»; la formulación operativa es
> la del modelo vigente.

Clasificar todo cambio del payload en tres clases, cada una con su vía mínima:

- **Clase A — Modelo conceptual o contratos** (cambia el significado del protocolo, sus contratos, sus máquinas de estado, o rompe compatibilidad con adoptantes): requiere RFC `Accepted`. Sin excepciones.
- **Clase B — Mejora documental compatible** (secciones aclaratorias, reubicación de contenido sin cambio de significado, correcciones de redacción con criterio): vía plan `Aprobado para ejecución` con justificación documentada + batería de checkers en verde. Es la formalización de lo que hicieron los planes 34–36 y 55–56.
- **Clase C — Corrección mecánica** (typos, formato, links, whitespace; cero cambio de significado): commit directo en `dev` con la batería en verde, sin plan; se registra en el changelog de la próxima versión que se corte. La clase C solo puede declararse si ningún checker cambia de resultado semántico (mismas secciones, mismas referencias).

Reglas de borde:

- Ante la duda entre clases, se elige la más estricta.
- La clase se declara en el plan (A/B) o en el mensaje de commit (C), y es revisable: una mala clasificación detectada se trata como desviación de gobernanza y se regulariza explícitamente.
- La verificación mecánica (checkers + tests) es requisito en las tres clases; la gobernanza no baja la vara técnica, solo la documental.

### Regularización de la serie Proposal

Como aplicación inmediata, las RFC-32…54 se revisan **una por una**: cada una
se lee contra el estado actual del payload y se acepta (con evidencia de su
plan asociado), se descarta explícitamente (`Superseded`/sin efecto) o queda
marcada con lo que le falta. Nada de aceptación masiva: la tanda es serial y
cada RFC queda con su veredicto individual registrado en su Amendment Log.
Estados y changelog se actualizan por tanda, al cierre de la revisión de cada
grupo coherente.

## Alternativas consideradas

- **Status quo (toda RFC por el ciclo completo):** descartada por la evidencia de desfase recurrente citada en Problema.
- **Eliminar las RFCs para cambios menores sin clases:** descartada — sin clases explícitas, "menor" queda a criterio del momento y la frontera se erosiona (exactamente lo que ANTI_CIRCUMVENTION prohíbe en el payload desde 3.0.7).
- **Solo dos clases (A y B):** descartada — obligaría un plan por typo, que es la ceremonia que hoy ya se salta informalmente; mejor declararla y acotarla.

## Impacto en el protocolo

Ninguno directo: esta RFC gobierna el proceso de desarrollo del repo, no el contenido del payload. Indirectos:

- `plans/INDEX.md` §Convenciones: el bullet de Inmutabilidad se reescribe en términos de clases A/B/C.
- `docs/VERSIONING.md` §7 y `AGENTS.md` raíz: el flujo referencia las clases.
- `plans/_TEMPLATE.md`: el header gana un campo `Clase` (A/B) cuando el plan toca el payload.

## Criterios de aceptación

- [ ] Las tres clases y las reglas de borde escritas en `plans/INDEX.md` §Convenciones.
- [ ] `docs/VERSIONING.md` y `AGENTS.md` raíz alineados con las clases.
- [ ] Campo `Clase` en `plans/_TEMPLATE.md`.
- [ ] Revisión en tanda de RFC-32…54 ejecutada y registrada (estados + changelog).
- [ ] Batería completa en verde tras los cambios.

## Modelo vigente (enmienda 2026-10-23)

Esta sección es la formulación operativa vigente de RFC-56. Sustituye, donde
difiera, el texto de `## Decisión propuesta`, que se conserva como registro
histórico.

### 1. Unidad de clasificación: el payload delta

Un **payload delta** es una modificación con efecto sobre el payload del
producto: contenido bajo `protocol/.agents/` (o `protocol/_AGENTS.md`). Es una
unidad conceptual de análisis; no es una entidad, un artefacto, un registry ni
un lifecycle state, y no se crea ninguna entidad `Payload Change`,
`Payload Delta` o equivalente.

La clasificación RFC-56 pertenece al **payload delta**. No pertenece al
documento que lo describe (RFC, ADR, plan, nota), ni al Plan, ni al Change
completo. Un Change puede contener **cero, uno o varios** payload deltas, con
clases distintas.

### 2. Clases

- **Clase A — modelo o contratos.** Cambia el significado del protocolo, sus
  contratos, sus máquinas de estado, o rompe compatibilidad con adoptantes.
  Ruta: RFC `Accepted` + Plan `Aprobado para ejecución`.
- **Clase B — mejora documental compatible del payload.** Secciones
  aclaratorias, reubicación de contenido sin cambio de significado o
  correcciones de redacción con criterio, siempre que el significado y los
  contratos del payload no cambien. Ruta: Plan `Aprobado para ejecución` con
  justificación documentada + batería en verde.
- **Clase C — transformación mecánica.** Transformación del payload que
  **preserva la semántica normativa y los contratos del payload**. Ruta: commit
  directo en `dev` con la batería en verde y registro en el changelog de la
  próxima versión, cuando la ruta directa sea aplicable (§5).

A/B/C **no** significan «código / documentación / typo». Clase B no es sinónimo
de «cambio documental» en general: es una mejora documental **del payload**. Un
cambio DEV puro (tooling, tests, runtime, documentación operativa) no tiene
clase RFC-56.

### 3. Clase C — definición semántica

Es Class C una **transformación mecánica del payload que preserva la semántica
normativa y los contratos del payload**. Ejemplos típicos: typo; whitespace;
formato; corrección puramente representacional; link corregido cuando la
corrección no altera el significado; reorganización puramente representacional
cuando la semántica permanece idéntica.

No es Class C si cambia una restricción, una condición, una excepción, una
transición, una interpretación, un contrato, un identificador consumido
semánticamente o una regla normativa.

**El checker es evidencia factual, no autoridad normativa.** Que un checker
produzca el mismo resultado no demuestra por sí solo que un cambio sea Class C.
La justificación de C es conceptualmente:

```text
preservación semántica
+ verificación aplicable (batería en verde; resultado de los checkers sin cambio
  cuando corresponda)
+ ausencia de cambio normativo
→ Class C
```

Un resultado de checker sin cambio es evidencia que sostiene el juicio; no lo
sustituye. Inversamente, un cambio en el resultado de un checker no convierte
por sí solo el cambio en Clase A o B: obliga a revisar si la semántica se
preservó. Una modificación semántica es Clase A o B aunque ningún checker
cambie de resultado.

### 4. Changes multi-clase y ruta efectiva

Un Change con varios payload deltas tiene varias clases. La ruta efectiva la
determina la **clase más estricta presente**, con el orden:

```text
A > B > C > N/A
```

| Composición de payload deltas | Ruta efectiva |
|---|---|
| sin payload deltas (N/A) | ninguna vía RFC-56; lifecycle DEV + Change Level |
| C | Direct (si la ruta directa es aplicable) |
| B | Plan |
| A | RFC `Accepted` + Plan |
| B + C | Plan |
| A + C | RFC `Accepted` + Plan |
| A + B | RFC `Accepted` + Plan |
| A + B + C | RFC `Accepted` + Plan |

No existe una clase `AB` ni ninguna clase combinada. No hace falta una entidad
nueva ni dividir el Change para evitar la composición: un delta C puede formar
parte del mismo Plan que los deltas A/B, y un Change exclusivamente C va por la
ruta directa cuando esa ruta es aplicable (§5). Convertir artificialmente un
Change multi-clase en varios Changes para eludir la clase más estricta es una
desviación de gobernanza.

### 5. RFC-56 N/A y relación con el Change Level

Un Change **sin payload deltas** es **RFC-56 N/A**. Su governance proviene del
lifecycle DEV (RFC-75) y de su Change Level. No se le asigna una clase A/B/C
«por defecto» y no se usa Clase B como sinónimo de cambio documental.

La clase RFC-56 y el **Change Level** son dimensiones independientes:

- la clase RFC-56 expresa la naturaleza semántica del cambio **sobre el
  payload**;
- el Change Level expresa complejidad, coordinación, alcance e impacto del
  Change (`Level = max(coordination, scope, architectural impact, release
  impact, duration/complexity)`; RFC-75 Mecanismo 2).

Una clase estricta no eleva por sí sola el Change Level y un Change Level alto
no cambia la clase. El Level se computa siempre desde sus cinco dimensiones, no
desde la clase. Son combinaciones posibles `RFC-56 Class = C` con
`Change Level = L3` y `RFC-56 Class = A` con `Change Level = L0`, siempre que las
cinco dimensiones del Level permitan ese valor.

**Ruta directa aplicable.** La vía directa de Class C es aplicable cuando la
clase del delta es C y el Change Level no exige un Plan. El Level no se deriva
aquí: lo fija la matriz operacional L0–L3
(`docs/plans/94-change-lifecycle-master-action-plan.md:9.2 Matriz operacional L0–L3`).
Si el Level exige Plan, el Change se ejecuta con un Plan sin RFC cuya clase
RFC-56 sigue siendo C: el Level agrega maquinaria, nunca rebaja el mínimo de la
clase ni convierte C en B.

### 6. Reglas de borde

- Ante la duda entre clases, se elige la **más estricta**.
- La clase se declara en el primer artifact del Change (header del Plan:
  `**RFC-56 Class:** N/A | A | B | C`; multi-clase: `A, B`; para un cambio sin
  Plan, en el mensaje de commit) y es revisable: una mala clasificación
  detectada se trata como desviación de gobernanza y se regulariza
  explícitamente.
- La verificación mecánica (checkers + tests) es requisito en las tres clases;
  la gobernanza no baja la vara técnica, solo la documental.

## Amendment Log

- 2026-08-12 — Creación.
- 2026-08-12 — Accepted por autorización explícita del usuario: Clase C confirmada; la regularización de la serie Proposal se hace con revisión individual por RFC, no masiva.
- 2026-10-23 — **Enmienda del modelo de clasificación** (Plan 174; instrucción directa del mantenedor, Priority 3). Se precisa la unidad de clasificación (payload delta), se define Class C por preservación semántica y de contratos con el checker como evidencia y no autoridad, se formalizan los Changes multi-clase y la ruta efectiva por la clase más estricta (`A > B > C > N/A`; sin clase `AB`), se declara RFC-56 N/A para cambios sin efecto payload y se explicita la independencia respecto del Change Level y la aplicabilidad de la ruta directa de C. El texto original de `## Decisión propuesta` se conserva como registro histórico y queda marcado como superado; la formulación operativa es `## Modelo vigente (enmienda 2026-10-23)`. El Change es DEV docs-only: no modifica `protocol/.agents/` (RFC-56 Class: N/A).
