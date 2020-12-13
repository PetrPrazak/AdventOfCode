# http://adventofcode.com/2016/day/XX
from __future__ import print_function
from collections import defaultdict, Counter
from pprint import pprint


def solve(lines):
    # part 1
    result = 0
    print("Part 1:", result)
    # part 2
    result = 0
    print("Part 2:", result)


def parse(line):
    return line


def main(file):
    with open(file) as f:
        # read all in once
        data = f.read()
        solve(data)
        # or read by lines
        lines = [parse(l.strip()) for l in f.readlines()]
        solve(lines)


if __name__ == "__main__":
    main("input.txt")