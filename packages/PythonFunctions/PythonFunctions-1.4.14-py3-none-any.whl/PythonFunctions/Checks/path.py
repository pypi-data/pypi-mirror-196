import os


def check(value, _, __, **___):
    if os.path.exists(value):
        return value
    if value == "":
        return False
    return None
