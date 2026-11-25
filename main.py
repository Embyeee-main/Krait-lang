from pathlib import Path
from sys import argv

from data import (ARITHMETIC_OP_MAP, COMP_OP_MAP, LOGIC_OP_MAP,
                  ROUNDING_OP_MAP, Inst)
from utils import (except_on_type_check_fail, is_float, is_int, is_num,
                   two_value_func_call)


def parse(raw: str) -> list[int]:
    buf = []

    for line in raw.split("\n"):
        if len(line) == 0 or line[0] == "#":
            continue
        split_line = line.split(" ")
        if split_line[0] == "INPUT":
            buf.append([split_line[0], " ".join(split_line[1:])])
        else:
            buf.append(split_line)

    inst_buf = []

    for val in buf:
        match (cur_inst := val[0]):
            case "PUSH" | "APPEND":
                if not is_num(val[1]):
                    inst_buf.append([Inst._member_map_[cur_inst], ord(val[1])])
                else:
                    inst_buf.append(
                        [Inst._member_map_[cur_inst], float(val[1])])
            case "MOV" | "INPUT" | "LABEL" | "GOTO" | "DEL":
                inst_buf.append([Inst._member_map_.get(cur_inst), val[1]])
            case _:
                if Inst._member_map_.get(cur_inst):
                    inst_buf.append([Inst._member_map_.get(cur_inst)])
                else:
                    inst_buf.append([cur_inst])
    return inst_buf


def run_program(program: list[int]) -> None:
    stack = []
    heap = {}
    labels = {}
    p_counter = 0

    while True:
        cur_inst = program[p_counter][0]
        if len(program[p_counter]) == 2:
            cur_val = program[p_counter][1]
        match (cur_inst := program[p_counter][0]):
            case Inst.PUSH:
                stack.insert(0, cur_val)
            case Inst.ARRAY:
                stack.insert(0, [])
            case Inst.APPEND:
                a = stack[0]
                if not isinstance(a, list):
                    raise ValueError("cannot append to a non array")
                a.append(cur_val)
            case Inst.ADD | Inst.SUB | Inst.MULT | Inst.DIV | Inst.EXP:
                two_value_func_call(
                    stack,
                    lambda a, b: except_on_type_check_fail(float, a, b),
                    ARITHMETIC_OP_MAP,
                    cur_inst.name,
                )
            case Inst.FLOOR | Inst.CEIL | Inst.ROUND:
                a = stack.pop(0)
                stack.insert(0, ROUNDING_OP_MAP[cur_inst.name](a))
            case Inst.NOT:
                a = stack.pop(0)
                if not a == 1 and not a == 0:
                    raise ValueError("NOT can only accept boolean values")
                stack.insert(0, not a)
            case Inst.AND | Inst.OR | Inst.XOR:
                two_value_func_call(
                    stack,
                    lambda a, b: (not a == 1 and not a == 0)
                    or (not b == 1 and not b == 0),
                    LOGIC_OP_MAP,
                    cur_inst.name,
                )
            case Inst.GT | Inst.GE | Inst.LT | Inst.LE | Inst.EQ:
                two_value_func_call(
                    stack,
                    lambda a, b: except_on_type_check_fail(float, a, b),
                    COMP_OP_MAP,
                    cur_inst.name,
                )
            case Inst.PRINT:
                a = stack.pop(0)
                if a is True:
                    print(1)
                elif a is False:
                    print(0)
                elif isinstance(a, list):
                    for num in a:
                        if is_float(num):
                            print(num, end=", ")
                        elif is_int(str(num)):
                            print(int(num), end=", ")
                        else:
                            raise TypeError(
                                "PRINT can only print ints or floats")
                elif is_float(a):
                    print(a)
                else:
                    print(int(a))
            case Inst.SPRINT:
                a = stack.pop(0)
                if is_float(a):
                    raise ValueError("SPRINT can only accept integers")
                elif isinstance(a, list):
                    for char in a:
                        if is_float(char):
                            raise ValueError("SPRINT can only accept integers")
                        print(chr(int(a)), end="")
                else:
                    print(chr(int(a)), end="")
            case Inst.INPUT:
                _in = input(cur_val)
                if not is_num(_in):
                    raise ValueError(
                        "only float or interger values are accepted for input"
                    )
                stack.insert(0, float(_in))
            case Inst.MOV:
                val = stack.pop(0)
                key = cur_val
                heap[key] = val
            case Inst.DEL:
                heap.pop(cur_val)
            case Inst.GOTO:
                go = stack.pop(0)
                if go == 1 or go is True:
                    new_count = cur_val
                    if not is_int(new_count):
                        raise ValueError("goto value must be an int or label")
                    elif not is_num(new_count):
                        new_count = labels.get(new_count)
                        if new_count is None:
                            raise ValueError(
                                f"{new_count} is not a valid label")
                    p_counter = int(new_count) - 1
                    continue
            case Inst.LABEL:
                labels[cur_val] = p_counter + 1
            case Inst.HALT:
                return heap
            case _:
                if cur_inst in heap:
                    stack.insert(0, heap[cur_inst])
                else:
                    raise ValueError(f"{cur_inst} is not a valid instruction")
        p_counter += 1


def main() -> None:
    program_file = Path(argv[1])
    if not program_file.suffix == ".krt":
        raise ValueError(f"file {str(program_file)} must be a .krt file")
    elif not program_file.exists():
        raise FileNotFoundError(f"file {str(program_file)} does not exist")

    with program_file.open() as file:
        program = parse(file.read().strip("\n"))

    res = run_program(program)
    print(res)


if __name__ == "__main__":
    main()
