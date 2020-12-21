# https://adventofcode.com/2020/day/21
from __future__ import print_function
from collections import Counter, defaultdict
from pprint import pprint


def find_allergens(data):
    allergen_list = defaultdict(list)
    for ingredients, allergens in data:
        for al in allergens:
            allergen_list[al].append(set(ingredients))

    allergens_map = {allegen: set.intersection(*sets)
                     for allegen, sets in allergen_list.items()}

    ingredients_allergens = dict()
    known_allergens = set()
    while allergens_map:
        unknowns = dict()
        for allegen, sets in allergens_map.items():
            ingr = sets - known_allergens
            assert ingr
            if len(ingr) == 1:
                known_allergens.update(ingr)
                ingredients_allergens[ingr.pop()] = allegen
            else:
                unknowns[allegen] = ingr
        allergens_map = unknowns
    return ingredients_allergens


def process(data):
    # part 1
    allergens = find_allergens(data)
    bad_ingredients = set(allergens.keys())
    c = Counter()
    for ingredients, _ in data:
        c.update(set(ingredients) - bad_ingredients)
    result = sum(c.values())
    print("part 1:", result)
    # part 2
    ingredients = sorted(allergens.keys(), key=lambda k: allergens[k])
    result = ','.join(ingredients)
    print("part 2:", result)


def parse_line(line):
    ingredients, allergens = line.strip(')').split(" (contains ")
    return ingredients.split(' '), allergens.split(", ")


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
