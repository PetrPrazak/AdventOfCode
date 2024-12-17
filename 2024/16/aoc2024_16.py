# https://adventofcode.com/2024/day/16
from pathlib import Path
import time
from heapq import heappush, heappop
from math import inf as INFINITY
import networkx as nx


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    r, c = point
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for d in dirs:
        yield (r + d[0], c + d[1]), d


def dijkstra(start, target, moves_f, end_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        total, current = heappop(pq)
        if end_f(current, target):
            return total
        for neighbor, value in moves_f(current):
            new_cost = path_cost[current] + value
            if new_cost < path_cost.get(neighbor, INFINITY):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return None, None


def shortest_path(grid, start, target):
    def value_f(dir, new_dir): return 1 if dir == new_dir else 1001

    def move(pos):
        pos, dir = pos
        for new_pos, new_dir in neighbors4(pos):
            if (grid.get(new_pos, '#')) != '#':
                yield (new_pos, new_dir), value_f(dir, new_dir)

    def endpos(curr, target):
        return curr[0] == target[0]

    return dijkstra((start, (0, 1)), (target, (0, 0)), move, endpos)


def print_grid(grid, prev=None):
    W = max(c for _, c in grid) + 1
    H = max(p for p, _ in grid) + 1
    if not prev:
        prev = dict()
    for r in range(H):
        line = "".join(
            "O" if (r, c) in prev else grid[(r, c)] for c in range(W))
        print(line)
    print()


def use_bigger_hammer(data):
    g = {(x, y): c
         for y, r in enumerate(data)
         for x, c in enumerate(r)}
    s = min(k for k, v in g.items() if v == 'S')
    e = min(k for k, v in g.items() if v == 'E')

    n = nx.DiGraph()
    for (x, y), c in g.items():
        if c != '#':
            for d in range(4):
                dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][d]
                n.add_edge((x, y, d), (x + dx, y + dy, d), weight=1)
                n.add_edge((x, y, d), (x, y, (d - 1) % 4), weight=1000)
                n.add_edge((x, y, d), (x, y, (d + 1) % 4), weight=1000)

    m = [nx.shortest_path_length(n, (*s, 0), (*e, d), "weight")
         for d in range(4)]
    all_paths = nx.all_shortest_paths(n, (*s, 0), (*e, d), "weight")
    cells = len(set(tuple(p) for d in range(4) if m[d] == min(m)
                    for t in all_paths
                    for *p, h in t))
    return min(m), cells


def process(data):
    grid, start, end = dict(), None, None
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            grid[(r, c)] = cell
            if cell == 'S':
                start = r, c
            elif cell == 'E':
                end = r, c
    # part 1
    result = shortest_path(grid, start, end)
    print("part 1:", result)
    # part 2
    part1, part2 = use_bigger_hammer(data)
    print("part 1:", part1)
    print("part 2:", part2)


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
