# Plan 70 — Bloque 1 de la auditoría de sistema 3.1 (coherencia de contratos)

**Status:** Executed
**Fecha:** 2026-08-16
**RFC:** —
**Clase:** B (vía plan; adición compatible al contrato de verificación y
alineación de metadata de salidas de discovery; el ítem 9 es tooling del repo,
sin clase)
**Depende de:** plan 69
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 1, ítems 7–9); autorizado por instrucción directa del usuario el
2026-08-16 (continuar con el bloque 1).

## Objetivo

Cerrar la coherencia de contratos de la auditoría de sistema 3.1:

7. **H06 vs contrato de verificación:** el ítem 7 del Gate Checklist de H06
   exige un campo `evidence` en `[[test_results]]` que el contrato de
   `VERIFICATION_REPORT.md` no define. Se agrega el campo (opcional, con
   semántica de evidencia) y se reformula el checklist para que verifique el
   campo cuando está declarado, manteniendo el fallback de `SESSION_LOG.md`.
8. **Metadata de salidas de discovery:** las listas `output_artifacts` de los
   workflows (y sus espejos en la taxonomía) son parciales y usan nombres de
   contrato en lugar de los paths reales de la KB (`ENVIRONMENT_DISCOVERY.md`
   vs `environment.md`; `DEVELOPMENT_PATTERNS.md` vs
   `development_patterns.md`; listas incompletas para stack/framework/
   business/merge). Se alinea todo con los paths reales declarados por la
   state machine y los cuerpos de los workflows, y se documenta la convención
   de naming en el contrato base de entradas de KB.
9. **Checker de coherencia taxonómica:** se extiende
   `tools/check_taxonomy_coherence.py` para comparar los "Required Output
   Artifacts" de las state machines contra los `output_artifacts` de los
   workflows (bidireccional), con tests.

## Criterio de entrada

- [ ] Plan 69 `Executed` y `dev` con batería en verde.
- [ ] Batería canónica en verde antes de tocar archivos
      (`docs/VERSIONING.md` §4.1).

## Entregables

1. `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` —
   campo `evidence` opcional en `[[test_results]]` con semántica definida.
2. `protocol/.agents/orchestrators/core/harness/policies/H06-verification-report.md`
   — ítem 7 del Gate Checklist alineado con el contrato.
3. `protocol/.agents/orchestrators/discovery/workflow/01-discovery-env.md`,
   `02-discovery-stack.md`, `03-discovery-framework.md`,
   `04-discovery-patterns.md`, `05-discovery-business.md`,
   `06-discovery-merge.md` — `output_artifacts` completos con los paths reales.
4. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — entidades de
   estado y de workflow de discovery alineadas (incluye corrección de
   `discovery:DISCOVERY_INIT.artifacts_output`, que listaba
   `KB_DISCOVERY_ENTRY.md` erróneamente).
5. `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`
   — nota de convención de naming (contrato por entrada vs archivo de KB).
6. `tools/check_taxonomy_coherence.py` + `tests/test_check_taxonomy_coherence.py`
   — chequeo bidireccional de salidas de state machines vs workflows.
7. `CHANGELOG.md` `[3.21.0]`, `protocol/.agents/VERSION` 3.21.0, INDEX
   actualizado.

## Pasos

1. Extender `tools/check_taxonomy_coherence.py` con el chequeo de salidas
   (parsear "Required Output Artifacts" de cada state machine y comparar
   basenames contra los `output_artifacts` del workflow mapeado).
2. Agregar tests del nuevo chequeo en `tests/test_check_taxonomy_coherence.py`.
3. Correr el checker nuevo sobre el payload actual y registrar los
   mismatches de discovery como evidencia.
4. Alinear front matters de los workflows de discovery (01–06) y las
   entidades de estado y workflow de la taxonomía.
5. Agregar el campo `evidence` al contrato de `VERIFICATION_REPORT.md` y
   reformular el ítem 7 de H06.
6. Documentar la convención de naming en `KB_DISCOVERY_ENTRY.md`.
7. Cerrar el plan: `Executed` con `Nota de ejecución`, INDEX, changelog
   `[3.21.0]`, `VERSION` 3.21.0.

## Criterios de salida

- [ ] `check_taxonomy_coherence.py` verde (incluido el chequeo nuevo).
- [ ] `check_protocol_invariants`, `check_plan_citations`,
      `check_plan_structure`, `check_session_artifacts` verdes.
- [ ] `python -m pytest tests/` verde (145 + tests nuevos).
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
```

## Riesgos

- Medio: el chequeo nuevo puede producir falsos positivos si la normalización
  de basenames (prefijos `<order>`/`D<order>`/numéricos, paths de `.project/`)
  no cubre algún formato. Mitigación: normalización conservadora + tests de
  los tres formatos (core, discovery con `D<order>-`, `.discovery_manifest`).
- Bajo: el campo `evidence` es opcional y compatible; no rompe artefactos
  existentes.

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 1, ítems 7–9) → este plan → ítems
del changelog `[3.21.0]` → commit atómico en `dev`.

## Nota de ejecución

2026-08-16: ejecutado en `dev`. Batería canónica en verde: invariantes (8.412
referencias), citas, estructura de planes, coherencia taxonómica (el chequeo
nuevo detectó 21 mismatches de discovery en el payload previo y quedó en verde
tras la alineación), artefactos de sesión, versiones (warnings de dev
esperados) y 148 tests de desarrollo (145 + 3 nuevos). Changelog `[3.21.0]` y
`protocol/.agents/VERSION` bumped; INDEX actualizado. Commit atómico en `dev`.
