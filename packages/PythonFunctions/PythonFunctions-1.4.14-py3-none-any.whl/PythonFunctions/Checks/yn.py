"""
Returns True ("y") or False ("n")

Arguments:
----------
None
"""


def check(value, Message, _, **info):
    """
    If value == `y` then return True
    if value == `n` then return False
    else return None
    """
    value = value.strip()

    if len(value) == 0:
        return Message.clear("Invalid input! Nothing there")

    v = value[0].lower()
    n = info.get("n")
    nA = info.get("nA")
    y = info.get("y")
    yA = info.get("yA")

    if v == "n":
        if n:
            return n(nA) if nA else n()
        return False

    if v == "y":
        if y:
            return y(yA) if yA else y()
        return True

    return None
