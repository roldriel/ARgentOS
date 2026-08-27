# Plan 50 — Frescura y revalidación de la KB de discovery

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-51 (`plans/rfc/51-discovery-kb-freshness.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 5.3 / 5.4

## Objetivo

Evitar el consumo de entradas de discovery vencidas y canalizar toda revalidación por el pipeline.

## Criterio de entrada

- [ ] RFC-51 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: TTLs en la máquina de discovery, marcadores existentes, entrada `environment.md` vencida.

## Entregables

1. Regla de frescura en `DISCOVERY_STATE_MACHINE.md` y `USING_PATTERNS.md`.
2. Marcador único `.last_discovery` con validación en `PROTOCOL_HEALTH.md`.
3. Procedimiento de limpieza del marcador legado.
4. Registro de la revalidación manual del 11-08 como desviación histórica.

## Pasos

1. Editar `DISCOVERY_STATE_MACHINE.md`: regla de consumo fresco (verificación de TTL antes de delegación que consume la entrada) y marcador único.
2. Editar `USING_PATTERNS.md`: obligación del worker/orquestador de verificar frescura de `environment.md`/`development_patterns.md`.
3. Agregar a `PROTOCOL_HEALTH.md` la validación del marcador `.last_discovery`.
4. Documentar la limpieza del marcador legado (`.project/knowledge/discovery/.last_discovery`).
5. Registrar en `SESSION_LOG.md`/bitácora la revalidación manual del 11-08 como desviación.
6. Actualizar el backlog B-3 y B-4 de `plans/INDEX.md` (resolución de F-12).
7. Ejecutar la verificación documental.

## Criterios de salida

- [ ] La regla de frescura está especificada y es verificable.
- [ ] Un solo marcador canónico.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Auditoría de la KB real: `environment.md` vencida debe quedar marcada y no recomendable hasta re-probe.

## Riesgos

- Bajo: reglas de proceso; requiere una re-probe `env` inicial para sanear la KB actual.

## Trazabilidad

- RFC-51; fricción F-12 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-3, B-4.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-51 Accepted). Regla de frescura agregada a
la máquina de discovery (sección "Freshness Rule": verificación de TTL antes
de delegar, `[entries] stale`, revalidación solo por pipeline) y a
la sección 5 del estándar de uso de patrones; marcador `.project/.last_discovery` declarado único
con el legado deprecado; ítem 10 del health checklist valida el marcador
canónico y proscribe el legado. La revalidación manual del 11-08 queda
registrada como desviación histórica en esta nota (el canal manual queda
proscripto por la regla nueva). Versión 3.6.0. Verificación: invariantes OK,
citas OK, estructura OK, 121 passed.
