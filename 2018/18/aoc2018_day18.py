# https://adventofcode.com/2018/day/18

from __future__ import print_function
from collections import Counter

INPUT = "aoc2018_day18.txt"
# INPUT = "test.txt"

cat = ''.join


def neighbors8(point, maxx, maxy):
    """The eight neighbors (with diagonals)."""
    x, y = point
    r = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
         (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
    return [(x, y) for x, y in r if 0 <= x < maxx and 0 <= y < maxy]


def get_adjacent(grid, adj, field_type):
    return [(x, y) for x, y in adj if grid[y][x] == field_type]


def make_change(grid):
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, field in enumerate(row):
            n = neighbors8((x, y), len(row), len(grid))
            if field == '.':
                if len(get_adjacent(grid, n, '|')) >= 3:
                    field = '|'
            elif field == '|':
                if len(get_adjacent(grid, n, '#')) >= 3:
                    field = '#'
            elif field == '#':
                if len(get_adjacent(grid, n, '#')) == 0 or len(get_adjacent(grid, n, '|')) == 0:
                    field = '.'
            new_row.append(field)
        new_grid.append(new_row)
    return new_grid


def print_grid(grid):
    for row in grid:
        print(cat(row))
    print("")


def grid_tuple(grid):
    r = []
    for row in grid:
        r.extend(row)
    return tuple(r)


def process(grid):
    # part 1
    # print_grid(grid)
    for _ in range(10):
        grid = make_change(grid)
        # print_grid(grid)

    c = Counter()
    for row in grid:
        c.update(row)
    print(c['|'] * c['#'])

    # part 2
    total_run = 1000000000
    grid_mem = dict()
    grid_mem[grid_tuple(grid)] = 10
    cycle_start = 0
    for itr in range(10, total_run):
        newgrid = make_change(grid)
        t = grid_tuple(newgrid)
        if t in grid_mem:
            cycle_start = grid_mem[t]
            break
        grid_mem[t] = itr
        grid = newgrid

    remain = (total_run - itr) % (itr - cycle_start)
    for _ in range(remain):
        grid = make_change(grid)

    cc = Counter()
    for row in grid:
        cc.update(row)
    print(cc['|'] * cc['#'])


with open(INPUT) as f:
    data = [l.rstrip() for l in f.readlines()]
    process(data)
