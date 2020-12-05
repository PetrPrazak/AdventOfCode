# http://adventofcode.com/2015/day/12
from __future__ import print_function
from collections import defaultdict
import re
import json


num_re = re.compile(r'(-?\d+)')


def sum_numbers(data):
    match = num_re.search(data)
    acc = 0
    while match:
        num = int(match.group(1))
        acc += num
        match = num_re.search(data, match.span(1)[1]+1)
    return acc


def object_hook(d):
    for _, v in d.items():
        if v == "red":
            return dict()
    return d


def part2(data):
    o = json.loads(data, object_hook=object_hook)
    data = json.dumps(o)
    return sum_numbers(data)


def process(data):
    # part 1
    print("Part 1:", sum_numbers(data))
    # part 2
    print("Part 2:", part2(data))


def test():
    process("{\"a\":2,\"b\":4}")  # 6
    process("[-1,{\"a\":1}]")    # 0
    process("[1,{\"c\":\"red\",\"b\":2},3]")  # 3


def load_data(fileobj):
    data = fileobj.read()
    return data


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # test()
    main("input.txt")
