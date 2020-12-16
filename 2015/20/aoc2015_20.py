# https://adventofcode.com/2015/day/20
from __future__ import print_function
import math


def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n // i)
    for divisor in reversed(large_divisors):
        yield divisor


def house_presents_part1(house):
    return sum(divisorGenerator(house)) * 10


def house_presents_part2(house):
    return sum(filter(lambda x: x * 50 >= house, divisorGenerator(house))) * 11


# stupid brute-force search :(
def search(value, start, end, evaluator):
    for h in range(start, end):
        if evaluator(h) > value:
            return h
    return None


def main():
    my_presents = 29000000
    house = search(my_presents, 600000, 1000000, house_presents_part1)
    print("Part 1:", house)
    house = search(my_presents, 600000, 1000000, house_presents_part2)
    print("Part 1:", house)


if __name__ == "__main__":
    main()
