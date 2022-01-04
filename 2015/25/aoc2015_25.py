# https://adventofcode.com/2015/day/25
from __future__ import print_function
from pathlib import Path
from itertools import count
import re


def gen_code():
    code = 20151125
    while True:
        yield code
        code = (code * 252533) % 33554393


def bf_part1(data):
    col, row = 1, 1
    for _, code in zip(count(1), gen_code()):
        if row == data[0] and col == data[1]:
            return code
        if row == 1:
            row = col + 1
            col = 1
        else:
            row -= 1
            col += 1


def fast_part1(data):
    def triangle(row, col):
        return ((row + col) ** 2 - 3 * row - col) // 2
    return pow(252533, triangle(*data), 33554393) * 20151125 % 33554393


def process(data):
    # part 1
    # print("part 1:", bf_part1(data))
    print("part 1:", fast_part1(data))


def load_data(fileobj):
    return tuple(map(int, re.findall(r'\d+', fileobj.read())))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main()
