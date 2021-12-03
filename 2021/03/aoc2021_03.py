# https://adventofcode.com/2021/day/3
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from collections import Counter
from copy import copy


def transpose(matrix): return zip(*matrix)


def first(iterable): return next(iter(iterable))


def num_from_list_of_bits(alist): return int(''.join(alist), 2)


def count_bits(row, indices):
    cntr = Counter()
    for idx in indices:
        cntr.update(row[idx])
    return cntr


def remove_bit(row, indices, bit):
    for idx in list(indices):
        if row[idx] != bit:
            indices.remove(idx)


def process(data):
    # part 1
    cntrs = [Counter(bitpos) for bitpos in transpose(data)]
    epsilon = num_from_list_of_bits([c.most_common()[0][0] for c in cntrs])
    gamma = num_from_list_of_bits([c.most_common()[1][0] for c in cntrs])
    result = epsilon * gamma
    print("part 1:", result)

    # part 2
    oxygen_indices = set(range(len(data)))
    co2_indices = set(range(len(data)))
    for bitpos in transpose(data):
        if len(oxygen_indices) > 1:
            oxy_cntr = count_bits(bitpos, oxygen_indices)
            oxy_bit = '1' if oxy_cntr['1'] >= oxy_cntr['0'] else '0'
            remove_bit(bitpos, oxygen_indices, oxy_bit)
        if len(co2_indices) > 1:
            co2_cntr = count_bits(bitpos, co2_indices)
            co2_bit = '0' if co2_cntr['0'] <= co2_cntr['1'] else '1'
            remove_bit(bitpos, co2_indices, co2_bit)

    oxygen_rating = num_from_list_of_bits(data[first(oxygen_indices)])
    co2_rating = num_from_list_of_bits(data[first(co2_indices)])
    result = oxygen_rating * co2_rating
    print("part 2:", result)


def parse_line(line):
    return list(line.strip())


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
