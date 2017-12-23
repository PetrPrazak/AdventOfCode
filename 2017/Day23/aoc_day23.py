"""
http://adventofcode.com/2017/day/23
"""
from __future__ import print_function
from collections import defaultdict

try:
    xrange
except NameError:
    xrange = range


def solve(lines):
    prog = [x.strip().split() for x in lines]

    part1(prog)
    part2()


def part1(prog):
    p = Coprocessor(prog)
    while True:
        if not p.step():
            break
    print(p.muls)


# faster is to emulate the program here
# it counts all non primes in defined range
def part2():
    count = 0
    for num in xrange(108100, 125100 + 1, 17):
        for i in xrange(2, int(num ** 0.5) + 1):
            if (num % i) == 0:
                count += 1
                break
    print(count)


class Coprocessor(object):
    def __init__(self, prog):
        self.regs = defaultdict(int)
        self.prog = prog
        self.muls = 0

    def getval(self, arg):
        return self.regs[arg] if arg[0].isalpha() else int(arg)

    def step(self):
        pos = self.regs['pc']
        if not (0 <= pos < len(self.prog)):
            return False
        p = self.prog[pos]
        cmd, arg1 = p[0], p[1]
        if cmd == "set":
            self.regs[arg1] = self.getval(p[2])
        elif cmd == "sub":
            self.regs[arg1] -= self.getval(p[2])
        elif cmd == "mul":
            self.regs[arg1] *= self.getval(p[2])
            self.muls += 1
        elif cmd == "jnz":
            if self.getval(arg1):
                pos += self.getval(p[2]) - 1
        pos += 1

        self.regs['pc'] = pos
        return True


INPUT = "aoc_day23_input.txt"


def main():
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
