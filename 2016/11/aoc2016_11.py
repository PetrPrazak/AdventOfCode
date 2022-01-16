# https://adventofcode.com/2016/day/11
from __future__ import print_function
from pathlib import Path
from itertools import combinations
from copy import copy, deepcopy
from math import inf as INFINITY
from heapq import heappop, heappush
import re


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
    return None


def add_dict(thelist, item):
    # if the item exist in the list returns its index
    # other it is added
    if item in thelist:
        return thelist.index(item)
    thelist.append(item)
    return len(thelist) - 1


def build_state(data):
    # the state = tuple of sets of object, index is the floor - 1
    # object is a tuple: first part : 1 - generator, 0 - chip, second the element
    names, state = [], []
    for gen, chip in data:
        objects = set()
        for g in gen:
            objects.add((1, add_dict(names, g)))
        for c in chip:
            objects.add((0, add_dict(names, c)))
        state.append(objects)
    return names, tuple(state)


def is_allowed(floor, state):
    # chip can't be alone on a floor with other generator
    objects = state[floor]
    for typ, kind in objects:
        if typ == 0 and (1, kind) not in objects:
            return False
    return True


def freeze_state(state):
    return tuple(frozenset(s) for s in state)


def move_objects(state, objects, floor, dif):
    newstate = [set(s) for s in state]
    newstate[floor].difference_update(objects)
    newstate[floor+dif].update(objects)
    newstate = freeze_state(newstate)
    if is_allowed(floor+dif, newstate):
        yield floor+dif, newstate


def solve(state):
    names, config = state
    target = [set() for _ in range(4)]
    for idx in range(len(names)):
        target[3].add((1, idx))
        target[3].add((0, idx))
    target = 3, freeze_state(target)

    def moves(node):
        elevator, state = node
        floor_state = state[elevator]
        up_moves = []
        if elevator < 3:
            # move up
            for obj1, obj2 in combinations(floor_state, 2):
                up_moves.extend(list(move_objects(state, {obj1, obj2}, elevator, 1)))
            if not up_moves:
                for obj in floor_state:
                    up_moves.extend(list(move_objects(state, {obj}, elevator, 1)))
        down_moves = []
        if elevator > 0:
            # move down
            for obj in floor_state:
                down_moves.extend(list(move_objects(state, {obj}, elevator, -1)))
            if not down_moves:
                for obj1, obj2 in combinations(floor_state, 2):
                    down_moves.extend(list(move_objects(state, {obj1, obj2}, elevator, -1)))
        return up_moves + down_moves

    return dijkstra((0, freeze_state(config)), target, moves)


def process(data):
    state = build_state(data)
    # # part 1
    result = solve(state)
    print("part 1:", result)
    # part 2
    elerium = add_dict(state[0], "elerium")
    dilithium = add_dict(state[0], "dilithium")
    state[1][0].update({(0, elerium), (1, elerium),
                       (0, dilithium), (1, dilithium)})
    result = solve(state)
    print("part 2:", result)


def parse_line(line):
    gens = list(re.findall('a (\w+) generator', line))
    chips = list(re.findall('a (\w+)-compatible microchip', line))
    return gens, chips


def load_data(fileobj):
    return [parse_line(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
