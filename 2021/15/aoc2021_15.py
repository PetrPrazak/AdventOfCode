# https://adventofcode.com/2021/day/15
from __future__ import print_function
from pathlib import Path
from heapq import heappush, heappop


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


def dijkstra(start_vertex, value_f, moves_f):
    D = {start_vertex: 0}
    pq = [(0, start_vertex)]
    visited = set()
    while pq:
        _, current_vertex = heappop(pq)
        visited.add(current_vertex)
        for neighbor in moves_f(current_vertex):
            distance = value_f(neighbor)
            if neighbor not in visited:
                old_cost = D.get(neighbor, float('inf'))
                new_cost = D[current_vertex] + distance
                if new_cost < old_cost:
                    heappush(pq, (new_cost, neighbor))
                    D[neighbor] = new_cost
    return D


def get_lowest_path(data, part=1):
    def in_bounds(x, y):
        return x in range(size[0]) and y in range(size[1])

    def moves(node):
        if node == end_node:
            return []
        return [p for p in neighbors4(node) if in_bounds(*p)]

    def value(node):
        x, y = node
        if part == 1: return data[y][x]
        add_x, x = divmod(x, max_x)
        add_y, y = divmod(y, max_y)
        val = data[y][x] + add_x + add_y
        while val > 9: val -= 9
        return val

    max_x, max_y = len(data[0]), len(data)
    size = (max_x * 5, max_y * 5) if part == 2 else (max_x, max_y)
    end_node = size[0] - 1, size[1] - 1
    r = dijkstra((0,0), value, moves)
    return r[end_node]


def process(data):
    # part 1
    result = get_lowest_path(data, 1)
    print("part 1:", result)
    # part 2
    result = 0
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
