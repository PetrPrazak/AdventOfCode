# replace XX with day

"""

http://adventofcode.com/2016/day/XX


"""
from __future__ import print_function
from collections import defaultdict, Counter


def solve(lines):
    total = 0
    for line in lines:
        line = line.strip()
        part = line.split()

    print(total)


INPUT = "aoc_dayXX_input.txt"
# INPUT = "aoc_dayXX_test.txt"


if __name__ == "__main__":
    with open(INPUT) as f:
        # read all in once
        data = f.read()
        solve(data)
        # read by lines
        lines = f.readlines()
        solve(lines)
