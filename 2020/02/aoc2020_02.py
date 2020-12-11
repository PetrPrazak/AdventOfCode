# https://adventofcode.com/2020/day/2
from __future__ import print_function
from functools import reduce


def part1reductor(accum, line):
    limits, char, pwd = line
    valid = pwd.count(char) in range(limits[0], limits[1] + 1)
    return accum + int(valid)


def part2reductor(accum, line):
    positions, char, pwd = line
    valid = sum(int(pwd[r - 1] == char) for r in positions) == 1
    return accum + int(valid)


def part1(data):
    acc = reduce(part1reductor, data, 0)
    print("part 1:", acc)


def part2(data):
    acc = reduce(part2reductor, data, 0)
    print("part 2:", acc)


def parse(line):
    bounds, char, pwd = line.split(' ')
    bounds = [int(n) for n in bounds.split('-')]
    char = char[0]
    return (bounds, char, pwd)


def main(file):
    print(file)
    with open(file) as f:
        data = [parse(l.strip()) for l in f.readlines()]
        part1(data)
        part2(data)


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
