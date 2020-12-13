# https://adventofcode.com/2020/day/13
from __future__ import print_function
from math import prod


def find_bus(timestamp, buses):
    mind_wait = min(buses)[0]
    for t in range(mind_wait):
        for b, _ in buses:
            if (timestamp + t) % b == 0:
                return t * b
    return None


# from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def chinese_remainder(buses):
    prd = prod(b for b, _ in buses)
    suma = 0
    for b, id in buses:
        rem = (b - id) % b
        p = prd // b
        suma += rem * mul_inv(p, b) * p
    return suma % prd


def process(data):
    # part 1
    result = find_bus(*data)
    print("part 1:", result)
    # part 2
    result = chinese_remainder(data[1])
    print("part 2:", result)


def load_data(fileobj):
    lines = fileobj.readlines()
    timestamp = int(lines[0])
    buses = [(int(wait), i)
             for i, wait in enumerate(lines[1].rstrip().split(','))
             if wait != 'x']
    return timestamp, buses


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
