#!/usr/bin/env python3
"""Audit EARS coverage and guard the parity of its mechanical subset (plan 137).

EARS is the acceptance-criteria standard of the payload
(``protocol/.agents/standards/requirements/EARS.md``). ``RFC-34`` / plan 33 fixed
the **canonical form** of ``## Acceptance Criteria``: one Markdown bullet per
criterion, atomic and verifiable, with the ``acceptance_criteria`` TOML block as
an *optional, derived* machine-readable representation that never replaces the
bullets. The payload's structural validator
(``protocol/.agents/harness/gate_validator.py``, RFC-57 / plan 66) already
implements the EARS check for ``H01``: its spec activates ``ears`` and the check
reads the bullets and matches them against ``EARS_RE``.

``F-01`` documents what a divergence between the contract and that validator
costs: a gate FAIL, a whole ``RECOVERY`` phase, rework. The alignment was fixed
(plans 33 and 66) but **nothing protected it**. This tool is that guard.

**It does not reimplement EARS validation.** It loads the payload's
``gate_validator.py`` with ``importlib.util`` and calls
``validate("H01", <artifact>)``; the ``ears`` entry of the returned checks list
is *evidence*, and the guard reports the validator's own ``PASS``/``FAIL``
vocabulary rather than producing it. Three sources of truth are read, and none
of them is owned here:

* ``standards/requirements/EARS.md:Patterns`` — the five sentence patterns;
* ``orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`` —
  the canonical Markdown-bullet form;
* ``orchestrators/core/harness/policies/H01-task-specification.md:Gate Checklist``
  — which item is ``[gate]``.

What it checks (deterministic; decided by reading bytes and comparing them):

* **R1** — a corpus artifact's ``## Acceptance Criteria`` contains at least one
  bullet (``-``/``*``);
* **R2** — every bullet is accepted by the payload validator's ``ears`` check;
* **R3** — the contract declares the Markdown-bullet form canonical **and**
  declares that TOML-only criteria do not satisfy it;
* **R4** — the payload spec still activates ``ears`` for ``H01`` and an
  invocation really produces an ``ears`` entry (regression guard);
* **R5** — parity: the five pattern templates the standard declares, read from its
  fenced ``text`` blocks and filled placeholder by placeholder, are exactly what
  the payload's own ``EARS_RE`` accepts and rejects. The guard compiles no pattern
  of its own: it reads the regex object out of the payload module, runs it, and
  compares the result with the declared templates — a pattern the validator
  accepted and the standard did not declare, or the reverse, is an ``ANOMALY``.

What it deliberately does **not** do (plan 137 §"Subset excluido"; plan 137
§"Naturaleza mecánica" block B). It never judges whether a criterion is specific,
verifiable, compound, free of negations, free of ``should``/``must``/``will``/
``may``, appropriate for the domain, or derived from an unconfirmed assumption.
Those items are ``[agent]`` judgement in ``H01``, or writing rules that ``H01``
does not mark ``[gate]`` at all, and **silence about them is a declared boundary,
not an approval.** A bullet that is compound, negative or modal is reported by
neither this tool nor the payload validator, and the suites prove it.

Vocabulary. ``VALID`` the rule holds; ``GAP`` evidence is missing or unobtainable
(advisory, never changes the exit code); ``ANOMALY`` a verifiable contradiction;
``N/A`` a legitimate declared absence (no corpus given to ``--corpus``, or a
corpus path that does not exist); ``BOUNDARY`` a structural ambiguity that needs
human review. ``FAIL`` is the payload validator's vocabulary: it is reported as
evidence, never produced as a classification of this tool.

Requirements are **derived** from the standard, never from a list maintained
here: R5 parses the fenced ``text`` template blocks of
``EARS.md:Patterns`` and substitutes their placeholders, so adding a sixth
pattern to the standard without teaching the validator about it is an
``ANOMALY`` rather than a silent pass.

Usage::

    python tools/check_ears_coverage.py [--payload protocol/.agents] [--root .]
                                       [--corpus SPEC] [--corpus SPEC] [--json]

Exit codes (the contract of the repository's checkers):

* ``0`` — no ``ANOMALY`` found. ``GAP`` is advisory and never changes the exit
  code; missing corpus evidence is a valid absence, not a failure.
* ``1`` — at least one ``ANOMALY`` (present but contradictory information).
* ``2`` — unrecoverable read error.

Standard library only. Read-only: nothing is written, repaired or archived.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

#: Signals (the repository's existing vocabulary; never conflated).
VALID = "VALID"
GAP = "GAP"
ANOMALY = "ANOMALY"
BOUNDARY = "BOUNDARY"
NOT_APPLICABLE = "N/A"

_SIGNAL_PRECEDENCE = (ANOMALY, BOUNDARY, GAP, NOT_APPLICABLE, VALID)

#: The trigger whose spec carries the ``ears`` flag (RFC-57).
TRIGGER = "H01"

#: Payload-relative paths of the three sources of truth, and the pattern section
#: R5 derives the mechanical set from. No pattern list is maintained here.
EARS_REL = "standards/requirements/EARS.md"
CONTRACT_REL = "orchestrators/core/contracts/TASK_SPECIFICATION.md"
POLICY_REL = "orchestrators/core/harness/policies/H01-task-specification.md"
VALIDATOR_REL = "harness/gate_validator.py"

EARS_SECTION = "Patterns"
CONTRACT_SECTION = "Acceptance Criteria"
POLICY_SECTION = "Gate Checklist"

#: Repository-relative citations recorded on every finding. The same constants
#: drive the ``ruta:sección`` a reader is sent to; they are the only paths this
#: tool names, and all of them are read-only inputs.
EARS_REF = f"protocol/.agents/{EARS_REL}:{EARS_SECTION}"
CONTRACT_REF = f"protocol/.agents/{CONTRACT_REL}:{CONTRACT_SECTION}"
POLICY_REF = f"protocol/.agents/{POLICY_REL}:{POLICY_SECTION}"
VALIDATOR_REF = f"protocol/.agents/{VALIDATOR_REL}"

#: ``ruta:sección`` of the corpus artifact itself, when the rule is about it.
CORPUS_REF = "--corpus TASK_SPECIFICATION.md:Acceptance Criteria"

#: The mechanical subset this guard establishes, with the normative source that
#: requires each rule. Reported by every run so a reader can see what is covered.
MECHANICAL_SUBSET: tuple[tuple[str, str, str], ...] = (
    ("R1", "## Acceptance Criteria contains at least one bullet (`-`/`*`)", POLICY_REF),
    ("R2", "every bullet is accepted by the payload validator's `ears` check", EARS_REF),
    ("R3", "the contract declares the bullet form canonical and TOML-only insufficient", CONTRACT_REF),
    ("R4", "the payload validator really activates and produces the `ears` check for H01", VALIDATOR_REF),
    ("R5", "the declared pattern set and the payload's `EARS_RE` are in parity", EARS_REF),
)

#: Block B of plan 137: declared **out** of the mechanical set, by name, with the
#: classification the payload gives it. The guard never rules on these.
EXCLUDED_SUBSET: tuple[tuple[str, str], ...] = (
    ("is the criterion specific?", "H01 item 10 `[agent]`"),
    ("is the criterion verifiable?", "H01 item 10 `[agent]`"),
    ("is the criterion compound?", "H01 item 12 `[agent]`"),
    ("does it avoid negations?", "EARS.md:Writing rules 3, not marked `[gate]` by H01"),
    ("does it avoid `should`/`must`/`will`/`may`?", "EARS.md:Writing rules 2, not marked `[gate]` by H01"),
    ("is it appropriate for the domain?", "H01 item 10 `[agent]`"),
    ("does it derive from an unconfirmed assumption?", "H01 item 16 `[agent]`"),
)

#: Filler substituted for every ``<...>`` placeholder of a pattern template. It
#: carries no comma and no `` shall ``, so a filled template exercises the
#: pattern itself and nothing else.
FILLER = "candidate response"

#: A sentence that matches none of the declared patterns (it carries no `shall`
#: clause at all). Used by R5 to show the accepted set is bounded.
UNPATTERNED_SENTENCE = "The candidate will be reviewed by the team."

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$", re.MULTILINE)
_FENCE_RE = re.compile(r"^[ \t]*```(\w*)[ \t]*\r?\n(.*?)\r?\n[ \t]*```[ \t]*$", re.MULTILINE | re.DOTALL)
_PLACEHOLDER_RE = re.compile(r"<([^<>\n]+)>")
_HEADING_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


class ReadError(RuntimeError):
    """An input could not be read at all (exit 2, never a claim about content)."""


# --------------------------------------------------------------------------- #
# Findings and report
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Finding:
    """One rule result: a signal, the reason, and the ``ruta:sección`` source."""

    target: str
    rule: str
    signal: str
    reason: str
    source: str = ""
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "rule": self.rule,
            "signal": self.signal,
            "reason": self.reason,
            "source": self.source,
            "evidence": self.evidence,
        }


@dataclass
class Report:
    """The accumulated findings of one run, in evaluation order."""

    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def by_rule(self, rule: str) -> list[Finding]:
        return [finding for finding in self.findings if finding.rule == rule]

    @property
    def has_anomaly(self) -> bool:
        return any(finding.signal == ANOMALY for finding in self.findings)

    def per_target(self) -> list[tuple[str, str, list[Finding]]]:
        grouped: dict[str, list[Finding]] = {}
        for finding in self.findings:
            grouped.setdefault(finding.target, []).append(finding)
        return [
            (target, _worst(item.signal for item in items), items)
            for target, items in sorted(grouped.items())
        ]

    def counts(self) -> dict[str, int]:
        counts = {signal: 0 for signal in _SIGNAL_PRECEDENCE}
        for target, signal, _ in self.per_target():
            counts[signal] += 1
        return counts


def _worst(signals: Iterable[str]) -> str:
    present = set(signals)
    for signal in _SIGNAL_PRECEDENCE:
        if signal in present:
            return signal
    return NOT_APPLICABLE


# --------------------------------------------------------------------------- #
# Read-only inputs
# --------------------------------------------------------------------------- #


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReadError(f"cannot read {path}: {exc}") from exc


def section_text(text: str, heading: str) -> str:
    """The body of ``## <heading>`` (case-insensitive), or ``""`` when absent.

    Section resolution is deliberately the same shape as the payload validator's
    ``section_text`` (line-based, ends at the next ``##``), so a corpus section
    this tool extracts is the section the validator reads.
    """
    wanted = _normalize_heading(heading)
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        match = _SECTION_RE.match(line)
        if match and _normalize_heading(match.group(1)) == wanted:
            start = index
            break
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start + 1 :]:
        if _SECTION_RE.match(line):
            break
        body.append(line)
    return "\n".join(body)


def has_section(text: str, heading: str) -> bool:
    wanted = _normalize_heading(heading)
    return any(
        _normalize_heading(match.group(1)) == wanted
        for match in _SECTION_RE.finditer(text)
    )


def _normalize_heading(value: str) -> str:
    return _HEADING_NORMALIZE_RE.sub("", value.strip().lower())


def collapse(value: str) -> str:
    """Whitespace-collapsed, case-folded text, for declaration matching."""
    return re.sub(r"\s+", " ", value).strip().casefold()


def text_blocks(text: str) -> list[str]:
    """The bodies of every ```` ```text ```` fenced block, in document order."""
    return [
        match.group(2)
        for match in _FENCE_RE.finditer(text)
        if match.group(1).lower() == "text"
    ]


def acceptance_bullets(text: str) -> list[str]:
    """The bullets of ``## Acceptance Criteria``, in document order.

    The extraction mirrors the payload validator's: a line whose ``lstrip``
    starts with ``-`` or ``*`` is a bullet, and the marker is stripped. Parity
    with that extraction is itself checked by R4's specimen and by the suites.
    """
    body = section_text(text, CONTRACT_SECTION)
    bullets: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            bullets.append(stripped.lstrip("-* ").strip())
    return bullets


# --------------------------------------------------------------------------- #
# The mechanical set, derived from the standard (never maintained here)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Pattern:
    """One declared EARS pattern template, as read from ``EARS.md:Patterns``."""

    template: str
    placeholders: tuple[str, ...]

    def filled(self, filler: str = FILLER) -> str:
        return _PLACEHOLDER_RE.sub(filler, self.template)

    def to_dict(self) -> dict[str, Any]:
        return {
            "template": self.template,
            "placeholders": list(self.placeholders),
            "filled": self.filled(),
        }


def parse_patterns(text: str) -> list[Pattern]:
    """Derive the pattern templates from the fenced ``text`` blocks.

    The templates are the fenced ``text`` blocks whose body contains a ``<...>``
    placeholder; the standard's *example* blocks are plain sentences and carry
    none, so they are not templates. Order is the document's order.
    """
    patterns: list[Pattern] = []
    for block in text_blocks(text):
        body = block.strip()
        placeholders = tuple(_PLACEHOLDER_RE.findall(body))
        if not placeholders:
            continue
        patterns.append(Pattern(template=body, placeholders=placeholders))
    return patterns


def _segments(template: str) -> list[tuple[str, str]]:
    """Split a template into ``("literal", text)`` / ``("placeholder", name)``.

    The split is done with the placeholder pattern itself (capturing), so a name
    is never searched for inside an escaped string: ``re.escape`` leaves ``<``
    and ``>`` alone but escapes the space inside ``<system name>``, and a
    string-matching approach silently stops finding placeholders there.
    """
    parts = _PLACEHOLDER_RE.split(template)
    segments: list[tuple[str, str]] = []
    for index, part in enumerate(parts):
        if index % 2 == 0:
            if part:
                segments.append(("literal", part))
        else:
            segments.append(("placeholder", part))
    return segments


def _free_pattern(template: str) -> str:
    """A matcher for one template: one ``.+`` per placeholder occurrence."""
    parts: list[str] = []
    for kind, text in _segments(template):
        parts.append(re.escape(text) if kind == "literal" else ".+")
    return "^" + "".join(parts) + "$"


@dataclass
class MechanicalSet:
    """The derived pattern set and the payload's implemented one."""

    patterns: list[Pattern]
    payload_re: re.Pattern[str]
    free: list[re.Pattern[str]]


def load_validator(payload: Path) -> Any:
    """Load the payload's ``gate_validator`` module; never import it at module level.

    The module is payload data loaded from its real path, so the guard invokes
    the shipped implementation instead of a second copy of it. Loading performs
    no writes and runs no check.
    """
    path = payload / VALIDATOR_REL
    if not path.is_file():
        raise ReadError(f"payload validator not found: {path}")
    spec = importlib.util.spec_from_file_location("_ears_coverage_gate_validator", path)
    if spec is None or spec.loader is None:
        raise ReadError(f"cannot load the payload validator: {path}")
    module = importlib.util.module_from_spec(spec)
    # The module is registered only for the duration of its own execution:
    # ``dataclasses`` and friends resolve ``cls.__module__`` through
    # ``sys.modules``, so a module that is never registered raises there. The
    # registry is restored before returning, so the guard leaves no state behind.
    #
    # Bytecode writing is disabled for the duration of the load: the read-only
    # policy forbids writing *anything*, and importing the payload validator by
    # its real path would otherwise leave a ``__pycache__`` directory inside the
    # payload. ``sys.dont_write_bytecode`` is restored afterwards.
    name = spec.name
    previous = sys.modules.get(name)
    previous_flag = sys.dont_write_bytecode
    sys.modules[name] = module
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous_flag
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
    return module


def load_mechanical_set(payload: Path, module: Any) -> MechanicalSet:
    """Read the standard's templates and the payload's ``EARS_RE``."""
    ears = payload / EARS_REL
    if not ears.is_file():
        raise ReadError(f"EARS standard not found: {ears}")
    patterns = parse_patterns(_read_text(ears))
    payload_re = getattr(module, "EARS_RE", None)
    if payload_re is None:
        raise ReadError(f"the payload validator declares no EARS_RE: {payload / VALIDATOR_REL}")
    return MechanicalSet(
        patterns=patterns,
        payload_re=payload_re,
        free=[re.compile(_free_pattern(pattern.template)) for pattern in patterns],
    )


# --------------------------------------------------------------------------- #
# R5 — pattern-set parity (the core of the guard)
# --------------------------------------------------------------------------- #


def check_pattern_parity(mechanical: MechanicalSet, report: Report) -> None:
    """R5: the declared pattern set and the payload's ``EARS_RE`` are in parity."""
    target = f"{EARS_REL}:{EARS_SECTION}"
    if not mechanical.patterns:
        report.add(
            Finding(
                target,
                "R5",
                GAP,
                "the standard declares no pattern template: no mechanical set can "
                "be derived, so parity cannot be established (missing evidence, "
                "advisory)",
                EARS_REF,
            )
        )
        return

    # (a) every template, placeholders filled, is accepted by the payload.
    rejected: list[str] = []
    for pattern in mechanical.patterns:
        sentence = pattern.filled()
        if not mechanical.payload_re.match(sentence):
            rejected.append(f"`{pattern.template}` (filled: `{sentence}`)")
    if rejected:
        report.add(
            Finding(
                target,
                "R5",
                ANOMALY,
                "the standard declares "
                f"{len(mechanical.patterns)} pattern(s) and the payload's `EARS_RE` "
                "rejects a sentence formed from "
                f"{len(rejected)} of them: {', '.join(rejected)}. A pattern declared "
                "by the standard and rejected by the validator is a false negative "
                "of the validator (R5, plan 137)",
                EARS_REF,
                evidence=f"templates={len(mechanical.patterns)}",
            )
        )
        return

    # (b) a sentence matching none of the declared patterns is rejected.
    unpatterned = UNPATTERNED_SENTENCE
    if mechanical.payload_re.match(unpatterned):
        report.add(
            Finding(
                target,
                "R5",
                ANOMALY,
                "the payload's `EARS_RE` accepts a sentence that matches none of the "
                f"patterns the standard declares (`{unpatterned}`): the implemented "
                "set is larger than the declared one, which is a false positive of "
                "the validator (R5, plan 137)",
                EARS_REF,
            )
        )
        return

    # (c) the payload regex is the declared set: one top-level alternative per
    #     declared pattern, carrying exactly one `.+` per placeholder occurrence,
    #     in the declared order. A missing, extra or widened alternative means the
    #     implemented set is not the declared one.
    divergent: list[str] = []
    declared = [len(pattern.placeholders) for pattern in mechanical.patterns]
    alternatives = _regex_alternatives(mechanical.payload_re)
    if alternatives is None:
        divergent.append(
            "`EARS_RE` is not a `^(?: alt | alt )$` alternation of the declared shape"
        )
    else:
        if len(alternatives) != len(mechanical.patterns):
            divergent.append(
                f"{len(alternatives)} regex alternative(s) for "
                f"{len(mechanical.patterns)} declared pattern(s)"
            )
        for pattern, count, alternative in zip(
            mechanical.patterns, declared, alternatives
        ):
            if alternative.count(".+") != count:
                divergent.append(
                    f"`{pattern.template}`: the alternative carries "
                    f"{alternative.count('.+')} wildcard(s) for {count} placeholder "
                    "occurrence(s)"
                )
    if divergent:
        report.add(
            Finding(
                target,
                "R5",
                ANOMALY,
                "the payload's `EARS_RE` is not the set of patterns the standard "
                f"declares, alternative by alternative: {'; '.join(divergent)} (R5, "
                "plan 137)",
                EARS_REF,
                evidence=f"declared={declared}",
            )
        )
        return

    report.add(
        Finding(
            target,
            "R5",
            VALID,
            f"the {len(mechanical.patterns)} pattern(s) declared by the standard, each "
            "placeholder filled, are all accepted by the payload's `EARS_RE`, and a "
            "sentence matching none of them is rejected: declared and implemented "
            "sets are in parity",
            EARS_REF,
            evidence="; ".join(f"`{pattern.template}`" for pattern in mechanical.patterns),
        )
    )


def _regex_alternatives(payload_re: re.Pattern[str]) -> list[str] | None:
    """The top-level alternatives of ``^(?: alt | alt )$``, in order.

    ``None`` when the regex is not that shape, which is itself a divergence from
    the declared form: the parity checks need the alternatives positionally.
    """
    source = payload_re.pattern
    prefix, suffix = "^(?:", ")$"
    if not source.startswith(prefix) or not source.endswith(suffix):
        return None
    body = source[len(prefix) : len(source) - len(suffix)]
    if "|" not in body:
        return None
    return body.split("|")


def _pattern_literal_counts(payload_re: re.Pattern[str]) -> list[int] | None:
    """``.+`` occurrences per top-level alternative of the payload regex."""
    alternatives = _regex_alternatives(payload_re)
    if alternatives is None:
        return None
    return [alternative.count(".+") for alternative in alternatives]


# --------------------------------------------------------------------------- #
# R4 — the payload validator still checks EARS for H01
# --------------------------------------------------------------------------- #


def check_spec_activation(module: Any, report: Report, specimen: Path) -> str | None:
    """R4: the spec activates ``ears`` **and** a run produces an ``ears`` entry.

    Returns the ``result`` of the produced ``ears`` check (``PASS``/``FAIL``), or
    ``None`` when the check could not be obtained. ``FAIL`` is the payload
    validator's vocabulary and is reported as evidence: a corpus-FAIL does not
    make the activation a regression, but a missing entry does.
    """
    target = VALIDATOR_REL
    triggers = getattr(module, "TRIGGERS", None)
    if not isinstance(triggers, dict):
        report.add(
            Finding(
                target,
                "R4",
                ANOMALY,
                "the payload validator declares no `TRIGGERS` table, so the `ears` "
                "spec of the H01 trigger cannot be read (R4, plan 137)",
                VALIDATOR_REF,
            )
        )
        return None
    spec = triggers.get(TRIGGER)
    if not isinstance(spec, dict):
        report.add(
            Finding(
                target,
                "R4",
                ANOMALY,
                f"the payload validator declares no `TRIGGERS[\"{TRIGGER}\"]` spec, so "
                "the activation of the `ears` check cannot be verified (R4, plan 137)",
                VALIDATOR_REF,
            )
        )
        return None
    if spec.get("ears") is not True:
        report.add(
            Finding(
                target,
                "R4",
                ANOMALY,
                f"the payload spec `TRIGGERS[\"{TRIGGER}\"]` does not activate the "
                f"`ears` check (declared `ears={spec.get('ears')!r}`), so the EARS "
                "validation H01 requires is not implemented: paridad regression "
                "(R4, plan 137)",
                VALIDATOR_REF,
            )
        )
        return None

    try:
        # The guard passes no project root: this call only reads the `ears`
        # verdict, and the validator reports the rooted checks (citations)
        # explicitly as SKIP when PROJECT_ROOT is not provided.
        checks, decision = module.validate(TRIGGER, specimen)
    except Exception as exc:  # noqa: BLE001 - any failure is a missing verdict
        report.add(
            Finding(
                target,
                "R4",
                BOUNDARY,
                f"the payload validator raised while validating the H01 specimen "
                f"({type(exc).__name__}: {exc}): the `ears` entry cannot be obtained "
                "(R4, plan 137)",
                VALIDATOR_REF,
            )
        )
        return None

    ears = [check for check in checks if check.get("id") == "ears"]
    if not ears:
        report.add(
            Finding(
                target,
                "R4",
                ANOMALY,
                "the payload spec activates `ears` for H01 but the run produced no "
                f"`ears` entry (checks: {[check.get('id') for check in checks]}): the "
                "declared activation is not materialized (R4, plan 137)",
                VALIDATOR_REF,
            )
        )
        return None
    result = str(ears[0].get("result"))
    evidence = str(ears[0].get("evidence"))
    report.add(
        Finding(
            target,
            "R4",
            VALID,
            f"the payload spec activates `ears` for H01 and the run produces it "
            f"(validator decision: {decision}; `ears` result: {result})",
            VALIDATOR_REF,
            evidence=evidence,
        )
    )
    return result


def build_specimen(module: Any, tmp_dir: Path) -> Path:
    """Write the H01 specimen the activation check is exercised on.

    The specimen is **not** a production artifact: it is built from the payload's
    own declared section list, with one EARS bullet (the standard's own
    ubiquitous form) under ``## Acceptance Criteria``, so the ``ears`` check is
    exercised and can be read. It lives in the session's temporary root, never in
    the repository.

    The section list is read defensively: a validator whose ``TRIGGERS`` table is
    absent or malformed is a payload regression the guard must *report*, so
    building the specimen may not raise on it.
    """
    sections: list[str] = []
    triggers = getattr(module, "TRIGGERS", None)
    if isinstance(triggers, dict) and isinstance(triggers.get(TRIGGER), dict):
        declared = triggers[TRIGGER].get("sections", [])
        if isinstance(declared, (list, tuple)):
            sections = [str(name) for name in declared]
    if CONTRACT_SECTION not in sections:
        sections.append(CONTRACT_SECTION)
    lines = ["# EARS coverage activation specimen", ""]
    for name in sections:
        if name == CONTRACT_SECTION:
            lines += ["## Acceptance Criteria", "", f"- The {FILLER} shall {FILLER}", ""]
        else:
            lines += [f"## {name}", "", "_Synthetic section used by the guard._", ""]
    tmp_dir.mkdir(parents=True, exist_ok=True)
    path = tmp_dir / "TASK_SPECIFICATION.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# R3 — the contract still declares the canonical form
# --------------------------------------------------------------------------- #

#: Declaration A: the bullets are the canonical form. Matched on collapsed,
#: case-folded text: ``canonical form`` + ``bullet`` in the same sentence.
_CANONICAL_DECLARATIONS = (
    re.compile(r"canonical form is one markdown bullet"),
    re.compile(r"canonical form[^.]{0,80}bullet"),
)

#: Declaration B: TOML-only criteria do not satisfy the canonical form.
_TOML_ONLY_DECLARATIONS = (
    re.compile(r"only in the toml block does not satisfy the canonical form"),
    re.compile(r"criteria[^.]{0,60}only in the toml block[^.]{0,60}does not satisfy"),
)

#: Contradictions of the canonical form, if the contract ever re-derives F-01.
_CANONICAL_CONTRADICTIONS = (
    re.compile(r"toml block is the canonical form"),
    re.compile(r"toml (?:block|array) is (?:the )?canonical"),
    re.compile(r"toml[^.]{0,40}replaces the bullets"),
    re.compile(r"toml[^.]{0,40}instead of (?:the )?bullets"),
)

#: A ``ruta:sección`` citation, in the two spellings the payload uses: the section
#: outside the backticks (``\`path\`:Section``, the payload validator's own
#: ``citation_targets`` convention) and inside them (``\`path:Section\```).
_CITATION_RE = re.compile(
    r"`(?P<path>[^`\n:]+)`\s*:\s*(?P<section>[A-Za-z][\w .-]*)"
    r"|`(?P<path_inline>[^`\n:]+):(?P<section_inline>[A-Za-z][^`\n]*)`"
)


def check_contract_coherence(payload: Path, report: Report) -> None:
    """R3: ``TASK_SPECIFICATION.md:Acceptance Criteria`` still declares the form.

    A contradiction (the TOML block re-declared canonical, or declared to
    replace the bullets) is an ``ANOMALY``; a contract that is absent, has no
    ``## Acceptance Criteria`` section, or does not make both declarations is a
    declared ``GAP`` (missing evidence), never ``VALID`` by omission.
    """
    target = f"{CONTRACT_REL}:{CONTRACT_SECTION}"
    path = payload / CONTRACT_REL
    if not path.is_file():
        report.add(
            Finding(
                target,
                "R3",
                GAP,
                "the contract is absent from the payload, so the canonical form it "
                "must declare cannot be read (missing evidence, advisory)",
                CONTRACT_REF,
            )
        )
        return
    text = _read_text(path)
    if not has_section(text, CONTRACT_SECTION):
        report.add(
            Finding(
                target,
                "R3",
                GAP,
                f"the contract declares no `## {CONTRACT_SECTION}` section, so the "
                "canonical form is not declared anywhere (missing evidence, advisory)",
                CONTRACT_REF,
            )
        )
        return
    body = collapse(section_text(text, CONTRACT_SECTION))
    if not body:
        report.add(
            Finding(
                target,
                "R3",
                GAP,
                f"`## {CONTRACT_SECTION}` is empty, so the canonical form is not "
                "declared (missing evidence, advisory)",
                CONTRACT_REF,
            )
        )
        return

    contradictions = [
        pattern.pattern for pattern in _CANONICAL_CONTRADICTIONS if pattern.search(body)
    ]
    if contradictions:
        report.add(
            Finding(
                target,
                "R3",
                ANOMALY,
                f"`## {CONTRACT_SECTION}` contradicts the canonical form it must "
                f"declare (matched {contradictions}): the contract would re-derive "
                "`F-01` (R3, plan 137)",
                CONTRACT_REF,
            )
        )
        return

    canonical = any(pattern.search(body) for pattern in _CANONICAL_DECLARATIONS)
    toml_only = any(pattern.search(body) for pattern in _TOML_ONLY_DECLARATIONS)

    # Citations the section relies on. A citation that does not resolve is
    # evidence that is *present but contradictory* (plan 137 §Contrato 10): it is
    # an ANOMALY, and it is reported even when one of the declarations is also
    # missing, because an unresolvable citation outweighs a missing declaration.
    unresolved = _unresolved_citations(section_text(text, CONTRACT_SECTION), payload)
    if unresolved:
        report.add(
            Finding(
                target,
                "R3",
                ANOMALY,
                f"`## {CONTRACT_SECTION}` cites "
                f"{len(unresolved)} source(s) that do not resolve in the payload: "
                f"{'; '.join(unresolved)}. The citation is present but contradictory, "
                "so the declaration it supports cannot be relied on (R3, plan 137)",
                CONTRACT_REF,
            )
        )
        return

    if not canonical and not toml_only:
        report.add(
            Finding(
                target,
                "R3",
                GAP,
                "the contract declares neither the Markdown-bullet form as canonical "
                "nor that TOML-only criteria do not satisfy it (missing evidence, "
                "advisory): the canonical form cannot be confirmed",
                CONTRACT_REF,
            )
        )
        return
    missing: list[str] = []
    if not canonical:
        missing.append("the Markdown-bullet form is not declared canonical")
    if not toml_only:
        missing.append(
            "TOML-only criteria are not declared insufficient for the canonical form"
        )
    if missing:
        report.add(
            Finding(
                target,
                "R3",
                GAP,
                f"`## {CONTRACT_SECTION}` declares the form only in part: "
                f"{'; '.join(missing)} (missing evidence, advisory)",
                CONTRACT_REF,
            )
        )
        return
    report.add(
        Finding(
            target,
            "R3",
            VALID,
            "the contract declares the Markdown-bullet form canonical and declares "
            "that criteria appearing only in the TOML block do not satisfy it",
            CONTRACT_REF,
        )
    )


def _unresolved_citations(text: str, payload: Path) -> list[str]:
    """Payload-relative citations of ``text`` whose file or section is absent.

    Only citations into the payload are resolved: a citation of a project path
    belongs to the corpus's own tree, not to the payload, and resolving it here
    would claim knowledge the guard does not have (plan 137 §Contrato 2: the
    sources of truth are the three payload documents).
    """
    unresolved: list[str] = []
    for match in _CITATION_RE.finditer(text):
        raw_path = (match.group("path") or match.group("path_inline") or "").strip()
        raw_section = (match.group("section") or match.group("section_inline") or "").strip()
        if not raw_path or not raw_section or raw_path.startswith("."):
            continue
        if "/" not in raw_path:
            continue
        candidate = payload / raw_path
        if not candidate.is_file():
            unresolved.append(f"`{raw_path}:{raw_section}` (file absent)")
            continue
        if not has_section(_read_text(candidate), raw_section):
            unresolved.append(f"`{raw_path}:{raw_section}` (section absent)")
    return unresolved


# --------------------------------------------------------------------------- #
# R1 / R2 — the corpus
# --------------------------------------------------------------------------- #


def resolve_corpus(root: Path, raw: str) -> Path:
    """A corpus path as given, resolved against ``--root`` when relative."""
    candidate = Path(raw)
    return candidate if candidate.is_absolute() else (root / candidate)


def check_corpus(
    specs: Sequence[Path],
    payload: Path,
    module: Any,
    mechanical: MechanicalSet,
    report: Report,
    *,
    ears_available: bool,
) -> None:
    """R1/R2 over every corpus artifact, in the given (sorted) order."""
    for path in specs:
        citation = _citation(path)
        if not path.is_file():
            report.add(
                Finding(
                    citation,
                    "R1",
                    NOT_APPLICABLE,
                    "the corpus path does not exist: declared absence, nothing is "
                    "claimed about it (N/A, plan 137 §Contrato 9)",
                    POLICY_REF,
                )
            )
            report.add(
                Finding(
                    citation,
                    "R2",
                    NOT_APPLICABLE,
                    "the corpus path does not exist: declared absence, so no bullet "
                    "can be evaluated (N/A, plan 137 §Contrato 9)",
                    EARS_REF,
                )
            )
            continue

        text = _read_text(path)
        if not has_section(text, CONTRACT_SECTION):
            report.add(
                Finding(
                    citation,
                    "R1",
                    GAP,
                    f"the artifact declares no `## {CONTRACT_SECTION}` section, so no "
                    "bullet can be evaluated (missing evidence, never `VALID` by "
                    "emptiness)",
                    POLICY_REF,
                )
            )
            report.add(
                Finding(
                    citation,
                    "R2",
                    NOT_APPLICABLE,
                    f"no `## {CONTRACT_SECTION}` section, so there is no bullet to "
                    "match against a pattern (declared absence)",
                    EARS_REF,
                )
            )
            continue

        bullets = acceptance_bullets(text)
        if not bullets:
            report.add(
                Finding(
                    citation,
                    "R1",
                    GAP,
                    f"`## {CONTRACT_SECTION}` contains no bullet (`-`/`*`): the "
                    "canonical form is not materialized (missing evidence, never "
                    "`VALID` by emptiness). Criteria present only in the "
                    "`acceptance_criteria` TOML block are this violation",
                    POLICY_REF,
                )
            )
            report.add(
                Finding(
                    citation,
                    "R2",
                    NOT_APPLICABLE,
                    "there is no bullet to match against a pattern (declared absence)",
                    EARS_REF,
                )
            )
            continue

        report.add(
            Finding(
                citation,
                "R1",
                VALID,
                f"`## {CONTRACT_SECTION}` contains {len(bullets)} bullet(s), so the "
                "canonical form is materialized",
                POLICY_REF,
                evidence=f"{len(bullets)} bullet(s)",
            )
        )
        _check_bullets(citation, path, bullets, module, mechanical, report, ears_available)


def _check_bullets(
    citation: str,
    path: Path,
    bullets: Sequence[str],
    module: Any,
    mechanical: MechanicalSet,
    report: Report,
    ears_available: bool,
) -> None:
    """R2 for one artifact: the payload validator's verdict, per bullet."""
    if not ears_available:
        report.add(
            Finding(
                citation,
                "R2",
                GAP,
                "the payload validator produced no `ears` verdict for H01 (see the R4 "
                "finding), so no bullet can be evaluated against the patterns "
                "(missing evidence, advisory)",
                CORPUS_REF,
            )
        )
        return

    try:
        # The guard passes no project root: it only reads the `ears` verdict.
        checks, _ = module.validate(TRIGGER, path)
    except Exception as exc:  # noqa: BLE001 - any failure is a missing verdict
        report.add(
            Finding(
                citation,
                "R2",
                BOUNDARY,
                f"the payload validator raised while validating this artifact "
                f"({type(exc).__name__}: {exc}): the `ears` verdict cannot be obtained "
                "(R2, plan 137)",
                EARS_REF,
            )
        )
        return
    ears = [check for check in checks if check.get("id") == "ears"]
    if not ears:
        report.add(
            Finding(
                citation,
                "R2",
                ANOMALY,
                "the payload validator produced no `ears` entry for an artifact with "
                "acceptance-criteria bullets, though the H01 spec activates the check "
                "(R2, plan 137)",
                EARS_REF,
            )
        )
        return

    result = str(ears[0].get("result"))
    evidence = str(ears[0].get("evidence"))
    if result != "PASS":
        report.add(
            Finding(
                citation,
                "R2",
                ANOMALY,
                f"{len(bullets)} bullet(s) present and the payload validator's `ears` "
                f"check reports FAIL: {evidence} (the validator's vocabulary is "
                "reported as evidence, never produced here)",
                EARS_REF,
                evidence=evidence,
            )
        )
        return

    # Corroboration of the validator's PASS against the set derived from the
    # standard: the payload's own regex must accept each bullet too, and each
    # accepted bullet must be built from a declared pattern. A bullet the payload
    # accepts but no declared template covers would be a false positive of the
    # validator, which is an `ANOMALY` and not a silent pass.
    payload_rejected: list[str] = []
    free_rejected: list[str] = []
    for bullet in bullets:
        if not mechanical.payload_re.match(bullet):
            payload_rejected.append(bullet)
        elif not any(regex.match(bullet) for regex in mechanical.free):
            free_rejected.append(bullet)

    if payload_rejected:
        report.add(
            Finding(
                citation,
                "R2",
                ANOMALY,
                "the payload validator reports `ears` PASS for bullet(s) its own "
                f"`EARS_RE` rejects: {payload_rejected}. The two verdicts of the same "
                "run contradict each other (R2, plan 137)",
                EARS_REF,
            )
        )
        return

    if free_rejected:
        report.add(
            Finding(
                citation,
                "R2",
                ANOMALY,
                "the payload validator accepts bullet(s) that match none of the "
                f"patterns the standard declares: {free_rejected} (false positive of "
                "the validator, R2/R5, plan 137)",
                EARS_REF,
            )
        )
        return

    report.add(
        Finding(
            citation,
            "R2",
            VALID,
            f"all {len(bullets)} bullet(s) are accepted by the payload validator's "
            "`ears` check and by the pattern set derived from the standard (the "
            "validator's PASS is reported as evidence)",
            EARS_REF,
            evidence=evidence,
        )
    )


def _citation(path: Path) -> str:
    return f"{path.name}:{CONTRACT_SECTION}"


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #


def render_text(report: Report, mechanical: MechanicalSet) -> str:
    lines = [
        "EARS coverage and parity check (plan 137):",
        "- mechanical subset (established; source of each rule):",
    ]
    for rule, description, source in MECHANICAL_SUBSET:
        lines.append(f"    - {rule}: {description} — {source}")
    lines.append("- excluded subset (declared judgement; never ruled on):")
    for description, classification in EXCLUDED_SUBSET:
        lines.append(f"    - {description} — {classification}")
    lines.append("- results:")
    for target, signal, items in report.per_target():
        lines.append(f"    - {target}: {signal} - {items[0].reason}")
        for item in items[1:]:
            lines.append(f"        - {item.rule}: {item.signal}: {item.reason}")
    counts = report.counts()
    summary = ", ".join(
        f"{signal}={counts[signal]}" for signal in _SIGNAL_PRECEDENCE if counts[signal]
    )
    lines.append(f"Summary: {summary or 'no artifacts inspected'}")
    return "\n".join(lines)


def render_json(report: Report, mechanical: MechanicalSet) -> str:
    payload = {
        "tool": "check_ears_coverage",
        "plan": 137,
        "ears_scope": (
            "mechanical subset: canonical bullet form, payload `ears` verdict, "
            "contract declaration and pattern parity; judgement items excluded"
        ),
        "mechanical_subset": [
            {"rule": rule, "check": description, "source": source}
            for rule, description, source in MECHANICAL_SUBSET
        ],
        "excluded_subset": [
            {"check": description, "classification": classification}
            for description, classification in EXCLUDED_SUBSET
        ],
        "patterns": [pattern.to_dict() for pattern in mechanical.patterns],
        "results": [finding.to_dict() for finding in report.findings],
        "per_target": [
            {"target": target, "signal": signal, "findings": len(items)}
            for target, signal, items in report.per_target()
        ],
        "counts": report.counts(),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python tools/check_ears_coverage.py",
        description=(
            "Audit EARS coverage and guard the parity of the payload's mechanical "
            "EARS subset; invokes the payload validator, never reimplements it."
        ),
    )
    parser.add_argument(
        "--payload",
        type=Path,
        default=Path("protocol") / ".agents",
        help="protocol payload root (default: protocol/.agents)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="project root a relative --corpus resolves against (default: .)",
    )
    parser.add_argument(
        "--corpus",
        action="append",
        default=[],
        metavar="PATH",
        help="TASK_SPECIFICATION.md (or a fragment with ## Acceptance Criteria) to "
        "audit; repeatable. Without it, R1/R2 are an explicit N/A",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def run(args: argparse.Namespace) -> int:
    """Evaluate R1-R5 and print the report; returns the exit code."""
    root = args.root.resolve()
    payload = args.payload if args.payload.is_absolute() else (root / args.payload)
    payload = payload.resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    module = load_validator(payload)
    mechanical = load_mechanical_set(payload, module)
    report = Report()

    check_pattern_parity(mechanical, report)

    tmp_dir = _session_temp_dir()
    ears_result: str | None = None
    try:
        specimen = build_specimen(module, tmp_dir)
    except OSError as exc:
        report.add(
            Finding(
                VALIDATOR_REL,
                "R4",
                BOUNDARY,
                f"the activation specimen could not be written ({exc}), so the `ears` "
                "check could not be exercised (R4, plan 137)",
                VALIDATOR_REF,
            )
        )
    else:
        ears_result = check_spec_activation(module, report, specimen)
    check_contract_coherence(payload, report)

    if args.corpus:
        specs = sorted(
            (resolve_corpus(root, raw) for raw in args.corpus),
            key=lambda path: path.as_posix(),
        )
        check_corpus(
            specs,
            payload,
            module,
            mechanical,
            report,
            ears_available=ears_result is not None,
        )
    else:
        for rule, source, text in (
            (
                "R1",
                POLICY_REF,
                "no `--corpus` was given, so no artifact with acceptance criteria was "
                "audited (declared absence, N/A; plan 137 §Contrato 1)",
            ),
            (
                "R2",
                EARS_REF,
                "no `--corpus` was given, so no bullet could be matched against a "
                "pattern (declared absence, N/A; plan 137 §Contrato 1)",
            ),
        ):
            report.add(Finding(CORPUS_REF, rule, NOT_APPLICABLE, text, source))

    print(render_json(report, mechanical) if args.json else render_text(report, mechanical))
    return 1 if report.has_anomaly else 0


def _session_temp_dir() -> Path:
    """A throw-away directory outside the repository for the H01 specimen.

    The repository convention is that no temporary is written inside the working
    tree (``tests/AGENTS.md``): the specimen goes to the platform temp directory,
    under the same session root the test suites use when it is set.
    """
    import os
    import tempfile

    override = os.environ.get("ARGENTOS_PYTEST_TMP", "").strip()
    base = Path(override).expanduser() if override else Path(tempfile.gettempdir())
    return base / "argentos-ears-coverage"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except ReadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
