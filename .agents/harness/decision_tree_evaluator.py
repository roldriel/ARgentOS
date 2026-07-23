#!/usr/bin/env python3
"""
Pure decision-tree evaluator for .agents recovery policies.

The evaluator is stateless, file-system agnostic, and does not use ``eval``,
``exec`` or ``compile``. It receives a parsed TOML tree and a variable map,
and returns the resulting action.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


class DecisionTreeError(Exception):
    """Base exception for decision-tree errors."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


# ---------------------------------------------------------------------------
# Safe condition parser
# ---------------------------------------------------------------------------

TOKEN_SPEC = [
    ("STRING", r'"(?:[^"\\]|\\.)*"|' r"'(?:[^'\\]|\\.)*'"),
    ("NUMBER", r"\d+(?:\.\d+)?"),
    ("OP_EQ", r"=="),
    ("OP_NE", r"!="),
    ("OP_LE", r"<="),
    ("OP_GE", r">="),
    ("OP_LT", r"<"),
    ("OP_GT", r">"),
    ("AND", r"\band\b"),
    ("OR", r"\bor\b"),
    ("NOT", r"\bnot\b"),
    ("IN", r"\bin\b"),
    ("TRUE", r"\btrue\b"),
    ("FALSE", r"\bfalse\b"),
    ("NULL", r"\bnull\b"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP", r"[ \t]+"),
]
TOKEN_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)


@dataclass
class Token:
    type: str
    value: Any


def tokenize(expr: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    while pos < len(expr):
        match = TOKEN_RE.match(expr, pos)
        if not match:
            raise DecisionTreeError(
                "INVALID_CONDITION",
                f"Unexpected character at position {pos}: {expr[pos:]!r}",
            )
        kind = match.lastgroup
        value = match.group()
        pos = match.end()
        if kind == "SKIP":
            continue
        if kind == "NUMBER":
            value = float(value) if "." in value else int(value)
        elif kind == "STRING":
            value = value[1:-1]
        elif kind in ("TRUE", "FALSE"):
            value = kind == "TRUE"
            kind = "BOOL"
        elif kind == "NULL":
            value = None
        tokens.append(Token(kind, value))
    return tokens


# AST nodes
@dataclass
class Compare:
    left: Any
    op: str
    right: Any


@dataclass
class BoolOp:
    op: str
    operands: list[Any]


@dataclass
class Not:
    operand: Any


@dataclass
class In:
    left: Any
    right: Any


@dataclass
class Var:
    name: str


class ConditionParser:
    """Recursive-descent parser for the restricted condition grammar."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected: str | None = None) -> Token:
        token = self.peek()
        if token is None:
            raise DecisionTreeError("INVALID_CONDITION", "Unexpected end of expression")
        if expected and token.type != expected:
            raise DecisionTreeError(
                "INVALID_CONDITION",
                f"Expected {expected}, got {token.type} ({token.value!r})",
            )
        self.pos += 1
        return token

    def parse(self) -> Any:
        if not self.tokens:
            raise DecisionTreeError("INVALID_CONDITION", "Empty condition")
        node = self.parse_or()
        if self.peek() is not None:
            raise DecisionTreeError("INVALID_CONDITION", "Unexpected trailing tokens")
        return node

    def parse_or(self) -> Any:
        left = self.parse_and()
        while self.peek() and self.peek().type == "OR":
            self.consume("OR")
            right = self.parse_and()
            left = BoolOp("or", [left, right])
        return left

    def parse_and(self) -> Any:
        left = self.parse_not()
        while self.peek() and self.peek().type == "AND":
            self.consume("AND")
            right = self.parse_not()
            left = BoolOp("and", [left, right])
        return left

    def parse_not(self) -> Any:
        if self.peek() and self.peek().type == "NOT":
            self.consume("NOT")
            return Not(self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self) -> Any:
        left = self.parse_primary()
        if self.peek() and self.peek().type in (
            "OP_EQ",
            "OP_NE",
            "OP_LT",
            "OP_GT",
            "OP_LE",
            "OP_GE",
        ):
            op = self.consume().value
            right = self.parse_primary()
            return Compare(left, op, right)
        if self.peek() and self.peek().type == "IN":
            self.consume("IN")
            right = self.parse_primary()
            return In(left, right)
        return left

    def parse_primary(self) -> Any:
        token = self.peek()
        if token is None:
            raise DecisionTreeError("INVALID_CONDITION", "Unexpected end of expression")
        if token.type == "LPAREN":
            self.consume("LPAREN")
            node = self.parse_or()
            self.consume("RPAREN")
            return node
        if token.type == "IDENT":
            self.consume("IDENT")
            return Var(token.value)
        if token.type in ("NUMBER", "STRING", "BOOL", "NULL"):
            self.consume()
            return token.value
        raise DecisionTreeError(
            "INVALID_CONDITION",
            f"Unexpected token {token.type} ({token.value!r})",
        )


def parse_condition(expr: str) -> Any:
    tokens = tokenize(expr)
    return ConditionParser(tokens).parse()


def evaluate(node: Any, variables: dict[str, Any]) -> Any:
    """Evaluate a parsed AST node against the variable map."""
    if isinstance(node, Var):
        return variables.get(node.name)
    if isinstance(node, Compare):
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        if node.op == "==":
            return left == right
        if node.op == "!=":
            return left != right
        if left is None or right is None:
            raise DecisionTreeError(
                "MISSING_VARIABLE",
                f"Cannot compare missing variable in condition",
            )
        if node.op == "<":
            return left < right
        if node.op == ">":
            return left > right
        if node.op == "<=":
            return left <= right
        if node.op == ">=":
            return left >= right
        raise DecisionTreeError("INVALID_CONDITION", f"Unknown operator {node.op}")
    if isinstance(node, BoolOp):
        values = [evaluate(operand, variables) for operand in node.operands]
        if node.op == "and":
            return all(values)
        if node.op == "or":
            return any(values)
        raise DecisionTreeError(
            "INVALID_CONDITION", f"Unknown boolean operator {node.op}"
        )
    if isinstance(node, Not):
        return not evaluate(node.operand, variables)
    if isinstance(node, In):
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        if not isinstance(right, list):
            raise DecisionTreeError(
                "INVALID_CONDITION", "'in' requires a list on the right side"
            )
        return left in right
    return node


# ---------------------------------------------------------------------------
# Tree evaluation
# ---------------------------------------------------------------------------

REQUIRED_ACTION_PARAMS: dict[str, list[str]] = {
    "RETRY_WORKER": ["target_phase", "role"],
    "NEEDS_CLARIFICATION": [],
    "RECOVERY_GENERIC": ["target_phase"],
    "ABORT": [],
}

DEFAULT_RECOVERY = {
    "action": "RECOVERY_GENERIC",
    "params": {"target_phase": "08-recovery.md"},
}

CRITICAL_VARIABLES = ["trigger", "artifact_exists", "retry_count"]

OPTIONAL_DEFAULTS: dict[type, Any] = {
    bool: False,
    int: 0,
    float: 0.0,
    list: [],
    str: "",
}


@dataclass
class DecisionResult:
    trigger: str
    result: str  # DECISION, ERROR, INCONCLUSIVE
    action: str | None = None
    params: dict[str, Any] = field(default_factory=dict)
    path: list[str] = field(default_factory=list)
    reason: str = ""
    input_vars: dict[str, Any] = field(default_factory=dict)
    error: dict[str, str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger,
            "result": self.result,
            "action": self.action,
            "params": self.params,
            "path": self.path,
            "reason": self.reason,
            "input_vars": self.input_vars,
            "error": self.error,
        }


def _prepare_variables(input_vars: dict[str, Any]) -> dict[str, Any]:
    """Merge provided variables with sensible defaults for optional booleans/numbers."""
    variables = dict(input_vars)
    for name in CRITICAL_VARIABLES:
        if name not in variables:
            raise DecisionTreeError(
                "MISSING_VARIABLE", f"Critical variable '{name}' not provided"
            )

    # Apply defaults only when the type is obvious from a declared hint; here we
    # keep it conservative: known optional booleans default to False. This list
    # covers every boolean variable referenced by the core and discovery
    # decision trees (see the VARIABLES.md next to each tree set).
    known_booleans = [
        "artifact_exists",
        "context_contradictory",
        "context_user_specific",
        "correction_cycle_exceeded",
        "execution_blocked",
        "execution_complete",
        "failures_fixable",
        "failures_require_user",
        "gaps_actionable",
        "merge_inconsistent",
        "objective_is_ambiguous",
        "plan_depends_on_user",
        "plan_out_of_scope",
        "project_unrecoverable",
        "request_is_ambiguous",
        "scope_compliant",
        "scope_expansion_requested",
        "scope_is_clear",
        "scope_violation_severe",
        "secrets_leaked",
        "task_fundamentally_unachievable",
        "unsourced_claims_found",
        "user_rejected",
        "user_unclear",
    ]
    for name in known_booleans:
        if name not in variables:
            variables[name] = False
    return variables


def _validate_tree(tree: dict[str, Any]) -> None:
    """Validate the structural integrity of the decision tree."""
    nodes = tree.get("nodes", {})
    if "start" not in nodes:
        raise DecisionTreeError("INVALID_TREE", "Missing required node 'start'")

    for node_id, node in nodes.items():
        if "condition" not in node:
            raise DecisionTreeError(
                "INVALID_TREE", f"Node '{node_id}' missing 'condition'"
            )
        for branch_name in ("true", "false"):
            branch = node.get(branch_name)
            if branch is None:
                raise DecisionTreeError(
                    "INVALID_TREE", f"Node '{node_id}' missing '{branch_name}' branch"
                )
            has_next = "next" in branch
            has_action = "action" in branch
            if not (has_next ^ has_action):
                raise DecisionTreeError(
                    "INVALID_TREE",
                    f"Branch '{branch_name}' of node '{node_id}' must have exactly one of 'next' or 'action'",
                )
            if has_next and branch["next"] not in nodes:
                raise DecisionTreeError(
                    "UNREACHABLE_NODE",
                    f"Node '{node_id}' references unknown node '{branch['next']}'",
                )

    # Cycle detection
    for start in nodes:
        stack: list[tuple[str, list[str]]] = [(start, [])]
        while stack:
            node_id, trace = stack.pop()
            if node_id in trace:
                cycle = " -> ".join(trace[trace.index(node_id) :] + [node_id])
                raise DecisionTreeError("CYCLE_DETECTED", f"Cycle detected: {cycle}")
            node = nodes.get(node_id, {})
            for branch_name in ("true", "false"):
                branch = node.get(branch_name, {})
                nxt = branch.get("next")
                if nxt is not None:
                    stack.append((nxt, trace + [node_id]))


def _validate_action(action: str, params: dict[str, Any]) -> None:
    """Validate that the action is known and required parameters are present."""
    if action not in REQUIRED_ACTION_PARAMS:
        raise DecisionTreeError("INVALID_ACTION", f"Unknown action '{action}'")
    for required in REQUIRED_ACTION_PARAMS[action]:
        if required not in params:
            raise DecisionTreeError(
                "INVALID_ACTION",
                f"Action '{action}' missing required parameter '{required}'",
            )


def evaluate_tree(tree: dict[str, Any], input_vars: dict[str, Any]) -> DecisionResult:
    """Evaluate a decision tree against the provided variables."""
    trigger = input_vars.get(
        "trigger", tree.get("metadata", {}).get("trigger", "UNKNOWN")
    )
    try:
        _validate_tree(tree)
        variables = _prepare_variables(input_vars)
    except DecisionTreeError as exc:
        result = DecisionResult(
            trigger=trigger,
            result="ERROR",
            path=[],
            input_vars=input_vars,
            error={"code": exc.code, "message": exc.message},
        )
        result.action = DEFAULT_RECOVERY["action"]
        result.params = dict(DEFAULT_RECOVERY["params"])
        result.reason = f"{exc.code}: {exc.message}; falling back to generic recovery."
        return result

    nodes = tree["nodes"]
    current = "start"
    path: list[str] = []
    visited: set[str] = set()

    while True:
        if current in visited:
            # Should have been caught by validation, but guard anyway.
            cycle_node = current
            result = DecisionResult(
                trigger=trigger,
                result="ERROR",
                path=path,
                input_vars=variables,
                error={
                    "code": "CYCLE_DETECTED",
                    "message": f"Looping at node '{cycle_node}'",
                },
            )
            result.action = DEFAULT_RECOVERY["action"]
            result.params = dict(DEFAULT_RECOVERY["params"])
            result.reason = (
                "Cycle detected during evaluation; falling back to generic recovery."
            )
            return result
        visited.add(current)

        if current not in nodes:
            result = DecisionResult(
                trigger=trigger,
                result="ERROR",
                path=path,
                input_vars=variables,
                error={
                    "code": "UNREACHABLE_NODE",
                    "message": f"Node '{current}' not found",
                },
            )
            result.action = DEFAULT_RECOVERY["action"]
            result.params = dict(DEFAULT_RECOVERY["params"])
            result.reason = (
                "Unreachable node during evaluation; falling back to generic recovery."
            )
            return result

        node = nodes[current]
        path.append(current)

        try:
            condition_ast = parse_condition(node["condition"])
            condition_value = evaluate(condition_ast, variables)
            if not isinstance(condition_value, bool):
                raise DecisionTreeError(
                    "INVALID_CONDITION",
                    f"Condition in node '{current}' did not evaluate to a boolean",
                )
        except DecisionTreeError as exc:
            result = DecisionResult(
                trigger=trigger,
                result="ERROR",
                path=path,
                input_vars=variables,
                error={"code": exc.code, "message": exc.message},
            )
            result.action = DEFAULT_RECOVERY["action"]
            result.params = dict(DEFAULT_RECOVERY["params"])
            result.reason = (
                f"{exc.code}: {exc.message}; falling back to generic recovery."
            )
            return result

        branch_name = "true" if condition_value else "false"
        branch = node.get(branch_name)
        if branch is None:
            result = DecisionResult(
                trigger=trigger,
                result="INCONCLUSIVE",
                path=path,
                input_vars=variables,
            )
            result.action = DEFAULT_RECOVERY["action"]
            result.params = dict(DEFAULT_RECOVERY["params"])
            result.reason = "Branch missing; falling back to generic recovery."
            return result

        if "action" in branch:
            action = branch["action"]
            params = {k: v for k, v in branch.items() if k not in ("action",)}
            try:
                _validate_action(action, params)
            except DecisionTreeError as exc:
                result = DecisionResult(
                    trigger=trigger,
                    result="ERROR",
                    path=path,
                    input_vars=variables,
                    error={"code": exc.code, "message": exc.message},
                )
                result.action = DEFAULT_RECOVERY["action"]
                result.params = dict(DEFAULT_RECOVERY["params"])
                result.reason = (
                    f"{exc.code}: {exc.message}; falling back to generic recovery."
                )
                return result

            reason = branch.get("reason", f"Decision reached at node '{current}'")
            return DecisionResult(
                trigger=trigger,
                result="DECISION",
                action=action,
                params=params,
                path=path,
                reason=reason,
                input_vars=variables,
            )

        current = branch["next"]
