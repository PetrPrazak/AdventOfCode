# https://adventofcode.com/2021/day/15
from __future__ import print_function
import time
from pathlib import Path
from heapq import heappush, heappop
from functools import wraps
from math import inf as INFINITY

def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f'{method.__name__} {(te - ts) * 1000:2.2f} ms')
        return result
    return timed


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


def dijkstra(start_vertex, target, value_f, moves_f):
    D = {start_vertex: 0}
    pq = [(0, start_vertex)]
    while pq:
        total, current_vertex = heappop(pq)
        if current_vertex == target:
            return total
        if total <= D[current_vertex]:
            for neighbor in moves_f(current_vertex):
                old_cost = D.get(neighbor, INFINITY)
                new_cost = total + value_f(neighbor)
                if new_cost < old_cost:
                    heappush(pq, (new_cost, neighbor))
                    D[neighbor] = new_cost
    return INFINITY


@timeit
def get_lowest_path(data, part=1):
    def in_bounds(x, y):
        return x in range(size[0]) and y in range(size[1])

    def moves(node):
        return [p for p in neighbors4(node) if in_bounds(*p)]

    def value(node):
        x, y = node
        if part == 1: return data[y][x]
        add_x, x = divmod(x, max_x)
        add_y, y = divmod(y, max_y)
        val = data[y][x] + add_x + add_y
        val = (val - 1) % 9 + 1
        return val

    scale = 5 if part == 2 else 1
    max_x, max_y = len(data[0]), len(data)
    size = (max_x * scale, max_y * scale)
    end_node = size[0] - 1, size[1] - 1
    r = dijkstra((0,0), end_node, value, moves)
    return r


def process(data):
    # part 1
    result = get_lowest_path(data, 1)
    print("part 1:", result)
    # part 2
    result = get_lowest_path(data, 2)
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
