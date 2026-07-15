# EARS — Easy Approach to Requirements Syntax

## Purpose

This document defines the standard for writing acceptance criteria in `.agents` task specifications.

EARS reduces ambiguity by enforcing a small set of sentence patterns. Each acceptance criterion must be atomic, unambiguous, and verifiable.

## Patterns

### 1. Ubiquitous requirement

Used when the system must always behave in a certain way.

```text
The <system name> shall <system response>
```

Example:

```text
The API shall return HTTP 201 when a user is created successfully.
```

### 2. Event-driven requirement

Used when a specific event triggers the response.

```text
When <event>, the <system name> shall <system response>
```

Example:

```text
When a POST request is sent to /users with an empty name, the API shall return HTTP 400.
```

### 3. State-driven requirement

Used while the system is in a particular state.

```text
While <state>, the <system name> shall <system response>
```

Example:

```text
While the database is unavailable, the API shall return HTTP 503.
```

### 4. Unwanted behavior

Used to define behavior in error or edge conditions.

```text
If <optional pre-condition>, then the <system name> shall <system response>
```

Example:

```text
If a user ID does not exist, then the API shall return HTTP 404.
```

### 5. Optional feature

Used when a requirement applies only if a feature is present.

```text
Where <feature>, the <system name> shall <system response>
```

Example:

```text
Where email validation is enabled, the API shall reject malformed email addresses.
```

## Writing rules

1. **One criterion per bullet**: do not combine multiple requirements with "and" or "or".
2. **Use "shall"**: avoid "should", "must", "will", or "may".
3. **Avoid negations**: write what the system shall do, not what it shall not do.
4. **Be specific**: include concrete inputs, outputs, HTTP codes, file names, or behaviors.
5. **Make it verifiable**: a test or inspection must be able to confirm the criterion.

## Examples for this project

Acceptable:

```text
- The API shall reject a POST /users request with a name longer than 100 characters.
- When the email is already registered, the API shall return HTTP 409.
- If the user ID is not a number, then the API shall return HTTP 400.
```

Not acceptable:

```text
- The API should handle errors gracefully.              (ambiguous)
- The API shall validate input and return errors.        (compound)
- Users can't create accounts with bad data.             (negative + informal)
```

## Validation

The harness policy H01 validates that every acceptance criterion follows one of the EARS patterns above.
