# https://adventofcode.com/2021/day/2
from __future__ import print_function
from pathlib import Path


def part1(data):
    hor_pos, depth = 0, 0
    for cmd, val in data:
        if cmd == 'forward':
            hor_pos += val
        elif cmd == 'down':
            depth += val
        elif cmd == 'up':
            depth -= val
        else:
            assert False

    return hor_pos * depth


def part2(data):
    hor_pos, depth, aim = 0, 0, 0
    for cmd, val in data:
        if cmd == 'forward':
            hor_pos += val
            depth += aim * val
        elif cmd == 'down':
            aim += val
        elif cmd == 'up':
            aim -= val
        else:
            assert False

    return hor_pos * depth


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def parse_line(line):
    row = line.split()
    return row[0], int(row[1])


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
