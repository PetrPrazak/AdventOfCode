# https://adventofcode.com/2019/day/13
from __future__ import print_function
import re
import math
import urllib.request
from collections import Counter, defaultdict, namedtuple, deque
from functools import lru_cache
from itertools import permutations, combinations, chain, cycle, product, islice
from heapq import heappop, heappush
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *
from aoc.intcode import IntCode, single_run
from enum import Enum

INPUT = "aoc2019_13_input.txt"
TEST = "test.txt"


class Object(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def get_pixel(self):
        if self == Object.WALL:
            pixel = 'x'
        elif self == Object.BLOCK:
            pixel = '#'
        elif self == Object.PADDLE:
            pixel = '_'
        elif self == Object.BALL:
            pixel = 'o'
        else:
            pixel = ' '
        return pixel


SCORE_POS = (-1, 0)


def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=lambda k: k[element])
    return res[0][element], res[-1][element]


def print_grid(grid):
    coords = list(grid.keys())
    min_x, max_x = minmax_tuples(coords, 0)
    min_y, max_y = minmax_tuples(coords, 1)
    screen = ""
    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            pos = col, line
            screen += grid[pos].get_pixel()
        screen += '\n'
    print(screen)


def process_instruction(grid, instruction):
    pos = instruction[0], instruction[1]
    score = None
    if pos == SCORE_POS:
        score = instruction[2]
    else:
        grid[pos] = Object(instruction[2])
    return score


def make_grid(output):
    tiles = [output[i:i + 3] for i in range(0, len(output), 3)]
    grid = dict()
    score = None
    for tile in tiles:
        score = process_instruction(grid, tile)
    return grid, score


def reverse_grid(grid):
    revgrid = defaultdict(list)
    for pos, item in grid.items():
        revgrid[item].append(pos)
    return revgrid


def get_blocks_count(grid):
    return Counter(grid.values())[Object.BLOCK]


def init_run(proc, single_input):
    output = []
    while True:
        try:
            x = next(proc)
            y = proc.send(single_input)
            item = proc.send(single_input)
            output.append(x)
            output.append(y)
            output.append(item)
            if x == -1 and y == 0:
                break
        except StopIteration:
            break
    return output


def read_one_instruction(proc, single_input):
    output = [proc.send(single_input) for _ in range(3)]
    return output


def move_joystick(ball, paddle):
    return 0 if ball == paddle else -1 if ball < paddle else 1


def play(program):
    program[0] = 2
    processor = IntCode(program)
    proc = processor.run()
    out = init_run(proc, 0)
    grid, score = make_grid(out)
    print_grid(grid)
    revgrid = reverse_grid(grid)
    ball = revgrid[Object.BALL][0][0]
    paddle = revgrid[Object.PADDLE][0][0]
    joystick = 0
    score = 0
    cycles = 0
    while True:
        instruction = read_one_instruction(proc, joystick)
        s = process_instruction(grid, instruction)
        if s is not None:
            score = s
            if get_blocks_count(grid) == 0:
                break
        else:
            obj = Object(instruction[2])
            if obj == Object.BALL:
                cycles += 1
                ball = instruction[0]
                # handle joystick only if ball has changed
                joystick = move_joystick(ball, paddle)
            elif obj == Object.PADDLE:
                paddle = instruction[0]

    print(score, cycles)


@timeit
def process(data):
    out = single_run(data)
    grid, _ = make_grid(out)
    # part 1
    print(get_blocks_count(grid))
    # print_grid(grid)
    # part 2
    play(data)


def main():
    data = read_input_ints_separated(INPUT)
    process(data)


if __name__ == "__main__":
    main()
