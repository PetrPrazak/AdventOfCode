# http://adventofcode.com/2016/day/3
from __future__ import print_function


def is_triangle(triangle):
    a, b, c = sorted(triangle)
    return a + b > c


def solve(lines):
    acc = sum(1 for line in lines if is_triangle(line))
    print("Part 1:", acc)


def solve2(lines):
    acc = sum(1 for i in range(0, len(lines), 3)
              for t in zip(lines[i], lines[i+1], lines[i+2])
              if is_triangle(t))
    print("Part 2:", acc)


def parse(line):
    return tuple(int(x) for x in line.split())


def main(file):
    with open(file) as f:
        lines = [parse(line.strip()) for line in f.readlines()]
        solve(lines)
        solve2(lines)


if __name__ == "__main__":
    main("day3_input.txt")
