# https://adventofcode.com/2022/day/15
from pathlib import Path
import time
import re
from functools import wraps


def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        print(f"Method {method.__name__} finished in {te - ts:.3} s")
        return result

    return timed


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def intersects(sensor, beacon, line):
    radius = manhattan_distance(sensor, beacon)
    sx, sy = sensor
    xd = radius - abs(sy - line)
    if xd < 0:
        return None
    return sx - xd, sx + xd


def covered(data, row):
    return sorted(filter(None, (intersects(s, b, row) for s, b in data)))


def count_convered(data, row):
    beacons = {x for _, (x, y) in data if y == row}
    covers = covered(data, row)
    suma, last_r = 0, covers[0][0] - 1
    for l, r in covers:
        if r < last_r:
            continue
        if l <= last_r:
            l = last_r + 1
        beacon = [x for x in beacons if l <= x <= r]
        suma += r - l + 1 - len(beacon)
        last_r = r
    return suma


def uncovered(intervals, width):
    # x in <0, width>
    last_r = max(0, intervals[0][0] - 1)
    for l, r in intervals:
        if r < last_r:
            continue
        if l < last_r:
            last_r = max(0, r)
            continue
        if l > last_r + 1:
            return last_r + 1, l - 1
        if r > width:
            break
        last_r = r


# naive solution, looking for a hole in the all lines itervals
def find_beacon(data, width):
    for row in range(width+1):
        covers = covered(data, row)
        hole = uncovered(covers, width + 1)
        if hole:
            return hole[0], row


def point_is_covered(scanners, point):
    return any(manhattan_distance(s, point) <= radius for s, radius in scanners.items())


def scanner_perimeter(scanner, radius, width):
    perimeter = set()
    x, y = scanner

    def add_clamped(x, y):
        if 0 <= x <= width and 0 <= y <= width:
            perimeter.add((x, y))
    for r in range(radius+1):
        add_clamped(x + r, y + radius - r)
        add_clamped(x - r, y - radius + r)
        add_clamped(x - radius + r, y + r)
        add_clamped(x + radius - r, y - r)
    return perimeter


# slightly faster solution - checking points outside of
# the scanners 'circle' - runs in 12s under pypy3
def find_beacon2(data, width):
    scanners = {s: manhattan_distance(s, b) for s, b in data}
    for scanner, radius in scanners.items():
        for point in scanner_perimeter(scanner, radius + 1, width):
            if not point_is_covered(scanners, point):
                return point


def freq(x, y):
    return x * 4000000 + y


@timeit
def process(data, row, width):
    # part 1
    result = count_convered(data, row)
    print("part 1:", result)
    # part 2
    # hole, hole = find_beacon(data, width)
    # result = freq(*hole)
    hole = find_beacon2(data, width)
    result = freq(*hole)
    print("part 2:", result)


def parse_line(line):
    gen = map(int, re.findall('-?\d+', line))
    return list(zip(gen, gen))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file, row, width):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f), row, width)


if __name__ == "__main__":
    # main("test.txt", 10, 20)
    main("input.txt", 2000000, 4000000)
