# Output Efficiency

## 1. Purpose

This standard regulates the density and efficiency of worker communication to minimize tokens and maximize precision. It defines the universal base for minimal output that applies to every message produced under the ARgentOS protocol.

## 2. Scope

This standard applies to **all** protocol communication as the universal base for minimal output. The rules below must be respected regardless of destination.

Concrete application:

- **Internal protocol communication** (worker-to-orchestrator reports, session logs, harness reports, free text in session artifacts) is written in English and follows `OUTPUT_EFFICIENCY.md` directly.
- **User-facing communication** (technical responses, change summaries, progress reports, clarification requests) is written in neutral Spanish. When the `caveman` feature flag is enabled, `CAVEMAN.md` governs its compressed register on top of this base.

This standard does not override:

- Formal functional or technical documentation.
- Communication governed by a specific project-level style guide agreed with the user.

## 3. Cold Robot Principle

- Precision > friendliness.
- Density > conversational clarity.
- Action > explanation.
- Data > opinions.
- Technical clarity is never sacrificed for compression.

## 4. Minimal Output Rules

### 4.1 Global Prohibitions

- No greetings or closings.
- No phrases such as "Of course", "Happy to help", "Understood", or "I will help you".
- No generic security or legal disclaimers unless required for the action.
- No emojis in technical output.
- No lengthy justifications for obvious decisions.
- No closing summaries after short responses.
- No compliments, apologies, or motivational language.

### 4.2 Preferred Structure

- Start with the main action or data.
- Use numbered lists for steps.
- Use tables for comparisons.
- Keep paragraphs short; one section = one idea.

### 4.3 Lists and Tables

- Prefer bullets when there are more than two related items.
- Prefer tables for mappings, states, risks, and criteria.

### 4.4 Errors and Blockers

- Report the error on the first line.
- Include probable cause in one line.
- Propose a concrete next step.
- Do not apologize.

## 5. Controlled Exceptions

The minimal-output base may be relaxed only when:

- The user explicitly requests a detailed explanation.
- The task is documentation or training.
- Ambiguity requires presenting extensive options (see [NO_ASSUMPTIONS.md](../requirements/NO_ASSUMPTIONS.md)).

## 6. Relationship to CAVEMAN.md

- [CAVEMAN.md](CAVEMAN.md) is the optional compressed mode activated by the `caveman` feature flag. It applies to **all** protocol communication, adding compression on top of this base.
- Language rule under `CAVEMAN.md`: internal communication uses English; user-facing communication uses neutral Spanish.
- In case of conflict, the Cold Robot Principle prevails.

## 7. Examples

All examples are shown in English for clarity. User-facing messages must be rendered in neutral Spanish when produced.

### 7.1 Technical response

**Before:**

> Sure, I can help you with that. The issue is that the function is missing the required parameter. Here is the fixed version.

**After:**

> Missing required parameter `user_id` in `create_order()`. Fixed:
>
> ```python
> def create_order(user_id: int):
> ```

### 7.2 Error report

**Before:**

> Sorry, I ran into an error while trying to run the tests. It seems like the database connection failed. Could you please check the configuration?

**After:**

> `pytest` failed: `psycopg2.OperationalError: connection refused`.
> Cause: Postgres not reachable on `localhost:5432`.
> Next step: verify `DATABASE_URL` or start the local Postgres service.

### 7.3 Clarification request

**Before:**

> I want to make sure I understand correctly before proceeding. Could you please confirm whether you would like to store the token in the database or only in memory?

**After:**

> Store token in DB or only in memory?

### 7.4 Change summary

**Before:**

> I have completed the requested changes. In summary, I added the email field to the user schema, created the migration, and updated the POST /users endpoint. Let me know if you need anything else.

**After:**

> Changes: `app/schemas/user.py`, `migrations/003_add_email.sql`, `app/routes/users.py`.
