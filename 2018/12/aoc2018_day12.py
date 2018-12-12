# https://adventofcode.com/2018/day/12

from __future__ import print_function
from collections import defaultdict, deque
from time import time

INPUT = "aoc2018_day12.txt"
# INPUT = "test.txt"


cat = ''.join


def process_rules(field, rules, pos):
    new_state = deque()
    for i in range(len(field) - 2):
        block = [field[q] for q in range(i - 2, i + 3)]
        new_state.append(rules[tuple(block)])

    # add empty pods to the left
    new_pos = pos + 1
    c = new_state.popleft()
    while c == 0:
        c = new_state.popleft()
        new_pos += 1
    new_state.extendleft([1, 0, 0, 0])
    new_pos -= 4

    # add empty pods to the right
    c = new_state.pop()
    while c == 0:
        c = new_state.pop()
    new_state.extend([1, 0, 0, 0])

    return new_state, new_pos


def print_field(field, pos):
    print(" %3d " % pos, end="")
    print(cat(['#' if c else '.' for c in field]))


def count_pods(field, pos):
    total = 0
    for c in field:
        total += pos if c else 0
        pos += 1
    return total


def make_generation(field, rules, cycles):
    pos = -3
    generations = {}
    state = tuple(field)
    prev_suma = count_pods(field, pos)
    generations[state] = 0, pos, prev_suma, prev_suma
    for iterace in range(1, cycles + 1):
        field, pos = process_rules(field, rules, pos)
        suma = count_pods(field, pos)

        state = tuple(field)
        snapshot = iterace, pos, suma, suma - prev_suma

        if state in generations:
            return snapshot

        generations[state] = snapshot
        prev_suma = suma
    return generations[state]


def process(data):
    init_state = data[0].split()[2]
    rules = defaultdict(int)
    for line in data[2:]:
        rule = line.split(" => ")
        l = [1 if c == "#" else 0 for c in rule[0]]
        rules[tuple(l)] = 1 if rule[1] == "#" else 0

    field = deque([0, 0, 0])
    for c in init_state:
        field.append(1 if c == '#' else 0)
    field.extend([0, 0, 0])

    iter_cycle, pos, suma, dif = make_generation(field, rules, 20)
    print(suma)

    # part 2
    total_cycle = 50000000000
    iter_cycle, pos, suma, dif = make_generation(field, rules, 120)
    print((total_cycle - iter_cycle) * dif + suma)


with open(INPUT) as f:
    data = [l.strip() for l in f.readlines()]
    process(data)
