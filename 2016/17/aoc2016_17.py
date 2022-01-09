# https://adventofcode.com/2016/day/17
from __future__ import print_function
from pathlib import Path
from hashlib import md5
from heapq import heappop, heappush
from math import inf as INFINITY
import sys

sys.setrecursionlimit(10000)

def hash(password):
    return md5(password.encode('ascii')).hexdigest()[:4]


def dijkstra(start, target, moves_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        _, current = heappop(pq)
        if current[0] == target[0]:
            return current[1]
        for neighbor in moves_f(current):
            new_cost = path_cost[current] + 1
            if new_cost < path_cost.get(neighbor, INFINITY):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return None


MAXY, MAXX = 4, 4
NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
DIRS = "UDLR"


def moves(node):
    pos, password = node
    doors = [int(x, 16) > 10 for x in hash(password)]
    for i, ((off_x, off_y), move) in enumerate(zip(NEIGHBORS, DIRS)):
        x, y = pos[0] + off_x, pos[1] + off_y
        if 0 <= x < MAXX and 0 <= y < MAXY and doors[i]:
            yield (x, y), password + move


def path_len(password):
    return dijkstra(((0, 0), password), ((3, 3), None), moves)


def longest_path_len(password):
    def next_door(node):
        if node[0] == (3, 3):
            return 0
        all_moves = list(moves(node))
        if not all_moves:
            return -INFINITY
        return 1 + max(map(next_door, all_moves))
    return next_door(((0, 0), password))


def process(data):
    password = data[0]
    # part 1
    path = path_len(password)
    result = path[len(password):]
    print("part 1:", result)
    # part 2
    result = longest_path_len(password)
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
