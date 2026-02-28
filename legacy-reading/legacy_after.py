from typing import Literal

OperationType = Literal["A", "B", "OTHER"]


def _base_value(left: int, right: int, operation_type: OperationType) -> int:
    if operation_type == "A":
        return left * right
    if operation_type == "B":
        return left + right
    return left - right


def _rate_multiplier(rate_code: int) -> float:
    if rate_code == 1:
        return 1.1
    if rate_code == 2:
        return 1.2
    return 1.0


def calculate_legacy_value(left: int | None, right: int | None, operation_type: str, rate_code: int) -> int:
    """legacy_before.c と同一の振る舞いを保つ。"""
    if left is None or right is None:
        return -1

    normalized_operation: OperationType = operation_type if operation_type in ("A", "B") else "OTHER"
    base = _base_value(left, right, normalized_operation)
    return int(base * _rate_multiplier(rate_code))
