# https://adventofcode.com/2022/day/1
from __future__ import print_function
from pathlib import Path


def process(data):
    # part 1
    elves = sorted(map(sum, data), reverse=True)
    print("part 1:", elves[0])
    # part 2
    print("part 2:", sum(elves[:3]))


def parse_section(section):
    return [int(line) for line in section.strip().split("\n")]


def load_data(fileobj):
    return [parse_section(part) for part in fileobj.read().split("\n\n")]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
