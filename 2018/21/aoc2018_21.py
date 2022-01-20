# https://adventofcode.com/2018/day/21
from __future__ import print_function
from pathlib import Path

# cpu from day 19

# all instructions store the result into regs[r3]
instruction_set = {
    "addr": lambda regs, r1, r2: regs[r1] + regs[r2],
    "addi": lambda regs, r1, im: regs[r1] + im,
    "mulr": lambda regs, r1, r2: regs[r1] * regs[r2],
    "muli": lambda regs, r1, im: regs[r1] * im,
    "banr": lambda regs, r1, r2: regs[r1] & regs[r2],
    "bani": lambda regs, r1, im: regs[r1] & im,
    "borr": lambda regs, r1, r2: regs[r1] | regs[r2],
    "bori": lambda regs, r1, im: regs[r1] | im,
    "setr": lambda regs, r1, r2: regs[r1],
    "seti": lambda regs, i1, im: i1,
    "gtir": lambda regs, im, r2: im > regs[r2],
    "gtri": lambda regs, r1, im: regs[r1] > im,
    "gtrr": lambda regs, r1, r2: regs[r1] > regs[r2],
    "eqir": lambda regs, im, r2: im == regs[r2],
    "eqri": lambda regs, r1, im: regs[r1] == im,
    "eqrr": lambda regs, r1, r2: regs[r1] == regs[r2]
}


def run(data):
    if data[0][0] == '#ip':
        ip_reg = data[0][1][0]
        program = data[1:]
    else:
        ip_reg = 0
        program = data
    regs = [0] * 6
    while 0 <= regs[ip_reg] < len(program):
        instr, (p1, p2, p3) = program[regs[ip_reg]]
        regs[p3] = instruction_set[instr](regs, p1, p2)
        regs[ip_reg] += 1
    return regs


def code(part1=True):
    """ reverse-engineereed code from the input """
    d = 0
    s = set()
    last_uniq = None
    while True:
        e = d | 65536
        d = 7637914
        while True:
            c = e & 255
            d += c
            d &= 16777215
            d *= 65899
            d &= 16777215
            if 256 > e:
                if part1:
                    return d
                else:
                    if d not in s:
                        s.add(d)
                        last_uniq = d
                        break
                    else:
                        return last_uniq
            else:
                # the following code was the optimised part
                e = e // 256


def process(data):
    # run(data)
    print("part 1:", code())
    # part 2
    print("part 2:", code(False))


def parse_line(line):
    instr, *line = line.split()
    return instr, tuple(map(int, line))


def load_data(fileobj):
    return [parse_line(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
