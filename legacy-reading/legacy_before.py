"""読みづらいレガシーコード（意図的）。

一見動くが、以下の問題を含む:
- 命名が不統一 (`doStuff`, `x1`, `tp`, `R`)
- 計算と副作用（監査ログ/グローバル状態更新）が密結合
- 隠れた仕様（不正入力時の値、未知タイプ時のフォールバック）がドキュメント化されていない
"""

AUDIT_TRAIL = []  # hidden side-effect sink
RUN_COUNTER = {"total": 0}
BONUS_MODE = False


def doStuff(x1, x2, tp, R, note=""):
    # hidden side effect #1
    RUN_COUNTER["total"] += 1

    if x1 is None or x2 is None:
        AUDIT_TRAIL.append({"tp": tp, "result": -1, "note": note})
        return -1

    # unclear branching + inconsistent naming
    zz = 0
    if tp == "A":
        zz = x1 * x2
    elif tp == "B":
        zz = x1 + x2
    elif tp == "C":
        zz = abs(x1 - x2)
    else:
        zz = x1 - x2

    # hidden side effect #2 (global flag changes behavior)
    if BONUS_MODE:
        zz = zz + 5

    # magic numbers
    if R == 1:
        out = int(zz * 1.10)
    elif R == 2:
        out = int(zz * 1.20)
    elif R == 99:
        out = 0
    else:
        out = int(zz)

    AUDIT_TRAIL.append({"tp": tp, "result": out, "note": note})
    return out
