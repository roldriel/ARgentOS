"""Behaviour, contract and determinism tests of the EARS coverage guard (plan 137).

The guard audits that EARS is implemented in the payload and protects the parity
between the standard (``EARS.md``), the contract (``TASK_SPECIFICATION.md``) and
the payload validator (``gate_validator.py``). This suite covers its **contract**:
CLI and exit codes, each signal, the JSON shape, determinism, read-only behaviour,
the stdlib-only rule and the ``GAP``-never-``VALID`` rule.

Everything here is **isolated** (``tests/AGENTS.md``): the payload is synthetic —
a standards file, a contract, a policy and a validator with the same interface
and the same five patterns, rendered by ``fake_validator_source`` — so the real
payload can evolve without breaking these tests. The deliberate coupling to the
real payload lives in ``tests/test_check_ears_coverage_dogfood.py``, and the
falsification table in
``tests/test_check_ears_coverage_falsification.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import check_ears_coverage as checker

# --------------------------------------------------------------------------- #
# Synthetic payload: the same shape and interface as the real one
# --------------------------------------------------------------------------- #

#: A synthetic ``EARS.md``. Same structure as the payload's (``## Patterns`` with
#: five ``### N. <name>`` subsections, one fenced ``text`` template each, then
#: examples and writing rules), so the guard derives its mechanical set from it
#: exactly as it does from the real standard.
EARS_STANDARD = """# EARS — synthetic standard for the guard's isolated tests

## Purpose

Synthetic, in the same shape as the payload standard.

## Patterns

### 1. Ubiquitous requirement

```text
The <system name> shall <system response>
```

### 2. Event-driven requirement

```text
When <event>, the <system name> shall <system response>
```

### 3. State-driven requirement

```text
While <state>, the <system name> shall <system response>
```

### 4. Unwanted behavior

```text
If <optional pre-condition>, then the <system name> shall <system response>
```

### 5. Optional feature

```text
Where <feature>, the <system name> shall <system response>
```

## Writing rules

1. **One criterion per bullet**: do not combine multiple requirements with "and".
2. **Use "shall"**: avoid "should", "must", "will", or "may".
3. **Avoid negations**: write what the system shall do.

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
```
"""

#: A synthetic contract whose ``## Acceptance Criteria`` makes both declarations
#: R3 requires: the bullet form is canonical, and TOML-only criteria are not.
CONTRACT = """# TASK_SPECIFICATION Contract (synthetic)

## Acceptance Criteria

The canonical form is one Markdown bullet per criterion. Each criterion must be
written using the EARS syntax defined in the standard.

```toml
acceptance_criteria = [""]
```

The TOML block is an optional machine-readable representation derived from the
bullets. It does not replace them: an artifact whose criteria appear only in the
TOML block does not satisfy the canonical form.

## Assumptions

Synthetic section.
"""

#: A synthetic H01 policy. R4 reads the activation from the validator module, not
#: from here; this file exists so the payload has the three declared sources.
POLICY = """# Harness Policy H01 (synthetic)

## Gate Checklist

3. Verify that `## Acceptance Criteria` contains at least one bullet (`-` or `*`).
"""

#: The validator the synthetic payload carries: same interface, same five
#: patterns, same greedy ``.+`` as the payload's ``EARS_RE``.
FAKE_VALIDATOR_TEMPLATE = '''"""Synthetic gate validator for the guard's isolated tests (plan 137).

Same public interface as the payload validator: ``TRIGGERS`` with an ``ears``
flag, ``EARS_RE``, and ``validate(trigger, artifact, root=None) -> (checks,
decision)`` where each check is a dict with ``id``/``result``/``evidence``.
Rendered by this suite with a chosen pattern set so a payload regression or a
pattern-set divergence can be simulated.
"""

from __future__ import annotations

import re

TRIGGERS = {
    "H01": {
        "artifact": "TASK_SPECIFICATION.md",
        "sections": [
            "Objective", "Expected Outcome", "Scope", "Constraints",
            "Acceptance Criteria", "Assumptions", "Unknowns", "Validation",
        ],
@EARS_LINE@    },
}

EARS_RE = re.compile(
    r"^(?:"
    r"The .+ shall .+"
    r"|When .+, the .+ shall .+"
    r"|While .+, the .+ shall .+"
    r"|If .+, then the .+ shall .+"
    r"|Where .+, the .+ shall .+"
    r")$"
)


def validate(trigger: str, artifact, root=None):
    """Same entry point as the payload validator's ``validate``."""
    spec = TRIGGERS.get(trigger)
    if spec is None:
        raise ValueError(f"unsupported trigger: {trigger}")
    artifact = __import__("pathlib").Path(artifact)
    checks = []
    if not artifact.is_file():
        checks.append({"id": "existence", "result": "FAIL", "evidence": "does not exist"})
        return checks, "FAIL"
    checks.append({"id": "existence", "result": "PASS", "evidence": str(artifact)})
    text = artifact.read_text(encoding="utf-8", errors="replace")
    if spec.get("ears"):
        body = text.split("## Acceptance Criteria", 1)[-1].split("\\n## ", 1)[0]
        bullets = [
            line.lstrip("-* ").strip()
            for line in body.splitlines()
            if line.strip().startswith(("-", "*"))
        ]
        if not bullets:
            checks.append({"id": "ears", "result": "FAIL", "evidence": "no bullets"})
        else:
            bad = [b for b in bullets if not EARS_RE.match(b)]
            if bad:
                checks.append(
                    {"id": "ears", "result": "FAIL",
                     "evidence": f"{len(bad)} bullets do not match EARS: {bad[:2]}"}
                )
            else:
                checks.append(
                    {"id": "ears", "result": "PASS", "evidence": f"{len(bullets)} EARS bullets"}
                )
    failed = any(check["result"] == "FAIL" for check in checks)
    return checks, ("FAIL" if failed else "PASS")
'''


def fake_validator_source(*, ears: bool = True) -> str:
    """The synthetic validator, optionally with the ``ears`` flag removed."""
    return FAKE_VALIDATOR_TEMPLATE.replace(
        "@EARS_LINE@", '        "ears": True,\n' if ears else ""
    )


def make_payload(
    tmp_path: Path,
    *,
    ears_standard: str | None = EARS_STANDARD,
    contract: str | None = CONTRACT,
    policy: str | None = POLICY,
    validator: str | None = None,
    fenced: str = "",
) -> Path:
    """A synthetic payload carrying the three sources of truth and the validator.

    Passing ``None`` for one source omits it, which is how the tests exercise the
    missing-source rules; passing a string replaces it, which is how they
    simulate a contract contradiction or a pattern-set divergence.
    """
    payload = tmp_path / "payload"
    (payload / "standards" / "requirements").mkdir(parents=True, exist_ok=True)
    (payload / "orchestrators" / "core" / "contracts").mkdir(parents=True, exist_ok=True)
    (payload / "orchestrators" / "core" / "harness" / "policies").mkdir(
        parents=True, exist_ok=True
    )
    (payload / "harness").mkdir(parents=True, exist_ok=True)
    if ears_standard is not None:
        (payload / checker.EARS_REL).write_text(ears_standard, encoding="utf-8")
    if contract is not None:
        (payload / checker.CONTRACT_REL).write_text(contract, encoding="utf-8")
    if policy is not None:
        (payload / checker.POLICY_REL).write_text(policy, encoding="utf-8")
    source = validator if validator is not None else fake_validator_source()
    (payload / checker.VALIDATOR_REL).write_text(source + fenced, encoding="utf-8")
    return payload


def write_specimen(path: Path, bullets: list[str] | str, *, section: bool = True) -> Path:
    """A synthetic ``TASK_SPECIFICATION.md`` carrying ``## Acceptance Criteria``.

    A list is rendered as ``-`` bullets (the canonical form); a string is
    rendered verbatim, which is how the TOML-only and prose-only cases are built.
    """
    body = ["# Specimen", "", "## Objective", "", "Synthetic.", ""]
    if section:
        body += ["## Acceptance Criteria", ""]
        if isinstance(bullets, str):
            body += [bullets, ""]
        else:
            body += [*(f"- {bullet}" for bullet in bullets), ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")
    return path


#: The five patterns of the standard, each filled, plus the standard's three
#: acceptable examples — the "positive corpus" of the plan's §Tests.
CANONICAL_BULLETS = [
    "The API shall reject a POST /users request with a name longer than 100 characters.",
    "When the email is already registered, the API shall return HTTP 409.",
    "While the database is unavailable, the API shall return HTTP 503.",
    "If the user ID is not a number, then the API shall return HTTP 400.",
    "Where email validation is enabled, the API shall reject malformed email addresses.",
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def run_cli(*args: str, capsys) -> tuple[int, str, str]:
    code = checker.main([str(arg) for arg in args])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def report_of(*args: str, capsys) -> checker.Report:
    """Run the CLI with ``--json`` and rebuild the findings from the JSON."""
    code, out, err = run_cli(*args, "--json", capsys=capsys)
    assert err == "", err
    payload = json.loads(out)
    report = checker.Report()
    for item in payload["results"]:
        report.add(
            checker.Finding(
                item["target"],
                item["rule"],
                item["signal"],
                item["reason"],
                item["source"],
                item["evidence"],
            )
        )
    report.exit_code = code  # type: ignore[attr-defined]
    return report


def signals_for(report: checker.Report, rule: str) -> set[str]:
    return {finding.signal for finding in report.findings if finding.rule == rule}


def signals_on(report: checker.Report, rule: str, target_contains: str) -> set[str]:
    return {
        finding.signal
        for finding in report.findings
        if finding.rule == rule and target_contains in finding.target
    }


def reasons_of(report: checker.Report) -> str:
    return " | ".join(finding.reason for finding in report.findings)


# --------------------------------------------------------------------------- #
# Positives
# --------------------------------------------------------------------------- #


def test_the_guard_is_valid_on_a_coherent_synthetic_payload(tmp_path, capsys):
    payload = make_payload(tmp_path)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 0, out + err
    assert "Summary:" in out
    assert "ANOMALY" not in out


def test_r4_and_r5_are_valid_and_r1_r2_are_a_declared_absence_without_a_corpus(
    tmp_path, capsys
):
    payload = make_payload(tmp_path)
    report = report_of("--payload", payload, capsys=capsys)
    assert report.exit_code == 0
    assert signals_for(report, "R4") == {checker.VALID}
    assert signals_for(report, "R5") == {checker.VALID}
    assert signals_for(report, "R3") == {checker.VALID}
    # R1/R2 are an explicit N/A: never VALID by vacuity of a missing corpus.
    assert signals_for(report, "R1") == {checker.NOT_APPLICABLE}
    assert signals_for(report, "R2") == {checker.NOT_APPLICABLE}
    assert "no `--corpus` was given" in reasons_of(report)


def test_a_canonical_corpus_is_r1_and_r2_valid(tmp_path, capsys):
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", CANONICAL_BULLETS)
    code, out, err = run_cli(
        "--payload", payload, "--corpus", specimen, capsys=capsys
    )
    assert code == 0, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R1") == {checker.VALID}
    assert signals_for(report, "R2") == {checker.VALID}
    assert "5 bullet(s)" in reasons_of(report)


def test_the_guard_reports_the_established_mechanical_set_with_its_sources(
    tmp_path, capsys
):
    """Criterio 1: the report names the mechanical subset and what is excluded."""
    payload = make_payload(tmp_path)
    code, out, _ = run_cli("--payload", payload, capsys=capsys)
    assert code == 0
    for rule, _description, source in checker.MECHANICAL_SUBSET:
        assert f"{rule}:" in out
        assert source in out
    for description, classification in checker.EXCLUDED_SUBSET:
        assert description in out
        assert classification in out


def test_every_finding_cites_its_source_as_path_colon_section(tmp_path, capsys):
    """Every finding cites a source; the four documentary sources are covered.

    The citation is ``ruta:sección`` for the documentary sources, and for the
    validator the module path (its activation is a fact about the module, not
    about one of its sections). A corpus finding cites the corpus artifact.
    """
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", ["The API should be nice."])
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert report.findings, "no findings produced"
    for finding in report.findings:
        assert finding.source, finding
        assert finding.source == checker.CORPUS_REF or finding.source.startswith(
            "protocol/.agents/"
        ), finding.source
        assert ":" in finding.source or finding.source.endswith(".py"), finding.source
    citations = {finding.source for finding in report.findings}
    assert checker.POLICY_REF in citations
    assert checker.CONTRACT_REF in citations
    assert checker.VALIDATOR_REF in citations


# --------------------------------------------------------------------------- #
# Exit codes and signals
# --------------------------------------------------------------------------- #


def test_a_bullet_matching_no_pattern_is_an_anomaly_and_exits_one(tmp_path, capsys):
    payload = make_payload(tmp_path)
    specimen = write_specimen(
        tmp_path / "spec.md",
        ["The API should handle errors gracefully.", "Users can't create accounts."],
    )
    code, out, err = run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert checker.ANOMALY in signals_for(report, "R2")
    assert "reports FAIL" in reasons_of(report)


def test_gap_does_not_change_the_exit_code_but_anomaly_does(tmp_path, capsys):
    payload = make_payload(tmp_path)
    empty = write_specimen(tmp_path / "empty.md", "", section=False)
    assert run_cli("--payload", payload, "--corpus", empty, capsys=capsys)[0] == 0

    bad = write_specimen(tmp_path / "bad.md", ["The API should be nice."])
    assert run_cli("--payload", payload, "--corpus", bad, capsys=capsys)[0] == 1


def test_a_missing_section_is_gap_and_never_valid(tmp_path, capsys):
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", "", section=False)
    code, out, err = run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R1") == {checker.GAP}
    assert checker.VALID not in signals_for(report, "R1")
    assert "no `## Acceptance Criteria` section" in reasons_of(report)


def test_an_empty_criteria_section_is_gap_and_never_valid(tmp_path, capsys):
    """A section with prose but no bullet is a declared GAP, not a pass."""
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", "To be defined later.")
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R1") == {checker.GAP}
    assert "contains no bullet" in reasons_of(report)


def test_criteria_only_in_the_toml_block_are_a_form_violation(tmp_path, capsys):
    """R3's violation of the canonical form: criteria in the TOML block only.

    The artifact carries no bullet, so R1 is a declared ``GAP`` and the exit code
    stays 0 (``GAP`` is advisory). The finding names the TOML-only violation the
    contract declares, so the violation is never silently accepted.
    """
    payload = make_payload(tmp_path)
    specimen = write_specimen(
        tmp_path / "spec.md",
        '```toml\nacceptance_criteria = ["The API shall respond."]\n```',
    )
    code, out, err = run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R1") == {checker.GAP}
    assert checker.ANOMALY not in signals_for(report, "R1")
    assert "acceptance_criteria` TOML block" in reasons_of(report)


def test_a_non_existent_corpus_is_a_declared_absence_and_does_not_crash(tmp_path, capsys):
    payload = make_payload(tmp_path)
    missing = tmp_path / "does-not-exist.md"
    code, out, err = run_cli("--payload", payload, "--corpus", missing, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, "--corpus", missing, capsys=capsys)
    assert signals_for(report, "R1") == {checker.NOT_APPLICABLE}
    assert signals_for(report, "R2") == {checker.NOT_APPLICABLE}
    assert "does not exist" in reasons_of(report)


# --------------------------------------------------------------------------- #
# Missing sources: GAP, never VALID
# --------------------------------------------------------------------------- #


def test_a_missing_standard_is_a_read_error(tmp_path, capsys):
    payload = make_payload(tmp_path, ears_standard=None)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 2, out + err
    assert "EARS standard not found" in err


def test_a_missing_validator_is_a_read_error(tmp_path, capsys):
    payload = make_payload(tmp_path)
    (payload / checker.VALIDATOR_REL).unlink()
    code, _out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 2
    assert "payload validator not found" in err


def test_a_standard_without_pattern_templates_is_gap_and_never_valid(tmp_path, capsys):
    standard = "# EARS\n\n## Patterns\n\nNo template here.\n"
    payload = make_payload(tmp_path, ears_standard=standard)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R5") == {checker.GAP}
    assert checker.VALID not in signals_for(report, "R5")


def test_a_missing_contract_is_gap_and_never_valid(tmp_path, capsys):
    payload = make_payload(tmp_path, contract=None)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R3") == {checker.GAP}
    assert checker.VALID not in signals_for(report, "R3")


def test_a_contract_without_the_criteria_section_is_gap(tmp_path, capsys):
    contract = "# Contract\n\n## Objective\n\nNo acceptance-criteria section.\n"
    payload = make_payload(tmp_path, contract=contract)
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R3") == {checker.GAP}
    assert "declares no `## Acceptance Criteria` section" in reasons_of(report)


def test_a_contract_declaring_only_one_half_is_gap(tmp_path, capsys):
    """Half a declaration is missing evidence, not a pass."""
    contract = "# Contract\n\n## Acceptance Criteria\n\nThe canonical form is one Markdown bullet per criterion.\n"
    payload = make_payload(tmp_path, contract=contract)
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R3") == {checker.GAP}
    assert "only in part" in reasons_of(report)


def test_a_contract_contradicting_the_canonical_form_is_an_anomaly(tmp_path, capsys):
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion. Criteria appear only "
        "in the TOML block does not satisfy the canonical form.\n\n"
        "The TOML block is the canonical form and replaces the bullets.\n"
    )
    payload = make_payload(tmp_path, contract=contract)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R3") == {checker.ANOMALY}
    assert "contradicts the canonical form" in reasons_of(report)


# --------------------------------------------------------------------------- #
# Payload regression and pattern-set divergence (the guard's reason to exist)
# --------------------------------------------------------------------------- #


def test_a_validator_that_stops_checking_ears_is_an_anomaly(tmp_path, capsys):
    payload = make_payload(tmp_path, validator=fake_validator_source(ears=False))
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R4") == {checker.ANOMALY}
    assert signals_on(report, "R4", checker.VALIDATOR_REL) == {checker.ANOMALY}


def test_a_validator_that_drops_a_pattern_is_a_divergence(tmp_path, capsys):
    """The standard declares five patterns; the validator implements four."""
    source = fake_validator_source().replace(
        '    r"|Where .+, the .+ shall .+"\n', ""
    )
    payload = make_payload(tmp_path, validator=source)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R5") == {checker.ANOMALY}
    assert "rejects a sentence formed from" in reasons_of(report)


def test_a_standard_declaring_an_extra_pattern_is_a_divergence(tmp_path, capsys):
    """A sixth pattern the validator does not implement is an ANOMALY, not a pass."""
    extra = (
        "### 6. Synthetic extra\n\n"
        "```text\n"
        "Where <feature>, the <system name> shall <system response> and <other>\n"
        "```\n\n"
    )
    standard = EARS_STANDARD.replace("## Writing rules", extra + "## Writing rules")
    payload = make_payload(tmp_path, ears_standard=standard)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R5") == {checker.ANOMALY}


def test_a_validator_accepting_an_undeclared_sentence_is_an_anomaly(tmp_path, capsys):
    """A regex wider than the declared set is reported, never assumed correct.

    The fifth alternative is widened past its declared placeholders, so the
    implemented set accepts a sentence the standard does not declare.
    """
    source = fake_validator_source().replace(
        'r"|Where .+, the .+ shall .+"', 'r"|Where .+, the .+ shall .+ and .+"'
    )
    assert '"|Where .+, the .+ shall .+ and .+"' in source
    payload = make_payload(tmp_path, validator=source)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R5") == {checker.ANOMALY}


def test_a_validator_producing_no_ears_entry_is_an_anomaly(tmp_path, capsys):
    """The spec declares the flag but the run materializes nothing for it."""
    fenced = '''

def validate(trigger, artifact, root=None):
    return ([{"id": "existence", "result": "PASS", "evidence": "ok"}], "PASS")
'''
    payload = make_payload(tmp_path, fenced=fenced)
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R4") == {checker.ANOMALY}
    assert "produced no `ears` entry" in reasons_of(report)


def test_a_validator_without_a_triggers_table_is_an_anomaly(tmp_path, capsys):
    payload = make_payload(
        tmp_path,
        validator=(
            "import re\n\n"
            "TRIGGERS = None\n"
            'EARS_RE = re.compile(r"^(?:The .+ shall .+)$")\n'
        ),
    )
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R4") == {checker.ANOMALY}
    assert "declares no `TRIGGERS` table" in reasons_of(report)


def test_a_validator_without_an_h01_spec_is_an_anomaly(tmp_path, capsys):
    payload = make_payload(
        tmp_path,
        validator=(
            "import re\n\n"
            'TRIGGERS = {"H02": {"sections": []}}\n'
            'EARS_RE = re.compile(r"^(?:The .+ shall .+)$")\n'
        ),
    )
    code, out, err = run_cli("--payload", payload, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, capsys=capsys)
    assert signals_for(report, "R4") == {checker.ANOMALY}
    assert "no `TRIGGERS[\"H01\"]` spec" in reasons_of(report)


def test_a_corpus_anomaly_is_still_reported_when_r4_is_broken(tmp_path, capsys):
    """Without an `ears` verdict the corpus is a GAP, never an invented PASS."""
    payload = make_payload(tmp_path, validator=fake_validator_source(ears=False))
    specimen = write_specimen(tmp_path / "spec.md", CANONICAL_BULLETS)
    code, out, err = run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert code == 1, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R2") == {checker.GAP}
    assert checker.VALID not in signals_for(report, "R2")


# --------------------------------------------------------------------------- #
# The excluded subset: the guard must stay silent about judgement
# --------------------------------------------------------------------------- #


def test_the_guard_does_not_rule_on_the_excluded_subset(tmp_path, capsys):
    """A bullet the guard must leave alone, by plan 137 block B.

    The bullet is compound and matches an EARS pattern, so ``ears`` PASSes and
    the guard reports R2 ``VALID``. It must not produce a finding about
    specificity, verifiability, compoundness, negation, modality or assumptions:
    silence is the declared boundary, not an approval.
    """
    payload = make_payload(tmp_path)
    specimen = write_specimen(
        tmp_path / "spec.md", ["The API shall validate input and return errors."]
    )
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R2") == {checker.VALID}
    assert {finding.rule for finding in report.findings} == {"R1", "R2", "R3", "R4", "R5"}
    assert checker.EXCLUDED_SUBSET, "the excluded subset must be declared in the tool"


# --------------------------------------------------------------------------- #
# Determinism, read-only policy and the tool contract
# --------------------------------------------------------------------------- #


def test_two_runs_produce_byte_identical_output(tmp_path, capsys):
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", CANONICAL_BULLETS)
    first = run_cli("--payload", payload, "--corpus", specimen, "--json", capsys=capsys)
    second = run_cli("--payload", payload, "--corpus", specimen, "--json", capsys=capsys)
    assert first == second
    assert run_cli("--payload", payload, capsys=capsys)[1] == run_cli(
        "--payload", payload, capsys=capsys
    )[1]


def test_the_corpus_order_does_not_depend_on_filesystem_order(tmp_path, capsys):
    """The same set of corpus paths in any argument order gives one report."""
    payload = make_payload(tmp_path)
    first = write_specimen(tmp_path / "aaa.md", CANONICAL_BULLETS)
    second = write_specimen(tmp_path / "bbb.md", ["The API should be nice."])
    left = run_cli("--payload", payload, "--corpus", second, "--corpus", first, capsys=capsys)
    right = run_cli("--payload", payload, "--corpus", first, "--corpus", second, capsys=capsys)
    assert left == right


def test_relative_corpus_paths_resolve_against_root(tmp_path, capsys, monkeypatch):
    make_payload(tmp_path)
    write_specimen(tmp_path / "spec.md", CANONICAL_BULLETS)
    monkeypatch.chdir(tmp_path)
    code, out, err = run_cli("--payload", "payload", "--root", ".", "--corpus", "spec.md", capsys=capsys)
    assert code == 0, out + err
    assert "spec.md" in out


def test_the_guard_writes_nothing_to_the_payload_or_the_corpus(tmp_path, capsys):
    """The read-only policy, including the bytecode cache the load could create."""
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", ["The API should be nice."])
    before = snapshot(payload, specimen)
    run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    run_cli("--payload", payload, "--corpus", specimen, "--json", capsys=capsys)
    assert snapshot(payload, specimen) == before
    assert not list(payload.rglob("__pycache__")), list(payload.rglob("__pycache__"))
    assert not list(specimen.parent.rglob("__pycache__"))


def test_the_guard_leaves_no_module_registered_in_sys_modules(tmp_path, capsys):
    """Loading the payload validator restores ``sys.modules`` as it found it."""
    import sys

    payload = make_payload(tmp_path)
    before = set(sys.modules)
    run_cli("--payload", payload, capsys=capsys)
    assert set(sys.modules) == before


def snapshot(*roots: Path) -> dict[str, bytes]:
    """Every regular file under ``roots``, keyed by path, with its bytes."""
    files: dict[str, bytes] = {}
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                files[str(path)] = path.read_bytes()
    return files


def test_the_tool_is_stdlib_only():
    import testsupport

    testsupport.assert_tool_imports_only_stdlib(
        Path(__file__).resolve().parents[1] / "tools" / "check_ears_coverage.py"
    )


def test_the_tool_does_not_import_another_tool():
    """The guard shares the DEV checker contract, not its code (plan 137)."""
    import ast

    source = (
        Path(__file__).resolve().parents[1] / "tools" / "check_ears_coverage.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for module in sorted(imported):
        assert not module.startswith("check_"), module


def test_the_json_report_has_the_expected_shape(tmp_path, capsys):
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", CANONICAL_BULLETS)
    _code, out, _err = run_cli(
        "--payload", payload, "--corpus", specimen, "--json", capsys=capsys
    )
    document = json.loads(out)
    assert document["tool"] == "check_ears_coverage"
    assert document["plan"] == 137
    assert set(document["counts"]) == {
        checker.ANOMALY,
        checker.BOUNDARY,
        checker.GAP,
        checker.NOT_APPLICABLE,
        checker.VALID,
    }
    assert document["mechanical_subset"]
    assert document["excluded_subset"]
    assert len(document["patterns"]) == 5
    for pattern in document["patterns"]:
        assert pattern["template"]
        assert pattern["filled"]
        assert pattern["placeholders"]
    for result in document["results"]:
        assert set(result) == {"target", "rule", "signal", "reason", "source", "evidence"}
        assert result["source"]
    # The JSON is stable: sorted keys and one document (``print`` adds the final
    # newline).
    assert out == json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def test_the_derived_mechanical_set_comes_from_the_standard_not_a_literal(tmp_path):
    """The tool holds no pattern list: it parses the standard's fenced blocks."""
    payload = make_payload(tmp_path)
    module = checker.load_validator(payload)
    mechanical = checker.load_mechanical_set(payload, module)
    assert [pattern.template for pattern in mechanical.patterns] == [
        "The <system name> shall <system response>",
        "When <event>, the <system name> shall <system response>",
        "While <state>, the <system name> shall <system response>",
        "If <optional pre-condition>, then the <system name> shall <system response>",
        "Where <feature>, the <system name> shall <system response>",
    ]
    # The standard's example blocks carry no placeholder and are not templates.
    assert all("<" in pattern.template for pattern in mechanical.patterns)


def test_a_corpus_artifact_with_matching_bullets_but_no_section_is_not_a_pass(
    tmp_path, capsys
):
    payload = make_payload(tmp_path)
    specimen = tmp_path / "spec.md"
    specimen.write_text(
        "# Specimen\n\n## Acceptance Criteria\n\n- The API shall respond.\n\n## Scope\n\n"
        "- The API shall respond.\n",
        encoding="utf-8",
    )
    code, out, err = run_cli("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert code == 0, out + err
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert signals_for(report, "R1") == {checker.VALID}
    assert "1 bullet(s)" in reasons_of(report)


@pytest.mark.parametrize(
    "bullet",
    [
        "The API shall validate input and return errors.",
        "Users can't create accounts with bad data.",
        "The API should handle errors gracefully.",
        "The API must validate JWTs.",
        "The API will log every request.",
        "The API may cache responses.",
    ],
)
def test_bad_but_passing_bullets_produce_no_rule_of_the_excluded_subset(
    tmp_path, capsys, bullet
):
    """The declared boundary, per bullet: compound, negative or modal.

    Whatever the payload validator's verdict is, the guard may only produce its
    five declared rules and its five declared signals. A finding about
    compoundness, negation or modality would have to introduce a new rule or a
    new signal, so this asserts the boundary structurally rather than by
    keyword: the offending bullet is quoted verbatim in the R2/R4 *evidence*,
    and that quote is not a finding of the guard.
    """
    payload = make_payload(tmp_path)
    specimen = write_specimen(tmp_path / "spec.md", [bullet, "The API shall respond."])
    report = report_of("--payload", payload, "--corpus", specimen, capsys=capsys)
    assert {finding.rule for finding in report.findings} <= {
        rule for rule, _description, _source in checker.MECHANICAL_SUBSET
    }
    assert {finding.signal for finding in report.findings} <= {
        checker.VALID,
        checker.GAP,
        checker.ANOMALY,
        checker.NOT_APPLICABLE,
        checker.BOUNDARY,
    }
    # The rules the excluded subset would need do not exist in the tool.
    assert {rule for rule, _d, _s in checker.MECHANICAL_SUBSET} == {
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
    }
