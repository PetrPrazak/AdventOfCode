# replace XX with day

"""

http://adventofcode.com/2017/day/XX


"""
from __future__ import print_function
from collections import defaultdict, Counter
from functools import reduce


def solve(lines):
    total = 0
    for line in lines:
        part = line.strip().split()
        # TODO
        print(part)
        pass
    data = [int(p) for line in lines for p in line.split()]
    print(data)
    print(total)


INPUT = "aoc_dayXX_input.txt"
# INPUT = "aoc_dayXX_test.txt"


def main():
    with open(INPUT) as f:
        # read all in once
        data = f.read()
        solve(data)
        # read by lines
        # lines = f.readlines()
        # solve(lines)


if __name__ == "__main__":
    main()
