# http://adventofcode.com/2015/day/2
from __future__ import print_function

with open("input.txt") as f:
    data = f.readlines()

    totarea = 0
    totribbon = 0
    for paper in data:
        l, w, h = sorted(map(int, paper.split('x')))

        area = 3 * l * w + 2 * (w * h + h * l)
        totarea += area

        ribbon = 2 * (l + w) + l * w * h
        totribbon += ribbon

    print(totarea, totribbon)
