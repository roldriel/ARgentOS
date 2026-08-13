# RFC-56 — Clasificación de cambios del payload y vía rápida de gobernanza

**Status:** Accepted (2026-08-12, autorización explícita del usuario, incluida la Clase C; la serie Proposal se revisa una por una)
**Fecha:** 2026-08-12
**Serie:** Gobernanza
**Origen:** `docs/AUDITORIA_DOCUMENTACION.md` §Feedback crítico (la gobernanza escala peor que el protocolo; regularizaciones retroactivas repetidas; 23 RFCs en `Proposal`).
**Pregunta:** ¿Qué cambios del payload requieren RFC y cuáles pueden ejecutarse por vía plan con verificación mecánica?
**Afectados:** `plans/INDEX.md` §Convenciones (bullets Inmutabilidad y ciclo de status), `docs/VERSIONING.md` §7, `AGENTS.md` raíz (Task lifecycle). No toca `protocol/.agents/` por sí misma.

## Problema

La regla vigente (`plans/INDEX.md` §Convenciones, Inmutabilidad) exige RFC `Accepted` o plan `Aprobado para ejecución` para todo cambio de `.agents/`, sin distinguir la naturaleza del cambio. La evidencia acumulada muestra que la ceremonia completa no escala:

- RFC-24…28 se regularizaron retroactivamente (11 ago 2026, plan 41).
- Los planes 31–36 se ejecutaron por vía plan con las RFC-35…37 aún en `Proposal`, regularización pendiente.
- Los planes 55–56 (12 ago 2026) volvieron a usar la vía plan porque el cambio era claramente menor.
- 23 RFCs (32…54) llevan redactadas en `Proposal` sin ejecutar: diseño aprobado en papel que no avanza.

El resultado es deuda de gobernanza recurrente: el estado documental se desfasa de la realidad y hay que regularizar a posteriori cada pocas semanas.

## Decisión propuesta

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

## Amendment Log

- 2026-08-12 — Creación.
- 2026-08-12 — Accepted por autorización explícita del usuario: Clase C confirmada; la regularización de la serie Proposal se hace con revisión individual por RFC, no masiva.
