from enum import Enum, auto
from math import ceil, floor


class Inst(Enum):
    PUSH = auto()
    ARRAY = auto()
    APPEND = auto()
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    EXP = auto()
    PRINT = auto()
    SPRINT = auto()
    MOV = auto()
    DEL = auto()
    EQ = auto()
    ROUND = auto()
    FLOOR = auto()
    CEIL = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    GT = auto()
    GE = auto()
    LT = auto()
    LE = auto()
    GOTO = auto()
    LABEL = auto()
    INPUT = auto()
    HALT = auto()


ARITHMETIC_OP_MAP = {
    "ADD": lambda a, b: a + b,
    "SUB": lambda a, b: a - b,
    "MULT": lambda a, b: a * b,
    "DIV": lambda a, b: a / b,
    "EXP": lambda a, b: a**b,
}

ROUNDING_OP_MAP = {
    "FLOOR": lambda a: floor(a),
    "CEIL": lambda a: ceil(a),
    "ROUND": lambda a: round(a),
}

LOGIC_OP_MAP = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
    "XOR": lambda a, b: a ^ b,
}

COMP_OP_MAP = {
    "GT": lambda a, b: a > b,
    "GE": lambda a, b: a >= b,
    "LT": lambda a, b: a < b,
    "LE": lambda a, b: a <= b,
    "EQ": lambda a, b: a == b,
}
