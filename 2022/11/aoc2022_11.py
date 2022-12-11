# https://adventofcode.com/2022/day/11
from pathlib import Path
from operator import mul, add
from collections import defaultdict
from copy import deepcopy
from math import prod


def monkey_round(data, max_test, inspect, part2):
    div = 1 if part2 else 3
    for monkey in range(len(data)):
        items, (op, arg), test, if_true, if_false = data[monkey]
        inspect[monkey] += len(items)
        for item in items:
            new_level = op(item, arg if arg is not None else item) // div
            new_level %= max_test
            next_monkey = if_true if new_level % test == 0 else if_false
            data[next_monkey][0].append(new_level)
        data[monkey][0] = []


def monkey_inspect(data, rounds=20, part2=False):
    data = deepcopy(data)
    inspect = defaultdict(int)
    max_test = prod(test for _, _, test, _, _ in data.values())
    for _ in range(rounds):
        monkey_round(data, max_test, inspect, part2)
    return inspect


def monkey_business(inspect):
    counts = sorted(inspect.values(), reverse=True)
    return counts[0] * counts[1]


def process(data):
    # part 1
    inspect = monkey_inspect(data)
    result = monkey_business(inspect)
    print("part 1:", result)
    # part 2
    inspect = monkey_inspect(data, rounds=10000, part2=True)
    result = monkey_business(inspect)
    print("part 2:", result)


def parse_section(section):
    header, *section = section.split('\n')
    items = list(map(int, section[0].split(': ')[1].split(', ')))
    op, arg = section[1].split("new = old ")[1].split()
    operation = add if op == '+' else mul, int(arg) if arg[0].isdigit() else None
    test = int(section[2].split("divisible by ")[1])
    if_true = int(section[3].split("monkey ")[1])
    if_false = int(section[4].split("monkey ")[1])
    return int(header.strip(':').split()[1]), [items, operation, test, if_true, if_false]


def load_data(fileobj):
    return dict(parse_section(part) for part in fileobj.read().split("\n\n"))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
