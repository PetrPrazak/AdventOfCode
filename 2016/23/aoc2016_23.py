# https://adventofcode.com/2016/day/23
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from collections import defaultdict


def emulate(prog, registers):
    def value(arg):
        return int(arg) if not arg.isalpha() else registers[arg]

    ip = 0
    while ip < len(prog):
        # print(prog[ip], registers)
        op, *args = prog[ip]
        if op == "nop":
            pass
        elif op == "mul":
            src, dest = args
            if dest.isalpha():
                registers[dest] *= value(src)
        elif op == "add":
            src, dest = args
            if dest.isalpha():
                registers[dest] += value(src)
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
        elif op == "tgl":
            reg = args[0]
            off = registers[reg]
            off += ip
            if 0 <= off < len(prog):
                t_op, *t_args = prog[off]
                # print("Toggling", off, prog[off], end=" ")
                if len(t_args) == 1:
                    instr = "dec" if t_op == "inc" else "inc"
                else:
                    instr = "cpy" if t_op == "jnz" else "jnz"
                prog[off] = [instr] + t_args
                # print(prog[off])
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
    result = run(data.copy(), ('a', 7))
    print("part 1:", result)
    # part 2
    result = run(data, ('a', 12))
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip().split() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input_mul.txt")
