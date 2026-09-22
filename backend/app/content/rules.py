"""Deterministic evaluation of red-flag rules over filled slots.

Rules are small boolean expressions over dotted slot ids, for example
    cp.onset == 'abrupt' and cp.quality in ['tearing', 'ripping'] and 'back' in cp.radiation
They are parsed with Python's ast and evaluated with no names, calls or attributes
other than dotted slot ids. An unfilled slot makes the rule undecidable rather than
false: the result reports the missing slot ids so the handover can say "not asked".
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field


class RuleError(ValueError):
    pass


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else None
    return None


def referenced_slot_ids(expr: str) -> list[str]:
    tree = ast.parse(expr, mode="eval")
    ids: list[str] = []

    def walk(n: ast.AST) -> None:
        d = _dotted(n)
        if d is not None and isinstance(n, (ast.Name, ast.Attribute)):
            if d not in ids:
                ids.append(d)
            return
        for child in ast.iter_child_nodes(n):
            walk(child)

    walk(tree.body)
    return ids


@dataclass
class RuleResult:
    fired: bool
    missing: list[str] = field(default_factory=list)


class _Missing(Exception):
    def __init__(self, slot_id: str):
        self.slot_id = slot_id


def evaluate(expr: str, values: dict[str, object]) -> RuleResult:
    tree = ast.parse(expr, mode="eval")
    missing: list[str] = []

    def ev(n: ast.AST):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, (ast.List, ast.Tuple)):
            return [ev(e) for e in n.elts]
        d = _dotted(n)
        if d is not None and isinstance(n, (ast.Name, ast.Attribute)):
            if d not in values or values[d] is None:
                raise _Missing(d)
            return values[d]
        if isinstance(n, ast.BoolOp):
            vals = []
            for v in n.values:
                try:
                    vals.append(bool(ev(v)))
                except _Missing as m:
                    if m.slot_id not in missing:
                        missing.append(m.slot_id)
                    vals.append(None)
            if isinstance(n.op, ast.And):
                if any(v is False for v in vals):
                    return False
                if any(v is None for v in vals):
                    raise _Missing(missing[-1])
                return True
            if isinstance(n.op, ast.Or):
                if any(v is True for v in vals):
                    return True
                if any(v is None for v in vals):
                    raise _Missing(missing[-1])
                return False
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return not ev(n.operand)
        if isinstance(n, ast.Compare):
            left = ev(n.left)
            for op, comp in zip(n.ops, n.comparators):
                right = ev(comp)
                if isinstance(op, ast.Eq):
                    ok = left == right
                elif isinstance(op, ast.NotEq):
                    ok = left != right
                elif isinstance(op, ast.In):
                    ok = left in (right if isinstance(right, (list, set, tuple, str)) else [right])
                elif isinstance(op, ast.NotIn):
                    ok = left not in (right if isinstance(right, (list, set, tuple, str)) else [right])
                elif isinstance(op, ast.Gt):
                    ok = left > right
                elif isinstance(op, ast.GtE):
                    ok = left >= right
                elif isinstance(op, ast.Lt):
                    ok = left < right
                elif isinstance(op, ast.LtE):
                    ok = left <= right
                else:
                    raise RuleError(f"unsupported comparison in rule: {expr}")
                if not ok:
                    return False
                left = right
            return True
        raise RuleError(f"unsupported syntax in rule: {expr}")

    try:
        return RuleResult(fired=bool(ev(tree.body)), missing=missing)
    except _Missing as m:
        if m.slot_id not in missing:
            missing.append(m.slot_id)
        return RuleResult(fired=False, missing=missing)
