"""Direct tests for runner.extract_toml_block (TOML section loader)."""

import runner


def test_valid_toml_block_returns_dict():
    content = """# Doc

## Metadata

```toml
id = "test"
status = "DONE"
```
"""
    data = runner.extract_toml_block(content, "Metadata")
    assert data == {"id": "test", "status": "DONE"}


def test_section_without_block_returns_none():
    content = """# Doc

## Metadata

No fenced block here.
"""
    assert runner.extract_toml_block(content, "Metadata") is None


def test_missing_section_returns_none():
    content = """# Doc

## Other

```toml
id = "test"
```
"""
    assert runner.extract_toml_block(content, "Metadata") is None


def test_invalid_toml_returns_none():
    content = """# Doc

## Metadata

```toml
id = = "test"
```
"""
    assert runner.extract_toml_block(content, "Metadata") is None


def test_yaml_block_is_ignored():
    content = """# Doc

## Metadata

```yaml
id: "test"
```
"""
    assert runner.extract_toml_block(content, "Metadata") is None


def test_arrays_and_array_of_tables():
    content = """# Doc

## Steps Executed

```toml
tags = ["a", "b"]
empty = []

[[steps_executed]]
order = 1
action = "Update schema"

[[steps_executed]]
order = 2
action = "Run tests"
```
"""
    data = runner.extract_toml_block(content, "Steps Executed")
    assert data["tags"] == ["a", "b"]
    assert data["empty"] == []
    assert data["steps_executed"] == [
        {"order": 1, "action": "Update schema"},
        {"order": 2, "action": "Run tests"},
    ]


def test_strings_containing_colons():
    """The old hand-rolled YAML parser mishandled colons inside values."""
    content = """# Doc

## Metadata

```toml
location = "app/services/user_service.py:42"
note = "key: value pairs are fine"
```
"""
    data = runner.extract_toml_block(content, "Metadata")
    assert data["location"] == "app/services/user_service.py:42"
    assert data["note"] == "key: value pairs are fine"


def test_nested_tables():
    content = """# Doc

## Technical Practice Evidence

```toml
[technical_practice_evidence.tdd]
applied = true
final_test_result = "PASS"

[[technical_practice_evidence.tdd.failing_tests]]
file = "tests/test_users.py"
```
"""
    data = runner.extract_toml_block(content, "Technical Practice Evidence")
    tdd = data["technical_practice_evidence"]["tdd"]
    assert tdd["applied"] is True
    assert tdd["final_test_result"] == "PASS"
    assert tdd["failing_tests"] == [{"file": "tests/test_users.py"}]


def test_scalars_bool_and_int():
    content = """# Doc

## Scope Compliance

```toml
[scope_compliance]
scope_respected = true
user_authorized_extra_work = false
count = 3
```
"""
    data = runner.extract_toml_block(content, "Scope Compliance")
    scope = data["scope_compliance"]
    assert scope["scope_respected"] is True
    assert scope["user_authorized_extra_work"] is False
    assert scope["count"] == 3
