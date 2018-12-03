# https://adventofcode.com/2018/day/3

from __future__ import print_function
from collections import defaultdict
import re


INPUT = "aoc2018_day03.txt"
# INPUT = "test.txt"

def get_area(left,top,width,height):
    s = set()
    for x in range(left, left+width):
        for y in range(top, top+height):
            s.add((x,y))
    return s


regex = re.compile(r"#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)")

with open(INPUT) as f:
    data = [x.strip() for x in f.readlines()]

    wholearea = defaultdict(set)
    ids = set()
    for line in data:
        r = regex.match(line)
        (id, left, top, width, height) = (int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4)), int(r.group(5)))
        ids.add(id)
        area = get_area(left, top, width, height)
        for x in area:
            wholearea[x].add(id)

    total = 0
    for x in wholearea:
        claims = wholearea[x]
        if len(claims) > 1:
            total += 1
            ids -= claims

    print(total)
    print(ids)
