# https://adventofcode.com/2022/day/14
from pathlib import Path
from itertools import pairwise
from collections import deque
from copy import deepcopy
import re
import time

WALL, SAND, EMPTY = '#', 'o', '.'


def build_grid(data):
    grid, max_depth = {}, 0
    for line in data:
        for (x1, y1), (x2, y2) in pairwise(line):
            max_depth = max(max_depth, y1, y2)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[(x, y)] = WALL
    return grid, max_depth


def pour_sand(grid, max_depth, part=1):
    def grid_get(pos):
        if part == 2 and pos[1] >= max_depth:
            return WALL
        return grid.get(pos, EMPTY)

    grid = deepcopy(grid)
    path = deque((500, -1))
    pos = 500, 0
    while pos:
        pos_x, pos_y = pos
        while pos_y <= max_depth:
            for dx in (0, -1, 1):
                if grid_get((pos_x+dx, pos_y+1)) == EMPTY:
                    path.append(pos)
                    pos_x += dx
                    pos_y += 1
                    pos = pos_x, pos_y
                    break
            else:
                break
        if pos_y > max_depth:
            break
        grid[pos] = SAND
        if pos_y == 0:
            break
        pos = path.pop()
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
    return (parse_line(line.rstrip()) for line in fileobj.readlines())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
