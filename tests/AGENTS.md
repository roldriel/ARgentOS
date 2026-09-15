# tests/ — Development test suites

This directory centralizes the test suites for the repository's development
tooling (`tools/`, `runtime/`). Tests here validate **repo tooling code**,
never the product payload.

## Rules

- **Do not depend on `protocol/`.** The payload is data, not dev code. Tests
  must be self-contained: build fake repos/payloads in `tmp_path` or vendor
  minimal fixtures under `tests/fixtures/`. A change in the payload (a renamed
  skill, a moved document) must never break a test here.
- **Harness tests are not part of the canonical battery.**
  `protocol/.agents/harness/tests/` belongs to the product: it ships with
  `dist`, runs in adopting projects, and is executed in the CI regression job
  (`.github/workflows/check-protocol.yml`) so payload code regressions are
  caught in this repository.
- **Never write temporaries inside the repository.** `tests/pytest_isolation.py`
  defines the single repository-external temporary root of a session (system
  temp + `argentos-pytest`, overridable with `ARGENTOS_PYTEST_TMP`); the root
  `conftest.py` points pytest's basetemp, cache and scratch there. Use
  `tmp_path`/`tmpdir` for files, and `pytest_isolation.scratch_root(<suite>)`
  for throw-away repositories a test builds itself — never a path under the
  repository root, not even under the ephemeral `.project/`. Running the suite
  must leave the repository surface unchanged;
  `tests/test_pytest_isolation.py` is the regression.
- New dev tools get their suite in this directory, following the existing
  style: fake-repo fixtures via `tmp_path`, CLI exit-code coverage, and a
  stdlib-only test for the tool.

See the root `AGENTS.md` for the full verification battery.
