"""
http://adventofcode.com/2015/day/1
"""
from __future__ import print_function
from collections import Counter

with open("input.txt") as f:
    data = f.read()

    # part 1
    c = Counter(list(data))
    print(c['('] - c[')'])

    # part 2
    floor = 0
    pos = 0
    for p in list(data):
        pos += 1
        if p == '(':
            floor += 1
        elif p == ')':
            floor -= 1
        if floor == -1:
            break
    print(pos)
