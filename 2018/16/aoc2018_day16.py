# https://adventofcode.com/2018/day/16

from __future__ import print_function
import re
from collections import defaultdict

INPUT = "aoc2018_day16.txt"
# INPUT = "test.txt"


def addr(regs, r1, r2, r3):
    regs[r3] = regs[r1] + regs[r2]


def addi(regs, r1, i, r3):
    regs[r3] = regs[r1] + i


def mulr(regs, r1, r2, r3):
    regs[r3] = regs[r1] * regs[r2]


def muli(regs, r1, i, r3):
    regs[r3] = regs[r1] * i


def banr(regs, r1, r2, r3):
    regs[r3] = regs[r1] & regs[r2]


def bani(regs, r1, i, r3):
    regs[r3] = regs[r1] & i


def borr(regs, r1, r2, r3):
    regs[r3] = regs[r1] | regs[r2]


def bori(regs, r1, i, r3):
    regs[r3] = regs[r1] | i


def setr(regs, r1, r2, r3):
    regs[r3] = regs[r1]


def seti(regs, i1, i, r3):
    regs[r3] = i1


def gtir(regs, i, r2, r3):
    regs[r3] = 1 if i > regs[r2] else 0


def gtri(regs, r1, i, r3):
    regs[r3] = 1 if regs[r1] > i else 0


def gtrr(regs, r1, r2, r3):
    regs[r3] = 1 if regs[r1] > regs[r2] else 0


def eqir(regs, i, r2, r3):
    regs[r3] = 1 if i == regs[r2] else 0


def eqri(regs, r1, i, r3):
    regs[r3] = 1 if regs[r1] == i else 0


def eqrr(regs, r1, r2, r3):
    regs[r3] = 1 if regs[r1] == regs[r2] else 0


instruction_set = [addr, addi,
                   mulr, muli,
                   banr, bani,
                   borr, bori,
                   setr, seti,
                   gtir, gtri, gtrr,
                   eqir, eqri, eqrr]


def get_numbers(s):
    return list(map(int, re.findall(r"(\d+)", s)))


def check_instr(before, instr, param, after):
    regs = before[::]
    instr(regs, *param)
    return True if regs == after else False


def check_all_instr(before, param, after):
    result = {instr for instr in instruction_set if check_instr(before, instr, param, after)}
    return result


def process(data):
    total = 0
    cnt = defaultdict(list)
    inp = iter(data)
    operations = {opcode: set(instruction_set) for opcode in range(16)}

    for line in inp:
        if not line:
            # print("empty line")
            break

        if line.find("Begins:"):
            init_state = get_numbers(line)
            op_code, *param = get_numbers(next(inp))
            result = get_numbers(next(inp))
            _ = next(inp)  # swallow empty line

            r = check_all_instr(init_state, param, result)
            if len(r) >= 3:
                total += 1
            operations[op_code].intersection_update(r)

    while True:
        unique_ops = {op: ops for op, ops in operations.items() if len(ops) == 1}
        if len(unique_ops) == len(operations):
            break
        for op_, ops_ in unique_ops.items():
            for op, ops in operations.items():
                if op != op_:
                    ops.difference_update(ops_)

    for op in operations:
        operations[op] = operations[op].pop()
        print(op, operations[op].__name__)

    # part 1
    print(total)  # 570

    # part 2
    regs = [0] * 4
    for line in inp:
        if not line:
            continue
        op_code, *param = get_numbers(line)
        f = operations[op_code]
        f(regs, *param)
        # print(f.__name__, *param)

    print(regs[0])


def main():
    with open(INPUT) as f:
        data = [l.strip() for l in f.readlines()]
        process(data)


if __name__ == "__main__":
    main()
