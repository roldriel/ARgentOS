# ARgentOS (desarrollo) — estado y feedback crítico

> **Histórico (2026-08-15):** este archivo documenta el estado y feedback de
> la auditoría de documentación del 12 ago 2026. Queda como histórico; el
> tracker vivo de remediación de sistema es `AUDITORIA_SISTEMA.md` en la raíz
> del repo (cerrado el 14 ago 2026 y actualizado a medida que la remediación
> avanza).

**Fecha:** 2026-08-14

**Nota:** este archivo reemplaza al informe de auditoría de documentación del
2026-08-12 (disponible en la historia de git). El estado de remediación de esa
auditoría: 10 de 11 puntos cerrados; los parciales 3 (links Markdown genéricos
sin checker, riesgo bajo) y 6 (referencia de RFC-42 en el payload) quedaron
cerrados el 12 ago 2026 (plan 56) — ver abajo.

**Actualización 2026-08-14 (Nivel 1 de remediación, tracker
`AUDITORIA_SISTEMA.md`):**

- La serie RFC-32…54 quedó **toda `Accepted`** (revisión individual vía
  RFC-56, plan 57); ninguna RFC queda en `Proposal`.
- `test_toolcalls.py` quedó desacoplado del payload (usa
  `tests/fixtures/skills/`).
- La batería pasó de 114 a **121 tests** (`python -m pytest tests/`).
- `docs/VERSIONING.md` §9 refleja el estado real de versiones (master 3.6.3,
  dev 3.8.0, dist 3.6.3) y §4.1 define la batería canónica.
- Pendientes de fondo sin cambio: branch protection, harness tests fuera de la
  CI del repo, checker mecánico de coherencia taxonómica (H13).

---

## Cómo funciona ahora

El repo se organiza en tres capas claras: `protocol/` es el producto (data,
intocable sin vía RFC/plan), `tools/` + `runtime/` son la instrumentación y la
implementación de referencia, y `plans/` es la historia de diseño que gobierna
todo cambio. Alrededor gira una batería de verificación (4 checkers + 114
tests) que corre igual en local y en CI. El flujo de trabajo es: RFC/plan
aprobado → ejecución en `dev` → verificación → cierre documental (estados,
changelog, VERSION) → commit atómico → promoción a `master` con tag → `dist`
regenerada por CI.

## Puntos fuertes

- **La gobernanza es real, no aspiracional.** Es el rasgo distintivo del
  proyecto: toda decisión tiene traza (RFC → plan → nota de ejecución →
  changelog), y gran parte es *mecánicamente enforceable* (estructura de
  planes, citas, invariantes del payload, sync de dist). Pocos repos pueden
  decir "la convención la hace cumplir un script".
- **La frontera producto/workspace está limpia.** La disolución de `dev/`
  eliminó la última ambigüedad conceptual: `protocol/` es data, el resto es
  tooling. Un agente nuevo lee un solo AGENTS.md operativo y tiene el mapa
  completo.
- **Dogfooding disciplinado.** El protocolo se usa para desarrollar el
  protocolo, y las fricciones se registran y remedian (la sexta serie entera
  nació de una auditoría).
- **Todo el trabajo de remediación quedó verificado**, no declarado: tests,
  checkers, y los cambios estructurales se hicieron con la batería corriendo
  al final de cada fase.

## Deuda técnica

- ~~**23 RFCs en `Proposal` (RFC-32…54)**~~ **(resuelto 12 ago 2026)**: la
  serie completa se revisó una por una vía RFC-56 (plan 57) y quedó
  `Accepted`; ninguna RFC está en `Proposal` y todos los planes numerados están
  `Executed`.
- ~~**`test_toolcalls.py` acoplado al payload**~~ **(resuelto 14 ago 2026)**:
  el test usa fixtures propias (`tests/fixtures/skills/`); ya no lee skills
  reales del payload y respeta la regla de `tests/AGENTS.md`.
- **El INDEX carga demasiados roles**: índice, backlog, convenciones, snapshot
  de estado, notas de regularización. Funciona, pero es frágil como fuente
  citada por todo el mundo; un día habrá que separar "convenciones" de
  "índice".
- ~~**`feature.md`**~~ **(resuelto 12 ago 2026)**: el documento de visión del
  EC Pipeline se movió a `plans/ec-pipeline-vision.md` con banner de cierre
  (visión completada). Las citas históricas `feature.md` resuelven por mapeo
  legacy en `check_plan_citations.py`; el documento ahora está gobernado y
  escaneado por los checkers.

## Puntos débiles

- **El modelo versión↔plan acopla el versionado del protocolo a la cadencia
  de planes.** Cada plan ejecutado es una versión: funciona, pero versiones
  como 3.0.2–3.0.5 nacieron de regularizaciones, no de cambios de producto.
  El número de versión comunica poco al adoptante.
- **La verificación depende de disciplina de ejecución local.** Los checkers
  corren en CI, pero CI no bloquea nada visible en el flujo actual (no hay
  branch protection mencionada); un push directo a `dev` roto no se entera
  nadie hasta que alguien mira.
- **El punto 6 residual quedó cerrado (12 ago 2026, plan 56)**: la regla de
  inmutabilidad del payload quedó incorporada inline a `ANTI_CIRCUMVENTION.md`
  ("el payload es inmutable dentro de una versión; todo cambio llega por una
  versión publicada"). Por frontera documental el payload no referencia RFCs;
  la regla RFC-42 vive en la documentación del repo (`plans/INDEX.md`
  §Convenciones).
- **Harness sin cobertura en el repo.** Decisión del usuario, respetada, pero
  el costo real es: el código ejecutable del payload (`hook_gate.py`,
  `runner_state.py`) no tiene regresión automática en este repo; sus tests
  solo corren en proyectos adoptantes. Un plan que rompa el harness se
  detecta tarde. El plan 46 agregó el test de integración del flujo enforced al
  payload, pero la CI del repo sigue sin ejecutarlos (pendiente en
  `AUDITORIA_SISTEMA.md` §Remediation Tracker).

## Cabos sueltos

1. ~~Referencia RFC-42 en el payload~~ **(cerrado 12 ago 2026, plan 56)**: regla
   inline en `ANTI_CIRCUMVENTION.md`.
2. Push de `dev` (2 commits locales sin publicar: planes 46 y 47) y eventual
   promoción a `master`.
3. Links Markdown genéricos sin checker (riesgo bajo, decisión consciente).
4. ~~Desacople de `test_toolcalls.py`~~ **(cerrado 14 ago 2026)**: fixtures
   propias en `tests/fixtures/skills/`.
5. ~~Hogar conceptual de los documentos de estado~~ **(cerrado 15 ago 2026)**:
   este archivo queda en `docs/` como histórico (banner arriba); el tracker
   vivo de remediación es `AUDITORIA_SISTEMA.md` en la raíz del repo.

## Feedback crítico

El proyecto tiene un riesgo estructural claro: **la gobernanza escala peor
que el protocolo**. Hay 58 RFCs y 57 planes para un producto que son, en
esencia, documentos Markdown. El aparato (ciclos de status, amendment logs,
citas verificables, checkers) es excelente para sostener calidad, pero cada
cambio chico paga un peaje burocrático alto, y la evidencia está a la vista:
regularizaciones retroactivas repetidas (RFC-24…28, planes 31–36, RFC-32…54
en Proposal permanente). Cuando la gobernanza necesita regularizarse a sí
misma cada dos semanas, la señal es que el proceso pide más ceremonia de la
que el riesgo real justifica. Los checkers ayudan (mecanizan el cumplimiento),
pero la pregunta que el proyecto eventualmente tiene que responder es: ¿qué
cambios del payload realmente necesitan RFC, y cuáles podrían pasar por
fast-track con checker verde? La serie Proposal se destrabó el 12 ago 2026
(RFC-56, plan 57): las 23 RFCs quedaron `Accepted`. El riesgo estructural de
fondo sigue vigente: la ceremonia de gobernanza es alta para un producto
documental, y conviene revisar el peaje de cada cambio chico con la evidencia
de los checkers como vara.
