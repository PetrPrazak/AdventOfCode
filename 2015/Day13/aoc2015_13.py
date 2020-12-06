# http://adventofcode.com/2015/day/13
from __future__ import print_function
from collections import defaultdict
from itertools import permutations


def sum_neighbors(relations, order, idx, person):
    return relations[order[idx - 1]] + relations[order[(idx + 1) % len(order)]]


def calculate_happiness(graph, order):
    return sum(sum_neighbors(graph[person], order, idx, person)
               for idx, person in enumerate(order))


def get_max_happiness(graph):
    return max(calculate_happiness(graph, list(perm))
               for perm in permutations(graph.keys()))


def process(graph):
    # part 1
    result = get_max_happiness(graph)
    print("Part 1:", result)
    # part 2
    for person in list(graph.keys()):
        graph['ME'][person] = 0
        graph[person]['ME'] = 0
    result = get_max_happiness(graph)
    print("Part 2:", result)


def parse(line):
    line = line.strip('\n.').split()
    person, sign, value, other = line[0], line[2], int(line[3]), line[-1]
    if sign == "lose":
        value = -value
    return person, other, value


def load_data(fileobj):
    data = [parse(line) for line in fileobj]
    graph = defaultdict(dict)
    for person, other, value in data:
        graph[person][other] = value
    return graph


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
