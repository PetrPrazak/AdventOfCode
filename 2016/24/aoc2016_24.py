# https://adventofcode.com/2016/day/24
from __future__ import print_function
from pathlib import Path
from itertools import permutations, combinations
from heapq import heappop, heappush
from math import inf as INFINITY


def dijkstra(start, target, moves_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        total, current = heappop(pq)
        if current == target:
            return total
        for neighbor in moves_f(current):
            new_cost = path_cost[current] + 1
            if new_cost < path_cost.get(neighbor, INFINITY):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return INFINITY


def path_len(grid, start, end):
    MAXY, MAXX = len(grid), len(grid[0])

    def moves(pos):
        for off_x, off_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = pos[0] + off_x, pos[1] + off_y
            if 0 <= x < MAXX and 0 <= y < MAXY and grid[y][x] != '#':
                yield x, y
    return dijkstra(start, end, moves)


def process(data):
    # part 1
    passages = {data[y][x]: (x, y)
                for y in range(len(data))
                for x in range(len(data[y]))
                if data[y][x].isdigit()}
    paths = {(s, e): path_len(data, passages[s], passages[e])
             for s, e in combinations(passages, 2)}
    targets = list(passages)
    targets.remove('0')
    shortest = 999999, None
    for path in permutations(targets):
        path = ('0',) + path
        length = sum(paths.get((a, b), paths.get((b, a)))
                     for a, b in zip(path, path[1:]))
        shortest = min((length, path), shortest)

    print("part 1:", shortest)
    # part 2
    shortest = 999999, None
    for path in permutations(targets):
        path = ('0',) + path + ('0',)
        length = sum(paths.get((a, b), paths.get((b, a)))
                     for a, b in zip(path, path[1:]))
        shortest = min((length, path), shortest)
    print("part 2:", shortest)


def load_data(fileobj):
    return [list(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
