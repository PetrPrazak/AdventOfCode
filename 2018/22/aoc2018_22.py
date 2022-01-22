# https://adventofcode.com/2018/day/22
from __future__ import print_function
from pathlib import Path
from functools import lru_cache
from heapq import heappush, heappop
from math import inf


def dijkstra(start, target, moves_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        total, current = heappop(pq)
        if current == target:
            return total
        for neighbor, value in moves_f(current):
            new_cost = path_cost[current] + value
            if new_cost < path_cost.get(neighbor, inf):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return None


class Cave:
    neither = 0
    torch = 1
    climbing = 2
    rocky = 0  # gear or torch
    wet = 1  # gear or neither
    narrow = 2  # torch or neither

    def __init__(self, data) -> None:
        self.depth = data['depth'][0]
        self.target = data['target']

    @lru_cache(maxsize=None)
    def erosion_level(self, pos):
        return (self.geologic_index(pos) + self.depth) % 20183

    def geologic_index(self, pos):
        if pos == (0, 0) or pos == self.target:
            return 0
        x, y = pos
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return self.erosion_level((x-1, y)) * self.erosion_level((x, y-1))

    def region_type(self, pos):
        return self.erosion_level(pos) % 3

    def area_risk_level(self):
        return sum(self.region_type((x, y))
                   for y in range(self.target[1] + 1)
                   for x in range(self.target[0] + 1))

    def shortest_path(self):
        def allowed_tools(region):
            if region == Cave.rocky:
                return [Cave.climbing, Cave.torch]
            if region == Cave.wet:
                return [Cave.neither, Cave.climbing]
            if region == Cave.narrow:
                return [Cave.neither, Cave.torch]

        def moves(pos):
            item, pos = pos
            terrain = self.region_type(pos)
            for tool in allowed_tools(terrain):
                if tool != item:
                    yield (tool, pos), 7
            x, y = pos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                newx, newy = x + dx, y + dy
                if 0 <= newx and 0 <= newy:
                    newpos = newx, newy
                    terrain = self.region_type(newpos)
                    if terrain != item:
                        # the terrain index is the same as object index
                        # that is not allowed for the terrain
                        yield (item, newpos), 1

        start = 0, 0
        return dijkstra((Cave.torch, start), (Cave.torch, self.target), moves)


def process(data):
    # part 1
    cave = Cave(data)
    result = cave.area_risk_level()
    print("part 1:", result)
    # part 2
    result = cave.shortest_path()
    print("part 2:", result)


def parse_line(line):
    kw, data = line.split(': ')
    return kw, tuple(map(int, data.split(',')))


def load_data(fileobj):
    return dict(parse_line(line.strip()) for line in fileobj.readlines())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
