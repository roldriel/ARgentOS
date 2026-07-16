# Execution Contexts

> Extracted from operational instructions. Correct execution context identification is mandatory.

## 1. Flask CLI / Command Context

Applies only to Flask CLI commands.

Rules:

* Use `click.echo` for console output
* Format user-facing messages with `log_message` (or `cli_echo` where applicable)
* Do NOT use `current_app.logger` for CLI output

CLI output is for terminal interaction, not application logging.

## 2. Application Runtime Context

Applies to views, services, providers, validators, models, and runtime logic.

Rules:

* Use `current_app.logger` (or appropriate application logger)
* Use `log_message` only as a formatter inside logger calls
* Do NOT use `click.echo`

## 3. Exception Logging (Runtime)

* Use `logger.exception()` when logging exceptions
* Preserve full stack traces
* Do NOT suppress or replace exception context
