# https://adventofcode.com/2024/day/6
from pathlib import Path
import time


def is_out(pos, width, height):
    return pos.real < 0 or pos.real >= height or pos.imag < 0 or pos.imag >= width


def make_grid(data):
    grid = set()
    startpos = complex(0, 0)
    dir = complex(-1, 0)
    for r, row in enumerate(data):
        for c, item in enumerate(row):
            if item == '#':
                grid.add(complex(r, c))
            elif item == '^':
                startpos = complex(r, c)
    return grid, startpos


def walk_grid(grid, startpos, width, height):
    visited = set()
    pos = startpos
    dir = complex(-1, 0)
    while not is_out(pos, width, height):
        visited.add(pos)
        nextpos = pos + dir
        while nextpos in grid:
            dir = dir * -1j
            nextpos = pos + dir
        pos = nextpos
    return visited


def is_loop(grid, startpos, width, height):
    pos = startpos
    dir = complex(-1, 0)
    visited2 = set()
    while not is_out(pos, width, height):
        visited2.add((pos, dir))
        nextpos = pos + dir
        while nextpos in grid:
            dir = dir * -1j
            nextpos = pos + dir
        pos = nextpos
        if (pos, dir) in visited2:
            # we have a loop
            return True
    return False


def process(data):
    # part 1
    width, height = len(data[0]), len(data)
    grid, startpos = make_grid(data)
    visited = walk_grid(grid, startpos, width, height)
    print("part 1:", len(visited))

    # part 2
    visited.remove(startpos)
    total = 0
    for obstacle in visited:
        grid.add(obstacle)
        if is_loop(grid, startpos, width, height):
            total += 1
        grid.remove(obstacle)

    print("part 2:", total)


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
