# https://adventofcode.com/2022/day/14
from pathlib import Path
from itertools import pairwise
from copy import deepcopy
import re

WALL, SAND, EMPTY = '#', 'o', '.'

def build_grid(data):
    grid, max_depth = {}, 0
    for line in data:
        for (x1, y1), (x2, y2) in pairwise(line):
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            max_depth = max(max_depth, y2)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[(x, y)] = WALL
    return grid, max_depth


def pour_sand(grid, max_depth, part=1):
    def grid_get(pos):
        if part == 2 and pos[1] >= max_depth:
            return WALL
        return grid.get(pos, EMPTY)

    grid = deepcopy(grid)
    while True:
        pos_x, pos_y = 500, 0
        while pos_y <= max_depth:
            for dx, dy in [(0,1), (-1, 1), (1, 1)]:
                if grid_get((pos_x+dx, pos_y+dy)) == EMPTY:
                    pos_x += dx
                    pos_y += dy
                    break
            else:
                break
        if pos_y > max_depth:
            break
        grid[(pos_x, pos_y)] = SAND
        if pos_y == 0:
            break
    return sum(c == SAND for c in grid.values())


def process(data):
    # part 1
    grid, max_depth = build_grid(data)
    result = pour_sand(grid, max_depth, part=1)
    print("part 1:", result)
    # part 2
    result = pour_sand(grid, max_depth + 2, part=2)
    print("part 2:", result)


def parse_line(line):
    gen = map(int, re.findall('\d+', line))
    return list(zip(gen, gen))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
