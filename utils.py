from math import floor
from typing import Any, Callable, Type


def is_num(val: str) -> bool:
    if val[-1] == "." or val[-1] == "-":
        return False
    elif val[0] == "-":
        val = val[1:]

    is_decimal = False
    for char in val:
        if char == "." and is_decimal:
            return False
        elif char == ".":
            is_decimal = True
        elif char.isdigit():
            continue
        else:
            return False
    return True


def is_float(val: float) -> bool:
    return not floor(val) == val


def is_int(val: str) -> bool:
    return not (is_num(val) and is_float(float(val)))


def two_value_func_call(
    stack: list[float],
    type_check: Callable[[float, float], None],
    _map: dict[str, Callable[[float, float], float]],
    key: str,
) -> None:
    b = stack.pop(0)
    a = stack.pop(0)
    if not type_check(a, b):
        raise TypeError
    stack.insert(0, _map[key](a, b))


def except_on_type_check_fail(_type: Type, *args: Any) -> None:
    for val in args:
        if not isinstance(val, _type):
            raise TypeError(f"{val} must be of type {str(_type.__name__)}")
    return True
