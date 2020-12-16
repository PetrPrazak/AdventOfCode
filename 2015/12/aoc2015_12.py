# http://adventofcode.com/2015/day/12
from __future__ import print_function
from collections import defaultdict
import re
import json


def sum_numbers(data):
    numbers = re.findall((r'(-?\d+)'), data)
    return sum(int(val) for val in numbers)


def object_hook(d):
    return d if "red" not in d.values() else dict()


def part2(data):
    obj = json.loads(data, object_hook=object_hook)
    return sum_numbers(json.dumps(obj))


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
