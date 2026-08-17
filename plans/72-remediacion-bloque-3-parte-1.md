# Plan 72 — Bloque 3 de la auditoría de sistema 3.1, parte 1 (ítems 15, 17, 18)

**Status:** Executed
**Fecha:** 2026-08-16
**RFC:** —
**Clase:** B (vía plan; el ítem 15 alinea el validador con el contrato y la
policy H06 ya declarados; el ítem 17 define el registro de desviaciones
documentadas; el ítem 18 es tooling del repo, sin clase)
**Depende de:** plan 71
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 3, ítems 15, 17 y 18); autorizado por instrucción directa del usuario
el 2026-08-16 (continuar con el bloque 3). Los ítems 13, 14 y 16 (Clase A,
modelo conceptual) se resuelven en RFCs + planes posteriores.

## Objetivo

Avanzar el bloque 3 de la auditoría de sistema 3.1 con los tres ítems
implementables sin cambio de modelo:

15. **Evidencia determinista de tests en H06:** `gate_validator.py` valida el
    bloque `[[test_results]]` de `VERIFICATION_REPORT.md`: resultados no
    `SKIPPED` deben tener `evidence` que resuelva a un archivo existente o el
    comando `test` presente en `SESSION_LOG.md` (semántica declarada por el
    contrato en 3.21.0 y por H06 ítem 7). Sin bloque `[[test_results]]` el
    chequeo es SKIP (compatible con artefactos previos).
17. **Semántica de "desviación documentada":** se define en el contrato de
    `HARNESS_REPORT.md` el registro obligatorio de la desviación (objeto
    `deviation` con `cause` y `evidence` en el ENTRY) como única vía para que
    un FAIL estructural se registre como PASS, y en `harness/INDEX.md` su
    regla (nunca silenciosa, no afecta el fail-open de los hooks, auditable
    post-hoc). `check_session_artifacts.py` valida la forma del objeto.
18. **Auditoría post-hoc de gates:** nuevo tool dev-only
    `tools/audit_gates.py` que recomputa el subconjunto estructural de los
    PASS registrados en `HARNESS_REPORT.md` invocando el validador del
    producto como subproceso, y reporta PASS registrados que el validador
    rechaza sin desviación registrada.

## Criterio de entrada

- [ ] Plan 71 `Executed` y `dev` con batería en verde.
- [ ] Batería canónica en verde antes de tocar archivos
      (`docs/VERSIONING.md` §4.1).

## Entregables

1. `protocol/.agents/harness/gate_validator.py` — chequeo `test_results` en
   H06 (con resolución de `evidence` y fallback a `SESSION_LOG.md`), con
   tests de producto.
2. `protocol/.agents/contracts/HARNESS_REPORT.md` — sección "Documented
   deviations" + campo opcional `deviation` en el ENTRY.
3. `protocol/.agents/harness/INDEX.md` — regla de desviaciones documentadas
   en §Enforcement model.
4. `tools/check_session_artifacts.py` + `tests/test_check_session_artifacts.py`
   — validación de la forma de `deviation` en los ENTRY.
5. `tools/audit_gates.py` + `tests/test_audit_gates.py` — auditoría post-hoc
   de gates.
6. `CHANGELOG.md` `[3.23.0]`, `protocol/.agents/VERSION` 3.23.0, INDEX
   actualizado.

## Pasos

1. Agregar el chequeo `test_results` al validador H06 (solo cuando el bloque
   TOML existe; SKIP si no) y sus tests de producto.
2. Definir el registro de desviaciones en `HARNESS_REPORT.md` (sección +
   campo `deviation` del ENTRY) y la regla en `harness/INDEX.md`.
3. Validar la forma de `deviation` en `check_session_artifacts.py` con tests.
4. Implementar `tools/audit_gates.py` (subproceso al validador, comparación
   con los ENTRY, soporte de desviaciones registradas) y sus tests.
5. Cerrar el plan: `Executed` con `Nota de ejecución`, INDEX, changelog
   `[3.23.0]`, `VERSION` 3.23.0.

## Criterios de salida

- [ ] Validador H06 con los tests nuevos en verde (producto).
- [ ] `check_session_artifacts` con los tests nuevos en verde.
- [ ] `audit_gates.py` con los tests nuevos en verde.
- [ ] Batería canónica de `docs/VERSIONING.md` §4.1 en verde.
- [ ] Plan `Executed` con `Nota de ejecución`, INDEX, changelog y `VERSION`
      actualizados.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
```

## Riesgos

- Medio (15): el chequeo exige evidencia o `SESSION_LOG.md` para resultados no
  `SKIPPED`; es fail-conservador y solo se activa cuando el bloque
  `[[test_results]]` existe, para no romper artefactos previos sin el bloque.
- Bajo (17): el campo `deviation` es opcional y compatible con el schema de
  ENTRY existente.
- Bajo (18): el tool es dev-only; los tests no dependen del payload (el
  subproceso se mockea).

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 3, ítems 15/17/18) → este plan →
ítems del changelog `[3.23.0]` → commit atómico en `dev`. Los ítems 13, 14 y
16 quedan para RFCs + planes de la parte 2 del bloque.

## Nota de ejecución

2026-08-16: ejecutado en `dev`. Batería canónica en verde (invariantes con
8.442 referencias, citas, estructura, coherencia taxonómica, artefactos de
sesión, versiones con warnings de dev esperados); 159 tests de desarrollo (151
+ 8 nuevos: 2 de desviaciones en session artifacts + 6 de audit gates) y 72
tests del harness del producto (67 + 5 de test_results). Changelog `[3.23.0]`
y `protocol/.agents/VERSION` bumped; INDEX actualizado. Commit atómico en
`dev`.
