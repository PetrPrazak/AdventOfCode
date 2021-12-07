# https://adventofcode.com/2021/day/7
from __future__ import print_function
from pathlib import Path
from math import inf


def sum_up_to(n):
    return n * (n + 1) // 2


def find_best_position(crabs, valuate_distance):
    min_fuel = inf
    for r in range(min(crabs), max(crabs) + 1):
        fuel = sum(valuate_distance(c - r) for c in crabs)
        min_fuel = min(min_fuel, fuel)
    return min_fuel


def process(crabs):
    # part 1
    result = find_best_position(crabs, lambda d: abs(d))
    print("part 1:", result)
    # part 2
    result = find_best_position(crabs, lambda d: sum_up_to(abs(d)))
    print("part 2:", result)


def load_data(fileobj):
    return list(map(int, fileobj.read().split(',')))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
