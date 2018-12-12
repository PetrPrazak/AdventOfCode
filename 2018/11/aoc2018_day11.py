# https://adventofcode.com/2018/day/11

from __future__ import print_function
from collections import defaultdict
from time import time

INPUT = 9306


def power_level(x, y, serial_number):
    rack = x + 10
    level = rack * y
    level += serial_number
    level *= rack
    return (level // 100 % 10) - 5


#
# assert (power_level(122, 79, 57) == -5)
# assert (power_level(217, 196, 39) == 0)
# assert (power_level(101, 153, 71) == 4)
#

def subgrid(grid, x, y, size):
    suma = sum([grid[(x + xx, y + yy)] for yy in range(0, size) for xx in range(0, size)])
    return suma


def sum_subgrid(grid, size):
    return [(subgrid(grid, x, y, size), x, y) for y in range(1, 302 - size) for x in range(1, 302 - size)]


def solve(serial_number):
    grid = {(x, y): power_level(x, y, serial_number) for y in range(1, 301) for x in range(1, 301)}

    # part 1
    result = sorted(sum_subgrid(grid, 3), reverse=True)
    print(result[0])

    # part 2
    result2 = []
    for size in range(1, 25):
        result = sorted(sum_subgrid(grid, size), reverse=True)
        maximum = result[0], size
        # print(maximum)
        result2.append(maximum)
    print(sorted(result2, reverse=True)[0])


# atempt using Summed-area table (SAT)

def subgridSAT(grid, x, y, size):
    offset = size - 1
    A = grid[(x - 1, y - 1)]
    B = grid[(x - 1, y + offset)]
    C = grid[(x + offset, y - 1)]
    D = grid[(x + offset, y + offset)]
    return D - B - C + A


def sum_subgridSAT(grid, size):
    return [(subgridSAT(grid, x, y, size), x, y) for y in range(1, 302 - size) for x in range(1, 302 - size)]


def solve2(serial_number):
    grid = defaultdict(int)
    for y in range(1, 301):
        for x in range(1, 301):
            grid[(x, y)] = power_level(x, y, serial_number) + grid[(x - 1, y)] + grid[(x, y - 1)] - grid[(x - 1, y - 1)]
    result2 = []
    for size in range(3, 25):
        result = sorted(sum_subgridSAT(grid, size), reverse=True)
        maximum = result[0], size
        if size == 3:
            print(maximum)
        result2.append(maximum)
    print(sorted(result2, reverse=True)[0])


s = time()
solve(INPUT)
p1 = time()
solve2(INPUT)
p2 = time()
print("Naive: %.3f" % (p1 - s))
print("SAT: %.3f" % (p2 - p1))
