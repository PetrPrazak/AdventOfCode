"""
http://adventofcode.com/2017/day/18

"""

from __future__ import print_function
from collections import defaultdict, deque


def solve(lines):
    prog = [x.strip().split() for x in lines]

    part1(prog)
    part2(prog)


def part2(prog):
    queue = [deque(), deque()]
    p0, p1 = DuetVM(prog, 0, queue[0], queue[1]), DuetVM(prog, 1, queue[1], queue[0])
    while True:
        if not p0.step() and not p1.step():
            break
    print(p1.sent)


class DuetVM(object):
    def __init__(self, prog, pid, qin, qout):
        self.regs = defaultdict(int)
        self.prog = prog
        self.pid = pid
        self.quein = qin
        self.queout = qout
        self.regs['p'] = pid
        self.sent = 0

    def getval(self, arg):
        return self.regs[arg] if arg[0].isalpha() else int(arg)

    def step(self):
        pos = self.regs['pc']
        if not (0 <= pos < len(self.prog)):
            return False
        p = self.prog[pos]
        cmd, arg1 = p[0], p[1]
        if cmd == "snd":
            self.queout.append(self.getval(arg1))
            self.sent += 1
        elif cmd == "rcv":
            if not self.quein:
                return False
            self.regs[arg1] = self.quein.popleft()
        elif cmd == "set":
            self.regs[arg1] = self.getval(p[2])
        elif cmd == "add":
            self.regs[arg1] += self.getval(p[2])
        elif cmd == "mul":
            self.regs[arg1] *= self.getval(p[2])
        elif cmd == "mod":
            self.regs[arg1] %= self.getval(p[2])
        elif cmd == "jgz":
            if self.getval(arg1) > 0:
                pos += self.getval(p[2]) - 1
        pos += 1

        self.regs['pc'] = pos
        return True


def part1(prog):
    lastsnd = 0
    pos = 0
    regs = defaultdict(int)
    while True:
        p = prog[pos]
        cmd, val = p[0], p[1]
        arg = 0
        if len(p) > 2:
            y = p[2]
            arg = regs[y] if y[0] >= 'a' else int(y)

        if cmd == "snd":
            y = val
            arg = regs[y] if y[0] >= 'a' else int(y)
            lastsnd = arg
        elif cmd == "rcv":
            if regs[val]:
                break
        elif cmd == "set":
            regs[val] = arg
        elif cmd == "add":
            regs[val] += arg
        elif cmd == "mul":
            regs[val] *= arg
        elif cmd == "mod":
            regs[val] %= arg
        elif cmd == "jgz":
            cond = regs[val] if val[0] >= 'a' else int(val)
            if cond > 0:
                pos += arg - 1

        pos += 1

    print(lastsnd)


INPUT = "aoc_day18_input.txt"
# INPUT = "aoc_day18_test.txt"

if __name__ == "__main__":
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)
