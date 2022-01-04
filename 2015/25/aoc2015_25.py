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


def process(data):
    col, row = 1, 1
    diag_row = 1
    for i in count(1):
        if row == data[0] and col == data[1]:
            break
        row -= 1
        col += 1
        if row == 0:
            diag_row += 1
            row = diag_row
            col = 1

    for _, code in zip(range(i), gen_code()):
        pass

    # part 1
    result = code
    print("part 1:", result)


def load_data(fileobj):
    return tuple(map(int, re.findall(r'\d+', fileobj.read())))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main()
