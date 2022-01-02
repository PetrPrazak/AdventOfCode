# https://adventofcode.com/2021/day/22
from __future__ import print_function
from pathlib import Path
from collections import defaultdict
from more_itertools import sliced
import re


def part1(data):
    """ keeps all bits in the set of coords """
    grid = set()
    for on, coords in data:
        x1, x2, y1, y2, z1, z2 = coords
        assert x1 < x2 and y1 < y2 and z1 < z2
        if not all(x in range(-50, 51) for x in coords):
            continue
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    if on:
                        grid.add((x, y, z))
                    else:
                        grid.discard((x, y, z))
    return len(grid)


def cube_volume(cube):
    """ computes volume of a cuboid defined by coordinates """
    if not cube:
        return 0
    (x1, x2, y1, y2, z1, z2) = cube
    return (x2+1-x1) * (y2+1-y1) * (z2+1-z1)


def overlap(interval1, interval2):
    """ returns the coords of an overlapped area """
    a1, a2 = interval1
    b1, b2 = interval2
    if a1 <= b2 and a2 >= b1:
        return max(a1, b1), min(a2, b2)


def cube_intersect(coord1, coord2):
    """" returns the intersecting cube of two cubes """
    int_cube = list()
    for c1, c2 in zip(sliced(coord1, 2), sliced(coord2, 2)):
        if common := overlap(c1, c2):
            int_cube.extend(common)
        else:
            return None
    return tuple(int_cube)


def part2(data):
    areas = defaultdict(int)
    for on, cuboid in data:
        updated_areas = defaultdict(int)
        if on:
            updated_areas[cuboid] += 1
        for area, val in areas.items():
            if intersect := cube_intersect(area, cuboid):
                updated_areas[intersect] -= val
        for area, val in updated_areas.items():
            areas[area] += val
    return sum(cube_volume(c) * val for c, val in areas.items())


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def parse_line(line):
    bit, coords = line.strip().split()
    nums = tuple(map(int, re.findall('-?\d+', coords)))
    return bit == 'on', nums


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test3.txt")
    main()
