# https://adventofcode.com/2021/day/9
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from math import prod


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


def make_grid(data):
    grid = dict()
    for y in range(len(data)):
        for x in range(len(data[0])):
            grid[(x, y)] = data[y][x]
    return grid


def get_low_points(grid):
    for coord, point in grid.items():
        if all(n not in grid or point < grid[n] for n in neighbors4(coord)):
            yield coord, point


def get_basin(grid, point, level=None, visits=None):
    if visits is None:
        visits = set()
    if point not in grid or point in visits:
        return 0
    visits.add(point)
    val = grid[point]
    if val == 9:
        return 0
    return 1 + sum(get_basin(grid, p, val, visits) for p in neighbors4(point))


def process(data):
    # part 1
    grid = make_grid(data)
    low_points = list(get_low_points(grid))
    result = sum(level+1 for _, level in low_points)
    print("part 1:", result)
    # part 2
    basins = sorted([get_basin(grid, coord) for coord, _ in low_points], reverse=True)
    result = prod(basins[:3])
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
