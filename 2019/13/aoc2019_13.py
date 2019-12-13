# https://adventofcode.com/2019/day/13
from __future__ import print_function
from collections import Counter, defaultdict
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *
from aoc.intcode import IntCode, single_run
from enum import Enum
import render
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
    render.print_grid(grid)
    revgrid = reverse_grid(grid)
    ball = revgrid[Object.BALL][0][0]
    paddle = revgrid[Object.PADDLE][0][0]
    joystick = 0
    score = 0
    cycles = 0
    # render.save_grid(grid, cycles)
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
                # render.save_grid(grid, cycles)
                # if cycles > 100:
                #     break
                ball = instruction[0]
                # handle joystick only if ball has changed
                joystick = move_joystick(ball, paddle)
            elif obj == Object.PADDLE:
                paddle = instruction[0]

    print(score, cycles)


@timeit
def process(data):
    out = single_run(data)
    # part 1
    grid, _ = make_grid(out)
    print(get_blocks_count(grid))
    # part 2
    play(data)


def main():
    data = read_input_ints_separated(INPUT)
    process(data)


if __name__ == "__main__":
    main()
