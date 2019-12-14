# https://adventofcode.com/2019/day/14
from __future__ import print_function
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *

INPUT = "aoc2019_14_input.txt"
TEST = "test.txt"


def parse_data(data):
    reactions = dict()
    for line in data:
        left, right = line.split(" => ")
        quantity, material = right.split()
        out = dict()
        for single in left.split(', '):
            x, y = single.split()
            out[y] = int(x)
        reactions[material] = (int(quantity), out)
    return reactions


def factory(store, reactions, material, quantity):
    made, leftover = store.setdefault(material, (0, 0))
    if material == "ORE":
        if leftover < quantity:
            raise StopIteration
        store[material] = made + quantity, leftover - quantity
        return
    tobemade = quantity - leftover
    quantum, components = reactions[material]
    multiple = (tobemade + quantum - 1) // quantum  # round to higher quantum
    store[material] = made + tobemade, multiple * quantum - tobemade
    for component, weight in components.items():
        factory(store, reactions, component, multiple * weight)


@timeit
def process(data):
    # part 1
    reactions = parse_data(data)
    store = dict()
    cargo_ore = 1000000000000
    store["ORE"] = (0, cargo_ore)
    factory(store, reactions, "FUEL", 1)
    ore_per_fuel = store["ORE"][0]
    print(ore_per_fuel)  # 1037742

    # part 2
    # find iteratively how much fuel can we produce
    # so the ore leftover is less then ore amount required for single fuel unit
    increment = 1
    coef = 1
    startfuel = cargo_ore / ore_per_fuel
    fuelcount = None
    while True:
        store = dict()
        store["ORE"] = (0, cargo_ore)
        coef += increment
        fuelcount = int(startfuel * coef)
        try:
            factory(store, reactions, "FUEL", fuelcount)
            ore_left = store["ORE"][1]
            if ore_left < ore_per_fuel:
                break
        except StopIteration:
            coef -= increment
            increment /= 10

    print(fuelcount)  # 1572358


def test():
    data = read_input_lines(TEST)
    process(data)


def main():
    data = read_input_lines(INPUT)
    process(data)


if __name__ == "__main__":
    # test()
    main()
