# https://adventofcode.com/2018/day/6

from __future__ import print_function
from collections import Counter
import re


INPUT = "aoc2018_day06.txt"
max_dist = 10000
# INPUT = "test.txt"
# max_dist = 32

coord_regex = re.compile("(\d+),\s(\d+)")


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


with open(INPUT) as f:
    data = [x.strip() for x in f.readlines()]
    coords = list()
    min_x = min_y = 10000
    max_x = max_y = 0
    for line in data:
        r = coord_regex.match(line)
        c_x, c_y = int(r.group(1)), int(r.group(2))
        min_x = min(min_x, c_x)
        max_x = max(max_x, c_x)
        min_y = min(min_y, c_y)
        max_y = max(max_y, c_y)
        coords.append((c_x, c_y))

    # part 1
    area = dict()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dists = sorted([(c, manhattan_distance(c, (x,y))) for c in coords], key=lambda t: t[1])
            f, s = dists[0], dists[1]
            area[(x,y)] = f[0] if f[1] < s[1] else '.'

    count = Counter(area.values())
    for c in coords:
        x,y = c
        if x == min_x or x == max_x or y == min_y or y == max_y:
            del count[c]
    print(count.most_common(1)[0][1])

    # part 2
    area = dict()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            total_dist = sum([manhattan_distance(c, (x,y)) for c in coords])
            area[(x,y)] = '#' if total_dist < max_dist else '.'
    print(Counter(area.values())['#'])
