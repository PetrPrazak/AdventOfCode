# replace XX with day

"""

http://adventofcode.com/2017/day/12


"""
from __future__ import print_function
from collections import defaultdict, Counter


def get_connections(mapping, visits, part):
    q = [part]
    visits.add(part)
    while q:
        a = q.pop()
        l = mapping[a]
        for cons in l:
            if cons not in visits:
                visits.add(cons)
                q.append(cons)
    return len(visits)


def solve(lines):
    total = 1
    mapping = defaultdict(set)
    for line in lines:
        parts = line.strip().split()
        node = int(parts[0])
        siblings = [int(x.strip(',')) for x in parts[2:]]
        for s in siblings:
            mapping[node].add(s)

    total = get_connections(mapping, set(), 0)
    print(total)

    nodes = set(mapping.keys())
    groups = set()
    while len(nodes) > 0:
        visits = set()
        get_connections(mapping, visits, nodes.pop())
        nodes -= visits
        groups.add(tuple(visits))
    print(len(groups))


INPUT = "aoc_day12_input.txt"
# INPUT = "aoc_day12_test.txt"


if __name__ == "__main__":
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)
