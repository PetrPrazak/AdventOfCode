# https://adventofcode.com/2024/day/4
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

DIRS1 = [
    [(1,  0), (2,  0), (3,  0)],     # horizontal right
    [(-1,  0), (-2,  0), (-3,  0)],  # horizontal left
    [(0,  1), (0,  2), (0,  3)],     # vertical down
    [(0, -1), (0, -2), (0, -3)],     # vertical up
    [(1,  1), (2,  2), (3,  3)],     # vertical down right
    [(1, -1), (2, -2), (3, -3)],     # vertical down left
    [(-1,  1), (-2,  2), (-3,  3)],  # vertical up right
    [(-1, -1), (-2, -2), (-3, -3)],  # vertical up left
]

DIRS2 = [
    [[(-1, -1), (1, 1)], [(1, -1), (-1, 1)]],
    [[(1, 1), (-1, -1)], [(-1, 1), (1, -1)]],
    [[(-1, -1), (1, 1)], [(-1, 1), (1, -1)]],
    [[(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]
]


def is_word(grid, rows, cols, word, dir, x, y):
    for i, (dx, dy) in enumerate(dir):
        wx, wy = x + dx, y+dy
        if not (wx in range(cols) and wy in range(rows)):
            break
        if grid[wy][wx] != word[i]:
            break
    else:
        return True
    return False


def check_word1(grid, rows, cols, dirs, word, x, y):
    found = 0
    for dir in dirs:
        found += is_word(grid, rows, cols, word, dir, x, y)
    return found


def check_word2(grid, rows, cols, dirs, word, x, y):
    for all_dirs in dirs:
        for dir in all_dirs:
            if not is_word(grid, rows, cols, word, dir, x, y):
                break
        else:
            return True
    return False


def find_words(grid, word, dirs, part=1):
    total = 0
    rows, cols = len(grid), len(grid[0])
    first, rest = word[0], word[1:]
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == first:
                if part == 1:
                    total += check_word1(grid, rows, cols, dirs, rest, x, y)
                else:
                    total += check_word2(grid, rows, cols, dirs, rest, x, y)
    return total


def process(data):
    # part 1
    result = find_words(data, "XMAS", DIRS1)
    print("part 1:", result)
    # part 2
    result = find_words(data, "AMS", DIRS2, part=2)
    print("part 2:", result)


def parse_line(line):
    return line  # list(line)


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
