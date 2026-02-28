import pathlib
import sys

CURRENT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from legacy_before import c
from legacy_after import calculate_legacy_value


def test_behavior_is_compatible():
    cases = [
        (2, 3, "A", 1),
        (2, 3, "B", 2),
        (5, 2, "X", 0),
        (None, 2, "A", 1),
    ]
    for left, right, operation_type, rate_code in cases:
        assert calculate_legacy_value(left, right, operation_type, rate_code) == c(left, right, operation_type, rate_code)
