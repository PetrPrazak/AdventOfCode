# https://adventofcode.com/2019/day/11
from __future__ import print_function
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import read_input_ints_separated
from aoc.intcode import IntCode
from collections import defaultdict
from enum import Enum

INPUT = "aoc2019_11_input.txt"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_left(self):
        return Direction((self.value + 3) % 4)

    def turn_right(self):
        return Direction((self.value + 1) % 4)

    def step(self):
        return [(0, -1), (1, 0), (0, 1), (-1, 0)][self.value]


def process(program, seed):
    panels = defaultdict(int)
    proc = IntCode(program).run()
    next(proc)

    d = Direction.UP
    pos = (0, 0)
    panels[pos] = seed
    while True:
        try:
            panels[pos] = proc.send(panels[pos])
            new_dir = next(proc)
            if new_dir == 0:
                d = d.turn_left()
            else:
                d = d.turn_right()
            step = d.step()
            pos = pos[0] + step[0], pos[1] + step[1]
        except StopIteration:
            break
    return panels


def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=lambda k: k[element])
    return res[0][element], res[-1][element]


def print_panels(panels):
    coords = list(panels.keys())
    min_x, max_x = minmax_tuples(coords, 0)
    min_y, max_y = minmax_tuples(coords, 1)
    print((min_x, min_y), (max_x, max_y))
    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            pos = col, line
            pixel = '#' if pos in panels and panels[pos] == 1 else ' '
            print(pixel, sep="", end="")
        print("")


def main():
    program = read_input_ints_separated(INPUT)
    # part 1
    panels = process(program, 0)
    print(len(panels.keys()))  # 2041
    # part 2
    panels = process(program, 1)
    print_panels(panels)  # ZRZPKEZR


if __name__ == "__main__":
    main()
