# https://adventofcode.com/2021/day/1
from __future__ import print_function
from pathlib import Path

def process(data):
    # part 1
    result = 0
    for d1, d2 in zip(data, data[1:]):
        if d2 > d1:
            result += 1
    print("part 1:", result)
    # part 2
    result = 0
    last_sum = None
    for d in zip(data, data[1:], data[2:]):
        sum_d = sum(d)
        if last_sum and sum_d > last_sum:
            result += 1
        last_sum = sum_d
    print("part 2:", result)


def load_data(fileobj):
    return [int(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
