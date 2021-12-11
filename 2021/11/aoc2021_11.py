# https://adventofcode.com/2021/day/11
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from itertools import count, takewhile, islice


def make_grid(data):
    return {(x, y): int(data[y][x]) for x in range(len(data[0])) for y in range(len(data))}


def neighbors8(point):
    """The eight neighbors (with diagonals)."""
    x, y = point
    return ((x + 1, y),     (x - 1, y),     (x, y + 1),     (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1))


def simulate(grid):
    while True:
        for point in grid:
            grid[point] += 1

        flashed = set()
        to_flash = { point for point, level in grid.items() if level > 9 }
        while to_flash:
            flashed.update(to_flash)
            for point in to_flash:
                for n in neighbors8(point):
                    if n in grid:
                        grid[n] += 1
            to_flash = { point for point, level in grid.items() if level > 9 and point not in flashed }

        for point in flashed:
            grid[point] = 0
        yield len(flashed)


def process(data):
    # part 1
    grid = make_grid(data)
    size = len(grid)
    result = sum(islice(simulate(grid), 100))
    print("part 1:", result)
    # part 2
    # assume it happens after 100 cycles
    *_, step = takewhile(lambda r: r[0] != size, zip(simulate(grid), count(101)))
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
