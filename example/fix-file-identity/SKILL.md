---
name: fix-file-identity
description: Inspect Python files in the working tree (via git status/diff or explicit paths) and add a first-line file path comment (`# apps/path/to/file.py`) to files that are missing it. Use when the user wants to fix missing file identity comments, after running a linter/validator that flagged missing paths, or when onboarding files to a codebase that requires first-line path comments. Never executes git commit or git push.
---

# Fix File Identity

Ensure every relevant Python file starts with a comment containing its relative path from `src/` (e.g., `"""apps/bind/views/transaction_view.py"""`). Never execute `git commit`, `git push`, or any git mutation.

## Procedure

1. **Discover target files**
   - If the user provides explicit paths, use those.
   - Otherwise, run `git status --short` and `git diff --name-only` to find modified/untracked `.py` files.
   - Skip `__init__.py`, test files (`tests/`), and migration files (`migrations/`).

2. **Check first line**
   For each file, read the first line. Accept as valid if it contains any of:
   - A `#` comment with `apps/`, `src/`, or `.py`
   - A `\"\"\"` or `'''` docstring with `apps/`, `src/`, or `.py`

3. **Compute expected path**
   - Relative to `src/`: `apps/<domain>/<layer>/file_name.py`.
   - If the file is under `src/` but the relative path starts with `apps/`, use that directly.
   - Example: `src/apps/bind/views/transaction_view.py` → `"""apps/bind/views/transaction_view.py"""`.

4. **Insert path comment**
   If the first line is not valid, prepend a new first line:

   ```python
   """apps/bind/views/transaction_view.py"""
   ```

   Followed by a blank line, then the original content.

5. **Report changes**
   List every file modified. If no files needed changes, say so.

## Constraints

- Only modify `.py` files.
- Do not overwrite an existing valid first line.
- Do not modify binary or non-Python files.
- Do not execute `git commit`, `git commit --amend`, `git push`, `git rebase`, or any other git mutation.
- Do not stage or unstage files.

## Example

Before:

```python
import os

class TransactionView(MethodView):
    ...
```

After:

```python
"""apps/bind/views/transaction_view.py"""
import os

class TransactionView(MethodView):
    ...
```
