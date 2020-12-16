# http://adventofcode.com/2017/day/18
from __future__ import print_function
from collections import defaultdict, Counter
from functools import reduce

try:
    xrange
except NameError:
    xrange = range


def solve(steplen):
    solve1(steplen)
    solve2(50000000, steplen)


def solve1(steplen):
    ring = [0]
    pos = 0
    for i in xrange(1, 2017 + 1):
        pos = (pos + steplen) % i
        ring.insert(pos + 1, i)
        pos += 1

    pos = (pos + 1) % (i + 1)
    print(ring[pos])


def solve2(maxcycle, steplen):
    pos = 0
    afterzero = 0
    for i in xrange(1, maxcycle + 1):
        pos = (pos + steplen) % i
        if pos == 0:
            afterzero = i
        pos += 1
    print(afterzero)


INPUT = 370

if __name__ == "__main__":
    solve(INPUT)
