# RFC-55 — Source containment: protocol payload in `protocol/`

**Status:** Accepted (2026-08-12, autorización explícita del usuario).

**Pregunta que responde:** ¿cómo se desarrolla ARgentOS sin que el propio
protocolo gobierne las sesiones de desarrollo del repositorio fuente?

## Problema

El repo fuente tiene `AGENTS.md` y `.agents/` en la raíz. Cualquier agente que
entra a desarrollar ARgentOS auto-descubre `AGENTS.md` y queda gobernado por el
protocolo que está construyendo (recursión). El repositorio fuente debe ser un
workspace de desarrollo con sus propias reglas; el protocolo debe quedar
contenido como data.

## Modelo

1. **Contención en `protocol/`:** el payload del producto vive en
   `protocol/.agents/` + `protocol/_AGENTS.md`. El archivo de entrada se
   renombra con guion bajo inicial para que no entre en la cadena de
   auto-descubrimiento de instrucciones del agente (la cadena por defecto es
   `AGENTS.override.md` → `AGENTS.md` → fallback names).
2. **Data, no instrucciones:** todo lo que vive en `protocol/` se interpreta
   como contenido para leer y editar; nunca como directivas de la sesión de
   desarrollo. El `AGENTS.md` raíz (dev) declara esta regla.
3. **`dist` no cambia:** la rama `dist` sigue publicando `.agents/` +
   `AGENTS.md` en la raíz del proyecto adoptante; el workflow copia
   `protocol/.agents` y `protocol/_AGENTS.md` y renombra el entry file al
   publicar. La adopción y el auto-descubrimiento en el adoptante quedan
   intactos.
4. **Links rotos intencionales:** los links relativos dentro del payload que
   apuntan a `AGENTS.md` quedan rotos en el árbol fuente y correctos en `dist`;
   se documentan en `dev/source-layout.md` y se protegen con un mapeo en el
   checker (entry file → `protocol/_AGENTS.md`).
5. **Workspace dev consolidado:** `dev/` gana índice (`dev/README.md`),
   roadmap (`dev/ROADMAP.md`) y la doc de layout (`dev/source-layout.md`); su
   cobertura se cataloga contra `plans/INDEX.md` sin implementar ítems nuevos
   en esta RFC.

## Alcance

- Cambios de layout del repo fuente, tooling dev, CI y documentación raíz.
- El contenido del payload distribuido no cambia semánticamente: misma data,
  entry file renombrado solo en fuente.
- Fuera de alcance: cambios de modelo del protocolo, nuevas políticas,
  implementación del roadmap de `dev/` (se cataloga, no se ejecuta).

## Amendment Log

- 2026-08-12 — RFC creada y aceptada con autorización explícita del usuario
  para ejecutar el plan 54 completo.
