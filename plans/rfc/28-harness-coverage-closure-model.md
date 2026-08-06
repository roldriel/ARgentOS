# RFC-28 — Harness Coverage Closure Model

**Status:** Proposal

**Author:** Rodrigo Roldán

**Impact:** Structural

**Breaking Changes:** Contracts gain an explicit `enforcement` declaration; new semantic checks in policies.

---

# Abstract

Esta RFC define el **cierre de cobertura del harness**: cada contrato de artefacto declara explícitamente su nivel de enforcement (`gated` / `informational`), y las policies existentes ganan validación semántica barata y automatizable. Hoy 13 de 25 contratos no son validados por ninguna policy — la ausencia de gate es ambigua: ¿descuido o decisión? Y las validaciones vigentes son exclusivamente estructurales: el harness verifica que un artefacto existe y tiene secciones, no que su contenido sea verdadero.

El modelo convierte toda ausencia de enforcement en declaración explícita, y agrega al runner una primera capa de checks semánticos mecánicos: los paths citados en artefactos deben existir, y los tests mencionados en VERIFICATION_REPORT deben haber corrido.

---

# Motivation

- **Cobertura ambigua:** contratos como `HARNESS_REPORT`, `SESSION_LOG`, `METRICS` o los 6 de discovery no aparecen como `artifact =` en ninguna policy. Nadie puede distinguir "no se gatea porque no hace falta" de "nadie lo cableó".
- **Rigor de apariencia:** un artefacto con todas las secciones pero contenido vacío o falso pasa todos los gates actuales. El riesgo no es la validación estructural en sí — es que su existencia simula garantía semántica.
- **La semántica barata ya tiene precedente:** `tools/check_plan_citations.py` verifica que las citas de los planes resuelvan a archivos reales. La misma idea, generalizada al runner, cierra el agujero más común (paths fantasma, tests no ejecutados) sin LLM en el camino del gate.
- La taxonomía de fallos (RFC-18) ya distingue checks `[machine]` y `[agent]`: este modelo agranda la superficie `[machine]` sin tocar la `[agent]`.

---

# Goals

- Todo contrato de artefacto declara `enforcement: gated | informational` en su front matter, con referencia a la policy que lo gatea cuando aplica.
- Para los 13 contratos hoy sin policy: decisión explícita por contrato — se crea la policy correspondiente o se declara `informational`.
- Nuevo check mecánico en policies de artefactos: **los paths citados deben existir** en el repo (generalización de `check_plan_citations.py`).
- Nuevo check mecánico en la policy de verificación (H10): **los comandos de test citados en VERIFICATION_REPORT tienen evidencia de ejecución** en el log de sesión o en un archivo de resultados referenciado y existente.
- Un check de suite (test del harness) que falle si un contrato no declara `enforcement` o declara `gated` sin policy que lo cubra — la cobertura pasa a ser invariante verificado, no auditoría manual.

---

# Non Goals

Esta RFC no propone:

- validación semántica por LLM en el camino del gate (los checks `[agent]` siguen siendo juicio del worker verificador; su mecanización vía hooks queda en Future Extensions de RFC-27);
- gatear artefactos puramente informativos por gatear: la declaración `informational` es un destino legítimo y final;
- reescribir el contenido de los contratos (solo el front matter y, en su caso, la policy nueva);
- cambiar los criterios de FAIL existentes.

---

# Definitions

## Niveles de enforcement

- **`gated`:** existe una policy de harness cuyo gate debe pasar antes de que la fase correspondiente se complete. El contrato nombra la policy; la policy nombra el contrato (`artifact =`); el check de suite verifica la correspondencia bidireccional.
- **`informational`:** el artefacto se produce para trazabilidad o consumo humano/agente, y ningún gate lo valida. La declaración es la decisión: cualquier futura omisión del artefacto es deviation F2 contra el contrato, no contra un gate inexistente.

No hay tercer estado: un contrato sin declaración rompe el build de tests del harness.

## Checks semánticos mecánicos

Primera capa, ejecutada por el runner dentro de las policies existentes:

1. **Citation resolution:** todo path en backticks o en campos de citas del artefacto se resuelve contra el filesystem del repo. Path inexistente → FAIL con lista de citas rotas. (Extensión directa de la lógica de `check_plan_citations.py`, que se migra al runner.)
2. **Test evidence:** en VERIFICATION_REPORT, todo comando de test declarado debe tener evidencia: referencia a archivo de resultados existente, o entrada correspondiente en `SESSION_LOG.md`/output capturado. Comando sin evidencia → FAIL.

Ambos checks son deterministas, sin LLM, y reportan la lista exacta de incumplimientos como razón del FAIL.

---

# Consequences

- La cobertura del harness deja de ser una pregunta abierta: 25 contratos, 25 declaraciones, 0 ambigüedad.
- El harness gana su primera garantía semántica real: un artefacto ya no puede citar archivos fantasmas ni reportar tests que nunca corrieron.
- `check_plan_citations.py` converge en el runner: una sola implementación de resolución de citas (coherente con el principio de RFC-25).
- El check de suite convierte esta pasada en invariante permanente: futuros contratos nacen con declaración obligatoria.

---

# Compatibility

Breaking change moderado: los contratos ganan front matter obligatorio y H10 gana un criterio de FAIL nuevo (VERIFICATION_REPORTs que hoy pasarían podrían fallar si declaran tests sin evidencia — comportamiento deseado, pero breaking). No se tocan artefactos de sesión, ni la máquina de estados, ni los decision trees salvo las policies nuevas que resulten de la decisión por contrato.

---

# Relationship with Previous RFCs

- **RFC-25 — Single-Source Required-Sections**: una vez que el runner parsea contratos para `required_sections`, leer `enforcement` del mismo parseo es incremental; esta RFC asume RFC-25 aplicada o co-aplicada.
- **RFC-27 — Hook-Based Enforcement**: los checks semánticos mecánicos agrandan la superficie `[machine]` que los hooks pueden gatear sin LLM.
- **RFC-18 — Failure & Recovery Taxonomy**: los nuevos FAILs son F5 (harness) con razón explícita; sin clases nuevas.

---

# Rationale

Se eligió declaración binaria `gated`/`informational` sobre niveles graduados (warn-only, soft-gate) por la misma razón que RFC-24 elige cable-or-kill: los estados intermedios son donde la ambigüedad se acumula. Se eligieron citation resolution y test evidence como primera capa semántica porque son los dos fallos más probables y más baratos de verificar mecánicamente — y porque ya existe un precedente funcionando (`check_plan_citations.py`) que prueba la viabilidad sin introducir un LLM en el gate.

---

# Future Extensions

- **Más checks semánticos mecánicos:** coherencia de IDs de artefactos entre iteraciones, unicidad de decisiones registradas, freshness de la KB de discovery por TTL.
- **Evidencia de tests estructurada:** un formato de resultados machine-readable que H10 valide directamente, en lugar de buscar evidencia en logs.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Proposal). Declaración `enforcement` obligatoria por contrato, decisión explícita para los 13 sin policy, checks mecánicos de citas y evidencia de tests, invariante de cobertura en la suite. | Análisis crítico de adopción (2026-08-05): 13 de 25 contratos sin policy; validación solo estructural |
