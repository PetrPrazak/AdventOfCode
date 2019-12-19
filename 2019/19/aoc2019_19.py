# https://adventofcode.com/2019/day/19
from __future__ import print_function
from collections import Counter
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *
from aoc.intcode import IntCode

INPUT = "aoc2019_19_input.txt"


def get_state(processor, x, y):
    processor.reset_mem()
    proc = processor.run()
    inp = next(proc)
    assert inp == "Input"
    proc.send(x)
    state = proc.send(y)
    return state


@timeit
def part1(data):
    processor = IntCode(data)
    grid = dict()
    for y in range(50):
        for x in range(50):
            state = get_state(processor, x, y)
            grid[(x, y)] = state
    c = Counter(grid.values())
    print(c[1])  # 197


@timeit
def part2(data):
    # part 2
    processor = IntCode(data)
    x = 5
    y = 6
    while True:
        x += 1
        y += 1
        if get_state(processor, x, y) == 0:
            x -= 1  # it's not always 45 degrees !!

        if x < 100:  # to avoid feeding negative position
            continue

        # square of len 100 - ergo position is 99 less :facepalm:
        if get_state(processor, x - 99, y + 99) == 1:
            break
    print(10000 * (x - 99) + y)  # 9181022


def main():
    data = read_input_ints_separated(INPUT)
    part1(data)
    part2(data)


if __name__ == "__main__":
    main()
