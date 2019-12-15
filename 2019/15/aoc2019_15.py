# https://adventofcode.com/2019/day/15
from __future__ import print_function
from random import choice
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *
from aoc.intcode import IntCode

INPUT = "aoc2019_15_input.txt"


def next_pos(pos, direction):
    dx, dy = [(0, -1), (0, 1), (1, 0), (-1, 0)][direction]
    return pos[0] + dx, pos[1] + dy


def next_direction(grid, pos, direction):
    possible_directions = [1, 3, 2, 0]
    paths = []
    while True:
        direction = choice(possible_directions)
        possible_directions.remove(direction)
        check_pos = next_pos(pos, direction)
        if check_pos in grid:
            if grid[check_pos] == '#':
                if not possible_directions:
                    # return direction
                    if paths:
                        return choice(paths)
                    raise Exception
            else:
                paths.append(direction)
                if not possible_directions:
                    return choice(paths)
        else:
            return direction


def scan_grid(grid, program):
    proc = IntCode(program[:]).run()
    next(proc)
    direction = 0
    pos = 0, 0
    steps = 0
    while True:
        grid[pos] = '.'
        status = proc.send(direction + 1)
        if status == 0:  # wall
            grid[next_pos(pos, direction)] = '#'
        elif status == 2:  # oxygen
            grid[(0, 0)] = 'S'
            pos = next_pos(pos, direction)
            grid[pos] = 'O'
            break
        elif status == 1:  # empty
            pos = next_pos(pos, direction)
            grid[pos] = '*'
        direction = next_direction(grid, pos, direction)
        steps += 1
    return pos, proc


def shortest_path(grid, proc, pos):
    # now to find shortest path to start
    path = [pos]
    direction = 0
    steps = 0
    while True:
        grid[pos] = '.'
        status = proc.send(direction + 1)
        if status == 0:  # wall
            wall_pos = next_pos(pos, direction)
            grid[wall_pos] = '#'
        elif pos == (0, 0):  # start position
            break
        else:  # empty or oxygen
            prevpos = path[-1]
            newpos = next_pos(pos, direction)
            if prevpos != newpos:
                path.append(pos)
            else:
                path.pop()
            pos = newpos
            grid[pos] = '*'

        direction = next_direction(grid, pos, direction)
        steps += 1
    print(len(path) - 1)  # 308


def fill_oxygen(grid, start_pos, time=0, max_time=0):
    """Recursively spread oxygen and keep track of the maximum depth."""
    neighbours = [next_pos(start_pos, d) for d in range(4)]
    for neighbour in neighbours:
        if grid[neighbour] == '.':
            grid[neighbour] = 'O'
            max_time = fill_oxygen(grid, neighbour, time + 1, max_time)
    return max(time, max_time)


@timeit
def part1(data, part):
    grid = dict()
    oxygen_pos, proc = scan_grid(grid, data)
    shortest_path(grid, proc, oxygen_pos)


def part2(grid, start_pos):
    minute = fill_oxygen(grid, start_pos)
    print(minute)  # 328


def load_grid():
    grid = dict()
    data = read_input_lines("grid.txt")
    center_x, center_y = 19, 21
    oxygen_pos = None
    for y, line in enumerate(data):
        for x, pixel in enumerate(line.rstrip()):
            pos = x - center_x, y - center_y
            if pixel == ' ':
                continue
            if pixel == 'S':
                assert pos == (0, 0)
                pixel = '.'
            elif pixel == 'O':
                oxygen_pos = pos
            grid[pos] = pixel
    return grid, oxygen_pos


def main():
    data = read_input_ints_separated(INPUT)
    part1(data, 1)
    grid, oxygen_pos = load_grid()
    part2(grid, oxygen_pos)


if __name__ == "__main__":
    main()
