# https://adventofcode.com/2021/day/5
from __future__ import print_function
from pathlib import Path
from collections import defaultdict


def gradient(a, b):
    return 1 if a < b else -1 if a > b else 0


def line_points(start, end, diagonals):
    x1, x2 = start[0], end[0]
    y1, y2 = start[1], end[1]
    inc_x, inc_y = gradient(x1, x2), gradient(y1, y2)
    if not diagonals and inc_x != 0 and inc_y != 0:
        return
    while True:
        yield x1, y1
        if x1 == x2 and y1 == y2:
            break
        x1 += inc_x
        y1 += inc_y


def process_lines(data, diagonals=False):
    grid = defaultdict(int)
    for start, end in data:
        for x, y in line_points(start, end, diagonals):
            grid[(x, y)] += 1
    return sum(n > 1 for n in grid.values())


def process(data):
    # part 1
    result = process_lines(data)
    print("part 1:", result)
    # part 2
    result = process_lines(data, diagonals=True)
    print("part 2:", result)


def parse_line(line):
    start, end = line.strip().split(' -> ')
    start = tuple(int(n) for n in start.split(','))
    end = tuple(int(n) for n in end.split(','))
    return start, end


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
