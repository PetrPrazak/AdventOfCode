# https://adventofcode.com/2021/day/14
from __future__ import print_function
from pathlib import Path
from functools import cache


def merge_counter(list1, list2):
    return list(map(sum, zip(list1, list2)))


def count_molecules(polymer, rules, iterations):
    def new_counter():
        return [0] * len(molecules)

    def inc_counter(counter, molecule):
        counter[molecules.index(molecule)] += 1

    @cache
    def expand_pair(pair, iterations):
        if not iterations:
            counter = new_counter()
            inc_counter(counter, pair[0])
            return tuple(counter)
        cntr = new_counter()
        added = rules[pair]
        cntr = merge_counter(cntr, expand_pair(pair[0] + added, iterations - 1))
        cntr = merge_counter(cntr, expand_pair(added + pair[1], iterations - 1))
        return tuple(cntr)

    molecules = list(set(rules.values()))
    counter = new_counter()
    for idx in range(len(polymer)-1):
        pair = polymer[idx:idx+2]
        counter = merge_counter(counter, expand_pair(pair, iterations))
    inc_counter(counter, polymer[-1])
    return counter


def get_diff(counter):
    sums = sorted(counter, reverse=True)
    return sums[0] - sums[-1]


def process(data):
    # part 1
    polymer, rules = data
    counter = count_molecules(*data, 10)
    result = get_diff(counter)
    print("part 1:", result)
    # part 2
    counter = count_molecules(*data, 40)
    result = get_diff(counter)
    print("part 2:", result)


def parse_recipes(recipes):
    ret = dict()
    for line in recipes.split('\n'):
        s, e = line.split(' -> ')
        ret[s] = e
    return ret


def load_data(fileobj):
    seed, recipes = fileobj.read().split("\n\n")
    return seed, parse_recipes(recipes.strip())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
