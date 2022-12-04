# https://adventofcode.com/2022/day/4
from __future__ import print_function
from pathlib import Path
import re


def is_contained(l1, r1, l2, r2):
    dif1, dif2 = r1 - l1, r2 - l2
    if dif1 < dif2:
        return l1 >= l2 and r1 <= r2
    else:
        return l2 >= l1 and r2 <= r1


def is_overlapping(l1, r1, l2, r2):
    if l1 < l2:
        return r1 > r2 or l2 <= r1 <= r2
    else:
        return r2 > r1 or l1 <= r2 <= r1


def process(data):
    # part 1
    result = sum(is_contained(*line) for line in data)
    print("part 1:", result)
    # part 2
    result = sum(is_overlapping(*line) for line in data)
    print("part 2:", result)


def parse_line(line):
    return list(map(int, re.findall('\d+', line)))


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
