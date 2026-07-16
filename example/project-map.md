# Mapa del Proyecto - PayBack Microservice

Este mapa resume el repositorio para usarlo como fuente rápida de contexto. El proyecto es una API backend Flask; no tiene vistas frontend. Los HTML en `src/templates/` son exclusivamente plantillas de email.

## Carpetas principales

| Ruta | Responsabilidad |
|---|---|
| `src/app.py` | Crea la app Flask, configura settings, logging, middlewares, DB y blueprints. |
| `src/settings/` | Configuración Pydantic por ambiente y `db = SQLAlchemy()`. |
| `src/middleware/` | Content-Type, request logging, error handler y Sentry. |
| `src/apps/preorder/` | Dominio principal: preorders, CPE, selección de método, emails, centralizador. |
| `src/apps/payment/` | Endpoints de sincronización/cancelación de pagos. |
| `src/apps/callback/` | Callbacks de proveedores externos. |
| `src/apps/api/` | Conciliaciones, centralizer, chatbot debts. |
| `src/apps/application/` | Aplicaciones cliente, settings y API keys. |
| `src/apps/common/` | Health, logs privados, jobs, helpers, tracing. |
| `src/apps/company/` | Empresas. |
| `src/apps/channel/` | Canales y relación canal-método. |
| `src/apps/pgp/` | CLI para PGP/GPG. |
| `src/templates/` | Emails: éxito, reversa, CRM, error CRM. |
| `command/` | Scripts shell para cron y ejecución local. |
| `install/` | Requirements, crontab y Apache vhost. |

## Archivos clave

| Archivo | Rol |
|---|---|
| `src/app.py` | Application factory `create_app()`. |
| `wsgi.py` | Entrada WSGI para Apache/mod_wsgi. |
| `src/settings/base.py` | Variables, defaults, validators, URI DB. |
| `src/settings/__init__.py` | Carga `.env` y selecciona settings por `FLASK_ENV`. |
| `src/apps/common/utils/generic.py` | `make_response`, UUID/API key helpers, sanitización. |
| `src/apps/common/helpers/logger.py` | Logging, correlation IDs, formatters. |
| `src/apps/common/payment_registry.py` | Carga de configuración de medios desde DB. |
| `src/apps/preorder/services/preorder_service.py` | Orquestación principal SAAS. |
| `src/apps/preorder/services/chatbot_service.py` | Orquestación REC/chatbot. |
| `src/apps/callback/services/payment_closure.py` | Cierre exitoso, cancelación total/parcial. |
| `src/apps/preorder/services/email_service.py` | Render y envío de emails. |

## Endpoints principales

Total detectado por lectura estática: 43 reglas HTTP incluyendo `/favicon.ico`.

| Grupo | Endpoints |
|---|---|
| Health | `GET /`, `/alive`, `/health`. |
| Preorder | `POST /api/v1/preorder`, `POST /api/v1/preorder/create`, `POST /api/v1/preorder/chatbot`, `GET/PUT /api/v1/preorder/<preorder_uuid>`, `GET/PUT /api/v1/preorder/update/<preorder_uuid>`. |
| Status | `GET /api/v1/preorder/status/<uuid>`. |
| Payment sync | `POST /api/v1/pay/sync/pcinet/<uuid>`, `POST /api/v1/pay/sync/qrlink/<uuid>`, `POST /api/v1/cancel/qrlink/<uuid>`. |
| Callbacks | `POST /api/v1/callback/hbb/<cpe>`, `/hbl/<cpe>`, `/pcinet/<cpe>`, `/qr/link/<cpe>`, `/rxt/bind/<cpe>`. |
| Conciliación | `GET /api/v1/centralizer`, `/centralizer/fiserv`, `/fiserv/file`, `/homebanking`, `/homebanking/file`, `/qr_link`, `/qr_link/file`, `/bind_rxt`, `/bind_rxt/file`, `/liq_bind_rxt`, `/liq_bind_rxt/file`. |
| Chatbot | `POST /api/v1/chatbot/debts`. |
| Application/company | `GET /api/v1/get_api_key`, `GET /api/v1/application/<api_key>`, `GET /api/v1/company`. |
| Privados JSON/logs | `GET /api/v1/json/jobs`, `/json/application`, `/json/application/list`, `/json/centralizer`, `/json/centralizer/details`, `/json/preorder`. |

## Modelos principales

| Modelo | Tabla | Relación funcional |
|---|---|---|
| `Application` | `applications` | App cliente, API key, callbacks, límites, config de cuotas. |
| `Company` | `companies` | Empresa dueña de aplicaciones. |
| `PayMethod` | `pay_methods` | Medio de pago. |
| `ApplicationPayMethod` | `applications_pay_methods` | Métodos habilitados por app. |
| `ApplicationSettings` | `applications_settings` | Rango de monto/horario y extras por app+método. |
| `Channel`, `ChannelPayMethod` | `channels`, `channels_pay_methods` | Canales disponibles por método. |
| `Preorder` | `preorders` | Orden de pago, CPE y `data_pay` JSON. |
| `PreorderStatus` | `preorder_status` | Estado actual/histórico de una preorder. |
| `Status` | `status` | Catálogo de estados. |
| `ElectronicCode` | `electronic_codes` | Persistencia de CPE generado. |
| `Centralizer`, `CentralizerDetails` | `centralizers`, `centralizer_details` | Consolidación y conciliación. |
| `JobsNotificationPay` | `jobs` | Jobs de webhook/notificación. |
| `Parameters` | `parameters` | Parámetros generales. |
| `FiservTax` | `fiserv_tax` | Tasas/coefs para cuotas PCINET/Fiserv. |

## Flujos principales

### Crear preorder SAAS

`PreorderView.post` -> `PreorderService.create_preorder` -> `PreorderValidator` -> `ApplicationService` -> `ElectronicCodeService` -> `Preorder`/`PreorderStatus` -> job webhook -> response UUID/URL.

### Crear preorder REC

`ChatbotView.post` -> `ChatbotService.create_preorder` -> `ChatbotCreateRequest` -> `ApplicationService` -> `RecAPI` -> `ElectronicCodeService.validate_and_generate_rec` -> DB -> response UUID/URL.

### Elegir medio de pago

`PreorderDetailView.put` -> `PreorderService.update_preorder` -> valida estado/método/horario -> crea attempt -> routea provider (`PcinetService`, `HbbService`, `HblService`, `HbService`, `QrLinkService`, `RxtService`) -> guarda `data_pay` -> status `proceso`.

### Cierre por callback/sync

Callback provider o sync payment -> carga `PreorderStatus` -> consulta provider -> `preorder.pay_saas()` -> `PaymentClosureService.complete/cancel_full/cancel_partial` -> actualiza status/data_pay -> webhook/email/CRM.

### Emails

`PreorderStatus.send_email` -> `Preorder.send_email_ticket` -> `PreorderEmailService` -> template Jinja de email transaccional -> `EnvialoSimpleAPI.send`.

Templates de email disponibles:

| Template | Caso funcional |
|---|---|
| `src/templates/comprobante_finalizado.html` | Pago exitoso con o sin carrito. |
| `src/templates/comprobante_cancelado.html` | Reversa/devolución. |
| `src/templates/comprobante_cancelado_crm.html` | Error con caso CRM creado. |
| `src/templates/comprobante_cancelado_crm_error.html` | Error sin caso CRM creado. |
| `src/templates/comprobante_parcial.html` | Pago parcial con devolución procesada. |
| `src/templates/comprobante_parcial_crm.html` | Pago parcial con caso CRM creado. |
| `src/templates/comprobante_parcial_crm_error.html` | Pago parcial sin devolución ni caso CRM creado. |

Las plantillas son HTML emails con CSS inline y tablas `role="presentation"`. Comparten los parciales Jinja `_comprobante_base.html` y `_comprobante_partial_details.html`. Requieren assets de contexto `email_logo`, `email_body_ok`, `email_body_error` y `email_body_warning`; los aliases `image_header`/`image_body` se mantienen para compatibilidad. `payment_summary` contiene solo los campos disponibles del webhook y `has_cart` permite reutilizar el template finalizado. Los links de comprobante se normalizan con `src/apps/preorder/utils/email_links.py` para incluir `noredir=1`.

### PGP

Cron `0003_encrypt_emails.sh` -> Flask CLI `pgp encrypt_emails` -> extrae emails del mes anterior -> CSV claro en `tmp` -> keyring temporal -> cifra con clave pública cliente -> `.csv.pgp` en `conciliate`.

## Integraciones externas

| Provider | Archivo |
|---|---|
| SAAS | `src/apps/preorder/providers/api_saas.py` |
| REC | `src/apps/preorder/providers/api_rec.py` |
| PCINET/Fiserv | `src/apps/preorder/providers/api_pcinet.py` |
| HBB | `src/apps/preorder/providers/api_hbb.py` |
| HBL | `src/apps/preorder/providers/api_hbl.py` |
| QR Link | `src/apps/preorder/providers/api_qr_link.py` |
| RXt Bind | `src/apps/preorder/providers/api_rxt_bind.py` |
| CRM 365 | `src/apps/preorder/providers/api_crm.py` |
| EnvialoSimple | `src/apps/preorder/providers/api_envialosimple.py` |
| Webhook cliente | `src/apps/preorder/providers/api_webhook.py` |

## Riesgos principales para tener presentes

- Sentry no queda conectado a settings por falta de `app.config["SENTRY"]`.
- Providers legacy sin timeout efectivo.
- Endpoints privados JSON/logs sin autenticación visible en código.
- Sin migraciones ni suite de tests visible.
- Modelo `Preorder` contiene lógica de integración/email/CRM.
- HTML injection en comprobantes mitigado: el ticket SAAS se renderiza escapado por Jinja y el HTML parcial fue migrado a templates.
- `PaySyncQrLink.post()` puede no retornar respuesta si QR recurrente está aprobado.
