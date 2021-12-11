# https://adventofcode.com/2021/day/11
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from itertools import count, takewhile


def make_grid(data):
    return {(x, y): int(data[y][x]) for x in range(len(data[0])) for y in range(len(data))}


def neighbors8(point):
    """The eight neighbors (with diagonals)."""
    x, y = point
    return ((x + 1, y),     (x - 1, y),     (x, y + 1),     (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1))


def simulate(grid):
    def check_flash(grid, point):
        if grid[point] > 9:
            grid[point] = 0
            for n in neighbors8(point):
                if n in grid and grid[n]:
                    grid[n] += 1
                    check_flash(grid, n)
    while True:
        for point in grid:
            grid[point] += 1
        for point in grid:
            check_flash(grid, point)
        yield sum(v == 0 for v in grid.values())


def process(data):
    # part 1
    grid = make_grid(data)
    result = sum(map(lambda r: r[0], zip(simulate(grid), range(100))))
    print("part 1:", result)
    # part 2
    grid = make_grid(data)
    *_, step = takewhile(lambda r: r[0] != 100, zip(simulate(grid), count(1)))
    result = step[1] + 1  # the last pair is not returned
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
