# https://adventofcode.com/2020/day/01
from __future__ import print_function

INPUT = "input.txt"
TOTAL = 2020


def find_two_complements(data, total):
    complement = [total - x for x in data]
    intersection = list(set(data).intersection(set(complement)))
    if len(intersection) != 2:
        return None
    return tuple(intersection)


def find_three_complements(data, total):
    for idx, num in enumerate(data):
        rest = data.copy()
        del rest[idx]
        rest_two = find_two_complements(rest, total - num)
        if rest_two is not None:
            break
    return num, rest_two[0], rest_two[1]


def test():
    test_data = [1721, 979, 366, 299, 675, 1456]
    n1, n2 = find_two_complements(test_data, TOTAL)
    assert(n1 * n2 == 514579)
    n1, n2, n3 = find_three_complements(test_data, TOTAL)
    assert(n1 * n2 * n3 == 241861950)


def part1(data):
    n1, n2 = find_two_complements(data, TOTAL)
    print(n1, n2, '->', n1 * n2)


def part2(data):
    n1, n2, n3 = find_three_complements(data, TOTAL)
    print(n1, n2, n3, '->', n1 * n2 * n3)


def main():
    with open(INPUT) as f:
        data = [int(l.strip()) for l in f.readlines()]
        part1(data)
        part2(data)


if __name__ == "__main__":
    test()
    main()
