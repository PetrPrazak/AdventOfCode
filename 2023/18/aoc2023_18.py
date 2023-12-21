# https://adventofcode.com/2023/day/18
from pathlib import Path
import time


def walk(data, part=1):
    x, y = 0, 0
    perimeter = 0
    polygon = []
    for d, l, c in data:
        polygon.append((x, y))
        if part == 2:
            l = int(c[:5], 16)
            d = "RDLU"[int(c[-1])]
        if d == 'R':
            x += l
        elif d == 'L':
            x -= l
        elif d == 'U':
            y -= l
        elif d == 'D':
            y += l
        else:
            raise ValueError(f"unknown direction {d}")
        perimeter += l

    return polygon, perimeter


# shoelace formula to calculate area of polygon
# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace(polygon):
    return abs(sum(x0*y1 - x1*y0 for (x0, y0), (x1, y1) in zip(polygon, polygon[1:] + [polygon[0]])) // 2)


# https://en.wikipedia.org/wiki/Pick%27s_theorem
# A = X + perimeter/2 - 1
# X = A - perimeter/2 + 1
# we want X + perimeter, so res = A + perimeter/2 + 1
def area(polygon, perimeter):
    return shoelace(polygon) + (perimeter // 2) + 1


def process(data):
    # part 1
    result = area(*walk(data))
    print("part 1:", result)
    # part 2
    result = area(*walk(data, part=2))
    print("part 2:", result)


def parse_line(line):
    d, l, c = line.split(' ')
    return d, int(l), c[2:-1]


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
