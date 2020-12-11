# https://adventofcode.com/2020/day/3
from __future__ import print_function
from math import prod

def check_slope(data, off_x, off_y):
    result = 0
    pos_x, pos_y = 0, off_y
    height, width = len(data), len(data[0])
    while pos_y < height:
        pos_x = (pos_x + off_x) % width
        result += int(data[pos_y][pos_x] == '#')
        pos_y += off_y
    return result


def part1(data):
    result = check_slope(data, 3, 1)
    print("part 1:", result)


def part2(data):
    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    result = prod(check_slope(data, off_x, off_y) for off_x, off_y in slopes)
    print("part 2:", result)


def main(file):
    print(file)
    with open(file) as f:
        data = [l.strip() for l in f.readlines()]
        part1(data)
        part2(data)


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
