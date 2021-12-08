# https://adventofcode.com/2021/day/8
from __future__ import print_function
from pathlib import Path
from collections import Counter


def count_unique(right):
    c = Counter(len(w) for w in right)
    return c[2] + c[3] + c[4] + c[7]


D1 = set('cf')       # len 2
D7 = set('acf')      # len 3
D4 = set('bcdf')     # len 4
D2 = set('acdeg')    # len 5
D3 = set('acdfg')    # len 5
D5 = set('abdfg')    # len 5
D6 = set('abdefg')   # len 6
D0 = set('abcefg')   # len 6
D9 = set('abcdfg')   # len 6
D8 = set('abcdefg')  # len 7
DIGITS = [D0, D1, D2, D3, D4, D5, D6, D7, D8, D9]


def find_mapping(left):
    mapping = dict()
    left.sort(key=lambda t: len(t))
    # D7 - D1
    a = set(left[1]) - set(left[0])
    mapping['a'] = a.pop()
    # D2,3,5
    for d in left[3:6]:
        eg = set(d) - set(left[2])  # -D4
        if len(eg) == 2:  # D3 or D5
            eg.remove(mapping['a'])
            mapping['g'] = eg.pop()
            break
    for d in left[3:6]:
        aeg = set(d) - set(left[2])  # -D4
        if len(aeg) == 3:  # D2
            aeg.remove(mapping['a'])
            aeg.remove(mapping['g'])
            mapping['e'] = aeg.pop()
            break
    for d in left[3:6]:
        dg = set(d) - set(left[1])  # -D7
        if len(dg) == 2:  # D3
            dg.remove(mapping['g'])
            mapping['d'] = dg.pop()
            break
    # D6,9,0
    for d in left[6:9]:
        r = set(d) - set(left[1])
        if len(r) == 3:  # D9 or D0
            r.remove(mapping['g'])
            r.discard(mapping['d'])  # segments d or e may not be present
            r.discard(mapping['e'])
            mapping['b'] = r.pop()
    for d in left[3:6]:
        r = set(d) - set(mapping.values())
        if len(r) == 1:
            if mapping['e'] in set(d):    # must be D2
                mapping['c'] = r.pop()
            elif mapping['b'] in set(d):  # D5
                mapping['f'] = r.pop()

    invmapping = {v: k for k, v in mapping.items()}
    return invmapping


def map_digit(mapping, word):
    conv_word = set(mapping[d] for d in word)
    return str(DIGITS.index(conv_word))


def solve_numbers(left, right):
    mapping = find_mapping(left)
    return int(''.join(map_digit(mapping, word) for word in right))


def process(data):
    # part 1
    result = sum(count_unique(l[1]) for l in data)
    print("part 1:", result)
    # part 2
    result = sum(solve_numbers(*l) for l in data)
    print("part 2:", result)


def parse_line(line):
    left, right = line.strip().split(' | ')
    return left.split(), right.split()


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
