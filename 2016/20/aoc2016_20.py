# https://adventofcode.com/2016/day/20
from __future__ import print_function
from pathlib import Path

MAX_IP = 2**32


def find_lowest_IP(data):
    lowest = 0
    for ip_min, ip_max in data:
        if ip_min <= lowest + 1:
            lowest = max(lowest, ip_max)
        else:
            return lowest + 1
    return lowest + 1


def total_allowed(data):
    lowest = 0
    total = 0
    for ip_min, ip_max in data:
        if ip_min > lowest + 1:
            total += ip_min - lowest - 1
        lowest = max(lowest, ip_max)
    total += MAX_IP - lowest - 1
    return total


def process(data):
    data = sorted(data)
    # part 1
    result = find_lowest_IP(data)
    print("part 1:", result)
    # part 2
    result = total_allowed(data)
    print("part 2:", result)


def parse_line(line):
    return tuple(map(int, line.split('-')))


def load_data(fileobj):
    return [parse_line(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
