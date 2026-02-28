# 読みにくいレガシーコード（意図的）

def c(a, b, t, r):
    if a is None or b is None:
        return -1
    x = 0
    if t == "A":
        x = a * b
    elif t == "B":
        x = a + b
    else:
        x = a - b
    if r == 1:
        return int(x * 1.1)
    if r == 2:
        return int(x * 1.2)
    return int(x)
