# https://adventofcode.com/2022/day/3
from __future__ import print_function
from pathlib import Path


def get_priority(letter):
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1
    if 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') + 27
    raise ValueError


def sum_priority(aset):
    return sum(get_priority(c) for c in aset)


def process(data):
    # part 1
    result = 0
    for line in data:
        length = len(line)//2
        left, right = line[:length], line[length:]
        common = set(left).intersection(set(right))
        result += sum_priority(common)
    print("part 1:", result)
    # part 2
    result = 0
    for i in range(0, len(data), 3):
        e1, e2, e3 = set(data[i]), set(data[i+1]), set(data[i+2])
        common = e1.intersection(e2).intersection(e3)
        result += sum_priority(common)
    print("part 2:", result)


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
