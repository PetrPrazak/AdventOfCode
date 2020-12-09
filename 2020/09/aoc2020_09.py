# https://adventofcode.com/2020/day/9
from __future__ import print_function
from itertools import combinations


def find_non_valid(data, preamble):
    for i in range(preamble, len(data)):
        comb = {a+b for a, b in combinations(data[i-preamble:i], 2)}
        if data[i] not in comb:
            return data[i]
    return None


def find_weakness(data, number):
    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            total = sum(data[i:j+1])
            if total == number:
                nset = set(data[i:j+1])
                return min(nset) + max(nset)
            if total > number:
                break
    return None


def process(data, preamble):
    # part 1
    result = find_non_valid(data, preamble)
    print("part 1:", result)
    # part 2
    result = find_weakness(data, result)
    print("part 2:", result)


def load_data(fileobj):
    return [int(line.rstrip()) for line in fileobj]


def main(file, preamble):
    print(file)
    with open(file) as f:
        process(load_data(f), preamble)


if __name__ == "__main__":
    main("test.txt", 5)
    main("input.txt", 25)
