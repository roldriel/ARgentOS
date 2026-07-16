# Domain Cheatsheet — Flujo de Preorder

> Resumen ejecutivo del dominio para documentación funcional. Extraído de `_common/DOMAIN_OVERVIEW.md`.

## Estados Válidos de Preorder

1. `Instanciado`
2. `Proceso`
3. `Finalizado`
4. `Cancelado`
5. `Vencido`

## Transiciones Permitidas

```
Instanciado → Proceso
Instanciado → Vencido

Proceso → Finalizado
Proceso → Cancelado
Proceso → Vencido

Vencido → Finalizado   (callback OK + barra cobrada)
Vencido → Cancelado    (callback OK + barra no cobrable)
```

## Reglas de Negocio Clave

| Regla | Valor / Condición |
|-------|-------------------|
| Horario operativo | 06:00 - 23:45 |
| Monto mínimo global | ARS 9 |
| Monto máximo global | ARS 1.000.000 |
| Preorder por barra | Actualmente una única barra por preorder |
| Vencimiento | Respeta fecha de vencimiento de la barra, pero solo operable en horario diario |
| Medios de pago | Al menos uno habilitado por aplicación |
| Callbacks tardíos | Siempre se intenta cobrar la barra, aunque la preorder esté vencida |

## Invariantes Globales

- UUID inmutable
- CPE (Código de Pago Electrónico) inmutable
- Código de barras inmutable
- Monto inmutable
- Aplicación inmutable

## Webhooks al Cliente Integrador

Se notifican los estados:
- `Instanciado`
- `Finalizado`
- `Cancelado`
- `Vencido`
