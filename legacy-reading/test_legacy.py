import pathlib
import sys

CURRENT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

import legacy_before
import legacy_after


def _reset_before_state() -> None:
    legacy_before.AUDIT_TRAIL.clear()
    legacy_before.RUN_COUNTER["total"] = 0
    legacy_before.BONUS_MODE = False


def _reset_after_state() -> None:
    legacy_after.AUDIT_TRAIL.clear()
    legacy_after.RUN_COUNTER["total"] = 0
    legacy_after.BONUS_MODE = False


def test_step1_lock_legacy_behavior_examples():
    """最初に legacy_before の仕様を固定する（回帰防止）。"""
    _reset_before_state()

    assert legacy_before.doStuff(2, 3, "A", 1) == 6
    assert legacy_before.doStuff(2, 3, "B", 2) == 6
    assert legacy_before.doStuff(5, 2, "X", 0) == 3
    assert legacy_before.doStuff(10, 4, "C", 0) == 6
    assert legacy_before.doStuff(None, 2, "A", 1) == -1
    assert legacy_before.doStuff(1, 2, "A", 99) == 0

    assert legacy_before.RUN_COUNTER["total"] == 6
    assert len(legacy_before.AUDIT_TRAIL) == 6


def test_step2_refactor_keeps_results_and_side_effects_compatible():
    """改善版の互換関数が戻り値と副作用を維持することを検証。"""
    _reset_before_state()
    _reset_after_state()

    cases = [
        (2, 3, "A", 1, "x"),
        (2, 3, "B", 2, "y"),
        (5, 2, "X", 0, "z"),
        (10, 4, "C", 0, "c"),
        (None, 2, "A", 1, "n"),
        (1, 2, "A", 99, "r"),
    ]

    for left, right, operation_type, rate_code, note in cases:
        before_value = legacy_before.doStuff(left, right, operation_type, rate_code, note)
        after_value = legacy_after.do_stuff_compatible(left, right, operation_type, rate_code, note)
        assert after_value == before_value

    assert legacy_after.RUN_COUNTER["total"] == legacy_before.RUN_COUNTER["total"]
    assert legacy_after.AUDIT_TRAIL == legacy_before.AUDIT_TRAIL


def test_step3_bonus_mode_behavior_is_preserved():
    _reset_before_state()
    _reset_after_state()

    legacy_before.BONUS_MODE = True
    legacy_after.BONUS_MODE = True

    before_value = legacy_before.doStuff(3, 4, "B", 1)
    after_value = legacy_after.do_stuff_compatible(3, 4, "B", 1)

    assert after_value == before_value
