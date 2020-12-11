# http://adventofcode.com/2016/day/12
from __future__ import print_function
from collections import defaultdict, Counter


def emulate(prog, registers):
    ip = 0
    while ip < len(prog):
        op, *args = prog[ip]
        if op == "cpy":
            src, dest = args
            registers[dest] = int(src) if src.isdigit() else registers[src]
            ip += 1
        elif op == "inc":
            reg = args[0]
            registers[reg] += 1
            ip += 1
        elif op == "dec":
            reg = args[0]
            registers[reg] -= 1
            ip += 1
        elif op == "jnz":
            reg, offset = args
            val = int(reg) if reg.isdigit() else registers[reg]
            ip += int(offset) if val else 1
        else:
            raise NotImplementedError(ip, ' '.join(prog[ip]))


def run(prog, reg_init=None):
    registers = defaultdict(int)
    if reg_init:
        reg, val = reg_init
        registers[reg] = val
    emulate(prog, registers)
    return registers['a']


def solve(lines):
    # part 1
    print("Part 1:", run(lines))
    # part 2
    print("Part 2:", run(lines, ('c', 1)))


def parse(line):
    return line.split(' ')


def main(file):
    with open(file) as f:
        lines = [parse(l.strip()) for l in f.readlines()]
        solve(lines)


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
