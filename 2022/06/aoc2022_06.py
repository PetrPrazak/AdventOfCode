# https://adventofcode.com/2022/day/6
from pathlib import Path


def find_marker(line, length=4):
    for i in range(length, len(line)):
        if len(set(line[i-length:i])) == length:
            return i


def process(data):
    # part 1
    for l in data:
        print("part 1: ", find_marker(l))
    # part 2
    for l in data:
        print("part 2: ", find_marker(l, 14))


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
