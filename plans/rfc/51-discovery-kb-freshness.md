# RFC-51 — Frescura y revalidación de la KB de discovery

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), puntos 5.3 y 5.4
**Pregunta:** ¿Cómo se garantiza que las entradas de la KB de discovery no se consuman vencidas o revalidadas por canales fuera del pipeline?
**Afectados:** `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`, `.agents/orchestrators/discovery/roles/workers/init_worker.md`, `.agents/standards/context/USING_PATTERNS.md`, `.project/knowledge/discovery/`.

## Problema

La KB de discovery puede quedar vencida y aun así consumirse: `environment.md` fue probada el 2026-08-05 con TTL de entorno de 6 horas (`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`) y sigue siendo la entrada activa el 2026-08-11; el estándar `USING_PATTERNS.md` ordena usar el shell y las herramientas que esa entrada declara (`.agents/standards/context/USING_PATTERNS.md:5. Using environment.md to choose shell and tools`). Además, `executive_summary.md` fue "revalidada manualmente" el 11-08 con correcciones de referencias a `runner.py`/`task.py` (`.project/knowledge/discovery/executive_summary.md:Executive Summary`), un canal de mantenimiento que el pipeline de discovery no define. Existen además dos marcadores `.last_discovery`: el canónico en `.project/.last_discovery` y un legado en `.project/knowledge/discovery/.last_discovery` (`plans/19-anexo-a-bitacora-fricciones.md:F-12`).

## Decisión propuesta

1. **Regla de frescura**: antes de delegar una fase que consume `environment.md` o `development_patterns.md`, el Orchestrator verifica la frescura de las entradas contra sus TTL; si expiró, invoca el scope `env` (o el scope correspondiente) antes de la delegación.
2. **Revalidación solo por pipeline**: las entradas de la KB solo se actualizan a través del flujo de discovery (workers); las correcciones manuales se registran como `deviation` y disparan el `init_worker` para revalidación formal. La revalidación manual del 11-08 queda documentada como desviación histórica.
3. **Marcador único**: `.project/.last_discovery` es el único marcador; se agrega su validación al health checklist y un procedimiento de limpieza del marcador legado en `.project/knowledge/discovery/`.
4. Las entradas vencidas se marcan en el manifest (`[entries] stale`) y se excluyen de recomendaciones hasta ser revalidadas.

## Alternativas consideradas

- **Re-probar entorno en cada sesión**: costoso y duplica el propósito del TTL.
- **Prohibir revalidación manual**: sin canal alternativo, una corrección urgente queda bloqueada; la desviación registrada cubre el caso.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `DISCOVERY_STATE_MACHINE.md` | Regla de consumo fresco y marcador único. |
| `USING_PATTERNS.md` | Verificación de frescura antes de aplicar patrones. |
| `PROTOCOL_HEALTH.md` | Validación del marcador `.last_discovery`. |
| `plans/19-anexo-a-bitacora-fricciones.md` | Nota de la desviación histórica (opcional). |

## Criterios de aceptación

- [ ] Ninguna entrada vencida se consume sin revalidación.
- [ ] Toda actualización de KB pasa por el pipeline (o se registra como desviación).
- [ ] Existe un único marcador `.last_discovery`.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, puntos 5.3 / 5.4; F-12 |
