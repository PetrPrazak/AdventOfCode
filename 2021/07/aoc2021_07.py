# https://adventofcode.com/2021/day/7
from __future__ import print_function
from pathlib import Path
from functools import cache


@cache
def sum_up_to(n):
    return sum(range(1, n+1))


def find_best_position(crabs, valuate_distance):
    min_fuel = None
    for r in range(min(crabs), max(crabs) + 1):
        fuel = sum(valuate_distance(c - r) for c in crabs)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
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
