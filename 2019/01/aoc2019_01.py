# https://adventofcode.com/2019/day/01

from __future__ import print_function

INPUT = "aoc2019_01_input.txt"


def calc_fuel(mass):
    fuel = mass // 3 - 2
    return fuel


def calc_fuel2(mass):
    total = 0
    while True:
        req_fuel = calc_fuel(mass)
        if req_fuel <= 0:
            break
        total += req_fuel
        mass = req_fuel
    return total


def test():
    print(list(map(calc_fuel, [1969, 100756])))
    print(list(map(calc_fuel2, [1969, 100756])))


def process(data):
    # part 1
    p1 = sum(list(map(calc_fuel, data)))
    print(p1)

    # part 2
    p2 = sum(list(map(calc_fuel2, data)))
    print(p2)


def main():
    with open(INPUT) as f:
        data = [int(l.strip()) for l in f.readlines()]
        process(data)


if __name__ == "__main__":
    main()
    test()
