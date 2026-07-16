# Domain Overview: Pay Back Payment Gateway

> Contexto funcional del microservicio `pay_back`.
> Este sistema forma parte de una **pasarela de pagos** implementada en Python con Flask y SQLAlchemy.

## Modelo de Acceso

Desde un backoffice se dan de alta **empresas**.
Cada empresa puede tener una o más **aplicaciones**, y cada aplicación se identifica mediante una **API Key**, utilizada para autenticar las llamadas a la API y aislar los datos entre clientes.

## Concepto de Preorder

Una *preorder* representa una **intención de pago preliminar**, con vencimiento definido, que puede ser utilizada por un cliente final para iniciar un pago dentro de una ventana de tiempo limitada.

La preorder:

* No implica un cobro
* No reserva fondos
* No ejecuta operaciones financieras

Su función es:

* Validar que un pago *podría* realizarse
* Generar un identificador externo reutilizable (CPE)
* Habilitar un acceso (link) al cliente final
* Servir como punto de trazabilidad del flujo completo

## Creación de una Preorder

La preorder se crea mediante una API REST consumida por el cliente integrado.

### Datos del cliente final (pagador)

* Nombre
* Apellido
* Email
* Tipo de documento
* Número de documento
* Género del documento

El sistema **no realiza validaciones regulatorias de identidad (KYC)**.

### Datos del servicio a pagar

* Código de barras del servicio
* Monto informado
* Nombre del servicio
* Descripción del servicio

Actualmente, una preorder admite **un único código de barras**.

## Restricciones Horarias

* **Horario de apertura:** 06:00
* **Horario de cierre:** 23:45

Reglas:

* Las preorders **solo pueden crearse** dentro de ese rango horario.
* Las preorders **solo pueden ser cobradas** dentro de ese mismo rango.
* Si un código de barras tiene una fecha de vencimiento futura:
  * La preorder respeta dicha fecha
  * Pero el pago solo podrá ejecutarse dentro del horario operativo diario

## Restricciones Monetarias

### Globales

* **Monto mínimo global:** ARS 9
* **Monto máximo global:** ARS 1.000.000

### Por Aplicación

Cada aplicación puede definir un monto mínimo y máximo propio, siempre dentro de las bandas globales.

### Por Medio de Pago

Cada medio de pago define su propio rango, que debe estar dentro de las bandas globales y de la aplicación.

Al momento de crear la preorder, **no se selecciona aún el medio de pago**, pero la preorder solo es válida si existe al menos un medio de pago capaz de operar con el monto solicitado.

## Validaciones contra Proveedor Interno

Antes de crear una preorder, el backend consulta a un **proveedor interno**, fuente de verdad absoluta.

Validaciones:

* Que el código de barras sea cobrable
* Que no esté expirado
* Que el monto informado sea válido para esa barra

Si el proveedor indica **NO**, la preorder **no se crea**.

## Generación de Identificadores

Si todas las validaciones son exitosas:

* Se crea una preorder en estado **`Instanciado`**
* Se genera un **UUID interno**
* El proveedor devuelve un **Código de Pago Electrónico (CPE)**
* El UUID y el CPE quedan asociados de forma unívoca

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

## Checkout y Proceso de Pago

Una vez creada la preorder (`Instanciado`), el cliente final accede mediante una URL.
Se muestran los medios de pago habilitados para el monto.

La preorder pasa de `Instanciado` a `Proceso` cuando:

* El cliente final acepta los términos y condiciones
* Presiona el botón de pagar
* El backend recibe la información necesaria para generar la intención de pago

### Intenciones de Pago con Proveedores

* **Síncronas** (tarjeta de débito/crédito, QR): tiempo de vida limitado (~3-5 minutos). Si falla, la preorder no se cancela; el cliente puede reintentar.
* **Asíncronas** (homebanking, transferencia): el cliente sale de la plataforma; el sistema depende de callbacks.

## Reintentos de Pago

Dentro del estado `Proceso`, una preorder puede tener **múltiples intentos de pago**, siempre que no esté en estado terminal ni haya finalizado exitosamente. La preorder **no vuelve** a `Instanciado`.

## Cierre del Pago

La operación se considera completa solo si:

1. El proveedor confirma el pago del medio
2. El sistema cobra la barra usando el CPE

### Pago OK → Finalizado

* Callback OK + cobro de barra exitoso
* Se envía email al cliente final
* Operación irreversible

### Pago Cancelado → Cancelado

Si el pago del medio es OK pero el cobro de barra falla:

1. **Reversa exitosa**: se devuelve el dinero; preorder pasa a `Cancelado`.
2. **Reversa falla, ticket generado**: se genera incidencia; preorder pasa a `Cancelado`.
3. **Reversa y ticketera fallan**: se muestra instrucción de contacto; preorder pasa a `Cancelado`.

### Callbacks Tardíos y Vencimiento

Si se recibe un callback de pago OK cuando la preorder está `Vencido`:

* **Siempre** se intenta cobrar la barra
* Si el cobro es OK → `Finalizado`
* Si el cobro falla → flujo de cancelación → `Cancelado`

El vencimiento bloquea acciones del cliente final, **no** el cierre por callbacks.

## Webhooks al Cliente Integrador

Se notifican vía webhook los siguientes estados:

* `Instanciado`
* `Finalizado`
* `Cancelado`
* `Vencido`

## Invariantes Globales

* UUID inmutable
* CPE inmutable
* Código de barras inmutable
* Monto inmutable
* Aplicación inmutable

La preorder **no se edita**, solo cambia de estado.

## Regla Crítica de Dominio

> El estado `Vencido` invalida acciones del cliente final, pero no invalida el procesamiento de dinero ya cobrado.

## Advertencia para Agentes

Este sistema **no es un CRUD** ni un flujo lineal simple.
Si una implementación omite validaciones, altera el orden de reglas o permite transiciones no definidas, el sistema queda **lógicamente inconsistente**, aunque compile y funcione.
