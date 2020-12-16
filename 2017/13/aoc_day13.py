
"""

http://adventofcode.com/2017/day/13


"""
from __future__ import print_function


def solve(lines):
    # init
    parts = [line.strip().split(': ') for line in lines]
    layers = {int(pos): int(height) for pos, height in parts}

    # part 1
    print(sum([n * layers[n] for n in layers if not n % ((layers[n] - 1) * 2)]))

    # part 2
    for d in range(0, 10000000, 2):
        try:
            next(iter(n for n in layers if not (n + d) % ((layers[n] - 1) * 2)))
        except StopIteration:
            print(d)
            break


INPUT = "aoc_day13_input.txt"
# INPUT = "aoc_day13_test.txt"

if __name__ == "__main__":
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)
