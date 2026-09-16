"""Mechanical realization of the Repository/Artifact Placement Contract.

This module does **not** own the placement rules: it realizes the rule table
published in ``docs/placement-contract.md`` §6 (and the algorithm of §7) so that
a caller can obtain a deterministic ``PLACE`` or ``STOP`` invitation instead of
inventing a path.

Two invariants of that contract are load-bearing here and must not be weakened:

- **Canonicality is a qualifier, never a discriminator** (§5). It never selects
  and never creates a namespace.
- **Kind is not a global closed enum** (§4, ``PC-8``/``PC-10``). The family
  vocabulary is domain-scoped, and a kind that resolves to no family rule
  produces ``STOP`` (``NEW_FAMILY``) — never a guess by similarity.

``FAMILIES`` is a re-expression of the contract's tables, not a second source of
truth. It is kept in lockstep with the contract by the drift guard in
``tests/test_placement_contract_drift.py``, which fails if either side changes
without the other.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

#: Repository-relative path of the normative source this module realizes.
CONTRACT_PATH = "docs/placement-contract.md"

#: The contract sections this module implements, cited as ``ruta:sección``.
CONTRACT_SECTIONS = {
    "domain": f"{CONTRACT_PATH}:3. Domain / owner identification",
    "kind": f"{CONTRACT_PATH}:4. Kind / family identification",
    "canonicality": f"{CONTRACT_PATH}:5. Canonicality qualification",
    "namespace": f"{CONTRACT_PATH}:6. Namespace selection",
    "algorithm": f"{CONTRACT_PATH}:7. Placement resolution algorithm",
    "stop": f"{CONTRACT_PATH}:8. STOP semantics",
    "exceptions": f"{CONTRACT_PATH}:9. Exceptions",
    "lifetime": f"{CONTRACT_PATH}:21. Project-durable state and Git persistence",
    "agent": f"{CONTRACT_PATH}:16. Agent responsibilities",
}

#: The two artifact domains of the contract (§3, ``PC-3``).
DOMAIN_DEV = "DEV"
DOMAIN_PROTOCOL = "Protocol"
DOMAINS = (DOMAIN_DEV, DOMAIN_PROTOCOL)

#: Canonicality statuses (§5, ``PC-13``). Qualifiers only.
CANONICALITY_SOURCE = "source-of-truth"
CANONICALITY_DERIVED = "derived"
CANONICALITY_GENERATED = "generated"
CANONICALITY_HISTORICAL = "historical"
CANONICALITY_FIXTURE = "fixture"
CANONICALITY_SCRATCH = "scratch"
CANONICALITIES = (
    CANONICALITY_SOURCE,
    CANONICALITY_DERIVED,
    CANONICALITY_GENERATED,
    CANONICALITY_HISTORICAL,
    CANONICALITY_FIXTURE,
    CANONICALITY_SCRATCH,
)


@dataclass(frozen=True)
class Namespace:
    """One canonical location of a family rule (§6).

    ``prefix`` is true when the location is a directory that contains the
    artifact; false when the location *is* the artifact (a single file whose
    path the contract fixes, e.g. ``conftest.py``).

    ``flat`` distinguishes the two directory forms the contract publishes:
    ``docs/rfc/`` **flat** holds the files directly inside it, while the
    unqualified form (``tests/``) also holds its subdirectories. It exists so a
    rule is never broader than the namespace the contract actually declares.
    """

    path: str
    prefix: bool = True
    flat: bool = False

    def contains(self, candidate: str) -> bool:
        normalized = candidate.replace("\\", "/").strip("/")
        root = self.path.rstrip("/")
        if not self.prefix:
            return normalized == root
        if normalized == root:
            return True
        if not normalized.startswith(f"{root}/"):
            return False
        remainder = normalized[len(root) + 1 :]
        return "/" not in remainder if self.flat else True


@dataclass(frozen=True)
class FamilyRule:
    """One row of the contract's §6 rule table, with its provenance."""

    family: str
    domain: str
    namespaces: tuple[Namespace, ...]
    distributed: bool
    canonicality: tuple[str, ...]
    kinds: tuple[str, ...]
    section: str


def _dev(
    family: str,
    namespace: str,
    kinds: tuple[str, ...],
    *,
    prefix: bool = True,
    flat: bool = False,
    status: tuple[str, ...] = (CANONICALITY_SOURCE,),
) -> FamilyRule:
    return FamilyRule(
        family=family,
        domain=DOMAIN_DEV,
        namespaces=(Namespace(namespace, prefix, flat),),
        distributed=False,
        canonicality=status,
        kinds=kinds,
        section=CONTRACT_SECTIONS["namespace"],
    )


#: DEV families — realizes the contract's "DEV families" table (§6). The table's
#: namespace cell can name several locations for one family; each is realized as
#: its own rule because a kind must resolve to exactly one namespace.
FAMILIES: tuple[FamilyRule, ...] = (
    # `docs/*.md` (root): the contract confines this family to the root files of
    # `docs/`, so the rule is flat and refuses `docs/<subdir>/x.md`.
    _dev("Normative policy", "docs", ("policy", "normative-policy"), flat=True),
    _dev(
        "Operational policy",
        ".agents/policies",
        ("operational-instruction", "dev-policy", "operational"),
    ),
    _dev("Operational workflow", ".agents/workflows", ("dev-workflow", "workflow")),
    _dev("RFC", "docs/rfc", ("rfc",), flat=True),
    _dev("ADR", "docs/adr", ("adr",), flat=True),
    _dev("Plan", "docs/plans", ("plan",), flat=True),
    _dev(
        "Working analysis",
        "docs/working",
        ("working", "audit", "research", "proposal", "working-analysis"),
    ),
    _dev(
        "Inventory / descriptive registry",
        "docs/glossary",
        ("inventory", "glossary", "descriptive-registry"),
    ),
    _dev(
        "Navigation / INDEX",
        "docs",
        ("index", "navigation"),
        status=(CANONICALITY_DERIVED,),
    ),
    _dev("Verification executable", "tools", ("tool", "verification-executable")),
    _dev("Reference runtime", "runtime", ("runtime", "reference-runtime")),
    _dev(
        "Test subsystem",
        "tests",
        ("test", "tests", "test-suite"),
        status=(CANONICALITY_SOURCE, CANONICALITY_FIXTURE),
    ),
    _dev(
        "Test fixture",
        "tests/fixtures",
        ("fixture", "test-fixture"),
        status=(CANONICALITY_FIXTURE,),
    ),
    # Protocol families (§6, "Protocol families" / "Payload specification and
    # capability"). The contract names one family per sub-namespace, so each
    # sub-namespace is realized as its own rule: a kind must resolve to exactly
    # one namespace, and a rule that yielded several would be TWO_VALID_LOCATIONS.
    *(
        FamilyRule(
            family=f"Payload {label}",
            domain=DOMAIN_PROTOCOL,
            namespaces=(Namespace(f"protocol/.agents/{slug}"),),
            distributed=True,
            canonicality=(CANONICALITY_SOURCE,),
            kinds=kinds,
            section=CONTRACT_SECTIONS["namespace"],
        )
        for label, slug, kinds in (
            ("contracts", "contracts", ("contract",)),
            ("delegation contract", "delegation", ("delegation",)),
            ("standards", "standards", ("standard", "standard-rule")),
            ("orchestrator data", "orchestrators", ("workflow", "state-machine", "orchestrator")),
            ("roles and profiles", "roles", ("role", "profile", "worker")),
            ("skills", "skills", ("skill", "capability")),
        )
    ),
    FamilyRule(
        family="Payload executable harness",
        domain=DOMAIN_PROTOCOL,
        namespaces=(Namespace("protocol/.agents/harness"),),
        distributed=True,
        canonicality=(CANONICALITY_SOURCE,),
        kinds=("harness", "harness-policy", "harness-test"),
        section=CONTRACT_SECTIONS["namespace"],
    ),
    # Project / session state (§6, "Project / session state" table).
    FamilyRule(
        family="Session execution state",
        domain=DOMAIN_PROTOCOL,
        namespaces=(Namespace(".project/orchestrator"),),
        distributed=False,
        # The host designates this namespace as its evidence area, which is the
        # explicit designation PC-47 requires for generated content.
        canonicality=(CANONICALITY_GENERATED,),
        kinds=("run-log", "session-artifact", "delegation-record", "worker-result"),
        section=CONTRACT_SECTIONS["lifetime"],
    ),
    # Project-durable state (§6, "Project / session state" table). The contract
    # designates two durable namespaces; each is realized as its own rule so a
    # kind maps to exactly one, and the Git-persistence decision of §21 is
    # recorded as metadata rather than as a placement.
    *(
        FamilyRule(
            family=label,
            domain=DOMAIN_PROTOCOL,
            namespaces=(Namespace(path),),
            distributed=False,
            canonicality=(CANONICALITY_SOURCE,),
            kinds=kinds,
            section=CONTRACT_SECTIONS["lifetime"],
        )
        for label, path, kinds in (
            (
                "Project-durable change governance",
                ".project/changes",
                ("change-governance", "governance-artifact"),
            ),
            (
                "Project-durable knowledge base",
                ".project/knowledge",
                ("knowledge-base", "knowledge-entry", "project-durable"),
            ),
        )
    ),
)

#: Root-anchored placements (§6, "Root-anchored placements" table). These are
#: not families: their location is dictated by an external convention or tool,
#: not by a domain-scoped kind lookup.
ROOT_ANCHORED: dict[str, Namespace] = {
    "entrypoint": Namespace("README.md", prefix=False),
    "conftest": Namespace("conftest.py", prefix=False),
    "ci-configuration": Namespace(".github/workflows", prefix=True),
}

#: Artifacts whose path the contract fixes exactly, mapped to their namespace.
EXACT_ARTIFACTS: tuple[tuple[str, Namespace], ...] = (
    ("AGENTS.md", Namespace("AGENTS.md", prefix=False)),
    # `.agents/AGENTS.md` is named by the "Operational instruction" row (§6) as one
    # of three fixed locations, not as a directory family: the operational layer's
    # entry point is pinned, while its policy and workflow directories are
    # families of their own.
    (".agents/AGENTS.md", Namespace(".agents/AGENTS.md", prefix=False)),
    ("README.md", Namespace("README.md", prefix=False)),
    ("CHANGELOG.md", Namespace("CHANGELOG.md", prefix=False)),
    ("ROADMAP.md", Namespace("ROADMAP.md", prefix=False)),
    ("LICENSE", Namespace("LICENSE", prefix=False)),
    ("conftest.py", Namespace("conftest.py", prefix=False)),
    ("runtime/README.md", Namespace("runtime/README.md", prefix=False)),
)


def family_by_name(name: str) -> FamilyRule | None:
    """Resolve a family by exact (case-insensitive) name within the vocabulary."""
    wanted = name.strip().casefold()
    for rule in FAMILIES:
        if rule.family.casefold() == wanted:
            return rule
    return None


def families_for_kind(domain: str, kind: str) -> tuple[FamilyRule, ...]:
    """Every family of ``domain`` whose declared kind set contains ``kind``."""
    wanted = kind.strip().casefold()
    return tuple(
        rule
        for rule in FAMILIES
        if rule.domain == domain and wanted in {k.casefold() for k in rule.kinds}
    )


def find_exact_artifact(candidate: str) -> Namespace | None:
    """The fixed namespace of a path the contract pins to one exact file."""
    normalized = candidate.replace("\\", "/").strip("/")
    for path, namespace in EXACT_ARTIFACTS:
        if normalized == path:
            return namespace
    return None


def repo_root() -> Path:
    """This repository's root, derived from this file's location."""
    return Path(__file__).resolve().parents[2]
