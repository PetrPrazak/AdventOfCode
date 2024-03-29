# $link$year/day/$day
from pprint import pprint
from pathlib import Path
from functools import reduce, cache
from operator import mul
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, islice
from string import whitespace, digits
from copy import copy, deepcopy
from math import prod
import time
import re


def process(data):
    pprint(data)
    # part 1
    result = 0
    print("part 1:", result)
    # part 2
    result = 0
    print("part 2:", result)


def parse_line(line):
    return line


def parse_section(section):
    header, *section = section
    return header.rstrip(), section.split("\n")


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]
    # alternatively
    # return dict(parse_section(part) for part in fileobj.read().split("\n\n"))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    main("test.txt")
    # main()
