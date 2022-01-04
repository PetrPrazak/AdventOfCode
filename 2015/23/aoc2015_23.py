# https://adventofcode.com/2015/day/23
from __future__ import print_function
from pathlib import Path


def run(data, regs):
    IP = 0
    while IP < len(data):
        instr, op, *off = data[IP]
        if instr == "hlf":
            regs[op] //= 2
        elif instr == "tpl":
            regs[op] *= 3
        elif instr == "inc":
            regs[op] += 1
        elif instr == "jmp":
            IP += int(op)
            continue
        elif instr == "jie":
            if regs[op[0]] % 2 == 0:
                IP += int(off[0])
                continue
        elif instr == "jio":
            if regs[op[0]] == 1:
                IP += int(off[0])
                continue
        else:
            assert False, f"Unknown instruction {data[IP]}"
        IP += 1
    return regs


def process(data):
    # part 1
    regs = {'a': 0, 'b': 0}
    run(data, regs)
    print("part 1:", regs['b'])
    # part 2
    regs = {'a': 1, 'b': 0}
    run(data, regs)
    print("part 2:", regs['b'])


def load_data(fileobj):
    return [line.strip().split() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
