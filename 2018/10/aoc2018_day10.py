# https://adventofcode.com/2018/day/10

from __future__ import print_function
import re

INPUT = "aoc2018_day10.txt"
# INPUT = "test.txt"

coord_regex = re.compile(r"<\s*(-?\d+),\s*(-?\d+)>")


def print_grid(points, lefttop, rightbottom):
    for y in range(lefttop[1], rightbottom[1] + 1):
        line = ""
        for x in range(lefttop[0], rightbottom[0] + 1):
            line += "*" if (x, y) in points else ' '
        print(line)


def map_tuple(func, t1, t2):
    return func(t1[0], t2[0]), func(t1[1], t2[1])


def sum_tuple(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


def solve(data):

    points = []
    velo = []
    for line in data:
        p, s = coord_regex.findall(line)
        point = int(p[0]), int(p[1])
        points.append(point)
        speed = int(s[0]), int(s[1])
        velo.append(speed)

    # part 1
    for iterace in range(1, 20000):
        lt = (100000, 100000)
        rb = (0, 0)
        for i, p in enumerate(points):
            new_pos = sum_tuple(p, velo[i])
            points[i] = new_pos
            lt = map_tuple(min, lt, new_pos)
            rb = map_tuple(max, rb, new_pos)

        grid_height = rb[1] - lt[1]
        if grid_height < 10:
            print_grid(points, lt, rb)
            break

    # part 2
    print(iterace)


"""
*    *  *****   *****   *    *  *****   *****   *    *   ****
*    *  *    *  *    *  *    *  *    *  *    *  *   *   *    *
*    *  *    *  *    *  *    *  *    *  *    *  *  *    *
*    *  *    *  *    *  *    *  *    *  *    *  * *     *
******  *****   *****   ******  *****   *****   **      *
*    *  *  *    *       *    *  *    *  *  *    **      *  ***
*    *  *   *   *       *    *  *    *  *   *   * *     *    *
*    *  *   *   *       *    *  *    *  *   *   *  *    *    *
*    *  *    *  *       *    *  *    *  *    *  *   *   *   **
*    *  *    *  *       *    *  *****   *    *  *    *   *** *

10355
"""


def main():
    with open(INPUT) as f:
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
