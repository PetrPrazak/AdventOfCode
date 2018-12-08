# https://adventofcode.com/2018/day/8

from __future__ import print_function

INPUT = "aoc2018_day08.txt"
TEST = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

tree = dict()
metasum = 0


def parse(data, index):
    global metasum
    global tree
    my_index = index
    num_children = data[index]
    num_meta = data[index + 1]
    index += 2
    children = list()
    for _ in range(num_children):
        children.append(index)
        index = parse(data, index)
    metadata = data[index: index + num_meta]
    index += num_meta
    tree[my_index] = (children, metadata)
    metasum += sum(metadata)
    return index


def find_value(index):
    (children, metadata) = tree[index]
    if not children:
        return sum(metadata)

    sum_children = 0
    for m in metadata:
        if 1 <= m <= len(children):
            sum_children += find_value(children[m-1])
    return sum_children


def process(data):
    # part 1
    numbers = list(map(int, data))
    parse(numbers, 0)
    print(metasum)
    # part 2
    print(find_value(0))


with open(INPUT) as f:
    data = f.readline().rstrip()
    # process(TEST.split())
    process(data.split())
