# https://adventofcode.com/2022/day/23
from pathlib import Path
from collections import defaultdict
from copy import copy
from math import inf
import time


NORTH = (-1 - 1j, -1j, 1 - 1j)
SOUTH = (-1 + 1j, 1j, 1 + 1j)
WEST = (-1 + 1j, -1 + 0j, -1 - 1j)
EAST = (1 + 1j, 1 + 0j, 1 - 1j)
DIRS = [NORTH, SOUTH, EAST, WEST]
AROUND = {off for d in DIRS for off in d}


def is_around(data, elf, side=None):
    if side is None:
        side = AROUND
    return any(elf + off in data for off in side)


# north, south, west, east
MOVES = [(NORTH, -1j), (SOUTH, 1j), (WEST, -1 + 0j), (EAST, 1 + 0j)]


def round(data, round_num):
    candidates = defaultdict(set)
    d_idx = round_num % len(MOVES)
    directions = MOVES[d_idx:] + MOVES[:d_idx]
    for elf in data:
        if not is_around(data, elf):
            continue
        for side, off in directions:
            newpos = elf + off
            if is_around(data, elf, side):
                continue
            if newpos not in data:
                candidates[newpos].add(elf)
                break

    if not candidates:
        return None

    movers = dict(
        (pos, newpos)
        for newpos, elfs in candidates.items()
        for pos in elfs
        if len(elfs) == 1
    )
    new_state = data.difference(set(movers.keys())).union(set(movers.values()))
    return new_state


def bounds(data):
    min_x, min_y, max_x, max_y = inf, inf, -inf, -inf
    for elf in data:
        col, row = elf.real, elf.imag
        min_x, min_y = min(min_x, col), min(min_y, row)
        max_x, max_y = max(max_x, col), max(max_y, row)
    return (int(min_x), int(max_x)), (int(min_y), int(max_y))


def count_space(data):
    (min_x, max_x), (min_y, max_y) = bounds(data)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(data)


def process(data):
    part2_data = copy(data)
    # part 1
    for r in range(10):
        data = round(data, r)
    result = count_space(data)
    print("part 1:", result)
    # part 2
    r = 0
    data = part2_data
    while True:
        new_data = round(data, r)
        if not new_data:
            break
        r += 1
        data = new_data
    result = r + 1
    print("part 2:", result)


def load_data(fileobj):
    return {
        (x + y * 1j)
        for y, line in enumerate(fileobj.read().split("\n"))
        for x, elf in enumerate(line)
        if elf == "#"
    }


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
