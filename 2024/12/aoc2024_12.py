# https://adventofcode.com/2024/day/12
from pathlib import Path
from collections import defaultdict, deque
from enum import Enum
import time


class Side(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def neighbors(pos):
    r, c = pos
    for nr, nc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
        yield nr, nc


def find_plot(grid, height, width, pos):
    land = grid[pos]
    q = deque([pos])
    seen = set([pos])
    while q:
        pos = q.popleft()
        for nr, nc in neighbors(pos):
            if nr < 0 or nr >= height or nc < 0 or nc >= width:
                continue
            npos = nr, nc
            if npos not in seen and grid[npos] == land:
                seen.add(npos)
                q.append(npos)
    return seen


def first(s):
    for e in s:
        break
    return e


def perimeter(grid, height, width, area):
    land = grid[first(area)]
    edges, total = set(), 0
    for pos in area:
        for nr, nc in neighbors(pos):
            if nr < 0 or nr >= height or nc < 0 or nc >= width or grid[(nr, nc)] != land:
                total += 1
                edges.add(pos)
    return total, edges


def count_groups(nums):
    first = nums[0]
    total = 1
    for n in nums[1:]:
        if n != first+1:
            total += 1
        first = n
    return total


def count_sides(area, edges):
    sides = defaultdict(set)
    for pos in edges:
        r, c = pos
        if (r-1, c) not in area:
            sides[(r, Side.UP)].add(pos)
        if (r+1, c) not in area:
            sides[(r, Side.DOWN)].add(pos)
        if (r, c-1) not in area:
            sides[(c, Side.LEFT)].add(pos)
        if (r, c+1) not in area:
            sides[(c, Side.RIGHT)].add(pos)

    total = 0
    for (_, d), s in sides.items():
        nums = sorted(n[d in (Side.UP, Side.DOWN)] for n in s)
        total += count_groups(nums)

    return total


def process(data):
    height, width = len(data), len(data[0])
    grid = {(r, c): l for r, row in enumerate(data) for c, l in enumerate(row)}
    # part 1
    area = set(grid)
    plots = []
    while area:
        spos = first(area)
        plot = find_plot(grid, height, width, spos)
        plots.append(plot)
        area -= plot

    result = sum(len(plot) * perimeter(grid, height, width, plot)[0]
                 for plot in plots)
    print("part 1:", result)
    # part 2
    result = sum(len(plot) * count_sides(plot, perimeter(grid, height, width, plot)[1])
                 for plot in plots)
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
