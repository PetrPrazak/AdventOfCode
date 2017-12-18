"""
http://adventofcode.com/2017/day/18

"""

from __future__ import print_function
from collections import defaultdict, deque

sends = [0, 0]


def solve(lines):
    prog = [x.strip().split() for x in lines]

    part1(prog)
    part2(prog)


def part2(prog):
    regset = [defaultdict(int), defaultdict(int)]
    queue = [deque(), deque()]

    regset[0]['p'] = 0
    regset[1]['p'] = 1

    while True:
        if not step(prog, 0, regset[0], queue[0], queue[1]) and \
           not step(prog, 1, regset[1], queue[1], queue[0]):
            break

    print(regset[1]['sent'])


def step(prog, pid, regs, qin, qout):
    pos = regs['pc']
    if not (0 <= pos < len(prog)):
        print(pid, "Out of bounds:", pos)
        return False
    p = prog[pos]
    # print(regs)
    cmd, val = p[0], p[1]
    arg = 0
    if len(p) > 2:
        y = p[2]
        arg = regs[y] if y[0] >= 'a' else int(y)
    if cmd == "snd":
        y = val
        arg = regs[y] if y[0] >= 'a' else int(y)
        qout.append(arg)
        regs['sent'] += 1
    elif cmd == "rcv":
        if not qin:
            return False
        regs[val] = qin.popleft()
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

    regs['pc'] = pos
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
