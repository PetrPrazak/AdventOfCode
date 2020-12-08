# https://adventofcode.com/2015/day/19
from __future__ import print_function
import re
from itertools import chain


def get_all_replacements(molecule, pattern, replacement):
    pos = -1
    while True:
        pos = molecule.find(pattern, pos+1)
        if pos == -1:
            return
        yield molecule[:pos] + replacement + molecule[pos+len(pattern):]


def apply_replacements(molecule, replacements):
    out = set(chain.from_iterable(get_all_replacements(molecule, r, to)
                                  for r, to in replacements))
    return out


def replacement(reductions, match):
    return reductions[match.group()]


# not my solution :((
# https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4nsdd?utm_source=share&utm_medium=web2x&context=3

def apply_reductions(molecule, reductions):
    def repl(match): return replacement(reductions, match)
    count = 0
    expr = '|'.join(reductions.keys())
    while molecule != 'e':
        molecule, n = re.subn(expr, repl, molecule, 1)
        assert n == 1
        count += 1
    return count


def process(data):
    molecule, replacements = data
    # part 1
    result = len(apply_replacements(*data))
    print("part 1:", result)
    # part 2
    reductions = {to[::-1]: r[::-1] for r, to in replacements}
    result = apply_reductions(molecule[::-1], reductions)
    print("part 2:", result)


def parse_line(line):
    if ' => ' in line:
        left, right = line.split(' => ')
        return left, right
    return (line, None)


def load_data(fileobj):
    replacements = [parse_line(line.rstrip())
                    for line in fileobj if len(line) > 1]
    molecule = replacements.pop()[0]
    return molecule, replacements


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
