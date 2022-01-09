# https://adventofcode.com/2016/day/25
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from collections import defaultdict

MAX_OUT = 12

def emulate(prog, registers):
    def value(arg):
        return int(arg) if not arg.isalpha() else registers[arg]

    ip = 0
    prev = 1
    cnt = 0
    while ip < len(prog):
        op, *args = prog[ip]
        if op == "out":
            val = value(args[0])
            cnt += 1
            if cnt >= MAX_OUT or abs(val - prev) == 0:
                registers['a'] = cnt
                break
            prev = val
        elif op == "cpy":
            src, dest = args
            if dest.isalpha():
                registers[dest] = value(src)
        elif op == "inc":
            reg = args[0]
            if reg.isalpha():
                registers[reg] += 1
        elif op == "dec":
            reg = args[0]
            if reg.isalpha():
                registers[reg] -= 1
        elif op == "jnz":
            reg, offset = args
            ip += value(offset) if value(reg) else 1
            continue
        else:
            raise NotImplementedError(ip, ' '.join(prog[ip]))
        ip += 1


def run(prog, reg_init=None):
    registers = defaultdict(int)
    if reg_init:
        reg, val = reg_init
        registers[reg] = val
    emulate(prog, registers)
    return registers['a']


def process(data):
    # part 1
    for i in range(1000):
        if run(data, ('a', i)) >= MAX_OUT:
            break
    print("part 1:", i)


def load_data(fileobj):
    return [line.strip().split() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main()
