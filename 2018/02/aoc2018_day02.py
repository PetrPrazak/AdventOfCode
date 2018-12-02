# https://adventofcode.com/2018/day/2

from __future__ import print_function
from collections import Counter

INPUT = "aoc2018_day02.txt"


def id_comm(id1, id2):
    s = ""
    for c1, c2 in zip(id1, id2):
        if c1 == c2:
            s += c1
    return s


with open(INPUT) as f:
    data = f.read().split()
    # part 1
    twos = threes = 0
    for index, line in enumerate(data):
        sums = Counter(line).values()
        if 2 in sums:
            twos += 1
        if 3 in sums:
            threes += 1

        # part 2
        for i in range(1, index):
            common = id_comm(line, data[i])
            if len(line) - len(common) == 1:
                print(common)
                break

    # part 1
    print(twos * threes)

