# https://adventofcode.com/2021/day/9
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from math import prod


def neighbors4(grid, point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return filter(lambda p: p in grid, ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))


def make_grid(data):
    return {(x, y): data[y][x] for x in range(len(data[0])) for y in range(len(data))}


def get_low_points(grid):
    for coord, point in grid.items():
        if all(point < grid[n] for n in neighbors4(grid, coord)):
            yield coord, point


def get_basin(grid, point, visits=None):
    if visits is None:
        visits = set()
    elif point in visits:
        return 0
    visits.add(point)
    if grid[point] == 9:
        return 0
    return 1 + sum(get_basin(grid, p, visits) for p in neighbors4(grid, point))


def process(data):
    # part 1
    grid = make_grid(data)
    low_points = list(get_low_points(grid))
    result = sum(level+1 for _, level in low_points)
    print("part 1:", result)
    # part 2
    basins = sorted([get_basin(grid, coord) for coord, _ in low_points])
    result = prod(basins[-3:])
    print("part 2:", result)


def parse_line(line):
    return list(map(int, line.strip()))


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
