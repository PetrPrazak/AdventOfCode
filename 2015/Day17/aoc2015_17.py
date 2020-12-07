# http://adventofcode.com/2015/day/17
from __future__ import print_function
from itertools import combinations


def filter(comb, capacity):
    return sum(comb) == capacity


def total_combinatios(data, capacity):
    return sum(int(filter(comb, capacity))
                 for cnt in range(2, len(data))
                 for comb in combinations(data, cnt))


def find_lowest_count(data, capacity):
    for cnt in range(2, len(data)):
        found = sum(int(filter(comb, capacity))
                    for comb in combinations(data, cnt))
        if found:
            return found
    return 0


def process(data, capacity):
    # part 1
    result = total_combinatios(data, capacity)
    print("Part 1:", result)
    # part 2
    result = find_lowest_count(data, capacity)
    print("Part 2:", result)


def load_data(fileobj):
    return [int(line.strip()) for line in fileobj]


def main(file, capacity):
    print(file)
    with open(file) as f:
        process(load_data(f), capacity)


if __name__ == "__main__":
    main("test.txt", 25)
    main("input.txt", 150)
