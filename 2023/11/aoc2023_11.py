# https://adventofcode.com/2023/day/11
from pathlib import Path
from itertools import combinations
import time


def empty_rows(data):
    return {r for r, l in enumerate(data) if all(s == '.' for s in l)}


def galaxies(space):
    return [(x, y) for x, l in enumerate(space) for y, c in enumerate(l) if c == '#']


def universe_distance(p, q, rows, cols, expand=2):

    def add_expand(start, end, empty):
        s, e = (start, end) if start < end else (end, start)
        return sum(expand - 1 for r in empty if r in range(s + 1, e))

    x1, y1 = p
    x2, y2 = q
    md = abs(x1 - x2) + abs(y1 - y2)
    md += add_expand(x1, x2, rows)
    md += add_expand(y1, y2, cols)
    return md


def process(data):
    # part 1
    rows = empty_rows(data)
    cols = empty_rows(zip(*data))
    g = galaxies(data)
    result = sum(universe_distance(a, b, rows, cols)
                 for a, b in combinations(g, 2))
    print("part 1:", result)
    # part 2
    result = sum(universe_distance(a, b, rows, cols, 1000000)
                 for a, b in combinations(g, 2))
    print("part 2:", result)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


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
