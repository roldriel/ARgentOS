# ADR-18 — Payload Boundary, Provenance and Classification

**Status:** Accepted
**Fecha:** 2026-09-15
**Decisión original:** — (decisiones nuevas de arquitectura de repositorio, decisiones C–K de la síntesis; no derivan del modelo D#)
**RFC:** — (Clase B de RFC-56: mejora documental compatible, vía plan; no cambia significado de protocolo ni rompe compatibilidad con adoptantes)
**Plan:** plan 126 (`docs/plans/126-repository-architecture-decisions-ck.md`)
**Clase de cambio:** B (aclaraciones documentales de payload + documentación de un vocabulario ya en uso; ver `## Estado de implementación`)
**Problemas que resuelve:** — (ambigüedad de distribución del harness, provenance del payload, enforcement del boundary, status del vocabulario `kind`, navegación y efecto del probe; ver Contexto)

## Contexto

ADR-17 fijó el modelo de *lifetime* y la arquitectura estructural compuesta, y dejó ocho decisiones de placement explícitamente abiertas (C, D, E, G, H, I, J, K). Una síntesis posterior las analizó contra evidencia primaria y el mantenedor aceptó un bundle de opciones (2026-09-15). Este ADR registra la decisión arquitectónica resultante.

Los hechos que la motivan:

- `protocol/.agents/harness/tests/` ejercita exclusivamente los cuatro scripts que **sí** se distribuyen (`hook_gate.py`, `runner_state.py`, `health_check.py`, `gate_validator.py`) y no referencia ningún path DEV; `publish-dist.yml` copia `protocol/.agents` sin exclusiones, de modo que los tests ya viajan en `dist`. La declaración de `harness/INDEX.md` enumeraba los cinco checkers DEV de `tools/` como «dev-only» y era legible como si los harness tests también lo fueran, aunque ningún artefacto del payload lo afirmara.
- Dos contratos del payload citan su **fuente normativa** en `docs/rfc/` — gobernanza del repositorio fuente que no se publica al adoptante —, mientras el checker de frontera declaraba `docs/` como violación pero **no** incluía `docs` en su conjunto de segmentos prohibidos: la regla existía y no era aplicable.
- `tags.kind` enumeraba ocho valores, mientras cinco archivos del payload declaraban `state_machine` (4 máquinas de estado) o `taxonomy` (el propio diccionario). Ningún consumidor validaba los valores: H13 exige la **presencia** del bloque y cruza `kind` sólo para `workflow` y `contract`.
- `ADR-17` dejó `docs/` sin reorganizar por lifetime, de modo que las inconsistencias de clasificación documental sólo podían resolverse **en el lugar**.
- La creación de `protocol/.project/` por el health probe es una consecuencia de diseño (round-trip auto-limpiante) y no un artefacto persistente.

## Alternativas consideradas

### A — Distribución de los harness tests

- **A1 (elegida):** son parte del payload y se reconcilia la declaración.
- **A2:** son DEV-only; se mueven fuera de `protocol/` y se reapunta CI. Descartada: los tests asumen el layout del adoptante, no referencian tooling DEV, y ningún artefacto del payload los declara no distribuidos; moverlos cambiaría lo que recibe el adoptante sin que exista una regla que lo exija.

### B — Referencias del payload a `docs/`

- **B1:** eliminar las citas. Descartada: borra la traza de autoridad del propio payload.
- **B2:** sustituirlas por referencias locales al payload. Descartada: no existe material local equivalente; las RFCs *son* la fuente normativa.
- **B3:** vendorizar un equivalente. Descartada: crea una segunda fuente de verdad.
- **B4 (elegida):** excepción acotada y documentada por par (archivo citante, target exacto).
- **B5:** diferir. Descartada: la regla de frontera seguiría siendo inaplicable.

### C — Enforcement del boundary

- **C1 (elegida):** extender el checker existente con `docs` en el conjunto de segmentos prohibidos, más la allowlist de B4.
- **C2:** sólo documentación (estrechar la prosa de la regla). Descartada: dejaría un invariante declarado inaplicable.
- **C3:** un checker nuevo. Descartada: ya existe y el punto de extensión es una entrada de conjunto.

### D — Vocabulario `tags.kind`

- **D1 (elegida, con D2):** declararlo vocabulario documentado **no exhaustivo**, y añadir los dos valores ya en uso.
- **D2 (elegida, con D1):** añadir los dos valores a la lista.
- **D3:** cambiar los cinco consumidores a valores declarados. Descartada: reescribiría cuatro máquinas de estado y su especificidad sin que ningún consumidor lo requiera.
- **D4:** diferir. Descartada: la deriva queda invisible.

### E — Navegación / INDEX

- **E1 (elegida):** INDEX opcional y semántico; no se crea ninguno.
- **E2:** un INDEX por dominio. Descartada: superficie descriptiva sin consumidor ni regla que la exija.

### F — `protocol/.project/`

- **F1 (elegida):** sin cambio de comportamiento; el directorio es consecuencia correcta del probe.
- **F2:** cambiar el probe. Descartada: alteraría un script distribuido para eliminar un directorio vacío e ignorado.

### G — Clasificación documental DEV

- **G1 (elegida):** corrección de clasificación **en el lugar**, sin relocalización.
- **G2:** separación física por lifetime. Descartada por A3/B4 (ADR-17): lifetime es semántico y `docs/` no se reorganiza.

## Decisión

Se materializan las decisiones aceptadas por el mantenedor:

1. **Distribución (C1).** Los harness tests de `.agents/harness/tests/` **forman parte del payload distribuido** y son la suite de regresión del harness. Los cinco checkers de desarrollo de `tools/` siguen siendo DEV-only. La distinción es intencional y queda declarada en `.agents/harness/INDEX.md`.
2. **Provenance (D4).** El payload **puede** citar su fuente normativa no distribuida mediante una **excepción acotada, explícita y auditable**, limitada al par (archivo citante, target exacto). No se elimina provenance, no se vendoriza material y no se inventan fuentes locales.
3. **Enforcement (E1).** `docs/` es un **segmento de frontera prohibido** para el payload. La frontera se aplica **extendiendo el checker existente**, no creando uno nuevo. La excepción de D4 se implementa con el patrón de allowlist ya presente en el checker.
4. **Vocabulario (G2+G1).** Las listas de `tags` son **vocabulario documentado, no un enum cerrado**; `tags.kind` es **no exhaustivo/extensible**. `state_machine` y `taxonomy` se documentan como miembros. No se añade enforcement de membresía.
5. **Clasificación documental DEV (H, derivada de A3+B4).** La documentación permanece **físicamente en su lugar**; las inconsistencias de naturaleza/lifecycle se corrigen **en el lugar**. `docs/architecture/` se clasifica **Historical** (`archived`) y `docs/AUDITORIA_DOCUMENTACION.md` como **Working/Audit** de raíz. No se crean clases documentales nuevas.
6. **Harness (I, derivada de C1).** La estructura actual del harness se mantiene: navegación, policy, código ejecutable del protocolo y tests de regresión. No se reestructura ni se mueve.
7. **Navegación (J1).** Un INDEX es **opcional y semántico**: existe por valor de navegación o de carga, no por simetría estructural. Su ausencia no es un defecto; su presencia no lo convierte en autoridad.
8. **Probe (K3).** La creación de `.project/` por el health probe se **acepta como correcta**: el round-trip es auto-limpiante, no deja artefacto persistente, el directorio está ignorado y nunca versionado, y el comportamiento no entra en conflicto con ADR-17. Sin cambio de comportamiento.

**Límite de autorización.** Este ADR **no autoriza migración**, no diseña el Repository/Artifact Placement Contract y no habilita cambios de payload fuera de la Clase B declarada.

## Consecuencias

- Un agente puede determinar qué se distribuye y qué no sin inferencia, y los dos pares de provenance quedan auditables y acotados.
- La frontera del payload pasa a ser **aplicable** para `docs/`, no sólo declarada; la regla preexistente no se debilita, se completa.
- La deriva del vocabulario `kind` queda resuelta como documentación, sin reclasificar artefactos ni añadir validación.
- La corrección documental DEV es puramente de clasificación: ninguna cita cambia de resolución y ninguna historia se reescribe.
- La asimetría de INDEX queda documentada como intencional.
- La allowlist de provenance introduce una **obligación de mantenimiento**: añadir una entrada exige autorización y documentación propias.

## Invariantes

- **RS-8**: Todo lo que vive bajo `.agents/` se distribuye tal cual, incluidos los tests de regresión del harness; los checkers de desarrollo de `tools/` no se distribuyen.
- **RS-9**: El payload puede citar su fuente normativa no distribuida **sólo** mediante una excepción acotada al par (archivo citante, target exacto); ninguna excepción autoriza un prefijo, un directorio ni una clase de path.
- **RS-10**: `docs/` es un segmento de frontera prohibido para el payload; la frontera se aplica con el checker existente, y la excepción nunca relaja la regla para el resto de los archivos.
- **RS-11**: Las listas de `tags` son vocabulario documentado, no un enum; `tags.kind` es no exhaustivo y su membresía no se valida mecánicamente.
- **RS-12**: La clasificación documental se corrige en el lugar; ninguna carpeta se reorganiza para expresar lifetime (ADR-17 RS-1/RS-2/RS-4).
- **RS-13**: La estructura del harness es coherente y no se subdivide por simetría.
- **RS-14**: Un INDEX es opcional y semántico, y nunca autoridad.
- **RS-15**: Un directorio runtime efímero creado por un probe auto-limpiante en el árbol fuente no es un artefacto y no requiere corrección.

## Relaciones

- Depende de: ADR-17 (lifetime semántico y estructura compuesta: determina la respuesta documental y prohíbe la relocalización).
- Consume, sin modificarlos: ADR-15 y ADR-16 (lifecycle y autoridad de cambios DEV) y RFC-56 (clases de cambio).
- Formalizada en: plan 126 (`docs/plans/126-repository-architecture-decisions-ck.md`).

## Estado de implementación

**Materializado en este mismo cambio** (plan 126):

- `tools/check_protocol_invariants.py` — `docs` en el boundary declarado + allowlist de provenance acotada por par + helper (RS-9, RS-10).
- `tests/test_check_protocol_invariants.py` — cobertura de los cuatro casos exigidos: `docs/` ordinario rechazado; provenance allowlisted aceptada; la allowlist no autoriza otros `docs/`; no aplica a un archivo no listado.
- `protocol/.agents/harness/INDEX.md` — declaración de qué se distribuye y qué no (RS-8, RS-13).
- `protocol/.agents/roles/profiles/functional_writer.md` — la mención a `docs/` es la carpeta del proyecto adoptante, no la del repo fuente.
- `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — `tags` como vocabulario documentado no cerrado; `state_machine` y `taxonomy` añadidos (RS-11).
- `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` — semántica del probe y de su target (RS-15).
- `docs/AGENTS.md` — INDEX opcional/semántico (RS-14) y mapa folder→clase con lifecycle, `docs/architecture/` Historical y la excepción Working de raíz (RS-12).

**Pendiente / no autorizado por este ADR:**

- Repository/Artifact Placement Contract — **no diseñado**; downstream de ADR-17, de este ADR y de las decisiones que queden abiertas.
- Cambios de payload fuera de la Clase B declarada.
- La lectura contractual de `tags.kind` (PC-1), la supervivencia a largo plazo de la allowlist (PC-2) y cualquier política de pureza del árbol fuente (PC-3) quedan como pendientes del plan 126.

El status `Accepted` refleja la **decisión registrada**, no el estado de formalización de implementaciones futuras; no habilita cambios de payload por sí solo.
