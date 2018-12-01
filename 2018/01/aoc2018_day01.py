# https://adventofcode.com/2018/day/1

from __future__ import print_function
from functools import reduce

INPUT = "aoc2018_day01.txt"

with open(INPUT) as f:
    data = [int(x) for x in f.readlines()]
    # part 1
    sum = reduce((lambda x, y: x + y), data)
    print(sum)
    # part 2
    cache = set()
    freq = 0
    i = 0
    while 1:
        if freq in cache:
            print(freq)
            break
        cache.add(freq)
        freq += data[i]
        i += 1
        if i == len(data):
            i = 0

