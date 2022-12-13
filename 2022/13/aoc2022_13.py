# https://adventofcode.com/2022/day/13
from pathlib import Path
from functools import cmp_to_key
from math import prod
from ast import literal_eval


def compare_lists(l1, l2):
    for idx in range(max(len(l1), len(l2))):
        if idx == len(l1):
            return -1
        if idx == len(l2):
            return 1
        item1, item2 = l1[idx], l2[idx]
        if type(item1) is int and type(item2) is int:
            if item1 != item2:
                return -1 if item1 < item2 else 1
            continue
        if type(item1) is int:
            item1 = [item1]
        if type(item2) is int:
            item2 = [item2]
        if list_compare := compare_lists(item1, item2):
            return list_compare
    return 0


def process(data):
    # part 1
    result = sum(idx for idx, val in
                 enumerate((compare_lists(*pair) for pair in data), start=1)
                 if val == -1)
    print("part 1:", result)
    # part 2
    packets = [packet for pair in data for packet in pair]
    div_packets = [[[2]], [[6]]]
    packets += div_packets
    packets.sort(key=cmp_to_key(compare_lists))
    result = prod(idx for idx, packet in enumerate(packets, start=1)
                  if packet in div_packets)
    print("part 2:", result)


def parse_section(section):
    return tuple(map(literal_eval, section.split('\n')))


def load_data(fileobj):
    return [parse_section(section) for section in fileobj.read().split("\n\n")]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
