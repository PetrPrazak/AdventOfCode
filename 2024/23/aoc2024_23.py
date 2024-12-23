# https://adventofcode.com/2024/day/23
from pathlib import Path
from collections import defaultdict
from itertools import combinations
from copy import copy
import time


def part1(conns):
    groups = set()
    for n, nn in conns.items():
        for a, b in combinations(nn, 2):
            if b in conns[a]:
                s = set([a, b, n])
                if any(item[0] == 't' for item in s):
                    groups.add(frozenset(s))
    return len(groups)


def part2(conns):
    cnt = defaultdict(int)
    for n, nn in conns.items():
        g = copy(nn)
        g.add(n)
        s = set()
        for c in nn:
            s.update(conns[c])
        g.intersection_update(s)
        cnt[frozenset(g)] += 1
    s = max((x, s) for s, x in cnt.items())[1]
    return ','.join(sorted(s))


def process(data):
    conns = defaultdict(set)
    for a, b in data:
        conns[a].add(b)
        conns[b].add(a)
    # part 1
    result = part1(conns)
    print("part 1:", result)
    # part 2
    result = part2(conns)
    print("part 2:", result)


def parse_line(line):
    return tuple(line.split('-'))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


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
