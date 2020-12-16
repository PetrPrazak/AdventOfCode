# http://adventofcode.com/2017/day/24
from __future__ import print_function
from collections import defaultdict
from time import time


def nextlink(ports, port, path, paths):
    atend = True
    for p, i in ports[port]:
        if i not in path:
            l = path[:]
            l.append(i)
            nextlink(ports, p, l, paths)
            atend = False
    if atend:
        paths.append(path[:])


def solve(lines):
    ports = defaultdict(set)
    pieces = defaultdict(int)
    for i, line in enumerate(lines):
        p_from, p_to = list(map(int, line.strip().split('/')))
        ports[p_from].add((p_to, i))
        ports[p_to].add((p_from, i))
        pieces[i] = p_from + p_to

    paths = []
    nextlink(ports, 0, [], paths)

    bridges = defaultdict(list)
    maxx = 0
    for p in paths:
        suma = sum(pieces[x] for x in p)
        maxx = max(maxx, suma)
        bridges[len(p)].append(suma)
    print("Part 1:", maxx)

    s = max(bridges[max(bridges.keys())])
    print("Part 2:", s)


def main():
    start = time()
    with open("input.txt") as f:
        # read by lines
        lines = f.readlines()
        solve(lines)
    end = time()
    print("Solved in {:.3f} s".format(end - start))


if __name__ == "__main__":
    main()
