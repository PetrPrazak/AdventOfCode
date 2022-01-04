# https://adventofcode.com/2021/day/19
from __future__ import print_function
from pathlib import Path
from collections import deque
from itertools import combinations, product


transforms = [(lambda x, y, z, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
              for x1, y1, z1 in product((-1, 1), repeat=3)] \
    + [(lambda x, z, y, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
       for x1, y1, z1 in product((-1, 1), repeat=3)] \
    + [(lambda y, x, z, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
       for x1, y1, z1 in product((-1, 1), repeat=3)] \
    + [(lambda y, z, x, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
       for x1, y1, z1 in product((-1, 1), repeat=3)] \
    + [(lambda z, x, y, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
       for x1, y1, z1 in product((-1, 1), repeat=3)] \
    + [(lambda z, y, x, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1))
       for x1, y1, z1 in product((-1, 1), repeat=3)]


def distance(a, b):
    return sum(abs(aa - bb) for aa, bb in zip(a, b))


def point_diff(a, b):
    return tuple(aa - bb for aa, bb in zip(a, b))


def point_add(a, b):
    return tuple(aa + bb for aa, bb in zip(a, b))


def find_transformation(pairs):
    for t in transforms:
        count = 0
        for (a1, b1), (a2, b2) in zip(pairs, pairs[1:]):
            tb1, tb2 = t(*b1), t(*b2)
            if point_diff(a1, a2) != point_diff(tb1, tb2):
                break
            count += 1
        if count >= 11:
            return t


def point_distances(points):
    return {p: set(distance(p, p1) for p1 in points) for p in points}


def find_matched_points(merged, scanner):
    a = point_distances(merged)
    b = point_distances(scanner)
    return [(p1, p2)
            for p1, d1 in a.items()
            for p2, d2 in b.items()
            if len(d1.intersection(d2)) >= 11]


def process(data):
    locations = [(0, 0, 0)]
    merged = data[0]
    queue = deque(data[1:])
    while queue:
        scanner = queue.popleft()
        matched = find_matched_points(merged, scanner)
        if not matched:
            queue.append(scanner)
            continue
        transform = find_transformation(matched)
        p_tr = transform(*matched[0][1])
        others = {m[1] for m in matched}
        rest = filter(lambda p: p not in others, scanner)
        offset = point_diff(matched[0][0], p_tr)
        transformed = {point_add(offset, transform(*point)) for point in rest}
        merged.update(transformed)
        locations.append(offset)
    # part 1
    result = len(merged)
    print("part 1:", result)
    # part 2
    result = max(distance(a, b) for a, b in combinations(locations, 2))
    print("part 2:", result)


def parse_section(section):
    _, *section = section.split('\n')
    return set(tuple(map(int, s.split(','))) for s in section if s)


def load_data(fileobj):
    return [parse_section(part) for part in fileobj.read().split("\n\n")]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
