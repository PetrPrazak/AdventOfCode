# https://adventofcode.com/2025/day/8
from pathlib import Path
from itertools import combinations
from math import prod, dist
import time


def part1_and_2(data: list[tuple], max_pairs: int):
    part1_ret, part2_ret = None, None

    pairs = sorted(combinations(data, 2), key=lambda x: dist(*x))
    circuits = {frozenset({p}) for p in data}

    def find_circuit(point):
        return next(c for c in circuits if point in c)

    for di, (p1, p2) in enumerate(pairs):
        c1, c2 = find_circuit(p1), find_circuit(p2)
        circuits = circuits - {c1, c2} | {c1|c2}

        if di + 1 == max_pairs:
            cl_len = sorted((len(c) for c in circuits), reverse=True)[:3]
            part1_ret = prod(cl_len)

        if len(circuits) == 1:
            part2_ret = p1[0] * p2[0]
            break

    return part1_ret, part2_ret


def process(data, max_pairs):
    # part 1 and part 2
    result = part1_and_2(data, max_pairs)
    print("part 1:", result[0])
    print("part 2:", result[1])


def parse_line(line):
    return tuple(map(int, line.split(',')))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt", max_pairs=1000):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f), max_pairs)
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt", max_pairs=10)
    main()
