# https://adventofcode.com/2025/day/6
from pathlib import Path
from itertools import zip_longest
from math import prod
import time
import re


def part1(data):
    acc = 0
    for row in list(zip(*data)):
        op, row = row[-1], row[:-1]
        fn = prod if op == '*' else sum
        acc += fn(int(n) for n in row)
    return acc


def part2(data):
    op_line, data = data[-1], data[:-1]
    # indices of separator columns
    cols = [i-1 for i, c in enumerate(op_line) if c != ' ' and i != 0]
    cols.append(max(len(l) for l in data))
    # list of functions to apply
    ops = [prod if c == '*' else sum for c in op_line if c != ' ']
    idx, acc = 0, 0
    for col, op in zip(cols, ops):
        # extract the numbers for particular column
        parts = [line[idx:col] for line in data]
        idx = col + 1
        # rotate, build the number and call operation on the list
        acc += op(int(''.join(c for c in num if c != ' '))
                  for num in zip_longest(*parts, fillvalue=' '))
    return acc


def process(data):
    # part 1
    part1_data, part2_data = data
    result = part1(part1_data)
    print("part 1:", result)
    # part 2
    result = part2(part2_data)
    print("part 2:", result)


def parse_line(line):
    return list(re.findall("([0-9]+|[+*])\b*", line))


def load_data(fileobj):
    lines = fileobj.read().split('\n')
    part1 = map(parse_line, lines)
    return part1, lines


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
