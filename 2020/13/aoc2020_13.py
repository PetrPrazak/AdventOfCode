# https://adventofcode.com/2020/day/13
from __future__ import print_function
from math import prod, gcd


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


# parameter: list of (module, remainder) tuples
def chinese_remainder(factors):
    """
    The Chinese Remainder Theorem supposes that given the
    integers n_1...n_k that are pairwise co-prime, then for
    any sequence of integers a_1...a_k there exists an integer
    x that solves the system of linear congruences:

    x === a_1 (mod n_1)
    ...
    x === a_k (mod n_k)
    """
    assert gcd(*[n for n, _ in factors]) == 1
    prd = prod(n for n, _ in factors)
    suma = 0
    for n_i, rem_i in factors:
        p = prd // n_i
        suma += rem_i * mul_inv(p, n_i) * p
    return suma % prd


def process(data):
    # part 1
    result = find_bus(*data)
    print("part 1:", result)
    # part 2
    factors = [(b, (b - id) % b) for b, id in data[1]]
    result = chinese_remainder(factors)
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
