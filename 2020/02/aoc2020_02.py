# https://adventofcode.com/2020/day/02
from __future__ import print_function
from collections import Counter

def part1(data):
    acc = 0
    for line in data:
        range, char, pwd = line
        ctr = Counter(pwd)
        if  range[0] <= ctr[char] <= range[1]:
            acc += 1
    print("part 1:", acc)


def part2(data):
    acc = 0
    for line in data:
        range, char, pwd = line
        pos = sum([int(pwd[r - 1] == char) for r in range])
        if pos == 1:
            acc += 1
    print("part 2:", acc)


def parse(line):
    range, char, pwd = line.split(' ')
    range = [int(n) for n in range.split('-')]
    char = char[0]
    return (range, char, pwd)


def main(file):
    print(file)
    with open(file) as f:
        data = [parse(l.strip()) for l in f.readlines()]
        part1(data)
        part2(data)


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
