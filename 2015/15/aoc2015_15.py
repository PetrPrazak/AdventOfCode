# http://adventofcode.com/2015/day/15
from __future__ import print_function
from collections import defaultdict
from math import prod


def proportions_gen(ratiolist, count, total, remaining):
    if count == 1:
        yield ratiolist + [remaining]
    else:
        for value in range(1, remaining):
            yield from proportions_gen(ratiolist + [value], count - 1, total, remaining - value)


def proportions(num):
    return iter(proportions_gen([], num, 100, 100))


def property_value(data, prop, ratios):
    weights = [weights[prop] for weights in data.values()]
    prop_sum = sum(n*m for n, m in zip(weights, ratios))
    return prop_sum if prop_sum > 0 else 0


def calc_score(data, ratios):
    properties = ['capacity', 'durability', 'flavor', 'texture']
    return prod(property_value(data, prop, ratios) for prop in properties)


def check_calories(data, ratios):
    calories = property_value(data, 'calories', ratios)
    return calories == 500


def process(data):
    # part 1
    num_ingredients = len(data.keys())
    result = max((calc_score(data, ratios), ratios)
                 for ratios in proportions(num_ingredients))
    print("Part 1:", result[0])
    # part 2
    result = max((calc_score(data, ratios), ratios)
                 if check_calories(data, ratios) else (0, ratios)
                 for ratios in proportions(num_ingredients))
    print("Part 2:", result[0])


def parse(line):
    name, rest = line.strip().split(': ')
    props = rest.strip().split(', ')
    line = [tuple(prop.split(' ')) for prop in props]
    return name, line


def load_data(fileobj):
    data = [parse(line) for line in fileobj]
    graph = defaultdict(dict)
    for ingredient, props in data:
        for prop, value in props:
            graph[ingredient][prop] = int(value)
    return graph


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
