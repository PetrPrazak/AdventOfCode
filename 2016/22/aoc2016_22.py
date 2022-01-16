# https://adventofcode.com/2016/day/22
from __future__ import print_function
from pathlib import Path
from itertools import product
import re

# tuple order
# 0     1     2     3     4      5
# NodeX NodeY Size  Used  Avail  Use%


def make_grid(data):
    maxx = max(t[0] for t in data)
    maxy = max(t[1] for t in data)
    start, hole = None, None
    grid = [['.' for _ in range(maxx+1)] for _ in range(maxy+1)]
    for x, y, size, used, _, _ in data:
        if x == 0 and y == 0:
            node = 'S'
        elif x == maxx and y == 0:
            node = 'G'
        elif used == 0:
            hole = x, y
            node = '_'
        elif size > 250:
            if not start:
                start = x - 1, y
            node = '#'
        else:
            node = '.'
        grid[y][x] = node
    return grid, hole, start


def process(data):
    # part 1
    result = sum(
        a != b and a[3] and a[3] <= b[4]
        for a, b in product(data, repeat=2))
    print("part 1:", result)
    # part 2
    grid, hole, start = make_grid(data)
    # for line in grid:
    #     print(''.join(line))
    maxx = len(grid[0]) - 1
    result = abs(hole[0] - start[0]) + abs(hole[1] - start[1])
    result += abs(start[0] - maxx) + start[1]
    result += 5 * (maxx - 1)
    print("part 2:", result)


def parse_line(line):
    return tuple(map(int, re.findall('\d+', line)))


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()[2:]]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
