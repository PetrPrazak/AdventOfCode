# https://adventofcode.com/2024/day/17
from pathlib import Path
from copy import copy
import time
import re


def emulate(regs, program):
    def combo(op):
        if op < 4:
            return op
        return regs[op-4]

    regs = copy(regs)
    output = []
    IP = 0
    while IP < len(program):
        inst, op = program[IP], program[IP+1]
        IP += 2
        if inst == 0:  # adv
            regs[0] //= (2 ** combo(op))
        elif inst == 1:  # bxl
            regs[1] ^= op
        elif inst == 2:  # bst
            regs[1] = combo(op) % 8
        elif inst == 3:  # jnz
            if regs[0]:
                IP = op
        elif inst == 4:  # bxc
            regs[1] ^= regs[2]
        elif inst == 5:  # out
            output.append(combo(op) % 8)
        elif inst == 6:  # bdv
            regs[1] = regs[0] // (2 ** combo(op))
        elif inst == 7:  # cdv
            regs[2] = regs[0] // (2 ** combo(op))
    return output


def compute_seed(program):
    """
    Reversed the program in the input
    """
    Avalues = [0]
    for n in program[::-1]:
        currentA = []
        for A in Avalues:
            B = n
            B ^= 5
            if A == 0:
                B ^= 1
                currentA.append(B)
            else:
                A *= 8
                candidates = []
                for b in range(8):
                    C = A + b
                    b ^= 1
                    C = C // (2 ** b)
                    b ^= C
                    if (b % 8) == B:
                        b ^= C
                        b ^= 1
                        candidates.append(b)
                if not candidates:
                    continue
                for B in candidates:
                    newA = A + B % 8
                    currentA.append(newA)
        Avalues = currentA
    return min(Avalues)


def process(data):
    # part 1
    out = emulate(*data)
    result = ",".join(str(i) for i in out)
    print("part 1:", result)
    # part 2
    A = compute_seed(data[1])
    data[0][0] = A
    out = emulate(*data)
    assert out == data[1]
    print("part 2:", A)


def load_data(fileobj):
    part1, part2 = fileobj.read().split("\n\n")
    regs = list(map(int, re.findall(r'\d+', part1)))
    program = list(map(int, re.findall(r'\d+', part2)))
    return regs, program


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
