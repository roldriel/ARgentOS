# Roadmap

Mapa **operativo actual** del trabajo de ARgentOS: qué se ejecuta ahora, qué
sigue, qué requiere autorización y qué es sólo candidato. No duplica el estado
detallado de los planes —eso vive en `docs/plans/INDEX.md`, en los planes y en
las RFCs, que son la fuente de trazabilidad— y no cataloga la historia ya
cerrada.

Los ítems marcados como **payload** tocan `protocol/.agents/` y requieren su
propia autorización (RFC-56) antes de ejecutarse.

## Trabajo activo / dogfood

| Prioridad | Trabajo | Origen | Estado |
| --- | --- | --- | --- |
| Alta | Mechanical D01 subset — DEV checker for discovery output structure and provenance | B-1 derivado · `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` | **Próximo dogfood** |
| Media | EARS structural validator | B-2 derivado · `docs/plans/33-ears-criteria-canonical-form.md` | Siguiente dogfood, después de B-1 |

Ambas entradas son **trabajo derivado nuevo**, no la reapertura de un ítem
histórico. Los problemas originales `B-1` y `B-2` están resueltos; lo que sigue
es una extensión que el propio contrato de D01 declara como futura (la
validación mecánica es hoy inexistente y el contrato la admite como extensión
posible) y la secuencia de dogfood decidida después.

**Criterio de prioridad.** La columna hereda la prioridad del ítem histórico del
que la entrada deriva (`Alta` en `B-1`, `Alta` en `B-2`), salvo que la secuencia
de dogfood fije un orden explícito: el validador EARS se registra `Media` porque
se ejecuta **después** del checker D01. No se recalifica ningún ítem histórico
sin evidencia nueva.

## Pendientes que requieren autorización

Ninguno de estos ítems es implementable de inmediato: los tres afectan contratos
del payload (`protocol/.agents/`) y por lo tanto requieren autorización RFC-56 y
un plan aprobado antes de tocarse.

| Prioridad | Trabajo | Origen | Estado |
| --- | --- | --- | --- |
| Media | Resolver `F-14` y `F-17` de discovery | B-4 residual · `docs/plans/19-anexo-a-bitacora-fricciones.md` | **PENDIENTE — PAYLOAD / REQUIERE AUTORIZACIÓN** (RFC-56) |
| Baja | Incorporar `project_shape` para repositorios documentales/protocolo (`F-16`) | B-7 residual · `docs/plans/19-anexo-a-bitacora-fricciones.md` | **PENDIENTE — PAYLOAD / REQUIERE AUTORIZACIÓN** (RFC-56) |
| Baja | Registrar el session risk de single-instance en métricas | B-8 residual · `protocol/.agents/contracts/METRICS.md` | **PENDIENTE — PAYLOAD / BAJA PRIORIDAD** (requiere cambio de payload) |

- **`B-4` residual.** El ítem histórico `B-4` está resuelto por los planes 37–43,
  53 y 58; lo que sigue abierto son dos fricciones concretas: `F-14` (el manifest
  no puede expresar marcado legacy) y `F-17` (procedencia de `source_files` para
  ausencias y hechos de árbol). Ambas tocan contratos de discovery, es decir el
  payload.
- **`B-7` residual.** El ítem histórico `B-7` está resuelto por los planes 29 y
  52; su residuo real es que `project_shape` no contempla repositorios
  documentales/de protocolo (`F-16`), lo que afecta contratos del payload. **No**
  debe confundirse con la corrección de trazabilidad de `docs/plans/INDEX.md`
  registrada en el Plan 132: son problemas distintos —uno arquitectónico, uno
  documental— y se atienden por vías separadas.
- **`B-8` residual.** El ítem histórico `B-8` está resuelto por el plan 49: el
  modelo de ejecución de delegaciones en runtimes de contexto único **existe**.
  Lo único pendiente es que la mitigación de session risk para single-instance no
  tiene slot ni evento correspondiente en el catálogo de
  `protocol/.agents/contracts/METRICS.md`. Es deuda de payload de baja prioridad,
  no el modelo principal de single-instance.

## Candidatos futuros

| Trabajo | Origen | Estado |
| --- | --- | --- |
| Mechanical checker de `.last_discovery` | B-3 (extensión) · `docs/plans/50-discovery-kb-freshness.md` | **Candidato futuro** — no autorizado, no planificado |

El ítem histórico `B-3` —marcador `.last_discovery` canónico y su validación en
health-check— está resuelto por el plan 50. La extensión mecánica del checker es
una posibilidad declarada, no trabajo comprometido: no se implementa ni se
planifica desde este documento.

## Trazabilidad histórica

> Los ítems históricos B-1…B-8 fueron resueltos como problemas originales. Sus
> planes y RFCs constituyen la trazabilidad histórica en `docs/plans/INDEX.md`.
> Los trabajos derivados posteriores se registran independientemente y no
> reabren esos ítems.

`B-5` (política de clarificación desatendida) y `B-6` (subcomandos del runner
para H15) están completamente resueltos y no requieren ninguna entrada en este
documento. La política de clarificación desatendida queda **disponible como
capacidad** para los dogfoods siguientes, sin trabajo adicional.

## Proceso

1. Cada ítem se toma como par RFC + plan según la gobernanza vigente
   (`docs/CONVENTIONS.md`); los ítems de payload requieren además RFC `Accepted`
   por RFC-56.
2. Los entregables DEV (`tools/`, `runtime/`, `docs/`) no requieren RFC por no
   tocar `protocol/.agents/`; los cambios de código del runtime se verifican con
   la batería canónica y la suite correspondiente.
3. Este documento se actualiza cuando un ítem pasa a plan, se ejecuta o cambia de
   categoría. El estado detallado de cada plan se consulta en
   `docs/plans/INDEX.md`, que es la fuente descriptiva; este Roadmap no lo
   duplica.
