# https://adventofcode.com/2025/day/4
from pathlib import Path
import time


def neighbors(x, y):
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            yield x + dx, y + dy


def accesibles(grid: set) -> set:
    return {
        (x, y)
        for x, y in grid
        if sum((nx, ny) in grid for nx, ny in neighbors(x, y)) < 4
    }


def part1(grid: set):
    return len(accesibles(grid))


def part2(grid: set):
    acc = 0
    while (positions := accesibles(grid)):
        acc += len(positions)
        grid -= positions
    return acc


def process(data):

    grid = {(x, y)
            for y, line in enumerate(data)
            for x, c in enumerate(line)
            if c == '@'}
    # part 1
    result = part1(grid)
    print("part 1:", result)
    # part 2
    result = part2(grid)
    print("part 2:", result)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
