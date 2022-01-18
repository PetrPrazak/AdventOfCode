# https://adventofcode.com/2018/day/17
from __future__ import print_function
from pathlib import Path
from collections import defaultdict

FLOW = '|'
WATER = '~'
WALL = '#'
EMPTY = ' '


def make_grid(data):
    grid = defaultdict(lambda: EMPTY)
    miny, maxy = 9999, 0
    for p1, p2 in data:
        axis, start, end = p2
        for r in range(start, end+1):
            coord = (r, p1[1]) if axis == 'x' else (p1[1], r)
            grid[coord] = WALL
        y = p1[1] if p1[0] == 'y' else p2[1]
        miny = min(miny, y)
        y = p1[1] if p1[0] == 'y' else p2[2]
        maxy = max(maxy, y)
    return grid, miny, maxy


def fill_grid(grid, miny, maxy):
    def pour(pos):
        x, y = pos
        while y <= maxy:
            ground = grid[pos]
            if ground == FLOW:
                break
            if ground == WATER:
                fill((x, y))
                break
            if ground == WALL:
                fill((x, y-1))
                break
            grid[pos] = FLOW
            y += 1
            pos = x, y

    def spill(pos, direction, leaks):
        while True:
            x, y = pos
            if grid[(x, y + 1)] == EMPTY:
                if grid[(x - direction, y + 1)] == WALL:
                    leaks.append(pos)
                return True
            if grid[(x, y)] == WALL:
                break
            grid[pos] = WATER
            pos = x + direction, y
        return False

    def flow(pos, direction):
        x, y = pos
        grid[pos] = FLOW
        x += direction
        while grid[(x, y)] == WATER:
            grid[(x, y)] = FLOW
            x += direction

    def fill(pos):
        origin_x, origin_y = pos
        leaks = []
        spilled = False
        while True:
            spilled = spill((origin_x, origin_y), 1, leaks)
            spilled = spill((origin_x, origin_y), -1, leaks) or spilled
            if spilled:
                break
            origin_y -= 1
        flow((origin_x, origin_y), -1)
        flow((origin_x, origin_y), 1)
        for pos in leaks:
            pour(pos)

    pour((500, miny))


def process(data):
    grid, miny, maxy = make_grid(data)
    fill_grid(grid, miny, maxy)
    # part 1
    result = sum(t == WATER or t == FLOW for t in grid.values())
    print("part 1:", result)
    # part 2
    result = sum(t == WATER for t in grid.values())
    print("part 2:", result)


def parse_line(line):
    def toint(t):
        return tuple(list(t[0]) + list(map(int, t[1].split('..'))))
    return tuple(toint(tuple(l.split('='))) for l in line.split(', '))


def load_data(fileobj):
    return [parse_line(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
