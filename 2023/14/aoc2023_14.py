# https://adventofcode.com/2023/day/14
from pathlib import Path
from copy import deepcopy
import time

EMPTY, ROCK = '.', 'O'


def tilt_north(grid):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == ROCK:
                for r in range(row, 0, -1):
                    if grid[r-1][col] != EMPTY:
                        break
                    grid[r][col] = EMPTY
                    grid[r-1][col] = ROCK
    return grid


def tilt_south(grid):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows-2, -1, -1):
        for col in range(cols):
            if grid[row][col] == ROCK:
                for r in range(row, rows - 1):
                    if grid[r+1][col] != EMPTY:
                        break
                    grid[r][col] = EMPTY
                    grid[r+1][col] = ROCK

    return grid


def tilt_west(grid):
    for line in grid:
        for col, el in enumerate(line):
            if el == ROCK:
                for c in range(col, 0, -1):
                    if line[c-1] != EMPTY:
                        break
                    line[c] = EMPTY
                    line[c-1] = ROCK
    return grid


def tilt_east(grid):
    for line in grid:
        for col in range(len(line)-2, -1, -1):
            if line[col] == ROCK:
                for c in range(col, len(line) - 1):
                    if line[c+1] != EMPTY:
                        break
                    line[c] = EMPTY
                    line[c+1] = ROCK
    return grid


def rocks(grid):
    return frozenset((x, y) for x, row in enumerate(grid)
                     for y, c in enumerate(row) if c == ROCK)


def score(data):
    rows = len(data)
    total = sum(rows - col for row in zip(*data)
                for col, c in enumerate(row) if c == ROCK)
    return total


def process(data):
    # part 1
    grid = tilt_north(deepcopy(data))
    result = score(grid)
    print("part 1:", result)
    # part 2
    cycles = 1000000000
    states, scores = dict(), []
    last_state = None
    grid = data
    for pos in range(cycles):
        grid = tilt_north(grid)
        grid = tilt_west(grid)
        grid = tilt_south(grid)
        grid = tilt_east(grid)
        last_state = rocks(grid)
        if last_state in states:
            break
        states[last_state] = pos
        scores.append(score(grid))
    idx = states[last_state]
    cycle_len = pos - idx
    endpos = ((cycles - idx) % cycle_len) + idx - 1
    result = scores[endpos]
    print("part 2:", result)


def load_data(fileobj):
    return [list(line.rstrip()) for line in fileobj.readlines()]


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
