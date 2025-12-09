# https://adventofcode.com/2025/day/9
from pathlib import Path
from itertools import combinations, pairwise
import time


def calculate_area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def ordered(a, b):
    return (a, b) if a < b else (b, a)


def normalize_edge(p1, p2):
    min_x, max_x = ordered(p1[0], p2[0])
    min_y, max_y = ordered(p1[1], p2[1])
    return min_x, min_y, max_x, max_y


def part1_and_2(data):
    areas = sorted(((calculate_area(p1, p2), p1, p2)
                   for p1, p2 in combinations(data, 2)), reverse=True)
    edges = list(normalize_edge(*p) for p in pairwise(data + [data[0]]))

    for area, p1, p2 in areas:
        min_x, max_x = ordered(p1[0], p2[0])
        min_y, max_y = ordered(p1[1], p2[1])

        # check if rectangle is fully contained
        if not any(min_x < e_max_x and max_x > e_min_x and min_y < e_max_y and max_y > e_min_y
               for e_min_x, e_min_y, e_max_x, e_max_y in edges):
            # found one
            break

    return areas[0][0], area


def process(data):
    result = part1_and_2(data)
    print("part 1:", result[0])
    print("part 2:", result[1])


def parse_line(line):
    return tuple(map(int, line.split(',')))


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
    main("test.txt")
    main()
