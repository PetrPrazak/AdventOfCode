# https://adventofcode.com/2021/day/10
from __future__ import print_function
from pprint import pprint
from pathlib import Path

matching = {'(': ')', '[': ']', '{': '}', '<': '>'}
valuation = {')': 3, ']': 57, '}': 1197, '>': 25137}


def parse_line(line):
    parens = list()
    for c in line:
        if c in '([{<':
            parens.append(c)
        elif c in ')]}>':
            if c != matching[parens[-1]]:
                return valuation[c], list()
            else:
                del parens[-1]
    return 0, parens


def evaluate(param):
    _, parens = param
    valuation = {')': 1, ']': 2, '}': 3, '>': 4}
    total = 0
    for p in reversed(parens):
        total *= 5
        total += valuation[matching[p]]
    return total


def process(data):
    # part 1
    result = sum(map(lambda t: t[0], map(parse_line, data)))
    print("part 1:", result)
    # part 2
    scores = sorted(list(filter(lambda l: l > 0, map(evaluate, map(parse_line, data)))))
    result = scores[len(scores)//2]
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
