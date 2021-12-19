# https://adventofcode.com/2021/day/18
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from itertools import permutations, starmap
from functools import reduce


def sf_add(a, b):
    if not a:
        return b
    if not b:
        return a
    return sf_reduce("[" + a + ',' + b + "]")


def is_number(x):
    return type(x) is int


def printable(sf):
    return ''.join(str(i) if is_number(i) else i for i in sf)


def sf_reduce(sf_str):
    sf = [int(x) if x.isdigit() else x for x in sf_str]
    repeat = True
    while repeat:
        pos, level = 0, 0
        repeat = False
        # find pairs to explode
        while pos < len(sf):
            n = sf[pos]
            if n == '[':
                level += 1
                if level == 5:
                    left, right = sf[pos+1], sf[pos+3]
                    del sf[pos+1:pos+5]
                    sf[pos] = 0
                    num_pos = pos + 1
                    while num_pos < len(sf) and not is_number(sf[num_pos]):
                        num_pos += 1
                    if num_pos < len(sf):
                        sf[num_pos] += right
                    num_pos = pos - 1
                    while num_pos > 0 and not is_number(sf[num_pos]):
                        num_pos -= 1
                    if num_pos > 0:
                        sf[num_pos] += left
                    repeat = True
                    level -= 1
                    continue
            elif n == ']':
                level -= 1
            pos += 1
        if repeat:
            continue
        # no more pairs to explode, check splits
        pos = 0
        while pos < len(sf):
            n = sf[pos]
            if is_number(n) and n > 9:
                sf[pos] = '['
                left = n // 2
                sf[pos+1:pos+1] = [left, ",", n - left, "]"]
                repeat = True
                break
            pos += 1
    return printable(sf)


def make_tree(data):
    def _build_part(stream, level):
        pos, subnode = 0, [None] * 2
        assert level < 5
        for n in stream:
            if n == '[':
                subnode[pos] = _build_part(stream, level + 1)
            elif n == ']':
                return tuple(subnode)
            elif n == ',':
                assert pos == 0
                pos = 1
            else:  # number
                subnode[pos] = int(n)
        return tuple(subnode)

    it = iter(data)
    s = next(it)
    assert s == '[', f"{data} should start with '['"
    return _build_part(it, 0)


def magnitude(tree):
    def calc_magnitude(pair):
        if is_number(tree):
            return tree
        left, right = tree
        return magnitude(left) * 3 + magnitude(right) * 2
    if isinstance(tree, str):
        tree = make_tree(tree)
    return calc_magnitude(tree)


def test():
    assert sf_add("[[[[4,3],4],4],[7,[[8,4],9]]]",
                  "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def process(data):
    # part 1
    result = magnitude(reduce(sf_add, data, []))
    print("part 1:", result)
    # part 2
    result = max(map(magnitude, starmap(sf_add, permutations(data, 2))))
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
