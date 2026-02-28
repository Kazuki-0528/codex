"""legacy_before を段階的に読み解いて改善した版。

改善方針:
- 計算ロジックを純粋関数化
- 互換のため副作用（監査ログ・実行回数カウント）は明示的に残す
- 暗黙仕様を定数化して意図を読める形にする
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

OperationType = Literal["A", "B", "C", "OTHER"]

RATE_MULTIPLIER = {
    1: 1.10,
    2: 1.20,
}


@dataclass
class LegacyContext:
    audit_trail: list[dict]
    run_counter: dict[str, int]
    bonus_mode: bool


# 互換維持のため module-level state を保持
AUDIT_TRAIL: list[dict] = []
RUN_COUNTER = {"total": 0}
BONUS_MODE = False


def normalize_operation(operation_type: str) -> OperationType:
    if operation_type in ("A", "B", "C"):
        return operation_type
    return "OTHER"


def base_value(left: int, right: int, operation_type: OperationType) -> int:
    if operation_type == "A":
        return left * right
    if operation_type == "B":
        return left + right
    if operation_type == "C":
        return abs(left - right)
    return left - right


def apply_rate(base: int, rate_code: int) -> int:
    if rate_code == 99:
        return 0
    multiplier = RATE_MULTIPLIER.get(rate_code, 1.0)
    return int(base * multiplier)


def calculate_value(left: int | None, right: int | None, operation_type: str, rate_code: int, *, bonus_mode: bool) -> int:
    """副作用なしの計算コア。"""
    if left is None or right is None:
        return -1

    normalized = normalize_operation(operation_type)
    base = base_value(left, right, normalized)
    adjusted = base + 5 if bonus_mode else base
    return apply_rate(adjusted, rate_code)


def do_stuff_compatible(left: int | None, right: int | None, operation_type: str, rate_code: int, note: str = "") -> int:
    """legacy_before.doStuff と同一の外部振る舞いを保つ互換関数。"""
    RUN_COUNTER["total"] += 1

    result = calculate_value(
        left=left,
        right=right,
        operation_type=operation_type,
        rate_code=rate_code,
        bonus_mode=BONUS_MODE,
    )

    AUDIT_TRAIL.append({"tp": operation_type, "result": result, "note": note})
    return result
